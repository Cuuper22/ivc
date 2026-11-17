# Sweep 06: leads from the chunk_06 reading list

Read in full: all 38 notes on the list (research/docs/archive/). Numbers marked (computed) were calculated in this sweep from research/data/open_prototype/lipi/metadata_filtered.csv (5,679 rows, one per inscribed side). Every other number is quoted from a note.

## Plain-words key

- H-number: the catalog name of one object. H-2238 is one tablet.
- Row ID: 1818.2 means raw ID 1818 (one object's record) and side 2. Raw IDs are numbers given at entry, so neighbouring raw IDs were often entered together.
- Companion row: the other inscribed side of the same object.
- Strict count: rows whose whole text equals the string exactly.
- Excavation prefix: the H95, H96 or H97 at the start of an excavation number. The series notes give 1995 to 1997 as the span. I read the prefix as a year, which no note states.
- Fisher p: the exact chance of a split at least this lopsided if the two groups were alike (two-sided).
- VIIII: Parpola's reading of a reverse side as nine, written with repeated I's.
- Sign 41: Parpola's sign number 41, a kneeling-figure sign.
- Allograph: two shapes counted as one sign. Crosswalk: a checked mapping between two sign-numbering systems.
- R/L, L/R, NR: recorded direction codes for one side.
- TAB:I, TAB:B: the tablet classes in the catalog (incised and the other tablet class). SEAL:S and SEAL:R: seal classes.
- "A bis": a second photograph of side A of the same object.
- CISI: the printed photo corpus of Indus seals and inscriptions. HARP: the Harappa excavation project's object records.
- OCR: text a computer read off a scanned page. IIIF and JP2: two kinds of page-image copy from the Internet Archive. sha256: a file fingerprint.
- Textual criticism: rebuilding the family tree of copies from the differences between them.

---

### 1. The 700-03x slot is a three-form set (032, 033, 034), and all three forms are common
- What was seen: Strict counts across the corpus (computed): +700-033+ 125 rows, +700-034+ 109, +700-032+ 89. Reversed forms: +033-700+ 32, +034-700+ 14. The H-series notes follow only 033 and 034 and treat 033 as a singleton inside the series. The notes never mention 032. For comparison, +154-003+ has 2 strict rows and +156-003+ has 31. Median raw ID (computed): 034 at 853, 032 at 1248, 033 at 1373.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (text, id). Notes: the H-2218 to H-2239 Fig. 4 mapping and external-distribution notes.
- Old label: the H-2238 033 form is a singleton variant with broad external support; source-gated inside the series. 032 is absent from the notes.
- Why it is alive: Three neighbouring sign numbers, each with 89 to 125 exact rows, form a paradigm, which is a set of forms that can fill one slot. A typo or a one-object variant does not produce that. The H-series singleton is one form from the paradigm that one batch used. Neighbouring numbers suggest the forms differ by one graded feature, such as a stroke count.
- What it would mean if true: The 700-03x slot is open and graded, filled by one of three forms. The H-2238 against H-2230 pair is one instance of a three-way choice that runs through the whole corpus.
- Cheapest next move: List every row matching +700-03[234]+ with its companion side, object type and site. If the three forms take different companions, the slot is contrastive. If they do not, the forms are free variants.

### 2. The 033 and 034 forms split by catalog batch, measured two ways
- What was seen: By raw ID (computed): 52 of the 109 +700-034+ rows sit in raw 500 to 999. 43 of the 125 +700-033+ rows sit in 1500 to 1999, and 33 in 1000 to 1499. In the raw 1330 to 1339 block, short sides are 034 in 5 of 7 cases (H-308, H-312, H-313, H-314, H-317). In the raw 1371 to 1376 block, all 7 short sides are 033 (H-352, H-353, H-354 seal, H-355 twice, H-356, H-357). By excavation prefix, read as a year (computed, strict counts): H95 has 033 at 9 and 034 at 10. H96 has 6 and 14. H97 has 4 and 27. Fisher p for H95 against H97 is 0.018. Fisher p for H96 against H97 is 0.16, which is the one contrary number and it is also non-significant. Counts are small and I looked at several year pairs, so treat this as exploratory.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (id, excavation-idno, text). The confound notes checked manufacturing group and Fig. 4 order only, never the batch axis.
- Old label: the 033 and 034 split is a catalog-side contrast from the planning layer. Confound checks against manufacturing group and figure order found no explanation, and the split was not promoted.
- Why it is alive: The notes tested two confounds, and neither explained the split. Nobody tested the accession batch, which is the axis the numbers point to. Both H-series variants come from the earliest prefixes (entry 3). A form that changes with batch is a time marker. A sign choice that follows a generation of practice is what a sign with a function looks like in a dated corpus.
- What it would mean if true: 033 and 034 fill the same slot in two generations of practice. The corpus is a sequence of dated habits, and the H-series is one slice of it.
- Cheapest next move: Tabulate the 033 and 034 rows by raw-ID block and by excavation prefix together, for the 700 frame and the 400-740-176 frame. If both axes agree, the batch becomes the first variable to test before any function is assigned.

### 3. Both H-series singleton variants come from the earliest accession prefixes, and one seal carries both variant forms
- What was seen: Of the 22 H-series objects, 19 carry an H97 prefix, 2 carry H96 (H-2237, H-2239) and 1 carries H95 (H-2238). The two variants are H-2237 (154 in side 3, H96) and H-2238 (033 in side 1, H95). They are the only two non-H97 objects with a variant. Chance that two randomly drawn objects out of 22 are both among the three non-H97 objects: 3 of 231, or 0.013 (computed). Chance that 3 drawn objects contain both variants: 20 of 1,540, or 0.013 (computed). The 16 H97 objects with lot suffixes 8040-01 to 8040-16 form a complete run of that lot (computed from the HARP IDs). None of the 19 H97 objects carries a variant. Contrary: H-2239 (H96) carries the main form, so the early group is not all variant. Separately, the Harappa seal H-1682 (SEAL:S, excavation H96-2796) reads +154-003-617-033+, so both variant forms sit on one seal. Mohenjo-daro seal M-102 reads +154-003-900-545+.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (rows 794.3, 693.1, 810.1, 2629.1). Notes: the Fig. 4 mapping, the series validation sheet, the external-distribution note, the localization null.
- Old label: singleton variants. The localization null found both in group 3 and in one template (exact 0.026). The workshop and template confound was called active. The 154 form has sparse external support (one tablet, H-366).
- Why it is alive: The old tests asked whether the variants share a manufacturing group or a template, and they do. Nobody asked whether they share a year. Both sit in the early prefixes, and the only seal with both forms also has an H96 prefix. Two forms of one slot, both from one early batch, on one seal, is what a time-marked practice produces. The current notes cannot separate workshop from year, which makes the separation the next question.
- What it would mean if true: The H-series minimal pairs are cross-year pairs. H-2237 (1996) against H-2233 (1997), and H-2238 (1995) against H-2230 (1997). The 154 and 033 forms are early-batch marks that reach seals as well as tablets.
- Cheapest next move: List every TAB:I and TAB:B row with an H95 or H96 prefix and count 154, 156, 033 and 034 against the H97 rows. This takes one query on the existing file.

### 4. The 400-740-176 long row sits beside a 033 or 034 companion on 33 objects, seals included
- What was seen: 32 objects carry the long row +400-740-176+ next to a companion side with 033 or 034, and H-787 carries the same two forms in one combined row (computed). The companion sides are 24 rows with 033 and 9 with 034. Examples: H-309 (+400-740-176+ / +700-033+), H-308 (+400-740-176+ / +700-034+), H-933 (+034-700+ / +400-740-176+). Two of the objects are seals (H-352, H-354). Of the 33 objects, 23 fall in the H-266 to H-1019 range that the CISI Pakistan photo section covers (computed from object numbers).
- Where: research/data/open_prototype/lipi/metadata_filtered.csv. Notes: the H-933 and H-960 contrast audit, the H-355 double-short-side audit.
- Old label: the H-933 and H-960 pair is source-gated with no object-level image. H-355 is a catalog artifact until a three-side source is inspected.
- Why it is alive: Each note treats its object as a single case. Together the 33 objects form a repeated two-line formula: a long string followed by a 03x companion, on seals and tablets alike. The packet's contrast is therefore a 33-object question, not a two-object question. The 033 companion outnumbers 034 by 24 to 9.
- What it would mean if true: The long string is a fixed heading, and 033 or 034 is the closing sign under it. The formula crosses from tablets to seals, which is a cross-medium formula.
- Cheapest next move: Check the 23 in-range objects in the CISI Pakistan scan first (entry 15). That needs no new request.

### 5. The three tablets the 2021 Nature article names all carry +700-033+, so its mirror-writing claim is about the 033 row
- What was seen: The Daggumati and Revesz 2021 article (Nature, s41599-021-00713-0) names H-1302, H-1303 and H-1822 as mirrored-writing and correction cases. Local rows: H-1302 4073.2 +700-033+ (R/L). H-1303 4077.2 +700-033+ (R/L). H-1822 550.1 +700-033+ (R/L), with companion 550.2 +400-740-176-519+ (L/R). H-1822 is a different object from raw ID 1822, which belongs to H-942. All 24 033 companion rows from entry 4 are coded R/L.
- Where: research/docs/archive/h1302_h1303_source_provenance_gate.md and h1302_h1303_direction_note_recheck.md. Rows 4073.2, 4077.2, 550.1, 1822.1 in metadata_filtered.csv.
- Old label: correction-risk acquisition priorities, not accepted evidence. Reconcile with the ICIT and Fuls correction notes.
- Why it is alive: Published discussion of mirrored writing picks out objects whose short row is 033, and only those. If the 033 and 034 glyphs differ mainly in orientation, the 125-to-109 corpus contrast (entry 1) and the H-2238 against H-2230 pair both become one glyph in two positions, and the R/L direction code becomes the variable. The article's own topic is allographs, so its authors already allowed that two shapes could be one sign.
- What it would mean if true: 033 and 034 are one sign in two orientations. The sign inventory shrinks, and the recorded direction codes carry information that the notes assigned to sign identity.
- Cheapest next move: Read the article's inline glyphs on page 6 (the note records a crop of that page) and check whether the 033 glyph is a mirror image of the 034 glyph. One plate would split the two readings: H-2238 side 1 (033) against H-2230 side 1 (034) in the same photographed orientation.

### 6. Parpola's two reverse-side readings line up with two companion tokens: VIIII with 034, sign 41 with 110
- What was seen: Parpola (2019) reads the reverse of H-938, H-939, H-1284 and H-2145 as VIIII. Their companion rows are 034 in all four: H-938 1818.2 +034-700+, H-939 1819.1 +700-034+, H-1284 4069.2 +700-034+, H-2145 827.1 +700-034+ (computed from metadata). Parpola places sign 41 on the reverse of H-940, H-2147 and H-2148. Their companion rows are 110 in all three: H-940 1820.2 +110+, H-2147 673.1 ]110+, H-2148 481.2 +110+. Outside control H-2152 (865.1 +110[) also carries 110. Seven of seven Parpola-named objects split cleanly by companion token.
- Where: research/docs/archive/h938_h939_h1284_h2145_parpola_reverse_clue.md and the H-2147, H-2148 and H-2100/H-2152 route notes. Rows as listed in metadata_filtered.csv. Parpola 2019 text is named as tmp/parpola_2019_bone_rods.txt (not present at research/tmp here).
- Old label: prior-work pressure only. No local-row mapping. 034 = 415 not accepted. 110 = sign 41 not accepted.
- Why it is alive: Each Parpola claim was checked against local rows one at a time, and no crosswalk was accepted. Nobody laid the two Parpola classes against the two companion tokens. The split is clean in all seven cases. A reading made for one reason (Parpola's reverse numbers) accounts for the companion row of objects nobody had linked to 034.
- What it would mean if true: The companion side of this family is a count or a unit. 034 would be nine, and 110 would be sign 41 (a kneeling figure). The reverse would carry a quantity beside a fixed obverse text, a label-plus-count pattern like early accounting tablets.
- Cheapest next move: Count strokes on the 034 companion in the source plates of H-939 and H-1284. The notes accept no value for 034, so a stroke count of nine would be the first test that could give it one.

### 7. The 415 frame varies in its last slot (415 against 016) and its first slot (520 against 074), and the terminal form picks its companion
- What was seen: The 520-220-415 frame appears on H-938, H-939, H-940, H-941, H-1284, H-2240, H-2148, H-786 and H-2145 (where the first sign is 074 in 827.2). H-942 carries 520-220-016 (1822.1), with companion +033-700+ (1822.2). Parpola says H-942's obverse text recurs with H-940's. Terminal-form pairing (computed from rows): 415 has companion 034 in all four short-companion cases (H-938, H-939, H-1284, H-2145). 016 has companion 033 in its one case (H-942). H-941's companion (1821.1) carries 032 inside a longer string, +590-032-645-003+.
- Where: research/docs/archive/h2148_parpola_obverse_recurrence_stress_gate.md, h786_h941 side notes. Rows 1818.1 to 1822.2, 4069.1 to 4069.2, 827.1 to 827.2, 816.1 to 816.2 in metadata_filtered.csv.
- Old label: stressor. 016 against 415 is not accepted as one text. A companion sign-inventory gate was set up and never run.
- Why it is alive: The notes read H-942 as a threat to the recurrence claim. Read directly, it is a second minimal pair in the terminal slot of the 415 frame, parallel to the 154 and 156 pair in the H-series. The two terminal forms each take a different companion, which is the same paradigm pattern as entry 1 in another frame. The 032 inside H-941's companion adds a third form to the terminal-companion mix.
- What it would mean if true: The 520-220-X frame is a template in which the terminal sign and the companion sign choose each other (415 with 034, 016 with 033). One choice, two marks.
- Contrary number, once: among the 415 objects, the companion is a 03x form only in the four cases above. H-940 and H-2148 carry 110, H-2240 (816.2) carries +869-575+, and H-786 carries +824-892-413+. The pairing is therefore a pattern of the VIIII group, not of every 415 object, and the check below is needed to see whether it holds beyond that group.
- Cheapest next move: Compare the final sign of the H-942 obverse against H-940 and H-1284 in the source plates, and check whether the H-2240 obverse (816.1, 415) differs from them in any stroke.

### 8. H-2145 carries four deviations at once
- What was seen: H-2145 (827 rows, H97 prefix) reads VIIII on the reverse (Parpola). Parpola reports its obverse as the one exception to left-to-right reading in the category. Its first sign is 074 where the frame has 520 (827.2 +074-220-415+). Both of its rows have no recorded direction (the "-" code). It is the only VIIII object with a non-520 frame.
- Where: research/docs/archive/h938_h939_h1284_h2145_parpola_reverse_clue.md, h2145_h2147_h2148_source_route_recheck.md. Rows 827.1 and 827.2 in metadata_filtered.csv.
- Old label: new acquisition and crosswalk candidate, not an exact 520-220-415 row. Route-dark with a prior-work clue.
- Why it is alive: An object with four independent deviations is either the most informative in its family or damaged. The notes mark it complete and condition "Fair", with no damage recorded. Each deviation measures a different rule: direction, first slot, reverse class, and recording. If the deviations hold, the 520 slot is variable, like the terminal slot in entry 7, and the direction rule breaks on this object.
- What it would mean if true: The family rules are local to objects. H-2145 is the first object where direction, frame and reverse class all change together.
- Cheapest next move: Get the H97-3283 side images (the request for this object is already drafted in the notes) and read the obverse direction and first sign against H-938's obverse.

### 9. H-1997 has an object-level public slide, and the old audit threw it out as off-target
- What was seen: The bharatkalyan97 page from 2025/08 ("shapes of tablets convey information") carries two slide images. The audit found slide 1 shows H-233 A and B panels. It dismissed slide 2 because it is about H-1997. Local H-1997 (row 423.1): TAB:B, rectangular, one side, +400-740-176-235+, direction R/L, excavation H2000-4483 (Figure 39.09). So slide 2 is an object-level public image of a member of the 400-740-176 family (entry 4).
- Where: research/docs/archive/h233_public_slide_visual_lead_audit.md. Row 423.1 in metadata_filtered.csv.
- Old label: off-target false positive, excluded.
- Why it is alive: The audit's own rule says page-level image extraction must be followed by object-level relevance checks. Slide 2 passes that rule for H-1997. The page is claim-heavy, but a visible object is still a visible object. This would be the first public image of a long-row family member outside the H-933 and H-960 packet.
- What it would mean if true: The long string carries a tail (-235) that the packet does not assume, so the family's long row is not one fixed string.
- Cheapest next move: Open slide 2 from the 2025/08 page and read whether its one side shows the 400-740-176-235 sign run.

### 10. Raw IDs run in sign-family blocks, which fits copies entered together
- What was seen: Raw IDs 1815 to 1825 in order: H-935 (400-740-176 with 700-033), H-936 (400-740-176 with 700-034), H-937 (400-740-176 with 000-033), H-938 to H-942 (the 415 and 016 frame, with 034, 110 and 033 companions), H-943 and H-944 (400-158-592 with 700-032), H-945 (400-234 with 034-700). Raw IDs 4066 to 4090: H-1270 (700-033), H-1281 (700-032), H-1284 (415 frame with 700-034), H-1302 and H-1303 (400-740-176 with 700-033), H-1344 to H-1348 (400-740-176 or ]740-176+ with 700-033). Across 4,074 objects in raw-ID order (computed), the 700-03x family marks agree between neighbours 90.1% of the time. Shuffled orders give 84.2% on average. None of 2,000 shuffles reached 90.1%.
- Where: research/data/open_prototype/lipi/metadata_filtered.csv (id column). No note in this chunk checks raw-ID order.
- Old label: none. No note tests catalog order.
- Why it is alive: Families from the 033, 415, 110 and 400-158 classes sit in unbroken runs of raw IDs. That is how a set of identical copies looks when entered together. The H-1302 notes name copy families and leave them unmeasured. The raw-ID runs measure them.
- What it would mean if true: The 22-object series, the 033 packet and the 415 family are copy families. That lowers the count of independent witnesses, and it turns the variants into differences between witnesses of one text (entry 11).
- Cheapest next move: Check whether the runs follow the excavation prefix or a cataloguer's batch. Repeat the adjacency count on the 033 frame and the 415 frame alone.

### 11. The H-2218 series is one text with 22 witnesses and a three-slot formula, and textual criticism has not been run on it
- What was seen: All 22 objects fit one three-role template: side 3 is always the 15x form, and sides 1 and 2 swap between the 861 form and the 700-03x form. Hidden-side reconstruction gets 66 of 66 role families right and 64 of 66 exact texts right. The two misses are the two variants. Side-index majority gets 47 of 66, and global majority 22 of 66 (both from the reconstruction note). Zero of 375 non-H rows carry two of the three H role families. The notes report a shuffle test chance p of about 3e-11 (the chance that a shuffle this extreme happens by luck), marked as not a population statistic. Meadow and Kenoyer 2000 say the 22 tablets carry the same set of inscriptions, not always in the same sequence or orientation.
- Where: the H-2218 to H-2239 side-role, reconstruction and template-recurrence notes (archive folder). Data: research/data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv (397 rows, present).
- Old label: series-specific copied problem. Not promoted. The shuffle p is labelled not a population statistic.
- Why it is alive: Twenty-two witnesses of one text, with a few variant readings, is the input to textual criticism, which reconstructs a family tree of copies from their differences. Nobody built the witness table and tree. The notes call copying a confound. For text criticism, copying is the method.
- What it would mean if true: The series is one short text copied 22 times, with two side orders and a few variant readings. The question becomes which copies share errors, which gives a tree of copies instead of a sign contrast.
- Cheapest next move: Build a 22-by-3 table of exact side texts from the existing template file, count pairwise differences, and build a tree. This runs in seconds.

### 12. Every panel of H-2219 carries a stroke group beside its sign, and the stroke count may be the local tail
- What was seen: The three public thumbnails of H-2219 (97 by 57, 99 by 49, 98 by 58 pixels) are described as one complex sign plus a stroke group (A), a rhombus-like sign plus a stroke group (B), and a V or oval-like sign plus a stroke group (C). The local sides are A +861-003+, B +700-034+, C +156-003+ (rows 856.1 to 856.3). The tails are 003, 034 and 003.
- Where: research/docs/archive/h2219_public_image_lead_audit.md. Row list: research/data/open_prototype/reports/h2219_public_image_leads.csv (named, not checked here).
- Old label: thumbnail grade. Can support side-label triage. Cannot validate segmentation, stroke counts or orientation.
- Why it is alive: This is the only object in the series with side images. The stroke group is how the Indus numerals are written, and each tail is the part of the token that looks numeric. The stroke counts are a single cheap measurement that could show whether the tails are counts.
- What it would mean if true: The part before the dash is a sign, and the tail is a count. 003 would be three strokes, and 034 a count of four with a sign. The sign-plus-count pattern would run through the corpus.
- Cheapest next move: Download the three thumbnails and count the separate dark marks in each stroke group with a short script. Counts of 3, 4 and 3 would fit the tails.

### 13. Direction codes are the hinge for several rejections, and they disagree between families
- What was seen: All 33 companion rows that carry 033 or 034 next to the 400-740-176 long row are coded R/L (computed). Among the long rows of that family, 28 are R/L and 4 are L/R. In the 415 family the 034 companions are coded differently: H-938 1818.2 is R/L, while H-939 1819.1 and H-1284 4069.2 are L/R. H-2145 has no code. Parpola (2019) says both faces read left to right in this category. The rejection of 034 = 415 rests on component order "under recorded R/L", which the H-786 side-policy note states.
- Where: direction column (dir.) of research/data/open_prototype/lipi/metadata_filtered.csv. Notes: the H-786 and H-941 side-policy gate and the H-938 and H-939 notes.
- Old label: component-order negative pressure against a direct 034 = 415 under the recorded R/L. Not promoted and not overriding.
- Why it is alive: The main objection to 034 = 415 depends on direction codes that no note checked against a plate, and the codes disagree between families. If the codes are reversed for one family, a convention for recording direction, the component-order objection flips, and 034 = 415 reopens. Parpola's left-to-right statement and the recorded R/L codes contradict each other, and both stay alive until one plate settles it.
- What it would mean if true: The direction column is a recording convention, not a fact of the inscription. Several old rejections would go with it.
- Cheapest next move: One plate with a direction label. Read H-938 or H-939 side A and side B and record which way the companion and the frame run. If the plate reads opposite to the metadata, the direction column is inverted for that family.

### 14. The three-part 415 picture sits on side A of four objects and never on side B
- What was seen: The broad 415 pattern runs in a fixed three-part order: a triangular pennant on a stem, then a split-leaf or fork, then a rake or vertical bundle. It appears on side A of H-786, H-938 (A and A bis), H-940 and H-941 (A and A bis). It does not appear on side B of H-786, H-938, H-940, or H-941. H-939 side A shows a partial version under damage (its local row .1 reads +700-034+). The notes call these candidate panels and hold them back because side labels are unresolved.
- Where: research/docs/archive/h786_h941_source_a_pattern_recheck.md and the 415 side-mapping adjudication. The verified panel crops are named in those notes (not present at research/tmp here).
- Old label: visually relevant candidates. Quarantined behind side policy. Whether 415 is one form or several is an open question.
- Why it is alive: The same three elements, in the same order, on the same face across four objects is a composite picture, not noise. If 415 is a three-part picture of a physical thing, the sign is pictographic and the fine-form question is about one element. Meaning first: a pennant on a stem, a forked leaf and a rake-like bundle could be plant or reed parts. That is a guess to be tested, not a finding.
- What it would mean if true: 415 is a picture of a material object, and the frame it sits in names a quantity or product beside a fixed obverse text.
- Cheapest next move: Put the four side-A panels next to each other at equal scale and mark which element changes. A change in one element would be the fine-form split the notes asked for.

### 15. The CISI Pakistan scan is a free route to plates for 23 of the 33 family objects, and the notes checked it only for two out-of-range objects
- What was seen: The notes say the CISI Pakistan photo section covers Harappa objects H-266 to H-1019, with gaps. The Internet Archive copy has page images (H-940 at 3258 by 4550 pixels; H-786 on page n359; H-939 and H-940 on n374). The OCR text file pakistan_djvu.xml is named in the notes. Of the 33 family objects, 23 are inside that range (computed): H-308, H-309, H-312, H-313, H-314, H-316, H-317, H-352 to H-357, H-787, H-933 to H-937, H-960, H-978, H-979, H-987. The notes grep-checked only H-1302 and H-1303, which are outside the range. The H-933 and H-960 note reached "no object-level image" by web search, not by the scan.
- Where: research/docs/archive/h1302_h1303_cisi_public_route_check.md, h933_h960_034_contrast_source_audit.md, h355_double_short_side_clarification_audit.md, h940 recrop note. tmp/cisi_pakistan_ocr/pakistan_djvu.xml (named; not present at research/tmp here).
- Old label: the public CISI volume is not the route for H-1302 or H-1303. CISI 3.1 or HARP is required. No public image was found.
- Why it is alive: The in-range members of the 033 and 034 pairs need no source-holder reply. The Internet Archive scan is a free route at page level, and the notes already pulled one page from it. The "nothing found" results came from web and blog searches, not from the volume.
- What it would mean if true: The 033 against 034 contrast can be checked on 23 objects now, without waiting for the Harappa and Fuls replies.
- Cheapest next move: Search the OCR file for H-933, H-960, H-308, H-309, H-312 to H-317 and H-352 to H-357, and map each hit to its page image.

### 16. The Gulf-type queue has 2 verified objects and 14 unmapped rows, and an Ur grave context could supply the same-context pairing the forger gate allows
- What was seen: The queue file (research/data/meluhha/gulf_type_indus_external_queue.csv, 22 rows, Laursen 2010 Table 1 entries 6 to 27, present) gives 2 verified object identities (entries 20 and 21, Ur Gadd nos. 15 and 16, rows 3899.1 and 3898.1), 6 candidates (entries 12, 13, 14, 16, 18, 22), and 14 rows with no mapping. Entry 16 (Ur Gadd no. 2) has a candidate local row 3897.1, which the priority note does not name. Entry 18 has a weak candidate 5231.1. Entry 13 (Failaka 279) has 3 grooves, entry 22 (Girsu) has 2, and most other rows with a groove count have 1. The Ur grave contexts recorded are PG 401 and the shaft fill leading to PG 1847.
- Where: research/data/meluhha/gulf_type_indus_external_queue.csv. Note: research/docs/archive/gulf_type_indus_external_queue.md.
- Old label: no anchors so far. Site overlap and Indus-only seals give no phonetic anchor. BM 120573/U.7683 shows cuneiform-only objects help only with a shared Indus object.
- Why it is alive: The forger gate's second condition accepts a documented same-context label or seal pairing. Two Indus objects already have documented grave contexts at Ur. A grave inventory listing a cuneiform object in PG 401 or PG 1847 would meet that condition with no new kind of evidence. The Susa object (Amiet no. 1643, queue entry 14) comes from Susa, where Proto-Elamite and Linear Elamite tablets were found, and Proto-Elamite numerals have been read. The queue never checked the object for numeral strokes.
- What it would mean if true: One grave with an Indus seal and a readable name is the first bilingual anchor, and a name slot gives the first sounds.
- Cheapest next move: Pull the Ur grave lists for PG 401 and PG 1847. Check the candidate 3897.1 for Gadd no. 2. Look at the Susa object's other faces for numeral strokes.

### 17. Triangular-section tablets: the two template classes may be two directions round a three-faced prism, and H-355 may carry a third face
- What was seen: Triangular-section TAB:I objects in the Harappa rows (computed, one count per object): 35 have 2 sides, 32 have 3 sides, 6 have 1 side. That is the one contrary number, and it means triangular section does not force three sides. All 22 H-series objects are triangular with 3 sides. Inside the series, the two template classes are 13 objects (861, then 700-03x, then 15x) and 9 (700-03x, then 861, then 15x). On a three-faced prism the faces run round in a cycle, so the two classes read the cycle in opposite directions. H-355 (triangular, 3 rows: +400-740-176+, +700-033+, +700-033+) has two identical short rows. H-1344 to H-1347 (triangular, 2 rows each) each have a long row and a 033 row.
- Where: cross-section and sides columns of research/data/open_prototype/lipi/metadata_filtered.csv. Notes: the side-role template note, the H-355 double-short-side audit, the dimension side-order note (which names physical adjacency on triangular tablets as the next check and never ran it).
- Old label: side order is a catalog or editorial convention. H-355's double row is a catalog artifact unless a three-side source shows two distinct sides.
- Why it is alive: A triangular prism has three faces, so a three-row record is the natural form, and a two-row record is missing a face. H-355's identical short rows could be faces 2 and 3 with the same text, and the 2-row prisms (H-1344 to H-1347) would be partial records. The cycle gives the 13 to 9 split a physical cause that the notes named and did not test.
- What it would mean if true: The side order is a geometry: a fixed text wrapped round a prism and read in one of two directions. H-355 is a full three-face record of the 033 formula, and the 2-row prisms are cut short.
- Cheapest next move: Read the end-profile markers in the public Fig. 4 for the 22 series objects and check each marker's orientation against the local side order. Ask for the face count of H-1344 to H-1347 in the CISI 3.1 route.

### 18. Some excavation numbers may be fused, and H-941's is two register numerals run together
- What was seen: H-941's excavation number is 2703464 in the metadata. The CISI data register lists the numerals 3464 and 2703 before HM 480, and the note reads the metadata as fusing them. Other seven-digit excavation values in the family include H-1303 (2357879), H-1346 (2894900), H-1345 (3509902) and H-1347 (1262896). H-1344 reads -752, a negative value.
- Where: research/docs/archive/h786_h941_415_side_mapping_adjudication.md. Metadata excavation-idno column.
- Old label: source-check flag.
- Why it is alive: If one number was fused at entry, others may be too. Each fused value points silently at the register entry of another object. Splitting them could re-link objects to CISI register entries, including some that the notes list as source-dark.
- What it would mean if true: Some object-to-register links in the corpus are wrong, and some source-dark objects already have a register entry under their split number.
- Cheapest next move: For each seven-digit excavation value, test whether its two halves appear as numerals on the CISI data-register pages.

---

## Sources on disk

- research/data/open_prototype/lipi/metadata_filtered.csv: the working corpus, 5,679 rows. Columns include id, cisi (object name), excavation-idno, type, cross-section, sides, dir. (direction), class, text. Present.
- research/data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv: the 397-row multi-side queue. Present.
- research/data/meluhha/gulf_type_indus_external_queue.csv: 22 external Gulf-type rows, Laursen 2010 Table 1 entries 6 to 27. Present.
- research/data/open_prototype/reports/: other CSV and JSON reports the notes name (h2218_h2239_*, h2147_*, h2148_*, h1302_h1303_*, h2219_public_image_leads.csv, h233_public_slide_visual_lead_summary.json, h786_h941_* and others). Named in the notes; not opened by me.
- tmp/ folders the notes name, not present at research/tmp in this checkout (I did not search the rest of the tree): tmp/cisi_pakistan_ocr/pakistan_djvu.xml (CISI Pakistan OCR); CISI Pakistan page images (n359, n374, data pages 478 and 479) and the Internet Archive IIIF and JP2 copies; tmp/h2147_source_route/kenoyer_meadow_1997_harappa.pdf (Meadow and Kenoyer 1997); tmp/h2148_h2100_h2152_110_route/ (Kenoyer 2005, Kenoyer and Meadow 2010, Kenoyer 2000, RIHN 2007 PDFs); tmp/h1302_h1303_direction_prior_work/daggumati_revesz_2021_allographs_nature_article.pdf (sha256 1061899319d3…, 1,616,753 bytes); tmp/parpola_2019_bone_rods.txt (Parpola 2019 text); tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/ (verified panel crops of the 415 side-A panels).
- Source-holder requests in the notes (Harappa, HARP, Fuls route): sent by email, no reply recorded in the notes. Not on disk.

## Ideas named but never run

1. Physical side adjacency on triangular-section tablets (dimension side-order note, next step; never run).
2. Check whether recurrent side marks correlate with physical side position, object size, manufacturing group, find context or longer-text neighbours (side-order and dimension notes).
3. Higher-resolution Fig. 4 or source plates for all 22 H-series tablets (Fig. 4 visual-availability note).
4. Blind comparison of outside-control 110 forms (H-2100, H-2152, Kanmer 4881.1) against H-940 B, the H-2147 right component and the H-2148 one-sign panel, with reviewers unable to see which object is which (110 route check and recrop note).
5. Crosswalk between the inline glyphs of the 2021 Nature article and the local numeric sign strings (provenance gate; never built).
6. Companion-text sign-inventory gate: check whether Parpola's obverse recurrence maps local 415 and 016 to one sign-list item (stress gate).
7. Object-specific side-label notes for H-786 and H-941 from CISI 3.1 tables or HARP end matter (side-policy gate).
8. Route checks for H-2100, H-2152 and Kanmer 4881.1 through the RIHN 2012 Kanmer volume, row "project08-1285" (outside-control note).
9. Local and CISI route check for H-1822, which the Nature article names (its local raw ID is 550, not 1822).
10. Validate the side-mark structure of the mixed short-long and TAB:B and TAB:I core queues on their own, without importing the H-series template (template recurrence note).
11. CISI 3.1 or HARP object records for H-1521 to H-2583 (the group-3 request route).
12. Compare the public A, B and C labels on H-2219 against CISI plate labels, Fig. 4 order and local side order (H-2219 audit, cross-check step).
13. Shape claims: the bharatkalyan97 page titled "shapes of tablets convey information" is named but its claim was never tested. The metadata has shape and cross-section columns that could test it.
14. Gulf-type acquisitions named in the queue: Kjaerum 1994 and 1983 catalogue nos. 279 and 319; Mitchell 1986 figures 106 to 117; Amiet 1972 no. 1643 and 1973 pl. 23a-b; Sarzec and Heuzey pl. 30.3a-b; Gadd 1932 pl. I nos. 2 to 5, 17 and 18; mapping of the 14 unmapped rows.
15. A synthetic same-site, same-length forger control for the bridge test in the Gulf-type queue (the forger rule names it; never generated).
16. Captions binding the two public Blogger object-panel candidates for H-1302 and H-1303 (named as a condition before use; never done).
17. Image-side check of the H-2219 public thumbnails for side order (named; no image measured).
18. Source image of all three rows of H-355, plus the direction basis for both short rows (named as the H-355 request; not sent as a separate item).
19. The Mahadevan side-ordering criterion, which the notes say is provisional for multi-side objects. Finding the written rule would show whether the 13 to 9 split is an analytic choice (side-policy gate; never looked up).
20. The Daggumati and Revesz page-6 inline glyphs (named; crop recorded in the note; not compared to local strings).
