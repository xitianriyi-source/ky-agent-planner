---
type: Agent协作协议
project: 考研Agent规划系统
status: active
updated: 2026-08-23
tags: [考研/系统, Agent/协作]
---

# Agent 协作交换区

> 本目录是 Pi、开发 Agent 与 Antigravity 之间的协作接缝，不是学习事实、正式计划、任务状态或有效规则的数据源。权威边界以 [[02_项目/考研Agent规划系统/SPEC|SPEC]] 为准。

## 内容路由

| 内容 | 目录 | 是否权威 |
|---|---|---|
| 跨 Agent 的系统维护、诊断或开发请求 | `requests/` | 否 |
| 需要用户批准的跨领域变化 | `proposals/` | 否 |
| 未完成工作的最小接力快照 | `handoffs/` | 否 |
| 校验、只读审计和集成健康摘要 | `reports/` | 否 |

以下内容不得进入本目录：

- 学习任务 checkbox；
- Daily 学习事实、正式周计划或周复盘的副本；
- `rules/active/` 的替代副本；
- 密码、SSH 私钥、令牌、原始生产日志或思维链；
- 仅为保存聊天历史而生成的全文记录。

## 写入原则

1. 已确认事实按权限直接写入所属权威文件，不先在这里复制。
2. 未知、越权、跨领域或需要批准的变化写为提案，只引用目标文件和证据。
3. 学习执行任务始终进入 [[01_学科/考研计划/考研任务看板|考研任务看板]]；`requests/` 只承载 Agent 工作。
4. 文件按生命周期分类，不按 Agent 名称分目录；参与者写入 `created_by` 和 `target_role`。
5. 提案被应用后记录 `applied_at` 与 `target_files`，正式结果以目标权威文件为准。
6. 已完成工作直接更新权威文件；只有中断或阻塞时才创建 handoff。

## 公共元数据

除各目录的 `README.md` 外，协作实例文件至少包含：

```yaml
type:
id:
created_at:
created_by:
status:
authority_files:
allowed_writes:
```

涉及用户批准时额外包含：

```yaml
requires_approval: true
approved_by:
approved_at:
```

未知字段写 `待确认`，不得由 Agent 推断。
