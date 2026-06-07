# Corpus Acquisition Protocol

Date: 2026-05-24

## Purpose

No translation system exists without a corpus. The first research job is to assemble a clean, versioned, auditable corpus without importing anyone's decipherment claims as labels.

## Trust Tiers

| Tier | Name | Description | Allowed Use |
| --- | --- | --- | --- |
| T0 | Primary image/publication | CISI image, excavation publication, museum record, or directly cited artifact image. | Ground truth candidate after authentication. |
| T1 | Scholarly corpus | M77, CISI, ICIT, IDF80, Wells/Fuls derived tools. | Core corpus after source/version logging. |
| T2 | Open digitization | Open JSON/CSV derived from primary or scholarly corpus, with separable metadata and no forced readings. | Working corpus after audit. |
| T3 | Claim-bearing dataset | Dataset that includes decipherment columns, phonetic values, or translations. | Metadata only, with claim columns removed. |
| T4 | Synthetic/generated | Model-generated sequences or augmented datasets. | Stress tests only, never evidence for decipherment. |
| T5 | Web claim or social post | Unreviewed online claim. | Hypothesis mining only, never evidence. |

## Current Source Audit

### M77 / IDF80 / Indus Script Web Application

Status: High priority, not yet locally acquired.

Use:

- Baseline Mahadevan sign list and concordance.
- Compare sign frequencies, positions, and text length distributions.

Action:

- Inspect `https://indusscript.in/` manually for export paths.
- Record whether data are downloadable, scrape-prohibited, or only interactively viewable.
- If no clean export exists, use it as a reference and seek permission or published files.

### CISI

Status: High priority, not directly machine-readable from public web.

Use:

- Artifact images and publication-grounded object IDs.
- Authentication and visual allograph checking.

Action:

- Build a bibliography and acquisition list for CISI volumes.
- Use open digitizations only as indexes until image-level checks are possible.

### ICIT

Status: High priority, access-gated.

Evidence:

- The ICIT page says the database supports sign-list search, corpus search, syntagmatic and paradigmatic analysis, statistical tools, and maps.
- The same page says access requires asking the administrator at `fuls(at)epigraphica.de`.

Action:

- Draft a concise access request once the local audit framework is ready.
- Until access is granted, cite ICIT findings through papers that report their methods.

### `mayig/indus-valley-script-corpus`

Status: Useful open WIP digitization, not a primary source.

Observed on 2026-05-24 through the GitHub tree API:

- Total paths: 622.
- Corpus JSON files: 179.
- Feature files: 397.

Use:

- Test parser design.
- Prototype sign-feature crosswalks.
- Compare against CISI IDs.

Restriction:

- Do not treat as complete CISI.
- Do not use without recording commit hash.

### Yajnadevam `lipi` CSV

Status: Quarantined T3 dataset.

Observed on 2026-05-24:

- Rows: 5,679.
- Columns include corpus-like metadata plus `sanskrit`, `translation`, and `notes`.
- Rows by `complete`: `Y` 3,673, `N` 1,338, `?` 668.
- Direction values include `R/L` 4,265, `-` 776, `NR` 386, `L/R` 215, plus rarer values.

Allowed columns:

```text
id, cisi, region, site, area-section, block-house, room-grid, excavation-idno,
time, period, phase, depth, boss, material, color, shape, cross-section,
preservation, symbol, cult, type, sides, condition, complete, dir., class,
text length, signs, h, v, th, horizontal(mm), vertical(mm), thickness(mm), text
```

Quarantined columns:

```text
sanskrit, translation, notes
```

Restriction:

- The quarantined columns must not be loaded into any model, evaluator, prompt, or working table except for an explicit audit of that decipherment claim.

### Hugging Face `hellosindh/indus-script-synthetic`

Status: T4 synthetic dataset.

Evidence:

- The dataset card says it contains 5,000 synthetic sequences generated from models trained on 3,310 real archaeological inscriptions, plus exact seal matches separated as validation evidence.

Use:

- Stress-test recognizers and grammar scorers.
- Study how synthetic augmentation changes model confidence.

Restriction:

- Synthetic sequences cannot support claims about actual IVC meaning.
- Exact matches need independent confirmation in a real corpus.

## Canonical Local Schema

Every inscription record should eventually normalize to:

```text
record_id
source_corpus
source_version_or_commit
source_publication
source_page_or_url
artifact_id
cisi_id
site
region
period
phase
material
object_type
iconography
side
line
raw_sign_string
normalized_sign_string
reading_direction
direction_basis
completeness
damage_notes
sign_list_authority
allograph_policy
image_reference
license_or_access
trust_tier
excluded_from_core
exclusion_reason
```

## Corpus Freezing Rule

Every experiment must name a frozen corpus build:

```text
ivc-corpus-YYYY-MM-DD-<short-hash>
```

If the corpus changes, previous results are not silently overwritten. They become results for the older corpus build.

## First Acquisition Sequence

1. Freeze a `T2-open-prototype` corpus from `mayig` with commit hash and schema notes.
2. Build a `T3-filtered-metadata` table from the Yajnadevam CSV with quarantined columns removed.
3. Compare overlapping CISI IDs between the two open sources.
4. Inspect `indusscript.in` for M77/IDF80 access and export possibilities.
5. Prepare ICIT access request with a precise research purpose.
6. Acquire primary images/publications for any inscriptions used in semantic claims.

Supporting documents:

- [Corpus freeze manifest](corpus_freeze_manifest.md)
- [Sign crosswalk protocol](sign_crosswalk_protocol.md)
- [Source access requests](source_access_requests.md)
