# Gulf Type Indus External Queue

Date: 2026-05-30

This is a Vector 1 acquisition surface, not a claim. It turns Laursen's external Gulf Type seals with Indus text into a row-level queue for the diffuse Meluhha bilingual search.

The queue exists because the current failures are informative: the Ur/Gadd audit shows that site overlap and Indus-only external seals do not produce phonetic anchors, while BM `120573/U.7683` shows that cuneiform-only Indus-style objects also do not help unless they share an object with an Indus sequence. The next target is therefore not "more Meluhha vibes"; it is exact object identity plus readable-writing adjacency.

## Artifact

- `data/meluhha/gulf_type_indus_external_queue.csv`

The CSV records Laursen Table 1 entries `6` through `27`, the external Gulf Type rows with `INDUS` text in the table extract readable through the PDF interface. It includes source provenance lines, current workspace linkage, current anchor status, and the next gate for each row.

## Source Surface

Primary source used:

- Laursen 2010 PDF, "The westward transmission of Indus Valley sealing technology": `https://www.harappa.com/sites/default/files/pdf/The_westward_transmission_of_Indus_Valle.pdf`

Source-access note:

- Browser PDF text access succeeded.
- Direct PowerShell download from Harappa failed behind a Cloudflare block, so no local PDF copy is claimed for this source in the workspace.

Relevant source facts from Laursen:

- The paper says circular seals with Indus text appeared in Mesopotamia through Gadd's Ur publication and related discoveries.
- Table 1 lists external `Gulf INDUS` rows from Bahrain, Failaka, Susa, Luristan, Ur, Girsu, the Near East, and Mesopotamia.
- The Ur rows include Gadd nos. `15` and `16`; the paper also gives their grave contexts as PG 401 and the shaft fill leading to PG 1847.
- The Failaka rows are Kjaerum 1983 catalogue nos. `319` and `279`.

## Priority Rows

| Queue row | Current value | Why it matters |
| --- | --- | --- |
| Laursen `20`, Gadd no. `15`, Ur | Maps to local `3899.1/U8685` | Verified object identity, but Indus-only so far. Best for archaeological-context tightening, not phonetics yet. |
| Laursen `21`, Gadd no. `16`, Ur | Maps to local `3898.1/U17649` | Verified object identity and strong local row; still no cuneiform bridge. |
| Laursen `12`, Kjaerum cat. `319`, Failaka | Candidate lane for local `147.1/148.1` | Needs primary catalogue page to resolve which Failaka row it is. |
| Laursen `13`, Kjaerum cat. `279`, Failaka | Candidate lane for local `147.1/148.1` | Same as above, with stronger need for plate-level row mapping. |
| Laursen `14`, Amiet no. `1643`, Susa | Candidate lane for local `3882.1 / SB 2425` | Strong object-route lead, but no readable cuneiform on the object in current workspace. |
| Laursen `22`, Sarzec and Heuzey plate `30.3a-b`, Girsu | Candidate lane for Girsu/Tello rows | Needs exact accession/object mapping before any bridge test. |

## Forger Rule

Any future candidate from this queue must clear the same gate:

1. The exact object must carry or be directly paired with an Indus sign sequence.
2. The same exact object, or a documented same-context label/seal pairing, must carry readable cuneiform or another readable-script name/title/formula.
3. The match must not be explainable by site, approximate date, object class, icon, row length, or duplicate-pattern compatibility alone.
4. A synthetic same-site/same-length forger must not reproduce the bridge at comparable rates.

## Decision

No claim increments. This queue is useful because it prevents the next Vector 1 pass from rediscovering the same failed shortcuts. It says exactly where to spend source-acquisition effort: Kjaerum cat. `279/319`, Mitchell 1986 figures `106-117`, Amiet `1643`, and the Sarzec/Heuzey Girsu plate.
