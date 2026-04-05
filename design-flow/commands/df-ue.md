# df-ue — 重新执行 Phase 4：UE 业务交互流程

重新执行 design-flow 的 Phase 4，修改状态机、线框图，或补充遗漏的交互设计。

## 前提条件

读取 `{project-slug}/product-overview.md`，确认项目存在。

## 执行步骤

1. 读取现有文件（如果存在）：
   - `{project-slug}/ue/state-machine.yaml`
   - `{project-slug}/ue/state-machine-visual.md`
   - `{project-slug}/ue/state-machine-interactive.html`
   - `{project-slug}/wireframes/*.md`（列出所有已有线框图页面）

2. 展示当前设计概要：
   - 已设计的页面列表
   - 每个页面的状态数量
   - 关键交互路径

3. 使用 `AskUserQuestion` 询问修改意图：
   ```
   question: "需要对 UE 设计做什么？"
   header: "修改意图"
   multiSelect: true
   options:
     - label: "修改已有页面的状态机"
     - label: "修改已有页面的线框图"
     - label: "新增页面"
     - label: "补充遗漏的交互逻辑"
     - label: "全部重新生成"
   ```

   > 注意：无论选择哪项，修改完成后**必须同步更新** `state-machine-visual.md`，保持可视化文档与 YAML 和线框图一致

4. **若选择"修改已有页面"**：
   用 `AskUserQuestion` 列出已有页面供选择，再收集具体修改内容

5. **若选择"新增页面"**：
   用 `AskUserQuestion` 询问新页面名称和主要功能，然后生成对应的状态机条目和线框图文件

6. **若选择"补充遗漏的交互逻辑"**：
   展示当前所有线框图内容摘要，然后：
   ```
   question: "请描述需要补充的交互逻辑"
   header: "补充交互"
   multiSelect: true
   options:
     - label: "补充某个新页面"
     - label: "补充某页面的异常状态"
     - label: "补充某条业务操作流程"
     - label: "修改已有的交互逻辑"
   ```

7. 执行修改后：
   - 更新 `state-machine.yaml`
   - 更新对应的 `wireframes/{page-name}.md`
   - **重新生成** `state-machine-visual.md`（Mermaid 图 + 状态-线框图对照表全部同步）
   - **重新生成** `state-machine-interactive.html`（同步更新 STATES 数据对象和 Mermaid 图定义）
   - 重新执行**交互设计评审**（同 SKILL.md Phase 4 Step 5 流程），直到用户确认完整

8. 展示修改摘要，若涉及新实体或新字段，提示：
   > "如果新增了新的数据实体或字段，建议运行 `/df-contracts` 同步更新数据契约。"
