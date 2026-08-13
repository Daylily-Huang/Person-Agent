# Codex Adapter

本目录保存 Personal Agent Harness 的 Codex 适配源文件。

## Important

- Codex 的项目入口仍是根目录 `AGENTS.md`。
- 本目录不是保证自动读取的项目级运行时。
- `.codex/skills/` 是可移植 skill 源文件；当前电脑需要复制到 `C:\Users\<用户名>\.codex\skills\` 才会作为用户级 Codex skill 被发现。

## Included Skills

| Skill | Purpose |
|---|---|
| `personal-agent-health-check` | 检查 Harness 状态、索引和边界漂移 |
| `personal-agent-knowledge-ingest` | 按 LLM Wiki 流程导入资料和沉淀知识 |
| `personal-agent-memory-review` | 审核长期记忆候选并生成 proposal |
| `personal-agent-teaching` | 教学解释、纠错、例子和练习 |
| `personal-agent-research` | 科研、文献、数据和方法 |
| `personal-agent-writing` | 脚本、文案、PPT 和内容修订 |
| `personal-agent-critique` | 审查、纠错、风险分析和质量门 |
| `personal-agent-planning` | 任务拆解、计划和验收标准 |
| `personal-agent-companionship` | 有边界的情绪承接 |
| `personal-agent-self-reflection` | 自我反思和价值澄清 |
| `personal-agent-agent-router` | Codex 模拟 task agent 路由 |

## Agent References

`.codex/agents/` 是 Codex agent reference adapter。Codex 不把它当作原生 subagent 注册目录；实际使用时通过 `personal-agent-agent-router` 读取 `agents/*.md`。

## Sync Rule

修改 `.codex/skills/*/SKILL.md` 后，同步复制到：

`C:\Users\<用户名>\.codex\skills\`

否则当前机器上的 Codex 可能仍使用旧版本。
