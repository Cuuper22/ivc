#!/usr/bin/env python3
"""Builds the DECOY test list for the Indus word list (builder only; the tester never runs or reads this).

WHAT IT DOES (plain words)
  1. Reads the strict words from work_data/values_master3.csv. Drops number / stroke signs (sign in gloss2.CNT), the jar (740),
     the man (090) and the joiner (060): those are fixed by structure alone, not content words.
  2. Gives each remaining sign a JOB CLASS with the same rule as work_scripts/blind2_build.py (opener / ending / crest / measure / other;
     the parser's most common role for the sign over all Lipi faces; measure also holds the MEASURE_KEEP signs), and a FREQUENCY
     (number of Lipi faces carrying it). Only signs with at least MIN_FACES faces can be drawn.
  3. Frequency bands = terciles of face count over the drawable signs. Draws 60 signs: proportional over class x band cells
     (largest remainder), at most one sign per word (variant signs sharing a word cannot both be drawn).
  4. Picks 30 of the 60 as decoys (balanced by class, seeded). A decoy sign gets the word of a DIFFERENT sign of the SAME class
     and the same frequency band (next band over only if the band has no choice). The donor must not be one of the 30 kept-real signs,
     the word must differ from the sign's own word, and no word (sound or English head) may appear twice in the 60.
  5. Writes work_data/decoy/test_list.csv (item, sign, sound, english, dedr), KEY_do_not_open.csv.
Run: python3 decoy_build.py"""
import sys, os, csv, random, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from sound_v3_common import d, lex, parse_face     # corpus only (this loader never reads the value lists)
from gloss2 import CNT

ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/decoy'
SEED_DRAW, SEED_HALF, SEED_MATCH, SEED_ORDER = 20261301, 20261302, 20261303, 20261304
N_TOTAL, N_DECOY, MIN_FACES = 60, 30, 15
MEASURE_KEEP = {'705', '706', '700', '320', '575', '540', '171', '711', '061', '480', '817', '820', '861', '176', '175'}
NOT_CONTENT = {'740', '090', '060'}
CLS = ('opener', 'ending', 'crest', 'measure', 'other')
def log(*a): print('[decoy_build]', *a, flush=True)

V = pd.read_csv(f'{ROOT}/work_data/values_master3.csv', dtype=str).fillna('')
S = V[V.status == 'strict']
log('strict rows in values_master3.csv:', len(S))
log('classifying signs by the template parser over all faces ...')
roles = collections.defaultdict(collections.Counter); fc = collections.Counter()
for x in d.tok:
    r = parse_face(x, lex)
    for s, ro in zip(x, r['roles']): roles[s][ro] += 1
    for s in set(x): fc[s] += 1
def slot_class(s):
    top = roles[s].most_common(1)[0][0] if roles[s] else 'self'
    if top == 'opener': return 'opener'
    if top in ('ending', 'relation', 'tail'): return 'ending'
    if top == 'crest': return 'crest'
    if top == 'counted' or s in MEASURE_KEEP: return 'measure'
    return 'other'
def clean_en(e):
    # the tester sees only the plain gloss: notes in brackets or after a colon name other signs, variants and files, and would show which are real
    e = re.sub(r'\([^)]*\)', '', e).split(':')[0]
    return re.sub(r'\s+', ' ', e).strip(' ;,')
def clean_snd(w): return re.sub(r'\?', '', w).strip('-').strip()
def skey(w): return re.sub(r"[?\-\s]", '', re.sub(r'\(.*?\)', '', w)).lower()
def ekey(e): return re.split(r'[(;,:]', e)[0].strip().lower()

rows = {}
for r in S.itertuples():
    if r.sign in CNT or r.sign in NOT_CONTENT: continue
    rows[r.sign] = dict(sign=r.sign, sound=clean_snd(r.sound), english=clean_en(r.english), raw=f'{r.sound} / {r.english}', dedr=r.dedr, cls=slot_class(r.sign), faces=fc[r.sign],
                        sk=skey(r.sound), ek=ekey(r.english))
log('content-word strict signs:', len(rows), '| by class:', dict(collections.Counter(v['cls'] for v in rows.values())))
pool = {s: v for s, v in rows.items() if v['faces'] >= MIN_FACES}
fs = sorted(v['faces'] for v in pool.values())
t1, t2 = fs[len(fs) // 3], fs[2 * len(fs) // 3]
for v in pool.values(): v['band'] = 0 if v['faces'] < t1 else 1 if v['faces'] < t2 else 2
for v in rows.values(): v['band'] = 0 if v['faces'] < t1 else 1 if v['faces'] < t2 else 2   # donors (any strict content sign) get a band too
log(f'drawable signs (>= {MIN_FACES} faces): {len(pool)}; band cut points {t1}, {t2}')
cells = collections.defaultdict(list)
for s, v in pool.items(): cells[(v['cls'], v['band'])].append(s)
log('pool per class x band:', {f'{c}/{b}': len(x) for (c, b), x in sorted(cells.items())})

# ---- 1. proportional draw over class x band, one sign per word ----
rng = random.Random(SEED_DRAW)
tot = len(pool); quota = {k: len(v) * N_TOTAL / tot for k, v in cells.items()}
alloc = {k: int(q) for k, q in quota.items()}
rest = N_TOTAL - sum(alloc.values())
for k in sorted(quota, key=lambda k: (-(quota[k] - alloc[k]), rng.random()))[:rest]: alloc[k] += 1
used_s, used_e = set(), set(); drawn = []
for k in sorted(cells):
    c = cells[k][:]; rng.shuffle(c); got = 0
    for s in c:
        if got == alloc[k]: break
        v = pool[s]
        if v['sk'] in used_s or v['ek'] in used_e: continue
        used_s.add(v['sk']); used_e.add(v['ek']); drawn.append(s); got += 1
    if got < alloc[k]: log(f'  cell {k}: wanted {alloc[k]}, only {got} (words shared among variants)')
# top up from any cell if some cell fell short
while len(drawn) < N_TOTAL:
    left = [s for s in pool if s not in drawn and pool[s]['sk'] not in used_s and pool[s]['ek'] not in used_e]
    s = rng.choice(sorted(left)); drawn.append(s); used_s.add(pool[s]['sk']); used_e.add(pool[s]['ek'])
log('drawn:', len(drawn), '| per class:', dict(collections.Counter(pool[s]['cls'] for s in drawn)),
    '| per band:', dict(collections.Counter(pool[s]['band'] for s in drawn)))

# ---- 2+3. pick the 30 decoys (balanced by class) and match each to a donor word (same class, same band; adjacent band only if needed).
# If a seeded split leaves some decoy with no possible donor (small classes), the next seed (SEED_HALF + k) is tried; k is printed.
bycls = collections.defaultdict(list)
for s in drawn: bycls[pool[s]['cls']].append(s)
def split(seed):
    r = random.Random(seed); dec = set(); odd = []
    for c in CLS:
        m = bycls[c][:]; r.shuffle(m); h = len(m) // 2
        dec |= set(m[:h])
        if len(m) % 2: odd.append(m[h])        # odd one out of each class: chosen at random so the total is exactly N_DECOY
    r.shuffle(odd); dec |= set(odd[:N_DECOY - len(dec)])
    return dec
def try_match(decoy, seed):
    keep = [s for s in drawn if s not in decoy]
    keep_sk = {pool[s]['sk'] for s in keep}; keep_ek = {pool[s]['ek'] for s in keep}
    donors_all = [s for s, v in rows.items() if s not in keep and v['sk'] not in keep_sk and v['ek'] not in keep_ek]
    def options(s, widen):
        v = pool[s]
        return [t for t in donors_all if t != s and rows[t]['cls'] == v['cls'] and abs(rows[t]['band'] - v['band']) <= widen
                and rows[t]['sk'] != v['sk'] and rows[t]['ek'] != v['ek']]
    for widen in (0, 1, 2):
        r = random.Random(seed); dl = sorted(decoy)
        order = sorted(dl, key=lambda s: len(options(s, widen)))
        opts = {s: sorted(options(s, widen)) for s in order}
        for s in order: r.shuffle(opts[s])
        asg = {}
        def bt(i, us, ue):
            if i == len(order): return True
            s = order[i]
            for t in opts[s]:
                sk, ek = rows[t]['sk'], rows[t]['ek']
                if sk in us or ek in ue: continue
                asg[s] = t
                if bt(i + 1, us | {sk}, ue | {ek}): return True
                del asg[s]
            return False
        if bt(0, set(keep_sk), set(keep_ek)): return keep, asg, widen
    return None
res = None
for k in range(500):
    decoy = split(SEED_HALF + k)
    res = try_match(decoy, SEED_MATCH + k)
    if res: break
assert res, 'no split with a full donor matching found'
keep, asg, widen = res
log(f'split attempt {k} (seeds half {SEED_HALF + k}, match {SEED_MATCH + k}): all {len(asg)} decoys matched with frequency band distance <= {widen}')
log('decoys per class:', dict(collections.Counter(pool[s]['cls'] for s in decoy)), '| real kept per class:', dict(collections.Counter(pool[s]['cls'] for s in keep)))
for s in sorted(decoy):
    if abs(rows[asg[s]]['band'] - pool[s]['band']) > 0: log('  decoy', s, 'donor', asg[s], 'is one band over')

# ---- 4. write ----
final = {}
for s in sorted(keep):
    v = pool[s]; final[s] = dict(sign=s, sound=v['sound'], english=v['english'], dedr=v['dedr'], kind='real', true=v['raw'], src='')
for s in sorted(decoy):
    v = pool[s]; t = rows[asg[s]]
    final[s] = dict(sign=s, sound=t['sound'], english=t['english'], dedr=t['dedr'], kind='decoy', true=v['raw'],
                    src=f"word of sign {asg[s]} (class {t['cls']}, band {t['band']}, {t['faces']} faces)")
sk_list = [skey(f['sound']) for f in final.values()]; ek_list = [ekey(f['english']) for f in final.values()]
assert len(set(sk_list)) == len(sk_list) and len(set(ek_list)) == len(ek_list), 'a word appears twice'
assert all(f['kind'] == 'real' or skey(f['sound']) != pool[f['sign']]['sk'] for f in final.values()), 'a sign got its own word'
order = sorted(final); random.Random(SEED_ORDER).shuffle(order)
os.makedirs(OUT, exist_ok=True)
with open(f'{OUT}/test_list.csv', 'w', newline='') as f, open(f'{OUT}/KEY_do_not_open.csv', 'w', newline='') as g:
    w = csv.writer(f); kw = csv.writer(g)
    w.writerow(['item', 'sign', 'sound', 'english', 'dedr'])
    kw.writerow(['item', 'sign', 'real_or_decoy', 'true_word', 'decoy_word_came_from', 'job_class', 'faces', 'freq_band'])
    for i, s in enumerate(order, 1):
        x = final[s]; v = pool[s]
        w.writerow([i, s, x['sound'], x['english'], x['dedr']])
        kw.writerow([i, s, x['kind'], x['true'], x['src'], v['cls'], v['faces'], v['band']])
log('wrote test_list.csv and KEY_do_not_open.csv in', OUT)
log('Seeds: draw', SEED_DRAW, 'half', SEED_HALF, 'match', SEED_MATCH, 'order', SEED_ORDER, '| split attempt k =', k, '(half seed', SEED_HALF + k, ', match seed', SEED_MATCH + k, ')')
