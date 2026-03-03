---
name: obsidian-cli-op
description: 当用户需要使用 Obsidian CLI 操作笔记时触发此 skill。触发场景包括：用户提到 "obsidian"、"ob" 或 "笔记" 并想要执行某个操作，用户想要创建、读取、更新、删除笔记文件等等。此 skill 提供 Obsidian CLI 的完整命令参考和使用指导。
---

# Obsidian CLI 使用指南

## 全局选项

所有命令都支持以下全局选项：

- `vault=<name>` - 指定要操作的仓库名称

## 常用命令速查

### 文件操作

| 操作        | 命令                                            | 示例                                             |
| ----------- | ----------------------------------------------- | ------------------------------------------------ |
| 创建文件    | `obsidian create name=<文件名> content=<内容>`  | `obsidian create name="新笔记" content="# 标题"` |
| 读取文件    | `obsidian read file=<文件名>`                   | `obsidian read file="新笔记"`                    |
| 追加内容    | `obsidian append file=<文件名> content=<内容>`  | `obsidian append file="新笔记" content="新段落"` |
| 前置内容    | `obsidian prepend file=<文件名> content=<内容>` | `obsidian prepend file="新笔记" content="前言"`  |
| 删除文件    | `obsidian delete file=<文件名>`                 | `obsidian delete file="旧笔记"`                  |
| 移动/重命名 | `obsidian move file=<原文件名> to=<目标路径>`   | `obsidian move file="笔记" to="文件夹/笔记"`     |
| 打开文件    | `obsidian open file=<文件名>`                   | `obsidian open file="笔记"`                      |

### 搜索

| 操作         | 命令                                     | 示例                                   |
| ------------ | ---------------------------------------- | -------------------------------------- |
| 全文搜索     | `obsidian search query=<关键词>`         | `obsidian search query="重要"`         |
| 带上下文搜索 | `obsidian search:context query=<关键词>` | `obsidian search:context query="会议"` |
| 列出所有文件 | `obsidian files`                         | `obsidian files`                       |
| 按文件夹筛选 | `obsidian files folder=<文件夹>`         | `obsidian files folder="项目"`         |

### 日记管理

| 操作       | 命令                                    | 示例                                            |
| ---------- | --------------------------------------- | ----------------------------------------------- |
| 打开日记   | `obsidian daily`                        | `obsidian daily`                                |
| 追加到日记 | `obsidian daily:append content=<内容>`  | `obsidian daily:append content="今天完成了..."` |
| 前置到日记 | `obsidian daily:prepend content=<内容>` | `obsidian daily:prepend content="计划："`       |
| 读取日记   | `obsidian daily:read`                   | `obsidian daily:read`                           |

### 任务管理

| 操作         | 命令                                             | 示例                                      |
| ------------ | ------------------------------------------------ | ----------------------------------------- |
| 列出任务     | `obsidian tasks`                                 | `obsidian tasks`                          |
| 列出待办     | `obsidian tasks todo`                            | `obsidian tasks todo`                     |
| 列出已完成   | `obsidian tasks done`                            | `obsidian tasks done`                     |
| 切换任务状态 | `obsidian task file=<文件名> line=<行号> toggle` | `obsidian task file="笔记" line=5 toggle` |
| 标记完成     | `obsidian task file=<文件名> line=<行号> done`   | `obsidian task file="笔记" line=5 done`   |

### 标签与属性

| 操作         | 命令                                                           | 示例                                                          |
| ------------ | -------------------------------------------------------------- | ------------------------------------------------------------- |
| 列出所有标签 | `obsidian tags`                                                | `obsidian tags`                                               |
| 查看标签详情 | `obsidian tag name=<标签名>`                                   | `obsidian tag name="重要"`                                    |
| 列出所有属性 | `obsidian properties`                                          | `obsidian properties`                                         |
| 读取属性     | `obsidian property:read name=<属性名> file=<文件名>`           | `obsidian property:read name="status" file="笔记"`            |
| 设置属性     | `obsidian property:set name=<属性名> value=<值> file=<文件名>` | `obsidian property:set name="tags" value="#工作" file="笔记"` |

### 链接相关

| 操作         | 命令                               | 示例                             |
| ------------ | ---------------------------------- | -------------------------------- |
| 查看出链     | `obsidian links file=<文件名>`     | `obsidian links file="笔记"`     |
| 查看反向链接 | `obsidian backlinks file=<文件名>` | `obsidian backlinks file="笔记"` |
| 查找孤立文件 | `obsidian orphans`                 | `obsidian orphans`               |
| 查找死链文件 | `obsidian deadends`                | `obsidian deadends`              |

## 高级用法

### 模板使用

```bash
# 列出模板
obsidian templates

# 读取模板
obsidian template:read name="会议模板"

# 插入模板到当前文件
obsidian template:insert name="会议模板"
```

### 仓库管理

```bash
# 查看仓库信息
obsidian vault

# 列出所有仓库
obsidian vaults

# 指定仓库执行命令
obsidian create name="笔记" vault="个人"
```

### 输出格式

许多命令支持 `format` 参数：

- `format=json` - JSON 格式
- `format=csv` - CSV 格式
- `format=tsv` - TSV 格式
- `format=md` - Markdown 格式

例如：`obsidian tags format=json`

## 特殊字符处理

- 值中包含空格时用引号包裹：`name="我的笔记"`
- 内容中的换行用 `\n` 表示
- 内容中的制表符用 `\t` 表示

## 使用建议

1. **文件定位**：可以通过 `file=<文件名>`（模糊匹配）或 `path=<路径>`（精确路径）指定文件
2. **默认文件**：很多命令在不指定文件时会默认操作当前活动文件
3. **批量操作**：结合 shell 脚本可以实现批量操作笔记
