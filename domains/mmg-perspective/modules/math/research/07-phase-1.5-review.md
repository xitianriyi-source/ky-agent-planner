---
type: nuwa_review
generated_by: nuwa_pipeline
generated_at: 2026-08-21
note: 本文件由 Nuwa 自动化流水线生成，汇总 Phase 1.5 调研审查结果，不参与正式排程。
---

# Phase 1.5 调研修复与 Review 报告

## 1. 研究来源数量与元数据汇总

- 入选语料总量：18 份考研数学专项文字稿，均来源于博主“考研的秘密”。
- 时间跨度：2026-03-05 至 2026-08-21，覆盖基础期、强化期至暑期过渡。
- 规范 manifest：`domains/mmg-perspective/modules/math/sources/source-manifest.md`。
- 所有语料拥有唯一 `source_id`（`mmg-src-01` 至 `mmg-src-18`）和规范相对路径。

## 2. 六条候选规则摘要

| 规则文件 | source_id | 核心主张 | 适用阶段 | 核心边界 |
|---|---|---|---|---|
| `candidate_mmg_A4_method.md` | mmg-src-15 | A4 框架默写与动态扩充 | 强化 | 必须闭卷默写，基础期不适用 |
| `candidate_mmg_custom_papers.md` | mmg-src-18 | 跨章节拼好卷抗遗忘 | 强化 | 已有全书基础后使用 |
| `candidate_mmg_drop_proofs.md` | mmg-src-16 | 证明题分层与投入产出取舍 | 通用 | 抓讲义/真题基础，跳过偏难怪题 |
| `candidate_mmg_instant_feedback.md` | mmg-src-12 | 日常单题及时反馈 | 通用 | 全真限时套卷除外 |
| `candidate_mmg_early_past_papers.md` | mmg-src-02 | 真题卷提前介入 | 冲刺 | 需先满足个人能力门槛 |
| `candidate_mmg_no_topic_videos_early.md` | mmg-src-14 | 限制基础期技巧视频 | 基础 | 强化期可按薄弱点定向使用 |

候选文件位置：`domains/mmg-perspective/modules/math/candidates/`。候选仍为 `status: candidate`、`evidence_status: ai_synthesis`。

## 3. 逐条引用核验

6 条候选规则的 `source_id`、`source_file` 与数学模块 manifest 一致；6 条 `source_quote` 均通过原始 transcript 的连续子串核验，并标记 `verbatim_match`。

| 规则 | source_id | 核验 |
|---|---|---|
| A4 大法 | mmg-src-15 | PASS |
| 拼好卷 | mmg-src-18 | PASS |
| 证明题取舍 | mmg-src-16 | PASS |
| 即时对答案 | mmg-src-12 | PASS |
| 提前真题 | mmg-src-02 | PASS |
| 限制技巧视频 | mmg-src-14 | PASS |

## 4. 原文矛盾点

1. 对顶尖学生，部分材料认为往年真题信息增量有限；另一部分材料又警告不要因“真题简单”而轻视真题。该矛盾应按能力和目的分流，不能调和成绝对规则。
2. 材料同时强调严格执行主线规划和根据真实反馈调整拼好卷策略，说明其方法不是机械顺推，而是“主线约束下的反馈修正”。

## 5. 信息缺口

- 原稿缺少互动数据，方法论提取主要基于正文与标题。
- 表达风格和他者视角文件是 Phase 1.5 调研材料，但不是独立的完整外部证据库；它们不阻断数学候选规则的原文核验。
- 当前内容只足以支持数学方法论模块，不足以支持英语、政治或 805 模块。

## 6. 不适用于当前用户的内容

- 跳过线代强化的激进路线只针对高基础且有明确正确率门槛的人，不作为默认规则。
- 9 小时等单日时长属于博主经验，不进入系统硬约束。
- 英语和政治片段已留在 `integrations/nuwa/inbox/raw-transcripts/`，不进入数学模块。

## 7. Phase 1.5 结论

**候选生成门槛通过。** 来源、引用和边界已经足以进入 Phase 2 数学方法论综合；这不等于完整人物 Skill 通过，也不等于任何候选规则已经生效。
