#!/usr/bin/env python3
"""Job 1 of the fourth sound pass: split the two readings of 705 (U-vessel with a stick standing in it) and 706.
One word may carry both: Tamil kalam = vessel, ship (DEDR 1305) AND "a measure of capacity" (Tamil Lexicon p. 778,
sense 10, citing Tolkappiyam; marakkal = 1/12 kalam, p. 3082).
Predictions written into this file before it was first run:
 MEASURE (kalam the grain measure)
  M1 new texts: a count follows 705 more than chance
  M2 new texts: the count after it is tall strokes (the container series)
  M3 new texts: grain / measure words stand on the same face (413 nel, 806 vilai, 575 kottai, 711, 700 cup, 845 sheaves,
     320 pati, 540 parai, 171 nirai, 480 kunri, 335 town-of-the-granary)
  M4 new texts: it sits on record objects (miniature tablets, copper tablets, pots) more than chance
  M5 Lipi findspots: Harappa objects with 705/706 lie in mound F (granary, threshing floors) more than Harappa objects overall
  M6 both catalogues: on goods objects (not seals) the count after it varies (not three) more than on seals
 SHIP (kalam the ship)
  S1 new texts: at Lothal (the port) more than chance
  S2 both catalogues: at the coast and abroad (Lothal, Dholavira, Bala-kot, Gola Dhoro, Kanmer, Surkotada, Kuntasi, Nageshwar,
     Desalpur, Juna Khatiya, and every site in the Gulf, Mesopotamia, Iran) more than chance
  S3 new texts: sail 500 follows it (the v3 result, rerun)
  S4 new texts: on sealings/tags more than chance
  S5 new texts: trade-tag words on the same face (055 dozen, 890 given, 892 sale, 048, 220 fish) more than chance
Then every single use (face) of 705/706 in both catalogues is put in a box: measure context, ship context, both, neither.
Writes work_data/sound_v4/job1_tests.csv, job1_uses.csv."""
from sound_v4_common import *
from scipy.stats import fisher_exact
S = {'705', '706'}
GRAIN = {'413', '806', '575', '711', '700', '845', '320', '540', '171', '480', '335'}
TRADE = {'055', '890', '892', '048', '220'}
COAST = {'Lothal', 'Dholavira', 'Bala-kot', 'Gola Dhoro (Bagasra)', 'Kanmer', 'Surkotada', 'Kuntasi', 'Nageshwar', 'Desalpur', 'Juna Khatiya',
         'abroad', 'Ur', "Ra's al-Junayz", 'Failaka', 'Kish', 'Susa', 'Salut', 'Nippur', "Qala'at al-Bahrain", 'Tell Umma', 'Tello', 'Tepe Yahya',
         'Girsu', 'Saar', 'Janabiyah', 'Kalba', 'Hajar', 'Luristan', 'Karzakan'}
ABROAD = COAST - {'Lothal', 'Dholavira', 'Bala-kot', 'Gola Dhoro (Bagasra)', 'Kanmer', 'Surkotada', 'Kuntasi', 'Nageshwar', 'Desalpur', 'Juna Khatiya'}
RECORD = ['mtab', 'ctab', 'pot']


def face_has(cat, test):
    rows = kfaces(cat)
    allm = np.array([test(x, k, st) for x, k, st in rows]); sub = np.array([test(x, k, st) for x, k, st in rows if S & set(x)])
    return allm, sub


def share_t(label, cat, test):
    a, s = face_has(cat, test); return share(a, s, f'{label} ({cat})')


def count_after(cat):
    k = n = K = N = 0
    for x, kk, st in kfaces(cat):
        for i, a in enumerate(x[:-1]):
            N += 1; K += x[i + 1] in VAL
            if a in S: n += 1; k += x[i + 1] in VAL
    return res(k / n > K / N, binomtest(k, n, K / N, alternative='greater').pvalue, f'a count right after it {k}/{n} = {k / n:.0%} against {K / N:.1%} ({cat})')


def tall_after(cat):
    c = [x[i + 1] for x, kk, st in kfaces(cat) for i, a in enumerate(x[:-1]) if a in S and x[i + 1] in VAL]
    allc = [a for x, kk, st in kfaces(cat) for a in x if a in VAL]
    bt = sum(a in TALL for a in allc) / max(1, sum((a in TALL) or (a in SHORT) for a in allc))
    ta = sum(a in TALL for a in c); n = sum((a in TALL) or (a in SHORT) for a in c)
    return res(ta / n > bt, binomtest(ta, n, bt, alternative='greater').pvalue, f'counts after it: tall {ta} of {n} ({ta / n:.0%}) against {bt:.0%} tall for all counts ({cat})')


def varied_on_goods():
    """count after 705/706: share that is not three, goods objects against seals (both catalogues)."""
    g = [0, 0]; s = [0, 0]; vals = collections.defaultdict(collections.Counter)
    for x, kk, st in kfaces('LM'):
        for i, a in enumerate(x[:-1]):
            if a in S and x[i + 1] in VAL:
                v = VAL[x[i + 1]]; vals[kk][v] += 1
                tgt = s if kk == 'seal' else g; tgt[0] += v != 3; tgt[1] += 1
    p = fisher_exact([[g[0], g[1] - g[0]], [s[0], s[1] - s[0]]], alternative='greater')[1]
    det = '; '.join(f'{k}: ' + ', '.join(f'{v}x{c}' for v, c in sorted(vals[k].items())) for k in sorted(vals))
    return res(g[0] / g[1] > s[0] / s[1], p, f'count after it is not three: goods objects {g[0]}/{g[1]} against seals {s[0]}/{s[1]} [values by kind: {det}]')


TESTS = [
 ('M1', 'measure', 'new texts: a count follows it', 'fresh', lambda: count_after('Mu')),
 ('M2', 'measure', 'new texts: the count after it is tall strokes', 'fresh', lambda: tall_after('Mu')),
 ('M3', 'measure', 'new texts: grain/measure words on the same face', 'fresh', lambda: share_t('faces with a grain/measure word', 'Mu', lambda x, k, st: bool(GRAIN & set(x)))),
 ('M4', 'measure', 'new texts: on miniature tablets, copper tablets, pots', 'fresh', lambda: on_kind(S, RECORD)),
 ('M5', 'measure', 'Lipi: Harappa objects with it lie in mound F (granary area)', 'fresh', lambda: share(objs[objs.site == 'Harappa'].area.str.startswith('F'), objs[(objs.site == 'Harappa') & objs.signs.apply(lambda z: bool(S & z))].area.str.startswith('F'), 'Harappa objects from mound F')),
 ('M6', 'measure', 'both catalogues: count after it varies on goods objects, fixed on seals', 'fresh', varied_on_goods),
 ('S1', 'ship', 'new texts: at Lothal', 'seen in v3', lambda: share_t('faces at Lothal', 'Mu', lambda x, k, st: st == 'Lothal')),
 ('S2', 'ship', 'both catalogues: coast and abroad', 'fresh', lambda: share_t('faces at coast/abroad sites', 'LM', lambda x, k, st: st in COAST)),
 ('S2b', 'ship', 'both catalogues: abroad only', 'fresh', lambda: share_t('faces abroad', 'LM', lambda x, k, st: st in ABROAD)),
 ('S3', 'ship', 'new texts: sail 500 follows it', 'seen in v3', lambda: adjacent('705', '500', 'next', 'Mu')),
 ('S4', 'ship', 'new texts: on sealings/tags', 'seen in v3', lambda: on_kind(S, 'tag')),
 ('S5', 'ship', 'new texts: trade-tag words on the same face', 'fresh', lambda: share_t('faces with a trade-tag word', 'Mu', lambda x, k, st: bool(TRADE & set(x)))),
]


def box(x, k, st):
    """the context of one face: measure clues and ship clues."""
    m = []; s_ = []
    for i, a in enumerate(x):
        if a in S and i + 1 < len(x) and x[i + 1] in VAL: m.append('count after')
        if a in S and i + 1 < len(x) and x[i + 1] == '500': s_.append('sail after')
    if GRAIN & set(x): m.append('grain word')
    if k in RECORD: m.append(k)
    if st in COAST: s_.append('coast/abroad')
    if k == 'tag' and TRADE & set(x): s_.append('trade tag')
    return m, s_


if __name__ == '__main__':
    rows = []
    for i, (tag, side, pred, fr, fn) in enumerate(TESTS, 1):
        print(f'({i}/{len(TESTS)})', end=' ')
        r = run(tag, '705/706', side, pred, fn); r['fresh'] = fr; rows.append(r)
    pd.DataFrame(rows).to_csv(f'{OUT4}/job1_tests.csv', index=False)
    # every use
    U = []
    for cat in ['L', 'Mu']:
        for x, k, st in kfaces(cat):
            if not S & set(x): continue
            m, s_ = box(x, k, st)
            U.append(dict(cat=cat, text='-'.join(x), kind=k, site=st, measure=';'.join(m), ship=';'.join(s_),
                          box='both' if m and s_ else 'measure' if m else 'ship' if s_ else 'neither'))
    U = pd.DataFrame(U); U.to_csv(f'{OUT4}/job1_uses.csv', index=False)
    print('\nuses by box:'); print(U.groupby(['cat', 'box']).size().unstack(fill_value=0))
    print('\nship and both uses:'); print(U[U.box.isin(['ship', 'both'])].to_string(max_colwidth=60))
    print('\nneither, by kind:'); print(U[U.box == 'neither'].kind.value_counts().to_dict())
    print('\nneither, commonest texts:'); print(U[U.box == 'neither'].text.value_counts().head(15).to_dict())


def grade_tests():
    """Why the fixed three: 'three kalam' as a grade written into titles.
    G1 (prediction written before running): the chief/spear 520 follows the phrase 705/706-033 more than it follows any sign.
    G2: seals carrying 705/706-033 are bigger than seals with the same number of signs (a graded holding)."""
    out = []
    k = n = K = N = 0
    for x, kk, st in kfaces('LM'):
        for i in range(len(x) - 1):
            N += 1; K += x[i + 1] == '520'
            if i >= 1 and x[i] == '033' and x[i - 1] in S: n += 1; k += x[i + 1] == '520'
    out.append(run('G1', '705/706-033', 'grade', 'the chief 520 follows "three kalam"', lambda: res(k / n > K / N, binomtest(k, n, K / N, alternative='greater').pvalue, f'520 after 705/706-033: {k}/{n} = {k / n:.0%} against {K / N:.1%} after any sign (LM)')))
    se = objs[objs.seal & (objs.face > 0)].copy()
    se['has'] = [any(f[i] in S and f[i + 1] == '033' for f in fs for i in range(len(f) - 1)) for fs in se.faces]
    med = se.groupby('nsign').face.median(); se['rel'] = se.face / se.nsign.map(med)
    a, b = se[se.has].rel, se[~se.has].rel
    out.append(run('G2', '705/706-033', 'grade', 'seals with "three kalam" are bigger at equal sign count', lambda: res(a.median() > 1, mannwhitneyu(a, b, alternative='greater').pvalue, f'seal face against seals of the same sign count x{a.median():.2f} (n {len(a)})')))
    return out


if __name__ == '__main__':
    g = grade_tests(); pd.DataFrame(g).to_csv(f'{OUT4}/job1_grade.csv', index=False)
