# 032-002-861 / 002-390-X Alpha Blind Boundary Read

Date: 2026-05-30

## Question

When object labels, target/control roles, and sign numbers are hidden, do blind readers recover stable local boundaries for the current `002-390-X` packet?

## Materials

- Blind packet generator: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\run_032_002_861_002390x_blind_boundary_packet.py`
- Blind sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\blind_boundary_packet_alpha\blind_boundary_packet_alpha_blind_sheet.jpg`
- Blind manifest: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_blind_manifest.csv`
- Response form: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_response_form.csv`
- Sealed key: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_sealed_key.csv`

Mechanic validation: PASS. The reader-facing packet uses alphabetic neutral IDs only and keeps object IDs, roles, sign numbers, and branch labels out of the blind layer.

## Key After Blind Read

| neutral | object | current role | branch |
|---|---|---|---|
| ALPHA | M-119 | strict target | 125 |
| BRAVO | M-71 | strict non-125 control | 095 |
| CHARLIE | Sktd-1 | downweighted candidate | 125 |
| DELTA | M-70 | strict non-125 control | 692 |
| ECHO | M-735 | strict target | 125 |

## Blind Result

Every blind reader treated the panels as partial rather than fully stable. No panel earned a clean segmentation verdict.

- ALPHA / M-119: partial. Repeated vertical-bar and fork/comb neighborhoods were noticed, but left-edge smear, central touching, and a cropped right hook-loop keep it below source-window proof.
- ECHO / M-735: partial. It shares vertical/fork/curved neighborhoods with other panels, but dense overlap and a partly off-frame sweeping curve make it unstable as a strict blind boundary witness.
- CHARLIE / Sktd-1: demoted. One reader rejected it; another marked it partial-leaning-no. It remains out of strict counts.
- DELTA / M-70: partial but among the clearer panels for internal repeated-bar boundaries.
- BRAVO / M-71: partial. The leaf/oval and sweeping curve are visually distinctive but both ends are cropped and central ticks are ambiguous.

## Research Decision

The alpha blind read downgrades the visual claim from `boxed-window-compatible branch contrast` to:

`catalog-guided boxed windows remain plausible, but blind source-window proof is not achieved`.

This does not kill the `002-390-X` branch hypothesis: the family-collapsed positional ecology still shows a live branch slot with `125`, `095`, `692`, and source-dark `705` alternatives. What it does kill is any move that treats the visible source bands alone as independently proving the immediate numeric windows.

## Consequence For 125

`125` remains live only as a positional continuation-bearing branch candidate after `002-390`, not as a source-proven visual boundary, value, sign meaning, phonetic reading, function, language identity, or translation.

The next useful work is not more polishing around `125`. It is going out and acquiring source routes for matched non-`125` alternatives, especially:

- H-1993, because it would test the `004 -> 002-390` split against Sktd-1.
- M-1825 and Dholavira 4237.1, because they are the repeated `705` branch needed to decide whether non-`125` alternatives are ordinary terminal branches.
