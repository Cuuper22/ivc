# H-940 IA JP2 Route Recheck

Date: 2026-05-26

This note records one attempt to get a sharper picture of a single object side, H-940 B, by fetching a different file format from the Internet Archive. It exists to close off that avenue in writing, so nobody spends another day chasing the same scan through a new download path.

## Question

Does the Internet Archive JP2 derivative for CISI Pakistan page n374 improve H-940 B enough to change the local `110` / Parpola sign-no.-41 branch gate? A branch is one open line of investigation; a gate is the checkpoint it must pass to advance.

## Source Route

A route is the exact path from a public archive to the image file. Checked IA archive-member route:

```text
https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_jp2.zip/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_jp2%2FCorpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_0374.jp2
```

Stored page files:

```text
tmp/h940_higher_res_route/ia_jp2/cisi_pakistan_0374.jp2
sha256: 352c8a84ad75ebdf36313768132a891aeff6a8c83c5a1ed6a49526ed5f753a36
dimensions: 3258 x 4550

tmp/h940_higher_res_route/ia_jp2/cisi_pakistan_0374_from_jp2.png
sha256: 1dd9e40baa6be252a9c4df22a7ed40c6bbea9fbf18d2383de205cb8399d211f2
dimensions: 3258 x 4550
```

Stored H-940 crops:

```text
tmp/h940_higher_res_route/derived/h940_a_panel_from_ia_jp2.png
tmp/h940_higher_res_route/derived/h940_b_panel_from_ia_jp2.png
tmp/h940_higher_res_route/derived/h940_b_panel_no_label_from_ia_jp2.png
```

## Result

No upgrade.

The direct JP2 archive member has the same pixel geometry as the checked IIIF max route (`3258 x 4550`). The H-940 B crop still reads as low-contrast paired/wavy vertical forms rather than a clean single compound branching figure comparable to H-2148. The JP2 route is useful as a reproducible source-path confirmation, but it does not remove the public-quality blocker.

Pixel comparison against the IIIF-derived crops gives high but non-identical similarity, consistent with another derivative of the same scan rather than a higher-resolution witness:

```text
H-940 A crop PSNR average: 47.513904
H-940 B full crop PSNR average: 47.887484
H-940 B no-label crop PSNR average: 47.399278
```

## Decision

Accepted:

- The IA JP2 route is now checked and stored.
- It gives no resolution or topology upgrade over the IIIF max route.
- H-940 B remains source-visible but visually split/non-binding at current public quality.

Rejected:

- H-940 rejoins H-2148 through the public JP2 route.
- The IA JP2 crop supports `local 110 = Parpola sign no. 41`.
- Any sign value, phonetic value, language identity, or translation.

## Stored Report

```text
data/open_prototype/reports/h940_ia_jp2_route_recheck.csv
data/open_prototype/reports/h940_ia_jp2_route_recheck_summary.json
```

## Next Gate

Stop treating IA page derivatives as likely to solve H-940 B. The next useful H-940 evidence is an independent source-grade crop, original plate/photo, HARP/CISI source note, or side-label transcription.
