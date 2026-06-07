# H-2145/H-2147/H-2148 Source Route Recheck

Date: 2026-05-26

## Question

Can the new Parpola reverse-side targets H-2145, H-2147, and H-2148 move from prior-work pressure into source-grade side/sign evidence?

Correction added 2026-05-26: H-2148 no longer remains route-dark. A later source pass found Kenoyer 2005 Figure 14.1, which publicly routes `H2001-5142` and gives count-level panel mapping. See [H-2148 / H2001-5142 Kenoyer 2005 Public Visual Route](h2148_kenoyer2005_public_visual_route.md).

## Result

Partly. The original pass improved only H-2147; the later H-2148 pass adds a second public visual route and gives count-level row-to-panel mapping for H-2148.

- H-2147 now has a public visual route through the H95-2514 hook, but still no local side/sign mapping.
- H-2145 remains route-dark in the checked local/public layer.
- H-2148 now has a public visual route through Kenoyer 2005 Figure 14.1 -> `H2001-5142`; its one-sign and three-sign panels match local rows `481.2 +110+` and `481.1 +520-220-415+` by sign count.

Accepted decipherment claims remain unchanged: no Parpola/local crosswalk, no local `110` identification, no `034=415`, no sign value, and no translation.

## Local Rows And Hooks

| Object | Local rows | Local source hook | Local status |
| --- | --- | --- | --- |
| H-2145 | `827.1 +700-034+`; `827.2 +074-220-415+` | `H97-3283Figure 16.04` | Complete two-side tablet row, direction missing, acquisition target |
| H-2147 | `673.1 ]110+`; `673.2 ]220-415+` | `H95-2514Figure 27.14` | Fragmentary/poor two-side row, damage blocks sign mapping |
| H-2148 | `481.1 +520-220-415+`; `481.2 +110+` | `H2001-5142Figure 48.01`; public Kenoyer 2005 Figure 14.1 | Good two-side row, exact `415` comparator, public visual route with count-level mapping |

Local row anchors:

- `data/open_prototype/lipi/metadata_filtered.csv:615-616`
- `data/open_prototype/lipi/metadata_filtered.csv:909-910`
- `data/open_prototype/lipi/metadata_filtered.csv:1146-1147`

## H-2147 Route Improvement

The H-2147 local source hook is `H95-2514Figure 27.14`.

A public Harappa PDF route now exists locally and is rendered:

- Meadow and Kenoyer 1997, "Excavations at Harappa 1994-1995: New Perspectives on the Indus Script, Craft Activities, and City Organization"
- Public URL: `https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf`
- Figure 10 page has visible item `17`.
- The continuation table maps `10.17` to `H95-2514`, excavation unit `4461-04`, "Tablet (incised), fired", "2-sides", "steatite", "Trench 11, dump".
- Stored visual packet: [H-2147 / H95-2514 public visual route](h2147_h95_2514_public_visual_route.md).
- Accession concordance: [H-2147 Figure 10 / Figure 27 accession concordance](h2147_fig10_fig27_accession_concordance.md).

This is useful because it confirms a public object-level route for the H95-2514 hook and gives a two-side steatite tablet context.

Later correction:

- A raw-page recrop from the embedded PDF image shows the H-2147 Figure 10.17 candidate panel is not a clean single-sign panel.
- It contains at least a left vertical/U-like component plus a right branching/figure-like component.
- The H-2147 visual lead is therefore component-level pressure only until source-side/sign notes connect a visible component to local `673.1 ]110+`.

It is not enough to accept a crosswalk:

- `10.17` and `27.14` are reconciled at accession/object level through `H95-2514`, but the source behind local `Figure 27.14` still needs direct citation.
- The local row is fragmentary: `]110+` and `]220-415+`.
- The public figure does not assign local row numbers or local numeric sign strings.
- The lower visible panel makes Parpola's sign-no.-41 clue inspectable only at component level; Parpola's sign no. 41 cannot be equated with local `110` from this alone.

Decision: H-2147 becomes `public_visual_route_no_local_mapping`, not `source_grade_side_mapping`.

## H-2145 Route State

The H-2145 local source hook is `H97-3283Figure 16.04`.

Checked routes:

- Local exact searches for `H97-3283`, `H-2145`, and `Figure 16.04`.
- Public exact web searches for `H97-3283`, `H-2145`, and `Figure 16.04`.
- Harappa "Tiny Steatite Seals" route for 1997 Trench 11 tablet groups.

Result:

- No exact public panel route found for H97-3283 in the checked layer.
- The Harappa 2000 Tiny Steatite paper is relevant for 1997 Harappa tablet context, but its visible Figure 4 list does not include H97-3283.

Decision: H-2145 remains `route_dark_with_prior_work_clue`.

## H-2148 Route State

The H-2148 local source hook is `H2001-5142Figure 48.01`.

Original checked routes:

- Local exact searches for `H2001-5142`, `H-2148`, and `Figure 48.01`.
- Public exact web searches for `H2001-5142`, `H-2148`, and `Figure 48.01`.
- Kenoyer/Meadow 2010 public Harappa PDF, which describes HARP object/photo database and CISI 3.1 publication context but has no exact H2001-5142 hit in the extracted text.

Corrected route:

- Kenoyer 2005 Figure 14.1 publicly identifies `H2001-5142 / 11759-01` as an incised fired-steatite flat rectangular tablet from foundation rubble.
- The visible item has a one-sign panel and a three-sign panel.
- Local H-2148 has exactly one one-token row, `481.2 +110+`, and one three-token row, `481.1 +520-220-415+`.
- Stored visual packet: [H-2148 / H2001-5142 Kenoyer 2005 Public Visual Route](h2148_kenoyer2005_public_visual_route.md).

Decision: H-2148 upgrades to `public_visual_route_count_mapped`, not to sign-value or Parpola sign-no.-41 proof.

## Decision Gate

Current state:

| Object | Status after recheck | Can it support Parpola/local crosswalk now? |
| --- | --- | --- |
| H-2145 | `route_dark_with_prior_work_clue` | No |
| H-2147 | `public_visual_route_no_local_mapping` | No |
| H-2148 | `public_visual_route_count_mapped` | Count-level row mapping only; no Parpola/local crosswalk |

Next acquisition request should ask for:

- H-2145 all-side panels and side labels for `H97-3283`.
- H-2147 exact source-side panels and the source behind local `Figure 27.14`.
- Higher-resolution H-2148 panels and side labels for `H2001-5142`, since the public scan is enough for count-level mapping but not diagnostic sign-list proof.
- Direction/orientation basis for each object.
- Source transcription/sign-list convention for Parpola `VIIII`, sign no. 41, local `+700-034+`, local `+110+`, and local `+220-415+`.

No translation or sign value is admitted before that.
