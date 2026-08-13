# Karpathy LLM Wiki 知识卡

## 分类

ai_agent_system

## 来源

- Andrej Karpathy, `llm-wiki.md`, GitHub Gist: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- 读取日期：2026-06-15

## 核心观点

LLM Wiki 的重点不是把资料临时检索出来回答问题，而是让 LLM 持续维护一个 Markdown Wiki 层。这个 Wiki 位于原始资料和用户问题之间，会随着新资料、新问题和新综合不断积累。

## 三层结构

| Layer | 含义 | 对本项目的映射 |
|---|---|---|
| Raw sources | 原始资料，只读保留 | `note/`、`knowledge/life/*.pdf`、原始 EPUB/PDF |
| Wiki | LLM 生成和维护的 Markdown 页面 | `knowledge/*/wiki/`、概念页、主题页、问题页 |
| Schema | 约束 LLM 如何维护 Wiki 的规则 | `AGENTS.md`、`CLAUDE.md`、`knowledge/knowledge_rules.md` |

## 操作流程

| Operation | 含义 | 本项目采用方式 |
|---|---|---|
| Ingest | 新资料进入后提取、归档、更新相关页面 | 先 source report，再 synthesis，再 wiki 页面 |
| Query | 基于 Wiki 回答问题，并引用来源 | 先 `master_index.md`，再领域 `index.md` |
| Writeback | 有价值回答沉淀为页面 | 只沉淀可复用、来源明确、边界清楚的内容 |
| Lint | 周期检查知识库健康 | 检查状态漂移、孤儿页、缺来源、矛盾和索引遗漏 |

## 可吸收部分

- Markdown + Git 优先，不先上复杂数据库。
- 原始资料只读，综合知识可更新。
- `index.md` 作为内容导航，`log.md` 作为时间线。
- LLM 负责维护交叉链接、摘要、冲突提示和状态记录。
- 用户负责选择资料、提出问题、判断哪些内容值得沉淀。

## 暂不吸收部分

- 暂不引入本地搜索引擎、向量检索或 MCP 搜索服务。
- 暂不要求 Obsidian 插件作为必要依赖。
- 暂不让 Wiki 自动改写人格核心、长期记忆或关系状态。

## 对 Personal Agent 的改进方向

1. 每个成熟知识域维护 `index.md` 和 `log.md`。
2. 单本资料报告之外，新增跨资料概念页。
3. 长回答可沉淀，但必须有来源、边界和更新时间。
4. 定期 lint，修复状态漂移和索引遗漏。
5. 人格、记忆、知识继续分层，知识只提供证据和候选 proposal。

## 适用边界

该知识卡用于 Agent Harness 和第二大脑架构设计，不代表必须照搬 Karpathy 的目录结构。当前项目优先保留现有 Harness 分层，只补知识编译层。

## 相关链接

- `knowledge/knowledge_rules.md`
- `knowledge/master_index.md`
- `knowledge/ai_agent_system/index.md`
- `templates/concept_page_template.md`
- `templates/source_page_template.md`
