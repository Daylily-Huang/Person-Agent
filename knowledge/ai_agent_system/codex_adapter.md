# Codex Adapter 知识卡

## 分类

ai_agent_system

## 来源

- 当前项目结构扫描：2026-06-15
- 本机 Codex 用户目录：`C:\Users\<用户名>\.codex\`
- 当前项目入口：`AGENTS.md`、`CODEX.md`、`.codex/`

## 核心结论

当前项目对 Codex 的适配采用双层结构：

1. 项目内入口：`AGENTS.md` 作为 Codex 主要入口，`CODEX.md` 说明平台差异。
2. 用户级 skill：将 `.codex/skills/*` 同步到 `C:\Users\<用户名>\.codex\skills\`，供 Codex 后续会话发现。

## 为什么不是只建 `.codex/`

项目内 `.codex/` 便于迁移和版本控制，但当前可确认的 Codex skill 发现位置是用户级 `C:\Users\<用户名>\.codex\skills\`。因此 `.codex/skills/` 作为源文件，用户级目录作为安装位置。

## 已适配能力

| 能力 | 说明 |
|---|---|
| 项目入口 | `AGENTS.md` + `CODEX.md` |
| 健康检查 | `personal-agent-health-check` |
| 知识导入 | `personal-agent-knowledge-ingest` |
| 记忆审核 | `personal-agent-memory-review` |
| 项目技能 | `personal-agent-teaching`、`personal-agent-research`、`personal-agent-writing`、`personal-agent-critique`、`personal-agent-planning`、`personal-agent-companionship`、`personal-agent-self-reflection` |
| Agent 路由 | `personal-agent-agent-router` + `.codex/agents/` reference |
| Claude Code 区分 | `.claude/` 仍作为 Claude Code 原生配置，不假设 Codex 执行 Claude hooks |

## 边界

- Codex skill 可以读取和维护项目知识规则，但不能自动修改核心人格。
- 长期记忆、关系状态、人格吸收仍必须走确认或 proposal。
- 复制项目到另一台电脑时，需要手动同步 `.codex/skills/` 到新机器的 Codex 用户级 skill 目录。
- `.codex/agents/` 只是 reference adapter，不是 Codex 原生 subagent 注册。

## 更新时间

2026-06-15
