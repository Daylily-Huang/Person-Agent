# STATUS.md

## Current Stage

框架搭建 + 平台激活完成，进入稳态运行和 Second Brain 渐进优化阶段。

## What Exists

- **人格层**：`SOUL.md` + `cognitive_style.md` + `emotional_map.md` + `language_fingerprint.md` + 价值/边界/张力文件（充实，荣格心理反思方法已写入）
- **模式层**：6 个 mode + mode_rules，每个 mode 有触发条件、输出风格、禁止事项（充实）
- **技能层**：7 个 skill + skill_rules，已从接口定义升级为操作手册（充实）
- **Agent 层**：7 个 task agent + agent_rules，已补充执行逻辑和决策规则（充实）
- **记忆层**：8 个记忆文件完整，`long_term_memory.md`、`project_memory.md`、`relationship_timeline.md` 已填充
- **知识层**：框架完整。Mao/Camus/Jung 三条外部思想线 source reports 和 synthesis 完成；命理线核心三本完成 + bazi_advanced/divination_methods 处理中；已引入 LLM Wiki 式 source / processed / wiki 三层规则
- **质量层**：7 个检查文件（充实）
- **进化层**：所有 proposal 已归档，规则完整，proposals 目录为空
- **上下文层**：规则完整
- **Claude Code 平台**：项目级 `.claude/settings.json`（权限 + PreToolUse 保护 hook + Stop hook + Notification hook）、周检 cron（`.claude/scheduled_tasks.json`）、hook 脚本（`.claude/hooks/protect_core_files.sh`、`.claude/hooks/notify.sh`）、Filesystem MCP（`.mcp.json`）
- **Codex 平台**：`AGENTS.md` 主入口、`CODEX.md` 适配说明、`.codex/skills/` 可移植 skill 源文件、`.codex/agents/` reference adapter、用户级 `personal-agent-*` skills
- **Claude Code Skill/Agent**：`.claude/skills/` 已同步项目高频 skills，`.claude/agents/` 已补齐 7 个 task agents

## What Does Not Exist Yet

- 可运行 Agent 程序、数据库或向量检索、Web UI。
- 完整知识域 Wiki 编译层（当前先从 `life/`、`personal/external_thoughts/`、`ai_agent_system/` 启动）。
- Codex hooks 或 Codex 原生 subagent 注册（当前用 `.codex/agents/` reference adapter，不伪装为原生 subagent）。

## Next Recommended Work

1. **P0**：后续新电脑迁移时同步 `.codex/skills/` 到用户级 Codex skills 目录
2. **P1**：完善 `knowledge/life/wiki/` 和 `knowledge/personal/external_thoughts/wiki/` 的概念页
3. **P1**：对 `knowledge/` 执行周期 lint，修复索引遗漏和状态漂移
4. **P3**：完成 Mao PDF OCR 后补写 source_report_02/05/06（如仍有缺口）
5. **长期**：继续填充 `learning/`、`research/`、`creation/`、`tools/`、`psychology/`
