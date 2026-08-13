# master_index.md

## Purpose

知识库总索引。所有知识入口先从这里导航。

## Categories

| Category | Directory | Use When |
|---|---|---|
| Personal | `personal/` | 需要用户个人背景、偏好、长期资料 |
| Learning | `learning/` | 学习、课程、考试、概念解释 |
| Research | `research/` | 论文、文献、研究设计、数据分析 |
| Creation | `creation/` | 短视频、PPT、脚本、商业内容 |
| Tools | `tools/` | 软件、命令、工作流、自动化 |
| Psychology | `psychology/` | 情绪支持、自我反思、关系议题 |
| Life | `life/` | 生活规划、选择、现实事务 |
| AI Agent System | `ai_agent_system/` | Agent Harness、提示词、MCP、RAG、Hooks |

## Navigation Rule

知识库采用两级索引：

1. 先读本文件，确定知识域。
2. 再读对应领域的 `index.md`，定位最小相关页面。

每个成熟知识域应维护：

- `index.md`：内容导航。
- `log.md`：导入、查询沉淀、修订和 lint 时间线。
- `wiki/`：跨资料概念页、主题页、人物页、问题页和冲突页。

## Current State

已导入内容：

| 路径 | 内容 | 状态 |
|---|---|---|
| `personal/external_thoughts/mao_zedong/` | 毛泽东思想外部融合：source inventory、theme_source_map、EPUB 索引、3 本 PDF OCR、source reports、综合报告 | 方法论已按用户确认写入 SOUL 等文件；资料作为 knowledge 长期保留 |
| `personal/external_thoughts/camus/` | 加缪外部思想知识包：source inventory、theme_source_map、PDF 文本层索引、MOBI 笔记清洗文本、source reports、`camus_synthesis.md`、证据表 | 人格底色已按用户确认写入 SOUL、认知风格、情绪地图、语言指纹和质量门；资料作为清醒反抗、有限尺度、自由责任、连带和克制表达的长期 knowledge 来源 |
| `personal/external_thoughts/jung/` | 荣格资料知识包：3 个源索引、keyword_hits、theme_source_map、3 份 source report、`jung_synthesis.md`；同时也是人格融合来源 | 作为 knowledge 可长期用于概念解释、分析心理学背景、思想对照和风险校验；心理反思方法已按用户确认写入人格和质量文件 |
| `life/` | 命理/周易/生活推演资料 | 当前可见原始 PDF 11 本；`processed/` 含核心三本 source report + `life_divination_synthesis.md`（已完成）、`bazi_advanced/`（八字高级处理中）、`divination_methods/`（卜筮方法处理中）；已建立领域 index/log 和 wiki 入口 |
| `ai_agent_system/llm_wiki_karpathy.md` | Karpathy LLM Wiki 知识卡 | 用于指导本 Harness 的第二大脑改造；状态：已建初版 |
| `ai_agent_system/codex_adapter.md` | Codex 适配知识卡 | 用于理解本项目在 Codex 中的入口、skill 安装和迁移方式；状态：已建初版 |

尚未填充内容的子目录：`learning/`、`research/`、`creation/`、`tools/`、`psychology/`（目录已创建，内容待导入）

## Index Update Rule

新增知识卡或资料后，在本文件登记标题、路径、用途、来源和更新时间。
