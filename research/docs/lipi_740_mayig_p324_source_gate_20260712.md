# Lipi 740 / Mayig P324 source gate

Date: 2026-07-12 America/Los_Angeles

Decision: `EXACT_NAMESPACE_EDGE_ACCEPTED_FOR_ANALYSIS`.

Scope: `lipi_numeric:740 <-> mayig_p:P324` only.

This is a grapheme-namespace crosswalk, not a sign meaning, reading, phonetic value, language identification, translation, or license to import every identifier attached to P324 in Mayig metadata.

## Prior pressure

The pinned positional-alignment table contains `73` aligned `740/P324` positions, `0` counterexamples, and top share `1.000000`. Before this gate the edge remained uncertain because none of those rows had a durable source-panel review.

## Three source-visible witnesses

The local CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

| Object | CISI page | Lipi sequence | Mayig sequence | Matched position |
| --- | --- | --- | --- | ---: |
| M-15 A | PDF 47 / printed 11 | `090 740 176 002 861` | `P013 P324 P194 P122 P385` | 2 |
| M-21 A | PDF 49 / printed 13 | `350 001 740 362 692 032 002 861` | `P091 P121 P324 P272 P256 P145 P122 P385` | 3 |
| M-29 A | PDF 52 / printed 16 | `740 055 240 235 806 002 220 455 503` | `P324 P142 P062 P060 P364 P122 P050 P221 P210` | 1 |

The rendered panels preserve the complete seal and printed object label. All three inscriptions are readable enough to confirm the stored sign count/order and the handled-jar graphic at the aligned position. They deliberately do not add interpretive token boxes or text overlays.

Final panels:

- `research/data/sign_crosswalk/source_panels/740_P324/M-15_A_CISI1_pdf47_print11.png`
- `research/data/sign_crosswalk/source_panels/740_P324/M-21_A_CISI1_pdf49_print13.png`
- `research/data/sign_crosswalk/source_panels/740_P324/M-29_A_CISI1_pdf52_print16.png`
- `research/data/sign_crosswalk/source_panels/740_P324/manifest.csv`

## Pinned Mayig evidence

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `features/P324.json` describes P324 as the classic jar symbol with two horizontal handles.
- `m015.json`, `m021.json`, and `m029.json` place P324 at the same stored positions as Lipi 740 on the same named objects.
- The local Mayig tree manifest pins the P324 feature blob as `01932f05bc88be9edc3d26d81be33a9b70eb591c`.

The earlier sign-policy sensitivity run preserved the structural result under the full observed Lipi-to-Mayig policy. This satisfies the protocol's held-out stability condition without treating a smaller vocabulary as proof of a mapping.

## Why exact is now justified

The protocol requires at least two evidence types. This edge now has:

1. same-artifact, same-length, same-position agreement across 73 aligned positions with no counterexample;
2. three independent, labeled source panels spanning initial and medial positions;
3. a pinned Mayig graphemic feature description consistent with the visible handled-jar form;
4. prior held-out policy-sensitivity evidence showing the crosswalk policy preserves structural prediction.

The source panels close the former `needs_image_or_authoritative_sign_list_validation` blocker for this exact namespace pair.

## Namespace guards

Mayig also attaches `V204`, `V526`, `W740`, and `M342` to P324. Those are mediated Mayig metadata, not primary Parpola, Wells, or Mahadevan table checks. This gate does not promote them.

It also does not promote any other Lipi-to-Mayig edge from the same three objects. Each edge needs its own counterexample and namespace review.

## Accepted state

- Mapping state: `exact`.
- Confidence: `high` for the bounded Lipi/Mayig P namespace edge.
- Accepted for structural analysis: `true`.
- Accepted sign meaning: `false`.
- Accepted phonetic value: `false`.
- Accepted translation: `false`.
- Accepted-count increment in the decipherment claim ledger: `0`.
