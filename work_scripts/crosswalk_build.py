#!/usr/bin/env python3
"""Turn the EM text matches (crosswalk_em.py) into work_data/lipi_mahadevan_crosswalk.csv.

One row per (Lipi sign, Mahadevan sign) pair with support: positions in text pairs matched at posterior >= 0.5,
distinct Lipi texts, objects, share of the Lipi sign's matched positions, whether the seedless run found the same
partner, how the pair was found. Also writes work_data/crosswalk_text_pairs.csv (each matched Lipi text with its
Mahadevan partner, for audit and for the parser port).
"""
import sys, pickle, collections, csv
import numpy as np
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from mah_common import *
from crosswalk_em import SEEDS, GROUP

W = '/home/claude/ivc/work_data'


def pairs_from(o, thr=0.5):
    """list of (group, lipi tuple, mah tuple, posterior)"""
    out = []
    for k, P in o['P'].items():
        A, B = o['pre'][k]
        ia, ib = np.nonzero(P >= thr)
        for x, y in zip(ia, ib): out.append((k[0], A[x], B[y], float(P[x, y])))
    return out


def main():
    o = pickle.load(open(f'{W}/crosswalk_em_raw.pkl', 'rb'))
    ns = pickle.load(open(f'{W}/crosswalk_em_raw_noseed.pkl', 'rb'))
    lt, mt = o['lt'], o['mt']
    pr = pairs_from(o)
    prn = pairs_from(ns)
    # per pair support
    pos = collections.Counter(); texts = collections.defaultdict(set); objs = collections.Counter(); wt = collections.Counter()
    for g, a, b, p in pr:
        nobj = len(lt[(g, a)])
        for x, y in zip(a, b):
            if x is None or y is None: continue
            pos[(x, y)] += 1; texts[(x, y)].add((g, a)); objs[(x, y)] += nobj; wt[(x, y)] += p
    posn = collections.Counter()
    for g, a, b, p in prn:
        for x, y in zip(a, b):
            if x is None or y is None: continue
            posn[(x, y)] += 1
    byl = collections.defaultdict(list)
    for (x, y), c in pos.items(): byl[x].append((c, y))
    # total Lipi occurrences over all rows (any text)
    l = load_lipi(); occ = collections.Counter(t for x in l.tok for t in x)
    sh = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str); shape = dict(zip(sh.lipi_wells_number, sh.shape_description))
    mocc = collections.Counter(); mm = load_mah()
    for t in mm.toks:
        for x in t: mocc[x] += 1
    rows = []
    for x, lst in byl.items():
        lst.sort(reverse=True); tot = sum(c for c, _ in lst)
        for rank, (c, y) in enumerate(lst):
            if c < 2 and not (x in SEEDS and SEEDS[x] == y): continue
            share = c / tot
            if rank > 0 and share < 0.1: continue
            if x in SEEDS and SEEDS[x] == y: how = 'known match (given); '
            else: how = ''
            how += 'whole-text alignment'
            if posn[(x, y)] >= 2: how += '; also found with no seeds'
            rows.append(dict(lipi=x, mahadevan=y, how_found=how, rank_for_lipi_sign=rank + 1, text_positions=c,
                             distinct_lipi_texts=len(texts[(x, y)]), objects=objs[(x, y)], share_of_lipi_sign=round(share, 3),
                             positions_in_seedless_run=posn[(x, y)], lipi_occurrences=occ[x], mahadevan_occurrences=mocc[y],
                             lipi_shape=shape.get(x, '')))
    df = pd.DataFrame(rows).sort_values(['lipi', 'rank_for_lipi_sign'])
    df.to_csv(f'{W}/lipi_mahadevan_crosswalk.csv', index=False)
    # text pairs
    with open(f'{W}/crosswalk_text_pairs.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['group', 'lipi_text', 'mahadevan_text', 'posterior', 'lipi_rows', 'mahadevan_rows'])
        for g, a, b, p in pr: w.writerow([g, '-'.join(x or '000' for x in a), '-'.join(str(y or 0) for y in b), round(p, 3), len(lt[(g, a)]), len(mt[(g, b)])])
    print('pairs', len(df), 'lipi signs', df.lipi.nunique(), 'mah signs', df.mahadevan.nunique(), 'text pairs', len(pr))
    top = df[df.rank_for_lipi_sign == 1]
    print('Lipi sign occurrences covered by a rank-1 pair:', int(top.lipi_occurrences.sum()), 'of', sum(occ.values()))
    print('Lipi signs with >=5 positions', int((top.text_positions >= 5).sum()), 'of', len(occ))
if __name__ == '__main__': main()
