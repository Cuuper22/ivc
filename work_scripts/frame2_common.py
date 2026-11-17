#!/usr/bin/env python3
"""Shared kit for FRAME v2 (frame2_*.py). Everything in this docstring and in the code below was written on 2026-11-17
BEFORE any frame-v2 score was computed. It builds on frame_common.py (same data, same models, same decoy dealing).

FRAME v2 = the hand frame (v1) plus the three changes the machine found (jobs/out/frame_machine.md), as explicit sign sets:
  OPEN      front word (opener): v1 openers 820 861 817 920 692, plus the signs the likelihood moved into the front
            words: 880 824 545 091 550 360 556.
  SLOT      the slot right after a front word: 002 060 741 742 368 365 (machine class; likelihood backed 368 742 365 741).
  NUM_NAME  the tall two 032 (lives inside fish names).
  NUM_TALL  other full-height stroke numbers 031 033 034 035 036.
  NUM_SHORT short and stacked stroke numbers and the comb counts (every other v1 number sign).
  CLOSER    v1 ending signs that the machine files as closers (jar 740, spear 520, porters 151 154 155 158, and the rare
            v1 ending signs it does not file as after-jar titles).
  TITLE     the after-jar title: v1 ending signs the machine files after the jar (comb 400, man 090, 679, 565 and the
            rare ones in that class) plus 527 621 161 241 (likelihood backed the move).
  CREST     name front: v1 crests 235 803 140 806 plus the fish signs 220 231 233 240 226 222 243.
  THING     counted goods: v1 counted things plus the trees 390 405 406 407 (machine 'counted goods' class).
  AFTER_M   what follows a measure: 760 690 752 585 (machine 'after-measure' class).
  NAME_BACK name back / tag: the other v1 tag signs (100 482).
  MEASURE   v1 measures.  PLACE  v1 place or time words.  PERSONAL  everything else (personal name part).

GRAMMAR v2 = which class may follow which, BY OBJECT KIND: class transitions are learned per kind (seal, tag/sealing,
  tablet, copper tablet, pot; anything else uses the pooled table), backed off to the pooled table with weight BETA = 5
  pseudo-counts:  P_k(c'|c) = (n_k(c, c') + BETA * P_pool(c'|c)) / (n_k(c) + BETA). Sign emissions inside a class are
  pooled over kinds (add-0.5). Start and end the same way. The same kind grammar is also built for v1 and the machine
  classes, so every frame is compared both pooled and by kind.

STRICT PATTERNS v2 (regular expressions over the v2 class string, one text type each), fixed here:
  name text      (OPEN SLOT?)? NAMESIGN+ (CLOSER TITLE? | TITLE)        NAMESIGN = CREST PERSONAL NUM_* PLACE NAME_BACK
                                                                                 MEASURE AFTER_M THING
  count line     (OPEN SLOT?)? (NUM+ THING)+                            NUM = NUM_SHORT NUM_TALL NUM_NAME
  record         name text followed by a count line                    (NAMESIGN+ CLOSER TITLE? (NUM+ THING)+)
  measure line   (OPEN SLOT?)? MEASURE (AFTER_M|NUM)+ (CLOSER TITLE?)?
  title alone    CLOSER | TITLE                                         (one sign)
  front alone    OPEN SLOT?
  one picture    one sign of any class (copper tablets only)
  v1's strict pattern stays as written in frame_grammar.py.
"""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from frame_common import *            # d, M, pairs, HAND, models, HMM, gap_posteriors, freq_band, deal_within_bands
import numpy as np, pandas as pd

OUT2 = f'{ROOT}/work_data/frame'
BETA = 5.0
KINDS = ['seal', 'tag', 'mtab', 'ctab', 'pot']
KIND_PLAIN = {'seal': 'seals', 'tag': 'tags and sealings', 'mtab': 'tablets', 'ctab': 'copper tablets', 'pot': 'pots', 'other': 'other objects'}
cls_m = pd.read_csv(f'{OUT}/classes.csv', dtype=str).fillna('')
HMM10 = {s: c for s, c in zip(cls_m.sign, cls_m.hmm10) if s}
EXCH10 = {s: c for s, c in zip(cls_m.sign, cls_m.exchange10) if s}

OPEN = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556'}
SLOT = {'002', '060', '741', '742', '368', '365'}
NUM_TALL = {'031', '033', '034', '035', '036'}
TITLE_ADD = {'527', '621', '161', '241'}
CREST_ADD = {'220', '231', '233', '240', '226', '222', '243'}
TREES = {'390', '405', '406', '407'}
AFTER_M = {'760', '690', '752', '585'}
V2_CLASSES = ['OPEN', 'SLOT', 'CREST', 'PERSONAL', 'NUM_NAME', 'NUM_SHORT', 'NUM_TALL', 'MEASURE', 'AFTER_M', 'THING',
              'NAME_BACK', 'PLACE', 'CLOSER', 'TITLE']
V2_PLAIN = {'OPEN': 'front word', 'SLOT': 'after-front slot', 'CREST': 'name front (crest)', 'PERSONAL': 'name part',
            'NUM_NAME': 'tall two (in names)', 'NUM_SHORT': 'short number', 'NUM_TALL': 'tall number', 'MEASURE': 'measure',
            'AFTER_M': 'after-measure', 'THING': 'counted thing', 'NAME_BACK': 'name back', 'PLACE': 'place or time word',
            'CLOSER': 'closer', 'TITLE': 'after-jar title'}


def v2_of(s):
    h = HAND.get(s, 'PERSONAL')
    if s in OPEN: return 'OPEN'
    if s in SLOT: return 'SLOT'
    if s == '032': return 'NUM_NAME'
    if s in NUM_TALL: return 'NUM_TALL'
    if h == 'NUMBER': return 'NUM_SHORT'
    if s in TITLE_ADD: return 'TITLE'
    if h == 'END': return 'TITLE' if HMM10.get(s) == 'H10_8' else 'CLOSER'
    if s in AFTER_M: return 'AFTER_M'
    if s in TREES or h == 'THING': return 'THING'
    if h == 'CREST' or s in CREST_ADD: return 'CREST'
    if h == 'TAG': return 'NAME_BACK'
    if h == 'MEASURE': return 'MEASURE'
    if h == 'PLACE': return 'PLACE'
    return 'PERSONAL'


def kind_of(k):
    return k if k in KINDS else 'other'


# ------------------------------------------------------------------ kind-aware class grammar
def kind_counts(texts, idx):
    """texts: (tokens, clean, kind). returns pooled counts and per-kind counts (frame_common.counts format)."""
    C = counts(texts, idx)
    CK = {k: counts([t for t in texts if kind_of(t[2]) == k], idx) for k in KINDS}
    return C, CK


class KindModel:
    """one SeqModel per kind (KINDS + 'other' = pooled)."""
    def __init__(self, name, per_kind):
        self.name, self.per = name, per_kind

    def get(self, k):
        return self.per.get(kind_of(k), self.per['other'])


def class_model_kind(C, CK, cmap, name, vocab, beta=BETA, pooled_only=False):
    V = len(vocab)
    labs = sorted({cmap.get(s, 'UNSEEN') for s in vocab}); li = {c: i for i, c in enumerate(labs)}; K = len(labs)
    cid = np.array([li[cmap.get(s, 'UNSEEN')] for s in vocab])
    Z = np.zeros((V, K)); Z[np.arange(V), cid] = 1
    cu = C['uni'] @ Z
    em = (C['uni'] + 0.5) / ((cu + 0.5 * Z.sum(0))[cid])

    def rows_of(CC):
        cb = Z.T @ CC['big'] @ Z; ce = CC['en'] @ Z; cs = CC['st'] @ Z
        return np.concatenate([cb, ce[:, None]], 1), cs
    R0, S0 = rows_of(C)
    P0 = (R0 + 0.1) / (R0 + 0.1).sum(1, keepdims=True)
    st0 = (S0 + 0.1) / (S0.sum() + 0.1 * K)

    def mk(P, st):
        ctrans, cend = P[:, :K], P[:, K]
        return SeqModel(name, st[cid] * em, ctrans[cid][:, cid] * em[None, :], cend[cid])
    per = {'other': mk(P0, st0)}
    info = {'other': P0}
    for k in KINDS:
        if pooled_only: per[k] = per['other']; continue
        Rk, Sk = rows_of(CK[k])
        Pk = (Rk + beta * P0) / (Rk.sum(1, keepdims=True) + beta)
        stk = (Sk + beta * st0) / (Sk.sum() + beta)
        per[k] = mk(Pk, stk); info[k] = Pk
    m = KindModel(name, per); m.labs = labs; m.cid = cid; m.em = em; m.info = info
    return m


class FixedKind:
    """wrap a kind-blind SeqModel in the KindModel interface."""
    def __init__(self, m): self.name, self.m = m.name, m
    def get(self, k): return self.m


def mix_kind(a, b, w=0.5, name='mix'):
    per = {}
    for k in KINDS + ['other']:
        ma, mb = a.get(k), b.get(k)
        per[k] = SeqModel(name, w * ma.start + (1 - w) * mb.start, w * ma.trans + (1 - w) * mb.trans, w * ma.end + (1 - w) * mb.end)
    return KindModel(name, per)


def bits(model, lines, idx, use_end=True):
    """lines: list of (tokens, kind). bits per sign."""
    lp = 0.0; n = 0
    for x, k in lines:
        ids = [idx[s] for s in x]; lp += model.get(k).logprob(ids, use_end); n += len(ids)
    return -lp / n


def new_texts(idx):
    Mu = M[~M.partnered]
    cand = [(tuple(x), k) for x, c, k in zip(Mu.tok, Mu.complete_b, Mu.kind) if c and x and not (set(x) & UNK) and not any(s.startswith('X') for s in x)]
    return [(x, k) for x, k in cand if all(s in idx for s in x)], len(Mu), len(cand)


V2_NAMESIGN = '(?:CREST|PERSONAL|NUM_NAME|NUM_SHORT|NUM_TALL|PLACE|NAME_BACK|MEASURE|AFTER_M|THING)'
V2_NUM = '(?:NUM_SHORT|NUM_TALL|NUM_NAME)'
V2_FRONT = '(?:OPEN (?:SLOT )?)?'
V2_PATTERNS = collections.OrderedDict([
    ('count line', re.compile(rf'^{V2_FRONT}(?:(?:{V2_NUM} )+THING )+$')),
    ('name text', re.compile(rf'^{V2_FRONT}(?:{V2_NAMESIGN} )+(?:CLOSER (?:TITLE )?|TITLE )$')),
    ('record', re.compile(rf'^{V2_FRONT}(?:{V2_NAMESIGN} )+CLOSER (?:TITLE )?(?:(?:{V2_NUM} )+THING )+$')),
    ('measure line', re.compile(rf'^{V2_FRONT}MEASURE (?:(?:AFTER_M|{V2_NUM}) )+(?:CLOSER (?:TITLE )?)?$')),
    ('title alone', re.compile(r'^(?:CLOSER|TITLE) $')),
    ('front alone', re.compile(r'^OPEN (?:SLOT )?$')),
])
V1_RE = re.compile(r'^(OPENER( NUMBER| JOINER)? )?(CREST )?((PERSONAL|PLACE|THING|NUMBER) )*(TAG )?END( END)?$')


def v2_type(classes, kind=None):
    """the first v2 strict pattern a class sequence fits, or ''. One-sign copper-tablet texts = 'one picture'."""
    s = ' '.join(classes) + ' '
    for nm, rx in V2_PATTERNS.items():
        if rx.match(s): return nm
    if kind == 'ctab' and len(classes) == 1: return 'one picture'
    return ''


def v1_fits(hjobs):
    return bool(V1_RE.match(' '.join(hjobs)))
