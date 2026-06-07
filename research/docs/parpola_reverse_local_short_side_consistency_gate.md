# Parpola Reverse / Local Short-Side Consistency Gate

Date: 2026-05-26

## Question

Does Parpola's reverse-side clue consistently point to the local short/companion side across the checked H-938/H-939/H-1284/H-2145 and H-940/H-2147/H-2148 cluster?

## Source

Parpola 2019, local extracted text `tmp/parpola_2019_bone_rods.txt`, lines 87-104.

Parpola states that H-938, H-939, H-1284, and H-2145 have `VIIII` on the reverse, while H-940, H-2147, and H-2148 have sign no. 41 on the reverse. He also notes that both sides read left-to-right in this tablet category, with H-2145's obverse as an exception.

This is a prior-work side-role clue. It is not a local numeric sign crosswalk by itself.

## Check

The seven mentioned objects split cleanly into a longer `415` side and a shorter companion side in the local Lipi rows:

| Object | Parpola reverse clue | Local reverse-candidate row | Local reverse-candidate text | Local class | Companion row | Companion text | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-938 | `VIIII` | `1818.2` | `+034-700+` | `NV` | `1818.1` | `+520-220-415+` | short-side match |
| H-939 | `VIIII` | `1819.1` | `+700-034+` | `VN` | `1819.2` | `+520-220-415+` | short-side match |
| H-1284 | `VIIII` | `4069.2` | `+700-034+` | `VN` | `4069.1` | `+520-220-415+` | short-side match |
| H-2145 | `VIIII` | `827.1` | `+700-034+` | `VN` | `827.2` | `+074-220-415+` | short-side match |
| H-940 | sign no. 41 | `1820.2` | `+110+` | `TS` | `1820.1` | `+520-220-415+` | short-side match |
| H-2147 | sign no. 41 | `673.1` | `]110+` | `UC` | `673.2` | `]220-415+` | fragmentary short-side match |
| H-2148 | sign no. 41 | `481.2` | `+110+` | `TS` | `481.1` | `+520-220-415+` | short-side match |

## Result

Parpola's reverse-side clue is role-consistent across all seven checked objects: the reverse clue always aligns with the local shorter companion row rather than the longer `415` row.

For H-2148, this adds real pressure:

- Parpola says H-2148's reverse has sign no. 41.
- The local shorter companion row is `481.2 +110+`.
- Kenoyer 2005 Figure 14.1 shows H2001-5142 with one single-sign panel and one three-sign panel.
- The one-sign panel is count-mapped to local `481.2 +110+`.

So the current best inference is:

```text
H-2148 Parpola reverse sign no. 41 -> local short side 481.2 +110+ -> Kenoyer 2005 one-sign panel
```

But this is still an inference through row role and sign count. It is not yet an explicit same-side source bridge.

## Decision

Accepted:

- The seven-object Parpola reverse clue is locally role-consistent.
- H-2148 is now the strongest candidate bridge between Parpola sign no. 41 and local `110`.
- This upgrades the H-2148 gate from generic visual pressure to `strong_same_role_inference`.

Not accepted:

- `local 110 = Parpola sign no. 41`.
- A/B, obverse/reverse, or physical-side label mapping for H-2148.
- Any sign value, phonetic value, language identity, or translation.

## Next Gate

Acquire a source note, sign-list table, CISI/HARP panel label, or archive transcription that explicitly says H-2148/H2001-5142's reverse is the one-sign panel. If that bridge is found, H-2148 can become an admissible local `110` <-> Parpola sign no. 41 crosswalk candidate, still subject to outside controls.
