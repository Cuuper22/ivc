Date: 2026-05-29

This note tests whether a rare ending is rare everywhere or only rare in the wrong place to look. The pair `533-717` follows `002-861` on just 2 of 144 seals — negligible. But narrow the field to one physical class of object and the same 2 rows become 2 of 3. The note works through those slices and records what the concentration does and does not license.

## Question

The context split — the earlier pass that sorted post-`861` endings by how restricted their context is — made `533-717` the P1 restricted post-`861` target, the highest-priority one.

This campaign asks the next linguistic question. A "register" is a coarse class of object defined by site, type, and shape; an "addendum" is an extra sign or signs tacked on after an otherwise complete ending:

```text
Is 533-717 behaving like a conditional register/subclass marker
inside no-icon Mohenjo-daro SEAL:R rows,
or is it only a rare addendum?
```

## Stored Outputs

```text
tmp/run_032_002_861_533717_register_test.py
data/open_prototype/reports/campaign_032_002_861_533717_register_test_rows.csv
data/open_prototype/reports/campaign_032_002_861_533717_register_test_scopes.csv
data/open_prototype/reports/campaign_032_002_861_533717_register_test_summary.json
```

Input layer. "Strict dedup" means near-duplicate rows are collapsed on text, site, type, and symbol so one object cannot be counted twice:

```text
data/open_prototype/lipi/metadata_filtered.csv
strict complete source strings, text/site/type/symbol dedup: 4011 rows
```

## Register Test

| scope | rows with `002-861` | `533-717` rows | bare `002-861` rows | other tails | result |
|---|---:|---:|---:|---:|---|
| all strict `002-861` rows | 144 | 2 | 113 | 29 | `533-717` is rare globally |
| Mohenjo-daro no-icon `SEAL:R` | 7 | 2 | 3 | 2 | `533-717` rises inside this register |
| Mohenjo-daro no-icon rectangular/cuboid `SEAL:R` | 7 | 2 | 3 | 2 | same as full no-icon `SEAL:R` pool |
| Mohenjo-daro no-icon cuboid-convex `SEAL:R` | 3 | 2 | 0 | 1 | strongest concentration |
| Mohenjo-daro `SEAL:S` with `002-861` | 71 | 0 | 59 | 12 | square/iconic seal controls reject a general seal-ending reading |

Focus rows in the no-icon `SEAL:R` `002-861` pool:

```text
M-1954 +740-407-590-031-752-033-705-220-415-798-002-861+
M-355  +740-877-032-033-705-231-235-002-861-360-520-919-140+
M-376  +740-100-176-002-861-533-717+
M-391  +405-845-686-740-793-003-233-805-002-861-533-717+
M-1267 +416-001-740-720-175-002-861+
M-1273 +740-055-002-861-603+
M-1973 +740-575-017-233-550-002-861+
```

## Decision

Promote `533-717` from generic restricted-tail candidate to conditional register candidate.

The exact promotion is:

```text
533-717 is not a global no-icon SEAL:R ending.
It is a strong conditional candidate inside the no-icon SEAL:R + 002-861 branch,
especially cuboid-convex rows.
```

The evidence that moves it:

```text
2/144 among all strict 002-861 rows
2/7 among Mohenjo-daro no-icon SEAL:R rows with 002-861
2/3 among cuboid-convex no-icon SEAL:R rows with 002-861
0/71 among Mohenjo-daro SEAL:S rows with 002-861
```

This is not enough to assign a value. It is enough to stop treating `533-717` as an arbitrary rare tail.

## Linguistic Consequence

`861` now has at least three downstream behaviors:

```text
bare closure:
  dominant global state

conditional register/subclass continuation:
  533-717, currently tied to no-icon SEAL:R / cuboid-convex branch

mixed reusable formula continuation:
  603, shared with independent Harappa TAB:B formula life
```

That is a real syntactic split. The next translation-relevant move is not "what sound is 861?" It is:

```text
What class of object/text is being marked when no-icon SEAL:R + 002-861 takes 533-717?
```

## Next Test

Source-route the five non-`533-717` no-icon `SEAL:R` `002-861` controls — that is, find for each a chain of pointers from our database row to a real published image:

```text
M-1954 bare
M-355 tail 360-520-919-140
M-1267 bare
M-1273 tail 603
M-1973 bare
```

Decision condition:

```text
If their source layouts show the same terminal zone without 533-717,
then 533-717 is a true conditional marker candidate.

If the controls collapse through source/order problems,
then the register promotion drops back to rare addendum.
```

No sign value, phonetic reading, language identity, or translation is accepted.
