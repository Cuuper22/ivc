import csv
import json
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
    return "other"


def load_rows(path, scope):
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
            tokens = r["text_dedup_key"].split()
            y_idx = int(r["idx_002"]) + 1
            tail = tokens[y_idx + 1 :]
            rr = dict(r)
            rr["scope"] = scope
            rr["tokens"] = tokens
            rr["tail_tokens"] = tail
            rr["tail_len"] = len(tail)
            rr["tail_full"] = " ".join(tail) if tail else "<END>"
            rr["tail_next1"] = tail[0] if tail else "<END>"
            rr["tail_next2"] = " ".join(tail[:2]) if len(tail) >= 2 else rr["tail_full"]
            rr["tail_has_032"] = str("032" in tail).lower()
            rr["tail_has_002"] = str("002" in tail).lower()
            rr["y_class"] = y_class(rr["y_after_002"])
            rows.append(rr)
    return rows


def summarize(rows, scope):
    groups = defaultdict(list)
    for r in rows:
        groups[r["y_after_002"]].append(r)

    out = []
    for y, rs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        terminals = [r for r in rs if r["tail_len"] == 0]
        continuing = [r for r in rs if r["tail_len"] > 0]
        next1 = Counter(r["tail_next1"] for r in continuing)
        full = Counter(r["tail_full"] for r in continuing)
        frame_counts = Counter(r.get("frame_kind", "") for r in rs if r.get("frame_kind", ""))
        out.append(
            {
                "scope": scope,
                "y_after_002": y,
                "y_class": y_class(y),
                "rows": len(rs),
                "terminal_rows": len(terminals),
                "continuing_rows": len(continuing),
                "terminal_rate": f"{len(terminals)}/{len(rs)}",
                "distinct_full_tails": len(full),
                "repeated_full_tails": sum(1 for _, c in full.items() if c > 1),
                "top_next1": ";".join(f"{k}:{v}" for k, v in next1.most_common(10)),
                "top_full_tails": ";".join(f"{k}:{v}" for k, v in full.most_common(10)),
                "frame_counts": ";".join(f"{k}:{v}" for k, v in frame_counts.most_common()),
                "site_counts": ";".join(f"{k}:{v}" for k, v in Counter(r["site"] for r in rs).most_common(10)),
                "type_counts": ";".join(f"{k}:{v}" for k, v in Counter(r["type"] for r in rs).most_common(10)),
                "symbol_counts": ";".join(f"{k}:{v}" for k, v in Counter(r["symbol"] for r in rs).most_common(10)),
                "example_cisi": ";".join(r["cisi"] for r in rs[:12]),
            }
        )
    return out


def instances(rows):
    out = []
    for r in rows:
        if r["tail_len"] == 0:
            continue
        out.append(
            {
                "scope": r["scope"],
                "id": r["id"],
                "cisi": r["cisi"],
                "site": r["site"],
                "type": r["type"],
                "symbol": r["symbol"],
                "frame_kind": r.get("frame_kind", ""),
                "text": r["text"],
                "idx_002": r["idx_002"],
                "y_after_002": r["y_after_002"],
                "y_class": r["y_class"],
                "tail_len": r["tail_len"],
                "tail_next1": r["tail_next1"],
                "tail_next2": r["tail_next2"],
                "tail_full": r["tail_full"],
                "tail_has_032": r["tail_has_032"],
                "tail_has_002": r["tail_has_002"],
            }
        )
    return sorted(out, key=lambda r: (r["scope"], r["y_class"], r["y_after_002"], r["tail_next1"], r["cisi"]))


def tail_pair_matrix(rows, scope):
    groups = defaultdict(Counter)
    for r in rows:
        if r["tail_len"] == 0:
            continue
        groups[(r["y_after_002"], y_class(r["y_after_002"]))][r["tail_next1"]] += 1
    out = []
    for (y, cls), counts in sorted(groups.items(), key=lambda kv: (-sum(kv[1].values()), kv[0])):
        for nxt, count in counts.most_common():
            out.append(
                {
                    "scope": scope,
                    "y_after_002": y,
                    "y_class": cls,
                    "tail_next1": nxt,
                    "rows": count,
                }
            )
    return out


def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main():
    all_rows = load_rows(ALL_ROWS, "all_002_strict_dedup")
    after_rows = load_rows(BRANCH_ROWS, "after_032_strict_dedup")

    summary_rows = summarize(all_rows, "all_002_strict_dedup") + summarize(after_rows, "after_032_strict_dedup")
    instance_rows = instances(all_rows) + instances(after_rows)
    matrix_rows = tail_pair_matrix(all_rows, "all_002_strict_dedup") + tail_pair_matrix(after_rows, "after_032_strict_dedup")

    summary_path = REPORTS / "campaign_032_002_post_y_tail_family_summary.csv"
    instances_path = REPORTS / "campaign_032_002_post_y_tail_family_instances.csv"
    matrix_path = REPORTS / "campaign_032_002_post_y_tail_next1_matrix.csv"
    json_path = REPORTS / "campaign_032_002_post_y_tail_family_summary.json"

    write_csv(
        summary_path,
        summary_rows,
        [
            "scope",
            "y_after_002",
            "y_class",
            "rows",
            "terminal_rows",
            "continuing_rows",
            "terminal_rate",
            "distinct_full_tails",
            "repeated_full_tails",
            "top_next1",
            "top_full_tails",
            "frame_counts",
            "site_counts",
            "type_counts",
            "symbol_counts",
            "example_cisi",
        ],
    )
    write_csv(
        instances_path,
        instance_rows,
        [
            "scope",
            "id",
            "cisi",
            "site",
            "type",
            "symbol",
            "frame_kind",
            "text",
            "idx_002",
            "y_after_002",
            "y_class",
            "tail_len",
            "tail_next1",
            "tail_next2",
            "tail_full",
            "tail_has_032",
            "tail_has_002",
        ],
    )
    write_csv(matrix_path, matrix_rows, ["scope", "y_after_002", "y_class", "tail_next1", "rows"])

    key_after = [r for r in summary_rows if r["scope"] == "after_032_strict_dedup"]
    key_all = [r for r in summary_rows if r["scope"] == "all_002_strict_dedup"]
    payload = {
        "all_002_rows": len(all_rows),
        "after_032_rows": len(after_rows),
        "continuing_instances": len(instance_rows),
        "summary_path": str(summary_path.resolve()),
        "instances_path": str(instances_path.resolve()),
        "matrix_path": str(matrix_path.resolve()),
        "top_all_002": key_all[:12],
        "after_032": key_after,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
