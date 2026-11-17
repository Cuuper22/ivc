# Extension studies, 2026-11-17

One study so far. Same layout as `../extensions_20261001/`: one script (fixed seeds, deterministic), its JSON output and a one-page REPORT.md.
Run from the repo root: `python3 research/extensions_20261117/<study>/<script>.py` (numpy).

| Study | Question | Headline result | Verdict | Folder |
|---|---|---|---|---|
| findspot_room | Do seals found in the same room at Mohenjo-daro share writing more than chance? | Same room, within 3 ft of depth: 5 pairs share an uncommon sign in the middle of the text, 0.73 expected (P 0.001). The ratio rises as the depth gap shrinks. First and last signs: no excess. Same house but a different room: no excess for text; the animal is shared a little more often than chance. | A small effect in the expected direction, resting on 5 pairs at one site; not in the claim ledger | `findspot_room/` |

Why it is here. Every earlier test used the catalogue's findspot columns (house, room, depth) only as strata to control for. This study treats the findspot as the thing to explain. It is the first test in the repository whose evidence comes from outside the sign sequence and is not zero.

Nothing in this folder changes `../docs/claim_ledger.md` or the root README.
