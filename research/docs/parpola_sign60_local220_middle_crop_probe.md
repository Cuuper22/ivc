# Parpola Sign 60 / Local 220 Middle-Crop Probe

Date: 2026-05-26

## Question

When local `220` is isolated from source-visible `+520-220-X` rows, does the middle component visually behave like the Parpola plain-fish / fish-leaf family?

This is a graphic-family probe. It does not accept a sign-number crosswalk or a reading.

## Packet

Neutral packet:

```text
tmp/parpola_sign60_local220_middle_probe/neutral_packet/neutral_contact_sheet.png
sha256 A6B47CF748C5978DA6C41A008AD7F4855EC8D6CC0B2A9E073CA3F3F835F1226A
width 760
height 436
```

Unblinded crop roles:

| Neutral ID | Role |
| --- | --- |
| `N001` | Parpola 1994 Fig. 5.1 sign no. `60`, variant a |
| `N002` | Parpola 1994 Fig. 5.1 sign no. `60`, variant b |
| `N003` | Parpola 1994 Fig. 5.1 sign no. `70`, variant a, fish-family control |
| `N004` | Parpola 1994 Fig. 5.1 sign no. `70`, variant b, fish-family control |
| `N005` | M-37 source middle component from local `+520-220-415+` |
| `N006` | H-938 A source middle component from local `+520-220-415+` |
| `N007` | H-940 A source middle component from local `+520-220-415+` |
| `N008` | H-942 A source middle component candidate from local `+520-220-016+`, side-mapping caution |

The packet was intentionally not used to infer meaning. It tests visual compatibility only.

## Blind Visual Result

The blind visual review clustered `N001-N004` as one line-drawing fish/leaf family: central oval or leaf body, side strokes/fins, and a lower fork/tail or stem split.

For the photographic candidate crops:

| Neutral ID | Result |
| --- | --- |
| `N005` | Compatible with the fish/leaf family, medium-high confidence. Central body and lower bifurcation are visible; some right-side neighbor contamination remains. |
| `N006` | Probably compatible, medium confidence. Tall central body and lower split are visible; side strokes are faint and low contrast. |
| `N007` | Compatible, medium-high confidence. Central body, side strokes, and lower bifurcation are visible; neighboring strokes crowd the crop. |
| `N008` | Ambiguous, low confidence. Blur and truncation block positive use. |

## Decision

Status:

```text
middle_crop_broad_fish_leaf_family_supported_sign60_specific_crosswalk_not_accepted
```

Accepted:

```text
N005, N006, and N007 are compatible with the broad fish/leaf graphic family represented by the Parpola line-drawing controls.
M-37, H-938 A, and H-940 A can be used as source-visible local-220 middle-component family witnesses.
H-942 A remains too weak for positive middle-component use in this packet.
```

Not accepted:

```text
local 220 = Parpola article sign no. 60
local 220 = Mayig P050 at source-image level
Parpola sign no. 60 versus sign no. 70 discrimination in local source crops
sign value
phonetic value
translation
```

## Consequence

This is real progress, but it is not the win condition. The local source crops now survive a broad fish/leaf-family test. They do not yet isolate the article's specific sign no. `60`, because the top-row controls themselves show neighboring fish-family signs that are visually close.

The next useful gate is stricter:

1. Build a line-drawing control panel separating Parpola sign no. `60` from nearby fish-family signs such as `57`, `61`, `66`, `70`, and `71`.
2. Add source-visible Mayig `P050` examples where the object identity and side are clean.
3. Re-run the local `220` middle crops against that richer control set.

Until then, the accepted statement is `local 220 is broad fish/leaf-family compatible in M-37/H-938/H-940 source crops`, not `local 220 is article sign 60`.
