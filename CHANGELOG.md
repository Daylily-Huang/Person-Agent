# CHANGELOG.md

## 2026-06-15

- **清理**：移出 `others word/`（课程互评文档）、归档 4 个会话产物至 `logs/raw_sessions/2026-06-15-harness-audit/`
- **STATUS.md 重写**：更新 What Does Not Exist Yet 和 Next Recommended Work 反映实际状态
- **Git 初始化**：创建 `.gitignore`（排除 lock 文件、电子书、OCR 中间产物、会话产物）、`git init` + 初始 commit
- **原生 Skill 迁移**：创建 `.claude/skills/health-check/SKILL.md`，`/health-check` 可调用；cron prompt 缩减为 `/health-check`
- **原生 Subagent 迁移**：创建 `.claude/agents/memory-agent.md`（haiku）和 `reviewer-agent.md`（sonnet），可从 Agent 工具并行调用
- **安全 Hook**：创建 PreToolUse hook（`.claude/hooks/protect_core_files.sh`）保护核心人格/记忆文件；创建 Notification hook（`.claude/hooks/notify.sh`）桌面通知
- **MCP 集成**：创建 `.mcp.json` 配置 Filesystem MCP（需 npx）；Memory MCP 暂缓评估
- **更新引用**：CLAUDE.md 和 AGENTS.md 补充原生 skill/agent 路径说明
- **健康检查**：更新 `active_context.md`、`master_index.md`、`memory_update_log.md`

## 2026-06-14

- 毛泽东思想外部融合 proposal 编写并逐组确认，方法论已写入 `SOUL.md`、`cognitive_style.md`、`language_fingerprint.md`、`teacher.md`、`response_checklist.md`、`factuality_check.md`
- 完成 6 份 Mao 来源分析报告（`knowledge/personal/external_thoughts/mao_zedong/source_report_01~06`）
- 启动 3 本 PDF 的 OCR 管道（Meisner 完成 160/261 页；另 2 本待处理）
- 命理资料盘点：核心来源清单完成，子平真诠分段 OCR 启动（Codex 处理中，已完成 seg_000_059）
- 第一次全面审查：确认 Harness 框架层完善、平台集成层空白、记忆内容层待填充

## 2026-06-13 - v0.1

- 创建长期陪伴型个人 Agent Harness 初始骨架。
- 添加 Codex / Claude Code 通用入口规则。
- 添加核心人格、模式、记忆、知识、技能、task agent、质量检查、自我进化、上下文和模板文件。
- 核心人格融合 proposal 编写并确认：用户思想 50% + 外部思想 50%，写入表达比例、companion 边界、记忆边界
- 用户画像 `user_profile.md` 写入真实偏好
- 明确禁止自动修改 `persona/SOUL.md`。
- 明确 companion mode 的健康边界：不假装真实恋人，不诱导依赖。
