"""Foreign objects that carry the box/tree-family signs, and a test of the "count + tree" formula.
Predictions written first:
 P1 (Umma 3884.1 reads ... 002-004-390): "two, four, cotton" is a home goods formula; home texts where short-stroke 4 stands right before a tree-family sign (390/392/405/406/407) are far above the share expected from how often 004 and tree signs occur.
 P2 the foreign objects (Umma, Salut, Ra's al-Junayz) that put 004 before a tree sign are each a count-before-goods use, not a name use (no jar after).
 P3 the box-tree pair 590-390 abroad (Kish, Gonur, unprovenanced 3335) keeps the name use (jar after) as at home.
Reading order = stored order reversed (goods_common). Output tables work_data/abroad2/."""
import sys
sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from cotton_common import *
OUTD='/home/antigravity/Cuuper22/ivc/work_data/abroad2'
d=faces()
TREE={'390','392','405','406','407'}
fsites={'Altyn Depe','Failaka','Girsu','Gonur Depe','Hajar','Janabiyah','Kalba','Karzakan','Kish','Luristan','Miri Qalat','Murda Sang','Nippur',"Qala'at al-Bahrain","Ra's al-Junayz",'Saar','Salut','Shortughai','Sibri','Susa','Tell Umma','Tello','Tepe Yahya','Ur','Unknown','Ornach area','Nindowari-damb'}
fr=d[d.site.isin(fsites)]
rows=[]
for _,r in fr.iterrows():
    t=r.toks
    if (TREE|{'590'})&set(t):
        rows.append(dict(id=r.id,site=r.site,region=r.region,type=r.type,mat=r.material,animal=r.symbol,period=r.period,findspot=f"{r['area-section']} {r['block-house']} {r['room-grid']} {r.depth}".strip(),text=' '.join(t)))
pd.DataFrame(rows).to_csv(f'{OUTD}/foreign_tree_box_objects.csv',index=False)
print(pd.DataFrame(rows).to_string())
# P1 home: count 004 immediately before a tree-family sign
home=d[~d.site.isin(fsites)]
def pairs(df):
    n=0; c=collections.Counter(); tot=0
    for t in df.toks:
        for i in range(len(t)-1):
            c[(t[i],t[i+1])]+=1
        tot+=len(t)
    return c,tot
c,tot=pairs(home)
sign=collections.Counter(x for t in home.toks for x in t)
tree_n=sum(sign[s] for s in TREE)
print('home signs',tot,'tree-family places',tree_n)
for k in ['001','002','003','004','005','006','007','031','032','033','034']:
    before=c[(k,'390')]+c[(k,'392')]+c[(k,'405')]+c[(k,'406')]+c[(k,'407')]
    print(k,'before tree',before,'of',sign[k],'places; expected by chance',round(sign[k]*tree_n/tot,2))
# 4 or 004 before a tree sign, per sign
for s in sorted(TREE):
    print(s,'places',sign[s],'with 004 right before',c[('004',s)],'with 002-004 before',sum(1 for t in home.toks for i in range(2,len(t)) if t[i]==s and t[i-1]=='004' and t[i-2]=='002'))
# all home objects having 002-004 adjacent and what follows
fol=collections.Counter(); nn=0
for t in home.toks:
    for i in range(len(t)-1):
        if t[i]=='002' and t[i+1]=='004':
            nn+=1; fol[t[i+2] if i+2<len(t) else 'END']+=1
print('home 002-004 adjacent:',nn,fol.most_common(8))
fo=collections.Counter(); nn=0
for t in fr.toks:
    for i in range(len(t)-1):
        if t[i]=='002' and t[i+1]=='004':
            nn+=1; fo[t[i+2] if i+2<len(t) else 'END']+=1
print('foreign 002-004 adjacent:',nn,fo.most_common(8))
# jar after 590-390 abroad vs home
for site_set,name in [(set(fsites),'abroad'),(None,'home')]:
    sub=fr if name=='abroad' else home
    k=j=0
    for t in sub.toks:
        for i in range(len(t)-1):
            if t[i]=='590' and t[i+1]=='390':
                k+=1; j+= (i+2<len(t) and t[i+2]=='740')
    print(name,'590-390 faces',k,'jar after',j)
