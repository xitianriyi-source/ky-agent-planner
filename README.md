# ky-agent-planner · 考研 Agent 规划系统

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-100%25-blue)

一套由 AI Agent 驱动的考研复习规划系统：用 Obsidian 保存事实与决策，用 Agent 降低记录、规划和复盘的摩擦。系统服务于复习本身，不以功能数量作为成果。

> **English summary** — An agent-driven study-planning system for China's postgraduate entrance exam. Facts and decisions live in an Obsidian vault; agents handle planning, logging and review following explicit rules, domain models and templates, with a verification script to keep the whole system consistent. Designed and maintained by a single developer.

## 系统组成

```
rules/          # 规划与复盘规则（Agent 执行的依据）
domains/        # 各科目领域模型（目标、阶段、评估口径）
templates/      # 计划、日志与复盘模板
coordination/   # 多 Agent 协作与任务交接
integrations/   # 外部系统对接（含错题系统等）
scripts/        # 工具脚本（见下方校验脚本）
docs/           # 系统文档
```

核心文档：

- [PROJECT.md](PROJECT.md) — 项目总览、已确认决策与里程碑
- [SPEC.md](SPEC.md) — 系统规格
- [HANDOFF.md](HANDOFF.md) — Agent 交接与故障切换（换 Agent 或任务中断时从这里开始）

## 校验

系统自带一致性校验脚本，修改规则、领域模型或模板后应运行：

```bash
python scripts/verify_planning_system.py
```

## 与错题系统的关系

本系统是规划层：它决定「今天复习什么、如何评估」，具体的错题管理与艾宾浩斯复盘由配套的 [ky-mistake-system](https://github.com/xitianriyi-source/ky-mistake-system) 执行，两者通过 `integrations/` 对接。

## 状态与维护

开发中（里程碑 M2 进行中）。本项目由作者独立设计与维护，原始开发仓库位于 [Gitee](https://gitee.com/nishida-riichi/ky-agent-planner)，此 GitHub 仓库为镜像。

## License

[MIT](LICENSE)
