# M-141 multiline damage-span gate

Date: 2026-07-12 America/Los_Angeles

Decision: `M141_TEN_IS_A_CATALOGUE_RECONSTRUCTION; SOURCE_HAS_SEVEN_BOUNDED_POSITIONS_PLUS_A_LOST_SPAN_OF_UNKNOWN_CAPACITY; SLASH_IS_A_ROW_BREAK`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. This gate covers one object, `M-141`, which is both broken and written on two rows.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `817`, uses `000` for a sign slot it cannot identify, and uses a slash for a relation other than plain succession. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P122`, and uses `P000` for a damage span — one stretch of lost surface, however many signs used to sit in it.

The trap on this object is that a broken stretch has no natural sign count. You can see that material is gone. You usually cannot see how much. A catalogue that writes three zeros there is proposing a number, not reading one, and that proposal must not be laundered into a source-supported count.

## Question

`M-141` is the remaining `multi_sign_count_disagreement` row, from the queue of objects whose two catalogue rows give different lengths. Lipi records `+817-255-636/000-000-000-240-002-031-000+`, with text length 10 and six identified signs. Mayig records only `P000 P122 P000`. The source question was whether either catalogue length is a source-supported sign count, and whether Lipi's slash denotes a compound or a physical layout boundary.

## Source-visible layout

CISI 1 PDF page 81 / printed page 45, in both `M-141 A` and `M-141 a`, shows two inscription rows. In image-left-to-right order:

- Lower row: `817 255 636`.
- Upper row: a broad destroyed span, then identifiable `240`, `002`, and `031`, followed by one damaged terminal sign position.

So the slash is a row break after the three-sign lower row. It does not fuse `636` with the following material, and it does not create a cross-row sign adjacency.

The two kinds of damage on this object behave differently. The lower row and the `240-002-031` upper-row suffix are individually visible. The terminal damage occupies roughly one sign position, so it supports one `<UNK_SIGN>`. The three consecutive Lipi zeros before `240` are another matter: they lie inside one continuous destroyed span, and the plate does not independently bound three positions there. Lipi's ten-slot representation is therefore a catalogue reconstruction, not a source-preserved count.

## Mayig alignment

Mayig stores `P000(40) P122 P000(10)`, with all three entries assigned to line 1 and no entry for the lower row. Its damage spans are coarser than Lipi's zeros, and they swallow visible signs:

| Source region | Lipi | Mayig | Decision |
| --- | --- | --- | --- |
| Lower row | `817 255 636` | absent | Three source-visible signs omitted by Mayig. |
| Upper row before `002` | `000 000 000 240` | `P000(40)` | One unbounded loss span followed by source-visible `240`; Mayig's span swallows the visible sign as well as the break. |
| Upper `002` | `002` | `P122` | Object-local positional match to the visible two-stroke sign. No global `002/P122` edge is promoted. |
| Upper row after `002` | `031 000` | `P000(10)` | Preserve visible `031`; attach the damage metadata to the bounded terminal unknown. Mayig omits `031`. |

`P000` remains non-sign damage metadata. Neither occurrence contributes a structural sign count, and neither is equivalent to a Lipi `000` token.

## Accepted normalization

Keep the two rows apart, and keep the unbounded loss span honest about not knowing its own size:

```text
lower: [817, 255, 636]
upper: [<LOSS_SPAN capacity=unknown>, 240, 002, 031, <UNK_SIGN>]
```

- Six sign identities and one bounded terminal unknown are source-supported.
- The lost span has unknown sign capacity. Lipi proposes three positions, but the plate does not establish that count.
- The minimum directly located sign count is seven; the complete original total remains indeterminate.
- Keep Lipi length 10 only in a catalogue-reconstruction lane with its first three upper-row zeros marked inferred.
- Exclude M-141 from complete-length, complete-order, and adjacency analyses that cross the loss span or row break.
- The intact lower row and the upper `240-002-031-<UNK_SIGN>` suffix may be used as separate source-supported row-local sequences.
- Do not treat Mayig array length 3, either `P000` transition, or Lipi's `636/000` boundary as sign-level evidence.

## Research consequence

The `multi_sign_count_disagreement` class is adjudicated at `2/2`, but its two objects land in different places. M-7 receives a source-supported compound-level count of nine. M-141 remains count-indeterminate, and is usable only through the structure preserved inside each row. The only unadjudicated class left in the 29-row mismatch queue is the four-object `damaged_boundary_fragment` class.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved evidence

Each file below is listed with its SHA-256 hash, so a later reader can confirm the exact bytes this decision was made from.

- CISI 1 panel: `research/data/sign_crosswalk/source_panels/m141_multiline_damage_span/M-141_A_a_CISI1_pdf81_print45.png`, SHA-256 `D8457BAB5EAD3CE2CDED6D95CD19FD405E77A915BBB323ED5DB521EA5AC9D73D`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi metadata SHA-256: `B3E2A94EFDF70EAA893BBBBD35FD057B53F766C82823A3EFB8EE37F9365311FE`.
- Mayig `m141.json` SHA-256: `E21284AE90A0E7285F0E2126A9E95A3A04BFBCA9D2C165645ED196F488E1FD0F`; Git blob `72fe9f1ac90d80490944178f1b1d03fbb28f1969` from pinned commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.
- Mayig `P000.json` SHA-256: `6F6B7ECC5D2DB2D6F317CDBBC3B4E24F4DC412C891554405E9312A0B8204467A`.
- Mayig `P122.json` SHA-256: `D4CE67111223322A560F6206EFE6D3FF858F6E1EDE676CB4B2FCC9787B499C68`.
