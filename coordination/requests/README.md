---
type: Agent协作目录说明
scope: requests
status: active
updated: 2026-08-23
---

# Requests

本目录保存跨 Agent 的系统维护、诊断、开发或生产操作请求，不保存考研学习任务。

## 状态

```text
pending -> claimed -> completed
                   -> blocked
                   -> cancelled
```

## 最小字段

```yaml
type: agent_request
id: AR-YYYYMMDD-NNN
created_at:
created_by:
target_role:
objective:
authority_files: []
allowed_writes: []
requires_approval: false
status: pending
```

- `objective` 必须可验证。
- 涉及 Antigravity 的 cron、服务、生产文件或远端 Git 变化时，`requires_approval` 必须为 `true`。
- 请求不得复制 Kanban checkbox；学习任务仍只存在于 [[01_学科/考研计划/考研任务看板|考研任务看板]]。
- 完成后记录验证结果和目标权威文件，不在本目录维护第二份结果。
