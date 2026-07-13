# Damaged-boundary fragment closure

Date: 2026-07-12 America/Los_Angeles

Decision: `ALL_FOUR_BOUNDARY_MISMATCHES_ARE_CENSORED_SEQUENCES; P000_IS_NONSIGN_EDGE_LOSS; PRESERVED_COUNTS_ARE_2_2_6_6`.

## Question

`M-19`, `M-22`, `M-39`, and `M-175` are the final unresolved class in the 29-row Lipi/Mayig count-mismatch queue. Every row combines an open Lipi boundary with one additional Mayig `P000`. The source question was whether `P000`, a Lipi boundary zero, or visible edge residue establishes another sign position.

## Object decisions

| Object | Lipi | Mayig | CISI result | Normalized source representation |
| --- | --- | --- | --- | --- |
| `M-19` | `]000-000-002-861+`; length `4+?`; 2 identified | `P000(75) P122 P385` | PDF 49 / print 13. Two bounded signs survive after one continuous broken prefix. Neither Lipi zero is individually source-bounded. The edge after `861` is closed. | `[LOSS_PREFIX capacity=unknown] 002 861 [CLOSED_EDGE]`; preserved count 2. |
| `M-175` | `]002-861+`; length `2+?`; 2 identified | `P000(70) P122 P385` | PDF 87 / print 51. Two sign-bearing units survive after an unbounded broken prefix. `002/P122` is damaged and uncertain; `861/P385` is clear at the closed edge. | `[LOSS_PREFIX capacity=unknown] 002 861 [CLOSED_EDGE]`; preserved count 2. |
| `M-39` | `]705-240-235-013-204-346+`; length `6+?`; 6 identified | `P000(15)` plus 6 named graphemes | PDF 56 / print 20. Six separately bounded signs survive after a chipped prefix. No seventh sign is bounded inside the break; the opposite edge is closed after `346`. | `[LOSS_PREFIX capacity=unknown] 705 240 235 013 204 346 [CLOSED_EDGE]`; preserved count 6. |
| `M-22` | `+740-904-176-220-032-798-000[`; length `7+?`; 6 identified | 6 named graphemes plus `P000(15)` | PDF 50 / print 14. Six signs are separately preserved. The final residue is edge-cut and has no independent outline in either mirrored view. | `[CLOSED_EDGE] 740 904 176 220 032 798 [LOSS_SUFFIX capacity=unknown]`; preserved count 6. |

The Mayig percentages are catalogue annotations, not new measurements. In all four rows, `P000` describes the open loss span and contributes zero signs.

## Accepted boundary policy

- Count only independently bounded source-visible sign positions.
- Encode an open fracture as `<LOSS_PREFIX>` or `<LOSS_SUFFIX>` with unknown capacity, not as `<UNK_SIGN>` and not as `P000` in the sign stream.
- A Lipi `000` counts as a sign only when the plate locates a bounded graphic slot. The two M-19 zeros and terminal M-22 zero are inside unbounded edge loss and do not meet that condition.
- Preserve every adjacency wholly inside the surviving run. Do not create an adjacency across a loss span.
- Preserve closed-edge status only on the intact side: after `861` on M-19/M-175, after `346` on M-39, and before `740` on M-22.
- Original total length remains unknown for all four objects. None belongs in complete-length, absolute-position, or closed-whole-string analyses.
- M-19 and M-175 may enter uncertainty-aware analysis as left-censored bare terminal `002-861` suffixes. M-39 contributes a left-censored six-sign suffix. M-22 contributes a right-censored six-sign prefix and does not license terminality for `798`.
- All Lipi/Mayig sign alignments remain object-local here. No global crosswalk is promoted.

## Research consequence

The `damaged_boundary_fragment` class closes at `4/4`, so all 29 rows in the mismatch queue now have source-level adjudications. Closure does not mean every row becomes a clean sequence: these four remain censored observations with unknown original length.

M-19 and M-175 add two source-visible bare terminal `002-861` suffix controls to the live fixed-prefix tail question. They should be added with left-censoring and damage flags, not as complete two-sign texts. The next research calculation is the delta in the `002-861` bare-versus-tailed contrast after admitting those two censored controls; no new GPU run is needed for that test.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-19_A_a_CISI1_pdf49_print13.png`, SHA-256 `1603EF160EA6CCB643ABB89B543235C14F6E3ABE34789A2BF1A87A1FF9CEFD7C`.
- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-22_A_a_CISI1_pdf50_print14.png`, SHA-256 `0C33E1E735694255F483528FCB43E2C6DEB49957AB1334E83495FFE07639108B`.
- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-39_A_a_CISI1_pdf56_print20.png`, SHA-256 `2510E0B551C11C1153D38A1DBC98E3F6D50FA4F0CF8F6390ABB582DC1D7522EE`.
- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-175_A_a_CISI1_pdf87_print51.png`, SHA-256 `28BE3AC79EB8742AF932C30B1FDCEA56AD525DA67F10C5F8083872A4842D68CB`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi metadata SHA-256: `B3E2A94EFDF70EAA893BBBBD35FD057B53F766C82823A3EFB8EE37F9365311FE`.
- Mayig records: `m019.json` `DC1501EAE242D086B21E8186361CDA10C2EEB18F3A4A6757D225FA65B69968BC`; `m022.json` `FC532337EAF7442A37B085C7C8528A6F7C18A89E30F637701DEE202ADAD34BA8`; `m039.json` `781743A8AB611959274D266A6418658ECCDDE92A390FB0AC2AB00C856D2F8E69`; `m175.json` `0E87ADD681F412685206165216C91027DDE3F6E470789362BE068CB82C39FA6F`.
- Mayig `P000.json` SHA-256: `6F6B7ECC5D2DB2D6F317CDBBC3B4E24F4DC412C891554405E9312A0B8204467A`.
