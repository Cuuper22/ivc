#!/usr/bin/env python3
"""Shared loaders for the Mahadevan 1977 concordance (second catalogue) and the Lipi catalogue.

Mahadevan lines are stored in reading order (S1 first read). Site comes from the text-number range
(Mahadevan codebook 1: 1001-3513 Mohenjo-daro, 4001-5601 Harappa, 6104-6405 Chanhu-daro, 7001-7301 Lothal,
8001-8302 Kalibangan, 9001-9701 other sites, 9801-9905 West Asian finds). Object class = column inscobj
(codebook 2). Picture (field symbol) = column fs80, read as code + one sub-type digit (see field_symbol()).
"""
import sys, os, collections
import pandas as pd
ROOT = '/home/claude/ivc'
sys.path.insert(0, f'{ROOT}/work_scripts')
MAH = f'{ROOT}/research/data/mahadevan_20260905/concordance_rows.csv'
S = [f'S{i}' for i in range(1, 15)]
OBJ = {'1': 'seal', '2': 'sealing', '3': 'miniature tablet', '4': 'pottery graffito', '5': 'copper tablet',
       '6': 'bronze implement', '7': 'ivory/bone rod', '9': 'miscellaneous'}
SITES = ['MD', 'HP', 'CD', 'LL', 'KB', 'OS', 'WA']


def mah_site(t):
    t = int(t)
    if t < 4000: return 'MD'
    if t < 6000: return 'HP'
    if t < 7000: return 'CD'
    if t < 8000: return 'LL'
    if t < 9000: return 'KB'
    if t < 9800: return 'OS'
    return 'WA'


def lipi_site(site, region):
    if site == 'Mohenjo-daro': return 'MD'
    if site == 'Harappa': return 'HP'
    if site == 'Chanhu-daro': return 'CD'
    if site == 'Lothal': return 'LL'
    if site == 'Kalibangan': return 'KB'
    if region in ('Persian Gulf', 'Mesopotamia', 'Iranian Plateau', 'Central Asia'): return 'WA'
    return 'OS'


def field_symbol(fs):
    """fs80 -> (code, subtype). '13' -> ('01','3'); '831' -> ('83','1'); '910' -> ('91','0'); '0' -> none."""
    fs = str(fs)
    if fs in ('0', ''): return (None, None)
    return (fs[:-1].zfill(2), fs[-1])


def load_mah():
    """One row per non-empty line. toks = tuple of ints (0 = lost) in reading order; dbt = positions marked doubtful."""
    d = pd.read_csv(MAH, dtype=str, keep_default_na=False)
    rows = []
    for _, r in d.iterrows():
        raw = [r[c] for c in S if r[c] != '']
        if not raw or r['dir'] == '0': continue
        toks = tuple(int(x.lstrip('*')) for x in raw)
        dbt = tuple(i for i, x in enumerate(raw) if x.startswith('*'))
        rows.append(dict(textnum=r.textnum, site=mah_site(r.textnum), cls=OBJ.get(r.inscobj, '?'), inscobj=r.inscobj,
                         fs=r.fs80, locus=r.locus, level=r.level, sideline=r.sideline, dir=r.dir, toks=toks, dbt=dbt,
                         complete=(0 not in toks and len(toks) == int(r.signnum or 0) and int(r.posnum or 0) == len(toks)),
                         n=len(toks)))
    return pd.DataFrame(rows)


def load_lipi():
    from gloss import load
    d = load()
    d['gsite'] = [lipi_site(s, r) for s, r in zip(d.site, d.region)]
    d['broken'] = ['broken' in f for f in d.flg]
    return d
