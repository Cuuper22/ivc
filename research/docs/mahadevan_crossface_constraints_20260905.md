# A paired-face constraint on numerical readings of the Indus script

**Research date:** 5 September 2026  
**Repository:** Cuuper22/ivc  
**Status:** reproducible catalogue-level finding, with a checked original plate; not a decipherment or an accepted lexical reading.

## Result

Four different front-side inscriptions in the Mahadevan concordance each occur with a cup sign plus two, three, and four long strokes on the other face. The twelve combinations cover 34 catalogued objects. Across the full eligible set, eight front-text families have variable reverse-side stroke counts.

This supplies a concrete constraint on numerical interpretations: a fixed front inscription cannot always be an alternative notation for the same scalar quantity as its reverse, if the reverse strokes have a fixed positive unit value. Changing a number base does not repair this contradiction.

The useful positive interpretation is a **fixed descriptor with a separately variable parameter**, rather than two redundant renderings of one amount. "Descriptor" is a proposed function, not a translation: the data do not identify a commodity, person, institution, sound, or language. Nor does the grid establish statistical independence of the two fields.

The main methodological advance is to test readings against *linked faces of the same archaeological object*, rather than against isolated sign frequencies. The deliverable contains every eligible object, rejected-row reasons, and machine-readable counterexample certificates.

## 1. Recovering the missing scholarly comparison corpus

The inspected repository relied on a Lipi planning corpus and smaller comparison layers. Its July checkpoint also narrowed the previously accepted terminal-tail observation; the root README's stronger wording was not treated as the current evidence standard.

I retrieved the publicly readable Mahadevan concordance used by the Indus Research Centre / RMRL's `indusscript.in` Browse interface. Acquisition used its ordinary public collection, without accounts or authentication bypass. Fourteen response pages exhausted the pagination. The preserved source is a frozen data snapshot, not a new transcription made by this project.

| Completeness check | Retrieved snapshot | Mahadevan's published corpus |
|---|---:|---:|
| Catalogued objects | 2,906 | 2,906 |
| Nonempty inscription lines | 3,573 | 3,573 |
| Legible sign occurrences, including doubtful readings | 13,372 | 13,372 |
| Sign inventory, including doubtful readings | 417 | 417 |
| Sign 342 occurrences, including doubtful readings | 1,395 | 1,395 |
| Sign 99 occurrences, including doubtful readings | 649 | 649 |

There are 3,916 database records because another 343 records describe surfaces with no text. These are not 3,916 independent inscriptions. The checks agree with the original 1977 book's corpus accounting, especially sections 4–5, 9.2, and its sign-frequency tables. Agreement is strong evidence of census completeness, not proof that every individual reading is correct.

The combined raw JSON has SHA-256:

```
6a0c597986783c5da8fbcb0afc3268a2c6a9f042a9b81746ebc4f89158efbd01
```

This is an independent **transcription system**, not an independent archaeological sample: many objects also occur in the other catalogues. The public announcement mentions later addenda; this snapshot reproduces the 2,906-object, 417-sign base corpus, not the expanded addendum totals.

The linked web manual PDFs returned HTTP 404 and are recorded as failed acquisitions. Codebook interpretation was checked against the original Mahadevan book already preserved in the repository and the public application's conventions. The missing PDFs were not silently substituted or claimed as retrieved.

## 2. Exact inclusion rules

The analysis preserves all fourteen original sign slots and all metadata. A `0` is an illegible or lost passage, **not the number zero**. A leading asterisk marks a doubtful reading; these entries contribute to the published-census comparison but never become undoubted signs in the strict analysis. Blank trailing slots are padding. No sign classes or possible allographs were merged.

The strict subset requires a nonempty line; an allowed direction code of 1, 2, or 3; undoubted sign IDs from 1 through 417; no damage marker; no internal blank slot; and agreement between the slot count and the recorded position and legible-sign counts. This gives 2,575 lines, or 1,659 distinct exact strings containing 7,409 tokens. "Strict" means unflagged under these catalogue rules, not newly verified undamaged photographs.

The paired-face analysis then requires exactly two recorded surfaces of an object, each with one line (`sideline` 10 and 20), both passing the strict filter, and object class 3, the miniature-tablet class. Exactly one face must be the cup sign 328 paired with one of the visually checked long-stroke groups. It never joins unrelated objects just because their texts look similar.

The long-stroke signs used here are 86, 87, 89, 95, and 96, showing respectively one through five strokes in the publisher's sign illustrations. These visual counts are observations; their numerical or metrological semantics remain hypotheses. The short-stacked sign 103 is kept distinct from the long-stroke groups.

This leaves **85 paired objects and 39 distinct front strings**. "Front" here simply means the face other than the cup-and-strokes face; it is not an assertion about ancient obverse/reverse conventions. Tables display the reverse of stored slot order for comparability with the repository's display convention. Both orders are retained; this display operation establishes no phonetic reading direction.

## 3. The four-by-three witness grid

All identifiers in this table are **Mahadevan 1977 text numbers**, not CISI artifact numbers. Sign numbers likewise belong to Mahadevan's sign list, not the Lipi/Wells namespace. One representative object is shown per cell; the JSON supplies all witnesses.

| Fixed front inscription | Cup + 2 long strokes | Cup + 3 long strokes | Cup + 4 long strokes | All objects in family |
|---|---|---|---|---:|
| 176–342–48 | text 4548 | text 4403 | text 4508 | 21 |
| 211–72 | text 4551 | text 5496 | text 4428 | 3 |
| 342–403–103 | text 4554 | text 4512 | text 4553 | 6 |
| 402–287 | text 5410 | text 4502 | text 5418 | 4 |

These are 12 occupied cells, not 12 identical copies of one text. Four additional front families have two different reverse counts, bringing the total to eight variable families. Entire front-plus-reverse deduplication leaves **51 distinct pairs** across the 39 front strings.

A useful finite-data bound follows immediately. Even an arbitrary lookup table, allowed to memorize every front, can assign only one reverse count to that front. It can therefore reproduce at most 39 of the 51 distinct pairs. Weighting by the 85 catalogued objects, the best possible such lookup fits 63 and necessarily misses 22. These are exact empirical bounds, not held-out accuracy estimates or statements about the whole Indus civilization. They are computed by selecting the largest reverse-count group for each front in `front_families.json`.

## 4. The conditional counterexample

Let **F** be the value assigned to one unchanged front expression. Suppose:

1. Its complete encoded sign string corresponds to the same expression and value on the compared objects.
2. A reverse with n long strokes represents n times a fixed unit u, where u is positive.
3. The front and reverse express the same scalar quantity.

For texts 4554 and 4553, the catalogue then requires both

```
F = 2u
F = 4u
```

Subtracting gives `2u = 0`, contrary to `u > 0`. The same argument applies to every variable-count family. It does not depend on a guessed value for a front sign, on a base of eight versus ten, or on how the front expression is parsed. It also works for any fixed reverse-value function that assigns different values to the observed stroke groups.

**At least one assumption must fail.** Possible explanations include a descriptor rather than a total on the front, context-dependent units, non-numerical strokes, missing contextual information, or a catalogue normalization that conflates genuinely different signs. Allowing a different unit on every object avoids the contradiction, but then a reading must supply independently motivated rules for that variation rather than claim a fixed conversion from the front alone.

This is a constraint on a class of readings, not a proof of the correct reading. In particular, it does not refute every restricted numerical equation proposed for a separately justified subgroup of tablets.

## 5. Original-source verification

The clearest controlled subset is Mahadevan texts **4553, 4554, and 4555**. Their encoded front is 342–403–103; their reverse stroke counts are four, two, and four. Both faces share the same recorded object class, direction, locus code 42, level −15, and field-symbol code. These metadata are useful controls, not proof of a common production event or an identical measurement unit.

The original Mahadevan text table lists this contrast. Its source-number appendix connects the 4xxx text series to Vats's numbered illustrations. I retrieved the repository's scan of **M. S. Vats, _Excavations at Harappa_, volume II, plate XCVII**, and inspected objects **553, 554, and 555** directly. The plate is PDF page index 201, not a guessed page based on the web record's volume label. The archive metadata labels the item as volume I, whereas the local source is the plate volume.

The original plate visibly preserves the paired objects and reverse-side contrast. Its low resolution does **not** independently settle every tiny stroke or possible allograph on the front: the exact normalized identity of all three front strings remains a catalogue-level proposition. The crop is included with its source PDF hash and rendering coordinates; enlarging it is not treated as recovering missing detail.

A second check concerns **CISI H-306**, linked to Mahadevan text **5474** by excavation number **13270**, not merely by a learned sign mapping. Both catalogues record the long-stroke contrast of two on the non-cup face and three on the cup face. The existing object photographs were inspected. This challenges an unrestricted same-unit, equal-face interpretation, but different units on the two faces could explain this one object in isolation; the identical-front families provide the stronger constraint.

No uncertain Mahadevan-to-CISI assignments for texts 4553–4555 were promoted into the repository's accepted crosswalk.

## 6. What changes in a decipherment attempt

The next numerical model should represent an artifact as a linked record with potentially complementary fields, not automatically as an equation between faces. A viable model must account for the full witness grid, including identical fronts with different reverses. Held-out testing must keep whole objects and related exact formula families together.

A reasonable working hypothesis is **descriptor plus quantity-like parameter**. What the descriptor identifies is unresolved. The present result cannot choose among personal names, institutional labels, commodities, ritual categories, or other functions. Likewise, recurrence and variable stroke groups alone do not establish that the complete sign system encodes spoken language.

The outstanding source task is a fresh, high-resolution comparison of the front signs in the exact counterexample pairs. That task could strengthen the conditional premise or reveal a real graphical distinction. It is a specific falsifiable target, not a request to re-audit the whole corpus before doing any further research.

## 7. Searches that did not earn a positive claim

An initial Lipi six-cell substitution grid looked striking against simple position-preserving shuffles. A stronger exploratory suffix-swap control preserved both adjacent-sign frequencies and position frequencies. The global observed pattern did not clear that control: its Monte Carlo tail frequency was about 0.095 before a suspected-allograph merge and 0.219 afterward. These were correlated MCMC samples without a certified mixing bound; no formal significance claim is made. The grid was dropped as breakthrough evidence.

An iconographic minimal-pair scan likewise produced no sufficiently repeated one-sign replacement tied to a motif change. Exploratory cross-catalogue sign alignments were not accepted: seed choices had seen the whole data, so their apparent test performance was not independent validation.

These failures are distinct from the paired-face result, which is an explicit conditional counterexample, not a claim that a discovered grid is statistically surprising under an n-gram null.

## 8. Conditional arithmetic appendix

Fuls's numerical proposal supplies the equations `v = 2S − L` and `vL + 1 = 7S + 5`, under its artifact interpretations [3]. Their positive-integer solutions can be characterized exhaustively rather than by a bounded search:

```
S(2L − 7) = L² + 4.
Let d = 2L − 7 > 0.
4S = d + 14 + 65/d.
```

Thus d must divide 65. Checking its four positive divisors gives exactly

```
(L, S, v) = (4,20,36), (6,8,10), (10,8,6), (36,20,4).
```

Adding the proposed bangle constraint `15 ≤ 7 + L ≤ 20` leaves `(10,8,6)`. This recovers a previously proposed assignment **conditionally**; it is not a new accepted sign value. The algebra does not validate the face-equality assumptions, the reconstructed bangle count, or the interpretation of the original numerical groups.

## 9. Reproduction and evidence status

From the repository root, Python 3.10 or later, no third-party packages:

```sh
python research/tools/mahadevan_constraint_audit.py \
  --input research/data/mahadevan_20260905/concordance_documents.json.gz \
  --output /tmp/ivc-mahadevan-audit
```

The script checks all six published census numbers, redundant transcription fields, consecutive row indices, and unique object/side/line keys before generating the paired-object tables and counterexample certificates. It preserves exclusions and original sign codes. Its outputs reproduce the source counts in sections 1–4; the exact lookup bounds follow from `front_families.json` by the stated formula.

Outputs reside in `research/data/mahadevan_20260905/`. The source snapshot and normalized CSV are accompanied by acquisition and SHA-256 manifests. Figure witnesses are separate from machine-readable text; nothing in the analysis depends on OCR of the displayed crop.

**Evidence ledger:** no accepted translation, phonetic value, sign meaning, language identification, or external anchor has been added. The prior accepted structural count has not been silently changed. The new item is a reproducible catalogue-level constraint, with an explicitly limited original-plate check. Its exact characterization is new to this repository; scholarly priority has not been established.

### Sources and provenance

[1] Iravatham Mahadevan, _The Indus Script: Texts, Concordance and Tables_, Memoirs of the Archaeological Survey of India 77 (1977). Original source text preserved in this repository under `evidence/tmp/cisi_xml/`; public concordance at https://indusscript.in/. The public collection URL and every acquisition response hash are in `acquisition_manifest.json`.

[2] M. S. Vats, _Excavations at Harappa_, volume II (1940), plate XCVII, objects 553–555. Repository source: `evidence/tmp/032_002_861_603_slot_source_normalization/vats_excavations_at_harappa_vol2_plates.pdf`. Archive record: https://archive.org/details/in.gov.ignca.9842.

[3] Andreas Fuls, "Ancient Writing and Modern Technologies – Structural Analysis of Numerical Indus Inscriptions" (2020), especially its numerical-value proposal. Author's public copy: https://www.researchgate.net/publication/361812318_Ancient_Writing_and_Modern_Technologies_-_Structural_Analysis_of_Numerical_Indus_Inscriptions.

[4] RMRL concordance announcement: https://www.harappa.com/blog/indus-concordance-and-tamil-potsherds-now-online. This describes the scholarly resource; acquisition and census checks, not the announcement alone, establish what the present snapshot contains.

The research code is distinct from the source materials. Attribution is retained; no new blanket license is asserted over third-party catalogues or photographs.
