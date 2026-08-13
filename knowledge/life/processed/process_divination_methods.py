from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parents[3]
SRC = BASE / "knowledge" / "life"
OUT = SRC / "processed" / "divination_methods"
MINERU = Path(r"D:\MinerU\run_mineru.ps1")
LOG = OUT / "divination_methods_processing.log"

DOCS = [
    {
        "id": "01_liuyao_classics",
        "pattern": "六爻古籍合集*.pdf",
        "role": "六爻古籍合集，提供传统断卦术语、用神、六亲、世应、动变、应期等背景",
        "method": "text_layer_garbled",
        "note": "有文本层但乱码明显，先抽取作为目录和粗索引，后续如需精读应分书 OCR。",
    },
    {
        "id": "02_najia_shifa",
        "pattern": "纳甲筮法讲座*.pdf",
        "role": "纳甲筮法现代讲座，补充装卦、纳甲、六亲、世应、动爻和断法流程",
        "method": "ocr",
        "note": "扫描版，无可用文本层，使用 MinerU 分段 OCR。",
    },
    {
        "id": "03_meihua_yishu",
        "pattern": "梅花易数预测学*.pdf",
        "role": "梅花易数预测资料，补充象数起卦、体用、互变、外应和具体问题推演",
        "method": "ocr",
        "note": "扫描版，无可用文本层，使用 MinerU 分段 OCR。",
    },
]


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    line = f"[{now()}] {message}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(message, flush=True)


def find_one(pattern: str) -> Path:
    matches = sorted(SRC.glob(pattern))
    if len(matches) != 1:
        raise FileNotFoundError(f"expected one match for {pattern}, got {len(matches)}")
    return matches[0]


def page_count(pdf: Path) -> int:
    from pypdf import PdfReader

    return len(PdfReader(str(pdf)).pages)


def selected_docs(ids: list[str]) -> list[dict]:
    if not ids or ids == ["all"]:
        return DOCS
    wanted = set(ids)
    docs = [doc for doc in DOCS if doc["id"] in wanted]
    missing = wanted - {doc["id"] for doc in docs}
    if missing:
        raise ValueError(f"unknown doc ids: {sorted(missing)}")
    return docs


def write_inventory() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for doc in DOCS:
        source = find_one(doc["pattern"])
        rows.append(
            {
                "id": doc["id"],
                "source": source.name,
                "role": doc["role"],
                "method": doc["method"],
                "note": doc["note"],
                "size_mb": round(source.stat().st_size / 1024 / 1024, 2),
                "pages": page_count(source),
            }
        )
    (OUT / "divination_methods_source_inventory.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Divination Methods Source Inventory",
        "",
        "| ID | Source | Role | Method | Pages | Size MB |",
        "|---|---|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['id']}` | `{row['source']}` | {row['role']} | {row['method']} | {row['pages']} | {row['size_mb']} |"
        )
    (OUT / "divination_methods_source_inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_text_layer(doc: dict) -> None:
    from pypdf import PdfReader

    source = find_one(doc["pattern"])
    doc_dir = OUT / doc["id"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    log(f"DOC START text-layer {doc['id']} source={source.name}")

    reader = PdfReader(str(source))
    records = []
    parts = [
        f"# Text Layer Extracted - {source.name}",
        "",
        f"- Role: {doc['role']}",
        f"- Quality: {doc['note']}",
        f"- Generated: {now()}",
        "",
    ]
    garble_chars = set("㭊㚠㔝卍绉俵卟刐罠兎陒俭孴匨圻妇禈敤衕敆")
    garble_hits = 0
    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            status = "success" if text.strip() else "empty"
            error = ""
        except Exception as exc:
            text = ""
            status = "failed"
            error = str(exc)
        garble_hits += sum(text.count(ch) for ch in garble_chars)
        records.append({"page": idx, "status": status, "text_length": len(text.strip()), "error": error})
        parts.extend([f"## Page {idx} - {status}", "", text.strip() if text.strip() else "[No extractable text]", ""])

    manifest = {
        "source": str(source),
        "doc_id": doc["id"],
        "role": doc["role"],
        "method": "pypdf_text_layer_with_garble_warning",
        "page_count": len(reader.pages),
        "generated_at": now(),
        "garble_marker_hits": garble_hits,
        "pages": records,
    }
    (doc_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (doc_dir / "combined.md").write_text("\n".join(parts).strip() + "\n", encoding="utf-8")

    ok = sum(1 for r in records if r["status"] == "success")
    empty = sum(1 for r in records if r["status"] == "empty")
    failed = sum(1 for r in records if r["status"] == "failed")
    total_chars = sum(r["text_length"] for r in records)
    notes = [
        f"# Quality Notes - {source.name}",
        "",
        "- Method: pypdf text layer extraction",
        "- Quality warning: 文本层存在系统性乱码，可用于目录/粗索引，不适合直接精读。",
        f"- Total pages: {len(reader.pages)}",
        f"- Successful pages: {ok}",
        f"- Empty pages: {empty}",
        f"- Failed pages: {failed}",
        f"- Total extracted chars: {total_chars}",
        f"- Garble marker hits: {garble_hits}",
        "",
        "## Suggested Follow-up",
        "",
        "- 如需精读六爻古籍，应按分书范围 OCR：增删卜易、卜筮正宗、卜筮大全、易林补遗、易冒、易隐、火珠林。",
    ]
    (doc_dir / "quality_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")
    log(f"DOC END text-layer {doc['id']} pages={len(reader.pages)} chars={total_chars} garble_hits={garble_hits}")


def find_md_files(path: Path) -> list[Path]:
    return sorted(p for p in path.rglob("*.md") if p.is_file())


def best_md(path: Path) -> Path | None:
    files = find_md_files(path)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_size)


def segment_name(start: int, end: int) -> str:
    return f"seg_{start:03d}_{end:03d}"


def run_mineru(pdf: Path, seg_dir: Path, start: int, end: int, timeout_s: int) -> dict:
    seg_dir.mkdir(parents=True, exist_ok=True)
    cmd = (
        f"& '{MINERU}' "
        f"-InputPath '{pdf}' "
        f"-OutputPath '{seg_dir}' "
        f"-Backend pipeline -Method ocr -Lang ch "
        f"-Start {start} -End {end} "
        f"-Formula:$false -Table:$false"
    )
    started = time.time()
    proc = subprocess.Popen(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "RemoteSigned", "-Command", cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    timed_out = False
    output = ""
    try:
        output, _ = proc.communicate(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        output, _ = proc.communicate()
    elapsed = round(time.time() - started, 1)
    md = best_md(seg_dir)
    md_size = md.stat().st_size if md else 0
    out_log = seg_dir / "mineru_stdout.log"
    out_log.write_text(output or "", encoding="utf-8")
    return {
        "start": start,
        "end": end,
        "status": "timeout" if timed_out else ("success" if proc.returncode == 0 and md_size > 100 else "failed"),
        "returncode": proc.returncode,
        "elapsed_seconds": elapsed,
        "md_file": str(md) if md else "",
        "md_size": md_size,
        "stdout_log": str(out_log),
    }


def process_range(pdf: Path, doc_dir: Path, start: int, end: int, timeout_s: int, records: list[dict]) -> None:
    seg_dir = doc_dir / segment_name(start, end)
    existing = best_md(seg_dir)
    if existing and existing.stat().st_size > 100:
        records.append(
            {
                "start": start,
                "end": end,
                "status": "success_existing",
                "returncode": 0,
                "elapsed_seconds": 0,
                "md_file": str(existing),
                "md_size": existing.stat().st_size,
                "stdout_log": str(seg_dir / "mineru_stdout.log"),
            }
        )
        log(f"SKIP existing {doc_dir.name} pages {start}-{end}")
        return

    log(f"START OCR {doc_dir.name} pages {start}-{end}")
    rec = run_mineru(pdf, seg_dir, start, end, timeout_s)
    log(f"END OCR {doc_dir.name} pages {start}-{end} status={rec['status']} seconds={rec['elapsed_seconds']} md_size={rec['md_size']}")
    if rec["status"] == "success":
        records.append(rec)
        return

    span = end - start + 1
    if span <= 5:
        rec["status"] = "blocked"
        records.append(rec)
        log(f"BLOCKED {doc_dir.name} pages {start}-{end}")
        return

    mid = start + (span // 2) - 1
    process_range(pdf, doc_dir, start, mid, timeout_s, records)
    process_range(pdf, doc_dir, mid + 1, end, timeout_s, records)


def combine_ocr_doc(doc_dir: Path, records: list[dict], source: Path, role: str, pages: int) -> None:
    records = sorted(records, key=lambda r: (r["start"], r["end"]))
    manifest = {
        "source": str(source),
        "doc_id": doc_dir.name,
        "role": role,
        "method": "mineru_segmented_ocr",
        "page_count": pages,
        "generated_at": now(),
        "segments": records,
    }
    (doc_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    parts = [f"# OCR Combined - {source.name}", "", f"- Role: {role}", f"- Generated: {now()}", ""]
    for rec in records:
        parts.extend([f"## Pages {rec['start']}-{rec['end']} - {rec['status']}", ""])
        md_file = rec.get("md_file")
        if str(rec.get("status", "")).startswith("success") and md_file and Path(md_file).exists():
            parts.append(Path(md_file).read_text(encoding="utf-8", errors="ignore").strip())
        else:
            parts.append(f"[OCR segment unavailable: {rec.get('status')}]")
        parts.append("")
    (doc_dir / "combined.md").write_text("\n".join(parts).strip() + "\n", encoding="utf-8")

    blocked = [r for r in records if r.get("status") == "blocked"]
    ok = sum(1 for r in records if str(r.get("status", "")).startswith("success"))
    notes = [
        f"# Quality Notes - {source.name}",
        "",
        "- Method: segmented OCR",
        f"- Total pages: {pages}",
        f"- Total segments: {len(records)}",
        f"- Successful segments: {ok}",
        f"- Blocked segments: {len(blocked)}",
        "",
        "## Blocked Segments",
        "",
    ]
    if blocked:
        for rec in blocked:
            notes.append(f"- Pages {rec['start']}-{rec['end']}: returncode={rec.get('returncode')} elapsed={rec.get('elapsed_seconds')}")
    else:
        notes.append("- None")
    (doc_dir / "quality_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")


def process_ocr_doc(doc: dict, segment_pages: int, timeout_s: int, max_segments: int | None) -> None:
    source = find_one(doc["pattern"])
    pages = page_count(source)
    doc_dir = OUT / doc["id"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    log(f"DOC START OCR {doc['id']} source={source.name} pages={pages}")
    records: list[dict] = []
    count = 0
    for start in range(0, pages, segment_pages):
        end = min(start + segment_pages - 1, pages - 1)
        process_range(source, doc_dir, start, end, timeout_s=timeout_s, records=records)
        combine_ocr_doc(doc_dir, records, source, doc["role"], pages)
        count += 1
        if max_segments is not None and count >= max_segments:
            log(f"DOC PAUSE OCR {doc['id']} max_segments={max_segments}")
            return
    log(f"DOC END OCR {doc['id']} segments={len(records)}")


def process_doc(doc: dict, segment_pages: int, timeout_s: int, max_segments: int | None) -> None:
    if doc["method"] == "text_layer_garbled":
        extract_text_layer(doc)
    elif doc["method"] == "ocr":
        process_ocr_doc(doc, segment_pages, timeout_s, max_segments)
    else:
        raise ValueError(f"unsupported method {doc['method']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", nargs="*", default=["all"], help="Doc ids to process, or all")
    parser.add_argument("--segment-pages", type=int, default=20)
    parser.add_argument("--timeout-s", type=int, default=1200)
    parser.add_argument("--max-segments", type=int, default=None)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text(f"[{now()}] divination methods processing started\n", encoding="utf-8")
    write_inventory()
    for doc in selected_docs(args.docs):
        process_doc(doc, args.segment_pages, args.timeout_s, args.max_segments)
    log("divination methods processing pass complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
