# 032-002-861 / 002-390-X Mayig shadow-lane check

Date: 2026-05-31 America/Los_Angeles

This note is a cross-check against a second corpus. Our main data lives in the Lipi numbering system; Mayig is an independent public-git corpus that records the same seals under its own P-numbered signs. The question: does the Mayig side reveal any object we are missing on the Lipi side? The answer is no — and the check also caught a trap, a Mayig sign pair that looks like a shortcut but silently mixes two different Lipi sequences.

Status: `mayig_shadow_exact_032_lane_no_replacement_pair_collision_guard_no_values`

This is a crosswalk/corpus triage guard only. (The "crosswalk" is our table of provisional links between Lipi signs and Mayig signs.) It does not accept a Lipi-to-Mayig sign mapping, source transcription, grammar, value, phonetics, language identity, function, sign meaning, or translation.

## Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531.mjs`
- Exact triple report: `data/open_prototype/reports/campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_exact_triples.csv`
- Broader pair report: `data/open_prototype/reports/campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_p122p086_rows.csv`
- Collision-edge report: `data/open_prototype/reports/campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_p086_collision_edges.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_mayig_shadow_lane_check_20260531_summary.json`

## Question

The local matched-lane gate says the live `032` predecessor split depends on two objects:

- strict/source-visible `M-70 +226-032-002-390-692+`
- blocked/unbound `3335.1 +740-205-032-002-390-590-032+`

The question here was whether the Mayig public-git P namespace, through the local provisional crosswalk, exposes a replacement witness for the blocked `032` lane — another object attesting the same pattern — or any new public-git shadow row that should change acquisition priority.

## Exact `032/P145` lane

The checked crosswalk edges still mark all relevant mappings as unaccepted:

| Lipi sign | Mayig sign | Support | Counters | Confidence | Accepted |
|---|---|---:|---:|---|---|
| `032` | `P145` | 20 | 1 | medium_low | false |
| `002` | `P122` | 57 | 2 | medium_low | false |
| `390` | `P086` | 25 | 0 | medium_low | false |

The exact Mayig sequence `P145 P122 P086` appears once:

| Mayig object | Mayig sequence | Local counterpart |
|---|---|---|
| `M-70` | `P051 P145 P122 P086 P256` | `M-70 +226-032-002-390-692+` |

The local exact `032-002-390` rows remain exactly the known pair:

| Local object | Local text | Status |
|---|---|---|
| `M-70` | `+226-032-002-390-692+` | known strict-visible `032` lane |
| `3335.1` | `+740-205-032-002-390-590-032+` | dash-CISI/source-unbound |

Decision: Mayig adds no replacement for `3335.1`. The exact shadow lane returns only `M-70`, which is already in the live gate.

## Broader `P122 P086` pair guard

The broader Mayig pair `P122 P086` appears six times:

| Mayig object | Mayig next | Local status |
|---|---|---|
| `M-34` | `P108` | local `002-405`, not `002-390` |
| `M-38` | `P035` | local `002-390-125` |
| `M-41` | `P035` | local `002-405`, not `002-390` |
| `M-70` | `P256` | local `002-390-692` |
| `M-71` | `P023` | local `002-390-095` |
| `M-119` | `P035` | local `002-390-125` |

This is the important adversarial result. If we broaden from exact `P145 P122 P086` to just `P122 P086`, the Mayig layer starts mixing local `002-390` with local `002-405` — two different Lipi sequences collapse into one Mayig pattern. The collision is not subtle: the provisional reverse edges include `390 -> P086`, but also weak, unaccepted `405 -> P086`, `406 -> P086`, and `407 -> P086` edges. In other words, the single Mayig sign `P086` may stand for several different Lipi signs.

Decision: do not use Mayig `P122 P086` to inflate the `002-390-X` frame. It is useful for triage, but it is unsafe as source-normalized branch evidence.

## Consequence

This check preserves the current live state:

- `M-70` remains the only strict/source-visible member of the `032 -> 002-390` matched lane.
- `3335.1` remains the required single-object unlock for a strict `032` matched predecessor split, unless a genuinely new source-bound replacement appears.
- The crosswalk does not rescue `3335.1` and does not add a new `032` branch witness.
- The broader Mayig `P122 P086` pair is an adversarial collision guard — a recorded warning against a tempting but unsafe inference — not a promotion route.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain `0`.
