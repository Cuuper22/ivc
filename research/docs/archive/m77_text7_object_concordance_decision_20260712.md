# M-77 / Parpola Text No. 7 Object Concordance Decision

Date: 2026-07-12

## What this is and why it exists

A concordance decision settles which physical object a published discussion is actually about. Papers cite seals by catalogue identifier. If the identifier is wrong, every downstream use of that paper's claim points at the wrong stone.

This note works through one such case. Parpola 2019 discusses a short inscription it calls text no. 7, and names seals that are supposed to carry a recurring three-sign piece of it. Two printed identifiers are checked here against three independent layers — the CISI published plates, the Lipi numeric catalogue, and the Mayig `P`-code catalogue — and neither survives. A third object does.

Two habits of shorthand cause trouble in this area and are avoided deliberately below. The first is direction: an Indus inscription can be written left-to-right on the object and read right-to-left, so any sign string has to say which order it is in. The second is namespace collapse: Parpola, Wells, Mahadevan, Lipi, and Mayig all number signs, and the same number means different signs in different systems. `BASE_T` below is a local label for the three-sign piece under discussion, so that it can be talked about without borrowing anyone's numbering.

## Decision

The three-sign graphic string survives. The printed seal identifiers do not.

Parpola 2019 Figure 1 shows text no. 7, assigned to `M-2109` and `M-2111`, as four standardized signs. The article says the last sign in reading order is sign no. `107`, and that the remaining three-sign sequence ends with sign no. `189`, following plain fish sign no. `60`.

To prevent another direction/namespace collapse, define the graphic strings explicitly:

```text
Figure 1 left-to-right:        107 - 189 - 60 - U
Figure 1 reading right-to-left: U - 60 - 189 - 107

BASE_T left-to-right:           189 - 60 - U
BASE_T reading right-to-left:   U - 60 - 189
```

`U` is the first sign in reading order. It is visible in Figure 1, but the checked 2019 prose does not number it. This decision does not guess its Parpola number.

The article gives two different answers itself. The 2019 recurrence paragraph prints `M-77` as the seal carrying `BASE_T`; the conclusion prints `M-35`. Both fail direct source normalization — that is, checking the printed identifier against what the plates and both catalogues record for that object:

| printed object | CISI source | Lipi | Mayig | decision |
| --- | --- | --- | --- | --- |
| `M-35` | complete seven-sign seal | `+740-390-590-233-231-002-107+` | `P324 P086 P276 P058 P056 P122 P007` | reject as `BASE_T` |
| `M-77` | complete five-sign seal | `+832-390-803-002-861+` | `P366 P086 P364 P122 P385` | reject as `BASE_T` |
| `M-37` | complete three-sign seal matching the Figure 1 base graphically | `+520-220-415+` | `P217 P050 P092` | high-confidence intended-reference candidate |

`M-37` is not an author-confirmed correction, and this note does not pretend otherwise. It is the source-supported correction candidate, for two reasons: all three current layers agree that it is an exact three-position seal, and the CISI impression matches the three standardized Figure 1 positions once the final `107` is removed.

## What identity survives

The exact local string `+520-220-415+` survives across:

```text
M-37
H-938
H-939
H-1284
H-940
H-2148
H-2240
```

Within that set, `M-37` is the source-visible seal anchor: it is the one whose plate has been inspected. `H-2240` is still source-dark, meaning no usable published image has been checked, so its identity is local only. H-940 and H-2148 have exact local companion strings but unresolved physical-side labels, so it is not settled which face of the object each row describes.

The non-exact controls — near misses kept as contrast cases — remain informative:

```text
H-2145  +074-220-415+   one stored-position variant
H-2147  ]220-415+       fragmentary suffix only
H-942   +520-220-016+   one stored-position variant, source-visible full signband
H-2241  ]415-240+       fragmentary pressure only
```

The full text-no.-7 identities `M-2109` and `M-2111` also survive at the author/object level. Their raw rods are not in the checked local source set. Lipi gives both as poor/incomplete `+400-000-220-415+`, so their local tokens are not aligned to the four standardized Figure 1 signs.

## Object-bound graphic bridge

A bridge lines up one system's labels against another's. This one is object-bound: it holds for the inspected object and string, and claims nothing beyond them. The direct M-37 comparison supports these three positional correspondences:

| M-37 Lipi | M-37 Mayig | Parpola Figure 1 `BASE_T` position |
| --- | --- | --- |
| `520` | `P217` | sign `189`, spear/arrow graphic |
| `220` | `P050` | sign `60`, plain-fish graphic |
| `415` | `P092` | `U`, unnumbered in the checked prose |

That alignment corrects an orientation error in the recurrence question. Lining the positions up shows that the local `415/016` split in H-942 concerns the `U` position, not Parpola sign `189`. It therefore cannot be used to argue either `415=189` or `016=189`.

The bridge stays object-bound for four reasons:

- raw M-2109/M-2111 rod transcriptions are unavailable here;
- H-942 supplies a real `415/016` local variant/stressor;
- the Mayig `V###` namespace is not the same thing as Parpola 2019's Figure 5.1 sign numbers;
- both printed seal references fail direct source normalization; the checked evidence does not establish which identifier the author intended.

## Accepted

These statements are accepted as source facts:

```text
Parpola text no. 7 is M-2109/M-2111 in the 2019 standardized figure.
Text no. 7 consists of BASE_T plus final sign 107 in Parpola's account.
M-35 is not BASE_T: source, Lipi, and Mayig all show seven signs.
M-77 is not BASE_T: source, Lipi, and Mayig all show five signs.
M-37 is the source-visible three-sign seal matching BASE_T and is the high-confidence intended-reference candidate.
The exact local +520-220-415+ string survives on seven named objects.
M-37 supports an object-bound positional graphic bridge 520/P217 -> 189, 220/P050 -> 60, 415/P092 -> U.
```

## Not accepted

These do not follow from the checked evidence and are not accepted:

```text
An author-confirmed M-35 or M-77 erratum.
A global Lipi-to-Parpola numeric crosswalk.
A global Mayig-to-Parpola-2019 numeric crosswalk.
local 415 = local 016.
local 110 = Parpola sign 41.
Any M-77 token mapping.
Any sign value, phonetic reading, language identity, or translation.
```

## Durable artifacts

```text
research/data/sign_crosswalk/m77_text7_object_concordance_20260712.csv
research/data/sign_crosswalk/m77_text7_concordance_summary_20260712.json
research/data/sign_crosswalk/source_panels/m77_text7_concordance/manifest.csv
research/data/sign_crosswalk/source_panels/m77_text7_concordance/parpola2019_fig1_text7_m2109_m2111.png
research/data/sign_crosswalk/source_panels/m77_text7_concordance/cisi1_pdf55_print19_m35_m37.jpg
research/data/sign_crosswalk/source_panels/m77_text7_concordance/cisi1_pdf69_print33_m75_m79.jpg
```

This gate is complete with the source material available here. Confirming that Parpola intended `M-37` would take an erratum or an author statement. That confirmation is not needed for what this note actually does: the two printed identifiers stay rejected on their own evidence, and the correction stays explicitly inferential.
