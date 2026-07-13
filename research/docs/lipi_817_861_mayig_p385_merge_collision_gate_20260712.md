# Lipi 817/861 / Mayig P385 merge and collision gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FEATURE_PRESERVING_MERGE_WITH_CONTEXTUAL_803_COLLISION`.

Scope:

- accept observed `{lipi_numeric:817, lipi_numeric:861} -> mayig_p:P385` only as a feature-preserving merge in an explicit Mayig-policy lane;
- reject exact/bidirectional identity and raw Lipi collapse;
- keep M-177's local `803 / P385` alignment as an object-level namespace conflict, not a global `803 -> P385` mapping;
- keep `lipi_numeric:803 -> mayig_p:P364` conflicted and unaccepted at 9/10.

Nothing here supplies a sign meaning, reading, phonetic value, language identification, or translation.

## Alignment pressure

Both intended merge members have clean forward lanes:

| Lipi member | P385 support | Counterexamples | Forward share |
| --- | ---: | ---: | ---: |
| 817 | 12 | 0 | 1.000000 |
| 861 | 12 | 0 | 1.000000 |

The reverse P385 lane has 25 positions:

| Lipi sign at P385 position | Count | P385 roundedness |
| --- | ---: | --- |
| 817 | 12 | `0` in all witnesses: round |
| 861 | 12 | `1` in all witnesses: angular |
| 803 | 1 | `0`: round, M-177 only |

The 817/861 division is exactly the distinction P385's own `roundedness` feature preserves. This supports a feature-bearing merge, not exact identity.

## Source-visible packet

The local CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

| Object | CISI page | Lipi sequence | Mayig sequence | Aligned sign/position | Role |
| --- | --- | --- | --- | --- | --- |
| M-1 A | PDF 37 / printed 1 | `001 368 861 255 371` | `P121 P202 P385 P073 P108` | `861/P385`, 3 | angular, medial |
| M-15 A | PDF 47 / printed 11 | `090 740 176 002 861` | `P013 P324 P194 P122 P385` | `861/P385`, 5 | angular, terminal |
| M-21 A | PDF 49 / printed 13 | `350 001 740 362 692 032 002 861` | `P091 P121 P324 P272 P256 P145 P122 P385` | `861/P385`, 8 | angular, terminal |
| M-14 A | PDF 47 / printed 11 | `740 776 503 002 817` | `P324 P117 P210 P122 P385` | `817/P385`, 5 | round, terminal |
| M-32 A | PDF 53 / printed 17 | `390 003 002 817` | `P086 P123 P122 P385` | `817/P385`, 4 | round, terminal |
| M-148 A | PDF 82 / printed 46 | `740 817 556` | `P324 P385 P231` | `817/P385`, 2 | round, medial |
| M-177 A | PDF 87 / printed 51 | `390 003 002 803` | `P086 P123 P122 P385` | `803/P385`, 4 | contextual collision |

The panels preserve the complete seal and printed object label. M-177's final reading-order sign is visibly the rounded P385 leaf/diamond family and lacks a clear basal tree. It closely matches the rounded M-32/817 form. The source image therefore confirms the catalogue-policy collision; it does not justify editing either corpus.

Panel manifest: `research/data/sign_crosswalk/source_panels/817_861_P385_conflict/manifest.csv`.

## Pinned Mayig evidence

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `P385` is a diamond or leaf with a small diamond attached at the top. It mediates Wells `W817` and `W861`, and its custom feature is roundedness: 0 round, 1 angular, 2 mixed/indeterminate.
- Every local-817 witness aligned to P385 has roundedness 0.
- Every local-861 witness aligned to P385 has roundedness 1. M-170 carries nonzero default damage/uncertainty fields, but its roundedness remains 1.
- `P364` is a leaf with a tree at the bottom and mediates Wells `W803/W805/W806`, with branch-count/style features.
- The nine ordinary local-803 alignments go to P364; M-177 is the sole local-803/P385 occurrence.

Exact raw-file hashes for both feature records and the seven selected Mayig object records are stored in `evidence_refs.csv`.

## Decision

The 817/861 merge is acceptable only because the target namespace explicitly preserves their visible rounded/angular distinction. Therefore:

- edges `817 -> P385` and `861 -> P385` become `mapping_state=merge`, `accepted_for_analysis=true` only in an explicit feature-preserving Mayig lane;
- raw Lipi and `conservative_merge` keep 817 and 861 distinct;
- no exact or bidirectional identity is accepted;
- M-177 is recorded as a source-visible contextual `803/P385` collision;
- edge `803 -> P364` becomes `mapping_state=conflict`, remains unaccepted, and must not be silently repaired;
- no new `803 -> P385` global edge is created.

Accepted decipherment-count increment: `0`.
