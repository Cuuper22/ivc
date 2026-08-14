"""One-off gate for the 002-390-X branch inside the 032-002-861 campaign.

This script reads the local inscription table (tmp/lipi_current_inscriptions_20260526.csv)
plus two report indexes: the source-queue source index and the negative-control candidates.
For every occurrence of the sign bigram 002-390 it records the sign before 002, the sign
after 390, and the remaining tail, then assigns each witness object a source-route tier —
a label for how close we currently are to seeing that row on a real artifact image instead
of only in a catalog transcription. It writes a per-row CSV, a next-after-390 distribution
CSV, a summary JSON, and a markdown note under docs/. The experiment exists to ask whether
125 is a meaningful continuation after 002-390 or a catalog mirage; the script accepts no
sign value, reading, or translation.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"

SLUG = "campaign_032_002_861_002390125_branch_source_route"
LIPI = ROOT / "tmp" / "lipi_current_inscriptions_20260526.csv"
SOURCE_INDEX = REPORTS / "effective_unicity_directionality_source_queue_source_index.csv"
NEG_CONTROLS = REPORTS / "source_box_negative_control_candidates.csv"


def signs(text: str) -> list[str]:
    return re.findall(r"\d{3}", text or "")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in fields})


def indexes() -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    source = {r.get("cisi", ""): r for r in read_csv(SOURCE_INDEX)} if SOURCE_INDEX.exists() else {}
    neg: dict[str, list[dict[str, str]]] = defaultdict(list)
    if NEG_CONTROLS.exists():
        for row in read_csv(NEG_CONTROLS):
            neg[row.get("cisi", "")].append(row)
    return source, neg


def route_tier(cisi: str, source: dict[str, dict[str, str]], neg: dict[str, list[dict[str, str]]]) -> dict[str, str]:
    if cisi == "M-70":
        return {
            "source_tier": "source_visible_order_window_candidate",
            "source_note": "CISI India n66 / printed p.31 crop already stored; source-visible 002-390-692 non-125 control, not token-value evidence.",
            "source_path_or_url": str(ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "M70_impression_a_signband_from_cisi_india_n066.png"),
        }
    if cisi == "M-38":
        idx = source.get(cisi, {})
        return {
            "source_tier": "public_cisi_plate_context_crop_not_token_boxed",
            "source_note": idx.get("best_note") or "M-38 has public CISI India n55 broad source-context crop; needs human token boxing.",
            "source_path_or_url": idx.get("best_local_image") or "tmp/source_box_negative_control_v2/crops/M-38_cisi_india_n55_plate_context_crop.jpg",
        }
    if cisi == "Sktd-1":
        return {
            "source_tier": "public_plate_route_candidate_not_panel_bound",
            "source_note": "CISI India has Surkotada 1-2 source plate route at India_0397/0828, but Sktd-1 is not cleanly panel-bound in this pass.",
            "source_path_or_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n397/mode/1up",
        }
    if cisi == "-":
        return {
            "source_tier": "unresolved_non_cisi_object",
            "source_note": "No stable CISI label in local row; object/source route must begin from local id and site metadata.",
            "source_path_or_url": "",
        }
    if cisi in {"M-119"}:
        return {
            "source_tier": "mayig_overlap_only",
            "source_note": "Mayig JSON witness exists, but no public CISI/source-panel route in current local source index.",
            "source_path_or_url": str(ROOT / "tmp" / "mayig_feature_namespace_probe" / "repo" / "indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb" / "corpus" / "m100_m199" / "m119.json"),
        }
    if cisi in neg:
        best = neg[cisi][0]
        return {
            "source_tier": best.get("source_status") or "negative_control_index_hint",
            "source_note": "from source_box_negative_control_candidates",
            "source_path_or_url": best.get("local_images", "") or best.get("mayig_path", ""),
        }
    if cisi in source:
        idx = source[cisi]
        status = idx.get("best_status_text") or "source index hint only"
        tier = "source_hint_only"
        if "public_cisi_plate_page" in status or "downloaded_and_cropped" in status:
            tier = "public_route_candidate_not_token_boxed"
        return {
            "source_tier": tier,
            "source_note": status,
            "source_path_or_url": idx.get("best_local_image") or idx.get("best_source_url", ""),
        }
    return {"source_tier": "unrouted", "source_note": "not in current local source index", "source_path_or_url": ""}


def build_rows() -> list[dict[str, object]]:
    source, neg = indexes()
    rows: list[dict[str, object]] = []
    for r in read_csv(LIPI):
        seq = signs(r["text"])
        for i in range(len(seq) - 1):
            if seq[i : i + 2] != ["002", "390"]:
                continue
            next_after_390 = seq[i + 2] if i + 2 < len(seq) else "<END>"
            tail_after_next = " ".join(seq[i + 3 :]) if i + 3 < len(seq) else "<END>"
            prev_before_002 = seq[i - 1] if i > 0 else "<START>"
            route = route_tier(r["cisi"], source, neg)
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
                    "text_len": len(seq),
                    "index_002": i,
                    "prev_before_002": prev_before_002,
                    "next_after_390": next_after_390,
                    "tail_after_next": tail_after_next,
                    "is_125_branch": next_after_390 == "125",
                    "branch_family": f"002-390-{next_after_390}",
                    **route,
                }
            )
    return rows


def distribution(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_next: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_next[str(row["next_after_390"])].append(row)
    out = []
    for nxt, items in sorted(by_next.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        source_tiers = Counter(str(r["source_tier"]) for r in items)
        tails = Counter(str(r["tail_after_next"]) for r in items)
        sites = Counter(str(r["site"]) for r in items)
        out.append(
            {
                "next_after_390": nxt,
                "rows": len(items),
                "exact_text_families": len({r["text"] for r in items}),
                "source_tiers": ";".join(f"{k}:{v}" for k, v in sorted(source_tiers.items())),
                "tail_after_next_distribution": ";".join(f"{k}:{v}" for k, v in sorted(tails.items())),
                "sites": ";".join(f"{k}:{v}" for k, v in sorted(sites.items())),
                "cisis": ";".join(str(r["cisi"]) for r in items),
                "decision": next_decision(nxt, items, source_tiers),
            }
        )
    return out


def next_decision(nxt: str, items: list[dict[str, object]], source_tiers: Counter[str]) -> str:
    if nxt == "125":
        if any("source" in tier and "visible" in tier for tier in source_tiers):
            return "plurality_branch_candidate_with_some_source_visibility"
        return "plurality_branch_candidate_source_weak"
    if nxt == "692":
        return "source_visible_non125_control_for_002390"
    if len(items) > 1:
        return "repeated_non125_comparator_needs_source_route"
    return "singleton_comparator"


def write_doc(summary: dict[str, object]) -> Path:
    doc = DOCS / f"{SLUG}.md"
    doc.write_text(
        f"""# 032-002-861 / 002-390-125 Branch Source Route

Date: 2026-05-29

## Question

Does `125` look like a meaningful continuation inside the `002-390-X` branch, or did the H-55 exact-prefix gate merely move the mirage from `861` to `390`?

## Result

`002-390-X` is now the live batch object. There are `{summary['rows']}` local `002-390-X` rows with `{summary['next_value_count']}` different next signs after `390`.

`125` is the largest raw next-after-`390` group at `{summary['next_125_rows']}` rows, but it is not source-strong enough for promotion. The four rows are `M-38`, `M-119`, `M-735`, and `Sktd-1`; all are nonterminal. Two of them (`M-38`, `M-119`) continue as `125-632-032`, while `M-735` continues `125-195` and `Sktd-1` continues `125-820`.

The decisive control is `M-70 +226-032-002-390-692+`: it is source-visible and shows that `002-390` can continue without `125`. So `125` is not a necessary branch marker for `002-390`.

## Source State

- `M-38`: public CISI India `n55` context crop exists, but it is not token-boxed.
- `M-119`: Mayig overlap only; no public source-panel route in the current index.
- `M-735`: metadata/source-hint only.
- `Sktd-1`: public Surkotada 1-2 plate route exists, but Sktd-1 is not panel-bound in this pass.
- `M-70`: source-visible non-`125` control for `002-390-692`.

## Linguistic Decision

Keep `125` alive only as a plurality member of the `002-390-X` continuation system. Do not treat it as a post-`861` suffix, do not treat it as a value, and do not use it for translation.

The next evidence gate is source-normalized contrast inside `002-390-X`: `125` must survive against `692`, repeated `095`, repeated `705`, and singleton continuations under source visibility, terminal-space, and copy-family controls.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
""",
        encoding="utf-8",
    )
    return doc


def main() -> None:
    rows = build_rows()
    dist = distribution(rows)
    next_counts = Counter(str(r["next_after_390"]) for r in rows)
    summary = {
        "date": "2026-05-29",
        "question": "Source-route 002-390-125-X as branch evidence, not isolated sign evidence.",
        "rows": len(rows),
        "next_value_count": len(next_counts),
        "next_after_390_counts": dict(next_counts),
        "next_125_rows": next_counts.get("125", 0),
        "next_125_cisis": [r["cisi"] for r in rows if r["next_after_390"] == "125"],
        "source_visible_non125_control": "M-70 +226-032-002-390-692+",
        "decision": "002390x_branch_live_125_plurality_source_weak_no_values",
        "accepted_values_translations": 0,
    }
    doc = write_doc(summary)
    write_csv(
        REPORTS / f"{SLUG}_rows.csv",
        rows,
        [
            "cisi",
            "id",
            "site",
            "type",
            "symbol",
            "cult",
            "shape",
            "material",
            "condition",
            "text",
            "text_len",
            "index_002",
            "prev_before_002",
            "next_after_390",
            "tail_after_next",
            "is_125_branch",
            "branch_family",
            "source_tier",
            "source_note",
            "source_path_or_url",
        ],
    )
    write_csv(
        REPORTS / f"{SLUG}_next_distribution.csv",
        dist,
        [
            "next_after_390",
            "rows",
            "exact_text_families",
            "source_tiers",
            "tail_after_next_distribution",
            "sites",
            "cisis",
            "decision",
        ],
    )
    (REPORTS / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"doc": str(doc), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
