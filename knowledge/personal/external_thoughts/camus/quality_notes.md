# Camus Processing Quality Notes

## PDF

- PDF 页数：1777。
- 文本层：可直接抽取中文文本。
- MinerU：已按本地规则尝试 `D:\MinerU\run_mineru.ps1 -Method txt` 全量转换，3 分钟超时，`raw_mineru/` 无 Markdown 产物；已停止本次残留进程。
- 本轮可靠证据来源：PDF 文本层、书签目录、页段关键词表。

## MOBI

- 状态：parsed_palmdoc_html。
- 原因：MOBI 为 PalmDOC 压缩、UTF-8 编码、未加密；已本地解压并清洗 HTML，可作为补充证据。
- 清洗文本：`camus_notebooks_cleaned.md`。
- 处理边界：MOBI 作为补充证据，不单独覆盖 PDF 主资料和用户确认流程。

## Scope Guard

- Camus 处理脚本未写入、未引用 `knowledge/life/`。
- 完成验证时若检测到 `knowledge/life/processed/bazi_advanced/` 下并行/既有产物，本轮 Camus 输出不使用这些文件。
- 完成验证时若检测到 `knowledge/personal/external_thoughts/jung/` 下已有报告文件，本轮 Camus 输出不使用这些文件。
- 未直接修改 `persona/SOUL.md` 或其他核心人格文件。
