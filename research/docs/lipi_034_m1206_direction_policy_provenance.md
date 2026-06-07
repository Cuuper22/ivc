# Lipi 034 M-1206 Direction Policy Provenance

Date: 2026-05-26

## Question

Where do the `R/L` fields for `H-938 B` and `H-910 B` come from, and can they be treated as source-grade direction evidence?

## Answer

They come from the Lipi corpus metadata field `dir.`.

The local source-image/component work does not derive `R/L` from the CISI panels. It consumes the recorded field and tests what follows from it.

So the admissible state is:

```text
recorded R/L = working corpus policy;
source-proven direction = not yet;
direct 034=415 component identity = negative under recorded R/L;
if recorded R/L fails = unresolved, not positive.
```

## Provenance Chain

| Step | Evidence | Result |
| --- | --- | --- |
| Local retained corpus field | `data/open_prototype/lipi/metadata_filtered.csv`, header includes `dir.` | Direction is present before the component probes. |
| H-910 target row | `1792.2`, `H-910`, `dir.` = `R/L`, `text` = `+700-034+` | H-910's order assignment is inherited from corpus metadata. |
| H-938 target row | `1818.2`, `H-938`, `dir.` = `R/L`, `text` = `+034-700+` | H-938's order assignment is inherited from corpus metadata. |
| Upstream check | Current Yajnadevam `lipi` raw CSV downloaded 2026-05-26 to `tmp/lipi_current_inscriptions_20260526.csv` | Current upstream target rows match the local `dir.` and `text` values. |
| Script propagation | `data/open_prototype/tools/lipi_scope_probe.mjs` reads `row[column['dir.']]` through `cleanDirection` | The scripts copy/normalize direction; they do not compute it from images. |
| Component gate | `data/open_prototype/reports/lipi_034_m1206_h938_h910_direction_sensitivity_gate.csv` | Recorded `R/L` is tested as a policy; forced `L/R` is only a counterfactual. |

## Source-Visible Checks

The source panels do prove some things:

- `H-938 A/A bis` are the clean exact-side `415` control for local `1818.1 +520-220-415+`.
- `H-938 B` is the source-visible companion side for local `1818.2 +034-700+`.
- `H-910 B` is source-visible and gives the mirror-order component check for local `1792.2 +700-034+`.
- `H-930` and `H-789` are clean two-panel FRAME700 controls where the source panel split matches local short/long side expectations.

They do not prove the reading direction field itself. The clean two-panel controls explicitly lack an independent visible direction basis, and the CISI original/impression convention blocks silently reversing a scan just because it makes the component assignment nicer.

## Consequence For The 034/415 Question

Under recorded `R/L`:

- `H-938 B +034-700+`: `034` maps to the right loop/leaf component; `700` maps to the left vertical/rake component.
- `H-910 B +700-034+`: `034` maps to the left loop/leaf component; `700` maps to the right vertical/rake component.

That is negative for direct component-level `034=415`, because the `415`-like component is the vertical/rake component, not the component assigned to `034`.

Under forced `L/R`, the result flips. That is not accepted, because no checked source/transcription-policy evidence currently licenses replacing the recorded `R/L` fields.

## Accepted

- The `R/L` values are inherited from Lipi/Yajnadevam corpus metadata and preserved locally.
- Local scripts propagate direction; they do not infer it from source images.
- Source images validate the relevant panels and component positions.
- Direct `034=415` component identity is rejected under recorded `R/L`.

## Not Accepted

- Source-grade proof that `H-938 B` or `H-910 B` must be read `R/L`.
- A forced `L/R` rescue of `034=415`.
- Any global `034`/`415` sign-identity decision.
- Any allograph status, sign value, function, language identity, or translation.

## Next Gate

Find one of:

1. Source/corpus notes defining how `dir.` was assigned for `H-938 B` and `H-910 B`.
2. Independent source-visible `+700-032+`, `+700-033+`, and `+700-034+` controls where component ownership can be checked without relying on this same pair.
3. An object-specific bridge from CISI/HARP/Mahadevan side notes that ties physical side, local row, direction, and sign segmentation together.
