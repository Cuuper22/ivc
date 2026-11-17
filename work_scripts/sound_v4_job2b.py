#!/usr/bin/env python3
"""Rescue stage for the job-2 signs whose A and B both missed (sound_v4_job2.py): one better test of the same
word (B2), then one new word (C).  Written before running.  Also the clean version of the 832 test (the first run
counted 832 standing after 832; this one does not).  Writes work_data/sound_v4/job2b_tests.csv."""
from sound_v4_job2 import *
LAND = {'615', '503', '845', '061'}
R = {
 '435': [('B2', 'taṭi', 'staff; measuring rod (DEDR 3030 lists "measuring rod")', '3030', 'a land measuring rod: land words (field, hill, sheaves, quarter) on the same face (both catalogues)', 'fresh', lambda: same_face('435', LAND, 'LM')),
         ('C', 'kōl', 'rod, sceptre, measuring rod (an office: the staff-holder)', 'Ta. kōl', 'an office held by a person: on new texts a carrier or the bound-word 690 follows it', 'seen', lambda: adjacent('435', {'156', '154', '690'}, 'next', 'Mu'))],
 '407': [('B2', 'kiḷai', 'the lot (tally word)', '2018', 'a tally word closes the record: on copper tablets it is the last sign more than other copper-tablet signs', 'seen',
          lambda: _last_ctab())],
 '382': [('B2', 'aracu', 'pipal; royal', '202', 'a lineage head: maka "child of" follows it (both catalogues)', 'seen', lambda: adjacent('382', '760', 'next', 'LM'))],
 '104': [('C', 'taṭṭāṉ', 'goldsmith (person with the seed-weight kuṉṟi at his foot)', '3039', 'a goldsmith works with the smith: 104 stands in the frames of the smith 391', 'fresh', lambda: frame_swap('104', {'391'})),
         ('C2', 'taṭṭāṉ', 'goldsmith', '3039', 'a goldsmith weighs gold: the gold weight 645 or seed-weight 480 on the same face (both catalogues)', 'seen', lambda: same_face('104', {'645', '480'}, 'LM'))],
 '832': [('B', 'kaṇ', 'at, in', '1161', 'clean rerun: on new texts a time or place word (not 832 itself) stands before it', 'fresh', lambda: prev_in('832', TIMEPLACE))],
}


def _last_ctab():
    """share of 407's uses on copper tablets that are text-final, against the text-final share of all signs on copper tablets."""
    F = [x for x, k, st in kfaces('L') if k == 'ctab' and len(x) >= 2]
    K = sum(1 for x in F for i, a in enumerate(x) if i == len(x) - 1); N = sum(len(x) for x in F)
    k = sum(1 for x in F for i, a in enumerate(x) if a == '407' and i == len(x) - 1); n = sum(1 for x in F for a in x if a == '407')
    return res(k / n > K / N, binomtest(k, n, K / N, alternative='greater').pvalue, f'last sign on copper tablets {k}/{n} = {k / n:.0%} against {K / N:.0%} for all copper-tablet sign places')


if __name__ == '__main__':
    rows = []
    for s, L in R.items():
        for st, w, en, ref, pred, fr, fn in L:
            r = run(st, s, w, pred, fn); r.update(english=en, dedr=ref, fresh=fr); rows.append(r)
    pd.DataFrame(rows).to_csv(f'{OUT4}/job2b_tests.csv', index=False)
