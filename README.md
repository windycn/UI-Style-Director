# UI Style Director

![UI Style Director icon](./assets/icon.png)

UI Style Director is a contract-first Codex plugin for UI design and frontend implementation.

It turns product requirements, content, screenshots, and existing code into a persistent UI style contract, then uses that contract to guide UI code changes, image draft prompts, style guides, and review.

Chinese usage guide: [README.zh-CN.md](./README.zh-CN.md)

## Version

Current version: `0.2.0`

This version includes both the workflow skill and an MCP server.

## Install In Codex

Clone the plugin into the local Codex plugin directory:

```bash
mkdir -p ~/plugins
git clone https://github.com/windycn/UI-Style-Director.git ~/plugins/ui-style-director
```

Register it in the local Codex marketplace:

```bash
mkdir -p ~/.agents/plugins
python3 - <<'PY'
import json
from pathlib import Path

marketplace = Path.home() / ".agents" / "plugins" / "marketplace.json"
entry = {
    "name": "ui-style-director",
    "source": {
        "source": "local",
        "path": "./plugins/ui-style-director"
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
    },
    "category": "Productivity"
}

if marketplace.exists():
    data = json.loads(marketplace.read_text())
else:
    data = {
        "name": "windy-local",
        "interface": {"displayName": "Windy Local Plugins"},
        "plugins": []
    }

plugins = [plugin for plugin in data.get("plugins", []) if plugin.get("name") != entry["name"]]
plugins.append(entry)
data["plugins"] = plugins
data.setdefault("interface", {}).setdefault("displayName", "Windy Local Plugins")
data.setdefault("name", "windy-local")
marketplace.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
PY
```

Restart Codex so it reloads `.codex-plugin/plugin.json`, `.mcp.json`, the skill, and the icon assets.

If you already have the plugin installed, update it with:

```bash
cd ~/plugins/ui-style-director
git pull
```

## Core Idea

Codex should not restyle UI from taste alone. It should first read or create:

```text
.ui-style/ui-style-contract.json
```

Then it should implement and review UI code against that contract.

## Built-In Presets

- `flat-white`
- `ink-black`
- `dense-saas`
- `soft-minimal`
- `editorial-product`
- `liquid-control`

## Useful Commands

Create a contract from a preset:

```bash
python3 ~/plugins/ui-style-director/scripts/build_style_contract.py \
  --preset flat-white \
  --out .ui-style/ui-style-contract.json
```

Create an image prompt from a contract:

```bash
python3 ~/plugins/ui-style-director/scripts/build_image_prompt.py \
  --contract .ui-style/ui-style-contract.json \
  --page "Dashboard" \
  --out .ui-style/image-prompts/dashboard.md
```

Run a lightweight style review:

```bash
python3 ~/plugins/ui-style-director/scripts/review_ui_against_contract.py \
  --contract .ui-style/ui-style-contract.json \
  path/to/page.tsx
```

## MCP Tools

The plugin also provides a local MCP server through `.mcp.json`.

Available tools:

- `list_presets`: list bundled UI style presets.
- `get_preset`: return full JSON for one preset.
- `build_contract`: create `.ui-style/ui-style-contract.json` from a preset.
- `build_image_prompt`: create a GPT-image-2-ready UI draft prompt from a contract.
- `review_ui`: run a lightweight style drift scan against a contract.

When using MCP tools against a project, pass the project directory as `base_dir` so relative paths resolve inside the project.

## Example Prompts

- Analyze this app and create a UI style contract.
- Apply the flat-white style to this frontend.
- Generate a UI draft prompt for this dashboard.
- Review this page against the UI style contract.
