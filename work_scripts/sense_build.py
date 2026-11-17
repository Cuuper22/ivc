#!/usr/bin/env python3
"""sense_build.py -- step 1: the sense list of every labelled sign's Dravidian word, and its categories.
Labelled signs = every row of work_data/values_master4.csv (strict, wide, testing: 195 signs).
Word = the Tamil-spelled word in the 'sound' column (marks '?' '-' dropped).
Sense list of a word = (in this order, duplicates dropped, at most MAXS = 25):
  1. the label's own English glosses (english + english_long columns of values_master4, split on ; , and brackets);
  2. every gloss phrase of DEDR-Tamil words spelled the same (accents/dots dropped, vowel length kept; work_data/lang_m/lex/dedr_tamil.tsv);
  3. every gloss phrase of the same word in Wiktionary Tamil (tamil_wiktionary.tsv);
  4. if the label cites DEDR entry numbers: all gloss phrases of that whole DEDR entry (all derived Tamil words of the etymon);
  5. if still nothing from 2-4: same spelling ignoring vowel length.
Outputs work_data/sense/signs.csv (sign -> word key, DEDR ids, class, band, faces), senses.csv (word key, sense number, phrase, categories).
Run: python3 sense_build.py"""
import sys, os, re, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from sense_common import *
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/sense'
MAXS = 25
def log(*a): print('[sense_build]', *a, flush=True)
V = pd.read_csv(f'{ROOT}/work_data/values_master4.csv', dtype=str).fillna('')
ded = pd.read_csv(f'{ROOT}/work_data/lang_m/lex/dedr_tamil.tsv', sep='\t', header=None, dtype=str, quoting=3).fillna('')
wik = pd.read_csv(f'{ROOT}/work_data/lang_m/lex/tamil_wiktionary.tsv', sep='\t', header=None, dtype=str, quoting=3).fillna('')
def nolen(k): return re.sub('[āēīōū]', lambda m: {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}[m.group()], k)
ded['k'] = ded[1].map(word_key); wik['k'] = wik[1].map(word_key)
ded['kn'] = ded.k.map(nolen); wik['kn'] = wik.k.map(nolen)
dby = ded.groupby('k'); wby = wik.groupby('k'); dn = ded.groupby('kn'); wn_ = wik.groupby('kn')
dentry = ded.groupby(0)
def phrases(df): return [p for g in df[4] for p in clean_gloss(g)]
rows = []; senses = {}
for r in V.itertuples():
    k = word_key(r.sound)
    if not k: continue
    lab = clean_gloss(r.english) + clean_gloss(r.english_long.replace(':', ','))
    if not lab: lab = [r.english.lower()]
    p2 = phrases(dby.get_group(k)) if k in dby.groups else []
    p3 = phrases(wby.get_group(k)) if k in wby.groups else []
    ids = [int(x) for x in re.findall(r'\d+', r.dedr)]
    p4 = []
    for i in ids:
        if str(i) in dentry.groups: p4 += phrases(dentry.get_group(str(i)))
    p5 = []
    if not (p2 or p3 or p4):
        kk = nolen(k)
        if kk in dn.groups: p5 += phrases(dn.get_group(kk))
        if kk in wn_.groups: p5 += phrases(wn_.get_group(kk))
    allp = []
    for p in lab + p2 + p3 + p4 + p5:
        if p not in allp: allp.append(p)
    allp = allp[:MAXS]
    src = f'label{len(lab)}/dedr{len(p2)}/wik{len(p3)}/entry{len(p4)}/fuzzy{len(p5)}'
    if k not in senses: senses[k] = (allp, src, r.sound, r.english)
    else:   # same word on several signs: keep the longer list
        if len(allp) > len(senses[k][0]): senses[k] = (allp, src, r.sound, r.english)
    rows.append(dict(sign=r.sign, word=k, sound=r.sound, english=r.english, status=r.status, dedr=r.dedr))
S = pd.DataFrame(rows)
log('labelled signs', len(S), 'distinct words', S.word.nunique())
sr = []
for k, (ps, src, snd, en) in senses.items():
    for i, p in enumerate(ps):
        sr.append(dict(word=k, sense=i, phrase=p, cats='|'.join(phrase_cats(p)), source=src))
SS = pd.DataFrame(sr)
n = SS.groupby('word').size()
log('senses per word: mean %.1f median %d min %d max %d' % (n.mean(), n.median(), n.min(), n.max()), '| words with 1 sense:', int((n == 1).sum()))
log('senses with at least one category: %.1f%%' % (100 * (SS.cats != '').mean()))
log('category counts:', {c: int(SS.cats.str.contains(c).sum()) for c in CATS})
# job class and frequency band
cl = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
cmap = dict(zip(cl.sign, cl.v2_base))
import json as _j
fc = collections.Counter()
for f in ('events_lipi',):
    for e in _j.load(open(f'{OUT}/{f}.json')):
        for fa in e['faces']:
            for s in set(fa): fc[s] += 1
S['cls'] = S.sign.map(lambda s: cmap.get(s, 'PERSONAL')); S['faces'] = S.sign.map(lambda s: fc.get(s, 0))
t = np.quantile(S.faces, [1 / 3, 2 / 3])
S['band'] = S.faces.map(lambda f: 0 if f < t[0] else 1 if f < t[1] else 2)
log('class counts', dict(S.cls.value_counts()), 'band cuts', t)
cells = S.groupby(['cls', 'band']).size()
log('class x band cells', len(cells), '| signs in cells of size >=2:', int(cells[cells >= 2].sum()), 'of', len(S))
S['nsenses'] = S.word.map(n)
S.to_csv(f'{OUT}/signs.csv', index=False); SS.to_csv(f'{OUT}/senses.csv', index=False)
