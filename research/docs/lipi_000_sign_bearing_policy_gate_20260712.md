# Lipi 000 sign-bearing policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `LIPI_000_IS_A_SIGN_BEARING_UNKNOWN_SLOT_IN_ALL_FOUR_FLAGGED_ROWS`.

## What this is and why it exists

This gate settles what the token `000` means in the Lipi catalogue. A gate is a written decision checked against the source images, so that later work does not relitigate the same question.

Lipi writes each sign as a number. `000` is what it writes when a sign is there but it cannot say which sign. The trouble is that a zero can be read two ways: as a real position holding an unidentified mark, or as a note that something is absent. Those readings give different sign counts for the same object, which is exactly why four rows were stuck in the mismatch queue, the running list of objects where Lipi and the Mayig catalogue disagree on how many units an inscription has.

## Question

The mismatch queue proposed counting Lipi `000` as a sign for `M-105`, `M-27`, `M-61`, and `M-62`. The source question was whether each `000` sits in a bounded graphic slot, or instead marks damage, empty space, or uncertainty lying outside the inscription.

All four objects in the class have now been inspected against the source. Every stored `000` occupies one visible structural unit. The reason the counts looked wrong is that Lipi's `signs` field tallies only the signs it could name; on these rows it is smaller than the number of units actually visible on the object.

## Source-visible decisions

Each row records what the published plate shows at the disputed position.

| Object | Lipi | Same-position Mayig evidence | CISI observation | Decision |
| --- | --- | --- | --- | --- |
| `M-105` | `+000-000-803-231-742-060-920+`; length 7; signs 5 | positions 1-2 are `P324 P324` | PDF page 75 / printed page 39 shows seven bounded units, including two distinct opening jar-form units. | Both `000` tokens count as sign-bearing unknown slots. |
| `M-27` | `+565-235-803-741-702-900-000+`; length 7; signs 6 | position 7 is `P123` | PDF page 52 / printed page 16 shows seven bounded units in both views. | Terminal `000` is a real seventh sign. `900` is penultimate, not terminal. |
| `M-61` | `+740-000-231-220-455-615-689+`; length 7; signs 6 | position 2 is `P251` | PDF page 64 / printed page 28 shows seven bounded positions despite poor preservation. | Internal `000` is one damaged but sign-bearing unit. |
| `M-62` | `+226-032-741-550-000-551+`; length 6; signs 5 | position 5 is `P310` | PDF page 64 / printed page 28 shows six bounded units in both views. | Penultimate `000` is a real sign; `551` remains terminal. |

The CISI 1 PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

## Accepted normalization policy

- Type each Lipi `000` as `unknown_graphic_sign`. It is a sign, not damage metadata.
- Count each occurrence as one structural unit.
- Keep it as an explicit `<UNK_SIGN>` position wherever order, adjacency, length, or terminality matters. The slot's position is known even though its identity is not.
- Leave it out only of analyses that need a resolved numeric sign identity.
- Do not swap a Lipi `000` for the Mayig ID sitting at the same position. Across these four objects, `000` lands on four different Mayig signs: `P324`, `P123`, `P251`, and `P310`. That spread is the proof that `000` is a placeholder meaning "identity unknown", not a sign number that can be crosswalked.
- Do not use Lipi's `signs` field as the structural count when `000` occurs. Use the stored text length, once the source has confirmed it.

Keep this policy separate from the one for Mayig `P000`, which looks similar and is not. Lipi `000` occupies a graphic sign slot. Mayig `P000` records a damage span with no sign in it.

The two can still land on the same spot. On `M-55` and `M-60`, partial traces visible in the source establish one damaged Lipi unknown-sign slot, and the Mayig `P000` at that position supplies how much of it is missing. The normalized slot counts once, not twice.

## Research consequence

The `lipi_unknown_zero_explains_count` class is closed at `4/4` source-inspected objects.

- All four rows can go back into analyses that need source-visible count and order, as long as `000` stays an unresolved sign token rather than being filled in.
- M-27 cannot be used to claim `900` is terminal. The source-visible terminal is the unknown sign that follows it.
- M-105's two opening unknown units must not be collapsed together, dropped, or rewritten as `740` on the strength of their Mayig form.
- No global Lipi-Mayig edge is promoted, and no `000` is assigned a sign identity.
- Nothing here adds a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

M-105's two object panels, full source page, manifest, and position concordance remain under `research/data/sign_crosswalk/source_panels/m105_unknown_policy/` and `research/data/sign_crosswalk/m105_source_position_concordance_20260712.csv`.

- `research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/M-27_A_a_CISI1_pdf52_print16.png`, SHA-256 `022187F98CBE48D900C3686A592A4359459F776C3F63021A926008601012AB93`.
- `research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/M-61_A_a_CISI1_pdf64_print28.png`, SHA-256 `4FCC19A57BB9AA414A3E96001B48E973D18B88C70120EE3D965481D0DBEE910C`.
- `research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/M-62_A_a_CISI1_pdf64_print28.png`, SHA-256 `2A3E5468EEA097D90A4671C92D9153F5F7FF1156B42820E2F2655C5E2F0F3C9E`.
- Mayig `m105.json`: `33D17D44BE46F313DDE9DCF4FBAE8C64C2E872E343E478C3E329CEA2BA3BBC34`.
- Mayig `m027.json`: `E795493183D7670DE19638C766D2F371142D4A6DE600C8E47F446847ACA89F89`.
- Mayig `m061.json`: `074F6B6A46ED5691F4DE8FF6DC2FE43AC2E0838A4126D8FA47DE3AF80751C9AA`.
- Mayig `m062.json`: `FF0FB6909E912390553BD498982F4E6BE67C6C2A98DC7F47545D19E735660404`.
