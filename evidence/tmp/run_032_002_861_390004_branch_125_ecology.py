"""Maps the 390-004 branch family and its 125 ecology for the 032-002-861 campaign.

This script reads the local inscription table (tmp/lipi_current_inscriptions_20260526.csv)
plus the source-queue source index and the negative-control candidates, with a small set
of hand-coded source-fact overrides carried over from earlier campaign packets. It scans
for the 390-004 prefix family, records the surrounding signs and tails, and asks the
summary question: does the 390-004-002-Y branch family make 125 or post-861 behavior
translation-relevant? It writes row and distribution CSVs, a summary JSON, and a docs/
markdown note. The recorded decision promotes the branch-tail ecology as a live research
object with no values accepted.
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

SLUG = "campaign_032_002_861_390004_branch_125_ecology"
LIPI = ROOT / "tmp" / "lipi_current_inscriptions_20260526.csv"
SOURCE_INDEX = REPORTS / "effective_unicity_directionality_source_queue_source_index.csv"
NEG_CONTROLS = REPORTS / "source_box_negative_control_candidates.csv"
PREV_390004_002_Y = REPORTS / "campaign_032_002_861_390004_exact_prefix_source_gate_390004_002_y_rows.csv"
PREV_125 = REPORTS / "campaign_032_002_861_390004_exact_prefix_source_gate_125_ecology.csv"


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


def source_indexes() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    by_cisi: dict[str, dict[str, str]] = {}
    if SOURCE_INDEX.exists():
        for row in read_csv(SOURCE_INDEX):
            by_cisi[row.get("cisi", "")] = row
    neg_by_cisi: dict[str, dict[str, str]] = {}
    if NEG_CONTROLS.exists():
        for row in read_csv(NEG_CONTROLS):
            neg_by_cisi[row.get("cisi", "")] = row
    return by_cisi, neg_by_cisi


def source_status(cisi: str, row_id: str, by_cisi: dict[str, dict[str, str]], neg_by_cisi: dict[str, dict[str, str]]) -> dict[str, str]:
    # Hand-coded overrides only for source facts established in earlier campaign packets.
    if cisi == "H-55":
        return {
            "source_tier": "source_visible_positive_witness",
            "source_note": "CISI India leaf n217 / printed p.182; same-line five-glyph H-55 band visible; token identity 125 remains catalog-mediated.",
            "source_path_or_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n217/mode/1up",
        }
    if cisi == "M-984":
        return {
            "source_tier": "source_visible_existing_public_crop",
            "source_note": "CISI Pakistan leaf n130 / printed p.96; M-984 A/a/a bis/a ter crops exist from prior 390-X-002 control packet; strongest public 390-004-002-817 control.",
            "source_path_or_url": str(ROOT / "tmp" / "m315_second_slot_controls" / "new_controls" / "derived" / "M-984_impression_a_signs_close.png"),
        }
    if cisi == "M-1750":
        return {
            "source_tier": "public_source_dark",
            "source_note": "Direct public CISI Pakistan/XML route failed for M-1750/HR 3506246 variants; cannot measure bare closure or terminal opportunity.",
            "source_path_or_url": "",
        }
    if cisi == "M-103":
        return {
            "source_tier": "mayig_overlap_only_public_ocr_false_positive",
            "source_note": "Mayig has M-103A = P086 P124 P122 P378 matching local 390-004-002-820 by crosswalk, but public CISI OCR hits are suffix-contaminated M-1031/M-1030/M-1036 etc., not an exact M-103 plate route.",
            "source_path_or_url": str(ROOT / "tmp" / "mayig_feature_namespace_probe" / "repo" / "indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb" / "corpus" / "m100_m199" / "m103.json"),
        }
    if cisi == "Sktd-1":
        return {
            "source_tier": "public_plate_route_candidate_not_panel_bound",
            "source_note": "CISI India public OCR routes Surkotada 1-2 seals to India_0397/0828, but Sktd-1 is not cleanly OCR-labelled on the panel; use as route candidate only.",
            "source_path_or_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n397/mode/1up",
        }
    if cisi in {"M-1844", "M-1823", "H-2003"}:
        return {
            "source_tier": "metadata_only_or_source_dark",
            "source_note": "Current source index has no usable local image/public plate route for this branch row.",
            "source_path_or_url": "",
        }
    if cisi == "-":
        return {
            "source_tier": "non_cisi_export_or_unresolved_object",
            "source_note": "No stable CISI object id in the local row; source acquisition must start from site/id/local metadata, not an object label.",
            "source_path_or_url": "",
        }
    neg = neg_by_cisi.get(cisi)
    if neg:
        return {
            "source_tier": neg.get("source_status", "source_index_hint"),
            "source_note": "from source_box_negative_control_candidates",
            "source_path_or_url": neg.get("local_images", "") or neg.get("mayig_path", ""),
        }
    idx = by_cisi.get(cisi)
    if idx:
        note = idx.get("best_status_text") or "source index hint only"
        return {
            "source_tier": "source_index_hint_only",
            "source_note": note,
            "source_path_or_url": idx.get("best_source_url", "") or idx.get("best_local_image", ""),
        }
    return {"source_tier": "unrouted", "source_note": "no route in current local source index", "source_path_or_url": ""}


def branch_rows(by_cisi: dict[str, dict[str, str]], neg_by_cisi: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    rows = read_csv(PREV_390004_002_Y)
    out = []
    for row in rows:
        status = source_status(row["cisi"], row["id"], by_cisi, neg_by_cisi)
        exact_text_family = row["text"]
        tail = row["tail_after_branch"]
        branch = row["branch_after_390_004_002"]
        if branch == "861" and tail == "125":
            role = "tailed_861_positive_witness"
        elif branch == "861" and tail == "<END>":
            role = "bare_861_source_dark_control"
        elif branch == "817" and tail == "<END>":
            role = "817_closure_pole"
        elif tail == "<END>":
            role = "other_closure_branch"
        else:
            role = "other_branch_with_tail"
        out.append(
            {
                **row,
                "branch_tail_class": f"{branch}->{tail}",
                "exact_text_family": exact_text_family,
                "decision_role": role,
                **status,
            }
        )
    return out


def branch_matrix(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["branch_after_390_004_002"])].append(row)
    out = []
    for branch, items in sorted(grouped.items()):
        tails = Counter(str(r["tail_after_branch"]) for r in items)
        tiers = Counter(str(r["source_tier"]) for r in items)
        exact_families = Counter(str(r["text"]) for r in items)
        out.append(
            {
                "branch": branch,
                "rows": len(items),
                "tail_distribution": ";".join(f"{k}:{v}" for k, v in sorted(tails.items())),
                "source_tiers": ";".join(f"{k}:{v}" for k, v in sorted(tiers.items())),
                "exact_text_families": len(exact_families),
                "example_cisis": ";".join(str(r["cisi"]) for r in items),
                "decision": branch_decision(branch, tails, tiers, len(exact_families)),
            }
        )
    return out


def branch_decision(branch: str, tails: Counter[str], tiers: Counter[str], family_count: int) -> str:
    if branch == "861":
        return "live_exact_prefix_split_but_source_gated"
    if branch == "817" and tails == Counter({"<END>": 4}):
        return "closure_pole_candidate_with_one_source_visible_control_and_formula_family_collapse_pressure"
    if branch == "820" and tails == Counter({"<END>": 1}):
        return "closure_branch_candidate_mayig_overlap_only_not_source_visible"
    if branch == "390":
        return "branch_continuation_candidate_links_to_125_820_but_panel_bound_source_missing"
    return "singleton_branch_tail_candidate_source_needed"


def ecology_rows(by_cisi: dict[str, dict[str, str]], neg_by_cisi: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    rows = read_csv(PREV_125)
    out = []
    for row in rows:
        seq = signs(row["text"])
        idx = int(row["position_index0"])
        prev1 = seq[idx - 1] if idx > 0 else "<START>"
        next1 = seq[idx + 1] if idx + 1 < len(seq) else "<END>"
        status = source_status(row["cisi"], row["id"], by_cisi, neg_by_cisi)
        if row["immediate_after_002_861"] == "True":
            ecology_class = "singleton_post_002_861_terminal_125"
        elif prev1 == "861":
            ecology_class = "post_861_terminal_125_outside_002_861"
        elif row["prev2"] == "002 390":
            ecology_class = "post_002_390_125_continuation"
        elif next1 == "<END>":
            ecology_class = "other_terminal_125"
        else:
            ecology_class = "other_nonterminal_125"
        out.append(
            {
                **row,
                "prev1": prev1,
                "next1": next1,
                "ecology_class": ecology_class,
                **status,
            }
        )
    return out


def ecology_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    total = len(rows)
    terminal = sum(1 for r in rows if r["terminal_125"] == "True")
    after_861 = sum(1 for r in rows if r["immediate_after_861"] == "True")
    after_002_861 = sum(1 for r in rows if r["immediate_after_002_861"] == "True")
    in_390004 = sum(1 for r in rows if r["in_390004_frame"] == "True")
    prev1 = Counter(str(r["prev1"]) for r in rows)
    prev2 = Counter(str(r["prev2"]) for r in rows)
    classes = Counter(str(r["ecology_class"]) for r in rows)
    return [
        {"metric": "all_125_occurrences", "value": total, "decision_relevance": "denominator"},
        {"metric": "terminal_125", "value": terminal, "decision_relevance": "125 is often terminal but not mostly terminal"},
        {"metric": "immediate_after_861", "value": after_861, "decision_relevance": "only two 861-125 cases, one outside 002-861"},
        {"metric": "immediate_after_002_861", "value": after_002_861, "decision_relevance": "H-55 singleton, not grammar"},
        {"metric": "in_390004_frame", "value": in_390004, "decision_relevance": "H-55 and Sktd-1 only; different branch contexts"},
        {"metric": "top_prev1", "value": ";".join(f"{k}:{v}" for k, v in prev1.most_common(8)), "decision_relevance": "tests whether 125 is more tied to 390/861/other frames"},
        {"metric": "top_prev2", "value": ";".join(f"{k}:{v}" for k, v in prev2.most_common(10)), "decision_relevance": "002-390-125 emerges as a separate subbranch from 002-861-125"},
        {"metric": "ecology_classes", "value": ";".join(f"{k}:{v}" for k, v in sorted(classes.items())), "decision_relevance": "class split used for next batch"},
    ]


def prev_frame_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    wanted = {"002 861", "002 390"}
    return [
        r
        for r in rows
        if r["prev2"] in wanted or r["prev1"] in {"861", "390"} or r["in_390004_frame"] == "True"
    ]


def write_doc(summary: dict[str, object]) -> Path:
    doc = DOCS / f"{SLUG}.md"
    doc.write_text(
        f"""# 032-002-861 / 390-004 Branch and 125 Ecology

Date: 2026-05-29

## Question

Does the `390-004-002-Y` branch family make `125` or post-`861` continuation behavior look translation-relevant, or is the apparent H-55/M-1750 contrast still only source acquisition pressure?

This is a decipherment campaign. It treats signs as possible members of a branch/continuation system, not as software artifacts and not as accepted readings.

## Main Result

No grammar, value, phonetics, language identity, or translation is promoted.

The useful movement is that the research object gets larger and sharper: the live object is now the `390-004-002-Y` branch-tail paradigm plus `125` adjacency ecology, not a one-row `125` claim.

`125` is not supported as a general post-`861` suffix. It occurs `{summary['all_125']}` times locally; `{summary['terminal_125']}` are terminal, `{summary['after_861']}` are immediate after `861`, and only `{summary['after_002_861']}` is immediate after `002-861`. That singleton is H-55.

The stronger new clue is different: `125` appears after `002-390` in `{summary['post_002_390_125']}` rows, including Sktd-1 in the `390-004-002` branch family. Those rows are nonterminal continuations, so the next target is `002-390-125-X`, not isolated `125`.

## Branch State

- `817` is the closure-pole candidate: four `390-004-002-817` rows close, but they collapse to one exact text formula. `M-984` is the only strong public source-visible control in the current packet.
- `861` is the exact-prefix split: H-55 is source-visible with terminal material, while M-1750 is public-source-dark. This remains acquisition-gated.
- `820` closes in M-103, but M-103 is Mayig-overlap only here; public CISI OCR hits are suffix-contaminated false positives.
- `390` continues as `125-820` in Sktd-1. The public CISI route reaches the Surkotada 1-2 plate page but is not panel-bound to Sktd-1 in this pass.
- `031` and `705` are singleton tailed branches and remain source-needed.

## Linguistic Decision

Promote the research object, not the reading:

`390-004-002` behaves like a small branch frame whose branches have different closure/continuation profiles. `125` becomes interesting only inside branch-tail ecology, especially `002-390-125-X` and the source-gated H-55 `002-861-125` singleton. It is not a value and not a translation unit yet.

## Next Batch

1. Source-route `002-390-125-X`: `M-38`, `M-119`, `M-735`, and `Sktd-1`, with exact comparison to `002-390` rows that do not take `125`.
2. Acquire M-1750 or an equivalent exact-prefix bare `390-004-002-861+` control, then measure terminal room.
3. Upgrade branch controls: M-984 is usable now; M-103, M-1844, M-1823, Sktd-1, H-2003, Dholavira `951.1`, and Tell Umma `3884.1` need source-grade object routes before they can carry branch grammar.
4. Keep `416/698/096` and long continuations as negative controls for all tail/addendum claims.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
""",
        encoding="utf-8",
    )
    return doc


def main() -> None:
    by_cisi, neg_by_cisi = source_indexes()
    b_rows = branch_rows(by_cisi, neg_by_cisi)
    b_matrix = branch_matrix(b_rows)
    e_rows = ecology_rows(by_cisi, neg_by_cisi)
    e_summary = ecology_summary(e_rows)
    frame_rows = prev_frame_rows(e_rows)

    post_002_390_125 = [r for r in e_rows if r["prev2"] == "002 390"]
    source_tiers = Counter(str(r["source_tier"]) for r in b_rows)
    summary = {
        "date": "2026-05-29",
        "question": "Does the 390-004-002-Y branch family make 125 or post-861 behavior translation-relevant?",
        "branch_rows": len(b_rows),
        "branch_count": len({r["branch_after_390_004_002"] for r in b_rows}),
        "branch_source_tiers": dict(source_tiers),
        "all_125": len(e_rows),
        "terminal_125": sum(1 for r in e_rows if r["terminal_125"] == "True"),
        "after_861": sum(1 for r in e_rows if r["immediate_after_861"] == "True"),
        "after_002_861": sum(1 for r in e_rows if r["immediate_after_002_861"] == "True"),
        "post_002_390_125": len(post_002_390_125),
        "post_002_390_125_rows": [r["cisi"] for r in post_002_390_125],
        "decision": "promote_branch_tail_ecology_as_live_research_object_no_values",
        "accepted_values_translations": 0,
    }
    doc = write_doc(summary)

    write_csv(
        REPORTS / f"{SLUG}_branch_rows.csv",
        b_rows,
        [
            "cisi",
            "id",
            "site",
            "type",
            "symbol",
            "cult",
            "shape",
            "condition",
            "text",
            "branch_after_390_004_002",
            "tail_after_branch",
            "branch_tail_class",
            "decision_role",
            "source_tier",
            "source_note",
            "source_path_or_url",
        ],
    )
    write_csv(
        REPORTS / f"{SLUG}_branch_matrix.csv",
        b_matrix,
        ["branch", "rows", "tail_distribution", "source_tiers", "exact_text_families", "example_cisis", "decision"],
    )
    write_csv(
        REPORTS / f"{SLUG}_125_rows.csv",
        e_rows,
        [
            "cisi",
            "id",
            "site",
            "type",
            "symbol",
            "cult",
            "shape",
            "text",
            "position_index0",
            "text_len",
            "prev2",
            "prev1",
            "next1",
            "next2",
            "terminal_125",
            "immediate_after_861",
            "immediate_after_002_861",
            "in_390004_frame",
            "ecology_class",
            "source_tier",
            "source_note",
            "source_path_or_url",
        ],
    )
    write_csv(
        REPORTS / f"{SLUG}_125_summary.csv",
        e_summary,
        ["metric", "value", "decision_relevance"],
    )
    write_csv(
        REPORTS / f"{SLUG}_125_frame_focus_rows.csv",
        frame_rows,
        [
            "cisi",
            "id",
            "site",
            "type",
            "symbol",
            "cult",
            "text",
            "prev2",
            "prev1",
            "next1",
            "next2",
            "terminal_125",
            "immediate_after_861",
            "immediate_after_002_861",
            "in_390004_frame",
            "ecology_class",
            "source_tier",
        ],
    )
    (REPORTS / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"doc": str(doc), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
