#!/usr/bin/env python3
"""COPPER step 8: the set table for the report (markdown), one row per text family with 2+ copies, plus single-copy
texts in a short list. Reads objects.csv, m77_objects.csv, spots_objects.csv. Writes work_data/copper/set_table.md."""
import sys; sys.path.insert(0, '/home/claude/ivc/work_scripts')
from copper_common import *
say = print
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
Mm = pd.read_csv(f'{OUT}/m77_objects.csv', dtype=str).fillna('')
SP = pd.read_csv(f'{OUT}/spots_objects.csv', dtype=str).fillna('')
exec(open(f'{ROOT}/work_scripts/copper_2_pairs.py').read().split('# ---- text families')[1].split('rng = np.random')[0])
L['fam'] = L.set_text.map(FAM).fillna(L.set_text); Mm['fam'] = Mm.set_text.map(FAM).fillna(Mm.set_text)
L = L.merge(SP[['obj', 'series', 'regno', 'regsuf', 'area2', 'building']], on='obj', how='left').fillna('')
out = ['| texts in the family (copies first catalogue / second catalogue) | copies | kind | picture: eye (n) | picture: first-catalogue code | picture: second-catalogue code | picture-face sign | areas | buildings (area house) | register lots | bins |',
       '|---|---|---|---|---|---|---|---|---|---|---|']
fams = sorted(set(L.fam) | set(Mm.fam), key=lambda f: -max((L.fam == f).sum(), (Mm.fam == f).sum()))
single = []
for f in fams:
    a = L[L.fam == f]; b = Mm[Mm.fam == f]
    tx = sorted(set(a.set_text) | set(b.set_text))
    cnt = {t: (int((a.set_text == t).sum()), int((b.set_text == t).sum())) for t in tx}
    copies = sum(max(x, y) for x, y in cnt.values())
    if copies < 2: single.append(f'{tx[0]} ({a.cat.iloc[0] if len(a) else "M77 " + (b.fs.iloc[0] or "-")})'); continue
    eye = collections.Counter(g for g, s in zip(a.eye_group, a.pic_src) if g and g not in ('worn', 'text'))
    cat = collections.Counter(c for c in a.cat if c not in NOPIC)
    m77 = collections.Counter(x for x in b.fs if x)
    ps = collections.Counter([p for p in a.picsign if p] + [p for p in b.picsign if p])
    sec = collections.Counter(p for p in a.second if p)
    kind = '/'.join(sorted({text_kind(t.split('-')) for t in tx if '000' not in t}))
    lots = sorted(f'{s} {r}{x}' for s, r, x in zip(a.series, a.regno, a.regsuf) if s)
    lots = [l.replace('.0', '') for l in lots]
    fmt = lambda c: ', '.join(f'{k} {v}' for k, v in c.most_common()) or '-'
    out.append(f'| {"; ".join(f"{t} ({x}/{y})" for t, (x, y) in cnt.items())} | {copies} | {kind} | {fmt(eye)} | {fmt(cat)} | {fmt(m77)} | '
               f'{fmt(ps)}{"; 2nd text " + fmt(sec) if sec else ""} | {fmt(collections.Counter(x for x in a.area2 if x))} | '
               f'{fmt(collections.Counter(x for x in a.building if x))} | {", ".join(lots) or "-"} | {fmt(collections.Counter(x for x in a.bin if x))} |')
out.append(''); out.append(f'Single-copy texts ({len(single)}): ' + '; '.join(single))
open(f'{OUT}/set_table.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:6])); print(len(out), 'lines')
