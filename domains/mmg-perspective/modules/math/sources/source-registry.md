---
type: nuwa_source_registry
id: mmg-source-registry
status: verified
subject: 考研数学方法论
source_count: 18
canonical_manifest: 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/sources/source-manifest.md
raw_source_root: 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/sources/transcripts
inbox_root: 02_项目/考研Agent规划系统/integrations/nuwa/inbox/raw-transcripts
created_by: Pi
created_at: 2026-08-23
evidence_status: ai_synthesis
---

# MMG 数学来源登记索引

本文件是 MMG 数学模块的来源入口。完整元数据保留在 `canonical_manifest`，原始文字稿位于 `raw_source_root`，尚未分域的新增文字稿进入 `inbox_root`，不直接参与正式规划。

## M4a 核验结论

- manifest 登记来源：18 条。
- canonical path：18/18 存在。
- 原始 transcript：位于数学模块 sources，不由 AI 改写覆盖。
- 6 条候选规则的 `source_id`、`source_file` 与本登记一致。
- 6 条候选规则的 `source_quote` 已通过原文连续子串核验。
- 来源仍属于外部经验材料；候选规则的 `evidence_status` 保持 `ai_synthesis`，不等于个人验证。

## 分域规则

- 数学内容进入 `modules/math/sources/`。
- 英语、政治或混合内容先留在 `integrations/nuwa/inbox/raw-transcripts/`，完成领域判断后进入独立模块。
- 新增来源不覆盖旧文字稿；同一视频更新时追加版本或修订记录，保留原始文件。
- 候选规则必须引用本模块已登记的 `source_id` 和可存在的 `source_file`；无法逐字核验的引语标记为待核验，不得进入 active。
