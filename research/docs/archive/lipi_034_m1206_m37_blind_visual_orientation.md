# Lipi 034 M-1206 / M-37 Blind Visual Orientation Probe

Date: 2026-05-25

## Question

This note records a blind visual check of two seal photographs. `M-37` and `M-1206` are two seals whose photographs are now directly visible in public pages of CISI, the Corpus of Indus Seals and Inscriptions — the standard photographic corpus for these objects. The question: do the source images support a clean `520-220-X` terminal-substitution frame? Here `520`, `220`, and `X` are local numeric sign labels — transcription codes, not readings. In that frame, the two seals would share the `520-220` prefix and differ only in the final, terminal sign — the last sign in the inscription.

The probe is blind in a specific sense: we classify the visible three-sign face inscriptions by shape alone, and we deliberately avoid the numeric sign labels while doing it.

## Inputs

Source pages:

- `M-37`: CISI Vol. 1 India, IA leaf `n54`, printed p. 19, labels `M-37 A/a`.
- `M-1206`: CISI Vol. 2 Pakistan, IA leaf `n181`, printed p. 147, labels `M-1206 A+E`, `M-1206 A`, `M-1206 a`, and long side `M-1206 e(1)`.

We cut crops in display coordinates with .NET image cropping and stored them under:

```text
tmp/m1206_terminal_triad_source_recheck/derived/dotnet_m37_bottom_left_A.png
tmp/m1206_terminal_triad_source_recheck/derived/dotnet_m37_bottom_right_a.png
tmp/m1206_terminal_triad_source_recheck/derived/dotnet_m1206_top_left_AE.png
tmp/m1206_terminal_triad_source_recheck/derived/dotnet_m1206_top_right_A.png
tmp/m1206_terminal_triad_source_recheck/derived/dotnet_m1206_bottom_right_a.png
```

The `M-1206 e(1)` crop is kept as object-context evidence only. It is not part of the three-sign face comparison.

## Blind Glyph Classes

Across the M-37 and M-1206 face crops, the same broad visual classes recur:

```text
T = triangular / standard-on-stem or pennant-like sign
L = split leaf / fish-like sign with lower fork
R = rake / vertical-stroke bundle sign
```

Source image order, left-to-right in the displayed page crop:

| Object / crop | Displayed order | Notes |
| --- | --- | --- |
| `M-37 A` | `R-L-T` | The rightmost triangular sign has a strong vertical stem. The left stroke-bundle has a crossbar/rake look. |
| `M-37 a` | `T-L-R` | Mirror/order counterpart of `M-37 A` under the displayed page. |
| `M-1206 A+E` | `R-L-T` | Same broad order as `M-37 A`; triangle/pennant is simpler than M-37's stemmed form. |
| `M-1206 A` | `R-L-T` | Same broad order as `M-1206 A+E`; darker scan, but the three units are separable. |
| `M-1206 a` | `T-L-R` | Mirror/order counterpart of `M-1206 A`. |

## Adjudication

Adjudication is the judgment we make after the blind classification is done and the labels come back into view. The source images do support this cautious claim:

```text
M-37 and M-1206 share a three-sign face pattern at the broad visual class level: R-L-T / T-L-R across mirrored views.
```

They do not yet support this stronger claim:

```text
M-37 and M-1206 have identical sign forms with only one substituted terminal.
```

Reason: the outer signs are graphically close but not identical. In particular, the M-37 `R` form looks like a rake/comb with a crossbar and stem, while the M-1206 `R` form is more like a vertical-stroke bundle. The `T` class also varies: M-37 has a stronger standard-on-stem profile, while M-1206 has a simpler triangular/pennant profile.

This is exactly where false decipherments get born if we rush. The better live interpretation is:

```text
source_visible_broad_pattern_match_with_fine_form_split_pressure
```

## Effect On The Local Triad

Before this probe, the terminal triad looked like:

```text
M-37    +520-220-415+
M-1206  +520-220-034+
```

After source inspection, the visual pattern is not a clean semantic substitution. It is a broad visual recurrence with two competing explanations:

1. The local numeric system may be splitting fine graphic variants inside the same broad sign family.
2. The source images may preserve a real terminal distinction, but only after orientation and allography are controlled.

No sign value follows from either explanation.

## Next Gate

A gate is a decision checkpoint: a test the evidence must pass before any claim moves forward. Do not generalize from this two-object comparison. The next useful test is:

1. Pull more `520-220-415` source-visible examples and see whether the M-37 rake/comb variant is stable.
2. Pull any additional `520-220-034` source-visible examples if public sources expose them.
3. Ask blind reviewers to sort the outer `R` and `T` signs into fine-form bins before seeing local numeric labels.
4. Only then decide whether `034` and `415` behave like allographs — variant written forms of one and the same sign — or subtypes, or separate signs.

Accepted:

- M-37 and M-1206 have the same broad three-class face pattern in source images.
- A/a views behave as mirror/order variants in the displayed crops.

Rejected:

- No accepted `034 = 415`.
- No accepted `034` value.
- No accepted `415` value.
- No accepted `520/220` mapping from these images.
- No accepted terminal meaning, phonetic reading, or translation.

