# 设计应用外壳

你正在帮助用户设计应用外壳——包裹所有模块的持久导航和布局。这是界面设计，而非实现代码。

## 第一步：检查前提条件

首先，验证前提条件是否存在：

1. 读取 `/product/product-overview.md` — 产品名称和描述
2. 读取 `/product/product-roadmap.md` — 导航所需的模块列表
3. 检查 `/product/design-system/colors.json` 和 `/product/design-system/typography.json` 是否存在

如果概述或路线图缺失：

"在设计外壳之前，您需要先定义产品和模块。请依次运行：
1. `/product-vision` — 定义您的产品
2. `/product-roadmap` — 定义您的模块"

如果概述或路线图缺失，停止于此。

如果设计令牌缺失，显示警告但继续：

"注意：设计令牌尚未定义。我将使用默认样式继续，但您可能希望先运行 `/design-tokens` 以获得一致的颜色和排版。"

## 第二步：分析产品结构

查阅路线图模块，展示导航选项：

"我正在为 **[产品名称]** 设计外壳。根据您的路线图，您有 [N] 个模块：

1. **[模块 1]** — [描述]
2. **[模块 2]** — [描述]
3. **[模块 3]** — [描述]

让我们决定外壳布局。常见模式：

**A. 侧边栏导航** — 左侧垂直导航，右侧内容区
   最适合：模块较多的应用、仪表板式工具、管理面板

**B. 顶部导航** — 顶部水平导航，下方内容区
   最适合：较简单的应用、营销风格产品、模块较少

**C. 极简标题** — 仅有 Logo + 用户菜单，模块以其他方式访问
   最适合：单一功能工具、向导式流程

哪种模式最适合 **[产品名称]**？"

等待他们的回复。

## 第三步：收集设计细节

使用 AskUserQuestion 澄清：

- "用户菜单（头像、退出）应放在哪里？"
- "您希望侧边栏在移动端可折叠，还是变成汉堡菜单？"
- "导航中是否需要额外项目？（设置、帮助等）"
- "应用加载时默认显示哪个视图？"

## 第四步：展示外壳规格

了解他们的偏好后：

"这是 **[产品名称]** 的外壳设计：

**布局模式：** [侧边栏/顶部导航/极简]

**导航结构：**
- [导航项 1] → [模块]
- [导航项 2] → [模块]
- [导航项 3] → [模块]
- [其他项目，如设置、帮助]

**用户菜单：**
- 位置：[右上角 / 侧边栏底部]
- 内容：头像、用户名、退出

**响应式行为：**
- 桌面端：[显示效果]
- 移动端：[适配方式]

这符合您的设想吗？"

反复迭代直到确认通过。

## 第五步：创建外壳规格文件

创建 `/product/shell/spec.md`：

```markdown
# 应用外壳规格

## 概述
[外壳设计的描述及其用途]

## 导航结构
- [导航项 1] → [模块 1]
- [导航项 2] → [模块 2]
- [导航项 3] → [模块 3]
- [其他导航项]

## 用户菜单
[用户菜单位置和内容的描述]

## 布局模式
[布局描述——侧边栏、顶部导航等]

## 响应式行为
- **桌面端：** [行为]
- **平板端：** [行为]
- **移动端：** [行为]

## 设计说明
[其他设计决策或说明]
```

## 第六步：创建外壳组件

在 `src/shell/components/` 创建外壳组件：

### AppShell.tsx
接受子元素并提供布局结构的主包装组件。

```tsx
interface AppShellProps {
  children: React.ReactNode
  navigationItems: Array<{ label: string; href: string; isActive?: boolean }>
  user?: { name: string; avatarUrl?: string }
  onNavigate?: (href: string) => void
  onLogout?: () => void
}
```

### MainNav.tsx
根据所选模式的导航组件（侧边栏或顶部导航）。

### UserMenu.tsx
带头像和下拉菜单的用户菜单。

### index.ts
导出所有组件。

**组件要求：**
- 所有数据和回调通过 props 传入（可移植）
- 如存在设计令牌，则应用它们（颜色、字体）
- 使用 `dark:` 变体支持亮色和深色模式
- 移动端响应式
- 使用 Tailwind CSS 样式
- 使用 lucide-react 图标

## 第七步：创建外壳预览

创建 `src/shell/ShellPreview.tsx`——用于在 Design OS 中预览外壳的包装器：

```tsx
import data from '@/../product/sections/[第一个模块]/data.json' // 如存在
import { AppShell } from './components/AppShell'

export default function ShellPreview() {
  const navigationItems = [
    { label: '[模块 1]', href: '/section-1', isActive: true },
    { label: '[模块 2]', href: '/section-2' },
    { label: '[模块 3]', href: '/section-3' },
  ]

  const user = {
    name: 'Alex Morgan',
    avatarUrl: undefined,
  }

  return (
    <AppShell
      navigationItems={navigationItems}
      user={user}
      onNavigate={(href) => console.log('导航到：', href)}
      onLogout={() => console.log('退出登录')}
    >
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">内容区域</h1>
        <p className="text-stone-600 dark:text-stone-400">
          各模块内容将在此渲染。
        </p>
      </div>
    </AppShell>
  )
}
```

## 第八步：应用设计令牌

如果设计令牌存在，将其应用于外壳组件：

**颜色：**
- 读取 `/product/design-system/colors.json`
- 使用主色调于活跃导航项、关键强调
- 使用辅色调于悬停状态、细微高亮
- 使用中性色于背景、边框、文字

**排版：**
- 读取 `/product/design-system/typography.json`
- 将标题字体应用于导航项和标题
- 将正文字体应用于其他文字
- 在预览中包含 Google Fonts 导入

## 第九步：确认完成

告知用户：

"我已为 **[产品名称]** 设计了应用外壳：

**已创建文件：**
- `/product/shell/spec.md` — 外壳规格
- `src/shell/components/AppShell.tsx` — 主外壳包装器
- `src/shell/components/MainNav.tsx` — 导航组件
- `src/shell/components/UserMenu.tsx` — 用户菜单组件
- `src/shell/components/index.ts` — 组件导出
- `src/shell/ShellPreview.tsx` — 预览包装器

**外壳功能：**
- [布局模式] 布局
- 支持所有 [N] 个模块的导航
- 带头像和退出的用户菜单
- 移动端响应式设计
- 亮色/深色模式支持

**重要：** 重启开发服务器后即可查看更改。

当您使用 `/design-screen` 设计各模块界面时，它们将在此外壳内渲染，呈现完整的应用体验。

下一步：运行 `/shape-section` 开始设计您的第一个模块。"

## 重要说明

- 外壳是界面设计——它展示导航和布局设计
- 组件基于 props，可移植到用户的代码库
- 预览包装器仅用于 Design OS——不会导出
- 存在设计令牌时应用它们以保持样式一致
- 外壳专注于导航框架——不包含身份验证界面
- 各模块界面设计将在外壳的内容区域内渲染
