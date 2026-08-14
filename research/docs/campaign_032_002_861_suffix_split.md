# 032-002 861 Suffix-Split Campaign

Date: 2026-05-28

## Research Question

This note asks one grammar question about the sign `861` (signs are numeric IDs; `+` marks a row boundary in our notation). Does `861` behave like a plain ending, or like a closure-capable sign — one that can end a row but can also govern a small set of tails that follow the closure?

The four shapes under test:

```text
...-002-861+
...-002-861-603+
...-002-861-533-717+
...-002-861-255-416+
```

If the source-token follow-up confirms the tails as separated signs, the corpus label to test is `861` as a closure-capable branch with optional extension behavior.

## Stored Outputs

```text
tmp/run_032_002_861_suffix_split.py
data/open_prototype/reports/campaign_032_002_861_suffix_split_rows.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_raw_rows.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_families.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_raw_families.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_contrasts.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_source_routes.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_source_crops.csv
data/open_prototype/reports/campaign_032_002_861_suffix_split_summary.json
tmp/032_002_861_suffix_split/032_002_861_suffix_split_source_contact_sheet.png
```

Two counting rules matter here. The strict tables treat exact repeated texts as one grammatical evidence unit — duplicates collapse to one. The raw tables preserve repeated formula families instead of erasing them.

## Corpus Result

Strict dedup `002-861`:

| scope | rows | terminal | continuing |
|---|---:|---:|---:|
| all `002` | 119 | 95 | 24 |
| adjacent `032-002` | 9 | 7 | 2 |

Raw strict `002-861` before exact-text dedup:

| scope | rows | terminal | continuing |
|---|---:|---:|---:|
| all `002` | 136 | 106 | 30 |
| adjacent `032-002` | 10 | 8 | 2 |

Strict repeated nonterminal families — tails that recur after `861` even with duplicates collapsed:

| tail after `861` | rows | examples |
|---|---:|---|
| `603` | 3 | `M-240`, `M-714`, `M-1273` |
| `533-717` | 2 | `M-376`, `M-391` |

Raw repeated nonterminal families:

| tail after `861` | rows | status |
|---|---:|---|
| `416` | 6 | Harappa exact-formula family, collapsed to one strict unit |
| `603` | 3 | strict repeated family across Mohenjo-daro seal types |
| `533-717` | 2 | strict repeated family on Mohenjo-daro rectangular/no-icon rows |
| `698` | 2 | Mohenjo-daro exact-formula pair, collapsed pressure likely |

The key adjacent contrast sits inside the same near frame — the same run of signs just before `861`:

```text
...-220-032-002-861+
...-220-032-002-861-603+
...-220-032-002-861-255-416+
```

Within strict adjacent `032-002`, prefix-last2 `220 032` has 4 terminal `861` rows and 2 continuing `861` rows. Mechanical result: `861` is closure-heavy in this packet, but not terminal-only.

## Source Routes

A source route is the chain from a transcribed row back to its published photograph. The four missing suffix-family witnesses — the actual rows carrying the pattern — now have public CISI routes (CISI is the published photographic corpus of Indus inscriptions):

| row | tail | route | source status |
|---|---|---|---|
| `M-376` | `861-533-717` | CISI India IA leaf `n129`, printed p.94, `MOHENJO-DARO 376-381` | source-visible |
| `M-391` | `861-533-717` | CISI India IA leaf `n131`, printed p.96, `MOHENJO-DARO 391-396` | source-visible |
| `M-714` | `861-603` | CISI Pakistan IA leaf `n79`, printed p.45, `MOHENJO-DARO 712-714` | source-visible |
| `M-1273` | `861-603` | CISI Pakistan IA leaf `n195`, printed p.161, `MOHENJO-DARO 1269-1274` | source-visible |

Together with the previous campaign:

| row | tail | route |
|---|---|---|
| `M-240` | `861-603` | CISI India IA leaf `n95`, printed p.60 |
| `M-91` | `861-255-416` | CISI India IA leaf `n71`, printed p.36 |

The source packet now covers all six focus rows at object level. It does not yet accept final token segmentation.

## Working Linguistic Models

Three rival explanations, stated so they can be broken.

### 1. Closure Plus Addendum

Leading model to test against the rival analyses below. The idea: `861` closes the text, and the tails are optional add-ons after the closure.

```text
002-861          = compact closure
002-861-603      = compact closure + addendum A
002-861-533-717  = compact closure + addendum B
002-861-255-416  = compact closure + addendum C
```

Why it fits:

- `861` is terminal in 95/119 strict all-`002` rows.
- The leaks are not formless: `603` repeats 3 times and `533-717` repeats twice under strict dedup.
- Adjacent `032-002` gives both terminal and continuing `861` in the same `220-032` lane — the same analysis track.

Prediction:

- `603`, `533-717`, and `255-416` should be final or internally closed tails.
- These tails should be much more compatible with closure-heavy `861` than with branch heads like `390` or `300`.
- Source-token spacing should show real post-`861` signs, not fused compounds.

### 2. Role Marker With Overt Subclass

The idea: `861` marks a role/class. Bare `861` is the unexpanded class; `603`, `533-717`, and `255-416` are subclass labels.

This rises if:

- `603` and `533-717` sort by object type, icon/register, or left-frame class.
- `533-717` staying on `SEAL:R` / no-icon Mohenjo-daro rows turns out to be stable.
- Bare `861` and expanded `861-X` occupy the same grammatical slot.

### 3. Boundary Marker Plus Second Phrase

The idea: `861` closes a phrase, and the following material is a second phrase, not a suffix.

```text
002-861 | 603
002-861 | 533-717
002-861 | 255-416
```

This rises if:

- `603`, `533-717`, or `255-416` have independent phrase behavior elsewhere.
- Similar second phrases occur after `817` or `820`.
- The post-`861` chunks ignore the left-frame context and behave under their own grammar.

## Current Decision

Working label generated by this packet:

```text
861 = closure-capable post-002 branch sign with restricted-tail candidate behavior
```

Do not promote:

```text
861 = lexical value
861 = phonetic value
603 / 533 / 717 / 255 / 416 = translated suffix values
```

The important gain is structural. `861` is no longer a vague member of a preferred ending family. It now has a testable split:

```text
bare closure vs closure-plus-tail
```

## Next Campaign

Run the suffix-attachment test:

1. Extract every occurrence of `603`, `533-717`, `255-416`, `416`, and `698`.
2. Ask whether each tail occurs independently, after other closure signs, or mainly after `861`.
3. Source-token inspect the six focus rows for physical spacing around `861`.
4. Compare with `390` tails (`390-125`, `390-705`, `390-692`) to separate closure-addenda from branch-head complements.

Pass condition:

```text
post-861 tails are final, bounded, repeated, source-separated, and preferentially attach to 861
```

Fail condition:

```text
tails occur freely after unrelated heads, or source images fuse/catalog-misorder the apparent suffixes
```
