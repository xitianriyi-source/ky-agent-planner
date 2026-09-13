---
type: agent_proposal
id: AP-20260823-001
created_at: 2026-08-23
created_by: Pi
status: approved
requires_approval: true
approved_by: user
approved_at: 2026-08-23
execution_status: active_observation
authority_files:
  - 01_学科/考研计划/周计划/2026-W35-正式.md
  - 01_学科/考研计划/考研任务看板.md
allowed_writes: []
target_files:
  - 01_学科/考研计划/执行细化/2026-W35.md
evidence_files:
  - 02_项目/考研Agent规划系统/coordination/reports/2026-08-23-m4a-mmg-phase-1-5.md
  - 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/research/07-phase-1.5-review.md
  - 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/sources/source-registry.md
summary: 使用 Nuwa Phase 1.5 数学候选规则细化 W35 执行块，不改变正式结果、任务或 active 规则。
reason: W35 已确认，但需要把候选方法转成可观察的执行建议并验证其适用边界。
proposal_scope: execution_detail_only
approval_scope: user_review_of_detailed_plan
---

# AP-20260823-001 W35 执行细化提案信封

## 提案内容

请审查并决定是否采用领域文件中的 W35 执行细化提案：

- 领域文件：[[01_学科/考研计划/执行细化/2026-W35|W35 执行细化提案]]
- 形式：每日学习块、输出证据、候选规则的受限观察点。
- 约束：不增加任务，不改变 block id，不修改正式计划，不晋升规则。

## M4a 依据

- Phase 1.5 已完成 18 条来源、6 条候选规则和逐字引用核验。
- 当前可使用范围主要是数学；英语、政治和 805 不接受跨领域规则移植。
- `mmg-src-02` 提前真题和 `mmg-src-14` 数学技巧视频规则本周明确排除。

## 用户确认结果

- 用户于 2026-08-23 同意执行本次 W35 细化提案。
- 执行范围仅为学习块、输出证据和候选规则观察。
- 不新增 Kanban 任务，不修改正式周计划，不将候选规则写入 `rules/active/`。
- W35 Daily 的真实执行结果将在 8/30 周复盘中统一评估。

## 下一关

本提案批准后进入 `active_observation`，不等于规则生效。Phase 2 已通过用户检查；当前下一关是 Phase 3 草案的 Phase 4 已知立场、边界和冲突测试。
