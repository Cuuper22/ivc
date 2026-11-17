#!/usr/bin/env python3
"""Job 1 of the fifth pass: turn wide into strict.  The 13 values that came true only on a fact glimpsed in the
sign profiles while the word was chosen each get one NEW prediction, on a kind of fact never printed for that sign
in any earlier script (seal size, the image on a copper tablet, the area of the city, the sign two places away,
the reverse face of a many-faced object).  All 13 were written into this file in one go, before any was computed,
and no profile was printed first.  A value moves to strict 'building' if its prediction comes true (P <= 0.1).
Writes work_data/sound_v5/job1_tests.csv."""
from sound_v5_common import *
J1 = [
 # sign, word, English, kind of fact, prediction, test
 ('240', 'mīmīn', 'High-star (house crest)', 'seal size',
  'High-star is a great house: seals with 240 are bigger than seals with the same number of signs', lambda: seal_size('240', True, True)),
 ('233', 'vāḷai', 'scabbard-fish, counted good', 'sign two places away',
  'a goods word takes measure then count: the sign two places after 233 is a number', lambda: two_away('233', set(VAL), (2,))),
 ('060', '-iṉ', 'of (joiner)', 'sign two places away',
  'opener-iṉ [ward] [crest ...]: the sign two places after 060 is a fish crest', lambda: two_away('060', FISH, (2,))),
 ('435', 'kōl', 'rod, sceptre: an office', 'sign two places away',
  'mutal kōl [carrier] [class]: the sign two places after 435 is a closing class sign (jar, man, comb, spear, carrier) or the text end',
  lambda: two_away('435', CLOSE | {'$'}, (2,))),
 ('388', 'aracu', 'royal (house name)', 'sign two places away',
  'aracu kuṭi [man/comb/spear]: the sign two places after 388 is a person or class sign after the jar (man, comb, spear, carrier) or the text end',
  lambda: two_away('388', {'090', '400', '520', '$'} | PORTER, (2,))),
 ('382', 'aracu', 'royal (lineage head)', 'sign two places away',
  'aracu maka kuṭi: the sign two places after 382 is the jar', lambda: two_away('382', '740', (2,))),
 ('097', 'aṭimai', 'bondsman, ration receiver', 'reverse face',
  'a ration receiver: the other face of a many-faced object with 097 carries a number or cup', lambda: reverse_has('097', NUMCUP)),
 ('790', 'maṇi', 'bead, gem', 'sign two places away',
  'beads are counted goods: a number stands two places before or after 790', lambda: two_away('790', set(VAL), (-2, 2))),
 ('550', 'vāy', 'gate', 'sign two places away',
  'vāy [guard/joiner] [class]: the sign two places after 550 is a closing class sign or the text end', lambda: two_away('550', CLOSE | {'$'}, (2,))),
 ('923', 'maruppu', 'crescent horn (counted thing)', 'copper-tablet image',
  'a horn word: copper tablets with 923 show a horned beast (bull, unicorn, gaur, zebu, buffalo, goat)', lambda: ctab_image('923', HORNED)),
 ('877', 'nālkāṇi', 'four shares (a holding opener)', 'sign two places away',
  'kāṇi [count] [crest]: the sign two places after 877 is a fish crest', lambda: two_away('877', FISH, (2,))),
 ('104', 'taṭṭāṉ', 'goldsmith (a craft hand)', 'seal size',
  'a craftsman, not a great house: seals with 104 are smaller than seals with the same number of signs', lambda: seal_size('104', False, True)),
 ('831', 'tiṉai', 'Italian millet', 'reverse face',
  'a crop is issued in amounts: the other face of a many-faced object with 831 carries a number or cup', lambda: reverse_has('831', NUMCUP)),
]
if __name__ == '__main__':
    rows = []
    for s, w, en, kind, pred, fn in J1:
        r = run('J1', s, w, pred, fn); r.update(kind=kind, english=en); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT5}/job1_tests.csv', index=False)
    print('moved to strict:', int((df.outcome == 'yes').sum()), 'of', len(df))
