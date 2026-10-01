# Meluhha Context Lead Matched Negatives

Date: 2026-05-29

## Question

This note records an attempt to find an outside handle on the Indus script, and a record of the shortcuts that attempt killed.

The idea behind it: Mesopotamian cuneiform texts mention a place called Meluhha, widely identified with the Indus region. If one of those texts named a person, title, commodity, or route that we could tie to a specific Indus-inscribed object, we would have an external anchor — a fixed point outside the Indus corpus that constrains what the signs can be. CDLI is the Cuneiform Digital Library Initiative, the public database of cuneiform texts we query.

Can the current CDLI Meluhha contexts produce a cuneiform-side name, title, commodity, or route phrase that is specific enough to become an external Indus bridge candidate?

Answer: not yet. The run produced a useful lead map and killed several attractive shortcuts, but no external anchor is accepted.

## Artifacts

- `data/meluhha/tools/mine_cdli_meluhha_context_leads.mjs`
- `data/meluhha/cdli_meluhha_context_leads.csv`
- `data/meluhha/cdli_meluhha_context_lead_query_plan.csv`
- `data/meluhha/cdli_meluhha_context_auto_token_leads.csv`
- `data/meluhha/tools/run_cdli_context_lead_matched_negatives.mjs`
- `data/meluhha/cdli_context_lead_matched_negative_summary.csv`
- `data/meluhha/cdli_context_lead_matched_negative_artifacts.csv`
- `data/meluhha/cdli_context_lead_matched_negative_fetch_log.csv`
- `data/meluhha/tools/retest_context_leads_against_external_objects.mjs`
- `data/meluhha/context_lead_external_bridge_retest.csv`
- `data/meluhha/context_lead_external_bridge_retest_summary.json`

## Method

The miner used the current CDLI line-context export and built 14 seeded lead families plus an automatic n-gram lead list. Seeds included the Shu-ilishu interpreter seal, Irisagrig ration group, Meluhha ship/work phrases, carnelian/copper/material formulae, `i3-dub`, `e2-duru5`, `dumu me-luh-ha`, route controls, and animal/object modifiers.

The matched-negative runner queried CDLI with `format=json&limit=100` and paginated up to five pages. This matters: first-page-only CDLI searches silently cap at 25 by default. The query `szu-i3-li2-su`, for example, returns 207 deduplicated artifacts over three pages.

For each query, the runner counted distinct returned artifacts, exact query-line artifacts, inscription hashes, duplicate clusters, artifacts with any Meluhha line, and artifacts where the query line is same-line or adjacent to Meluhha. A "matched negative" is the control step: we check how often a phrase turns up on texts that have nothing to do with Meluhha, because a phrase that is everywhere cannot point at Meluhha. A phrase only passed the source-side negative gate — the checkpoint a phrase must clear before it counts as a lead — when it had at least two query-line artifacts and low false positives. Passing this gate does not make an Indus claim.

The external retest then joined source-side survivors to the local external Indus-style object table, our list of Indus or Indus-style objects found outside the Indus region. Same-site and same-region strict length/duplicate-pattern matches were treated as forger-positive by construction. The "forger" is our standard adversary test: we ask whether a fake target, built to have no real relationship, would score just as well. Here it would — any synthetic target with the same duplicate pattern would produce the same match count.

## Main Kills

`szu-i3-li2-su` is not a Meluhha-diagnostic name. Paginated CDLI search returned 207 artifacts; 175 had query-line hits, and only one query-line artifact had any Meluhha line. False-positive rate: `0.994286`.

`lu2-tukul` fails as a ship/work anchor. It returned 46 artifacts; 42 had query-line hits, and only one had Meluhha. False-positive rate: `0.976190`.

`gurusz`, `nu-banda3`, `ur-{d}lamma`, and `ur-{d}ig-alim` all fail as standalone anchors. The broad title/name searches hit the five-page cap where applicable, with false-positive rates from `0.995772` to `1.000000`.

`a-li-a-hi` is not diagnostic by itself. It returned 8 artifacts, 6 query-line hits, and only 3 Meluhha-bearing hits. False-positive rate: `0.500000`. The longer phrase `a-li-a-hi dam-a-ni` is source-side interesting at 3/3, but it is just an Irisagrig cluster until an external object bridge exists.

`ur gun3-a` is not diagnostic. It has 4 query-line artifacts, only 2 with Meluhha. False-positive rate: `0.500000`.

## Source-Side Survivors

Nineteen queries passed only as cuneiform-side context leads. Most literally include `me-luh-ha`, so they are useful for source semantics but cannot be negative-control anchors. Examples:

- `i3-ba lu2 me-luh-ha`
- `ma2 me-luh-ha`
- `gug gi-rin-e`
- `i3-dub me-luh-ha`
- `e2-duru5 me-luh-ha`
- `dumu me-luh-ha`
- `ur-{d}lamma dumu me-luh-ha`
- `ur gun3-a me-luh-ha`

These are not readings. They are source-side lanes — separate lines of inquiry kept apart so one cannot contaminate another — for future object-level bridge work.

## External Retest

The bridge retest produced 23 query/site rows and 4 Ur/Susa/Failaka-focus rows. Object-level bridge count: `0`.

Same-site strict pattern-only matches exist in 8 rows. The most tempting is Ur:

- Cuneiform lead: `ur gun3-a me-luh-ha`
- Cuneiform site: Ur
- Target pattern: `ABCDEF`
- Same-site external match: `3898.1:Ur:+002-004-328-001-803-415+`

This is rejected. It has no accession, publication, title, personal-name, seal-owner, or archaeological-object link tying the cuneiform phrase to that Indus row. It is a same-site length/pattern match only, with pattern-only forger share `1.000000`.

The other same-site matches are Girsu/Tello five-unit formulae against local Girsu/Tello external rows `3885.1` and `5222.1`. Those are also rejected as site-overlap and length-pattern evidence only.

## Source-Route Queue

A "route" here is the trail from a catalog row to a real, citable object record: museum number, excavation number, publication, image. External-object source routing now has better acquisition targets, but none are anchors:

- Failaka rows `147.1` and `148.1`: secondary route through Laursen 2010 and Kjærum 1983; no primary public object route verified in this workspace.
- Susa row `3882.1`: strong Louvre route via `SB 2425 / AS 41 / CCO S.299`, but no cuneiform name/title on the object.
- Ur rows `3897.1`, `3898.1`, `3899.1`, `5225.1`, and `5231.1`: public BM/Gadd/Mitchell route pool exists. Follow-up now verifies `3898.1/U17649` and `3899.1/U8685`; the other three local rows remain unmapped or weak candidates.
- BM `120573`, excavation `U.7683`, registration `1928,1009.56`, is the strongest object-level bridge route seen so far because it is an Indus-style stamp seal from Diqdiqqah/Ur with a Sumerian inscription. It is not currently one of the local external-Indus rows and the public route does not expose a verified Meluhha name/title reading.

Follow-up audit on 2026-05-30: BM `120573` is now verified as an object-level route but rejected as an external phonetic anchor in the current workspace. The BM/Gadd source surface exposes a rectangular cuneiform-inscribed Indus-style seal, not an Indus sign sequence. The five local Ur external rows (`3897.1`, `3898.1`, `3899.1`, `5225.1`, `5231.1`) do not map to it; four are circular and all carry local Indus numeric sign sequences rather than the cuneiform-only BM object. See `docs/bm120573_object_bridge_audit.md`.

Second follow-up audit on 2026-05-30: the broader Gadd Ur accession bridge audit verifies two exact local mappings, `3898.1/U17649` and `3899.1/U8685`, but rejects the micro-bilingual route. Those mapped objects are Indus-inscribed only in the current source surface; BM `120573/U.7683` is cuneiform-only; candidate mappings for `3897.1` and `5231.1` are not accession-verified. The modeled Gadd/BM/Penn surface contains zero objects with both an Indus sequence and readable cuneiform. See `docs/gadd_ur_accession_bridge_audit.md`.

## Decision

No translation, phonetic value, sign meaning, language identification, or external anchor is accepted.

Residual value: this is now a cleaner Meluhha lead surface. Future work should target object-level routes first, not more same-site pattern matching.
