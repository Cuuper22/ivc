#!/usr/bin/env python3
"""Shared kit for the "abroad4" job: are the texts found abroad the same writing system doing the same thing?
Written 2026-11-17. No word is attached to any sign anywhere: sign numbers, pictures, jobs and findspots only.

PLAIN WORDS
- FOREIGN SET ("abroad"): Lipi faces whose region is Persian Gulf, Mesopotamia, Iranian Plateau or Central Asia
  (41 faces = 41 objects). Tier "unk_round": faces at site Unknown whose type is a round or cylinder seal (SEAL:C, SEAL:CY);
  the catalogue gives no findspot but the shape is the overseas shape. Tier "M_only": West-Asian lines of the second
  catalogue (Mahadevan) that have no partner in Lipi. The main numbers use the 41 (core); other tiers are shown beside them.
- HOME SET: Lipi faces from the Indus region (regions Lower Indus, Inter-Riverine, Gujarat/Kutch, Eastern Headwaters,
  Upper Indus). Left out of both sets: region Other (Unknown site, square seals and tablets), South India (Daimabad).
- DISTINCT TEXT: identical sign strings counted once (moulded copies).
- USABLE SIGN: a real catalogue sign (three digits) that occurs in at least one home text. A lost sign (000), an unclear
  sign (ALT) and a sign never seen at home are not scored: they cut a text into RUNS. Only steps between neighbouring
  usable signs inside a run are scored ("transitions"). bits per step = -log2 of the model's probability for the next sign.
- CROSS-FITTING: the home texts are split into 10 folds (by distinct text). A home text is scored by the model trained
  on the other 9 folds; a foreign text is scored by all 10 models and the 10 results are averaged. So no text is scored
  by a model that saw it, and the foreign texts face models trained on as much data as the home texts do.
- MODELS (all trained on home texts only): unigram (sign frequencies alone), sign-pair model (Witten-Bell smoothed bigram),
  frame v2 (14 job classes, class-to-class rules learned per object kind, signs inside a class by frequency; classes from
  work_data/frame/classes_v2.csv column v2_base), mix (half sign-pair, half frame v2).
- MATCHED HOME TEXTS: for each foreign text, a home distinct text with the same object kind, the same number of steps,
  and (for seals) the same animal group; drawn at random; repeated 2,000 times (fixed seed). Widening rule when fewer than
  5 candidates: length within 1, then animal dropped, then kind dropped; the number of widened texts is reported.
"""
import sys, os, re, io, contextlib, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from frame2_common import *      # d, M, pairs, HAND, kind_counts, class_model_kind, mix_kind, FixedKind, KindModel, train_texts, ...
import numpy as np, pandas as pd

OUT4 = f'{ROOT}/work_data/abroad4'
os.makedirs(OUT4, exist_ok=True)
T0 = time.time()
def log(*a): print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)

ABROAD_REG = ['Persian Gulf', 'Mesopotamia', 'Iranian Plateau', 'Central Asia']
HOME_REG = ['Lower Indus', 'Inter-Riverine', 'Gujarat/Kutch', 'Eastern Headwaters', 'Upper Indus']
REGION_GROUP = {'Persian Gulf': 'Gulf', 'Mesopotamia': 'Mesopotamia', 'Iranian Plateau': 'Iran', 'Central Asia': 'Central Asia'}
NMODEL = ['unigram', 'sign pair', 'frame v2', 'mix']

# ------------------------------------------------------------------ face table
ab_base = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str, keep_default_na=False)
ANIMAL = dict(zip(ab_base.id, ab_base.animal))
AG_MAP = {'UNICORN': 'unicorn', 'SHORTHORN': 'short-horned bull', 'NONE': 'none', 'UNKNOWN': 'none', '': 'none'}
def ag_of(i, kind):
    if kind != 'seal': return 'n/a'
    return AG_MAP.get(ANIMAL.get(i, ''), 'other beast')

F = d[['id', 'obj', 'site', 'region', 'area-section', 'block-house', 'room-grid', 'type', 'shape', 'material', 'symbol',
       'complete', 'kind', 'tok', 'flg']].copy()
F['round'] = F.type.isin(['SEAL:C', 'SEAL:CY'])
F['animal'] = [ANIMAL.get(i, '') for i in F.id]
F['ag'] = [ag_of(i, k) for i, k in zip(F.id, F.kind)]
F['clean'] = [not (f & {'broken', 'lost', 'alt'}) and not (set(x) & UNK) for x, f in zip(F.tok, F.flg)]
F['tier'] = 'other'
F.loc[F.region.isin(HOME_REG), 'tier'] = 'home'
F.loc[F.region.isin(ABROAD_REG), 'tier'] = 'core'
F.loc[(F.site == 'Unknown') & F['round'], 'tier'] = 'unk_round'
F['rgroup'] = F.region.map(REGION_GROUP).fillna('')
HOME_IDS = set(F[F.tier == 'home'].id)

# ------------------------------------------------------------------ home vocabulary, folds, models
SIGNRE = re.compile(r'^\d{3}$')
def real(s): return bool(SIGNRE.match(s)) and s != '000'

home_faces = F[F.tier == 'home']
home_distinct = {}                                   # token tuple -> (clean, kind, ag, round, site, id)
for i, x, c, k, ag, r, st in zip(home_faces.id, home_faces.tok, home_faces.clean, home_faces.kind, home_faces.ag, home_faces['round'], home_faces.site):
    if x and x not in home_distinct: home_distinct[x] = (c, k, ag, r, st, i)
HOME_USE = collections.Counter(s for x in home_faces.tok for s in x if real(s))     # token counts in all home faces
GV = sorted({s for x in home_distinct for s in x if real(s)})
GIDX = {s: i for i, s in enumerate(GV)}
V2MAP_DF = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
V2MAP = dict(zip(V2MAP_DF.sign, V2MAP_DF.v2_base))
V2CLASS = {s: V2MAP.get(s, 'PERSONAL') for s in GV}

NFOLD = 10
_rng = np.random.default_rng(4242)
_keys = list(home_distinct)
_perm = _rng.permutation(len(_keys))
FOLD = {_keys[j]: int(n % NFOLD) for n, j in enumerate(_perm)}


def build_models(train):
    C, CK = kind_counts(train, GIDX)
    uni = unigram_model(C); big = bigram_model(C)
    v2 = class_model_kind(C, CK, V2CLASS, 'frame v2', GV)
    mix = mix_kind(FixedKind(big), v2, 0.5, 'mix')
    return {'unigram': FixedKind(uni), 'sign pair': FixedKind(big), 'frame v2': v2, 'mix': mix}, C


FOLD_MODELS = []
def make_folds():
    if FOLD_MODELS: return
    for f in range(NFOLD):
        tr = [(x, home_distinct[x][0], home_distinct[x][1]) for x in home_distinct if FOLD[x] != f]
        ms, C = build_models(tr)
        FOLD_MODELS.append(ms)
    log(f'built {NFOLD} fold models on home texts ({len(home_distinct)} distinct home texts, {len(GV)} usable signs)')


def runs_of(tok):
    """maximal runs of usable signs (indices into GV) in a token tuple."""
    out, cur = [], []
    for s in tok:
        if real(s) and s in GIDX: cur.append(GIDX[s])
        else:
            if cur: out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def edge_ok(tok):
    """True if every token is a usable sign (no lost, unclear, unseen): edges can be scored."""
    return all(real(s) and s in GIDX for s in tok)


def score_with(models, tok, kind, clean):
    """per-transition bits (n x 4), start bits (4) and end bits (4) (nan unless clean and fully usable), per model in NMODEL."""
    rs = runs_of(tok)
    tr = []
    for r in rs:
        for a, b in zip(r, r[1:]):
            tr.append([-np.log2(models[nm].get(kind).trans[a, b]) for nm in NMODEL])
    tr = np.array(tr).reshape(-1, len(NMODEL))
    st = np.full(len(NMODEL), np.nan); en = np.full(len(NMODEL), np.nan)
    first_bits = np.full(len(NMODEL), np.nan)
    if clean and edge_ok(tok) and len(tok) >= 1:
        ids = [GIDX[s] for s in tok]
        st = np.array([-np.log2(models[nm].get(kind).start[ids[0]]) for nm in NMODEL])
        en = np.array([-np.log2(models[nm].get(kind).end[ids[-1]]) for nm in NMODEL])
    return tr, st, en


class Scored:
    """one text with its scores. bits arrays are per transition (rows) by model (columns)."""
    __slots__ = ('tok', 'kind', 'ag', 'id', 'n_sign', 'n_step', 'tr', 'st', 'en', 'intact', 'meta')
    def __init__(self, tok, kind, ag, id_, tr, st, en, intact, meta=None):
        self.tok, self.kind, self.ag, self.id = tok, kind, ag, id_
        self.n_sign = sum(1 for s in tok if real(s)); self.n_step = len(tr)
        self.tr, self.st, self.en, self.intact = tr, st, en, intact; self.meta = meta or {}


def score_home_pool():
    """every home distinct text scored by the model that did not see it."""
    make_folds()
    pool = []
    for x, (c, k, ag, r, st_, i) in home_distinct.items():
        if not x: continue
        tr, st, en = score_with(FOLD_MODELS[FOLD[x]], x, k, c)
        pool.append(Scored(x, k, ag, i, tr, st, en, bool(c and edge_ok(x)), dict(round=r, site=st_)))
    return pool


def score_foreign(row):
    """a foreign face scored by all folds, averaged."""
    make_folds()
    trs, sts, ens = [], [], []
    for ms in FOLD_MODELS:
        tr, st, en = score_with(ms, row.tok, row.kind, row.clean)
        trs.append(tr); sts.append(st); ens.append(en)
    tr = np.mean(trs, 0) if len(trs[0]) else trs[0]
    return Scored(row.tok, row.kind, row.ag, row.id, tr, np.mean(sts, 0), np.mean(ens, 0), bool(row.clean and edge_ok(row.tok)),
                  dict(round=row._asdict().get('round', False) if hasattr(row, '_asdict') else False, site=row.site))


def pool_index(pool):
    """lookup (kind, ag, n_step) -> list of pool indices; usable only for texts with >= 1 step."""
    by = collections.defaultdict(list)
    for j, t in enumerate(pool):
        if t.n_step >= 1: by[(t.kind, t.ag, t.n_step)].append(j)
    return by


def candidates(by, pool, kind, ag, nstep, minc=5):
    """candidate pool indices by the widening rule; returns (list, level) level 0 exact, 1 length +-1, 2 animal dropped, 3 kind dropped."""
    c = list(by.get((kind, ag, nstep), []))
    if len(c) >= minc: return c, 0
    c = [j for n in (nstep - 1, nstep, nstep + 1) for j in by.get((kind, ag, n), [])]
    if len(c) >= minc: return c, 1
    c = [j for (k2, a2, n2), L in by.items() if k2 == kind and abs(n2 - nstep) <= 1 for j in L]
    if len(c) >= minc: return c, 2
    c = [j for (k2, a2, n2), L in by.items() if abs(n2 - nstep) <= 1 for j in L]
    return c, 3


def matched_draws(pool, by, subjects, ndraw=2000, seed=1, shape_rule=None):
    """subjects: list of Scored foreign texts (n_step >= 1). returns (index array ndraw x len(subjects), levels)."""
    rng = np.random.default_rng(seed)
    cand = []; levels = []
    for s in subjects:
        c, lv = candidates(by, pool, s.kind, s.ag, s.n_step)
        if shape_rule is not None: c = [j for j in c if shape_rule(pool[j])] or c
        cand.append(np.array(c)); levels.append(lv)
    idx = np.stack([rng.choice(c, size=ndraw) for c in cand], 1)
    return idx, levels


def pooled_bits(texts, col):
    """total bits / total steps over a list of Scored texts for model column col."""
    n = sum(t.n_step for t in texts)
    return sum(t.tr[:, col].sum() for t in texts if t.n_step) / n if n else np.nan


def draws_bits(pool, idx, col):
    """pooled bits per step for each draw."""
    tb = np.array([t.tr[:, col].sum() if t.n_step else 0.0 for t in pool]); tn = np.array([t.n_step for t in pool])
    return tb[idx].sum(1) / tn[idx].sum(1)


def summarize(real_val, draws):
    lo, hi = np.percentile(draws, [2.5, 97.5])
    p_hi = (np.sum(draws >= real_val) + 1) / (len(draws) + 1)
    p_lo = (np.sum(draws <= real_val) + 1) / (len(draws) + 1)
    return dict(real=real_val, ctrl_mean=draws.mean(), ctrl_lo=lo, ctrl_hi=hi, diff=real_val - draws.mean(), P_real_higher=p_hi, P_real_lower=p_lo)


def foreign_rows(tiers=('core',)):
    return F[F.tier.isin(tiers)]


def shape_of(r):
    if r.kind != 'seal': return r.type or r.kind
    return 'round' if r['round'] else 'square'
