# research/docs

Notes from an LLM-assisted study of the Indus script. Most of the 427 files that used to sit here were working notes (source hunts, packet reviews, one-object gates). They are in `archive/`. Read the files below first.

## Start here

| File | What it is |
| --- | --- |
| [claim_ledger.md](claim_ledger.md) | Scoreboard: one accepted descriptive item (M-376 and M-391 share `861-533-717` after `002`), the live candidates, the retractions, and the instrument failures that are not retractions. Machine-readable twin: `../data/claim_ledger/claims.json`. |
| [reading_direction_note.md](reading_direction_note.md) | The Lipi catalogue stores inscriptions in reverse of the conventional (Mahadevan) order. Every Lipi "terminal" or "closure" result means the reading-initial end. |
| [strongest_result_brief.md](strongest_result_brief.md) | One page: what the repo can and cannot claim today. |
| [replacement_run_checkpoint_20260712.md](replacement_run_checkpoint_20260712.md) | The July restart point: what was accepted, demoted and closed, with the July decisions on 034, 603 and physical direction. |
| [mahadevan_crossface_constraints_20260905.md](mahadevan_crossface_constraints_20260905.md) | The one self-contained paper-style write-up: the cup + N-stroke reverse faces and what they imply for numerical readings (Fuls 2020). Credits Priyanka 2003 and Mukhopadhyay 2023 for the basic observation. |

## Current results (2026-10-01)

New tests are in `../extensions_20261001/` (one script, JSON output and a one-page REPORT.md each).

| Question | Result | Where |
| --- | --- | --- |
| Does the front inscription predict the cup + N-stroke count? | Yes within a catalogue; looks like production batches, not a portable rule. | `front_count/` |
| Are 034 tablets smaller than 032/033? | About 14% smaller in area (same format, one vote per source family). Reopens the July closure as a size difference, not a tier. | `size_034/` |
| Is there a 002-specific end effect? | Real for 861, 817, 820 and replicates in Mahadevan, where these are the known text-opening pairs 267-99 and 391-99 (Yadav et al. 2010). Not unique to 002. | `context_002/` |
| Do the roof/87 and 211 rewrites beat matched decoys? | Only selection-sensitively (1-9%); 94 other swap types recur as often. The candidate ranks last of 8 models in the campaign's joint test. | `alternation_null/` |
| Do the Sept-7 Sanskrit dictionary fits beat chance? | No. The optimizer is missing; a re-implementation does no better than Markov text with the same local repetition. | `phonetic_null/` |

## Known results: cite, do not re-derive

- Directionality of the sign order (stored order beats reversed): Yadav et al. 2010, PLoS ONE 5:e9506. Re-derived in `archive/effective_unicity_directionality_*.md`, `direction_order_baseline.md`, `lipi_*_order_baseline.md`. The recorded "failures" (leave-site-out, Lothal, L/R, Lipi/Mayig overlap) were small-sample artifacts.
- Conditional entropy and hidden-sign prediction: Rao et al. 2009, Science 324:1165. Re-derived in `archive/effective_unicity_methods_note.md`, `effective_unicity_*_comparator.md`, `findings_dossier.md`.
- Fish-sign diacritics and positional fish variants: Parpola 1994, Deciphering the Indus Script. Re-derived in `archive/parpola_sign60_local220_*.md`, `m041_middle_fish_omission_gate_20260712.md`, `decoding_followup_20260907.md`.
- Arithmetic reading of the stroke-count tablets: Fuls 2020, "Structural Analysis of Numerical Indus Inscriptions". Audited, not re-derived, in `mahadevan_crossface_constraints_20260905.md`; counter-field follow-up in `archive/decoding_followup_20260907.md`.
- Same front, different reverse (paired faces): Priyanka 2003; Mukhopadhyay 2023. Re-observed in `mahadevan_crossface_constraints_20260905.md`.
- Indus text against non-linguistic and known-script controls: Sproat 2014, Language 90:457. Re-derived in `archive/effective_unicity_nonlinguistic_comparator.md`, `effective_unicity_realworld_nonlinguistic_comparator.md`, `effective_unicity_known_script_comparator.md`, `effective_unicity_sumtablets_comparator.md`, `linear_b_series_d_scarcity_baseline.md`.

## Archive (`archive/`, 422 files, flat)

Links among archived files are relative and still work. A path written `docs/X.md` inside an archived file means `archive/X.md`. These are a historical record; the ledger above is the authority where they disagree.

| Files | Count | What it was and how it ended |
| --- | ---: | --- |
| `campaign_032_*` | 125 | The 002-861 branch: tails, source routes, controls, post-hoc partitions. Ended in one descriptive observation (M-376 / M-391); the 0.0002 false-positive rate came from a prefix chosen after the fact. |
| other `campaign_*` | 10 | The 002-Y branch gap, the 520/220 formula stem and unit boundary. No claim survived; the 520-220-X context slot is retracted. |
| `lipi_034_*`, `lipi_frame700_034_*`, `h933_h960_034*`, `frame700_034_*` | 71 | The 034 sign: source routes, matched contrasts, the size-tier test. Closed in July on one object; `../extensions_20261001/size_034/` finds a real size difference. |
| `effective_unicity_directionality_*`, order baselines, `m70`, methods notes | 26 | Directionality tests and blind source-review packets. The blind packets failed as instruments; the directionality result itself is Yadav 2010. |
| comparator and baseline docs | 9 | Indus vs. Linear B, SumTablets, non-linguistic and synthetic controls. Reruns of published comparisons. |
| `h*` (H-series objects) | 40 | Source-route and image hunts for individual Harappa tablets. Mostly "no usable public image"; no sign function established. |
| per-object gates (`m###_*`, `p###_*`, `parpola*`, `lipi_NNN_mayig_*`) | 39 | July 2026 decisions that gave each disputed object one settled reading. Housekeeping for the corpus, not findings. |
| `sign_*`, `provisional_*`, `mismatch_*` | 6 | Crosswalk between Lipi, Mayig, Mahadevan and Parpola numbering. Zero accepted edges; useful as a map. |
| `brahmi_*`, `meluhha_*`, `gadd_*`, `bm120573_*`, `gulf_*`, `failaka_*`, `external_anchor_*`, `deep_research_*` | 18 | External-anchor attempts (Brahmi descent, Meluhha names, Ur seals, Shu-ilishu). All rejected; zero anchors. |
| `lipi_*` probes | 26 | Class, short-mark, multi-side and subtype probes on the Lipi catalogue. Descriptive; no claim. |
| `vector*`, `formula_*`, `brief_*`, `structural_*`, `blind_boundary_*` | 19 | Terminal-formula, context-association and structural-class work. Register effects explain the apparent associations. |
| `source_*`, `cisi31_*`, `corpus_*`, `completion_gap_*`, `translation_*` | 15 | Source catalogue and URL-check logs (14k words), access requests, corpus freeze, blind-review protocols. |
| ledgers, plans, checkpoints (`evidence_ledger`, `findings_dossier`, `research_manifest`, `experiment_backlog`, ...) | 13 | Process records from May to July. Superseded by the claim ledger. |
| `decoding_followup_20260907`, `semantic_reading_search_20260906`, `slm_*`, `open_prototype_results` | 5 | Sept phonetic and compositional searches and the SLM test. No reading found; the phonetic fits do not beat Markov controls; SLM transfer is matched by non-writing pretraining. |
