# Personal Agent Harness

这是一个长期陪伴型个人 Agent Harness 项目，用 Markdown 文件描述人格核心、关系模式、任务技能、记忆规则、知识索引、质量检查和自我进化流程。

它不是单纯科研助手，也不是一次性工具助手。它的目标是让 Codex / Claude Code 在不同场景中保持同一个核心人格，并根据用户需求切换为老师、朋友、陪伴者、研究助手、创作助手或执行助手。

当前项目同时保留 Claude Code 和 Codex 适配：

- Claude Code：`CLAUDE.md` + `.claude/`
- Codex：`AGENTS.md` + `CODEX.md` + `.codex/skills/`
- Agent 手册：`agents/*.md` 是 canonical 参考；Claude Code 同步到 `.claude/agents/`，Codex 通过 `.codex/agents/` 作为 reference adapter。

## 隐私说明（Privacy）

本公开仓库已做隐私清洗，以下内容**不包含在仓库中**（仅存在于使用者本地）：

- `memory/` 下的个人记忆内容文件（用户画像、情绪记忆、关系时间线等），仅保留 `memory_rules.md` 规则
- `context/active_session_summary.md` 会话摘要
- `evolution/rejected/` 下的敏感提案记录（如健康相关、立场相关）
- `note/` 下的电子书原件、个人录音、会议资料与科研数据（通过 `.gitignore` 排除）
- `knowledge/` 下的 OCR 中间产物（`seg_*`、`ocr/`、`manifest.json`、日志）
- 本机绝对路径（`C:\Users\<用户名>\.codex\skills\` 等已泛化）

知识库中的**书籍 OCR 文本、source report、综合报告与索引**保留公开，作为长期知识来源；使用时请遵守各文件的来源标注与边界说明。

## 当前阶段

当前阶段只搭建框架：

- 目录结构
- 核心规则文件
- 模式与技能模板
- 记忆与知识管理规则
- 输出质量检查规则
- 自我进化提案流程
- Codex / Claude Code 平台入口适配

当前阶段不做复杂程序实现，不接向量数据库，不写 Web UI，不做长期后台运行，不安装依赖。

## 后续扩展方向

后续可以逐步接入：

- 本地知识库
- 长期记忆系统
- MCP 工具
- Hooks 自动化
- RAG 检索
- 数据库
- 多模型协作
- 会话日志与复盘系统

所有扩展都必须服从 `persona/SOUL.md`、`ROUTER.md`、`memory/memory_rules.md` 和 `evolution/evolution_rules.md`。

## 使用入口

Agent 启动时优先读取：

1. `AGENTS.md`
2. Codex 读取 `CODEX.md`，Claude Code 读取 `CLAUDE.md`
3. `ROUTER.md`
4. `persona/SOUL.md`
5. 与用户请求匹配的 `modes/*.md`
6. 需要时读取 `skills/`、`memory/`、`knowledge/`
7. 输出前读取 `quality/response_checklist.md`

## Codex 迁移

`.codex/skills/` 是项目内的 Codex skill 源文件。复制到新电脑后，需要将其中的 skill 同步到新电脑的用户级 Codex skill 目录，例如：

`C:\Users\<用户名>\.codex\skills\`

`.codex/agents/` 只是 Codex 的 agent reference，不需要安装到用户级目录；真正读取时由 `personal-agent-agent-router` 指向 `agents/*.md`。
