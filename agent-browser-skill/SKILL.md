---
name: agent-browser-skill
description: 用于 AI 代理的无头浏览器自动化 CLI。当 Claude 需要自动化网页浏览任务时使用，如导航页面、点击元素、填写表单、截取屏幕截图、提取内容或与 Web 应用程序交互。支持基于引用的元素选择、语义定位器和通过 Playwright 的程序化控制。
---

# 代理浏览器（Agent Browser）

为 AI 代理优化的无头浏览器自动化 CLI。使用 Rust CLI 与 Node.js 回退和 Playwright 浏览器引擎。

## 快速开始

```bash
agent-browser open <url>              # 导航到 URL
agent-browser snapshot                # 获取带有引用的可访问性树
agent-browser click @e2               # 通过引用点击
agent-browser fill @e3 "文本"         # 通过引用填写
agent-browser screenshot page.png
agent-browser close
```

## 安装

```bash
npm install -g agent-browser
agent-browser install  # 下载 Chromium
```

对于 Linux 系统依赖：

```bash
agent-browser install --with-deps
```

## 核心工作流程

1. **导航**：`agent-browser open <url>`
2. **快照**：`agent-browser snapshot` - 获取带有引用（@e1, @e2, ...）的页面结构
3. **交互**：使用引用进行点击、填写或获取元素
4. **重新快照**：页面变化后，获取新快照
5. **关闭**：完成后执行 `agent-browser close`

## 为什么使用引用？

引用提供来自快照的确定性元素选择：

- 快速：无需 DOM 重新查询
- 可靠：引用指向快照中的确切元素
- AI 友好：快照 + 引用工作流程对 LLM 来说是最佳的

## 命令

### 导航

```bash
agent-browser open <url>              # 导航（别名：goto, navigate）
agent-browser back                    # 返回
agent-browser forward                 # 前进
agent-browser reload                  # 重新加载页面
agent-browser close                   # 关闭浏览器（别名：quit, exit）
```

### 页面交互

```bash
agent-browser click <sel>             # 点击元素
agent-browser dblclick <sel>          # 双击
agent-browser focus <sel>             # 聚焦元素
agent-browser type <sel> <text>       # 在元素中输入文本
agent-browser fill <sel> <text>       # 清空并填写
agent-browser press <key>             # 按键（Enter, Tab, Control+a）
agent-browser hover <sel>             # 悬停元素
agent-browser select <sel> <val>      # 选择下拉框
agent-browser check <sel>             # 勾选复选框
agent-browser uncheck <sel>           # 取消勾选复选框
```

### 滚动

```bash
agent-browser scroll <dir> [px]       # 滚动（上/下/左/右）
agent-browser scrollintoview <sel>    # 将元素滚动到视图中
```

### 获取信息

```bash
agent-browser get text <sel>          # 获取文本内容
agent-browser get html <sel>          # 获取 innerHTML
agent-browser get value <sel>         # 获取输入值
agent-browser get attr <sel> <attr>   # 获取属性
agent-browser get title               # 获取页面标题
agent-browser get url                 # 获取当前 URL
agent-browser get count <sel>         # 统计匹配元素数量
agent-browser get box <sel>           # 获取边界框
```

### 检查状态

```bash
agent-browser is visible <sel>        # 检查是否可见
agent-browser is enabled <sel>        # 检查是否启用
agent-browser is checked <sel>        # 检查是否已勾选
```

### 截图

```bash
agent-browser snapshot                # 可访问性树及引用
agent-browser screenshot [path]       # 截取屏幕截图（--full 表示全页面）
agent-browser pdf <path>              # 保存为 PDF
```

### 查找（语义定位器）

```bash
agent-browser find role <role> <action> [value]     # 通过 ARIA 角色
agent-browser find text <text> <action>             # 通过文本内容
agent-browser find label <label> <action> [value]   # 通过标签
agent-browser find placeholder <ph> <action> [val]  # 通过占位符
agent-browser find testid <id> <action> [value]     # 通过 data-testid
```

操作：`click`, `fill`, `check`, `hover`, `text`

### 等待

```bash
agent-browser wait <sel>              # 等待元素可见
agent-browser wait <ms>               # 等待毫秒
agent-browser wait --text "欢迎"      # 等待文本出现
agent-browser wait --url "**/dash"    # 等待 URL 模式匹配
agent-browser wait --load networkidle # 等待加载状态
```

### 其他

```bash
agent-browser eval <js>               # 运行 JavaScript
agent-browser drag <src> <tgt>        # 拖放
agent-browser upload <sel> <files>    # 上传文件
```

## 快照选项

```bash
agent-browser snapshot                # 完整可访问性树
agent-browser snapshot -i             # 仅交互元素
agent-browser snapshot -c             # 紧凑模式
agent-browser snapshot -d 3           # 限制深度为 3 层
agent-browser snapshot -s "#main"     # 限定在 CSS 选择器范围内
agent-browser snapshot -i -c -d 5     # 组合选项
```

## 选择器

**引用**（推荐）：`@e1`, `@e2` 等，来自快照
**CSS**：`#id`, `.class`, `div > button`
**文本**：`text=提交`
**XPath**：`xpath=//button`
**语义**：`agent-browser find role button click --name "提交"`

## JSON 模式

用于机器可读的输出：

```bash
agent-browser snapshot --json
agent-browser get text @e1 --json
agent-browser is visible @e2 --json
```

## 会话

运行多个隔离的浏览器实例：

```bash
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com
agent-browser session list            # 列出活动会话
```

## 浏览器设置

```bash
agent-browser set viewport <w> <h>    # 设置视口大小
agent-browser set device "iPhone 14"  # 模拟设备
agent-browser set geo <lat> <lng>     # 设置地理位置
agent-browser set offline on          # 切换离线模式
agent-browser set media dark          # 模拟配色方案
```

## 高级功能

**请求头**：`agent-browser open <url> --headers '{"Authorization": "Bearer token"}'`
**有头模式**：`agent-browser open <url> --headed`（显示浏览器窗口）
**CDP**：`agent-browser --cdp 9222`（通过 Chrome DevTools 协议连接）
**追踪**：`agent-browser trace start` / `trace stop` 用于调试

## 完整参考

有关完整的命令参考及示例，请参阅 [commands.md](references/commands.md)。
