#!/usr/bin/env python3
"""FRONT job 1: the inventory of front words and after-front slot signs.  2026-11-17.

Predictions, written before the numbers:
 P1  the front is a seal thing: 20-35% of seal stones with a readable first sign begin with a front word; tablets under
     10%; copper under 5%; tags (impressions of seals) close to seals.
 P2  front + slot pairing is not free: each front word keeps one slot sign (861/817/824 -> 002, 920/692/550 -> 060),
     chi-square of the front x slot table far above slot signs dealt at random among front texts of the same site
     (P < 0.001), and the 'diamond' fronts never take 060.
 P3  the slot signs (002 060 741 742 368 365) stand right after a front word in most of their uses for 060/741/742/368,
     not for 002 (002 is also a number elsewhere).
Unit: one row per copy event (same site, same findspot, same full text = once) unless stated; stones counted once for
shares by object kind.
"""
from front_common import *

say = make_logger('log_1_inventory.txt')
rng = np.random.default_rng(1)
D = load(); F, uses, first, fslot = front_set(D, say); D = add_parse(D, F)
R = D[D.first_ok].copy()
E = copy_events(R)
say(f'faces {len(D)}, faces with readable first sign {len(R)}, copy events {len(E)}')

# ---------- A. front words
rows = []
allfaces_uses = collections.Counter()
for t in D.tok:
    for s in set(t): allfaces_uses[s] += 1
for f in sorted(F, key=lambda s: -(R.front == s).sum()):
    sub = R[R.front == f]; se = E[E.front == f]
    kinds = sub.groupby('kind').stone.nunique().to_dict()
    cities = sub.site.value_counts()
    nxt = collections.Counter(t[1] if len(t) > 1 else '(end)' for t in sub.tok)
    rows.append(dict(front=f, faces_first=len(sub), stones=sub.stone.nunique(), copy_events=len(se),
                     faces_any_position=allfaces_uses[f],
                     share_first=round(len(sub) / max(1, allfaces_uses[f]), 2),
                     seal=kinds.get('seal', 0), tablet=kinds.get('tablet', 0), copper=kinds.get('copper', 0),
                     tag=kinds.get('tag', 0), pot=kinds.get('pot', 0), other=kinds.get('other', 0),
                     n_cities=len(cities), cities='; '.join(f'{k} {v}' for k, v in cities.items()),
                     next_sign='; '.join(f'{k} {v}' for k, v in nxt.most_common(6)),
                     count_line=int(sub.is_count.sum()), name_closer=int(((sub.name.map(len) > 0) & sub.has_closer).sum())))
FW = pd.DataFrame(rows); FW.to_csv(f'{OUTF}/f1_front_words.csv', index=False)
say('\nFRONT WORDS (faces where the sign is first; stones by kind)')
say(FW.drop(columns=['cities']).to_string(index=False))

# ---------- B. slot signs
SL = sorted(SLOT | {'745'})
rows = []
for s in SL:
    n_all = allfaces_uses[s]; after_front = 0; pos = collections.Counter(); prevf = collections.Counter()
    for t in D.tok:
        for i, x in enumerate(t):
            if x != s: continue
            pos['first' if i == 0 else ('last' if i == len(t) - 1 else 'middle')] += 1
            if i > 0 and (t[i - 1] in F or (i > 1 and t[i - 2] in F and t[i - 1] in SLOT)):
                after_front += 1; prevf[t[i - 1] if t[i - 1] in F else t[i - 2] + '+' + t[i - 1]] += 1
    rows.append(dict(slot=s, uses=sum(pos.values()), faces=n_all, right_after_front=after_front,
                     share_after_front=round(after_front / max(1, sum(pos.values())), 2),
                     positions='; '.join(f'{k} {v}' for k, v in pos.items()),
                     fronts_before='; '.join(f'{k} {v}' for k, v in prevf.most_common(8))))
SS = pd.DataFrame(rows); SS.to_csv(f'{OUTF}/f1_slot_signs.csv', index=False)
say('\nSLOT SIGNS'); say(SS.to_string(index=False))

# ---------- C. share of texts of each object kind that begin with a front (stones once)
rows = []
for k in KINDS:
    sub = R[R.kind == k]
    st = sub.groupby('stone').front.apply(lambda s: (s != '').any())
    stc = R[(R.kind == k) & R.complete].groupby('stone').front.apply(lambda s: (s != '').any())
    ek = E[E.kind == k]
    rows.append(dict(kind=k, stones=len(st), stones_with_front=int(st.sum()), share=round(st.mean(), 3) if len(st) else 0,
                     complete_stones=len(stc), complete_with_front=int(stc.sum()),
                     share_complete=round(stc.mean(), 3) if len(stc) else 0,
                     copy_events=len(ek), events_with_front=int((ek.front != '').sum())))
SK = pd.DataFrame(rows); SK.to_csv(f'{OUTF}/f1_share_by_kind.csv', index=False)
say('\nSHARE OF TEXTS BEGINNING WITH A FRONT, by object kind'); say(SK.to_string(index=False))
# seals by city and format
S = R[R.kind == 'seal']
for col in ('site', 'fmt'):
    g = S.groupby(col).apply(lambda x: pd.Series(dict(stones=x.stone.nunique(), front=x[x.front != ''].stone.nunique())))
    g = g[g.stones >= 15]; g['share'] = (g.front / g.stones).round(3)
    say(f'\nseals: share with a front by {col}'); say(g.to_string())
    g.to_csv(f'{OUTF}/f1_seal_share_by_{col}.csv')

# ---------- D. front x the sign after it
X = E[(E.front != '') & (E.tok.map(len) >= 2)].copy()
X = X[X.tok.map(lambda t: t[1] not in ('000', 'ALT') and not t[1].startswith('X'))]
def after_cls(t):
    s = t[1]
    if s in SLOT or s == '745': return s
    if s in NUMS: return 'number'
    if s in CLOSERS or s in TITLES: return 'closer/title'
    return 'name sign'
X['after'] = X.tok.map(after_cls)
main = [f for f in X.front.value_counts().index if (X.front == f).sum() >= 5]
X = X[X.front.isin(main)]
tab = pd.crosstab(X.front, X.after)
def chi(tab):
    o = tab.values.astype(float); e = o.sum(1, keepdims=True) * o.sum(0, keepdims=True) / o.sum()
    return float(((o - e) ** 2 / np.where(e > 0, e, 1)).sum()), e
c_obs, exp = chi(tab)
null = []; cells = []
for _ in range(5000):
    a = deal_within(X.after.values, X.site.values, rng)
    t2 = pd.crosstab(X.front.values, a).reindex(index=tab.index, columns=tab.columns, fill_value=0)
    null.append(chi(t2)[0]); cells.append(t2.values)
cells = np.array(cells)
say(f'\nFRONT x SIGN AFTER IT (copy events, fronts with 5+): chi-square {c_obs:.1f}; after-sign dealt within site 5000x: '
    f'mean {np.mean(null):.1f}, max {np.max(null):.1f}, P {pval_hi(null, c_obs):.4f}')
say(tab.to_string())
rows = []
for i, f in enumerate(tab.index):
    for j, a in enumerate(tab.columns):
        o = tab.values[i, j]; m = cells[:, i, j].mean()
        rows.append(dict(front=f, after=a, observed=int(o), dealt_mean=round(m, 2),
                         P_high=round(pval_hi(cells[:, i, j], o), 4), P_low=round(pval_lo(cells[:, i, j], o), 4)))
PT = pd.DataFrame(rows); PT.to_csv(f'{OUTF}/f1_front_after_pairs.csv', index=False)
say('\ncells (observed against dealt mean), observed 3+ or dealt 3+:')
say(PT[(PT.observed >= 3) | (PT.dealt_mean >= 3)].to_string(index=False))
