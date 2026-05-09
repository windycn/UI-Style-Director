# UI Style Director 中文使用说明

![UI Style Director 图标](./assets/icon.png)

UI Style Director 是一个 **Contract-first UI 风格插件**。

它的核心目标不是单次生成一张漂亮 UI 图，而是让 Codex 在写 UI 代码前，先读取或生成一份稳定的 UI 风格契约：

```text
.ui-style/ui-style-contract.json
```

然后 Codex 基于这份契约去生成页面、修改组件、统一风格、生成草稿图、输出设计文档和审查 UI 代码。

## 适合做什么

- 给一个项目创建统一 UI 风格。
- 按某个预设风格重写页面。
- 根据需求文档、产品说明、代码或截图生成 UI 风格规范。
- 生成 GPT-image-2 可用的 UI 草稿图 prompt。
- 把自定义风格沉淀成可复用的 `ui-style-contract.json`。
- 审查现有 UI 代码是否偏离项目风格。
- 防止 Codex 多轮修改时 UI 风格漂移。

## 当前版本

当前版本是 `0.2.0`。

这一版已经从“Skill + 脚本版”升级成了 **Skill + MCP 工具版**：

- Skill 负责告诉 Codex 正确的 UI 风格工作流。
- MCP 工具负责把常用能力变成 Codex 可以直接调用的正式工具。
- 脚本仍然保留，作为 MCP 不可用时的备用方式。

## Codex 插件安装手册

### 1. 克隆插件到本地插件目录

推荐安装到：

```text
~/plugins/ui-style-director
```

命令：

```bash
mkdir -p ~/plugins
git clone https://github.com/windycn/UI-Style-Director.git ~/plugins/ui-style-director
```

如果你已经安装过，更新即可：

```bash
cd ~/plugins/ui-style-director
git pull
```

### 2. 注册到 Codex 本地 marketplace

Codex 通过下面这个文件发现本地插件：

```text
~/.agents/plugins/marketplace.json
```

可以用下面的命令自动添加或更新 `ui-style-director` 条目：

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

注册后的关键条目长这样：

```json
{
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
```

### 3. 重启 Codex

安装或更新后，重启 Codex。

重启后 Codex 会重新加载：

- `.codex-plugin/plugin.json`
- `.mcp.json`
- `skills/ui-style-director/SKILL.md`
- `assets/icon.png`
- `assets/logo.png`

### 4. 验证安装

在 Codex 里可以问：

```text
用 UI Style Director 列出所有内置 UI 风格 preset。
```

或者：

```text
用 UI Style Director 按 flat-white 创建这个项目的 ui-style-contract.json。
```

如果插件和 MCP 都加载成功，Codex 应该能使用 `list_presets`、`build_contract`、`build_image_prompt`、`review_ui` 等工具。

## 核心理念

普通 UI 生成流程容易变成：

```text
用户说一个风格
  -> Codex 临场发挥
  -> 这次好看
  -> 下次又换一种感觉
```

UI Style Director 的流程是：

```text
用户需求 / 文档 / 代码 / 截图
  -> 选择或生成风格
  -> 创建 ui-style-contract.json
  -> 生成草稿图或设计文档
  -> 按 contract 修改 UI 代码
  -> 按 contract review 风格一致性
```

所以它真正控制的是 **UI 代码风格**，不是只控制图片风格。

## 如何唤起插件

在 Codex 里可以直接这样说：

```text
用 UI Style Director 分析这个项目并创建 UI 风格契约。
```

或者：

```text
按 flat-white 风格改这个页面，先读取 ui-style-contract.json。
```

也可以描述目标，不一定要写插件名：

```text
帮我把这个前端统一成一个清爽的 SaaS 风格，并沉淀成可复用的 UI 风格规范。
```

如果 Codex 识别到你是在做 UI 风格、UI 代码、设计规范、视觉草稿或风格审查，它就应该使用这个插件的 skill。

## 内置风格预设

当前内置 6 个 preset：

### flat-white

清晰、克制、浅色、高可读性。

适合 SaaS、后台、生产力工具、开发者工具。

### ink-black

深色、高对比、专业、控制台感。

适合 AI 工具、开发者工具、监控面板、安全产品。

### dense-saas

高信息密度、强扫描效率、偏运营系统。

适合 CRM、ERP、管理后台、财务、库存、运营平台。

### soft-minimal

柔和、安静、内容友好。

适合知识管理、写作、笔记、个人效率、教育产品。

### editorial-product

有品牌表达和内容节奏。

适合官网、产品介绍页、案例页、报告型页面。

### liquid-control

现代系统感、轻玻璃、精致控件。

适合 macOS/iOS 气质工具、创意工具、AI 控制面板。这个风格要克制使用，避免玻璃效果泛滥。

## 常见使用方式

### 1. 给项目创建 UI 风格契约

对 Codex 说：

```text
用 UI Style Director 读取这个项目，推荐一个合适的 UI 风格，并生成 .ui-style/ui-style-contract.json。
```

Codex 应该做：

1. 读取项目结构、前端框架、样式系统和关键页面。
2. 判断产品类型、用户场景和信息密度。
3. 选择一个 preset 或生成自定义风格。
4. 创建 `.ui-style/ui-style-contract.json`。
5. 输出人类可读的 UI 风格说明。

### 2. 按预设风格改页面

对 Codex 说：

```text
用 UI Style Director 按 flat-white 风格改这个 Dashboard 页面。
```

Codex 应该做：

1. 查找 `.ui-style/ui-style-contract.json`。
2. 如果没有，就用 `flat-white` preset 创建 contract。
3. 分析目标页面代码。
4. 把 contract 映射到现有 CSS、Tailwind、组件库或主题系统。
5. 修改页面代码。
6. 按 contract review 结果。

### 3. 生成自定义风格

对 Codex 说：

```text
根据这个 PRD 和现有代码，帮我生成一个适合 AI 工作台的自定义 UI 风格，并沉淀成 contract。
```

Codex 应该做：

1. 读取 PRD、内容和代码。
2. 判断产品气质和使用场景。
3. 可能融合多个 preset，例如 `ink-black` + `dense-saas`。
4. 生成自定义 `styleId`。
5. 写入 `.ui-style/ui-style-contract.json`。

### 4. 生成 UI 草稿图 prompt

对 Codex 说：

```text
基于当前 ui-style-contract.json，生成一个 Dashboard UI 草稿图 prompt。
```

插件会优先生成 prompt：

```text
.ui-style/image-prompts/dashboard.md
```

如果当前 Codex 环境有图片生成能力，可以再基于这个 prompt 调用 GPT-image-2 生成 UI 草稿图。

注意：草稿图是视觉对齐样张，不是最终实现标准。最终实现仍然以 `ui-style-contract.json` 为准。

### 5. 审查 UI 是否跑偏

对 Codex 说：

```text
用 UI Style Director review 这个页面是否符合当前 UI 风格契约。
```

Codex 应该检查：

- 颜色 token 是否一致。
- 间距、圆角、阴影是否符合 contract。
- 布局密度是否符合产品场景。
- 是否出现 contract 禁止的设计手法。
- 表单、表格、按钮、导航等组件是否统一。
- 响应式和可访问性是否被破坏。

## 生成的项目文件

在被处理的项目里，建议产物统一放到：

```text
.ui-style/
  ui-style-contract.json
  UI_STYLE_GUIDE.md
  implementation-notes.md
  review-checklist.md
  image-prompts/
  drafts/
```

其中最重要的是：

```text
.ui-style/ui-style-contract.json
```

它是 Codex 后续写 UI 代码时应该优先读取的风格来源。

## 插件文件位置

插件安装在：

```text
~/plugins/ui-style-director
```

主 skill 在：

```text
~/plugins/ui-style-director/skills/ui-style-director/SKILL.md
```

预设风格在：

```text
~/plugins/ui-style-director/assets/presets/
```

脚本在：

```text
~/plugins/ui-style-director/scripts/
```

## 常用脚本命令

### 从 preset 创建 contract

```bash
python3 ~/plugins/ui-style-director/scripts/build_style_contract.py \
  --preset flat-white \
  --out .ui-style/ui-style-contract.json
```

### 生成 UI 草稿图 prompt

```bash
python3 ~/plugins/ui-style-director/scripts/build_image_prompt.py \
  --contract .ui-style/ui-style-contract.json \
  --page "Dashboard" \
  --out .ui-style/image-prompts/dashboard.md
```

### 对 UI 文件做基础风格检查

```bash
python3 ~/plugins/ui-style-director/scripts/review_ui_against_contract.py \
  --contract .ui-style/ui-style-contract.json \
  path/to/page.tsx
```

这个脚本只是轻量启发式检查，不能替代 Codex 对代码和界面的人工级 review。

## MCP 工具怎么用

插件现在包含一个 MCP server：

```text
~/plugins/ui-style-director/.mcp.json
```

Codex 重新加载插件后，会看到一组更正式的工具能力。

### list_presets

列出所有内置 UI 风格预设。

适合在你还不确定用什么风格时使用。

### get_preset

读取某个 preset 的完整 JSON。

例如读取 `flat-white`，查看它的颜色、布局、组件规则和禁止事项。

### build_contract

根据 preset 创建：

```text
.ui-style/ui-style-contract.json
```

这个是最重要的工具。它把风格从“感觉”变成可执行的项目契约。

### build_image_prompt

根据当前 contract 生成 UI 草稿图 prompt。

这个 prompt 可以给 GPT-image-2 使用，用来生成视觉对齐样张。

### review_ui

读取 contract，然后扫描指定 UI 文件，检查是否出现明显风格漂移。

它会提示一些可能问题，比如：

- 预设禁止渐变，但代码里出现 `bg-gradient`。
- 预设要求克制圆角，但代码里出现 `rounded-full`。
- 预设要求轻阴影，但代码里出现 `shadow-2xl`。

这个工具是启发式检查，不是最终审美判断。

## MCP 和脚本的区别

脚本版像这样用：

```bash
python3 ~/plugins/ui-style-director/scripts/build_style_contract.py \
  --preset flat-white \
  --out .ui-style/ui-style-contract.json
```

MCP 版是 Codex 直接调用工具，概念上像这样：

```text
build_contract({
  preset: "flat-white",
  base_dir: "/path/to/project",
  out_path: ".ui-style/ui-style-contract.json"
})
```

实际聊天时你不需要手写 JSON。你可以直接对 Codex 说：

```text
用 UI Style Director 的 MCP 工具，按 flat-white 创建这个项目的 ui-style-contract.json。
```

注意：MCP 工具读写项目文件时，应该传入项目目录 `base_dir`，这样 `.ui-style/` 会创建在你的项目里，而不是插件目录里。

## 推荐提示词

```text
用 UI Style Director 分析这个项目，并创建一个适合它的 UI 风格契约。
```

```text
按 dense-saas 风格重构这个管理后台页面，先生成或更新 ui-style-contract.json。
```

```text
读取当前 ui-style-contract.json，然后把这个组件改得更符合项目风格。
```

```text
基于这个 PRD 和当前代码生成一个自定义 UI 风格，并输出 UI_STYLE_GUIDE.md。
```

```text
用当前 UI 风格契约 review 这些前端改动，指出哪里风格跑偏。
```

## 使用建议

第一次用于一个项目时，先让 Codex 创建 contract，不要直接改页面。

推荐顺序：

```text
1. 分析项目
2. 创建 contract
3. 生成 UI style guide
4. 选择一个页面试改
5. review 页面是否符合 contract
6. 再扩大到更多页面
```

如果你已经有明确风格，可以直接指定 preset。

如果你只有模糊感觉，比如“高级一点”“更像专业工具”“更清爽”，让 Codex 先分析项目并推荐 preset。

## 当前能力说明

这一版包含：

- 主工作流 skill。
- MCP server。
- `list_presets` 工具。
- `get_preset` 工具。
- `build_contract` 工具。
- `build_image_prompt` 工具。
- `review_ui` 工具。
- 6 个风格 preset。
- contract 模板。
- style guide 模板。
- image prompt 模板。
- contract 生成脚本。
- image prompt 生成脚本。
- 基础 UI review 脚本。

后续还可以继续升级，比如增加 `merge_contract`、`generate_style_guide`、`apply_contract_to_tailwind`、`inspect_project_ui_stack` 等工具。
