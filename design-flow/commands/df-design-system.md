# df-design-system — 重新执行 Phase 5：设计系统

重新执行 design-flow 的 Phase 5，修改 Design Token 或组件映射表。

## 前提条件

读取 `{project-slug}/product-overview.md`，确认项目存在。

## 执行步骤

1. 读取现有文件（如果存在）：
   - `{project-slug}/design/tokens.json`
   - `{project-slug}/design/component-map.yaml`

2. 若 tokens.json 存在，展示当前设计系统概要：
   - 主色/辅色
   - 字体族
   - 版本号

3. 使用 `AskUserQuestion` 询问修改范围：
   ```
   question: "需要修改哪些设计系统内容？"
   header: "修改范围"
   multiSelect: true
   options:
     - label: "色彩方案（主色/辅色/中性色/语义色）"
     - label: "字体排版（字体族/字号/行高）"
     - label: "间距/圆角/阴影规格"
     - label: "组件-数据映射表"
     - label: "全部重新生成"
   ```

4. **若修改色彩方案**：
   ```
   question: "选择新的色彩风格方向"
   header: "色彩风格"
   options:
     - label: "活力橙红（运动/健康类）"
     - label: "专业蓝（金融/企业类）"
     - label: "渐变紫粉（社交/娱乐类）"
     - label: "极简中性（工具/效率类）"
   ```
   选择后，尝试调用 ui-ux-pro-max 脚本获取推荐色盘；若失败则手动生成

5. **若修改 tokens.json**：
   - 创建新版本（`_version` 递增，如 `1.0.0` → `1.1.0`）
   - 在 `_changelog` 字段记录本次修改原因
   - 覆写文件（`Write` 工具）

6. **若修改组件映射表**：
   用 `AskUserQuestion` 询问要新增、修改或删除哪些组件绑定，然后更新 `component-map.yaml`

7. 展示修改摘要，版本变更时特别标注：
   > "Design Token 已更新至 v{新版本}，建议检查引用该 Token 的组件是否需要同步调整。"
