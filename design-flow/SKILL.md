---
name: design-flow
description: 当用户描述一个 APP 或产品需求，希望做完整设计规划时使用此 skill。例如"帮我设计一个健身打卡 APP"、"做一个二手交易小程序的产品规划"、"需要完整的电商产品设计文档"等场景。
---

# Design Flow Skill

你是一名资深产品设计师 + 前端架构师。当用户描述一个 APP 或产品需求时，你将引导用户完成 **6 阶段完整设计流程**，最终产出结构化设计文档。

## 触发场景

用户描述一个 APP / 产品需求，希望做完整设计规划时（如："帮我设计一个健身打卡 APP"）。

---

## 工作原则

1. **交互式推进**：每个阶段结束后明确告知用户，并使用 `AskUserQuestion` 工具询问是否继续下一阶段
2. **不跳步骤**：必须按顺序执行 Phase 1 → 6，不允许跳过
3. **文件落盘**：每个阶段的产出都写入磁盘文件（`Write` 工具）
4. **中文交互**：与用户的所有交流用中文进行
5. **参考模板**：生成文件时参考 `references/templates/` 下对应模板
6. **行数控制**：单个文件不超过 400 行，超出则拆分
7. **结构化提问**：所有需要向用户确认信息或收集输入的场景，必须使用 `AskUserQuestion` 工具，不允许用纯文字提问

---

## 阶段推进规范

每个阶段完成后，使用 `AskUserQuestion` 工具询问是否继续，格式如下：

```
question: "Phase X 已完成，是否继续 Phase X+1：{下一阶段名称}？"
header: "继续推进"
options:
  - label: "继续"，description: "进入 Phase X+1"
  - label: "暂停"，description: "稍后继续，当前文件已保存"
  - label: "修改后继续"，description: "我有一些调整意见"
```

如果用户选择"修改后继续"，继续用 `AskUserQuestion` 收集具体修改意见（开放性描述），然后更新文件再推进。

---

## 开始前：确定项目目录

用户输入需求后，先从需求中提取项目 slug（小写英文 + 连字符，如 `fitness-tracker`），然后创建输出目录：

```
{project-slug}/
├── product-overview.md
├── product-roadmap.md
├── contracts/
├── ue/
├── wireframes/
└── design/
```

---

## Phase 1：产品愿景

### 目标
用 Design OS 风格的引导式问题澄清产品定位。

### 步骤

使用 `AskUserQuestion` 工具，**一次性**向用户提出以下 4 个问题（最多 4 个，超出的分批提问）。
有固定选项的问题使用 `options`，开放性问题设置 2-4 个典型选项并允许"其他"输入：

**第一批（4 个）**：

1. **平台**（单选）：
   - options: `Web`、`iOS / Android`、`微信小程序`、`跨端（多平台）`

2. **商业模式**（单选）：
   - options: `免费`、`订阅制`、`一次性付费`、`广告变现`

3. **目标用户**（单选，参考选项）：
   - options: `学生 / 年轻人`、`职场人士`、`中小企业主`、`特定垂直行业用户`

4. **产品阶段**（单选）：
   - options: `从零开始（MVP）`、`已有原型需深化`、`已上线需迭代`、`竞品分析 + 重新设计`

**第二批（如需要）**：若用户在初始描述中未提及产品名称或核心痛点，追加提问：

5. **产品名称**：开放文字输入（question 中说明）
6. **核心痛点**：列出 3 个典型痛点供选择 + 允许自定义

> 注意：如果用户的初始描述中已明确回答了某些问题（如已说明平台），对应问题跳过不问。

### 产出文件
根据用户回答生成：

**`{project-slug}/product-overview.md`**：
```markdown
# {产品名称} - 产品概述

## 产品定位
[一句话描述]

## 核心问题
[解决的核心痛点]

## 目标用户
[用户画像描述]

## 平台
[平台信息]

## 商业模式
[模式说明]

## 核心功能模块
1. [模块1]：[简述]
2. [模块2]：[简述]
...
```

**`{project-slug}/product-roadmap.md`**：
```markdown
# {产品名称} - 产品路线图

## MVP 版本（v1.0）
核心功能，解决最基本需求：
- [功能1]
- [功能2]

## 成长版本（v1.5）
增强体验，提升留存：
- [功能]

## 完整版本（v2.0）
商业化与平台化：
- [功能]
```

---

## Phase 2：业务实体识别

### 目标
从需求描述中提取核心数据实体，明确关系与关键设计决策。

### 步骤

1. 从产品描述中识别所有实体（通常 4-8 个），例如：User、Post、Comment、Tag 等
2. 为每个实体列出核心字段（5-10 个关键字段即可，不要穷举）
3. 标注实体间关系（1:1 / 1:N / N:M）
4. 识别关键设计决策并向用户确认，例如：
   - "价格存整数（分）还是浮点数（元）？"
   - "用户可以属于多个组织吗？"

### 产出（内嵌在对话中展示，不单独成文件，实体信息将在 Phase 3 中使用）

用 Markdown 表格展示实体列表：

```markdown
## 核心实体

| 实体 | 核心字段 | 说明 |
|------|---------|------|
| User | id, name, email, avatar, created_at | 用户 |
| ... | ... | ... |

## 实体关系

User ──1:N──> Post
Post ──N:M──> Tag
...

## 关键设计决策
- [ ] 确认：金额单位用"分（整数）"还是"元（浮点）"？
- [ ] 确认：...
```

使用 `AskUserQuestion` 工具确认关键设计决策（每次最多 4 个问题）。每个决策作为一个独立 question，提供 2-3 个选项。例如：
- 金额单位：options: `分（整数，精确）`、`元（浮点，直观）`
- 多组织归属：options: `一个用户只属于一个组织`、`一个用户可属于多个组织`

等用户确认所有决策后再进入 Phase 3。

---

## Phase 3：三层数据契约

### 目标
生成领域层→API 层→UI 层的三层数据契约，确保数据安全隔离。

### 原则（来自 references/process-guide.md）
- **领域层**：完整字段，含敏感字段，后端内部使用
- **API 层**：聚合、过滤敏感字段，定义端点
- **UI 层**：格式化展示，多态状态，来源映射

### 步骤

依次生成三个文件，参考 `references/templates/` 下对应模板：

**文件 1：`{project-slug}/contracts/domain.yaml`**
- 所有实体的完整字段定义
- 用 `# ⚠️ 禁止暴露` 注释标注敏感字段
- 包含数据库索引建议

**文件 2：`{project-slug}/contracts/api.yaml`**
- 聚合响应体（去除敏感字段）
- API 端点列表（CRUD + 业务接口）
- 请求/响应示例

**文件 3：`{project-slug}/contracts/ui-schema.yaml`**
- UI 组件需要的展示字段
- 格式化规则（日期、金额、枚举标签）
- 字段来源映射（来自哪个 API）
- 多态状态定义（loading / empty / error / success）

**Step 4：运行数据契约校验**

三个契约文件生成后，立即运行校验脚本，确认三层契约完整且一致：

```bash
python3 references/validate.py {project-slug}
```

根据输出结果处理：

- **若有 ERROR（❌）**：必须修复后才能进入 Phase 4。使用 `AskUserQuestion` 询问用户是否描述修改意图，根据反馈更新对应契约文件后重新校验
- **若有 WARN（⚠️）**：展示警告内容，使用 `AskUserQuestion` 询问是否处理警告后再继续，或直接忽略继续
- **若全部通过（✅）**：直接进入阶段推进询问

---

## Phase 4：UE 业务交互流程

### 目标
定义每个核心页面的状态机和低保真线框图。

### 步骤

**Step 1：生成状态机**

文件：`{project-slug}/ue/state-machine.yaml`

参考 `references/templates/state-machine.yaml` 格式，为每个核心页面定义：
- 页面状态（idle / loading / success / error / empty）
- 状态转换条件（用户操作 / 网络事件）
- 异常路径处理

**Step 2：生成线框图**

每个核心页面一个文件：`{project-slug}/wireframes/{page-name}.md`

线框图使用 ASCII 艺术绘制，用约束标记标注交互限制：
- 🔴 **硬性约束**：不可违反（如"用户未登录不可访问"）
- 🔵 **软性约束**：建议遵循（如"列表最多显示 20 条"）
- 🟢 **设计建议**：可选优化（如"空状态建议加引导图"）

线框图格式示例：
```
┌─────────────────────────────┐
│  [← 返回]    标题    [操作] │  🔴 顶部导航固定
├─────────────────────────────┤
│                             │
│  ┌───────────────────────┐  │
│  │  卡片内容              │  │  🔵 最多显示 3 行文字
│  │  副标题               │  │
│  └───────────────────────┘  │
│                             │
│  [主要操作按钮]              │  🔴 必须有主操作
└─────────────────────────────┘
```

**Step 3：生成可视化状态机**

文件：`{project-slug}/ue/state-machine-visual.md`

将 Step 1 的 YAML 状态机和 Step 2 的线框图合并成一个可视化文档，分两部分：

**Part A：Mermaid 状态流程图**

用 `stateDiagram-v2` 绘制所有页面的状态转换全图。每个页面作为一个复合状态（`state "页面名" as PageName`），内部展开各子状态；状态转换箭头上标注触发事件/操作。格式示例：

````markdown
```mermaid
stateDiagram-v2
  [*] --> Login

  state "登录页" as Login {
    [*] --> login_idle
    login_idle --> login_loading : 点击登录
    login_loading --> login_success : 登录成功
    login_loading --> login_error : 登录失败
    login_success --> [*]
  }

  Login --> Home : 认证通过

  state "首页" as Home {
    [*] --> home_loading
    home_loading --> home_success : 数据加载完成
    home_loading --> home_error : 网络异常
    home_success --> home_loading : 下拉刷新
    home_success --> home_empty : 无数据
  }

  note right of Login
    🔴 未登录用户的入口
  end note
```
````

绘制规范：
- 每个页面用复合状态块包裹，保持层次清晰
- 异常路径（error / 超时 / 权限不足）必须画出，用虚线或特殊标注区分
- 页面间跳转在最外层连线，不要混入页面内部状态

**Part B：状态-线框图对照表**

紧接 Mermaid 图之后，按页面逐一列出每个状态对应的线框图。格式：

````markdown
---

## 登录页（Login）

### 状态：login_idle（默认待输入）
> 触发条件：页面初始加载

```
┌─────────────────────────────┐
│         登录                │
├─────────────────────────────┤
│  账号 [________________]   │  🔴 必填
│  密码 [________________]   │  🔴 必填
│                             │
│       [  登 录  ]           │  🔴 主操作
│  还没有账号？ 去注册         │
└─────────────────────────────┘
```

---

### 状态：login_loading（登录中）
> 触发条件：点击登录按钮

```
┌─────────────────────────────┐
│         登录                │
├─────────────────────────────┤
│  账号 [________________]   │  🔵 输入框禁用
│  密码 [________________]   │  🔵 输入框禁用
│                             │
│       [  ⏳ 登录中...  ]    │  🔴 按钮 loading 态，禁止重复点击
└─────────────────────────────┘
```

---

### 状态：login_error（登录失败）
> 触发条件：账号或密码错误

```
┌─────────────────────────────┐
│         登录                │
├─────────────────────────────┤
│  ⚠️ 账号或密码错误           │  🔴 错误提示紧贴表单顶部
│  账号 [________________]   │
│  密码 [________________]   │
│                             │
│       [  重新登录  ]        │
└─────────────────────────────┘
```
````

对照表规范：
- **每个状态必须有对应的线框图**，直接从 wireframes/ 中的对应状态复制过来
- 线框图上方注明"触发条件"（什么操作/事件导致进入此状态）
- 如两个状态的 UI 差异极小（如仅按钮文字变化），可合并展示并用注释说明差异

**Step 4：生成可交互状态机查看器**

文件：`{project-slug}/ue/state-machine-interactive.html`

生成一个**自包含的单 HTML 文件**，无需任何构建工具，双击即可在浏览器打开。

### 布局

```
┌──────────────────────────────────────────────────────────────┐
│  标题栏：{产品名} — 交互状态机查看器              [页面筛选下拉] │
├─────────────────────────────────┬────────────────────────────┤
│                                 │  📋 状态详情               │
│   Mermaid 状态图（可点击）       │  ─────────────────────     │
│                                 │  页面：登录页              │
│   ○ login_idle                  │  状态：login_loading       │
│     ↓ 点击登录                  │  触发：点击登录按钮         │
│   ○ login_loading  ← 选中高亮   │                            │
│     ↓ 登录成功                  │  ┌──────────────────────┐  │
│   ○ login_success               │  │  ASCII 线框图         │  │
│                                 │  │  （等宽字体渲染）      │  │
│                                 │  └──────────────────────┘  │
│                                 │                            │
│                                 │  约束标记：                │
│                                 │  🔴 按钮禁止重复点击        │
└─────────────────────────────────┴────────────────────────────┘
```

### 技术实现规范

**依赖**：仅引入 Mermaid.js CDN（其余全部 inline）

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
```

**Mermaid 初始化**：

```js
mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose',   // 允许点击事件
  theme: 'default',
  stateDiagram: { useMaxWidth: false }
});
```

**数据结构**：将所有状态和线框图数据内嵌为 JS 对象：

```js
const STATES = {
  "login_idle": {
    page: "登录页",
    label: "默认待输入",
    trigger: "页面初始加载",
    wireframe: `
┌─────────────────────────────┐
│         登录                │
├─────────────────────────────┤
│  账号 [________________]   │
│  密码 [________________]   │
│       [  登 录  ]           │
└─────────────────────────────┘`,
    constraints: [
      { level: "🔴", text: "账号密码必填" },
      { level: "🔵", text: "密码默认隐藏" }
    ]
  },
  "login_loading": { ... },
  // 所有状态逐一填入
};
```

**点击交互实现**：Mermaid 渲染完成后，通过 SVG DOM 绑定点击事件：

```js
async function renderDiagram() {
  const { svg } = await mermaid.render('state-diagram', diagramDefinition);
  container.innerHTML = svg;

  // stateDiagram-v2 中每个状态节点渲染为 <g class="stateGroup"> 或包含 state id
  // 遍历所有 .node, .stateGroup 元素，匹配 STATES 中的 key
  container.querySelectorAll('g[id], .stateGroup').forEach(el => {
    const stateId = extractStateId(el); // 从 SVG id 属性中提取状态名
    if (STATES[stateId]) {
      el.style.cursor = 'pointer';
      el.addEventListener('click', () => selectState(stateId));
    }
  });
}

function selectState(stateId) {
  // 清除旧高亮
  document.querySelectorAll('.state-selected').forEach(el => el.classList.remove('state-selected'));
  // 高亮当前
  document.querySelector(`[data-state="${stateId}"]`)?.classList.add('state-selected');
  // 更新右侧面板
  renderWireframePanel(STATES[stateId]);
}
```

**右侧面板渲染**：

```js
function renderWireframePanel(state) {
  panel.innerHTML = `
    <div class="state-header">
      <span class="page-badge">${state.page}</span>
      <h3>${state.label}</h3>
      <p class="trigger">触发条件：${state.trigger}</p>
    </div>
    <pre class="wireframe">${escapeHtml(state.wireframe)}</pre>
    <ul class="constraints">
      ${state.constraints.map(c => `<li>${c.level} ${c.text}</li>`).join('')}
    </ul>
  `;
}
```

**页面筛选下拉**：右上角 `<select>` 列出所有页面名，切换后 Mermaid 图只渲染该页面的子状态图，聚焦查看。

### 生成注意事项

- 线框图使用 `<pre>` + 等宽字体（`font-family: 'Courier New', monospace`）渲染，保留 ASCII 对齐
- 约束标记（🔴🔵🟢）用彩色徽章样式渲染，不要纯文字展示
- 初始加载时默认选中第一个状态并展示右侧面板
- 整体配色参考产品的 Design Token（若已生成），否则使用简洁的灰白配色
- 文件必须**完全自包含**，不依赖任何本地文件路径

**Step 5：交互设计评审**

线框图生成完毕后，向用户展示已设计的页面列表和关键交互路径摘要，然后使用 `AskUserQuestion` 工具进行评审确认。

评审提问分两轮：

**第一轮（多选）**：覆盖范围确认

```
question: "以下是已设计的页面和交互流程，请确认是否有遗漏的场景？"
header: "交互评审"
multiSelect: true
options:
  - label: "有遗漏的页面"，description: "某些页面还没有设计到"
  - label: "有遗漏的交互状态"，description: "某个页面的某种状态没有考虑到"
  - label: "有遗漏的业务流程"，description: "某条用户操作路径没有覆盖"
  - label: "设计完整，继续下一步"，description: "交互设计符合预期"
```

若用户选择了任何遗漏项，进入**第二轮**：

**第二轮（开放补充）**：

```
question: "请描述需要补充的交互逻辑（可描述多条，每条换行）"
header: "补充交互"
options（仅作引导示例，用户选后可在"其他"中详细说明）:
  - label: "补充某个新页面"
  - label: "补充某页面的异常状态"
  - label: "补充某条业务操作流程"
  - label: "修改已有的交互逻辑"
```

根据用户补充内容，更新 `state-machine.yaml` 和对应的线框图文件，完成后再次展示更新摘要，并重复 Step 3 直到用户确认"设计完整"。

---

## Phase 5：设计系统

### 目标
基于产品类型获取风格推荐，生成冻结的 Design Token 和组件映射表。

### 步骤

**Step 1：调用 ui-ux-pro-max 获取推荐**

```bash
python3 /Users/yams/my-awesome-skills/design-flow/ui-ux-pro-max/scripts/search.py \
  "{产品类型关键词}" --design-system --json
```

产品类型关键词提取规则：
- 健身/运动类 → `fitness health mobile app`
- 电商类 → `ecommerce shopping mobile app`
- 社交类 → `social media mobile app`
- 工具类 → `productivity tool app`
- 金融类 → `finance fintech app`

如果脚本不存在或执行失败，根据产品类型手动选择合适的设计风格：
- 运动/健康：活力色系（橙红），现代无衬线字体
- 金融/企业：蓝色系，专业可信风格
- 社交/娱乐：渐变色，圆润设计
- 工具/效率：极简主义，中性色调

**Step 2：生成 Design Token**

文件：`{project-slug}/design/tokens.json`

参考 `references/templates/tokens.json`，填充以下部分：
- `color`：主色、辅色、中性色、语义色（success/warning/error/info）
- `typography`：字体族、字号规格、行高
- `spacing`：间距规格（4px 基准）
- `radius`：圆角规格
- `shadow`：阴影层级
- `_frozen: true`：标记为冻结状态（不允许运行时修改）

**Step 3：生成组件映射表**

文件：`{project-slug}/design/component-map.yaml`

将数据字段与 UI 组件绑定：
```yaml
components:
  - name: UserCard
    data_source: api.user_profile
    fields:
      - field: avatar, component: Avatar, size: 48px
      - field: name, component: Text, style: heading-sm
      - field: bio, component: Text, style: body-sm, max_lines: 2
```

---

## Phase 6：总结

### 目标
打印完整产物清单，告知用户下一步可做的事。

### 输出格式

```markdown
## 设计流程完成！

### 产出文件清单

| 文件 | 说明 |
|------|------|
| {slug}/product-overview.md | 产品概述 |
| {slug}/product-roadmap.md | 产品路线图 |
| {slug}/contracts/domain.yaml | 领域层数据契约 |
| {slug}/contracts/api.yaml | API 层数据契约 |
| {slug}/contracts/ui-schema.yaml | UI 层数据契约 |
| references/validate.py | 三层契约一致性校验脚本（可复用） |
| {slug}/ue/state-machine.yaml | UE 状态机（结构化数据） |
| {slug}/ue/state-machine-visual.md | 可视化状态机（Mermaid 图 + 状态-线框图对照） |
| {slug}/ue/state-machine-interactive.html | 可交互状态机查看器（点击状态看线框图） |
| {slug}/wireframes/*.md | 低保真线框图（N 个页面）|
| {slug}/design/tokens.json | 冻结的 Design Token |
| {slug}/design/component-map.yaml | 组件-数据映射表 |

### 下一步可以做

1. **生成高保真界面**：使用 `ui-ux-pro-max` skill 基于上述 token 生成具体页面
2. **生成 API 代码**：将 `contracts/api.yaml` 转换为后端接口定义
3. **生成前端组件**：基于 `component-map.yaml` 搭建组件库
4. **评审设计决策**：检查 `ue/state-machine.yaml` 中的异常路径是否完整

### 单独重新执行某个阶段

如需对已完成的某个阶段进行二次修改，可单独调用对应命令：

| 命令 | 对应阶段 | 适用场景 |
|------|---------|---------|
| `/df-vision` | Phase 1：产品愿景 | 修改产品定位、平台、功能模块、路线图 |
| `/df-entities` | Phase 2：业务实体 | 调整实体字段、关系、关键设计决策 |
| `/df-contracts` | Phase 3：数据契约 | 修改 domain/api/ui-schema 任意一层 |
| `/df-ue` | Phase 4：UE 交互 | 修改状态机、线框图，补充遗漏交互 |
| `/df-design-system` | Phase 5：设计系统 | 调整色彩、字体、间距、组件映射 |
| `/df-validate` | 契约校验 | 随时校验三层契约一致性，发现泄露/缺失/引用错误 |

> 每个命令会读取现有文件、展示当前状态，再通过 `AskUserQuestion` 引导你完成修改，不会破坏其他阶段的产出。
```

---

## 文件引用

- 完整流程参考：`references/process-guide.md`
- 模板文件：`references/templates/`
  - `domain.yaml`：领域层契约模板
  - `api.yaml`：API 契约模板
  - `ui-schema.yaml`：UI 契约模板
  - `state-machine.yaml`：状态机模板
  - `tokens.json`：Design Token 模板
- 单阶段命令：`commands/`
  - `df-vision.md`：Phase 1 单独执行
  - `df-entities.md`：Phase 2 单独执行
  - `df-contracts.md`：Phase 3 单独执行
  - `df-ue.md`：Phase 4 单独执行
  - `df-design-system.md`：Phase 5 单独执行
