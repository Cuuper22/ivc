"""Goods job step 3: the checks. Every prediction is written before its number. Output goods_out/checks.txt (also printed).
Run from work_scripts: python3 goods_3_checks.py"""
from goods_common import *
import sys
d=load(); N=len(d)
log=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); log.append(s)
has=lambda s:d.toks.apply(lambda t:s in t)
def test(name,pred,sign,group,label):
    ix=has(sign) if isinstance(sign,str) else d.toks.apply(lambda t:any(x in t for x in sign))
    m=group
    a=int((ix&m).sum()); b=int((~ix&m).sum()); c=int((ix&~m).sum()); e=int((~ix&~m).sum())
    r,p=fe(a,b,c,e)
    ok = p<0.05
    P(f'CHECK {name} | predicts: {pred} | {a} of {a+c} faces with the sign are {label} against {m.mean():.1%} of all faces (x{r:.2f}, P {p:.2g}) | {"TRUE" if ok else "NOT TRUE"}')
    return ok
res={}
coast=d.site.isin(['Lothal','Dholavira','Allahdino','Bala-kot','Sutkagen-dor','Kanmer','Gola Dhoro (Bagasra)','Nageshwar','Kuntasi','Shikarpur','Surkotada'])
P('coastal/Kutch group sites in data:',d[coast].site.value_counts().to_dict())
# C1 sesame 838
res['838 tags/ports']=test('C1 sesame 838 sits on goods tags or pots (container labels)','838 on tag or pot > chance','838',d.cls.isin(['tag','pot']),'tag or pot')
res['838 lothal']=test('C2 sesame 838 at the port Lothal','838 at Lothal','838',d.site=='Lothal','at Lothal')
res['838 rods']=test('C2b 838 on ivory/bone rods','838 on rods (sesame oil rods? unexpected)','838',d.cls=='rod','rods')
# C3 fish 220 coast
res['220 coast']=test('C3 fish 220 at coast and Kutch sites','220 coastal','220',coast,'at coast/Kutch sites')
res['220 tags']=test('C4 fish 220 on goods tags','220 on tags','220',d.cls=='tag','tags')
res['055 tag']=test('C5 dozen 055 on goods tags','055 on tags','055',d.cls=='tag','tags')
res['055 lothal']=test('C5b dozen 055 at Lothal','055 Lothal','055',d.site=='Lothal','Lothal')
res['048 boxtag']=test('C6 seven-in-parens 048 on wooden-box sealings (TAG:B)','048 box-sealing','048',d.type=='TAG:B','TAG:B box sealings')
# C7 bin 590 granary
res['590 gran']=test('C7 bin 590 in the Harappa granary area','590 granary','590',d.gran,'granary area')
res['595 gran']=test('C7b bin variant 595 in granary area','595 granary','595',d.gran,'granary area')
# grain with cup
cisi=d.cisi.where(~d.cisi.isin(['-','']),d.id)
d['obj']=cisi
objsigs=d.groupby('obj').toks.apply(lambda L:set(x for t in L for x in t))
objhas700=objsigs.apply(lambda s:'700' in s)
def cup_test(name,pred,sign):
    hs=objsigs.apply(lambda s:sign in s); a=int((hs&objhas700).sum()); b=int((hs&~objhas700).sum()); c=int((~hs&objhas700).sum()); e=int((~hs&~objhas700).sum())
    r,p=fe(a,b,c,e); ok=p<0.05
    P(f'CHECK {name} | predicts: {pred} | {a} of {a+b} objects with {sign} also carry the cup 700 against {objhas700.mean():.1%} of objects (x{r:.2f}, P {p:.2g}) | {"TRUE" if ok else "NOT TRUE"}'); return ok
res['413 cup']=cup_test('C8 grain ear 413 beside the cup measure','413 with cup','413')
res['806 cup']=cup_test('C9 crop 806 beside the cup measure','806 with cup','806')
res['803 cup']=cup_test('C9b leaf-in-tree 803 beside cup (house sign, control)','control: no excess','803')
res['176 cup']=cup_test('C9c tax 176 beside cup','176 with cup (known)','176')
res['806 gran']=test('C10 crop 806 in granary area','806 granary','806',d.gran,'granary area')
res['806 harF']=test('C10b crop 806 in Harappa mound F','806 mound F','806',d.harF,'mound F')
res['413 E11']=test('C10c grain ear 413 in E trench 11 (ration batch)','413 E11','413',d.E11,'E trench 11')
# bangles 840
res['840 bngl']=test('C11 pair-of-leaves 840 on bangles','840 bangles (pair)','840',d.cls=='bngl','bangles')
res['790 bngl']=test('C12 lens 790 on bangles','790 bangles','790',d.cls=='bngl','bangles')
res['790+850+832 copper obj']=test('C13 eye signs (790,832,850) on copper objects: eye as kaṉ "copper"','eye signs on copper material (all object types)',['790','832','850'],d.mat=='copper','copper objects')
res['eye tools']=test('C13b eye signs (790,832,850) on tools (impl/bangle/rod)','eye on tools',['790','832','850'],d.cls.isin(['impl','bngl','rod']),'tools/bangles/rods')
res['391 impl']=test('C14 391 on copper implements','391 impl','391',d.cls=='impl','implements')
res['400 rod']=test('C15 comb 400 on ivory/bone rods','comb rods','400',d.cls=='rod','rods')
res['400 ivory']=test('C15b comb 400 on ivory material','comb ivory','400',d.mat=='ivory','ivory objects')
res['892 tag']=test('C16 bow 892 "sale" on goods tags','sale on tags','892',d.cls=='tag','tags')
res['440 pot']=test('C17 hook 440 "received/bought" on pots','440 pots','440',d.cls=='pot','pots')
res['480 pot']=test('C18 caret 480 (kuṉṟi bead/seed weight) on pots','480 pots','480',d.cls=='pot','pots')
res['390 chanhu']=test('C19 tree 390 at craft town Chanhu-daro','tree Chanhu','390',d.site=='Chanhu-daro','Chanhu-daro')
res['390 tag']=test('C19b tree 390 on tags','tree tags','390',d.cls=='tag','tags')
res['407 cu']=test('C20 tree 407 on copper tablets (timber/goods list)','407 copper tablets','407',d.cls=='tabC','copper tablets')
res['850 cu']=test('C21 lozenge 850 on copper objects','850 copper','850',d.mat=='copper','copper objects')
res['845 cu']=test('C22 845 on copper tablets','845 copper tablets','845',d.cls=='tabC','copper tablets')
res['900 steatite']=test('C23 crescent 900 on steatite seals','900 steatite','900',d.mat=='steatite','steatite')
for s in ['417','056','890','500']:
    res[s+' tag']=test(f'C24 {s} on goods tags','tags',s,d.cls=='tag','tags')
# bead towns: signs enriched at both Lothal and Chanhu-daro
rows=[]
for s in set(x for t in d.toks for x in t):
    if s in CNT or s in('000','ALT'): continue
    ix=has(s)
    if ix.sum()<10: continue
    out=[]
    for site in ['Lothal','Chanhu-daro']:
        m=d.site==site; a=int((ix&m).sum()); r,p=fe(a,int(m.sum())-a,int((ix&~m).sum()),int((~ix&~m).sum())); out+= [a,r,p]
    rows.append((s,int(ix.sum()),*out))
B=pd.DataFrame(rows,columns=['sign','faces','L_n','L_x','L_p','C_n','C_x','C_p'])
both=B[(B.L_p<0.05)&(B.C_p<0.05)&(B.L_n>=3)&(B.C_n>=3)].sort_values('L_p')
P('BEAD-TOWN signs enriched at both Lothal and Chanhu-daro (P<0.05 each, n>=3 each):'); P(both.round(3).to_string(index=False))
# tag subtype x sign
tg=d[d.cls=='tag']
P('TAG subtype counts:',tg.type.value_counts().to_dict())
sub=tg.groupby('type').apply(lambda g:collections.Counter(x for t in g.toks for x in t if x not in CNT and x!='000'))
for k,v in sub.items(): P('  ',k,v.most_common(8))
tick=sum(res.values()); P(f'\nTOTAL checks run {len(res)}; true {tick}')
open(f'{OUT}/checks.txt','w').write('\n'.join(log))

# C25 eye signs on copper objects other than copper tablets (tools, rods, misc)
nt=d.cls!='tabC'
ix=d.toks.apply(lambda t:any(x in t for x in ['790','832','850']))&nt; m=(d.mat=='copper')&nt
a=int((ix&m).sum()); r,p=fe(a,int((~ix&m&nt).sum()),int((ix&~m).sum()),int((~ix&~m&nt).sum()))
print(f'CHECK C25 eye signs on copper objects that are not tablets | {a} of {int(ix.sum())} non-tablet faces with the sign are copper against {(m.sum()/nt.sum()):.1%} (x{r:.2f}, P {p:.2g})')
