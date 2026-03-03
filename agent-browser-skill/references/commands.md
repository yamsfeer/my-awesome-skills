# 代理浏览器 - 完整命令参考

所有 agent-browser 命令的完整参考，包含详细示例。

## 目录

- [导航](#导航)
- [页面交互](#页面交互)
- [鼠标控制](#鼠标控制)
- [键盘](#键盘)
- [获取信息](#获取信息)
- [检查状态](#检查状态)
- [截图](#截图)
- [查找元素](#查找元素)
- [等待](#等待)
- [浏览器设置](#浏览器设置)
- [Cookie 与存储](#cookie-与存储)
- [网络](#网络)
- [标签页与窗口](#标签页与窗口)
- [框架](#框架)
- [对话框](#对话框)
- [调试](#调试)
- [会话](#会话)
- [选项](#选项)

---

## 导航

### open
```bash
agent-browser open <url>
agent-browser goto <url>      # 别名
agent-browser navigate <url>   # 别名
```

导航到 URL。如果不存在浏览器实例，则打开一个新的。

### back
```bash
agent-browser back
```

在浏览器历史中返回。

### forward
```bash
agent-browser forward
```

在浏览器历史中前进。

### reload
```bash
agent-browser reload
```

重新加载当前页面。

### close
```bash
agent-browser close
agent-browser quit   # 别名
agent-browser exit  # 别名
```

关闭浏览器并结束会话。

---

## 页面交互

### click
```bash
agent-browser click <selector>
agent-browser click @e2              # 使用引用
agent-browser click "#submit"        # CSS 选择器
agent-browser click "text=提交"      # 文本选择器
```

点击一个元素。

### dblclick
```bash
agent-browser dblclick <selector>
```

双击一个元素。

### focus
```bash
agent-browser focus <selector>
```

聚焦一个元素。

### type
```bash
agent-browser type <selector> <text>
```

在元素中输入文本，不清空原有内容。

### fill
```bash
agent-browser fill <selector> <text>
```

清空元素并用文本填写。

### press
```bash
agent-browser press <key>
agent-browser key <key>   # 别名
```

按键盘键。常用键：`Enter`, `Tab`, `Escape`, `Backspace`, `ArrowDown`, `Control+a`, `Meta+c`。

### hover
```bash
agent-browser hover <selector>
```

悬停在元素上。

### select
```bash
agent-browser select <selector> <value>
```

从下拉框中选择一个选项。

### check
```bash
agent-browser check <selector>
```

勾选复选框。

### uncheck
```bash
agent-browser uncheck <selector>
```

取消勾选复选框。

---

## 鼠标控制

### mouse move
```bash
agent-browser mouse move <x> <y>
```

将鼠标移动到坐标位置。

### mouse down
```bash
agent-browser mouse down [button]   # left, right, middle
```

按下鼠标按钮（默认：左键）。

### mouse up
```bash
agent-browser mouse up [button]
```

释放鼠标按钮。

### mouse wheel
```bash
agent-browser mouse wheel <dy> [dx]
```

滚动鼠标滚轮。

---

## 键盘

### keydown
```bash
agent-browser keydown <key>
```

按住一个键。

### keyup
```bash
agent-browser keyup <key>
```

释放按住的键。

---

## 获取信息

### get text
```bash
agent-browser get text <selector>
```

获取元素的文本内容。

### get html
```bash
agent-browser get html <selector>
```

获取元素的 innerHTML。

### get value
```bash
agent-browser get value <selector>
```

获取输入元素的值。

### get attr
```bash
agent-browser get attr <selector> <attribute>
```

获取属性值（例如 `href`, `src`, `data-id`）。

### get title
```bash
agent-browser get title
```

获取页面标题。

### get url
```bash
agent-browser get url
```

获取当前 URL。

### get count
```bash
agent-browser get count <selector>
```

统计匹配元素的数量。

### get box
```bash
agent-browser get box <selector>
```

获取元素的边界框（x, y, width, height）。

---

## 检查状态

### is visible
```bash
agent-browser is visible <selector>
```

检查元素是否可见。

### is enabled
```bash
agent-browser is enabled <selector>
```

检查元素是否启用。

### is checked
```bash
agent-browser is checked <selector>
```

检查复选框是否已勾选。

---

## 截图

### snapshot
```bash
agent-browser snapshot
agent-browser snapshot -i                 # 仅交互元素
agent-browser snapshot -c                 # 紧凑模式
agent-browser snapshot -d 3               # 最大深度
agent-browser snapshot -s "#main"         # 限定在选择器范围内
```

获取带有引用的可访问性树。最适合 AI 代理。

输出格式：
```
- heading "标题" [ref=e1] [level=1]
- button "提交" [ref=e2]
- textbox "邮箱" [ref=e3]
- link "了解更多" [ref=e4]
```

### screenshot
```bash
agent-browser screenshot [path]
agent-browser screenshot --full page.png   # 全页面
agent-browser screenshot -f page.png       # --full 的简写
```

截取当前页面的屏幕截图。

### pdf
```bash
agent-browser pdf <path>
```

将当前页面保存为 PDF。

---

## 查找元素

通过角色、文本、标签等查找元素的语义定位器。

### find role
```bash
agent-browser find role <role> <action> [value]
agent-browser find role button click --name "提交"
agent-browser find role link hover --name "了解更多"
agent-browser find role textbox fill "邮箱" "test@test.com"
```

通过 ARIA 角色查找。角色：`button`, `link`, `textbox`, `heading`, `listbox`, `menuitem` 等。

### find text
```bash
agent-browser find text <text> <action>
agent-browser find text "登录" click
agent-browser find text "欢迎" text
```

通过文本内容查找。

### find label
```bash
agent-browser find label <label> <action> [value]
agent-browser find label "邮箱" fill "test@test.com"
agent-browser find label "密码" fill "secret123"
```

通过关联标签查找。

### find placeholder
```bash
agent-browser find placeholder <placeholder> <action> [value]
agent-browser find placeholder "搜索" fill "查询词"
```

通过占位符属性查找。

### find alt
```bash
agent-browser find alt <text> <action>
agent-browser find alt "Logo" click
```

通过 alt 文本查找（图片）。

### find title
```bash
agent-browser find title <text> <action>
agent-browser find title "提示" hover
```

通过 title 属性查找。

### find testid
```bash
agent-browser find testid <id> <action> [value]
agent-browser find testid "submit-btn" click
```

通过 data-testid 属性查找。

### find first/last/nth
```bash
agent-browser find first <selector> <action> [value]
agent-browser find last <selector> <action> [value]
agent-browser find nth <n> <selector> <action> [value]
```

查找第 n 个匹配的元素。

**操作**：`click`, `fill`, `check`, `hover`, `text`

---

## 等待

### wait (selector)
```bash
agent-browser wait <selector>
```

等待元素可见。

### wait (time)
```bash
agent-browser wait 5000   # 等待 5000 毫秒
```

等待指定的毫秒数。

### wait --text
```bash
agent-browser wait --text "欢迎"
```

等待文本出现在页面上。

### wait --url
```bash
agent-browser wait --url "**/dashboard"
agent-browser wait --url "https://example.com/*"
```

等待 URL 匹配模式。

### wait --load
```bash
agent-browser wait --load networkidle
agent-browser wait --load domcontentloaded
agent-browser wait --load load
```

等待页面加载状态。

### wait --fn
```bash
agent-browser wait --fn "window.ready === true"
```

等待 JavaScript 条件为真。

---

## 浏览器设置

### set viewport
```bash
agent-browser set viewport <width> <height>
agent-browser set viewport 1920 1080
```

设置视口大小。

### set device
```bash
agent-browser set device <name>
agent-browser set device "iPhone 14"
agent-browser set device "Pixel 5"
```

模拟设备。常用设备：`iPhone 14`, `iPhone SE`, `Pixel 5`, `iPad Pro` 等。

### set geo
```bash
agent-browser set geo <latitude> <longitude>
agent-browser set geo 37.7749 -122.4194
```

设置地理位置。

### set offline
```bash
agent-browser set offline on
agent-browser set offline off
```

切换离线模式。

### set headers
```bash
agent-browser set headers '{"Authorization": "Bearer token"}'
```

设置全局 HTTP 请求头。

### set credentials
```bash
agent-browser set credentials <username> <password>
```

设置 HTTP 基本认证凭据。

### set media
```bash
agent-browser set media dark
agent-browser set media light
```

模拟配色方案偏好。

---

## Cookie 与存储

### cookies
```bash
agent-browser cookies
```

获取所有 Cookie。

### cookies set
```bash
agent-browser cookies set <name> <value>
```

设置一个 Cookie。

### cookies clear
```bash
agent-browser cookies clear
```

清除所有 Cookie。

### storage local
```bash
agent-browser storage local           # 获取所有
agent-browser storage local <key>     # 获取特定
agent-browser storage local set <k> <v>  # 设置值
agent-browser storage local clear     # 清除所有
```

管理 localStorage。

### storage session
```bash
agent-browser storage session
agent-browser storage session <key>
agent-browser storage session set <k> <v>
agent-browser storage session clear
```

管理 sessionStorage。

---

## 网络

### network route
```bash
agent-browser network route <url>
agent-browser network route <url> --abort
agent-browser network route <url> --body '{"status": "ok"}'
```

拦截和修改请求。

### network unroute
```bash
agent-browser network unroute [url]
```

移除请求拦截。

### network requests
```bash
agent-browser network requests
agent-browser network requests --filter api
```

查看已追踪的请求。

---

## 标签页与窗口

### tab
```bash
agent-browser tab              # 列出标签页
agent-browser tab <n>          # 切换到标签页
```

列出或切换标签页。

### tab new
```bash
agent-browser tab new [url]
```

打开新标签页。

### tab close
```bash
agent-browser tab close [n]
```

关闭标签页（当前或指定）。

### window new
```bash
agent-browser window new
```

打开新窗口。

---

## 框架

### frame
```bash
agent-browser frame <selector>
```

切换到 iframe。

### frame main
```bash
agent-browser frame main
```

切换回主框架。

---

## 对话框

### dialog accept
```bash
agent-browser dialog accept [text]
```

接受 alert/confirm/prompt 对话框（带可选的提示文本）。

### dialog dismiss
```bash
agent-browser dialog dismiss
```

关闭对话框。

---

## 调试

### trace start/stop
```bash
agent-browser trace start [path]
agent-browser trace stop [path]
```

录制追踪用于调试。

### console
```bash
agent-browser console
agent-browser console --clear
```

查看或清除控制台消息。

### errors
```bash
agent-browser errors
agent-browser errors --clear
```

查看或清除页面错误。

### highlight
```bash
agent-browser highlight <selector>
```

在页面上高亮显示一个元素。

### state save/load
```bash
agent-browser state save <path>
agent-browser state load <path>
```

保存/加载认证状态（Cookie, localStorage）。

---

## 会话

运行多个隔离的浏览器实例。

### 通过标志
```bash
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com
```

### 通过环境变量
```bash
AGENT_BROWSER_SESSION=agent1 agent-browser click "#btn"
```

### session list
```bash
agent-browser session list
```

列出所有活动会话。

### session
```bash
agent-browser session
```

显示当前会话名称。

---

## 选项

适用于大多数命令的全局选项：

| 选项 | 描述 |
|--------|-------------|
| `--session <name>` | 使用隔离会话 |
| `--headers <json>` | 为 URL 来源设置 HTTP 请求头 |
| `--executable-path <path>` | 自定义浏览器可执行文件 |
| `--json` | JSON 输出用于机器解析 |
| `--full, -f` | 全页面截图 |
| `--name, -n` | 定位器名称过滤 |
| `--exact` | 精确文本匹配 |
| `--headed` | 显示浏览器窗口 |
| `--cdp <port>` | 通过 Chrome DevTools 协议连接 |
| `--debug` | 调试输出 |

---

## 滚动

### scroll
```bash
agent-browser scroll <direction> [pixels]
agent-browser scroll down 500
agent-browser scroll up
agent-browser scroll left
agent-browser scroll right
```

滚动页面。

### scrollintoview
```bash
agent-browser scrollintoview <selector>
agent-browser scrollinto <selector>   # 别名
```

将元素滚动到视图中。

---

## 其他命令

### drag
```bash
agent-browser drag <source> <target>
```

拖放。

### upload
```bash
agent-browser upload <selector> <files>
agent-browser upload "#file-input" "/path/to/file1.png,/path/to/file2.jpg"
```

上传文件（逗号分隔）。

### eval
```bash
agent-browser eval <javascript>
agent-browser eval "document.title"
```

在页面上下文中执行 JavaScript。

---

## 完整工作流程示例

### 登录流程
```bash
agent-browser open https://example.com/login
agent-browser snapshot
agent-browser fill @e3 "user@example.com"
agent-browser fill @e4 "password123"
agent-browser click @e5
agent-browser wait --url "**/dashboard"
agent-browser screenshot dashboard.png
agent-browser close
```

### 表单测试
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i    # 仅交互元素
agent-browser find label "姓名" fill "张三"
agent-browser find label "邮箱" fill "zhangsan@example.com"
agent-browser find role button click --name "提交"
agent-browser wait --text "谢谢"
agent-browser is visible ".success-message"
```

### 数据抓取
```bash
agent-browser open https://example.com/list
agent-browser get count ".item"
agent-browser get text ".item:first-child"
agent-browser get attr ".item:first-child a" "href"
```
