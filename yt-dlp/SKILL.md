---
name: yt-dlp
description: 使用 yt-dlp 下载 Bilibili 或 YouTube 的视频、音频、字幕。当用户提到"下载视频"、"下载B站"、"下载油管"、"下载bilibili"、"下载youtube"、"保存视频"、"提取音频"、"下载字幕"等场景时使用此技能。支持 Bilibili cookie 登录（纯文本或 JSON 格式均可），处理清晰度选择、音频提取、字幕下载等常见需求。即使用户只是说"帮我下载这个视频"并附上 bilibili 或 youtube 链接，也应触发此技能。
---

# yt-dlp 视频下载助手

帮助用户通过 yt-dlp 下载 Bilibili 和 YouTube 的视频、音频、字幕。

## 快速决策流程

收到下载请求后，按以下顺序判断：

1. **链接来源** → Bilibili 还是 YouTube？
2. **下载内容** → 视频 / 仅音频 / 仅字幕？
3. **Bilibili 是否需要登录** → 用户有 cookie 吗？
4. **输出路径** → 保存到哪里？（未指定则用当前目录）

---

## Cookie 处理（Bilibili 必读）

Bilibili 高清视频（720P 及以上）通常需要登录。yt-dlp 接受 **Netscape 格式** 的 cookie 文件（`--cookies`），不能直接接受字符串。

使用 `scripts/cookie_helper.py` 将用户提供的 cookie 写入临时文件：

```bash
# 用户提供纯文本 cookie（浏览器 DevTools 复制的 "Cookie:" 请求头内容）
python scripts/cookie_helper.py --text "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx" --output /tmp/bili_cookies.txt

# 用户提供 JSON 格式（从 Cookie Editor 等浏览器插件导出）
python scripts/cookie_helper.py --json '[{"name":"SESSDATA","value":"xxx","domain":".bilibili.com",...}]' --output /tmp/bili_cookies.txt

# 用户提供 JSON 文件路径
python scripts/cookie_helper.py --json-file /path/to/cookies.json --output /tmp/bili_cookies.txt
```

下载完成后删除临时 cookie 文件：`rm -f /tmp/bili_cookies.txt`

### 两种 Cookie 格式说明

**纯文本格式**（从浏览器复制 Cookie 请求头）：
```
SESSDATA=abc123; bili_jct=def456; DedeUserID=789
```

**JSON 格式**（Cookie Editor 等插件导出）：
```json
[
  {"name": "SESSDATA", "value": "abc123", "domain": ".bilibili.com", "path": "/", "secure": true, "expirationDate": 1700000000},
  {"name": "bili_jct", "value": "def456", "domain": ".bilibili.com", "path": "/"}
]
```

---

## 常用下载命令

### 1. 下载视频（默认最佳质量）

```bash
# YouTube
yt-dlp -o "%(title)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"

# Bilibili（无需登录，最高可能只有360P/480P）
yt-dlp -o "%(title)s.%(ext)s" "https://www.bilibili.com/video/BV..."

# Bilibili（带 cookie，可下载高清）
yt-dlp --cookies /tmp/bili_cookies.txt -o "%(title)s.%(ext)s" "https://www.bilibili.com/video/BV..."
```

### 2. 查看可用清晰度

```bash
yt-dlp -F "URL"
# 或带 cookie
yt-dlp --cookies /tmp/bili_cookies.txt -F "URL"
```

### 3. 指定清晰度下载

```bash
# 下载 1080P（Bilibili 格式 ID 通常为 80）
yt-dlp --cookies /tmp/bili_cookies.txt -f 80 -o "%(title)s.%(ext)s" "URL"

# YouTube 指定 1080P + 最佳音频，合并为 mp4
yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]" -o "%(title)s.%(ext)s" "URL"
```

### 4. 仅下载音频（提取 MP3）

```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" "URL"
```

音频质量说明：`--audio-quality 0` 是最高质量，`9` 是最低。

### 5. 下载字幕

```bash
# 先列出所有可用字幕，确认语言代码
yt-dlp --list-subs "URL"

# 下载指定语言字幕（不下载视频）
yt-dlp --write-subs --sub-langs "LANG_CODE" --skip-download -o "%(title)s.%(ext)s" "URL"

# 下载视频同时附带字幕
yt-dlp --write-subs --sub-langs "LANG_CODE" -o "%(title)s.%(ext)s" "URL"

# 嵌入字幕到视频文件（mp4 格式）
yt-dlp --embed-subs --sub-langs "LANG_CODE" -o "%(title)s.%(ext)s" "URL"
```

**Bilibili 常见字幕语言代码：**

| 代码 | 说明 |
|------|------|
| `ai-zh` | AI 自动生成的中文字幕（最常见） |
| `danmaku` | 弹幕（XML 格式，不是字幕） |
| `zh-Hans` | 人工简体中文字幕（创作者上传，较少见） |

> **注意**：Bilibili 视频不是都有字幕。先用 `--list-subs` 确认可用语言，再下载。
> YouTube 字幕语言代码通常是 `zh-Hans`、`zh-CN`、`en` 等标准代码。

### 6. 下载播放列表

```bash
# 整个播放列表
yt-dlp -o "%(playlist_index)s-%(title)s.%(ext)s" "PLAYLIST_URL"

# 只下载前 5 个
yt-dlp --playlist-end 5 -o "%(playlist_index)s-%(title)s.%(ext)s" "PLAYLIST_URL"
```

### 7. 指定输出目录

```bash
yt-dlp -o "/path/to/dir/%(title)s.%(ext)s" "URL"
```

---

## Bilibili 常见格式 ID

| 格式ID | 清晰度 | 备注 |
|--------|--------|------|
| 6      | 240P   | 无需登录 |
| 16     | 360P   | 无需登录 |
| 32     | 480P   | 无需登录 |
| 64     | 720P   | 需要登录 |
| 74     | 720P60 | 需要登录 |
| 80     | 1080P  | 需要登录 |
| 112    | 1080P+ | 需要大会员 |
| 116    | 1080P60| 需要大会员 |
| 120    | 4K     | 需要大会员 |

---

## 执行步骤模板

```
1. 确认链接、平台、下载类型
2. 若 Bilibili 且用户有 cookie → 运行 cookie_helper.py 生成临时文件
3. 若用户未指定格式 → 先运行 yt-dlp -F URL 列出可用格式供参考
4. 执行下载命令
5. 确认文件已生成（ls -lh）
6. 删除临时 cookie 文件（若有）
7. 告知用户文件路径
```

---

## 常见问题处理

**问题：下载失败报 403 或 "requested format not available"**
→ 可能需要 cookie 登录，或该格式需要大会员

**问题：合并音视频失败**
→ 检查是否安装了 ffmpeg：`which ffmpeg`；若无则 `brew install ffmpeg`

**问题：字幕是 vtt 格式，想要 srt**
→ 添加 `--convert-subs srt` 参数

**问题：下载速度慢**
→ 添加 `--concurrent-fragments 4` 提升并发分片数

**问题：Bilibili cookie 格式确认**
→ 运行 `yt-dlp --cookies /tmp/bili_cookies.txt --simulate URL` 测试是否登录成功
