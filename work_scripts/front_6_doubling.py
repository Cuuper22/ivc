#!/usr/bin/env python3
"""FRONT job 6: doubling. Texts with two fronts, a front in the middle, and objects with two or more faces.  2026-11-17.

The catalogue has no line breaks inside a face, so 'second line' is tested as 'second face' (each face of a 2+ face
object is its own text), plus fronts standing inside one text.

Predictions, written before the numbers:
 P1  a front word standing inside a text (not first) is followed by its own slot (a restart: 861-002, 920-060 ...) in
     under a third of its inside uses; inside a text the front words are mostly something else (861 as a counted thing
     after a number: 003-861).
 P2  on objects with 2+ faces, a front on one face does NOT predict a front on the other (faces do not each restart
     with a front): same-object front pairs at chance against faces dealt among 2+ face objects of the same site and kind.
 P3  texts with two front units (front at start AND a restart inside) are rare: under 1% of fronted texts.
"""
from front_common import *

say = make_logger('log_6_doubling.txt')
rng = np.random.default_rng(6)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
C = copy_events(D[D.complete])

# ---------- front words inside a text
rows = []; inside = collections.Counter(); restart = collections.Counter(); prev = collections.defaultdict(collections.Counter)
two_units = []
for r in C.itertuples():
    t = r.tok
    for i in range(1, len(t)):
        if t[i] in F:
            inside[t[i]] += 1; prev[t[i]][t[i - 1]] += 1
            if i + 1 < len(t) and t[i + 1] in SLOT:
                restart[t[i]] += 1
                if r.front: two_units.append((r.signs, r.kind, r.site, r.cisi))
for f, n in inside.most_common():
    rows.append(dict(front=f, inside_uses=n, followed_by_slot=restart[f], share_restart=round(restart[f] / n, 2),
                     sign_before='; '.join(f'{k} {v}' for k, v in prev[f].most_common(6))))
IN = pd.DataFrame(rows); IN.to_csv(f'{OUTF}/f6_inside.csv', index=False)
say('\nFRONT WORDS INSIDE A TEXT (complete copy events):'); say(IN.to_string(index=False))
nf = int((C.front != '').sum())
say(f'\ntexts with a front at the start AND a front+slot restart inside: {len(two_units)} of {nf} fronted texts')
for x in two_units: say('   ', x)
# texts with any second front word
two_words = C[(C.front != '') & C.tok.map(lambda t: any(s in F for s in t[1:]))]
say(f'fronted texts with any second front word inside: {len(two_words)}: ' + ', '.join(two_words.signs.head(30)))
# 861 after a number: on what objects
ex = [(r.signs, r.kind) for r in C.itertuples() if any(r.tok[i] == '861' and r.tok[i - 1] in NUMS for i in range(1, len(r.tok)))]
say(f'\n861 right after a number: {len(ex)} texts; kinds {collections.Counter(k for _, k in ex)}; e.g. {[s for s, _ in ex[:12]]}')

# ---------- multi-face objects
M = D[D.first_ok].copy()
g = M.groupby('stone')
multi = [s for s, x in g if len(x) >= 2]
MM = M[M.stone.isin(multi)].copy()
MM['hasf'] = MM.front != ''
by = MM.groupby('stone').agg(n=('face', 'size'), nf=('hasf', 'sum'), site=('site', 'first'), kind=('kind', 'first'))
say(f'\nobjects with 2+ faces whose first sign is readable on 2+ faces: {len(by)}; kinds {by.kind.value_counts().to_dict()}')
def stat(h):
    t = pd.DataFrame({'stone': MM.stone.values, 'h': h}).groupby('stone').h.sum()
    return int((t >= 2).sum()), int((t >= 1).sum())
ob = stat(MM.hasf.values)
grp = (MM.site + '|' + MM.kind).values
null = np.array([stat(deal_within(MM.hasf.values, grp, rng).astype(bool)) for _ in range(3000)])
say(f'objects with a front on 2+ faces: {ob[0]} against {null[:, 0].mean():.2f} with faces dealt among 2+ face objects of '
    f'the same site and kind (P high {pval_hi(null[:, 0], ob[0]):.4f}, P low {pval_lo(null[:, 0], ob[0]):.4f}); objects '
    f'with a front on any face {ob[1]} against {null[:, 1].mean():.2f}')
rows = []
for s, x in MM[MM.stone.isin(by[by.nf >= 1].index)].groupby('stone'):
    rows.append(dict(stone=s, kind=x.kind.iloc[0], site=x.site.iloc[0], cisi=x.cisi.iloc[0], faces=' | '.join(x.signs),
                     fronted_faces=int(x.hasf.sum()), n_faces=len(x)))
MF = pd.DataFrame(rows); MF.to_csv(f'{OUTF}/f6_multiface_with_front.csv', index=False)
say(f'multi-face objects with a front: {len(MF)}; front on every face: {int((MF.fronted_faces == MF.n_faces).sum())}')
say(MF.groupby('kind').apply(lambda x: f'{len(x)} objects, all faces fronted {int((x.fronted_faces == x.n_faces).sum())}').to_string())
say('\nthe multi-face objects with a front on 2+ faces:')
say(MF[MF.fronted_faces >= 2].to_string(index=False))
say('\nsample of multi-face seals with one fronted face:')
say(MF[(MF.kind == 'seal') & (MF.fronted_faces == 1)].head(25).to_string(index=False))
