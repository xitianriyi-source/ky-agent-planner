# 规划规则层

本目录保存跨领域的生效规则入口，不保存正式周计划或任务。

```text
domains/*/modules/*/sources/
  -> domains/*/modules/*/candidates/
  -> synthesis/checkpoint
  -> skill/shadow
  -> rules/active/ 或 retired
```

- `domains/*/modules/*/sources/`：领域原始来源记录和逐字稿索引，不覆盖原文。
- `domains/*/modules/*/candidates/`：按领域归属的 AI 蒸馏候选规则，不参与正式排程。
- `rules/active/`：用户明确批准、可被正式周计划和周复盘读取的规则。
- `shadow` 是候选规则的状态，不单设目录；影子期只比较建议与实际结果。

证据状态和晋升权限以 [[SPEC]] 为准。
