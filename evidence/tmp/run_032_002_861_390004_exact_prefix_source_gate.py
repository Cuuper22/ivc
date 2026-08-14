"""Source gate for the exact prefix 390-004-002-861.

This script reads the local inscription table, the tail-predictor all-rows table, and
the OCR text layer of the CISI Pakistan volume (a djvu XML dump) to locate candidate
plate pages. With PIL it crops, enhances, and copies candidate panels into
tmp/032_002_861_390004_exact_prefix_source_gate. The question: can the exact prefix
390-004-002-861 be promoted from a catalog split to a source-visible sign-system
alternation — that is, can we actually see the alternation on artifact images rather
than trust the transcription? It writes batch CSVs, a summary JSON, and a docs/
markdown note. Positive witnesses are recorded as source-visible but not accepted as
token values; negative witnesses stay acquisition-gated with no grammar promotion.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
OUT = ROOT / "tmp" / "032_002_861_390004_exact_prefix_source_gate"
REPORTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

SLUG = "campaign_032_002_861_390004_exact_prefix_source_gate"
LIPI = ROOT / "tmp" / "lipi_current_inscriptions_20260526.csv"
ALL_ROWS = REPORTS / "campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv"
PAKISTAN_XML = ROOT / "tmp" / "cisi_xml" / "Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml"
H55_SOURCE_PAGE = ROOT / "tmp" / "390004_exact_prefix_probe" / "india_n217_w2000.jpg"
H55_CONTACT = ROOT / "tmp" / "390004_exact_prefix_probe" / "crops3" / "H55_correct_contact_sheet.jpg"


def signs(text: str) -> list[str]:
    return re.findall(r"\d{3}", text or "")


def has_subseq(seq: list[str], sub: list[str]) -> bool:
    n = len(sub)
    return any(seq[i : i + n] == sub for i in range(max(0, len(seq) - n + 1)))


def first_subseq_index(seq: list[str], sub: list[str]) -> int | None:
    n = len(sub)
    for i in range(max(0, len(seq) - n + 1)):
        if seq[i : i + n] == sub:
            return i
    return None


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in fields})


def make_h55_contact_sheet() -> Path:
    final = OUT / f"{SLUG}_H55_source_contact_sheet.jpg"
    if H55_CONTACT.exists():
        shutil.copyfile(H55_CONTACT, final)
        return final

    if not H55_SOURCE_PAGE.exists():
        return Path("")

    img = Image.open(H55_SOURCE_PAGE)
    boxes = {
        "H55_A_panel": (820, 1780, 1560, 2460),
        "H55_A_signband": (820, 1780, 1560, 2010),
        "H55_a_panel": (820, 2560, 1560, 3260),
        "H55_a_signband": (820, 2560, 1560, 2810),
    }
    thumbs = []
    for name, box in boxes.items():
        crop = img.crop(box)
        enh = ImageOps.grayscale(crop)
        enh = ImageOps.autocontrast(enh)
        enh = ImageEnhance.Sharpness(enh).enhance(1.8)
        enh = ImageEnhance.Contrast(enh).enhance(1.25)
        crop_path = OUT / f"{SLUG}_{name}.jpg"
        enh.save(crop_path, quality=95)
        thumb = enh.convert("RGB")
        thumb.thumbnail((470, 270))
        canvas = Image.new("RGB", (500, 330), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((8, 8), name, fill=(0, 0, 0))
        canvas.paste(thumb, ((500 - thumb.width) // 2, 45))
        thumbs.append(canvas)
    sheet = Image.new("RGB", (1000, ((len(thumbs) + 1) // 2) * 330), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % 2) * 500, (idx // 2) * 330))
    sheet.save(final, quality=95)
    return final


def pakistan_direct_hits() -> list[dict[str, str]]:
    if not PAKISTAN_XML.exists():
        return []
    text = PAKISTAN_XML.read_text(encoding="utf-8", errors="ignore")
    terms = ["M-1750", "M1750", "M 1750", "HR 3506246", "3506246", "M-I750", "M-l750", "M-17S0"]
    rows = []
    for term in terms:
        count = len(re.findall(re.escape(term), text))
        rows.append({"term": term, "hits": str(count)})
    return rows


def route_rows(lipi_rows: list[dict[str, str]], h55_sheet: Path) -> list[dict[str, object]]:
    by_cisi = {r["cisi"]: r for r in lipi_rows}
    h55 = by_cisi["H-55"]
    m1750 = by_cisi["M-1750"]
    direct = pakistan_direct_hits()
    direct_note = "; ".join(f"{r['term']}={r['hits']}" for r in direct) if direct else "pakistan_xml_missing"
    return [
        {
            "cisi": "H-55",
            "local_text": h55["text"],
            "site": h55["site"],
            "type": h55["type"],
            "symbol": h55["symbol"],
            "cult": h55["cult"],
            "source_status": "source_visible_same_line_five_glyph_band",
            "source_route": "CISI Collections in India IA leaf n217 / printed page 182 / H-55 A and H-55 a panels",
            "reader_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n217/mode/1up",
            "image_path": str(h55_sheet) if h55_sheet else "",
            "evidence": "Both source plate panels labelled H-55 show a same-line five-glyph band; impression a is the cleaner comparator for the local five-sign catalog row.",
            "limit": "Source confirms same-line five-glyph field and terminal content, but token-level numeric mapping to 125 is still catalog-mediated, not independently accepted.",
            "decision": "positive_witness_source_visible_but_not_token_value_accepted",
        },
        {
            "cisi": "M-1750",
            "local_text": m1750["text"],
            "site": m1750["site"],
            "type": m1750["type"],
            "symbol": m1750["symbol"],
            "cult": m1750["cult"],
            "source_status": "public_source_not_located",
            "source_route": "CISI Pakistan public OCR/plate run searched; direct terms absent; public visible plate sequence observed through M-1658, not M-1750",
            "reader_url": "",
            "image_path": "",
            "evidence": f"Direct public Pakistan XML hit counts: {direct_note}. Local row gives HR 3506246 and catalog text only; Bhaskar supplemental local text confirms icon class only, not inscription.",
            "limit": "Cannot source-confirm bare closure or measure terminal opportunity for M-1750 from current public/local evidence.",
            "decision": "negative_witness_acquisition_gated_no_grammar_promotion",
        },
    ]


def build_390004_rows(lipi_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for r in lipi_rows:
        seq = signs(r["text"])
        if seq[:2] != ["390", "004"]:
            continue
        idx_002 = seq.index("002") if "002" in seq else None
        branch_after_002 = seq[idx_002 + 1] if idx_002 is not None and idx_002 + 1 < len(seq) else ""
        idx_861 = first_subseq_index(seq, ["002", "861"])
        tail_after_861 = " ".join(seq[idx_861 + 2 :]) if idx_861 is not None and idx_861 + 2 < len(seq) else "<END>" if idx_861 is not None else ""
        rows.append(
            {
                "cisi": r["cisi"],
                "id": r["id"],
                "site": r["site"],
                "type": r["type"],
                "symbol": r["symbol"],
                "cult": r["cult"],
                "shape": r["shape"],
                "material": r["material"],
                "condition": r["condition"],
                "text": r["text"],
                "signs": " ".join(seq),
                "starts_390004": True,
                "has_390004_002": idx_002 == 2,
                "branch_after_002": branch_after_002,
                "has_002_861": has_subseq(seq, ["002", "861"]),
                "tail_after_002_861": tail_after_861,
                "source_priority": "exact_prefix_focus" if r["cisi"] in {"H-55", "M-1750"} else "next_batch",
            }
        )
    return rows


def build_390004_002_y_rows(lipi_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for r in lipi_rows:
        seq = signs(r["text"])
        if seq[:3] != ["390", "004", "002"]:
            continue
        branch = seq[3] if len(seq) > 3 else ""
        tail = " ".join(seq[4:]) if len(seq) > 4 else "<END>"
        rows.append(
            {
                "cisi": r["cisi"],
                "id": r["id"],
                "site": r["site"],
                "type": r["type"],
                "symbol": r["symbol"],
                "cult": r["cult"],
                "shape": r["shape"],
                "condition": r["condition"],
                "text": r["text"],
                "branch_after_390_004_002": branch,
                "tail_after_branch": tail,
                "focus_role": "target_split" if r["cisi"] in {"H-55", "M-1750"} else "near_exact_branch_control",
            }
        )
    return rows


def build_125_ecology(lipi_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for r in lipi_rows:
        seq = signs(r["text"])
        for idx, sign in enumerate(seq):
            if sign != "125":
                continue
            prev2 = " ".join(seq[max(0, idx - 2) : idx])
            next2 = " ".join(seq[idx + 1 : idx + 3])
            rows.append(
                {
                    "cisi": r["cisi"],
                    "id": r["id"],
                    "site": r["site"],
                    "type": r["type"],
                    "symbol": r["symbol"],
                    "cult": r["cult"],
                    "shape": r["shape"],
                    "text": r["text"],
                    "position_index0": idx,
                    "text_len": len(seq),
                    "prev2": prev2,
                    "next2": next2,
                    "terminal_125": idx == len(seq) - 1,
                    "immediate_after_861": idx > 0 and seq[idx - 1] == "861",
                    "immediate_after_002_861": idx >= 2 and seq[idx - 2 : idx] == ["002", "861"],
                    "in_390004_frame": seq[:2] == ["390", "004"],
                    "class": "post_002_861_125" if idx >= 2 and seq[idx - 2 : idx] == ["002", "861"] else "other_125_context",
                }
            )
    return rows


def exact_prefix_split_candidates(all_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in all_rows:
        groups[r["prefix"] or "<START>"].append(r)
    out = []
    for prefix, rows in groups.items():
        tails = Counter(r["tail"] or "<END>" for r in rows)
        if "<END>" not in tails or sum(v for k, v in tails.items() if k != "<END>") == 0:
            continue
        source_ready_non_bare = sum(
            1
            for r in rows
            if (r["tail"] or "<END>") != "<END>"
            and r.get("source_status")
            and r.get("source_status") != "source_pending_or_not_checked"
        )
        out.append(
            {
                "prefix": prefix,
                "rows": len(rows),
                "non_bare_rows": sum(v for k, v in tails.items() if k != "<END>"),
                "tail_distribution": ";".join(f"{k}:{v}" for k, v in sorted(tails.items())),
                "source_ready_non_bare": source_ready_non_bare,
                "examples": "; ".join(f"{r['cisi']} {r['tail'] or '<END>'} {r['text']}" for r in rows[:12]),
                "priority": "current_focus" if prefix == "390 004" else "background_candidate",
            }
        )
    out.sort(key=lambda r: (r["priority"] != "current_focus", -int(r["non_bare_rows"]), r["prefix"]))
    return out


def summarize(
    route: list[dict[str, object]],
    rows_390004: list[dict[str, object]],
    rows_390004_002_y: list[dict[str, object]],
    ecology_125: list[dict[str, object]],
    split_candidates: list[dict[str, object]],
) -> dict[str, object]:
    branch_counts = Counter(str(r["branch_after_390_004_002"]) for r in rows_390004_002_y)
    tail_125_classes = Counter(str(r["class"]) for r in ecology_125)
    return {
        "date": "2026-05-29",
        "question": "Can the exact prefix 390-004-002-861 be promoted from catalog split to source-visible sign-system alternation?",
        "route_decision": {
            "H-55": next(r for r in route if r["cisi"] == "H-55")["decision"],
            "M-1750": next(r for r in route if r["cisi"] == "M-1750")["decision"],
        },
        "main_result": "H-55 is source-visible as a same-line five-glyph positive witness; M-1750 is public-source-dark, so the exact-prefix split remains acquisition-gated and cannot promote grammar.",
        "counts": {
            "starts_390004_rows": len(rows_390004),
            "starts_390004_002_y_rows": len(rows_390004_002_y),
            "125_occurrences": len(ecology_125),
            "post_002_861_125_occurrences": tail_125_classes.get("post_002_861_125", 0),
            "exact_prefix_mixed_candidates": len(split_candidates),
        },
        "branch_after_390_004_002": dict(sorted(branch_counts.items())),
        "125_classes": dict(sorted(tail_125_classes.items())),
        "linguistic_state": "live acquisition target, not accepted grammar; if M-1750 is later source-visible with tail-sized terminal room, the live hypotheses are closure-plus-terminal-addendum, register-conditioned subclass, and whole-template alternation.",
        "accepted_values_translations": 0,
    }


def write_doc(summary: dict[str, object], h55_sheet: Path) -> Path:
    doc = DOCS / f"{SLUG}.md"
    routes = REPORTS / f"{SLUG}_source_routes.csv"
    rows_390004 = REPORTS / f"{SLUG}_390004_rows.csv"
    rows_390004_002_y = REPORTS / f"{SLUG}_390004_002_y_rows.csv"
    ecology_125 = REPORTS / f"{SLUG}_125_ecology.csv"
    exact_splits = REPORTS / f"{SLUG}_exact_prefix_split_candidates.csv"
    summary_path = REPORTS / f"{SLUG}_summary.json"
    text = f"""# 032-002-861 / 390-004 Exact-Prefix Source Gate

Date: 2026-05-29

## Question

Can the exact catalog split `390-004-002-861` be upgraded into source-visible sign-system evidence, or is it still only an acquisition target?

This is a decipherment campaign, not a software task. It tests whether the same visible stem can close bare or take terminal material under comparable source conditions. No values, phonetics, language identity, or translations are accepted.

## Inputs

- Exact-prefix candidate: `H-55 +390-004-002-861-125+` vs `M-1750 +390-004-002-861+`
- Source route report: `{routes}`
- `390-004` batch: `{rows_390004}`
- `390-004-002-Y` branch batch: `{rows_390004_002_y}`
- `125` ecology: `{ecology_125}`
- Mixed exact-prefix candidates: `{exact_splits}`
- Summary: `{summary_path}`
- H-55 source contact sheet: `{h55_sheet}`

## Main Result

H-55 is now source-visible. CISI India leaf `n217` / printed page 182 has both `H-55 A` and `H-55 a`; the cleaner `a` impression shows a same-line five-glyph signband. That supports the catalog claim that the row has terminal material after the `390-004-002-861` stem, but it does not independently accept the numeric identity or value of `125`.

M-1750 is not source-visible in the current public/local source layer. Direct searches for `M-1750`, `M1750`, `HR 3506246`, and OCR variants failed in the public CISI Pakistan XML. The public visible Mohenjo-daro plate sequence in that volume reaches the `M-1657/M-1658` area, while M-1750 is later and remains gated. Bhaskar local supplemental material confirms icon class only, not the inscription text.

Therefore the exact-prefix split is not promoted. The correct status is:

`H-55 positive source-visible; M-1750 negative source-dark; exact-prefix alternation acquisition-gated`.

## Why This Matters

If M-1750 later becomes source-visible and has tail-sized same-line terminal opportunity while still closing bare, then `390-004-002-861` becomes the cleanest test of a closure-capable stem with optional or conditioned terminal material.

Right now it cannot carry that weight. The terminal-space recut set a concrete bar: bare closures currently show only `28-45px` post-terminal margins, while tailed rows use `120-525px` terminal windows. Since M-1750 cannot yet be measured, it cannot defeat the layout-capacity adversary.

## Linguistic Hypotheses Held Alive

1. Closure plus terminal addendum
   - `002-861` can close, but some stems allow bounded terminal material.
   - Prediction: source-visible bare rows with tail-sized terminal opportunity still close, while matched rows take simple/fixed/long terminal units.

2. Register-conditioned subclass
   - H-55 differs from M-1750 by site, icon subtype, and cult/register: Harappa `Bull1:X/SAF` versus Mohenjo-daro `Bull1:W/SAN`.
   - Prediction: tail choice sorts by source/register after controlling exact or near-exact sign frames.

3. Whole-template alternation
   - The two rows may be separate formulas sharing a visible prefix, not optional grammar.
   - Prediction: complete left formula, source family, or object register predicts tail outcome better than the post-`861` field.

## Batch Results

- `390-004` starts rows: `{summary["counts"]["starts_390004_rows"]}`
- `390-004-002-Y` rows: `{summary["counts"]["starts_390004_002_y_rows"]}`
- Branches after `390-004-002`: `{summary["branch_after_390_004_002"]}`
- `125` occurrences in local corpus: `{summary["counts"]["125_occurrences"]}`
- Immediate `002-861-125` occurrences: `{summary["counts"]["post_002_861_125_occurrences"]}`
- Mixed exact-prefix candidates in the post-`861` universe: `{summary["counts"]["exact_prefix_mixed_candidates"]}`

## Decision

Do not promote grammar from this pair yet.

Promote only if M-1750 is acquired and all of these hold:

- Same-line source confirms `390-004-002-861`.
- It has tail-sized same-line terminal opportunity comparable to H-55 and the prior tailed windows.
- It still closes bare.
- The contrast replicates in `390-004-002-Y`, `prefix_last1=004`, or another exact/near-exact source-visible frame.
- `125` recurs as post-`861` material under matched structural conditions, rather than as a general terminal sign elsewhere.

## Next Batch

1. Acquire M-1750 or an equivalent exact-prefix bare control from a non-public/source-gated image.
2. Source-route `390-004-002-Y`: especially `M-103`, `M-984`, `M-1844`, `Sktd-1`, and `M-1823`.
3. Run `125` ecology as a sign-system question: terminal `125`, post-`861-125`, and `390-004-*125*` contexts.
4. Keep `416/698/096` and long continuations as negative controls so `125` does not become another one-sign mirage.

Accepted values, phonetics, language identity, translations, and sign meanings remain `0`.
"""
    doc.write_text(text, encoding="utf-8")
    return doc


def main() -> None:
    lipi_rows = read_csv(LIPI)
    all_rows = read_csv(ALL_ROWS)
    h55_sheet = make_h55_contact_sheet()
    routes = route_rows(lipi_rows, h55_sheet)
    rows_390004 = build_390004_rows(lipi_rows)
    rows_390004_002_y = build_390004_002_y_rows(lipi_rows)
    ecology_125 = build_125_ecology(lipi_rows)
    splits = exact_prefix_split_candidates(all_rows)
    summary = summarize(routes, rows_390004, rows_390004_002_y, ecology_125, splits)

    write_csv(
        REPORTS / f"{SLUG}_source_routes.csv",
        routes,
        ["cisi", "local_text", "site", "type", "symbol", "cult", "source_status", "source_route", "reader_url", "image_path", "evidence", "limit", "decision"],
    )
    write_csv(
        REPORTS / f"{SLUG}_390004_rows.csv",
        rows_390004,
        ["cisi", "id", "site", "type", "symbol", "cult", "shape", "material", "condition", "text", "signs", "starts_390004", "has_390004_002", "branch_after_002", "has_002_861", "tail_after_002_861", "source_priority"],
    )
    write_csv(
        REPORTS / f"{SLUG}_390004_002_y_rows.csv",
        rows_390004_002_y,
        ["cisi", "id", "site", "type", "symbol", "cult", "shape", "condition", "text", "branch_after_390_004_002", "tail_after_branch", "focus_role"],
    )
    write_csv(
        REPORTS / f"{SLUG}_125_ecology.csv",
        ecology_125,
        ["cisi", "id", "site", "type", "symbol", "cult", "shape", "text", "position_index0", "text_len", "prev2", "next2", "terminal_125", "immediate_after_861", "immediate_after_002_861", "in_390004_frame", "class"],
    )
    write_csv(
        REPORTS / f"{SLUG}_exact_prefix_split_candidates.csv",
        splits,
        ["prefix", "rows", "non_bare_rows", "tail_distribution", "source_ready_non_bare", "examples", "priority"],
    )
    with (REPORTS / f"{SLUG}_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    doc = write_doc(summary, h55_sheet)
    print(json.dumps({"doc": str(doc), "summary": summary}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
