# M-110 P000 damage-span policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `P000_IS_A_NONSIGN_DAMAGE_SPAN_RETAIN_AS_EVIDENCE_EXCLUDE_FROM_RECOGNIZED_SIGN_COUNT`.

## Direct evidence

- CISI 1 PDF page 75 / printed page 39 shows both `M-110 A` and `M-110 a`. The PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- The two published views preserve two identifiable signs at the right of the reading-order sequence and a broken inscription stretch to their left. The plate does not independently resolve the number of originally occupied sign slots inside that lost stretch.
- Lipi row `2637.1` stores `+000-000-002-817+`, reports `text length = 4`, and reports `signs = 2`.
- Mayig snapshot `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb` stores `P000 P122 P385` for `M-110A`. Its `P000` feature record defines the token as a section of significant damage or lost material and supplies `percent_lost`, rather than a graphic sign identity.

## Count-policy correction

`P000` is not a third source sign and should not be counted as one. It is also not disposable noise. It records the damaged span that Mayig compresses into one sentinel while Lipi represents the same span as two unresolved `000` positions.

For M-110:

- recognized-sign count is `2`;
- Mayig grapheme-array length `3` is a mixed token count, not a structural sign count;
- preserve `P000` as a non-sign damage-span event in provenance-aware alignment;
- exclude `P000` from recognized-sign counts and sign-frequency/model inputs;
- align that event only to the object-level Lipi gap `000-000`, never one-to-one to either `000`;
- retain Lipi's two unknown slots as its explicit reconstruction, but do not claim that the surviving CISI plate independently proves a four-sign original.

The mismatch is therefore a schema difference, not evidence that one corpus saw an extra sign. The queue proposal `drop_mayig_P000` is acceptable only as a derived counting operation after the damage-span event has been preserved separately; deleting it from the source record would erase real missingness evidence.

## Boundaries

The two preserved signs support only the existing object-bound positional comparison `002/P122` and `817/P385`. Neither edge is promoted globally: `002/P122` is conflicted, and `{817,861}/P385` remains a feature-policy merge. No sign identity is assigned to either `000`, and no value, meaning, reading, language identification, translation, or decipherment claim is added.

Source panel: `research/data/sign_crosswalk/source_panels/m110_p000_damage_span/M-110_A_a_CISI1_pdf75_print39.png`, SHA-256 `B22D7D69DB5287B8D26DED730029139721BB76AD51BDED65761CD638A551EDCF`.

Pinned raw-record hashes:

- Mayig `m110.json`: `8357E870199F4FC37B0A068A1F32882937DEDCA9EA00A0A6CF2F4E6F4B76F6C1`.
- Mayig `P000.json`: `6F6B7ECC5D2DB2D6F317CDBBC3B4E24F4DC412C891554405E9312A0B8204467A`.
