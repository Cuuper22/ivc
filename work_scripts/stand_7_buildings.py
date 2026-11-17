#!/usr/bin/env python3
"""Step 5: a stone's identity, and what each Mohenjo-daro building's set of seals looks like.
HOLDER = text + animal + stand letter (+ size): two stones are one holder only if all agree.
For each of the 40 Mohenjo-daro buildings with the most seals, compared with the same number of seals drawn at random
from the whole city (2,000 draws): CREST CONCENTRATION = share of the building's named seals that carry its commonest
crest (first name sign); SPECIES = number of different animals; LETTER CONCENTRATION = share of its unicorn letter
seals with its commonest letter; KIND mix = share of count lines + front formulas (standard / office texts).
CLASS RULE, fixed before any number:
 HOUSEHOLD = crest concentration above chance (draw P <= 0.10) and species at or above chance.
 OFFICE   = crest concentration at chance, and office/standard texts (count line + front formula) above chance (P<=0.10).
 SHOP     = letter concentration above chance (P <= 0.10) with crests at chance (one cutter's stones kept together).
 ORDINARY = none of these; a building may take two labels.
PREDICTION: most buildings ORDINARY; HOUSEHOLD in about 1 in 8; SHOP rare (letter is a city style, not a building one).
"""
from stand_common import *
rng = np.random.default_rng(7)
S = stand_seals()
md = S[S.site == 'Mohenjo-daro'].drop_duplicates('obj').reset_index(drop=True)
md['crestk'] = md.crest.where((md.signs.str.count('-') >= 1) & (md.crest != '000'), '')   # '000' = a lost sign, not a crest
md['office'] = md.kind.isin(['count line', 'front formula'])
md['sp'] = md.animal.where(md.animal != '', np.nan)
# holders city-wide
t = md[md.signs != '']
hold = t.assign(h=t.signs + '|' + t.animal + '|' + t.stand5).h
log('holders', f'Mohenjo-daro: {len(t)} stones with text, {t.signs.nunique()} different texts, {hold.nunique()} different text+animal+letter holders')
cr = t[t.crestk != ''].groupby('crestk').agg(stones=('obj', 'size'), texts=('signs', 'nunique'), buildings=('building', lambda x: x[x != ''].nunique()))
cr['holders'] = t[t.crestk != ''].assign(h=lambda x: x.signs + '|' + x.animal + '|' + x.stand5).groupby('crestk').h.nunique()
cr.sort_values('stones', ascending=False).to_csv(f'{OUT}/crest_holders.csv')
log('holders', 'top crests (stones / texts / holders / buildings):', cr.sort_values('stones', ascending=False).head(8).to_dict('index'))
for site, g in S[S.signs != ''].drop_duplicates('obj').groupby('site'):
    if len(g) >= 40: log('holders by city', site, f'{len(g)} stones, {g.signs.nunique()} texts, {(g.signs + g.animal + g.stand5).nunique()} holders')
bc = md[md.building != ''].building.value_counts()
top = bc.index[:40]
pool = md[md.building != ''].reset_index(drop=True)
def feats(g):
    named = g[g.crestk != '']
    cc = named.crestk.value_counts(); lc = g[g.stand5 != ''].stand5.value_counts()
    return dict(crest_top=(cc.iloc[0] / len(named)) if len(named) >= 3 else np.nan, n_named=len(named),
                species=g.sp.nunique(), letter_top=(lc.iloc[0] / lc.sum()) if lc.sum() >= 3 else np.nan, n_letter=int(lc.sum()),
                office=g.office.mean(), same_crest_pairs=int((cc * (cc - 1) / 2).sum()), same_letter_pairs=int((lc * (lc - 1) / 2).sum()))
rows = []
for bname in top:
    g = md[md.building == bname]; f = feats(g); n = len(g)
    sims = pd.DataFrame([feats(pool.iloc[rng.choice(len(pool), n, replace=False)]) for _ in range(2000)])
    r = dict(building=bname.replace('Mohenjo-daro|', ''), seals=n, depth_span=round(g.depth.max() - g.depth.min(), 1) if g.depth.notna().sum() >= 2 else np.nan,
             crests=g[g.crestk != ''].crestk.nunique(), top_crest=g[g.crestk != ''].crestk.value_counts().index[0] if (g.crestk != '').any() else '',
             crest_top=round(f['crest_top'], 2), crest_P=(sims.crest_top >= f['crest_top']).mean() if f['n_named'] >= 3 else np.nan,
             same_crest_pairs=f['same_crest_pairs'], scp_dealt=round(sims.same_crest_pairs.mean(), 1), scp_P=(sims.same_crest_pairs >= f['same_crest_pairs']).mean(),
             species=f['species'], species_dealt=round(sims.species.mean(), 1), species_P_low=(sims.species <= f['species']).mean(),
             animals='; '.join(f'{k} {v}' for k, v in g.sp.value_counts().items()),
             letters='; '.join(f'{k} {v}' for k, v in g[g.stand5 != ''].stand5.value_counts().items()),
             letter_top=round(f['letter_top'], 2) if f['n_letter'] >= 3 else np.nan, letter_P=(sims.letter_top >= f['letter_top']).mean() if f['n_letter'] >= 3 else np.nan,
             office=round(f['office'], 2), office_P=(sims.office >= f['office']).mean(),
             same_letter_pairs=f['same_letter_pairs'], slp_dealt=round(sims.same_letter_pairs.mean(), 1),
             agents=int((g.signs.str.contains('740-090')).sum()), median_mm2=round(g.area_mm2.median(), 0))
    lab = []
    if r['scp_P'] <= 0.10 and r['species_P_low'] > 0.10: lab.append('HOUSEHOLD')
    if r['scp_P'] > 0.10 and r['office_P'] <= 0.10: lab.append('OFFICE')
    if (r['letter_P'] <= 0.10) and r['scp_P'] > 0.10: lab.append('SHOP')
    r['class'] = '+'.join(lab) if lab else 'ORDINARY'
    rows.append(r); log('building', r['building'], r['seals'], r['class'])
B = pd.DataFrame(rows); B.to_csv(f'{OUT}/buildings_md40.csv', index=False)
log('classes', B['class'].value_counts().to_dict())
# Pooled over the 40: same-crest pairs and letter concentration against draws
log('pooled', f"same-crest pairs in the 40 buildings {B.same_crest_pairs.sum()} against {B.scp_dealt.sum():.1f} for same-size random draws")
log('pooled', f"same-letter pairs in the 40 buildings {B.same_letter_pairs.sum()} against {B.slp_dealt.sum():.1f}")
log('pooled', f"false-positive expectation per class at P<=0.10 over 40 buildings: about 4")
