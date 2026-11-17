"""PART 3. The fibre family: 390 (cotton), 405, 407 (same tree drawing, ticked branches).
Run: python3 cotton_3_fibre.py  (log -> cotton_out/fibre_log.txt, tables cotton_out/fibre_*.csv)

JOBS AND WORDS, WITH PREDICTIONS WRITTEN FIRST (DEDR numbers from work_data/lexicons/dedr)
 390 = RAW COTTON, parutti (3976) / pañci (3836): counted in lots of bales; near fields/craft towns; the box name; whorls.
 405 = THREAD or SKEIN, nūl "yarn, cotton thread" (3726) or cīṭu "skein of thread" (2611) or ir̤ai "yarn" (506).
   P405a counted in lots of 3 or more at least 85% (a skein is counted in tens); P405b seen at craft places like 390: Chanhu-daro, dyers' quarter above 1.3x; P405c NOT on copper tablets (<=1.5x); P405d shares objects with 390 above chance (a house selling cotton and yarn).
 407 = CLOTH, tuṇi "cloth" (3307) or tukil "fine cloth" (3285) or tiṇṭu "bale of cloth" (3224, Ma./Ka.).
   P407a counted but in a mix of small and large lots (less than 85% >=3, since cloth pieces are counted singly too); P407b on goods lists (copper tablets, as 63/127 already known) above 5x; P407c seen abroad >= 1.5x (Ur III weaver lists, cloth exported); P407d when two members share a face, order is 390 or 405 before 407 (raw -> thread -> cloth) more often than the reverse.
 DYE (cāyam 2457, kāvi 1490 red ochre, aviri 269 indigo, tōmpu 3553 red dye): a dye sign should be enriched in the dyers' quarter above 390's 2.0x and be counted in small numbers, and be rare on seals abroad. No sign is picked first: a scan of every sign with >=4 faces in the quarter is run, and any with ratio >=3 is named.
"""
from cotton_common import *
from scipy.stats import binomtest
f = open(f'{OUTC}/fibre_log.txt', 'w')
d = faces(); T = d.toks.tolist(); N = len(d)
FOREIGN = ['Ur','Susa','Kish',"Qala'at al-Bahrain",'Failaka',"Ra's al-Junayz",'Hajar','Luristan','Nippur','Tell Umma','Tello','Tepe Yahya','Gonur Depe','Girsu','Saar','Janabiyah','Kalba','Altyn Depe','Shortughai','Salut','Karzakan','Sibri','Murda Sang']
NUMS = {k: v for k, v in CNT.items() if v[0] != 'A'}
zones = {
 'dyers quarter (Mohenjo-daro VS)': d['area-section'].str.startswith('VS') & d.site.eq('Mohenjo-daro'),
 'Chanhu-daro': d.site.eq('Chanhu-daro'),
 'abroad': d.site.isin(FOREIGN),
 'Harappa granary': d.gran,
 'Lothal': d.site.eq('Lothal'),
 'copper tablets': d.mat.eq('copper') & d.cls.isin(['tabB', 'tabI', 'tabC']),
 'Kalibangan': d.site.eq('Kalibangan'),
 'Dholavira': d.site.eq('Dholavira'),
}
rows = []
for s in ['390', '405', '407']:
    h = d.toks.apply(lambda t: s in t)
    nn = int(h.sum())
    cn = [(NUMS[t[j-1]]) for t in T for j, x in enumerate(t) if x == s and j > 0 and t[j-1] in NUMS]
    ser = collections.Counter(c[0] for c in cn)
    vals = [c[1] for c in cn]
    boxed = sum(1 for t in T for j, x in enumerate(t) if x == s and j > 0 and t[j-1] == '590')
    log(f, f'\n== sign {s}: faces {nn}; counted places {len(cn)} (series {dict(ser)}); count>=3 share {np.mean([v>=3 for v in vals]):.2f}; median count {np.median(vals):.0f}; max {max(vals)}; right after the box {boxed}')
    log(f, f'   by object class: {dict(d[h].cls.value_counts())}')
    for z, m in zones.items():
        a = int((h & m).sum()); n = int(m.sum()); r, p = fe(a, n - a, int((h & ~m).sum()), int((~m).sum() - (h & ~m).sum()))
        rows.append(dict(sign=s, zone=z, faces_in_zone=n, with_sign=a, ratio=round(r, 2), P=p))
        log(f, f'   {z}: {a}/{n} -> {r:.2f}x, P {p:.3g}')
pd.DataFrame(rows).to_csv(f'{OUTC}/fibre_zones.csv', index=False)
# co-occurrence and order
log(f, '\n== co-occurrence and order (same face)')
for a_, b_ in [('390', '405'), ('390', '407'), ('405', '407')]:
    ha = d.toks.apply(lambda t: a_ in t); hb = d.toks.apply(lambda t: b_ in t)
    both = int((ha & hb).sum()); exp = ha.sum() * hb.sum() / N
    before = after_ = 0
    for t in T:
        if a_ in t and b_ in t:
            ia = t.index(a_); ib = t.index(b_)
            if ia < ib: before += 1
            elif ib < ia: after_ += 1
    p = binomtest(before, before + after_, .5, alternative='greater').pvalue if before + after_ else np.nan
    log(f, f'   {a_} & {b_} on one face: {both} (chance {exp:.1f}); {a_} before {b_}: {before}, after: {after_} (P that first is earlier {p:.3f})')
    # object-level (any face)
    oa = set(d[ha].obj); ob = set(d[hb].obj); ex = len(oa) * len(ob) / d.obj.nunique()
    log(f, f'      same object (any face): {len(oa & ob)} (chance {ex:.1f})')
# copper tablets with 407: what stands with it
cu = d[zones['copper tablets'] & d.toks.apply(lambda t: '407' in t)]
cc = collections.Counter(x for t in cu.toks for x in set(t) if x not in NUMS and x != '000')
log(f, f'\ncopper tablets carrying 407: {len(cu)}; commonest co-signs: {cc.most_common(12)}')
log(f, '   sample texts: ' + ' | '.join('-'.join(t) for t in cu.toks.head(8)))
# dye scan: every sign with >=4 faces in the dyers' quarter
m = zones['dyers quarter (Mohenjo-daro VS)']; out = []
for s in sorted({x for t in d[m].toks for x in t} - {'000', 'ALT'}):
    h = d.toks.apply(lambda t: s in t); a = int((h & m).sum())
    if a < 4: continue
    r, p = fe(a, int(m.sum()) - a, int((h & ~m).sum()), int((~m).sum() - (h & ~m).sum()))
    out.append((s, a, int(h.sum()), round(r, 2), p))
O = pd.DataFrame(out, columns=['sign', 'in_quarter', 'all_faces', 'ratio', 'P']).sort_values('ratio', ascending=False)
O.to_csv(f'{OUTC}/fibre_dyers_scan.csv', index=False)
log(f, f'\ndyers-quarter scan: {len(O)} signs with >=4 faces there; top by ratio (sign, in quarter, all faces, x, P):')
for r_ in O.head(12).itertuples(): log(f, f'   {r_.sign}: {r_.in_quarter}/{r_.all_faces} {r_.ratio}x P {r_.P:.3g}')
f.close()
