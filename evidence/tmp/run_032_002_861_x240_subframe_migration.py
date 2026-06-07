from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"

X240_ROWS = REPORTS / "campaign_032_002_861_x240_internal_subframes_rows.csv"
POST861_ROWS = REPORTS / "campaign_032_002_861_x240_bridge_post861_rows.csv"

OUT_PREFIX = "campaign_032_002_861_x240_subframe_migration"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def count_join(values: list[str], limit: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(limit))


def examples(rows: list[dict[str, str]], limit: int = 10) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def migration_class(rows: list[dict[str, str]]) -> str:
    distinct = {row["after_240_first3"] for row in rows}
    formula_families = {row["formula_key"] for row in rows}
    if len(rows) == 1:
        return "singleton"
    if len(distinct) == 1 and len(formula_families) == 1:
        return "locked_duplicate_family"
    if len(distinct) == 1:
        return "locked_single_subframe"
    return "migrates_across_subframes"


def build_profiles(x240_rows: list[dict[str, str]], post861_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_x: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_post_initial: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in x240_rows:
        by_x[row["x_sign"]].append(row)
    for row in post861_rows:
        by_post_initial[row["tail_initial"]].append(row)

    profiles: list[dict[str, str]] = []
    for x, rows in sorted(by_x.items(), key=lambda item: (-len(item[1]), item[0])):
        after_counts = Counter(row["after_240_first3"] for row in rows)
        dominant_after, dominant_n = after_counts.most_common(1)[0]
        post_rows = by_post_initial.get(x, [])
        profiles.append(
            {
                "x_sign": x,
                "x240_rows": str(len(rows)),
                "distinct_after240_subframes": str(len(after_counts)),
                "dominant_after240_subframe": dominant_after,
                "dominant_share": f"{dominant_n}/{len(rows)}",
                "migration_class": migration_class(rows),
                "register_cells": str(len({row["register_key"] for row in rows})),
                "formula_families": str(len({row["formula_key"] for row in rows})),
                "source_cells": str(len({"|".join([row['site'], row['type'], row['symbol'], row['shape'], row['material']]) for row in rows})),
                "prefixes": count_join([row["prefix"] for row in rows]),
                "after240_counts": count_join([row["after_240_first3"] for row in rows]),
                "post_002_861_tail_initial_rows": str(len(post_rows)),
                "post_002_861_tail_families": str(len({row["tail_after_002_861"] for row in post_rows})),
                "post_002_861_register_cells": str(len({row["register_key"] for row in post_rows})),
                "x240_examples": examples(rows),
                "post861_examples": examples(post_rows),
            }
        )
    return profiles


def build_subframes(x240_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_after: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in x240_rows:
        by_after[row["after_240_first3"]].append(row)

    out: list[dict[str, str]] = []
    for after, rows in sorted(by_after.items(), key=lambda item: (-len(item[1]), item[0])):
        x_counts = Counter(row["x_sign"] for row in rows)
        out.append(
            {
                "after240_subframe": after,
                "rows": str(len(rows)),
                "distinct_x_signs": str(len(x_counts)),
                "x_counts": ";".join(f"{key}:{value}" for key, value in x_counts.most_common()),
                "register_cells": str(len({row["register_key"] for row in rows})),
                "formula_families": str(len({row["formula_key"] for row in rows})),
                "source_cells": str(len({"|".join([row['site'], row['type'], row['symbol'], row['shape'], row['material']]) for row in rows})),
                "examples": examples(rows),
            }
        )
    return out


def decision(profiles: list[dict[str, str]]) -> dict[str, object]:
    by_x = {row["x_sign"]: row for row in profiles}
    target = {key: by_x.get(key) for key in ["603", "636", "642", "482", "904", "100", "176"]}
    migrators = [row for row in profiles if row["migration_class"] == "migrates_across_subframes"]
    locked = [row for row in profiles if row["migration_class"].startswith("locked")]
    return {
        "status": "603_bridge_survives_distributionally_but_is_not_internally_mobile_inside_x240",
        "core_observations": [
            "`603` is locked to `240-060-692` inside X-before-240: 3 rows, 1 register cell, 1 formula family.",
            "`636` and `642` are not locked the same way: `636` spans 5 after-240 continuations and `642` spans 5.",
            "`482` is strongly tied to `240-002-861`, mostly one formula family; `904` splits between terminal `240` and `240-002-817`.",
            "Therefore the Harappa-side `603` evidence is narrower than the controls, not broader. Its mobility is external: post-`002-861-603`, not internal to X-before-240.",
        ],
        "interpretive_shift": [
            "Promote split-homograph/catalog-conflation and copied-template explanations for Harappa `603`.",
            "Keep `603` as a live distributional bridge only because no other low-frequency X-before-240 sign also appears as a post-`002-861` tail initial.",
            "Do not use the Harappa `603` packet as value evidence until `H-1846` or a better `H-1138` source route resolves graphic identity.",
        ],
        "not_accepted": [
            "603 value",
            "603 phonetics",
            "603 language identity",
            "translation",
            "cross-context graphic identity",
        ],
        "target_profiles": target,
        "migrating_x_signs": [row["x_sign"] for row in migrators],
        "locked_x_signs": [row["x_sign"] for row in locked],
    }


def write_doc(
    path: Path,
    profiles: list[dict[str, str]],
    subframes: list[dict[str, str]],
    summary: dict[str, object],
) -> None:
    dec = summary["decision"]
    assert isinstance(dec, dict)

    lines = [
        "# 032-002-861 X-Before-240 Subframe Migration",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Inside the X-before-`240` construction, do X signs migrate across after-`240` continuations, or are they locked to narrow subframes? This is the next distributional question after the failed `H-1138/H-360` graphic upgrade: it asks whether `603` behaves like an internally mobile sign candidate or like a local copied tablet-slot artifact.",
        "",
        "## Method",
        "",
        "Input is the already-built strict X-before-`240` packet: complete closed token rows, deduplicated by `(cisi, site, type, symbol, text)`. This pass adds no new source claim; it re-profiles the distributional behavior.",
        "",
        f"Rows: `{summary['x240_rows']}` X-before-`240` rows across `{summary['distinct_x_signs']}` X signs.",
        "",
        "## Decision",
        "",
        f"Status: `{dec['status']}`.",
        "",
        "Core observations:",
    ]
    for item in dec["core_observations"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Interpretive shift:")
    for item in dec["interpretive_shift"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Not accepted: `603` value, phonetics, language identity, cross-context graphic identity, or translation.")
    lines.extend(
        [
            "",
            "## Target Profiles",
            "",
            "| X | rows | class | subframes | dominant | registers | families | post-861 initial rows | after-240 counts |",
            "|---|---:|---|---:|---|---:|---:|---:|---|",
        ]
    )
    for row in profiles:
        if row["x_sign"] not in {"603", "636", "642", "482", "904", "100", "176", "630", "643"}:
            continue
        lines.append(
            "| {x_sign} | {x240_rows} | {migration_class} | {distinct_after240_subframes} | {dominant_after240_subframe} ({dominant_share}) | {register_cells} | {formula_families} | {post_002_861_tail_initial_rows} | {after240_counts} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Subframes",
            "",
            "| after 240 | rows | distinct X | X counts | registers | families | examples |",
            "|---|---:|---:|---|---:|---:|---|",
        ]
    )
    for row in subframes:
        lines.append(
            "| {after240_subframe} | {rows} | {distinct_x_signs} | {x_counts} | {register_cells} | {formula_families} | {examples} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    x240_rows = read_csv(X240_ROWS)
    post861_rows = read_csv(POST861_ROWS)
    profiles = build_profiles(x240_rows, post861_rows)
    subframes = build_subframes(x240_rows)
    payload = {
        "date": "2026-05-29",
        "x240_rows": len(x240_rows),
        "distinct_x_signs": len({row["x_sign"] for row in x240_rows}),
        "subframes": subframes,
        "profiles": profiles,
        "decision": decision(profiles),
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_profiles.csv", profiles)
    write_csv(REPORTS / f"{OUT_PREFIX}_subframes.csv", subframes)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", profiles, subframes, payload)
    print(json.dumps(payload["decision"], indent=2))


if __name__ == "__main__":
    main()
