#!/usr/bin/env python3
"""Shared kit for the SIZE job (size_*.py): read rank out of seal size.  Written 2026-11-17, before any size_* number.

Plain words:
- SEAL: a carved stamp (first catalogue, Lipi; tier 'seal' in work_data/stamps/objects.csv). One row per inscribed face.
- FACE AREA: catalogue width x height of the face in mm2. logA = natural log of it. A difference of 0.1 in logA = about
  10% bigger. 'Size' below always means logA.
- COMPLETE TEXT: no lost sign, no break flag (twins_common.seals()).
- SITE GROUP: Mohenjo-daro (MD), Harappa (HP), Dholavira (DHO), Lothal (LOT), Chanhu-daro (CHD), Kalibangan (KLB), other.
- FORMAT: square (beast seal), rectangular (the long inscription-only bar), round, cylinder, other (catalogue type
  'SEAL' with no shape letter).
- LENGTH: number of signs, as a category 1, 2, ... 7, 8+.
- BASELINE (model b): length + site + format, each as a set of yes/no columns. Every claim must beat it.
- HALVES: seals are split in two by TEXT (identical texts always land in the same half, so a twin cannot be seen in
  training and then scored in testing). Seed 0 is the headline split; 20 more splits give the spread.
- HELD-OUT SHARE (R2): 1 - (squared error on the test half) / (squared spread of the test half around its own mean).
  The share of size variation the model explains on seals it never saw. Extra share = model R2 - baseline R2.
- RIDGE: a least-squares fit where the per-sign (or per-phrase, per-class) weights are pulled toward 0 by a penalty;
  the baseline columns are not penalised. The penalty is chosen by 5-fold cross-validation inside the training half only.
- SIZE WEIGHT of a sign: its ridge weight = how much bigger (in logA) a seal is when its text carries the sign, after
  length, site and format and all other signs are taken out. +0.10 = about 10% bigger.
- DECOYS: (i) token dealing: every sign in every text is replaced by a random sign of the same frequency band (10 bands
  over seal sign counts), so each seal keeps its length and its mix of common and rare signs but loses which signs it
  has; (ii) class dealing (model c): the frame-v2 job labels dealt to wrong signs of the same band (as in frame v2);
  (iii) phrase dealing (model e): each fixed phrase replaced by a random run of the same length found in a similar
  number of seal texts; (iv) cell dealing: sizes shuffled among seals of the same site, length and format.
- NEW TEXTS from the second catalogue (Mahadevan 1977) carry no size: that catalogue has no measurement field.
  Stand-in outside set: first-catalogue seals whose text has NO partner in the second catalogue (texts that catalogue
  never transcribed, mostly later digs).
"""
import sys, os, io, contextlib, time, hashlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
with contextlib.redirect_stdout(io.StringIO()):
    from twins_common import seals, crest_of, text_kind
    from frame2_pictures import pic, pic_book
ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/size'; os.makedirs(OUT, exist_ok=True)
T0 = time.time()
def log(tag, *a): print(f'[{tag} {time.time()-T0:6.1f}s]', *a, flush=True)

C2 = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
V2 = dict(zip(C2.sign, C2.v2_base))
V2_CLASSES = ['OPEN', 'SLOT', 'CREST', 'PERSONAL', 'NUM_NAME', 'NUM_SHORT', 'NUM_TALL', 'MEASURE', 'AFTER_M', 'THING',
              'NAME_BACK', 'PLACE', 'CLOSER', 'TITLE']
JOB = {'OPEN': 'front word', 'SLOT': 'after-front slot', 'CREST': 'name front (crest)', 'PERSONAL': 'name part',
       'NUM_NAME': 'tall two', 'NUM_SHORT': 'short number', 'NUM_TALL': 'tall number', 'MEASURE': 'measure',
       'AFTER_M': 'after-measure', 'THING': 'counted thing', 'NAME_BACK': 'name back', 'PLACE': 'place or time word',
       'CLOSER': 'closer', 'TITLE': 'after-jar title'}
def job(s): return JOB.get(V2.get(s, 'PERSONAL'), 'name part')

PH = pd.read_csv(f'{ROOT}/work_data/phrases/atlas_all.csv', dtype=str).fillna('')
PHRASES = [tuple(p.split('-')) for p in PH.phrase]
SITEG = {'Mohenjo-daro': 'MD', 'Harappa': 'HP', 'Dholavira': 'DHO', 'Lothal': 'LOT', 'Chanhu-daro': 'CHD', 'Kalibangan': 'KLB'}


def table():
    """complete seal faces with a face area: one row each."""
    S = seals()
    S = S[S.complete & S.area_mm2.notna()].copy()
    S['logA'] = np.log(S.area_mm2)
    S['tok'] = S.signs.str.split('-').map(tuple)
    S['L'] = S.n.clip(upper=8).astype(int)
    S['siteg'] = S.site.map(SITEG).fillna('other')
    P = pd.read_csv(f'{ROOT}/work_data/crosswalk_text_pairs.csv', dtype=str)
    S['partnered'] = S.signs.isin(set(P.lipi_text))
    S['crest'] = S.signs.map(crest_of)
    return S.reset_index(drop=True)


def split(S, seed=0):
    """True = training half. By text: same text same half."""
    def h(t): return int(hashlib.md5(f'{seed}|{t}'.encode()).hexdigest(), 16) % 2 == 0
    return S.signs.map(h).values


def base_X(S, levels=None):
    cols = {}
    for c in ('L', 'siteg', 'fmt'):
        lv = levels[c] if levels else sorted(S[c].astype(str).unique())
        for v in lv[1:]: cols[f'{c}={v}'] = (S[c].astype(str) == v).astype(float).values
    X = pd.DataFrame(cols, index=S.index)
    return X, ({c: sorted(S[c].astype(str).unique()) for c in ('L', 'siteg', 'fmt')} if levels is None else levels)


def extra_X(S, cols_list, name):
    return pd.DataFrame({f'{name}={k}': v for k, v in cols_list}, index=S.index)


def sign_X(toks, signs):
    ix = {s: i for i, s in enumerate(signs)}
    X = np.zeros((len(toks), len(signs)))
    for r, t in enumerate(toks):
        for s in set(t):
            if s in ix: X[r, ix[s]] = 1
    return X


def class_X(toks, cmap):
    ix = {c: i for i, c in enumerate(V2_CLASSES)}
    X = np.zeros((len(toks), len(V2_CLASSES)))
    for r, t in enumerate(toks):
        for s in t: X[r, ix[cmap.get(s, 'PERSONAL')]] = 1
    return X


def has_run(t, p):
    k = len(p)
    return any(t[i:i + k] == p for i in range(len(t) - k + 1))


def phrase_X(toks, phrases):
    X = np.zeros((len(toks), len(phrases)))
    for r, t in enumerate(toks):
        for j, p in enumerate(phrases):
            if has_run(t, p): X[r, j] = 1
    return X


def ridge_fit(B, Z, y, lam):
    """B: unpenalised (baseline) columns, Z: penalised columns, intercept added. returns (beta_B with intercept, beta_Z)."""
    n = len(y)
    X = np.hstack([np.ones((n, 1)), B, Z])
    pen = np.r_[np.zeros(1 + B.shape[1]), np.full(Z.shape[1], lam)]
    A = X.T @ X + np.diag(pen) + 1e-8 * np.eye(X.shape[1])
    w = np.linalg.solve(A, X.T @ y)
    return w[:1 + B.shape[1]], w[1 + B.shape[1]:]


def ridge_pred(B, Z, wb, wz):
    return wb[0] + B @ wb[1:] + (Z @ wz if Z.shape[1] else 0)


LAMS = [0.3, 1, 3, 10, 30, 100, 300]


def ridge_cv(B, Z, y, groups, seed=0, lams=LAMS):
    """penalty by 5-fold CV over text groups inside the training data."""
    if Z.shape[1] == 0: return 0.0
    ug = np.unique(groups); r = np.random.default_rng(seed); f = dict(zip(ug, r.integers(0, 5, len(ug))))
    fold = np.array([f[g] for g in groups])
    best = None
    for lam in lams:
        sse = 0
        for k in range(5):
            tr, te = fold != k, fold == k
            wb, wz = ridge_fit(B[tr], Z[tr], y[tr], lam)
            sse += ((y[te] - ridge_pred(B[te], Z[te], wb, wz)) ** 2).sum()
        if best is None or sse < best[0]: best = (sse, lam)
    return best[1]


def r2(y, p): return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def freq_bands(toks, nb=10):
    c = collections.Counter(s for t in toks for s in t)
    order = sorted(c, key=lambda s: (-c[s], s))
    band = {}; per = int(np.ceil(len(order) / nb))
    for i, s in enumerate(order): band[s] = i // per
    return band, c


def deal_tokens(toks, band, cnt, seed):
    """each token -> random sign of the same frequency band, drawn by frequency."""
    r = np.random.default_rng(seed)
    pools = collections.defaultdict(list)
    for s, b in band.items(): pools[b].append(s)
    pp = {b: (np.array(v), np.array([cnt[s] for s in v], float) / sum(cnt[s] for s in v)) for b, v in pools.items()}
    out = []
    for t in toks:
        out.append(tuple(pp[band[s]][0][r.choice(len(pp[band[s]][0]), p=pp[band[s]][1])] for s in t))
    return out


def deal_classes(band, seed):
    """frame-v2 class labels dealt among signs of the same band (sizes of each label per band kept)."""
    r = np.random.default_rng(seed)
    pools = collections.defaultdict(list)
    for s, b in band.items(): pools[b].append(s)
    out = {}
    for b, v in pools.items():
        labs = [V2.get(s, 'PERSONAL') for s in v]; r.shuffle(labs)
        out.update(dict(zip(v, labs)))
    return out


def runs_in(toks, k):
    c = collections.Counter()
    for t in toks:
        for p in {t[i:i + k] for i in range(len(t) - k + 1)}: c[p] += 1
    return c


def deal_phrases(toks, phrases, seed):
    """each phrase -> a random adjacent run of the same length whose seal-text count is within x0.67-1.5 of the phrase's."""
    r = np.random.default_rng(seed)
    out = []
    used = set(phrases)
    rc = {k: runs_in(toks, k) for k in (2, 3, 4)}
    for p in phrases:
        k = len(p); n = rc[k].get(p, 0)
        cand = [q for q, m in rc[k].items() if q not in used and (m >= max(1, n * 0.67) and m <= max(2, n * 1.5))]
        if not cand: cand = [q for q in rc[k] if q not in used]
        q = cand[r.integers(len(cand))]; used.add(q); out.append(q)
    return out


def cell_medians(S, y):
    """median logA in each site x length x format cell (falls back to site x length, then length)."""
    keys = [('siteg', 'L', 'fmt'), ('siteg', 'L'), ('L',)]
    meds = [pd.Series(y, index=S.index).groupby([S[c] for c in k]).agg(['median', 'size']) for k in keys]
    out = np.full(len(S), np.nan)
    for i, (_, row) in enumerate(S.iterrows()):
        for k, m in zip(keys, meds):
            key = tuple(row[c] for c in k) if len(k) > 1 else row[k[0]]
            if key in m.index and m.loc[key, 'size'] >= 4:
                out[i] = m.loc[key, 'median']; break
    return out
