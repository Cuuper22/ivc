"""Goods job step 6: thirty goods tags, pots, rods, bangles, tools and tablets read whole. Looks every object up in the corpus
(so site, type, material, findspot are the data's own) and writes goods_out/thirty_reads.md. Readings are guesses built on goods_table values."""
from goods_common import *
d=load()
S=lambda x:x.split()
def find(cisi=None,text=None,cls=None,site=None,typ=None,area=None,idx=0):
    m=pd.Series(True,index=d.index)
    if cisi: m&=d.cisi==cisi
    if text: m&=d.toks.apply(lambda t:t==S(text))
    if cls: m&=d.cls==cls
    if site: m&=d.site==site
    if typ: m&=d.type==typ
    if area: m&=d['area-section']==area
    x=d[m]
    if len(x)==0: return None,0
    return x.iloc[idx],len(x)
R=[
 (dict(cisi='L-124',text='705 500 741 001 055 220 740 090'),'One dozen fish, of the First-ward [tag] house; its man (agent).','goods tag (leather-sack type TAG:L), clay; one stone, 11 objects all at Lothal on three container types (5 TAG:L, 5 TAG, 1 TAG:W)'),
 (dict(cisi='L-161',text='817 002 048 740'),'Two shares: a bundle of seven, of the house.','sealing of a wooden box (TAG:B) with an elephant seal; 10 identical at Lothal; the same four signs on a Mohenjo-daro seal'),
 (dict(cisi='L-153',text='838'),'Sesame (eḷ) - or bone/tusk (eḷumpu); the whole text.','goods tag, Lothal warehouse'),
 (dict(cisi='C-19',text='838'),'Sesame (or bone/tusk); the whole text.','steatite square seal, Chanhu-daro craft town'),
 (dict(cisi='L-143',text='920 060 004 220 388 740'),'In the opening month: four fish, of the royal (aracu) house.','goods tag, Lothal'),
 (dict(cisi='K-69',text='091 056 002 417 890 892'),'For the Pair (partners): lot 056, two twin-fork bundles, 890, for sale (vil).','terracotta goods tag; 8 identical at Kalibangan, 7 in area KLB-1'),
 (dict(cisi='L-130',text='861 002 236'),'Two shares of the Bamboo-star-cluster [house].','goods tag, Lothal; 2 identical'),
 (dict(cisi='L-146',text='705 033 520'),'Assembly-place, three, chief.','tag with cane-packing reverse (TAG:O), Lothal'),
 (dict(cisi='H-1394',text='003 220 590'),'Three fish, bin.','pot (POT:T:g), Harappa granary area'),
 (dict(cisi='H-2336',text='220 495 463 740'),'Fish, [striped horn], Three-peaks, of the house.','pot, Harappa'),
 (dict(cisi='H-1732',text='480 805 158'),'One kuṉṟi-measure, 805, carried.','small pot (POT:T:s), Harappa'),
 (dict(cisi='H-1726',text='817 002 491 692 100 740'),'Two shares, 491, the 692-office, the three-headed man, of the house.','pot (POT:T:s), Harappa trench 43'),
 (dict(cisi='M-2106',text='240 838 585 740 400'),'The High-star [house]: bone/tusk (or sesame), the Seven, of the house, junior.','bone rod, Mohenjo-daro DKG; same text on ivory rod M-1651'),
 (dict(cisi='M-2086',text='838 482 740'),'Bone/tusk (eḷ), tusk-summit (kōṭu), of the house.','ivory rod, Mohenjo-daro DK; twin M-2102'),
 (dict(cisi='M-2107',text='240 013 840 740 400'),'The High-star house: three pairs, of the house, junior.','ivory rod, Mohenjo-daro HRB; twin M-2108'),
 (dict(cisi='M-2097',text='176 740 400'),'The tax-man\'s house, junior.','ivory rod, Mohenjo-daro DK'),
 (dict(cisi='H-2570',text='001 034 700'),'One, four cups.','bone rod, Harappa E trench 55'),
 (dict(cisi='M-2121',text='391 595 850 480 001 821'),'[391]-maker, fold/workshop, copper (kaṉ, eye-sign), one kuṉṟi, a quarter.','copper tool, Mohenjo-daro DKG(S); same text on M-2118 and one more'),
 (dict(cisi='H-380',text='920 632 930'),'Opening-month, many (pal), 930.','copper tool, Harappa; twin H-381'),
 (dict(cisi='M-2129',text='817 002 645 017 898'),'Two shares, X-unit, seven, 898.','gold object, Mohenjo-daro DKE'),
 (dict(cisi='H-1009',text='840'),'A pair (iṇai).','bangle, Harappa'),
 (dict(cisi='M-2079',text='630 845'),'Many, [hatched pair].','stoneware bangle, Mohenjo-daro DKC'),
 (dict(cisi='M-1659',text='706 140'),'Assembly-place, lady (ammai).','bangle, Mohenjo-daro'),
 (dict(cisi='H-278',text='803 415 220 318 920 255 436 690 590 407 740'),'House [il], branch, fish, 318, opening-month, chief, 436, bound, bin, tree-lot, of the house.','steatite tablet; 11 copies, all Harappa, 7 in the granary area'),
 (dict(cisi='H-2229',text='003 861'),'Three shares (hands) | 4 cups | 3 loads: the E-11 ration chit.','steatite tablet face 1 of 3, Harappa E trench 11'),
 (dict(cisi='M-437',text='820 002 590 390 740'),'Two quarters: bin, tree (timber), of the house.','pot-mouth tag, Mohenjo-daro DKG(S)'),
 (dict(cisi='K-85',text='861 002 033 520'),'Two shares, three, chief.','tag, Kalibangan'),
 (dict(cisi='H-1761',text='440'),'Received / bought (koḷ).','small pot (POT:T:s); 12 small pots carry this one sign, all at Harappa, 7 in trench 43'),
 (dict(text='503 615 752 740',cls='tabC'),'Hill, field, child-of, of the house: a copper-tablet deed.','copper tablet; 29 identical copper tablets, all Mohenjo-daro'),
 (dict(cisi='C-40',idx=1,text='066 900 031 235 240 835 000 740'),'Tall-066, crescent, one, fish-hat, High-star, 835, [lost], of the house.','copper tool, Chanhu-daro'),
]
out=['| # | object | site / findspot | type, material | text in reading order | reading |','|---|---|---|---|---|---|']
bad=0
for i,(k,eng,note) in enumerate(R,1):
    k2={a:b for a,b in k.items() if a!='idx'}
    r,n=find(**k2,idx=k.get('idx',0)) if 'idx' not in k else find(cisi=k['cisi'],idx=k['idx'])
    if r is None:
        # fall back to text only
        r,n=find(text=k['text']);
        if r is None: print('NOT FOUND',k); bad+=1; continue
    out.append(f"| {i} | {r.cisi if r.cisi!='-' else 'id '+r.id}: {note} | {r.site}; {r['area-section'].strip('-') or 'no findspot'} | {r.type}, {r.material} | `{' '.join(r.toks)}` | {eng} |")
open(f'{OUT}/thirty_reads.md','w').write('\n'.join(out))
print('\n'.join(out)); print('missing',bad)
