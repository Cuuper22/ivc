# Parpola 41 / Mayig Namespace Probe

Date: 2026-05-26

## Question

This note records a short check with a useful negative answer. It exists because several sign catalogs number their signs, the numbers look interchangeable, and they are not.

Terms first. "Mayig" is one independent sign catalog; its primary ids are `P###` "features," and each feature record also lists the equivalent codes in other catalogs — Parpola `V###`, Wells `W###`, Mahadevan `M###`. "Namespace" means one such numbering scheme. Local Lipi codes are bare numbers like `110`, `112`. Parpola 2019 is a published paper that cites signs by its own article number, as "sign no. 41" — yet another namespace. A "probe" is an exploratory pass, not accepted evidence. H-numbers are Harappa artifacts.

Does the Mayig feature namespace tell us what "Parpola sign no. 41" is?

## Result

No. It proves the opposite: the numeric labels are not portable.

Downloaded the pinned Mayig repo archive for commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`:

```text
tmp/mayig_feature_namespace_probe/mayig_commit.zip
SHA256 4d0bee925b20e1c3e5539517bf30b3adbf397e24fdc130b349b990752367e42c
features parsed: 397
```

## Target Features

| Mayig feature | Parpola field | Wells field | Mahadevan field | Description |
| --- | --- | --- | --- | --- |
| `P041` | `V141` | `W112` | `M034` | Person with U with vertical stroke inserted, stroke has a small dot at the bottom |
| `P301` | `V041`; `V479` | `W526`; `W527` | `M254` | Small box with horizontal hatching, vertical lines coming from top left and bottom right corners |
| `P110` | `V094`; `V739` | `W388` | `M327` | Upside-down heart symbol with hatching and bottom stroke |
| `P112` | `V093`; `V293` | `W384`; `W385` | `M326` | Upside-down heart symbol, possible bottom stroke |

This means:

```text
Mayig P041 != Mayig's Parpola V041
Mayig P110 != local 110
Mayig P112 != current local 112 pressure
local 041 != Mayig P041
```

## Crosswalk Pressure

A "crosswalk" is a mapping between two catalogs' sign codes; "pressure" is weak evidence that nudges toward one mapping without settling it. The local overlap machinery — which compares catalogs position by position on inscriptions they share — agrees with the danger:

| Candidate | Status | Evidence |
| --- | --- | --- |
| local `112` <-> Mayig `P041` | `uncertain`, `sparse_singleton_or_doubleton`, confidence `very_low` | one terminal aligned position in M-33 |
| local `388` <-> Mayig `P110` | `uncertain`, `low_consistency_positional_candidate`, confidence `very_low` | three aligned positions |

There is no current clean overlap candidate confirming local `110` through Mayig `P041`, `P110`, `P112`, or `V041`.

## Effect On H-2148

Parpola 2019 line 104 describes sign no. 41 as "a [kneeling] man holding a pot" in the H-940/H-2147/H-2148 reverse cluster.

That article-specific clue remains alive — still a live line of inquiry, not accepted:

```text
H-2148 reverse sign no. 41
-> local short row 481.2 +110+
-> Kenoyer 2005 one-sign panel by count
```

But the sign-list bridge is now convention-gated. Mayig `P041` cannot confirm it. Mayig `V041` cannot confirm it either until we prove Parpola 2019 uses the same `V###` convention, because Mayig's `V041` is attached to `P301`, a small hatched box, not the article's described kneeling-man/pot form.

## Decision

Accepted:

- Mayig feature IDs, Mayig's `parpola_graphemes`, Wells IDs, Mahadevan IDs, and local Lipi numeric IDs are separate namespaces.
- Mayig `P041` maps to `V141/W112/M034`.
- Mayig's `V041` maps to `P301`, not `P041`.
- Current overlap only gives very-low local `112` <-> Mayig `P041` pressure.
- H-2148 stays `strong_same_role_inference`: the sides line up by the role they play, which is not the same as the signs being identified.

Not accepted:

- `local 110 = Parpola sign no. 41`.
- `Mayig P041 = Parpola sign no. 41`.
- `Mayig V041 = Parpola 2019 sign no. 41`.
- `Mayig P041 = local 112`.
- Any value, language identity, or translation.

## Next Gate

Find the actual sign-list convention behind Parpola 2019's "sign no. 41" phrase. Until then, do not equate it with Mayig `P041`, Mayig `V041`, Mahadevan `M034`, Wells `W112`, or local `110`.
