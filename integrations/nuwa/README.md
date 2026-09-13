# Nuwa Skill Integration

状态：M4a 进行中，Phase 2 已启动。

## 三类资产边界

```text
integrations/nuwa/vendor/nuwa-skill/       # GitHub 上游源码，独立 Git 仓库
integrations/nuwa/inbox/raw-transcripts/   # 尚未分域的原始文字稿
 domains/<perspective>/modules/<domain>/    # 领域来源、研究、候选与 Skill
```

- `vendor/nuwa-skill/` 当前锁定上游提交 `27642f5`，保留其 `.git`、远端和原始目录结构。更新时在该目录内独立 `fetch/pull`，不由 Vault 根仓库代替上游管理。
- `inbox/raw-transcripts/` 保存刚收集但尚未完成科目/领域登记的文字稿；不直接参与正式规划。
- MMG 数学内容位于 `domains/mmg-perspective/modules/math/`，后续英语、政治等内容分别进入独立模块，不与数学 Skill 混写。

## MMG 当前状态

- 数学领域已有 18 条来源、6 条候选规则和 Phase 1.5 审查结果。
- Phase 2 已通过用户检查，五个模型保持独立；当前已生成 Phase 3 数学方法模块 Skill 草案。
- 草案仍需 Phase 4 边界、冲突和保真度测试，不得直接安装为生产 Skill。
- 仍不得写入 `rules/active/`、正式周计划、Kanban 或 Daily。

## 责任边界

Nuwa 适配层只负责调用或解释上游蒸馏流程，并把结果落入对应领域目录。它不得写入 `rules/active/`、正式周计划、Kanban 或 Daily。

## 领域模块最小结构

```text
modules/<domain>/
  sources/       # manifest、source registry、原始 transcript
  research/      # Phase 1.x 调研材料
  candidates/    # 未生效候选规则
  synthesis/     # Phase 2/2.5 综合和用户检查点
  skill/         # Phase 3 草案、Phase 4 评分和版本记录
```

## 规则晋升

```text
source -> research -> candidate -> synthesis/checkpoint
      -> skill draft -> shadow -> active/retired
```

`candidate` 和 `shadow` 不参与正式排程；晋升 `active` 需要用户批准和个人执行证据。
