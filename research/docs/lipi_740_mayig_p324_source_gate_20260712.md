# Lipi 740 / Mayig P324 source gate

Date: 2026-07-12 America/Los_Angeles

Decision: `EXACT_NAMESPACE_EDGE_ACCEPTED_FOR_ANALYSIS`.

Scope: `lipi_numeric:740 <-> mayig_p:P324` only.

## What this is and why it exists

Lipi and Mayig are two catalogues of the same inscriptions with different sign labels: Lipi numbers like `740`, Mayig Parpola-style codes like `P324`. A crosswalk is the table saying which label matches which, and a gate is the written decision that accepts or refuses one entry after checking the source images.

This gate accepts one. `740` and `P324` are the same grapheme, both of them the jar sign with two handles. It is the only crosswalk edge in this batch marked `exact`, and it is worth being clear about how small that claim is. Saying two catalogue numbers name the same drawing is a statement about the catalogues. It says nothing about what the drawing meant.

So this is a crosswalk between catalogue namespaces. It is not a sign meaning, a reading, a phonetic value, a language identification, or a translation. It is also not permission to import every other identifier Mayig happens to attach to P324.

## Prior pressure

The pinned positional-alignment table contains `73` aligned `740/P324` positions, `0` counterexamples, and top share `1.000000`. That is perfect agreement. It still was not enough. Before this gate the edge stayed `uncertain`, because agreement between two tables can come from the two tables sharing an ancestor rather than from the object. None of the 73 rows had yet been checked against a durable source panel.

## Three source-visible witnesses

A witness is a specific object whose published image is examined to confirm the mapping holds on a real inscription. Panels are labeled crops rendered from the source PDF and kept as files, so the reading can be rechecked later.

The local CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.

| Object | CISI page | Lipi sequence | Mayig sequence | Matched position |
| --- | --- | --- | --- | ---: |
| M-15 A | PDF 47 / printed 11 | `090 740 176 002 861` | `P013 P324 P194 P122 P385` | 2 |
| M-21 A | PDF 49 / printed 13 | `350 001 740 362 692 032 002 861` | `P091 P121 P324 P272 P256 P145 P122 P385` | 3 |
| M-29 A | PDF 52 / printed 16 | `740 055 240 235 806 002 220 455 503` | `P324 P142 P062 P060 P364 P122 P050 P221 P210` | 1 |

Each panel shows the complete seal and the printed object label. All three inscriptions are legible enough to confirm the stored sign count and order, and to see the handled-jar form sitting at the aligned position. The panels carry no token boxes or text overlays, and that omission is deliberate: an overlay would show the reader the interpretation instead of letting them check it.

Final panels:

- `research/data/sign_crosswalk/source_panels/740_P324/M-15_A_CISI1_pdf47_print11.png`
- `research/data/sign_crosswalk/source_panels/740_P324/M-21_A_CISI1_pdf49_print13.png`
- `research/data/sign_crosswalk/source_panels/740_P324/M-29_A_CISI1_pdf52_print16.png`
- `research/data/sign_crosswalk/source_panels/740_P324/manifest.csv`

## Pinned Mayig evidence

Pinned means the evidence is read from one fixed commit, so the record cannot change under the decision later.

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `features/P324.json` describes P324 as the classic jar symbol with two horizontal handles.
- `m015.json`, `m021.json`, and `m029.json` place P324 at the same stored positions as Lipi 740 on the same named objects.
- The local Mayig tree manifest pins the P324 feature blob as `01932f05bc88be9edc3d26d81be33a9b70eb591c`.

An earlier sign-policy sensitivity run rebuilt the structural result under the full observed Lipi-to-Mayig policy and the result held. That satisfies the protocol's held-out stability condition. It is worth naming what that check does not show: a smaller sign vocabulary can improve a score by itself, so surviving the swap is a stability test, not proof of the mapping.

## Why exact is now justified

The protocol requires at least two kinds of evidence before an edge can be called exact. This one has four:

1. same-artifact, same-length, same-position agreement across 73 aligned positions with no counterexample;
2. three independent, labeled source panels spanning initial and medial positions;
3. a pinned Mayig graphemic feature description consistent with the visible handled-jar form;
4. prior held-out policy-sensitivity evidence showing the crosswalk policy preserves structural prediction.

The source panels clear the former `needs_image_or_authoritative_sign_list_validation` blocker, and they clear it for this namespace pair only.

## Namespace guards

Mayig also hangs `V204`, `V526`, `W740`, and `M342` on P324. Those are identifiers Mayig has copied across from other catalogues, not checks anyone here made against the primary Parpola, Wells, or Mahadevan tables. Accepting `740 <-> P324` does not accept them; a chain of second-hand equations is not evidence. This gate does not promote them.

The same caution applies within these three objects. Each of them aligns many other sign pairs, and none of those pairs is promoted here. Every edge needs its own counterexample search and its own namespace review.

## Accepted state

- Mapping state: `exact`.
- Confidence: `high` for the bounded Lipi/Mayig P namespace edge.
- Accepted for structural analysis: `true`.
- Accepted sign meaning: `false`.
- Accepted phonetic value: `false`.
- Accepted translation: `false`.
- Accepted-count increment in the decipherment claim ledger: `0`.
