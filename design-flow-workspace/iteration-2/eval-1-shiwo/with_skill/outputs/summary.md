# 拾物（Shiwo）设计流程完成总结

## 任务概述

为校园二手闲置物品交易微信小程序「拾物」完成了完整的 6 阶段设计规划，所有产物自主生成，无需人工确认。

---

## 设计流程执行记录

### Phase 1：产品愿景 ✅
- 基于已知信息直接生成（平台/商业模式/目标用户均已明确，无需追问）
- 产品定位：校园面交场景为核心差异化，区别于闲鱼等通用平台
- 路线图分三版本：MVP（核心交易链路）→ v1.5（诚信体系增强）→ v2.0（商业化）

### Phase 2：业务实体识别 ✅
- 识别 8 个核心实体：User / School / Campus / Item / Category / Conversation / Message / Review / Favorite
- 关键设计决策（自主判断）：
  - 金额单位：分（整数），精确无浮点误差
  - 消息架构：Conversation + Message 两级，支持预约面交卡片
  - 评分：1-5 星整数

### Phase 3：三层数据契约 ✅
- 生成 domain.yaml / api.yaml / ui-schema.yaml
- 运行 validate.py 校验：0 错误，0 警告（首次有 1 个 ERROR + 13 个 WARN，已修复）
  - 修复 ERROR：`ReviewItem.role` 改名为 `reviewer_role`，消除与 `User.role` 敏感字段的同名冲突
  - 修复 WARN：UI 层 source 字段引用格式调整，使验证器能正确追溯到 API 响应顶层字段

### Phase 4：UE 业务交互流程 ✅
- 生成 5 个核心页面状态机（共 30+ 个状态节点）
- 生成 5 个线框图文件（home / item-detail / publish-item / messages / profile）
- 生成 Mermaid 可视化状态机 + 状态-线框图对照表
- 生成完全自包含的可交互 HTML 查看器（点击状态节点展示线框图）

### Phase 5：设计系统 ✅
- 调用 ui-ux-pro-max 脚本成功获取推荐：Vibrant & Block-based 风格
- 根据产品特性调整主色：主色调整为青绿（#22c55e，传递校园新鲜感 + 信任感）
- 字体：Inter（正文）/ Calistoga（展示标题）
- 生成 tokens.json（含微信小程序特有规范）和 component-map.yaml（12 个核心组件）

---

## 产出文件清单

| 文件 | 说明 |
|------|------|
| `shiwo-marketplace/product-overview.md` | 产品概述（定位/用户/平台/功能） |
| `shiwo-marketplace/product-roadmap.md` | 产品路线图（MVP → v1.5 → v2.0） |
| `shiwo-marketplace/contracts/domain.yaml` | 领域层数据契约（8 个实体，含敏感字段标注） |
| `shiwo-marketplace/contracts/api.yaml` | API 层数据契约（8 个分组，30+ 个端点） |
| `shiwo-marketplace/contracts/ui-schema.yaml` | UI 层数据契约（6 个页面，多态状态定义） |
| `shiwo-marketplace/ue/state-machine.yaml` | UE 状态机（6 个页面，30+ 个状态节点） |
| `shiwo-marketplace/ue/state-machine-visual.md` | 可视化状态机（Mermaid 图 + 状态-线框图对照） |
| `shiwo-marketplace/ue/state-machine-interactive.html` | 可交互状态机查看器（自包含 HTML，点击状态看线框） |
| `shiwo-marketplace/wireframes/home.md` | 首页线框图（loading / success / empty / error） |
| `shiwo-marketplace/wireframes/item-detail.md` | 商品详情线框图（loading / success / not_found） |
| `shiwo-marketplace/wireframes/publish-item.md` | 发布商品线框图（idle / uploading / error / submitting） |
| `shiwo-marketplace/wireframes/messages.md` | 私信列表+详情线框图 |
| `shiwo-marketplace/wireframes/profile.md` | 个人主页线框图（self / other / edit） |
| `shiwo-marketplace/design/tokens.json` | 冻结的 Design Token（含小程序特有规范） |
| `shiwo-marketplace/design/component-map.yaml` | 组件-数据映射表（12 个核心组件） |

---

## 关键设计决策摘要

| 决策点 | 选择 | 原因 |
|--------|------|------|
| 金额单位 | 分（整数） | 避免浮点精度问题，后端统一存储 |
| 认证方式 | 微信 code 换 JWT | 小程序标准做法，无密码注册 |
| 图片存储 | CDN URL 数组（最多6张） | 轻量化，避免 base64 |
| 消息架构 | Conversation + Message 两级 | 支持未读计数、消息分页、面交卡片 |
| 主色 | 青绿 #22c55e | 传递新鲜感 + 信任感，适合校园场景 |
| 评分 | 1-5 星整数 | 简单直观，大学生易理解 |

---

## 数据契约校验结果

```
✅ 所有检查通过！三层契约完整且一致。
汇总：0 个错误  0 个警告
```

---

## 下一步建议

1. **生成高保真界面**：使用 `ui-ux-pro-max` skill 基于 design/tokens.json 生成具体小程序页面
2. **生成 API 代码**：将 `contracts/api.yaml` 转换为后端接口（Node.js/Python）
3. **生成前端组件**：基于 `design/component-map.yaml` 搭建微信小程序组件库
4. **补充学生证认证流程**：Phase 4 未设计认证页面，可用 `/df-ue` 命令补充
5. **补充搜索页**：SearchPage 状态机和线框图待设计
