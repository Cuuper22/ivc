# 032-002-861 603 Slot Substitution

Date: 2026-05-29

This note tries to destroy the `603` bridge and only half succeeds. The bridge claim is that `603` matters because it appears in two unrelated settings. The obvious objection: at Harappa it merely fills a slot in a fixed tablet formula, and other signs fill that same slot, so `603` is nothing special. This note checks the other slot-fillers. Neither of them shows up after `002-861`, so the objection does not land — but a second objection, that the Harappa side is one copied formula, is still standing.

## Question

The strongest falsifier — the finding that would kill the claim — for `603` mobility is the Harappa tablet formula, where `X` marks the position that varies:

```text
740-X-240-060-692
```

If `603` is just one value of this Harappa tablet `X` slot, and if that slot has no relationship to the post-`002-861` tail field, then `603` is not a decipherment bridge. It is just a reused graph in two separate template systems.

## Stored Outputs

```text
tmp/run_032_002_861_603_slot_substitution.py
data/open_prototype/reports/campaign_032_002_861_603_slot_substitution_slot_rows.csv
data/open_prototype/reports/campaign_032_002_861_603_slot_substitution_post_tail_rows.csv
data/open_prototype/reports/campaign_032_002_861_603_slot_substitution_matrix.csv
data/open_prototype/reports/campaign_032_002_861_603_slot_substitution_summary.json
```

Input layer. "Strict" rows have complete readings rather than partly reconstructed ones; "dedup" collapses near-duplicate rows so one object cannot be counted twice:

```text
strict complete source strings, cisi/site/type/symbol/text dedup: 4011 rows
post-002-861 rows: 144
740-X-240-060-692 slot rows: 7
```

## Slot Matrix

A "formula family" is a group of rows with identical text, weighed as one piece of evidence; a "register cell" is one coarse class of object by site, type, and shape; "tail-initial" means the sign appears first in the material following `002-861`.

| `X` in `740-X-240-060-692` | slot rows | exact slot formula families | slot register cells | post-`002-861` tail-initial rows |
|---|---:|---:|---:|---:|
| `603` | 3 | 1 | 1 | 3 |
| `636` | 2 | 1 | 2 | 0 |
| `642` | 2 | 1 | 2 | 0 |

The Harappa slot rows:

```text
X=603:
  H-1138 +740-603-240-060-692+
  H-1846 +740-603-240-060-692+
  H-1137 +740-603-240-060-692+

X=636:
  H-360 +740-636-240-060-692+
  H-823 +740-636-240-060-692+

X=642:
  H-1845 +740-642-240-060-692+
  H-237  +740-642-240-060-692+
```

The post-`861` side:

```text
tail-initial 603:
  M-240  +520-240-220-032-002-861-603+
  M-714  +740-585-017-033-705-233-798-803-002-861-603+
  M-1273 +740-055-002-861-603+

tail-initial 636:
  0 rows

tail-initial 642:
  0 rows
```

## Read

The falsifier partially fails:

```text
603 is not merely one Harappa X-slot value in this strict layer,
because the other observed X-slot values, 636 and 642, do not appear as post-861 tail initials.
```

But the bridge is still under pressure:

```text
the Harappa X-slot side is formula-family-heavy
the 603 slot side has one exact text family
the 636 and 642 slot rows also form exact formula families
the Harappa side is not source-normalized yet
```

"Source-normalized" means the rows have been rescored by what can actually be seen on published photographs, rather than trusted from catalogue transcriptions.

## Decision

```text
603_cross_slot_bridge_survives_but_is_under_template_attack
```

Current best interpretation:

```text
603 is uniquely cross-slot among the observed Harappa 740-X-240-060-692 fillers,
but the independent side may still be one copied tablet formula family.
```

## Next Test

The next campaign should not broaden the search randomly. It should normalize the Harappa slot family:

```text
603 family:
  H-1137 / H-1138 / H-1846

636 family:
  H-360 / H-823

642 family:
  H-1845 / H-237
```

Questions:

```text
Are these three X-slot values physically comparable?
Are the row pairs/triples copy-family duplicates or independent tablets?
Does X occupy a visible equivalent component position?
Does 603 have any source-layout property that explains why only it also appears after 002-861?
```

No sign value, phonetic reading, language identity, or translation is accepted.
