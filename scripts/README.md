---
type: 系统脚本说明
project: 考研Agent规划系统
status: active
updated: 2026-08-23
---

# Scripts

本目录保存考研规划系统的确定性脚本。脚本必须只读取或只转换已确认数据，保持幂等，不调用 LLM 作决策，并通过 `VAULT_ROOT`、`MY_LIB_HOME` 或相对路径定位 Vault。

## 规划系统完整性校验

```powershell
python "02_项目/考研Agent规划系统/scripts/verify_planning_system.py" --mock
python "02_项目/考研Agent规划系统/scripts/verify_planning_system.py"
```

JSON 输出：

```powershell
python "02_项目/考研Agent规划系统/scripts/verify_planning_system.py" --json
```

指定其他 Vault：

```powershell
python "02_项目/考研Agent规划系统/scripts/verify_planning_system.py" --vault-root "D:\Vault"
```

退出码：

| 退出码 | 含义 |
|---:|---|
| `0` | 没有错误；默认允许警告 |
| `1` | 发现完整性错误，或使用 `--strict-warnings` 时发现警告 |
| `2` | 无法定位合法 Vault 根目录 |

校验器完全只读，不会自动修改 Daily、Kanban、周计划、规则或协作文件。主要检查：

- Kanban 固定列、WIP 上限、任务格式、验收条件、checkbox 状态和全 Vault block id 唯一性；
- 周计划命名、正式版确认、草案替代、日期与容量等式；
- 切换日后的 Daily 文件名、frontmatter 与 checkbox 禁令；
- `coordination/` 文件类型、状态、最小元数据和审批记录；
- candidate/active 规则状态、审批信息及来源文件可追溯性；
- 正式周计划存在时阶段路线仍待批准的风险提示。
