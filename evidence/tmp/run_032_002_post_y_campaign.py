"""Track what happens after the Y sign that follows 002, in and out of the 032 lane.

The earlier context scan asked which sign Y follows 002; this one asks what
comes after Y. It reads the Lipi metadata CSV and records every 002
occurrence with its Y, the next one and two signs, whether Y is terminal, and
a continuation class (terminal, one-token continuation, continues with a
later 032 or 002, or multi-token continuation). Rows where 002 follows 032
get extra branch fields, including the frame kind and up to three signs
before the 032. Summaries are built over the strict deduped layers, grouped
by Y, by frame-and-Y, and by register (site, type, symbol). Writes the
all-002 rows CSV and branch rows CSV that later 861 scripts consume, plus Y
and register summary CSVs and a JSON summary.
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


def strict_row(row):
    text = row.get("text", "")
    toks = parse_tokens(text)
    return (
        row.get("complete") == "Y"
        and text.startswith("+")
        and text.endswith("+")
        and "[" not in text
        and "]" not in text
        and "/" not in text
        and toks
        and "000" not in toks
    )


def frame_kind(tokens, idx_032):
    prev1 = tokens[idx_032 - 1] if idx_032 >= 1 else "<START>"
    prev2 = tokens[idx_032 - 2] if idx_032 >= 2 else "<START>"
    if prev1 == "220" and prev2 == "240":
        return "target_240_220_032"
    if prev1 == "220":
        return "non240_a_220_032"
    return "outside_032"


def continuation_class(tokens, idx_y):
    remaining = tokens[idx_y + 1 :]
    if not remaining:
        return "terminal"
    if len(remaining) == 1:
        return "one_token_continuation"
    if "032" in remaining:
        return "continues_with_later_032"
    if "002" in remaining:
        return "continues_with_later_002"
    return "multi_token_continuation"


def main():
    all_002_rows = []
    branch_rows = []
    with SRC.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tokens = parse_tokens(row.get("text", ""))
            strict = strict_row(row)
            for i in range(len(tokens) - 1):
                if tokens[i] != "002":
                    continue
                y_idx = i + 1
                y = tokens[y_idx]
                prev1 = tokens[i - 1] if i >= 1 else "<START>"
                r = {
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
                    "text_dedup_key": " ".join(tokens),
                    "strict_complete_closed": str(strict).lower(),
                    "idx_002": i,
                    "prev1_before_002": prev1,
                    "prev2_before_002": tokens[i - 2] if i >= 2 else "<START>",
                    "y_after_002": y,
                    "next1_after_y": tokens[y_idx + 1] if y_idx + 1 < len(tokens) else "<END>",
                    "next2_after_y": tokens[y_idx + 2] if y_idx + 2 < len(tokens) else "<END>",
                    "post_y_len": len(tokens) - y_idx - 1,
                    "y_terminal": str(y_idx + 1 >= len(tokens)).lower(),
                    "continuation_class": continuation_class(tokens, y_idx),
                    "context_scope": "after_032" if prev1 == "032" else "other_after_002",
                }
                all_002_rows.append(r)
                if prev1 == "032":
                    idx_032 = i - 1
                    r2 = dict(r)
                    r2["frame_kind"] = frame_kind(tokens, idx_032)
                    r2["prev1_before_032"] = tokens[idx_032 - 1] if idx_032 >= 1 else "<START>"
                    r2["prev2_before_032"] = tokens[idx_032 - 2] if idx_032 >= 2 else "<START>"
                    r2["prev3_before_032"] = tokens[idx_032 - 3] if idx_032 >= 3 else "<START>"
                    branch_rows.append(r2)

    OUT.mkdir(parents=True, exist_ok=True)
    all_path = OUT / "campaign_032_002_post_y_all_002_rows.csv"
    all_fields = [
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
        "text_dedup_key",
        "strict_complete_closed",
        "idx_002",
        "prev1_before_002",
        "prev2_before_002",
        "y_after_002",
        "next1_after_y",
        "next2_after_y",
        "post_y_len",
        "y_terminal",
        "continuation_class",
        "context_scope",
    ]
    with all_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=all_fields)
        w.writeheader()
        w.writerows(all_002_rows)

    branch_path = OUT / "campaign_032_002_post_y_branch_rows.csv"
    branch_fields = all_fields + [
        "frame_kind",
        "prev1_before_032",
        "prev2_before_032",
        "prev3_before_032",
    ]
    with branch_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=branch_fields)
        w.writeheader()
        w.writerows(branch_rows)

    strict_all = [r for r in all_002_rows if r["strict_complete_closed"] == "true"]
    strict_branch = [r for r in branch_rows if r["strict_complete_closed"] == "true"]

    def dedup(rows):
        seen = set()
        out = []
        for r in rows:
            key = (r["text_dedup_key"], r["site"], r["type"], r["idx_002"])
            if key not in seen:
                seen.add(key)
                out.append(r)
        return out

    strict_all_dedup = dedup(strict_all)
    strict_branch_dedup = dedup(strict_branch)

    def branch_summary(rows, scope, group_keys):
        groups = defaultdict(list)
        for r in rows:
            key = tuple(r.get(k, "") for k in group_keys)
            groups[key].append(r)
        out = []
        for key, rs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            terminals = sum(1 for r in rs if r["y_terminal"] == "true")
            cls = Counter(r["continuation_class"] for r in rs)
            nexts = Counter(r["next1_after_y"] for r in rs)
            item = {
                "scope": scope,
                "rows": len(rs),
                "terminal_rows": terminals,
                "continuing_rows": len(rs) - terminals,
                "terminal_rate": f"{terminals}/{len(rs)}",
                "continuation_classes": ";".join(f"{k}:{v}" for k, v in cls.most_common()),
                "next1_counts": ";".join(f"{k}:{v}" for k, v in nexts.most_common()),
                "sites": ";".join(sorted({r["site"] for r in rs})),
                "types": ";".join(sorted({r["type"] for r in rs})),
                "symbols": ";".join(sorted({r["symbol"] for r in rs})),
                "example_cisi": ";".join(r["cisi"] for r in rs[:12]),
            }
            for name, val in zip(group_keys, key):
                item[name] = val
            out.append(item)
        return out

    y_summary_rows = []
    y_summary_rows += branch_summary(strict_all_dedup, "all_002_strict_dedup", ["y_after_002"])
    y_summary_rows += branch_summary(strict_branch_dedup, "after_032_strict_dedup", ["y_after_002"])
    y_summary_rows += branch_summary(strict_branch_dedup, "after_032_by_frame_strict_dedup", ["frame_kind", "y_after_002"])
    y_path = OUT / "campaign_032_002_post_y_y_summary.csv"
    y_fields = [
        "scope",
        "frame_kind",
        "y_after_002",
        "rows",
        "terminal_rows",
        "continuing_rows",
        "terminal_rate",
        "continuation_classes",
        "next1_counts",
        "sites",
        "types",
        "symbols",
        "example_cisi",
    ]
    with y_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=y_fields)
        w.writeheader()
        for r in y_summary_rows:
            w.writerow({k: r.get(k, "") for k in y_fields})

    register_rows = []
    register_rows += branch_summary(strict_branch_dedup, "after_032_site_type_symbol", ["site", "type", "symbol"])
    register_rows += branch_summary(strict_branch_dedup, "after_032_frame_site_type", ["frame_kind", "site", "type"])
    reg_path = OUT / "campaign_032_002_post_y_register_summary.csv"
    reg_fields = [
        "scope",
        "frame_kind",
        "site",
        "type",
        "symbol",
        "rows",
        "terminal_rows",
        "continuing_rows",
        "terminal_rate",
        "continuation_classes",
        "next1_counts",
        "sites",
        "types",
        "symbols",
        "example_cisi",
    ]
    with reg_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=reg_fields)
        w.writeheader()
        for r in register_rows:
            w.writerow({k: r.get(k, "") for k in reg_fields})

    summary = {
        "all_002_rows": len(all_002_rows),
        "all_002_strict_rows": len(strict_all),
        "all_002_strict_dedup_rows": len(strict_all_dedup),
        "after_032_rows": len(branch_rows),
        "after_032_strict_rows": len(strict_branch),
        "after_032_strict_dedup_rows": len(strict_branch_dedup),
        "branch_rows_path": str(branch_path.resolve()),
        "all_002_rows_path": str(all_path.resolve()),
        "y_summary_path": str(y_path.resolve()),
        "register_summary_path": str(reg_path.resolve()),
        "after_032_strict_dedup_y_counts": dict(Counter(r["y_after_002"] for r in strict_branch_dedup)),
        "after_032_strict_dedup_continuation_counts": dict(Counter(r["continuation_class"] for r in strict_branch_dedup)),
    }
    summary_path = OUT / "campaign_032_002_post_y_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
