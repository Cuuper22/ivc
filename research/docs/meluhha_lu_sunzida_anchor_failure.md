# Meluhha Lu-Sunzida Anchor Failure

Date: 2026-05-29

This is Vector 1 hard-anchor work. It is not a decipherment claim.

## Question

Can the cuneiform string `lu2-sun2-zi-da`, commonly cited through the Meluhha-adjacent CDLI text `P212982 / CT 50, 076`, be used as a Meluhha-diagnostic personal-name anchor for an Indus phonetic value search?

## Source Route

The previous local seed table had one `Lu-sunzida` lead. This pass uses current CDLI search exports through the advanced-search field `atf_transliteration`, plus the ORACC/ePSD2 Meluhha name entry as an external count check.

Source routes:

- CDLI search guide: <https://cdli.earth/docs/search>
- CDLI current query exports, source-hashed locally: `data/meluhha/cdli_current_query_fetch_log.csv`
- ORACC/ePSD2 Meluhha entry: <https://oracc.museum.upenn.edu/epsd2/names/cbd/qpn/x000016710.html>

## Outputs

- `data/meluhha/tools/build_cdli_current_meluhha_exports.mjs`
- `data/meluhha/cdli_current_query_fetch_log.csv`
- `data/meluhha/cdli_current_meluhha_artifacts.csv`
- `data/meluhha/cdli_current_line_contexts.csv`
- `data/meluhha/cdli_current_lu_sunzida_test.csv`
- `data/meluhha/cdli_current_anchor_failure_summary.json`

## Counts

Current CDLI export rows:

| Query | Artifacts | Matched lines |
| --- | ---: | ---: |
| `me-luh-ha` | 25 | 29 |
| `me-luh-ha{ki}` | 21 | 23 |
| `lu2 me-luh-ha` | 5 | 5 |
| `ma2 me-luh-ha` | 8 | 4 |
| `me-luh-ha-ta` | 17 | 18 |
| `me-luh-ha-da` | 2 | 2 |
| `lu2-sun2-zi-da` | 15 | 15 |

Across the seven current CDLI queries, the export has 79 distinct artifacts and 96 matched line-context rows. ORACC/ePSD2 reports `Meluhha` as a geographic name with 70 instances and 8 spellings in the online entry fetched for this run.

## Forger / Matched Negative

Hypothesis tested: `lu2-sun2-zi-da` is a Meluhha-diagnostic personal-name anchor.

Matched negative definition: every current CDLI `atf_transliteration=lu2-sun2-zi-da` artifact where the same ATF text has no Meluhha line.

Result:

| Metric | Value |
| --- | ---: |
| `lu2-sun2-zi-da` distinct artifacts | 15 |
| Artifacts with any Meluhha line | 1 |
| Artifacts with adjacent Meluhha line | 1 |
| False positives if the name alone marks Meluhha | 14 |
| False-positive rate if the name alone marks Meluhha | 0.933333 |

The one surviving adjacency is real and useful as a lead:

| Artifact | Line | Following line |
| --- | --- | --- |
| `P212982 / CT 50, 076` | `5. lu2-sun2-zi-da` | `6. lu2 me-luh-ha-ke4` |

But the name itself appears in 14 current CDLI artifacts without any Meluhha line, mostly Ur III Puzrish-Dagan administrative contexts. Therefore the name cannot be used as a diagnostic Meluhha phonetic anchor by itself.

## Skeptic Attacks

Survived:

- Exact CDLI `atf_transliteration` export rather than a hand-picked seed.
- Same-query matched negatives from the same digital corpus route.
- Line-context extraction preserving previous and following lines.
- Source hashes recorded for every CDLI query export.

Fatal to promotion:

- The false-positive rate for the name-alone detector is `0.933333`.
- `P212982` lacks a paired external Indus object in the current local data.
- The adjacency proves only that the name and Meluhha title occur in neighboring lines in one text; it does not prove the name is Meluhhan, much less that any Indus sign sequence transcribes it.

## Decision

Retract the shortcut.

`Lu-sunzida` remains a cuneiform-side lead for a named Meluhha-adjacent administrative text, but it is not an accepted external phonetic anchor. No Indus sign value, phonetic value, sign meaning, language-family claim, or translation is earned.

The useful frontier movement is negative and concrete: the famous name lead is now measured against current CDLI matched negatives, and it fails hard enough that future bilingual searches must require more than onomastic adjacency. The next admissible gate is a paired external object or a source-validated sign-sequence match, not site overlap and not name citation.
