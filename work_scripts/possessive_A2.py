#!/usr/bin/env python3
"""Second pass for master/servant pairs: all object types, broken texts allowed when the name before the jar is intact,
three match levels. Writes work_data/possessive/master_servant_pairs_wide.csv."""
import sys, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from gloss2 import *
d = load2(); lex = learn(d); own = lex['owner']
d['r'] = [parse_face(x, lex, own) for x in d.tok]
d['house'] = d['site'] + ' / ' + d['area-section'] + ' / ' + d['block-house']
d['text_s'] = ['-'.join(x) for x in d.tok]
rows = []
for _, r in d.iterrows():
    x = r.tok; j = r.r['jars']
    if not j: continue
    # left edge of the reading text must be closed ('+' on the stored right) -- use flags: broken text still ok if no lost sign before the final jar
    if any(s in ('000', 'ALT') for s in x[:j[-1]]): continue
    nm = tuple(r.r['name'])
    if not nm: continue
    after = x[j[-1] + 1:]
    kind = 'owner' if not after and not ('broken' in r.flg) else ('servant' if after[:1] == ('090',) else None)
    if kind is None: continue
    rows.append(dict(kind=kind, name=nm, cisi=r['cisi'], site=r.site, house=r.house, zone=r['area-section'], type=r.type, text=r.text_s, symbol=r.symbol, depth=r.depth))
T = pd.DataFrame(rows)
T = T.drop_duplicates(['site', 'text', 'cisi'])
print(T.kind.value_counts().to_dict())
own_ = T[T.kind == 'owner']; srv = T[T.kind == 'servant']
def place(a, b):
    if a.site != b.site: return 'other site'
    blk = lambda h: h.split(' / ')[2] not in ('--', '', '-')
    if a.house == b.house and blk(a.house): return 'same house'
    if a.zone == b.zone and a.zone not in ('--', ''): return 'same area'
    return 'same site'
out = []
levels = {'exact name': lambda n: n, 'name without its tag': lambda n: n[:-1] if len(n) >= 3 else None, 'self+tag (last two signs)': lambda n: n[-2:] if len(n) >= 2 else None}
for lv, f in levels.items():
    idx = collections.defaultdict(list)
    for _, o in own_.iterrows():
        k = f(o['name'])
        if k: idx[k].append(o)
    for _, s in srv.iterrows():
        k = f(s['name'])
        if not k: continue
        for o in idx.get(k, []):
            if lv != 'exact name' and o['name'] == s['name']: continue
            out.append(dict(level=lv, servant_name='-'.join(s['name']), servant_cisi=s.cisi, servant_site=s.site, servant_house=s.house, servant_type=s.type, servant_text=s.text,
                            owner_name='-'.join(o['name']), owner_cisi=o.cisi, owner_site=o.site, owner_house=o.house, owner_type=o.type, owner_text=o.text, place=place(s, o)))
O = pd.DataFrame(out); O.to_csv('/home/antigravity/Cuuper22/ivc/work_data/possessive/master_servant_pairs_wide.csv', index=False)
for lv in levels:
    s = O[O.level == lv]
    print(lv, 'pairs', len(s), 'servants matched', s.servant_cisi.nunique(), 'of', len(srv), s.place.value_counts().to_dict())
# base rate: owner -> other owner, exact, same-site
idx = collections.defaultdict(list)
for _, o in own_.iterrows(): idx[o['name']].append(o)
hit = sum(1 for _, o in own_.iterrows() if any((q.cisi != o.cisi) for q in idx[o['name']]))
print('owners with another owner seal of the same name', hit, 'of', len(own_))
ex = O[O.level == 'exact name']
print(ex[['servant_cisi', 'servant_site', 'servant_house', 'servant_text', 'owner_cisi', 'owner_site', 'owner_house', 'owner_text', 'place']].to_string())
print(O[(O.level != 'exact name') & (O.place.isin(['same house', 'same area']))][['level','servant_cisi','servant_house','servant_text','owner_cisi','owner_house','owner_text','place']].to_string())

# ---- summaries used in the report
ms = srv[srv.name.map(len) >= 2]; mo = own_[own_.name.map(len) >= 2]
idx2 = collections.defaultdict(list)
for _, o in mo.iterrows(): idx2[o['name']].append(o)
print('multi-sign servants', len(ms), 'matched to an owner seal', sum(1 for _, s in ms.iterrows() if idx2.get(s['name'])))
hit = sum(1 for _, o in mo.iterrows() if any(q.cisi != o.cisi for q in idx2[o['name']]))
print('multi-sign owners with another owner of same name', hit, 'of', len(mo))
e = O[(O.level == 'exact name') & (O.servant_name.str.count('-') >= 1)]
rank = {'same house': 0, 'same area': 1, 'same site': 2, 'other site': 3}
e = e.assign(r=e.place.map(rank)).sort_values(['r', 'servant_name'])
e.drop(columns='r').to_csv('/home/antigravity/Cuuper22/ivc/work_data/possessive/master_servant_pairs_multisign.csv', index=False)
print('multi-sign exact pairs', len(e), 'servants', e.servant_cisi.nunique(), e.place.value_counts().to_dict())
print(e[['servant_name','servant_cisi','servant_site','servant_house','owner_cisi','owner_site','owner_house','place']].to_string())
# animals / zones
import pandas as pd
sym = lambda df: df.symbol.str.split(':').str[0].value_counts(normalize=True).round(2).head(4).to_dict()
print('animal servant', sym(srv), 'owner', sym(own_))
print('site servant', srv.site.value_counts().to_dict()); print('site owner', own_.site.value_counts().head(6).to_dict())
print('type servant', srv.type.value_counts().to_dict())

# ---- second design: same excavation house + same first sign of the name (house crest) / same last sign
def hk(r):
    return None if r.house.endswith('-- / --') or r.house.split(' / ')[2] in ('--', '') else r.house
T['hk'] = T.apply(hk, axis=1)
Th = T[T.hk.notna() & (T.name.map(len) >= 2)]
def housemate_rate(src, pool, pos):
    hit = n = 0
    for _, s in src.iterrows():
        n += 1
        if any(o.hk == s.hk and o.cisi != s.cisi and o['name'][pos] == s['name'][pos] for _, o in pool.iterrows() if o.hk == s.hk): hit += 1
    return hit, n
so = Th[Th.kind == 'servant']; oo = Th[Th.kind == 'owner']
for pos, nm in ((0, 'first sign (crest slot)'), (-1, 'last sign (tag slot)')):
    a = housemate_rate(so, oo, pos); b = housemate_rate(oo, oo, pos)
    print('house-mate owner shares', nm, ': servant seals', a, round(a[0]/max(a[1],1),2), '| owner seals', b, round(b[0]/max(b[1],1),2))
