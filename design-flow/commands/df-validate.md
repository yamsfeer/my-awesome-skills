# df-validate — 校验三层数据契约一致性

运行 `references/validate.py` 校验脚本，检查 domain / api / ui-schema 三层契约的完整性与跨层一致性。

## 前提条件

读取 `{project-slug}/product-overview.md`，确认项目存在。

若不存在，提示：
> "找不到产品概述，请先完成 Phase 1（`/df-vision`）。"

## 执行步骤

1. 确认 `contracts/` 目录下三个文件均已生成：
   - `{project-slug}/contracts/domain.yaml`
   - `{project-slug}/contracts/api.yaml`
   - `{project-slug}/contracts/ui-schema.yaml`

   若任一文件缺失，提示用户先运行 `/df-contracts`。

2. 执行校验脚本：

   ```bash
   python3 references/validate.py {project-slug}
   ```

3. 根据输出结果处理：

   **若有 ERROR（❌）**：
   - 展示所有错误条目
   - 使用 `AskUserQuestion` 询问修复方式：
     ```
     question: "校验发现以下错误，需要如何处理？"
     header: "修复方式"
     options:
       - label: "我来描述修改内容，你帮我修复"
       - label: "打开 /df-contracts 逐层调整"
       - label: "我先手动修改文件，修改后再次校验"
     ```
   - 若选择"描述修改内容"，收集用户输入后直接修复对应契约文件，修复完成后重新运行校验

   **若有 WARN（⚠️）**：
   - 展示所有警告条目
   - 使用 `AskUserQuestion` 询问：
     ```
     question: "存在以下警告，是否需要处理？"
     header: "处理警告"
     options:
       - label: "处理警告后继续"
       - label: "忽略警告，继续流程"
     ```

   **若全部通过（✅）**：
   - 输出：
     > "三层契约校验通过！domain / api / ui-schema 完整且一致，可放心进行后续设计。"

## 校验规则说明

| 规则 | 层 | 说明 |
|------|-----|------|
| D02 | domain | 每个实体必须有 primary_key 字段 |
| D04 | domain | 外键引用的实体必须存在 |
| D05 | domain | enum 类型字段必须定义 values |
| D06 | domain | sensitive_fields_summary 与字段标注对齐 |
| A01 | api | 端点引用的响应类型必须在 responses 中定义 |
| A02 | api | responses 中嵌套引用的类型必须存在 |
| A03 | cross | 域层标注"禁止暴露"的字段不得出现在 API 响应中 |
| U01 | ui | data_source 引用的端点必须在 api.yaml 中存在 |
| U02 | ui | 每个页面建议定义 loading 和 error 状态 |
| U03 | ui | 组件字段 source 应可追溯到对应 API 响应字段 |
