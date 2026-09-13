# Candidate Rules

全局候选规则目录仅保留兼容入口。新候选规则必须放入对应领域模块，例如：

```text
domains/mmg-perspective/modules/math/candidates/
```

每条候选规则必须指向领域来源记录，并声明适用科目、阶段、触发条件、建议动作、停止条件和 AI 推断边界。候选规则不得修改正式计划，也不得直接进入 `rules/active/`。
