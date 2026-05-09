#!/usr/bin/env python3
"""MCP server for UI Style Director.

This server intentionally avoids third-party dependencies so the plugin can run
immediately after installation.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "ui-style-director"
SERVER_VERSION = "0.2.0"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = PLUGIN_ROOT / "assets" / "presets"


class ToolError(Exception):
    """User-facing tool error."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ToolError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ToolError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ToolError(f"Expected JSON object in {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def base_path(base_dir: str | None = None) -> Path:
    base = base_dir or os.environ.get("CODEX_CWD") or os.environ.get("PWD") or "."
    return Path(base).expanduser().resolve()


def resolve_output(path_value: str, base_dir: str | None = None) -> Path:
    path = Path(path_value).expanduser()
    if path.is_absolute():
        return path
    return (base_path(base_dir) / path).resolve()


def available_preset_paths() -> list[Path]:
    return sorted(PRESETS_DIR.glob("*.json"))


def load_preset(preset: str) -> dict[str, Any]:
    preset_path = PRESETS_DIR / f"{preset}.json"
    if not preset_path.exists():
        available = ", ".join(path.stem for path in available_preset_paths())
        raise ToolError(f"Unknown preset '{preset}'. Available presets: {available}")
    return load_json(preset_path)


def compact_preset(preset: dict[str, Any]) -> dict[str, Any]:
    return {
        "styleId": preset.get("styleId", ""),
        "styleName": preset.get("styleName", ""),
        "intent": preset.get("intent", ""),
        "bestFor": preset.get("bestFor", []),
        "density": preset.get("visualPosture", {}).get("density", ""),
        "tone": preset.get("visualPosture", {}).get("tone", ""),
    }


def list_presets(arguments: dict[str, Any]) -> dict[str, Any]:
    include_details = bool(arguments.get("include_details", False))
    presets = [load_json(path) for path in available_preset_paths()]
    return {
        "presets": presets if include_details else [compact_preset(preset) for preset in presets],
        "count": len(presets),
    }


def get_preset(arguments: dict[str, Any]) -> dict[str, Any]:
    preset = str(arguments.get("preset", "")).strip()
    if not preset:
        raise ToolError("Missing required argument: preset")
    return load_preset(preset)


def build_contract(arguments: dict[str, Any]) -> dict[str, Any]:
    preset_id = str(arguments.get("preset", "")).strip()
    if not preset_id:
        raise ToolError("Missing required argument: preset")

    out_path = resolve_output(
        str(arguments.get("out_path") or ".ui-style/ui-style-contract.json"),
        arguments.get("base_dir"),
    )
    contract = load_preset(preset_id)
    primary_jobs = arguments.get("primary_jobs", [])
    if isinstance(primary_jobs, str):
        primary_jobs = [primary_jobs]
    if not isinstance(primary_jobs, list):
        raise ToolError("primary_jobs must be a string or list of strings")

    contract.setdefault("productContext", {})
    product_context = {
        "project": arguments.get("project", ""),
        "productType": arguments.get("product_type", ""),
        "audience": arguments.get("audience", ""),
        "primaryJobs": primary_jobs,
        "contentDensity": arguments.get("content_density")
        or contract.get("visualPosture", {}).get("density", ""),
    }
    contract["productContext"].update(product_context)
    contract["source"] = {
        "kind": "preset",
        "preset": preset_id,
        "notes": arguments.get("notes", ""),
        "generatedBy": SERVER_NAME,
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    }

    write_json(out_path, contract)
    return {
        "path": str(out_path),
        "styleId": contract.get("styleId", preset_id),
        "styleName": contract.get("styleName", preset_id),
        "message": "UI style contract written.",
    }


def lines(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    if isinstance(value, dict):
        rendered: list[str] = []
        for key, val in value.items():
            if isinstance(val, list):
                rendered.append(f"- {key}: " + "; ".join(str(item) for item in val))
            else:
                rendered.append(f"- {key}: {val}")
        return "\n".join(rendered)
    return str(value or "")


def build_image_prompt(arguments: dict[str, Any]) -> dict[str, Any]:
    page = str(arguments.get("page", "")).strip()
    if not page:
        raise ToolError("Missing required argument: page")

    contract_path = resolve_output(
        str(arguments.get("contract_path") or ".ui-style/ui-style-contract.json"),
        arguments.get("base_dir"),
    )
    contract = load_json(contract_path)
    style_name = contract.get("styleName") or contract.get("styleId") or "custom style"
    prompt = f"""Create a high-fidelity UI draft for: {page}

Style: {style_name}
Intent: {contract.get("intent", "")}

Visual direction:
{contract.get("imagePromptStyle", "")}

Layout rules:
{lines(contract.get("layoutRules", []))}

Component rules:
{lines(contract.get("componentRules", {}))}

Avoid:
{lines(contract.get("avoid", []))}

The output should look like a real usable product screen. Do not make a generic marketing mockup unless the requested page is explicitly a landing page. Keep text legible, hierarchy clear, and controls implementable in code.
"""

    out_path_value = arguments.get("out_path")
    if out_path_value:
        out_path = resolve_output(str(out_path_value), arguments.get("base_dir"))
        write_text(out_path, prompt)
        path: str | None = str(out_path)
    else:
        path = None

    return {
        "prompt": prompt,
        "path": path,
        "contractPath": str(contract_path),
        "styleId": contract.get("styleId", ""),
    }


DRIFT_PATTERNS = {
    "decorative gradients": ["bg-gradient", "linear-gradient", "radial-gradient"],
    "large radius": ["rounded-3xl", "rounded-full", "border-radius: 999"],
    "heavy shadow": ["shadow-2xl", "shadow-xl", "box-shadow"],
    "blur/glass": ["backdrop-blur", "blur(", "rgba("],
    "low contrast gray": ["text-gray-300", "text-slate-300", "color: #9CA3AF"],
}


def scan_file(path: Path) -> list[dict[str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(errors="ignore")

    findings: list[dict[str, str]] = []
    for label, patterns in DRIFT_PATTERNS.items():
        for pattern in patterns:
            if pattern in text:
                findings.append(
                    {
                        "file": str(path),
                        "kind": label,
                        "pattern": pattern,
                        "message": f"Possible {label} via '{pattern}'. Review against the contract.",
                    }
                )
                break
    return findings


def review_ui(arguments: dict[str, Any]) -> dict[str, Any]:
    contract_path = resolve_output(
        str(arguments.get("contract_path") or ".ui-style/ui-style-contract.json"),
        arguments.get("base_dir"),
    )
    contract = load_json(contract_path)
    files = arguments.get("files", [])
    if isinstance(files, str):
        files = [files]
    if not isinstance(files, list) or not files:
        raise ToolError("Missing required argument: files")

    findings: list[dict[str, str]] = []
    missing_files: list[str] = []
    for file_value in files:
        file_path = resolve_output(str(file_value), arguments.get("base_dir"))
        if not file_path.exists():
            missing_files.append(str(file_path))
            continue
        findings.extend(scan_file(file_path))

    return {
        "contractPath": str(contract_path),
        "styleId": contract.get("styleId", ""),
        "avoid": contract.get("avoid", []),
        "findings": findings,
        "missingFiles": missing_files,
        "summary": (
            "No obvious heuristic drift patterns found. Manual review is still required."
            if not findings and not missing_files
            else "Review findings manually against the contract."
        ),
    }


TOOLS = {
    "list_presets": {
        "description": "List bundled UI style presets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "include_details": {
                    "type": "boolean",
                    "description": "Return full preset JSON instead of compact summaries.",
                    "default": False,
                }
            },
            "additionalProperties": False,
        },
        "handler": list_presets,
    },
    "get_preset": {
        "description": "Return the full JSON for a named UI style preset.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "preset": {
                    "type": "string",
                    "description": "Preset id, for example flat-white or ink-black.",
                }
            },
            "required": ["preset"],
            "additionalProperties": False,
        },
        "handler": get_preset,
    },
    "build_contract": {
        "description": "Build a .ui-style/ui-style-contract.json file from a bundled preset.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "preset": {"type": "string", "description": "Preset id."},
                "base_dir": {
                    "type": "string",
                    "description": "Project directory used to resolve relative paths.",
                },
                "out_path": {
                    "type": "string",
                    "description": "Output path, relative to base_dir unless absolute.",
                    "default": ".ui-style/ui-style-contract.json",
                },
                "project": {"type": "string"},
                "product_type": {"type": "string"},
                "audience": {"type": "string"},
                "primary_jobs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Primary user jobs.",
                },
                "content_density": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["preset"],
            "additionalProperties": False,
        },
        "handler": build_contract,
    },
    "build_image_prompt": {
        "description": "Build a GPT-image-2 UI draft prompt from a style contract.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "string", "description": "Page or feature goal."},
                "base_dir": {
                    "type": "string",
                    "description": "Project directory used to resolve relative paths.",
                },
                "contract_path": {
                    "type": "string",
                    "description": "Contract path, relative to base_dir unless absolute.",
                    "default": ".ui-style/ui-style-contract.json",
                },
                "out_path": {
                    "type": "string",
                    "description": "Optional output prompt path.",
                },
            },
            "required": ["page"],
            "additionalProperties": False,
        },
        "handler": build_image_prompt,
    },
    "review_ui": {
        "description": "Run a lightweight heuristic UI style review against a contract.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_dir": {
                    "type": "string",
                    "description": "Project directory used to resolve relative paths.",
                },
                "contract_path": {
                    "type": "string",
                    "description": "Contract path, relative to base_dir unless absolute.",
                    "default": ".ui-style/ui-style-contract.json",
                },
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "UI files to scan, relative to base_dir unless absolute.",
                },
            },
            "required": ["files"],
            "additionalProperties": False,
        },
        "handler": review_ui,
    },
}


def read_message() -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if line == b"":
            return None
        if line in (b"\r\n", b"\n"):
            break
        decoded = line.decode("ascii", errors="replace").strip()
        if ":" in decoded:
            key, value = decoded.split(":", 1)
            headers[key.lower()] = value.strip()

    length_raw = headers.get("content-length")
    if not length_raw:
        return None
    body = sys.stdin.buffer.read(int(length_raw))
    if not body:
        return None
    return json.loads(body.decode("utf-8"))


def write_message(message: dict[str, Any]) -> None:
    body = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def result_response(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def error_response(message_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}


def tool_result(data: Any, is_error: bool = False) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": data if isinstance(data, str) else json.dumps(data, indent=2, ensure_ascii=False),
            }
        ],
        "isError": is_error,
    }


def handle_request(message: dict[str, Any]) -> dict[str, Any] | None:
    message_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if message_id is None:
        return None

    if method == "initialize":
        return result_response(
            message_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )

    if method == "ping":
        return result_response(message_id, {})

    if method == "tools/list":
        tools = []
        for name, tool in TOOLS.items():
            tools.append(
                {
                    "name": name,
                    "description": tool["description"],
                    "inputSchema": tool["inputSchema"],
                }
            )
        return result_response(message_id, {"tools": tools})

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments") or {}
        if tool_name not in TOOLS:
            return result_response(message_id, tool_result(f"Unknown tool: {tool_name}", True))
        try:
            data = TOOLS[tool_name]["handler"](arguments)
        except ToolError as exc:
            return result_response(message_id, tool_result(str(exc), True))
        except Exception as exc:  # Keep the MCP server alive and surface context.
            return result_response(message_id, tool_result(f"Tool failed: {exc}", True))
        return result_response(message_id, tool_result(data))

    return error_response(message_id, -32601, f"Method not found: {method}")


def main() -> int:
    while True:
        message = read_message()
        if message is None:
            return 0
        response = handle_request(message)
        if response is not None:
            write_message(response)


if __name__ == "__main__":
    raise SystemExit(main())
