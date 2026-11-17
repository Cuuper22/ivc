#!/usr/bin/env python3
"""CHITS 3: amounts by class.  Two- and three-sided tablets: the amount face goes with the name face.

Groups by the name face's ending: comb (740-400), man (740-090), jar only, other title / other after-jar sign, and
name faces with no jar.  Amounts read off the OTHER faces of the same object: cups (700), big measure (705/706), tree
signs (390/405/406/407), porter 156, load-carrier (154/158).
Each object counted once ("objects"), and again with identical tablets in one trench counted once ("issues" =
distinct signature + site + trench).  Control: group labels shuffled among the records of the same site (4,000).

PREDICTIONS (written before any number):
 A1 if the comb marks a LOWER class: comb names draw fewer cups than jar-only names (mean cups lower) and almost never
    the big measure.
 A2 if the comb marks RECIPIENTS AS A GROUP (workers on rations): comb amounts are nearly all one value: the modal cup
    count holds 80%+ of comb records against a lower share for jar-only names.
 A3 the bet: A2 holds (3 cups modal) and the mean is the same as jar-only (rations, not rank).
Writes work_data/chits/c3_*.csv, c3_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
LOG = open(f'{OUT}/c3_log.txt', 'w'); say = say_to(LOG)
O = load(); rng = np.random.default_rng(33)
rows = []
for o, r in O[O.nfaces >= 2].iterrows():
    # the name face: first face with a jar parse and a readable name; else first face typed name
    nf = None
    for k, (jp, t) in enumerate(zip(r.jars, r.types)):
        if jp is not None and len(jp[0]) > 0: nf = k; break
    if nf is None:
        for k, t in enumerate(r.types):
            if t == 'name': nf = k; break
    if nf is None: continue
    jp = r.jars[nf]
    if jp is None: grp, name, after = 'name, no jar', '-'.join(r.faces[nf]), ''
    else:
        name, after = '-'.join(jp[0]), jp[1]
        grp = {'400': 'comb 740-400', '090': 'man 740-090', '': 'jar only'}.get(after, 'other after-jar sign')
    amt = {}; other = []
    for k, f in enumerate(r.faces):
        if k == nf: continue
        other.append('-'.join(f))
        for u, v in amount_of(f).items(): amt.setdefault(u, v)
    lab = []
    for u in ('cup', 'big', 'tree', 'porter', 'carrier'):
        if u in amt: lab.append(f'{amt[u]} {u}' if amt[u] is not None else f'? {u}')
    rows.append(dict(obj=o, cisi=r.cisi, site=r.site, kind=r.kind, type=r.type, area=r.area, bin=r.bin, nfaces=r.nfaces,
                     group=grp, name=name, after=after, other_faces=' | '.join(other), sig=r.sig, lostfree=r.lostfree,
                     cups=amt.get('cup'), big=amt.get('big'), tree=amt.get('tree'), porter=amt.get('porter'), carrier=amt.get('carrier'),
                     amount=' + '.join(lab) if lab else 'no amount'))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/c3_records.csv', index=False)
R['issue'] = R.sig + '#' + R.site + '#' + R.area
say(f'multi-face objects with a name face: {len(R)}; by group: {fmt_counter(collections.Counter(R.group))}')
GR = ['comb 740-400', 'man 740-090', 'jar only', 'other after-jar sign', 'name, no jar']

def dist(df, label):
    out = []
    for g in GR:
        s = df[df.group == g]
        if len(s) == 0: continue
        c = collections.Counter(s.amount); cups = s.cups.dropna()
        cc = collections.Counter(int(x) for x in cups)
        mode_share = (max(cc.values()) / len(cups)) if len(cups) else np.nan
        out.append(dict(set=label, group=g, records=len(s), with_cups=len(cups), cup_counts=fmt_counter(dict(sorted(cc.items()))),
                        mean_cups=round(cups.mean(), 2) if len(cups) else np.nan, modal_cup_share=round(mode_share, 3),
                        with_big=int(s.big.notna().sum()), with_tree=int(s.tree.notna().sum()), with_porter=int(s.porter.notna().sum()),
                        no_amount=int((s.amount == 'no amount').sum()), top_amounts=fmt_counter(c, 6)))
    return pd.DataFrame(out)

H = R[R.site == 'Harappa']
D = pd.concat([dist(R, 'all sites, objects'), dist(H, 'Harappa, objects'),
               dist(H.drop_duplicates('issue'), 'Harappa, issues (copies in one trench once)')])
D.to_csv(f'{OUT}/c3_distributions.csv', index=False)
for _, r in D.iterrows():
    say(f'  [{r.set}] {r.group:22s} rec {r.records:4d} cups {r.with_cups:3d} [{r.cup_counts}] mean {r.mean_cups} modal {r.modal_cup_share} | big {r.with_big} tree {r.with_tree} porter {r.with_porter} none {r.no_amount} | {r.top_amounts}')

# tests on Harappa: comb vs jar only, mean cups and modal share, shuffle labels among Harappa records with cups
say('\ntests (Harappa records with a cup count; group labels shuffled among them):')
for label, df in (('objects', H), ('issues', H.drop_duplicates('issue'))):
    C = df[df.cups.notna() & df.group.isin(['comb 740-400', 'jar only', 'man 740-090', 'name, no jar'])].reset_index(drop=True)
    g = C.group.values; v = C.cups.values.astype(int)
    def stats(g):
        out = {}
        for k in ('comb 740-400', 'jar only', 'man 740-090', 'name, no jar'):
            x = v[g == k]
            if len(x) == 0: out[k] = (np.nan, np.nan); continue
            out[k] = (x.mean(), np.bincount(x).max() / len(x))
        return out
    ob = stats(g); nm = []; nmode = []
    for _ in range(4000):
        p = rng.permutation(g); s = stats(p)
        nm.append(s['comb 740-400'][0] - s['jar only'][0]); nmode.append(s['comb 740-400'][1] - s['jar only'][1])
    nm, nmode = np.array(nm), np.array(nmode)
    dm = ob['comb 740-400'][0] - ob['jar only'][0]; dmo = ob['comb 740-400'][1] - ob['jar only'][1]
    say(f'  [{label}] n {len(C)}: mean cups comb {ob["comb 740-400"][0]:.2f} / jar only {ob["jar only"][0]:.2f} / man {ob["man 740-090"][0]:.2f} / no-jar name {ob["name, no jar"][0]:.2f}; '
        f'comb minus jar-only {dm:+.2f} (P low {(nm <= dm).mean():.4f}, P high {(nm >= dm).mean():.4f})')
    say(f'  [{label}] modal cup share comb {ob["comb 740-400"][1]:.2f} / jar only {ob["jar only"][1]:.2f} / man {ob["man 740-090"][1]:.2f}; comb minus jar-only {dmo:+.2f} (P high {(nmode >= dmo).mean():.4f})')

# per name: how many distinct names carry which cup count, comb vs jar-only (one vote per name)
say('\none vote per name (Harappa, modal cup count of each name):')
for g in ('comb 740-400', 'jar only', 'man 740-090', 'name, no jar'):
    s = H[(H.group == g) & H.cups.notna()]
    per = s.groupby('name').cups.agg(lambda x: int(pd.Series(x).mode().iloc[0]))
    say(f'  {g:16s} names {len(per)}: ' + fmt_counter(dict(sorted(collections.Counter(per).items()))))
# without the 176 holder
s = H[(H.group == 'comb 740-400') & H.cups.notna() & (H.name != '176')]
say(f'  comb without name 176: records {len(s)} cups {fmt_counter(dict(sorted(collections.Counter(s.cups.astype(int)).items())))}, mean {s.cups.mean():.2f}')
# non-cup amounts with comb
say('\ncomb records whose other face is not a cup count (Harappa):')
s = H[(H.group == 'comb 740-400') & H.cups.isna()]
say('  ' + fmt_counter(collections.Counter(s.other_faces), 30))
s = H[(H.group == 'jar only') & H.cups.isna()]
say('jar-only records with no cup count (Harappa), top other faces: ' + fmt_counter(collections.Counter(s.other_faces), 20))
say('done')
