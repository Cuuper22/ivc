#!/usr/bin/env python3
"""JOB 3, ONE REDESIGN PER MISS (written in one go after sound_v7_j3.py reported, before this file computed anything).
Every sign that did not come out building gets one more test, A2. Most A2 tests use a fact visible in the printed profile,
so a yes counts WIDE (basis 'seen'); fresh ones are marked. Measure words that missed get one more each (M2).
Verdict: building if A2 yes (strict if fresh, wide if seen); else stays testing.
Outputs: work_data/sound_v7/j3b_tests.csv, j3b_log.txt; final job-3 values: sound_v7_j3vals.py is written from both runs."""
from sound_v7_common import *
J3 = pd.read_csv(f'{OUT7}/j3_tests.csv', dtype=str).fillna('')
NUM = set(VAL)
TIT = {'151', '152', '153', '154', '155', '156', '157', '158', '400', '842', '617', '150', '090'}
FISHC = {'220', '226', '231', '233', '235', '236', '240'}
LOG = open(f'{OUT7}/j3b_log.txt', 'w')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')
def edge(s, cat='LM'):
    k = n = K = N = 0
    for x, P, st, g in faces_all(cat):
        for i, a in enumerate(x):
            e = i == 0 or i == len(x) - 1; N += 1; K += e
            if a == s: n += 1; k += e
    if n < 3: return None
    return res(k / n > K / N, binomtest(k, n, K / N, alternative='greater').pvalue, f'at the first or last place {k}/{n} = {k / n:.0%} against {K / N:.0%} (LM)')
def last(s, cat='LM'):
    k = n = K = N = 0
    for x, P, st, g in faces_all(cat):
        for i, a in enumerate(x):
            e = i == len(x) - 1; N += 1; K += e
            if a == s: n += 1; k += e
    if n < 3: return None
    return res(k / n > K / N, binomtest(k, n, K / N, alternative='greater').pvalue, f'last sign {k}/{n} = {k / n:.0%} against {K / N:.0%} (LM)')
A2 = {
 '592': ('a keeper, junior, deputy, servant or manager title follows directly ("keeper of the pen")', 'seen', lambda: adjacent('592', TIT, 'next', 'LM')),
 '703': ('Mohenjo-daro house-mates both carry it (a house-site belongs to a household)', 'fresh', lambda: house_share('703', where='any')),
 '064': ('it sits on bangles and pots (a portion mark on goods)', 'seen', lambda: on_kind('064', {'bangle', 'pot'}, 'L')),
 '136': ('a number stands right before it (counted heads)', 'seen', lambda: adjacent('136', NUM, 'prev', 'LM')),
 '603': ('the share 861 or the jar follows directly ("share of the store", "of the store house")', 'seen', lambda: adjacent('603', {'861', '740'}, 'next', 'LM')),
 '098': ('the junior 400 follows directly ("junior attendant")', 'seen', lambda: adjacent('098', {'400'}, 'next', 'LM')),
 '408': ('a number stands right after it (lots counted after, like a measure)', 'seen', lambda: adjacent('408', NUM, 'next', 'LM')),
 '621': ('it is the last sign of its text', 'seen', lambda: last('621', 'L')),
 '243': ('a servant / keeper title follows directly (617, 151, 150)', 'seen', lambda: adjacent('243', {'617', '151', '150', '152'}, 'next', 'LM')),
 '130': ('a number stands right before it', 'seen', lambda: adjacent('130', NUM, 'prev', 'LM')),
 '697': ('it sits on pots (a mark on vessels of woven stuff)', 'seen', lambda: on_kind('697', {'pot'}, 'L')),
 '776': ('the jar follows directly (a name word)', 'seen', lambda: adjacent('776', {'740'}, 'next', 'LM')),
 '804': ('a crest fish stands right before it (Leaf after a crest)', 'seen', lambda: adjacent('804', FISHC, 'prev', 'LM')),
 '127': ('it stands at the edge of its text (first or last), as a personal name does on the Umma sealing', 'seen', lambda: edge('127', 'L')),
 '167': ('a kalam sign 704/705/706 stands right before it ("kalam as wages")', 'seen', lambda: adjacent('167', {'704', '705', '706'}, 'prev', 'LM')),
 '165': ('the month 900 / 920 stands right before it', 'seen', lambda: adjacent('165', {'900', '920'}, 'prev', 'LM')),
 '236': ('a number stands right before it (Two-Bamboo-star, spelled)', 'seen', lambda: adjacent('236', NUM, 'prev', 'LM')),
 '832': ('a number stands right before it (counted leaves)', 'seen', lambda: adjacent('832', NUM, 'prev', 'LM')),
 '821': ('it sits on copper tools (a weight word on weighed metal)', 'seen', lambda: on_kind('821', {'tool'}, 'L')),
 '350': ('a number stands right before it (n ploughs)', 'seen', lambda: adjacent('350', NUM, 'prev', 'LM')),
 '027': ('a tall two follows directly (Nine-Two: a spelled name number)', 'seen', lambda: adjacent('027', {'032'}, 'next', 'L')),
 '201': ('the joiner 060 follows directly (a head word: "of the rain season")', 'seen', lambda: adjacent('201', {'060'}, 'next', 'LM')),
 '232': ('it is the last sign of its text (a crest standing as the whole name)', 'seen', lambda: last('232', 'LM')),
}
rows = []
log('[j3b] redesigns for the signs that did not come out building')
for r in J3.itertuples():
    if r.status in ('strict', 'wide'): continue
    if r.sign not in A2: log(f'  {r.sign}: no redesign written'); continue
    desc, basis, fn = A2[r.sign]
    o = run('A2', r.sign, r.sound, desc, fn)
    st = ('strict' if basis == 'fresh' else 'wide') if o['outcome'] == 'yes' else 'testing'
    rows.append(dict(sign=r.sign, sound=r.sound, A2=desc, A2_basis=basis, A2_outcome=o['outcome'], A2_p=o['p'], A2_result=o['result'], status=st))
T = pd.DataFrame(rows); T.to_csv(f'{OUT7}/j3b_tests.csv', index=False)
log('[j3b] statuses after the redesign:', dict(T.status.value_counts()))
# measure-word redesigns
log('\n[M2] measure words that missed: one redesign each')
mr = []
def mm(sign, pred, basis, fn):
    o = run('M2', sign, '', pred, fn); o['basis'] = basis; mr.append(o)
mm('530', 'uncounted 530 is the last sign of its text ("proclaimed": a closing verb, not a name word)', 'seen', lambda: last('530', 'LM'))
mm('575', 'Mohenjo-daro house-mates both carry 575 (Fort as a household\'s name)', 'fresh', lambda: house_share('575', where='any'))
mm('868', 'the other face of objects carrying 868 holds a who-word (jar, title or person) (half a kalam issued to someone)', 'fresh', lambda: reverse_has('868', {'740', '090', '400', '097', '137', '140', '520'}))
pd.DataFrame(mr).to_csv(f'{OUT7}/j3b_measure_tests.csv', index=False)
LOG.close()
