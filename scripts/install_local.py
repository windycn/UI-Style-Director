#!/usr/bin/env python3
"""Register UI Style Director in the local Codex plugin marketplace."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PLUGIN_NAME = "ui-style-director"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
EXPECTED_PLUGIN_PATH = HOME / "plugins" / PLUGIN_NAME
MARKETPLACE_PATH = HOME / ".agents" / "plugins" / "marketplace.json"


def load_marketplace(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "name": "windy-local",
            "interface": {"displayName": "Windy Local Plugins"},
            "plugins": [],
        }
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid marketplace JSON: {path}")
    data.setdefault("name", "windy-local")
    data.setdefault("interface", {}).setdefault("displayName", "Windy Local Plugins")
    data.setdefault("plugins", [])
    return data


def ensure_expected_plugin_path() -> None:
    if PLUGIN_ROOT == EXPECTED_PLUGIN_PATH:
        return

    EXPECTED_PLUGIN_PATH.parent.mkdir(parents=True, exist_ok=True)
    if EXPECTED_PLUGIN_PATH.exists():
        raise SystemExit(
            "Plugin is not located at ~/plugins/ui-style-director, and that path already exists. "
            "Install with: git clone https://github.com/windycn/UI-Style-Director.git ~/plugins/ui-style-director"
        )

    EXPECTED_PLUGIN_PATH.symlink_to(PLUGIN_ROOT, target_is_directory=True)
    print(f"Created symlink: {EXPECTED_PLUGIN_PATH} -> {PLUGIN_ROOT}")


def main() -> int:
    ensure_expected_plugin_path()
    MARKETPLACE_PATH.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }

    data = load_marketplace(MARKETPLACE_PATH)
    plugins = [plugin for plugin in data["plugins"] if plugin.get("name") != PLUGIN_NAME]
    plugins.append(entry)
    data["plugins"] = plugins

    with MARKETPLACE_PATH.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Registered {PLUGIN_NAME} in {MARKETPLACE_PATH}")
    print("Restart Codex to load the plugin, MCP tools, and icon.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
