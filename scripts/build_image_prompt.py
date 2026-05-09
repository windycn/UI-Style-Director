#!/usr/bin/env python3
"""Build a UI draft image prompt from a UI style contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def as_lines(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"- {key}: {val}" for key, val in value.items())
    return str(value or "")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=".ui-style/ui-style-contract.json", help="Contract JSON path.")
    parser.add_argument("--page", required=True, help="Page or feature goal.")
    parser.add_argument("--out", default="", help="Optional prompt output path.")
    args = parser.parse_args()

    contract = load_json(Path(args.contract))
    style_name = contract.get("styleName") or contract.get("styleId") or "custom style"
    intent = contract.get("intent", "")
    image_style = contract.get("imagePromptStyle", "")
    layout_rules = as_lines(contract.get("layoutRules", []))
    component_rules = as_lines(contract.get("componentRules", {}))
    avoid = as_lines(contract.get("avoid", []))

    prompt = f"""Create a high-fidelity UI draft for: {args.page}

Style: {style_name}
Intent: {intent}

Visual direction:
{image_style}

Layout rules:
{layout_rules}

Component rules:
{component_rules}

Avoid:
{avoid}

The output should look like a real usable product screen. Do not make a generic marketing mockup unless the requested page is explicitly a landing page. Keep text legible, hierarchy clear, and controls implementable in code.
"""

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt, encoding="utf-8")
        print(f"Wrote image prompt: {args.out}")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
