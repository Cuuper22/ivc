# Evidence batch 041 — source acquisition + external landscape (2026-06-11)

This directory stages the deep-research pass of 2026-06-11. It is documentation and verification, not binary source artifacts.

## Why no binary artifacts

This run's network allowlist passes the approved search/fetch proxy but blocks direct artifact download. Recorded outcomes:

- Raw `https://arxiv.org/pdf/2604.17828` -> `Host not in allowlist`.
- Raw Wikimedia `Special:FilePath` for Louvre AO 22310 -> `Host not in allowlist`.
- `https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31` -> HTTP 403 to automated fetch.
- Wikimedia file page for AO 22310 -> HTTP 403 to automated fetch.

So this batch records confirmed routes, metadata, and verification verdicts. Binary source images (CISI plates, the AO 22310 photo) remain to be fetched by a human or an authenticated tool. No SHA-256 artifact manifest is included because no artifact was fetched; fabricating one would violate the project's source-binding standard.

## Files

- `sources_manifest.csv` — every external URL touched, what it binds, access status, confidence.
- `claim_verification_ledger.csv` — falsifiable claims extracted, adversarial 3-vote verdict, confidence.

## Companion docs (outside this dir)

- `research/docs/deep_research_landscape_20260611.md` — synthesized cited report.
- `research/docs/source_route_updates_20260611.md` — per-target updates for H-1993, Dholavira 8758, M-1825, 3335.1.
- `research/docs/external_anchor_shu_ilishu_AO22310_candidate_20260611.md` — external-anchor candidate.
- `research/notes/2026-06-11-literature-update.md` — delta vs 2026-05-24 notes.

## Boundary

No reading, value, phonetics, language identity, function, sign meaning, translation, or external anchor is accepted by this batch. The claim ledger (`research/data/claim_ledger/claims.json`, `research/docs/claim_ledger.md`) is unchanged. Accepted counts remain: translations 0, phonetic values 0, sign meanings 0, language identification 0, external anchors 0, structural findings 1.
