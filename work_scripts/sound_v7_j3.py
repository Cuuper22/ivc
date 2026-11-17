#!/usr/bin/env python3
"""JOB 3: the next 30 signs, and the measure words stuck inside names.
Order kept: picture and slot first (sound_v7_j3_profile.py printed them), then the word, then ALL predictions below were
written in one go (2026-11-17) before this file computed any of them. One redesign per miss: sound_v7_j3b.py.

For each sign: word, English, DEDR, CLASS (the job the word does, as in sound_v7_time_pred.py), and two predictions:
  A  a word-specific test (frames shared with signs of the same meaning, seal size, the other face of the object, ...);
     BASIS says whether the fact behind A had been glimpsed in the printed profile ('seen') or not ('fresh').
  B  THE TIME TEST, a fresh kind of fact: the class signature must show (share above the bin base) BOTH in the middle bin
     (most of the dated data) AND in early + late pooled; each part needs 3+ uses, else 'too few'.
Verdict rule (written first): building if A came true ('yes', P <= 0.1), or if B held in both parts and A pointed the
right way; strict if the true test was fresh; otherwise testing.

MEASURE WORDS INSIDE NAMES (700, 705, 530, 540, 575, 711, 868, 861): each gets a name-sense or a rule that moves it out
of the name, with one prediction (M tests below), written in the same go.
Outputs: work_data/sound_v7/j3_tests.csv, j3_log.txt"""
from sound_v7_common import *
from sound_v7_time_pred import CLASS as TCLASS
V, S, Wd = load_values()
NUM = set(VAL)
FISHC = {'220', '226', '231', '233', '235', '236', '240'}
TITLES = {'090', '400', '520', '368', '525', '526', '527', '617', '679', '717', '842'} | set(PORTER) | {'152', '161'}
CLOSE = TITLES | {'740'}
HEAD = {'920', '900', '550', '555', '820', '692'}
LOG = open(f'{OUT7}/j3_log.txt', 'w')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')

# ---------------- the words (sign: sound, English, DEDR, class) ----------------
W = {
 '592': ('paṭṭi', 'pen, fold, hamlet', '3868', 'NAME'),
 '703': ('maṉai', 'house-site; a land measure', '4776', 'MEASURE'),
 '554': ('kaḷam', 'threshing floor (kaḷam kāval: threshing-floor guard)', '1376', 'NAME'),
 '064': ('pāti', 'half, a share (a counted portion)', '4074', 'THING'),
 '136': ('aṭimai', 'bondsman (counted head)', '72', 'THING'),
 '603': ('kūṭu', 'grain receptacle, pen', '1883', 'NAME'),
 '098': ('ēvalaṉ', 'servant, attendant (raised arm: at command)', '909', 'NAME'),
 '408': ('kiḷai', 'lot, bunch (counted tree)', '2018', 'COUNTED'),
 '621': ('aṭai', 'shut in, stored, pledged (a closing word)', '83', 'TITLE'),
 '243': ('kayal', 'carp (a crest fish)', '1252', 'NAME'),
 '130': ('kaḷamar', 'threshing-floor men, husbandmen (counted)', '1376', 'THING'),
 '697': ('ney', 'weaving, woven (with cotton)', '3745', 'GOODS'),
 '776': ('malar', 'Bloom (a name word: to abound, flower)', '4729', 'NAME'),
 '804': ('ilai', 'Leaf (a name word after a crest)', '497', 'NAME'),
 '127': ('villavaṉ', 'archer, bowman', '5422', 'NAME'),
 '167': ('kūli', 'wages, pay, freight (closes kalam chits)', '1905', 'TITLE'),
 '165': ('nāḷ', 'day (after the month: a date)', '3656', 'DATE'),
 '645': ('kar̤añcu', 'a gold weight (counted)', '1348', 'THING'),
 '236': ('vēymīn', 'Bamboo-star (caged crest variant)', '', 'NAME'),
 '048': ('er̤uvar', 'the Seven (a house name)', '', 'NAME'),
 '832': ('aṭai', 'leaves, greens, betel leaf (counted)', '59', 'THING'),
 '460': ('mukkōṭu', 'Three-peaks', '', 'NAME'),
 '222': ('aṭaimīn', 'Shut-in-fish (crest)', '83', 'NAME'),
 '821': ('mañcāṭi', 'red-wood seed: a small goldsmith\'s weight (counted)', '4636', 'THING'),
 '792': ('aracu', 'royal (house name; variant of 384/388)', '201', 'NAME'),
 '350': ('kalappai', 'plough (counted: ploughs of land)', '1304', 'THING'),
 '027': ('toṇṭu', 'Nine (a spelled number in a name)', '3532', 'NAME'),
 '201': ('kār', 'the rain season and its crop (a date head before -iṉ)', '1395', 'OPENER'),
 '921': ('vil', 'bow (vil-ampu vēḷ: chief of bow and arrow)', '5422', 'NAME'),
 '232': ('kūṭumīn', 'Cluster-star (caged fish crest)', '', 'NAME'),
}
# ---------------- prediction A per sign: (description, basis, function) ----------------
A = {
 '592': ('shares frames with place / store words 335 336 605 615 503', 'fresh', lambda: frame_swap('592', {'335', '336', '605', '615', '503'})),
 '703': ('shares frames with land words 615 421-424 503', 'fresh', lambda: frame_swap('703', {'615', '421', '422', '423', '424', '503'})),
 '554': ('shares frames with the gate words 550 555 (both stand before the guard)', 'fresh', lambda: frame_swap('554', {'550', '555'})),
 '064': ('shares frames with the share words 850 861 817 868', 'fresh', lambda: frame_swap('064', {'850', '861', '817', '868'})),
 '136': ('shares frames with counted persons 097 137 130', 'fresh', lambda: frame_swap('136', {'097', '137', '130'})),
 '603': ('shares frames with grain-store words 605 590 335', 'fresh', lambda: frame_swap('603', {'605', '590', '335'})),
 '098': ('the other face of its objects holds a cup or a number (ration chit)', 'fresh', lambda: reverse_has('098', NUM | {'700'})),
 '408': ('shares frames with the tree signs 390 405 407', 'fresh', lambda: frame_swap('408', {'390', '405', '407'})),
 '621': ('seals ending in it carry no jar (it stands in the jar\'s place)', 'fresh', lambda: no_jar('621', 'L')),
 '243': ('shares frames with the crest fish 231 233 235 240', 'fresh', lambda: frame_swap('243', {'231', '233', '235', '240'})),
 '130': ('shares frames with counted persons 097 137 136', 'fresh', lambda: frame_swap('130', {'097', '137', '136'})),
 '697': ('shares frames with cotton / thread 390 405', 'fresh', lambda: frame_swap('697', {'390', '405'})),
 '776': ('shares frames with produce words 806 838 831', 'fresh', lambda: frame_swap('776', {'806', '838', '831'})),
 '804': ('shares frames with produce / leaf words 806 838 832', 'fresh', lambda: frame_swap('804', {'806', '838', '832'})),
 '127': ('shares frames with fighter words 125 565 130', 'fresh', lambda: frame_swap('127', {'125', '565', '130'})),
 '167': ('the other face of its tablets holds a who-word (a name with the jar, or a person sign)', 'fresh', lambda: reverse_has('167', {'740', '090', '400', '097', '137', '140'})),
 '165': ('shares frames with the time words 920 900 904 927', 'fresh', lambda: frame_swap('165', {'920', '900', '904', '927'})),
 '645': ('shares frames with the weight words 480 171 850', 'fresh', lambda: frame_swap('645', {'480', '171', '850'})),
 '236': ('shares frames with 235 Bamboo-star', 'fresh', lambda: frame_swap('236', {'235'})),
 '048': ('two places before it stands a share opener 817 / 850 / 851 (seen in the texts)', 'seen', lambda: two_away('048', {'817', '850', '851'}, offs=(-2,), cat='LM')),
 '832': ('shares frames with counted goods 390 845 405', 'fresh', lambda: frame_swap('832', {'390', '845', '405'})),
 '460': ('shares frames with 463 Three-peaks', 'fresh', lambda: frame_swap('460', {'463'})),
 '222': ('shares frames with the crest fish 220 231 240', 'fresh', lambda: frame_swap('222', {'220', '231', '240'})),
 '821': ('shares frames with the weights 480 645 171', 'fresh', lambda: frame_swap('821', {'480', '645', '171'})),
 '792': ('shares frames with the royal words 382 384 388', 'fresh', lambda: frame_swap('792', {'382', '384', '388'})),
 '350': ('shares frames with land words 615 421 422 503', 'fresh', lambda: frame_swap('350', {'615', '421', '422', '503'})),
 '027': ('shares frames with the many-stroke numbers 018 019 016', 'fresh', lambda: frame_swap('027', {'018', '019', '016'})),
 '201': ('shares frames with the head words 920 550 820', 'fresh', lambda: frame_swap('201', {'920', '550', '820'})),
 '921': ('seals carrying it are bigger than seals of the same length (the bow-and-arrow chief)', 'fresh', lambda: seal_size('921', True)),
 '232': ('shares frames with the caged fish 226 236', 'fresh', lambda: frame_swap('232', {'226', '236'})),
}

def sigc(cls, x, i, kind):
    n = len(x)
    if cls == 'NAME': return any(y in CLOSE for y in x[i + 1:])
    if cls == 'TITLE': return i == n - 1
    if cls == 'MEASURE': return i + 1 < n and x[i + 1] in NUM
    if cls == 'THING': return i > 0 and x[i - 1] in NUM
    if cls == 'COUNTED': return (i > 0 and x[i - 1] in NUM) or (i + 1 < n and x[i + 1] in NUM)
    if cls == 'OPENER': return i == 0
    if cls == 'GOODS': return kind != 'seal'
    if cls == 'DATE': return (i > 0 and x[i - 1] in {'900', '920', '904', '927'}) or i == 0
    raise ValueError(cls)
F = dated_faces()
ALLU = [(b, x, i, k) for x, k, site, b, st, o in F for i, a in enumerate(x) if a not in NUM and a not in ('000', 'ALT')]
_base = {}
def base(cls, part):
    if (cls, part) not in _base:
        u = [sigc(cls, x, i, k) for b, x, i, k in ALLU if (b == 'middle') == (part == 'middle')]
        _base[(cls, part)] = float(np.mean(u))
    return _base[(cls, part)]
def time_test(s, cls):
    out = {}
    for part in ('middle', 'early+late'):
        u = [sigc(cls, x, i, k) for b, x, i, k in ALLU if x[i] == s and ((b == 'middle') == (part == 'middle'))]
        out[part] = (sum(u), len(u), base(cls, part))
    if any(n < 3 for k, n, b in out.values()): verdict = 'too few'
    else: verdict = 'held' if all(k / n > b for k, n, b in out.values()) else 'failed'
    txt = '; '.join(f'{p} {k}/{n} against base {b:.0%}' for p, (k, n, b) in out.items())
    return verdict, txt

rows = []
log('[j3] 30 signs: A (word test) and B (time test)')
for s, (snd, en, dedr, cls) in W.items():
    desc, basis, fn = A[s]
    r = run('A', s, snd, desc, fn); r['basis'] = basis
    tv, tt = time_test(s, cls)
    log(f'[B] {s} {snd}: class {cls} signature holds in middle and in early+late -> {tv}: {tt}')
    ok_a = r['outcome'] == 'yes'; dir_a = r['outcome'] in ('yes', 'direction only')
    if ok_a: status = 'strict' if basis == 'fresh' else 'wide'
    elif tv == 'held' and dir_a: status = 'strict'
    else: status = 'testing'
    rows.append(dict(sign=s, sound=snd, english=en, dedr=dedr, cls=cls, A=desc, A_basis=basis, A_outcome=r['outcome'], A_p=r['p'], A_result=r['result'],
                     B=tv, B_result=tt, status=status))
T = pd.DataFrame(rows)
log('\n[j3] statuses:', dict(T.status.value_counts()), ' A:', dict(T.A_outcome.value_counts()), ' B:', dict(T.B.value_counts()))

# ---------------- measure words inside names ----------------
log('\n[M] measure words inside names: name-senses and rules (predictions written before computing)')
LM = faces_all('LM')
def uses(s, cat='LM'):
    for x, P, site, g in faces_all(cat):
        for i, a in enumerate(x):
            if a == s: yield x, i, site
def counted(x, i): return (i > 0 and x[i - 1] in NUM) or (i + 1 < len(x) and x[i + 1] in NUM)
def in_name(x, i): return any(y in CLOSE for y in x[i + 1:])
mrows = []
def mrun(sign, rule, pred, fn):
    try: res_ = fn()
    except Exception as e: res_ = None; log('   error', e)
    if res_ is None: out = ('n/a', np.nan, 'too few')
    else: ok, p, txt = res_; out = ('yes' if ok and p <= 0.1 else 'direction only' if ok else 'no', p, txt)
    log(f'[M] {sign}: {rule}\n     prediction: {pred}\n     -> {out[0]}: {out[2]}, P {out[1]:.3g}')
    mrows.append(dict(sign=sign, rule=rule, prediction=pred, outcome=out[0], p=out[1], result=out[2]))
COAST = {'Lothal', 'Chanhu-daro', 'Dholavira', 'Surkotada', 'abroad', 'Kanmer', 'Desalpur', 'Rangpur', 'Bala-kot', 'Shikarpur'}
def m705():
    sub = [site in COAST or site not in ('Mohenjo-daro', 'Harappa', 'Kalibangan', 'other', 'Unknown', 'Banawali', 'Rakhigarhi') and False for x, i, site in uses('705')]
    a = [(site in COAST) for x, i, site in uses('705') if not counted(x, i) and in_name(x, i)]
    b = [(site in COAST) for x, i, site in uses('705') if counted(x, i)]
    return share(b, a, 'uncounted 705 inside a name at Gujarat / coast / abroad sites, against counted 705')
mrun('705', 'uncounted 705 inside a name = Kalam "Ship" (the vessel sense of kalam); counted 705 keeps "n kalam" and moves out of the name as an allowance',
     'uncounted name uses sit at coast / Gujarat / abroad sites more than counted uses', m705)
def m700():
    se = objs[objs.seal & (objs.face > 0)].copy()
    med = se.groupby('nsign').face.median(); se['rel'] = se.face / se.nsign.map(med)
    has = se.faces.apply(lambda fs: any(a == '700' and not counted(x, i) for x in fs for i, a in enumerate(x)))
    from scipy.stats import mannwhitneyu
    a, b = se[has].rel, se[~has].rel
    if len(a) < 4: return None
    return res(a.median() < 1, mannwhitneyu(a, b, alternative='less').pvalue, f'seals with an uncounted cup: x{a.median():.2f} of seals of the same length (n {len(a)})')
mrun('700', 'uncounted 700 on a seal = nāḻi "the Measurer", a ration-issuer\'s seal (a title, out of the name)', 'such seals are smaller than seals of the same length (a low office)', m700)
def m530():
    a = [any(y in CLOSE for y in x[i + 1:i + 3]) for x, i, site in uses('530') if not counted(x, i)]
    allm = [any(y in CLOSE for y in x[j + 1:j + 3]) for x, P, st, g in LM for j in range(len(x)) if x[j] not in NUM]
    return share(allm, a, 'uncounted 530 with the jar or a closer within two after it')
mrun('530', 'uncounted 530 in a name = paṟaiyaṉ "Drummer, the crier" (paṟai "proclamation")', 'the jar or a closing title stands within two signs after it more than after other signs', m530)
def m540():
    a = [(i == len(x) - 1) for x, i, site in uses('540') if not counted(x, i)]
    allm = [(j == len(x) - 1) for x, P, st, g in LM for j in range(len(x)) if x[j] not in NUM]
    return share(allm, a, 'uncounted 540 last in its text')
mrun('540', 'uncounted 540 = paṟai "Drum": the goods word on pots and bangles, a name word on seals; counted 540 is the rice measure', 'uncounted 540 ends its text more than other signs (a goods label)', m540)
def m575():
    se = objs[objs.seal & (objs.face > 0)].copy()
    med = se.groupby('nsign').face.median(); se['rel'] = se.face / se.nsign.map(med)
    has = se.faces.apply(lambda fs: any(a == '575' and in_name(x, i) for x in fs for i, a in enumerate(x)))
    from scipy.stats import mannwhitneyu
    a, b = se[has].rel, se[~has].rel
    if len(a) < 4: return None
    return res(a.median() > 1, mannwhitneyu(a, b, alternative='greater').pvalue, f'seals with 575 inside a name: x{a.median():.2f} of seals of the same length (n {len(a)})')
mrun('575', '575 inside a seal name = kōṭṭai "Fort, store-house" (the holder of a store); on a goods line it stays the great measure', 'seals with it in a name are bigger than seals of the same length', m575)
def m711():
    a = [in_name(x, i) and not counted(x, i) for x, i, site in uses('711')]
    allm = [in_name(x, j) and not counted(x, j) for x, P, st, g in LM for j in range(len(x)) if x[j] not in NUM]
    return share_less(allm, a, 'uncounted 711 before a jar or closer')
mrun('711', '711 is never a name word: on a goods line "pot, n vaḷḷam" it is a measure and the line is not a name (no hyphened name on goods tablets)', 'uncounted uses before a jar or closer are fewer than for other signs', m711)
def m868():
    m = M[~M.partnered]
    a = []
    for x in m.tok:
        for i, s_ in enumerate(x):
            if s_ == '868': a.append(i > 0 and x[i - 1] in ('705', '706'))
    allm = [i > 0 and x[i - 1] in ('705', '706') for x in m.tok for i in range(len(x))]
    return share(allm, a, 'new texts: 868 right after a kalam sign')
mrun('868', '705/706 + 868 = "half a kalam" (araikkāṇi as the fraction of the measure before it), read as an amount, never inside a name', 'on new texts 868 stands right after a kalam sign more than chance (fact glimpsed on first-catalogue texts)', m868)
def m861():
    a = []
    for x, i, site in uses('861'):
        if i == 0 and i + 1 < len(x) and x[i + 1] in NUM:
            j = i + 1
            while j < len(x) and x[j] in NUM: j += 1
            if j < len(x): a.append(x[j] in FISHC or x[j] in {'803', '798', '415', '590', '140', '235', '255', '503', '806'})
    allm = [x[j] in FISHC or x[j] in {'803', '798', '415', '590', '140', '235', '255', '503', '806'} for x, P, st, g in LM for j in range(len(x)) if x[j] not in NUM]
    return share(allm, a, 'front 861 + count: the next word is a crest or house word')
mrun('861', '861 + count at the front = the share opener ("two shares:"), moved out of the name; the name starts after the count', 'the next word after the count is a crest or house word more than chance', m861)
MT = pd.DataFrame(mrows)
T.to_csv(f'{OUT7}/j3_tests.csv', index=False); MT.to_csv(f'{OUT7}/j3_measure_tests.csv', index=False)
LOG.close()
