"""Check that the numbers the project's conclusions rest on still come out the same.

Run after `make audit campaign`. Compares values, not file bytes: float noise and
extra report fields are fine; a changed count or a changed model ranking is not.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "build" / "audit" / "summary.json"
JOINT = ROOT / "research/campaigns/integrated_20260906/integration/summary.json"

EXPECTED_AUDIT = {
    "all_six_published_census_checks_pass": True,
    "strict_rows": 2575,
    "strict_unique_strings": 1659,
    "strict_two_face_cup_long_stroke_objects": 85,
    "distinct_front_strings": 39,
    "front_strings_with_variable_reverse_count": 8,
    "front_strings_observed_at_all_of_2_3_4": 4,
    "core_grid_object_count": 34,
}

# Joint description length (bits) of each model in the integrated campaign; lower is better.
EXPECTED_JOINT = {
    "categorical_identity": 3169.575,
    "fish211": 3177.455,
    "fish_roof87_tick211": 3192.965,
}
TOLERANCE_BITS = 0.01

failures = []

audit = json.loads(AUDIT.read_text())
for key, want in EXPECTED_AUDIT.items():
    if audit.get(key) != want:
        failures.append(f"audit {key}: expected {want}, got {audit.get(key)}")

joint = {m["model"]: m["total_bits"] for m in json.loads(JOINT.read_text())["joint"]}
for model, want in EXPECTED_JOINT.items():
    got = joint.get(model)
    if got is None or abs(got - want) > TOLERANCE_BITS:
        failures.append(f"joint {model}: expected {want}, got {got}")
ranking = sorted(joint, key=joint.get)
if ranking[0] != "categorical_identity" or ranking[-1] != "fish_roof87_tick211":
    failures.append(f"joint ranking changed: best {ranking[0]}, worst {ranking[-1]}")

if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"headline numbers ok ({len(EXPECTED_AUDIT)} audit values, {len(joint)} joint models)")
