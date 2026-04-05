# 设计界面

你正在帮助用户为产品的某个模块创建界面设计。界面设计将是一个基于 props 的 React 组件，可以导出并集成到任何 React 代码库中。

## 第一步：检查前提条件

首先，确定目标模块，并验证 `spec.md`、`data.json` 和 `types.ts` 都存在。

读取 `/product/product-roadmap.md` 获取可用模块列表。

如果只有一个模块，自动选中它。如果有多个模块，使用 AskUserQuestion 工具询问用户想要为哪个模块创建界面设计。

然后验证所有必需文件存在：

- `product/sections/[模块id]/spec.md`
- `product/sections/[模块id]/data.json`
- `product/sections/[模块id]/types.ts`

如果 spec.md 不存在：

"我没有看到 **[模块标题]** 的规格。请先运行 `/shape-section` 定义模块需求。"

如果 data.json 或 types.ts 不存在：

"我没有看到 **[模块标题]** 的示例数据。请先运行 `/sample-data` 为界面设计创建示例数据和类型。"

如果任何文件缺失，停止于此。

## 第二步：检查设计系统和外壳

检查可选的增强功能：

**设计令牌：**
- 检查 `/product/design-system/colors.json` 是否存在
- 检查 `/product/design-system/typography.json` 是否存在

如果设计令牌存在，读取并使用它们进行样式设置。如果不存在，显示警告：

"注意：设计令牌尚未定义。我将使用默认样式，但为了品牌一致性，建议先运行 `/design-tokens`。"

**外壳：**
- 检查 `src/shell/components/AppShell.tsx` 是否存在

如果外壳存在，界面设计将在 Design OS 中于外壳内渲染。如果不存在，显示警告：

"注意：应用外壳尚未设计。界面设计将独立渲染。建议运行 `/design-shell` 在完整应用上下文中查看模块界面设计。"

## 第三步：分析需求

读取并分析所有三个文件：

1. **spec.md** — 了解用户流程和界面需求
2. **data.json** — 了解数据结构和示例内容
3. **types.ts** — 了解 TypeScript 接口和可用回调

根据规格确定需要哪些视图。常见模式：

- 列表/仪表板视图（展示多个条目）
- 详情视图（展示单个条目）
- 表单/创建视图（用于新建/编辑）

## 第四步：明确界面设计范围

如果规格暗示需要多个视图，使用 AskUserQuestion 工具确认先构建哪个视图：

"**[模块标题]** 的规格建议了几种不同的视图：

1. **[视图 1]** — [简短描述]
2. **[视图 2]** — [简短描述]

应该先创建哪个视图？"

如果只有一个明显的视图，直接继续。

## 第五步：调用前端设计技能

在创建界面设计之前，读取 `frontend-design` 技能以确保高质量的设计输出。

读取 `.claude/skills/frontend-design/SKILL.md` 中的文件，并遵循其创建独特、生产级界面的指导。

## 第六步：创建基于 Props 的组件

在 `src/sections/[模块id]/components/[视图名称].tsx` 创建主组件文件。

### 组件结构

组件**必须**：

- 从 types.ts 文件导入类型
- 通过 props 接受所有数据（绝不直接导入 data.json）
- 为所有操作接受回调 props
- 完全自包含且可移植

示例：

```tsx
import type { InvoiceListProps } from '@/../product/sections/[模块id]/types'

export function InvoiceList({
  invoices,
  onView,
  onEdit,
  onDelete,
  onCreate
}: InvoiceListProps) {
  return (
    <div className="max-w-4xl mx-auto">
      {/* 组件内容 */}

      {/* 示例：使用回调 */}
      <button onClick={onCreate}>创建发票</button>

      {/* 示例：映射数据和回调 */}
      {invoices.map(invoice => (
        <div key={invoice.id}>
          <span>{invoice.clientName}</span>
          <button onClick={() => onView?.(invoice.id)}>查看</button>
          <button onClick={() => onEdit?.(invoice.id)}>编辑</button>
          <button onClick={() => onDelete?.(invoice.id)}>删除</button>
        </div>
      ))}
    </div>
  )
}
```

### 设计要求

- **移动端响应式：** 使用 Tailwind 响应式前缀（`sm:`、`md:`、`lg:`），确保布局在移动端、平板端和桌面端都能正常显示。
- **亮色和深色模式：** 为所有颜色使用 `dark:` 变体
- **使用设计令牌：** 如果已定义，应用产品的配色方案和排版
- **遵循前端设计技能：** 创建独特、令人印象深刻的界面

### 应用设计令牌

**如果 `/product/design-system/colors.json` 存在：**
- 按钮、链接和关键强调使用主色调
- 标签、高亮、次要元素使用辅色调
- 背景、文字和边框使用中性色
- 示例：如果主色调是 `lime`，主要操作使用 `lime-500`、`lime-600` 等

**如果 `/product/design-system/typography.json` 存在：**
- 在注释中记录字体选择以供参考
- 字体将在应用级别应用，但要使用合适的字重

**如果设计令牌不存在：**
- 中性色退回使用 `stone`，强调色使用 `lime`（Design OS 默认值）

### 应包含的内容

- 实现规格中的所有用户流程和界面需求
- 使用 prop 数据（而非硬编码值）
- 包含真实的界面状态（悬停、激活等）
- 所有交互元素使用回调 props
- 可选回调使用可选链调用：`onClick={() => onDelete?.(id)}`

### 不应包含的内容

- 不含 `import data from` 语句——数据通过 props 传入
- 不含规格未指定的功能
- 不含路由逻辑——回调处理导航意图
- 不含导航元素（由外壳处理）

## 第七步：创建子组件（如需要）

对于复杂视图，拆分为子组件。每个子组件也应基于 props。

在 `src/sections/[模块id]/components/[子组件].tsx` 创建子组件。

示例：

```tsx
import type { Invoice } from '@/../product/sections/[模块id]/types'

interface InvoiceRowProps {
  invoice: Invoice
  onView?: () => void
  onEdit?: () => void
  onDelete?: () => void
}

export function InvoiceRow({ invoice, onView, onEdit, onDelete }: InvoiceRowProps) {
  return (
    <div className="flex items-center justify-between p-4 border-b">
      <div>
        <p className="font-medium">{invoice.clientName}</p>
        <p className="text-sm text-stone-500">{invoice.invoiceNumber}</p>
      </div>
      <div className="flex gap-2">
        <button onClick={onView}>查看</button>
        <button onClick={onEdit}>编辑</button>
        <button onClick={onDelete}>删除</button>
      </div>
    </div>
  )
}
```

然后在主组件中导入并使用：

```tsx
import { InvoiceRow } from './InvoiceRow'

export function InvoiceList({ invoices, onView, onEdit, onDelete }: InvoiceListProps) {
  return (
    <div>
      {invoices.map(invoice => (
        <InvoiceRow
          key={invoice.id}
          invoice={invoice}
          onView={() => onView?.(invoice.id)}
          onEdit={() => onEdit?.(invoice.id)}
          onDelete={() => onDelete?.(invoice.id)}
        />
      ))}
    </div>
  )
}
```

## 第八步：创建预览包装器

在 `src/sections/[模块id]/[视图名称].tsx` 创建预览包装器（注意：这在模块根目录，而非 components/ 中）。

这个包装器是 Design OS 渲染的内容。它导入示例数据并通过 props 传入基于 props 的组件。

示例：

```tsx
import data from '@/../product/sections/[模块id]/data.json'
import { InvoiceList } from './components/InvoiceList'

export default function InvoiceListPreview() {
  return (
    <InvoiceList
      invoices={data.invoices}
      onView={(id) => console.log('查看发票：', id)}
      onEdit={(id) => console.log('编辑发票：', id)}
      onDelete={(id) => console.log('删除发票：', id)}
      onCreate={() => console.log('创建新发票')}
    />
  )
}
```

预览包装器：

- 有 `default` 导出（Design OS 路由所必需）
- 从 data.json 导入示例数据
- 通过 props 将数据传入组件
- 为回调提供 console.log 处理器（用于测试交互）
- **不会**导出到用户的代码库——仅用于 Design OS
- **如果已设计外壳，将在外壳内渲染**

## 第九步：创建组件索引

在 `src/sections/[模块id]/components/index.ts` 创建索引文件，干净地导出所有组件。

示例：

```tsx
export { InvoiceList } from './InvoiceList'
export { InvoiceRow } from './InvoiceRow'
// 根据需要添加其他子组件
```

## 第十步：确认并说明后续步骤

告知用户：

"我已为 **[模块标题]** 创建了界面设计：

**可导出组件**（基于 props，可移植）：

- `src/sections/[模块id]/components/[视图名称].tsx`
- `src/sections/[模块id]/components/[子组件].tsx`（如已创建）
- `src/sections/[模块id]/components/index.ts`

**预览包装器**（仅用于 Design OS）：

- `src/sections/[模块id]/[视图名称].tsx`

**重要：** 重启开发服务器后即可查看更改。

[如果外壳存在]：界面设计将在您的应用外壳内渲染，呈现完整的应用体验。

[如果设计令牌存在]：我已应用了您的配色方案（[主色调]、[辅色调]、[中性色]）和排版选择。

**后续步骤：**

- 运行 `/screenshot-design` 截取此界面设计的截图用于文档记录
- 如果规格需要其他视图，再次运行 `/design-screen` 创建它们
- 当所有模块完成后，运行 `/export-product` 生成完整的导出包"

如果规格指出还需要其他视图：

"规格还需要 [其他视图]。再次运行 `/design-screen` 创建它们，然后运行 `/screenshot-design` 截取每个视图。"

## 重要说明

- 创建界面设计前**务必**读取 `frontend-design` 技能
- 组件**必须**基于 props——绝不在可导出组件中导入 data.json
- 预览包装器是**唯一**导入 data.json 的文件
- 所有 props 使用 types.ts 中的 TypeScript 接口
- 回调应为可选项（使用 `?`）并以可选链调用（`?.`）
- 创建文件后务必提醒用户重启开发服务器
- 子组件也应基于 props 以获得最大可移植性
- 存在设计令牌时应用它们以保持品牌一致性
- 在 Design OS 中查看时，界面设计在外壳内渲染（如果外壳存在）
