# Lipi FRAME700 034 Source Note And Panel Graph

Date: 2026-05-25

## Question

Did the accessible CISI vol. 1/2 OCR contain object-specific notes that resolve the live `034` blockers, and if not, what is the source-normalized panel graph allowed to say?

This is not a translation attempt. It is a gate before translation: if the source panel graph is unstable, substitution claims are fake precision.

## Inputs

- IA bundle: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- Prior source convention probe: `docs/lipi_frame700_034_cisi_variant_convention_probe.md`
- Script: `data/open_prototype/tools/lipi_frame700_034_source_note_panel_graph.mjs`
- Source-note CSV: `data/open_prototype/reports/lipi_frame700_034_source_note_route_probe.csv`
- Panel-graph CSV: `data/open_prototype/reports/lipi_frame700_034_panel_graph_readiness.csv`
- Summary JSON: `data/open_prototype/reports/lipi_frame700_034_source_note_panel_graph_summary.json`

No page images or OCR dumps are stored as research artifacts.

## Source Note Result

The probe searched the accessible IA OCR layer for `H-771`, `H-893`, `H-925`, `H-983`, and `H-353`, plus excavation/catalog hooks where available. The result is blunt:

```text
object-specific notes found in accessible IA OCR: 0
plate-label target hits found: 5
strict substitution-ready lanes: 0
accepted translations/sign values/meanings: 0
```

The important new source fact is not just "nothing found." CISI itself points the needed kind of data elsewhere:

| Scope | OCR locator | Consequence |
| --- | --- | --- |
| CISI Pakistan vol. 2 | table of contents line `346`; introduction lines `2099-2102` | The accessible volume routes detailed archaeology, measures, material/manufacture, text/iconography notes, and references to the detailed catalogue/vol. 3 layer. |
| CISI India vol. 1 | table of contents line `307`; introduction lines `1621-1623` | The same route applies for India objects: object-specific documentation is not expected to be fully carried by plate labels. |
| CISI vol. 3.1 | Harappa.com, University of Helsinki, Tiedekirja, and the Linguistic Society book notice | Vol. 3.1 is the concrete next lookup route; the book notice says object data such as excavation number, museum/owner, and photograph source are in the end matter, pp. `413-443`. |

That means the next source route is CISI vol. 3/detailed catalogue, HARP/object archive plates, library scans, or equivalent object-level notes. The IA vol. 1/2 OCR is useful for page and plate labels, not for resolving the hardest current blockers.

External route links:

- <https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31>
- <https://researchportal.helsinki.fi/en/publications/corpus-of-indus-seals-and-inscriptions-volume-3-new-material-untr/>
- <https://tiedekirja.fi/en/corpus-of-indus-seals-and-inscriptions-3-1>
- <https://journals.linguisticsociety.org/booknotices/?p=1785>

## Target Consequences

| Object | Accessible IA OCR gave | Missing object note |
| --- | --- | --- |
| `H-771` | Plate labels for `A/A bis/A ter/A quater` plus `B`. | Which side-A photograph anchors the local companion row, and whether preservation changed. |
| `H-893` | Base `H-893 A/B` and `H-893 (1) A/B` label hits. | Whether `(1)` is a copy, separate object, catalogue sub-entry, or alternate photograph group. |
| `H-925` | Base, numbered, `bis`, and `ter` label hits. | What `H-925 (1)/(2) A/B` means before using it as a shared `033` control. |
| `H-983` | Garbled but useful target area, including `B` and `C/C bis` context. | Why a source `C` side is omitted by the local two-row packet. |
| `H-353` | Duplicate B/C OCR contexts on IA leaves `n265` and `n696`; visual page already showed A/B/C. | Whether `C` is inscriptional, iconographic, blank/edge, or intentionally excluded by corpus policy. |

## Panel Graph

The graph now separates side nodes, photo witnesses, unresolved numbered groups, and source-route absences:

| Lane | Objects | Current graph status |
| --- | --- | --- |
| independent low-copy | `H-771 / H-789 / H-1123` | Blocked. `H-789` is a clean two-panel calibration control, but `H-771` needs same-side photo selection and `H-1123` is source-request-only in this route. |
| strict local contrast | `H-893 / H-925 / H-930` | Blocked. `H-930` is a clean calibration control, but both `H-893` and `H-925` have unresolved object-number groups. |
| visual local contrast | `H-983 / H-353 / H-2211` | Blocked. `H-983` and `H-353` both have true `C`-side hazards, and `H-2211` still needs source-normalized side labels. |

The graph has two useful controls, `H-789` and `H-930`, but zero ready substitution lanes. That is progress because it prevents us from laundering dirty source mapping into a clean-looking linguistic result.

## Readiness Rule

A `032/033/034` substitution test is admissible only when every object in a lane has:

1. Confirmed physical side nodes.
2. Photo witnesses attached to those nodes rather than counted as new sides.
3. Numbered object groups resolved or excluded.
4. Local rows mapped to source panels with direction and subtype uncertainty explicitly carried.
5. No unmodeled `C` side or source-route gap.

The current graph satisfies that for no full lane.

## Next Source Requests

1. `H-893`: resolve `H-893 (1) A/B`.
2. `H-925`: resolve `H-925 (1)/(2) A/B` and separate `bis/ter` photo witnesses.
3. `H-983`: explain or include source side `C`.
4. `H-353`: explain or include source side `C`.
5. `H-1123`, `H-2211`: locate source-grade side labels so the 032 controls are not ghosts in the graph.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted FRAME700 subtype readings from this artifact: 0
```
