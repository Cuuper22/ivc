# Meluhha External Phonetic Anchor Attempts

Date: 2026-05-29

This note records the first direct attempt to turn cuneiform Meluhha-side phonetic strings into Indus sign values on physically external Indus or Indus-style objects from Mesopotamia and the Gulf.

It produces no accepted phonetic value. That is the point of the gate: candidate values were generated, then tested against a pattern-matched forger and rejected.

## Inputs

Primary generated files:

- `data/meluhha/tools/attempt_external_phonetic_anchors.mjs`
- `data/meluhha/external_phonetic_anchor_candidates.csv`
- `data/meluhha/external_phonetic_anchor_target_summary.csv`
- `data/meluhha/external_phonetic_anchor_forger_iterations.csv`
- `data/meluhha/external_phonetic_anchor_summary.json`

The script used the local external-object table:

- `data/meluhha/external_indus_objects.csv`

The focus lane contains 29 parseable external rows from Mesopotamia and the Gulf. The full external context table contains 41 parseable rows.

## Tested Targets

The script tested only externally attested cuneiform strings, not language-family guesses:

| Target | Cuneiform units | Pattern | Source route |
| --- | --- | --- | --- |
| Meluhha toponym | `me-luh-ha` | `ABC` | ORACC/ePSD2 plus current CDLI Meluhha exports |
| Meluhha ship context | `ma2-me-luh-ha` | `ABCD` | current CDLI `ma2 me-luh-ha` exports |
| Lu-Sunzida | `lu2-sun2-zi-da` | `ABCD` | current CDLI Lu-Sunzida export plus P212982 adjacency |
| Shu-ilishu | `szu-i3-li2-su` | `ABCD` | CDLI seals 014339, interpreter seal |
| Interpreter title | `e-me-bal-me-luh-ha` | `ABCBDE` | CDLI seals 014339, duplicate `me` constraint |

The strict matching rule was deliberately narrow: a target can map to an external sign sequence only if the sign count and duplicate pattern match exactly. For example, an `ABCD` cuneiform target can map only to a four-sign all-distinct external sequence.

## Candidate Values Generated And Rejected

Examples of generated assignments:

- Kish `1970.1`, text `+000-643-240+`: `000=me;643=luh;240=ha` for `me-luh-ha`.
- Failaka `147.1`, text `+317-817-000-090+`: `317=ma2;817=me;000=luh;090=ha` for `ma2-me-luh-ha`.
- Failaka `147.1`, same text: `317=lu2;817=sun2;000=zi;090=da` for `lu2-sun2-zi-da`.
- Failaka `147.1`, same text: `317=szu;817=i3;000=li2;090=su` for `szu-i3-li2-su`.

These are not values. They are the mechanical output of length and duplicate-pattern compatibility. The same external row can be made to "read" as multiple unrelated cuneiform strings, which is exactly the failure mode the forger is meant to expose.

## Forger Result

The forger generated 2,000 synthetic phonetic targets per tested target with the same length and duplicate pattern. Because the matcher ignores phonetic identity and uses only pattern compatibility, a valid method should not treat any observed match as evidential unless it beats this null.

It did not.

| Target | Focus candidates | All external candidates | Null >= observed share | Decision |
| --- | ---: | ---: | ---: | --- |
| `me-luh-ha` | 2 | 4 | 1.000000 | failed forger gate |
| `ma2-me-luh-ha` | 5 | 6 | 1.000000 | failed forger gate |
| `lu2-sun2-zi-da` | 5 | 6 | 1.000000 | failed forger gate |
| `szu-i3-li2-su` | 5 | 6 | 1.000000 | failed forger gate |
| `e-me-bal-me-luh-ha` | 0 | 0 | 1.000000 | no strict candidate |

The duplicate `me` constraint in `e-me-bal-me-luh-ha` is the only target with real internal shape pressure under this one-sign-per-unit test. It produced no strict external candidate.

## Skeptic Boundary

The skeptic breaks every candidate for the same reasons:

- No candidate is paired to a specific cuneiform attestation by accession, owner, title, profession, date, or object-level publication route.
- The external Indus object rows are still `T3_quarantined_lipi_metadata`; they are useful for search, but not source-image or catalogue validated here.
- The same four-sign external rows can be assigned to `ma2-me-luh-ha`, `lu2-sun2-zi-da`, and `szu-i3-li2-su` with equal formal success.
- The Lu-Sunzida prior is independently failed: current CDLI exports give 15 Lu-Sunzida artifacts, only one with any Meluhha line, for a name-alone false-positive rate of `0.933333`.

## Decision

No external phonetic anchor survives. Accepted external anchors remain zero.

The next admissible gate is stricter than co-occurrence. A future candidate needs at least one object-level bridge: source-validated external Indus object, accession/publication linkage to a cuneiform name or title, owner/profession linkage, or independent repetition of the same external sign sequence tied to the same cuneiform token.
