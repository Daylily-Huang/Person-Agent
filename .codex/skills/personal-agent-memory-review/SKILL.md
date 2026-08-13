---
name: personal-agent-memory-review
description: Review memory candidates for the Personal Agent Harness. Use when the user asks to remember, forget, update memory, review long-term memory, or decide whether conversation content should become memory.
---

# Personal Agent Memory Review

Use this skill for memory decisions in `F:\桌面\Personal Agent`.

## Purpose

帮助判断某条信息是否应该进入长期记忆、临时上下文、memory proposal，或不记录。

## Reading Order

1. `AGENTS.md`
2. `CODEX.md` if present
3. `memory/memory_rules.md`
4. Relevant memory file:
   - `memory/user_profile.md`
   - `memory/long_term_memory.md`
   - `memory/project_memory.md`
   - `memory/emotional_memory.md`
   - `memory/relationship_timeline.md`
5. `quality/memory_check.md`
6. `quality/emotional_boundary_check.md` if emotion or relationship is involved

## Decision Categories

- 长期记：稳定偏好、长期项目、核心价值观、工作方式、反复出现的思考模式。
- 临时记：当天情绪、某次聊天细节、一次性任务状态。
- proposal：影响人格、长期关系状态、核心偏好或存在不确定性的内容。
- 不记录：未经用户确认的人际关系判断、羞辱性标签、过度情绪化断言、缺少价值的一次性碎片。

## Write Rules

- 用户明确要求写入且符合规则，才可更新 memory 文件。
- 不确定时写 proposal 或先询问。
- 修改长期记忆时同步记录 `memory/memory_update_log.md`。
- 不自动修改 `persona/SOUL.md`。

## Output

用中文输出：

- 建议类别：长期记 / 临时记 / proposal / 不记录。
- 判断依据。
- 若需要写入，给出拟写文本。
- 若已经写入，列出修改文件。
