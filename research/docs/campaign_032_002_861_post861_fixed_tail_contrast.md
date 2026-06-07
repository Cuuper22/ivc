# 032-002-861 Post-861 Fixed-Tail Contrast

Date: 2026-05-29

## Question

Inside the post-`002-861` secondary zone, which tails behave like recurrent grammar objects, which are singleton contrasts, and which are just bare closure background?

## Profiles

| rank | tail | class | rows | cells | source-visible | matched bare pressure | notes |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `<END>` | `background_closure` | 113 | 110 | 7 | last2 0; last1 0; broad 0 | dominant post-002-861 state, not a tail value |
| 2 | `533 717` | `fixed_restricted_tail_unit` | 2 | 2 | 2 | last2 0; last1 1; broad 2 | repeated fixed-prefix terminal unit;not decomposed because independent 533 is absent;broad no-icon SEAL:R field has bare controls |
| 3 | `603` | `recurrent_simple_tail_parked_from_bridge` | 3 | 3 | 3 | last2 1; last1 2; broad 3 | recurrent simple tail across multiple source-visible rows;bridge route killed at family-cell level |
| 4 | `255 416` | `source_visible_singleton_contrast` | 1 | 1 | 1 | last2 1; last1 1; broad 1 | source-visible singleton tail;same last-2 frame has bare controls |
| 5 | `360 520 919 140` | `source_visible_singleton_contrast` | 1 | 1 | 1 | last2 0; last1 1; broad 1 | source-visible singleton tail |

## Decision

Status: `post861_secondary_zone_has_fixed_unit_singletons_and_bare_background_no_values`.

- `533-717` is the best fixed restricted-tail unit, but it remains one narrow grammatical object, not a value.
- `603` is recurrent and source-visible as a post-`861` simple tail, but the X-before-240 bridge route is parked, so it cannot carry cross-context value evidence.
- `255-416` and `360-520-919-140` are source-visible singleton contrasts: useful for defining the secondary zone, not for reading it.
- Bare `<END>` remains the closure background and supplies matched controls in several preframes/registers.
- The next grammar move is a source-normalized contrast among tail classes, not component translation.

Accepted values, phonetics, language identity, translations, and exact source-normalized token boundaries remain 0/unaccepted.
