# Excalidraw 图表技能

一个编码代理技能，可以从自然语言描述生成美观实用的 Excalidraw 图表。不仅仅是框和箭头——而是能够**进行可视化论证**的图表。

兼容任何支持技能的编码代理。对于从 `.claude/skills/` 读取的代理（如 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 和 [OpenCode](https://github.com/nicepkg/OpenCode)），只需放入即可使用。

## 与众不同之处

- **图表进行论证，而非仅仅展示。** 每个形状/形状组都镜像它所代表的概念——扇出表示一对多，时间线表示序列，汇聚表示聚合。没有统一的卡片网格。
- **证据工件。** 例如，技术图表包含真实的代码片段和实际的 JSON 载荷。
- **内置视觉验证。** 基于 Playwright 的渲染管道让代理看到自己的输出，捕捉布局问题（重叠文本、箭头错位、间距不平衡），并在交付前在循环中修复它们。
- **品牌可定制。** 所有颜色和品牌样式存在于单个文件（`references/color-palette.md`）中。替换它，每个图表都遵循你的调色板。

## 安装

克隆或下载此仓库，然后将其复制到你项目的 `.claude/skills/` 目录：

```bash
git clone https://github.com/coleam00/excalidraw-diagram-skill.git
cp -r excalidraw-diagram-skill .claude/skills/excalidraw-diagram
```

## 设置

该技能包含一个渲染管道，让代理可以视觉验证其图表。有两种设置方式：

**选项 A：询问你的编码代理（最简单）**

只需告诉你的代理：*"按照 SKILL.md 中的说明设置 Excalidraw 图表技能渲染器。"* 它会为你运行命令。

**选项 B：手动**

```bash
cd .claude/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

## 使用

让你的编码代理创建图表：

> "创建一个 Excalidraw 图表，展示 AG-UI 协议如何将事件从 AI 代理流式传输到前端 UI"

技能会处理其余部分——概念映射、布局、JSON 生成、渲染和视觉验证。

## 自定义颜色

编辑 `references/color-palette.md` 以匹配你的品牌。技能中的其他所有内容都是通用的设计方法论。

## 文件结构

```
excalidraw-diagram/
  SKILL.md                          # 设计方法论 + 工作流程
  references/
    color-palette.md                # 品牌颜色（编辑此文件以自定义）
    element-templates.md            # 每种元素类型的 JSON 模板
    json-schema.md                  # Excalidraw JSON 格式参考
    render_excalidraw.py            # 将 .excalidraw 渲染为 PNG
    render_template.html            # 用于渲染的浏览器模板
    pyproject.toml                  # Python 依赖（playwright）
```
