#!/usr/bin/env python3
"""Shared loader for the odd-readings job (odd_*.py). Every face of the first catalogue (Lipi, 5,679) and the 'new texts'
(second-catalogue lines with no partner in the first, 1,183 lines, never used to choose a value), each with its tokens,
object kind, parse roles. Import: from odd_common import *"""
import sys, os, collections, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v4_common import d, M, lex, parse_face, CNT, ROOT, np, pd
from scipy.stats import binomtest
OUT = f'{ROOT}/work_data/odd'; os.makedirs(OUT, exist_ok=True)
SHORT_S = {'001','002','003','004','005','006','007'}
STACK = {'012','013','014','015','016','017','018'}
TALL = {'031','032','033','034','035','036'}
FISH = {'220','226','231','233','235','236','240','241'}
SEAL = {'seal'}
def stype(s): return 'short' if s in SHORT_S else 'stacked' if s in STACK else 'tall' if s in TALL else None
def val(s): return CNT[s][1] if s in CNT else None
def faces():
    """list of dicts: cat ('L' / 'Mu'), id, x (tokens), kind, site, roles (list), P (parse)"""
    out = []
    for i, x, k, st, P in zip(d.id, d.tok, d.kind, d.site, d.P):
        out.append(dict(cat='L', id=i, x=tuple(x), kind=k, site=st, P=P, roles=P['roles']))
    m = M[~M.partnered]
    for i, x, k, st, P in zip(m.textnum if 'textnum' in m else range(len(m)), m.tok, m.kind, m.site_l, m.P):
        out.append(dict(cat='Mu', id=str(i), x=tuple(x), kind=k, site=st, P=P, roles=P['roles']))
    return out
def pbin(k, n, p, alt='greater'):
    return binomtest(k, n, p, alternative=alt).pvalue if n else 1.0
