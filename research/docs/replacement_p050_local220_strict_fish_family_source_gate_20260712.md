# Replacement P050 / Local 220 Strict Fish-Family Source Gate

Date: 2026-07-12

State: fixed adjudication snapshot pending execution. Its current inputs deterministically record `PARK`; genuinely new evidence requires a new dated gate.

## Question

Do exact same-object, same-side, same-position source token boxes earn a strict crosswalk between local Lipi `220` and Mayig `P050`?

This is narrower than the earlier Parpola sign-60 gate. It tests the missing local-to-Mayig source bridge first. It does not test a lexical value, phonetic reading, language identity, or translation.

## Why this is the next gate

The 2026-05-26 strict packet established only broad fish/leaf-family compatibility for local `220`. Its explicit next requirement was clean source-visible Mayig `P050` examples. The pinned Mayig repository does not bundle object images, but it does identify `P050` on exact CISI sides. A workable public-data route is therefore:

1. bind a Lipi row and a Mayig side for the same CISI object;
2. require `220` and `P050` at the same sequence index;
3. bind that index to a visible glyph box on the matching object panel;
4. distinguish broad fish/leaf compatibility from the stronger claim that the body is visibly undecorated.

The runner is:

```text
research/data/open_prototype/tools/replacement_p050_local220_strict_fish_family_source_gate_20260712.py
```

## Pinned witnesses

| Neutral ID | Object-side | Lipi row | Local sequence | Mayig sequence | Target index | Cached panel |
| --- | --- | --- | --- | --- | --- | --- |
| `T001` | `M-37A` | `2565.1` | `520 220 415` | `P217 P050 P092` | 2 | `M-37_a.jpg` |
| `T002` | `M-124A` | `2651.1` | `740 923 220 032` | `P324 P175 P050 P145` | 3 | `M-124_a.jpg` |
| `T003` | `M-151A` | `2678.1` | `220 065 864` | `P050 P201 P393` | 1 | `M-151_a.jpg` |
| `T004` | `M-174A` | `2699.1` | `740 923 220 032 002 820` | `P324 P175 P050 P145 P122 P378` | 3 | `M-174_a.jpg` |

All four source panels were visually inspected before the snapshot was encoded. Each object is one-sided in Lipi, with `R/L` metadata, and each lowercase-`a` cached derivative exposes the expected row and a broad fish/leaf-compatible target at the visually aligned transcript position. The object/impression mirror relation remains unresolved and is not used to claim physical reading direction. None is a high-resolution, independently cited primary catalog plate. Fine internal decoration cannot be ruled out from these cached derivatives, and `M-174` is marked `Poor` in the Lipi condition field.

That distinction is decisive. Mayig describes `P050` as `Fish with no other decoration`; a blurred fish-like outline does not prove the absence of decoration.

## Fixed adjudication decisions

### Pass

The strict `220 = P050` source bridge passes only if all of the following hold:

1. at least three independent CISI artifacts have exact Lipi/Mayig same-position bindings;
2. at least three independent target boxes come from pinned primary-catalog object-side panels;
3. each passing box isolates the target, resolves the row token count, and visibly shows the plain undecorated fish type at medium-high or high confidence;
4. no strict witness is position-inconsistent, decorated, or assigned to a neighboring fish-family type.

Passing this gate would accept only the local `220` to Mayig `P050` sign crosswalk. It would not establish Parpola article sign no. `60`, a semantic value, or a translation.

### Park

The bridge parks when at least one exact source-position binding survives and no contradiction is visible, but the primary-source, isolation, resolution, or undecorated-body requirements remain incomplete.

The pinned snapshot parks because all four panels are low-resolution cached derivatives and every internal-decoration judgment is unresolved.

### Fail

The bridge fails if a strict source witness contradicts the same-position assignment, visibly belongs to a decorated or different nearby type, or no source-bound target survives validation.

## Outputs on execution

The runner writes only generated artifacts under `research/data/open_prototype/reports/`:

```text
replacement_p050_local220_strict_fish_family_source_gate_20260712_witnesses.csv
replacement_p050_local220_strict_fish_family_source_gate_20260712_criteria.csv
replacement_p050_local220_strict_fish_family_source_gate_20260712_summary.json
replacement_p050_local220_strict_fish_family_source_gate_20260712_token_boxes/
```

The token-box directory contains a neutral contact sheet, original crops, and grayscale review enlargements. The output summary keeps accepted crosswalks, values, phonetic readings, and translations at zero unless the strict pass rule is actually met.

## Execution

From the repository root, fold this into the next integrated research run:

```powershell
& 'C:\Users\Acer\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\data\open_prototype\tools\replacement_p050_local220_strict_fish_family_source_gate_20260712.py'
```

Do not treat successful file generation as a substantive pass. The outcome field in the generated summary is the gate decision.
