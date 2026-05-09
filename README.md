<p align="center">
  <img src="./assets/icon.png" alt="UI Style Director" width="128" />
</p>

<h1 align="center">UI Style Director</h1>

<p align="center">
  Contract-first UI style control for Codex.
</p>

<p align="center">
  <a href="./README.zh-CN.md">中文说明</a>
  ·
  <a href="#install-in-codex">Install</a>
  ·
  <a href="#mcp-tools">MCP Tools</a>
</p>

UI Style Director turns requirements, content, screenshots, and existing frontend code into a persistent UI style contract. Codex can then use that contract to generate UI drafts, guide implementation, and review UI code for style drift.

Current version: `0.3.0`

## Why It Exists

Without a durable style source, UI generation tends to drift between sessions. This plugin makes Codex design with memory:

```text
requirements / code / screenshots
  -> choose or create a style
  -> write .ui-style/ui-style-contract.json
  -> generate image prompts or style docs
  -> implement UI code from the contract
  -> review code against the contract
```

The image draft is only an alignment artifact. The durable source of truth is:

```text
.ui-style/ui-style-contract.json
```

## Install In Codex

Install with three commands:

```bash
mkdir -p ~/plugins
git clone https://github.com/windycn/UI-Style-Director.git ~/plugins/ui-style-director
python3 ~/plugins/ui-style-director/scripts/install_local.py
```

The installer updates `~/.agents/plugins/marketplace.json` while preserving existing plugin entries. Restart Codex after installation so it reloads the plugin manifest, skill, MCP server, and icon assets.

To update an existing install:

```bash
cd ~/plugins/ui-style-director
git pull
python3 scripts/install_local.py
```

## How To Call It In Codex

You can call the plugin by name:

```text
Use UI Style Director to analyze this app and create a UI style contract.
```

You can also describe the UI task naturally. The skill is meant to activate for UI style, frontend styling, design-system guidance, image draft prompts, and style review work.

| Goal | Prompt |
| --- | --- |
| Create a project style contract | `Use UI Style Director to analyze this project and create .ui-style/ui-style-contract.json.` |
| Apply a preset | `Apply the flat-white style to this frontend. Read or create ui-style-contract.json first.` |
| Create a custom style | `Use this PRD and codebase to create a custom AI workspace UI style contract.` |
| Generate an image prompt | `Based on the current UI style contract, create a Dashboard UI draft prompt for GPT-image-2.` |
| Generate a style guide | `Generate UI_STYLE_GUIDE.md from the current UI style contract.` |
| Tailwind implementation | `Apply this UI style contract to Tailwind and generate token mapping artifacts.` |
| Inspect UI stack | `Inspect this project UI stack before creating the style contract.` |
| Review style drift | `Review this page against the current UI style contract and point out drift.` |

Expected behavior:

```text
1. Read or create .ui-style/ui-style-contract.json
2. Map the contract to the existing UI stack
3. Implement or generate prompts from the contract
4. Review touched UI against the contract
```

## Quick Examples

```text
Use UI Style Director to list the built-in presets.
```

```text
Use UI Style Director to build a dense-saas contract for this admin app.
```

```text
Use UI Style Director to generate an image prompt for the billing settings page.
```

## Built-In Presets

| Preset | Best for | Tone |
| --- | --- | --- |
| `flat-white` | SaaS, dashboards, productivity tools | Clear, light, restrained |
| `ink-black` | AI tools, developer tools, monitoring | Dark, focused, technical |
| `dense-saas` | CRM, ERP, admin, operations | Compact, efficient, operational |
| `soft-minimal` | Notes, writing, knowledge tools | Calm, content-friendly |
| `editorial-product` | Product pages, reports, launches | Branded, narrative, polished |
| `liquid-control` | macOS-style tools, control panels | Modern, tactile, restrained glass |

## MCP Tools

The plugin provides a local MCP server through [.mcp.json](./.mcp.json).

| Tool | Purpose |
| --- | --- |
| `list_presets` | List bundled UI style presets. |
| `get_preset` | Return the full JSON for one preset. |
| `build_contract` | Create `.ui-style/ui-style-contract.json` from a preset. |
| `build_image_prompt` | Create a GPT-image-2-ready UI draft prompt from a contract. |
| `merge_contract` | Merge a preset, existing contract, and explicit overrides. |
| `generate_style_guide` | Generate `.ui-style/UI_STYLE_GUIDE.md` from a contract. |
| `apply_contract_to_tailwind` | Write CSS variables, a Tailwind theme snippet, and implementation notes. |
| `review_ui` | Run a lightweight style drift scan against a contract. |
| `inspect_project_ui_stack` | Detect frontend framework, styling stack, component libraries, and useful UI files. |

When a tool reads or writes project files, pass the target project path as `base_dir` so relative paths resolve inside that project.

## CLI Fallback

If MCP tools are not loaded, the same core operations are available as local scripts.

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

## Project Artifacts

For each target project, UI Style Director writes durable style artifacts under:

```text
.ui-style/
  ui-style-contract.json
  UI_STYLE_GUIDE.md
  implementation-notes.md
  review-checklist.md
  ui-style-tokens.css
  tailwind-theme-snippet.cjs
  tailwind-implementation-notes.md
  image-prompts/
  drafts/
```

## Repository Layout

```text
.codex-plugin/plugin.json
.mcp.json
skills/ui-style-director/SKILL.md
assets/presets/
assets/templates/
scripts/
```

## License

MIT
