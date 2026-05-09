#!/usr/bin/env python3
"""Run a lightweight heuristic UI review against a style contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DRIFT_PATTERNS = {
    "decorative gradients": ["bg-gradient", "linear-gradient", "radial-gradient"],
    "large radius": ["rounded-3xl", "rounded-full", "border-radius: 999"],
    "heavy shadow": ["shadow-2xl", "shadow-xl", "box-shadow"],
    "blur/glass": ["backdrop-blur", "blur(", "rgba("],
    "low contrast gray": ["text-gray-300", "text-slate-300", "color: #9CA3AF"],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def scan_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(errors="ignore")

    findings: list[str] = []
    for label, patterns in DRIFT_PATTERNS.items():
        for pattern in patterns:
            if pattern in text:
                findings.append(f"{path}: possible {label} via '{pattern}'")
                break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=".ui-style/ui-style-contract.json", help="Contract JSON path.")
    parser.add_argument("files", nargs="+", help="UI files to scan.")
    args = parser.parse_args()

    contract = load_json(Path(args.contract))
    style_id = contract.get("styleId", "unknown")
    avoid = contract.get("avoid", [])

    print(f"UI style review")
    print(f"Contract: {args.contract}")
    print(f"Style: {style_id}")
    if avoid:
        print("Avoid rules:")
        for item in avoid:
            print(f"- {item}")
    print("")

    findings: list[str] = []
    for file_name in args.files:
        path = Path(file_name)
        if not path.exists():
            findings.append(f"{path}: file not found")
            continue
        findings.extend(scan_file(path))

    if findings:
        print("Heuristic findings:")
        for finding in findings:
            print(f"- {finding}")
        print("")
        print("Review these manually against the contract before delivery.")
    else:
        print("No obvious heuristic drift patterns found. Manual review is still required.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
