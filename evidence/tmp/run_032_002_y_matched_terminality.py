import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()
REPORTS = ROOT / "data/open_prototype/reports"
ALL_ROWS = REPORTS / "campaign_032_002_post_y_all_002_rows.csv"
BRANCH_ROWS = REPORTS / "campaign_032_002_post_y_branch_rows.csv"


def y_class(y):
    if y == "817":
        return "hard_closure"
    if y in {"820", "861"}:
        return "leaky_closure"
    if y in {"390", "368", "031", "220", "900", "300"}:
        return "branch_head"
    if y in {"824", "880", "003", "112", "142", "144", "221", "281", "326", "370"}:
        return "small_n_closure_like"
    return "other"


def y_binary(y):
    c = y_class(y)
    if c in {"hard_closure", "leaky_closure"}:
        return "closure_family"
    if c == "branch_head":
        return "branch_family"
    return "other"


def load_rows(path, after_only=False):
    rows = []
    seen = set()
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("strict_complete_closed") != "true":
                continue
            key = (r.get("text_dedup_key"), r.get("site"), r.get("type"), r.get("idx_002"))
            if key in seen:
                continue
            seen.add(key)
            rr = dict(r)
            tokens = rr["text_dedup_key"].split()
            rr["text_len"] = str(len(tokens))
            rr["idx_002_int"] = int(rr["idx_002"])
            rr["terminal_int"] = 1 if rr["y_terminal"] == "true" else 0
            rr["y_class"] = y_class(rr["y_after_002"])
            rr["y_binary"] = y_binary(rr["y_after_002"])
            rr["scope"] = "after_032_strict_dedup" if after_only else "all_002_strict_dedup"
            rows.append(rr)
    return rows


def summarize_classes(rows, scope):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["y_binary"], r["y_class"], r["y_after_002"])].append(r)
    out = []
    for (yb, yc, y), rs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        terminals = sum(r["terminal_int"] for r in rs)
        out.append(
            {
                "scope": scope,
                "y_binary": yb,
                "y_class": yc,
                "y_after_002": y,
                "rows": len(rs),
                "terminal_rows": terminals,
                "continuing_rows": len(rs) - terminals,
                "terminal_rate": f"{terminals}/{len(rs)}",
                "sites": ";".join(sorted({r["site"] for r in rs})),
                "types": ";".join(sorted({r["type"] for r in rs})),
                "symbols": ";".join(sorted({r["symbol"] for r in rs})),
                "example_cisi": ";".join(r["cisi"] for r in rs[:10]),
            }
        )
    return out


def block_contrasts(rows, scope, block_name, keys):
    blocks = defaultdict(list)
    for r in rows:
        if r["y_binary"] not in {"closure_family", "branch_family"}:
            continue
        blocks[tuple(r.get(k, "") for k in keys)].append(r)

    out = []
    for key, rs in sorted(blocks.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        closure = [r for r in rs if r["y_binary"] == "closure_family"]
        branch = [r for r in rs if r["y_binary"] == "branch_family"]
        if not closure or not branch:
            continue
        c_term = sum(r["terminal_int"] for r in closure)
        b_term = sum(r["terminal_int"] for r in branch)
        c_rate = c_term / len(closure)
        b_rate = b_term / len(branch)
        row = {
            "scope": scope,
            "block_name": block_name,
            "block_key": "|".join(key),
            "rows": len(rs),
            "closure_rows": len(closure),
            "closure_terminal": c_term,
            "closure_rate": f"{c_term}/{len(closure)}",
            "branch_rows": len(branch),
            "branch_terminal": b_term,
            "branch_rate": f"{b_term}/{len(branch)}",
            "closure_minus_branch": f"{c_rate - b_rate:.6f}",
            "closure_y_counts": ";".join(f"{k}:{v}" for k, v in Counter(r["y_after_002"] for r in closure).most_common()),
            "branch_y_counts": ";".join(f"{k}:{v}" for k, v in Counter(r["y_after_002"] for r in branch).most_common()),
            "example_cisi": ";".join(r["cisi"] for r in rs[:12]),
        }
        out.append(row)
    return out


def loo_scores(rows, scope, model_name, keys):
    alpha = 1.0
    global_n = len(rows)
    global_t = sum(r["terminal_int"] for r in rows)
    groups = defaultdict(lambda: [0, 0])
    for r in rows:
        key = tuple(r.get(k, "") for k in keys)
        groups[key][0] += 1
        groups[key][1] += r["terminal_int"]

    brier = 0.0
    logloss = 0.0
    acc = 0
    for r in rows:
        y = r["terminal_int"]
        key = tuple(r.get(k, "") for k in keys)
        n, t = groups[key]
        n -= 1
        t -= y
        if n <= 0:
            n = global_n - 1
            t = global_t - y
        p = (t + alpha) / (n + 2 * alpha)
        p = min(max(p, 1e-6), 1 - 1e-6)
        brier += (p - y) ** 2
        logloss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
        acc += int((p >= 0.5) == bool(y))

    return {
        "scope": scope,
        "model": model_name,
        "keys": ";".join(keys),
        "rows": len(rows),
        "terminal_rows": global_t,
        "accuracy": f"{acc / len(rows):.6f}" if rows else "",
        "brier": f"{brier / len(rows):.6f}" if rows else "",
        "logloss": f"{logloss / len(rows):.6f}" if rows else "",
    }


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def run_scope(rows, scope):
    class_rows = summarize_classes(rows, scope)

    block_specs = [
        ("site_type_symbol", ["site", "type", "symbol"]),
        ("site_type_symbol_idx002", ["site", "type", "symbol", "idx_002"]),
        ("site_type_symbol_prev1", ["site", "type", "symbol", "prev1_before_002"]),
        ("site_type_symbol_prev2_prev1", ["site", "type", "symbol", "prev2_before_002", "prev1_before_002"]),
    ]
    if rows and "frame_kind" in rows[0]:
        block_specs.append(("frame_site_type", ["frame_kind", "site", "type"]))
        block_specs.append(("frame_site_type_symbol", ["frame_kind", "site", "type", "symbol"]))

    contrast_rows = []
    for name, keys in block_specs:
        contrast_rows.extend(block_contrasts(rows, scope, name, keys))

    model_specs = [
        ("global", []),
        ("y_binary", ["y_binary"]),
        ("y_class", ["y_class"]),
        ("y_exact", ["y_after_002"]),
        ("site_type_symbol", ["site", "type", "symbol"]),
        ("site_type_symbol_plus_y_binary", ["site", "type", "symbol", "y_binary"]),
        ("site_type_symbol_plus_y_class", ["site", "type", "symbol", "y_class"]),
        ("site_type_symbol_prev1", ["site", "type", "symbol", "prev1_before_002"]),
        ("site_type_symbol_prev1_plus_y_binary", ["site", "type", "symbol", "prev1_before_002", "y_binary"]),
    ]
    if rows and "frame_kind" in rows[0]:
        model_specs.extend(
            [
                ("frame_site_type", ["frame_kind", "site", "type"]),
                ("frame_site_type_plus_y_binary", ["frame_kind", "site", "type", "y_binary"]),
                ("frame_site_type_plus_y_class", ["frame_kind", "site", "type", "y_class"]),
            ]
        )
    score_rows = [loo_scores(rows, scope, name, keys) for name, keys in model_specs]
    return class_rows, contrast_rows, score_rows


def main():
    all_rows = load_rows(ALL_ROWS, after_only=False)
    after_rows = load_rows(BRANCH_ROWS, after_only=True)

    all_class, all_contrast, all_scores = run_scope(all_rows, "all_002_strict_dedup")
    after_class, after_contrast, after_scores = run_scope(after_rows, "after_032_strict_dedup")

    class_path = REPORTS / "campaign_032_002_y_matched_terminality_class_summary.csv"
    contrast_path = REPORTS / "campaign_032_002_y_matched_terminality_block_contrasts.csv"
    score_path = REPORTS / "campaign_032_002_y_matched_terminality_prediction_scores.csv"
    summary_path = REPORTS / "campaign_032_002_y_matched_terminality_summary.json"

    write_csv(
        class_path,
        all_class + after_class,
        [
            "scope",
            "y_binary",
            "y_class",
            "y_after_002",
            "rows",
            "terminal_rows",
            "continuing_rows",
            "terminal_rate",
            "sites",
            "types",
            "symbols",
            "example_cisi",
        ],
    )
    write_csv(
        contrast_path,
        all_contrast + after_contrast,
        [
            "scope",
            "block_name",
            "block_key",
            "rows",
            "closure_rows",
            "closure_terminal",
            "closure_rate",
            "branch_rows",
            "branch_terminal",
            "branch_rate",
            "closure_minus_branch",
            "closure_y_counts",
            "branch_y_counts",
            "example_cisi",
        ],
    )
    write_csv(
        score_path,
        all_scores + after_scores,
        ["scope", "model", "keys", "rows", "terminal_rows", "accuracy", "brier", "logloss"],
    )

    def best(scores, metric):
        return min(scores, key=lambda r: float(r[metric]))

    summary = {
        "all_002_strict_dedup_rows": len(all_rows),
        "after_032_strict_dedup_rows": len(after_rows),
        "class_summary_path": str(class_path.resolve()),
        "block_contrasts_path": str(contrast_path.resolve()),
        "prediction_scores_path": str(score_path.resolve()),
        "all_002_best_brier": best(all_scores, "brier"),
        "all_002_best_logloss": best(all_scores, "logloss"),
        "after_032_best_brier": best(after_scores, "brier"),
        "after_032_best_logloss": best(after_scores, "logloss"),
        "matched_blocks_all_002": len(all_contrast),
        "matched_blocks_after_032": len(after_contrast),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
