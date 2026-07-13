# Lipi 000 and Mayig P000 overlap policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `LIPI_000_AND_MAYIG_P000_COLOCATE_AS_ONE_DAMAGED_UNKNOWN_SIGN_SLOT_ON_M55_M60`.

## Question

`M-55` and `M-60` were ambiguous because either counting Lipi `000` or excluding Mayig `P000` reconciled the corpus counts. On both objects the tokens occupy the same sequence position. The live question was whether they represented separate events, an empty damage span, or two attributes of one damaged sign slot.

## Source-visible decisions

| Object | Corpus records | CISI observation | Decision |
| --- | --- | --- | --- |
| `M-55` | Lipi `+000-760-463-510-001-692+`, length 6, signs 5; Mayig `P000 P332 P215 P275 P121 P256`, with `P000` loss 10% | PDF page 61 / printed page 25 shows five complete units and a distinct partial trace at the chipped initial boundary in both mirrored views. | One damaged unknown initial sign slot. Lipi preserves its structural occupancy; Mayig records damage at the same slot. |
| `M-60` | Lipi `+151-000+`, length 2, signs 1; Mayig `P001 P000`, with `P000` loss 40% | PDF page 63 / printed page 27 shows the complete `151/P001` unit plus an isolated partial stroke at the opposite side in the mirrored view. | One damaged unknown terminal sign slot. `151` is not terminal. |

The CISI 1 PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

## Accepted normalization policy

For these same-position overlaps, construct one normalized slot:

```text
structural_token = <DAMAGED_UNK_SIGN>
structural_count = 1
lipi_identity = 000
mayig_damage = P000
percent_lost = source value
```

- Do not count Lipi `000` and Mayig `P000` as two units.
- Do not drop the Lipi slot; the source preserves a bounded partial trace and the sequence requires its position.
- Do not promote Mayig `P000` into a graphic sign identity; it supplies missingness metadata for the slot established independently by the source and Lipi.
- When Mayig `P000` lacks independent evidence for a sign slot, retain it as a non-counting damage-span event under the separate P000 policy.
- Exclude `<DAMAGED_UNK_SIGN>` from identity-specific analyses, but retain it in length, order, boundary, adjacency, and missingness-aware models.

## Research consequence

The complete `ambiguous_unknown_policy_reconciles` class is closed at `2/2` source-inspected objects.

- `M-55` has six structural slots. `760` is not initial.
- `M-60` has two structural slots. `151` is not terminal.
- Both rows can re-enter source-count and stored-order analyses with one damaged unknown token and an attached damage percentage.
- No sign identity, global crosswalk, value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/ambiguous_zero_overlap_policy/M-55_A_a_CISI1_pdf61_print25.png`, SHA-256 `11DA3AE0084C3EB9190F8C2260EBEA53F2E86AE30C5ACF585C9609CEE977AEA1`.
- `research/data/sign_crosswalk/source_panels/ambiguous_zero_overlap_policy/M-60_A_a_CISI1_pdf63_print27.png`, SHA-256 `BC4F43233726551E3D81A3A85498E3DA08E9456388B5B46D4E0F6FAE6EA3BD04`.
- Mayig `m055.json`: `49D47058F4AF2916AC175E0DC076B912092A2782190233E4C05DC550C58F2C6E`.
- Mayig `m060.json`: `27DA9FF80A3C8B9598D974E1D52AF41784E5F50F96C229E1445A8B2D4734562A`.
