# P041 / Parpola 41 Crosswalk Falsification Gate

Date: 2026-05-26

## Question

Does Mayig feature id `P041` independently confirm the H-2148 local `110` / Parpola sign no. 41 branch?

## Result

No. It does the opposite of a shortcut: it exposes a sign-system namespace conflict.

The H-2148 role inference remains alive, but Mayig `P041` cannot be used as confirmation that local `110` equals Parpola sign no. 41.

## Evidence

Mayig feature `P041` was downloaded from the GitHub blob listed in `data/open_prototype/mayig/tree_manifest.csv`.

Stored source files:

| File | SHA256 |
| --- | --- |
| `tmp/p041_mayig_route/features__P041.json` | `9db51b7614620dd00b82eceaf6d1850e382ab448dd889f5d3f46c87efed77028` |
| `tmp/p041_mayig_route/corpus__m001_m099__m033.json` | `297ac2881c84ae99699393217a658682c749b2eeebc5e80d26b51daa90bc666a` |

Mayig `P041` says:

```json
{
  "id": "P041",
  "description": "Person with U with vertical stroke inserted, stroke has a small dot at the bottom",
  "parpola_graphemes": ["V141"],
  "wells_graphemes": ["W112"],
  "mahadevan_graphemes": ["M034"]
}
```

That is the trap. The label `P041` looks numerically tempting, but the feature metadata itself maps it to Parpola `V141`, Wells `W112`, and Mahadevan `M034`, not to "Parpola sign no. 41" by number.

## Current Overlap Check

The current Mayig index has only one `P041` occurrence:

| Mayig side | Mayig graphemes | Local row | Local text | Positional pressure |
| --- | --- | --- | --- | --- |
| `M-33A` | `P324 P145 P175 P111 P058 P122 P041` | `2561.1` / `M-33` | `+740-032-923-382-233-002-112+` | terminal `P041` aligns with terminal local `112` |

So the only current open overlap pressures Mayig `P041` toward local `112`, not local `110`.

`data/open_prototype/reports/crosswalk_alignment_pairs.csv` records the same pair as `provisional_position_alignment_only`.

This still does not accept `P041 = local 112`, because it is one sign-system-unmapped overlap row. It is conflict pressure, not a solved crosswalk.

## Local Namespace Check

Local numeric `041` is a separate Lipi token, not Mayig feature id `P041`.

| Local token | Rows in checked Lipi layer |
| --- | --- |
| `041` | `M-1151 +241-742-041+`; `M-2128 +041-705-002-905+` |
| `112` | `M-33 +740-032-923-382-233-002-112+`; `M-239 +740-760-921-235-002-112+` |
| `110` | H-940, H-2147, H-2148, H-2100, H-2152, Kanmer `4881.1` |

The numeric labels are not portable across systems.

## Effect On H-2148

This does not kill the H-2148 role chain:

```text
Parpola 2019 object-specific clue: H-2148 reverse has sign no. 41
-> local short side: 481.2 +110+
-> Kenoyer 2005 Figure 14.1 one-sign panel by count
```

That chain remains `strong_same_role_inference`.

This is not yet a linguistic refutation of H-2148. It is a numbering-system collision with real damage potential.

But Mayig `P041` now blocks a lazy confirmation route. The current state is:

```text
H-2148 role inference: alive
local 110 <-> Parpola sign no. 41 crosswalk: blocked / unaccepted
Mayig P041 as Parpola sign no. 41: rejected as namespace shortcut
Mayig P041 -> local 112: single-overlap pressure only
```

## Decision

Accepted:

- Mayig `P041` is adversarial evidence against equating same-looking numeric labels across sign systems.
- The current open overlap places Mayig `P041` against local `112` in M-33 only.
- H-2148 remains the strongest object-specific role candidate for local `110` / Parpola sign no. 41.

Not accepted:

- `local 110 = Parpola sign no. 41`.
- `Mayig P041 = Parpola sign no. 41`.
- `Mayig P041 = local 112`.
- `local 041 = Mayig P041`.
- Any sign value, phonetic value, language identity, or translation.

## Next Gate

Resolve sign-list namespaces from authoritative tables before using any numeric crosswalk:

```text
Parpola sign no. 41
Parpola V141
Wells W112
Mahadevan M034
local 110 / 112 / 034 / 041
```

Then return to the H-2148 same-side test: prove whether H-2148's reverse, the one-sign panel, and local `481.2 +110+` are the same physical side.
