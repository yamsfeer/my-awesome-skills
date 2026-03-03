# Excalidraw 图表生成 Skill

一个将自然语言描述转换为专业 Excalidraw 图表的 Claude Code Skill。

不只是画框框和箭头——而是创建能够**用视觉进行论证**的图表。

---

## 核心设计理念

### 图表应该"论证"，而非"展示"

传统的架构图只是把信息装进方框里。这个 Skill 创建的图表**用形状本身来表达含义**：

| 概念类型 | 视觉模式 | 用途 |
|---------|---------|------|
| 一对多关系 | **扇形展开（Fan-out）** | 源头、中心枢纽 |
| 多对一聚合 | **汇聚（Convergence）** | 聚合、漏斗、综合 |
| 层级结构 | **树形（Tree）** | 文件系统、组织架构 |
| 时间序列 | **时间线（Timeline）** | 协议、工作流、生命周期 |
| 持续循环 | **螺旋/循环（Spiral）** | 反馈循环、迭代过程 |
| 抽象状态 | **云朵（Cloud）** | 上下文、对话、心理状态 |
| 输入到输出 | **流水线（Assembly Line）** | 转换、处理、转换 |

**同构测试**：如果你删除所有文字，仅靠结构本身能否传达概念？如果不能，重新设计。

### 证据工件（Evidence Artifacts）

技术图表不是用占位符（如"API"、"事件"），而是展示：
- 真实的代码片段
- 实际的 JSON 格式
- 真实的事件名称（如 `RUN_STARTED`, `STATE_DELTA`）
- 实际的 API 端点

### 多层级架构

一张全面的图表同时工作在多个缩放级别：

1. **Level 1 - 摘要流程**：简化的整体概览
2. **Level 2 - 区域边界**：按职责分组的组件
3. **Level 3 - 区域细节**：代码示例、具体数据

---

## 文件结构

```
excalidraw-diagram-skill/
├── SKILL.md                      # 完整的设计方法论（550+ 行）
├── README_CN.md                  # 本文件
└── references/
    ├── color-palette.md          # 颜色配置（可自定义品牌色）
    ├── element-templates.md      # JSON 元素模板
    ├── json-schema.md            # Excalidraw JSON 格式参考
    ├── render_excalidraw.py      # 渲染脚本：JSON → PNG
    ├── render_template.html      # 浏览器渲染模板
    └── pyproject.toml            # Python 依赖（Playwright）
```

---

## 使用方法

### 1. 安装 Skill

将本目录复制到你的 Claude Code 项目的 `.claude/skills/` 目录下：

```bash
cp -r excalidraw-diagram-skill .claude/skills/excalidraw-diagram
```

### 2. 设置渲染器（首次使用）

```bash
cd .claude/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

### 3. 使用 Skill 创建图表

告诉 Claude：

> "创建一个 Excalidraw 图表，展示 AG-UI 协议如何将事件从 AI Agent 流式传输到前端 UI"

Skill 会自动处理：
- 概念映射
- 布局设计
- JSON 生成
- 渲染验证

---

## 渲染与验证流程（核心特性）

这是本 Skill 的关键特性：**AI 可以看到自己生成的图表并修复问题**。

### 渲染循环

```
生成 JSON → 渲染为 PNG → 查看图像 → 发现问题 → 修复 → 重新渲染 → ...
```

### 典型问题检查清单

- [ ] 文字是否被容器截断或溢出
- [ ] 元素是否重叠
- [ ] 箭头是否穿过元素而不是绕过
- [ ] 箭头是否正确连接到目标元素
- [ ] 间距是否均匀
- [ ] 构图是否平衡（没有大片空白或拥挤区域）
- [ ] 文字在渲染后是否可读

### 渲染命令

```bash
cd .claude/skills/excalidraw-diagram/references
uv run python render_excalidraw.py <path-to-file.excalidraw>
```

输出 PNG 文件会与 `.excalidraw` 文件位于同一目录。

---

## 自定义品牌颜色

编辑 `references/color-palette.md` 即可自定义所有图表的颜色：

```markdown
| 语义用途 | 填充色 | 描边色 |
|----------|--------|--------|
| Primary/Neutral | `#3b82f6` | `#1e3a5f` |
| Start/Trigger | `#fed7aa` | `#c2410c` |
| End/Success | `#a7f3d0` | `#047857` |
| AI/LLM | `#ddd6fe` | `#6d28d9` |
```

所有其他文件包含的都是通用的设计方法论，无需修改。

---

## 大型图表的分段构建策略

对于复杂的技术图表，**不要一次性生成整个文件**（会超出 token 限制）。

### 分段工作流程

**第一阶段：逐段构建**

1. 创建基础 JSON（包含 `type`, `version`, `appState`, `files`）
2. 每次编辑添加一个区域（section）
3. 使用描述性 ID（如 `"trigger_rect"`, `"arrow_fan_left"`）
4. 按区域命名种子（如区域1用 100xxx，区域2用 200xxx）
5. 实时更新跨区域的绑定关系

**第二阶段：整体审查**

- 检查跨区域箭头是否双向绑定正确
- 检查间距是否平衡
- 验证所有 ID 和绑定关系

**第三阶段：渲染验证**

运行渲染循环，修复视觉问题。

---

## 容器 vs 自由浮动文本

**不是每个文本都需要边框**。默认使用自由浮动文本，仅在需要时添加容器：

| 使用容器当... | 使用自由浮动文本当... |
|--------------|----------------------|
| 它是某区域的焦点 | 它是标签或描述 |
| 需要与其他元素视觉分组 | 是支持性细节或元数据 |
| 箭头需要连接到它 | 描述附近的事物 |
| 形状本身携带含义（如决策菱形） | 仅排版就能创建层次结构 |

**目标**：<30% 的文本元素在容器内。

---

## 技术架构

### 渲染管线

```
.excalidraw JSON
       ↓
validate_excalidraw()      # 验证 JSON 结构
       ↓
compute_bounding_box()     # 计算元素边界框
       ↓
Playwright + Chromium      # 启动无头浏览器
       ↓
render_template.html       # 加载 Excalidraw exportToSvg
       ↓
exportToSvg()              # 生成 SVG
       ↓
screenshot()               # 保存为 PNG
```

### 关键技术

- **Playwright**：控制 Chromium 浏览器
- **Excalidraw npm 包**：通过 CDN (esm.sh) 加载 `exportToSvg` 函数
- **边界框计算**：自动根据所有元素计算画布大小

---

## 质量检查清单

### 深度与证据（技术图表）
- [ ] 是否研究了实际的规范、格式、事件名？
- [ ] 是否包含代码片段、JSON 示例？
- [ ] 是否具有多层级（摘要+区域+细节）？
- [ ] 展示的是真实内容，而非抽象标签？

### 概念设计
- [ ] 每个视觉结构是否反映了概念的行为？
- [ ] 图表是否展示了文字无法单独表达的内容？
- [ ] 每个主要概念是否使用了不同的视觉模式？
- [ ] 是否避免了统一的卡片网格？

### 容器规范
- [ ] 是否有元素可以改为自由浮动文本？
- [ ] 树/时间线是否使用线条+文本而非方框？
- [ ] 字体大小和颜色是否创建了视觉层次？

### 视觉验证（必须渲染）
- [ ] 是否渲染为 PNG 并肉眼检查？
- [ ] 文字是否溢出或截断？
- [ ] 元素是否意外重叠？
- [ ] 箭头是否正确连接？
- [ ] 整体构图是否平衡？

---

## 示例

用户请求：
> "创建一个图表，展示 React 组件生命周期"

生成逻辑：
1. **评估深度** → 技术教程类，需要具体示例
2. **选择模式** → 使用**时间线（Timeline）**展示生命周期顺序
3. **收集证据** → 包含真实的 `componentDidMount`、`useEffect` 代码
4. **分段构建** → Mount → Update → Unmount 三个区域
5. **渲染验证** → 生成 PNG，检查文字可读性，修复间距问题

---

## 与其他工具的区别

| 特性 | 传统图表工具 | 本 Skill |
|------|-------------|---------|
| 布局 | 统一方框网格 | 形状即含义 |
| 内容 | 占位符标签 | 真实代码/数据 |
| 验证 | 人工检查 | AI 自动渲染验证 |
| 定制 | 每个图单独设置 | 统一调色板配置 |
| 教学价值 | 仅展示结构 | 结构+细节都能教学 |

---

## 许可证

与原项目保持一致。
