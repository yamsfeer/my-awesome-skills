# Design Flow 完整流程参考

## 1. 三层数据契约设计原则

### 核心思想：数据分层隔离

```
数据库（领域层）→ API 响应（API 层）→ UI 展示（UI 层）
     ↓                  ↓                  ↓
  完整字段            聚合过滤            格式化展示
  含敏感字段          去除敏感字段         多态状态
  后端私有            前后端契约           组件直接消费
```

### 领域层（domain.yaml）设计规范

1. **包含所有字段**，不做裁剪
2. 用注释 `# ⚠️ 禁止暴露` 标注敏感字段（密码哈希、内部标记、审核字段等）
3. 明确字段类型和约束（`required`、`unique`、`indexed`）
4. 记录数据库级别的关系（外键、索引）

```yaml
# 示例
User:
  id: uuid, primary_key
  email: string, unique, indexed  # ⚠️ 禁止暴露（API 层需脱敏）
  password_hash: string          # ⚠️ 禁止暴露
  role: enum[user, admin]        # ⚠️ 禁止暴露
  name: string, required
  avatar_url: string, nullable
  created_at: timestamp
  deleted_at: timestamp, nullable  # 软删除标记 # ⚠️ 禁止暴露
```

### API 层（api.yaml）设计规范

1. **只包含前端需要的字段**，不暴露敏感数据
2. 用聚合对象替代 ID 关联（如 `author` 对象而非 `author_id`）
3. 定义所有端点，包含请求参数和响应体
4. 标注分页、过滤、排序支持

```yaml
# 示例
PostListResponse:
  items:
    - id: string
      title: string
      summary: string           # 摘要（由 content 截取，非原始字段）
      author:
        id: string
        name: string
        avatar_url: string
      created_at: string        # ISO 8601 格式
      like_count: number
      comment_count: number
  pagination:
    total: number
    page: number
    per_page: number

endpoints:
  - GET /posts         # 列表，支持 ?page=&per_page=&tag=
  - GET /posts/:id     # 详情
  - POST /posts        # 创建，需认证
  - PUT /posts/:id     # 更新，需认证+所有权
  - DELETE /posts/:id  # 删除，需认证+所有权
```

### UI 层（ui-schema.yaml）设计规范

1. **按页面/组件组织**，而非按实体组织
2. 明确每个字段的展示格式（日期格式、金额格式、枚举标签）
3. 定义多态状态（loading / empty / error / success / partial）
4. 标注字段来源（来自哪个 API 响应的哪个字段）

```yaml
# 示例
PostCard:
  data_source: GET /posts (items[])
  states:
    loading: 骨架屏，3 行灰色占位
    error: "加载失败，点击重试"
    empty: "还没有内容，点击发布第一篇"
    success: 正常渲染
  fields:
    - field: title
      format: 最多 2 行，超出省略号
      source: items[].title
    - field: created_at
      format: "相对时间（3小时前 / 昨天 / 2024-01-01）"
      source: items[].created_at
    - field: like_count
      format: "≥1000 显示为 1.2k"
      source: items[].like_count
```

---

## 2. UE 状态机 YAML 格式规范

### 结构规范

```yaml
page_name: PageName
description: 页面用途描述

states:
  initial:            # 初始状态（页面加载前）
    ui: loading

  loading:
    ui: 骨架屏 / 加载动画
    transitions:
      - event: fetch_success → success
      - event: fetch_error → error

  success:
    ui: 正常内容展示
    transitions:
      - event: user_action → [target_state]
      - event: data_refresh → loading

  error:
    ui: 错误提示 + 重试按钮
    transitions:
      - event: retry → loading

  empty:
    ui: 空状态提示 + 引导操作
    transitions:
      - event: create_action → [create_page]

error_paths:
  - scenario: 网络断开
    handling: Toast 提示"网络异常"，保留当前页面数据
  - scenario: 登录过期
    handling: 跳转登录页，登录后回跳
  - scenario: 权限不足
    handling: 提示"无权限访问"，返回上一页
```

---

## 3. 线框图约束标记规范

### 标记级别

| 标记 | 级别 | 含义 | 示例 |
|------|------|------|------|
| 🔴 | 硬性约束 | 不可违反，违反会导致功能问题或安全问题 | "未登录不可访问此页面" |
| 🔵 | 软性约束 | 建议遵循，违反会影响体验但不影响功能 | "列表项最多显示 3 行" |
| 🟢 | 设计建议 | 可选优化，能提升体验 | "空状态建议加插画" |

### ASCII 线框图绘制规范

使用以下字符绘制线框图：

```
边框字符：┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼
圆角（可选）：╭ ╮ ╰ ╯
填充：░ 灰色区域，▓ 深灰区域，█ 黑色区域
```

常用组件表示：

```
导航栏：  [← 返回]   标题   [操作]
输入框：  [_________________]
按钮：    [   主要操作   ]  [次要]
列表项：  ○ 标题文字
          副标题文字
图片占位：┌──────┐
          │ IMG  │
          └──────┘
Tab 栏：  [首页] [发现] [我的]
```

---

## 4. Design Token 冻结原则

### 什么是冻结

冻结（`_frozen: true`）意味着这套 Token 是**设计决策的最终产物**，在产品迭代中**不应随意修改**。要修改，需要走正式的设计评审流程。

### 冻结的 Token 结构

```json
{
  "_frozen": true,
  "_version": "1.0.0",
  "_created": "2024-01-01",
  "color": {
    "primary": {
      "50": "#...",
      "100": "#...",
      "500": "#...",  // 主色
      "900": "#..."
    },
    "semantic": {
      "success": "#22c55e",
      "warning": "#f59e0b",
      "error": "#ef4444",
      "info": "#3b82f6"
    },
    "neutral": {
      "0": "#ffffff",
      "50": "#f9fafb",
      "100": "#f3f4f6",
      "900": "#111827",
      "1000": "#000000"
    }
  },
  "typography": {
    "fontFamily": {
      "sans": ["Inter", "system-ui", "sans-serif"],
      "mono": ["JetBrains Mono", "monospace"]
    },
    "fontSize": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px",
      "2xl": "24px",
      "3xl": "30px"
    },
    "lineHeight": {
      "tight": "1.25",
      "normal": "1.5",
      "relaxed": "1.75"
    }
  },
  "spacing": {
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "6": "24px",
    "8": "32px",
    "12": "48px",
    "16": "64px"
  },
  "radius": {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "full": "9999px"
  },
  "shadow": {
    "sm": "0 1px 2px rgba(0,0,0,0.05)",
    "md": "0 4px 6px rgba(0,0,0,0.07)",
    "lg": "0 10px 15px rgba(0,0,0,0.10)",
    "xl": "0 20px 25px rgba(0,0,0,0.15)"
  }
}
```

### 修改冻结 Token 的正确姿势

1. 创建新版本（如 `v1.1.0`）而非直接修改
2. 记录修改原因（为什么要改）
3. 检查所有引用该 Token 的组件是否需要同步更新
