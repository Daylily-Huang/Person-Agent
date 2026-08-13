# AI Agent System Knowledge Log

## [2026-06-15] ingest | Karpathy LLM Wiki

- 新增 `knowledge/ai_agent_system/llm_wiki_karpathy.md`。
- 建立 `knowledge/ai_agent_system/index.md` 和 `knowledge/ai_agent_system/log.md`。
- 建立 `knowledge/ai_agent_system/wiki/index.md`。
- 采用中度改造：Markdown + Git + 索引 + 日志，不引入数据库或向量检索。

## [2026-06-15] adapter | Codex 适配

- 新增 `CODEX.md` 作为 Codex 平台适配说明。
- 新增 `.codex/skills/` 保存项目可移植 Codex skill 源文件。
- 新增 `knowledge/ai_agent_system/codex_adapter.md` 记录 Codex 适配方式和迁移边界。

## [2026-06-15] adapter | Skill / Agent 全量适配

- 新增 7 个项目 skill 的 Codex / Claude Code 包装层。
- 新增 `personal-agent-agent-router`，用于 Codex 模拟 task agent 路由。
- 新增 `.codex/agents/` 作为 Codex agent reference adapter。
- 补齐 `.claude/agents/` 中 teacher、researcher、creator、companion、knowledge agent。
