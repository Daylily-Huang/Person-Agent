# Codex Agent References

Codex 当前不把本目录作为原生 subagent 注册目录。本目录用于保存 Personal Agent 的 task agent 参考适配，让 Codex 在需要时按 `personal-agent-agent-router` 读取和模拟执行。

## Canonical Sources

| Reference | Canonical File |
|---|---|
| `memory-agent.md` | `agents/memory_agent.md` |
| `knowledge-agent.md` | `agents/knowledge_agent.md` |
| `teacher-agent.md` | `agents/teacher_agent.md` |
| `researcher-agent.md` | `agents/researcher_agent.md` |
| `creator-agent.md` | `agents/creator_agent.md` |
| `companion-agent.md` | `agents/companion_agent.md` |
| `reviewer-agent.md` | `agents/reviewer_agent.md` |

## Rule

- 这里的 agent 不是独立人格。
- Codex 使用它们时必须先读 `agents/agent_rules.md`。
- 任何 agent 都必须服从 `persona/SOUL.md`、当前 mode 和 quality gate。
- 修改核心人格、长期记忆或关系状态必须走 proposal。
