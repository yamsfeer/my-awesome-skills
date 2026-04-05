# ui-ux-pro-max Skill 工作原理

## 整体架构

```
用户任务 → Skill 触发 → 脚本查询本地知识库 → 注入设计上下文 → 生成 UI 代码
```

## 目录结构

```
ui-ux-pro-max/
├── SKILL.md          # Skill 主指令文件（触发时展开为上下文）
├── data/             # 本地知识库（CSV 格式）
└── scripts/          # 检索脚本（Python）
```

## 知识库（data/）

所有设计知识**完全存储在本地 CSV 文件中，无需联网**：

| 文件 | 内容 | 大小 |
|------|------|------|
| `styles.csv` | 50+ 种 UI 风格（玻璃拟态、粘土拟态、极简等） | 143k |
| `colors.csv` | 161 个配色方案（按产品类型映射） | 32k |
| `typography.csv` | 57 种字体组合 | 50k |
| `google-fonts.csv` | Google Fonts 完整数据 | 745k |
| `products.csv` | 161 种产品类型 + 推荐设计风格 | 58k |
| `ux-guidelines.csv` | 99 条 UX 规范（含 Do/Don't/代码示例） | 19k |
| `charts.csv` | 25 种图表类型选型指南 | 19k |
| `icons.csv` | 图标库推荐 | 21k |
| `react-performance.csv` | React 性能优化规则 | 15k |
| `app-interface.csv` | 移动端 App 界面规范 | 9.7k |
| `ui-reasoning.csv` | UI 决策推理规则 | 53k |
| `design.csv` / `draft.csv` | 设计系统草稿数据 | 各 106k |
| `landing.csv` | 落地页设计模式 | 17k |

## 检索引擎（scripts/）

| 脚本 | 作用 |
|------|------|
| `core.py` | BM25 搜索引擎，对 CSV 数据做全文检索（纯本地） |
| `design_system.py` | 根据产品类型推导完整设计系统（风格+配色+字体+图标） |
| `search.py` | CLI 入口，支持 `--domain` 参数指定检索领域 |

## 规则优先级体系（SKILL.md 内嵌）

| 优先级 | 分类 | 关键要求 |
|--------|------|----------|
| 1 | 无障碍访问 | 对比度 4.5:1、键盘导航、ARIA 标签 |
| 2 | 触控与交互 | 最小 44×44px、8px+ 间距、加载反馈 |
| 3 | 性能优化 | WebP/AVIF、懒加载、CLS < 0.1 |
| 4 | 风格一致性 | 匹配产品类型、SVG 图标（不用 emoji） |
| 5 | 布局与响应式 | 移动优先、无横向滚动 |
| 6 | 字体与颜色 | 正文 16px、行高 1.5、语义化 token |
| 7 | 动画效果 | 时长 150–300ms，遵守减弱动效设置 |
| 8 | 表单与反馈 | 可见标签、错误靠近字段 |
| 9 | 导航模式 | 可预测返回、底部导航 ≤5 项 |
| 10 | 图表与数据 | 图例、Tooltip、无障碍配色 |

## 网络依赖说明

- **Skill 本身**：完全离线，知识库全部本地化
- **shadcn/ui MCP 集成**：可选，若触发则可能走网络
- **生成代码运行时**：页面加载 Google Fonts 字体需要网络（但这是生成代码的依赖，不是 skill 的依赖）

## 已知局限性

### 偏视觉设计，缺少组件级交互行为规范

`ux-guidelines.csv` 的 `Interaction` 分类仅 8 条，主要覆盖状态表示和视觉反馈，**以下常见交互模式未覆盖**：

- 弹窗（Modal）行为：点击遮罩关闭、Esc 关闭、焦点陷阱（Focus Trap）
- Dropdown / Select 的点击外部收起
- Bottom Sheet 的手势关闭
- Tooltip 的触发与消失逻辑
- Toast 的自动消失时机
- 多步骤表单的返回行为
- 拖拽排序的交互反馈

### 改进方向

可在 `data/ux-guidelines.csv` 中新增 `Component Behavior` 分类，补充组件级交互规范。
