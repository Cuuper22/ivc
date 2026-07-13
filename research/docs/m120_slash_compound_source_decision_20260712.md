# M-120 slash-compound source decision

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SIX_UNIT_SEQUENCE_TREATS_858_SLASH_740_AS_ONE_COMPOUND_SLOT`.

## Direct evidence

- CISI 1 PDF page 77, printed page 41, labels both `M-120 A` and `M-120 a`. The source PDF SHA-256 is `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Both the impression and seal views show six independently bounded inscription units.
- Lipi row `2647.1` stores `+858/740-100-585-741-840-346+`. It has six hyphen-delimited slots but reports `text length=7` and `signs=7` because the first slash compound is counted as two numeric components.
- Mayig `M-120A` stores six graphemes: `P324 P009 P288 P325 P349 P044`.

## Object-bound concordance

| Source slot | Lipi | Mayig | Source decision |
| ---: | --- | --- | --- |
| 1 | `858/740` | `P324` | One bounded jar-family glyph. Preserve the Lipi compound token; do not split it into sequential `858`, `740` signs or reduce it to `740`. |
| 2 | `100` | `P009` | Same-object positional match only. |
| 3 | `585` | `P288` | Same-object positional match only. |
| 4 | `741` | `P325` | Same-object positional match only. |
| 5 | `840` | `P349` | Same-object positional match only. |
| 6 | `346` | `P044` | Same-object positional match only. |

M-120's source-visible structural count is six. The Lipi fields `text length=7` and `signs=7` are component-count metadata for this row, not a literal count of sequential source units. M-120 may enter analyses that require only source-unit count if `858/740` remains an atomic compound token. It remains excluded from analyses that require resolved numeric sign identity at slot 1.

This decision does not accept `858/740 = P324`, any global crosswalk edge, a sign value, meaning, reading, language identification, or translation.

## Source panels

- `research/data/sign_crosswalk/source_panels/m120_slash_compound/M-120_impression_A_CISI1_pdf77_print41.png`, SHA-256 `D505326F02DEE47DF46F58C17D78B0EE609B152F00A712B779C7C2BD89DD68C4`.
- `research/data/sign_crosswalk/source_panels/m120_slash_compound/M-120_seal_a_CISI1_pdf77_print41.png`, SHA-256 `412CD6C4EFF9F3E9908412A416F86723F2AE89E3505AFA15B601BA631D6C5433`.

