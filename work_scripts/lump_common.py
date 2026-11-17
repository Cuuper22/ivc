#!/usr/bin/env python3
"""Shared loader for the LUMPS job (lump_*.py).  Written 2026-11-17, before any lump count was made.

Plain words
- LUMP: one clay sealing with 2+ impressions (see lump_1_build.py).  One row per lump here.
- Counting rules (FRAME.md "How pairs are counted"): one row per physical object; a lump's impressions are never paired
  across lumps; a Mahadevan lump that is also a Lipi lump is kept once (dup_of); lumps with the same site, locus and set of
  impression texts (a batch of identical lumps found together) are kept once; impressions of one lump with identical text are
  one stamp; chance is dealt among lumps of the same site (all are clay sealings, so the same object kind).
- STRATUM A, lumps proper: no impression is a cup-count face.  STRATUM B, name + cup-count objects: some impression is a cup
  (sign 700) with a count.  Harappa's second-catalogue "sealings" are 119 of 146 of this kind and 34 match Lipi moulded tablets
  (tablets, not lumps) one for one, so B is reported on its own and never pooled with A.
- Roles are those of lump_1_build.py (name / short / other / unreadable).
"""
import sys, os
import numpy as np, pandas as pd
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/lumps'
SLOT = {'002', '060', '741', '742', '368', '365'}
OPEN = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556', '347', '201', '263'}


def wild(x): return x in ('000', 'ALT') or x.startswith('X')


def sset(s): return [x for x in s.split('-') if x and not wild(x)] if isinstance(s, str) else []


def load_lumps():
    I = pd.read_csv(f'{OUT}/impressions.csv', dtype=str).fillna('')
    n0 = I.lump.nunique()
    TAG = os.environ.get('LUMP_VARIANT', 'base')   # base | nodup | lenient | both
    if TAG in ('nodup', 'both'): pass            # keep Mahadevan lumps that overlap Lipi (upper bound, some lumps counted twice)
    else: I = I[I.dup_of == '']
    if TAG in ('lenient', 'both'):               # a damaged text of 3+ signs with no closer left is allowed to be a name stamp
        I = I.copy(); I.loc[(I.role == 'other') & (I.text.str.split('-').map(len) >= 3), 'role'] = 'name'
    n1 = I.lump.nunique()
    keep = I.drop_duplicates('lump').drop_duplicates('batch').lump
    I = I[I.lump.isin(keep)]
    n2 = I.lump.nunique()
    I = I.drop_duplicates(['lump', 'text']).copy()           # same stone pressed twice = one stamp
    k = I.groupby('lump').size()
    I = I[I.lump.isin(k[k >= 2].index)].copy()               # two or more DIFFERENT impressions
    def cupf(t):
        x = t.split('-')
        if '700' in x and len(x) <= 3: return True
        # a tall-stroke count beside a lost sign: the cup sign is lost (033-000, 034-X46)
        return len(x) == 2 and ((x[0] in ('031', '032', '033', '034', '035', '036') and wild(x[1])) or (x[1] in ('031', '032', '033', '034', '035', '036') and wild(x[0])))
    I['cupface'] = [cupf(t) for t in I.text]
    cup = I.groupby('lump').cupface.any()
    I['stratum'] = I.lump.map(lambda l: 'B' if cup[l] else 'A')
    I['imp'] = I.imp.astype(int)
    steps = dict(all_lumps=n0, after_dup=n1, after_batch=n2, two_or_more_different=I.lump.nunique())
    return I, steps


def lump_table(I):
    """one row per lump: its name stamps and short stamps (lists of dicts)."""
    rows = []
    for l, g in I.groupby('lump', sort=False):
        g = g.sort_values('imp')
        rows.append(dict(lump=l, label=g.label.iloc[0], cat=g.cat.iloc[0], site=g.site.iloc[0], spot=g.spot.iloc[0],
                         stratum=g.stratum.iloc[0], stamps=g.to_dict('records'),
                         names=[r for r in g.to_dict('records') if r['role'] == 'name'],
                         shorts=[r for r in g.to_dict('records') if r['role'] == 'short' and not r['cupface']],
                         cups=[r for r in g.to_dict('records') if r['cupface']]))
    return pd.DataFrame(rows)


def deal(values, sites, rng):
    """shuffle `values` (list of objects) inside each site group; returns new list."""
    out = list(values); sites = np.asarray(sites)
    for s in np.unique(sites):
        ix = np.where(sites == s)[0]
        p = rng.permutation(ix)
        for a, b in zip(ix, p): out[a] = values[b]
    return out


def pvals(obs, null):
    null = np.asarray(null, dtype=float)
    return dict(obs=obs, chance=float(null.mean()), p_ge=float((1 + (null >= obs).sum()) / (len(null) + 1)),
                p_le=float((1 + (null <= obs).sum()) / (len(null) + 1)), n=len(null))
