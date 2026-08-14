# Lipi 000 sign-bearing policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `LIPI_000_IS_A_SIGN_BEARING_UNKNOWN_SLOT_IN_ALL_FOUR_FLAGGED_ROWS`.

## Question

The mismatch queue proposed counting Lipi `000` as a sign for `M-105`, `M-27`, `M-61`, and `M-62`. The source question was whether each `000` occupies a bounded graphic slot or instead marks damage, empty space, or uncertainty outside the inscription.

The complete four-object class is now source-inspected. Every stored `000` occupies one visible structural unit. Lipi's `signs` field counts recognized numeric identities, not all source-visible units, on these rows.

## Source-visible decisions

| Object | Lipi | Same-position Mayig evidence | CISI observation | Decision |
| --- | --- | --- | --- | --- |
| `M-105` | `+000-000-803-231-742-060-920+`; length 7; signs 5 | positions 1-2 are `P324 P324` | PDF page 75 / printed page 39 shows seven bounded units, including two distinct opening jar-form units. | Both `000` tokens count as sign-bearing unknown slots. |
| `M-27` | `+565-235-803-741-702-900-000+`; length 7; signs 6 | position 7 is `P123` | PDF page 52 / printed page 16 shows seven bounded units in both views. | Terminal `000` is a real seventh sign. `900` is penultimate, not terminal. |
| `M-61` | `+740-000-231-220-455-615-689+`; length 7; signs 6 | position 2 is `P251` | PDF page 64 / printed page 28 shows seven bounded positions despite poor preservation. | Internal `000` is one damaged but sign-bearing unit. |
| `M-62` | `+226-032-741-550-000-551+`; length 6; signs 5 | position 5 is `P310` | PDF page 64 / printed page 28 shows six bounded units in both views. | Penultimate `000` is a real sign; `551` remains terminal. |

The CISI 1 PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

## Accepted normalization policy

- Type each Lipi `000` as `unknown_graphic_sign`, not damage metadata.
- Count each occurrence as one structural unit.
- Preserve it as an explicit `<UNK_SIGN>` position in order-, adjacency-, length-, and terminality-sensitive analyses.
- Exclude it only from analyses requiring a resolved numeric sign identity.
- Do not replace a Lipi `000` with its same-position Mayig ID. The four objects map `000` to different Mayig signs (`P324`, `P123`, `P251`, and `P310`), proving that `000` is an unknown-identity sentinel rather than a crosswalkable sign number.
- Do not use Lipi's `signs` field as the structural count when `000` occurs; use the stored text length after source validation.

This policy is deliberately distinct from Mayig `P000`: Lipi `000` occupies a graphic sign slot, while Mayig `P000` records a non-sign damage span.

The two layers can co-locate. On `M-55` and `M-60`, source-visible partial traces establish one damaged Lipi unknown-sign slot while same-position Mayig `P000` supplies its missingness attributes; the normalized slot counts once.

## Research consequence

The full `lipi_unknown_zero_explains_count` class is closed at `4/4` source-inspected objects.

- All four rows can re-enter analyses requiring source-visible count and order if `000` remains an unresolved sign token.
- M-27 must not support terminal claims for `900`; the source-visible terminal is the unknown sign after it.
- M-105's two opening unknown units must not be collapsed, dropped, or rewritten as `740` from their Mayig form.
- No global Lipi-Mayig edge is promoted, and no sign identity is assigned to any `000`.
- No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved evidence

M-105's two object panels, full source page, manifest, and position concordance remain under `research/data/sign_crosswalk/source_panels/m105_unknown_policy/` and `research/data/sign_crosswalk/m105_source_position_concordance_20260712.csv`.

- `research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/M-27_A_a_CISI1_pdf52_print16.png`, SHA-256 `022187F98CBE48D900C3686A592A4359459F776C3F63021A926008601012AB93`.
- `research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/M-61_A_a_CISI1_pdf64_print28.png`, SHA-256 `4FCC19A57BB9AA414A3E96001B48E973D18B88C70120EE3D965481D0DBEE910C`.
- `research/data/sign_crosswalk/source_panels/lipi_000_sign_bearing_policy/M-62_A_a_CISI1_pdf64_print28.png`, SHA-256 `2A3E5468EEA097D90A4671C92D9153F5F7FF1156B42820E2F2655C5E2F0F3C9E`.
- Mayig `m105.json`: `33D17D44BE46F313DDE9DCF4FBAE8C64C2E872E343E478C3E329CEA2BA3BBC34`.
- Mayig `m027.json`: `E795493183D7670DE19638C766D2F371142D4A6DE600C8E47F446847ACA89F89`.
- Mayig `m061.json`: `074F6B6A46ED5691F4DE8FF6DC2FE43AC2E0838A4126D8FA47DE3AF80751C9AA`.
- Mayig `m062.json`: `FF0FB6909E912390553BD498982F4E6BE67C6C2A98DC7F47545D19E735660404`.
