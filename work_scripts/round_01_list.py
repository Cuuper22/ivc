#!/usr/bin/env python3
"""ROUND SEALS, step 1: the full list (no double counting). Written 2026-11-17. No word on any sign.
Round seal = Lipi catalogue type SEAL:C (circular) or SEAL:CY (cylinder). 41 faces; two objects (1388, 2419) have two faces,
so 39 objects. Second-catalogue-only West Asia lines (9) carry no shape field, so they are listed apart; M9801 is read as the
same stone as Lipi 3882.1 and M9846 as 3898.1 (same first signs, same animal region), so they are not counted twice.
Boss code decoding (first letter P pierced / N not pierced; second letter B boss, N none; further letters = boss form).
Photo notes (PHOTO) were written by looking at each photograph in seal_images/ (home pieces only; no foreign photograph was
obtainable, see report). Output: work_data/round/round_list.csv
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
OUTR = f'{ROOT}/work_data/round'; os.makedirs(OUTR, exist_ok=True)
sk = pd.read_csv(f'{ROOT}/work_data/frame/seal_kinds.csv', dtype=str).set_index('id')
R = d[d.type.isin(['SEAL:C', 'SEAL:CY'])].copy()
TIER = {'home': 'home', 'core': 'abroad', 'unk_round': 'unknown site', 'other': 'South India'}
PHOTO = {
 '114.1': 'photo 380x572: one line of 4 signs above the animal (unicorn with stand); signs drawn the home way; the hatched box sign (632, first in reading order) sits at the right end; no marks.',
 '122.1': 'photo: worn disc, one big sign, no animal; too worn to say how the sign is drawn.',
 '1387.1': 'photo: cylinder roll-out, beast and standing figures with a stroke group at the right; signs are small and sit between the figures (not a line).',
 '1388.1': 'photo: cylinder, no animal, 7 signs in ONE straight line along the band; signs drawn the home way.',
 '1388.2': 'second face of 1388; two signs only; same hand style.',
 '1924.1': 'photo: cylinder with a Mesopotamian-style scene (horned figures, beasts, men with bows, a tree); the signs are 3 tall strokes and a branched tree sign standing loose in the scene; no line of text.',
 '2153.1': 'no photograph found.',
 '2419.1': 'photo not in the repository.',
 '2419.2': 'photo not in the repository.',
 '2911.1': 'photo: 2 signs in one line above the bull; home drawing.',
 '2912.1': 'photo: 5 signs in a cluster above and in front of the animal, plus a hatched sign at the right edge; not one straight line.',
 '2913.1': 'photo: composite many-headed beast scene with a plant at the left; no sign can be made out (catalogue has 000 and 140).',
 '2977.1': 'photo: 8 signs run round the rim of the disc, a big X-like motif fills the centre (no animal); text is ring-shaped, not a line.',
 '3668.1': 'photo: broken fragment; 8 signs follow the curved edge in an arc (one line bent round the rim); a block of stacked strokes at the left end; no beast on the fragment.',
 '3669.1': 'photo: small fragment, zigzag mark and 1 sign; nothing else.',
}
rows = []
for r in R.itertuples():
    i = r.id
    tier = F.set_index('id').loc[i, 'tier']
    b = r.boss if isinstance(r.boss, str) else ''
    pierced = {'P': 'pierced', 'N': 'not pierced', '?': '?'}.get(b[:1], 'not recorded') if b not in ('-', '') else 'not recorded'
    bossed = ('boss' if b[1:2] == 'B' else ('no boss' if b[1:2] == 'N' else 'not recorded')) if b not in ('-', '') else 'not recorded'
    tb = sk.bin.get(i, '') if i in sk.index else ''
    rows.append(dict(id=i, obj=r.obj, tier=TIER.get(tier, tier), site=r.site, region=r.region,
        area=r[5], house=r[6], room=r[7], depth=r.depth, period=r.period, phase=r.phase, time=r.time, bin=tb if isinstance(tb, str) else '',
        horiz_mm=r[32], vert_mm=r[33], thick_mm=r[34], shape=r.shape, material=r.material, symbol=r.symbol,
        animal=ANIMAL.get(i, ''), boss_code=b, pierced=pierced, bossed=bossed, type=r.type,
        complete=r.complete, text=('-'.join(r.tok)), n_signs=len([s for s in r.tok if real(s)]), photo_note=PHOTO.get(i, 'no photograph obtained')))
L = pd.DataFrame(rows)
L.to_csv(f'{OUTR}/round_list.csv', index=False)
print(len(L), 'faces', L.obj.nunique(), 'objects'); print(L.tier.value_counts())
print(L[['id', 'tier', 'site', 'area', 'house', 'room', 'depth', 'bin', 'thick_mm', 'animal', 'boss_code', 'text']].to_string())
