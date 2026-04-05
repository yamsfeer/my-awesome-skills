#!/usr/bin/env python3
"""
Cookie Helper for yt-dlp
将浏览器 cookie 转换为 yt-dlp 所需的 Netscape 格式文件。

支持两种输入格式：
1. 纯文本（浏览器 DevTools 中复制的 Cookie 请求头内容）
   例如：SESSDATA=abc; bili_jct=def; DedeUserID=123
2. JSON 格式（Cookie Editor 等浏览器插件导出）
   例如：[{"name": "SESSDATA", "value": "abc", "domain": ".bilibili.com", ...}]

用法：
  # 纯文本 cookie
  python cookie_helper.py --text "SESSDATA=xxx; bili_jct=xxx" --output /tmp/cookies.txt

  # JSON 字符串
  python cookie_helper.py --json '[{"name":"SESSDATA","value":"xxx",...}]' --output /tmp/cookies.txt

  # JSON 文件
  python cookie_helper.py --json-file /path/to/cookies.json --output /tmp/cookies.txt
"""

import argparse
import json
import sys
import time
from pathlib import Path


def parse_text_cookies(text: str, default_domain: str = ".bilibili.com") -> list[dict]:
    """解析纯文本 cookie（分号分隔的 name=value 对）"""
    cookies = []
    for part in text.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            name, _, value = part.partition("=")
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": default_domain,
                "path": "/",
                "secure": True,
                "httpOnly": False,
                "expirationDate": int(time.time()) + 86400 * 365,
            })
        else:
            print(f"警告：跳过无效 cookie 片段：{part!r}", file=sys.stderr)
    return cookies


def parse_json_cookies(json_str: str) -> list[dict]:
    """解析 JSON 格式的 cookie（浏览器插件导出格式）"""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"错误：JSON 解析失败：{e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("错误：JSON 格式应为数组（[...]）", file=sys.stderr)
        sys.exit(1)

    return data


def to_netscape_line(cookie: dict) -> str:
    """将单个 cookie 字典转换为 Netscape 格式的一行文本"""
    domain = cookie.get("domain", ".bilibili.com")
    # Netscape 格式要求 domain 以 . 开头时，include_subdomains 为 TRUE
    include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
    path = cookie.get("path", "/")
    secure = "TRUE" if cookie.get("secure", False) else "FALSE"
    # expirationDate 可能是 None 或 0，设为一年后
    expiry = cookie.get("expirationDate") or cookie.get("expiry") or (int(time.time()) + 86400 * 365)
    name = cookie.get("name", "")
    value = cookie.get("value", "")

    # Netscape 格式：domain \t include_subdomains \t path \t secure \t expiry \t name \t value
    return f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{int(expiry)}\t{name}\t{value}"


def write_netscape_cookies(cookies: list[dict], output_path: str) -> int:
    """将 cookie 列表写入 Netscape 格式文件，返回写入的 cookie 数量"""
    lines = ["# Netscape HTTP Cookie File", "# 由 cookie_helper.py 自动生成\n"]
    written = 0
    for cookie in cookies:
        name = cookie.get("name", "").strip()
        value = cookie.get("value", "").strip()
        if not name:
            continue
        lines.append(to_netscape_line(cookie))
        written += 1

    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return written


def guess_default_domain(text: str) -> str:
    """根据 cookie 内容猜测默认域名"""
    bilibili_keys = {"SESSDATA", "bili_jct", "DedeUserID", "buvid3", "buvid4"}
    keys = {part.split("=")[0].strip() for part in text.split(";") if "=" in part}
    if keys & bilibili_keys:
        return ".bilibili.com"
    return ".youtube.com"


def main():
    parser = argparse.ArgumentParser(
        description="将浏览器 cookie 转换为 yt-dlp 所需的 Netscape 格式文件"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="纯文本 cookie 字符串（如：SESSDATA=xxx; bili_jct=xxx）")
    source.add_argument("--json", help="JSON 格式的 cookie 字符串")
    source.add_argument("--json-file", help="JSON 格式的 cookie 文件路径")

    parser.add_argument("--output", required=True, help="输出文件路径（如 /tmp/cookies.txt）")
    parser.add_argument("--domain", default=None, help="默认域名（纯文本模式下使用，默认自动猜测）")

    args = parser.parse_args()

    if args.text:
        domain = args.domain or guess_default_domain(args.text)
        cookies = parse_text_cookies(args.text, default_domain=domain)
        print(f"解析到 {len(cookies)} 个 cookie（域名：{domain}）")
    elif args.json:
        cookies = parse_json_cookies(args.json)
        print(f"从 JSON 字符串解析到 {len(cookies)} 个 cookie")
    else:  # json-file
        json_path = Path(args.json_file)
        if not json_path.exists():
            print(f"错误：文件不存在：{args.json_file}", file=sys.stderr)
            sys.exit(1)
        cookies = parse_json_cookies(json_path.read_text(encoding="utf-8"))
        print(f"从文件 {args.json_file} 解析到 {len(cookies)} 个 cookie")

    if not cookies:
        print("错误：未解析到任何有效 cookie", file=sys.stderr)
        sys.exit(1)

    written = write_netscape_cookies(cookies, args.output)
    print(f"已写入 {written} 个 cookie 到 {args.output}")
    print(f"\n使用方法：yt-dlp --cookies {args.output} [其他参数] URL")
    print(f"下载完成后请删除：rm -f {args.output}")


if __name__ == "__main__":
    main()
