#!/usr/bin/env python3
"""Audit a frozen public Mahadevan concordance and mine cross-face constraints.

Python 3.10+, standard library only. No learned readings, sign mergers, or
unlabelled repair of damaged text. Catalogue-level findings require image review.
"""
from __future__ import annotations
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

# Drawn long-stroke groups, not accepted phonetic or lexical values.
LONG_STROKES = {86: 1, 87: 2, 89: 3, 95: 4, 96: 5}
PUBLISHED_CENSUS = {
    "catalogued_objects": 2906, "nonempty_lines": 3573,
    "legible_sign_occurrences_including_doubtful": 13372,
    "sign_inventory_including_doubtful": 417,
    "sign_342_frequency_including_doubtful": 1395,
    "sign_99_frequency_including_doubtful": 649,
}
META = ["index", "textnum", "dockey", "sideline", "locus", "level", "inscobj",
        "fs80", "dir", "posnum", "signnum"]


def decode(v: dict[str, Any]) -> Any:
    for key in ("stringValue", "integerValue", "doubleValue", "booleanValue"):
        if key in v:
            return int(v[key]) if key == "integerValue" else v[key]
    if "arrayValue" in v:
        return [decode(x) for x in v["arrayValue"].get("values", [])]
    if "nullValue" in v:
        return None
    raise ValueError(f"Unrecognized Firestore field type: {list(v)}")


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reject_reasons(row: dict[str, Any]) -> list[str]:
    seq = row["tokens"]
    reasons: list[str] = []
    if not seq:
        reasons.append("no_text")
    if row["dir"] not in ("1", "2", "3"):
        reasons.append("direction_not_in_strict_set")
    if "0" in seq:
        reasons.append("lost_or_illegible_passage")
    if any(x.startswith("*") for x in seq):
        reasons.append("doubtful_sign")
    if any(not x.isdigit() or not 1 <= int(x) <= 417 for x in seq):
        reasons.append("not_all_undoubted_1_to_417")
    if len(seq) != int(row["posnum"]) or len(seq) != int(row["signnum"]):
        reasons.append("position_or_legible_count_mismatch")
    slots = [str(row[f"S{i}"]) for i in range(1, 15)]
    if any(not x for x in slots[:len(seq)]):
        reasons.append("nonterminal_blank_slot")
    return reasons


def row_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return {k: row[k] for k in META} | {"tokens_raw": row["tokens"],
        "tokens_display": list(reversed(row["tokens"]))}


def positive_integer_solutions() -> list[dict[str, int]]:
    """Exhaustive, not bounded search: d=2L-7 is a positive divisor of 65."""
    result = []
    for d in range(1, 66):
        if 65 % d or (d + 7) % 2:
            continue
        L = (d + 7) // 2
        numerator = L * L + 4
        if numerator % d:
            continue
        S = numerator // d
        v = 2 * S - L
        if min(L, S, v) <= 0:
            continue
        if not (v == 2 * S - L and v * L + 1 == 7 * S + 5):
            raise AssertionError("Algebraic certificate failed")
        result.append({"L": L, "S": S, "v": v})
    return result


def audit(input_path: Path, output: Path) -> dict[str, Any]:
    packed = input_path.read_bytes()
    raw = gzip.decompress(packed) if input_path.suffix == ".gz" else packed
    documents = json.loads(raw)
    if not isinstance(documents, list) or not documents:
        raise ValueError("Expected a nonempty array of public concordance documents")
    rows = []
    for doc in documents:
        row = {k: decode(v) for k, v in doc["fields"].items()}
        if str(row["dockey"]) != str(row["textnum"]):
            raise ValueError("Object identity fields disagree")
        slots = [str(row.get(f"S{i}", "")) for i in range(1, 15)]
        if slots != row.get("texts"):
            raise ValueError(f"Redundant transcription fields disagree at {row['index']}")
        row["tokens"] = [x for x in slots if x]
        row["reasons"] = reject_reasons(row)
        rows.append(row)
    rows.sort(key=lambda r: int(r["index"]))
    indices = [int(r["index"]) for r in rows]
    if indices != list(range(len(rows))):
        raise ValueError("Missing, duplicated, or nonconsecutive public record indices")
    if len({(r["textnum"], r["sideline"]) for r in rows}) != len(rows):
        raise ValueError("Duplicated object/side/line records")
    frequency = collections.Counter(int(t.lstrip("*")) for r in rows
                                    for t in r["tokens"] if t != "0")
    census = {
        "catalogued_objects": len({r["textnum"] for r in rows}),
        "nonempty_lines": sum(bool(r["tokens"]) for r in rows),
        "legible_sign_occurrences_including_doubtful": sum(frequency.values()),
        "sign_inventory_including_doubtful": len(frequency),
        "sign_342_frequency_including_doubtful": frequency[342],
        "sign_99_frequency_including_doubtful": frequency[99],
    }
    if census != PUBLISHED_CENSUS:
        raise ValueError(f"Snapshot does not match the published 1977 census: {census}")
    strict = [r for r in rows if not r["reasons"]]
    unique = {tuple(r["tokens"]) for r in strict}
    by_object: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for r in rows:
        by_object[r["textnum"]].append(r)
    pairs = []
    for tid, rr in sorted(by_object.items()):
        # Exactly two recorded surfaces, each with its only line.
        if len(rr) != 2 or {r["sideline"] for r in rr} != {"10", "20"}:
            continue
        if any(r["reasons"] or r["inscobj"] != "3" for r in rr):
            continue
        orientations = []
        for front, reverse in (rr, rr[::-1]):
            s = [int(x) for x in reverse["tokens"]]
            if len(s) == 2 and s[1] == 328 and s[0] in LONG_STROKES:
                orientations.append((front, reverse, LONG_STROKES[s[0]]))
        if len(orientations) != 1:
            continue
        front, reverse, count = orientations[0]
        pairs.append({"textnum": tid, "front": row_provenance(front),
                      "reverse": row_provenance(reverse), "long_stroke_count": count})
    families: dict[tuple[str, ...], list[dict[str, Any]]] = collections.defaultdict(list)
    for p in pairs:
        families[tuple(p["front"]["tokens_display"])].append(p)
    family_rows, certificates = [], []
    for seq, ps in sorted(families.items()):
        by_count: dict[int, list[str]] = collections.defaultdict(list)
        for p in ps:
            by_count[p["long_stroke_count"]].append(p["textnum"])
        entry = {"front_display": list(seq), "front_raw": list(reversed(seq)),
                 "objects_by_long_stroke_count": dict(sorted(by_count.items())),
                 "object_count": len(ps)}
        family_rows.append(entry)
        if len(by_count) > 1:
            lo, hi = min(by_count), max(by_count)
            p0 = next(p for p in ps if p["long_stroke_count"] == lo)
            p1 = next(p for p in ps if p["long_stroke_count"] == hi)
            certificates.append(entry | {
                "level": "catalogue_encoding_conditional_counterexample",
                "witnesses": [p0, p1],
                "assumptions": [
                    "The two encoded front strings represent the same complete expression.",
                    "An n-stroke reverse denotes n*u with the same u>0 in these cases.",
                    "The front and reverse each denote the same scalar quantity."
                ],
                "contradiction": f"F={lo}*u and F={hi}*u imply {hi-lo}*u=0, contradicting u>0.",
                "not_established": "Which assumption fails, a sign meaning, or a phonetic reading."
            })
    core = [e for e in family_rows if {2, 3, 4}.issubset(e["objects_by_long_stroke_count"])]
    counts = collections.Counter(reason for r in rows for reason in r["reasons"])
    solutions = positive_integer_solutions()
    summary = {
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "corpus": "Public indusscript.in / RMRL Mahadevan 1977 concordance",
        "snapshot_date_utc": "2026-09-05",
        "records": len(rows), "empty_surface_records": sum(not r["tokens"] for r in rows),
        "published_census": census, "all_six_published_census_checks_pass": True,
        "strict_rows": len(strict), "strict_unique_strings": len(unique),
        "strict_unique_string_tokens": sum(map(len, unique)),
        "strict_sign_inventory": len({t for s in unique for t in s}),
        "exclusion_reason_counts_overlapping": dict(counts),
        "strict_two_face_cup_long_stroke_objects": len(pairs),
        "distinct_front_strings": len(families),
        "front_strings_with_variable_reverse_count": len(certificates),
        "front_strings_observed_at_all_of_2_3_4": len(core),
        "core_grid_object_count": sum(e["object_count"] for e in core),
        "independence_warning": "Independent transcription, not an independent archaeological sample.",
        "novelty_warning": "New to this repository; scholarly priority is not established.",
    }
    output.mkdir(parents=True, exist_ok=True)
    with (output / "concordance_rows.csv").open("w", newline="", encoding="utf-8") as f:
        fields = META + [f"S{i}" for i in range(1, 15)] + ["strict", "exclusion_reasons"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fields[:-2]} |
                            {"strict": int(not r["reasons"]),
                             "exclusion_reasons": "|".join(r["reasons"])})
    (output / "concordance_documents.json.gz").write_bytes(gzip.compress(raw, mtime=0))
    write_json(output / "summary.json", summary)
    write_json(output / "paired_objects.json", pairs)
    write_json(output / "front_families.json", family_rows)
    write_json(output / "scalar_counterexamples.json", certificates)
    write_json(output / "four_by_three_grid.json", core)
    write_json(output / "conditional_radix_algebra.json", {
        "status": "conditional_arithmetic_not_a_decipherment",
        "prior_hypothesis": "Andreas Fuls (2020), numerical-value proposal",
        "equations": ["v=2*S-L", "v*L+1=7*S+5"],
        "derivation": "S*(2L-7)=L^2+4. Positive S requires d=2L-7>0. Then 4S=d+14+65/d, hence d divides 65.",
        "all_positive_integer_solutions": solutions,
        "with_assumed_bangle_bound_15_le_7_plus_L_le_20": [s for s in solutions if 15 <= 7+s["L"] <= 20],
        "evidence_warning": "The face-equality, additive, place-value, and bangle-count assumptions are not proved by this algebra."
    })
    write_json(output / "files.sha256.json", {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                              for p in sorted(output.iterdir())
                                              if p.is_file() and p.name != "files.sha256.json"})
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.input, args.output), indent=2))


if __name__ == "__main__":
    main()
