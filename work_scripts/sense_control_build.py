#!/usr/bin/env python3
"""sense_control_build.py -- builds the CONTROL where meaning is known.
Source: the English translations of the example sentences that Wiktionary gives for Tamil, Telugu and Kannada words
(work_data/lang_m/raw/{Tamil,Telugu,Kannada}.jsonl: a real sentence with a human English translation). A sentence's words belong together by meaning.
Units = English content words (lowercased, reduced to a base form by WordNet 'morphy', stop words dropped, WordNet-known only).
A word's real multi-sense entry = its WordNet senses (up to 8, in WordNet's own order, one per sense: the first clause of the definition, at most 8 words;
category by the same rule as for the Indus senses: keyword lists first, else the WordNet file of that sense).
Job class = the word's part of speech (its first WordNet sense: noun/verb/adjective/adverb); frequency band = tercile of how many sentences carry the word.
Only words found in 2 or more sentences are kept (so a swap can mean something); texts need 2 or more distinct kept words.
Outputs work_data/sense/control_*.csv/json. Run: /tmp/senv/bin/python sense_control_build.py"""
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from sense_common import *
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/sense'
W = wn()
def log(*a): print('[sense_control_build]', *a, flush=True)
sents = set()
for lang in ('Tamil', 'Telugu', 'Kannada'):
    for l in open(f'{ROOT}/work_data/lang_m/raw/{lang}.jsonl'):
        j = json.loads(l)
        for s in j.get('senses', []):
            for e in s.get('examples', []) or []:
                t = (e.get('english') or e.get('translation') or '').strip()
                if t and len(t.split()) >= 3: sents.add(re.sub(r'\s+', ' ', t))
sents = sorted(sents); log('distinct English translations', len(sents))
SW = set('the a an and or but of to in on at by for with from as is are was were be been being it its this that these those i you he she we they me him her us them my your his our their who whom which what when where why how not no so if then than there here do does did have has had will would shall should can could may might must also very just into out up down over under about after before all any each both some such only own same too s t one two said say says'.split())
def base(t):
    for pos in ('n', 'v', 'a', 'r'):
        m = W.morphy(t, pos)
        if m: return m
    return None
texts = []
cnt = collections.Counter()
for s in sents:
    ws = []
    for t in re.findall(r"[a-z]+", s.lower()):
        if t in SW or len(t) < 3: continue
        b = base(t)
        if b and b not in SW and W.synsets(b): ws.append(b)
    ws = list(dict.fromkeys(ws))
    if len(ws) >= 2: texts.append(ws); cnt.update(ws)
keep = {w for w, c in cnt.items() if c >= 2}
texts = [[w for w in t if w in keep] for t in texts]; texts = [t for t in texts if len(t) >= 2]
cnt = collections.Counter(w for t in texts for w in t)
log('sentences with >=2 kept content words', len(texts), 'vocabulary', len(cnt))
# senses
POS = {'n': 'noun', 'v': 'verb', 'a': 'adj', 's': 'adj', 'r': 'adv'}
rows = []; wrows = []
fs = np.array(sorted(cnt.values())); q = np.quantile(list(cnt.values()), [1 / 3, 2 / 3])
for w, c in sorted(cnt.items()):
    ss = W.synsets(w)[:8]
    for i, sy in enumerate(ss):
        d = re.split(r'[;:]', sy.definition())[0]
        d = re.sub(r'\([^)]*\)', ' ', d); d = ' '.join(d.split()[:8])
        ln = sy.lexname(); cat = LEX2CAT.get(ln) or ('action' if ln.startswith('verb.') else 'quality' if ln.startswith('adj') else '')
        pc = phrase_cats(d, use_wn=False)    # keyword lists on the definition as well
        cats = sorted(set([cat] if cat else []) | set(pc))
        rows.append(dict(word=w, sense=i, phrase=d, cats='|'.join(cats)))
    pos = POS.get(W.synsets(w)[0].pos(), 'noun')
    wrows.append(dict(word=w, cls=pos, band=0 if c < q[0] else 1 if c < q[1] else 2, count=c, nsenses=len(ss)))
pd.DataFrame(rows).to_csv(f'{OUT}/control_senses.csv', index=False)
pd.DataFrame(wrows).to_csv(f'{OUT}/control_words.csv', index=False)
json.dump(texts, open(f'{OUT}/control_texts.json', 'w'))
log('words', len(wrows), 'senses', len(rows), 'phrases unique', len(set(r['phrase'] for r in rows)), 'band cuts', q)
log('texts length mean %.2f' % np.mean([len(t) for t in texts]), 'max', max(len(t) for t in texts))
