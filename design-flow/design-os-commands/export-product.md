# 导出产品

你正在帮助用户将完整的产品设计导出为移交包，用于实现阶段。这将生成将界面设计集成到真实代码库所需的所有文件。

## 第一步：检查前提条件

验证最低要求是否满足：

**必需：**
- `/product/product-overview.md` — 产品概述
- `/product/product-roadmap.md` — 已定义的模块
- `src/sections/[模块id]/` 中至少一个模块的界面设计

**推荐（如缺失则显示警告）：**
- `/product/data-shape/data-shape.md` — 产品实体
- `/product/design-system/colors.json` — 颜色令牌
- `/product/design-system/typography.json` — 排版令牌
- `src/shell/components/AppShell.tsx` — 应用外壳

如果必需文件缺失：

"要导出您的产品，您至少需要：
- 产品概述（`/product-vision`）
- 包含模块的路线图（`/product-roadmap`）
- 至少一个模块的界面设计

请先完成这些步骤。"

如果必需文件缺失，停止于此。

如果推荐文件缺失，显示警告但继续：

"注意：以下推荐项目缺失：
- [ ] 产品实体 — 运行 `/data-shape` 以确保实体命名一致
- [ ] 设计令牌 — 运行 `/design-tokens` 以确保样式一致
- [ ] 应用外壳 — 运行 `/design-shell` 以获取导航结构

您可以在没有这些的情况下继续，但它们有助于确保完整的移交。"

## 第二步：收集导出信息

读取所有相关文件：

1. `/product/product-overview.md` — 产品名称、描述、功能
2. `/product/product-roadmap.md` — 按顺序排列的模块列表
3. `/product/data-shape/data-shape.md`（如存在）
4. `/product/design-system/colors.json`（如存在）
5. `/product/design-system/typography.json`（如存在）
6. `/product/shell/spec.md`（如存在）
7. 每个模块：`spec.md`、`data.json`、`types.ts`
8. 列出 `src/sections/` 和 `src/shell/` 中的界面设计组件

## 第三步：创建导出目录结构

创建 `product-plan/` 目录，结构如下：

```
product-plan/
├── README.md                    # 快速入门指南
├── product-overview.md          # 产品摘要（始终提供）
│
├── prompts/                     # 可直接使用的提示词
│   ├── one-shot-prompt.md       # 完整实现提示词
│   └── section-prompt.md        # 按模块实现的提示词模板
│
├── instructions/                # 实现说明
│   ├── one-shot-instructions.md # 所有里程碑合并版
│   └── incremental/             # 按里程碑逐步实现
│       ├── 01-shell.md
│       ├── 02-[第一个模块].md
│       ├── 03-[第二个模块].md
│       └── ...
│
├── design-system/               # 设计令牌
│   ├── tokens.css
│   ├── tailwind-colors.md
│   └── fonts.md
│
├── data-shapes/                 # UI 数据契约
│   ├── README.md
│   └── overview.ts
│
├── shell/                       # 外壳组件
│   ├── README.md
│   ├── components/
│   │   ├── AppShell.tsx
│   │   ├── MainNav.tsx
│   │   ├── UserMenu.tsx
│   │   └── index.ts
│   └── screenshot.png（如存在）
│
└── sections/                    # 模块组件
    └── [模块id]/
        ├── README.md
        ├── tests.md               # UI 行为测试规格
        ├── components/
        │   ├── [组件].tsx
        │   └── index.ts
        ├── types.ts
        ├── sample-data.json
        └── screenshot.png（如存在）
```

## 第四步：生成 product-overview.md

创建 `product-plan/product-overview.md`：

```markdown
# [产品名称] — 产品概述

## 摘要

[来自 product-overview.md 的产品描述]

## 规划模块

[来自路线图的有序模块列表及描述]

1. **[模块 1]** — [描述]
2. **[模块 2]** — [描述]
...

## 产品实体

[如果数据结构存在：列出实体名称和简短描述]
[如果不存在："实体将在实现阶段定义"]

## 设计系统

**颜色：**
- 主色调：[颜色或"未定义"]
- 辅色调：[颜色或"未定义"]
- 中性色：[颜色或"未定义"]

**排版：**
- 标题：[字体或"未定义"]
- 正文：[字体或"未定义"]
- 等宽：[字体或"未定义"]

## 实现顺序

按以下里程碑构建此产品：

1. **外壳** — 设置设计令牌和应用外壳
2. **[模块 1]** — [简短描述]
3. **[模块 2]** — [简短描述]
...

每个里程碑在 `product-plan/instructions/` 中都有专属说明文档。
```

## 第五步：生成里程碑说明

每个里程碑说明文件应以以下前言开头（根据里程碑具体细节调整）：

```markdown
---

## 关于此次移交

**您收到的内容：**
- 完成的界面设计（带完整样式的 React 组件）
- 产品需求和用户流程规格
- 设计系统令牌（颜色、排版）
- 展示组件期望数据形状的示例数据
- 专注于用户可见行为的测试规格

**您的工作：**
- 将这些组件集成到您的应用中
- 将回调 props 连接到您的路由和业务逻辑
- 用后端真实数据替换示例数据
- 实现加载、错误和空状态

这些组件基于 props——它们接受数据并触发回调。后端架构、数据层和业务逻辑的实现方式由您决定。

---
```

### 01-shell.md

放置在 `product-plan/instructions/incremental/01-shell.md`：

```markdown
# 里程碑 1：外壳

> **需同时提供：** `product-overview.md`
> **前提条件：** 无

[在此包含上述前言]

## 目标

设置设计令牌和应用外壳——包裹所有模块的持久界面框架。

## 需要实现的内容

### 1. 设计令牌

[如果设计令牌存在：]
使用以下令牌配置您的样式系统：

- 参见 `product-plan/design-system/tokens.css` 了解 CSS 自定义属性
- 参见 `product-plan/design-system/tailwind-colors.md` 了解 Tailwind 配置
- 参见 `product-plan/design-system/fonts.md` 了解 Google Fonts 设置

[如果不存在：]
根据您的品牌规范定义您自己的设计令牌。

### 2. 应用外壳

[如果外壳存在：]

从 `product-plan/shell/components/` 复制外壳组件到您的项目：

- `AppShell.tsx` — 主布局包装器
- `MainNav.tsx` — 导航组件
- `UserMenu.tsx` — 带头像的用户菜单

**连接导航：**

将导航连接到您的路由：

[列出来自外壳规格的导航项]

**用户菜单：**

用户菜单需要：
- 用户名
- 头像 URL（可选）
- 退出登录回调

[如果外壳不存在：]

自行设计和实现应用外壳，包含：
- 所有模块的导航
- 用户菜单
- 响应式布局

## 参考文件

- `product-plan/design-system/` — 设计令牌
- `product-plan/shell/README.md` — 外壳设计意图
- `product-plan/shell/components/` — 外壳 React 组件
- `product-plan/shell/screenshot.png` — 外壳视觉参考

## 完成标准

- [ ] 设计令牌已配置
- [ ] 外壳带导航渲染正常
- [ ] 导航链接到正确路由
- [ ] 用户菜单显示用户信息
- [ ] 移动端响应式正常
```

### [NN]-[模块id].md（每个模块一份）

放置在 `product-plan/instructions/incremental/[NN]-[模块id].md`（第一个模块从 02 开始）：

```markdown
# 里程碑 [N]：[模块标题]

> **需同时提供：** `product-overview.md`
> **前提条件：** 里程碑 1（外壳）已完成，以及所有之前的模块里程碑

[在此包含上述前言]

## 目标

实现 [模块标题] 功能——[来自路线图的简短描述]。

## 概述

[一段描述此模块用户可以做什么的话。聚焦于用户视角和他们从此功能获得的价值。从 spec.md 概述提取。]

**核心功能：**
- [要点 1 — 例如："查看带状态指示器的所有项目列表"]
- [要点 2 — 例如："用名称、描述和截止日期创建新项目"]
- [要点 3 — 例如："内联编辑现有项目详情"]
- [要点 4 — 例如："带确认的项目删除"]
- [要点 5 — 例如："按状态筛选或按名称搜索项目"]

[列出 UI 组件支持的 3-6 个核心功能]

## 提供的组件

从 `product-plan/sections/[模块id]/components/` 复制模块组件：

[列出组件及简短描述]

## Props 参考

组件期望以下数据形状（完整定义参见 `types.ts`）：

**数据 props：**

[来自 types.ts 的关键类型——简短展示主要接口]

**回调 props：**

| 回调 | 触发时机 |
|------|---------|
| `onView` | 用户点击查看详情 |
| `onEdit` | 用户点击编辑 |
| `onDelete` | 用户点击删除 |
| `onCreate` | 用户点击新建 |

[根据实际 Props 接口调整]

## 预期用户流程

完整实现后，用户应能完成以下流程：

### 流程 1：[主要流程名称——例如"创建新项目"]

1. 用户[起始操作——例如"点击'新建项目'按钮"]
2. 用户[下一步——例如"填写项目名称和描述"]
3. 用户[下一步——例如"点击'创建'保存"]
4. **结果：** [预期结果——例如"新项目出现在列表中"]

### 流程 2：[次要流程名称——例如"编辑现有项目"]

1. 用户[起始操作——例如"点击某个项目行"]
2. 用户[下一步——例如"修改项目详情"]
3. 用户[下一步——例如"点击'保存'确认修改"]
4. **结果：** [预期结果——例如"项目就地更新"]

### 流程 3：[附加流程——例如"删除项目"]

1. 用户[起始操作——例如"点击项目上的删除图标"]
2. 用户[下一步——例如"在弹窗中确认删除"]
3. **结果：** [预期结果——例如"项目从列表移除，如是最后一项则显示空状态"]

[包含 2-4 个涵盖此模块主要用户旅程的流程。参考组件中具体的界面元素和按钮标签。]

## 空状态

组件包含空状态设计。请确保处理以下情况：

- **尚无数据：** 当主列表/集合为空时显示空状态 UI
- **无关联记录：** 处理关联记录不存在的情况（例如没有任务的项目）
- **首次使用体验：** 通过清晰的 CTA 引导用户创建第一条记录

## 测试

参见 `product-plan/sections/[模块id]/tests.md` 了解覆盖以下内容的 UI 行为测试规格：
- 用户流程成功和失败路径
- 空状态渲染
- 组件交互和边界情况

## 参考文件

- `product-plan/sections/[模块id]/README.md` — 功能概述和设计意图
- `product-plan/sections/[模块id]/tests.md` — UI 行为测试规格
- `product-plan/sections/[模块id]/components/` — React 组件
- `product-plan/sections/[模块id]/types.ts` — TypeScript 接口
- `product-plan/sections/[模块id]/sample-data.json` — 测试数据
- `product-plan/sections/[模块id]/screenshot.png` — 视觉参考

## 完成标准

- [ ] 组件使用真实数据正常渲染
- [ ] 无记录时正确显示空状态
- [ ] 所有回调 props 已连接到正常工作的功能
- [ ] 用户可以端到端完成所有预期流程
- [ ] 与视觉设计一致（参见截图）
- [ ] 移动端响应式正常
```

## 第六步：生成 one-shot-instructions.md

创建 `product-plan/instructions/one-shot-instructions.md`，将所有里程碑内容合并为一个文档。在最顶部包含前言：

```markdown
# [产品名称] — 完整实现说明

---

## 关于此次移交

**您收到的内容：**
- 完成的界面设计（带完整样式的 React 组件）
- 产品需求和用户流程规格
- 设计系统令牌（颜色、排版）
- 展示组件期望数据形状的示例数据
- 专注于用户可见行为的测试规格

**您的工作：**
- 将这些组件集成到您的应用中
- 将回调 props 连接到您的路由和业务逻辑
- 用后端真实数据替换示例数据
- 实现加载、错误和空状态

这些组件基于 props——它们接受数据并触发回调。后端架构、数据层和业务逻辑的实现方式由您决定。

---

## 测试

每个模块都包含一个 `tests.md` 文件，内含 UI 行为测试规格。这些规格**与框架无关**——请根据您的测试设置进行调整。

**对于每个模块：**
1. 阅读 `product-plan/sections/[模块id]/tests.md`
2. 为关键用户流程编写测试（成功和失败路径）
3. 实现功能使测试通过
4. 在保持测试绿色的情况下重构

---

[包含 product-overview.md 的内容]

---

# 里程碑 1：外壳

[包含 01-shell.md 的内容，但**不包含**前言——它已在顶部。包括设计令牌和应用外壳。]

---

# 里程碑 2：[第一个模块名称]

[包含第一个模块移交内容，**不包含**前言]

---

# 里程碑 3：[第二个模块名称]

[包含第二个模块移交内容，**不包含**前言]

[对所有模块重复，里程碑编号递增]
```

## 第七步：复制并转换组件

### 外壳组件

从 `src/shell/components/` 复制到 `product-plan/shell/components/`：

- 将导入路径从 `@/...` 转换为相对路径
- 移除任何特定于 Design OS 的导入
- 确保组件自包含

### 模块组件

对于每个模块，从 `src/sections/[模块id]/components/` 复制到 `product-plan/sections/[模块id]/components/`：

- 转换导入路径：
  - `@/../product/sections/[模块id]/types` → `../types`
- 移除特定于 Design OS 的导入
- 仅保留可导出组件（不含预览包装器）

### 类型文件

将 `product/sections/[模块id]/types.ts` 复制到 `product-plan/sections/[模块id]/types.ts`

### 示例数据

将 `product/sections/[模块id]/data.json` 复制到 `product-plan/sections/[模块id]/sample-data.json`

## 第八步：生成模块 README

为每个模块创建 `product-plan/sections/[模块id]/README.md`：

```markdown
# [模块标题]

## 概述

[来自 spec.md 的概述]

## 用户流程

[来自 spec.md 的用户流程]

## 设计决策

[界面设计中的重要设计选择]

## 数据形状

**实体：** [列出来自 types.ts 的实体]

**来自全局实体：** [如适用，说明使用了数据结构中的哪些实体]

## 视觉参考

参见 `screenshot.png` 了解目标界面设计。

## 提供的组件

- `[组件]` — [简短描述]
- `[子组件]` — [简短描述]

## 回调 Props

| 回调 | 触发时机 |
|------|---------|
| `onView` | 用户点击查看详情 |
| `onEdit` | 用户点击编辑 |
| `onDelete` | 用户点击删除 |
| `onCreate` | 用户点击新建 |

[根据实际 Props 接口调整]
```

## 第九步：生成模块测试说明

为每个模块创建 `product-plan/sections/[模块id]/tests.md`，内含基于模块规格、用户流程和界面设计的 UI 行为测试规格。

```markdown
# 测试规格：[模块标题]

这些测试规格**与框架无关**。请根据您的测试设置（Jest、Vitest、Playwright、Cypress、React Testing Library 等）进行调整。

## 概述

[简短描述此模块的功能和需要测试的核心功能]

---

## 用户流程测试

### 流程 1：[主要用户流程名称]

**场景：** [描述用户想要完成的目标]

#### 成功路径

**前提条件：**
- [前置条件——应用应处于什么状态]
- [要使用的示例数据——参考 types.ts 中的类型]

**步骤：**
1. 用户导航到 [页面/路由]
2. 用户看到 [具体 UI 元素——具体说明标签、文字]
3. 用户点击 [具体按钮/链接，含确切标签]
4. 用户在 [具体字段] 输入 [具体数据]
5. 用户点击 [提交按钮，含确切标签]

**预期结果：**
- [ ] [具体 UI 变化——例如"出现成功消息：'条目已创建'"]
- [ ] [数据变化——例如"新条目出现在列表中"]
- [ ] [状态变化——例如"表单被清空并重置"]
- [ ] [导航——例如"用户被重定向到 /items/:id"]

#### 失败路径：[具体失败场景]

**步骤：**
1. [与成功路径相同的步骤，或有修改]

**预期结果：**
- [ ] [错误消息——例如"出现错误消息：'无法保存，请重试。'"]
- [ ] [UI 状态——例如"表单数据被保留，不被清空"]

#### 失败路径：[验证错误]

**步骤：**
1. 用户将 [具体字段] 留空
2. 用户点击 [提交按钮]

**预期结果：**
- [ ] [验证消息——例如"字段显示错误：'名称为必填项'"]
- [ ] [表单状态——例如"表单未提交"]

---

### 流程 2：[次要用户流程名称]

[对其他流程重复相同结构]

---

## 空状态测试

### 主要空状态

**场景：** 用户尚无 [主要记录]（首次使用或全部删除）

**前提条件：**
- [主要数据集合] 为空（`[]`）

**预期结果：**
- [ ] [空状态消息可见——例如"显示标题'暂无项目'"]
- [ ] [帮助性描述——例如"显示文字'创建您的第一个项目以开始使用'"]
- [ ] [主要 CTA 可见——例如"显示按钮'创建项目'"]
- [ ] [CTA 可正常使用——例如"点击'创建项目'打开创建表单/弹窗"]

### 关联记录空状态

**场景：** [父记录] 存在但尚无 [子记录]

**前提条件：**
- [父记录] 存在且数据有效
- [子记录集合] 为空（`[]`）

**预期结果：**
- [ ] [父记录正确渲染及其数据]
- [ ] [子记录区域显示空状态——例如"任务面板中显示'暂无任务'"]
- [ ] [添加子记录的 CTA——例如"显示'添加任务'按钮"]

---

## 组件交互测试

### [组件名称]

**正确渲染：**
- [ ] [具体元素可见——例如"显示条目标题'示例条目'"]
- [ ] [数据显示——例如"显示格式化日期'2025年12月12日'"]

**用户交互：**
- [ ] [点击行为——例如"点击'编辑'按钮以条目 id 调用 onEdit"]
- [ ] [悬停行为——例如"悬停行时显示操作按钮"]
- [ ] [键盘——例如"按 Escape 键关闭弹窗"]

---

## 边界情况

- [ ] [边界情况 1——例如"对很长的条目名称进行文字截断处理"]
- [ ] [边界情况 2——例如"1 条和 100 条以上记录时均能正常工作"]
- [ ] [边界情况 3——例如"离开再返回时数据保持不变"]
- [ ] [从空到有的过渡——例如"创建第一条记录后列表正确渲染"]
- [ ] [从有到空的过渡——例如"删除最后一条记录后显示空状态"]

---

## 无障碍检查

- [ ] [所有交互元素均可通过键盘访问]
- [ ] [表单字段有关联标签]
- [ ] [错误消息会通知屏幕阅读器]
- [ ] [操作后焦点管理得当]

---

## 示例测试数据

使用 `sample-data.json` 中的数据或创建变体：

[根据 types.ts 包含 2-3 个测试可使用的示例数据对象]

```typescript
// 有数据状态
const mockItem = {
  id: "test-1",
  name: "测试条目",
  // ... 来自 types.ts 的其他字段
};

const mockItems = [mockItem, /* ... 更多条目 */];

// 空状态
const mockEmptyList = [];

const mockItemWithNoChildren = {
  id: "test-1",
  name: "测试条目",
  children: [],
};
```
```

### 编写 tests.md 的指导原则

为每个模块生成 tests.md 时：

1. **仔细阅读 spec.md** — 提取所有用户流程和需求
2. **研究界面设计组件** — 注意确切的按钮标签、字段名称、界面文字
3. **查阅 types.ts** — 了解断言所需的数据形状
4. **包含具体的界面文字** — 测试应验证确切的标签、消息、占位符
5. **覆盖成功和失败路径** — 每个操作都应测试两种情况
6. **始终测试空状态** — 无条目的主列表，无子记录的父记录
7. **断言要具体** — "显示错误"太模糊；"字段下方显示红色边框和消息'邮箱为必填项'"才够具体
8. **包含边界情况** — 边界条件，空状态和有数据状态之间的过渡
9. **与框架无关** — 描述**测试什么**（UI 行为），而非**如何编写**测试代码

## 第十步：生成设计系统文件

### tokens.css

```css
/* [产品名称] 设计令牌 */

:root {
  /* 颜色 */
  --color-primary: [Tailwind 颜色];
  --color-secondary: [Tailwind 颜色];
  --color-neutral: [Tailwind 颜色];

  /* 排版 */
  --font-heading: '[标题字体]', sans-serif;
  --font-body: '[正文字体]', sans-serif;
  --font-mono: '[等宽字体]', monospace;
}
```

### tailwind-colors.md

```markdown
# Tailwind 颜色配置

## 颜色选择

- **主色调：** `[颜色]` — 用于按钮、链接、关键强调
- **辅色调：** `[颜色]` — 用于标签、高亮、次要元素
- **中性色：** `[颜色]` — 用于背景、文字、边框

## 使用示例

主要按钮：`bg-[primary]-600 hover:bg-[primary]-700 text-white`
次要徽章：`bg-[secondary]-100 text-[secondary]-800`
中性文字：`text-[neutral]-600 dark:text-[neutral]-400`
```

### fonts.md

```markdown
# 排版配置

## Google Fonts 导入

在您的 HTML `<head>` 或 CSS 中添加：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=[标题字体]&family=[正文字体]&family=[等宽字体]&display=swap" rel="stylesheet">
```

## 字体用途

- **标题：** [标题字体]
- **正文：** [正文字体]
- **代码/技术内容：** [等宽字体]
```

## 第十一步：生成数据形状文件

### data-shapes/README.md

创建 `product-plan/data-shapes/README.md`：

```markdown
# UI 数据形状

这些类型定义了 UI 组件期望通过 props 接收的数据形状。它们代表**前端契约**——组件正确渲染所需的内容。

您如何在后端建模、存储和获取这些数据是实现决策。您可以根据自己的架构组合、拆分或扩展这些类型。

## 实体

[列出所有模块中的所有实体及简短描述]

- **[实体1]** — [描述]（用于：[模块名称]）
- **[实体2]** — [描述]（用于：[模块名称]）
- **[实体3]** — [描述]（用于：[模块名称1]、[模块名称2]）

## 按模块分类的类型

每个模块都包含自己的 `types.ts` 文件，内含完整的接口定义：

- `sections/[模块-1]/types.ts`
- `sections/[模块-2]/types.ts`
- ...

## 综合参考

参见 `overview.ts` 了解所有实体类型的汇总文件。
```

### data-shapes/overview.ts

创建 `product-plan/data-shapes/overview.ts`，汇总所有模块类型：

```typescript
// =============================================================================
// UI 数据形状——综合参考
//
// 这些类型定义了 UI 组件期望通过 props 接收的数据。
// 它们是前端契约，而非数据库模式。如何建模、存储
// 和获取这些数据是实现决策。
// =============================================================================

// -----------------------------------------------------------------------------
// 来自：sections/[模块-1]
// -----------------------------------------------------------------------------

[从 section-1/types.ts 复制实体类型——只包含数据接口，不包含 Props]

// -----------------------------------------------------------------------------
// 来自：sections/[模块-2]
// -----------------------------------------------------------------------------

[从 section-2/types.ts 复制实体类型——只包含数据接口，不包含 Props]

// [对所有模块重复]
```

仅包含数据形状接口（例如 `Invoice`、`LineItem`），不包含组件 Props 接口。Props 接口保留在每个模块自己的 `types.ts` 中。

## 第十二步：生成提示词文件

创建 `product-plan/prompts/` 目录，包含两个可直接使用的提示词文件。

### one-shot-prompt.md

创建 `product-plan/prompts/one-shot-prompt.md`：

```markdown
# 一次性实现提示词

我需要您根据我提供的详细界面设计和产品规格实现一个完整的 Web 应用。

## 说明

请仔细阅读并分析以下文件：

1. **@product-plan/product-overview.md** — 包含模块和实体概述的产品摘要
2. **@product-plan/instructions/one-shot-instructions.md** — 所有里程碑的完整实现说明

阅读后，还请查阅：
- **@product-plan/design-system/** — 颜色和排版令牌
- **@product-plan/data-shapes/** — UI 数据契约（组件期望的数据形状）
- **@product-plan/shell/** — 应用外壳组件
- **@product-plan/sections/** — 所有模块组件、类型、示例数据和测试规格

## 开始前

查阅所有提供的文件，然后向我提出关于以下方面的澄清性问题：

1. **我的技术栈** — 我使用的框架、语言和工具，以及现有代码库约定
2. **身份验证与用户** — 用户应如何注册、登录，以及存在哪些权限
3. **产品需求** — 规格或用户流程中需要澄清的任何内容
4. **其他任何问题** — 实现前您需要了解的任何信息

最后，询问我是否有关于此次实现的其他说明。

回答您的问题后，请在编码前制定全面的实现计划。

```

### section-prompt.md

创建 `product-plan/prompts/section-prompt.md`：

```markdown
# 模块实现提示词

## 定义模块变量

- **SECTION_NAME** = [可读名称，例如"发票"或"项目仪表板"]
- **SECTION_ID** = [sections/ 中的文件夹名称，例如"invoices"或"project-dashboard"]
- **NN** = [里程碑编号，例如"02"或"03"——模块从 02 开始，因为 01 是外壳]

---

我需要您实现我应用中的 **SECTION_NAME** 模块。

## 说明

请仔细阅读并分析以下文件：

1. **@product-plan/product-overview.md** — 用于整体背景的产品摘要
2. **@product-plan/instructions/incremental/NN-SECTION_ID.md** — 此模块的具体实现说明

还请查阅模块资源：
- **@product-plan/sections/SECTION_ID/README.md** — 功能概述和设计意图
- **@product-plan/sections/SECTION_ID/tests.md** — UI 行为测试规格
- **@product-plan/sections/SECTION_ID/components/** — 需要集成的 React 组件
- **@product-plan/sections/SECTION_ID/types.ts** — TypeScript 接口
- **@product-plan/sections/SECTION_ID/sample-data.json** — 测试数据

## 开始前

查阅所有提供的文件，然后向我提出关于以下方面的澄清性问题：

1. **集成** — 此模块如何连接到现有功能和已构建的任何 API
2. **产品需求** — 规格或用户流程中需要澄清的任何内容
3. **其他任何问题** — 实现前您需要了解的任何信息

最后，询问我是否有关于此次实现的其他说明。

回答您的问题后，继续进行实现。

```

## 第十三步：生成 README.md

创建 `product-plan/README.md`：

```markdown
# [产品名称] — 设计移交

此文件夹包含实现 [产品名称] 所需的一切内容。

## 包含内容

**可直接使用的提示词：**
- `prompts/one-shot-prompt.md` — 完整实现提示词模板
- `prompts/section-prompt.md` — 按模块实现提示词模板

**说明文档：**
- `product-overview.md` — 产品摘要（每次实现时都需提供）
- `instructions/one-shot-instructions.md` — 所有里程碑合并版，用于完整实现
- `instructions/incremental/` — 按里程碑的说明（外壳，然后是各模块）

**设计资源：**
- `design-system/` — 颜色、字体、设计令牌
- `data-shapes/` — UI 数据契约（组件期望的数据形状）
- `shell/` — 应用外壳组件
- `sections/` — 所有模块组件、类型、示例数据和测试规格

## 使用方式

### 方式 A：增量实现（推荐）

按里程碑逐步构建应用，获得更好的控制感：

1. 将 `product-plan/` 文件夹复制到您的代码库
2. 从外壳开始（`instructions/incremental/01-shell.md`）——包括设计令牌和应用外壳
3. 对于每个模块：
   - 打开 `prompts/section-prompt.md`
   - 填写顶部的模块变量（SECTION_NAME、SECTION_ID、NN）
   - 粘贴到您的编程助手中
   - 回答问题并实现
4. 每个里程碑完成后审查和测试

### 方式 B：一次性实现

在一次会话中构建整个应用：

1. 将 `product-plan/` 文件夹复制到您的代码库
2. 打开 `prompts/one-shot-prompt.md`
3. 在提示词中添加任何附加说明
4. 将提示词粘贴到您的编程助手中
5. 回答助手的澄清性问题
6. 让助手规划并实现所有内容

## 测试

每个模块都包含一个 `tests.md` 文件，内含 UI 行为测试规格。为获得最佳效果：

1. 在实现前阅读 `sections/[模块id]/tests.md`
2. 为关键用户流程编写测试
3. 实现功能使测试通过
4. 在保持测试绿色的情况下重构

测试规格是**与框架无关**的——它们描述**测试什么**（用户可见行为），而非**如何编写**测试。请根据您的测试设置进行调整。

## 使用技巧

- **使用预写的提示词** — 它们会提示询问关于您的技术栈和需求的重要澄清性问题。
- **添加您自己的说明** — 根据需要在提示词中添加项目特定的背景信息。
- **在您的设计基础上构建** — 将已完成的模块作为未来功能开发的起点。
- **仔细审查** — 仔细检查计划和实现，发现细节和不一致之处。
- **组件是灵活的** — 它们接受数据并触发回调。后端架构由您决定。

---

*由 Design OS 生成*
```

## 第十四步：复制截图

复制以下 `.png` 文件：
- `product/shell/` → `product-plan/shell/`
- `product/sections/[模块id]/` → `product-plan/sections/[模块id]/`

## 第十五步：创建压缩文件

生成所有导出文件后，创建 product-plan 文件夹的 zip 压缩包：

```bash
# 删除任何已存在的压缩文件
rm -f product-plan.zip

# 创建压缩文件
cd . && zip -r product-plan.zip product-plan/
```

这将在项目根目录创建 `product-plan.zip`，可在导出页面下载。

## 第十六步：确认完成

告知用户：

"我已在 `product-plan/` 和 `product-plan.zip` 创建了完整的导出包。

**包含内容：**

**可直接使用的提示词：**
- `prompts/one-shot-prompt.md` — 完整实现提示词
- `prompts/section-prompt.md` — 按模块实现提示词模板

**说明文档：**
- `product-overview.md` — 产品摘要（每次使用说明时都需提供）
- `instructions/one-shot-instructions.md` — 所有里程碑合并版
- `instructions/incremental/` — [N] 个里程碑说明（外壳，然后是各模块）

**设计资源：**
- `design-system/` — 颜色、字体、令牌
- `data-shapes/` — UI 数据契约和综合类型参考
- `shell/` — 应用外壳组件
- `sections/` — [N] 个模块组件包（含测试规格）

**下载：**

重启开发服务器，访问导出页面下载 `product-plan.zip`。

**使用方式：**

1. 将 `product-plan/` 复制到您的实现代码库
2. 打开 `prompts/one-shot-prompt.md` 或 `prompts/section-prompt.md`
3. 添加任何附加说明，然后粘贴到您的编程助手中
4. 回答助手关于技术栈、身份验证等的澄清性问题
5. 让助手根据说明进行实现

这些组件基于 props 且可移植——它们接受数据和回调，让您的实现助手根据自己的技术栈决定路由、数据获取和状态管理。"

## 重要说明

- 复制组件时始终转换导入路径
- 每次实现会话都要提供 `product-overview.md` 背景
- 使用预写的提示词——它们会提示询问重要的澄清性问题
- 截图为保真度检查提供视觉参考
- 示例数据文件在真实 API 构建之前用于测试
- 导出包是自包含的——不依赖 Design OS
- 组件可移植——适用于任何 React 设置
