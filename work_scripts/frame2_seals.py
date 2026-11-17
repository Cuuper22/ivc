#!/usr/bin/env python3
"""JOB 2: the two kinds of seal. Everything below down to the line '# ---- numbers' was written 2026-11-17 before any number.

SPLIT (by machine, v2 base classes, frame2_common.v2_type), one text per seal object (its longest face):
  damaged          lost or unclear sign, or broken edge
  name seal        v2 'name text' pattern: [front word + slot]? [name signs] [closer] [title]?   (or a title as last sign)
  opener count     v2 'count line' starting with a front word: [front word][slot]? ([number] [counted thing])+
  bare count       v2 'count line' with no front word: ([number] [counted thing])+
  name + count     v2 'record': name text, closer, then a count line
  title alone / front alone / measure line   as in frame2_common
  loose name       not fitting any pattern but holding a closer or title  (kept apart from 'name seal')
  other            the rest
  'count-line seal' = opener count + bare count.

PREDICTIONS (count-line seals against name seals):
  (a) size and shape: count-line seals are SMALLER (median face area) and more often have NO animal; the round and
      cylinder shapes are more common among them.
  (b) animal: the short-horned bull with trough is MORE common on count-line seals.
  (c) findspot: count-line seals sit MORE often at the ports (Lothal, Bala-kot, Gola Dhoro) and in store / public areas
      (Harappa granary area 'FGranery'/'FGranary', Harappa mound AB, Mohenjo-daro SD mound, Dholavira Castle and Bailey,
      the warehouse site Khirsara) than in the house areas (Mohenjo-daro DK, HR, VS, L areas; Dholavira Middle and Lower
      Town). The catalogue has no gateway label, so gateways cannot be split off.
  (d) sealing: the exact same text is found on a clay sealing or tag (first-catalogue TAG faces, second-catalogue
      'sealing' lines) MORE often for count-line seals; checked also against name seals of the same length.
  (e) time: count-line seals are EARLIER (more in the early bin; counting came before names).
  (f) abroad: count-line seals are found abroad (Gulf, Mesopotamia, Iran, Central Asia) MORE often.
  THINGS: the counted things on count-line seals are the SAME signs that are counted on tablets and tags (a sign right
      after a number on a tablet, copper tablet or tag face): share of count-line thing uses whose sign is counted on
      tablets/tags at least twice, against the same share for the sign after a number on name seals.
DECOY for every difference: the v2 base labels dealt among signs of the same frequency band (20 deals, seeds 500-519),
  the seals split again with the decoy labels, the same difference computed.
Output: work_data/frame/seal_kinds.csv (one row per seal object), seal_kind_tests.csv, seal_things.csv, log_seals.txt
"""
from frame2_common import *
from frame2_pictures import pic
import io as _io
with contextlib.redirect_stdout(_io.StringIO()):
    import time_common as tc
from scipy.stats import mannwhitneyu, fisher_exact

c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
V2B = dict(zip(c2.sign, c2.v2_base))
ABROAD = {'Persian Gulf', 'Mesopotamia', 'Iranian Plateau', 'Central Asia'}
PORT = {'Lothal', 'Bala-kot', 'Gola Dhoro (Bagasra)'}


def spot(site, area):
    a = str(area)
    if site in PORT: return 'port'
    if site == 'Khirsara': return 'store/public'
    if site == 'Harappa' and (a.startswith('FGran') or a.startswith('AB')): return 'store/public'
    if site == 'Mohenjo-daro' and a.startswith('SD'): return 'store/public'
    if site == 'Dholavira' and (a.startswith('Castle') or a.startswith('Bailey')): return 'store/public'
    if site == 'Mohenjo-daro' and re.match(r'^(DK|HR|VS|L)', a): return 'house'
    if site == 'Dholavira' and (a.startswith('Middle Town') or a.startswith('Lower Town')): return 'house'
    return ''


def seal_kind(x, flg, mp):
    if not x or set(x) & UNK or flg & {'broken', 'lost', 'alt'}: return 'damaged'
    cl = [mp.get(s, 'PERSONAL') for s in x]
    t = v2_type(cl, 'seal')
    if t == 'count line': return 'opener count' if cl[0] == 'OPEN' else 'bare count'
    if t == 'name text': return 'name seal'
    if t == 'record': return 'name + count'
    if t: return t
    if 'CLOSER' in cl or 'TITLE' in cl: return 'loose name'
    return 'other'


# seal objects: longest face
S = d[d.kind == 'seal'].copy()
S['n'] = S.tok.map(len)
S = S.sort_values('n', ascending=False).drop_duplicates('obj')
AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
S['animal'] = AB.animal.reindex(S.obj).values
S['area_mm2'] = pd.to_numeric(S['horizontal(mm)'], errors='coerce') * pd.to_numeric(S['vertical(mm)'], errors='coerce')
S.loc[S.area_mm2 <= 0, 'area_mm2'] = np.nan
S['shape'] = S.type.map({'SEAL:S': 'square', 'SEAL:R': 'rectangle', 'SEAL:C': 'round', 'SEAL:CY': 'cylinder'}).fillna('other')
S['spot'] = [spot(a, b) for a, b in zip(S.site, S['area-section'])]
S['abroad'] = S.region.isin(ABROAD)
S['bin'] = tc.T['bin'].reindex(S.obj).values
# sealing texts
seal_txt = set('-'.join(x) for x, k in zip(d.tok, d.kind) if k == 'tag' and x and not set(x) & UNK)
seal_txt |= set('-'.join(x) for x, k in zip(M.tok, M.kind) if k == 'tag' and x and not set(x) & UNK)
S['text'] = S.tok.map('-'.join)
S['on_sealing'] = S.text.isin(seal_txt)
S['seal_kind'] = [seal_kind(x, f, V2B) for x, f in zip(S.tok, S.flg)]
S['count_line'] = S.seal_kind.isin(['opener count', 'bare count'])
S['name'] = S.seal_kind == 'name seal'

# counted things on tablets and tags (sign right after a v2 number)
NUMS = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
tab_counted = collections.Counter()
for x, k in list(zip(d.tok, d.kind)) + list(zip(M[~M.partnered].tok, M[~M.partnered].kind)):
    if k in ('mtab', 'ctab', 'tag'):
        for a, b in zip(x, x[1:]):
            if V2B.get(a) in NUMS and b not in UNK and V2B.get(b) not in NUMS: tab_counted[b] += 1


def measures(S_, mp):
    """the six differences, count-line minus name seals. returns dict."""
    kinds = [seal_kind(x, f, mp) for x, f in zip(S_.tok, S_.flg)]
    cl = np.array([k in ('opener count', 'bare count') for k in kinds]); nm = np.array([k == 'name seal' for k in kinds])
    out = dict(n_count=int(cl.sum()), n_name=int(nm.sum()))
    if cl.sum() < 3 or nm.sum() < 3: return out
    a = S_.area_mm2.values
    out['median_area_count'] = np.nanmedian(a[cl]); out['median_area_name'] = np.nanmedian(a[nm])
    out['area_diff'] = out['median_area_count'] - out['median_area_name']
    noan = S_.animal.isin(['NONE']).values
    out['no_animal_diff'] = noan[cl].mean() - noan[nm].mean()
    sh = (S_.animal == 'SHORTHORN').values
    out['shorthorn_diff'] = sh[cl].mean() - sh[nm].mean()
    rd = S_['shape'].isin(['round', 'cylinder']).values
    out['round_diff'] = rd[cl].mean() - rd[nm].mean()
    sp = S_.spot.values
    def share_ps(m):
        v = sp[m]; z = v[v != '']
        return np.mean(np.isin(z, ['port', 'store/public'])) if len(z) else np.nan
    out['port_store_diff'] = share_ps(cl) - share_ps(nm)
    ons = S_.on_sealing.values
    out['sealing_diff'] = ons[cl].mean() - ons[nm].mean()
    b = S_['bin'].values
    def early(m):
        v = b[m]; v = v[pd.notna(v)]
        return np.mean(v == 'early') if len(v) else np.nan
    out['early_diff'] = early(cl) - early(nm)
    ab = S_.abroad.values
    out['abroad_diff'] = ab[cl].mean() - ab[nm].mean()
    return out


# ---- numbers
log(f'seal objects {len(S)}; kinds: ' + ', '.join(f'{k} {v}' for k, v in S.seal_kind.value_counts().items()))
real = measures(S, V2B)
T = train_texts(); vocab, idx = vocab_of(T); C = counts(T, idx)
band = freq_band({s: int(C['uni'][idx[s]]) for s in vocab})
dec = [measures(S, deal_within_bands({s: V2B[s] for s in vocab}, band, q)) for q in range(500, 520)]
D = pd.DataFrame(dec)
rows = []
for k, v in real.items():
    dv = D[k].dropna() if k in D else pd.Series(dtype=float)
    rows.append(dict(measure=k, real=v, decoy_mean=dv.mean() if len(dv) else np.nan, decoy_min=dv.min() if len(dv) else np.nan,
                     decoy_max=dv.max() if len(dv) else np.nan, decoys_valid=len(dv)))
    log(f'  {k:22s} real {v:9.3f} | decoy mean {dv.mean():9.3f} range {dv.min():.3f} .. {dv.max():.3f} ({len(dv)} decoys with 3+ of each kind)')
R = pd.DataFrame(rows)

# plain tables per kind, with tests
grp = S[S.seal_kind.isin(['name seal', 'opener count', 'bare count', 'name + count', 'title alone', 'loose name', 'other', 'front alone', 'measure line'])]
tab = grp.groupby('seal_kind').agg(n=('obj', 'size'), median_area=('area_mm2', 'median'), no_animal=('animal', lambda a: (a == 'NONE').mean()),
                                    unicorn=('animal', lambda a: (a == 'UNICORN').mean()), shorthorn=('animal', lambda a: (a == 'SHORTHORN').mean()),
                                    round_or_cyl=('shape', lambda s: s.isin(['round', 'cylinder']).mean()), rectangle=('shape', lambda s: (s == 'rectangle').mean()),
                                    on_sealing=('on_sealing', 'mean'), abroad=('abroad', 'mean'), mean_len=('n', 'mean'))
log('\n' + tab.round(3).to_string())
CL = S[S.count_line]; NM = S[S.name]
tests = []
def t2(name, a, b, c, e):
    o, p = fisher_exact([[a, b], [c, e]]); tests.append(dict(test=name, count_line=f'{a} of {a + b}', name_seals=f'{c} of {c + e}', odds=o, p=p))
    log(f'  {name}: count-line {a} of {a + b} ({a / max(a + b, 1):.1%}) against name seals {c} of {c + e} ({c / max(c + e, 1):.1%}); Fisher P {p:.3g}')
u = mannwhitneyu(CL.area_mm2.dropna(), NM.area_mm2.dropna())
log(f'  (a) face area median: count-line {CL.area_mm2.median():.0f} mm2 (n {CL.area_mm2.notna().sum()}) against name seals {NM.area_mm2.median():.0f} (n {NM.area_mm2.notna().sum()}); Mann-Whitney P {u.pvalue:.3g}')
tests.append(dict(test='(a) face area', count_line=f'median {CL.area_mm2.median():.0f}', name_seals=f'median {NM.area_mm2.median():.0f}', p=u.pvalue))
for lab, col in [('(a) no animal', CL.animal == 'NONE'), ('(a) round or cylinder', CL['shape'].isin(['round', 'cylinder'])),
                 ('(a) rectangle', CL['shape'] == 'rectangle'), ('(b) short-horned bull', CL.animal == 'SHORTHORN'), ('(b) unicorn', CL.animal == 'UNICORN')]:
    colN = {'(a) no animal': NM.animal == 'NONE', '(a) round or cylinder': NM['shape'].isin(['round', 'cylinder']), '(a) rectangle': NM['shape'] == 'rectangle',
            '(b) short-horned bull': NM.animal == 'SHORTHORN', '(b) unicorn': NM.animal == 'UNICORN'}[lab]
    t2(lab, int(col.sum()), int((~col).sum()), int(colN.sum()), int((~colN).sum()))
for lab, keep in [('(c) port or store/public, among seals with a classed findspot', ['port', 'store/public']), ('(c) port only', ['port']), ('(c) store/public only', ['store/public'])]:
    a_ = CL[CL.spot != '']; b_ = NM[NM.spot != '']
    t2(lab, int(a_.spot.isin(keep).sum()), int((~a_.spot.isin(keep)).sum()), int(b_.spot.isin(keep).sum()), int((~b_.spot.isin(keep)).sum()))
t2('(d) same text on a sealing or tag', int(CL.on_sealing.sum()), int((~CL.on_sealing).sum()), int(NM.on_sealing.sum()), int((~NM.on_sealing).sum()))
NL = NM[NM.n.isin(CL.n.unique())]
# length-matched: weight name seals to the count-line length mix
w = CL.n.value_counts(normalize=True)
lm = sum(w.get(L, 0) * NL[NL.n == L].on_sealing.mean() for L in w.index if (NL.n == L).any())
log(f'  (d) length-matched: name seals of the same lengths would be on a sealing {lm:.1%} of the time (count-line {CL.on_sealing.mean():.1%})')
for lab, b_ in [('(e) early bin, among dated', 'early'), ('(e) late bin, among dated', 'late')]:
    a_ = CL[CL['bin'].notna()]; c_ = NM[NM['bin'].notna()]
    t2(lab, int((a_['bin'] == b_).sum()), int((a_['bin'] != b_).sum()), int((c_['bin'] == b_).sum()), int((c_['bin'] != b_).sum()))
t2('(f) found abroad', int(CL.abroad.sum()), int((~CL.abroad).sum()), int(NM.abroad.sum()), int((~NM.abroad).sum()))
log('  count-line seals by site: ' + ', '.join(f'{k} {v}' for k, v in CL.site.value_counts().items()))
log('  name seals by site (top): ' + ', '.join(f'{k} {v}' for k, v in NM.site.value_counts().head(8).items()))
log('  count-line seals by findspot: ' + ', '.join(f'{k or "unclassed"} {v}' for k, v in CL.spot.value_counts().items()))
log('  name seals by findspot: ' + ', '.join(f'{k or "unclassed"} {v}' for k, v in NM.spot.value_counts().items()))
log('  count-line seals by animal: ' + ', '.join(f'{k} {v}' for k, v in CL.animal.value_counts().items()))
log('  count-line seals by shape: ' + ', '.join(f'{k} {v}' for k, v in CL['shape'].value_counts().items()))

# THINGS
things = collections.Counter(); nums = collections.Counter(); front = collections.Counter()
for x in CL.tok:
    cl = [V2B.get(s, 'PERSONAL') for s in x]
    for i, c in enumerate(cl):
        if c == 'THING': things[x[i]] += 1
        if c in NUMS: nums[x[i]] += 1
    if cl[0] == 'OPEN': front['-'.join(x[:2]) if len(x) > 1 and cl[1] == 'SLOT' else x[0]] += 1
nt = collections.Counter()
for x in NM.tok:
    for a, b in zip(x, x[1:]):
        if V2B.get(a) in NUMS and V2B.get(b) not in NUMS: nt[b] += 1
sh_cl = sum(v for s, v in things.items() if tab_counted[s] >= 2) / max(sum(things.values()), 1)
sh_nm = sum(v for s, v in nt.items() if tab_counted[s] >= 2) / max(sum(nt.values()), 1)
log(f'THINGS on count-line seals: ' + ', '.join(f'{s} [{pic(s)}] {v} (counted on tablets/tags {tab_counted[s]}x)' for s, v in things.most_common(15)))
log(f'  share of count-line thing uses whose sign is counted on tablets/tags 2+ times: {sh_cl:.0%}; same for the sign after a number on name seals: {sh_nm:.0%}')
log('  numbers on count-line seals: ' + ', '.join(f'{s} [{pic(s)}] {v}' for s, v in nums.most_common(10)))
log('  front words on count-line seals: ' + ', '.join(f'{s} {v}' for s, v in front.most_common(10)))
log('  top counted things on tablets/tags: ' + ', '.join(f'{s} [{pic(s)}] {v}' for s, v in tab_counted.most_common(15)))
pd.DataFrame([dict(sign=s, picture=pic(s), on_count_line_seals=v, counted_on_tablets_tags=tab_counted[s]) for s, v in things.most_common()]).to_csv(f'{OUT2}/seal_things.csv', index=False)
pd.concat([R, pd.DataFrame(tests)]).to_csv(f'{OUT2}/seal_kind_tests.csv', index=False)
S[['id', 'obj', 'cisi', 'site', 'region', 'area-section', 'type', 'shape', 'animal', 'area_mm2', 'spot', 'bin', 'abroad', 'on_sealing', 'text', 'seal_kind']].to_csv(f'{OUT2}/seal_kinds.csv', index=False)
for k in ['opener count', 'bare count']:
    log(f'  examples {k}: ' + ' | '.join(f'{r.site}: {r.text}' for r in S[S.seal_kind == k].head(12).itertuples()))

# REDESIGN of the decoy (written after the frequency-band decoys produced 3+ count-line seals in only 2 of 20 deals):
# draw, 2,000 times, 75 undamaged seals that are NOT count-line seals with the same text-length mix as the count-line seals,
# and compute each measure; report the share of draws reaching the real count-line value.
pool = S[(S.seal_kind != 'damaged') & ~S.count_line]
rs = np.random.default_rng(31)
bylen = {L: pool[pool.n == L] for L in CL.n.unique()}
def mvals(X):
    sp = X.spot[X.spot != '']
    dt = X['bin'][X['bin'].notna()]
    return dict(area=X.area_mm2.median(), shorthorn=(X.animal == 'SHORTHORN').mean(), no_animal=(X.animal == 'NONE').mean(),
                port_store=sp.isin(['port', 'store/public']).mean(), sealing=X.on_sealing.mean(), early=(dt == 'early').mean(), abroad=X.abroad.mean())
realv = mvals(CL); draws = []
for _ in range(2000):
    parts = [bylen[L].sample(n=c, replace=len(bylen[L]) < c, random_state=int(rs.integers(1e9))) for L, c in CL.n.value_counts().items() if len(bylen[L])]
    draws.append(mvals(pd.concat(parts)))
DR = pd.DataFrame(draws)
for k, v in realv.items():
    hi = (DR[k] >= v).mean(); lo = (DR[k] <= v).mean()
    log(f'  length-matched draw [{k}]: count-line {v:.3f} | draws mean {DR[k].mean():.3f}; share of draws at or above {hi:.3f}, at or below {lo:.3f}')
DR.describe().to_csv(f'{OUT2}/seal_length_matched_draws.csv')
hit = CL[CL.on_sealing]
log('  count-line texts also on sealings: ' + ' | '.join(f'{r.site}: {r.text}' for r in hit.itertuples()))
