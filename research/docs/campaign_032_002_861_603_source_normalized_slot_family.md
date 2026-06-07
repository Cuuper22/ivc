# Campaign: `032-002-861` / `603` Source-Normalized Slot Family

Date: 2026-05-29

## Research Question

Does the Harappa `740-X-240-060-692` family make `603` a real cross-slot bridge, or is the independent Harappa side just one copied/formulaic tablet family?

This is a source-normalization pass, not a value claim. It asks how much independent physical weight each X-slot witness deserves before using the slot linguistically.

## Inputs

Previous slot-substitution campaign:

```text
740-X-240-060-692

X = 603: H-1137, H-1138, H-1846
X = 636: H-360, H-823
X = 642: H-1845, H-237
```

Raw slot result: only `603` among observed X-slot values also appears as a post-`002-861` tail initial. `636` and `642` do not.

## Source-Visible Upgrades

### `603`

`H-1138` is now source-visible through Vats:

- Vats, *Excavations at Harappa*, vol. I text p. 345: tabulation entry for Plate XCIV no. 346.
- Vats, vol. II plates: Plate XCIV no. 346.
- Local crops:
  - `tmp/032_002_861_603_slot_source_normalization/H1138_Vats_Plate_XCIV_346_full_labeled_crop.png`
  - `tmp/032_002_861_603_slot_source_normalization/H1138_Vats_Plate_XCIV_346_signband_upper.png`
  - `tmp/032_002_861_603_slot_source_normalization/Vats_p345_tabulation_plate346_crop.png`

`H-1846` was already partly source-visible through Kenoyer and Meadow 1997:

- H95-2672 / Figure 11.11 / Table 2.
- Local crop:
  - `tmp/032_002_861_603_slot_source_normalization/H1846_H95_2672_Figure11_11_crop_v3.png`

`H-1137` remains route-only:

- Vats text p. 166 describes no. 7537 as similar to no. 346 in Plate XCIV.
- Local metadata maps `H-1137` to `7537824`.
- No direct local image for no. 7537 has been located yet.

### `636`

`H-360` is now source-visible through Vats:

- Vats text route: no. 3508 / Plate XCVIII no. 584.
- Vats, vol. II plates: Plate XCVIII no. 584.
- Local crops:
  - `tmp/032_002_861_603_slot_source_normalization/H360_Vats_Plate_XCVIII_584_full_labeled_crop.png`
  - `tmp/032_002_861_603_slot_source_normalization/H360_Vats_Plate_XCVIII_584_signband_crop.png`

`H-823` remains route-only:

- Local metadata gives `H88-1196`.
- No source image was located in this pass.
- Follow-up control-source routing checked public CISI IA OCR, local text routes, and web search routes; `H88-1196` remains exact-route-dark.

### `642`

`H-1845` has a public source route:

- Harappa.com, "Tablet with script", H2000-4484 / 2227-15 / Figure 42.05: `https://www.harappa.com/indus3/206.html`
- Local metadata: ETrench 54, Period 3B/C, faience rectangular two-sided tablet/sealing.
- Direct shell download was blocked by Cloudflare, so no local image is stored yet.
- Public CISI IA OCR did not produce a source route in the checked layer.

`H-237` is demoted from independent control status:

- No excavation-idno in the local metadata.
- It is a fish-shaped TAB:B object with `L/R` direction and companion `+700-033+`.
- The current local export marks its SP text as `ref:424.2`, the same reference pressure attached to the `642` Harappa route.
- Until a source image or independent excavation route is found, it counts as clone-pressure on `H-1845`, not as an independent `642` source witness.

## Normalized Witness Weights

Main data artifact:

```text
data/open_prototype/reports/campaign_032_002_861_603_source_normalized_slot_family.csv
```

Current weighted state:

| X value | raw rows | source-visible / public-route objects | low-weight route-only witnesses | current source-object weight |
|---|---:|---:|---:|---:|
| `603` | 3 | 2 (`H-1138`, `H-1846`) | 1 (`H-1137`) | 2.25 |
| `636` | 2 | 1 (`H-360`) | 1 (`H-823`) | 1.25 |
| `642` | 2 | 1 (`H-1845`) | 1 near-zero clone-pressure row (`H-237`) | 0.80 |

The exact numerical weights are only working weights. The decision-relevant point is categorical: `603` is no longer supported only by one invisible repeated metadata row. It now has two distinct source-visible objects from different source routes. That is not the same as proving formula-family independence.

## Linguistic Decision

The metadata-duplicate attack is weakened. The copied-template/formula-family attack is not dead.

What changed:

- `H-1138` and `H-1846` are distinct source-visible objects for `X=603`.
- They are not just one duplicated catalog row: `H-1138` routes to Vats Plate XCIV no. 346, while `H-1846` routes to H95-2672 / Kenoyer and Meadow 1997.
- They may still belong to one formula/copy family; that remains an active attack, not a solved issue.
- Both keep the same local slot formula and companion pattern `+700-034+`.
- `H-1137` should not be counted as a full independent witness yet because its route is "similar to no. 346" rather than a located image.

What still blocks a value:

- The local sign sequence `+740-603-240-060-692+` has not yet been re-tokenized directly from the source image for `H-1138` or `H-1846`.
- `H-1845` source visibility is browser-only/public-page route in this pass, not a local stored crop.
- `H-823` remains route-dark after CISI IA/web checks, and `H-237` is too weak to carry independent control weight because it has no excavation route and carries `ref:424.2` clone-pressure.
- The slot may still be a formulaic tablet template with substitutable X-signs, rather than a lexical slot.

## Current Status

`603` survives the source-normalized attack better than it did before this campaign.

It is now:

```text
603_survives_metadata_duplicate_attack_as_two_source_visible_objects
```

It is not:

```text
603_has_value
603_is_phonetic
603_is_translated
```

## Next Linguistic Test

Treat `740-X-240-060-692` as a productive slot candidate and test the X-signs by external ecology:

1. Treat `H-237` as non-independent unless a source route is found.
2. Compare all non-slot occurrences of `603`, `636`, and `642`.
3. Ask whether `603` alone bridges into post-`002-861` tail behavior.
4. Ask whether `636` and source-bearing `642` stay confined to Harappa tablet formula families.
5. If yes, `603` becomes a stronger lexical/classifier-handle candidate.
6. If no, the slot is probably a local tablet-template alternation and should not be used as translation evidence.

Accepted values/translations remain 0.
