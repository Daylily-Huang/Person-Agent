---
name: personal-agent-critique
description: Use when the Personal Agent project needs review, critique, risk analysis, logic checking, factuality checking, quality gate review, or plan validation.
---

# Personal Agent Critique

## Purpose

在 Claude Code 中调用项目批判审查能力。此 skill 是平台包装层，详细规则以 `skills/critique_skill.md` 和 `agents/reviewer_agent.md` 为准。

## Required Reading

1. `AGENTS.md`
2. `CLAUDE.md`
3. `ROUTER.md`
4. `persona/SOUL.md`
5. `skills/critique_skill.md`
6. `agents/reviewer_agent.md`
7. Relevant `quality/*.md`

## Output Rule

- findings first：先列问题，再给摘要。
- 区分事实错误、逻辑问题、执行风险和边界风险。
- 每个问题给依据和修正方案。
- 不为了显得严格而制造不存在的问题。
