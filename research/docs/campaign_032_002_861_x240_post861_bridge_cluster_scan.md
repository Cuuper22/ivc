# 032-002-861 X-Before-240 / Post-861 Bridge Cluster Scan

Date: 2026-05-29

## Question

This note widens an earlier single-sign test into a scan over every sign, then charges the scan for the searching it did. Signs in this corpus are numeric IDs. "X-before-`240`" names the slot filled by the sign X in rows shaped `...-X-240-...`; a "tail" is material at the end of an inscription row, here after `002-861`. A sign "bridges" when it turns up in both places. "Ecology" means the set of contexts a sign normally lives in. A "background" sign is one so common it appears almost everywhere, so it carries no information. A "family cell" collapses near-identical repeated rows into one unit of evidence, so copies cannot pose as independent witnesses.

Does any nonbackground sign form a real family-cell bridge between the X-before-`240` ecology and post-`002-861` tail-initial ecology, after correcting for the fact that the packet was searched?

## Method

- Unit: family cell.
- X-before-`240` side: `81` family cells from the family-cell audit.
- Post-`002-861` side: `25` nonterminal tail-initial family cells.
- Post-`002-861` cells collapse by `(tail initial, pre-002-861 frame, tail string, register key, signless tail template)` — the "register" being the object class the row sits on.
- Within-side null: shuffle X labels over X-family cells and tail-initial labels over post-`002-861` tail cells for 20,000 iterations. This preserves side-specific sign frequencies and tests context placement.
- Identity-remap null: remap post-`002-861` tail sign groups onto the X-before-`240` sign universe for 20,000 iterations. This breaks the cross-side sign identity match while preserving tail group sizes.

Both are null models: randomized copies of the data. If the shuffles reproduce the observed pattern often, the pattern is cheap.

A candidate must have at least two independent family cells on both sides before it can become decipherment-bearing. That minimum is the "shape gate" in the tables below — a checkpoint a candidate must clear. Single-cell intersections are logged only.

## Observed Candidates

| rank | sign | score | X cells | post-861 cells | dominant after-240 | shape gate | templates X/post | examples |
|---:|---|---:|---:|---:|---|---|---|---|
| 1 | 603 | -8 | 1 | 3 | 060 692 (1/1) | False | 1/3 | H-1138 +740-603-240-060-692+ |

## Max-Scan Null

- Observed top sign: `603`
- Observed max score: `-8`
- Within-side `P(max shuffled score >= observed max score) = 1.000000`
- Within-side `P(any shuffled sign passes the multi-cell shape gate) = 0.000000`
- Identity-remap `P(max remapped score >= observed max score) = 1.000000`
- Identity-remap `P(any remapped sign passes the multi-cell shape gate) = 0.071350`

## Decision

Status: `no_family_cell_bridge_cluster_promoted_from_x240_post861_scan`.

- At family-cell level the observed nonbackground X-before-240/post-002-861 intersection has no multi-cell bridge cluster passing the shape gate.
- `603` remains the visible intersection sign, but its X-before-240 side is one family cell, so it fails the minimum recurrence rule before semantics or value can be discussed.
- The max-scan null is the relevant decision adversary because the target was found by searching for bridge-like behavior across signs.
- The next decipherment move is to pivot away from 603-only work unless source acquisition creates graphic identity or a second independent 603 family cell.

Accepted values, phonetics, language identity, translations, and graphic identity remain 0/unaccepted.
