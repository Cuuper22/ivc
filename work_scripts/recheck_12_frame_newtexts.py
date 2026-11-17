#!/usr/bin/env python3
"""Recheck 12: frame scores on the "482 new texts" (frame2_score.py) and the 77 gap-test texts. Is any text counted
twice through two faces or two catalogues?

Plain words: NEW TEXTS = lines of the second catalogue (Mahadevan 1977) whose text has no partner text in the first
catalogue (Lipi), used as unseen test texts. A new text can still be (a) a repeat of another new line (two faces of
one object, two lines of one face, moulded copies), or (b) a RE-TRANSCRIPTION of a stone that IS in the first
catalogue, read with one sign different (then the frame was built on that stone). BITS PER SIGN = how many yes/no
questions a model needs per sign to guess the text; lower is better. DECOY = the frame's classes dealt among signs of
the same frequency band (20 seeds).
(b) is decided per line: same site, same length, and equal to some first-catalogue face at every position but one
(lost signs count as matching anything). Chance of such a near-match for a text that is really new is measured on the
first catalogue itself: first-catalogue texts that have a near-match on a DIFFERENT stone of the same site.
Clean run: new texts with repeats counted once and near-matches removed, then unigram, sign-pair, frame v2 base and
its 20 decoys rescored.
Run: python3 recheck_12_frame_newtexts.py   (several minutes; run in the background)
"""
import sys, io, contextlib, collections
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from recheck_common import log_to, OUT, stone_map, ROOT
say = log_to(f'{OUT}/r12_log.txt')
with contextlib.redirect_stdout(io.StringIO()):
    from frame2_common import *
import numpy as np, pandas as pd
say('[1/4] building the training model (as frame2_score.py)')
c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
V2 = dict(zip(c2.sign, c2.v2_base))
T = train_texts(); vocab, idx = vocab_of(T)
C, CK = kind_counts(T, idx)
uni = unigram_model(C); big = bigram_model(C)
NEW, nMu, ncand = new_texts(idx)
say(f'  new texts scored: {len(NEW)} (old report: 482)')

say('[2/4] repeats and re-transcriptions')
Mu = M[~M.partnered]
rows = [(tuple(x), k, tn, sl) for x, c, k, tn, sl in zip(Mu.tok, Mu.complete_b, Mu.kind, Mu.textnum, Mu.site_l)
        if c and x and not (set(x) & UNK) and not any(s.startswith('X') for s in x) and all(s in idx for s in x)]
assert len(rows) == len(NEW)
strs = collections.Counter(r[0] for r in rows)
same_obj = collections.Counter((r[0], r[2]) for r in rows)
say(f'  lines whose exact string occurs on another new line: {sum(c for c in strs.values() if c > 1)} lines, {sum(1 for c in strs.values() if c > 1)} strings; '
    f'repeats inside one object (same textnum): {sum(c - 1 for c in same_obj.values() if c > 1)}')
f2s, _ = stone_map()
L = d[[bool(x) for x in d.tok]][['id', 'site', 'tok']].copy(); L['stone'] = L.id.map(f2s)
bysite = collections.defaultdict(list)
for s, t, st in zip(L.site, L.tok, L.stone): bysite[(s, len(t))].append((t, st))
def near(t, site, own=None):
    # strict: 3+ signs, both strings fully legible, exactly one position different
    if len(t) < 3 or '000' in t: return False
    for u, st in bysite.get((site, len(t)), []):
        if own is not None and st == own: continue
        if '000' in u: continue
        if sum(1 for a, b in zip(t, u) if a != b) == 1: return True
    return False
nm = [near(r[0], r[3]) for r in rows]
say(f'  new lines with a first-catalogue face at the same site, same length (3+ signs, all legible), exactly one sign different: {sum(nm)} of {len(rows)} ({np.mean(nm):.0%})')
Ls = L[L.tok.map(lambda t: '000' not in t)].drop_duplicates(['site', 'tok'])
base = [near(t, s, st) for t, s, st in zip(Ls.tok, Ls.site, Ls.stone)]
say(f'  chance level: first-catalogue texts with such a near-match on another stone of the same site: {np.mean(base):.0%} of {len(base)}')
pd.DataFrame([dict(text='-'.join(r[0]), kind=r[1], textnum=r[2], site=r[3], near_first_catalogue=n) for r, n in zip(rows, nm)]).to_csv(f'{OUT}/r12_newtexts.csv', index=False)

say('[3/4] rescoring')
band = freq_band({s: int(C['uni'][idx[s]]) for s in vocab})
def score(lines, label, pooled):
    u = bits(FixedKind(uni), lines, idx); b = bits(FixedKind(big), lines, idx)
    m = class_model_kind(C, CK, {s: V2.get(s, 'UNSEEN') for s in vocab}, 'v2', vocab, pooled_only=pooled)
    x = bits(m, lines, idx); dec = []
    for q in range(500, 520):
        dm = deal_within_bands({s: V2[s] for s in vocab if s in V2}, band, q)
        dec.append(bits(class_model_kind(C, CK, {s: dm.get(s, 'UNSEEN') for s in vocab}, 'decoy', vocab, pooled_only=pooled), lines, idx))
    dec = np.array(dec); sh = lambda v: (u - v) / (u - b)
    say(f'  {label} [{"pooled" if pooled else "by kind"}]: {len(lines)} lines | frequency {u:.3f}, sign pairs {b:.3f}, frame v2 {x:.3f} (share {sh(x):.1%}); decoys mean {dec.mean():.3f}, '
        f'best {dec.min():.3f}, {int((dec <= x).sum())} of 20 at or below the frame')
    return dict(n=len(lines), uni=u, big=b, v2=x, share=sh(x), dec_mean=dec.mean(), dec_best=dec.min(), dec_beat=int((dec <= x).sum()))
r0 = [score(NEW, 'A  as run', p) for p in (True, False)]
seen = set(); NEW1 = []
for (x, k, tn, sl), n_ in zip(rows, nm):
    if (x, k) in seen: continue
    seen.add((x, k)); NEW1.append((x, k))
r1 = [score(NEW1, 'B  repeats counted once', p) for p in (True, False)]
seen = set(); NEW2 = []
for (x, k, tn, sl), n_ in zip(rows, nm):
    if n_ or (x, k) in seen: continue
    seen.add((x, k)); NEW2.append((x, k))
r2 = [score(NEW2, 'C  repeats once and near-matches of first-catalogue faces removed', p) for p in (True, False)]

say('[4/4] the 77 gap-test items')
mah2lipi = dict(zip(M.reading_mah, M.tok))
items = []; seen = set(); dirs = collections.Counter()
for g, lt, mt in zip(pairs.group, pairs.lipi_text, pairs.mahadevan_text):
    Lt = tuple(lt.split('-')); Mt = mah2lipi.get(mt)
    if Mt is None or len(Lt) != len(Mt): continue
    for side, (gapped, full_) in (('lipi gapped', (Lt, Mt)), ('second gapped', (Mt, Lt))):
        lost = [i for i, s in enumerate(gapped) if s == '000']
        if len(lost) != 1 or set(full_) & UNK or any(s.startswith('X') for s in full_): continue
        p = lost[0]
        if any(gapped[i] != full_[i] for i in range(len(Lt)) if i != p): continue
        key = (gapped, full_[p])
        if key in seen: continue
        seen.add(key); items.append((lt, gapped, p, full_[p], '-'.join(full_))); dirs[side] += 1
ans = collections.Counter(it[4] for it in items)
lip = collections.Counter(it[0] for it in items)
say(f'  items {len(items)} ({dict(dirs)}); answers shared by 2+ items: {sum(c for c in ans.values() if c > 1)} items on {sum(1 for c in ans.values() if c > 1)} answer texts; '
    f'first-catalogue texts giving 2+ items: {sum(c for c in lip.values() if c > 1)}')
import json
json.dump(dict(as_run=r0, repeats_once=r1, clean=r2, near_share=float(np.mean(nm)), near_chance=float(np.mean(base))), open(f'{OUT}/r12.json', 'w'), indent=1)
say('done')
