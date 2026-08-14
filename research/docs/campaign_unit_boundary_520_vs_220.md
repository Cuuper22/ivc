# Unit Boundary Campaign: `520`, `220-415`, or `520-220`

Date: 2026-05-26

## What This Note Is

This note reports a structural campaign on the Indus sign sequences. The numbers like `520`, `220`, and `415` are catalog codes for individual signs, not values or readings. The campaign asks where the unit boundary falls in sequences that contain these signs: is the reusable unit the single sign `520`, the pair `220-415`, or the pair `520-220`?

## Result

The best current parse is not a single frozen reading. It is a construction — a grammatical frame with slots:

```text
520-H-C

520 = opener / frame / classifier-like sign
H   = slot-2 head selected by 520
C   = slot-3 closure / class / complement selected by H
```

Within that construction, `520-220-415` is the strongest branch. `520-220` is a real subframe, and `415` is its default closure, especially at Harappa. But `220-415` also has independent life outside `520`, so the boundary cannot be collapsed to one flat chunk.

No phonetic value, lexical value, language identity, or translation is accepted.

## Data Stored

- `data/open_prototype/reports/campaign_unit_boundary_520_start_rows.csv`
- `data/open_prototype/reports/campaign_unit_boundary_520_start_second_summary.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_occurrence_rows.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_frame_summary.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_next_summary.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_415_rows.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_415_prev_summary.csv`
- `data/open_prototype/reports/campaign_unit_boundary_exact3_520_220_related_rows.csv`
- `data/open_prototype/reports/campaign_unit_boundary_exact3_520_220_related_summary.csv`
- `data/open_prototype/reports/campaign_unit_boundary_520_vs_220_summary.json`
- `data/open_prototype/reports/campaign_unit_boundary_520_220_to_415_effects.csv`
- `data/open_prototype/reports/campaign_unit_boundary_520_start_site_second_summary.csv`
- `data/open_prototype/reports/campaign_unit_boundary_520_head_closure_profile.csv`
- `data/open_prototype/reports/campaign_unit_boundary_520_second_site_type_addendum.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_next_site_type_addendum.csv`
- `data/open_prototype/reports/campaign_unit_boundary_220_next415_enrichment_addendum.csv`
- `data/open_prototype/reports/campaign_unit_boundary_damage_open_addendum.csv`
- `data/open_prototype/reports/campaign_unit_boundary_validation_addendum_summary.json`
- `data/open_prototype/reports/campaign_unit_boundary_hypothesis_rank.csv`

## What Changed

### 1. `520` is a broad opener with restricted heads

`520` starts 263 rows — 263 inscriptions in the filtered corpus, or 4.63 percent of it.

The slot after initial `520` is concentrated on a few signs:

- `520-220`: 59 rows
- `520-033`: 52 rows
- `520-240`: 44 rows
- `520-233`: 19 rows
- `520-070`: 13 rows

The top three followers, `220`, `033`, and `240`, account for 155/263 start-`520` rows, or 58.94 percent.

This makes `520` look like an opener/frame/classifier sign, not a one-off lexical sign.

### 2. Slot 2 predicts slot 3

The strongest new structural result is that the second sign after `520` selects a preferred third sign:

| start frame | count | dominant closure | closure count | closure share | top two closures |
|---|---:|---|---:|---:|---|
| `520-220-*` | 59 | `415` | 28 | 0.47 | `415:28`; `<END>:7` |
| `520-033-*` | 52 | `705` | 29 | 0.56 | `705:29`; `706:16` |
| `520-240-*` | 44 | `002` | 29 | 0.66 | `002:29`; `<END>:7` |
| `520-233-*` | 19 | `240` | 6 | 0.32 | `240:6`; `803:4` |
| `520-070-*` | 13 | `255` | 3 | 0.23 | `255:3`; `921:2` |

This is stronger than the previous one-branch story. It suggests a constructional grammar: `520` opens a frame, slot 2 picks the head, and slot 3 is a closure/complement distribution tied to that head.

### 3. `220-415` is real but not owned by `520`

`220` occurs 477 times. It is followed by `415` 91 times.

The previous sign before those 91 `220-415` frames is diverse:

- `520`: 28
- `318`: 11
- `740`: 6
- row start: 5
- `000`: 5
- `845`: 5
- `176`: 4

So `220-415` is a portable chunk or head-closure tendency. It is not exclusive to the `520` frame.

### 4. `520` strongly conditions `220 -> 415`

Among `220` occurrences with a known next sign:

- `P(next=415 | prev=520) = 28/60 = 0.4667`
- `P(next=415 | prev!=520) = 63/330 = 0.1909`
- risk ratio: 2.44
- odds ratio: 3.71

That is the main reason `520-220` remains a real subframe. `520` changes the continuation behavior of `220`.

### 5. The effect is site/type conditioned

The enrichment is not equally strong everywhere. It varies by find site (Harappa vs Mohenjo-daro) and by object type — `TAB:I` is an incised tablet class, `SEAL:S` a stamp seal class:

- All known-next `220`: `0.4667` vs `0.1909`, odds ratio 3.71
- Harappa: `0.7600` vs `0.2451`, odds ratio 9.75
- Mohenjo-daro: `0.2667` vs `0.2318`, odds ratio 1.21
- TAB:I: `0.8667` vs `0.3333`, odds ratio 13.00
- Harappa TAB:I: `0.9286` vs `0.3529`, odds ratio 23.83
- Mohenjo-daro SEAL:S: `0.2414` vs `0.1500`, odds ratio 1.80

So the exact `520-220-415` formula is heavily Harappa/TAB:I-shaped. It should not be generalized as a pan-IVC lexical unit without controls.

## Ranked Boundary Decision

### 1. `520-H-C` construction

This is the current lead.

`520` is the opener/frame. Slot 2 is a head. Slot 3 is the head-conditioned closure or complement.

Why it wins:

- `520` has multiple strong followers.
- The main followers have different closure profiles.
- `520-033` and `520-240` are not noise; they are parallel branches.
- `520-220-415` becomes one branch of a broader grammar, not an isolated lucky formula.

Prediction:

- `520-033`, `520-240`, and `520-220` should differ in companion-side classes, object-type distributions, and continuation tails.

### 2. `520-220` subframe

Still strong, but now nested inside `520-H-C`.

Why it survives:

- `520-220` enriches `415` hard relative to non-`520` `220`.
- Exact `520-220-415` has 17 rows.
- Bare `+520-220+` rows exist.
- Previous campaign showed Harappa standardization and Mohenjo-daro terminal diversity.

Prediction:

- `520-220-X` should have a limited terminal class and a distinct side-pairing profile from `520-033-X` and `520-240-X`.

### 3. Portable `220-415` chunk

Real but secondary for this campaign.

Why it survives:

- `220-415` occurs 91 times.
- It appears after many previous signs.
- It may be a reusable head-closure chunk embedded in several frames.

Why it loses as the main unit:

- `520` nearly doubles or triples the chance of `415` after `220`.
- `520` is the largest single previous sign before `220-415`.
- Exact `520-220-415` dominates related exact triplets.

Prediction:

- Other `A-220-415` frames such as `318-220-415`, `740-220-415`, and `845-220-415` should form their own object/site/side classes if `220-415` is a portable formula.

### 4. Frozen `520-220-415` whole formula

Possible but lower-ranked.

Why it remains possible:

- Exact `+520-220-415+` is a major repeated formula.
- Harappa repeats it heavily.

Why it is not enough:

- `520-220` also appears bare.
- `520-220-X` has other terminals.
- `520` has parallel branches with their own closure systems.
- `220-415` occurs outside `520`.

Prediction:

- If source checks collapse singleton `X` values and companion-side distinctions do not matter, this can rise again as a Harappan frozen formula.

## Semantic Consequences

### Winners

1. Formulaic administrative label

This now leads. `520` behaves like a frame marker; slot-2 heads identify formula families; slot-3 signs close or classify them. Harappa exact repetition fits standardized administration.

2. Title or office formula

Still strong. `520` could introduce title/authority frames, with `220`, `033`, and `240` as head terms and `415`, `705/706`, and `002` as closures/classes.

3. Identity or house formula

Still live, especially if `220-415` clusters with iconography, object families, or findspots. But `520` looks more grammatical than clan-specific.

### Losers

1. Simple fish/commodity phrase

Weaker now. The `520-H-C` pattern says the fish/leaf pressure on `220` cannot carry the whole reading. `220` is one head in a larger construction.

2. Direct Parpola text7 bridge

Still downgraded. Parpola's catalog is an external sign-numbering system; this campaign works entirely in our local sign namespace and measures structure, not identity across catalogs. Parpola sign60 pressure stays a clue, not a boundary proof.

## Next Campaign

Run the `A-220-X` frame campaign.

Targets:

- `520-220-X`
- `318-220-X`
- `740-220-X`
- `845-220-X`
- row-start `220-X`
- `000-220-X`
- `176-220-X`

Goal:

Decide whether each previous sign before `220` selects a different terminal distribution. If yes, the grammar is `A-220-X`, where `A` is a frame/operator and `X` is selected by the frame-head pair. If no, `220-415` is the stronger chunk.

## Bottom Line

The strongest current statement is:

`520` opens a construction. Its second slot is a head. Its third slot is a head-conditioned closure. `520-220-415` is the strongest branch of that construction, heavily standardized at Harappa and especially TAB:I. `220-415` is real and portable, but the `520` frame changes its behavior enough that the best parse is constructional: `520-H-C`, with `520-220-415` as one branch.
