---
name: agent-browser-skill
description: Headless browser automation CLI for AI agents. Use when Claude needs to automate web browsing tasks like navigating pages, clicking elements, filling forms, taking screenshots, extracting content, or interacting with web applications. Supports refs-based element selection, semantic locators, and programmatic control via Playwright.
---

# Agent Browser

Headless browser automation CLI optimized for AI agents. Uses Rust CLI with Node.js fallback and Playwright browser engine.

## Quick Start

```bash
agent-browser open <url>              # Navigate to URL
agent-browser snapshot                # Get accessibility tree with refs
agent-browser click @e2               # Click by ref
agent-browser fill @e3 "text"         # Fill by ref
agent-browser screenshot page.png
agent-browser close
```

## Installation

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
```

For Linux system dependencies:

```bash
agent-browser install --with-deps
```

## Core Workflow

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot` - Get page structure with refs (@e1, @e2, ...)
3. **Interact**: Use refs to click, fill, or get elements
4. **Re-snapshot**: After page changes, get new snapshot
5. **Close**: `agent-browser close` when done

## Why Refs?

Refs provide deterministic element selection from snapshots:

- Fast: No DOM re-query needed
- Reliable: Ref points to exact element from snapshot
- AI-friendly: Snapshot + ref workflow is optimal for LLMs

## Commands

### Navigation

```bash
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser back                    # Go back
agent-browser forward                 # Go forward
agent-browser reload                  # Reload page
agent-browser close                   # Close browser (aliases: quit, exit)
```

### Page Interaction

```bash
agent-browser click <sel>             # Click element
agent-browser dblclick <sel>          # Double-click
agent-browser focus <sel>             # Focus element
agent-browser type <sel> <text>       # Type into element
agent-browser fill <sel> <text>       # Clear and fill
agent-browser press <key>             # Press key (Enter, Tab, Control+a)
agent-browser hover <sel>             # Hover element
agent-browser select <sel> <val>      # Select dropdown
agent-browser check <sel>             # Check checkbox
agent-browser uncheck <sel>           # Uncheck checkbox
```

### Scrolling

```bash
agent-browser scroll <dir> [px]       # Scroll (up/down/left/right)
agent-browser scrollintoview <sel>    # Scroll element into view
```

### Get Info

```bash
agent-browser get text <sel>          # Get text content
agent-browser get html <sel>          # Get innerHTML
agent-browser get value <sel>         # Get input value
agent-browser get attr <sel> <attr>   # Get attribute
agent-browser get title               # Get page title
agent-browser get url                 # Get current URL
agent-browser get count <sel>         # Count matching elements
agent-browser get box <sel>           # Get bounding box
```

### Check State

```bash
agent-browser is visible <sel>        # Check if visible
agent-browser is enabled <sel>        # Check if enabled
agent-browser is checked <sel>        # Check if checked
```

### Capture

```bash
agent-browser snapshot                # Accessibility tree with refs
agent-browser screenshot [path]       # Take screenshot (--full for full page)
agent-browser pdf <path>              # Save as PDF
```

### Find (Semantic Locators)

```bash
agent-browser find role <role> <action> [value]     # By ARIA role
agent-browser find text <text> <action>             # By text content
agent-browser find label <label> <action> [value]   # By label
agent-browser find placeholder <ph> <action> [val]  # By placeholder
agent-browser find testid <id> <action> [value]     # By data-testid
```

Actions: `click`, `fill`, `check`, `hover`, `text`

### Wait

```bash
agent-browser wait <sel>              # Wait for element to be visible
agent-browser wait <ms>               # Wait milliseconds
agent-browser wait --text "Welcome"   # Wait for text to appear
agent-browser wait --url "**/dash"    # Wait for URL pattern
agent-browser wait --load networkidle # Wait for load state
```

### Other

```bash
agent-browser eval <js>               # Run JavaScript
agent-browser drag <src> <tgt>        # Drag and drop
agent-browser upload <sel> <files>    # Upload files
```

## Snapshot Options

```bash
agent-browser snapshot                # Full accessibility tree
agent-browser snapshot -i             # Interactive elements only
agent-browser snapshot -c             # Compact mode
agent-browser snapshot -d 3           # Limit depth to 3 levels
agent-browser snapshot -s "#main"     # Scope to CSS selector
agent-browser snapshot -i -c -d 5     # Combine options
```

## Selectors

**Refs** (recommended): `@e1`, `@e2`, etc. from snapshot
**CSS**: `#id`, `.class`, `div > button`
**Text**: `text=Submit`
**XPath**: `xpath=//button`
**Semantic**: `agent-browser find role button click --name "Submit"`

## JSON Mode

For machine-readable output:

```bash
agent-browser snapshot --json
agent-browser get text @e1 --json
agent-browser is visible @e2 --json
```

## Sessions

Run multiple isolated browser instances:

```bash
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com
agent-browser session list            # List active sessions
```

## Browser Settings

```bash
agent-browser set viewport <w> <h>    # Set viewport size
agent-browser set device "iPhone 14"  # Emulate device
agent-browser set geo <lat> <lng>     # Set geolocation
agent-browser set offline on          # Toggle offline mode
agent-browser set media dark          # Emulate color scheme
```

## Advanced

**Headers**: `agent-browser open <url> --headers '{"Authorization": "Bearer token"}'`
**Headed**: `agent-browser open <url> --headed` (show browser window)
**CDP**: `agent-browser --cdp 9222` (connect via Chrome DevTools Protocol)
**Trace**: `agent-browser trace start` / `trace stop` for debugging

## Full Reference

See [commands.md](references/commands.md) for complete command reference with examples.
