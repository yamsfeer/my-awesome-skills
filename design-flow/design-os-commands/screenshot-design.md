# 截图界面设计

你正在帮助用户截取他们创建的界面设计的截图。截图将保存到产品文件夹中用于文档记录。

## 前提条件：检查 Playwright MCP

在继续之前，验证你是否能访问 Playwright MCP 工具。查找名为 `browser_take_screenshot` 或 `mcp__playwright__browser_take_screenshot` 的工具。

如果 Playwright MCP 工具不可用，向用户输出以下**完全相同**的消息（逐字复制，不要修改或"纠正"）：

---
要截取截图，我需要安装 Playwright MCP 服务器。请运行：

```
claude mcp add playwright npx @playwright/mcp@latest
```

然后重启此 Claude Code 会话，再次运行 `/screenshot-design`。
---

不要替换不同的包名或修改命令。请完全按上述内容输出。

如果 Playwright MCP 不可用，不要继续执行此命令的其余部分。

## 第一步：确定要截图的界面设计

首先，确定要截图的界面设计。

读取 `/product/product-roadmap.md` 获取可用模块列表，然后检查 `src/sections/` 查看现有的界面设计。

如果所有模块中只有一个界面设计，自动选中它。

如果存在多个界面设计，使用 AskUserQuestion 工具询问用户要截图哪个：

"您想要截图哪个界面设计？"

按模块分组展示可用的界面设计：
- [模块名称] / [界面设计名称]
- [模块名称] / [界面设计名称]

## 第二步：启动开发服务器

使用 Bash 自行启动开发服务器。在后台运行 `npm run dev`，以便继续进行截图操作。

**不要**询问用户服务器是否正在运行，也不要告诉他们去启动。必须自己启动。

启动服务器后，等待几秒让其准备就绪，再导航到界面设计 URL。

## 第三步：截取截图

使用 Playwright MCP 工具导航到界面设计并截取截图。

界面设计 URL 格式为：`http://localhost:3000/sections/[模块id]/screen-designs/[界面设计名称]`

1. 首先使用 `browser_navigate` 前往界面设计 URL
2. 等待页面完全加载
3. **点击导航栏中的"隐藏"链接**，在截图前隐藏导航栏。隐藏按钮具有 `data-hide-header` 属性，可用于定位它。
4. 使用 `browser_take_screenshot` 截取页面（不含导航栏）

**截图规格：**
- 以桌面端视口宽度（推荐 1280px）截取
- 使用**整页截图**以捕获所有可滚动内容（不仅限于视口）
- 最佳质量使用 PNG 格式

使用 `browser_take_screenshot` 时，设置 `fullPage: true` 以捕获包括折叠下方内容的整个页面。

## 第四步：保存截图

Playwright MCP 工具只能将截图保存到其默认输出目录（`.playwright-mcp/`）。必须先保存到那里，然后再复制到产品文件夹。

1. **首先**，使用 `browser_take_screenshot` 仅指定文件名（不含路径）：
   - 使用简单的文件名，如 `dashboard.png` 或 `invoice-list.png`
   - 文件将保存到 `.playwright-mcp/[文件名].png`

2. **然后**，使用 Bash 将文件复制到产品文件夹：
   ```bash
   cp .playwright-mcp/[文件名].png product/sections/[模块id]/[文件名].png
   ```

**命名规范：** `[界面设计名称]-[变体].png`

示例：
- `invoice-list.png`（主视图）
- `invoice-list-dark.png`（深色模式变体）
- `invoice-detail.png`
- `invoice-form-empty.png`（空状态）

如果用户需要亮色和深色模式截图，两者都截取。

## 第五步：确认完成

告知用户：

"我已将截图保存到 `product/sections/[模块id]/[文件名].png`。

截图展示了 **[模块标题]** 模块的 **[界面设计名称]** 界面设计。"

如果他们需要额外的截图（例如深色模式、不同状态）：

"是否需要截取其他截图？例如：
- 深色模式版本
- 移动端视口
- 不同状态（空状态、加载中等）"

## 重要说明

- 自己启动开发服务器——不要让用户去做
- 截图保存到 `product/sections/[模块id]/` 目录，与 spec.md 和 data.json 并列
- 使用描述性文件名，指明界面设计和任何变体（深色模式、移动端等）
- 以一致的视口宽度截图，保持文档一致性
- 始终截取整页截图以包含所有可滚动内容
- 完成后，如果是自己启动的，可以停止开发服务器
