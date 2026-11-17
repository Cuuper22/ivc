#!/usr/bin/env python3
"""Job 1, second round: the 9 values whose round-one prediction missed get a redesigned test (rule: a null means the
test was wrong; redesign once).  Each uses a kind of fact not printed for that sign before, including round one.
All 9 written here in one go before any was computed.  Writes work_data/sound_v5/job1b_tests.csv."""
from sound_v5_common import *
J1B = [
 ('240', 'mīmīn', 'High-star (house crest)', 'reverse face',
  'a house is the who-face of a tablet: the other face of a many-faced object with 240 carries a number or cup (the amount)', lambda: reverse_has('240', NUMCUP)),
 ('382', 'aracu', 'royal (lineage head)', 'seal size',
  'a royal lineage head: seals with 382 are bigger than seals with the same number of signs', lambda: seal_size('382', True, True)),
 ('097', 'aṭimai', 'bondsman, ration receiver', 'sign two places away',
  'count + cup + bondsman: a number stands two places before 097', lambda: two_away('097', set(VAL), (-2,))),
 ('790', 'maṇi', 'bead, gem', 'area inside the city',
  'bead workshops: Harappa objects with 790 lie in mound E (the craft mound) more than Harappa objects overall', lambda: harappa_area('790', 'E')),
 ('550', 'vāy', 'gate', 'seal size',
  'a gate office: seals with 550 are bigger than seals with the same number of signs', lambda: seal_size('550', True, True)),
 ('923', 'maruppu', 'horn; elephant tusk (DEDR 4720)', 'copper-tablet image',
  'the tusk sense: copper tablets with 923 show the elephant', lambda: ctab_image('923', {'Elep'})),
 ('877', 'nālkāṇi', 'four shares', 'seal size',
  'a four-share holder outranks a two-share holder: seals with 877 are bigger than seals with the same number of signs', lambda: seal_size('877', True, True)),
 ('104', 'taṭṭāṉ', 'goldsmith', 'area inside the city',
  'the jewellery hoards: Mohenjo-daro objects with 104 lie in the DK area more than Mohenjo-daro objects overall', lambda: moh_area('104', 'DK')),
 ('831', 'tiṉai', 'Italian millet', 'depth/era',
  'millet spreads late: Harappa objects with 831 come from Period 3C more than dated Harappa objects overall', lambda: harappa_late('831')),
]
if __name__ == '__main__':
    rows = []
    for s, w, en, kind, pred, fn in J1B:
        r = run('J1B', s, w, pred, fn); r.update(kind=kind, english=en); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT5}/job1b_tests.csv', index=False)
    print('moved to strict in round two:', int((df.outcome == 'yes').sum()), 'of', len(df))
