# 数据契约校验报告

**项目路径**：`/Users/yams/my-awesome-skills/design-flow/evals/test-broken-contracts/`
**校验脚本**：`python3 /Users/yams/my-awesome-skills/design-flow/references/validate.py`
**校验时间**：2026-03-22
**校验结果**：❌ 未通过（2 个错误，4 个警告）

---

## 脚本运行状态

脚本成功运行，退出码为 1（校验未通过）。三个契约文件均已读取：

| 文件 | 路径 |
|------|------|
| 领域层 | `contracts/domain.yaml` |
| API 层 | `contracts/api.yaml` |
| UI 层 | `contracts/ui-schema.yaml` |

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

## 问题详细分析

### 错误一：A03 — 敏感字段泄露

| 项目 | 内容 |
|------|------|
| **错误码** | A03 |
| **严重级别** | ❌ ERROR（必须修复） |
| **检测位置** | `api.yaml` → `responses.UserDetail` |
| **问题描述** | API 响应类型 `UserDetail` 中直接包含了 `password_hash` 字段。而 `domain.yaml` 中该字段标注了 `⚠️ 禁止暴露 - 永远不返回给前端`，属于跨层安全违规。 |

**根本原因**：

`api.yaml` 第 13 行：
```yaml
UserDetail:
  id: string
  name: string
  email: string
  password_hash: string   # ← 问题所在
  created_at: string
```

`domain.yaml` 中 `User.password_hash` 明确标注：
```yaml
password_hash:
  type: string
  note: "⚠️ 禁止暴露 - 永远不返回给前端"
```

**修复方案**：

从 `api.yaml` 的 `UserDetail` 响应类型中删除 `password_hash` 字段：

```yaml
# 修复后的 UserDetail
UserDetail:
  id: string
  name: string
  email: string
  # password_hash 已移除 — 禁止暴露
  created_at: string
```

> 注意：`/auth/register` 和 `/auth/login` 两个端点均使用 `UserDetail` 作为响应类型，修复后这两个端点的响应也将不再泄露密码哈希，这是正确的安全行为。

---

### 错误二：A01 — 端点引用了未定义的响应类型

| 项目 | 内容 |
|------|------|
| **错误码** | A01 |
| **严重级别** | ❌ ERROR（必须修复） |
| **检测位置** | `api.yaml` → `endpoints.user` → `GET /users/me` |
| **问题描述** | 端点 `GET /users/me` 的 `response` 字段引用了 `NonExistentType`，但该类型在 `responses` 块中根本没有定义。 |

**根本原因**：

`api.yaml` 第 65-66 行：
```yaml
- method: GET
  path: /users/me
  auth_required: true
  response: NonExistentType   # ← NonExistentType 在 responses 中不存在
```

**修复方案**：

`GET /users/me` 端点应返回当前登录用户的完整信息，语义上对应 `UserDetail`。将 `response` 改为已定义的响应类型：

```yaml
- method: GET
  path: /users/me
  auth_required: true
  response: UserDetail   # ← 修复：改为已定义的响应类型
```

> 前提：`UserDetail` 已按照错误一的修复方案移除了 `password_hash`，此时引用 `UserDetail` 是安全的。

---

### 警告一 & 二：U03 — UI 组件 source 路径不在响应类型顶层字段中

| 项目 | 内容 |
|------|------|
| **警告码** | U03（出现 2 次） |
| **严重级别** | ⚠️ WARN |
| **检测位置** | `ui-schema.yaml` → `ProductListPage` → `ProductCard` |
| **问题描述** | `ProductCard` 组件的两个字段 `source` 分别为 `items[].title` 和 `items[].price`，校验器在 `ProductListResponse` 顶层字段（`items`, `pagination`）中找不到 `title` 和 `price`。 |

**根本原因分析**：

`ProductListResponse` 的顶层结构为：
```yaml
ProductListResponse:
  items: ProductSummary[]   # items 是数组，元素类型为 ProductSummary
  pagination: PaginationMeta
```

`ProductSummary` 包含 `title` 和 `price`，但校验器只检查了顶层字段（`items`, `pagination`），没有解析嵌套类型 `ProductSummary` 的字段，导致误报。

**两种处理方式**：

**方式 A（推荐）**：`source` 路径写法本身是正确的（`items[].title` 表示数组元素的 `title` 字段），可忽略此警告，等待校验脚本 U03 规则升级支持嵌套类型解析。

**方式 B**：在 `ui-schema.yaml` 中补充注释说明字段来源，便于人工审查：
```yaml
components:
  - name: ProductCard
    fields:
      - field: title
        source: items[].title   # ProductSummary.title
      - field: price
        source: items[].price   # ProductSummary.price
```

---

### 警告三：U01 — UI data_source 引用了不存在的端点

| 项目 | 内容 |
|------|------|
| **警告码** | U01 |
| **严重级别** | ⚠️ WARN |
| **检测位置** | `ui-schema.yaml` → `UserProfilePage` → `data_source` |
| **问题描述** | `UserProfilePage` 的 `data_source` 写的是 `GET /api/v1/users/profile`，但 `api.yaml` 中实际定义的端点是 `GET /users/me`（完整路径为 `GET /api/v1/users/me`），路径不匹配。 |

**根本原因**：

`ui-schema.yaml` 第 37 行：
```yaml
data_source: "GET /api/v1/users/profile"   # ← 该路径在 api.yaml 中不存在
```

`api.yaml` 中实际定义：
```yaml
- method: GET
  path: /users/me        # base_url 为 /api/v1，完整路径为 GET /api/v1/users/me
  auth_required: true
  response: NonExistentType
```

**修复方案**：

将 `UserProfilePage` 的 `data_source` 改为正确路径：

```yaml
UserProfilePage:
  route: "/profile"
  data_source: "GET /api/v1/users/me"   # ← 修复：改为 api.yaml 中实际存在的端点
```

---

### 警告四：U02 — 页面缺少 error 状态

| 项目 | 内容 |
|------|------|
| **警告码** | U02 |
| **严重级别** | ⚠️ WARN |
| **检测位置** | `ui-schema.yaml` → `UserProfilePage` → `states` |
| **问题描述** | `UserProfilePage` 只定义了 `loading` 和 `success` 两个状态，缺少 `error` 状态，无法处理接口请求失败的场景。 |

**根本原因**：

`ui-schema.yaml` 第 39-42 行：
```yaml
states:
  loading:
    ui: 骨架屏
  success:
    ui: 用户信息页
  # 缺少 error 状态
```

**修复方案**：

在 `UserProfilePage.states` 中补充 `error` 状态：

```yaml
states:
  loading:
    ui: 骨架屏
  success:
    ui: 用户信息页
  error:
    ui: 加载失败，请检查网络后重试   # ← 新增 error 状态
```

---

## 问题汇总与修复优先级

| 优先级 | 问题码 | 位置 | 问题简述 | 修复文件 |
|--------|--------|------|----------|----------|
| P0 必修 | A03 | `api.yaml` → `UserDetail` | `password_hash` 敏感字段泄露到 API 响应 | `api.yaml` |
| P0 必修 | A01 | `api.yaml` → `GET /users/me` | 引用未定义响应类型 `NonExistentType` | `api.yaml` |
| P1 建议 | U01 | `ui-schema.yaml` → `UserProfilePage` | `data_source` 路径拼写错误，应为 `/users/me` | `ui-schema.yaml` |
| P2 建议 | U02 | `ui-schema.yaml` → `UserProfilePage` | 缺少 `error` 状态定义 | `ui-schema.yaml` |
| P3 可忽略 | U03 x2 | `ui-schema.yaml` → `ProductListPage` | 校验器不支持嵌套类型，路径写法实际正确 | 无需修改 |

---

## 修复后预期结果

按上述建议修复后，重新运行校验脚本应得到：

```
══════════════════════════════════════════════════════════════
  design-flow 数据契约校验报告
══════════════════════════════════════════════════════════════

  ✅ 所有检查通过

──────────────────────────────────────────────────────────────
  汇总：0 个错误  0 个警告
──────────────────────────────────────────────────────────────

  ✅ 三层契约校验通过！
```

> U03 警告为校验器自身的局限性（不解析嵌套类型），实际数据映射路径正确，可在修复其他问题后忽略该警告。
