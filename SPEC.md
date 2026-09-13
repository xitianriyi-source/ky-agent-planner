---
type: 系统规范
project: 考研Agent规划系统
scope: 全系统
version: 1.3
status: active
updated: 2026-08-23
tags: [考研/系统, 规范/SPEC]
---

# 考研 Agent 规划系统｜统一规范

> 本文件是规划系统唯一契约。`PROJECT.md` 只记录路线与决策，冲突时以本文件为准。

## 1. 权威与继承

| 内容 | 唯一数据源 |
|---|---|
| 系统行为与权限 | 本 `SPEC.md` |
| 项目路线和决策记录 | `PROJECT.md` |
| 报考、目标、时间和真实进度 | `01_学科/考研计划/个人基线与考试事实.md` |
| 阶段切换 | `01_学科/考研计划/阶段路线图.md` |
| 本周结果承诺 | 当周 `周计划/*-正式.md` |
| 可执行任务及状态 | `考研任务看板.md` |
| 每日事实 | `00_Daily/YYYY-MM-DD.md` |
| 调整决策 | 当周 `周复盘/YYYY-Www.md` |
| 跨 Agent 请求、待批提案、交接与审计报告 | `02_项目/考研Agent规划系统/coordination/`；仅保存过程材料，不成为学习事实或正式决策源 |
| 展示 | `考研指挥中心_Dashboard.md`，只读投影 |

英语精读规范和数学方法论规范继续管理各自内容。旧 `05_系统/Prompts/**` 与本地 cron 脚本仅作历史参考，不得覆盖本契约。

## 2. 核心原则

1. Markdown Vault 保存事实、规则和决策，不另建业务数据库。
2. AI 生成草案，用户批准目标、正式周计划、重排和规则晋升。
3. 未知字段写 `待确认`；不得推断学习进度、正确率或完成状态。
4. 一项任务只有一个可勾选实例；Kanban 是任务状态源。
5. Daily 记录事实而非预填计划；自动生成内容不等于已经学习。
6. 先人工跑通，再自动化稳定重复动作；系统搭建不挤占主线复习。
7. 每项任务必须有结果、验收证据和未完成处置。

### 2.1 证据状态

| 值 | 含义 |
|---|---|
| `official` | 官方招生信息、大纲或考试文件 |
| `user_fact` | 用户提供的目标、进度、时间或体验 |
| `external_claim` | 博主、学长或其他外部经验 |
| `ai_synthesis` | AI 对材料的转译或建议 |
| `personal_decision` | 用户明确批准的规则或计划 |
| `personal_evidence` | 经个人执行数据重复验证的规律 |

读取到外部材料只能证明来源存在，不能把观点标记为已验证。

## 3. 角色与权限

| 角色 | 职责 | 权限边界 |
|---|---|---|
| 用户 | 提供事实、确认计划、决定取舍 | 唯一最终决策者 |
| Pi | 日常问答、周计划草案、复盘与重排建议 | 不自行修改正式目标或 active 规则 |
| Antigravity 服务器 | 运行夜间审计、英语精读、多模态摄取及后续生产任务 | 只能执行已批准契约；越界变化写为候选 |
| Codex / Claude Code | 开发、测试和维护脚本与 Vault 结构 | 不承担生产定时运行；不自动 git push |
| 确定性脚本 | 查询、汇总和转换已确认数据 | 必须幂等、可 dry-run、有日志，不调用 LLM 作决策 |

## 4. 目录结构

```text
00_Daily/                                   # 每日事实
01_学科/
  考研计划/
    个人基线与考试事实.md
    阶段路线图.md
    周计划/
    周复盘/
    考研任务看板.md
    考研指挥中心_Dashboard.md
  错题库/
    数学一/                                 # M2 创建
    _复习清单/
02_项目/考研Agent规划系统/
  PROJECT.md
  SPEC.md
  HANDOFF.md
  coordination/                              # 非权威的 Agent 协作交换区
    requests/                                # 跨 Agent 工作请求，不保存学习任务
    proposals/                               # 需要批准的跨领域变更提案
    handoffs/                                # 仅保存未完成工作的交接快照
    reports/                                 # 校验、审计与集成健康报告
  domains/                                  # 按人物/主题与领域隔离的蒸馏资产
    mmg-perspective/
      README.md
      modules/
        math/
          README.md
          sources/                         # 数学原始文字稿、manifest、来源登记
          research/                        # Phase 1.x 调研材料
          candidates/                      # 数学域候选规则，不参与正式排程
          synthesis/                       # Phase 2/2.5 综合与检查点
          skill/                           # Phase 3 数学 Skill 与 Phase 4 评分
  rules/
    sources/                                # 跨域规则来源说明；领域来源归属 domains/*/modules/*/sources/
    candidates/                             # 兼容入口；新候选归属对应领域模块
    active/                                 # 用户批准、可被正式系统读取的规则
  integrations/nuwa/
    README.md
    vendor/nuwa-skill/                      # GitHub 上游源码快照，保留独立 .git
    inbox/raw-transcripts/                  # 未分域原始文字稿
  templates/
  scripts/
04_英语精读/
05_系统/
attachments/错题/数学一/
```

### 4.1 Agent 协作交换区

`coordination/` 是多个 Agent 之间的协作接缝，不是新的业务数据源：

- `requests/` 只保存系统维护、诊断或跨 Agent 工作请求；学习任务仍只存在于 Kanban。
- `proposals/` 保存尚待批准的跨领域变化，并引用目标权威文件；周计划草案继续保存在领域目录，规则候选继续保存在对应 `domains/*/modules/*/candidates/`，不复制正文。
- `handoffs/` 只保存被中断工作的最小交接快照；工作完成后直接更新权威文件。
- `reports/` 保存确定性校验、只读审计和集成健康摘要；原始服务器日志不进入 Vault。
- `domains/<perspective>/modules/<domain>/` 保存领域来源、研究、候选、综合和 Skill；当前 MMG 数学模块位于 `domains/mmg-perspective/modules/math/`。
- `integrations/nuwa/vendor/nuwa-skill/` 是 GitHub 上游源码快照，保留独立 `.git`；`integrations/nuwa/inbox/raw-transcripts/` 只保存尚未分域的原始材料。
- `rules/active/` 是跨系统生效规则的统一入口；领域候选不再集中复制到 `rules/candidates/`。

## 5. 计划与执行闭环

### 5.1 周计划

- 草案路径：`周计划/YYYY-Www-草案.md`，包含依据、容量、结果目标、最低交付、质量证据、风险和待确认项。
- 正式路径：`周计划/YYYY-Www-正式.md`，只在用户确认后存在。
- 正式版生成时必须写入 `confirmed_at`；对应草案改为 `status: superseded`，Dashboard 不再把它列为有效计划。
- 周计划描述结果，不复制任务复选框；任务只写入 Kanban。

### 5.2 Kanban

固定列为：`今日（最多3项）`、`进行中（最多1项）`、`本周队列`、`完成`、`取消/改期`。每个任务包含科目、优先级、日期或截止日、可验收结果和稳定 block id。`2026-08-19` 为唯一任务源切换日；此前 Daily 中的 checkbox 只视为历史记录，不参与重复任务验收。

### 5.3 Daily

Daily 只记录实际产出、耗时、质量证据、未完成原因与处置、一个关键错误和一个次日调整。`study_minutes`、专注度等字段默认为空。任务链接可以引用 Kanban block id，但不得复制 checkbox。

### 5.4 周复盘

周日晚上完成。必须记录承诺与实际、质量证据、阶段风险、最大偏差、下周保留/压缩/改期，以及一句策略结论。连续两周未完成 P0/P1 时提出重排，正式变化仍需用户确认。

### 5.5 夜间审计

Antigravity 读取正式周计划、Kanban 和当日事实。在已确认周目标内可生成次日候选；候选写入 `coordination/proposals/`。新增任务、跨科调速、阶段变化或规则变化只能作为待批提案，不得直接修改权威文件。夜间审计不得把未完成任务无声顺延。

## 6. 英语自动化状态

英语材料必须区分：

```yaml
processing_status: processed
study_status: pending
```

只有用户事实记录可以把 `study_status` 改为 `studied`。Dashboard 不把 processed 数量计入学习进度。

## 7. 数学错题试点

M1 人工闭环通过后，用 10 道真实错题验证以下最小字段：

```yaml
type: 错题
subject: 数学一
module: 高等数学
chapter:
knowledge_point:
error_type: 概念不清
source:
source_id:
review_count: 0
last_review: null
next_review:
status: active
created:
images: []
```

错误类型限定为 `概念不清`、`方法不会`、`计算错误`、`审题失误`。前两类和重复性错误展开解法/SOP；偶发错误只记一句错因。1/3/7/15 天仅为候选间隔，必须定义复习通过/失败行为并完成真实试跑后才能自动化。

## 8. Nuwa 规则晋升

Nuwa Skill 尚未安装，只预留适配层。上游 GitHub 仓库属于 `integrations/nuwa/vendor/nuwa-skill/`，保留独立 Git 历史；它是工具依赖，不是语料或规则来源。未分域文字稿进入 `integrations/nuwa/inbox/raw-transcripts/`，分域后进入 `domains/<perspective>/modules/<domain>/sources/`。

领域管道固定为：

```text
vendor source / raw inbox -> domain source record -> research
-> candidate -> synthesis/checkpoint -> skill draft -> shadow -> active/retired
```

候选规则归属对应领域模块，不参与正式排程；全局 `rules/active/` 只保存用户明确批准、允许正式系统读取的生效规则。原文不可覆盖；AI 转译必须能回溯原文。晋升 `active` 需要用户批准，且优先要求个人执行证据。

## 9. 文件与脚本规范

- Markdown 使用 UTF-8 和标准 YAML；日期为 `YYYY-MM-DD`，周号为 `YYYY-Www`。
- 路径相对 Vault 根目录；脚本使用 `MY_LIB_HOME` 或 `VAULT_ROOT`，不写机器绝对路径。
- 自动文件包含 `generated_by`、`generated_at` 和“自动生成”说明。
- Windows/Android 文件名避免冒号、星号、问号、引号、尖括号和竖线。
- 图片进入 `attachments/错题/<科目>/`，笔记保留原图并使用 Obsidian 嵌入。

## 10. 变更与验收

1. 修改契约前先更新 `PROJECT.md` 决策记录。
2. 目标、角色、正式计划、重排和 active 规则必须由用户确认。
3. 自动化先 dry-run，再用小样本验证幂等性和写入范围。
4. 保留旧文件作为归档，不顺手清理用户现有改动。
5. 本地 Agent 不执行自动 commit/push；服务器同步策略独立管理。

M0-lite 验收：Dashboard 30 秒内回答“距考试多久、本周交付什么、今天做什么、最大风险是什么”；自 `2026-08-19` 起，任务全库只有一个可勾选实例。
