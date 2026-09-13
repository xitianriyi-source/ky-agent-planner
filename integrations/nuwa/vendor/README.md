---
type: nuwa_vendor_registry
id: nuwa-skill-upstream
status: pinned
repository: https://github.com/alchaincyf/nuwa-skill.git
path: 02_项目/考研Agent规划系统/integrations/nuwa/vendor/nuwa-skill
pinned_commit: 27642f5bfed2dc1bbf8ee59a2c1ee602a626bbd7
created_by: Pi
created_at: 2026-08-23
---

# Nuwa 上游源码登记

`vendor/nuwa-skill/` 是从 GitHub 同步的上游源码仓库，保留独立 `.git`。它提供女娲流程、模板和脚本，不是 MMG 数学语料，也不是规划系统事实源。

## 更新方式

在该目录内独立执行只读检查、`git fetch` 和经确认的更新；外层 Vault Git 不替代上游仓库的 Git 历史。更新上游后应记录新的 pinned commit，并重新检查适配器和脚本兼容性。

## 当前边界

- 不从 vendor 目录直接读取候选规则进入正式排程。
- 不把 vendor 示例人物材料当作 MMG 证据。
- 上游脚本的输出必须经过本 Vault 的来源登记、候选状态和审批边界。
