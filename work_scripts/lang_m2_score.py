#!/usr/bin/env python3
"""lang_m2 steps 1-6: rebus score per dictionary and family, both picture variants, full 3 x 2 grid, controls C1-C4, step-6 summary.
Rules: lang_m2_common.py header (fixed before this script computed any score).
Output (work_data/lang_m2/): grid.csv (every cell), summary.csv (step 6 per family and variant), unit_hits.csv (per unit, per family
cell: real hit and its hit rate under C3, for step 8), evidence.csv (strict and medium picture-word / sound-alike pairs that carry the
class keyword of a unit with that picture noun).  Progress is printed as it runs.
"""
import sys, os, csv, time, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m2_common import *

rng = np.random.default_rng(20261119)
def log(*a): print(f'[lang_m2_score {time.strftime("%H:%M:%S")}]', *a, flush=True)
NOUNS = blind_nouns(); NI = {n: i for i, n in enumerate(NOUNS)}
OUTS = outside_list(); OUTN = [f'OUT:{e}' for e, _ in OUTS]
CI = {c: i for i, c in enumerate(CLS)}
U = list(csv.DictReader(open(f'{OUT}/units.csv', encoding='utf-8')))
VU = {v: [u for u in U if u['variant'] == v] for v in VARIANTS}
log(f'{len(NOUNS)} picture nouns, {len(OUTS)} outside nouns; units ' + ', '.join(f'{v} {len(x)}' for v, x in VU.items()) + f'; N3 = {N3}')


def matrices(L, nouns, perm=None, evidence=None, ev_cls=None):
    """-> {(dist,breadth): (H[noun, class] = sound-alikes carrying the class keyword, T[noun] = all sound-alikes)}"""
    out = {k: (np.zeros((len(nouns), len(CLS)), np.float32), np.zeros(len(nouns), np.float32)) for k in KEYS}
    inv = None
    if perm is not None: inv = np.empty_like(perm); inv[perm] = np.arange(len(perm))
    for a, noun in enumerate(nouns):
        pws = L.is_pic.get(noun, [])
        if not pws: continue
        pf = L.pic_flag[noun]
        for d in DISTS:
            qs = set()
            for pw in pws:
                f = L.nf[pw] if perm is None else L.nf[perm[pw]]
                c = L.near_form(f, d)
                if not c: continue
                c = np.asarray(c)
                if perm is not None: c = inv[c]
                c = [q for q in c[(L.eid_arr[c] != L.eid[pw])] if q not in pf]
                if evidence is not None and d != 'loose':
                    for q in c:
                        for col in np.nonzero(L.kwmat[q])[0]:
                            cc, b = L.kwkeys[col]
                            if cc in ev_cls.get(noun, ()):
                                evidence.append(dict(dict=L.name, dist=d, breadth=b, noun=noun, cls=cc, picture_word=L.hw[pw],
                                                     picture_entry=L.eid[pw], picture_gloss=L.gl[pw][:70], soundalike=L.hw[q],
                                                     soundalike_entry=L.eid[q], soundalike_gloss=L.gl[q][:100]))
                qs.update(c)
            if not qs: continue
            km = L.kwmat[sorted(qs)].sum(axis=0)
            for col, (cc, b) in enumerate(L.kwkeys): out[(d, b)][0][a, CI[cc]] = km[col]
            for b in BREADTHS: out[(d, b)][1][a] = len(qs)
    return out


ev_cls = collections.defaultdict(set)
for u in U:
    for n in u['nouns'].split('|'): ev_cls[n].add(u['cls'])
allnames = [n for fam in FAMILIES.values() for n in fam]
if os.environ.get('LANG_M2_ONLY'): allnames = os.environ['LANG_M2_ONLY'].split(',')
real, outm, c3, c3row, cover, size = {}, {}, {}, {}, {}, {}
evidence = []
for name in allnames:
    t0 = time.time(); L = Lex(name, NOUNS, OUTS)
    real[name] = matrices(L, NOUNS, evidence=evidence, ev_cls=ev_cls)
    outm[name] = matrices(L, OUTN)
    cover[name] = {n for n in NOUNS if L.is_pic.get(n)}; size[name] = (L.n, L.nentries)
    log(f'{name}: {L.n} words / {L.nentries} entries; picture nouns with a picture word {len(cover[name])}/{len(NOUNS)}; control 3 running ...')
    # entry-level deal: entries with the same number of rows trade their form lists
    ent = collections.OrderedDict()
    for i, e in enumerate(L.eid): ent.setdefault(e, []).append(i)
    strata = collections.defaultdict(list)
    for e, rows_ in ent.items(): strata[len(rows_)].append(rows_)
    def entry_perm():
        perm = np.arange(L.n)
        for k_, groups_ in strata.items():
            if len(groups_) < 2: continue
            src = np.array(groups_); dst = src[rng.permutation(len(groups_))]
            perm[src.ravel()] = dst.ravel()
        return perm
    runs, runs_row = [], []
    rowlevel = L.n != L.nentries
    for t in range(N3):
        runs.append(matrices(L, NOUNS, perm=entry_perm()))
        if rowlevel: runs_row.append(matrices(L, NOUNS, perm=rng.permutation(L.n)))
        if (t + 1) % 100 == 0: log(f'   {name} control 3: {t + 1}/{N3}  ({time.time() - t0:.0f}s)')
    c3[name] = runs; c3row[name] = runs_row if rowlevel else runs
    log(f'   {name} done in {time.time() - t0:.0f}s')

gridrows, sumrows, unitrows = [], [], []
for v, units in VU.items():
    nU = len(units)
    A = np.zeros((nU, len(NOUNS)), np.float32)
    for i, u in enumerate(units):
        for n in u['nouns'].split('|'): A[i, NI[n]] = 1
    cls = np.array([CI[u['cls']] for u in units])
    vn = sorted({NI[n] for u in units for n in u['nouns'].split('|')})
    # draws shared by every dictionary and family in this variant
    P1 = np.array([rng.permutation(cls) for _ in range(N1)])
    maps2 = [rng.choice(len(OUTN), size=len(NOUNS), replace=False) for _ in range(N2)]
    groups = collections.defaultdict(list)
    for i, u in enumerate(units): groups[u['nouns']].append(i)
    cfreq = np.bincount(cls, minlength=len(CLS)).astype(float)
    P4 = np.tile(cls, (N4, 1))
    for t in range(N4):
        for g in groups.values():
            avail = np.array([c for c in range(len(CLS)) if c not in set(cls[g])])
            w_ = cfreq[avail] + 1e-9; w_ = w_ / w_.sum()
            P4[t, g] = rng.choice(avail, size=len(g), replace=len(avail) < len(g), p=w_)
    ar = np.arange(nU)

    def stats(H, T, C):
        """H nouns x classes, T nouns; C = class vector (U) or matrix (runs x U) -> (hits, share) arrays"""
        UH = A @ H; UT = A @ T; UB = (A @ (H > 0)) > 0
        C = np.atleast_2d(C)
        hits = UB[ar[None, :], C].sum(axis=1)
        with np.errstate(invalid='ignore', divide='ignore'):
            sh = np.where(UT[None, :] > 0, UH[ar[None, :], C] / UT[None, :], 0).sum(axis=1)
        return hits, sh

    targets = [(n, [n]) for n in allnames] + [(f'FAMILY {f}', ns) for f, ns in FAMILIES.items() if all(x in real for x in ns)]
    zcache = {}
    for unit, names in targets:
        for k in KEYS:
            H = sum(real[n][k][0] for n in names); T = sum(real[n][k][1] for n in names)
            r_h, r_s = stats(H, T, cls)
            n1 = stats(H, T, P1)
            n2 = [stats(sum(outm[n][k][0] for n in names)[m], sum(outm[n][k][1] for n in names)[m], cls) for m in maps2]
            n2 = (np.array([x[0][0] for x in n2]), np.array([x[1][0] for x in n2]))
            n3 = [stats(sum(c3[n][t][k][0] for n in names), sum(c3[n][t][k][1] for n in names), cls) for t in range(N3)]
            n3 = (np.array([x[0][0] for x in n3]), np.array([x[1][0] for x in n3]))
            n3r = [stats(sum(c3row[n][t][k][0] for n in names), sum(c3row[n][t][k][1] for n in names), cls) for t in range(N3)]
            n3r = (np.array([x[0][0] for x in n3r]), np.array([x[1][0] for x in n3r]))
            n4 = stats(H, T, P4)
            row = dict(variant=v, unit=unit, dist=k[0], breadth=k[1], units=nU,
                       covered=int(sum(any(x in set().union(*[cover[n] for n in names]) for x in u['nouns'].split('|')) for u in units)),
                       words=sum(size[n][0] for n in names), entries=sum(size[n][1] for n in names))
            for si, stat in enumerate(('hits', 'share')):
                obs = float((r_h, r_s)[si][0]); row[stat] = round(obs, 3)
                for tag, arr in (('c1', n1[si]), ('c2', n2[si]), ('c3', n3[si]), ('c4', n4[si]), ('c3row', n3r[si])):
                    arr = np.asarray(arr, float)
                    row[f'{stat}_{tag}_mean'] = round(arr.mean(), 3); row[f'{stat}_{tag}_sd'] = round(arr.std(), 3)
                    row[f'{stat}_{tag}_P'] = round((1 + (arr >= obs - 1e-9).sum()) / (1 + len(arr)), 4)
                row[f'{stat}_all4'] = all(row[f'{stat}_{t}_P'] < 0.05 for t in ('c1', 'c2', 'c3', 'c4'))
                row[f'{stat}_c2c3'] = row[f'{stat}_c2_P'] < 0.05 and row[f'{stat}_c3_P'] < 0.05
            gridrows.append(row)
            if not unit.startswith('FAMILY'):
                def z(o, a):
                    a = np.asarray(a, float); s = a.std()
                    return (np.zeros(len(a)) if s == 0 else (a - a.mean()) / s), (0.0 if s == 0 else (o - a.mean()) / s)
                zcache[(unit, k)] = (z(float(r_s[0]), n3[1]), z(float(r_s[0]), n4[1]), z(float(r_s[0]), n1[1]))
            else:
                # per-unit hits for step 8: real hit and the unit's hit rate under C3
                UB = (A @ (H > 0)) > 0; real_hit = UB[ar, cls]
                c3rate = np.mean([((A @ (sum(c3[n][t][k][0] for n in names) > 0)) > 0)[ar, cls] for t in range(N3)], axis=0)
                for i, u in enumerate(units):
                    unitrows.append(dict(variant=v, family=unit[7:], dist=k[0], breadth=k[1], nouns=u['nouns'], cls=u['cls'],
                                         signs=u['signs'], real_hit=int(real_hit[i]), c3_hit_rate=round(float(c3rate[i]), 3)))
        log(f'{v} {unit}: ' + '  '.join(f'{r["dist"][0]}{r["breadth"][0]} share {r["share"]:.2f} (P c1 {r["share_c1_P"]} c2 {r["share_c2_P"]} '
                                         f'c3 {r["share_c3_P"]} c4 {r["share_c4_P"]}) hits {r["hits"]:.0f}' for r in gridrows[-len(KEYS):]))
    for fam, names in FAMILIES.items():
        if not all(x in real for x in names): continue
        cells = [r for r in gridrows if r['variant'] == v and (r['unit'] in names or r['unit'] == f'FAMILY {fam}')]
        ncells = 2 * len(cells)
        all4 = sum(r['hits_all4'] + r['share_all4'] for r in cells)
        c2c3 = sum(r['hits_c2c3'] + r['share_c2c3'] for r in cells)
        out = dict(variant=v, family=fam, dictionaries=len(names), cells=ncells, beat_all4=all4, expected_bound=round(0.05 * ncells, 2),
                   beat_c2_and_c3=c2c3)
        for tag, j in (('Z3', 0), ('Z4', 1), ('Z1', 2)):
            zs = [zcache[(n, k)][j] for n in names for k in KEYS]
            real_mean = float(np.mean([z[1] for z in zs]))
            null = np.mean([z[0] for z in zs], axis=0)
            out[tag] = round(real_mean, 3)
            out[f'{tag}_P'] = round((1 + (null >= real_mean - 1e-12).sum()) / (1 + len(null)), 4)
        out['clears_bar'] = (v == PRIMARY and out['Z3_P'] < 0.05 / 7 and all4 > 0.05 * ncells)
        sumrows.append(out); log(f'SUMMARY {out}')

for fn, data in (('grid.csv', gridrows), ('summary.csv', sumrows), ('unit_hits.csv', unitrows), ('evidence.csv', evidence)):
    if not data: continue
    with open(f'{OUT}/{fn}', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
log('written grid.csv, summary.csv, unit_hits.csv, evidence.csv')
