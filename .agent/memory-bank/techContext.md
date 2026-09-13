# Tech Context: 技术栈与开发环境规范

## 1. 运行环境与技术栈
- **客户端环境**: Windows 11 / PowerShell 5.1 & 7.x
- **服务器自动化环境**: Linux (Ubuntu), 通过 SSH `ssh antigravity` (alias `tasks-server`) 连接
- **核心开发语言**:
  - **Python 3.10+**: 系统一致性校验、多模态文字稿抽取、规则测试（核心脚本保持零三方包依赖，仅用标准库 `pathlib`, `re`, `dataclasses`, `argparse`）
  - **Node.js**: 英语精读生词导出与墨墨背单词（Maimemo）同步接口
  - **Bash / Shell**: Linux 服务器上的夜间审计与定时维护任务
- **核心数据承载**:
  - **Obsidian Vault**: 笔记、知识 MOC、周复盘报告
  - **Obsidian 插件依赖**: `Dataview`（Dashboard 投影与查询）、`Kanban`（任务状态管理）

## 2. 工具链与常用验证命令
在本地进行任何提交或重构前，运行相关校验：

```powershell
# 1. 规划系统完整性校验（核心防御）
python "scripts/verify_planning_system.py" --vault .

# 2. 数学方法论 Skill 契约测试
python "domains/mmg-perspective/modules/math/skill/verify_phase4.py"

# 3. 语法与静态检查
node --check "05_系统/Scripts/sync_to_maimemo.js"
bash -n "05_系统/Scripts/cron_nightly_audit.sh"

# 4. Agent 任务归档脚本（完成功能后触发）
powershell -ExecutionPolicy Bypass -File "C:\Users\cokerin\.gemini\config\skills\agent-workspace-init\scripts\archive-task.ps1" -TaskName "<task-slug>" -Type "<feat|fix|refactor>"
```

## 3. 约束与编码规范
- **文件编码**: 强制使用 `UTF-8`（无 BOM）。
- **元数据规范**: Markdown 头部必须为标准合法的 YAML frontmatter。
- **排版与命名**:
  - 日期命名规范：`YYYY-MM-DD.md`（如 `2026-08-20.md`）；
  - 周计划命名规范：`YYYY-Www-草案.md` / `YYYY-Www-正式.md`（如 `2026-W35-正式.md`）；
  - 代码缩进：Python 统一 4 空格，JavaScript 统一 2 空格；
  - 路径处理：命令中含中文路径需使用双引号包裹，脚本中禁止硬编码单机绝对路径，优先使用相对路径或动态推导。

## 4. 远程同步与 Git 边界
- 本地开发严禁设置无提示的定时自动 `git push`；
- 版本同步由服务器及指定定时备份方案统一协调；
- 临时产物与日志隔离于 `.agent/scratch/`。
