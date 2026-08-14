# Damaged-boundary fragment closure

Date: 2026-07-12 America/Los_Angeles

Decision: `ALL_FOUR_BOUNDARY_MISMATCHES_ARE_CENSORED_SEQUENCES; P000_IS_NONSIGN_EDGE_LOSS; PRESERVED_COUNTS_ARE_2_2_6_6`.

## What this is and why it exists

Some seals are broken. When an inscription runs off a fractured edge, you cannot know how many signs were lost, and pretending otherwise corrupts every count that follows. This note decides how to record four such objects so that what survives can still be used and what is missing stays visibly missing.

The two catalogues involved are Lipi, which writes signs as numbers, and Mayig, which writes them as `P` codes. Lipi marks an open, broken boundary with a bracket: `]` at the start of a row means the text is cut off before the first surviving sign, and `[` at the end means it is cut off after the last one. Lipi also writes `000` for a sign slot it cannot identify. Mayig instead writes `P000` for a span of lost material, with a percentage for how much is gone.

Where those conventions meet at a broken edge, they can look like they are each claiming an extra sign position. That is the ambiguity here.

## Question

`M-19`, `M-22`, `M-39`, and `M-175` are the final unresolved class in the 29-row Lipi/Mayig count-mismatch queue, the running list of objects where the two catalogues disagree about how many units an inscription has. Every one of these four rows combines an open Lipi boundary with one extra Mayig `P000`. The source question was whether any of three things establishes another sign position: the `P000`, a Lipi boundary zero, or visible residue at the edge.

## Object decisions

| Object | Lipi | Mayig | CISI result | Normalized source representation |
| --- | --- | --- | --- | --- |
| `M-19` | `]000-000-002-861+`; length `4+?`; 2 identified | `P000(75) P122 P385` | PDF 49 / print 13. Two bounded signs survive after one continuous broken prefix. Neither Lipi zero is individually source-bounded. The edge after `861` is closed. | `[LOSS_PREFIX capacity=unknown] 002 861 [CLOSED_EDGE]`; preserved count 2. |
| `M-175` | `]002-861+`; length `2+?`; 2 identified | `P000(70) P122 P385` | PDF 87 / print 51. Two sign-bearing units survive after an unbounded broken prefix. `002/P122` is damaged and uncertain; `861/P385` is clear at the closed edge. | `[LOSS_PREFIX capacity=unknown] 002 861 [CLOSED_EDGE]`; preserved count 2. |
| `M-39` | `]705-240-235-013-204-346+`; length `6+?`; 6 identified | `P000(15)` plus 6 named graphemes | PDF 56 / print 20. Six separately bounded signs survive after a chipped prefix. No seventh sign is bounded inside the break; the opposite edge is closed after `346`. | `[LOSS_PREFIX capacity=unknown] 705 240 235 013 204 346 [CLOSED_EDGE]`; preserved count 6. |
| `M-22` | `+740-904-176-220-032-798-000[`; length `7+?`; 6 identified | 6 named graphemes plus `P000(15)` | PDF 50 / print 14. Six signs are separately preserved. The final residue is edge-cut and has no independent outline in either mirrored view. | `[CLOSED_EDGE] 740 904 176 220 032 798 [LOSS_SUFFIX capacity=unknown]`; preserved count 6. |

The Mayig percentages are catalogue annotations copied from the source, not measurements taken here. In all four rows, `P000` describes the open loss span and contributes zero signs.

## Accepted boundary policy

The rule is simple: count what you can see the edges of, and mark the rest as unknown rather than guessing at it.

- Count only sign positions that are independently bounded and visible in the source.
- Encode an open fracture as `<LOSS_PREFIX>` or `<LOSS_SUFFIX>` with unknown capacity. Do not encode it as `<UNK_SIGN>`, which would assert exactly one lost sign, and do not leave `P000` sitting in the sign stream.
- A Lipi `000` counts as a sign only when the plate shows a bounded graphic slot for it. The two M-19 zeros and the terminal M-22 zero sit inside unbounded edge loss, so they do not meet that condition.
- Keep every adjacency that lies wholly inside the surviving run. Never create an adjacency across a loss span, because you do not know what stood in between.
- Record closed-edge status only on the side that is actually intact: after `861` on M-19/M-175, after `346` on M-39, and before `740` on M-22.
- Original total length stays unknown for all four objects. None of them belongs in an analysis of complete length, absolute position, or closed whole strings.
- Censored means one end of the text is cut off, so the observation is real but incomplete. M-19 and M-175 may enter uncertainty-aware analysis as left-censored bare terminal `002-861` suffixes. M-39 contributes a left-censored six-sign suffix. M-22 contributes a right-censored six-sign prefix, and it does not license a terminality claim for `798`, because something may have followed it.
- Every Lipi/Mayig sign alignment here is object-local. No global crosswalk edge is promoted.

## Research consequence

The `damaged_boundary_fragment` class closes at `4/4`. That was the last open class, so all 29 rows in the mismatch queue now have source-level adjudications. Closure does not mean these four became clean sequences. They remain censored observations of unknown original length.

M-19 and M-175 are useful for a separate live question. That question asks whether the fixed prefix `002-861` behaves differently when a tail follows it than when it stands bare, and these two objects supply source-visible bare terminal `002-861` controls. Add them with left-censoring and damage flags, not as if they were complete two-sign texts. The next calculation is the change in the `002-861` bare-versus-tailed contrast once those two censored controls are admitted. That test needs no new GPU run.

Nothing here adds a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-19_A_a_CISI1_pdf49_print13.png`, SHA-256 `1603EF160EA6CCB643ABB89B543235C14F6E3ABE34789A2BF1A87A1FF9CEFD7C`.
- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-22_A_a_CISI1_pdf50_print14.png`, SHA-256 `0C33E1E735694255F483528FCB43E2C6DEB49957AB1334E83495FFE07639108B`.
- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-39_A_a_CISI1_pdf56_print20.png`, SHA-256 `2510E0B551C11C1153D38A1DBC98E3F6D50FA4F0CF8F6390ABB582DC1D7522EE`.
- `research/data/sign_crosswalk/source_panels/damaged_boundary_fragment_closure/M-175_A_a_CISI1_pdf87_print51.png`, SHA-256 `28BE3AC79EB8742AF932C30B1FDCEA56AD525DA67F10C5F8083872A4842D68CB`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi metadata SHA-256: `B3E2A94EFDF70EAA893BBBBD35FD057B53F766C82823A3EFB8EE37F9365311FE`.
- Mayig records: `m019.json` `DC1501EAE242D086B21E8186361CDA10C2EEB18F3A4A6757D225FA65B69968BC`; `m022.json` `FC532337EAF7442A37B085C7C8528A6F7C18A89E30F637701DEE202ADAD34BA8`; `m039.json` `781743A8AB611959274D266A6418658ECCDDE92A390FB0AC2AB00C856D2F8E69`; `m175.json` `0E87ADD681F412685206165216C91027DDE3F6E470789362BE068CB82C39FA6F`.
- Mayig `P000.json` SHA-256: `6F6B7ECC5D2DB2D6F317CDBBC3B4E24F4DC412C891554405E9312A0B8204467A`.
