# M-105 unknown-sign count-policy gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SEVEN_UNIT_SEQUENCE_CORRECTS_STRUCTURAL_COUNT_TO_SEVEN_WHILE_BOTH_000_IDENTITIES_REMAIN_UNKNOWN`.

## Bound sources

- CISI 1 local PDF, PDF page 75 / printed page 39, SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi row `2632.1`, object `M-105`, direction `R/L`, stored text `+000-000-803-231-742-060-920+`. Lipi stores seven positions and reports `text length = 7`, but its `signs` field is `5`.
- Mayig `M-105A` at commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`, sequence `P324 P324 P364 P056 P326 P120 P154`, raw-record SHA-256 `33D17D44BE46F313DDE9DCF4FBAE8C64C2E872E343E478C3E329CEA2BA3BBC34`.

The durable page and object panels are listed in `research/data/sign_crosswalk/source_panels/m105_unknown_policy/manifest.csv`. The normalized position-by-position record is `research/data/sign_crosswalk/m105_source_position_concordance_20260712.csv`.

## Visual check

Each published view separately shows seven bounded inscription units.

- `M-105 A`, the impression, shows the sequence in right-to-left reading order.
- `M-105 a`, the seal, shows the same sequence in its physical mirror, left to right.
- In each view, the opening pair consists of two distinct jar-form units. Neither is a scratch, damaged box, missing sign, or decorative spillover.

The seven visual forms are congruent with the pinned Mayig order: two classic jar units, leaf-with-tree, fish with an internal vertical stroke, jar with two small internal strokes, paired vertical lines with one lower slant, and a right-parenthesis form. This is an object-bound visual concordance, not a global namespace identity claim.

## Count-policy correction

For M-105, structural count is `7`. Lipi's `signs = 5` field is not a literal source count because it silently excludes the two stored `000` positions even though both positions contain genuine source-visible signs.

Each `000` therefore counts as one unresolved sign-bearing unit. Both identities stay unknown. In particular:

- do not rewrite either `000` as Lipi `740`;
- do not rewrite either `000` as Mayig `P324`;
- do not infer that the accepted `740/P324` edge applies to `000`;
- do not collapse the opening pair into one unit.

## Crosswalk boundaries

No global edge is accepted or promoted by this gate. Existing states remain unchanged:

- `803/P364` remains a `9:1` conflict and unaccepted;
- `920/P154` remains uncertain at `4:3` and unaccepted;
- `231/P056`, `742/P326`, and `060/P120` remain source-position evidence on this object only, without promotion here.

No sign meaning, reading, phonetic value, language identification, translation, or accepted decipherment claim is added.
