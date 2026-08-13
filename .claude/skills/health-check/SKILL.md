---
name: health-check
description: 每周 Harness 健康检查。逐项审查 active_context、master_index、long_term_memory、memory_update_log、evolution/proposals/、settings.json 是否过期。
---

执行以下 8 项检查，发现过期或需更新的内容直接手术式修改，并在 `memory/memory_update_log.md` 登记：

1. **`memory/active_context.md`** — 当前上下文是否过时？Open Tasks 是否已完成或已变更？
2. **`knowledge/master_index.md`** — 索引是否与实际知识目录一致？是否有新增或变更的内容未登记？
3. **`memory/long_term_memory.md`** — 长期记忆是否还准确？有没有需要修正或补充的条目？
4. **`memory/memory_update_log.md`** — 近一周是否有未登记的更新？
5. **`evolution/proposals/`** — 是否有待处理（未归档/未决定）的 proposal？
6. **`.claude/settings.json`** — 项目级配置是否仍然合理？
7. **`.claude/skills/` 与 `.claude/agents/`** — Claude Code 原生 skill / agent 是否与项目参考手册一致？
8. **`.codex/skills/` 与 `C:\Users\<用户名>\.codex\skills\personal-agent-*`** — Codex 项目源文件与用户级安装是否同步？

## 输出规则

- 如果一切正常：只回复 "本周健康检查正常"。
- 如果发现问题：列出修改了哪些文件、改了什么，并在 `memory_update_log.md` 登记。
