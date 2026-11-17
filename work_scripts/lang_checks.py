# Checks that the Dravidian sound values predict and the other candidates do not.
# Reading order = reverse of stored order. Run from /home/claude/ivc:  python3 work_scripts/lang_checks.py
#  C1  spear 520 = vel 'spear' ~ vel 'chief, petty ruler' (DEDR 5536/5545): spear-closer seals sit in citadels.
#  C2  person-with-staff 142 = kol 'staff' ~ ko/kon 'king' (DEDR 2237/2177): 142 seals are larger than other seals.
#  C3  comb 400 = ciippu/cirppu 'comb' ~ ciru/ciir 'small, young' (DEDR 1610/1594): comb seals are the smallest and
#      the comb closes texts that name a junior; also check the zone.
#  C4  jar 740 = kutam 'waterpot' ~ kuti 'house, family, lineage' (DEDR 1651/1655): the sign before a closing jar is
#      shared by house-mates; the sign before the OTHER closers is not.
#  C5  the jar is a pot when counted: counted jars sit on other object types than closing jars.
#  C6  person 090 = aal 'man, servant' ~ aal 'to rule' (DEDR 399/5157): bare-person-closer seals vs jar+person seals size.
import csv, re, collections, random, statistics as st
import numpy as np
random.seed(7)
R = list(csv.DictReader(open('research/data/open_prototype/lipi/metadata_filtered.csv', encoding='utf-8')))
def toks(x): return re.findall(r'\d{3}', x['text'])[::-1]          # reading order
def area(x):
    try: return float(x['horizontal(mm)']) * float(x['vertical(mm)']) or None
    except: return None
CLOSERS = {'740': 'jar', '520': 'spear', '090': 'person', '400': 'comb', '151': 'carrier', '154': 'carrier',
           '156': 'carrier', '158': 'carrier', '155': 'carrier'}
def zone(x):
    s, a = x['site'], x['area-section']
    if s == 'Mohenjo-daro':
        if a.startswith('SD') or a.startswith('L'): return 'citadel'
        if a.startswith(('DK', 'HR', 'VS', 'MN')): return 'lower'
    if s == 'Harappa':
        if a.startswith('AB'): return 'citadel'
        if a.startswith(('F', 'E', 'D', 'G', 'H', 'J')): return 'lower'
    if s == 'Kalibangan':
        if a.startswith('KLB-1'): return 'citadel'
        if a.startswith('KLB-2'): return 'lower'
    if s == 'Dholavira':
        if 'Castle' in a or 'Bailey' in a: return 'citadel'
        if a.startswith(('Middle', 'Lower', 'Annexe', 'East', 'South')): return 'lower'
    return None
seals = []
for x in R:
    if not x['type'].startswith('SEAL'): continue
    t = toks(x)
    if len(t) < 2 or '000' in t[-1:]: continue
    seals.append(dict(x=x, t=t, cl=CLOSERS.get(t[-1]), z=zone(x), a=area(x)))
print('seals with a readable last sign:', len(seals))

print('\n== C1 closer by town zone (citadel vs lower town), all sites with a zone ==')
zc = collections.Counter((s['cl'], s['z']) for s in seals if s['z'] and s['cl'])
tot = collections.Counter(s['z'] for s in seals if s['z'] and s['cl'])
for c in ['jar', 'spear', 'person', 'comb', 'carrier']:
    a, b = zc[(c, 'citadel')], zc[(c, 'lower')]
    print(f"  {c:8s} citadel {a:3d}/{tot['citadel']} ({100*a/tot['citadel']:.1f}%)   lower {b:3d}/{tot['lower']} ({100*b/tot['lower']:.1f}%)")
# permutation: spear share in citadel vs lower
lab = [(s['cl'] == 'spear', s['z']) for s in seals if s['z'] and s['cl']]
obs = sum(1 for sp, z in lab if sp and z == 'citadel')
zs = [z for _, z in lab]; sps = [sp for sp, _ in lab]; null = []
for _ in range(5000):
    random.shuffle(zs); null.append(sum(1 for sp, z in zip(sps, zs) if sp and z == 'citadel'))
print(f"  spear seals in citadels: {obs}, chance {np.mean(null):.2f}, P {(1+sum(n>=obs for n in null))/5001:.4f}")
for site in ['Mohenjo-daro', 'Harappa', 'Kalibangan', 'Dholavira']:
    c = collections.Counter((s['cl'] == 'spear', s['z']) for s in seals if s['x']['site'] == site and s['z'] and s['cl'])
    nc, nl = c[(True,'citadel')] + c[(False,'citadel')], c[(True,'lower')] + c[(False,'lower')]
    if nc and nl: print(f"   {site:13s} spear in citadel {c[(True,'citadel')]}/{nc}  lower {c[(True,'lower')]}/{nl}")

print('\n== C2 seals carrying person-with-staff 142 (kol ~ ko "king") vs other seals, face area mm2 ==')
A142 = [s['a'] for s in seals if '142' in s['t'] and s['a']]
Aoth = [s['a'] for s in seals if '142' not in s['t'] and s['a']]
print(f"  142 seals n={len(A142)} median {st.median(A142):.0f}; other seals n={len(Aoth)} median {st.median(Aoth):.0f}")
allA = A142 + Aoth; k = len(A142); obs = st.median(A142); null = []
for _ in range(5000):
    random.shuffle(allA); null.append(st.median(allA[:k]))
print(f"  P(median of a random set this large >= observed) = {(1+sum(n>=obs for n in null))/5001:.4f}")
A142alone = [s['a'] for s in seals if s['t'][-2:-1] == ['142'] and s['a']]
print(f"  seals whose name ends in 142 right before the closer: n={len(A142alone)} median {st.median(A142alone) if A142alone else 0:.0f}")

print('\n== C3 comb 400: size, what precedes it, zone ==')
comb = [s for s in seals if s['cl'] == 'comb']
print('  comb-closer seals', len(comb), 'median area', st.median([s['a'] for s in comb if s['a']]))
print('  sign before the comb:', collections.Counter(s['t'][-2] for s in comb).most_common(8))
jc = [s for s in seals if len(s['t']) >= 3 and s['t'][-1] == '400' and s['t'][-2] == '740']
print('  [.. jar comb] seals:', len(jc), 'median area', st.median([s['a'] for s in jc if s['a']]) if jc else '-')

print('\n== C4 house-mates share the sign before the closer? jar closers vs other closers (Mohenjo-daro) ==')
def dep(s):
    m = re.search(r'(-?\d+(\.\d+)?)\s*ft', s); return float(m.group(1)) if m else None
def house_test(pred, label):
    U = []
    for s in seals:
        x = s['x']
        if x['site'] != 'Mohenjo-daro' or x['block-house'] in ('--', '-', '') or len(s['t']) < 3: continue
        if not pred(s) or s['t'][-2] == '000' or dep(x['depth']) is None: continue
        U.append(dict(pre=s['t'][-2], d=dep(x['depth']), hk=(x['area-section'], x['block-house']), ar=x['area-section']))
    def cnt(hk):
        idx = collections.defaultdict(list); c = 0; p = 0
        for i, h in enumerate(hk): idx[h].append(i)
        for m in idx.values():
            for a in range(len(m)):
                for b in range(a+1, len(m)):
                    i, j = m[a], m[b]
                    if abs(U[i]['d'] - U[j]['d']) > 5: continue
                    p += 1; c += U[i]['pre'] == U[j]['pre']
        return c, p
    hk = [u['hk'] for u in U]; o, p = cnt(hk)
    strata = collections.defaultdict(list)
    for i, u in enumerate(U): strata[(u['ar'], int(u['d'] // 3))].append(i)
    null = []
    for _ in range(2000):
        ph = hk[:]
        for idx in strata.values():
            sh = idx[:]; random.shuffle(sh)
            for i, j in zip(idx, sh): ph[i] = hk[j]
        null.append(cnt(ph)[0])
    print(f"  {label:28s} seals {len(U):4d} same-house pairs {p:4d}: share pre-closer sign {o} vs chance {np.mean(null):.1f}  P {(1+sum(n>=o for n in null))/2001:.4f}")
house_test(lambda s: s['t'][-1] == '740', 'closer = jar')
house_test(lambda s: s['cl'] and s['t'][-1] != '740', 'closer = spear/person/comb/carr')
house_test(lambda s: s['t'][-1] == '090' and s['t'][-2] == '740', '[.. jar person] (pre = jar)')

print('\n== C5 counted jar vs closing jar: object types ==')
cnt_t, close_t = collections.Counter(), collections.Counter()
for x in R:
    t = toks(x)
    for i, s in enumerate(t):
        if s != '740': continue
        if i > 0 and re.match(r'03[1-6]', t[i-1]): cnt_t[x['type'].split(':')[0]] += 1
        elif i == len(t) - 1 and i > 0: close_t[x['type'].split(':')[0]] += 1
print('  jar right after full-height strokes (a counted pot):', dict(cnt_t))
print('  jar closing a text after a non-count sign       :', dict(close_t))

print('\n== C6 person 090 (aal: man/servant and to rule) ==')
bare = [s['a'] for s in seals if s['t'][-1] == '090' and s['t'][-2] != '740' and s['a']]
jp = [s['a'] for s in seals if s['t'][-1] == '090' and s['t'][-2] == '740' and s['a']]
jar = [s['a'] for s in seals if s['t'][-1] == '740' and s['a']]
print(f"  [name person] n={len(bare)} median {st.median(bare):.0f} | [name jar person] n={len(jp)} median {st.median(jp):.0f} | [name jar] n={len(jar)} median {st.median(jar):.0f}")
zc2 = collections.Counter(('bare' if s['t'][-2] != '740' else 'jar+', s['z']) for s in seals if s['t'][-1] == '090' and s['z'])
print('  zones:', dict(zc2))
