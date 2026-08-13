from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parents[3]
SRC = BASE / "knowledge" / "life"
OUT = SRC / "processed" / "bazi_advanced"
MINERU = Path(r"D:\MinerU\run_mineru.ps1")
LOG = OUT / "bazi_advanced_processing.log"

TEXT_DOCS = [
    {
        "id": "01_ditiansui",
        "pattern": "滴天髓*.pdf",
        "role": "气势、通关、清浊、体用补充",
    },
    {
        "id": "02_qiongtong_baojian",
        "pattern": "穷通宝鉴*.pdf",
        "role": "调候、月令、寒暖燥湿补充",
    },
]

OCR_DOCS = [
    {
        "id": "03_yuanhai_ziping",
        "pattern": "渊海子平*.pdf",
        "role": "基础术语、十神、格局、传统断法补充",
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


def extract_text_doc(doc: dict) -> None:
    from pypdf import PdfReader

    source = find_one(doc["pattern"])
    doc_dir = OUT / doc["id"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    log(f"DOC START text {doc['id']} source={source.name}")

    reader = PdfReader(str(source))
    pages = len(reader.pages)
    records = []
    parts = [f"# Text Extracted - {source.name}", "", f"- Role: {doc['role']}", f"- Generated: {now()}", ""]
    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            status = "success" if text.strip() else "empty"
            error = ""
        except Exception as exc:
            text = ""
            status = "failed"
            error = str(exc)
        records.append({"page": idx, "status": status, "text_length": len(text.strip()), "error": error})
        parts.append(f"## Page {idx} - {status}")
        parts.append("")
        parts.append(text.strip() if text.strip() else "[No extractable text]")
        parts.append("")

    manifest = {
        "source": str(source),
        "doc_id": doc["id"],
        "role": doc["role"],
        "method": "pypdf_text_extraction",
        "page_count": pages,
        "generated_at": now(),
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
        "- Method: pypdf text extraction",
        f"- Total pages: {pages}",
        f"- Successful pages: {ok}",
        f"- Empty pages: {empty}",
        f"- Failed pages: {failed}",
        f"- Total extracted chars: {total_chars}",
    ]
    (doc_dir / "quality_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")
    log(f"DOC END text {doc['id']} pages={pages} chars={total_chars} empty={empty} failed={failed}")


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
    for rec in sorted(records, key=lambda r: (r["start"], r["end"])):
        parts.append(f"## Pages {rec['start']}-{rec['end']} - {rec['status']}")
        parts.append("")
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


def process_ocr_doc(doc: dict) -> None:
    source = find_one(doc["pattern"])
    pages = page_count(source)
    doc_dir = OUT / doc["id"]
    doc_dir.mkdir(parents=True, exist_ok=True)
    log(f"DOC START OCR {doc['id']} source={source.name} pages={pages}")
    records: list[dict] = []
    for start in range(0, pages, 20):
        end = min(start + 19, pages - 1)
        process_range(source, doc_dir, start, end, timeout_s=1200, records=records)
        combine_ocr_doc(doc_dir, records, source, doc["role"], pages)
    combine_ocr_doc(doc_dir, records, source, doc["role"], pages)
    log(f"DOC END OCR {doc['id']} segments={len(records)}")


def write_inventory() -> None:
    rows = []
    for doc in TEXT_DOCS + OCR_DOCS:
        source = find_one(doc["pattern"])
        rows.append(
            {
                "id": doc["id"],
                "source": source.name,
                "role": doc["role"],
                "size_mb": round(source.stat().st_size / 1024 / 1024, 2),
                "pages": page_count(source),
            }
        )
    (OUT / "bazi_advanced_source_inventory.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Bazi Advanced Source Inventory", "", "| ID | Source | Role | Pages | Size MB |", "|---|---|---|---:|---:|"]
    for row in rows:
        lines.append(f"| `{row['id']}` | `{row['source']}` | {row['role']} | {row['pages']} | {row['size_mb']} |")
    (OUT / "bazi_advanced_source_inventory.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"[{now()}] bazi advanced processing started\n", encoding="utf-8")
    write_inventory()
    for doc in TEXT_DOCS:
        extract_text_doc(doc)
    for doc in OCR_DOCS:
        process_ocr_doc(doc)
    log("bazi advanced processing complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
