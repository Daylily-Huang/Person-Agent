---
name: personal-agent-agent-router
description: Use when the Personal Agent project needs task-agent routing, agent reference lookup, simulated subagent behavior, or coordination across memory, knowledge, teacher, researcher, creator, companion, and reviewer agents.
---

# Personal Agent Agent Router

## Purpose

Codex 当前不把项目内 `agents/*.md` 当作原生 subagent。此 skill 用于让 Codex 按参考 agent 规则模拟 task agent，不伪装成真正并行 subagent。

## Required Reading

1. `AGENTS.md`
2. `CODEX.md`
3. `agents/agent_rules.md`
4. Relevant `agents/*.md`
5. Relevant `modes/*.md`
6. Relevant `skills/*.md`
7. `quality/response_checklist.md`

## Routing

| Need | Read |
|---|---|
| 记忆整理 | `agents/memory_agent.md` |
| 知识查找或索引维护 | `agents/knowledge_agent.md` |
| 教学解释 | `agents/teacher_agent.md` |
| 科研任务 | `agents/researcher_agent.md` |
| 创作任务 | `agents/creator_agent.md` |
| 陪伴回应 | `agents/companion_agent.md` |
| 输出审查 | `agents/reviewer_agent.md` |

## Boundary

- Agent 是任务执行者，不是独立人格。
- 不自动修改 `persona/SOUL.md`。
- 不私自写入长期记忆或关系状态。
- 需要写入核心人格或敏感记忆时，先走 proposal。
