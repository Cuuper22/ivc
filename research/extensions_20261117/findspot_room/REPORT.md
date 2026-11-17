# findspot_room: do seals found in the same room share writing?

Question. If seal texts name people or households, seals dug up together should share uncommon signs. If texts are generic formulas, they should not. Do seals from the same room at Mohenjo-daro share signs more often than seals from the same part of town and the same depth?

Data. Lipi `metadata_filtered.csv` (5,679 rows), seals only, faces of one object merged, at least two legible signs. Mohenjo-daro: 979 seals with a house, 849 with a room, 845 with a room and a depth in feet. Columns used: `area-section` (excavation area), `block-house` (house), `room-grid` (room), `depth`, `symbol` (the animal), `text`. No earlier test in this repository uses the house or room columns. Sign order is the stored Lipi order (reverse of the conventional reading order): "ends" = first and last stored sign, "middle" = everything between.

Method. For every pair of seals from the same room (or house), record whether they share a sign that occurs on at most N catalogue rows ("rarity cut-off"), separately for middle signs and end signs; also sign-set overlap with uncommon signs weighted up, and whether the animal matches. Chance level: shuffle the findspot labels among seals of the same excavation area (part A) or the same excavation area and the same 3-ft depth band (parts B and C), 2,000-3,000 shuffles, fixed seeds. P = share of shuffles reaching the observed value, one-sided. Part C repeats the same-room count over 4 rarity cut-offs x 4 depth windows x middle/ends (32 cells). Part D runs the same count at the other sites that have a room or grid field.

Result.
| Test | Observed | Chance | P |
|---|---|---|---|
| Same room, depth gap <= 3 ft (193 pairs): share a middle sign with rarity <= 80 | 5 pairs | 0.73 | 0.0010 |
| Same, rarity <= 40 | 3 pairs | 0.23 | 0.0027 |
| Same, rarity <= 80, by depth gap: any / <= 5 ft / <= 3 ft / <= 2 ft | 5 / 5 / 5 / 4 pairs | 1.38 / 1.05 / 0.73 / 0.55 (ratio 3.6 / 4.8 / 6.9 / 7.2) | 0.013 / 0.006 / 0.001 / 0.004 |
| Middle signs, all 16 grid cells | 10 cells below P 0.05, all 16 above chance | | |
| End signs, all 16 grid cells | 0-3 pairs per cell, no cell below P 0.05 | 0.04-2.5 | 0.08-1.0 |
| Same room, depth gap <= 3 ft: middle-sign overlap (weighted) | 0.0326 | 0.0226 | 0.023 |
| Same room, depth gap <= 3 ft: end-sign overlap (weighted) | 0.0392 | 0.0357 | 0.31 |
| Same house, different room, depth gap <= 3 ft (1,778 pairs): middle-sign overlap | 0.0228 | 0.0224 | 0.40 |
| Same house, any room, depth gap <= 3 ft (1,971 pairs): same animal | 12.5% | 11.0% | 0.027 |
| Same house, no depth condition (3,821 pairs): same animal / all-sign overlap | 12.8% / 0.0336 | 10.8% / 0.0329 | 0.001 / 0.27 |
| Other sites, same room or grid square: Harappa (79 pairs), Kalibangan (15), Chanhu-daro (3), rarity <= 80, middle | 0 / 0 / 1 pairs | 0.35 / 0.00 / 0.01 | 1.0 / 1.0 / 0.009 |

The five pairs behind the headline cell. Area, house and room are the catalogue's own codes; texts are in stored sign order; the number after each shared sign is how many catalogue rows it occurs on; the excavation number is the raw catalogue string.

| Area / house / room | Seal 1 | Seal 2 | Shared middle sign |
|---|---|---|---|
| `DKG. (S)` / `9XI` / `70` | M-153, `DK12877361`, -11.5 ft, `269-130-190` | M-1112, `DK12878366`, -11.4 ft, `740-585-220-002-130-035-171` | 130 (16 rows) |
| `DKG. (S)` / `7I` / `15` | M-1661, `DK6791436`, -13.1 ft, `520-070-219-002-861-032-520-919-140` | M-1045, `DK6792447`, -13.3 ft, `740-100-415-070-032-002-820-000` | 070 (38 rows) |
| `DKG. (N)` / `16II` / `11` | M-723, `DK1164954`, -4.6 ft, `740-460-510-235-220-032-002-861` | M-937, `DK1169066`, -5.0 ft, `740-460-503-031-002-900-615` | 460 (39 rows) |
| `DKG. (S)` / `10I` / `10` | M-92, `DK6422407`, -12.5 ft, `740-798-460-350-002-814-084` | M-195, `DK6596415`, -12.7 ft, `298-350-590-032-900-853` | 350 (48 rows) |
| `DKG. (S)` / `8A-` / `44` | M-1923, `DK1082945`, -4.5 ft, `740-760-440-853-016-043` | M-53, `DK10916128`, -6.6 ft, `090-740-220-016-002-297-190-920-140` | 016 (49 rows) |

The excavation strings look like a field number followed by a three-digit publication number with the separator lost (`DK12877361` = DK 12877 + 361). Read that way, the first two pairs carry field numbers that differ by one (12877 / 12878 and 6791 / 6792): they were registered one after the other.

What it shows. Seals found in the same room at the same depth share an uncommon sign in the middle of their text about 7 times as often as chance, and the ratio climbs as the two seals get closer in depth. The first and last signs show no excess; house-mates in other rooms show none. The middle of a seal text belongs to the people of that room. The opening and closing are citywide formula.

What it opens. A name slot. The middle signs shared by room-mates are the first candidates for name or family elements, which is where sounds start. Next: collect every sign shared inside a room, check whether they keep one position in the text, and look for the same signs on the round seals found abroad.

The strongest rival. One carver cutting several seals for one household would repeat his own sign shapes. Photographs of the five pairs separate a shared sign from a shared hand. Either way the room decides what is in the middle of the text.

Earlier work. Mukhopadhyay 2023 (s41599-023-02320-7) noted by inspection that seals in one house share the animal and differ in text. The room-level count, the depth matching and the middle/ends contrast are new here.

Reproduce. `python3 research/extensions_20261117/findspot_room/findspot_room.py` from the repo root (numpy; seeds 7, 11, 3, 5 for parts A-D; several minutes). Output: `findspot_room_results.json`.
