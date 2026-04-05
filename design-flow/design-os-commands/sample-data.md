# 示例数据

你正在帮助用户为产品的某个模块创建或更新真实的示例数据。这些数据将用于填充界面设计。你还将根据数据结构生成 TypeScript 类型。

## 第一步：检查前提条件

首先，确定目标模块并验证其 `spec.md` 是否存在。

读取 `/product/product-roadmap.md` 获取可用模块列表。

如果只有一个模块，自动选中它。如果有多个模块，使用 AskUserQuestion 工具询问用户想要为哪个模块生成数据。

然后检查 `product/sections/[模块id]/spec.md` 是否存在。如果不存在：

"目前尚未为 **[模块标题]** 创建规格。请先运行 `/shape-section` 定义模块需求，然后再生成示例数据。"

如果规格不存在，停止于此。

## 第二步：检查现有示例数据

检查 `product/sections/[模块id]/data.json` 是否已存在。

**如果示例数据已存在：**

读取现有的 `data.json` 和 `types.ts` 文件，然后询问用户：

"**[模块标题]** 的示例数据已存在。您希望对现有数据结构或示例数据做哪些修改？"

等待用户回复描述他们想要的修改。收到反馈后，**立即**根据他们的要求更新 `data.json` 和 `types.ts`——无需事先展示草稿征求确认。

更新后，告知用户：

"我已根据您的反馈更新了 **[模块标题]** 的示例数据和类型。请查阅修改内容，如需进一步调整请告知我，或在准备好时运行 `/design-screen`。"

到此结束——以下步骤仅适用于从头生成新数据。

**如果没有示例数据：** 继续第三步。

## 第三步：检查全局数据结构

检查 `/product/data-shape/data-shape.md` 是否存在。

**如果存在：**
- 读取文件了解全局实体定义
- 示例数据中的实体名称应与全局数据结构保持一致
- 以描述和关系作为指导

**如果不存在：**
显示警告但继续：

"注意：尚未定义全局数据结构。我将根据模块规格创建实体结构，但为了各模块间的一致性，建议先运行 `/data-shape`。"

## 第四步：分析并生成

读取并分析 `product/sections/[模块id]/spec.md`，了解：

- 用户流程隐含了哪些数据实体？
- 每个实体需要哪些字段/属性？
- 哪些示例值对设计来说真实且有帮助？
- 每个实体可以执行哪些操作？（这些将成为回调 props）

**如果全局数据结构存在：** 将规格与数据结构交叉参考，使用相同的实体名称，确保一致性。

**立即**生成两个文件——无需事先展示草稿征求确认。

### 生成 `product/sections/[模块id]/data.json`

创建包含以下内容的数据文件：

- **`_meta` 部分** — 每个实体及其在界面中的关联关系的通俗描述（在 Design OS 界面中展示）
- **真实的示例数据** — 使用可信的姓名、日期、描述等
- **多样化内容** — 混合长短文本、不同状态等
- **边界案例** — 至少包含一个空数组、一段较长的描述等
- **TypeScript 友好的结构** — 使用一致的字段名和类型

#### 必需的 `_meta` 结构

每个 data.json **必须**在顶层包含一个 `_meta` 对象，包含：

1. **`models`** — 键为实体名称、值为该实体在界面中代表什么的通俗描述的对象
2. **`relationships`** — 从用户视角描述实体关联方式的字符串数组

示例结构：

```json
{
  "_meta": {
    "models": {
      "invoices": "每张发票代表您向客户发送的完成工作的账单。",
      "lineItems": "行项目是每张发票上列出的各项服务或产品。"
    },
    "relationships": [
      "每张发票包含一个或多个行项目（费用明细）",
      "发票通过 clientName 字段跟踪所属客户"
    ]
  },
  "invoices": [
    {
      "id": "inv-001",
      "invoiceNumber": "INV-2024-001",
      "clientName": "Acme Corp",
      "clientEmail": "billing@acme.com",
      "total": 1500.00,
      "status": "sent",
      "dueDate": "2024-02-15",
      "lineItems": [
        { "description": "网页设计", "quantity": 1, "rate": 1500.00 }
      ]
    }
  ]
}
```

`_meta` 描述应当：
- 使用通俗、非技术性语言
- 从用户视角解释每个实体代表什么
- 用"包含"、"属于"、"关联"等词描述关系——这些是概念性的，而非数据库关系
- **如果存在全局数据结构，应匹配其实体名称**

数据应直接支持规格中的用户流程和界面需求。

### 生成 `product/sections/[模块id]/types.ts`

根据数据结构生成 TypeScript 类型。

#### 类型生成规则

1. **从示例数据值推断类型：**
   - 字符串 → `string`
   - 数字 → `number`
   - 布尔值 → `boolean`
   - 数组 → `TypeName[]`
   - 对象 → 创建具名接口

2. **为状态/枚举字段使用联合类型：**

   - 如果 `status` 等字段有已知值，使用联合类型：`'draft' | 'sent' | 'paid' | 'overdue'`

   - 根据规格和示例数据的多样性确定

3. **为主组件创建 Props 接口：**
   - 将数据作为 prop（例如 `invoices: Invoice[]`）
   - 为每个操作包含可选回调 props（例如 `onDelete?: (id: string) => void`）

4. **使用一致的实体名称：**
   - 如果全局数据结构存在，使用相同的实体名称
   - 这确保各模块间的一致性

示例 types.ts：

```typescript
// =============================================================================
// UI 数据形状——定义组件期望通过 props 接收的数据
// =============================================================================

export interface LineItem {
  description: string
  quantity: number
  rate: number
}

export interface Invoice {
  id: string
  invoiceNumber: string
  clientName: string
  clientEmail: string
  total: number
  status: 'draft' | 'sent' | 'paid' | 'overdue'
  dueDate: string
  lineItems: LineItem[]
}

// =============================================================================
// 组件 Props
// =============================================================================

export interface InvoiceListProps {
  /** 要展示的发票列表 */
  invoices: Invoice[]
  /** 用户想要查看发票详情时调用 */
  onView?: (id: string) => void
  /** 用户想要编辑发票时调用 */
  onEdit?: (id: string) => void
  /** 用户想要删除发票时调用 */
  onDelete?: (id: string) => void
  /** 用户想要归档发票时调用 */
  onArchive?: (id: string) => void
  /** 用户想要创建新发票时调用 */
  onCreate?: () => void
}
```

#### 命名规范

- 接口名使用 PascalCase：`Invoice`、`LineItem`、`InvoiceListProps`

- 属性名使用 camelCase：`clientName`、`dueDate`、`lineItems`

- Props 接口应命名为 `[模块名称]Props`（例如 `InvoiceListProps`）

- 为回调 props 添加 JSDoc 注释，说明何时调用

- **如果全局数据结构存在，匹配其实体名称**

## 第五步：告知用户并说明后续步骤

创建两个文件后，告知用户：

"我已为 **[模块标题]** 创建了两个文件：

1. `product/sections/[模块id]/data.json` — 包含 [X] 条记录的示例数据

2. `product/sections/[模块id]/types.ts` — 用于类型安全的 TypeScript 接口

类型包含：

- `[实体]` — 主数据类型
- `[模块名称]Props` — 组件的 Props 接口（包含[列出操作]的回调）

请查阅文件，如需调整请告知我。准备好后，运行 `/design-screen` 为此模块创建界面设计。"

## 重要说明

- 生成真实可信的示例数据——不使用"Lorem ipsum"或"测试 123"
- 主要实体包含 5-10 条示例记录（足以展示真实的列表效果）
- 包含边界案例：空数组、长文本、不同状态
- 字段名保持清晰、TypeScript 友好（camelCase）
- 数据结构应直接映射到规格的用户流程
- 始终与 data.json 一起生成 types.ts
- 回调 props 应涵盖规格中提及的所有操作
- **为保持各模块间的一致性，使用全局数据结构中的实体名称**
- **不要**事先展示草稿征求确认——立即生成文件，让用户事后审阅
- 如果用户在审阅后提出修改，立即更新文件
