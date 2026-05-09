---
name: ui-style-director
description: Use when the user asks to design, restyle, implement, generate, review, stabilize, or apply UI style/code. Creates and applies contract-first UI style systems from requirements, content, code, screenshots, visual drafts, and style presets.
---

# UI Style Director

## Core Principle

Use contract-first UI generation.

Before creating, restyling, or reviewing UI code, look for a project style contract at:

```text
.ui-style/ui-style-contract.json
```

If the contract exists, treat it as the primary design source. If it does not exist, create one from the user request, project context, and the closest preset in `assets/presets/`.

The plugin is not mainly an image generator. Images are alignment artifacts. The durable output is a style contract that can guide code changes and future review.

## When To Use

Use this skill when the user asks for any of these:

- Apply a named UI style to a page or app.
- Create a custom UI style from requirements, documents, content, screenshots, or code.
- Generate UI draft images as a visual direction.
- Produce a UI style guide or design-system guidance.
- Review UI code for consistency with an existing style.
- Prevent UI style drift across repeated Codex edits.

## Required Workflow

1. Inspect the project context.
   - Find the frontend stack, component library, CSS system, theme files, and existing UI conventions.
   - Read relevant requirements, Markdown, screenshots, or code before choosing a style.

2. Resolve the style source in this order:
   - The user's explicit current request.
   - Page-level override, if present.
   - `.ui-style/ui-style-contract.json`.
   - A named preset from `assets/presets/`.
   - A new inferred custom style.

3. Create or update the contract before changing UI code.
   - Persist project artifacts under `.ui-style/` unless the user asks otherwise.
   - Prefer editing an existing contract over replacing it.
   - Keep the contract concrete enough to map into code.

4. Map the contract to the actual codebase.
   - Use the project's existing token system, Tailwind config, CSS variables, theme files, component wrappers, or SwiftUI modifiers.
   - Avoid inventing a parallel design system unless the project has none.

5. Implement UI changes with scoped edits.
   - Keep product workflows usable.
   - Preserve accessibility and responsive behavior.
   - Do not add decorative effects that are not in the contract.

6. Review the result against the contract.
   - Check tokens, spacing, density, typography, layout, components, states, and forbidden patterns.
   - Fix drift before handing work back to the user.

## Image Draft Workflow

Use image generation only when it helps align visual direction.

1. Build a prompt from the contract and page goal.
2. Generate one or more draft images if an image tool is available.
3. Treat the image as a visual sample, not as the final implementation.
4. Refine the contract if the image reveals a better or clearer direction.
5. Implement from the contract, not by copying image pixels blindly.

If no image generation tool is available, write the image prompt to `.ui-style/image-prompts/`.

## Contract Requirements

A useful contract must include:

- `styleId` and `intent`.
- Product and audience assumptions.
- Density, layout, and interaction posture.
- Design tokens for color, type, spacing, radius, shadow, and borders.
- Component rules for buttons, forms, cards, tables, navigation, modals, charts, and states.
- Accessibility rules.
- Explicit `avoid` rules.
- `codeMapping` for the current stack.

Use `references/style-contract-schema.md` as the target shape.

## Preset Guidance

Built-in presets:

- `flat-white`: clear, restrained, light SaaS and productivity UI.
- `ink-black`: dark, high-contrast, professional control surfaces.
- `dense-saas`: high-density operational interfaces.
- `soft-minimal`: calm, content-friendly personal or knowledge tools.
- `editorial-product`: branded product and narrative pages.
- `liquid-control`: modern system-feeling tools with restrained glass.

Presets are starting points. Adjust them to match the project's actual audience, data density, and implementation stack.

## MCP Tools

When the UI Style Director MCP server is available, prefer its tools over shell scripts for structured plugin operations:

- `list_presets`: list bundled UI style presets.
- `get_preset`: read the full JSON for a named preset.
- `build_contract`: create `.ui-style/ui-style-contract.json` from a preset.
- `build_image_prompt`: create a GPT-image-2-ready prompt from a contract.
- `merge_contract`: merge a preset, an existing contract, and explicit overrides.
- `generate_style_guide`: generate `.ui-style/UI_STYLE_GUIDE.md` from a contract.
- `apply_contract_to_tailwind`: write Tailwind token mapping artifacts.
- `review_ui`: run a lightweight contract-based UI drift scan.
- `inspect_project_ui_stack`: detect frontend framework, styling system, component libraries, and useful UI files.

For tools that write or read project files, pass `base_dir` as the absolute path to the target project directory so relative paths resolve into the project, not the plugin directory.

## Script Helpers

If MCP tools are not available yet, use these scripts:

Use these scripts when useful:

```bash
python3 ~/plugins/ui-style-director/scripts/build_style_contract.py --preset flat-white --out .ui-style/ui-style-contract.json
python3 ~/plugins/ui-style-director/scripts/build_image_prompt.py --contract .ui-style/ui-style-contract.json --page "Dashboard" --out .ui-style/image-prompts/dashboard.md
python3 ~/plugins/ui-style-director/scripts/review_ui_against_contract.py --contract .ui-style/ui-style-contract.json path/to/ui-file.tsx
```

The scripts are helpers, not replacements for reading the codebase carefully.

## Output Standards

For implementation tasks, finish with:

- What contract was used or created.
- Which UI files changed.
- What verification or review was performed.
- Any remaining visual risk.

For design-only tasks, finish with the contract path, guide path, and image prompt or generated image path.
