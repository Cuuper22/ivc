# Meluhha Diffuse Bilingual Vector

Date: 2026-05-29

This directory starts Vector 1: the attempt to build a diffuse Meluhha bilingual. Instead of one Rosetta-style object carrying both scripts, the plan is to assemble the two sides from scattered pieces — readable cuneiform attestations that mention Meluhha on one side, external Indus-style objects on the other — and only join them where the evidence genuinely lines up.

This is not a claim ledger, and it contains no accepted external anchor yet. The current tables are reproducible infrastructure:

- `cuneiform_seed_attestations.csv`: exact cuneiform-side attestations verified or queued.
- `cuneiform_attestations_expanded.csv`: fetch-backed Meluhha-bearing cuneiform inventory, with line context, metadata, and source hashes.
- `cuneiform_fetch_log.csv`: URL/status/byte/hash log for the primary digital source fetches.
- `meluhha_token_inventory.json`: machine-readable counts and caveats for the expanded inventory.
- `meluhha_indus_join_surface.csv`: literal site-overlap lanes between the cuneiform inventory and external Indus-style objects.
- `meluhha_indus_join_surface_summary.json`: counts and caveats for the join surface.
- `meluhha_join_surface_null_summary.json`: forger result showing site overlap alone fails as evidence.
- `cuneiform_source_routes.csv`: primary digital routes to query.
- `external_indus_objects.csv`: local external Indus-style object rows from the filtered Lipi metadata.
- `control_toponyms.csv`: negative/co-route controls so Meluhha is not special-pleaded.
- `cdli_current_query_fetch_log.csv`: current CDLI/ORACC query fetch log for the Lu-Sunzida hard-anchor test.
- `cdli_current_meluhha_artifacts.csv`: distinct CDLI artifact table across current Meluhha and Lu-Sunzida queries.
- `cdli_current_line_contexts.csv`: line-level CDLI context rows for the current query set.
- `cdli_current_lu_sunzida_test.csv`: matched-negative table testing whether `lu2-sun2-zi-da` is Meluhha-diagnostic.
- `cdli_current_anchor_failure_summary.json`: forger/skeptic summary rejecting the Lu-Sunzida shortcut as an external phonetic anchor.
- `external_phonetic_anchor_candidates.csv`: strict length/pattern candidate values generated for Meluhha-side cuneiform strings against external Indus-style rows.
- `external_phonetic_anchor_target_summary.csv`: target-level forger summary for the external phonetic-anchor attempt.
- `external_phonetic_anchor_forger_iterations.csv`: pattern-matched null iterations for the external phonetic-anchor attempt.
- `external_phonetic_anchor_summary.json`: machine-readable decision record: no strict external phonetic candidate survives.
- `cdli_meluhha_context_leads.csv`: ranked cuneiform-side context leads mined from current CDLI line contexts.
- `cdli_meluhha_context_lead_query_plan.csv`: diagnostic, anchor, and control query plan for the context leads.
- `cdli_context_lead_matched_negative_summary.csv`: paginated CDLI matched-negative results for the context lead queries.
- `cdli_context_lead_matched_negative_artifacts.csv`: artifact-level context and Meluhha-adjacency results for matched-negative queries.
- `context_lead_external_bridge_retest.csv`: retest of source-side survivor phrases against external Indus-style object rows.
- `context_lead_external_bridge_retest_summary.json`: machine-readable decision record: no context lead becomes an object-level external anchor.
- `gadd_ur_accession_bridge_audit.csv`: Ur/Gadd object-identity audit for local Ur rows, including verified `3898.1/U17649` and `3899.1/U8685` mappings.
- `gadd_ur_accession_bridge_audit_summary.json`: decision record for the Gadd Ur micro-bilingual gate; zero objects combine an Indus sequence with readable cuneiform.
- `gulf_type_indus_external_queue.csv`: Laursen Table 1 external Gulf Type `INDUS` rows converted into a source-acquisition queue; no accepted anchors.
- `failaka_kjaerum_acquisition_20260531.csv`: replacement-branch source-acquisition guardrail showing that the clean CDLI Failaka/Kjaerum publication route does not contain Laursen target catalogue nos. `279/319`.
- `failaka_kjaerum_acquisition_20260531_summary.json`: machine-readable decision record for the Failaka acquisition guardrail; accepted external anchors remain zero.
- `object_level_onomastic_value_attempts.csv`: direct object-routed value attempts from cuneiform Meluhha strings to external Indus rows; all rejected.
- `object_level_onomastic_value_forger_iterations.csv`: 10,000 target-site shuffle forger iterations for the strict mapped-object value attempt.
- `object_level_onomastic_value_summary.json`: decision record for the onomastic value harness; accepted external anchors remain zero.
- `manifest.json`: counts and caveats.

The joining rule is simple: join by date, provenience, object context, and source route first. Do not join by desired reading.

The expanded inventory currently holds 16 source-side rows from 10 requested source pages, with 18 successful fetches and zero failed fetches on 2026-05-29. The first literal site-overlap join surface has 25 rows across Ur, Girsu, Tello, and Nippur — but the forger (the adversarial null model that measures how often chance reproduces a result) rejects site overlap alone as evidence. Accepted external anchors remain zero.

The hard-anchor test checks whether one famous name can carry the weight. CDLI current exports find `lu2-sun2-zi-da` in 15 distinct artifacts, but only one has any Meluhha line, and only that one has adjacent Meluhha. A detector that fires on the name alone therefore has a measured false-positive rate of 0.933333. `P212982` remains a real cuneiform-side lead, not an Indus sign-value anchor.

The external-object phonetic attempt tried strict one-sign-per-cuneiform-unit matching against 29 Mesopotamia/Gulf focus rows. It generated apparent assignments for `me-luh-ha`, `ma2-me-luh-ha`, `lu2-sun2-zi-da`, and `szu-i3-li2-su` — but every positive target failed the pattern-matched forger, with null >= observed share 1.000000. The stronger duplicate-pattern title target `e-me-bal-me-luh-ha` produced no strict candidate at all. Accepted external anchors remain zero.

The context-lead matched-negative run tested 14 lead families across 52 unique paginated CDLI queries. `szu-i3-li2-su` now has 207 returned artifacts over three pages, 175 query-line hits, and only one Meluhha-bearing query-line artifact — a false-positive rate of 0.994286 as a Meluhha detector. `lu2-tukul`, `gurusz`, `nu-banda3`, `ur-{d}lamma`, and `ur-{d}ig-alim` likewise fail as standalone anchors. Nineteen source-side phrases survive, but only as cuneiform context leads, and mostly because they contain `me-luh-ha`. External retesting finds 23 query/site bridge rows, 4 Ur/Susa/Failaka-focus rows, 8 same-site length-pattern matches, and zero object-level bridges. Accepted external anchors remain zero.

The Ur/Gadd accession bridge audit ties `3898.1` to `U17649` and `3899.1` to `U8685` through local excavation IDs and Gadd/Penn routes. Both are Indus-inscribed external objects with no readable cuneiform/name/title bridge. In the modeled Gadd surface, seven objects carry only an Indus sequence and one (`BM 120573 / U.7683`) carries only cuneiform; zero are micro-bilinguals — no single object carries both. Accepted external anchors remain zero.

The Gulf Type acquisition queue normalizes Laursen Table 1 external `Gulf INDUS` rows `6-27` into `gulf_type_indus_external_queue.csv`. The immediate high-pressure rows are Kjaerum cat. `319/279` for Failaka, Amiet `1643` for Susa, Gadd nos. `15/16` for Ur, and Sarzec/Heuzey plate `30.3a-b` for Girsu. This is acquisition infrastructure only.

The Failaka source-acquisition guardrail cached and parsed CDLI publication `1773730` as an adjacent Kjaerum/Failaka route. Its four related artifacts cite `168-189`, `379`, `397`, and `399` — not Laursen's target `279/319` — and the DAI download route returned anti-bot HTML rather than a PDF. The replacement branch also cached publisher/library access routes through Aarhus University Press, CiNii Books, and Open Library, but none exposes the target catalogue pages digitally. The Failaka rows stay live as source-acquisition targets only.

The object-level onomastic value attempt tested 12 cuneiform-side Meluhha strings against 30 external Mesopotamia/Gulf rows with parseable signs. The only strict mapped-object attempt is `ur gun3-a me-luh-ha` against `3898.1/U17649`, proposing `002=ur;004=gun3;328=a;001=me;803=luh;415=ha`. It is rejected for two reasons: `U17649` is Indus-only, and the cuneiform phrase comes from a separate text. And the forger seals it: target-site shuffled nulls reproduce at least one strict mapped same-site pattern attempt in 0.6857 of iterations.

Next schema artifact: `docs/meluhha_matched_control_schema.md`.
