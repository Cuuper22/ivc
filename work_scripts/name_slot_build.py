#!/usr/bin/env python3
"""Build the seal-level name table: one row per seal face with parsed roles.
Name = the 'who' signs of a tightly parsed seal text (reading order). Writes work_data/name_rows.csv."""
import sys, pandas as pd, re
sys.path.insert(0, '/home/claude/ivc/work_scripts')
ROOT = '/home/claude/ivc'
d = pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv', dtype=str).fillna('')
g = pd.read_csv(f'{ROOT}/work_data/gloss_all.csv', dtype=str).fillna('')
assert len(d) == len(g) and (d.id.values == g.id.values).all()
TEMPL = {'opener','opener-strokes','class','class-tail','count','amount','house','house-marker','cap','cap-selector','title-phrase'}
rows = []
for i in range(len(d)):
    r = d.iloc[i]; gg = g.iloc[i]
    if not r.type.startswith('SEAL'): continue
    toks = gg.reading_order_text.split('-'); roles = gg.role_string.split()
    if len(toks) != len(roles): continue
    if any(('[' in r.text, ']' in r.text, '/' in r.text, '000' in toks)): continue
    if 'unknown' in roles: continue
    who_idx = [k for k, x in enumerate(roles) if x == 'who']
    tight = len(who_idx) <= 2 and sum(x in TEMPL for x in roles) * 2 >= len(roles)
    contiguous = bool(who_idx) and who_idx[-1] - who_idx[0] + 1 == len(who_idx)
    name = [toks[k] for k in who_idx]
    SEGR = {'who','house','house-marker','fixed-ending','phrase','head','second-slot','mark'}
    kc = [k for k, x in enumerate(roles) if x in ('class', 'class-tail')]
    kend = kc[0] if kc else len(toks)
    ko = [k for k, x in enumerate(roles) if x in ('opener', 'opener-strokes', 'cap', 'cap-selector') and k < kend]
    kstart = (ko[-1] + 1) if ko else 0
    seg_idx = [k for k in range(kstart, kend) if roles[k] in SEGR]
    seg = [toks[k] for k in seg_idx]
    cls = [toks[k] for k, x in enumerate(roles) if x == 'class']
    op = [toks[k] for k, x in enumerate(roles) if x in ('opener', 'cap')]
    house = [toks[k] for k, x in enumerate(roles) if x == 'house']
    rows.append(dict(id=r.id, obj=r.id.split('.')[0], cisi=r.cisi, site=r.site, region=r.region, area=r['area-section'],
        bh=r['block-house'], room=r['room-grid'], depth=r.depth, symbol=r.symbol, material=r.material, hmm=r['horizontal(mm)'], vmm=r['vertical(mm)'],
        reading='-'.join(toks), roles=' '.join(roles), tight=tight, contiguous=contiguous, nwho=len(who_idx),
        name='-'.join(name), first=name[0] if name else '', last=name[-1] if name else '',
        cls='-'.join(cls), cls_last=cls[-1] if cls else '', opener='-'.join(op), house='-'.join(house),
        pos=','.join(map(str, who_idx)), seg='-'.join(seg), seglen=len(seg), segroles=' '.join(roles[k] for k in seg_idx), has_class=bool(kc), n=len(toks)))
o = pd.DataFrame(rows)
o.to_csv(f'{ROOT}/work_data/name_rows.csv', index=False)
print(len(o), 'seal faces; tight', o.tight.sum(), '; tight with a name', ((o.tight) & (o.nwho > 0)).sum())
