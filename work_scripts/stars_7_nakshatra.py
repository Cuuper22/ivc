#!/usr/bin/env python3
"""Rescue idea tried after step 1 went against: the name-slot numbers before a fish follow the star counts of the
lunar mansions (nakshatras), where two-star mansions are the commonest numbered kind.
PREDICTION: on values 2 and up, the name-slot mix is closer to the mansion star-count mix than the ordinary
goods-count mix is. Mansion star counts: Wikipedia 'Nakshatra' table, 'Associated stars' column (fetched 2026-11-17),
counted by hand: 1 star x8, 2 x9 (Abhijit included), 3 x5, 4 x2, 5 x2, 6 x1 (Pleiades), 9 x1.
"""
from stars_common import *
NAK = {2: 9, 3: 5, 4: 2, 5: 2, 6: 1, 9: 1}
U = distinct(all_units('L')); U = U[U.pre.isin(['', '002', '031'])]
N = U[(U.slot == 'name') & U.nxt.isin(FISHALL)]; O = U[(~U.nxt.isin(FISHALL)) & U.slot.isin(['count_pure', 'count_named'])]
vals = range(2, 10)
def mix(c): c = {k: v for k, v in c.items() if k >= 2}; t = sum(c.values()); return np.array([c.get(v, 0) / t for v in vals])
nak = mix(NAK); nm = mix(collections.Counter(N.value)); gd = mix(collections.Counter(O.value))
print('name-slot mix', dict(zip(vals, nm.round(2)))); print('goods mix', dict(zip(vals, gd.round(2)))); print('mansions', dict(zip(vals, nak.round(2))))
print(f'distance to mansion counts: name slot {0.5*np.abs(nm-nak).sum():.2f}, goods counts {0.5*np.abs(gd-nak).sum():.2f}')
