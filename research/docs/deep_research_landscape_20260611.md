# Deep research landscape — Indus script frontier (2024–2026)

Date: 2026-06-11 America/Los_Angeles

Status: external landscape synthesis. No reading, value, phonetics, language identity, function, sign meaning, or translation is accepted by this document. It stages cited routes and comparators only.

## Scope And Method

This is the synthesis half of a deep-research pass run on 2026-06-11. Five angles were swept: (1) source-acquisition routes for the four blocking objects (H-1993, Dholavira 8758/4237.1, M-1825, 3335.1), (2) computational decipherment state of the art, (3) corpus and sign-inventory landscape, (4) decipherment validation methodology comparators, (5) external anchor candidates.

Each claim below carries a source URL and a confidence tag. An adversarial verification pass was applied: for every "decipherment" or "binding achieved" claim, an independent source or rebuttal was sought, and the claim was kept only if it survived. Per-claim verdicts are recorded in `evidence/tmp/041_source_acquisition_20260611/claim_verification_ledger.csv`.

Environment constraint, recorded honestly: this run's network allowlist passes the approved search/fetch proxy but blocks direct artifact download (raw `arxiv.org` and `wikimedia.org` pulls returned `Host not in allowlist`; `harappa.com` and the Wikimedia file page returned HTTP 403 to automated fetch). So this batch confirms routes and metadata; it does not add binary source images. That is the same evidence-tier ceiling the prior run hit, now re-confirmed from a fresh angle.

## 1. The four blocking objects — route state

Full per-target detail is in `docs/source_route_updates_20260611.md`. Summary:

- **CISI 3.1 is the correct, still-gated shared source for H-1993 and M-1825.** The volume is *Corpus of Indus Seals and Inscriptions, Volume 3: New material, untraced objects, and collections outside India and Pakistan, Part 1: Mohenjo-daro and Harappa*, ed. Asko Parpola, B. M. Pande, Petteri Koskikallio, in collaboration with Richard H. Meadow and J. Mark Kenoyer; Suomalainen Tiedeakatemia, Helsinki, 2010; 504 pp.; Annales Academiae Scientiarum Fennicae Humaniora 359 / Memoirs of the Archaeological Survey of India no. 96; ISBN 9789514110405; contains photographs, line drawings, and tables. This independently confirms the prior run's acquisition target identity and the Meadow/Kenoyer Harappa authorship behind the `H96-2769 / Figure 17.07` material. Confidence: HIGH. Sources: harappa.com vol-3.1 page; Helsinki research portal; Cambridge JRAS review; AbeBooks ISBN listing.
- **No free full-text download was obtained.** The academia.edu record for the volume exists but is access-gated; the harappa.com page and the Wikimedia file page returned 403 to automated fetch; the environment allowlist blocked direct pulls. This neither proves nor disproves that a scan exists elsewhere; it records that the public, frictionless route is still purchase/library-gated, matching the prior run's Tiedekirja payment-pending state. Confidence: HIGH (for "not obtained here"), MEDIUM (for "not obtainable anywhere").
- **New lead the prior run did not record: CISI volume 3.3 (2022).** *Corpus of Indus Seals and Inscriptions* vol. 3.3, ed. Parpola & Koskikallio, Finnish Academy of Science and Letters, 2022, exists and includes D. T. Potts (2022) "The Graffiti from Tepe Yahya …". The vol. 3 series ("New material, untraced objects, and collections outside India and Pakistan") is precisely the strand that should be checked for unprovenanced / "untraced" objects like 3335.1 (`RAF`, no CISI id) before declaring its source dead. Confidence: MEDIUM-HIGH. Sources: academia.edu records 94861598, 94880292.

## 2. Computational decipherment — state of the art

- **The conditional-entropy debate remains unresolved and is the methodological backbone for this project's null-model discipline.** Rao et al. (2009, *Science*) argued the script's conditional entropy is language-like; Sproat and Farmer reply that conditional entropy is a measure of order, not a discriminator of linguistic vs non-linguistic systems. Both sides agree that, barring full decipherment, neither thesis is provable. This is exactly why this project accepts structure but refuses language identification. Confidence: HIGH. Sources: Language Log (ldc.upenn.edu/nll/?p=1374); Rao reply (homes.cs.washington.edu/~rao/IndusCompLing.pdf); Farmer (safarmer.com/more.on.Rao.pdf).
- **Nair (2026), arXiv:2604.17828, is directly comparator-relevant and uses the same corpus this project uses.** "How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard" (submitted 2026-04-20) tests the observed corpus against two synthetic non-linguistic baselines (heraldic, administrative), each calibrated with Zipfian frequencies, positional constraints, and bigram dependencies from six attested non-linguistic corpora, scoring the four Farmer-Sproat-Witzel (2004) properties (brevity, repeated formulae, hapax rate, positional rigidity). It runs on **1,916 deduplicated inscriptions, 584 unique signs, 11,110 tokens, from the ICIT/Yajnadevam digitization** and reports an intermediate result, not a clean language/not-language verdict. Reproducibility caveat from the prior literature note stands (abstract says data public; arXiv comment says code on request). Confidence: HIGH (existence/specs). Sources: arxiv.org/abs/2604.17828; this repo's `notes/2026-05-24-literature-update.md`.
- **The Tamil Nadu prize is real, named, and unclaimed.** CM M. K. Stalin announced a US$1,000,000 award in January 2025 at the Chennai conference marking the IVC centenary; it is named the **Iravatham Mahadevan Prize**. Reporting notes there is still no official submission portal. The prize has driven a wave of fresh claims; none is accepted. Confidence: HIGH. Sources: archaeologymag.com (2025/01); business-standard.com; smithsonianmag.com; euronews.com.

## 3. Live claimed readings and their reception (all contested; none accepted here)

- **Yajnadevam (cryptographic Sanskrit).** Treats the corpus as one cryptogram, applies Shannon unicity-distance reasoning, and claims a pre-Paninian Vedic Sanskrit reading. Contested on three grounds: not peer-reviewed / not journal-published; output "doesn't sound like" Vedic or classical Sanskrit (Sivasenani Nori); the many-signs-to-one-syllable mapping has no script precedent and permits overfitting. This independently supports the project's existing quarantine of the Lipi `sanskrit`/`translation` columns. Confidence: HIGH (not peer-reviewed), MEDIUM-HIGH (specific flaws). Sources: kyabaat.blogspot.com (2025/03); vshiksha.com; academia.edu 128566898 ("A short, definitive flaw …"); Medium/Tamilselvan (2025/08).
- **Mukhopadhyay (administrative semasiography).** 2023 *Humanities and Social Sciences Communications* (Nature) paper argues Indus inscribed objects are administrative-commercial instruments (tax tokens, trade/craft licences, metrological records) — a functional, semasiographic reading rather than a phonetic language claim. This is the most institutionally-published functional hypothesis and is a useful comparator for a structure-first program; it is a hypothesis, not an accepted decipherment. Confidence: HIGH (publication), MEDIUM (reception). Sources: nature.com/articles/s41599-023-02320-7; SSRN 4316270, 3778943.

## 4. Validation comparators — what makes a decipherment stick

- **Linear Elamite (Desset et al. 2022) shows that a top-journal "decipherment" can still be field-contested.** Published in *Zeitschrift für Assyriologie und Vorderasiatische Archäologie*; reception is mixed; Born et al. (forthcoming) argue many of the Linear-Elamite-to-proto-Elamite sign comparisons are unlikely; skeptics withhold assent pending detailed, checkable text translations. Lesson for this project: publication venue is not validation; checkable, predictive readings are. Confidence: MEDIUM-HIGH. Sources: en.wikipedia.org/wiki/Linear_Elamite; anetoday.org/desset-irans-linear-elamite-deciphered; ora.ox.ac.uk (proto-Elamite relationship).
- **Linear B and Maya (background anchors).** The decipherments that held were confirmed by *external predictive events* (Blegen's Pylos tripod tablet matching Ventris's values) and by *compounding independent evidence* (Maya: Knorozov's phonetic complementation plus Proskouriakoff's historical-structure readings cross-checking). The common thread is out-of-sample prediction, not in-sample fit — the standard this project encodes as its forger/null + blind-adjudication gates. Confidence: HIGH (well-established history). (Background; standard references.)

## 5. External anchors — the most tractable source-visible lead

The project's external-anchor count is 0 and the bar is source-visible imagery, not mention. The single most tractable, well-provenanced, freely-illustrated contact anchor is the **Shu-ilishu cylinder seal, Louvre AO 22310** (serpentine, ~2020 BCE, late Akkadian), whose cuneiform names its owner an "interpreter of the Meluhhan language." Full candidate write-up, with the explicit caveat that it is a *contact* anchor and **not** a bilingual (no Indus signs are securely read on it), is in `docs/external_anchor_shu_ilishu_AO22310_candidate_20260611.md`. It does not earn an external-anchor claim under the ledger gates; it is staged as the best-imaged starting point for that lane. Confidence: HIGH (artifact facts), HIGH (it is not a bilingual). Sources: penn.museum Expedition "Shu-ilishu's Cylinder Seal"; Wikimedia Commons File AO 22310.

Secondary anchor lanes worth queueing (mention-level, not yet imaged here): Gulf/Dilmun seals (Failaka, Bahrain) with Indus-related signs; Indus-style seals from Ur (Gadd 1932) in the British Museum; Meluhha personal-name onomastics in Ur III Lagash texts. These remain acquisition targets, not anchors.

## Net Effect On The Project

Nothing here promotes any reading. Concretely, batch 041:

1. Re-confirms (from a fresh angle) that CISI 3.1 is the right gated source for H-1993/M-1825 and that no free full image binding is reachable in this environment.
2. Adds one genuinely new acquisition lead — CISI vol. 3.2/3.3 "untraced objects" strand — as the next place to chase 3335.1 (`RAF`) before calling its source dead.
3. Anchors the project's structure-only, null-model-first stance in the current external literature (Rao/Sproat unresolved; Nair intermediate scorecard on the same corpus; Yajnadevam contested; Desset contested).
4. Surfaces the strongest source-visible external-anchor starting point (Shu-ilishu AO 22310) without overclaiming it.

Next useful work is unchanged in kind: acquire the gated CISI volumes (now including 3.2/3.3 for untraced objects), and pursue museum-database image binding for the anchor lane.
