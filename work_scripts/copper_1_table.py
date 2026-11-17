#!/usr/bin/env python3
"""COPPER step 1: the full table of Mohenjo-daro copper tablets, joined into objects and grouped into sets.

Predictions written 2026-11-17 before any number below was computed:
 P1.1 The eye check will name a clear animal on about half the picture sides the catalogue left vague (Othr / blank / -),
      as the earlier check found (13 of 51).
 P1.2 Wherever a set has two or more legible copies, every legible copy shows the same picture (no set with two animals).
 P1.3 The second catalogue adds fewer than 15 copies beyond the first under the max-per-text rule (they are mostly the
      same tablets).
 P1.4 The register numbers (excavation numbers) of copies of one set fall close together far more often than numbers of
      copper tablets of different sets (tested in copper_6_spots.py; here only listed).

Writes work_data/copper/objects.csv (one row per first-catalogue object), m77_objects.csv (second catalogue), sets.csv
(one row per text: copies in each catalogue, union copies, pictures by source, picture-side signs, findspots, bins),
and log_1.txt.
"""
import sys; sys.path.insert(0, '/home/claude/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_1.txt')
say('loading the two catalogues')
L = load_L(); L = L[L.site == 'Mohenjo-daro'].copy()
Mm = load_M()
E = eye_table()
L = L.merge(E, on='cisi', how='left').fillna({'eye': '', 'eye_group': '', 'note': ''})

# ---------------- catalogue picture code to a plain group name (labels only)
CATG = {'Hare': 'hare', 'Elep': 'elephant', 'Anth': 'human figure', 'Comp': 'composite beast', 'Gaur': 'gaur', 'Goat': 'goat',
        'Loop': 'knot', 'Bull1': 'unicorn', 'Rhin': 'rhinoceros', 'Tigr': 'tiger', 'Bull': 'bull', 'Buff': 'buffalo', 'Hgls': 'loop motif'}
EYEG = {'archer': 'human figure', 'figure': 'human figure'}
def working(r):
    if r.eye_group and r.eye_group not in ('worn', 'text', 'sign'): return EYEG.get(r.eye_group, r.eye_group), 'eye'
    if r.picsign: return f'sign {r.picsign}', 'picture-face sign'
    if r.second: return 'no picture (text both faces)', 'second text face'
    if r.eye_group == 'sign': return 'sign (eye)', 'eye'
    if r.cat not in NOPIC: return CATG.get(r.cat, r.cat), 'catalogue'
    return '', ''
L['pic'], L['pic_src'] = zip(*[working(r) for r in L.itertuples()])

# ---------------- photo check summary
chk = L[L.eye != '']
say(f'photo check: {len(chk)} objects looked at')
vag = chk[chk.cat.isin(NOPIC)]
leg = vag[~vag.eye_group.isin(['worn', 'text', 'sign'])]
say(f'  catalogue code vague on {len(vag)}; of those the photo shows a clear picture on {len(leg)}, a sign on '
    f'{(vag.eye_group == "sign").sum()}, text on both faces {(vag.eye_group == "text").sum()}, too worn {(vag.eye_group == "worn").sum()}')
say('  P1.1 predicted about half named:', f'{len(leg)} of {len(vag)}')
spec = chk[~chk.cat.isin(NOPIC)]
legs = spec[~spec.eye_group.isin(['worn', 'text', 'sign'])]
agree = [(r.cisi, r.cat, r.eye_group) for r in legs.itertuples()]
say(f'  specific catalogue code with a legible picture: {len(legs)}; code vs eye: {agree}')

# ---------------- damaged texts join a set
full = sorted(set(L[L.complete].text))
def set_text(t):
    if '000' not in t: return t, 'exact'
    c = [f for f in full if fits(t, f)]
    return (c[0], 'damaged copy') if len(c) == 1 else (t, 'damaged, unplaced')
L['set_text'], L['set_how'] = zip(*[set_text(t) for t in L.text])
say(f'damaged texts: {(L.set_how != "exact").sum()}; placed into a set {(L.set_how == "damaged copy").sum()}')

# ---------------- second catalogue texts to first-catalogue set texts
Lt = sorted(set(L.set_text))
def mset(t):
    nL = L.set_text.value_counts()
    best = max(Lt, key=lambda f: (align_score(t, f), nL.get(f, 0))) if Lt else ''
    sc = align_score(t, best)
    if sc == 1 or (sc >= 0.75 and len(t.split('-')) >= 3): return best, sc
    if '000' in t:
        c = [f for f in Lt if fits(t, f)]
        if len(c) == 1: return c[0], 1
    return t, sc
Mm['set_text'], Mm['score'] = zip(*[mset(t) for t in Mm.text])
Mm['famname'] = Mm.fam.map(FAMILY).fillna('')
say(f'second catalogue copper objects: {len(Mm)}; matched to a first-catalogue text {(Mm.set_text.isin(Lt)).sum()}')

# ---------------- sets
rows = []
for t in sorted(set(L.set_text) | set(Mm.set_text)):
    a = L[L.set_text == t]; b = Mm[Mm.set_text == t]
    pics = collections.Counter(p for p in a.pic if p)
    eye = collections.Counter(p for p, s in zip(a.pic, a.pic_src) if s == 'eye')
    rows.append(dict(text=t, n_L=len(a), n_M=len(b), copies=max(len(a), len(b)), kind=text_kind(t.split('-')),
                     pic_eye=dict(eye), pic_all=dict(pics), cat_codes=dict(collections.Counter(a.cat)),
                     m77_codes=dict(collections.Counter(b.fs)), picsigns=dict(collections.Counter(p for p in a.picsign if p)),
                     m77_picsigns=dict(collections.Counter(p for p in b.picsign if p)),
                     second=dict(collections.Counter(p for p in a.second if p)),
                     findspots='; '.join(f'{r.cisi}:{r.area}|{r.bh}|{r.room}|{r.depth}|{r.exc}' for r in a.itertuples()),
                     bins=dict(collections.Counter(x for x in a.bin if x)),
                     m77_loci=dict(collections.Counter(b.locus))))
S = pd.DataFrame(rows).sort_values(['copies', 'text'], ascending=[False, True])
S.to_csv(f'{OUT}/sets.csv', index=False)
L.to_csv(f'{OUT}/objects.csv', index=False); Mm.to_csv(f'{OUT}/m77_objects.csv', index=False)
say(f'sets (distinct texts): {len(S)}; with 2+ copies {(S.copies >= 2).sum()}; objects first catalogue {len(L)}, '
    f'union copies {S.copies.sum()} (second catalogue adds {S.copies.sum() - len(L)})')
say('P1.3 predicted fewer than 15 added:', S.copies.sum() - len(L))
# P1.2 one picture per set by eye
mixed = [(r.text, r.pic_eye) for r in S.itertuples() if len(r.pic_eye) >= 2]
n2 = sum(1 for r in S.itertuples() if sum(r.pic_eye.values()) >= 2)
say(f'P1.2 sets with 2+ copies read by eye: {n2}; with two different pictures by eye: {len(mixed)} {mixed}')
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 70)
print(S[S.copies >= 2][['text', 'n_L', 'n_M', 'copies', 'kind', 'pic_all', 'm77_codes', 'picsigns', 'm77_picsigns', 'bins']].to_string())
