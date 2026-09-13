---
type: Agent协作目录说明
scope: proposals
status: active
updated: 2026-08-23
---

# Proposals

本目录保存尚待批准的跨领域变化。周计划草案继续保存在 `01_学科/考研计划/周计划/`，规则候选继续保存在对应 `domains/*/modules/*/candidates/`；此处只保存指向领域文件的提案信封，不复制正文。

## 状态

```text
pending -> approved -> applied
        -> rejected
        -> expired
```

`approved` 只表示用户同意；目标权威文件写入并验证后才能标记为 `applied`。

## 最小字段

```yaml
type: agent_proposal
id: AP-YYYYMMDD-NNN
created_at:
created_by:
status: pending
requires_approval: true
authority_files: []
allowed_writes: []
target_files: []
evidence_files: []
summary:
reason:
```

应用后补充：

```yaml
approved_by: user
approved_at:
applied_at:
verification:
```

新增任务、跨科调速、阶段变化、正式周计划变化、重排和 active 规则晋升必须遵守 [[02_项目/考研Agent规划系统/SPEC|SPEC]] 的审批边界。提案本身不参与 Dashboard 学习进度或正式排程。
