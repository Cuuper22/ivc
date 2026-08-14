# 032-002-861 X-Before-240 Subframe Migration

Date: 2026-05-29

## Question

This note asks how freely signs move around inside one recurring construction. Signs in this corpus are numeric IDs. "X-before-`240`" names the slot filled by the sign X in rows shaped `...-X-240-...`; a "subframe" is the short fixed run of signs that follows `240` in such a row. A sign that appears with many different subframes is mobile; a sign stuck with one is locked.

Inside the X-before-`240` construction, do X signs migrate across after-`240` continuations, or are they locked to narrow subframes? This is the next distributional question after the failed `H-1138/H-360` graphic upgrade: it asks whether `603` behaves like an internally mobile sign candidate or like a local copied tablet-slot artifact.

## Method

Input is the already-built strict X-before-`240` packet — a fixed bundle of rows assembled for this question: complete closed token rows, deduplicated by `(cisi, site, type, symbol, text)`, so identical texts count once. This pass adds no new source claim; it re-profiles the distributional behavior.

Rows: `95` X-before-`240` rows across `28` X signs.

## Decision

Status: `603_bridge_survives_distributionally_but_is_not_internally_mobile_inside_x240`.

Core observations:
- `603` is locked to `240-060-692` inside X-before-240: 3 rows, 1 register cell, 1 formula family. A register cell groups rows sharing an object class — site, seal type, icon, shape; a formula family groups near-identical repeated texts. One of each means the three rows are close to being one witness.
- `636` and `642` are not locked the same way: `636` spans 5 after-240 continuations and `642` spans 5.
- `482` is strongly tied to `240-002-861`, mostly one formula family; `904` splits between terminal `240` and `240-002-817`.
- Therefore the Harappa-side `603` evidence is narrower than the controls, not broader. Its mobility is external: post-`002-861-603`, not internal to X-before-240.

Interpretive shift:
- Promote split-homograph/catalog-conflation and copied-template explanations for Harappa `603`.
- Keep `603` as a live distributional bridge — a sign linking two otherwise separate structures — only because no other low-frequency X-before-240 sign also appears as a post-`002-861` tail initial, the first sign of the material ending a row after `002-861`.
- Do not use the Harappa `603` packet as value evidence until `H-1846` or a better `H-1138` source route resolves graphic identity.

Not accepted: `603` value, phonetics, language identity, cross-context graphic identity, or translation.

## Target Profiles

| X | rows | class | subframes | dominant | registers | families | post-861 initial rows | after-240 counts |
|---|---:|---|---:|---|---:|---:|---:|---|
| 636 | 15 | migrates_across_subframes | 5 | <END> (8/15) | 9 | 7 | 0 | <END>:8;031 032 171:3;060 692:2;066 556:1;233 235 002:1 |
| 100 | 8 | migrates_across_subframes | 5 | <END> (4/8) | 7 | 7 | 0 | <END>:4;220 032 002:1;235 741 175:1;741 702 900:1;031:1 |
| 482 | 8 | migrates_across_subframes | 2 | 002 861 (7/8) | 6 | 2 | 0 | 002 861:7;002 944 920:1 |
| 642 | 7 | migrates_across_subframes | 5 | 060 692 (2/7) | 4 | 5 | 0 | 060 692:2;001 692:2;204 705 621:1;<END>:1;031 002 861:1 |
| 904 | 7 | migrates_across_subframes | 3 | 002 817 (3/7) | 4 | 4 | 0 | 002 817:3;<END>:3;235:1 |
| 176 | 5 | migrates_across_subframes | 4 | <END> (2/5) | 4 | 4 | 0 | <END>:2;002 702 503:1;002 817:1;798 002 861:1 |
| 603 | 3 | locked_duplicate_family | 1 | 060 692 (3/3) | 1 | 1 | 3 | 060 692:3 |
| 630 | 3 | migrates_across_subframes | 3 | 031 032 171 (1/3) | 3 | 3 | 0 | 031 032 171:1;741 861:1;<END>:1 |
| 643 | 3 | migrates_across_subframes | 2 | <END> (2/3) | 3 | 3 | 0 | <END>:2;002 861:1 |

## Subframes

| after 240 | rows | distinct X | X counts | registers | families | examples |
|---|---:|---:|---|---:|---:|---|
| <END> | 33 | 14 | 636:8;100:4;904:3;760:3;233:3;176:2;643:2;000:2;152:1;630:1;642:1;235:1;637:1;772:1 | 18 | 23 | C-51 +151-740-100-240+;- +740-904-240+;H-1895 +400-740-100-240+;H-1897 +400-740-904-240+;H-2076 +740-760-240+;H-2077 +740-760-240+;H-2200 +400-740-176-240+;H-2201 +400-740-176-240+;H-2189 +400-740-152-240+;H-1308 +740-690-636-240+ |
| 002 861 | 9 | 3 | 482:7;643:1;637:1 | 7 | 3 | H-2010 +740-482-240-002-861+;H-2011 +740-482-240-002-861+;H-51 +740-643-240-002-861+;H-806 +740-482-240-002-861+;H-807 +740-482-240-002-861+;H-808 +740-482-240-002-861+;- +740-637-240-002-861+;H-1130 +740-482-240-002-861+;H-1131 +740-482-240-002-861+ |
| 060 692 | 7 | 3 | 603:3;642:2;636:2 | 3 | 3 | H-1138 +740-603-240-060-692+;H-1845 +740-642-240-060-692+;H-1846 +740-603-240-060-692+;H-237 +740-642-240-060-692+;H-360 +740-636-240-060-692+;H-823 +740-636-240-060-692+;H-1137 +740-603-240-060-692+ |
| 002 817 | 5 | 3 | 904:3;176:1;923:1 | 2 | 3 | - +740-904-240-002-817+;H-697 +740-904-240-002-817+;M-289 +740-176-240-002-817+;M-1166 +740-923-240-002-817+;H-1100 +740-904-240-002-817+ |
| 031 032 171 | 4 | 2 | 636:3;630:1 | 3 | 2 | H-2192 +740-630-240-031-032-171+;H-301 +400-740-636-240-031-032-171+;H-905 +400-740-636-240-031-032-171+;H-988 +400-740-636-240-031-032-171+ |
| 001 692 | 2 | 1 | 642:2 | 1 | 1 | H-821 +740-642-240-001-692+;H-822 +740-642-240-001-692+ |
| 031 | 2 | 2 | 100:1;927:1 | 2 | 2 | M-1982 +740-100-240-031+;M-951 +740-927-240-031+ |
| 220 032 002 | 2 | 2 | 100:1;585:1 | 2 | 2 | C-65 +000-100-240-220-032-002-861+;M-722 +740-585-240-220-032-002-817+ |
| 235 | 2 | 2 | 904:1;455:1 | 2 | 2 | L-111 +740-904-240-235+;M-1096 +740-455-240-235+ |
| 235 060 820 | 2 | 2 | 923:1;455:1 | 2 | 2 | M-1760 +740-923-240-235-060-820+;M-808 +740-455-240-235-060-820+ |
| 001 368 920 | 1 | 1 | 765:1 | 1 | 1 | M-84 +740-765-240-001-368-920+ |
| 001 820 | 1 | 1 | 440:1 | 1 | 1 | H-411 +740-440-240-001-820+ |
| 002 435 255 | 1 | 1 | 639:1 | 1 | 1 | H-598 +740-639-240-002-435-255-777+ |
| 002 702 503 | 1 | 1 | 176:1 | 1 | 1 | H-408 +740-176-240-002-702-503+ |
| 002 820 | 1 | 1 | 806:1 | 1 | 1 | L-83 +740-806-240-002-820+ |
| 002 861 031 | 1 | 1 | 773:1 | 1 | 1 | M-706 +740-773-240-002-861-031+ |
| 002 900 003 | 1 | 1 | 772:1 | 1 | 1 | M-958 +740-772-240-002-900-003-590+ |
| 002 944 920 | 1 | 1 | 482:1 | 1 | 1 | M-280 +740-482-240-002-944-920-140+ |
| 031 002 861 | 1 | 1 | 642:1 | 1 | 1 | M-941 +000-642-240-031-002-861+ |
| 060 111 166 | 1 | 1 | 798:1 | 1 | 1 | L-26 +740-798-240-060-111-166+ |
| 060 415 056 | 1 | 1 | 772:1 | 1 | 1 | H-14 +740-772-240-060-415-056+ |
| 066 556 | 1 | 1 | 636:1 | 1 | 1 | M-1879 +740-636-240-066-556+ |
| 204 705 621 | 1 | 1 | 642:1 | 1 | 1 | H-206 +740-642-240-204-705-621+ |
| 220 032 806 | 1 | 1 | 055:1 | 1 | 1 | M-1265 +740-055-240-220-032-806+ |
| 233 235 002 | 1 | 1 | 636:1 | 1 | 1 | M-41 +740-636-240-233-235-002-405-125-820+ |
| 235 002 220 | 1 | 1 | 798:1 | 1 | 1 | M-46 +740-798-240-235-002-220-065-215+ |
| 235 031 900 | 1 | 1 | 835:1 | 1 | 1 | C-40 +740-000-835-240-235-031-900-066+ |
| 235 060 692 | 1 | 1 | 773:1 | 1 | 1 | M-5 +740-773-240-235-060-692+ |
| 235 741 175 | 1 | 1 | 100:1 | 1 | 1 | H-76 +740-100-240-235-741-175-132+ |
| 235 806 | 1 | 1 | 923:1 | 1 | 1 | M-405 +740-923-240-235-806+ |
| 235 806 002 | 1 | 1 | 055:1 | 1 | 1 | M-29 +740-055-240-235-806-002-220-455-503+ |
| 415 798 060 | 1 | 1 | 055:1 | 1 | 1 | H-386 +527-555-740-055-240-415-798-060-201+ |
| 741 702 900 | 1 | 1 | 100:1 | 1 | 1 | H-450 +740-100-240-741-702-900-003+ |
| 741 861 | 1 | 1 | 630:1 | 1 | 1 | H-102 +740-630-240-741-861+ |
| 798 002 861 | 1 | 1 | 176:1 | 1 | 1 | M-629 +679-740-176-240-798-002-861+ |
| 798 365 263 | 1 | 1 | 233:1 | 1 | 1 | H-659 +407-845-140-740-233-240-798-365-263+ |
| 803 | 1 | 1 | 772:1 | 1 | 1 | M-705 +740-772-240-803+ |
