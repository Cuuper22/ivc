# Parpola Sign 60 / Local 220 Strict Fish-Family Gate

Date: 2026-05-26

## Question

After adding nearby Parpola fish-family controls, do local `220` source crops specifically match article sign no. `60`, or only the broader fish/leaf neighborhood?

This gate tests sign-list discrimination, not meaning.

## Packet

Neutral contact sheet:

```text
tmp/parpola_sign60_local220_strict_probe/neutral_packet/strict_contact_sheet.png
width 740
height 588
sha256 C97B93B15F5494CCE9E63B5DA59B9F1236D306470DF1C09D43913F62E31AD2C1
```

Unblinded control roles:

| Neutral ID | Role |
| --- | --- |
| `S001` | Parpola 1994 Fig. 5.1 sign no. `60`, variant a, plain target |
| `S002` | Parpola 1994 Fig. 5.1 sign no. `60`, variant b, plain target |
| `S003` | Parpola 1994 Fig. 5.1 sign no. `57`, reduced/stalk-like nearby control |
| `S004` | Parpola 1994 Fig. 5.1 sign no. `58`, hatched fish/leaf control |
| `S005` | Parpola 1994 Fig. 5.1 sign no. `59`, hatched fish/leaf control |
| `S006` | Parpola 1994 Fig. 5.1 sign no. `66`, plain-ish fish/leaf control |
| `S007` | Parpola 1994 Fig. 5.1 sign no. `70`, variant a, plain fish/leaf control |
| `S008` | Parpola 1994 Fig. 5.1 sign no. `70`, variant b, plain fish/leaf control |
| `S009` | M-37 source middle component from local `+520-220-415+` |
| `S010` | H-938 A source middle component from local `+520-220-415+` |
| `S011` | H-940 A source middle component from local `+520-220-415+` |
| `S012` | H-942 A source middle component candidate from local `+520-220-016+` |

Mayig `P050` remains metadata-only in this gate. The pinned Mayig repository contains `P050` feature metadata and corpus occurrences, but no bundled object/source images suitable as clean visual controls.

## Reviewer Results

Three visual reads were used:

| Reviewer | Result |
| --- | --- |
| `R1` | `S009-S011` give sign-specific visual support for the plain target `S001-S002`, with `S012` unusable. |
| `R2` | `S009-S011` support broad fish/leaf-family compatibility only; `S012` unusable. |
| `R3` | Adversarial tiebreak: `S009-S011` do not cross sign-specific threshold; broad neighborhood only; `S012` unusable. |

The decisive point is not whether local `220` is fish/leaf-like. That already survived. The decisive point is whether damaged source-photo crops can discriminate plain sign no. `60` from nearby plain-ish or decorated fish-family controls. Two of three reviewers say no, and the dissenting reviewer still blocks exact crosswalk identity.

## Decision

Status:

```text
strict_packet_broad_fish_leaf_family_only_sign60_specific_not_accepted
```

Accepted:

```text
M-37, H-938 A, and H-940 A source middle crops support broad fish/leaf-neighborhood compatibility for local 220.
S009/M-37 is the strongest current local-220 source crop.
S012/H-942 A is not usable for positive sign-specific adjudication.
```

Not accepted:

```text
local 220 = Parpola article sign no. 60
local 220 = Mayig P050 at source-image level
plain undecorated sign-60 identity for S009-S011
fish lexical value
phonetic value
translation
```

## Consequence

This is a downgrade relative to the tempting reading. Local `220` survives as a real fish/leaf-family candidate, but it does not yet become article sign no. `60`.

The next useful evidence must be stronger than this packet:

1. Acquire or derive clean source-visible Mayig `P050` visual examples, not just metadata.
2. Add higher-quality source crops for local `220` where the body outline and absence/presence of internal decoration are visible.
3. Keep `S009/M-37` as the best current candidate, but do not let it carry a crosswalk alone.
