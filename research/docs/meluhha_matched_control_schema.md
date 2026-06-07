# Meluhha Matched-Control Schema

Date: 2026-05-29

The site-overlap gate failed, so Vector 1 now needs pairwise matched controls. Raw site overlap is a blocking stratum, not evidence.

## Row Model

Each row should be one observed or control candidate inside a `match_set_id`.

Recommended arms:

- `observed_meluhha_join`
- `same_external_site_non_meluhha_cuneiform`
- `same_cuneiform_source_class_nonoverlap_external_site`
- `same_external_object_context_shuffled_site`
- `same_external_sign_sequence_non_meluhha_cuneiform`

Core fields:

```text
control_row_id
match_set_id
target_join_id
arm
control_family
status
cuneiform_attestation_id
cuneiform_term_class
cuneiform_control_toponym_id
cuneiform_source_system
cuneiform_source_id
cuneiform_line_ref
cuneiform_transliteration
cuneiform_translation
cuneiform_token_type
cuneiform_source_class
cuneiform_period_raw
cuneiform_date_start_bce
cuneiform_date_end_bce
cuneiform_date_precision
cuneiform_provenience
cuneiform_site_aliases
cuneiform_co_route_tokens
cuneiform_artifact_type
cuneiform_language
cuneiform_genre
cuneiform_source_hash
external_row_id
external_cisi
external_region
external_site
external_type
external_material
external_shape
external_symbol
external_text
external_text_length
external_sequence_family
external_object_context_bucket
external_date_start_bce
external_date_end_bce
external_date_precision
external_catalogue_ref
external_image_ref
external_validation_status
site_match_class
chronology_overlap
chronology_gap_years
object_context_match_class
sign_sequence_match_class
source_class_match_class
eligible_pool_size
selection_rule
random_seed
exclusion_reason
forger_metric_bucket
skeptic_flags
notes
```

## Populated Now

- Cuneiform identity, line, transliteration, token type, period/date strings, provenience, source class proxies, and source hashes: `data/meluhha/cuneiform_attestations_expanded.csv`
- Target join IDs and external object fields: `data/meluhha/meluhha_indus_join_surface.csv`
- External object pool, still T3/quarantined and undated: `data/meluhha/external_indus_objects.csv`
- Control toponym seeds: `data/meluhha/control_toponyms.csv`
- Fetch routes/status: `data/meluhha/cuneiform_source_routes.csv`
- Null failure baseline: `data/meluhha/meluhha_join_surface_null_summary.json`

## Missing Before Scoring

P0 fetch/acquisition needs:

- Catalogue/image validation for the 41 external Indus-style objects, especially the 25 joined rows.
- Date range, find context, source citation, image/source hash, accession/publication IDs for each external row.
- Non-Meluhha cuneiform controls for Dilmun, Magan, Marhasi, Elam, Gutium, Gubi, and Susa.
- Provenience-matched non-Meluhha rows from Ur, Girsu/Tello, and Nippur, matched on period and source class.
- Validated external object pools with same object contexts, such as `SEAL:C/circular/Gaur`, `SEAL:S/square/Tigr`, and `SEAL:S/square/Zebu`.
- Exact or near sign-sequence family controls for joined external texts, validated from catalogue/image sources.
- Primary Shu-ilishu / AO 22310 inscription edition check.

## Scoring Rule

The target is conditional enrichment inside matched strata. Meluhha rows must beat non-Meluhha controls after matching on site/provenience, date, cuneiform source class, external object context, and sign-sequence family.

No matched-control row can become an external anchor until it has a measured forger false-positive rate and a skeptic pass.
