---
type: Agent协作目录说明
scope: reports
status: active
updated: 2026-08-23
---

# Reports

本目录保存确定性校验、只读审计和集成健康摘要，例如规划系统完整性检查、Antigravity 只读审计结果和适配器诊断。

## 约束

- 报告是派生结果，不是学习事实、任务状态或正式决策源。
- 自动报告必须包含 `generated_by`、`generated_at`、输入范围和验证结论。
- 原始服务器日志保留在服务器；Vault 只保存必要摘要和脱敏异常。
- 报告发现越权或需批准变化时，只能创建 `../proposals/` 提案，不得直接修改正式计划、Kanban、阶段或 active 规则。
- 可重复生成的报告应保持幂等；旧报告是否归档由对应脚本的保留策略决定。
