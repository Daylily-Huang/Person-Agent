---
name: personal-agent-knowledge-ingest
description: Import and compile sources into the Personal Agent LLM Wiki knowledge layer. Use when the user asks to read new materials, process books/PDFs/notes, create source reports, update knowledge indexes, or turn reusable answers into wiki pages.
---

# Personal Agent Knowledge Ingest

Use this skill for `knowledge` workflows.

## Purpose

按 LLM Wiki 流程把资料从原始来源整理为可追溯、可复用、可维护的知识层。

## Reading Order

1. `AGENTS.md`
2. `CODEX.md` if present
3. `knowledge/master_index.md`
4. `knowledge/knowledge_rules.md`
5. Relevant domain `index.md`
6. Relevant source report, synthesis, or raw material index

## Ingest Flow

1. 登记 source：路径、类型、状态、处理日期。
2. 先做单源提取：核心观点、方法、表达、可吸收、不吸收、边界。
3. 再做 synthesis：跨资料综合、冲突、适用场景。
4. 需要长期复用时，生成 `wiki/` 概念页、人物页、问题页或冲突页。
5. 更新领域 `index.md` 和 `log.md`。
6. 更新 `knowledge/master_index.md`，只登记成熟入口。

## PDF / Office Rule

遇到 PDF/DOCX/PPTX/XLSX/图片资料，按项目规则优先使用 `D:\MinerU\run_mineru.ps1` 转 Markdown，再读取生成结果。失败段必须记录，不伪造内容。

## Writeback Boundary

- 可以写 `knowledge/`、`templates/`、过程记录文件。
- 不直接写 `persona/SOUL.md`、长期记忆或关系状态。
- 人格吸收必须生成 `evolution/proposals/` 并等待用户确认。

## Output

用中文输出：

- 处理了哪些来源。
- 生成或更新了哪些文件。
- 哪些结论可追溯到来源。
- 哪些内容暂缓、失败或需要用户确认。
