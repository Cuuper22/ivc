#!/usr/bin/env python3
"""FRONT job 5: fronts on tablets and tags against fronts on seals; count-line seals; multi-stamp lumps.  2026-11-17.

Predictions, written before the numbers:
 P1  tablets and seals use two separate sets of first signs: of the signs that open 5+ complete tablet texts and stand
     first in 50%+ of their tablet uses ('tablet heads'), at most one is a seal front word, and the Harappa heading signs
     413 and 415 open under 2% of seal texts.
 P2  where a seal front word does open a tablet, the tablet text is a seal-like name text (front + name + jar) and NOT
     an amount line: seal front words on tablets are seal texts written on clay.
 P3  count-line seals and the short stamps on multi-stamp lumps use the seal set (861 817 820 with 002), not the
     tablet set.
"""
from front_common import *

say = make_logger('log_5_sets.txt')
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
R = copy_events(D[D.first_ok])
C = R[R.complete]

# ---------- first signs by kind
rows = []
for k in ['seal', 'tablet', 'copper', 'tag', 'pot']:
    g = C[C.kind == k]
    fc = g.tok.map(lambda t: t[0]).value_counts()
    uses = collections.Counter(s for t in g.tok for s in set(t))
    for s, n in fc.items():
        if n >= 5:
            rows.append(dict(kind=k, sign=s, first=int(n), uses=uses[s], share_first=round(n / uses[s], 2),
                             share_of_kind=round(n / len(g), 3), front_word=s in F,
                             v2=V2.get(s, 'PERSONAL')))
FS = pd.DataFrame(rows); FS.to_csv(f'{OUTF}/f5_first_signs_by_kind.csv', index=False)
for k in ['seal', 'tablet', 'tag', 'copper', 'pot']:
    g = FS[FS.kind == k].sort_values('first', ascending=False).head(18)
    say(f'\n{k}: commonest first signs (complete copy events {int((C.kind == k).sum())})')
    say(g[['sign', 'first', 'uses', 'share_first', 'share_of_kind', 'front_word', 'v2']].to_string(index=False))

heads_tab = FS[(FS.kind == 'tablet') & (FS.share_first >= 0.5)]
heads_seal = FS[(FS.kind == 'seal') & (FS.share_first >= 0.5)]
say(f'\ntablet heads (open 5+ complete tablet texts, first in 50%+ of tablet uses): {list(heads_tab.sign)}')
say(f'seal heads (same rule on seals): {list(heads_seal.sign)}')
say(f'shared: {sorted(set(heads_tab.sign) & set(heads_seal.sign))}; tablet heads that are front words: '
    f'{sorted(set(heads_tab.sign) & F)}')
for s in ('413', '415'):
    for k in ('seal', 'tablet'):
        g = C[C.kind == k]; n = int(g.tok.map(lambda t: t[0] == s).sum())
        say(f'  {s} opens {n} of {len(g)} complete {k} texts ({n/len(g):.3%})')

# ---------- seal front words on tablets: what the texts are
T = C[(C.kind == 'tablet') & (C.front != '')].copy()
def tk(r):
    if r.is_count: return 'front + count line'
    if not len(r.body): return 'front alone'
    if len(r.name) and r.has_closer: return 'front + name + closer'
    if all(s in NUMS or V2.get(s) in ('THING', 'MEASURE', 'AFTER_M') for s in r.body): return 'front + amount/measure'
    return 'front + other'
T['tk'] = [tk(r) for r in T.itertuples()]
say(f'\nseal front words opening complete tablet texts: {len(T)}')
say(pd.crosstab(T.unit.where(T.unit.isin(T.unit.value_counts().head(10).index), 'other'), T.tk).to_string())
say(f'by site: {T.site.value_counts().to_dict()}; moulded {int((T.type == "TAB:B").sum())}, incised {int((T.type == "TAB:I").sum())}')
S_ = C[(C.kind == 'seal') & (C.front != '')].copy(); S_['tk'] = [tk(r) for r in S_.itertuples()]
say('seals, same table: ' + str(S_.tk.value_counts().to_dict()))
# partner faces of fronted tablet faces
Dall = D.copy()
objs = Dall.groupby('stone')
rows = []
for r in T.itertuples():
    other = Dall[(Dall.stone == r.stone) & (Dall.face != r.face)]
    rows.append(dict(face=r.face, cisi=r.cisi, site=r.site, text=r.signs, kind=r.tk, partners=' | '.join(other.signs)))
TP = pd.DataFrame(rows); TP.to_csv(f'{OUTF}/f5_tablet_front_faces.csv', index=False)
withp = TP[TP.partners != '']
say(f'fronted tablet faces with a partner face: {len(withp)} of {len(TP)}; partner is an amount (number + cup/thing) on '
    f'{int(withp.partners.str.contains("700|705|706").sum())}')

# ---------- count-line seals and multi-stamp lumps
CL = C[(C.kind == 'seal') & C.is_count]
say(f'\ncount-line seals (complete copy events): {len(CL)}; with a front {int((CL.front != "").sum())}; fronts: '
    f'{CL[CL.front != ""].unit.value_counts().to_dict()}')
MS = pd.read_csv(f'{ROOT}/work_data/stamps/multistamp.csv', dtype=str, keep_default_na=False)
stamps = [s.strip() for t in MS.texts for s in t.split('|')]
fs = collections.Counter(); short = []
for s in stamps:
    x = s.split('-')
    if x and x[0] in F:
        fs['-'.join(x[:2])] += 1
        if len(x) <= 4: short.append(s)
say(f'multi-stamp lumps: {len(MS)} objects, {len(stamps)} stamps; stamps opening with a front word: {sum(fs.values())} {dict(fs)}')
say(f'short front stamps (4 signs or fewer): {short}')
# all impressions vs seals: front unit mix
for k in ('seal', 'tag'):
    g = R[(R.kind == k) & (R.front != '')]
    say(f'{k}: front units {g.unit.value_counts().head(10).to_dict()}')
# tablets in the 'heads' job: 413/415 never after a seal front word?
n = sum(1 for t in C.tok if len(t) > 1 and t[0] in F and t[1] in ('413', '415'))
say(f'texts where a seal front word is directly followed by 413 or 415: {n}')
