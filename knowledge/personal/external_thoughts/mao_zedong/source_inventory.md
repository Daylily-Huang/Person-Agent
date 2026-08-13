# Mao Zedong Source Inventory

## Scope

本清单登记 `note/Mao Zedong` 中 6 个本地资料。PDF 已按本地规则尝试 MinerU 批量转换，但 30 分钟超时且 `raw_mineru/` 未产出 Markdown；后续提取使用本地页码级文本抽取兜底，并保留该状态。

## Sources

| # | 文件 | 类型 | 大小 MB | 页数/章节 | 可读文本量 | 索引文件 |
|---:|---|---|---:|---:|---:|---|
| 1 | `共产主义运动中的“左派”幼稚病 (列宁) (Z-Library).pdf` | PDF | 6.3 | 175 | 0 | `knowledge\personal\external_thoughts\mao_zedong\indexes\共产主义运动中的“左派”幼稚病 (列宁) (Z-Library)_pdf_index.json` |
| 2 | `共和国的历程 (北京大学马克思主义学会) (Z-Library).pdf` | PDF | 19.0 | 236 | 0 | `knowledge\personal\external_thoughts\mao_zedong\indexes\共和国的历程 (北京大学马克思主义学会) (Z-Library)_pdf_index.json` |
| 3 | `毛泽东与马克思主义、乌托邦主义 ([美] 莫里斯·迈斯纳，译者 中共中央文献研究室《国外研究毛泽东思想资料选辑》 编辑组) (Z-Library).pdf` | PDF | 10.7 | 261 | 0 | `knowledge\personal\external_thoughts\mao_zedong\indexes\毛泽东与马克思主义、乌托邦主义 ([美] 莫里斯·迈斯纳，译者 中共中央文献研究室《国外研究毛泽东思想资料选辑》 编辑组) (Z-Library)_pdf_index.json` |
| 4 | `毛泽东传 ((英)迪克.威尔逊中共中央文献研究室《国外研究毛泽东思想资料选辑》编辑组) (z-library.sk, 1lib.sk, z-lib.sk).epub` | EPUB | 9.7 | 9 | 282700 | `knowledge\personal\external_thoughts\mao_zedong\indexes\毛泽东传 ((英)迪克.威尔逊中共中央文献研究室《国外研究毛泽东思想资料选辑》编辑组) (z-library.sk, 1lib.sk, z-lib.sk)_epub_index.json` |
| 5 | `毛泽东诗词全编鉴赏 (毛泽东 [毛泽东]) (z-library.sk, 1lib.sk, z-lib.sk).epub` | EPUB | 12.1 | 97 | 381946 | `knowledge\personal\external_thoughts\mao_zedong\indexes\毛泽东诗词全编鉴赏 (毛泽东 [毛泽东]) (z-library.sk, 1lib.sk, z-lib.sk)_epub_index.json` |
| 6 | `毛泽东选集一至七卷 (毛泽东) (Z-Library).epub` | EPUB | 2.8 | 416 | 1879862 | `knowledge\personal\external_thoughts\mao_zedong\indexes\毛泽东选集一至七卷 (毛泽东) (Z-Library)_epub_index.json` |

## Processing Priority

- P0：`毛泽东选集一至七卷`，主资料。
- P1：`毛泽东与马克思主义、乌托邦主义`、`毛泽东传`，批判校验与背景脉络。
- P2：`毛泽东诗词全编鉴赏`、`共产主义运动中的“左派”幼稚病`，表达风格和反教条背景。
- P3：`共和国的历程`，历史背景资料，暂不全文精读。

## Knowledge Role

本资料集同时具有 knowledge 角色，不只用于人格融合。后续使用时按以下边界处理：

- 可作为思想脉络、历史背景、概念解释、表达风格、方法论对照和风险校验资料。
- 人格融合只吸收用户确认后的方法论与表达边界；未确认内容不得直接写入 `SOUL.md`。
- 回答中引用这些资料时，应区分资料原文、作者/研究者解释、历史叙述和本 Harness 的吸收判断。
- OCR 文本保留为可查来源，但具体句子仍需结合页段、报告和必要时的原 PDF 校验。

## OCR Update 2026-06-14

- `毛泽东与马克思主义、乌托邦主义` 已完成 0-260 页分段 OCR，报告见 `source_report_02_meisner_marxism_utopianism_ocr.md`。
- `共产主义运动中的“左派”幼稚病` 已完成 0-174 页分段 OCR，报告见 `source_report_05_left_wing_communism_ocr.md`。
- `共和国的历程` 已完成 0-235 页分段 OCR，报告见 `source_report_06_republic_history_ocr.md`。
