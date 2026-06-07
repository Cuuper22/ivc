# A-220-X 240 Selector Contrast

Date: 2026-05-26

## Result

`240-220` strongly favors `032` in strict deduped data.

This upgrades `240-220-032` from "clean survivor" to the strongest current A-conditioned selector contrast. The result is not a translation and not a sign value. It says:

```text
when A = 240 before 220, X = 032 is strongly preferred
```

Best current wording:

`240-220` is a productive or semi-productive construction that selects `032` far more often than matched non-`240` frames do.

Accepted lexical values, phonetic readings, allography, language identity, and translations remain `0`.

## Data Stored

- `data/open_prototype/reports/campaign_a_220_x_240_contrast_strict_rows.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_contrast_dedup_units.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_contrast_no_companion_dedup_units.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_contrast_block_units.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_contrast_block_summary.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_leave_one_block_out.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_position_tail_profile.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_selector_source_queue.csv`
- `data/open_prototype/reports/campaign_a_220_x_240_contrast_summary.json`

Mechanic validation: pass after definition correction.

Definitions:

- global units are exact `frame + text` dedup units.
- blocked units are `site + type + frame + text`.
- there are `260` blocked units but only `256` distinct `site + type + text` keys because four exact texts contain two `220` occurrences.
- `no_companion_side` means no reconstructable companion side under the current `cisi` object grouping. It is not proof that the object physically had one side.

## Main Contrast

| scope | `240 -> 032` | non-`240 -> 032` | difference | odds ratio |
|---|---:|---:|---:|---:|
| all strict frame-text dedup units | 9/12 = 0.750 | 46/239 = 0.192 | +0.558 | 12.59 |
| no-companion frame-text dedup units | 9/12 = 0.750 | 43/215 = 0.200 | +0.550 | 12.00 |
| matched site/type/frame/text blocks | 9/12 = 0.750 | 35/150 = 0.233 | +0.517 | 9.86 |
| matched no-companion blocks | 9/12 = 0.750 | 35/148 = 0.236 | +0.514 | 9.69 |

The effect survives:

- exact text dedupe,
- no-companion filtering,
- site/type blocking,
- and no-companion site/type blocking.

This rules out the easy explanations: not a single copied text, not a companion-side artifact, not broad seal behavior alone.

## Block Behavior

| block | `240 -> 032` | non-`240 -> 032` | status |
|---|---:|---:|---|
| Mohenjo-daro `SEAL:S` | 6/7 | 23/104 | main load-bearing block |
| Harappa `SEAL:S` | 1/1 | 6/29 | supportive but tiny |
| Chanhu-daro `SEAL:S` | 1/1 | 1/1 | non-discriminating |
| Mohenjo-daro `SEAL:R` | 1/2 | 5/16 | weak supportive |
| Mohenjo-daro `SEAL` | 0/1 | no comparator | negative but not interpretable |

The remaining serious confound is Mohenjo-daro `SEAL:S` dominance. The effect is not erased outside that block, but outside it the sample is small.

Leave-one-block result:

- remove Mohenjo-daro `SEAL:S`: `240 -> 032` is 3/5 versus non-`240 -> 032` at 12/46.
- remove Mohenjo-daro entirely: `240 -> 032` is 2/2 versus non-`240 -> 032` at 7/30.

So the signal is real, but the honest phrasing is:

`240-220` strongly favors `032`, especially in Mohenjo-daro SEAL:S, with small compatible support outside that block.

Not:

`240` universally selects `032`.

## Position And Continuation

`032` is not yet an ending.

Among the 9 `240-220-032` target units:

- 2 are terminal after `032`.
- 7 continue after `032`.

That means `032` may be a continuation marker, classifier, subtype, or internal complement rather than a closure. The next sign-function question is whether `032` changes the continuation pattern after `240-220`, not whether it simply ends the phrase.

The three `240-220-non032` internal controls are:

- `M-1990`: `240-220-002`
- `M-133`: `240-220-255`
- `M-369`: `240-220-415`

These are mandatory controls. If source inspection collapses `032` into one of those forms, the current selector result weakens sharply.

## Linguistic Interpretation

### Strongest

`240-220-032` is a positional formula or constructional stem.

It behaves like a local grammatical frame: `240-220` licenses `032` at a rate far above matched non-`240` frames.

### Plausible

`240-220` is a classifier/head construction and `032` is a selected qualifier or subclass marker.

This fits the fact that many `240-220-032` texts continue after `032`.

### Still Live

Hidden object-template formula.

Mohenjo-daro `SEAL:S` carries most of the mass. If the six Mohenjo-daro `SEAL:S` target rows share a visual/source-template family, layout, iconography, excavation route, or local copy tradition, the claim downgrades from productive frame to seal-template formula.

## Source Queue

P0 target rows:

- `C-65`: `+000-100-240-220-032-002-861+`
- `H-1678`: `+520-233-240-220-032+`
- `M-1728`: `+161-055-240-220-032-002-820+`
- `M-49`: `+527-550-240-220-032-002-300-350-032-190+`
- `M-240`: `+520-240-220-032-002-861-603+`
- `M-319`: `+740-812-033-240-220-032+`
- `M-631`: `+520-033-706-240-220-032-368-263+`
- `M-722`: `+740-585-240-220-032-002-817+`
- `M-1265`: `+740-055-240-220-032-806+`

P0 internal controls:

- `M-1990`: `+740-760-440-240-220-002-861+`
- `M-133`: `+527-550-240-220-255-812-906-388+`
- `M-369`: `+740-690-435-255-240-220-415-806-742-060-920+`

The source test must verify:

- `240`, `220`, `032`, `002`, `255`, and `415` are visually distinct under the same sign policy.
- the six Mohenjo-daro `SEAL:S` successes are not one visual/source-template family.
- the target rows do not share a layout, icon, findspot, or catalog convention that explains the effect without grammar.

## Next Campaign

Run a `032-after-220 function campaign`:

```text
240-220-032
non-240 A-220-032
240-220-non032
032 outside A-220-X in comparable positions
```

Questions:

1. Is `032` specifically selected by `240-220`, or is it a general after-`220` continuation sign?
2. Does `032` predict the tail after it, especially `002-861`, `002-820`, `002-817`, or terminal closure?
3. Do the `240-220-non032` controls differ by source-visible sign shape, layout, or semantic context?
4. Does the Mohenjo-daro `SEAL:S` cluster break into independent source families?

Follow-up executed:

- [032 after 220 function campaign](campaign_032_after_220_function.md) rejects `032` as an ending after `240-220`.
- `240-220-032` is terminal only 2/9.
- `A-220-032` is much more likely than outside `032` to continue into `002`.
- The next live object is `A-220-032-002-Y`, especially `002-861/820/817`.

## Bottom Line

`240-220-032` is now the best live sign-function target in the A-220-X campaign.

It is not a reading. It is a strong selector fact:

```text
240 before 220 sharply raises the probability of 032 after 220.
```

The next move is not to assign a value. It is to explain what kind of slot `032` occupies by comparing continuation, source shape, and matched non-`240` controls.
