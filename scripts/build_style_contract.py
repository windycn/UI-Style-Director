#!/usr/bin/env python3
"""Build a project UI style contract from a bundled preset."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = PLUGIN_ROOT / "assets" / "presets"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", required=True, help="Preset id, for example flat-white.")
    parser.add_argument("--out", default=".ui-style/ui-style-contract.json", help="Output JSON path.")
    parser.add_argument("--project", default="", help="Optional project name.")
    parser.add_argument("--product-type", default="", help="Optional product type.")
    parser.add_argument("--audience", default="", help="Optional audience.")
    parser.add_argument("--primary-job", action="append", default=[], help="Primary user job. Repeatable.")
    parser.add_argument("--content-density", default="", help="Optional density override.")
    parser.add_argument("--notes", default="", help="Optional source requirement notes.")
    args = parser.parse_args()

    preset_path = PRESETS_DIR / f"{args.preset}.json"
    if not preset_path.exists():
        available = ", ".join(sorted(path.stem for path in PRESETS_DIR.glob("*.json")))
        raise SystemExit(f"Unknown preset '{args.preset}'. Available presets: {available}")

    contract = load_json(preset_path)
    contract.setdefault("productContext", {})
    contract["productContext"].update(
        {
            "project": args.project,
            "productType": args.product_type,
            "audience": args.audience,
            "primaryJobs": args.primary_job,
            "contentDensity": args.content_density or contract.get("visualPosture", {}).get("density", ""),
        }
    )
    contract["source"] = {
        "kind": "preset",
        "preset": args.preset,
        "notes": args.notes,
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
    }

    write_json(Path(args.out), contract)
    print(f"Wrote UI style contract: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
