# Repository Guidelines & AGENTS.md

> Universal AI Agent Workspace Instructions & Operating Protocol.
> Single Source of Truth for Cursor, Claude Code, Copilot, Antigravity, and other AI coding assistants.

---

## 1. Project Overview & Boundaries

本工作区为**考研 Agent 规划系统**（同时作为 Obsidian 考研知识与规划库的核心工程子集/关联工作区）。
目标：用 Obsidian 保存事实与决策，用 Agent 降低记录和复盘摩擦。系统服务真实复习，不以功能堆砌为目标。

- **目标考试**：深圳大学信息工程学院通信工程（初试 2026-12-19）
- **目标分数**：总分 350（数学一 120、英语一 70、政治 60、专业课805 100）
- **主要执行端**：Pi（日常交互与建议）、Codex / Claude Code（开发与维护）、Antigravity 服务器（定时生产任务）、Nuwa Skill（方法论蒸馏）
- **核心契约**：详见 [SPEC.md](file:///d:/Files/antigarvity/考研Agent规划系统/SPEC.md) 与 [PROJECT.md](file:///d:/Files/antigarvity/考研Agent规划系统/PROJECT.md)。任务中断或切换参阅 [HANDOFF.md](file:///d:/Files/antigarvity/考研Agent规划系统/HANDOFF.md)。

---

## 2. Project Structure & Module Organization

保持各领域现有目录边界：

- `.agent/`: Agent 记忆中枢、当前任务状态、临时探针及归档冷存储。
  - `memory-bank/`: 持久化上下文（`projectbrief`, `productContext`, `systemPatterns`, `techContext`, `activeContext`, `progress`）。
  - `tasks/`: 当前活跃任务执行计划与验证走查（`current_plan.md`, `current_walkthrough.md`）。
  - `scratch/`: 临时调试、实验探针脚本（Git 忽略）。
  - `archive/`: 已完成任务的历史冷存储。
- `coordination/`: 跨 Agent 协作交换区（`requests/`, `proposals/`, `handoffs/`, `reports/`）。仅保存接缝材料，非事实源。
- `domains/`: 按领域/视角沉淀的资产（如 `mmg-perspective/modules/math/` 数学方法论与 Skill）。
- `integrations/`: 外部集成与原始输入（如 Nuwa 文字稿收件箱 `nuwa/inbox/` 与 vendor）。
- `rules/`: 系统规则（`active/` 经用户确认生效，`candidates/` 候选规则，`sources/` 规则源）。
- `scripts/`: 系统确定性校验与自动化工具（如 `verify_planning_system.py`）。
- `templates/`: 规划与复盘模板（`Template_周计划正式.md`, `Template_周复盘.md` 等）。
- `docs/adr/`: 架构决策记录（ADR）。
- 关联外部 Vault 域（若在完整 Vault 根运行）：`00_Daily/`, `01_学科/`, `02_项目/`, `04_英语精读/`, `05_系统/`。

---

## 3. Build, Test, and Development Commands

本项目无统一构建，修改对应模块后需运行就近验证：

```powershell
# 规划系统完整性自检
python "scripts/verify_planning_system.py" --vault .

# 数学技能契约测试
python "domains/mmg-perspective/modules/math/skill/verify_phase4.py"

# 若在完整 Vault 环境：
python "01_学科/自动控制原理/verify_exams.py" --mock
python "01_学科/自动控制原理/verify_exams.py"
node --check "05_系统/Scripts/sync_to_maimemo.js"
bash -n "05_系统/Scripts/cron_nightly_audit.sh"
```

---

## 4. Operational Boundaries & Guardrails

### Always（强制要求）
- 启动新会话或新任务时，**优先读取** `.agent/memory-bank/activeContext.md` 与 `PROJECT.md` 恢复上下文。
- 遵循单一事实源原则（Kanban 为唯一可勾选任务源；Daily 仅记事实；周计划重在结果承诺）。
- 编写脚本时采用外科手术式最小变更，保持幂等性、可 dry-run、日志可审计。
- 临时探针、中间测试脚本必须放置在 `.agent/scratch/`，不得污染工作区根目录。
- 代码与 Markdown 文件严格使用 UTF-8 编码，保留既有 YAML frontmatter。

### Ask First（必须经用户明确批准）
- 晋升任何规则至 `rules/active/`（候选规则绝不能直接进入正式排程）。
- 调整考试事实、基线时间或周计划正式承诺。
- 改变 `coordination/`、`domains/` 等系统规范目录结构。
- 执行可能导致数据丢失或强制覆盖远程 Git 的操作。
- 远程 Antigravity 服务器配置（cron、服务、生产数据文件）。

### Never（严禁操作）
- 提交密码、SSH 私钥、API 令牌或临时日志。
- 将生成的外部材料标记为已验证（必须由用户执行数据生成 `personal_evidence` 后方可验证）。
- 自动执行 `git push`（同步由服务器/备份机制专职负责）。
- 在根目录随意堆放测试脚本或无归属的 Markdown 笔记。

---

## 5. Session Handover & Memory Bank Protocol

### A. 会话启动 (Bootstrapping)
1. 读取 `.agent/memory-bank/activeContext.md` 查看当前阶段、最近决策与交接注意事项。
2. 若涉及长期架构，参考 `.agent/memory-bank/systemPatterns.md`。
3. 若存在执行中任务，检查 `.agent/tasks/current_plan.md`。

### B. 任务结束与归档 (Wrap-up & Archiving)
1. **验收与记录**：在 `.agent/tasks/current_walkthrough.md` 记录验证结果。
2. **任务归档**：将已完成的计划归档至 `.agent/archive/YYYY-MM-DD_<type>_<task-name>/`，或运行：
   - `powershell -File "<skill_path>/scripts/archive-task.ps1" -TaskName "<task-name>" -Type "<type>"`
3. **记忆库同步**：
   - 更新 `.agent/memory-bank/progress.md`（记录里程碑交付物）。
   - 更新 `.agent/memory-bank/activeContext.md`（更新当前状态与下一步焦点）。
4. **清理临时区**：清空 `.agent/scratch/` 中的临时生成文件。

---

## 6. Coding Style & Naming Conventions

- Markdown 使用 UTF-8 与合法 YAML frontmatter。
- 日期格式为 `YYYY-MM-DD`，周名称为 ISO 格式如 `2026-W34`。
- 保留既有中文领域名称与 MOC 模式（如 `MOC_高等数学.md`）。
- Python 缩进 4 格，JavaScript 缩进 2 格。含中文路径在命令中加引号。
- 路径解析优先使用相对路径或环境变量 `MY_LIB_HOME`/`VAULT_ROOT`，避免硬编码机器绝对路径。
