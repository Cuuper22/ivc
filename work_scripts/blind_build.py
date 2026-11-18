#!/usr/bin/env python3
"""Builds the BLIND test set for the Indus readings: real value table vs three scrambled tables, graded blind by another reader.

WHAT IT DOES (plain words)
  1. Reads work_data/values_master2.csv (each valued sign has an English word, with extra words for inside-a-name / on-an-account-line /
     text-final / opener use). Every sign's full set of words is one "bundle". A scramble moves bundles between signs.
       S1  free shuffle of bundles among ALL valued signs (strict + wide)
       S2  shuffle only inside the same slot class: number signs stay put; opener words go to opener signs; ending words to ending
           signs; crest words to crest signs; measure words to measure signs; other words to other signs
       S3  shuffle only inside the same frequency band (five bands of equal size by how many faces a sign is on)
     Slot class of a sign = what the template parser does with it most often over all 5,679 faces (opener / ending [= ending, relation,
     tail] / crest / measure [= counted thing, plus the measure list MEASURE_KEEP in corpus_build2.py] / other; number = a stroke sign).
     A sign never gets back its own bundle when another bundle is available in its group (random tries are repeated, best one kept).
  2. Draws 60 inscriptions (faces graded "whole" under the real table), stratified by object kind in proportion, by seed.
     Faces whose English comes out identical under all four tables (e.g. a bare number) are left out of the pool: they cannot tell tables apart.
     Two faces with the same sign string are never both drawn.
  3. Builds each drawn inscription four times with corpus_build2.py's own rules (build()) under real, S1, S2, S3: 240 lines.
  4. Writes work_data/blind/blind_set.csv (item, object_kind, english), KEY_do_not_open.csv, README_for_reader.md.
Hard-coded word rules inside corpus_build2.py that name a sign are neutralised in the scrambles so the real words do not leak in:
  the 590-390 'Boxed-cotton' name and the ward-selector words (first/second/third ward). The real table keeps them exactly as in corpus_build2.py.
Run: python3 blind_build.py     (about 10 seconds)"""
import sys, os, csv, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_build2 as cb
from sound_v4_common import d, lex, parse_face

ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/blind'
SEED_S1, SEED_S2, SEED_S3 = 20261201, 20261202, 20261203     # seeds of the three scrambled tables
SEED_DRAW = 20261204                                          # seed of the draw of 60 inscriptions
SEED_ORDER = 20261205                                         # seed of the order of the 240 lines
N_DRAW = 60; MIN_GAP = 8                                      # same inscription's lines are at least MIN_GAP positions apart
STRATA = ['seal', 'tablet', 'tag or sealing', 'pot', 'copper tablet', 'other']
def log(*a): print('[blind_build]', *a, flush=True)

# ---------- original bundles ----------
SLOTS = ('name', 'count', 'final', 'open')
READ = sorted(cb.READ)
ORIG_SHORT = dict(cb.SHORT); ORIG_SW = {k: dict(v) for k, v in cb.SW.items()}
def bundle(s): return (ORIG_SHORT.get(s, ''),) + tuple(ORIG_SW[k].get(s, '') for k in SLOTS)
BUN = {s: bundle(s) for s in READ}
cb.READ.add('X590')       # alias sign used to stop the hard-coded Boxed-cotton rule in scrambles

# ---------- slot class and frequency of each valued sign ----------
log('classifying signs by what the template parser does with them over all faces ...')
roles = collections.defaultdict(collections.Counter); freq = collections.Counter()
for x in d.tok:
    r = parse_face(x, lex)
    for s, ro in zip(x, r['roles']): roles[s][ro] += 1; freq[s] += 1
def slot_class(s):
    if s in cb.CNT: return 'number'
    top = roles[s].most_common(1)[0][0] if roles[s] else 'self'
    if top == 'opener': return 'opener'
    if top in ('ending', 'relation', 'tail'): return 'ending'
    if top == 'crest': return 'crest'
    if top == 'counted' or s in cb.MEASURE_KEEP: return 'measure'
    return 'other'
CLASS = {s: slot_class(s) for s in READ}
order = sorted(READ, key=lambda s: (freq[s], s)); BAND = {}
for i, s in enumerate(order): BAND[s] = min(4, i * 5 // len(order))
log('slot classes:', dict(collections.Counter(CLASS.values())))
log('frequency bands (signs):', dict(collections.Counter(BAND.values())))

def shuffle_group(sg, rng, label):
    """permute bundles among signs sg; repeat random tries, keep the one with the fewest signs that get an identical bundle back"""
    sg = list(sg)
    if len(sg) < 2: return {s: s for s in sg}
    best = None
    for _ in range(3000):
        p = sg[:]; rng.shuffle(p)
        same = sum(BUN[a] == BUN[b] for a, b in zip(sg, p))
        if best is None or same < best[0]: best = (same, p)
        if same == 0: break
    return dict(zip(sg, best[1])), best[0]
def make_table(name, seed, groups):
    rng = random.Random(seed); perm = {}; stuck = 0
    for g in groups:
        r = shuffle_group(g, rng, name)
        if isinstance(r, dict): perm.update(r)
        else: perm.update(r[0]); stuck += r[1]
    for s in READ: perm.setdefault(s, s)
    moved = sum(BUN[s] != BUN[perm[s]] for s in READ)
    log(f'{name}: seed {seed}; {moved} of {len(READ)} signs now carry a different set of words; {stuck} got an identical set back (group had too many look-alike words)')
    return perm
S1 = make_table('S1', SEED_S1, [READ])
S2 = make_table('S2', SEED_S2, [[s for s in READ if CLASS[s] == c] if c != 'number' else [] for c in ('opener', 'ending', 'crest', 'measure', 'other')])
S3 = make_table('S3', SEED_S3, [[s for s in READ if BAND[s] == b] for b in range(5)])
TABLES = {'real': {s: s for s in READ}, 'S1': S1, 'S2': S2, 'S3': S3}

# ---------- apply a table to corpus_build2's dictionaries ----------
_orig_eng = cb.eng; _orig_nt = cb.name_tokens; MODE = {'scr': False}
def _eng(s, slot=None, selector=False):
    return _orig_eng(s, slot, False if MODE['scr'] else selector)      # no fixed ward words in scrambles
def _nt(x, idx, R, kind, slot='name'):
    if MODE['scr']:
        x = list(x)
        for q in range(len(x) - 1):
            if x[q] == '590' and x[q + 1] == '390': x[q] = 'X590'      # no fixed Boxed-cotton in scrambles
    return _orig_nt(x, idx, R, kind, slot)
cb.eng = _eng; cb.name_tokens = _nt
def apply_table(name):
    perm = TABLES[name]; MODE['scr'] = name != 'real'
    cb.SHORT.clear(); cb.SHORT.update(ORIG_SHORT)
    for k in SLOTS: cb.SW[k].clear()
    allp = dict(perm); allp['X590'] = perm['590'] if name != 'real' else '590'
    for s, p in allp.items():
        b = BUN[p]; cb.SHORT[s] = b[0]
        for k, w in zip(SLOTS, b[1:]):
            if w: cb.SW[k][s] = w
def read_face(x, kind):
    r = parse_face(x, lex); return cb.build(x, r, kind)[0]

# ---------- real-table check against the stored corpus ----------
log('checking that the real table reproduces work_data/corpus_english2.csv ...')
stored = {}
with open(f'{ROOT}/work_data/corpus_english2.csv', newline='') as f:
    for r in csv.DictReader(f): stored[r['face_id']] = r
apply_table('real'); pool = []; bad = 0
KINDMAP = {'seal': 'seal', 'mtab': 'tablet', 'tag': 'tag or sealing', 'pot': 'pot', 'ctab': 'copper tablet'}
n = 0
for fid, x, flg, kind, site in zip(d.id, d.tok, d.flg, d.kind, d.site):
    n += 1
    if cb.grade(x, flg, cb.READ) != 'whole': continue
    e = read_face(x, kind)
    if fid in stored and stored[fid]['english'] != e: bad += 1
    pool.append((fid, x, kind, e))
    if n % 1000 == 0: log(f'  ... {n} of {len(d)} faces checked')
log(f'whole faces under the real table: {len(pool)}; lines that differ from the stored corpus: {bad}')
if bad: log('WARNING: real-table lines differ from corpus_english2.csv; check before using'); 

# ---------- English of every whole face under all four tables ----------
log('building every whole face under all four tables to find faces that cannot tell tables apart ...')
ENG = {}
for name in TABLES:
    apply_table(name)
    for fid, x, kind, e in pool: ENG[(fid, name)] = read_face(x, kind)
    log(f'  table {name} done')
elig = [p for p in pool if len({ENG[(p[0], t)] for t in TABLES}) > 1]
log(f'faces whose English is identical in all four tables (left out): {len(pool) - len(elig)}; eligible pool: {len(elig)}')

# ---------- stratified draw ----------
def stratum(kind): return KINDMAP.get(kind, 'other')
bystr = collections.defaultdict(list)
for p in elig: bystr[stratum(p[2])].append(p)
tot = len(elig); raw = {k: N_DRAW * len(bystr[k]) / tot for k in STRATA}
alloc = {k: int(raw[k]) for k in STRATA}
for k in sorted(STRATA, key=lambda k: -(raw[k] - alloc[k]))[:N_DRAW - sum(alloc.values())]: alloc[k] += 1
log('pool per object kind:', {k: len(bystr[k]) for k in STRATA}); log('draw per object kind (largest-remainder share of 60):', alloc)
rng = random.Random(SEED_DRAW); drawn = []; seen = set()
for k in STRATA:
    cand = bystr[k][:]; rng.shuffle(cand); got = 0
    for p in cand:
        s = '-'.join(p[1])
        if s in seen: continue
        seen.add(s); drawn.append((k, p)); got += 1
        if got == alloc[k]: break
    log(f'  drew {got} {k} inscriptions')
assert len(drawn) == N_DRAW, len(drawn)

# ---------- 240 lines in a seeded order, same inscription never close together ----------
lines = [(i, k, p, t) for i, (k, p) in enumerate(drawn) for t in TABLES]
rng = random.Random(SEED_ORDER)
def ok(seq): 
    last = {}
    for pos, l in enumerate(seq):
        if l[0] in last and pos - last[l[0]] < MIN_GAP: return False
        last[l[0]] = pos
    return True
def violations(seq):
    bad = []; last = {}
    for pos, l in enumerate(seq):
        if l[0] in last and pos - last[l[0]] < MIN_GAP: bad.append(pos)
        last[l[0]] = pos
    return bad
seq = lines[:]; rng.shuffle(seq); swaps = 0
while violations(seq):                      # repair: swap a too-close line with a random other place, keep the swap if violations do not rise
    v = violations(seq); pos = rng.choice(v); other = rng.randrange(len(seq)); before = len(v)
    seq[pos], seq[other] = seq[other], seq[pos]; swaps += 1
    if len(violations(seq)) > before: seq[pos], seq[other] = seq[other], seq[pos]
    if swaps > 200000: raise SystemExit('could not space the lines')
assert not violations(seq)
log(f'order built with {swaps} repair swaps; every inscription\'s four lines are at least {MIN_GAP} places apart')

os.makedirs(OUT, exist_ok=True)
with open(f'{OUT}/blind_set.csv', 'w', newline='') as f, open(f'{OUT}/KEY_do_not_open.csv', 'w', newline='') as g:
    w = csv.writer(f); kw = csv.writer(g)
    w.writerow(['item', 'object_kind', 'english']); kw.writerow(['item', 'object id', 'face id', 'object kind', 'signs', 'which table'])
    for item, (i, k, p, t) in enumerate(seq, 1):
        w.writerow([item, k, ENG[(p[0], t)]])
        kw.writerow([item, p[0].split('.')[0], p[0], k, '-'.join(p[1]), t])
same_as_real = sum(ENG[(p[0], t)] == ENG[(p[0], 'real')] for k, p in drawn for t in ('S1', 'S2', 'S3'))
log(f'wrote {len(seq)} lines. Scrambled lines that came out identical to the real line of the same inscription: {same_as_real} of {3 * N_DRAW}')

with open(f'{OUT}/README_for_reader.md', 'w') as f:
    f.write("""# Reading task

Open only `blind_set.csv`. It has 240 lines, one per row: `item`, `object_kind`, `english`.

Each line is a proposed English reading of a short text on an ancient object of the named kind:
a personal seal, a ration or account tablet, a goods tag or sealing, a pot, a copper tablet, or another small object.

Grade each line:

- **sense**: it reads as something that kind of object would plausibly say: a name with house and title, an amount of goods, an ownership or office label.
- **odd**: parts make sense, something is off.
- **nonsense**: it does not read as anything that kind of object would say.

Grade every line on its own. Do not compare lines with each other.

Do not open any other file in this folder or in the repository.

Write your grades to `grades.csv` in this folder, with columns `item`, `grade`, `reason`: one row per item (240 rows), `grade` being exactly `sense`, `odd` or `nonsense`, and `reason` one short phrase.
""")
log('wrote README_for_reader.md. Done. Seeds: S1', SEED_S1, 'S2', SEED_S2, 'S3', SEED_S3, 'draw', SEED_DRAW, 'order', SEED_ORDER)
