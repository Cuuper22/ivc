"""Catalog every adjacent 032-002 pair and the sign Y that follows it.

This is the base context scan for the 032-002 campaign. It reads the Lipi
metadata CSV and, for every inscription where 002 directly follows 032,
records the sign after 002 (called Y), what precedes 032, and whether Y ends
the inscription. Each occurrence gets a frame kind: target_240_220_032 (the
full 240-220-032 frame), non240_a_220_032 (just 220 before 032), or
outside_032. Three scopes are reported — all rows, strict complete-closed
rows (complete, +-delimited, undamaged, no 000), and a deduped strict layer
keyed by (text, site, type). Writes four CSVs: all rows, per-frame branch
summary, Y-by-frame counts, and prev1-by-Y counts, plus a JSON summary.
"""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()
SRC = ROOT / "data/open_prototype/lipi/metadata_filtered.csv"
OUT = ROOT / "data/open_prototype/reports"

TOKEN_RE = re.compile(r"\d{3}")


def parse_tokens(text):
    return TOKEN_RE.findall(text or "")


def closed_undamaged(row):
    text = row.get("text", "")
    if row.get("complete") != "Y":
        return False
    if not (text.startswith("+") and text.endswith("+")):
        return False
    if "[" in text or "]" in text or "/" in text:
        return False
    toks = parse_tokens(text)
    return bool(toks) and "000" not in toks


def frame_kind(tokens, idx_032):
    prev1 = tokens[idx_032 - 1] if idx_032 >= 1 else "<START>"
    prev2 = tokens[idx_032 - 2] if idx_032 >= 2 else "<START>"
    if prev1 == "220" and prev2 == "240":
        return "target_240_220_032"
    if prev1 == "220":
        return "non240_a_220_032"
    return "outside_032"


def before_frame(tokens, idx_032):
    start = max(0, idx_032 - 3)
    return "-".join(tokens[start:idx_032])


def main():
    rows = []
    with SRC.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tokens = parse_tokens(row.get("text", ""))
            for i in range(len(tokens) - 2):
                if tokens[i] == "032" and tokens[i + 1] == "002":
                    y = tokens[i + 2]
                    rows.append(
                        {
                            "id": row.get("id", ""),
                            "cisi": row.get("cisi", ""),
                            "site": row.get("site", ""),
                            "region": row.get("region", ""),
                            "type": row.get("type", ""),
                            "material": row.get("material", ""),
                            "shape": row.get("shape", ""),
                            "symbol": row.get("symbol", ""),
                            "cult": row.get("cult", ""),
                            "condition": row.get("condition", ""),
                            "complete": row.get("complete", ""),
                            "dir": row.get("dir.", ""),
                            "class": row.get("class", ""),
                            "text": row.get("text", ""),
                            "token_index_032": i,
                            "prev3_frame": before_frame(tokens, i),
                            "prev2": tokens[i - 2] if i >= 2 else "<START>",
                            "prev1": tokens[i - 1] if i >= 1 else "<START>",
                            "y_after_002": y,
                            "next_after_y": tokens[i + 3] if i + 3 < len(tokens) else "<END>",
                            "y_terminal": str(i + 3 >= len(tokens)).lower(),
                            "frame_kind": frame_kind(tokens, i),
                            "strict_complete_closed": str(closed_undamaged(row)).lower(),
                            "text_dedup_key": " ".join(tokens),
                        }
                    )

    OUT.mkdir(parents=True, exist_ok=True)
    all_path = OUT / "campaign_032_002_context_all_rows.csv"
    fields = [
        "id",
        "cisi",
        "site",
        "region",
        "type",
        "material",
        "shape",
        "symbol",
        "cult",
        "condition",
        "complete",
        "dir",
        "class",
        "text",
        "token_index_032",
        "prev3_frame",
        "prev2",
        "prev1",
        "y_after_002",
        "next_after_y",
        "y_terminal",
        "frame_kind",
        "strict_complete_closed",
        "text_dedup_key",
    ]
    with all_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    strict = [r for r in rows if r["strict_complete_closed"] == "true"]
    dedup_seen = set()
    strict_dedup = []
    for r in strict:
        key = (r["text_dedup_key"], r["site"], r["type"])
        if key not in dedup_seen:
            dedup_seen.add(key)
            strict_dedup.append(r)

    def summarize(scope_rows, scope):
        out = []
        groups = defaultdict(list)
        for r in scope_rows:
            groups[r["frame_kind"]].append(r)
        for frame, rs in sorted(groups.items()):
            y_counts = Counter(r["y_after_002"] for r in rs)
            terminal = sum(1 for r in rs if r["y_terminal"] == "true")
            sites = sorted({r["site"] for r in rs})
            types = sorted({r["type"] for r in rs})
            symbols = sorted({r["symbol"] for r in rs})
            out.append(
                {
                    "scope": scope,
                    "frame_kind": frame,
                    "rows": len(rs),
                    "unique_text_site_type": len({(r["text_dedup_key"], r["site"], r["type"]) for r in rs}),
                    "terminal_rows": terminal,
                    "continuing_rows": len(rs) - terminal,
                    "y_counts": ";".join(f"{k}:{v}" for k, v in y_counts.most_common()),
                    "sites": ";".join(sites),
                    "types": ";".join(types),
                    "symbols": ";".join(symbols),
                }
            )
        return out

    branch_summary = (
        summarize(rows, "all_adjacent_032_002")
        + summarize(strict, "strict_complete_closed")
        + summarize(strict_dedup, "strict_complete_closed_dedup_text_site_type")
    )
    branch_path = OUT / "campaign_032_002_context_branch_summary.csv"
    with branch_path.open("w", newline="", encoding="utf-8") as f:
        fields2 = [
            "scope",
            "frame_kind",
            "rows",
            "unique_text_site_type",
            "terminal_rows",
            "continuing_rows",
            "y_counts",
            "sites",
            "types",
            "symbols",
        ]
        w = csv.DictWriter(f, fieldnames=fields2)
        w.writeheader()
        w.writerows(branch_summary)

    y_rows = []
    for scope, scope_rows in [
        ("all_adjacent_032_002", rows),
        ("strict_complete_closed", strict),
        ("strict_complete_closed_dedup_text_site_type", strict_dedup),
    ]:
        groups = defaultdict(list)
        for r in scope_rows:
            groups[(r["frame_kind"], r["y_after_002"])].append(r)
        for (frame, y), rs in sorted(groups.items()):
            y_rows.append(
                {
                    "scope": scope,
                    "frame_kind": frame,
                    "y_after_002": y,
                    "rows": len(rs),
                    "terminal_rows": sum(1 for r in rs if r["y_terminal"] == "true"),
                    "continuing_rows": sum(1 for r in rs if r["y_terminal"] != "true"),
                    "sites": ";".join(sorted({r["site"] for r in rs})),
                    "types": ";".join(sorted({r["type"] for r in rs})),
                    "example_cisi": ";".join(r["cisi"] for r in rs[:12]),
                }
            )
    y_path = OUT / "campaign_032_002_context_y_by_frame.csv"
    with y_path.open("w", newline="", encoding="utf-8") as f:
        fields3 = [
            "scope",
            "frame_kind",
            "y_after_002",
            "rows",
            "terminal_rows",
            "continuing_rows",
            "sites",
            "types",
            "example_cisi",
        ]
        w = csv.DictWriter(f, fieldnames=fields3)
        w.writeheader()
        w.writerows(y_rows)

    prev_rows = []
    for scope, scope_rows in [
        ("strict_complete_closed", strict),
        ("strict_complete_closed_dedup_text_site_type", strict_dedup),
    ]:
        groups = defaultdict(list)
        for r in scope_rows:
            groups[(r["prev1"], r["y_after_002"])].append(r)
        for (prev1, y), rs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            prev_rows.append(
                {
                    "scope": scope,
                    "prev1_before_032": prev1,
                    "y_after_002": y,
                    "rows": len(rs),
                    "frame_kinds": ";".join(sorted({r["frame_kind"] for r in rs})),
                    "sites": ";".join(sorted({r["site"] for r in rs})),
                    "example_cisi": ";".join(r["cisi"] for r in rs[:12]),
                }
            )
    prev_path = OUT / "campaign_032_002_context_prev1_y.csv"
    with prev_path.open("w", newline="", encoding="utf-8") as f:
        fields4 = [
            "scope",
            "prev1_before_032",
            "y_after_002",
            "rows",
            "frame_kinds",
            "sites",
            "example_cisi",
        ]
        w = csv.DictWriter(f, fieldnames=fields4)
        w.writeheader()
        w.writerows(prev_rows)

    summary = {
        "all_adjacent_032_002_rows": len(rows),
        "strict_complete_closed_rows": len(strict),
        "strict_complete_closed_dedup_text_site_type_rows": len(strict_dedup),
        "all_path": str(all_path.resolve()),
        "branch_summary_path": str(branch_path.resolve()),
        "y_by_frame_path": str(y_path.resolve()),
        "prev1_y_path": str(prev_path.resolve()),
        "strict_frame_counts": Counter(r["frame_kind"] for r in strict),
        "strict_dedup_frame_counts": Counter(r["frame_kind"] for r in strict_dedup),
    }
    summary = json.loads(json.dumps(summary, default=dict))
    summary_path = OUT / "campaign_032_002_context_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
