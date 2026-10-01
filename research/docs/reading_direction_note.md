# Reading-direction note (2026-10-01)

Lipi stores inscriptions in the reverse of the conventional (Mahadevan) reading order. Every Lipi-based "terminal", "closure" or "line end" result in this repo therefore describes the reading-initial end.

## Evidence

The jar sign is Lipi 740 = Mahadevan 342. Rows of two or more signs, counted by position of the jar:

| Catalogue | Rows used | Sign at first position | Sign at last position |
| --- | --- | ---: | ---: |
| Lipi `metadata_filtered.csv` (`text`) | no `[`, `/` or `000`: 1,337 occurrences | 937 | 4 |
| Mahadevan `concordance_rows.csv` (S1..S14, `strict`=1) | 1,051 occurrences | 0 | 739 |

Counts shift with the row filter (all Lipi rows: 1,272 first / 33 last; all Mahadevan rows: 1 first / 971 last). The direction does not. Under the standard reading convention the jar is text-final, so Lipi stored order runs against it.

## Consequence

Lipi stored-final = reading-initial under the conventional reading. The accepted observation, `002-861` followed by `533-717` on M-376 and M-391, sits at the reading-initial end. Read in conventional order, those seals begin `717-533-861-002`.

## Claims affected

- Accepted claim (M-376 / M-391): "terminal" means stored-final.
- The `002-Y` closure branch and its `817/820` versus `390/368` poles.
- The `095`, `705` and `590-032` branch descriptions.
- The bare-closure counts for `002-861`, including the censored M-19 / M-175 controls.
- The FRAME700 `034` first/last counts.
- Any statement that equates Lipi `R/L` or `L/R` with physical direction.

The stored-versus-reversed asymmetry itself is unchanged. It is already published (Yadav et al. 2010).

## Caveat kept

The July 2026-07-12 checkpoint stands: stored order is a transcription property, and physical writing direction per object is not established (Meadow and Kenoyer's H-1682 is left-to-right on the seal and recorded `R/L`). This note concerns only the reversal between two catalogues.
