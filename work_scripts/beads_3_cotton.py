"""beads_3: is sign 390 (tree with branches at the top) COTTON / the spinner's-weaver's sign?
Found by looking at the findspot-type column: five terracotta MISC objects from Karanpura carry only 390, and the excavators
(harappa.com Karanpura pages, fetched today) say the inscribed objects at Karanpura are spindle whorls used by weavers.
PREDICTIONS written before the numbers below were computed:
 C1 390 is the whole text of >=5 terracotta MISC objects; chance-based Fisher P < 1e-6 against 390's share of all faces.
 C2 390 is the whole text of >=2 of the 42 rods (ivory spindle shafts / needles?) ; P < 0.01.
 C3 Among all single-sign faces, 390's single-sign faces are on non-seal object types (not SEAL*) >=80% of the time against <=40% for other single signs.
 C4 Counts before 390 are 3 or more in >=85% of its counted uses, against <=50% for the other counted nouns (bolls/hanks counted in lots).
 C5 390 is enriched on the foreign faces (Ur, Susa, Kish, Gulf ...) at >=2x (cloth went to Mesopotamia), one-sided Fisher.
 C6 the box+390 pair (590-390, 'bale of cotton') is >=3x at the Harappa granary store area (already seen 4.9x; recomputed).
 C7 Kalibangan terracotta MISC (K-458.. series): if those are the same kind of object (whorls) they carry a sign from the same short list; list them.
"""
from goods_common import *
d=load(); d['n']=d.toks.apply(len)
has390=d.toks.apply(lambda t:'390' in t)
allf=len(d)
# C1
misc=d[(d.type=='MISC')&(d.mat=='terracotta')]
print('C1 terracotta MISC objects:',len(misc),' of them 390 alone:',((misc.toks.apply(lambda t:t==['390']))).sum(), misc[misc.toks.apply(lambda t:t==['390'])].site.value_counts().to_dict())
a=int(misc.toks.apply(lambda t:t==['390']).sum()); 
r,p=fe(a,len(misc)-a,int(has390.sum())-a,allf-len(misc)-(int(has390.sum())-a)); print('   Fisher (390 on terracotta MISC vs elsewhere) ratio %.1f P %.2g'%(r,p))
# C2
rod=d[d.cls=='rod']; a=int(rod.toks.apply(lambda t:'390' in t).sum()); print('C2 rods with 390:',a,'of',len(rod),[ ( r.id,'-'.join(r.toks)) for _,r in rod[rod.toks.apply(lambda t:'390' in t)].iterrows()])
r,p=fe(a,len(rod)-a,int(has390.sum())-a,allf-len(rod)-(int(has390.sum())-a)); print('   ratio %.1f P %.2g'%(r,p))
# C3
single=d[d.n==1]; s390=single[single.toks.apply(lambda t:t[0]=='390')]
print('C3 single-sign faces',len(single),' 390 single:',len(s390),' non-seal share 390: %.2f  others: %.2f'%((~s390.cls.eq('seal')).mean(), (~single[~single.toks.apply(lambda t:t[0]=='390')].cls.eq('seal')).mean()))
print('   390 single by type',s390.type.value_counts().to_dict())
# C4
cs=collections.Counter(); tot=collections.Counter()
tall_or_short=lambda c: c[1]
for t in d.toks:
    for i,u in enumerate(t):
        if i>0 and t[i-1] in CNT and u not in CNT and u!='ALT':
            tot[u]+=1
            c=CNT[t[i-1]]
            if (c[0] in 'ST' and c[1]>=3) or (c[0]=='F' and c[1]>=3): cs[u]+=1
n390=tot['390']; print('C4 390 counted uses',n390,' with count>=3: %d (%.0f%%)'%(cs['390'],100*cs['390']/n390))
oth=[(cs[u]/tot[u]) for u in tot if tot[u]>=15 and u!='390']; print('   other nouns (>=15 counted uses): n=%d median share >=3: %.2f ; share of them above 390: %d'%(len(oth),np.median(oth),sum(1 for x in oth if x>=cs['390']/n390)))
# C5
FOREIGN=['Ur','Susa','Kish',"Qala'at al-Bahrain",'Failaka',"Ra's al-Junayz",'Hajar','Luristan','Nippur','Tell Umma','Tello','Tepe Yahya','Gonur Depe','Girsu','Saar','Janabiyah','Kalba','Altyn Depe','Shortughai','Salut','Karzakan','Sibri','Murda Sang']
fo=d.site.isin(FOREIGN); a=int((has390&fo).sum())
r,p=fe(a,int(fo.sum())-a,int((has390&~fo).sum()),int((~fo).sum())-int((has390&~fo).sum())); print('C5 foreign faces',int(fo.sum()),' with 390:',a,' ratio %.2f P %.3g'%(r,p))
# C6
pair=d.toks.apply(lambda t:any(x=='590' and y=='390' for x,y in zip(t,t[1:])))
g=d.gran; a=int((pair&g).sum()); r,p=fe(a,int(g.sum())-a,int((pair&~g).sum()),int((~g).sum())-int((pair&~g).sum())); print('C6 590-390 pair in granary',a,'of',int(g.sum()),' ratio %.2f P %.2g'%(r,p))
# C7
k=d[(d.site=='Kalibangan')&(d.type=='MISC')]; print('C7 Kalibangan MISC terracotta texts:',collections.Counter('-'.join(t) for t in k.toks).most_common())
