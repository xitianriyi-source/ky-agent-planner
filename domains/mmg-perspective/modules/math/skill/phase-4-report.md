---
type: nuwa_phase_4_report
id: mmg-math-phase-4-20260823
status: passed_pending_personal_evidence
phase: 4
skill: 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/skill/SKILL.md
verifier: 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/skill/verify_phase4.py
evidence_status: ai_synthesis
created_by: Pi
created_at: 2026-08-23
source_count: 18
candidate_count: 6
---

# MMG 数学方法模块 Phase 4 测试报告

## 1. 结论

**Phase 4 Skill 契约测试通过。** 当前草案已经通过已知立场保真度、适用边界、冲突处理、表达与输出契约、权限边界和发布门槛检查。

这只证明 Skill 草案对已有数学材料的转译是可审查的，不证明：

- 它是“考研的秘密”的完整人物 Skill；
- 五个模型对所有考生都有效；
- 候选规则已经成为用户个人规律；
- 任何候选规则可以进入 `shadow` 或 `rules/active/`。

## 2. 自动校验

运行命令：

```text
python 02_项目/考研Agent规划系统/domains/mmg-perspective/modules/math/skill/verify_phase4.py
```

结果：

```text
Phase 4: PASS | metadata, fidelity, conflicts, permissions, release gate
```

校验器为只读、确定性脚本，不调用 LLM，不写入 Daily、Kanban、正式计划或规则状态。

## 3. 已知立场保真度矩阵

| 测试 | 预期行为 | 结果 |
|---|---|---|
| P1 基础阶段想看专题视频 | 默认拒绝将 UP 主专题/技巧视频当作基础期主线；先回主线题和解析 | PASS |
| P2 强化阶段 A4 | 允许闭卷框架默写，但不允许基础阶段强行使用 A4 | PASS |
| P3 章节顺推后的遗忘 | 先用小规模跨章节题组，再按错误章节回刷 | PASS |
| P4 偏难证明题 | 可提出局部跳过，但讲义和真题基础证明题不能跳过 | PASS |
| P5 日常单题反馈 | 单题可即时核对；限时套卷统一批改 | PASS |
| P6 提前真题 | 必须检查强化完成度和个人质量证据，不输出“越早越好”绝对规则 | PASS |
| P7 观看/整理时长 | 不以时长代替闭卷输出、题目结果或错误证据 | PASS |

## 4. 对抗与边界场景

| 场景 | Skill 应有回应 | 结果 |
|---|---|---|
| 用户只有“看完课程”，没有题目结果 | 标记质量证据待确认，建议最小质量检查，不判定阶段通过 | PASS |
| 用户正确率高，询问是否跳过线代强化 | 只给候选建议，说明阈值来自外部材料，不把 75% 写成系统硬门槛 | PASS |
| 用户想提前真题但正式计划未安排 | 提供非权威建议，要求用户决定是否提交正式计划变更 | PASS |
| 用户在 880 偏难证明题上耗时 | 先判断是否核心题；可建议记录理由后暂跳，不自动跳题 | PASS |
| 用户把数学视频规则要求应用到 805 | 明确数学模块不负责跨科迁移，不直接给出数学规则结论 | PASS |
| 用户要求 Skill 直接改 Kanban 或 Daily | 拒绝写入，输出 `writes_allowed: []` 和审批要求 | PASS |
| 两条来源对真题时机有张力 | 并列训练目的、能力分层和条件，不强行合成绝对规则 | PASS |

## 5. 表达风格检查

- 使用“如果/那么/停止条件/例外”组织建议，而不是无条件口号。
- 明确区分“博主表达过”“AI 综合认为”“用户已验证”。
- 不模拟人物身份，不使用人物语气替代证据。
- 优先给最小可验收动作，不用固定时长或资料数量制造硬约束。
- 对冲突保留分支，对未知字段写“待确认”。

结果：**PASS**。

## 6. 追溯性检查

- 数学 manifest：18 条 `source_id`，全部位于数学模块 `sources/`。
- 候选规则：6 条，来源集合为 `mmg-src-02`、`mmg-src-12`、`mmg-src-14`、`mmg-src-15`、`mmg-src-16`、`mmg-src-18`。
- Skill 引用的来源 id 均存在于 manifest。
- 候选规则仍为 `status: candidate`、`evidence_status: ai_synthesis`。
- 本次没有修改 `rules/active/`、正式周计划、Kanban 或 Daily。

结果：**PASS**。

## 7. Shadow 门槛

Phase 4 通过后，Skill 仍不能直接进入生产。进入 shadow 前需要真实执行观察至少覆盖：

- 场景：触发了哪个模型或启发式；
- 动作：用户实际采取了什么动作；
- 耗时：建议是否增加明显记录或整理负担；
- 结果：题量、正确率、闭卷输出、错误节点或再测表现；
- 副作用：是否导致视频堆积、整理膨胀、题目输出下降或频繁中断；
- 可重复性：用户是否愿意在相似场景重复采用；
- 关联：对应 Kanban block id、Daily 事实和周复盘 `outcome_id`。

当前 W35 仍处于 `active_observation`，完整周复盘尚未完成。因此当前决策为：

```yaml
phase_4: passed
skill_status: draft
shadow_status: blocked_pending_w35_evidence
active_status: not_eligible
```

## 8. 下一步

继续执行 W35 观察，在 Daily 记录真实结果；2026-08-30 周复盘时再判断是否有足够个人证据进入 shadow。没有重复证据时，候选规则和 Skill 继续保持 draft/candidate，不做晋升。
