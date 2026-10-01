Date: 2026-05-29

This note separates the interesting endings from the ordinary ones. Various things follow `002-861`, and treating them all alike wastes effort. The test used here is simple: does the ending ever appear anywhere else in the corpus? An ending found only after `002-861` is tied to that position and worth chasing. One found all over the place is a common sign that sometimes lands there and proves nothing. That split gives the campaign its next two targets.

## Question

The batch result split the post-`861` tails into restricted, mixed, and background material.

This campaign asks the linguistic question directly. An "addendum" is extra material tacked on after an otherwise complete ending; a "subclass slot" would be a position reserved for marking what kind of object or text this is:

```text
Which post-861 tails behave like a restricted final addendum/subclass slot,
and which are ordinary formula signs that only sometimes appear after 861?
```

## Stored Outputs

```text
tmp/run_032_002_861_context_split.py
data/open_prototype/reports/campaign_032_002_861_context_split_occurrences.csv
data/open_prototype/reports/campaign_032_002_861_context_split_summary.csv
data/open_prototype/reports/campaign_032_002_861_context_split_summary.json
```

Input layer. "Strict" rows have complete readings rather than partly reconstructed ones; "dedup" collapses near-duplicate rows so one object cannot be counted twice:

```text
data/open_prototype/lipi/metadata_filtered.csv
strict complete source strings, text/site/type/symbol dedup: 4011 rows
```

## Result Table

"Independent behavior" counts occurrences of the same unit outside the post-`002-861` position. A "register" is a coarse class of object by site, type, and shape; a "control" is a comparison case kept on hand to check a claim against.

| unit | post-`002-861` behavior | independent behavior | current read |
|---|---|---|---|
| `533-717` | 2 rows, both terminal, both source-visible focus rows | 0 rows | P1 restricted post-`861` target |
| `603` | 3 rows, all terminal, all source-visible focus rows | 4 rows: 3 Harappa `TAB:B` in `740-603-240-060-692`, plus one weak scene row | P1 mixed bridge target |
| `255-416` | 1 row, terminal, source-visible focus row | 0 rows as a two-sign unit | P2 singleton stress |
| `096` | 1 Mohenjo-daro ivory rod row | 1 Mohenjo-daro seal row | control only |
| `416` | 6 Harappa `TAB:I` rows, all terminal, usually paired with `700-034` / `034-700` companion rows | 39 rows across sites and object types | broad control, not restricted-tail evidence |
| `698` | 2 Mohenjo-daro square seal rows, both terminal | 7 rows, mostly Harappa pots/tablets | broad control, not restricted-tail evidence |

## Linguistic Read

`533-717` is now the clean restricted target. Both rows are Mohenjo-daro `SEAL:R`, no icon, cuboid-convex/rectangular register, terminal after `002-861`, and have no independent strict occurrence. That makes it the best candidate for a final addendum/subclass/register marker after `861`.

`603` is not the same kind of thing. Its three post-`002-861` uses are Mohenjo-daro seal terminals, but its independent life is a repeated Harappa `TAB:B` formula:

```text
H-1138 +740-603-240-060-692+
H-1846 +740-603-240-060-692+
H-1137 +740-603-240-060-692+
```

Two of those Harappa objects also carry a short `+700-034+` companion row. So `603` looks like a reusable formula component that can occupy the post-`861` slot, not a dedicated post-`861` suffix.

`255-416` stays alive but cannot lead the model. It has source-visible support in the `220-032` lane through `M-91`, plus bare controls `H-444/M-723/M-1044`, but it is still a singleton.

`416` and `698` are useful because they are the opposite case: they show what broad terminal material looks like when it is not restricted to the post-`861` environment.

## Model Movement

This changes the working parse from:

```text
861 sometimes takes tails
```

to:

```text
861 can close bare.
After it, at least two different continuation types exist:
1. restricted/register-like final material: strongest current case 533-717
2. reusable formula material in a final slot: strongest current case 603
```

## Next Research Move

Do not spend another block proving that `861` can be tailed. That is established enough for the next step.

Next campaign:

```text
533-717 register test:
compare every no-icon SEAL:R / rectangular / cuboid-convex row
against the two 533-717 rows and their bare 176-002-861 controls.
```

Decision condition:

```text
If 533-717 clusters with no-icon SEAL:R endings and not with square/iconic SEAL:S endings,
promote it as a register/subclass marker candidate.

If it does not cluster, demote it to rare addendum material.
```

No sign value, phonetic reading, language identity, or translation is accepted.
