# Agent Browser - Complete Command Reference

Complete reference for all agent-browser commands with detailed examples.

## Table of Contents

- [Navigation](#navigation)
- [Page Interaction](#page-interaction)
- [Mouse Control](#mouse-control)
- [Keyboard](#keyboard)
- [Get Info](#get-info)
- [Check State](#check-state)
- [Capture](#capture)
- [Find Elements](#find-elements)
- [Wait](#wait)
- [Browser Settings](#browser-settings)
- [Cookies & Storage](#cookies--storage)
- [Network](#network)
- [Tabs & Windows](#tabs--windows)
- [Frames](#frames)
- [Dialogs](#dialogs)
- [Debug](#debug)
- [Sessions](#sessions)
- [Options](#options)

---

## Navigation

### open
```bash
agent-browser open <url>
agent-browser goto <url>      # alias
agent-browser navigate <url>   # alias
```

Navigate to a URL. Opens a new browser instance if none exists.

### back
```bash
agent-browser back
```

Go back in browser history.

### forward
```bash
agent-browser forward
```

Go forward in browser history.

### reload
```bash
agent-browser reload
```

Reload the current page.

### close
```bash
agent-browser close
agent-browser quit   # alias
agent-browser exit  # alias
```

Close the browser and end the session.

---

## Page Interaction

### click
```bash
agent-browser click <selector>
agent-browser click @e2              # using ref
agent-browser click "#submit"        # CSS selector
agent-browser click "text=Submit"    # text selector
```

Click an element.

### dblclick
```bash
agent-browser dblclick <selector>
```

Double-click an element.

### focus
```bash
agent-browser focus <selector>
```

Focus an element.

### type
```bash
agent-browser type <selector> <text>
```

Type text into an element without clearing first.

### fill
```bash
agent-browser fill <selector> <text>
```

Clear the element and then fill with text.

### press
```bash
agent-browser press <key>
agent-browser key <key>   # alias
```

Press a keyboard key. Common keys: `Enter`, `Tab`, `Escape`, `Backspace`, `ArrowDown`, `Control+a`, `Meta+c`.

### hover
```bash
agent-browser hover <selector>
```

Hover over an element.

### select
```bash
agent-browser select <selector> <value>
```

Select an option from a dropdown.

### check
```bash
agent-browser check <selector>
```

Check a checkbox.

### uncheck
```bash
agent-browser uncheck <selector>
```

Uncheck a checkbox.

---

## Mouse Control

### mouse move
```bash
agent-browser mouse move <x> <y>
```

Move mouse to coordinates.

### mouse down
```bash
agent-browser mouse down [button]   # left, right, middle
```

Press mouse button (default: left).

### mouse up
```bash
agent-browser mouse up [button]
```

Release mouse button.

### mouse wheel
```bash
agent-browser mouse wheel <dy> [dx]
```

Scroll mouse wheel.

---

## Keyboard

### keydown
```bash
agent-browser keydown <key>
```

Hold a key down.

### keyup
```bash
agent-browser keyup <key>
```

Release a held key.

---

## Get Info

### get text
```bash
agent-browser get text <selector>
```

Get text content of an element.

### get html
```bash
agent-browser get html <selector>
```

Get innerHTML of an element.

### get value
```bash
agent-browser get value <selector>
```

Get value of an input element.

### get attr
```bash
agent-browser get attr <selector> <attribute>
```

Get attribute value (e.g., `href`, `src`, `data-id`).

### get title
```bash
agent-browser get title
```

Get page title.

### get url
```bash
agent-browser get url
```

Get current URL.

### get count
```bash
agent-browser get count <selector>
```

Count matching elements.

### get box
```bash
agent-browser get box <selector>
```

Get bounding box (x, y, width, height) of element.

---

## Check State

### is visible
```bash
agent-browser is visible <selector>
```

Check if element is visible.

### is enabled
```bash
agent-browser is enabled <selector>
```

Check if element is enabled.

### is checked
```bash
agent-browser is checked <selector>
```

Check if checkbox is checked.

---

## Capture

### snapshot
```bash
agent-browser snapshot
agent-browser snapshot -i                 # interactive only
agent-browser snapshot -c                 # compact
agent-browser snapshot -d 3               # max depth
agent-browser snapshot -s "#main"         # scope to selector
```

Get accessibility tree with refs. Best for AI agents.

Output format:
```
- heading "Title" [ref=e1] [level=1]
- button "Submit" [ref=e2]
- textbox "Email" [ref=e3]
- link "Learn more" [ref=e4]
```

### screenshot
```bash
agent-browser screenshot [path]
agent-browser screenshot --full page.png   # full page
agent-browser screenshot -f page.png       # short for full
```

Take a screenshot of the current page.

### pdf
```bash
agent-browser pdf <path>
```

Save current page as PDF.

---

## Find Elements

Semantic locators for finding elements by role, text, label, etc.

### find role
```bash
agent-browser find role <role> <action> [value]
agent-browser find role button click --name "Submit"
agent-browser find role link hover --name "Learn more"
agent-browser find role textbox fill "Email" "test@test.com"
```

Find by ARIA role. Roles: `button`, `link`, `textbox`, `heading`, `listbox`, `menuitem`, etc.

### find text
```bash
agent-browser find text <text> <action>
agent-browser find text "Sign In" click
agent-browser find text "Welcome" text
```

Find by text content.

### find label
```bash
agent-browser find label <label> <action> [value]
agent-browser find label "Email" fill "test@test.com"
agent-browser find label "Password" fill "secret123"
```

Find by associated label.

### find placeholder
```bash
agent-browser find placeholder <placeholder> <action> [value]
agent-browser find placeholder "Search" fill "query"
```

Find by placeholder attribute.

### find alt
```bash
agent-browser find alt <text> <action>
agent-browser find alt "Logo" click
```

Find by alt text (images).

### find title
```bash
agent-browser find title <text> <action>
agent-browser find title "Tooltip" hover
```

Find by title attribute.

### find testid
```bash
agent-browser find testid <id> <action> [value]
agent-browser find testid "submit-btn" click
```

Find by data-testid attribute.

### find first/last/nth
```bash
agent-browser find first <selector> <action> [value]
agent-browser find last <selector> <action> [value]
agent-browser find nth <n> <selector> <action> [value]
```

Find nth matching element.

**Actions**: `click`, `fill`, `check`, `hover`, `text`

---

## Wait

### wait (selector)
```bash
agent-browser wait <selector>
```

Wait for element to be visible.

### wait (time)
```bash
agent-browser wait 5000   # wait 5000ms
```

Wait for specified milliseconds.

### wait --text
```bash
agent-browser wait --text "Welcome"
```

Wait for text to appear on page.

### wait --url
```bash
agent-browser wait --url "**/dashboard"
agent-browser wait --url "https://example.com/*"
```

Wait for URL to match pattern.

### wait --load
```bash
agent-browser wait --load networkidle
agent-browser wait --load domcontentloaded
agent-browser wait --load load
```

Wait for page load state.

### wait --fn
```bash
agent-browser wait --fn "window.ready === true"
```

Wait for JavaScript condition to be true.

---

## Browser Settings

### set viewport
```bash
agent-browser set viewport <width> <height>
agent-browser set viewport 1920 1080
```

Set viewport size.

### set device
```bash
agent-browser set device <name>
agent-browser set device "iPhone 14"
agent-browser set device "Pixel 5"
```

Emulate a device. Common devices: `iPhone 14`, `iPhone SE`, `Pixel 5`, `iPad Pro`, etc.

### set geo
```bash
agent-browser set geo <latitude> <longitude>
agent-browser set geo 37.7749 -122.4194
```

Set geolocation.

### set offline
```bash
agent-browser set offline on
agent-browser set offline off
```

Toggle offline mode.

### set headers
```bash
agent-browser set headers '{"Authorization": "Bearer token"}'
```

Set global HTTP headers.

### set credentials
```bash
agent-browser set credentials <username> <password>
```

Set HTTP basic authentication credentials.

### set media
```bash
agent-browser set media dark
agent-browser set media light
```

Emulate color scheme preference.

---

## Cookies & Storage

### cookies
```bash
agent-browser cookies
```

Get all cookies.

### cookies set
```bash
agent-browser cookies set <name> <value>
```

Set a cookie.

### cookies clear
```bash
agent-browser cookies clear
```

Clear all cookies.

### storage local
```bash
agent-browser storage local           # get all
agent-browser storage local <key>     # get specific
agent-browser storage local set <k> <v>  # set value
agent-browser storage local clear     # clear all
```

Manage localStorage.

### storage session
```bash
agent-browser storage session
agent-browser storage session <key>
agent-browser storage session set <k> <v>
agent-browser storage session clear
```

Manage sessionStorage.

---

## Network

### network route
```bash
agent-browser network route <url>
agent-browser network route <url> --abort
agent-browser network route <url> --body '{"status": "ok"}'
```

Intercept and modify requests.

### network unroute
```bash
agent-browser network unroute [url]
```

Remove request interception.

### network requests
```bash
agent-browser network requests
agent-browser network requests --filter api
```

View tracked requests.

---

## Tabs & Windows

### tab
```bash
agent-browser tab              # list tabs
agent-browser tab <n>          # switch to tab
```

List or switch tabs.

### tab new
```bash
agent-browser tab new [url]
```

Open new tab.

### tab close
```bash
agent-browser tab close [n]
```

Close tab (current or specified).

### window new
```bash
agent-browser window new
```

Open new window.

---

## Frames

### frame
```bash
agent-browser frame <selector>
```

Switch to iframe.

### frame main
```bash
agent-browser frame main
```

Switch back to main frame.

---

## Dialogs

### dialog accept
```bash
agent-browser dialog accept [text]
```

Accept alert/confirm/prompt dialog (with optional prompt text).

### dialog dismiss
```bash
agent-browser dialog dismiss
```

Dismiss dialog.

---

## Debug

### trace start/stop
```bash
agent-browser trace start [path]
agent-browser trace stop [path]
```

Record trace for debugging.

### console
```bash
agent-browser console
agent-browser console --clear
```

View or clear console messages.

### errors
```bash
agent-browser errors
agent-browser errors --clear
```

View or clear page errors.

### highlight
```bash
agent-browser highlight <selector>
```

Highlight an element on the page.

### state save/load
```bash
agent-browser state save <path>
agent-browser state load <path>
```

Save/load authentication state (cookies, localStorage).

---

## Sessions

Run multiple isolated browser instances.

### Via flag
```bash
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com
```

### Via environment
```bash
AGENT_BROWSER_SESSION=agent1 agent-browser click "#btn"
```

### session list
```bash
agent-browser session list
```

List all active sessions.

### session
```bash
agent-browser session
```

Show current session name.

---

## Options

Global options that work with most commands:

| Option | Description |
|--------|-------------|
| `--session <name>` | Use isolated session |
| `--headers <json>` | Set HTTP headers for URL origin |
| `--executable-path <path>` | Custom browser executable |
| `--json` | JSON output for machine parsing |
| `--full, -f` | Full page screenshot |
| `--name, -n` | Locator name filter |
| `--exact` | Exact text match |
| `--headed` | Show browser window |
| `--cdp <port>` | Connect via Chrome DevTools Protocol |
| `--debug` | Debug output |

---

## Scrolling

### scroll
```bash
agent-browser scroll <direction> [pixels]
agent-browser scroll down 500
agent-browser scroll up
agent-browser scroll left
agent-browser scroll right
```

Scroll page.

### scrollintoview
```bash
agent-browser scrollintoview <selector>
agent-browser scrollinto <selector>   # alias
```

Scroll element into view.

---

## Other Commands

### drag
```bash
agent-browser drag <source> <target>
```

Drag and drop.

### upload
```bash
agent-browser upload <selector> <files>
agent-browser upload "#file-input" "/path/to/file1.png,/path/to/file2.jpg"
```

Upload files (comma-separated).

### eval
```bash
agent-browser eval <javascript>
agent-browser eval "document.title"
```

Execute JavaScript in page context.

---

## Complete Workflow Examples

### Login Flow
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

### Form Testing
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i    # interactive only
agent-browser find label "Name" fill "John Doe"
agent-browser find label "Email" fill "john@example.com"
agent-browser find role button click --name "Submit"
agent-browser wait --text "Thank you"
agent-browser is visible ".success-message"
```

### Scraping
```bash
agent-browser open https://example.com/list
agent-browser get count ".item"
agent-browser get text ".item:first-child"
agent-browser get attr ".item:first-child a" "href"
