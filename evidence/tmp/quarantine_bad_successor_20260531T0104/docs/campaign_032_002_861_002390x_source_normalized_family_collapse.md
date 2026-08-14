# 032-002-861 / 002-390-X Source-Normalized Family Collapse

Date: 2026-05-31

## Question

Do the two tempting `125` positives survive once we enforce source visibility and formula-family collapse?

Targets:

- `235 -> 002-390 -> 125`
- `125 -> 632 032`

This is an adversarial gate against the positive subframe reading, not a route hunt and not a value claim.

## Materials

- Runner: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\tools\campaign_032_002_861_002390x_source_normalized_family_collapse.py`
- Summary: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_source_normalized_family_collapse_summary.json`
- Collapse tests: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_source_normalized_family_collapse_collapse_tests.csv`
- Occurrences: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_source_normalized_family_collapse_occurrences.csv`
- Focus rows: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_source_normalized_family_collapse_focus_rows.csv`

Input rows scanned: `5,679` local metadata rows.

## Collapse Results

| pattern | raw rows | strict source-visible rows | strict source-visible objects | adversarial result |
|---|---:|---:|---|---|
| `235-002-390-125` | 2 | 1 | `M-735` | raw `2/2` demotes to one strict witness because `M-38` remains weak/not token-boxable |
| `125-632-032` global | 4 | 1 | `M-119` | wider than the earlier in-frame count, but still one strict witness only |
| `125-632-032` inside `002-390-X` | 2 | 1 | `M-119` | in-frame positive demotes because the second row is weak `M-38` |
| `002-390-125` | 4 | 2 | `M-119 M-735` | branch survives as plurality, but strict layer is only two Mohenjo-daro square seal rows |
| `002-390-095` | 2 | 1 | `M-71` | one strict terminal comparator plus H-1993 route-only pressure |
| `002-390-705` | 2 | 0 | none | repeated terminal comparator remains source-gated |
| `002-390-692` | 1 | 1 | `M-70` | single strict visible terminal control |

## Extra Row Correction

The global `125-632-032` scan found four rows:

- `M-1692`: `+390-600-617-002-190-125-632-032+`
- `M-38`: `+740-690-435-255-220-032-240-235-002-390-125-632-032+`
- `M-119`: `+151-337-484-002-390-125-632-032-900-563+`
- `M-1188`: damaged/open row `]000/000-125-632-032/240-002-244-632+`

Only `M-38` and `M-119` sit in the immediate `002-390-X` lane. Only `M-119` is strict source-visible right now.

This matters because `125-632-032` is not merely a private tail of `002-390-125`. It has a broader Mohenjo-daro `SEAL:S` metadata footprint. A broader footprint raises formula-family pressure, not confidence.

## Decision

The positive subframes do not survive source-normalized family collapse.

Accepted:

- `002-390-X` remains a live branch-tail ecology object.
- `125` remains a plurality branch after `002-390`, with strict source-visible support from `M-119/M-735`.
- `125-632-032` is a broader local formula/tail candidate worth source-normalizing.

Demoted:

- `235 -> 002-390 -> 125` as an independent positive subframe. It is now one strict witness plus weak `M-38`.
- `125 -> 632 032` inside `002-390-X` as an independent positive subframe. It is now one strict witness plus weak `M-38`.

Still blocked:

- H-1993 is still transcription/figure-route pressure only.
- `705` remains source-gated: M-1825 is image-dark and Dholavira `4237.1` remains unbound.
- No source-window proof, sign function, value, phonetic reading, language identity, sign meaning, or translation is accepted.

## Next Gate

The next high-payoff gate is no longer defending either positive subframe. It is one of:

1. Bind `705` through Dholavira `4237.1` or M-1825.
2. Bind H-1993 Figure `17.07` to an artifact image for the repeated `095` comparator.
3. Token-box or demote `M-38`, because it is the shared weak hinge of both failed positive subframes.
