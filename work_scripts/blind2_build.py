#!/usr/bin/env python3
"""Builds the SIDE-BY-SIDE (forced choice) test for the Indus readings.

WHAT IT DOES (plain words)
  Value table: work_data/values_master2.csv through corpus_build2.py (no corpus_build3.py exists; values_master4.csv has a different
  column layout and no builder reads it, so it is not used).
  1. Makes the real table and three NEW scrambles of the word bundles (same bundle idea as blind_build.py):
       S1  free shuffle among all valued signs;  S2  shuffle inside the same job class (opener / ending / crest / measure / other; numbers stay);
       S2b a second, independent shuffle inside the same job classes.
  2. English of every inscription that reads whole, under all four tables, with the NAME renderer of render_names.py (same layout rules
     in all four tables). Inscriptions whose four versions are all identical are left out.
  3. Draws 120 by seed: 50 seals, 50 tablets, 20 from tags / pots / copper tablets / the rest together; no two with the same sign string.
  4. For each, puts the four versions in a seeded random order (options a-d), rows in a seeded random order.
  Writes work_data/blind2/choice_set.csv, KEY_do_not_open.csv, README_for_reader.md.
Run: python3 blind2_build.py [--old-names]   (--old-names uses the old hyphen-chain renderer; default is the new name renderer)"""
import sys, os, csv, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_build2 as cb
import render_names as rn
from sound_v4_common import d, lex, parse_face

ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/blind2'
SEED_S1, SEED_S2, SEED_S2B = 20261211, 20261212, 20261213
SEED_DRAW, SEED_ROWS, SEED_OPT = 20261214, 20261215, 20261216
N_SEAL, N_TAB, N_REST = 50, 50, 20
NEW_NAMES = '--old-names' not in sys.argv
def log(*a): print('[blind2_build]', *a, flush=True)
if NEW_NAMES: rn.use_new(cb)
log('name renderer:', 'NEW (render_names.py)' if NEW_NAMES else 'OLD hyphen chains')

SLOTS = ('name', 'count', 'final', 'open')
READ = sorted(cb.READ)
ORIG_SHORT = dict(cb.SHORT); ORIG_SW = {k: dict(v) for k, v in cb.SW.items()}
def bundle(s): return (ORIG_SHORT.get(s, ''),) + tuple(ORIG_SW[k].get(s, '') for k in SLOTS)
BUN = {s: bundle(s) for s in READ}
cb.READ.add('X590')

log('classifying signs by what the template parser does with them over all faces ...')
roles = collections.defaultdict(collections.Counter)
for x in d.tok:
    r = parse_face(x, lex)
    for s, ro in zip(x, r['roles']): roles[s][ro] += 1
def slot_class(s):
    if s in cb.CNT: return 'number'
    top = roles[s].most_common(1)[0][0] if roles[s] else 'self'
    if top == 'opener': return 'opener'
    if top in ('ending', 'relation', 'tail'): return 'ending'
    if top == 'crest': return 'crest'
    if top == 'counted' or s in cb.MEASURE_KEEP: return 'measure'
    return 'other'
CLASS = {s: slot_class(s) for s in READ}
log('slot classes:', dict(collections.Counter(CLASS.values())))

def shuffle_group(sg, rng):
    sg = list(sg)
    if len(sg) < 2: return {s: s for s in sg}, 0
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
        r, st = shuffle_group(g, rng); perm.update(r); stuck += st
    for s in READ: perm.setdefault(s, s)
    moved = sum(BUN[s] != BUN[perm[s]] for s in READ)
    log(f'{name}: seed {seed}; {moved} of {len(READ)} signs carry a different set of words; {stuck} got an identical set back')
    return perm
CLS = ('opener', 'ending', 'crest', 'measure', 'other')
def jobgroups(): return [[s for s in READ if CLASS[s] == c] for c in CLS]
TABLES = {'real': {s: s for s in READ},
          'S1': make_table('S1', SEED_S1, [READ]),
          'S2': make_table('S2', SEED_S2, jobgroups()),
          'S2b': make_table('S2b', SEED_S2B, jobgroups())}
same_perm = sum(TABLES['S2'][s] == TABLES['S2b'][s] for s in READ)
log(f'S2 and S2b give the same bundle to {same_perm} of {len(READ)} signs')

_orig_eng = cb.eng; _orig_nt = cb.name_tokens; MODE = {'scr': False}
def _eng(s, slot=None, selector=False): return _orig_eng(s, slot, False if MODE['scr'] else selector)
def _nt(x, idx, R, kind, slot='name'):
    if MODE['scr']:
        x = list(x)
        for q in range(len(x) - 1):
            if x[q] == '590' and x[q + 1] == '390': x[q] = 'X590'
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
    r = parse_face(x, lex); e = cb.build(x, r, kind)[0]
    return rn.finish(e) if NEW_NAMES else e

log('checking the OLD renderer reproduces work_data/corpus_english2.csv (sanity of the builder) ...')
stored = {}
with open(f'{ROOT}/work_data/corpus_english2.csv', newline='') as f:
    for r in csv.DictReader(f): stored[r['face_id']] = r['english']
rn.use_old(cb); apply_table('real'); bad = 0; chk = 0
for fid, x, kind in zip(d.id, d.tok, d.kind):
    r = parse_face(x, lex); e = cb.build(x, r, kind)[0]; chk += 1
    if fid in stored and stored[fid] != e: bad += 1
log(f'old renderer: {chk} faces re-read, {bad} differ from the stored corpus')
if NEW_NAMES: rn.use_new(cb)

log('finding faces that read whole ...')
KINDMAP = {'seal': 'seal', 'mtab': 'tablet', 'tag': 'tag or sealing', 'pot': 'pot', 'ctab': 'copper tablet'}
pool = [(fid, x, KINDMAP.get(kind, 'other'), kind) for fid, x, flg, kind in zip(d.id, d.tok, d.flg, d.kind) if cb.grade(x, flg, cb.READ) == 'whole']
log(f'faces that read whole: {len(pool)}')
ENG = {}
for name in TABLES:
    apply_table(name)
    for i, (fid, x, ok, kind) in enumerate(pool):
        ENG[(fid, name)] = read_face(x, kind)
    log(f'  table {name} built')
elig = [p for p in pool if len({ENG[(p[0], t)] for t in TABLES}) > 1]
log(f'all-four-identical (left out): {len(pool) - len(elig)}; eligible: {len(elig)}')
for p in elig: pass

def group(k): return 'seal' if k == 'seal' else 'tablet' if k == 'tablet' else 'rest'
by = collections.defaultdict(list)
for p in elig: by[group(p[2])].append(p)
log('eligible per group:', {k: len(v) for k, v in by.items()})
rng = random.Random(SEED_DRAW); drawn = []; seen = set()
for g, n in (('seal', N_SEAL), ('tablet', N_TAB), ('rest', N_REST)):
    cand = by[g][:]; rng.shuffle(cand); got = 0
    for p in cand:
        s = '-'.join(p[1])
        if s in seen: continue
        seen.add(s); drawn.append(p); got += 1
        if got == n: break
    log(f'  drew {got} for {g} (wanted {n})')
    assert got == n
log('drawn per object kind:', dict(collections.Counter(p[2] for p in drawn)))

rows = drawn[:]; random.Random(SEED_ROWS).shuffle(rows)
orng = random.Random(SEED_OPT); LET = 'abcd'
os.makedirs(OUT, exist_ok=True)
tie_real = collections.Counter()
with open(f'{OUT}/choice_set.csv', 'w', newline='') as f, open(f'{OUT}/KEY_do_not_open.csv', 'w', newline='') as g:
    w = csv.writer(f); kw = csv.writer(g)
    w.writerow(['item', 'object_kind', 'option_a', 'option_b', 'option_c', 'option_d'])
    kw.writerow(['item', 'object id', 'face id', 'object kind', 'signs', 'real_option', 'S1_option', 'S2_option', 'S2b_option', 'options_identical_to_real'])
    for item, p in enumerate(rows, 1):
        order = list(TABLES); orng.shuffle(order); pos = {t: LET[i] for i, t in enumerate(order)}
        txt = {t: ENG[(p[0], t)] for t in TABLES}
        w.writerow([item, p[2]] + [txt[t] for t in order])
        same = ''.join(sorted(pos[t] for t in TABLES if t != 'real' and txt[t] == txt['real']))
        tie_real[len(same)] += 1
        kw.writerow([item, p[0].split('.')[0], p[0], p[2], '-'.join(p[1]), pos['real'], pos['S1'], pos['S2'], pos['S2b'], same])
log('items by number of scrambles identical to the real line (0,1,2,3):', dict(tie_real))
with open(f'{OUT}/README_for_reader.md', 'w') as f:
    f.write("""# Side-by-side reading task

Open only `choice_set.csv`. It has 120 rows. Each row gives four proposed English readings (option_a to option_d) of ONE short text on an ancient object of the kind named in `object_kind` (a personal seal, a ration or account tablet, a goods tag or sealing, a pot, a copper tablet, or another small object).

Exactly one of the four comes from a real word list; the other three come from scrambled word lists. Pick the one that reads most like something that kind of object would actually say: a name with house and title, an amount of goods, an office or ownership label. Also mark the one that reads worst.

If two options are identical, pick either.

Do not open any other file in this folder or in the repository.

Write your grades to the grades file named in your task message, with columns `item`, `best`, `worst`, `reason`: one row per item (120 rows), `best` and `worst` each being one letter, a, b, c or d, and `reason` one short phrase.
""")
log('wrote choice_set.csv, KEY_do_not_open.csv, README_for_reader.md in', OUT)
log('Seeds: S1', SEED_S1, 'S2', SEED_S2, 'S2b', SEED_S2B, 'draw', SEED_DRAW, 'row order', SEED_ROWS, 'option order', SEED_OPT)
