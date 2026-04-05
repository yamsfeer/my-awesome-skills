# df-contracts — 重新执行 Phase 3：三层数据契约

重新执行 design-flow 的 Phase 3，修改或重新生成领域层/API 层/UI 层数据契约。

## 前提条件

读取以下文件确认前置阶段已完成：
- `{project-slug}/product-overview.md`（Phase 1 产出）

若不存在，提示：
> "找不到产品概述，请先完成 Phase 1（`/df-vision`）。"

## 执行步骤

1. 读取现有契约文件（如果存在）：
   - `{project-slug}/contracts/domain.yaml`
   - `{project-slug}/contracts/api.yaml`
   - `{project-slug}/contracts/ui-schema.yaml`

2. 展示当前契约概要（实体数量、端点数量、UI 组件数量）

3. 使用 `AskUserQuestion` 询问修改范围：
   ```
   question: "需要修改哪一层的契约？"
   header: "修改范围"
   multiSelect: true
   options:
     - label: "领域层（domain.yaml）— 实体字段、敏感标注、索引"
     - label: "API 层（api.yaml）— 端点、响应体结构"
     - label: "UI 层（ui-schema.yaml）— 展示字段、格式化规则、多态状态"
     - label: "全部重新生成"
   ```

4. 针对勾选的层，使用 `AskUserQuestion` 进一步收集具体修改需求：
   - 领域层：新增/删除字段？调整敏感字段标注？
   - API 层：新增端点？修改响应结构？调整分页/过滤规则？
   - UI 层：新增组件状态？调整展示格式？

5. 重新生成勾选层的文件（`Write` 工具覆写），参考 `references/templates/` 对应模板

6. **运行契约校验**，确保修改后三层仍然一致：

   ```bash
   python3 references/validate.py {project-slug}
   ```

   - 若有 ERROR：立即修复，再次校验直至通过
   - 若有 WARN：展示警告，使用 `AskUserQuestion` 询问是否处理

7. 展示修改摘要，若 UI 层有变更，提示：
   > "UI 层契约已更新，建议运行 `/df-ue` 检查线框图是否需要同步调整。"
