# knowledge_rules.md

## Purpose

定义知识库如何组织和读取。

## Core Principle

知识库是 Personal Agent 的长期第二大脑，但不是无边界资料堆。知识只在相关时读取，不允许无关读取污染上下文。

知识库采用 LLM Wiki 思路：原始资料保留为 source of truth，Agent 将资料逐步编译为可维护、可追溯、可交叉链接的 Markdown Wiki。

## Organization

知识按用途分类，而不是只按学科分类：

- `personal/`：个人资料、个人偏好、生活背景。
- `learning/`：学习资料、课程、考试。
- `research/`：科研、论文、数据、方法。
- `creation/`：自媒体、脚本、PPT、商业表达。
- `tools/`：软件、命令、工作流。
- `psychology/`：心理学和情绪支持知识。
- `life/`：生活决策和现实事务。
- `ai_agent_system/`：Agent 架构、提示词、自动化系统。

## Source Handling

- 原始资料应保留。
- Markdown 作为可读知识层。
- `master_index.md` 作为导航层。
- 需要引用时标明来源。
- 不确定事实必须标注。

## Layer Model

| Layer | Purpose | Edit Rule |
|---|---|---|
| Source / Raw | 原始 PDF、EPUB、网页、笔记、图片和附件 | 只读保留，不覆盖、不伪造 |
| Processed | OCR、单本报告、章节索引、证据表、综合报告 | 可由 Agent 生成和修订，但必须保留来源 |
| Wiki | 概念页、人物页、主题页、问题页、冲突页、领域综述 | 可由 Agent 维护，必须更新索引和日志 |

## LLM Wiki Operations

### Ingest

新增资料时：

1. 登记来源、路径、类型、处理状态。
2. 先做单本或单源提取，不直接融合进人格或长期记忆。
3. 再根据需要更新概念页、主题页、人物页或综合页。
4. 更新对应领域 `index.md` 和 `log.md`。

### Query

回答知识型问题时：

1. 先读 `master_index.md`。
2. 再读对应领域 `index.md`。
3. 只读取最小相关的 source report、synthesis 或 wiki 页面。
4. 输出中区分事实、原文观点、Agent 推断和现实建议。

### Writeback

以下内容可以沉淀为知识卡或 Wiki 页面：

- 多次可能复用的长回答。
- 跨资料综合出的稳定概念。
- 用户明确要求保留的分析。
- 纠错、反思、方法论和工作流经验。

以下内容不要直接写入知识库：

- 一次性聊天碎片。
- 未经确认的人际关系判断。
- 缺少来源的强事实结论。
- 情绪化、宿命化或可能伤害现实判断的断言。

### Lint

定期检查：

- `master_index.md` 与真实目录是否一致。
- 领域 `index.md` 是否漏掉重要页面。
- `log.md` 是否记录了新增、修订和检查。
- 是否存在孤儿页、重复页、过时结论或来源缺失。
- source report、synthesis 和 wiki 页面是否有明显矛盾。
- 知识库更新是否绕过了 persona / memory 的 proposal 边界。

## Reading Rule

先读 `master_index.md`，再读对应领域 `index.md`，最后读最小相关资料。不要为了“更全面”读取无关目录。

## Boundary

- 知识库可以支撑人格提案，但不能自动修改 `persona/SOUL.md`。
- 知识库可以提示长期记忆候选，但不能自动写入长期记忆。
- 个人思想融合、关系状态和核心偏好变更，必须走 `evolution/proposals/` 或 memory proposal。
