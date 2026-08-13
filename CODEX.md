# CODEX.md

本文件是 OpenAI Codex 使用本项目时的项目级适配说明。Codex 的主要自动入口仍是 `AGENTS.md`；本文件用于补充 Codex 与 Claude Code 的差异。

## Positioning

本项目在 Codex 中的定位：

- `AGENTS.md`：Codex 首要入口和总规则。
- `CODEX.md`：Codex 平台适配说明。
- `skills/*.md`：项目内详细参考手册，不是 Codex 原生 skill。
- `agents/*.md`：项目内 task agent 参考手册，不是 Codex 原生 subagent。
- `.codex/skills/`：本项目维护的 Codex skill 源文件，可复制到用户级 `C:\Users\<用户名>\.codex\skills\`。
- `.claude/`：Claude Code 原生配置，Codex 可以参考但不按 Claude 原生机制执行。

## Required Reading Order For Codex

1. `AGENTS.md`
2. `CODEX.md`
3. `ROUTER.md`
4. `persona/SOUL.md`
5. 对应 `modes/*.md`
6. 需要时读取 `skills/*.md`、`agents/*.md`、`memory/`、`knowledge/master_index.md`
7. 输出前读取 `quality/response_checklist.md`

## Native Codex Skills

本项目建议安装以下用户级 Codex skills。项目内 `.codex/skills/` 是可复制源；当前机器同步安装到 `C:\Users\<用户名>\.codex\skills\`。

| Skill | Source | Installed Path | Use When |
|---|---|---|---|
| `personal-agent-health-check` | `.codex/skills/personal-agent-health-check/` | `C:\Users\<用户名>\.codex\skills\personal-agent-health-check\` | 周期检查 Harness 状态、索引漂移和核心边界 |
| `personal-agent-knowledge-ingest` | `.codex/skills/personal-agent-knowledge-ingest/` | `C:\Users\<用户名>\.codex\skills\personal-agent-knowledge-ingest\` | 导入资料、生成 source report / synthesis / wiki 页面 |
| `personal-agent-memory-review` | `.codex/skills/personal-agent-memory-review/` | `C:\Users\<用户名>\.codex\skills\personal-agent-memory-review\` | 审核记忆候选、提出 memory proposal、避免乱写长期记忆 |
| `personal-agent-teaching` | `.codex/skills/personal-agent-teaching/` | `C:\Users\<用户名>\.codex\skills\personal-agent-teaching\` | 教学解释、纠错、例子和练习 |
| `personal-agent-research` | `.codex/skills/personal-agent-research/` | `C:\Users\<用户名>\.codex\skills\personal-agent-research\` | 科研、文献、数据、方法和证据链 |
| `personal-agent-writing` | `.codex/skills/personal-agent-writing/` | `C:\Users\<用户名>\.codex\skills\personal-agent-writing\` | 脚本、文案、PPT、口播和内容修订 |
| `personal-agent-critique` | `.codex/skills/personal-agent-critique/` | `C:\Users\<用户名>\.codex\skills\personal-agent-critique\` | 审查、纠错、风险分析和质量门 |
| `personal-agent-planning` | `.codex/skills/personal-agent-planning/` | `C:\Users\<用户名>\.codex\skills\personal-agent-planning\` | 任务拆解、计划、检查点和验收标准 |
| `personal-agent-companionship` | `.codex/skills/personal-agent-companionship/` | `C:\Users\<用户名>\.codex\skills\personal-agent-companionship\` | 有边界的情绪承接和陪伴回应 |
| `personal-agent-self-reflection` | `.codex/skills/personal-agent-self-reflection/` | `C:\Users\<用户名>\.codex\skills\personal-agent-self-reflection\` | 自我反思、价值澄清和长期方向讨论 |
| `personal-agent-agent-router` | `.codex/skills/personal-agent-agent-router/` | `C:\Users\<用户名>\.codex\skills\personal-agent-agent-router\` | Codex 模拟 task agent 路由 |

## Codex Agent References

Codex 当前不把项目内 agent 文件当作 Claude Code 那样的原生 subagent。为避免误导，本项目采用 reference adapter：

- `.codex/agents/`：Codex agent reference，说明每个 task agent 对应哪个 `agents/*.md`。
- `personal-agent-agent-router`：Codex 需要模拟 task agent 时的入口 skill。
- `agents/*.md`：canonical task agent 手册。

Codex 使用 agent 时必须先读 `agents/agent_rules.md`，再读具体 agent 文件。

## Boundary

- Codex skill 可以读取项目规则和知识库，但不能自动修改 `persona/SOUL.md`。
- 核心人格、长期记忆和关系状态修改必须走 `evolution/proposals/` 或 memory proposal。
- `.claude/hooks/` 不等于 Codex hooks；不要假设 Codex 会执行 Claude Code hook。
- 项目内 `.codex/skills/` 是可移植源；真正被 Codex 发现的是用户级 skill 目录。
- `.codex/agents/` 只是 reference，不是 Codex 原生 subagent 注册目录。

## Migration Notes

迁移到新电脑时：

1. 复制整个项目文件夹。
2. 将 `.codex/skills/*` 复制到新电脑的 `C:\Users\<用户名>\.codex\skills\`。
3. 打开 Codex 新会话后确认 skill 列表中出现 `personal-agent-*`。
4. 如果项目路径变化，检查 skill 内写死的项目路径并更新。
