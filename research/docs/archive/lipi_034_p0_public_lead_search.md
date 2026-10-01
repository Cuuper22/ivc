# Lipi 034 P0 Public Lead Search

Date: 2026-05-25

This note is a lead search. A previous note produced a ranked list of objects worth acquiring; the six most urgent are labelled P0. Here each of those six is chased through the open literature to see what, if anything, is already public.

The result is deliberately mundane: URLs, page numbers, plate labels, and the exact wording of what each source does and does not say. Prior work is evidence to interrogate, not authority to obey. Gated, used below, means an object is visible in a source but still barred from decipherment use until a specific missing check is done.

Question:

```text
Do the six P0 Mohenjo-daro 034 crosswalk-acquisition targets have public object/source leads, and do any of them already contain extractable sign data?
```

Input:

- `data/open_prototype/reports/lipi_034_mayig_acquisition_priority_objects.csv`

Output:

- `data/open_prototype/reports/lipi_034_p0_public_leads.csv`
- `data/open_prototype/reports/lipi_034_p0_public_leads_summary.json`

## Result

```text
P0 targets checked: 6
public lead rows stored: 6
object-level or image leads: M-2104;M-315;M-1206;M-685;M-1584
route or catalogue leads: none remaining after M-315/M-685 follow-up
no relevant public hit in checked queries: M-1963
accepted decipherment claims: 0
```

## Object Leads

One entry per P0 object: our transcription, the public source found, the exact datum extracted, and what it may be used for.

### M-2104

Local lipi text:

```text
+151-097-700-034+
```

Public lead:

- Source: Parpola 2019, "Inscriptions Incised on Harappan Ivory/Bone Rods"
- URL: <https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf>
- Extracted datum: Parpola treats M-2104 as text no. 12. In the prose, the rod text begins with `UIII` ("three pots"), then signs 15 and 1. The closest tablet parallels M-478, M-480, and M-1425 begin with `UIIII` ("four pots"), then signs 15 and 107.

Use:

- This is the first actual public prior-sign datum for a P0 `034` object.
- It is not accepted as a crosswalk mapping yet. It must be checked against Fig. 1 and the CISI photo, because Parpola says the chart normalizes sign shapes and direction rather than reproducing the rod forms.

Immediate next extraction:

```text
Compare Parpola text no. 12 sequence UIII + 15 + 1 against lipi +151-097-700-034+.
Do not force a four-token lipi row into a three-unit Parpola prose summary until Fig. 1 and CISI image are inspected.
```

### M-315

Local lipi text:

```text
+390-034-002-374-228-741+
```

Public lead:

- Source: Kenoyer and Meadow 2010, "Inscribed Objects from Harappa Excavations 1986-2007"
- URL: <https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf>
- Extracted datum: M-315 is grouped with M-313 and M-316 as Mohenjo-daro examples of similar no-animal-motif seal types, with the route `CISI 1, p. 78`.

Use:

- Follow-up source probe inspected the route. CISI Vol. 1 IA leaf `n113` / printed p. 78 is source-visible and labels `M-315 A` and `M-315 a` under `MOHENJO-DARO 313-317 SEALS` / `no iconography; silver`.
- CISI Vol. 1 IA leaf `n403` / printed p. 368 is also source-visible and shows `M-315 1395 VS 1190 ASI 63.10.117 HU 318`.
- This upgrades M-315 to source-visible object binding — a published page tying our row to a pictured object — but not to accepted numeric sign mapping. Exact `034` identity, direction, and source transcription convention remain gated.
- Targeted local contrast: 37 rows match `390-X-002`, only one matches `390-034-002`, and only three rows begin `390-034` (`Ai-7`, `H-335`, `M-315`).

### M-1206

Local lipi text:

```text
+520-220-034+
```

Public lead:

- Source: Bhaskar 2022, "Indus zoomorphism and its avatars"
- URL: <https://www.harappa.com/sites/default/files/pdf/Bhaskar2022_IJHS_57_3_1.pdf>
- Extracted datum: Fig. 3 identifies M-1206 as the right-hand image in a two-object figure with M-635 and says the images are from CISI.

Use:

- This is an object-level image lead.
- It does not contain sign transcription, but it gives an image-bearing public route back to CISI.
- Follow-up source probe rendered Fig. 3 and found a real downgrade: the caption says `M-1206`, but the running text says `M-2016 (Fig. 3)`. Treat this lead as source-gated — barred from use until a published source settles it — until CISI/HARP confirms object identity and all-side row binding.

### M-685

Local lipi text:

```text
]034-204+
```

Public lead:

- Source: CISI Vol. 2 p. 37 follow-up plus Bhaskar 2022 supplemental S1 catalogue after CISI
- CISI URL: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n71/mode/1up>
- S1 URL: <https://storage.googleapis.com/cahcblr-pdfs/assets/ijhs/S1-IndusZoomorphicIconCatalogue.pdf>
- Extracted datum: CISI p. 37 labels `M-685 A` and `M-685 a`; S1 lists M-685 as a Unicorn row with text present and marker `b`.

Use:

- Follow-up source probe inspected the route. CISI Vol. 2 IA leaf `n71` / printed p. 37 is source-visible and labels `M-685 A` and `M-685 a` under `'unicorn' II / SEALS / MOHENJO-DARO 683-686`.
- Bhaskar S1 still matters as an independent secondary catalogue row: it lists `M-685` with text-present marker `b` and Unicorn.
- This upgrades M-685 to source-visible object binding, but not to accepted numeric sign mapping. The local row is fragmentary `]034-204+`, and exact `034/204` token identity remains gated.
- The source route creates an iconography conflict: CISI/Bhaskar say Unicorn, while local lipi says `Bull1`.
- Targeted local contrast: 8 rows contain `204`, exactly one contains both `034` and `204`, and exactly one has adjacent `034-204`: `M-685`.

### M-1584

Local lipi text:

```text
+034+
```

Public lead:

- Source: CISI Vol. 2 p. 232 follow-up plus CISI Vol. 2 p. 440 data-page route
- Plate URL: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n266/mode/1up>
- Data URL: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n474/mode/1up>
- Extracted datum: CISI p. 232 labels `M-1584 A (50 %)` under `MOHENJO-DARO 1579-1587 / GRAFFITI on pottery, rim`; CISI p. 440 has a blurred M-1584 data row.

Use:

- Follow-up source probe inspected the route. CISI Vol. 2 IA leaf `n266` / printed p. 232 is source-visible and labels `M-1584 A (50 %)`.
- The data page on IA leaf `n474` / printed p. 440 is visible but blurred. Conservative extraction is `M-1584`, `2911`, `LF?`, and `D&K, p. 567-N5`; the middle field remains too unclear to code.
- This upgrades M-1584 to source-visible object binding, but not to accepted numeric sign mapping. The local row remains `+034+` as a local code until a source transcription, high-resolution image, or sign-list bridge verifies it.
- Harappa high-resolution/source-transcription request sent as Gmail message `[redacted-msgid]`.

### M-1963

Local lipi text:

```text
+000-034-104+
```

Public lead:

- No relevant object-level public hit found in the checked exact-object web queries.

Use:

- Direct CISI 3.1/HARP/source request. The local row contains uncertainty token `000`, so it cannot anchor a clean crosswalk without source inspection.

## Boundary

The hard line between what was gathered and what the project is allowed to claim.

Accepted translations: 0

Accepted phonetic values: 0

Accepted sign meanings: 0

Accepted source mappings: 0

This is source data gathering. Prior work is evidence to interrogate, not authority to obey. The upgraded objects are now `M-2104` as a public prior-sign datum requiring adversarial crosswalk extraction, `M-1206` as a CISI-derived public image lead with an object-number conflict, `M-315` as a source-visible CISI 1 object binding, `M-685` as a source-visible CISI 2 object binding, and `M-1584` as a source-visible CISI 2 pottery/graffiti object binding. Numeric `034` token mapping remains unaccepted for all of them.

## Next Move

1. Extract Fig. 1 text no. 12 from Parpola 2019 visually, not just from prose.
2. Compare the extracted sequence to `+151-097-700-034+` under all plausible tokenizations.
3. Inspect or acquire CISI photo/record for M-2104 before accepting any sign-number alignment.
4. For M-315, M-685, and M-1584, finish the narrow source gates: high-resolution images, image conventions, direction bases, source transcription conventions, and metadata reconciliation.
5. Send M-1963 straight to direct CISI/HARP request lanes — the parallel track for asking archives directly rather than searching the open literature.
