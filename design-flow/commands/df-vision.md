# df-vision — 重新执行 Phase 1：产品愿景

重新执行 design-flow 的 Phase 1，对现有项目的产品定位进行修改或重新生成。

## 前提条件

使用 `AskUserQuestion` 工具询问目标项目：

```
question: "要对哪个项目重新执行产品愿景？"
header: "选择项目"
options: 扫描当前目录下的子目录，列出含有 product-overview.md 的项目作为选项
```

若当前目录只有一个项目，自动选中，无需提问。

## 执行步骤

1. 读取现有文件（如果存在）：
   - `{project-slug}/product-overview.md`
   - `{project-slug}/product-roadmap.md`

2. 展示当前内容摘要，告知用户哪些信息已存在

3. 使用 `AskUserQuestion` 询问修改范围：
   ```
   question: "需要修改哪些内容？"
   header: "修改范围"
   multiSelect: true
   options:
     - label: "产品定位/名称/核心痛点"
     - label: "目标用户"
     - label: "平台/商业模式"
     - label: "核心功能模块"
     - label: "产品路线图（MVP/v1.5/v2.0）"
     - label: "全部重新生成"
   ```

4. 针对勾选的修改项，用 `AskUserQuestion` 逐一收集新内容（参考 SKILL.md Phase 1 的提问规范）

5. 更新对应文件（`Write` 工具覆写）

6. 展示修改摘要，提示用户：若已完成 Phase 3（数据契约），建议运行 `/df-contracts` 同步更新
