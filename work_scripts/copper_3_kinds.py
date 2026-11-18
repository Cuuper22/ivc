#!/usr/bin/env python3
"""COPPER step 3: what the text side is, by frame v2 jobs, and which kinds go with which pictures; what the count lines
count, against the Harappa clay tablets ('chits').

TEXT KIND (copper_common.text_kind): one sign / name+closer / record (name + closer + count after) / name+count (no
closer) / count line / name. COUNTED THING: the sign next to a number run whose job is THING or MEASURE, or the cup 700.
PICTURE GROUP of a set: an animal / a motif (knot, loop) / a human figure / one sign on the picture face / text on both
faces / unknown.

Predictions written 2026-11-17 before the numbers:
 P3.1 Name+closer is the commonest kind on copper, over 40% of distinct texts and over half of copies.
 P3.2 Count lines on copper count different things from the Harappa chits: the cup 700 (the chits' main counted thing,
      on about half of Harappa tablets) is on under 5% of copper texts, while the big measure 705/706 and the tree signs
      407/405 carry most copper counts.
 P3.3 Sets whose text carries a count (record, name+count) go with picture-face signs and two-text tablets more often
      than plain name+closer sets do (the count tablets are the 'account' end, the name sets the 'token' end).
Writes work_data/copper/kinds.csv, counted.csv, log_3.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_3.txt')
S = pd.read_csv(f'{OUT}/sets.csv', dtype=str).fillna('')
S['copies'] = S.copies.astype(int)
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
S = S[~S.text.str.contains('000') & ~S.text.str.contains('X')]
ANIMAL = {'stag', 'hare', 'goat', 'elephant', 'tiger', 'rhinoceros', 'buffalo', 'gaur', 'unicorn', 'spotted composite',
          'striped horned beast', 'composite beast', 'marked-body beast', 'bull'}
def group(t):
    a = L[L.set_text == t]
    ps = [p for p in a.pic if p]
    if not ps: return 'unknown'
    c = collections.Counter('animal' if p in ANIMAL else 'motif' if p in ('knot', 'loop motif') else
                            'human figure' if p == 'human figure' else 'picture-face sign' if p.startswith('sign') else
                            'text both faces' if p.startswith('no picture') else 'unknown' for p in ps)
    if c.get('picture-face sign') and c.get('animal'): return 'animal, some copies a sign'
    if c.get('picture-face sign') and c.get('human figure'): return 'figure, some copies a sign'
    return c.most_common(1)[0][0]
S['pgroup'] = S.text.map(group)
kc = S.groupby('kind').agg(texts=('text', 'count'), copies=('copies', 'sum'))
kc['share_texts'] = (kc.texts / kc.texts.sum()).round(3); kc['share_copies'] = (kc.copies / kc.copies.sum()).round(3)
say('text kinds on copper (distinct complete texts, union copies):\n' + kc.to_string())
ct = pd.crosstab(S.kind, S.pgroup, values=S.copies, aggfunc='sum').fillna(0).astype(int)
say('copies by kind x picture group:\n' + ct.to_string())
ctt = pd.crosstab(S.kind, S.pgroup)
say('texts by kind x picture group:\n' + ctt.to_string())
S.to_csv(f'{OUT}/kinds.csv', index=False)

# P3.3: count-carrying sets vs picture-face sign / text both faces
cnt = S.kind.isin(['record', 'name+count', 'count line'])
alt = S.pgroup.isin(['picture-face sign', 'text both faces', 'animal, some copies a sign', 'figure, some copies a sign'])
from scipy.stats import fisher_exact
tab = [[(cnt & alt).sum(), (cnt & ~alt).sum()], [(~cnt & alt).sum(), (~cnt & ~alt).sum()]]
say(f'P3.3 texts with a count: sign-or-text on the other face {tab[0][0]} of {sum(tab[0])}; without a count {tab[1][0]} of {sum(tab[1])}; '
    f'Fisher P (more) {fisher_exact(tab, alternative="greater")[1]:.4f}')

# ---------------- counted things, copper against Harappa clay tablets and Mohenjo-daro seals
def counted(tok):
    out = []
    R = runs(list(tok))
    for a, b, v, ser in R:
        for k in (b, a - 1):
            if 0 <= k < len(tok) and (job(tok[k]) in ('THING', 'MEASURE') or tok[k] == '700'):
                out.append((tok[k], v, ser)); break
    return out
def table(rows_tok, label, dedup=True):
    seen = set(); c = collections.Counter(); n = 0; withc = 0
    for t in rows_tok:
        if dedup and t in seen: continue
        seen.add(t); n += 1
        cc = counted(t)
        if cc: withc += 1
        for s, v, ser in cc: c[s] += 1
    say(f'{label}: distinct texts {n}, with a count {withc} ({withc / max(n, 1):.3f}); counted things: {c.most_common(12)}')
    return c, n, withc
cop = [tuple(t.split('-')) for t in S.text]
ob = objs.copy()
har = [tuple(f) for o in ob[(ob.site == 'Harappa') & (ob.kind == 'mtab')].itertuples() for f in o.faces if '000' not in f]
mdt = [tuple(f) for o in ob[(ob.site == 'Mohenjo-daro') & (ob.kind == 'mtab')].itertuples() for f in o.faces if '000' not in f]
mds = [tuple(f) for o in ob[(ob.site == 'Mohenjo-daro') & (ob.kind == 'seal')].itertuples() for f in o.faces if '000' not in f]
cc, n1, w1 = table(cop, 'Mohenjo-daro copper tablets (text faces)')
# all copper faces including second faces
allc = [tuple(f) for o in ob[(ob.site == 'Mohenjo-daro') & (ob.kind == 'ctab')].itertuples() for f in o.faces if '000' not in f]
ca, na, wa = table(allc, 'Mohenjo-daro copper tablets (all faces)')
hc, n2, w2 = table(har, 'Harappa clay tablets (faces)')
tc, n3, w3 = table(mdt, 'Mohenjo-daro clay tablets (faces)')
sc, n4, w4 = table(mds, 'Mohenjo-daro seals (faces)')
rows = []
for s in sorted(set(ca) | set(hc) | set(tc) | set(sc), key=lambda s: -(ca[s] + hc[s])):
    rows.append(dict(sign=s, job=job(s), copper_faces=ca[s], copper_share=round(ca[s] / max(wa, 1), 3), harappa_tab=hc[s],
                     harappa_share=round(hc[s] / max(w2, 1), 3), md_clay_tab=tc[s], md_seal=sc[s]))
C = pd.DataFrame(rows); C.to_csv(f'{OUT}/counted.csv', index=False)
say('counted things side by side (share = of faces with a count):\n' + C.head(20).to_string(index=False))
say('--- per object face (every copy counted):')
ca2, na2, wa2 = table(allc, 'Mohenjo-daro copper tablets, all faces, every copy', dedup=False)
hc2, n22, w22 = table(har, 'Harappa clay tablets, every face', dedup=False)
for s in ('700', '705', '706', '407', '390', '156'):
    say(f'  sign {s}: copper {ca2[s]}/{wa2} faces with a count, Harappa tablets {hc2[s]}/{w22}, Fisher P {fisher_exact([[ca2[s], wa2 - ca2[s]], [hc2[s], w22 - hc2[s]]])[1]:.2g}')
say('--- per distinct text:')
for s in ('700', '705', '706', '390', '405', '407', '156'):
    a, b = ca[s], hc[s]
    t = [[a, wa - a], [b, w2 - b]]
    say(f'  sign {s}: copper {a}/{wa}, Harappa tablets {b}/{w2}, Fisher P two-sided {fisher_exact(t)[1]:.2g}')
