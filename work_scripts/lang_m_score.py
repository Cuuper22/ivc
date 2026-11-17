#!/usr/bin/env python3
"""lang_m step 3b-5: the rebus score for every dictionary and language family, with three controls, on the full 3 x 2 grid.

For each sign (work_data/lang_m/jobs.csv: picture nouns + job) and each dictionary: the sign HITS when, for one of its picture nouns,
a word for that thing has a sound-alike (lang_m_common rules) whose gloss carries a keyword of the sign's job.
SCORE (binary) = number of units that hit.  SHARE (graded, the one with power: the binary count saturates once sound-alikes are
many) = sum over units of the share of the picture words' sound-alikes whose gloss carries the unit's job keyword.  Family score: a sign hits if it hits in any dictionary of that family.
CONTROL 1 (2,000 runs): jobs dealt at random among the signs (pictures stay).  Measures what a dictionary gives from its size and gloss
          habits with the real pictures.  (Dealing the pictures among signs instead is the same permutation, so it is not run twice.)
CONTROL 2 (2,000 runs): every picture noun replaced by a different outside concrete noun (water, stone, dog, ...; same noun -> same
          replacement), jobs kept.  Asks whether the real pictures do better than any set of drawable things would.
CONTROL 3 (200 runs): the dictionary's sound forms dealt at random among its words (every gloss gets another word's form).  Keeps the
          exact density of sound-alikes and the gloss habits, destroys every real link between sound and meaning.  (A consistent
          swap of consonant letters, the first idea, leaves every sound-alike relation unchanged, so it would measure nothing.)
P = share of control runs scoring at least the real score ((k+1)/(n+1)).
Output: work_data/lang_m/grid.csv, work_data/lang_m/evidence.csv, work_data/lang_m/signhits.csv
Run in the background; prints progress.
"""
import sys, os, csv, time, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m_common import *

N1, N2, N3 = 2000, 2000, int(os.environ.get('LANG_M_N3', 200))
ONLY = os.environ.get('LANG_M_ONLY')
rng = np.random.default_rng(20261117)
def log(*a): print(f'[lang_m_score {time.strftime("%H:%M:%S")}]', *a, flush=True)

J = list(csv.DictReader(open(f'{OUT}/jobs.csv', encoding='utf-8')))
# UNITS: signs with the same picture nouns and the same job are one unit (fifty 'person' name signs are one test, not fifty)
_u = collections.OrderedDict()
for r in J: _u.setdefault((r['nouns'], r['job']), []).append(r['sign'])
SIGNS = ['/'.join(v) for v in _u.values()]; SN = [k[0].split('|') for k in _u]; SJ = [k[1] for k in _u]
NOUNS = sorted({n for ns in SN for n in ns}); NI = {n: i for i, n in enumerate(NOUNS)}
OUTN = [f'OUT:{e}' for e, _ in OUTSIDE]
JI = {j: i for i, j in enumerate(JOBS)}
log(f'{len(SIGNS)} units (picture x job) from {len(J)} signs, {len(NOUNS)} picture nouns, jobs {dict(collections.Counter(SJ))}')
KEYS = [(d, b) for d in DISTS for b in BREADTHS]


def matrices(L, nouns, perm=None, evidence=None):
    """-> {(dist,breadth): (H, T)}: H[noun, job] = number of distinct sound-alike words carrying a keyword of that job,
    T[noun] = number of distinct sound-alike words at all (other entries, not glossed as the thing itself)."""
    out = {k: (np.zeros((len(nouns), len(JOBS))), np.zeros(len(nouns))) for k in KEYS}
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
                if evidence is not None:
                    for q in c:
                        for col in np.nonzero(L.kwmat[q])[0]:
                            j, b = L.kwkeys[col]
                            evidence.append(dict(dict=L.name, dist=d, breadth=b, noun=noun, job=j, picture_word=L.hw[pw],
                                                 picture_gloss=L.gl[pw][:80], soundalike=L.hw[q], soundalike_gloss=L.gl[q][:120]))
                qs.update(c)
            if not qs: continue
            km = L.kwmat[sorted(qs)].sum(axis=0)
            for col, (j, b) in enumerate(L.kwkeys):
                out[(d, b)][0][a, JI[j]] = km[col]
            for b in BREADTHS: out[(d, b)][1][a] = len(qs)
    return out


def score(HT, sn_idx, sj_idx):
    """binary score: units with at least one sound-alike carrying the unit's job keyword."""
    H = HT[0]
    return sum(any(H[n, j] > 0 for n in ns) for ns, j in zip(sn_idx, sj_idx))


def share(HT, sn_idx, sj_idx):
    """graded score: sum over units of (sound-alikes with the unit's job keyword) / (all sound-alikes of the unit's picture words)."""
    H, T = HT; tot = 0.0
    for ns, j in zip(sn_idx, sj_idx):
        t = sum(T[n] for n in ns)
        if t: tot += sum(H[n, j] for n in ns) / t
    return tot


def score_vec(HT, sn_idx, sj_idx):
    return np.array([any(HT[0][n, j] > 0 for n in ns) for ns, j in zip(sn_idx, sj_idx)])


def pool(mats):
    return (sum(m[0] for m in mats), sum(m[1] for m in mats))


SNI = [[NI[n] for n in ns] for ns in SN]; SJI = [JI[j] for j in SJ]
real, outm, c3 = {}, {}, {}
evidence = []
allnames = [n for fam in FAMILIES.values() for n in fam]
if ONLY: allnames = ONLY.split(',')
for name in allnames:
    t0 = time.time(); L = Lex(name)
    real[name] = matrices(L, NOUNS, evidence=evidence)
    outm[name] = matrices(L, OUTN)
    cover = np.array([any(L.is_pic.get(n) for n in ns) for ns in SN])
    log(f'{name}: {L.n} words / {L.nentries} entries; signs with a picture word {cover.sum()}/{len(SN)}; real score strict-narrow '
        f'{score(real[name][("strict","narrow")], SNI, SJI)}, loose-wide {score(real[name][("loose","wide")], SNI, SJI)}; control 3 running ...')
    runs = []
    for t in range(N3):
        perm = rng.permutation(L.n)
        runs.append(matrices(L, NOUNS, perm=perm))
        if (t + 1) % 50 == 0: log(f'   {name} control 3: {t + 1}/{N3}')
    c3[name] = runs
    real[name]['_cover'] = cover; real[name]['_size'] = (L.n, L.nentries)
    log(f'   {name} done in {time.time() - t0:.0f}s')

units = [(n, [n]) for n in allnames] + [(f'FAMILY {f}', ns) for f, ns in FAMILIES.items() if all(x in real for x in ns)]
# same control-1 and control-2 draws for every unit
perms1 = [rng.permutation(len(SJI)) for _ in range(N1)]
maps2 = [rng.choice(len(OUTN), size=len(NOUNS), replace=False) for _ in range(N2)]
rows = []; signrows = []
for unit, names in units:
    for k in KEYS:
        R = pool([real[n][k] for n in names]); O = pool([outm[n][k] for n in names])
        C3 = [pool([c3[n][t][k] for n in names]) for t in range(N3)]
        row = dict(unit=unit, dist=k[0], breadth=k[1], units=len(SJI),
                   words=sum(real[n]['_size'][0] for n in names), entries=sum(real[n]['_size'][1] for n in names),
                   covered=int(np.logical_or.reduce([real[n]['_cover'] for n in names]).sum()))
        for stat, fn in (('hits', score), ('share', share)):
            obs = fn(R, SNI, SJI); row[stat] = round(obs, 3)
            n1 = np.array([fn(R, SNI, [SJI[i] for i in p]) for p in perms1])
            n2 = np.array([fn(O, [[m[x] for x in ns] for ns in SNI], SJI) for m in maps2])
            n3 = np.array([fn(c, SNI, SJI) for c in C3])
            for tag, a_ in (('c1', n1), ('c2', n2), ('c3', n3)):
                row[f'{stat}_{tag}_mean'] = round(a_.mean(), 3); row[f'{stat}_{tag}_sd'] = round(a_.std(), 3)
                row[f'{stat}_{tag}_P'] = round((1 + (a_ >= obs - 1e-12).sum()) / (1 + len(a_)), 4)
        rows.append(row)
        if unit.startswith('FAMILY'):
            v = score_vec(R, SNI, SJI)
            for sg, h, ns, j in zip(SIGNS, v, SN, SJ):
                if h: signrows.append(dict(unit=unit, dist=k[0], breadth=k[1], signs=sg, nouns='|'.join(ns), job=j))
    log(f'{unit}: ' + '  '.join(f'{r["dist"][0]}{r["breadth"][0]} hits {r["hits"]} (c1 {r["hits_c1_mean"]}) share {r["share"]:.2f} '
                                 f'(c1 {r["share_c1_mean"]:.2f} P{r["share_c1_P"]}, c2 {r["share_c2_mean"]:.2f} P{r["share_c2_P"]}, c3 {r["share_c3_mean"]:.2f} P{r["share_c3_P"]})'
                                 for r in rows[-len(KEYS):]))
for fn, data in (('grid.csv', rows), ('evidence.csv', evidence), ('signhits.csv', signrows)):
    if not data: continue
    with open(f'{OUT}/{fn}', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
log('written grid.csv, evidence.csv, signhits.csv')
