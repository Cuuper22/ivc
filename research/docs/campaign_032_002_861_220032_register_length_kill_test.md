# 032-002-861 / 220-032 Register-Length Kill Test

Date: 2026-05-29

## Question

Does broad register, fine icon label, total line length, prefix length, or measured terminal space explain the `220-032` post-`861` split before we treat it as a grammar object?

## Packet

- Rows tested: `7`
- Source-ready rows: `5`
- Outcomes: `bare_closure:5;compound_tail_255_416:1;simple_tail_603:1`
- Source-ready outcomes: `bare_closure:3;compound_tail_255_416:1;simple_tail_603:1`

## Decisions

- `broad_register`: `fails_as_explanation`. type/shape source-ready split is SEAL:S|square:3 vs SEAL:S|square:1 vs SEAL:S|square:1 Limit: all source-ready rows are seal-square in this packet, so broad register cannot choose the tail.
- `site`: `fails_as_determinant`. site split is Mohenjo-daro:2;Harappa:1 vs Mohenjo-daro:1 vs Mohenjo-daro:1 Limit: Mohenjo-daro contains bare closure, simple tail, and compound tail; Harappa only contributes one source-ready bare control here.
- `total_text_length`: `insufficient_as_explanation`. all rows bare lengths 5,5,7,8,8 vs tailed 7,9; source-ready bare 5,5,8 vs tailed 7,9 Limit: total length partly tracks available continuation, but bare rows reach length 7/8 while tailed rows are 7/9; it is not a clean selector.
- `fine_icon_symbol`: `not_testable_as_general_explanation`. fine symbol labels differ across the five image rows: Bull/Bull1/Bull1:W bare, Gaur for 603, Bull1:S for 255-416 Limit: single rows per fine icon cannot distinguish icon function from row accident; broad Mohenjo seal-square already fails as determinant.
- `terminal_space`: `not_closed`. measured layout rows are 2 total: 0 bare and 2 tailed Limit: bare controls were visually scored but not quantified with comparable line-width/tail-space metrics, so this remains the next recut target.

## Feature Read

- `type_shape`: bare `SEAL:S|square:3`, `603` `SEAL:S|square:1`, `255-416` `SEAL:S|square:1`.
- `site`: bare `Mohenjo-daro:2;Harappa:1`, `603` `Mohenjo-daro:1`, `255-416` `Mohenjo-daro:1`.
- `symbol`: bare `Bull1:W:1;Bull1:1;Bull:1`, `603` `Gaur:1`, `255-416` `Bull1:S:1`.
- `site_type_shape`: bare `Mohenjo-daro|SEAL:S|square:2;Harappa|SEAL:S|square:1`, `603` `Mohenjo-daro|SEAL:S|square:1`, `255-416` `Mohenjo-daro|SEAL:S|square:1`.

## Numeric Read

- `text_length_all_rows`: bare `5,5,7,8,8`, tailed `7,9`, range overlap `True`, exact overlap `True`.
- `text_length_source_ready`: bare `5,5,8`, tailed `7,9`, range overlap `True`, exact overlap `False`.
- `prefix_len_all_rows`: bare `3,3,5,6,6`, tailed `4,5`, range overlap `True`, exact overlap `True`.
- `prefix_len_source_ready`: bare `3,3,6`, tailed `4,5`, range overlap `True`, exact overlap `False`.

## Result

The `220-032` split survives broad-register and total-length attacks in the current evidence layer: Mohenjo seal-square rows can be bare, simple-tailed, or compound-tailed, and total text length is not a clean selector.

The kill test is not fully closed. Fine icon labels are singletons, and comparable terminal-space metrics do not yet exist for the bare controls. The next recut should quantify empty terminal margin and line occupancy for `H-444/M-723/M-1044` the same way `M-91/M-240` were quantified.

Current status: `220032_split_survives_broad_register_and_length_attacks_terminal_space_unclosed`.

Accepted sign values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain 0/unaccepted.
