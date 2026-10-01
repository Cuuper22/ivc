# 3335.1 source-identity recheck for `002-390-X`

Date: 2026-05-31 America/Los_Angeles

Status: identity/source gate triaged; no source-token upgrade.

## Target

Local row:

- Row: `3335.1`
- Object: `-`
- Site/region: Unknown / Other
- Type: `SEAL:S`
- Symbol/cult: `Bull1:J` / `RAF`
- Shape: square
- Dimensions: `2.9cm x 2.9cm`; normalized local fields `29 x 29 x 0`
- Direction: `R/L`
- Text: `+740-205-032-002-390-590-032+`
- Structural role: continuing non-`125` branch inside adjacent `002-390-X`: `032 -> 002-390 -> 590 -> 032`

The question was whether this raw continuing non-`125` exception can be source-bound or at least identified through the nearby Mohenjo-daro numbering gap.

## Row-order trap: `M-940`

The local corpus order places `3335.1` between:

- `3334.1 / M-939`, text `+527-550+`
- `3336.1 / M-941`, text `+000-642-240-031-002-861+`

Sitting between `M-939` and `M-941`, the row made `M-940` a tempting inferred identity. The inference fails.

Local metadata already has a separate `M-940` row:

- Row: `2243.1`
- Object: `M-940`
- Site: Mohenjo-daro
- Excavation id: `DK1211060`
- Text: `+527-555-002-817+`
- Dimensions: `20.8 x 20.8 x 7.1`

CISI Pakistan page 91 / IA leaf `n125` visibly contains `M-940 A`, `M-940 a`, and `M-940 a bis`, between the neighboring `M-939` and `M-941` entries. The page image is stored here:

- `tmp/3335_source_identity_recheck_20260531/cisi_pakistan_n125_w2400.jpg`
- `tmp/3335_source_identity_recheck_20260531/M940_cluster_cisi_pakistan_n125_w2400_crop.png`

Archive source:

- `https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n125_w2400.jpg`

The visual page therefore confirms that `M-940` is not missing and cannot be silently reassigned to `3335.1`. It is already a distinct four-sign local row, and the visible `M-940` cluster does not match the seven-sign `3335.1` target.

## Public and local route checks

Exact public searches for the target string and local gloss did not recover a usable source route:

- `"+740-205-032-002-390-590-032+"`
- `"740-205-032-002-390-590-032" Indus seal`
- `"3335.1" "740-205"`
- `"sva-rava-sahana" Indus`

The hits were Sanskrit dictionary/noise pages or unrelated numeric PDFs, not an Indus catalog object, source plate, excavation id, museum handle, or image.

Local source-route tables also keep the row blocked:

- `campaign_032_002_branch_tail_source_routes.csv`: `blocked_until_object_id_resolved`
- `campaign_032_002_source_normalized_branch_tail_decisive_rows.csv`: `no_object_id`
- `campaign_002_y_partition_source_queue.csv`: `source_hint_only`
- `campaign_032_002_861_002390x_branch_sign_ecology_20260531_exceptions.csv`: raw continuing non-`125` exception only

The `RAF` tag does not solve identity either. In `metadata_filtered.csv`, `RAF` occurs in 57 rows, and only three `RAF` rows lack a CISI object id: `3335.1` plus two Dholavira rows. So `RAF` is a source-family/context clue, not an object bridge.

## Decision

Current status:

`3335_1_m940_false_bridge_rejected_object_id_blocked_no_source_count`

Use `3335.1` as:

- Yes: raw local metadata pressure that `002-390` can have a continuing non-`125` branch.
- Yes: an acquisition target, especially for whatever source fed the cisi-less `RAF` rows.
- No: a source-normalized exception.
- No: a source-bound `590 -> 032` witness.
- No: an inferred `M-940` duplicate or missing CISI row.
- No: sign value, phonetics, function, language identity, meaning, or translation.

## Consequence for `002-390-X`

The local adversarial pressure remains: `3335.1` is a continuing non-`125` branch in the 15-row matrix. But the source-normalized pressure does not increase, because nothing new binds the row to a real object. For strict or source-bound model testing, `3335.1` must stay out until a real object/source bridge is found.

This leaves H-773 as the only currently image-panel-bound continuing non-`125` pressure row, and even H-773 remains boxed-compatible rather than token-strict. The positive model cannot use `3335.1` to prove a branch-conditioned exception, and the adversarial model cannot use it as a source-bound catalog artifact either. It remains live, but unbound.

