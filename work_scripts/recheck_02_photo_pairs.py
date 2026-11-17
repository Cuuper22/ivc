#!/usr/bin/env python3
"""Recheck 2: "different hands carved the shared sign: 24 pairs, 4 same hand" (jobs/out/photo_pairs_A.md, _B.md;
pair lists jobs/photo_pairs_0.txt to _3.txt).

Plain words: each listed PAIR is two seals from one house that share a sign; a photo judge said whether the sign is
on both stones and whether one hand cut both. Check: is any pair two faces, or two catalogue rows, of ONE stone
(same CISI number, same Lipi object, or merged by the stone rule in recheck_common.py), or two stones with an
identical full text (a possible double entry)?
Run: python3 recheck_02_photo_pairs.py   (seconds)
"""
import sys, re, glob
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from recheck_common import *
say = log_to(f'{OUT}/r02_log.txt')
d = faces(); f2s, _ = stone_map(d)
c2stone = {}
for cisi, fid in zip(d.cisi, d.id):
    if cisi not in EMPTY: c2stone.setdefault(cisi, set()).add(f2s[fid])
c2text = d.groupby('cisi').text.apply(lambda s: '|'.join(sorted(s))).to_dict()
c2exc = d.groupby('cisi')['excavation-idno'].first().to_dict()
rows = []
for f in sorted(glob.glob(f'{ROOT}/jobs/photo_pairs_[0-3].txt')):
    for ln in open(f):
        ids = re.findall(r'\|\s*(M-\d+|H-\d+|[A-Z][a-z]?-\d+) \(', ln)
        if len(ids) == 2: rows.append((f.split('_')[-1][0], ids[0], ids[1]))
say(f'pairs listed: {len(rows)}')
bad = 0
for fi, a, b in rows:
    sa, sb = c2stone.get(a, set()), c2stone.get(b, set())
    one = bool(sa & sb) or a == b
    same_text = c2text.get(a) == c2text.get(b)
    same_exc = c2exc.get(a) == c2exc.get(b) and c2exc.get(a) not in EMPTY
    if one or same_text or same_exc:
        bad += 1; say(f'  FLAG file {fi}: {a} + {b} one stone {one}, identical text {same_text}, same excavation number {same_exc}')
say(f'pairs that are one stone, or identical texts, or one excavation number: {bad} of {len(rows)}')
say(f'distinct stones in the list: {len({x for _, a, b in rows for x in (a, b)})}')
