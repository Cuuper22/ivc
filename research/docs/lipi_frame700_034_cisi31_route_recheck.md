# Lipi FRAME700 034 CISI 3.1 Route Recheck

Date: 2026-05-25

## Question

This note records a recheck of the source route — the path by which the project expects to obtain trustworthy catalog evidence for a set of objects. The panel graph for the sign codes `032/033/034` — the map of which catalog rows sit on which physical sides of which objects — is blocked on unresolved catalog labels, so the next step depends on which published source can unblock it. The question: what does the fresh public web layer actually prove about that next source route?

## Stored Data

- CSV: `data/open_prototype/reports/lipi_frame700_034_cisi31_route_recheck.csv`

## Result

```text
sources_checked: 8
accessible_source_pages: 7
direct_fetch_blocked_pages: 1
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
```

## Source Route

The recheck confirms that CISI 3.1 — the Corpus of Indus Seals and Inscriptions, volume 3.1, the standard photographic catalog of Indus objects — is not decorative bibliography. It is the right next target for the current blockers because it is the Mohenjo-daro/Harappa supplement and its end matter is reported to include object-level data such as excavation number, owner/museum, and photograph source.

That matters directly for the live cases:

| Object or family | Why CISI 3.1/end matter matters |
| --- | --- |
| `H-893` | The accessible IA vol. 1/2 layer shows `H-893 (1) A/B`, but does not explain what `(1)` means. |
| `H-925` plus `H-326/H-924/H-925` | These objects may be a copy family — objects carrying the same inscription, possibly copies of one another — so a single-object lookup is too weak; the family needs group-level source notes. |
| `H-983` | The source-side `C` hazard needs object-note policy before local two-row metadata can be trusted. |
| `H-353` plus repeated `+400-740-176+ / +700-033+` family | The repeated family and source `C` side require a family/source-policy check, not an isolated visual guess. |
| `H-2211` | Still needs source-normalized side labels before it can serve as a `032` control — a comparison object used to test whether a contrast holds. |

## Prior-Work Pressure

Parpola's overview is useful here, but not because it gives us a reading. It pressures the method: a forgotten script needs reliable collection of all material, all sides, photographs, and object context before linguistic claims are allowed to harden. The same overview also makes archaeological context a confound, especially for Mohenjo-daro where deposits can be mixed.

The Bryn Mawr review adds the adversarial version: CISI is the backbone, but the script remains undeciphered and many seals lack strong contextualization. So the fair move is not "Parpola says X, accept X." The fair move is "use CISI to stabilize object identity, side identity, and source photographs, then attack any proposed reading."

## Research Consequence

This recheck narrows the next real acquisition work:

1. Get CISI 3.1/end-matter data for `H-893`, `H-925`, `H-983`, `H-353`, and `H-2211`.
2. For `H-925` and `H-353`, request family-level notes rather than isolated object notes.
3. Keep public web leads as route evidence only.

No decipherment claim changes from this pass.
