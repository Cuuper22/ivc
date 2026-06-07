# BM 120573 Object-Bridge Audit

Date: 2026-05-30

This audits the strongest Priority A object-level route surfaced by the Meluhha context-lead work: British Museum `120573`, registration `1928,1009.56`, excavation number `U.7683`.

It is a real object-level cuneiform route. It is not an accepted external Indus phonetic anchor.

## Source Facts

British Museum collection record:

- URL: `https://www.britishmuseum.org/collection/object/W_1928-1009-56`
- Museum number: `120573`
- Registration: `1928,1009.56`
- Excavation/small finds number: `U.7683`
- Findspot: Diqdiqqah, Ur, surface
- Excavator: Sir Leonard Woolley, 1926/27
- Description: rectangular grey steatite stamp seal with pierced lug, bull design, and a cuneiform line above. The BM description calls it an Indus-style seal with Sumerian inscription.
- Dimensions: 27 mm x 24 mm
- BM bibliography: Gadd 1932 no. 1, pp. 5-6, pl. I:1; Mitchell 1986 no. 7, p. 280, fig. 111; Aruz and Wallenfels 2003 no. 301b.

Gadd 1932 source route:

- BM bibliography page: `https://www.britishmuseum.org/collection/term/BIB2877`
- Digital PDF route found: `https://ignca.gov.in/Asi_data/33779.pdf`
- Gadd identifies this object as no. 1 and treats the cuneiform reading as doubtful.
- Reported sign choices: first sign `SAG(K)` or `KA`; second `KU` or possibly `LU`; third probably `SHI`; possible fourth uncertain.
- Best provisional reading in ASCII: `sak-ku-shi-?`
- Gadd explicitly does not use this cuneiform line to read the Indus script.

## Local Row Mapping Test

Generated files:

- `data/meluhha/tools/audit_bm120573_object_bridge.mjs`
- `data/meluhha/bm120573_object_bridge_audit.csv`
- `data/meluhha/bm120573_object_bridge_audit_summary.json`

The local Ur external-object rows tested were:

| Local row | Shape | Local text | Mapping verdict |
| --- | --- | --- | --- |
| `3897.1` | circular | `+093-340-924-220-528+` | not mapped |
| `3898.1` | circular | `+002-004-328-001-803-415+` | not mapped |
| `3899.1` | circular | `+000-000-004-090-350+` | not mapped |
| `5225.1` | circular | `]000-001-000-090-000[` | not mapped |
| `5231.1` | unknown | `]405-090[` | not mapped |

Reasons:

- BM `120573` is rectangular; the strongest local Ur rows are circular.
- BM/Gadd expose a cuneiform line, not an Indus sign sequence.
- The local rows are Indus numeric sign-sequence rows, and no current local row gives the BM registration, BM number, or excavation number.
- Therefore `3898.1` remains a rejected same-site length/pattern temptation, not an object bridge.

## Decision

BM `120573` is important, but it is not the desired external phonetic anchor in the current evidence state.

What it earns:

- A verified object-level route for a cuneiform-inscribed Indus-style seal from the Ur orbit.
- A provisional cuneiform fragment, `sak-ku-shi-?`, whose reading is uncertain and possibly non-Sumerian/non-Akkadian.
- A concrete acquisition target: Mitchell 1986 no. 7 / fig. 111 and Parpola 1994 p. 131 should be checked for later drawings/readings.

What it does not earn:

- No Indus sign value.
- No sign meaning.
- No language-family identification.
- No external anchor.
- No translation.

Future use is bounded: BM `120573` can only become an anchor if a source explicitly records an Indus sign sequence on this object, maps it to a local external Indus row, or ties the cuneiform line to an independent Indus-sign text. Current evidence does none of those.
