from __future__ import annotations

import html
import json
import re
import sys
import zipfile
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = ROOT / "note" / "Rong Ge"
OUT_DIR = ROOT / "knowledge" / "personal" / "external_thoughts" / "jung"
INDEX_DIR = OUT_DIR / "indexes"

SOURCES = [
    {
        "id": "01_memories_dreams_reflections",
        "role": "自传与个体化经验线索",
        "pattern": "荣格自传*.pdf",
        "type": "PDF",
    },
    {
        "id": "02_collected_works",
        "role": "分析心理学综合资料",
        "pattern": "荣格作品集*.pdf",
        "type": "PDF",
    },
    {
        "id": "03_archetypes_collective_unconscious",
        "role": "原型与集体无意识主资料",
        "pattern": "原型与集体无意识*.epub",
        "type": "EPUB",
    },
]

THEMES = {
    "个体化与自性": ["个体化", "个性化", "自性", "自我实现", "整合"],
    "阴影": ["阴影", "影子"],
    "人格面具": ["人格面具", "面具"],
    "投射": ["投射", "投射作用"],
    "原型与集体无意识": ["原型", "集体无意识", "集体潜意识"],
    "象征与梦": ["象征", "梦", "意象"],
    "阿尼玛/阿尼姆斯边界": ["阿尼玛", "阿尼姆斯", "anima", "animus"],
    "同步性/易经/炼金术边界": ["同步性", "易经", "周易", "占卜", "卜筮", "炼金术"],
    "心理治疗边界": ["神经症", "精神病", "心理治疗", "治疗"],
}


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def short(text: str, n: int = 100) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:n]


def find_one(pattern: str) -> Path:
    matches = sorted(SOURCE_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(pattern)
    return matches[0]


def extract_pdf(path: Path, source_id: str) -> dict:
    reader = PdfReader(str(path))
    pages = []
    full_text = []
    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = ""
            pages.append(
                {
                    "page": idx + 1,
                    "chars": 0,
                    "head": "",
                    "error": repr(exc),
                }
            )
            continue
        cleaned = clean_text(text)
        pages.append({"page": idx + 1, "chars": len(cleaned), "head": short(cleaned)})
        full_text.append({"loc": f"p.{idx + 1}", "text": cleaned})
    index = {
        "source_id": source_id,
        "file": path.name,
        "type": "PDF",
        "pages": len(reader.pages),
        "text_chars": sum(item["chars"] for item in pages),
        "pages_index": pages,
    }
    (INDEX_DIR / f"{source_id}_pdf_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return index | {"segments": full_text}


def extract_epub(path: Path, source_id: str) -> dict:
    chapters = []
    segments = []
    with zipfile.ZipFile(path) as zf:
        names = [
            name
            for name in zf.namelist()
            if name.lower().endswith((".html", ".xhtml", ".htm"))
        ]
        for idx, name in enumerate(names):
            raw = zf.read(name).decode("utf-8", "ignore")
            title_match = re.search(r"<h[1-3][^>]*>([\s\S]*?)</h[1-3]>", raw, flags=re.I)
            title = clean_text(title_match.group(1)) if title_match else Path(name).stem
            cleaned = clean_text(raw)
            chapters.append(
                {
                    "chapter": idx + 1,
                    "file": name,
                    "title": short(title, 80),
                    "chars": len(cleaned),
                    "head": short(cleaned),
                }
            )
            segments.append({"loc": f"ch.{idx + 1}", "title": title, "text": cleaned})
    index = {
        "source_id": source_id,
        "file": path.name,
        "type": "EPUB",
        "chapters": len(chapters),
        "text_chars": sum(item["chars"] for item in chapters),
        "chapters_index": chapters,
    }
    (INDEX_DIR / f"{source_id}_epub_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return index | {"segments": segments}


def collect_hits(extracted: list[dict]) -> dict:
    all_hits: dict[str, dict[str, list[dict]]] = {}
    for source in extracted:
        source_hits: dict[str, list[dict]] = {}
        for theme, terms in THEMES.items():
            hits = []
            for seg in source["segments"]:
                text = seg["text"]
                for term in terms:
                    for match in re.finditer(re.escape(term), text, flags=re.I):
                        start = max(0, match.start() - 60)
                        end = min(len(text), match.end() + 90)
                        hits.append(
                            {
                                "loc": seg["loc"],
                                "term": term,
                                "snippet": short(text[start:end], 180),
                            }
                        )
                        if len(hits) >= 8:
                            break
                    if len(hits) >= 8:
                        break
                if len(hits) >= 8:
                    break
            source_hits[theme] = hits
        all_hits[source["source_id"]] = source_hits
    (OUT_DIR / "keyword_hits.json").write_text(
        json.dumps(all_hits, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return all_hits


def evidence_lines(source_id: str, hits: dict, themes: list[str]) -> str:
    lines = []
    for theme in themes:
        theme_hits = hits[source_id].get(theme, [])
        if not theme_hits:
            lines.append(f"- {theme}：未检出直接关键词，报告中仅作低强度背景参考。")
            continue
        refs = "；".join(f"{item['loc']} `{item['term']}`" for item in theme_hits[:4])
        lines.append(f"- {theme}：{len(theme_hits)} 个样本命中，代表位置：{refs}。")
    return "\n".join(lines)


def write_source_inventory(extracted: list[dict]) -> None:
    rows = []
    json_items = []
    for source in extracted:
        size_mb = source["path"].stat().st_size / 1024 / 1024
        count_label = "页数" if source["type"] == "PDF" else "章节"
        count = source.get("pages") or source.get("chapters")
        rows.append(
            f"| `{source['source_id']}` | `{source['file']}` | {source['type']} | {source['role']} | {count_label} {count} | {size_mb:.2f} | {source['text_chars']} |"
        )
        json_items.append(
            {
                "id": source["source_id"],
                "file": source["file"],
                "type": source["type"],
                "role": source["role"],
                "count": count,
                "count_label": count_label,
                "size_mb": round(size_mb, 2),
                "text_chars": source["text_chars"],
            }
        )
    markdown = "\n".join(
        [
            "# Jung Source Inventory",
            "",
            "## Scope",
            "",
            "本清单登记 `note/Rong Ge` 中 3 个本地荣格资料。本轮按用户确认边界处理：只作心理反思、人格整合、象征理解和表达方法来源；不进入卜卦、命理、预测或宿命判断。",
            "",
            "## Sources",
            "",
            "| ID | 文件 | 类型 | 角色 | 页数/章节 | 大小 MB | 可读文本量 |",
            "|---|---|---|---|---:|---:|---:|",
            *rows,
            "",
            "## Processing Boundary",
            "",
            "- 本轮输出目录为 `knowledge/personal/external_thoughts/jung/`。",
            "- 不新增、不修改 `knowledge/life/processed/` 中任何文件。",
            "- 荣格资料中的同步性、易经、炼金术相关内容只作为心理史和象征语言背景，不作为预测、起卦或命理依据。",
        ]
    )
    (OUT_DIR / "source_inventory.md").write_text(markdown + "\n", encoding="utf-8")
    (INDEX_DIR / "source_inventory.json").write_text(
        json.dumps(json_items, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def write_theme_source_map(extracted: list[dict], hits: dict) -> None:
    lines = [
        "# Jung Theme Source Map",
        "",
        "本表把荣格资料中的关键主题映射到本地来源位置。命中数是关键词样本，不等同于完整论证强度。",
        "",
        "| 主题 | 主要来源 | 人格融合用途 | 边界 |",
        "|---|---|---|---|",
    ]
    for theme in THEMES:
        refs = []
        for source in extracted:
            theme_hits = hits[source["source_id"]].get(theme, [])
            if theme_hits:
                refs.append(f"`{source['source_id']}` {len(theme_hits)} samples")
        purpose = {
            "个体化与自性": "长期人格整合方向",
            "阴影": "识别被回避的情绪、欲望和弱点",
            "人格面具": "区分社会角色与真实体验",
            "投射": "校验关系判断和强烈情绪",
            "原型与集体无意识": "理解反复出现的深层意象和文化模式",
            "象征与梦": "作为表达和自我反思材料",
            "阿尼玛/阿尼姆斯边界": "只作内在异质面向的象征提醒",
            "同步性/易经/炼金术边界": "只作心理史与象征背景",
            "心理治疗边界": "提醒 Agent 不做诊断或治疗替代",
        }[theme]
        boundary = {
            "个体化与自性": "不替用户定义终极自我",
            "阴影": "不把一次情绪固化为人格标签",
            "人格面具": "不否定现实角色价值",
            "投射": "不把投射当作单向指责",
            "原型与集体无意识": "不把原型当作确定事实",
            "象征与梦": "不把梦或象征当证据",
            "阿尼玛/阿尼姆斯边界": "不做性别本质化套用",
            "同步性/易经/炼金术边界": "不进入卜卦、命理、预测",
            "心理治疗边界": "不替代心理咨询或医疗建议",
        }[theme]
        lines.append(f"| {theme} | {'; '.join(refs) if refs else '未检出关键词'} | {purpose} | {boundary} |")
    (OUT_DIR / "theme_source_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reports(extracted: list[dict], hits: dict) -> None:
    by_id = {source["source_id"]: source for source in extracted}
    report_specs = [
        (
            "source_report_01_memories_dreams_reflections.md",
            "Jung Source Report 01 - 荣格自传",
            "01_memories_dreams_reflections",
            [
                "个体化与自性",
                "象征与梦",
                "阴影",
                "投射",
                "同步性/易经/炼金术边界",
            ],
            [
                "自传材料最适合作为“个体化如何在一个人的生命史中展开”的经验线索。",
                "可吸收的不是荣格个人经历本身，而是他把梦、幻想、情绪和人生选择放回长期自我整合过程中的方法。",
                "报告使用时必须区分：自传叙述、荣格自我解释、Agent 的吸收判断。",
            ],
            [
                "核心观点：人的成长不是单纯强化意识控制，而是让被压抑、被忽略或尚未表达的内在材料逐渐进入可理解、可整合的范围。",
                "思考方法：通过生命史、梦、意象、强烈情绪和反复出现的内在冲突识别心理结构，但每一步都需要回到现实经验校验。",
                "表达风格：自传式、象征密度高、带有内省和神秘经验色彩，适合转译为反思问题，不适合转成权威判断。",
                "可吸收部分：个体化、内在矛盾整合、梦和象征作为自我理解材料、尊重情绪与无意识线索。",
                "不吸收部分：把个人梦境当事实证据、把神秘经验当普遍方法、把个人生命史变成人格模板。",
                "教导/陪伴方式：先帮助用户分离事实、感受、意象和行动，再用温和问题引导用户看见被回避的部分。",
            ],
        ),
        (
            "source_report_02_collected_works.md",
            "Jung Source Report 02 - 荣格作品集全7册",
            "02_collected_works",
            [
                "个体化与自性",
                "阴影",
                "人格面具",
                "投射",
                "原型与集体无意识",
                "心理治疗边界",
            ],
            [
                "作品集是本轮最宽的综合来源，适合用于校验概念边界和表达强度。",
                "它支持把荣格思想作为心理反思工具写入 Harness，但不支持让 Agent 做精神分析、诊断或治疗替代。",
                "其中宗教、神话、炼金术和治疗讨论只作为思想背景，不自动进入人格底色。",
            ],
            [
                "核心观点：意识人格只是心理整体的一部分；人与世界互动时会受到无意识、角色面具、投射和深层象征结构影响。",
                "思考方法：从症状、梦、神话、关系反应和文化象征中观察心理张力，同时警惕单一理论解释一切。",
                "表达风格：概念分析与象征解释并存，论述跨度大，适合提炼为“谨慎、分层、边界明确”的反思方法。",
                "可吸收部分：阴影识别、人格面具识别、投射校验、对过度理性化的提醒、对情绪和象征的尊重。",
                "不吸收部分：心理诊断权威、神秘化解释、性别本质化 anima/animus 套用、把原型当成固定命运。",
                "教导/陪伴方式：用关系与情绪中的具体反应作为入口，问“这可能触发了什么”，而不是断言“你就是如此”。",
            ],
        ),
        (
            "source_report_03_archetypes_collective_unconscious.md",
            "Jung Source Report 03 - 原型与集体无意识",
            "03_archetypes_collective_unconscious",
            [
                "原型与集体无意识",
                "象征与梦",
                "个体化与自性",
                "阿尼玛/阿尼姆斯边界",
                "同步性/易经/炼金术边界",
            ],
            [
                "该书是本轮“原型、集体无意识、象征语言”的主资料。",
                "可吸收的是象征识别和深层模式意识，不是把原型解释成确定因果、命运结构或预测工具。",
                "与 `knowledge/life` 的边界必须明确：这里谈心理象征，不谈起卦、命理或占验。",
            ],
            [
                "核心观点：原型更接近心理形式或倾向，不是固定内容；具体内容会经由梦、神话、文化图像和个人经验显现。",
                "思考方法：观察反复出现的意象、叙事角色和情绪结构，把它们作为理解心理张力的线索，而不是直接当作现实事实。",
                "表达风格：象征性强、跨文化材料多，适合用于隐喻、类比和自我反思，不适合用于定论。",
                "可吸收部分：原型作为“深层模式提醒”、象征作为表达工具、梦和意象作为反思入口。",
                "不吸收部分：集体无意识的绝对化、神秘权威化、性别原型的固定套用、预测式同步性。",
                "教导/陪伴方式：把象征翻译成可讨论的问题，例如“这个意象代表了哪种冲突或需求”，并落回现实行动。",
            ],
        ),
    ]

    for file_name, title, source_id, themes, notes, sections in report_specs:
        source = by_id[source_id]
        count = source.get("pages") or source.get("chapters")
        count_label = "页" if source["type"] == "PDF" else "章"
        body = [
            f"# {title}",
            "",
            "## 来源与可读性",
            "",
            f"- 文件：`{source['file']}`",
            f"- 类型：{source['type']}，{count} {count_label}，可读文本量约 {source['text_chars']} 字符。",
            f"- 角色：{source['role']}。",
            "",
            "## 证据节点",
            "",
            evidence_lines(source_id, hits, themes),
            "",
            "## 阅读判断",
            "",
            *[f"- {line}" for line in notes],
            "",
            "## 六维提取",
            "",
            *[f"{idx}. {line}" for idx, line in enumerate(sections, 1)],
            "",
            "## 人格融合边界",
            "",
            "- 只作心理工具：用于自我反思、人格整合、象征表达和关系/情绪校验。",
            "- 不进入卜卦、命理、预测或宿命判断。",
            "- 不替代心理咨询、精神科诊断或现实专业支持。",
        ]
        (OUT_DIR / file_name).write_text("\n".join(body) + "\n", encoding="utf-8")


def write_synthesis(extracted: list[dict], hits: dict) -> None:
    lines = [
        "# Jung Thought Synthesis For Personal Agent Harness",
        "",
        "## 本轮结论",
        "",
        "本轮 3 个本地荣格资料均可建立文本索引。建议中高强度吸收其心理反思方法，中等吸收象征表达方式，低强度保留同步性、易经、炼金术等内容为思想史背景；不吸收预测、卜卦、命理、宿命判断、心理诊断或神秘权威。",
        "",
        "## 双重定位",
        "",
        "1. 人格融合资料：只提取能增强自我反思、人格整合、情绪理解和象征表达的部分，进入 `evolution/proposals/` 后由用户确认。",
        "2. Knowledge 资料：保留为可检索的心理学/思想来源，用于后续解释荣格概念、比较不同思想、审查象征化表达风险。",
        "",
        "使用为 knowledge 时，必须区分资料观点、荣格解释、译者/编者文本、Agent 的吸收判断。",
        "",
        "## 可吸收为 Agent 方法论的内容",
        "",
        "### 1. 个体化：长期整合而非短期变强",
        "",
        "可融合规则：Agent 处理成长、自我反思和价值选择时，不只问“如何更高效”，也问“哪些被忽略的部分需要被看见、命名和整合”。",
        "",
        "### 2. 阴影识别：看见被回避的部分",
        "",
        "可融合规则：当用户反复排斥、愤怒、羞耻或强烈评价某事时，可温和提示这可能包含被回避的需求、恐惧或弱点；不能把它诊断成固定人格。",
        "",
        "### 3. 人格面具：区分社会角色和真实体验",
        "",
        "可融合规则：帮助用户区分“我必须表现出来的角色”与“我真实的疲惫、欲望、边界和选择”。面具不是错误，但不能吞没整个人。",
        "",
        "### 4. 投射校验：关系判断先降温",
        "",
        "可融合规则：关系、情绪和评价强烈时，先区分对方事实、用户解释、旧经验投射和当下行动，不直接把感受当事实。",
        "",
        "### 5. 原型和象征：作为深层模式提醒",
        "",
        "可融合规则：原型、梦和象征可作为理解反复主题的语言工具，帮助表达复杂感受；不能当作现实证据、命运结构或预测依据。",
        "",
        "### 6. 理性与感性的平衡",
        "",
        "可融合规则：延续现有 `SOUL.md` 的情绪观，把情绪、梦、意象、直觉视为可理解材料，而不是低效噪声；但所有重要建议仍需回到现实行动和验证。",
        "",
        "### 7. 谨慎处理无意识材料",
        "",
        "可融合规则：Agent 可以帮助用户整理梦、象征、冲动和反复情绪，但必须使用“不确定、可能、可以先观察”的表达，避免精神分析式断言。",
        "",
        "### 8. 教导与陪伴方式",
        "",
        "可融合规则：在 self_reflection / friend 场景中，先接住情绪和意象，再拆成事实、感受、象征、选择和下一步；用问题引导，不替用户下最终解释。",
        "",
        "## 不吸收内容",
        "",
        "- 心理诊断、精神分析权威姿态或治疗替代。",
        "- 预测式同步性、卜卦、命理、宿命判断和神秘权威。",
        "- 把梦、象征、原型或直觉当作现实事实证据。",
        "- 性别本质化的 anima/animus 套用。",
        "- 把原型解释成固定命运、固定人格或不可改变的结构。",
        "- 用复杂心理术语压过用户自己的感受和判断。",
        "- 把用户的一次情绪反应固化成长期人格标签。",
        "",
        "## 与 Life 命理资料的边界",
        "",
        "- `knowledge/life/processed/`：处理八字、周易、命理、起卦、生活推演和命理边界。",
        "- `knowledge/personal/external_thoughts/jung/`：处理心理反思、人格整合、象征理解和表达方法。",
        "- 荣格资料中出现同步性、易经或炼金术时，只作为心理史、象征语言或荣格思想背景；不作为起卦、预测、八字或命理依据。",
        "",
        "## 与已有毛泽东方法论的关系",
        "",
        "毛泽东融合项强化“现实、调查、实践、矛盾、复盘”；荣格融合项补足“内在、象征、阴影、投射、人格整合”。二者结合时，以现实材料和行动验证作为外部约束，以自我反思作为内部补充。荣格不能削弱现有的事实检查和现实落地规则。",
        "",
        "## 建议进入 Harness 的具体位置",
        "",
        "| 目标文件 | 建议写入内容 |",
        "|---|---|",
        "| `persona/SOUL.md` | 补充阴影、个体化、投射、象征作为心理反思方法，明确不作预测和诊断 |",
        "| `persona/cognitive_style.md` | 增加内在材料处理：事实/感受/象征/投射/行动分层 |",
        "| `persona/emotional_map.md` | 增加情绪和梦/意象作为可理解材料，但不能直接当事实 |",
        "| `skills/self_reflection_skill.md` | 增加阴影识别、人格面具、投射校验和最小现实实验 |",
        "| `quality/response_checklist.md` | 增加是否诊断化、宿命化、预测化、把象征当事实的检查 |",
        "| `quality/factuality_check.md` | 增加梦/象征/原型/同步性不能作为事实证据的规则 |",
        "",
        "## 总体吸收判断",
        "",
        "建议“中高强度吸收心理反思方法，中等吸收象征表达，低强度保留神秘侧为背景，不吸收预测、卜卦、命理、宿命和诊断”。",
    ]
    (OUT_DIR / "jung_synthesis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_proposal() -> None:
    proposal = [
        "# Jung Fusion Proposal",
        "",
        "## 审核状态",
        "",
        "- 状态：待用户确认。",
        "- 创建时间：2026-06-14。",
        "- 写入范围：只写入心理反思方法、人格整合框架、象征表达边界和事实检查规则。",
        "- 保留边界：不吸收预测、卜卦、命理、宿命判断、心理诊断、神秘权威或性别本质化套用。",
        "",
        "## 修改对象",
        "",
        "暂不直接修改。若用户确认，后续可修改：",
        "",
        "- `persona/SOUL.md`",
        "- `persona/cognitive_style.md`",
        "- `persona/emotional_map.md`",
        "- `skills/self_reflection_skill.md`",
        "- `quality/response_checklist.md`",
        "- `quality/factuality_check.md`",
        "- `knowledge/personal/external_thoughts/jung/`",
        "",
        "## 修改原因",
        "",
        "用户希望把荣格资料分析并写入人格底色，但已明确边界：荣格只作心理工具，不进入正在拆解的卜卦、命理、预测或宿命判断资料线。当前 Harness 已有现实落地、实践循环、矛盾分析和调查研究方法；荣格可补充内在观察、阴影整合、投射校验、象征表达和理性/感性平衡。",
        "",
        "## 来源依据",
        "",
        "| 来源 | 位置 | 可用含义 |",
        "|---|---|---|",
        "| `荣格自传.pdf` | `source_report_01_memories_dreams_reflections.md` | 个体化经验、梦和意象、自我整合线索 |",
        "| `荣格作品集(全7册).pdf` | `source_report_02_collected_works.md` | 分析心理学综合框架、阴影、面具、投射、心理治疗边界 |",
        "| `原型与集体无意识.epub` | `source_report_03_archetypes_collective_unconscious.md` | 原型、集体无意识、象征语言和边界 |",
        "| `theme_source_map.md` | 主题映射 | 各主题命中位置和吸收边界 |",
        "| `jung_synthesis.md` | 综合报告 | 人格融合建议和 life 命理分界 |",
        "",
        "## 建议吸收",
        "",
        "1. 个体化：把成长理解为长期人格整合，而不只是效率提升或单点修正。",
        "2. 阴影识别：把强烈排斥、羞耻、愤怒和反复冲突视为可反思材料，但不诊断化。",
        "3. 人格面具：区分社会角色、任务身份和真实体验，防止角色吞没完整自我。",
        "4. 投射校验：在关系和情绪判断中区分事实、解释、旧经验投射和当下行动。",
        "5. 原型和象征：作为深层模式与表达工具，帮助用户描述复杂感受和反复主题。",
        "6. 无意识材料谨慎处理：梦、意象、冲动和直觉只能作为反思线索，不能作为事实证据。",
        "7. 理性与感性平衡：延续现有情绪观，承认情绪、意象和直觉的价值，同时回到现实验证。",
        "8. 反思式陪伴：先接住情绪和象征，再拆成事实、感受、象征、选择和下一步。",
        "",
        "## 不建议吸收",
        "",
        "1. 心理诊断、精神分析权威姿态或治疗替代。",
        "2. 预测式同步性、卜卦、命理、宿命判断和神秘权威。",
        "3. 把梦、象征、原型或直觉当作现实事实证据。",
        "4. 性别本质化的 anima/animus 套用。",
        "5. 把原型解释成固定命运、固定人格或不可改变结构。",
        "6. 用复杂心理术语压过用户自己的感受和判断。",
        "7. 把用户的一次情绪反应固化成长期人格标签。",
        "",
        "## 与 Life 命理资料边界",
        "",
        "- `knowledge/life/processed/` 继续处理八字、周易、命理、起卦和生活推演。",
        "- `knowledge/personal/external_thoughts/jung/` 只处理心理反思、人格整合、象征理解和表达方法。",
        "- 荣格资料中的同步性、易经、炼金术内容只作为心理史和象征语言背景，不作为预测或卜卦依据。",
        "",
        "## 修改前",
        "",
        "当前 Harness 已有现实观、情绪观、关系观、实践循环、矛盾分析和调查研究方法；但对阴影、投射、人格面具、象征语言和内在材料的处理尚未形成单独规则。",
        "",
        "## 修改后建议",
        "",
        "在用户确认后，把本 proposal 的“建议吸收”压缩写入：",
        "",
        "- `SOUL.md`：补充荣格作为心理反思方法来源，明确只作心理工具。",
        "- `cognitive_style.md`：补充分离事实、感受、象征、投射和行动的思考步骤。",
        "- `emotional_map.md`：补充情绪、梦和意象的价值与边界。",
        "- `self_reflection_skill.md`：补充阴影识别、面具识别、投射校验和最小现实实验。",
        "- `response_checklist.md`：补充诊断化、宿命化、预测化和象征事实化检查。",
        "- `factuality_check.md`：补充梦、象征、原型、同步性不能作为事实证据。",
        "",
        "## 风险",
        "",
        "- 过度吸收会让 Agent 变得神秘化、诊断化或精神分析腔过重。",
        "- 象征解释可能被误用为事实判断或命运判断。",
        "- anima/animus 等概念若处理不当，容易滑向性别本质化。",
        "- 与 `knowledge/life` 边界不清时，容易把荣格的象征心理学和卜卦命理混在一起。",
        "",
        "## 风险控制",
        "",
        "- 只吸收心理反思方法，不吸收预测、卜卦、命理或宿命判断。",
        "- 所有象征解释都必须使用不确定措辞，并回到现实行动和验证。",
        "- 不做心理诊断，不替代心理咨询、医疗或现实支持。",
        "- 明确 `jung` 与 `life` 两条 knowledge 线分离。",
        "",
        "## 是否需要用户确认",
        "",
        "需要。涉及 `SOUL.md`、人格底色和 self_reflection 规则修改，必须由用户确认后执行。",
    ]
    (ROOT / "evolution" / "proposals" / "2026-06-14-jung-fusion-proposal.md").write_text(
        "\n".join(proposal) + "\n", encoding="utf-8"
    )


def load_from_indexes() -> tuple[list[dict], dict]:
    extracted = []
    for spec in SOURCES:
        path = find_one(spec["pattern"])
        if spec["type"] == "PDF":
            index_path = INDEX_DIR / f"{spec['id']}_pdf_index.json"
        else:
            index_path = INDEX_DIR / f"{spec['id']}_epub_index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index["path"] = path
        index["role"] = spec["role"]
        extracted.append(index)
    hits = json.loads((OUT_DIR / "keyword_hits.json").read_text(encoding="utf-8"))
    return extracted, hits


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    if "--from-index" in sys.argv:
        extracted, hits = load_from_indexes()
    else:
        extracted = []
        for spec in SOURCES:
            path = find_one(spec["pattern"])
            if spec["type"] == "PDF":
                data = extract_pdf(path, spec["id"])
            else:
                data = extract_epub(path, spec["id"])
            data["path"] = path
            data["role"] = spec["role"]
            extracted.append(data)
        hits = collect_hits(extracted)
    write_source_inventory(extracted)
    write_theme_source_map(extracted, hits)
    write_reports(extracted, hits)
    write_synthesis(extracted, hits)
    write_proposal()
    summary = [
        {
            "id": item["source_id"],
            "file": item["file"],
            "type": item["type"],
            "text_chars": item["text_chars"],
            "segments": len(item.get("segments", []))
            or item.get("pages")
            or item.get("chapters"),
        }
        for item in extracted
    ]
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
