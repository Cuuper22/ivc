#!/usr/bin/env python3
"""Step 1 rescue and step 2 redesigned: the number before a fish as a fixed word, not a count.

Step 1 went against: name-slot numbers before a fish pile up on TWO (136 of 191 distinct texts), not on 3, 6, 7.
PREDICTIONS for the rescue (written before the run):
 R1  (P3 with a P value) the value mix of name-slot numbers before a fish is further from the ordinary count mix
     on goods objects than count-slot numbers before a fish are (slot labels shuffled 5,000 times).
 R2  (fixed word) in names each fish type takes ONE number form (value + stroke style): the share of its single
     commonest form is higher in names than in counts for the same fish types.
 R3  (form rule) the stroke style of the two before a fish is set by the fish: tall two with the plain/caged fish,
     short two with the marked fish. The rule is sharper in names than in count slots.
 R4  (six-star) six + fish is a name everywhere: on goods objects it stands alone, or is followed by a closer
     (spear, jar, comb, porter), never by another goods word or count.
 R5  (Venus) tall two + plain fish (Parpola's vel(li) miin, Venus) is a house element: same-house seals at
     Mohenjo-daro share it more than chance (shuffled within area and 3-ft band).
"""
from stars_common import *

rng2 = np.random.default_rng(5)
PLAINISH = {'220', '226', '222'}
for cat in ('L', 'Mu'):
    U = distinct(all_units(cat)); U = U[U.pre.isin(['', '002', '031'])]
    F = U[U.nxt.isin(FISHALL)].copy(); F['S'] = F.slot.map({'name': 'NAME', 'sealx': 'X', 'count_pure': 'COUNT', 'count_named': 'COUNT'})
    F = F[F.S != 'X']
    O = U[(~U.nxt.isin(FISHALL)) & U.slot.isin(['count_pure', 'count_named'])]
    vals = list(range(1, 9))
    def mix(v): c = collections.Counter(np.clip(v, 1, 8)); t = sum(c.values()); return np.array([c[a] / max(t, 1) for a in vals])
    base = mix(O.value.values)
    def stat(lab, v): return 0.5 * np.abs(mix(v[lab == 'NAME']) - base).sum() - 0.5 * np.abs(mix(v[lab == 'COUNT']) - base).sum()
    lab = F.S.values; v = F.value.values; obs = stat(lab, v)
    sims = [stat(rng2.permutation(lab), v) for _ in range(5000)]
    print(f'\n== {cat} distinct texts: name {sum(lab=="NAME")}, count {sum(lab=="COUNT")}, ordinary goods counts {len(O)}')
    print(f'R1 name-minus-count distance from ordinary counts {obs:+.2f}; shuffled mean {np.mean(sims):+.2f}; P {(1+np.sum(np.array(sims)>=obs))/5001:.4f}')
    # R2
    F['form'] = F['style'] + F.value.astype(str)
    for S in ('NAME', 'COUNT'):
        g = F[F.S == S]; tops = []
        for f, h in g.groupby('nxt'):
            if len(h) >= 3: c = collections.Counter(h.form); tops.append((f, len(h), c.most_common(1)[0]))
        k = sum(t[2][1] for t in tops); n = sum(t[1] for t in tops)
        print(f'R2 {S}: commonest form per fish covers {k}/{n} = {k/max(n,1):.0%}  ', tops)
    # R3
    T = F[F.value == 2]
    for S in ('NAME', 'COUNT'):
        g = T[T.S == S]
        a = ((g.nxt.isin(PLAINISH)) & (g['style'] == 'tall')).sum(); b = ((g.nxt.isin(PLAINISH)) & (g['style'] != 'tall')).sum()
        c_ = ((~g.nxt.isin(PLAINISH)) & (g['style'] == 'tall')).sum(); e = ((~g.nxt.isin(PLAINISH)) & (g['style'] != 'tall')).sum()
        from scipy.stats import fisher_exact
        o, p = fisher_exact([[a, b], [c_, e]]) if min(a + b, c_ + e) else (np.nan, np.nan)
        print(f'R3 {S}: plain/caged fish two tall {a}, short {b} | marked fish two tall {c_}, short {e} | odds {o:.1f} P {p:.2g}')
    # R4 six + fish everywhere (all faces, not only deduped)
    A = all_units(cat); six = A[(A.value == 6) & A.nxt.isin(FISHALL)]
    print('R4 six + fish, every face:')
    for _, r in six.drop_duplicates(['text']).iterrows():
        x = r.text.split('-'); after = x[r.j + 2:] if r.j + 2 < len(x) else []
        print(f'    {r.cisi:8s} {r.kind:5s} {r.site:12s} {r.text:40s} after the unit: {"-".join(after) or "(nothing)"}  closer={r.closer}')

# R5 house share of the tall-two + plain fish, and of each fish compound, at Mohenjo-daro
def has_unit(o, f, form):
    for x, P in zip(o.faces, o.parses):
        for u in units(x, P):
            if u['nxt'] == f and (u['style'] + str(u['value'])) == form: return True
    return False
print('\nR5 house-mates share the compound (Mohenjo-daro seals; chance = shuffled within area and 3-ft band)')
for f, form in (('220', 'tall2'), ('235', 'short2'), ('240', 'short2'), ('233', 'short2'), ('231', 'short2'), ('220', 'short3'), ('220', 'stacked6')):
    r = house_share(None, pred=lambda o: has_unit(o, f, form))
    print(f'   {form} + {f}:', r)
