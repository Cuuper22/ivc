# Parpola Text No. 7 Feature Namespace Bridge Gate

Date: 2026-05-26

## Question

Can Parpola text no. 7 and the H-obverse recurrence be bridged by taking the article's sign numbers `60`, `107`, and `189` as Mayig `V060/V107/V189`, Mahadevan `M060/M107/M189`, or local Lipi tokens with the same Arabic numerals?

## Decision

No.

The next bridge is not numeric label matching. It has to be object-side source transcription or a sign-list concordance that explicitly ties Parpola 1994 Fig. 5.1 sign numbers to the local Lipi rows and Mayig feature IDs.

This gate does add something useful: Parpola 2019's article sign numbers can be visually anchored in Parpola 1994 Fig. 5.1, and the Mayig feature metadata blocks the obvious false shortcut through Mayig `V###` and Mahadevan `M###` labels.

## Source Anchors

Parpola 2019 says its sign numbers come from Parpola 1994 Fig. 5.1. The local rendered sign-list pages now give direct visual anchors:

| Article sign | Source page | Local file | Observation |
| --- | --- | --- | --- |
| sign no. `60` | Parpola 1994 Fig. 5.1, rendered PDF page 89 / printed p. 71 | `tmp/parpola_1994_signlist/rendered/fig5_1-089.png` | Fish-form sign family; this matches the article's "plain fish sign no. 60" wording. |
| sign no. `107` | Parpola 1994 Fig. 5.1, rendered PDF page 90 / printed p. 72 | `tmp/parpola_1994_signlist/rendered/fig5_1-090.png` | Comb/rake-like diagonal-hatch variants; this matches the article's final-sign role in text no. 7 better than local numeric `107`. |
| sign no. `189` | Parpola 1994 Fig. 5.1, rendered PDF page 92 / printed p. 74 | `tmp/parpola_1994_signlist/rendered/fig5_1-092.png` | Spear/arrow-like sign; this matches the article's "spear-like sign no. 189" wording. |

Render locks:

```text
fig5_1-089.png 1805x2357 SHA256 8AFCF0D1D4662FC47014FDBF6CD6CED0F85E0FF07C2799169758E2AC2FF6996B
fig5_1-090.png 1804x2357 SHA256 0368015D49DD13C24AB6E7DFC889A2FE1A2FB16C7AF607827AB7B6C7D104FA4D
fig5_1-092.png 1231x1607 SHA256 3EF658B0D255988184F55ADB8883B97FDFC7661DEE12DF41248018134AF3A51C
```

## Mayig Feature Metadata Check

Mayig's README says its primary `P###` IDs use Parpola's inclusive allograph scheme while `V###` is an alternate Parpola numbering layer. That makes Mayig useful as a namespace witness, but not as an automatic bridge into Parpola 2019 article sign numbers.

The feature files show the trap:

| Shortcut being tested | Mayig feature result | Consequence |
| --- | --- | --- |
| `V060` | `P264`, tall rectangle with two horizontal hatches, Mahadevan `M238`, Wells `W603` | Not article sign no. 60 by numeric shortcut. |
| Mahadevan `M060` | `P051`, fish with four corner strokes, Parpola `V513/V321`, Wells `W226` | Not article plain fish sign no. 60 by numeric shortcut. |
| `V107` | `P191`, W-shaped wave motif, Mahadevan `M132`, Wells `W450` | Not article sign no. 107 by numeric shortcut. |
| Mahadevan `M107` | `P125`, five vertical strokes, Parpola `V005/V017/V715/V799` | Not article sign no. 107 by numeric shortcut. |
| M-35 local terminal `107` | current overlap aligns it to `P007`, person-with-flag, Parpola `V146/V374`, Mahadevan `M004`, Wells `W105/W107` | Local `107` is not Parpola 1994 sign no. 107 in the current evidence layer. |
| `V189` | `P071`, leftward bird with vertical tail, Mahadevan `M076`, Wells `W260` | Not article sign no. 189 by numeric shortcut. |
| Mahadevan `M189` | `P305`, long horizontal with verticals, Parpola `V058/V716`, Wells `W420` | Not article sign no. 189 by numeric shortcut. |
| M-77 local terminal `861` | current overlap aligns it to `P385`, diamond/leaf, Parpola `V162/V420/V421/V510`, Mahadevan `M267`, Wells `W817/W861` | M-77 terminal cannot be mapped to article sign no. 189 by number. |
| M-37 local terminal `415` | current overlap aligns it to `P092`, pitchfork, Parpola `V042/V182`, Mahadevan `M171`, Wells `W415` | Local `415` cannot be mapped to article sign no. 189 by number. |
| local `016` controls | current M-17/M-178 overlap aligns local `016` to `P126`, six short strokes, Parpola `V006/V018/V670/V723`, Mahadevan `M108/M109`, Wells `W006/W016` | H-942's local `016` remains a stress/control, not article sign no. 189. |

One live positive clue remains bounded:

```text
M-37 local +520-220-415+ aligns positionally to Mayig P217 P050 P092.
P050 is a plain fish-like sign.
Parpola article sign no. 60 is a fish-form sign in Fig. 5.1.
```

That is a visual/source-routing clue for the local `220` / article sign no. `60` bridge. It is not an accepted crosswalk yet because it still comes through one object-level overlap and a rendered sign-list comparison, not a source transcription saying the local `220` token is Parpola 1994 sign no. 60 in the H/M recurrence set.

## Accepted

```text
Parpola 2019 sign no. 60, 107, and 189 are now directly locatable in Parpola 1994 Fig. 5.1.
Mayig V107, V189, and V060-style shortcuts are not safe bridges into article sign numbers.
Mahadevan M107, M189, and M060-style shortcuts are not safe bridges into article sign numbers.
Local M-35 terminal 107, M-77 terminal 861, local 415, and local 016 cannot be equated with article signs 107 or 189 by numeric label.
Local 220 to article sign 60 is a bounded fish-form bridge candidate only.
```

## Not Accepted

```text
Parpola article sign no. 107 = Mayig V107
Parpola article sign no. 107 = Mahadevan M107
Parpola article sign no. 107 = local M-35 token 107
Parpola article sign no. 60 = Mayig V060
Parpola article sign no. 60 = Mahadevan M060
Parpola article sign no. 189 = Mayig V189
Parpola article sign no. 189 = Mahadevan M189
Parpola article sign no. 189 = local 415
Parpola article sign no. 189 = local 016
Parpola article sign no. 189 = M-77 terminal 861
Parpola article sign no. 60 = local 220
any M-77 token mapping
any sign value
any phonetic value
any translation
```

## Next Action

Stop spending time on naked numeric matching. The next useful artifact is an explicit object-level bridge table:

```text
Parpola 1994 Fig. 5.1 sign no. 60/107/189
Parpola 2019 text no. 7 and recurrence objects
M-35, M-77, H-942/H-2240/H-2241, H-940/H-2147/H-2148
local Lipi rows
Mayig P IDs and feature metadata where object overlap exists
source image side labels and source transcriptions when obtainable
```

Until that table has explicit source-side evidence, keep text no. 7 as a source-routing anchor, not a translation or local-string identity key.
