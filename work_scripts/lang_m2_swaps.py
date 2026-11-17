#!/usr/bin/env python3
"""lang_m2 step 7: SOUND-ALIKE SIGN PAIRS with the blind pictures (rule unchanged from lang_m_swaps.py; pictures from
work_data/lang_m2/signs.csv, both variants A = 3of3, B = 3of3 + 2of3; homonym-aware dictionaries from lang_m2_lexicons.py).
Original description:

1. Swap pairs found by rule, both catalogues: two distinct texts of the same length (3+ signs) that are identical except at one
   position; the two signs at that position are a swap.  Lost / unmapped signs are skipped.  A pair is kept when it swaps in at least
   2 different frames (frame = the rest of the text), counting the first catalogue (Lipi) and the second (Mahadevan 1977, read through the
   crosswalk) separately.
2. Pairs where both signs have a picture (work_data/lang_m/pictures.csv) and the two pictures share no noun (same thing drawn two ways
   is a drawing variant, not a sound swap).
3. For each dictionary / family and each sound distance: the pair is SOUND-ALIKE when some word for picture A and some word for picture
   B (different entries) are within the distance.  Score = number of sound-alike swap pairs.
   CONTROL R (2,000 runs): the same number of random pairs of pictured signs (each sign used 3+ times, no shared noun).
   CONTROL S (2,000 runs): the pictures dealt at random among the signs of the swap pairs (a dealt pair that shares a noun gets its
   second sign re-drawn from the same signs).
Output: work_data/lang_m/swap_pairs.csv, work_data/lang_m/swap_grid.csv
"""
import sys, os, csv, collections, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m2_common import *
import v2_common as v
rng = np.random.default_rng(20261120); N = 2000
def log(*a): print(f'[lang_m2_swaps {time.strftime("%H:%M:%S")}]', *a, flush=True)

def ok(s): return s not in ('000', 'ALT') and not s.startswith('X')
cats = {'Lipi': set(tuple(x) for x in v.d.tok), 'Mahadevan': set(tuple(x) for x in v.M.tok)}
frames = collections.defaultdict(set); occ = collections.Counter()
for cat, texts in cats.items():
    groups = collections.defaultdict(set)
    for x in texts:
        for s in x: occ[s] += 1
        if len(x) < 3 or not all(ok(s) for s in x): continue
        for i in range(len(x)):
            groups[(x[:i], x[i + 1:])].add(x[i])
    for key, ss in groups.items():
        for a, b in itertools.combinations(sorted(ss), 2): frames[(a, b)].add((cat, key))
pairs = {p: f for p, f in frames.items() if len(f) >= 2}
log(f'{len(frames)} sign pairs swap at least once; {len(pairs)} swap in 2+ frames')
SG = list(csv.DictReader(open(f'{OUT}/signs.csv', encoding='utf-8')))
NOUNS_ALL = blind_nouns()
LEXS = {n: Lex(n, NOUNS_ALL, []) for ns in FAMILIES.values() for n in ns}
log('dictionaries loaded')
rows = []; pair_rows = []
for VAR, LV in VARIANTS.items():
  P = {r['sign']: r['nouns'].split(';') for r in SG if r['level'] in LV and r['nouns']}
  pic_pairs = [(a, b) for (a, b) in pairs if a in P and b in P and not set(P[a]) & set(P[b])]
  same_pic = [(a, b) for (a, b) in pairs if a in P and b in P and set(P[a]) & set(P[b])]
  log(f'swap pairs with both signs pictured: {len(pic_pairs) + len(same_pic)}; same thing drawn two ways (left out): {len(same_pic)}; '
      f'different things (tested): {len(pic_pairs)}')
  for (a, b), fr in sorted(pairs.items(), key=lambda kv: -len(kv[1])):
      if a in P and b in P:
          pair_rows.append(dict(variant=VAR, a=a, b=b, frames=len(fr), lipi_frames=sum(c == 'Lipi' for c, _ in fr),
                                mahadevan_frames=sum(c == 'Mahadevan' for c, _ in fr), nouns_a='|'.join(P[a]), nouns_b='|'.join(P[b]),
                                tested=(a, b) in pic_pairs))

  pool_signs = [s for s in P if occ[s] >= 3]
  NOUNS = sorted({n for s in P for n in P[s]}); NI = {n: i for i, n in enumerate(NOUNS)}

  def nn_matrix(L, d):
      M = np.zeros((len(NOUNS), len(NOUNS)), dtype=bool)
      for a in NOUNS:
          for pw in L.is_pic.get(a, []):
              for q in L.near_form(L.nf[pw], d):
                  if L.eid[q] == L.eid[pw]: continue
                  for b in NOUNS:
                      if b != a and q in L.pic_flag[b]: M[NI[a], NI[b]] = M[NI[b], NI[a]] = True
      return M

  def sa(M, a, b): return any(M[NI[x], NI[y]] for x in P[a] for y in P[b])
  swap_signs = sorted({s for p in pic_pairs for s in p})
  rand_pairs = []
  for _ in range(N):
      out = []
      while len(out) < len(pic_pairs):
          a, b = rng.choice(pool_signs, 2, replace=False)
          if not set(P[a]) & set(P[b]): out.append((a, b))
      rand_pairs.append(out)
  shuf = []
  for _ in range(N):
      perm = dict(zip(swap_signs, rng.permutation(swap_signs)))
      out = []
      for a, b in pic_pairs:
          x, y = perm[a], perm[b]
          while set(P[x]) & set(P[y]): y = swap_signs[rng.integers(len(swap_signs))]   # local repair when a dealt pair shares a noun
          out.append((x, y))
      shuf.append(out)

  mats = {}
  for fam, names in FAMILIES.items():
      for n in names:
          mats[n] = {d: nn_matrix(LEXS[n], d) for d in DISTS}
  log(f'{VAR}: noun-noun sound-alike matrices built')
  units = [(n, [n]) for ns in FAMILIES.values() for n in ns] + [(f'FAMILY {f}', ns) for f, ns in FAMILIES.items()]
  for unit, names in units:
      for d in DISTS:
          M = np.logical_or.reduce([mats[n][d] for n in names])
          obs = sum(sa(M, a, b) for a, b in pic_pairs)
          hit = [f'{a}-{b}' for a, b in pic_pairs if sa(M, a, b)]
          r = np.array([sum(sa(M, a, b) for a, b in ps) for ps in rand_pairs])
          s_ = np.array([sum(sa(M, a, b) for a, b in ps) for ps in shuf])
          rows.append(dict(variant=VAR, unit=unit, dist=d, pairs=len(pic_pairs), soundalike=obs, R_mean=round(r.mean(), 2), R_sd=round(r.std(), 2),
                           R_P=round((1 + (r >= obs).sum()) / (N + 1), 4), S_mean=round(s_.mean(), 2), S_sd=round(s_.std(), 2),
                           S_P=round((1 + (s_ >= obs).sum()) / (N + 1), 4), hit_pairs=' '.join(hit)))
      log(f'{VAR} {unit}: ' + '  '.join(f'{x["dist"]} {x["soundalike"]}/{x["pairs"]} (R {x["R_mean"]} P{x["R_P"]}; S {x["S_mean"]} P{x["S_P"]})' for x in rows[-3:]))

with open(f'{OUT}/swap_grid.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(f'{OUT}/swap_pairs.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(pair_rows[0])); w.writeheader(); w.writerows(pair_rows)
log('written swap_pairs.csv, swap_grid.csv')
