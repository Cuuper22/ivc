# H-786 / H-941 415 Side Mapping Adjudication

Date: 2026-05-26

This note is an adjudication — a ruling on a disputed point of evidence. The dispute is whether two objects, `H-786` and `H-941`, actually contradict the project's local transcription, or whether the apparent contradiction came from a bad assumption about how two different labeling systems line up. The ruling matters because it decides whether those two objects can be used as evidence at all.

## Question

Do the source labels for `H-786` and `H-941` really conflict with the local exact `+520-220-415+` rows, or is the conflict an artifact of assuming local `.1/.2` row order equals CISI `A/B` side labels? (CISI is the Corpus of Indus Seals and Inscriptions; its `A/B` letters label the sides of an object as published, while the local `.1/.2` numbers are the project's own row order.)

This matters for the live `M-1206 / M-37 / 520-220-X` terminal-family branch — an open line of investigation the project is still working, as opposed to one already closed. The previous fine-form packet found target-like source panels on `H-786 A` and `H-941 A/A bis`, while the local exact rows are `.2`:

```text
H-786  1677.2  +520-220-415+
H-941  1821.2  +520-220-415+
```

The old blocker was:

```text
target-like panel is source A, but the exact local row is .2, so exact-side evidence is unresolved
```

## Source Layer Checked

Local rows:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_inputs.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_blind_review.csv
```

Source images and crops:

```text
tmp/m1206_m37_blind_visual_comparanda/cisi_pakistan_n359_h786_w2000.jpg
tmp/m1206_m37_blind_visual_comparanda/cisi_pakistan_n374_h939_h940_w2000.jpg
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/contact_sheet_415_verified_panels.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H786_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H786_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_A_bis_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_B_bis_panel.png
```

Clean comparators on the same source-page layer:

```text
H-938  1818.1  +520-220-415+  source A/A bis
H-940  1820.1  +520-220-415+  source A
```

Data-register pages checked after the first adjudication:

```text
tmp/cisi_pakistan_pages/data_h786_h941/page-478.png
tmp/cisi_pakistan_pages/data_h786_h941/page-479.png
tmp/cisi_pakistan_pages/data_h786_h941/page478_h786_h800_wide_enlarged.png
tmp/cisi_pakistan_pages/data_h786_h941/page479_h938_h943_enlarged.png
```

These pages do not close the sign-string side mapping. They do sharpen the source layer:

```text
H-786 data row: one register entry, accession/object id 13178, catalogue reference AV 775. No side-specific sign string is given.
H-941 data row: register numerals 3464 and 2703 appear before HM 480; local metadata appears to fuse this numeric material as 2703464. The source references are P 1180, A: Pl. 37:673, and B: Pl. 36:3872. No side-specific sign string is given.
```

So the CISI data register confirms that `H-941 A` and `H-941 B` are distinct physical/source references, but it still does not say which one is local `1821.1` or local `1821.2`. For `H-786`, the checked data row is even less decisive: it gives a single catalogue reference, not an A/B mapping.

## Adjudication

The side conflict is weaker than previously stated.

The visually target-like pattern in this packet is the same broad three-class side:

```text
triangular/pennant-on-stem -> split-leaf/fork -> rake/vertical-bundle
```

This appears on:

```text
H-786 A
H-938 A/A bis
H-940 A
H-941 A/A bis
```

It does not appear securely on:

```text
H-786 B
H-941 B/B bis
```

The clean same-page controls show that source `A` can be the local exact `+520-220-415+` side:

```text
H-938  local 1818.1 +520-220-415+ -> source A/A bis
H-940  local 1820.1 +520-220-415+ -> source A
```

Therefore this simple equation is not allowed:

```text
local .1 = source A
local .2 = source B
```

For `H-786` and `H-941`, the better current visual reconciliation is:

```text
H-786 source A is the candidate visual match for local .2 +520-220-415+.
H-941 source A/A bis is the candidate visual match for local .2 +520-220-415+.
```

This is not an accepted row-to-source-side mapping yet. It is a correction to the failure mode: the previous blocker assumed `.2 = B`, but the available evidence only proves that `.2` and `B` cannot be equated without an explicit source table.

## Claim Status

Accepted:

```text
Local row number and CISI side letter are not interchangeable.
The old H-786/H-941 blocker cannot be stated as ".2 means B" without external side-policy evidence.
H-786 A and H-941 A/A bis remain admissible candidate panels for the exact local +520-220-415+ row under visual row-to-side reconciliation.
```

Refined cautiously:

```text
H-786 and H-941 move from "side-mapping conflict proves A cannot be exact-side evidence" to "candidate source A exact-row mapping, still not admissible until explicit source-policy confirmation."
```

Not accepted:

```text
H-786 A equals local 1677.2 +520-220-415+.
H-941 A/A bis equals local 1821.2 +520-220-415+.
415 is a stable fine form.
034 = 415.
415 has a semantic or phonetic value.
Harappa tablet sides and Mohenjo-daro seal faces are one equivalent semantic unit.
Any translation.
```

## Effect On The 520-220-X Branch

This sharpens the source-visible recurrence side of the `415` pool without admitting H-786/H-941 as exact-side evidence.

Previously safe exact-side candidates:

```text
H-938 A/A bis
H-940 A
```

Now candidate exact-row reconciliations, still quarantined behind side policy — held aside as unusable evidence until the side-labeling question is settled:

```text
H-786 A
H-941 A/A bis
```

The branch still does not support a reading. It supports a sharper source-side question:

```text
Is local 415 a broad graphemic family spanning seal/tablet media, or is it a transcription-policy bin hiding fine-form splits?
```

## Next Gate

Find an explicit CISI/HARP/Mahadevan side-label policy or object data note that explains whether local row ordering follows publication order, physical side order, transcription order, or an internal catalogue order.

Follow-up source-panel pattern recheck:

```text
docs/h786_h941_source_a_pattern_recheck.md
data/open_prototype/reports/h786_h941_source_a_pattern_recheck.csv
data/open_prototype/reports/h786_h941_source_a_pattern_recheck_summary.json
```

That recheck strengthens the visual side of the result: `H-786 A` and `H-941 A/A bis` sit in the same source-A target-like pattern as clean controls `H-938 A/A bis` and `H-940 A`, while source `B` panels do not. It still does not accept exact local row mapping for `H-786` or `H-941`.

Until that source-policy gate — the checkpoint that must be passed before the branch may advance — is closed, use these bins:

```text
accepted exact-source-side: H-938 A/A bis, H-940 A
candidate exact-source-side only: H-786 A, H-941 A/A bis
excluded for now: H-939, H-786 B, H-941 B/B bis
```

Accepted translations, phonetic values, and sign meanings remain:

```text
0
```
