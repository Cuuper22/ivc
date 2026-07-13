# Mayig P000 damage-span policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `P000_UNIFORMLY_NONSIGN_DAMAGE_SPAN_IN_ALL_THREE_FLAGGED_ROWS`.

## Question

The mismatch queue proposed dropping Mayig `P000` to reconcile counts for `M-110`, `M-126`, and `M-73`. The source question was whether `P000` represented an additional bounded sign, disposable padding, or a different record type embedded in Mayig's grapheme array.

Mayig's pinned `P000` feature record defines it as a section of significant damage or lost material and supplies `percent_lost`. It carries no graphic identity. The CISI plates confirm that definition across the complete three-object queue class.

## Source-visible decisions

| Object | Lipi | Mayig | CISI observation | Count decision |
| --- | --- | --- | --- | --- |
| `M-110` | `+000-000-002-817+`; text length 4; signs 2 | `P000 P122 P385`; `P000` loss 50% | PDF page 75 / printed page 39 preserves two identifiable signs plus a broken inscription stretch. The plate cannot recover how many signs originally occupied the lost stretch. | Two recognized signs. `P000` is the lost span, not a third sign. Lipi's two `000` slots remain its reconstruction, not a source-proven four-sign original. |
| `M-126` | `+520-552-060-692+`; text length 4; signs 4 | `P000 P230 P234 P120 P256`; `P000` loss 10% | PDF page 78 / printed page 42 shows four bounded signs in both published views and edge damage, with no fifth glyph. | Four signs. The count mismatch is resolved after typing `P000` as damage metadata. |
| `M-73` | `+400-520-897+`; text length 3; signs 3 | `P098 P217 P181 P000`; `P000` loss 20% | PDF page 68 / printed page 32 shows three bounded signs in both views and a chipped terminal edge, with no fourth glyph. | Three signs. The count mismatch is resolved after typing `P000` as damage metadata. |

The CISI 1 PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

## Accepted normalization policy

- Type `P000` as `damage_span`, not `graphic_sign`.
- Exclude `P000` from sign counts, sign frequencies, and model token sequences.
- Preserve its sequence position and `percent_lost` in a parallel damage/missingness layer.
- Do not assume a one-to-one relation from the token names. On `M-110`, `P000` aligns only to the object-level lost region represented by Lipi's `000-000` gap, not to either slot individually.
- Where source traces and a same-position Lipi `000` independently establish one damaged sign slot (`M-55`, `M-60`), attach the `P000` damage attributes to that slot without counting `P000` separately.
- Treat Mayig grapheme-array length as a mixed-token count whenever `P000` occurs.

The queue operation `drop_mayig_P000` is therefore valid only as a derived sign-count transformation. Deleting `P000` from the source record would erase real damage evidence.

## Research consequence

The full `mayig_unknown_p000_explains_count` class is closed at `3/3` source-inspected objects.

- `M-126` and `M-73` can re-enter analyses that require preserved-sign count and order after carrying their damage flags separately.
- `M-110` can enter recognized-subsequence analyses, but remains excluded from analyses requiring complete original length, terminality, or position across its lost span.
- No global sign crosswalk is promoted. In particular, `002/P122` remains conflicted and `{817,861}/P385` remains a feature-policy merge.
- No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved panels and raw hashes

- `research/data/sign_crosswalk/source_panels/p000_damage_span_policy/M-110_A_a_CISI1_pdf75_print39.png`, SHA-256 `B22D7D69DB5287B8D26DED730029139721BB76AD51BDED65761CD638A551EDCF`.
- `research/data/sign_crosswalk/source_panels/p000_damage_span_policy/M-126_A_a_CISI1_pdf78_print42.png`, SHA-256 `523AE2A6CE318B47BE727DED0E3CF7845E29515BCAF9CB09E9301B0634D26104`.
- `research/data/sign_crosswalk/source_panels/p000_damage_span_policy/M-73_A_a_CISI1_pdf68_print32.png`, SHA-256 `40BBE9119E21BA097689123D029867C5217E55F3F28160AA166B2F824F70ACFD`.
- Mayig `m110.json`: `8357E870199F4FC37B0A068A1F32882937DEDCA9EA00A0A6CF2F4E6F4B76F6C1`.
- Mayig `m126.json`: `0676BDB606F468FC3511BAA4176C90E47D67F758DFDFA88DA26386270AA1F41B`.
- Mayig `m073.json`: `967E4B3AA9B61F675BE6928C01CFD3A3F8987FB57F85ED94514173A895BABDF4`.
- Mayig `P000.json`: `6F6B7ECC5D2DB2D6F317CDBBC3B4E24F4DC412C891554405E9312A0B8204467A`.
