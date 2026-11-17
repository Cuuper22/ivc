#!/usr/bin/env python3
"""EARLY job, step 1: give the second catalogue's Mohenjo-daro seals a level, and ask what the earliest level of the dig
(Mackay's DK-G Early I, 20.5 ft and deeper) carries.

PLAIN WORDS
- The second catalogue (Mahadevan 1977) has a `level` column. It is the find depth in feet below the dig datum, as a negative
  whole number (0 = not recorded). Checked here against the first catalogue's own depth on 388 text-matched seals: the two agree to
  the foot (r -0.98; level + depth averages 0), so a depth band means the same thing in both catalogues.
- Its `locus` column is an area code. Matching again against the first catalogue shows 31 = DK-G South, 32 = DK-G North
  (139 and 39 of the matched seals), the long dug sequence the history job used. Only those two loci are used.
- A level is a depth band cut at the first catalogue's own period boundaries (Early I deeper than 20.5 ft; 16-20.5; 13-16; 10-13;
  7-10; 5-7; shallower than 5).
- "New texts" = Mahadevan texts with no partner text in the first catalogue (the crosswalk's own list), so the second catalogue adds
  independent seals only through them. "Union" = first-catalogue seals plus new texts.
- FISH CREST = a marked fish sign (231, 233, 235, 240, 236) as the first sign of the name (lost signs skipped).
  ANY MARKED FISH = one of those signs anywhere in the name.

PREDICTIONS (written before the second-catalogue numbers were computed; the first-catalogue table 0 of 36 was already known, and the
printout of the 39 deep Mahadevan texts had been glanced at once before this file was written):
 E1  Mahadevan DK-G seals at the earliest level again lack the fish crest as first sign: at most 2 of the new texts, union rate under 4%
     (the base rate over all levels is about 12.6%).
 E2  The crest slot at the earliest level is filled by non-fish houses (plain fish 220, leaf 803, produce 806, lady 140, chest 590 ...).
 E3  Where fish crests arrive (level 1), they arrive together with the agent form `X jar man` and the overseas short-horned bull is
     not yet linked to them; the office opening and the overseas bull are already present at level 0.
 E4  Any-marked-fish names are also rarer at the earliest level than later (the crest is what is missing, not just the first slot).
Outputs: work_data/early/dkg_union_levels.csv, early_level_seals.csv, early_level_read.csv, log_1.txt
"""
import sys, os, io, contextlib, collections, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import *
    import corpus_build2 as cb
    from sound_v4_common import lex, parse_face
from scipy.stats import fisher_exact

OUTE = f'{ROOT}/work_data/early'
os.makedirs(OUTE, exist_ok=True)
EDGES = [20.5, 16.0, 13.0, 10.0, 7.0, 5.0]       # band 0 = deeper than 20.5 ft ... band 6 = shallower than 5 ft


def band(ft):
    for i, e in enumerate(EDGES):
        if ft >= e - 1e-9: return i
    return 6


def seq(x, s):
    return '-'.join(s) in '-'.join(x)


def feats(x, name):
    """x = token list in reading order (lost = '000'); name = tuple of name signs from the parser."""
    nm = [a for a in name if a not in ('000', 'ALT')]
    last = [a for a in x if a not in ('000', 'ALT')]
    ln = ''.join(' ' + a for a in x)
    f = dict(
        n=len(last), nmlen=len(nm), hasname=len(nm) > 0,
        fishfirst=len(nm) > 0 and nm[0] in MARKED,
        fishfirst_clean=len(nm) > 0 and nm[0] in MARKED and x[:1] != ['000'] and (x.index(nm[0]) == 0 or all(a not in ('000', 'ALT') for a in x[:x.index(nm[0])])),
        fishpos=(min([i for i, a in enumerate(nm) if a in MARKED]) if any(a in MARKED for a in nm) else -1),
        anymarked=any(a in MARKED for a in nm),
        anyfish=any(a in FISHALL for a in nm),
        agent=seq(x, ('740', '090')),
        jar='740' in x, spear=(len(last) > 0 and last[-1] == '520'),
        office=seq(x, ('920', '060', '741')), boxcot=seq(x, ('590', '390')),
        starname=any(x[i] in NUM and x[i + 1] in FISHALL for i in range(len(x) - 1)),
        counted=any(a in NUM for a in x),
        first=nm[0] if nm else '')
    return f


# ------------------------------------------------------------------ calibration: depth and locus, second vs first catalogue
m = M[(M.site == 'MD') & (M.cls == 'seal')].copy()
m['lv'] = m.level.astype(int); m['loc'] = m.locus.astype(int)
L = T[(T.site == 'Mohenjo-daro') & (T.kind == 'seal')].copy()
L['txt'] = L.faces.apply(lambda fs: '-'.join(max(fs, key=len)) if len(fs) else '')
lc = L.txt.value_counts()
pairs = []
for t, g in m[m.complete == 'True'].groupby('reading_lipi'):
    if len(g) == 1 and lc.get(t, 0) == 1:
        o = L[L.txt == t].iloc[0]
        pairs.append((int(g.iloc[0].locus), int(g.iloc[0].level), o.area, o.ft))
P = pd.DataFrame(pairs, columns=['locus', 'level', 'area', 'ft'])
Q = P[P.ft.notna() & (P.level != 0)]
print(f'[calibration] {len(P)} text-matched seals; {len(Q)} with a depth in both: r(level, depth) = {np.corrcoef(Q.level, Q.ft)[0, 1]:.3f}; mean(level + depth) = {(Q.level + Q.ft).mean():+.2f} ft, sd {(Q.level + Q.ft).std():.2f}')
print('[calibration] locus -> first-catalogue area (matched seals):')
for lo in (31, 32): print(f'   locus {lo}:', P[P.locus == lo].area.value_counts().to_dict())

# ------------------------------------------------------------------ first catalogue: DK-G seals with a Mackay level
G = D[(D.site == 'Mohenjo-daro') & D.area.str.startswith('DKG') & (D.rule == 'B layer-map') & D.seal].copy()
LV = {'Early I': 0, 'Intermediate III': 1, 'Intermediate II': 2, 'Intermediate I': 3, 'Late III': 4, 'Late II': 5, 'Late I': 6, 'Late IA': 6, 'Late IB': 6}
G['lvl'] = (G.period.str.strip() + ' ' + G.phase.str.strip()).map(LV)
G = G[G.lvl.notna()].copy(); G['lvl'] = G.lvl.astype(int)
G['band'] = G.ft.map(lambda v: band(v) if v == v else -1)
ok = G[G.band >= 0]
print(f'[calibration] first-catalogue DK-G seals: depth band agrees with Mackay level on {int((ok.band == ok.lvl).sum())} of {len(ok)} '
      f'({(ok.band == ok.lvl).mean() * 100:.0f}%); band 0 (>=20.5 ft) vs Early I: {int(((ok.band == 0) & (ok.lvl == 0)).sum())} of {int((ok.lvl == 0).sum())} Early I seals are band 0, {int(((ok.band == 0) & (ok.lvl != 0)).sum())} other seals are band 0')
rowsL = []
for o, r in G.iterrows():
    x = list(max(r.faces, key=len)); f = feats(x, r['name'])
    f.update(cat='first', id=r.cisi, obj=o, lvl=r.lvl, ft=r.ft, text='-'.join(x), animal=r.animal if 'animal' in r else '')
    rowsL.append(f)
FL = pd.DataFrame(rowsL)
AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
FL['short'] = [AB.animal.get(str(o), '') == 'SHORTHORN' for o in FL.obj]
FL['noanimal'] = [AB.animal.get(str(o), '') == 'NONE' for o in FL.obj]

# ------------------------------------------------------------------ second catalogue: DK-G seals, one row per object
S2 = m[m['loc'].isin([31, 32]) & (m.lv < 0)].copy()
S2['ft'] = -S2.lv
S2['len'] = S2.n.astype(int)
S2 = S2.sort_values('len', ascending=False).drop_duplicates('textnum')
S2['band'] = S2.ft.map(band)
rowsM = []
for _, r in S2.iterrows():
    x = list(r.tok); name = tuple(r['name'].split('-')) if r['name'] else ()
    f = feats(x, name)
    code = str(r.fs)[:-1].zfill(2) if str(r.fs) not in ('0', '') else None
    f.update(cat='second', id=f'Mah {r.textnum}', obj=r.textnum, lvl=int(r.band), ft=float(r.ft), text='-'.join(x),
             partnered=bool(r.partnered), short=(code == '04'), noanimal=(code is None))
    rowsM.append(f)
FM = pd.DataFrame(rowsM)
# Object-level match: the second catalogue re-transcribes mostly the same stones. A second-catalogue seal counts as the SAME STONE as a
# first-catalogue seal when their depths differ by 1.0 ft or less (the second catalogue rounds to whole feet) and their texts line up
# (sequence ratio 0.25 or more, lost signs treated as wildcards), taking best matches first, each stone used once.
LP = T[(T.site == 'Mohenjo-daro') & T.area.str.startswith('DKG') & (T.kind == 'seal') & T.ft.notna() & (T.ft > 0)].copy()
LP['tok'] = LP.faces.apply(lambda fs: tuple(max(fs, key=len)) if len(fs) else ())


def sim(a, b):
    a = [x if x not in ('000', 'ALT') else f'?a{i}' for i, x in enumerate(a)]
    b = [x if x not in ('000', 'ALT') else f'?b{i}' for i, x in enumerate(b)]
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


cand = []
for i, r in FM.iterrows():
    tk = tuple(r.text.split('-'))
    for j, o in LP.iterrows():
        if abs(o.ft - r.ft) <= 1.0:
            sc = sim(tk, o.tok)
            if sc >= 0.25: cand.append((sc - 0.01 * abs(o.ft - r.ft), i, j))
cand.sort(reverse=True)
um, ul = set(), set()
for sc, i, j in cand:
    if i in um or j in ul: continue
    um.add(i); ul.add(j)
FM['same_stone'] = FM.index.isin(um)
print(f'[object match] second-catalogue DK-G seals {len(FM)}; same stone as a first-catalogue seal {len(um)}; with no matching stone {int((~FM.same_stone).sum())}')
print(f'   by the earlier crosswalk flag (no partner TEXT): {int((~FM.partnered).sum())}; the two agree on {int(((~FM.partnered) & (~FM.same_stone)).sum())} seals; {int(((~FM.partnered) & FM.same_stone).sum())} "new text" seals are re-transcriptions of a first-catalogue stone')
new = FM[~FM.same_stone].copy()
print(f'[second catalogue] DK-G seals with a depth: {len(FM)}; no matching first-catalogue stone: {len(new)}; at the earliest level: {int((FM.lvl == 0).sum())} (of which no matching stone {int((new.lvl == 0).sum())})')

# ------------------------------------------------------------------ the numbers by level
cols = ['hasname', 'fishfirst', 'fishfirst_clean', 'anymarked', 'anyfish', 'agent', 'jar', 'spear', 'office', 'boxcot', 'starname', 'short', 'noanimal']
U = pd.concat([FL.assign(src='first'), new.assign(src='new')], ignore_index=True)


def table(df, label):
    rows = []
    for l, g in df.groupby('lvl'):
        e = g  # seals
        ag_den = int((g.jar | g.spear).sum())
        rows.append(dict(set=label, level=l, seals=len(g), named=int(g.hasname.sum()), fishfirst=int(g.fishfirst.sum()), fishclean=int(g.fishfirst_clean.sum()),
                         anymarked=int(g.anymarked.sum()), anyfish=int(g.anyfish.sum()), agent=int(g.agent.sum()), jar=int(g.jar.sum()),
                         spear=int(g.spear.sum()), office=int(g.office.sum()), boxcot=int(g.boxcot.sum()), starname=int(g.starname.sum()),
                         short=int(g.short.sum()), noanimal=int(g.noanimal.sum()), median_len=float(g.n.median()), median_ft=float(g.ft.median())))
    return pd.DataFrame(rows)


TB = pd.concat([table(FL, 'first catalogue'), table(new, 'second catalogue, extra stones'), table(FM, 'second catalogue, all'), table(U, 'union (first + new)')])
TB.to_csv(f'{OUTE}/dkg_union_levels.csv', index=False)
print(TB.to_string(index=False))


def early_vs_later(df, col, label):
    a = df[df.lvl == 0]; b = df[df.lvl > 0]
    t = [[int(a[col].sum()), len(a) - int(a[col].sum())], [int(b[col].sum()), len(b) - int(b[col].sum())]]
    p = fisher_exact(t)[1]
    print(f'  {label:34s} {col:10s} earliest {t[0][0]}/{len(a)} ({100 * t[0][0] / max(1, len(a)):.1f}%) against later {t[1][0]}/{len(b)} ({100 * t[1][0] / max(1, len(b)):.1f}%), Fisher P {p:.3g}')
    return t[0][0], len(a), t[1][0], len(b), p


print('\nEARLIEST LEVEL AGAINST ALL LATER LEVELS')
for lab, df in [('first catalogue', FL), ('second catalogue, extra stones', new), ('second catalogue, all', FM), ('union (first + new)', U)]:
    for c in ['fishfirst', 'fishfirst_clean', 'anymarked', 'anyfish', 'agent', 'office', 'boxcot', 'short', 'starname']:
        early_vs_later(df, c, lab)
    print()

# where the fish stands: among names that hold a marked fish, how often is it the FIRST name sign?
from scipy.stats import binomtest
print('\nAMONG NAMES WITH A MARKED FISH, THE FISH IS THE FIRST NAME SIGN')
for lab, df in [('first catalogue', FL), ('union (first + extra stones)', U)]:
    w = df[df.anymarked]; a, b = w[w.lvl == 0], w[w.lvl > 0]
    t = [[int(a.fishfirst.sum()), len(a) - int(a.fishfirst.sum())], [int(b.fishfirst.sum()), len(b) - int(b.fishfirst.sum())]]
    print(f'  {lab}: earliest {t[0][0]}/{len(a)}; later {t[1][0]}/{len(b)} ({100 * t[1][0] / len(b):.0f}%); Fisher P {fisher_exact(t)[1]:.3g}; clean (no lost sign before it): earliest {int(a.fishfirst_clean.sum())}/{len(a)}, later {int(b.fishfirst_clean.sum())}/{len(b)}')
    print('   position of the first marked fish in the name (0 = first), earliest:', sorted(a.fishpos.tolist()), '| later share at position 0, 1, 2, 3+:', [int((b.fishpos == k).sum()) for k in (0, 1, 2)], int((b.fishpos >= 3).sum()))
for lab, df in [('first catalogue', FL), ('union', U)]:
    nl = df[(df.lvl > 0) & df.hasname]; p0 = nl.fishfirst.mean()
    e = df[(df.lvl == 0) & df.hasname]
    for col in ('fishfirst', 'fishfirst_clean'):
        k = int(e[col].sum()); n = len(e); p_ = nl[col].mean()
        print(f'  {lab}: {col} among named seals, earliest {k}/{n}; later rate {100 * p_:.1f}%; chance of {k} or fewer at the later rate (binomial) {binomtest(k, n, p_, alternative="less").pvalue:.3g}')

# fish stands later in longer names; control for name length
print('\nSAME TEST HOLDING NAME LENGTH: among marked-fish names, first-position rate by name length (union)')
w = U[U.anymarked].copy(); w['lenband'] = pd.cut(w.nmlen, [0, 3, 5, 99], labels=['1-3 signs', '4-5 signs', '6+ signs'])
for lb, g in w.groupby('lenband', observed=True):
    a, b = g[g.lvl == 0], g[g.lvl > 0]
    print(f'  {lb}: earliest fish-first {int(a.fishfirst_clean.sum())}/{len(a)}; later {int(b.fishfirst_clean.sum())}/{len(b)} ({100 * b.fishfirst_clean.mean():.0f}%)')
a, b = w[w.lvl == 0], w[w.lvl > 0]
print(f'  all lengths, clean first position: earliest {int(a.fishfirst_clean.sum())}/{len(a)} against later {int(b.fishfirst_clean.sum())}/{len(b)}; Fisher P {fisher_exact([[int(a.fishfirst_clean.sum()), len(a) - int(a.fishfirst_clean.sum())], [int(b.fishfirst_clean.sum()), len(b) - int(b.fishfirst_clean.sum())]])[1]:.3g}')
print('  earliest-level names with a marked fish (union):')
for _, r in a.iterrows(): print('    ', r.id, r.text, '| name length', r.nmlen, '| fish position', r.fishpos)

# agent rate needs seals with an ending, so the denominators for the agent form are jar or spear seals
for lab, df in [('first catalogue', FL), ('union', U)]:
    en = df[df.jar | df.spear]
    a, b = en[en.lvl == 0], en[en.lvl > 0]
    print(f'agents among seals with a jar or spear ending, {lab}: earliest {int(a.agent.sum())}/{len(a)}, later {int(b.agent.sum())}/{len(b)}')

# ------------------------------------------------------------------ the earliest seals read whole
E0 = U[U.lvl == 0].copy().sort_values(['src', 'ft'], ascending=[True, False])
CE = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('')
CEg = CE.groupby('object_id').agg(sounds=('sounds', ' | '.join), english=('english', ' '.join), grade=('grade', ','.join))
SOUND, READ = cb.SOUND, cb.READ
rd_rows = []
for _, r in E0.iterrows():
    x = r.text.split('-')
    if r.src == 'first':
        c = CEg.loc[str(r.obj)] if str(r.obj) in CEg.index else None
        snd, eng, gr = (c.sounds, c.english, c.grade) if c is not None else ('', '', '')
    else:
        rr = parse_face(tuple(x), lex)
        eng, parts, op = cb.build(tuple(x), rr, 'seal')
        snd = ' '.join(SOUND.get(s, f'[{s}]') if s in READ else (f'[{s}]' if s not in ('000', 'ALT') else '[lost]') for s in x)
        gr = cb.grade(x, set(), READ)
    rd_rows.append(dict(src=r.src, id=r.id, depth_ft=round(r.ft, 1), text=r.text, sounds=snd, english=eng, grade=gr, first=r['first'], fishfirst=r.fishfirst,
                        anymarked=r.anymarked, agent=r.agent, office=r.office, short=r.short))
RD = pd.DataFrame(rd_rows)
RD.to_csv(f'{OUTE}/early_level_read.csv', index=False)
U.to_csv(f'{OUTE}/early_level_seals.csv', index=False)
print(f'\nEARLIEST LEVEL: {len(RD)} seals (first catalogue {int((RD.src == "first").sum())}, new second-catalogue {int((RD.src == "new").sum())})')
print(RD[['src', 'id', 'depth_ft', 'text', 'sounds', 'english']].to_string(index=False))

# ------------------------------------------------------------------ what stands in the crest slot, by level
print('\nFIRST NAME SIGN (the crest slot) by level, union; top signs per level')
for l, g in U.groupby('lvl'):
    c = collections.Counter(g[g.first != ''].first)
    print(f'  level {l} ({len(g)} seals, {int((g["first"] != "").sum())} with a first name sign):', c.most_common(8))
