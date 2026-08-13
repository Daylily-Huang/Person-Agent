---
name: personal-agent-teaching
description: Use when the Personal Agent project needs teaching, explanation, misconception correction, examples, exercises, or concept learning support.
---

# Personal Agent Teaching

## Purpose

在 Codex 中调用项目教学能力。此 skill 是平台包装层，详细规则以 `skills/teaching_skill.md` 和 `agents/teacher_agent.md` 为准。

## Required Reading

1. `AGENTS.md`
2. `CODEX.md`
3. `ROUTER.md`
4. `persona/SOUL.md`
5. `modes/teacher.md`
6. `skills/teaching_skill.md`
7. `agents/teacher_agent.md`
8. `quality/response_checklist.md`

## Output Rule

- 先判断用户当前理解水平。
- 先给结论或定义，再展开背景、逻辑、例子和反思。
- 纠错时说明错在哪里、为什么错、怎么修正。
- 不把教学变成权威压制，不自动写入记忆。
