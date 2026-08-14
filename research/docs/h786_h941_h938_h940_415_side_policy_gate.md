# H-786 / H-941 / H-938 / H-940 415 Side Policy Gate

Date: 2026-05-26

This note is a gate — a checkpoint that evidence must pass before it may be used further. The thing being gated is a labeling question: published sources label the sides of an object with letters, the project's own transcription labels them with numbers, and nobody has shown the two systems line up. Until they do, some otherwise promising panels cannot count as evidence.

## Question

After the M-1206 terminal-component blind packet — a bundle assembled so the panels could be compared without the reviewer knowing which was the target — can the close `415` terminal-family panels on `H-786 A` and `H-941 A/A bis` be counted as exact-source-side evidence for local `+520-220-415+`, or must they remain quarantined behind side policy? To quarantine here means to set evidence aside as unusable until a specific blocker is cleared.

This is a language-decipherment gate, not a software task. The point is to decide which witnesses — individual source panels offered as evidence for a claim — are admissible evidence units before any claim about allography (deciding which shapes are variants of the same sign), sign splitting, or eventual translation is allowed.

## Policy Evidence

CISI Pakistan's introduction defines capital letters as side/photo labels: `A` normally marks the obverse, `B` the reverse, `C-F` other physical sides. Lowercase labels mark impressions of those sides. `bis`, `ter`, `quater`, and `quinquies` mark additional photographs of the same side, usually arranged oldest to latest. The stated purpose is unambiguous photo/reference identification.

Mahadevan/M77 uses numeric side codes in the text/concordance layer: `1` means first side, `2` second side, and so on. Its introduction says side order is fixed for analysis, the original publication order is not followed, and the criteria are provisional when multiple inscribed sides exist.

Therefore this equation is not admissible as a general rule:

```text
local .1 = CISI A
local .2 = CISI B
```

The two systems answer different questions. CISI `A/B` label physical or photographic sides. M77/local `.1/.2` label analytic side order in the standardized text layer.

## Local Rows

| Object | Local row | Local text | Source/visual side in current packet | Status before this gate |
| --- | --- | --- | --- | --- |
| `H-786` | `1677.1` | `+824-892-413+` | `A` is target-like | Conflict under naive `.1=A`, `.2=B` pairing |
| `H-786` | `1677.2` | `+520-220-415+` | `B` is not target-grade | Exact local row, source side unresolved |
| `H-938` | `1818.1` | `+520-220-415+` | `A/A bis` target-like | Clean exact-side control |
| `H-938` | `1818.2` | `+034-700+` | `B` companion side | Side-relation pressure only |
| `H-940` | `1820.1` | `+520-220-415+` | `A` target-like | Clean exact-side control |
| `H-940` | `1820.2` | `+110+` | `B` companion side | Non-target companion |
| `H-941` | `1821.1` | `+590-032-645-003+` | `A/A bis` target-like | Conflict under naive `.1=A`, `.2=B` pairing |
| `H-941` | `1821.2` | `+520-220-415+` | `B/B bis` not target-grade | Exact local row, source side unresolved |

The data-register pass does not close this. `H-786` has a single `AV 775` register route with no side-specific sign string. `H-941` separates physical/source references as `A: Pl. 37:673` and `B: Pl. 36:3872`, but still does not assign those source labels to local `1821.1` or `1821.2`.

## Adjudication

The old blocker was too crude: "`H-786/H-941` cannot be exact evidence because the target-like face is `A` while local exact `+520-220-415+` is `.2`."

That argument depended on a false general equation between local row numbers and CISI letters. The corrected blocker is sharper:

```text
H-786 A and H-941 A/A bis are visually relevant 415-family candidates.
They are not accepted exact-source-side 415 controls until an object-specific source table maps A/B to the local sign strings.
```

The exact-source-side control bin is therefore:

```text
H-938 A/A bis
H-940 A
```

`H-938 A bis` is a duplicate photograph of side `A`, not an independent recurrence. It is useful for preservation/visibility but does not add another object-level witness.

The side-policy-gated candidate bin is:

```text
H-786 A
H-941 A/A bis
```

A follow-up source-panel pattern recheck strengthens this candidate bin without changing admissibility:

```text
docs/h786_h941_source_a_pattern_recheck.md
```

It finds that source `A` carries the target-like broad three-class `415` pattern for `H-786`, `H-938`, `H-940`, and `H-941`, while source `B` does not. `H-939` remains a damaged stress case. This weakens any row-order explanation based on `.1/.2`, but still does not map `H-786 A` to `1677.2` or `H-941 A/A bis` to `1821.2`.

The excluded bin remains:

```text
H-939
H-786 B
H-941 B/B bis
```

## Effect On The M-1206 Branch

The terminal-component result stands, but its evidentiary weights are now explicit:

- `T006/T007` from `H-938 A/A bis` remain the strongest clean external `415` terminal controls.
- `H-940 A` remains a secondary exact-side `415` control.
- `T009/T010` from `H-786 A` and `H-941 A` remain close visual pressure only, not exact-side evidence.
- `H-938` also contains companion side `+034-700+`, which creates within-object `034/415` proximity pressure. It does not provide a sign value or translation.

The language question after this gate is:

```text
Do 034 and 415 represent separate signs, allographs, source-side mapping artifacts, or a transcription-policy split inside the 520-220-X frame?
```

This gate does not answer that question. It defines which witnesses are admissible for the next answer.

## Claim Status

Accepted:

```text
CISI A/B side labels and local .1/.2 row numbers cannot be equated globally.
H-938 A/A bis and H-940 A are the only current clean exact-source-side 415 controls in this H-786/H-941/H-938/H-940 side-policy packet.
H-786 A and H-941 A/A bis remain visually relevant but side-policy-gated.
```

Not accepted:

```text
H-786 A = local 1677.2 +520-220-415+
H-941 A/A bis = local 1821.2 +520-220-415+
415 stable fine-form identity
034 = 415
034 or 415 sign value
phonetic value
semantic value
translation
```

## Next Gate

Acquire or locate object-specific side-label/transcription notes for `H-786` and `H-941`, preferably from HARP/CISI end matter, CISI 3.1/supplemental tables, or archive/database rows that explicitly connect photo side labels to sign strings.

Until then, `H-786/H-941` should be used only as visual pressure in the `034/415` graphic-family branch.
