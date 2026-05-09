<p align="center">
  <img src="./assets/icon.png" alt="UI Style Director 图标" width="128" />
</p>

<h1 align="center">UI Style Director</h1>

<p align="center">
  Contract-first UI 风格控制插件，让 Codex 写 UI 不再风格漂移。
</p>

<p align="center">
  <a href="./README.md">English</a>
  ·
  <a href="#codex-插件安装手册">安装</a>
  ·
  <a href="#mcp-工具">MCP 工具</a>
</p>

UI Style Director 是一个 **Contract-first UI 风格插件**。它会把需求文档、产品内容、截图和现有前端代码转成一份持续存在的 UI 风格契约，然后让 Codex 基于这份契约生成草稿图、指导实现、审查 UI 代码。

当前版本：`0.3.0`

## 核心理念

普通 UI 生成很容易变成：

```text
用户说一个风格
  -> Codex 临场发挥
  -> 这次好看
  -> 下次又换一种感觉
```

UI Style Director 的流程是：

```text
需求 / 文档 / 代码 / 截图
  -> 选择或生成风格
  -> 创建 .ui-style/ui-style-contract.json
  -> 生成草稿图 prompt 或设计文档
  -> 按 contract 修改 UI 代码
  -> 按 contract review 风格一致性
```

最重要的产物是：

```text
.ui-style/ui-style-contract.json
```

草稿图只是视觉对齐样张，真正控制 UI 代码风格的是这份 contract。

## 适合做什么

- 给项目创建统一 UI 风格。
- 按预设风格重写页面。
- 根据 PRD、Markdown、代码或截图生成 UI 风格规范。
- 生成 GPT-image-2 可用的 UI 草稿图 prompt。
- 把自定义风格沉淀成可复用的 `ui-style-contract.json`。
- 审查现有 UI 代码是否偏离项目风格。
- 防止 Codex 多轮修改时 UI 风格漂移。

## Codex 插件安装手册

### 1. 三步安装

```bash
mkdir -p ~/plugins
git clone https://github.com/windycn/UI-Style-Director.git ~/plugins/ui-style-director
python3 ~/plugins/ui-style-director/scripts/install_local.py
```

安装脚本会自动更新：

```text
~/.agents/plugins/marketplace.json
```

它会保留你已有的其他插件条目，只添加或更新 `ui-style-director`。

### 2. 更新插件

如果已经安装过：

```bash
cd ~/plugins/ui-style-director
git pull
python3 scripts/install_local.py
```

### 3. 重启 Codex

安装或更新后重启 Codex，让它重新加载：

- `.codex-plugin/plugin.json`
- `.mcp.json`
- `skills/ui-style-director/SKILL.md`
- `assets/icon.png`
- `assets/logo.png`

### 4. 验证安装

在 Codex 里可以说：

```text
用 UI Style Director 列出所有内置 UI 风格 preset。
```

或者：

```text
用 UI Style Director 按 flat-white 创建这个项目的 ui-style-contract.json。
```

如果插件和 MCP 都加载成功，Codex 应该能使用 `list_presets`、`build_contract`、`build_image_prompt`、`review_ui` 等工具。

## 怎么调用插件

最稳的方式是直接点名：

```text
用 UI Style Director 分析这个项目并创建 UI 风格契约。
```

也可以不用点名，只描述 UI 风格任务：

```text
帮我把这个前端统一成清爽的 SaaS 风格，并沉淀成可复用的 UI 风格规范。
```

适合触发插件的任务包括：

| 目标 | 推荐提示词 |
| --- | --- |
| 创建项目风格契约 | `用 UI Style Director 分析这个项目，并创建 .ui-style/ui-style-contract.json。` |
| 应用预设风格 | `按 flat-white 风格改这个页面，先读取或创建 ui-style-contract.json。` |
| 生成自定义风格 | `根据这个 PRD 和现有代码，生成一个适合 AI 工作台的自定义 UI 风格。` |
| 生成图片 prompt | `基于当前 UI 风格契约，生成一个 Dashboard UI 草稿图 prompt。` |
| 生成风格文档 | `基于当前 UI 风格契约，生成 UI_STYLE_GUIDE.md。` |
| 落地到 Tailwind | `把当前 UI 风格契约转换成 Tailwind token 映射产物。` |
| 探测 UI 技术栈 | `先 inspect 这个项目的 UI stack，再创建风格契约。` |
| 审查风格漂移 | `用当前 UI 风格契约 review 这个页面，指出哪里风格跑偏。` |

插件的理想执行顺序是：

```text
1. 读取或创建 .ui-style/ui-style-contract.json
2. 把 contract 映射到当前项目的 UI 技术栈
3. 基于 contract 改 UI、生成 prompt 或输出设计文档
4. 按 contract review 被改动的 UI
```

## 如何使用

### 创建项目风格契约

```text
用 UI Style Director 读取这个项目，推荐一个合适的 UI 风格，并生成 .ui-style/ui-style-contract.json。
```

Codex 应该读取项目结构、前端框架、样式系统和关键页面，再选择 preset 或生成自定义风格。

### 按预设风格改页面

```text
用 UI Style Director 按 flat-white 风格改这个 Dashboard 页面。
```

Codex 应该先查找 `.ui-style/ui-style-contract.json`。如果没有，就用 `flat-white` 创建 contract，再映射到现有 CSS、Tailwind、组件库或主题系统。

### 生成自定义风格

```text
根据这个 PRD 和现有代码，帮我生成一个适合 AI 工作台的自定义 UI 风格，并沉淀成 contract。
```

Codex 可以融合多个 preset，例如 `ink-black` + `dense-saas`，再生成自定义 `styleId`。

### 生成 UI 草稿图 prompt

```text
基于当前 ui-style-contract.json，生成一个 Dashboard UI 草稿图 prompt。
```

默认产物建议放到：

```text
.ui-style/image-prompts/dashboard.md
```

如果当前 Codex 环境有图片生成能力，可以再基于这个 prompt 调用 GPT-image-2。最终实现仍然以 contract 为准。

### 审查 UI 是否跑偏

```text
用 UI Style Director review 这个页面是否符合当前 UI 风格契约。
```

Codex 应该检查颜色 token、间距、圆角、阴影、布局密度、组件规则、响应式、可访问性，以及 contract 的 `avoid` 禁止项。

## 内置风格预设

| Preset | 适合场景 | 气质 |
| --- | --- | --- |
| `flat-white` | SaaS、后台、生产力工具、开发者工具 | 清晰、克制、浅色 |
| `ink-black` | AI 工具、开发者工具、监控面板、安全产品 | 深色、高对比、专业 |
| `dense-saas` | CRM、ERP、管理后台、财务、运营系统 | 高密度、高效率 |
| `soft-minimal` | 知识管理、写作、笔记、教育产品 | 柔和、安静、内容友好 |
| `editorial-product` | 官网、产品介绍页、案例页、报告页 | 品牌感、叙事感 |
| `liquid-control` | macOS/iOS 气质工具、创意工具、控制面板 | 现代、精致、轻玻璃 |

## MCP 工具

插件通过 [.mcp.json](./.mcp.json) 提供本地 MCP server。

| 工具 | 作用 |
| --- | --- |
| `list_presets` | 列出所有内置 UI 风格 preset。 |
| `get_preset` | 读取某个 preset 的完整 JSON。 |
| `build_contract` | 根据 preset 创建 `.ui-style/ui-style-contract.json`。 |
| `build_image_prompt` | 根据 contract 生成 GPT-image-2 可用的 UI 草稿图 prompt。 |
| `merge_contract` | 合并 preset、已有 contract 和显式覆盖项。 |
| `generate_style_guide` | 根据 contract 生成 `.ui-style/UI_STYLE_GUIDE.md`。 |
| `apply_contract_to_tailwind` | 生成 CSS variables、Tailwind theme snippet 和落地说明。 |
| `review_ui` | 读取 contract，对 UI 文件做轻量风格漂移检查。 |
| `inspect_project_ui_stack` | 探测前端框架、样式系统、组件库和建议阅读的 UI 文件。 |

MCP 工具读写项目文件时，应传入项目目录 `base_dir`，这样 `.ui-style/` 会创建在目标项目里，而不是插件目录里。

## 脚本备用命令

如果 MCP 暂时没有加载，可以直接使用脚本。

从 preset 创建 contract：

```bash
python3 ~/plugins/ui-style-director/scripts/build_style_contract.py \
  --preset flat-white \
  --out .ui-style/ui-style-contract.json
```

生成 UI 草稿图 prompt：

```bash
python3 ~/plugins/ui-style-director/scripts/build_image_prompt.py \
  --contract .ui-style/ui-style-contract.json \
  --page "Dashboard" \
  --out .ui-style/image-prompts/dashboard.md
```

对 UI 文件做基础风格检查：

```bash
python3 ~/plugins/ui-style-director/scripts/review_ui_against_contract.py \
  --contract .ui-style/ui-style-contract.json \
  path/to/page.tsx
```

脚本只是轻量启发式检查，不能替代 Codex 对代码和界面的人工级 review。

## 生成的项目文件

建议每个被处理项目把产物放在：

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

## 插件结构

```text
.codex-plugin/plugin.json
.mcp.json
skills/ui-style-director/SKILL.md
assets/presets/
assets/templates/
scripts/
```

## 已支持的增强能力

- `merge_contract`：把预设、已有 contract 和自定义覆盖项合并成新的风格契约。
- `generate_style_guide`：把机器可读 contract 转成人类可读 UI 风格文档。
- `apply_contract_to_tailwind`：生成 Tailwind 落地需要的 token 片段和 CSS variables。
- `inspect_project_ui_stack`：先探测项目技术栈，再决定如何映射 contract。

## License

MIT
