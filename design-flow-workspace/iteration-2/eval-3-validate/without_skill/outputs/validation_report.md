# 数据契约校验报告

**项目路径：** `/Users/yams/my-awesome-skills/design-flow/evals/test-broken-contracts/`
**校验时间：** 2026-03-22
**校验脚本：** `references/validate.py`

---

## 校验结果汇总

| 级别 | 数量 |
|------|------|
| ❌ 错误 | 2 |
| ⚠️ 警告 | 4 |
| **总计** | **6** |

**结论：校验未通过，需修复 2 个错误后方可通过。**

---

## 完整原始输出

```
══════════════════════════════════════════════════════════════
  design-flow 数据契约校验报告
══════════════════════════════════════════════════════════════

▌ API 层 (api.yaml)
  ❌ [A01] 端点 GET /users/me 引用了未定义响应类型 NonExistentType
     💡 在 responses 中补充 NonExistentType 的定义

▌ UI 层 (ui-schema.yaml)
  ⚠️  [U03] 页面 ProductListPage 组件 ProductCard source='items[].title' 中 'title' 不在响应类型 ProductListResponse 中
     💡 ProductListResponse 包含：items, pagination
  ⚠️  [U03] 页面 ProductListPage 组件 ProductCard source='items[].price' 中 'price' 不在响应类型 ProductListResponse 中
     💡 ProductListResponse 包含：items, pagination
  ⚠️  [U01] 页面 UserProfilePage data_source 'GET /api/v1/users/profile' 在 api.yaml 中无对应端点
     💡 检查路径拼写或在 api.yaml 中补充该端点
  ⚠️  [U02] 页面 UserProfilePage 缺少 error 状态
     💡 建议添加处理接口异常的 UI

▌ 跨层一致性
  ❌ [A03] API 响应 UserDetail 直接暴露了敏感字段 password_hash（源：User.password_hash）
     💡 敏感字段需脱敏后暴露（如 email → email_masked）或移除

──────────────────────────────────────────────────────────────
  汇总：2 个错误  4 个警告
──────────────────────────────────────────────────────────────

  ❌ 校验未通过，请修复上述错误后重试。
```

---

## 逐条问题分析与修复建议

### 错误 1 — [A01] API 端点引用未定义的响应类型

**层级：** API 层（`contracts/api.yaml`）
**位置：** `endpoints.user` → `GET /users/me`
**错误描述：** 该端点的 `response` 字段设置为 `NonExistentType`，但该类型在 `responses` 字典中不存在，导致无法确定该接口的返回数据结构。

**根本原因分析：**
从 `api.yaml` 第 65-66 行注释可以看出，这是一个明显的测试用占位错误，`NonExistentType` 从未被定义。根据业务语义，`GET /users/me` 是"获取当前登录用户信息"的端点，应该返回用户详情类型。

**修复建议：**
将 `response: NonExistentType` 改为 `response: UserDetail`（文件中已定义的用户详情类型）。如果需要一个不含敏感字段的用户响应类型，也可以先修复错误 A03（见下文），再让该端点返回清洁后的 `UserDetail`。

```yaml
# 修复前（api.yaml 第 62-66 行）
user:
  - method: GET
    path: /users/me
    auth_required: true
    response: NonExistentType   # ← 错误

# 修复后
user:
  - method: GET
    path: /users/me
    auth_required: true
    response: UserDetail        # ← 改为已定义的合法类型
```

---

### 错误 2 — [A03] API 响应直接暴露敏感字段

**层级：** 跨层一致性（`contracts/api.yaml` 违反 `contracts/domain.yaml` 约束）
**位置：** `responses.UserDetail` → 字段 `password_hash`
**错误描述：** `UserDetail` 响应类型中包含 `password_hash` 字段，而 `domain.yaml` 的 `sensitive_fields_summary` 明确标注该字段"永远不暴露"。这是一个安全漏洞——密码哈希值不应通过任何 API 接口返回给前端。

**根本原因分析：**
`api.yaml` 第 8-13 行注释已自注明这是已知错误。`domain.yaml` 第 13-15 行对 `password_hash` 有明确限制：`note: "⚠️ 禁止暴露 - 永远不返回给前端"`。

**修复建议：**
从 `responses.UserDetail` 中删除 `password_hash` 字段。

```yaml
# 修复前（api.yaml responses.UserDetail）
UserDetail:
  id: string
  name: string
  email: string
  password_hash: string   # ← 删除此行
  created_at: string

# 修复后
UserDetail:
  id: string
  name: string
  email: string
  created_at: string
```

---

### 警告 1 & 2 — [U03] UI 组件字段引用超出响应类型顶层字段范围

**层级：** UI 层（`contracts/ui-schema.yaml`）
**位置：** `pages.ProductListPage.components.ProductCard`
**警告描述：**
- `source: items[].title` — 校验器报告 `title` 不在 `ProductListResponse` 中
- `source: items[].price` — 校验器报告 `price` 不在 `ProductListResponse` 中

**根本原因分析：**
`ProductListResponse` 的顶层字段只有 `items` 和 `pagination`，校验器仅检查了顶层字段名，未做嵌套展开。

实际上，`items` 类型为 `ProductSummary[]`，而 `ProductSummary` 确实包含 `title` 和 `price` 字段。这是**校验器的字段解析局限性**（不支持 `items[].subField` 的嵌套路径），并非真正的数据契约错误。

**修复建议（两种方案）：**

方案 A（推荐）：调整 UI schema 中 `source` 的写法为直接引用展开对象，避免触发校验器的路径解析限制：
```yaml
# 将 source 改写为更明确的嵌套形式，或在 ProductListResponse 中展开 items 类型
components:
  - name: ProductCard
    response_type: ProductSummary   # 新增：明确声明组件消费的子类型
    fields:
      - field: title
        source: items[].title
      - field: price
        source: items[].price
```

方案 B：在 `ProductListResponse` 响应类型中内联展开 items 元素字段说明，使校验器可直接感知：
```yaml
ProductListResponse:
  items: ProductSummary[]   # 保持不变，但同时在校验器中支持嵌套路径解析
  pagination: PaginationMeta
```
实际上这两个警告更多反映校验器需要升级支持嵌套路径，业务逻辑本身是正确的。**短期内可标记为 known-limitation 忽略；长期应改进校验器。**

---

### 警告 3 — [U01] UI 页面引用了不存在的 API 端点

**层级：** UI 层（`contracts/ui-schema.yaml`）
**位置：** `pages.UserProfilePage.data_source`
**警告描述：** `UserProfilePage` 的 `data_source` 设置为 `GET /api/v1/users/profile`，但 `api.yaml` 中该路径不存在，只有 `GET /api/v1/users/me`。

**根本原因分析：**
`ui-schema.yaml` 第 35-37 行注释已自注明这是测试用已知错误——路径拼写不一致（`/users/profile` vs `/users/me`）。

**修复建议：**
将 `UserProfilePage` 的 `data_source` 改为与 `api.yaml` 一致的路径：

```yaml
# 修复前（ui-schema.yaml）
UserProfilePage:
  data_source: "GET /api/v1/users/profile"   # ← 路径错误

# 修复后
UserProfilePage:
  data_source: "GET /api/v1/users/me"        # ← 与 api.yaml 对齐
```

---

### 警告 4 — [U02] UI 页面缺少 error 状态

**层级：** UI 层（`contracts/ui-schema.yaml`）
**位置：** `pages.UserProfilePage.states`
**警告描述：** `UserProfilePage` 只定义了 `loading` 和 `success` 两种状态，缺少 `error` 状态（接口异常时的 UI 处理）。

**根本原因分析：**
`ui-schema.yaml` 第 43 行注释已自注明。对比同文件中 `ProductListPage` 和 `ProductDetailPage`，它们都正确定义了 `error` 状态。这是一个 UI 健壮性缺口——当 API 接口调用失败时，用户界面没有对应的错误处理方案。

**修复建议：**
在 `UserProfilePage.states` 中补充 `error` 状态：

```yaml
# 修复后（ui-schema.yaml）
UserProfilePage:
  route: "/profile"
  data_source: "GET /api/v1/users/me"   # 同时修复 U01
  states:
    loading:
      ui: 骨架屏
    success:
      ui: 用户信息页
    error:                               # ← 新增
      ui: 加载失败，请稍后重试
```

---

## 修复优先级汇总

| 优先级 | 问题代码 | 类型 | 简述 | 影响范围 |
|--------|----------|------|------|----------|
| P0（必须修复） | A03 | ❌ 错误 | 敏感字段 `password_hash` 暴露在 API 响应 | 安全漏洞，涉及用户数据安全 |
| P0（必须修复） | A01 | ❌ 错误 | 端点引用未定义类型 `NonExistentType` | API 契约无法解析，影响所有依赖方 |
| P1（建议修复） | U01 | ⚠️ 警告 | UI 页面引用不存在的端点路径 | 前后端路径不一致，开发时会产生 404 |
| P1（建议修复） | U02 | ⚠️ 警告 | `UserProfilePage` 缺少 error 状态 | 用户体验缺口，异常无处理 |
| P2（可接受/改进校验器） | U03×2 | ⚠️ 警告 | 嵌套字段路径超出校验器解析能力 | 校验器局限，业务逻辑实际正确 |

---

## 附：各契约文件说明

| 文件 | 层级 | 职责 |
|------|------|------|
| `contracts/domain.yaml` | 领域层 | 定义实体字段、约束、敏感字段清单 |
| `contracts/api.yaml` | API 层 | 定义端点、响应类型，承接领域层 |
| `contracts/ui-schema.yaml` | UI 层 | 定义页面状态机、组件与 API 的字段映射 |
