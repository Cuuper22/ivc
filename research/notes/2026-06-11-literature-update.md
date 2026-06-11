# Literature Update

Date: 2026-06-11

Delta against `2026-05-24-literature-update.md`. Full synthesis with confidence tags and per-claim verification verdicts: `docs/deep_research_landscape_20260611.md` and `evidence/tmp/041_source_acquisition_20260611/`.

## Confirmed since May 24

### Nair 2026 (arXiv:2604.17828) — specifics nailed down

The May 24 note flagged this preprint and its reproducibility caveat. This pass confirms the specifics:

- Two synthetic non-linguistic baselines (heraldic emblem system; administrative coding system), each calibrated with Zipfian frequencies, positional constraints, and bigram dependencies from six attested non-linguistic corpora.
- Scorecard = the four Farmer-Sproat-Witzel (2004) properties: brevity, repeated formulae, hapax rate, positional rigidity.
- Corpus: 1,916 deduplicated inscriptions, 584 unique signs, 11,110 tokens, from the ICIT/Yajnadevam digitization — i.e. the same lineage this project uses.
- Result is intermediate, not clean language / not-language.

Impact: keep the reproducibility flag (code "on request"). Use the 1,916 / 584 / 11,110 figures as an external cross-check on our own deduplicated counts and as a baseline-strength comparator for our null models. Do not cite its result as settled.

## New since May 24

### CISI volume 3 series scope clarified (acquisition strategy)

The four blocking objects collapse to one coordinated source action. CISI 3.1 (2010, Parpola/Pande/Koskikallio with Meadow & Kenoyer) is the gated source for H-1993 and M-1825. CISI vol. 3.2/3.3 (3.3 = 2022, Parpola & Koskikallio) is the "untraced objects / collections outside India and Pakistan" strand — the right place to chase 3335.1 (`RAF`, no CISI id) before calling its source dead. See `docs/source_route_updates_20260611.md`.

### Tamil Nadu "Iravatham Mahadevan Prize"

US$1,000,000, announced by CM M. K. Stalin, January 2025, at the IVC-centenary Chennai conference. No official submission portal reported. Context only; it changes no evidence tier and has produced no accepted decipherment.

### Decipherment-reception landscape (all contested, none accepted)

- Yajnadevam (Sanskrit, cryptographic): not peer-reviewed; contested on overfitting (many signs → one syllable, no precedent) and non-idiomatic output. Independently supports our existing quarantine of the Lipi `sanskrit`/`translation` columns.
- Mukhopadhyay (administrative semasiography): 2023 Nature *Humanities and Social Sciences Communications* — the most institutionally-published functional hypothesis; a comparator for a structure-first program, not an accepted reading.
- Linear Elamite (Desset et al. 2022, ZA): a top-journal "decipherment" that remains field-contested (Born et al. forthcoming). Reinforces our rule: venue is not validation; checkable predictive readings are.
- Rao (2009 Science) vs Sproat/Farmer conditional-entropy debate: still unresolved; both sides agree neither thesis is provable without full decipherment. This is the backbone for our structure-only / null-model-first stance.

### External-anchor candidate staged

Shu-ilishu cylinder seal, Louvre AO 22310 (~2020 BCE, "interpreter of the Meluhhan language"), openly illustrated (Penn Museum *Expedition*; Wikimedia Commons). Staged as a *contact* anchor candidate, explicitly not a bilingual and not a reading. See `docs/external_anchor_shu_ilishu_AO22310_candidate_20260611.md`. Accepted external anchors remains 0.

## Research decision

No new claim is added to the ledger. The actionable changes are: (1) consolidate the four object hunts into one CISI vol.-3-series acquisition plus the Dholavira ASI-2015 / National Museum route; (2) open the external-anchor lane with the source-visible Shu-ilishu candidate; (3) use Nair's corpus figures as a null-model strength comparator. Environment limit recorded honestly: the network allowlist blocked direct artifact download this run, so routes/metadata were confirmed but no binary source images were added.
