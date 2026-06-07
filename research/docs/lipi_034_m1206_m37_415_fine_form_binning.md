# Lipi 034 M-1206 / M-37 415 Fine-Form Binning

Date: 2026-05-25

## Question

The M-37/M-1206 source probe found a real broad visual recurrence but blocked the lazy conclusion:

```text
M-37    +520-220-415+
M-1206  +520-220-034+
```

Both source images show a three-class face pattern, but the fine forms do not match cleanly. This packet asks whether local `415` has more source-visible examples, and whether those examples make `415` look like a stable fine form, a mixed/allographic bin, or just a catalog side-effect.

## Source Packet

The exact local `+520-220-415+` scout found 17 rows. This follow-up verified the public CISI 1/2 source panels currently reachable for:

```text
M-37
H-346
H-786
H-938
H-939
H-940
H-941
```

Fresh verified crops are stored under:

```text
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/
```

Manifest and contact sheet:

```text
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/verified_panel_crops_manifest.csv
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/contact_sheet_415_verified_panels.png
```

The earlier rough crop packet is not used for adjudication because several crops were partial or mislabeled. The verified contact sheet was visually checked before this packet was written.

After the first pass, a blind visual review was added:

```text
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_blind_review.csv
```

That review caught a real trap: the target-like visual panel is not always the side that naive local row order would predict.

## Visual Bins

The broad pattern now has real recurrence outside M-37, but the exact local side mapping is not settled for every candidate.

Strong source-visible target-like panels in candidate `415` objects:

| Unit | Source side(s) | Broad visual result | Weight |
| --- | --- | --- | --- |
| `H-786` | `H-786 A` | `T-L-R` target-like three-class side | strong visual, side mapping unresolved |
| `H-938` | `H-938 A/A bis` | `R-L-T` target-like three-class side | strong, duplicate photos collapsed |
| `H-940` | `H-940 A` | `T-L-R` target-like three-class side | strong |
| `H-941` | `H-941 A/A bis` | `T-L-R` target-like three-class side | moderate visual, side mapping conflict |

Weak or unresolved units:

| Unit | Problem |
| --- | --- |
| `H-346` | `H-346 A` is target-like but weak; scale/blur blocks fine-form identity. |
| `H-939` | No side survives strict blind review as a secure target. A is partial/ambiguous, B is not target-grade. |

Explicit side-mapping conflicts:

| Object | Conflict |
| --- | --- |
| `H-786` | Blind review finds the target-like side on source `A`, while the local exact row is `.2`; source `B` is not target-grade. |
| `H-941` | Blind review finds the target-like side on source `A/A bis`, while the local exact row is `.2`; source `B/B bis` is not target-grade. |

## Adjudication

Accepted cautiously:

```text
The candidate-object pool is not just the single M-37 witness anymore. Public CISI 1/2 images expose repeated broad three-class target-like panels in Harappa objects.
```

Not accepted:

```text
The exact local 415 side mapping is settled for all checked objects.
415 is a stable fine form.
034 = 415.
415 has a value.
The Harappa tablet sides and Mohenjo-daro seal side are equivalent semantic units.
Any translation.
```

The useful change is narrower and more important:

```text
The M-37/M-1206 contrast is now under stronger allograph/sign-splitting and source-side mapping pressure.
```

If `415` were a single stable fine form and local row sides mapped directly to source side labels, the Harappa examples should converge tightly on the M-37 terminal profile. They do not. They preserve the broad triangular/standard, split-leaf/fish, and rake/bundle family, but the incised tablet forms and side mappings vary enough that a numeric local split cannot be treated as semantic evidence.

## Prior-Work Pressure

The relevant prior-work lesson here is not "believe a sign list." It is the opposite: sign-list comparability, allography, mirroring, and segmentation have to be treated as live variables.

Local crosswalk pressure still makes the frame worth studying:

```text
520 -> P217 is consistent in the current overlap layer.
220 -> P050 is strong but not perfect.
415 -> P092 is not accepted, and 034 remains crosswalk-dark.
```

So the `520-220-X` frame can select source targets, but it cannot settle sign identity. The blind result reinforces the allograph/mapping warning that Daggumati-Revesz-style allograph work and the project's own crosswalk audits were built to catch.

## Adversarial Controls

Kuhn's attack survives in the packet:

- `A/A bis` and `B/B bis` are duplicate photograph evidence unless source notes prove otherwise.
- `H-786` and `H-941` cannot be counted as exact-side `415` evidence until source side labels are reconciled with local row numbering.
- Harappa tablets and Mohenjo-daro seals are separate strata, not one pooled semantic unit.
- Broad visual similarity is only a source-targeting result; sign identity needs side mapping, orientation control, and blind fine-form clustering.

This is why the packet counts recurrence as candidate-object pressure, not accepted sign identity.

## Effect On The 034 Branch

This does not kill the `034` branch. It changes what counts as progress.

The old tempting story:

```text
M-1206 and M-37 have the same prefix and different terminals, so 034 and 415 may contrast semantically.
```

The source-visible story after this packet:

```text
M-1206, M-37, and multiple 415 candidate objects share a broad three-class visual pattern. The decisive question is whether local 034/415 are fine-form splits, transcription-policy splits, allographs, true sign distinctions, or source-side mapping artifacts.
```

That is actual decipherment pressure because it removes a false shortcut. A value claim here would be fake precision.

## Stored Reports

```text
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_inputs.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_blind_review.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_bins.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_adjudication.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_summary.json
```

## Next Gate

1. Resolve `H-786` and `H-941` source/local side mapping before counting them as exact-side `415` evidence.
2. Keep `H-939` out of recurrence counts until stronger source imagery or side mapping appears.
3. Acquire route-dark exact `415` rows before claiming distribution over the whole `+520-220-415+` class.

Current accepted mappings, phonetic values, sign meanings, and translations:

```text
0
```
