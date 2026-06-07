# Lipi 034 M-1206 Terminal Triad

Date: 2026-05-25

Question:

```text
Does M-1206 give a cleaner 034 constraint outside the failed M-2104 count-compound branch?
```

## Result

Yes, but only as a source-gated terminal-slot target, not as a reading.

The broad `520-220-X` pool has:

```text
rows with prefix 520-220: 52
unique terminals after 520-220: 16
terminal 415 rows: 28
terminal 034 rows: 1
```

The important new result is the tight same-stratum triad:

```text
M-1912: +520-220-003+
M-1206: +520-220-034+
M-37:   +520-220-415+
```

All three are local:

```text
Mohenjo-daro
SEAL:S
Steatite
square
class MT
3 signs
R/L
prefix 520-220
```

This moves `034` from a broad singleton into a specific terminal-slot contrast. That is actual decipherment work: a constrained sign-function target that can be killed by source images.

## Stored Outputs

- `data/open_prototype/reports/lipi_034_m1206_terminal_triad_rows.csv`
- `data/open_prototype/reports/lipi_034_m1206_terminal_triad_source_ladder.csv`
- `data/open_prototype/reports/lipi_034_m1206_terminal_triad_crosswalk_shadow.csv`
- `data/open_prototype/reports/lipi_034_m1206_terminal_triad_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m1206_terminal_triad_summary.json`

## Why This Matters

M-2104 tested whether `034` could be the three-stroke side of a `700-034` versus `700-004` count contrast. Current public source evidence failed exact three.

M-1206 asks a different question:

```text
When 520-220 is held fixed, what changes in the terminal position?
```

The immediate controlled slot is:

| Object | Local Text | Terminal | Iconography Layer | Source Status |
| --- | --- | --- | --- | --- |
| `M-1912` | `+520-220-003+` | `003` | local `Elep`; secondary drawing also labels M-1912 with elephant | secondary visual lead only |
| `M-1206` | `+520-220-034+` | `034` | local `Gaur`; Bhaskar S1 says `Bison` | public CISI-derived photo lead, identity conflict unresolved |
| `M-37` | `+520-220-415+` | `415` | local `Bull1:S`; Mayig says `unicorn III seal` | exact Mayig overlap, no source image in current packet |

The icon labels are not stable enough to read as meaning. They are exactly why this triad is useful and dangerous: it could be an icon/species-linked terminal system, a formula suffix system, or a metadata/source artifact.

## Crosswalk Shadow

Current overlap data gives a partial control layer:

```text
520 -> P217: 15/15 aligned positions
220 -> P050: 27/29 aligned positions
003 -> P123: 10/10 aligned positions
415 -> P092: 5/6 aligned positions, one P122 counterexample
034 -> no clean overlap row
```

M-37 is the cleanest public overlap comparator:

```text
M-37 local: +520-220-415+
M-37 Mayig: P217 P050 P092
```

So the live M-1206 shadow is:

```text
M-1206 local: +520-220-034+
crosswalk shadow: P217 P050 ?
```

That is a useful missing-sign target. It is not a solved mapping. The missing terminal `?` cannot be filled from the current public Mayig layer because `034` has zero clean overlap rows.

## Source Adjudication

### M-1206

Positive:

- Bhaskar 2022 Fig. 3 caption identifies the right-hand image as `M-1206`.
- The caption says the images are from CISI.
- The visible inscription band has three visible sign groups and is compatible with local `+520-220-034+`.
- S1 separately lists `M-1206` with a text-present marker, `P8`, `F0`, and `Bison`.

Downgrade:

- The same article's running text says `M-2016 (Fig. 3)`.
- Fig. 3 does not show the local companion side `+740-690-435-255-002-861+`.
- The article says seal imagery faces as impressed, while local order is `R/L`; order and terminality need source convention.
- Local `Gaur` and S1 `Bison` are not identical labels.

Verdict:

```text
M-1206 is a strong visual lead, not source-grade terminal 034 proof.
```

### M-1912

Positive:

- The local row gives `M-1912 +520-220-003+`.
- A June 2025 RMRL bulletin page has a figure labelled as representative drawings of `M-294`, `M-1912`, and related inscriptions.
- The rendered page shows `M-1912` as an elephant seal with a three-sign row in the same visual family as the local `520-220-X` triad.

Downgrade:

- This is secondary, not a CISI/HARP source-grade image.
- The drawing is used in an interpretive paper, so it must not import the author's semantic claims.
- Source-grade M-1912 plate/record is still needed before treating it as a confirmed comparator.

Verdict:

```text
M-1912 is a strong comparator lead for the 003 terminal, not a settled source comparator.
```

### M-37

Positive:

- The local row gives `M-37 +520-220-415+`.
- Current Mayig overlap has `M-37A = P217 P050 P092`, matching the local three-sign count exactly.
- This makes `415` the only terminal in the triad with a current overlap shadow.

Downgrade:

- The local icon label `Bull1:S` and Mayig description `unicorn III seal` conflict or use different icon-class conventions.
- No source-grade M-37 image has been added to this packet.
- `415 -> P092` is low-confidence globally: 5/6 aligned positions, with one `P122` counterexample.

Verdict:

```text
M-37 anchors the crosswalk shadow, but not terminal meaning.
```

## Live Hypotheses

### H1: Terminal Icon/Class Marker

The terminal after `520-220` may index an icon or administrative class:

```text
003 with elephant-like M-1912
034 with gaur/bison-like M-1206
415 with bull/unicorn-labelled M-37
```

This is tempting and therefore dangerous. It survives only if source images confirm the signs and if broader `520-220-X` rows do not destroy the icon association.

### H2: Formula Suffix, Not Icon Meaning

The terminal may be a formula suffix independent of animal icon. `415` dominates the broad `520-220-X` pool, so the triad could reflect common formula endings with rare substitutions.

### H3: Source/Metadata Artifact

The triad may be produced by catalog normalization, icon-label inconsistency, or secondary-source image selection. This stays live until all three objects are source-visible under the same standard.

## Current Accepted Claims

Accepted:

- `M-1206` is the only `520-220-034` row in the filtered local planning layer.
- `M-1912/M-1206/M-37` form a tight local terminal triad under the same site/type/material/shape/class/length stratum.
- `M-37` supplies a current crosswalk comparator: `+520-220-415+` aligns with `P217 P050 P092`.
- `034` remains crosswalk-dark in the current Mayig overlap.
- Follow-up source recheck closed two image gates: CISI India IA leaf `n54` / printed p. 19 labels `M-37 A/a`, and CISI Pakistan IA leaf `n181` / printed p. 147 directly labels multiple `M-1206` views including the long `M-1206 e(1)` side. This upgrades M-37 and M-1206 to source-visible triad members while leaving M-1912 secondary/CISI 3.1-gated.
- Blind visual orientation follow-up finds that source-visible M-37 and M-1206 share the same broad three-class face pattern, `R-L-T` / `T-L-R` across A/a mirror views: rake or vertical-stroke bundle, split leaf/fish-like sign, and triangular/standard sign. Fine-form identity is not established, and this weakens a naive semantic terminal-substitution reading.

Rejected or quarantined:

- No accepted `034` value.
- No accepted `003`/`034`/`415` semantic contrast.
- No accepted `034 = 415` collapse.
- No accepted animal/species reading.
- No accepted phonetic value.
- No accepted language identity.
- No accepted translation.

## Next Gate

Do not widen yet. The next source work is exact:

```text
Get source-grade images/records for M-1912.
Use the new CISI M-37 and M-1206 page witnesses for blind outer-sign classification.
Confirm each object identity and side/face.
Treat Bhaskar M-1206 versus M-2016 as a conflict in that article, not as a blocker against the direct CISI M-1206 route.
Resolve local Gaur versus S1 Bison and local Bull versus Mayig unicorn label conventions.
Blind-classify the terminal signs 003, 034, and 415 from images before using labels.
Collapse repeated 520-220-415 rows into source-independent units.
```

If those gates pass, this triad becomes a real functional-class test. If they fail, M-1206 stays a useful public lead and nothing more.
