---
type: Agent交接指南
project: 考研Agent规划系统
status: active
updated: 2026-08-23
tags: [考研/系统, Agent/交接]
---

# Agent 交接与故障切换

本文件只定义接力流程。当前事实始终从权威文件读取，不在这里复制 Kanban、Daily 或阶段状态。跨 Agent 请求、提案、交接和报告的共同边界见 [[coordination/README|Agent 协作交换区]]。

## 选择接手方式

- **同机文件型 Agent（Claude Code 等）**：从 Vault 根目录开始，按下方顺序只读预检后再工作。它可以替代 Codex 做开发和维护。
- **纯聊天 Agent（无 Vault 权限）**：只做建议或草案。向它提供当前正式周计划、Kanban、最新 Daily 和本次目标；最终写回由有文件权限的 Agent 或用户完成。
- **Antigravity**：只运行已批准的生产任务，不承担规划接管。连接服务器前先核对仓库提交是否与本地一致；生产变更继续遵守 `SPEC.md` 和 `AGENTS.md` 的审批边界。

## 接手步骤

1. 按顺序读取 `AGENTS.md`、`SPEC.md`、`PROJECT.md`、当前 `周计划/*-正式.md`、`考研任务看板.md` 和最新相关 Daily/周复盘。
2. 只读检查当前分支、提交、工作区改动和远端/服务器版本。保留既有改动；跨设备时，提交不一致即先报告，不基于旧副本写入。
3. 开始前复述：当前 M 阶段、正式周计划、相关 Kanban block id、本次允许写入范围、待用户确认项。
4. 只在授权范围内执行并验证。正式目标、正式周计划、阶段切换、重排和 active 规则仍由用户确认。
5. 结束时报告：修改文件、验证结果、未完成事项和下一步。任务未完成才创建交接快照；已完成状态直接写回权威文件。

## 最小交接快照

```yaml
type: agent_handoff
id: AH-YYYYMMDD-NNN
created_at:
created_by:
target_role: Pi | development_agent | antigravity
status: active
objective:
authority_files:
relevant_block_ids:
allowed_writes:
completed:
verification:
pending_approvals:
next_step:
git_commit:
working_tree_notes:
```

快照不包含密码、SSH 私钥、令牌、思维链或任务复选框，也不复制权威文件。文件型 Agent 可将临时快照保存为 `02_项目/考研Agent规划系统/coordination/handoffs/YYYY-MM-DD-HHmm-主题.md`。工作完成后将快照标记为 `resolved`；只有未完成工作才保留有效交接。

## 通用启动提示词

```text
你正在接手 C:\my_lib 的考研 Agent 规划系统。

先只读并依次读取：
1. AGENTS.md
2. 02_项目/考研Agent规划系统/SPEC.md
3. 02_项目/考研Agent规划系统/PROJECT.md
4. 当前正式周计划、考研任务看板、最新相关 Daily/周复盘

本次目标：[填写]
允许写入：[填写具体文件或目录]
完成标准：[填写可验证结果]

SPEC.md 是唯一系统契约。保留现有工作区改动，不推断学习进度或完成状态，不复制 Kanban 任务，不自动 commit/push。正式目标、正式计划、阶段切换、重排和 active 规则需要用户明确确认。Antigravity 的 cron、服务、生产文件和远端 Git 变更需要单独批准。

开始编辑前，先报告：你读到的当前 M 阶段、正式周计划、相关 block id、Git/同步状态、拟修改范围和待确认项。
```
