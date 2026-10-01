# A-220-X Frame Selection Campaign

Date: 2026-05-26

This note establishes the research object that later campaigns work on. Signs in this corpus are numeric IDs. `A-220-X` means: some sign `A`, then the sign `220`, then a variable sign `X`. "Frame selection" is the claim being tested — that `A` changes which `X` can follow. "Entropy" in the tables below measures how spread out the choices of `X` are: low entropy means one `X` dominates. A "copy family" is a set of rows repeating the same text, which really counts as one witness, not many.

## Result

`A-220-X` is a real frame-selection environment in the local corpus.

The previous sign `A` materially changes the distribution of the sign after `220`. This means the current grammatical object is not bare `220`, and not one universal `220-X` chunk. The live object is:

```text
A - 220 - X

A   = frame / operator / domain sign
220 = shared head or slot-bearing sign
X   = frame-conditioned terminal / closure / complement
```

This is a structural result, not a translation. Accepted lexical meanings, phonetic values, and translations remain `0`.

## Data Stored

- `data/open_prototype/reports/campaign_a_220_x_frame_profile.csv`
- `data/open_prototype/reports/campaign_a_220_x_key_frame_rows.csv`
- `data/open_prototype/reports/campaign_a_220_x_key_frame_next_summary.csv`
- `data/open_prototype/reports/campaign_a_220_x_site_type_profile.csv`
- `data/open_prototype/reports/campaign_a_220_x_exact_triplet_by_prev.csv`
- `data/open_prototype/reports/campaign_a_220_x_summary.json`
- `data/open_prototype/reports/campaign_a_220_x_occurrence_flags_addendum.csv`
- `data/open_prototype/reports/campaign_a_220_x_frame_mechanical_addendum.csv`
- `data/open_prototype/reports/campaign_a_220_x_site_type_concentration_addendum.csv`
- `data/open_prototype/reports/campaign_a_220_x_exact_triplet_frame_addendum.csv`
- `data/open_prototype/reports/campaign_a_220_x_validation_addendum_summary.json`
- `data/open_prototype/reports/campaign_a_220_x_duplicate_text_families.csv`
- `data/open_prototype/reports/campaign_a_220_x_frame_independence_profile.csv`
- `data/open_prototype/reports/campaign_a_220_x_hypothesis_rank.csv`

## Corpus Scope

- `220` occurrences: 477
- known-next `220` occurrences: 390
- previous-sign frames before `220`: 89
- key-frame rows inspected: 326
- exact triplet A-220-X rows in the related table: 59

The mechanic validation found no missing or extra occurrence keys versus the prior unit-boundary extraction.

## Main Frame Profiles

| previous A | total | known next | dominant X | dominant count | entropy | immediate status |
|---|---:|---:|---|---:|---:|---|
| `520` | 67 | 60 | `415` | 28 | 2.93 | productive, broad, strongest branch |
| `740` | 52 | 48 | `055` / `003` | 11 / 10 | 3.19 | productive but multi-branch |
| row start | 63 | 44 | `000` | 10 | 3.68 | boundary/damage-heavy, weak formula |
| `000` | 43 | 32 | `000` / `002` / `415` | 6 / 5 / 5 | 3.48 | artifact-heavy until cleaned |
| `176` | 18 | 15 | `235` | 7 | 1.75 | promising but duplicate-family pressure |
| `240` | 15 | 13 | `032` | 10 | 1.15 | strong compact productive candidate |
| `318` | 11 | 11 | `415` | 11 | 0.00 | locked but likely one Harappa TAB:B family |
| `845` | 6 | 5 | `415` | 5 | 0.00 | locked but small Mohenjo-daro family |

## Copy-Family Pressure

Some high-looking frames are not independent evidence units.

- `318-220-415`: 11 rows, 1 unique text, all Harappa TAB:B.
  - Repeated text: `+740-407-590-690-436-255-920-318-220-415-803+`
  - Status: local batch/family formula until independent source/object controls exist.

- `740-220-055`: 11 rows, 1 unique text, all Lothal tags.
  - Repeated text: `+090-740-220-055-001-741-500-705+`
  - Status: Lothal tag-family formula, not general grammar by itself.

- `176-220-235`: 7 rows, 1 unique text, all Harappa TAB:B.
  - Repeated text: `+740-176-220-235+`
  - Status: promising as a local formula family, but not independent.

- `845-220-415`: 5 known-next rows, 2 unique texts, largest text family 4 rows.
  - Repeated text: `+407-845-220-415+`
  - Status: small Mohenjo-daro formula family.

By contrast:

- `240-220-032`: 10 rows, 10 unique texts, 3 sites, 2 object types.
  - Status: stronger productive-frame candidate than raw count alone suggested.

- `520-220-415`: 28 rows, 12 unique texts, largest text family 17 exact `+520-220-415+` rows.
  - Status: real but mixed, with a major Harappa exact-form branch inside a broader productive frame.

## Ranked Interpretation

### 1. A-conditioned frame selection

Lead structural claim.

`A` governs or frames `220`, and the A-220 pair conditions the possible `X`.

Why it wins:

- Different A signs select different terminals.
- `520-220` favors `415`.
- `240-220` favors `032`.
- `740-220` favors `055/003`, not `415`.
- `318-220` and `845-220` lock to `415`, but as local/family formulas.

Current wording:

`220` is a slot-bearing sign whose terminal behavior depends strongly on the previous sign.

### 2. Productive A-220 stems with X endings

Several A-220 pairs behave like stems that take endings or closures.

Strongest current candidates:

- `520-220-X`: broad productive frame with `415` as default.
- `740-220-X`: separate productive frame with `055/003` preference.
- `240-220-X`: compact productive frame with `032` preference.

The `318`, `845`, and `176` branches may be frozen local formulas rather than productive stems.

### 3. Administrative or title formula family

Best semantic model, still unaccepted as a reading.

The frame behavior fits administrative or titulary morphology better than a simple commodity phrase:

- `A`: register, office, authority, domain, or formula frame
- `220`: head, emblem, office stem, identity stem, or slot-bearing class sign
- `X`: closure, subtype, rank, status, or branch marker

The narrow locked frames, especially `318-220-415` and `845-220-415`, are title/office-like but also batch-risky.

### 4. Portable `220-X` chunk

Real but insufficient.

`220-415` is portable, and `220` has many continuations. But the previous sign changes the X distribution too strongly for a universal `220-X` chunk to explain the data.

### 5. Pure graphic or catalog artifact

Necessary adversarial control, not the leading explanation.

Artifact risk is real for damaged rows, `000`, row-start forms, and exact copied families. But `240-220-032` and the difference between `520-220-X` and `740-220-X` make a pure artifact story too weak.

## Semantic Consequences

### Winners

1. Formulaic administrative label

This remains the lead semantic domain. Different frames selecting different terminals looks like a formula system with registers, status markers, object classes, or administrative subtypes.

2. Title / office

Still strong. Locked local frames can be read as title-like or office-like formulas for future testing, especially if they predict companion sides or object families.

3. Identity / house / affiliation

Still live, but secondary. It needs iconography, findspot, copy-family, or companion-side support.

### Losers

1. Simple fish or commodity phrase

Weaker. `220` may have broad fish/leaf-family form pressure, but the A-conditioned terminal behavior means a direct fish/commodity reading cannot carry the grammar.

2. Numeral or measure reading

Weak. The terminal distribution is frame-conditioned but not transparently numerical.

3. Direct Parpola sign60 bridge

Still downgraded. This campaign works in local sign namespace. Parpola/Mayig remain shadow clues, not accepted values.

## Next Discriminating Campaigns

### 1. Strict deduped A-220-X table

Collapse exact duplicate texts, same object families, same site/type batches, and damaged/open rows.

Pass:

- `240-220-032`, `520-220-415`, and `740-220-003/055` remain after deduplication.

Fail:

- Most frame concentration collapses into one repeated object family.

### 2. Companion-side frame test

The companion side is the other inscribed face of the same object. Compare companion formulas for:

- `520-220-415`
- `520-220` singleton terminals
- `240-220-032`
- `740-220-003`
- `740-220-055`
- `318-220-415`
- `845-220-415`

Pass:

- Different A-220-X frames predict different companion classes.

Fail:

- Companion behavior tracks only site/type/object family.

### 3. Source-image validation by frame

Check that the signs `220`, `032`, `003`, `055`, `235`, and `415` remain visually distinct and locally stable inside their dominant frames.

Pass:

- Frame selection survives source-grade sign identity.

Fail:

- Local signs collapse into visual/source-policy artifacts.

## Bottom Line

The A-220-X campaign shows real frame-conditioned selection. `520-220-415` remains the strongest branch, but it is no longer the only structural story. The more general result is:

```text
A conditions the terminal distribution after 220.
```

The most productive frames to pursue are `520-220-X`, `740-220-X`, and `240-220-X`. The most dangerous inflated frames are `318-220-415`, `740-220-055`, and `176-220-235`, because each is dominated by a single repeated text family. The next serious step is not another crosswalk guess — another attempt to map our sign numbers onto an outside catalog's signs; it is a strict deduped and companion-side A-220-X campaign.
