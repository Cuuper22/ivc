# A-220-X Strict Dedupe And Companion Campaign

Date: 2026-05-26

This note re-runs an earlier result under a stricter counting rule, and the ranking changes. Signs in this corpus are numeric IDs. `A-220-X` means: some sign `A`, then `220`, then a variable sign `X`. "Strict dedup" collapses rows repeating the same text into one unit of evidence, so a copied inscription cannot pose as many witnesses; that is what shifts the ranking here. The "companion" is the other inscribed face of the same object. A "copy family" or "formula family" is a set of such near-identical rows.

## Result

The strict pass keeps `A-220-X` alive, but changes the ranking.

The old raw story was too impressed by high counts. After removing damaged/open rows and collapsing exact duplicate text families, the useful grammatical target is:

```text
A - 220 - X

A   = frame / domain / operator sign
220 = shared head or slot-bearing sign
X   = frame-conditioned closure / complement / branch marker
```

The strongest survivor is now `240-220-032`, not raw `520-220-415`.

Accepted lexical values, phonetic readings, language identity, and translations remain `0`.

## Data Stored

- `data/open_prototype/reports/campaign_a_220_x_strict_closed_rows.csv`
- `data/open_prototype/reports/campaign_a_220_x_strict_dedup_units.csv`
- `data/open_prototype/reports/campaign_a_220_x_strict_frame_survival.csv`
- `data/open_prototype/reports/campaign_a_220_x_strict_prev_profile.csv`
- `data/open_prototype/reports/campaign_a_220_x_strict_companion_rows.csv`
- `data/open_prototype/reports/campaign_a_220_x_strict_companion_summary.csv`
- `data/open_prototype/reports/campaign_a_220_x_strict_dedup_companion_summary.json`
- `data/open_prototype/reports/campaign_a_220_x_strict_hypothesis_rank.csv`

Mechanic validation: packet counts are internally consistent.

- strict closed rows: `210`
- exact-text dedup units: `149`
- strict frames: `78`
- key previous signs: `520`, `740`, `240`, `318`, `845`, `176`, `<START>`, `000`, `235`, `590`, `002`, `233`, `904`
- overall exact-dedupe collapse: `210 -> 149`

Companion-class dedup counts are frame-local only. They are not globally additive because one dedup text unit can appear under multiple companion classes.

## Main Dedupe Shift

| frame | strict rows | dedup units | status |
|---|---:|---:|---|
| `240-220-032` | 9 | 9 | strongest clean productive survivor |
| `520-220-415` | 26 | 10 | major branch, duplicate-inflated |
| `740-220-003` | 10 | 6 | surviving `740` branch after raw `055` collapse |
| `520-220-016` | 5 | 4 | small but real companion-side branch clue |
| `002-220-455` | 5 | 5 | secondary compact candidate |
| `233-220-032` | 4 | 4 | secondary `032` branch |
| `235-220-032` | 4 | 4 | secondary `032` branch |
| `590-220-003` | 4 | 4 | secondary `003` branch |
| `318-220-415` | 11 | 1 | excluded from general grammar for now |
| `740-220-055` | 11 | 1 | Lothal tag-family formula |
| `176-220-235` | 7 | 1 | Harappa tablet-family formula |
| `845-220-415` | 4 | 1 | small Mohenjo-daro tablet-family formula |

## Ranked Interpretation

### 1. `240-220-032`

Current best productive-frame candidate.

Evidence:

- `9` strict rows and `9` dedup text units.
- at the previous-sign level, `240` has `12` strict rows and `12` dedup units; `032` is `9/12`.
- `3` sites: Chanhu-daro, Harappa, Mohenjo-daro.
- `2` seal types.
- largest exact text family is only `1`.
- no companion side in all 9 rows.

Working linguistic interpretation:

`240` strongly selects `032` through `220`. This is the cleanest evidence that the sign before `220` conditions the sign after `220`, rather than `220-X` being a universal chunk.

Next check:

Source-grade visual and context pass for `C-65`, `H-1678`, `M-1728`, `M-49`, `M-240`, `M-319`, `M-631`, `M-722`, and `M-1265`.

### 2. `520-220-X`

Still a productive frame, but not a fixed `520-220-415` phrase.

Evidence:

- `520` strict profile: `55` rows, `38` dedup units.
- `415` drops from `26/55` strict rows to `10/38` dedup units.
- `520` branch remains broad across Harappa, Kalibangan, Lothal, Mohenjo-daro, and Nausharo.
- dedup terminal profile: `415:10;240:5;016:4;002:3;235:3;003:2;001:1;621:1`.

Working linguistic interpretation:

`520-220` is a productive construction with a real `X` slot. `415` is a major branch inside it, not the whole grammar.

Next check:

Treat `520-220-415`, `520-220-016`, and `520-220-240` as contrastive branches. Do not collapse them into one reading.

### 3. `740-220-003`

The dedupe correction flips the `740` branch.

Evidence:

- raw `740-220-055`: `11` rows, but only `1` dedup text unit, all Lothal tags.
- `740` dedup dominant terminal becomes `003`, not `055`.
- `740-220-003`: `10` strict rows, `6` dedup units, `3` sites, `3` types.
- no companion side in all 10 rows.

Working linguistic interpretation:

`740-220-X` remains productive, but its general branch is `003` pressure, while `055` is a Lothal local formula until proved otherwise.

Next check:

Separate exact `+740-220-003+` rows from longer non-exact contexts, then source-check whether `003` is stable across `H-68`, `K-9`, `M-294`, `M-725`, `M-1429`, `M-1439`, `M-1441`, `M-1442`, and `M-1443`.

### 4. `520-220-016`

Small, not decisive, but it is the best companion-side branch clue.

Evidence:

- `5` strict rows, `4` dedup units.
- companion profile: `700_033_branch:3;no_companion_side:2`.
- the `700_033` cases are `H-1121`, `H-789`, and `H-942`.

Working linguistic interpretation:

This could mark a branch distinct from `520-220-415`, because its companion side leans toward `700_033`. It is not a bilingual clue yet. It is a side-pairing hypothesis.

Next check:

All-side source panels for `H-1121`, `H-789`, and `H-942`, including side labels, direction, and whether normalizing `033-700` and `700-033` into one class is legitimate.

### 5. `520-220-415`

Still important, but downgraded from "reading clue" to "major branch inside a broader frame."

Evidence:

- `26` strict rows, `10` dedup units.
- exact `+520-220-415+` family alone contributes `17` rows.
- companion side is mixed: `700_034`, `700_032`, `110`, companion-starts-`520-220`, longer-other, no companion.

Working linguistic interpretation:

This is probably a real formula branch. It cannot carry the entire interpretation of `220`, `415`, or `520`.

Next check:

Source panels and side labels for the exact core and companion-bearing cases, especially `H-319`, `H-938`, `H-939`, `H-940`, `H-941`, `H-1284`, `H-2148`, `H-2240`, and `M-37`.

## Excluded From General Grammar For Now

These are not dead. They are moved out of general grammar and into local formula/source-family work.

- `318-220-415`: `11 -> 1`; all Harappa `TAB:B`; repeated long text family.
- `740-220-055`: `11 -> 1`; all Lothal tags.
- `176-220-235`: `7 -> 1`; all Harappa `TAB:B`.
- `845-220-415`: `4 -> 1`; Mohenjo-daro `TAB:C`.

They can come back only if source-family dedupe breaks them open into independent families across sites/types.

## Competing Linguistic Models

### Model A: classifier stem plus ending

`A` is a semantic or administrative classifier, `220` is a productive head, and `X` is an ending or branch marker.

Best support:

- `240-220-032` survives cleanly.
- `520-220-X` has a real substitution slot.
- `740-220-003` survives after dedupe.

Falsifier:

Source-level inspection shows `032`, `003`, `016`, `415`, or `240` are unstable transcription artifacts inside these frames.

### Model B: administrative predicate frame

`A` is an operator/register, `220` is a governed object or role, and `X` marks result/status/closure.

Best support:

- `520-220-X` branch diversity.
- companion pressure around `520-220-016`.
- formula-like behavior without full exact-text identity.

Falsifier:

Companion-side classes fail to distinguish the `520` branches once source sides and object families are controlled.

### Model C: corporate, house, office, or identity formula

`A-220` is a named institutional or identity stem, and `X` marks branch/rank/locality/status.

Best support:

- high formula recurrence without global collapse.
- local locked families can be meaningful within sites or workshops.

Falsifier:

`X` values do not cluster by object type, iconography, findspot, site, or companion-side formula.

## Next Campaign

Run a three-frame contrast:

```text
240-220-032
520-220-{415,016,240}
740-220-003
```

Decision targets:

1. Does `240-220-032` stay intact under source-image inspection?
2. Do `520-220-415`, `520-220-016`, and `520-220-240` behave as contrastive endings/branches?
3. Is `740-220-003` a true productive branch or another hidden object-family formula?
4. Are `032`, `003`, `016`, `240`, and `415` source-visible distinct signs in these frames?

First statistical contrast:

```text
P(next=032 | prev=240)
vs
P(next=032 | prev!=240)
```

Run it on strict dedup text units only, blocked by site and object type. Then repeat on no-companion-side rows only. If the `240` effect stays high while matched non-`240` frames are diffuse, `240-220-032` is the best live formulaic signal. If it collapses inside one site/type block, demote it to local catalog behavior.

Second contrast:

Within deduped `520-220-X`, compare companion class for `X=016`, `X=415`, and `X=240`, especially `700_033` versus all other/no-companion classes. If `016` keeps `700_033` dependence after Harappa/TAB blocking, it becomes the next side-pairing lead.

Follow-up executed:

- [A-220-X 240 selector contrast](campaign_a_220_x_240_selector_contrast.md) upgrades `240-220-032` from clean survivor to strongest current selector contrast.
- Strict frame-text dedup: `240 -> 032` is 9/12 versus non-`240` 46/239.
- Matched site/type/frame/text blocks: 9/12 versus 35/150.
- The signal survives no-companion filtering but is heavily carried by Mohenjo-daro `SEAL:S`.
- Position/tail check blocks calling `032` an ending: 7/9 target rows continue after `032`.

## Bottom Line

The strict campaign did not merely "audit" the old result. It changed the research object.

The live grammar is now:

```text
240 strongly selects 032 through 220.
520 opens a broad X-slot after 220.
740 has a dedupe-surviving 003 branch, while raw 055 was mostly a Lothal tag family.
318, 845, and 176 are local formula families until proved independent.
```

This is decipherment progress because it identifies the next sign-function target: not "what is `220`?", but which `A-220-X` frames behave like productive grammar and which are copied administrative formulae.
