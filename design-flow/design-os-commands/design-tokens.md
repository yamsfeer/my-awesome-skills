# 设计令牌

你正在帮助用户为产品选择颜色和排版。这些设计令牌将在所有界面设计和应用外壳中统一使用。

## 第一步：检查前提条件

首先，验证产品概述是否存在：

读取 `/product/product-overview.md` 了解产品是什么。

如果不存在：

"在定义设计系统之前，您需要先确立产品愿景。请先运行 `/product-vision`。"

如果前提条件缺失，停止于此。

## 第二步：说明流程

"让我们为 **[产品名称]** 定义视觉风格。

我将帮您选择：
1. **颜色** — 主色调、辅色调和中性色
2. **排版** — 标题、正文和代码的字体

这些将统一应用于您所有的界面设计和应用外壳。

您有现成的品牌色或字体想法，还是希望我提供建议？"

等待他们的回复。

## 第三步：选择颜色

帮助用户从 Tailwind 内置调色板中选择。根据他们的产品类型提供选项：

"对于颜色，我们将从 Tailwind 调色板中选取，以便与您的界面设计无缝配合。

**主色调**（主要强调色、按钮、链接）：
常见选择：`blue`、`indigo`、`violet`、`emerald`、`teal`、`amber`、`rose`、`lime`

**辅色调**（互补强调色、标签、高亮）：
应与主色调相搭——通常是不同色调或中性变体

**中性色**（背景、文字、边框）：
选项：`slate`（冷灰）、`gray`（纯灰）、`zinc`（略暖）、`neutral`、`stone`（暖灰）

基于 [产品名称]，我建议：
- **主色调：** [建议] — [适合原因]
- **辅色调：** [建议] — [搭配原因]
- **中性色：** [建议] — [适用原因]

哪种方案最适合您的产品？"

如果他们不确定，使用 AskUserQuestion 收集偏好：

- "您想要什么风格？专业、活泼、现代还是极简？"
- "有哪些颜色是您一定要避免的？"
- "亮色模式、深色模式还是两者都要？"

## 第四步：选择排版

帮助用户选择 Google 字体：

"对于排版，我们将使用 Google 字体，便于在网页中集成。

**标题字体**（标题、章节标题）：
热门选择：`DM Sans`、`Inter`、`Poppins`、`Manrope`、`Space Grotesk`、`Outfit`

**正文字体**（段落、界面文字）：
通常与标题相同，或选用：`Inter`、`Source Sans 3`、`Nunito Sans`、`Open Sans`

**等宽字体**（代码、技术内容）：
选项：`IBM Plex Mono`、`JetBrains Mono`、`Fira Code`、`Source Code Pro`

针对 [产品名称] 我的建议：
- **标题：** [建议] — [原因]
- **正文：** [建议] — [原因]
- **等宽：** [建议] — [原因]

您更倾向于哪种？"

## 第五步：展示最终选择

一旦他们做出决定：

"这是您的设计系统：

**颜色：**
- 主色调：`[颜色]`
- 辅色调：`[颜色]`
- 中性色：`[颜色]`

**排版：**
- 标题：[字体名称]
- 正文：[字体名称]
- 等宽：[字体名称]

看起来不错吗？准备好保存了吗？"

## 第六步：创建文件

确认后，创建两个文件：

**文件 1：** `/product/design-system/colors.json`
```json
{
  "primary": "[颜色]",
  "secondary": "[颜色]",
  "neutral": "[颜色]"
}
```

**文件 2：** `/product/design-system/typography.json`
```json
{
  "heading": "[字体名称]",
  "body": "[字体名称]",
  "mono": "[字体名称]"
}
```

## 第七步：确认完成

告知用户：

"我已保存您的设计令牌：
- `/product/design-system/colors.json`
- `/product/design-system/typography.json`

**您的调色板：**
- 主色调：`[颜色]` — 用于按钮、链接、关键操作
- 辅色调：`[颜色]` — 用于标签、高亮、次要元素
- 中性色：`[颜色]` — 用于背景、文字、边框

**您的字体：**
- [标题字体] 用于标题
- [正文字体] 用于正文
- [等宽字体] 用于代码

这些将在为您的模块创建界面设计时使用。

下一步：运行 `/design-shell` 设计应用的导航和布局。"

## 参考：Tailwind 调色板

可用颜色（每种颜色有 50-950 的色阶）：
- **暖色系：** `red`、`orange`、`amber`、`yellow`、`lime`
- **冷色系：** `green`、`emerald`、`teal`、`cyan`、`sky`、`blue`
- **紫色系：** `indigo`、`violet`、`purple`、`fuchsia`、`pink`、`rose`
- **中性色：** `slate`、`gray`、`zinc`、`neutral`、`stone`

## 参考：热门 Google 字体搭配

- **现代简洁：** DM Sans + DM Sans + IBM Plex Mono
- **专业风格：** Inter + Inter + JetBrains Mono
- **友好亲切：** Nunito Sans + Nunito Sans + Fira Code
- **粗犷现代：** Space Grotesk + Inter + Source Code Pro
- **编辑风格：** Playfair Display + Source Sans 3 + IBM Plex Mono
- **科技感：** JetBrains Mono + Inter + JetBrains Mono

## 重要说明

- 颜色应使用 Tailwind 调色板名称（而非十六进制代码）
- 字体应使用确切的 Google Fonts 名称
- 建议应与产品类型相关
- 等宽字体是可选的，但建议用于任何包含代码/技术内容的产品
- 设计令牌仅应用于界面设计——Design OS 应用本身保持独立的视觉风格
