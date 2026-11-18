#!/usr/bin/env python3
"""Recheck 11: the 136 fixed phrases (phrases_1_list.py). Rule: a sign run that occurs in 8+ DISTINCT TEXTS (plus order
and lift rules). Question: distinct texts or distinct objects, and do moulded copies, damaged copies of one text, or two
faces of one stone inflate a phrase's count?

Plain words: DISTINCT TEXT (old) = distinct token string of one face. A damaged copy (one sign lost, written 000) of a
text is a different string, so one text and its damaged copies count as several. CLEAN COUNT for a phrase = number of
carrier texts after (a) strings that agree sign for sign wherever both are legible (same length) are merged as one text,
and (b) all faces of one stone count once. Also reported: number of COPY EVENTS = stones carrying the phrase, with all
stones of one site + area + full text counted once.
A phrase passes the count rule when the clean count is 8 or more (the order and lift rules do not depend on this).
Run: python3 recheck_11_phrases.py   (about 1 minute)
"""
import sys, io, contextlib, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r11_log.txt')
with contextlib.redirect_stdout(io.StringIO()):
    from phrases_common import d, find_in, is_sign
f2s, _ = stone_map()
PL = pd.read_csv(f'{ROOT}/work_data/phrases/phrase_list.csv', dtype=str).fillna('')
PL['n_texts'] = PL.n_texts.astype(int)
say(f'phrases in the list: {len(PL)}')
F = d[['id', 'obj', 'site', 'area-section', 'tok']].copy(); F = F[F.tok.map(len) > 0]
F['stone'] = F.id.map(f2s)
full = F.groupby('stone').tok.apply(lambda s: '|'.join(sorted('-'.join(t) for t in s)))
F['full'] = F.stone.map(full)

def compatible(a, b):
    return len(a) == len(b) and all(x == y or not is_sign(x) or not is_sign(y) for x, y in zip(a, b))

rows = []
for i, r in enumerate(PL.itertuples()):
    p = tuple(r.phrase.split('-'))
    car = F[F.tok.map(lambda t: find_in(t, p))]
    texts = list(dict.fromkeys(car.tok))                       # old unit
    # (a) merge strings that agree wherever both legible: greedy, most legible first
    texts_sorted = sorted(texts, key=lambda t: -sum(is_sign(x) for x in t))
    groups = []
    for t in texts_sorted:
        for g in groups:
            if compatible(g, t): break
        else: groups.append(t)
    # (b) a stone carries the phrase once: count text groups, but drop a group if every string in it comes only from
    #     stones that already gave another group (two faces of one stone)
    stone_groups = collections.defaultdict(set)
    gid = {}
    for t in texts:
        for k, g in enumerate(groups):
            if compatible(g, t): gid[t] = k; break
    for s, t in zip(car.stone, car.tok): stone_groups[s].add(gid[t])
    owner = {}
    for s, gs in stone_groups.items():
        gs = sorted(gs)
        for g in gs[1:]: owner.setdefault(g, set()).add(s)
    multi_only = [g for g in owner if all(len(stone_groups[s]) > 1 for s in
                  {s for s, t in zip(car.stone, car.tok) if gid[t] == g})]
    clean_n = len(groups) - len(multi_only)
    events = car.drop_duplicates('stone').drop_duplicates(['site', 'area-section', 'full']).shape[0]
    rows.append(dict(phrase=r.phrase, old_n_texts=r.n_texts, recount_strings=len(texts), merged_damaged=len(groups),
                     clean_n=clean_n, stones=car.stone.nunique(), copy_events=events, passes_clean=clean_n >= 8))
    if (i + 1) % 34 == 0: print(f'    {i + 1}/{len(PL)} phrases', flush=True)
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/r11_phrases.csv', index=False)
say(f'old count reproduced (strings) for {(R.recount_strings == R.old_n_texts).sum()} of {len(R)} phrases')
say(f'phrases still at 8+ texts after merging damaged copies of one text and counting each stone once: {int(R.passes_clean.sum())} of {len(R)}')
say(f'phrases with 8+ copy events (stones, copies in one spot once): {int((R.copy_events >= 8).sum())} of {len(R)}')
say('phrases that drop below 8:')
for r in R[~R.passes_clean].itertuples():
    say(f'   {r.phrase:18s} old {r.old_n_texts} texts -> clean {r.clean_n} (stones {r.stones}, copy events {r.copy_events})')
say(f'median loss per phrase: {np.median(R.old_n_texts - R.clean_n):.0f} texts; largest: '
    + ', '.join(f'{x.phrase} {x.old_n_texts}->{x.clean_n}' for x in R.assign(l=R.old_n_texts - R.clean_n).sort_values('l', ascending=False).head(5).itertuples()))
