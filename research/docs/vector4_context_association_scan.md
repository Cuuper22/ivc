# Vector 4 Context-Association Scan

Date: 2026-05-29

## Question

This note records a broad search for signs that go with particular kinds of object, and the killing of every lead it produced.

The idea. If a sign turns up overwhelmingly on copper tablets, or beside one animal motif, that would tell us something about the sign without anyone having to guess how it sounded. Vector 4 is this project's line of work on exactly that: context semantics, meaning from company kept. "Earning" an association means clearing the controls the project requires before a lead can be believed. A "scan" is a broad exploratory sweep over many candidates at once. `lipi` is the filtered catalog dataset the project computes from; numbers like `407` and `158-806` are its sign codes, not readings; `TAB:C` and `TAB:B` are catalog artifact-type codes.

Can any sign or short sign unit earn a context association from object metadata and iconography without assigning sounds?

The broad scan tests unigrams, bigrams, first signs, and last signs against object/context labels: type, material, symbol, cult, type-symbol, material-type, site-type, and site-type-symbol.

## Method

Script: `data/open_prototype/tools/vector4_context_association_scan.mjs`

Input: `data/open_prototype/reports/lipi_scope_rows.csv`

Scope:

- `readiness_bucket = lipi_numeric_clean_candidate`
- `complete=Y`
- no `000`, question marks, brackets, slashes, or complex text

Two collapse modes were run:

- `context_exact`: collapse by `text + site + type + material + symbol + cult`
- `text_only`: collapse by exact text, retaining context labels as a per-text union

Both modes ran 100 iterations for each null model. A null model is a scrambled version of the data that keeps some structure but destroys the sign-to-context link, so a real association has to beat it:

- `shuffle_contexts_global`
- `shuffle_contexts_within_site`
- `shuffle_contexts_within_token_count`
- `shuffle_units_within_site_type`

The reported false-positive fields are family-wise, meaning they account for the whole scan rather than one pair at a time — otherwise testing thousands of pairs would guarantee a winner by luck. A candidate is compared against the strongest discovered association in each null run, not only against the same pair.

## Result

No context-sign association survives as an accepted candidate.

In `context_exact` mode, the top association is `407` with Mohenjo-daro `TAB:C`/copper context:

- Support: 25
- z: 16.520717
- Whole-scan max-null share: 1
- Worst null: `shuffle_units_within_site_type`

That is a corpus/register association, not a sign meaning.

The most tempting symbol-specific lead was `158-806` with `symbol=Phyt`:

- `context_exact` rank: 22
- Support: 5
- z: 12.839621
- Whole-scan max-null share: 1

The skeptic check — a deliberate attempt to argue the lead down — breaks it. Three of the five supporting context rows are the exact same inscription text `+158-806-465+` split across material/context variants. Under `text_only` collapse, support falls below the scan's own minimum of five distinct texts, so the candidate is retracted as an association claim.

## Boundary

This is a negative Vector 4 result, not a failure of the vector. It found plausible-looking associations and then killed them with matched controls. No sign meaning, phonetic value, translation, or language-family claim follows.

"Promotion" means moving a lead to a stronger status in the project's ledger. Minimum next promotion test for `158-806 / Phyt`: exact-text collapse first, then a pre-registered focused test — one whose rules are fixed in writing before the data is looked at — inside matched Harappa `TAB:B` controls, stratified by length/material/position family, with at least five distinct exact texts or source-verified object families, leave-one-text-family survival, leave-one-material survival, and symbol-field false-positive rate <= 0.05 under at least 1,000 matched shuffles.

## Files

- `data/open_prototype/reports/vector4_context_association_summary.json`
- `data/open_prototype/reports/vector4_context_association_candidates.csv`
- `data/open_prototype/reports/vector4_context_association_nulls.csv`
- `data/open_prototype/reports/vector4_context_association_scope_rows.csv`
- `data/open_prototype/reports/vector4_context_association_text_only_summary.json`
- `data/open_prototype/reports/vector4_context_association_text_only_candidates.csv`
- `data/open_prototype/reports/vector4_context_association_text_only_nulls.csv`
- `data/open_prototype/reports/vector4_context_association_text_only_scope_rows.csv`
