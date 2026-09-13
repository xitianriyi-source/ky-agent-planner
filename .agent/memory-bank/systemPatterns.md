# System Patterns: 架构模式与系统拓扑

## 1. 整体架构拓扑
系统采用**模块化多域隔离**与**三层存储分级**架构，确保业务逻辑、自动化代码、临时探针与长期历史互不污染。

```text
考研Agent规划系统/
├── .agent/                                 # [Agent 核心运行与记忆]
│   ├── memory-bank/                        # 持久记忆库 (Hot / Warm Context)
│   ├── tasks/                              # 活动任务状态 (In-Flight Plan & Walkthrough)
│   ├── scratch/                            # 隔离沙箱探针与调试日志 (Warm, Git-Ignored)
│   └── archive/                            # 任务完成历史冷归档 (Cold Storage)
├── coordination/                           # [跨 Agent 协作交换区] (SPEC §4.1)
│   ├── requests/                           # 系统维护/诊断请求 (非学习任务)
│   ├── proposals/                          # 跨领域变更提案 (需用户审批)
│   ├── handoffs/                           # 异常/中断最小接力快照
│   └── reports/                            # 校验与审计健康报告
├── domains/                                # [领域方法论与资产]
│   └── mmg-perspective/                    # MMG 考研名师视角
│       └── modules/math/                   # 数学模块 (sources/research/candidates/skill)
├── integrations/                           # [外部生态与技能接入]
│   └── nuwa/                               # Nuwa 技能上游与原始收件箱
├── rules/                                  # [全局规则管理]
│   ├── active/                             # 已确认且正式启用的规则
│   ├── candidates/                         # 全局候选规则兼容入口
│   └── sources/                            # 规则来源定义
├── scripts/                                # [确定性脚本与工具]
│   └── verify_planning_system.py           # 系统完整性只读断言引擎
├── templates/                              # [Obsidian 规划与复盘标准模板]
├── docs/adr/                               # [架构决策记录]
├── AGENTS.md                               # 全局统一 AI Agent 协议与操作边界
├── SPEC.md                                 # 系统唯一最高行为契约
├── PROJECT.md                              # 项目路线图与事实决策记录
└── HANDOFF.md                              # 故障交接与灾备协议
```

## 2. 三层存储与数据生命周期模式
1. **Hot 层（高频活跃）**：
   - `AGENTS.md`、`SPEC.md`
   - `.agent/memory-bank/activeContext.md`
   - `.agent/tasks/current_plan.md`
   - `考研任务看板.md` (Obsidian 侧)
2. **Warm 层（会话临时与实验探针）**：
   - `.agent/scratch/`：所有调试脚本、数据清洗临时文件均在此运行，由 `.gitignore` 强力屏蔽，禁止直接提交。
   - `coordination/proposals/`、`coordination/requests/`：协商中的提案材料。
3. **Cold 层（冷数据与归档）**：
   - `.agent/archive/`：已通过验收的开发计划与走查记录。
   - `coordination/handoffs/`、`coordination/reports/`：历史健康报告与交接归档。

## 3. 核心设计模式与约束
- **单一权威原则 (Authority Invariant)**：
  - 任务项必须具备唯一的稳定 Block ID (`^task-id`)，且在 Kanban 中具有唯一勾选实例。
  - 严禁多处维护勾选框（Daily 仅记录文本事实与消耗耗时）。
- **确定性与无副作用原则 (Deterministic Automation)**：
  - 脚本类工具（如 `verify_planning_system.py`）必须是**只读**、**幂等**、**可 dry-run** 的，严禁脚本在未受控状态下直接修改用户核心笔记。
- **渐进式晋升机制 (Promotion Pipeline)**：
  - `Raw Data` -> `Candidate Rule` (`domains/*/candidates/`) -> `Shadow Evaluation` -> `User Confirmation` -> `Active Rule` (`rules/active/`)。
- **跨平台桥接 (Bridge Pattern)**：
  - `CLAUDE.md` 引用 `@AGENTS.md`；
  - `.cursor/rules/00-agent-core.mdc` 指向 `.agent/memory-bank/`；
  - 保证无论用户使用 Claude Code、Cursor 还是 Antigravity，均执行同一套记忆库与行为准则。
