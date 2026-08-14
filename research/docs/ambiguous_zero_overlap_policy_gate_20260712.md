# Lipi 000 and Mayig P000 overlap policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `LIPI_000_AND_MAYIG_P000_COLOCATE_AS_ONE_DAMAGED_UNKNOWN_SIGN_SLOT_ON_M55_M60`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. This gate covers two objects, `M-55` and `M-60`.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `760`, and it uses `000` for a sign it cannot identify. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P332`, and it uses `P000` to mark a stretch of lost or damaged material. The two catalogues disagree on how many units each object has, and the disagreement has to be resolved before either row can be used.

## Question

On `M-55` and `M-60`, the arithmetic worked out two different ways: counting Lipi `000` as a sign reconciled the corpus counts, and so did excluding Mayig `P000`. That is why these rows were ambiguous. On both objects the two tokens sit at the same sequence position. So the live question was whether they represented separate events, an empty damage span with no sign in it, or two attributes of one damaged sign slot.

## Source-visible decisions

A panel is a labeled crop rendered from the published plate, kept as a file so anyone can recheck the reading later. Each row below records what the plate actually shows.

| Object | Corpus records | CISI observation | Decision |
| --- | --- | --- | --- |
| `M-55` | Lipi `+000-760-463-510-001-692+`, length 6, signs 5; Mayig `P000 P332 P215 P275 P121 P256`, with `P000` loss 10% | PDF page 61 / printed page 25 shows five complete units and a distinct partial trace at the chipped initial boundary in both mirrored views. | One damaged unknown initial sign slot. Lipi preserves its structural occupancy; Mayig records damage at the same slot. |
| `M-60` | Lipi `+151-000+`, length 2, signs 1; Mayig `P001 P000`, with `P000` loss 40% | PDF page 63 / printed page 27 shows the complete `151/P001` unit plus an isolated partial stroke at the opposite side in the mirrored view. | One damaged unknown terminal sign slot. `151` is not terminal. |

The CISI 1 PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

## Accepted normalization policy

The answer is the third option: one damaged sign slot, described twice. Where Lipi `000` and Mayig `P000` land on the same position, build one normalized slot that carries both descriptions:

```text
structural_token = <DAMAGED_UNK_SIGN>
structural_count = 1
lipi_identity = 000
mayig_damage = P000
percent_lost = source value
```

- Do not count Lipi `000` and Mayig `P000` as two units. They describe one slot.
- Do not drop the Lipi slot. The source preserves a bounded partial trace there, and the sequence needs that position.
- Do not promote Mayig `P000` into a graphic sign identity. It supplies missingness metadata for a slot that the source and Lipi already establish on their own.
- When Mayig `P000` has no independent evidence for a sign slot behind it, keep it as a non-counting damage-span event under the separate P000 policy.
- Leave `<DAMAGED_UNK_SIGN>` out of any analysis that needs to know which sign it is. Keep it in models of length, order, boundary, adjacency, and missingness, where an unidentified slot still carries information.

## Research consequence

The `ambiguous_unknown_policy_reconciles` class has only two members, and both have now been checked against the source, so the class is closed at `2/2`.

- `M-55` has six structural slots. `760` is not initial.
- `M-60` has two structural slots. `151` is not terminal.
- Both rows can go back into source-count and stored-order analyses, carrying one damaged unknown token with a damage percentage attached.
- Nothing here adds a sign identity, a global crosswalk edge, a value, a meaning, a phonetic reading, a language identification, a translation, or a decipherment claim.

## Preserved evidence

Each file below is listed with its SHA-256 hash so a later reader can confirm the exact bytes that this decision was made from.

- `research/data/sign_crosswalk/source_panels/ambiguous_zero_overlap_policy/M-55_A_a_CISI1_pdf61_print25.png`, SHA-256 `11DA3AE0084C3EB9190F8C2260EBEA53F2E86AE30C5ACF585C9609CEE977AEA1`.
- `research/data/sign_crosswalk/source_panels/ambiguous_zero_overlap_policy/M-60_A_a_CISI1_pdf63_print27.png`, SHA-256 `BC4F43233726551E3D81A3A85498E3DA08E9456388B5B46D4E0F6FAE6EA3BD04`.
- Mayig `m055.json`: `49D47058F4AF2916AC175E0DC076B912092A2782190233E4C05DC550C58F2C6E`.
- Mayig `m060.json`: `27DA9FF80A3C8B9598D974E1D52AF41784E5F50F96C229E1445A8B2D4734562A`.
