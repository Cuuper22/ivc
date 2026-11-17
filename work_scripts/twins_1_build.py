#!/usr/bin/env python3
"""TWINS step 1: every set of two or more SEALS with the identical complete text, in each catalogue and across them.
Written 2026-11-17 before any twin set was counted.

How one stone is kept from counting twice:
- Inside the first catalogue (Lipi) a twin set is a set of different object ids. Faces of one prism never pair with each
  other. Two members that share a CISI number or an excavation number, or that have the same site, same findspot,
  same animal and face size within 0.5 mm both ways, are flagged 'possible double entry' and are merged into one stone.
- The second catalogue (Mahadevan 1977) re-transcribes mostly the same stones. Its seal twin sets are counted on their
  own, in its own sign numbers (a replication). For the union, a text (in Lipi numbers, through the sign crosswalk
  already in work_data/mahadevan_parsed.csv) at one site counts max(Lipi seals, Mahadevan seals) stones: a second-
  catalogue seal adds a stone only where it has more copies at that site than the first catalogue does.
Writes work_data/twins/seals.csv, members.csv, sets.csv, mah_sets.csv, union_sets.csv, log_1.txt.
"""
from twins_common import *
import itertools, collections

S = seals()
S.to_csv(f'{OUT}/seals.csv', index=False)
log('t1', f'seal faces {len(S)}, objects {S.obj.nunique()}; complete faces {int(S.complete.sum())} on {S[S.complete].obj.nunique()} objects; wide {int(S.complete_wide.sum())}')

def build_sets(col):
    C = S[S[col]].copy()
    C = C.sort_values('face').drop_duplicates(['obj', 'signs'])          # one prism face per text per stone
    sets = []
    for t, g in C.groupby('signs'):
        if g.obj.nunique() < 2: continue
        g = g.copy()
        # double-entry check
        stone = {o: o for o in g.obj}
        rows = list(g.itertuples())
        for a, b in itertools.combinations(rows, 2):
            same = False
            if a.cisi not in ('', '-') and a.cisi == b.cisi: same = True
            if a.excav_id.strip() not in ('', '-', '--') and a.excav_id.strip() == b.excav_id.strip() and a.site == b.site: same = True
            try:
                if (a.site == b.site and a.building == b.building and a.animal == b.animal and a.stand == b.stand and
                        abs(float(a.hmm) - float(b.hmm)) <= 0.5 and abs(float(a.vmm) - float(b.vmm)) <= 0.5 and str(a.depth_ft) == str(b.depth_ft)):
                    same = True
            except ValueError: pass
            if same: stone[b.obj] = stone[a.obj]
        g['stone'] = g.obj.map(stone)
        sets.append(g)
    M = pd.concat(sets) if sets else pd.DataFrame()
    return M

for col in ('complete', 'complete_wide'):
    M = build_sets(col)
    dup = M.groupby('signs').apply(lambda g: g.obj.nunique() - g.stone.nunique()).sum()
    print('   merged as one stone:', [(r.signs, r.cisi, r.stone) for r in M[M.obj != M.stone].itertuples()])
    M = M.drop_duplicates('stone')
    vc = M.groupby('signs')['obj'].nunique(); keep = vc[vc >= 2].index
    M = M[M.signs.isin(keep)].copy()
    sid = {t: f'T{i+1:03d}' for i, t in enumerate(sorted(keep, key=lambda t: (-vc[t], t)))}
    M['set'] = M.signs.map(sid); M['set_size'] = M.signs.map(vc)
    log('t1', f'[{col}] possible double entries merged: {int(dup)}; twin sets {len(keep)}, seals in them {len(M)}')
    if col == 'complete':
        M.to_csv(f'{OUT}/members.csv', index=False)
        main = M
    else:
        M.to_csv(f'{OUT}/members_wide.csv', index=False)

M = main
def joinu(s): return ' '.join(sorted(set(x for x in s if x)))
rows = []
for t, g in M.groupby('signs'):
    rows.append(dict(set=g.set.iloc[0], signs=t, length=g.n.iloc[0], size=len(g), kind=g.kind.iloc[0],
                     cities=joinu(g.site), n_cities=g.site.nunique(), areas=joinu(g.area_key), buildings=joinu(g.building),
                     depths=' '.join(f'{v:.1f}' for v in g.depth.dropna()), bins=joinu(g.bin),
                     animals=' '.join(a or '-' for a in g.animal), stands=' '.join(s or '-' for s in g.stand),
                     sizes_mm2=' '.join('-' if v != v else f'{v:.0f}' for v in g.area_mm2), formats=' '.join(g.fmt),
                     boss=' '.join(b or '-' for b in g.boss), condition=' '.join(g.condition), objects=' '.join(g.cisi.where(g.cisi.isin(['', '-']) == False, g.obj))))
SETS = pd.DataFrame(rows).sort_values(['size', 'length'], ascending=[False, False])
SETS.to_csv(f'{OUT}/sets.csv', index=False)
print(SETS.groupby('length').agg(sets=('set', 'size'), seals=('size', 'sum')).to_string())
print('set sizes:', SETS['size'].value_counts().sort_index().to_dict())

# ---------------------------------------------------------------- second catalogue
P = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
R = pd.read_csv(f'{ROOT}/research/data/mahadevan_20260905/concordance_rows.csv', dtype=str, keep_default_na=False)
# the second catalogue stores a multi-line face as several lines (sideline = 10 x side + line: 1, 2 = lines of the only side;
# 10, 11, 12 = side 1; 20 ... = side 2). A face text = its lines joined in line order; a face is complete only if every line is.
P = P[P.cls == 'seal'].copy()
P['sl'] = P.sideline.astype(int); P['side'] = P.sl // 10; P['line'] = P.sl % 10
rowsm = []
for (tn, sd), g in P.sort_values(['textnum', 'side', 'line']).groupby(['textnum', 'side']):
    rowsm.append(dict(textnum=tn, site=g.site.iloc[0], fs=g.fs.iloc[0], locus=g.locus.iloc[0], level=g.level.iloc[0],
                      complete=str(all(g.complete == 'True')), lines=len(g),
                      reading_mah='-'.join(g.reading_mah), reading_lipi='-'.join(g.reading_lipi),
                      n=sum(int(v) for v in g.n)))
ms = pd.DataFrame(rowsm)
ms = ms[ms.complete == 'True'].copy()
ms['mtext'] = ms.reading_mah
ms = ms.drop_duplicates(['textnum', 'mtext'])
mv = ms.groupby('mtext').textnum.nunique()
mk = mv[mv >= 2]
MS = ms[ms.mtext.isin(mk.index)].copy()
MS['set_size'] = MS.mtext.map(mk); MS['L'] = MS.n.astype(int)
MS.to_csv(f'{OUT}/mah_sets.csv', index=False)
log('t1', f'second catalogue: complete seal lines {len(ms)} on {ms.textnum.nunique()} objects; twin sets {len(mk)}, seals in them {int(mk.sum())}')
print(MS.drop_duplicates('mtext').groupby('L').agg(sets=('mtext', 'size'), seals=('set_size', 'sum')).to_string())

# ---------------------------------------------------------------- union without double counting
from mah_common import lipi_site
# both catalogues on the second catalogue's seven site groups (MD, HP, CD, LL, KB, OS = other Indian sites, WA = abroad):
# its other-site rows carry no site name, so a stone is matched at group level, and the count per group is the larger of the two.
Lc = S[S.complete].drop_duplicates(['obj', 'signs']).copy()
REG = pd.read_csv(f'{ROOT}/work_data/stamps/objects.csv', dtype=str).fillna('')
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v4_common import d
regmap = dict(zip(d.id, d.region))
Lc['grp'] = [lipi_site(s, regmap.get(f, '')) for s, f in zip(Lc.site, Lc.face)]
lip = Lc.groupby(['signs', 'grp'])['obj'].nunique()
mah = ms[~ms.reading_lipi.str.contains('X|000')].copy()
mahc = mah.groupby(['reading_lipi', 'site']).textnum.nunique()
U = collections.Counter(); src = collections.defaultdict(dict)
for (t, s), n in lip.items(): U[(t, s)] = max(U[(t, s)], n); src[t][s] = [n, 0]
for (t, s), n in mahc.items():
    U[(t, s)] = max(U[(t, s)], n); src[t].setdefault(s, [0, 0])[1] = n
tot = collections.Counter()
for (t, s), n in U.items(): tot[t] += n
UN = pd.DataFrame([dict(signs=t, length=len(t.split('-')), stones=n, by_site=' '.join(f'{s}:{a}/{b}' for s, (a, b) in sorted(src[t].items())))
                   for t, n in tot.items() if n >= 2]).sort_values(['stones', 'length'], ascending=False)
UN.to_csv(f'{OUT}/union_sets.csv', index=False)
added = UN[~UN.signs.isin(SETS.signs)]
log('t1', f'union (larger of the two catalogues in each site group): twin sets {len(UN)}, stones {int(UN.stones.sum())}; sets only seen through the second catalogue {len(added)}')
print(UN.groupby('length').agg(sets=('signs', 'size'), stones=('stones', 'sum')).to_string())
print(added.head(30).to_string())
