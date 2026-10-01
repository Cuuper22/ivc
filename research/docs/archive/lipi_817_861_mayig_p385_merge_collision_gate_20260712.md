# Lipi 817/861 / Mayig P385 merge and collision gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FEATURE_PRESERVING_MERGE_WITH_CONTEXTUAL_803_COLLISION`.

## What this is and why it exists

Lipi, the numeric catalogue, keeps two separate numbers for a leaf-or-diamond sign: `817` and `861`. Mayig, the Parpola-style catalogue, files both under one code, `P385`. That is a merge, an edge where several signs in one catalogue map to a single sign in the other.

A merge normally destroys information, and that is why merges are dangerous. This one is different, and the difference is the whole reason it can be accepted. Mayig does not just assign the code; alongside it Mayig stores a feature vector, a fixed list of measured attributes attached to the sign. One of P385's features is roundedness. Every `817` witness is round and every `861` witness is angular, so the very distinction Lipi encodes in two numbers is still recorded inside Mayig, just in a different field. Nothing is lost, provided the analysis actually reads that field.

There is also a complication. One object, M-177, puts a third Lipi number at a P385 position. That is a collision, and it is handled separately below rather than being smoothed away.

Scope:

- accept observed `{lipi_numeric:817, lipi_numeric:861} -> mayig_p:P385` only as a feature-preserving merge, and only in a run that explicitly declares itself a Mayig-policy lane;
- reject exact/bidirectional identity and raw Lipi collapse;
- keep M-177's local `803 / P385` alignment as an object-level namespace conflict, not a global `803 -> P385` mapping;
- keep `lipi_numeric:803 -> mayig_p:P364` conflicted and unaccepted at 9/10.

Nothing here supplies a sign meaning, reading, phonetic value, language identification, or translation.

## Alignment pressure

Alignment pressure is the case for the mapping: how often each label lands on the same position of the same object. A lane is one direction of that mapping, and the two directions have to be read separately.

Both intended merge members have clean forward lanes:

| Lipi member | P385 support | Counterexamples | Forward share |
| --- | ---: | ---: | ---: |
| 817 | 12 | 0 | 1.000000 |
| 861 | 12 | 0 | 1.000000 |

Going the other way, from P385 back to Lipi, the lane has 25 positions and lands on three different numbers:

| Lipi sign at P385 position | Count | P385 roundedness |
| --- | ---: | --- |
| 817 | 12 | `0` in all witnesses: round |
| 861 | 12 | `1` in all witnesses: angular |
| 803 | 1 | `0`: round, M-177 only |

Look at the roundedness column. The split between `817` and `861` is not blurred by the merge; it is exactly what P385's own `roundedness` feature records, round in every 817 witness and angular in every 861 witness. That is what justifies a merge that carries features along, and it is also why the pair still cannot be called an exact identity: `817` and `861` remain two different things inside Mayig's own record.

## Source-visible packet

A witness is a specific object whose published image is checked so that a mapping rests on a real inscription and not only on agreeing tables. Panels are labeled crops rendered from the source PDF and kept as files.

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

Each panel shows the complete seal and the printed object label. The last row is the awkward one. M-177's final sign in reading order is plainly in the rounded P385 leaf/diamond family, and it has no clear tree at its base, which is what a `803` form would need. It looks much like the rounded M-32 `817` form. So the image confirms that the collision is real rather than clerical. Confirming a collision is not the same as resolving it, and it is certainly not grounds for editing either corpus.

Panel manifest: `research/data/sign_crosswalk/source_panels/817_861_P385_conflict/manifest.csv`.

## Pinned Mayig evidence

Pinned means the evidence is read from one fixed commit, so the record cannot change under the decision later.

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `P385` is a diamond or leaf with a small diamond attached at the top. It mediates Wells `W817` and `W861`, meaning those are the Wells-catalogue identifiers Mayig associates with the code. Its custom feature is roundedness: 0 round, 1 angular, 2 mixed/indeterminate.
- Every local-817 witness aligned to P385 has roundedness 0.
- Every local-861 witness aligned to P385 has roundedness 1. M-170 has nonzero damage and uncertainty fields, but its roundedness still reads 1.
- `P364` is a leaf with a tree at the bottom. It mediates Wells `W803/W805/W806` and carries branch-count and style features.
- Nine of the ten local-803 alignments go to P364, where they belong. M-177 is the only place local `803` meets P385.

Exact raw-file hashes for both feature records and the seven selected Mayig object records are stored in `evidence_refs.csv`.

## Decision

The merge is acceptable for one reason only: the target namespace keeps the visible rounded-versus-angular distinction instead of discarding it. Take away that feature and the merge would not be acceptable. Therefore:

- edges `817 -> P385` and `861 -> P385` become `mapping_state=merge`, with `accepted_for_analysis=true` only in a run that explicitly declares itself a feature-preserving Mayig lane;
- raw Lipi and `conservative_merge` keep 817 and 861 distinct;
- no exact or bidirectional identity is accepted;
- M-177 is recorded as a source-visible contextual `803/P385` collision, kept as a known exception rather than tidied away;
- edge `803 -> P364` becomes `mapping_state=conflict`, remains unaccepted, and must not be quietly repaired to hide the M-177 case;
- no new global `803 -> P385` edge is created. One object does not make a rule.

Accepted decipherment-count increment: `0`.
