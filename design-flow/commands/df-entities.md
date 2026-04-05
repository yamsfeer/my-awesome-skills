# df-entities — 重新执行 Phase 2：业务实体识别

重新执行 design-flow 的 Phase 2，修改核心实体定义或关键设计决策。

## 前提条件

读取 `{project-slug}/product-overview.md`，确认项目存在。

若不存在，提示：
> "找不到产品概述文件，请先运行 `/df-vision` 完成 Phase 1。"

## 执行步骤

1. 重新从产品描述中识别实体，展示当前实体列表（Markdown 表格）

2. 使用 `AskUserQuestion` 询问修改范围：
   ```
   question: "需要调整哪些内容？"
   header: "修改范围"
   multiSelect: true
   options:
     - label: "添加遗漏的实体"
     - label: "修改已有实体的字段"
     - label: "调整实体间关系"
     - label: "重新确认关键设计决策"
     - label: "全部重新分析"
   ```

3. 针对勾选项，用 `AskUserQuestion` 逐一收集具体修改意见

4. 更新实体列表并在对话中展示（Phase 2 不生成独立文件，但更新结果将用于 Phase 3）

5. 使用 `AskUserQuestion` 重新确认关键设计决策（每条决策一个 question，提供 2-3 个选项）

6. 展示最终确认的实体和决策，提示用户：
   > "实体已更新，建议同步运行 `/df-contracts` 更新数据契约文件。"
