# Corpus Freeze Manifest

Date: 2026-05-24

## Freeze Name

```text
ivc-corpus-2026-05-24-open-prototype
```

## Purpose

A corpus freeze is a snapshot with a name: once frozen, its inputs, versions, and filters cannot change silently, so any experiment that cites the freeze name can be rerun against exactly the same data.

This is the first non-authoritative working corpus freeze. Its job is to support parser design, source overlap checks, sign-string normalization decisions, and baseline experiment planning.

It is not a translation corpus. It is not authoritative. It cannot prove meaning.

## Inputs

### Input A: `mayig/indus-valley-script-corpus`

Trust tier: T2 open digitization.

Pinned source:

```text
Repository: https://github.com/mayig/indus-valley-script-corpus
Commit: ad2f1e218a34b8c33c57de0d6cb8d99272765bbb
Commit date checked: 2025-04-16
Checked locally: 2026-05-24
```

Observed structure:

- 179 corpus JSON files.
- 397 feature files.
- Sample file `corpus/m001_m099/m001.json` contains side `M-1A`.
- Sample grapheme IDs use Parpola-style notation such as `P121`, `P202`, `P385`, `P073`, and `P108`.
- README says JSON files represent artifacts, with sides and graphemes.
- README says graphemes are recorded left-to-right on the artifact side while the script is understood as right-to-left.
- README says seals are transcribed as sealings rather than as seal faces.
- README says the corpus uses Parpola numbering and additional feature vectors for finer graphemic distinctions.

Allowed use:

- Prototype parser.
- Grapheme-feature inspection.
- Crosswalk design.
- Comparison against other sources where IDs overlap.

Excluded use:

- Authoritative frequency counts.
- Accepted sign readings.
- Image-level validation.
- Semantic or linguistic claims.

### Input B: Yajnadevam `lipi` CSV, filtered

Trust tier: T3 claim-bearing dataset.

Pinned source:

```text
URL: https://raw.githubusercontent.com/yajnadevam/lipi/refs/heads/main/src/assets/data/inscriptions.csv
Checked locally: 2026-05-24
Rows observed: 5,679
```

Allowed columns:

```text
id
cisi
region
site
area-section
block-house
room-grid
excavation-idno
time
period
phase
depth
boss
material
color
shape
cross-section
preservation
symbol
cult
type
sides
condition
complete
dir.
class
text length
signs
h
v
th
horizontal(mm)
vertical(mm)
thickness(mm)
text
```

Quarantined columns:

```text
sanskrit
translation
notes
```

Allowed use:

- Metadata coverage checks.
- Direction distribution checks.
- Completeness distribution checks.
- Candidate overlap with CISI-style IDs.
- Comparison against other sign-string sources.

Excluded use:

- Any claimed Sanskrit, phonetic, semantic, or English translation data.
- Any model input containing the quarantined columns.
- Any prompt context that could leak the quarantined labels into interpretation.

## Source Priority

When two sources disagree about the same artifact, the disagreement is settled by distance from the physical object:

1. Primary image/publication beats all.
2. CISI/ICIT/M77 beats open digitization.
3. Open digitization beats claim-bearing dataset.
4. Claim-bearing dataset can only trigger an audit question, not resolve it.

## Required Record Fields

Every merged working record must include:

```text
local_record_id
freeze_name
source_records
artifact_id
cisi_id
source_priority
raw_sign_strings
normalized_sign_string
direction
direction_basis
object_type
site
region
material
iconography
completeness
damage_or_uncertainty
sign_authority
allograph_policy
trust_tier
excluded_from_core
exclusion_reason
claim_columns_removed
primary_image_checked
notes
```

## Normalization Policy For This Freeze

The two input sources write signs in incompatible notations, and there is no evidence yet for how they map onto each other. So sign strings are not forced into one sign list. Each record preserves both notations side by side:

- `raw_mayig_graphemes`: e.g. `P121 P202 P385 P073 P108`.
- `raw_lipi_text`: e.g. `+740-540-002-820+`.
- `normalized_placeholder`: empty until crosswalk evidence exists.
- `crosswalk_status`: `unmapped`, `mapped`, `conflict`, `partial`, or `not_applicable`.

This prevents a fake precision problem where two incompatible sign systems are silently treated as identical.

## Core Exclusion Rules

Exclude from core analysis if:

- No stable artifact ID exists.
- Text contains unresolved missing signs that cannot be encoded.
- Source is only T3 or lower and no cross-source check exists.
- Direction is missing and the experiment depends on direction.
- Record comes from any source with translation labels that were not removed.
- Artifact authenticity is questioned and not resolved.

Excluded records can remain in an audit table.

## First Freeze Questions

These are the questions this freeze exists to answer:

1. How many `mayig` IDs overlap with filtered `lipi`/CISI IDs?
2. For overlaps, do sign counts agree?
3. For overlaps, do directions agree?
4. Which source has richer archaeological metadata?
5. Which source has richer graphemic/allograph metadata?
6. Which mismatches are due to sign-list notation rather than real disagreement?
7. Which records can enter structural experiments without image validation?

## Freeze Status

Status: first audit artifacts materialized locally.

Local artifacts:

- [Open prototype corpus artifacts](../data/open_prototype/README.md)
- [Open prototype results](open_prototype_results.md)

Current limitation:

The prototype is still not authoritative. It supports overlap triage and parser/crosswalk design, not translation.
