# M-106 damage-span structural-count gate

Date: 2026-07-12 America/Los_Angeles

Decision: `M106_HAS_SIX_STRUCTURAL_SLOTS; MAYIG_P000_COLLAPSES_FOUR_SLOTS_AS_DAMAGE_METADATA`.

## Question

`M-106` is the sole `complex_manual_collation` row in the mismatch queue. Lipi records six positions, including two `000` unknowns, while Mayig records two named graphemes followed by one `P000` damage token. The source question was whether the object supports six sign slots, three units, or only an unresolved damaged remainder.

## Source-visible alignment

Both published views in CISI 1, PDF page 75 / printed page 39, preserve the same structure. The opening handled jar and decorated U are clear. Across the abraded remainder, the two-stroke `002` and terminal branched `350` remain recoverable. Two damaged sign slots are separately located on either side of `002`; their graphic identities are not recoverable.

| Structural position | Lipi row `2633.1` | Mayig `M-106A` | CISI decision |
| --- | --- | --- | --- |
| 1 | `740` | `P324` | Identifiable handled jar. |
| 2 | `760` | `P332` | Identifiable decorated U. |
| 3 | `000` | rowspan of terminal `P000` | Damaged, sign-bearing slot; identity unresolved. |
| 4 | `002` | rowspan of terminal `P000` | Recoverable two-stroke graphic. |
| 5 | `000` | rowspan of terminal `P000` | Second damaged, sign-bearing slot; identity unresolved. |
| 6 | `350` | rowspan of terminal `P000` | Recoverable terminal branched graphic. |

The Lipi record is `+740-760-000-002-000-350+`, with `text length=6`, `signs=4`, `complete=N`, and `condition=Poor`. Here `signs=4` is the count of identified numeric signs, not the structural length.

Mayig records `P324 P332 P000`. Its pinned `P000` definition is “a section of significant damage or lost material,” and this occurrence stores `percent_lost=70`. `P000` therefore covers the four-position damaged remainder after `P332`; it is not equivalent to either Lipi `000` and its array position is not a third sign.

## Accepted normalization

- Use six structural positions: four identified graphics plus two `<UNK_SIGN>` positions.
- Keep the two unknown positions distinct because the recoverable `002` separates them.
- Attach Mayig's `P000` and 70% loss value to positions 3–6 as span-level damage metadata.
- Exclude `P000` from sign counts, sign frequencies, and model token sequences.
- Do not infer identities for either Lipi `000`, and do not treat the apparent Mayig `P332-P000` transition as a sign adjacency.
- The source supports preserved order and six slots, but not the missing graphics' internal features.

## Research consequence

The `complex_manual_collation` class closes at `1/1`. `M-106` can re-enter length- and order-sensitive structural analyses only with the two explicit unknown slots retained and the four-position damage span carried separately. Treating Mayig's three array entries as a sign count would erase two recoverable signs and two separately located unknown positions.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved evidence

- CISI 1 panel: `research/data/sign_crosswalk/source_panels/m106_damage_span/M-106_A_a_CISI1_pdf75_print39.png`, SHA-256 `6A1B95E2417F0887319F5E3286EE1942712C390B01209D92BD3CD2B996F5A086`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi metadata SHA-256: `B3E2A94EFDF70EAA893BBBBD35FD057B53F766C82823A3EFB8EE37F9365311FE`.
- Mayig `m106.json` SHA-256: `019F67C4406323578FC082F79C251933089FF3E8AAD285A9CDA84E3FFB289C5D`; pinned Git blob `075bc67b7a6ca9e1aecf372dc767f24c1f03107e`.
- Mayig `P000.json` SHA-256: `6F6B7ECC5D2DB2D6F317CDBBC3B4E24F4DC412C891554405E9312A0B8204467A`.
