"""Item 3. Read every foreign object whole with current values (work_data/values_master.csv) and classify the statement.
Prediction first: (a) foreign seals skew to lot labels (a count right before a thing, template N-THING) compared with home seals of the same kind: foreign share of texts with an N-THING part at least 1.3 times home; (b) foreign round seals (cylinders) skew further, because the abroad job found 23% of their signs are counts against 16% at home; (c) the share of texts that END in the jar (possessive 'of the house') is lower abroad.
Statement kinds: LOT (has a counted thing), NAME-POSS (ends in the jar: 'of the house of X'), NAME (name parts only, no jar), TITLE/OFFICE (ends in a class sign: man, spear, carrier, comb), MIXED (name + lot).
Uses the gloss2 parser's template column; reads English from values_master."""
import sys, csv, collections
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from cotton_common import *
OUTD='/home/claude/ivc/work_data/abroad2'
g=pd.read_csv('/home/claude/ivc/work_data/gloss2_all.csv',dtype=str,keep_default_na=False)
vm=pd.read_csv('/home/claude/ivc/work_data/values_master.csv',dtype=str,keep_default_na=False).set_index('sign')
d=faces(); 
fs={'Altyn Depe','Failaka','Girsu','Gonur Depe','Hajar','Janabiyah','Kalba','Karzakan','Kish','Luristan','Miri Qalat','Murda Sang','Nippur',"Qala'at al-Bahrain","Ra's al-Junayz",'Saar','Salut','Shortughai','Sibri','Susa','Tell Umma','Tello','Tepe Yahya','Ur','Unknown','Ornach area','Nindowari-damb'}
d=d.merge(g[['id','template','ending_kind','gloss']],on='id',how='left')
d['foreign']=d.site.isin(fs)
CLASS={'090','091','151','154','156','226','400','407','520','527','617','621'}
def kind(t,tmpl):
    tm=tmpl if isinstance(tmpl,str) else ''
    lot='N-THING' in tm
    poss=t and t[-1]=='740'
    name='NAME' in tm
    last=[x for x in t if x!='000']
    off= bool(last) and last[-1] in {'090','091','151','154','156','520','527','617','621','400'}
    if lot and (name or poss): return 'MIXED name+lot'
    if lot: return 'LOT'
    if poss: return 'NAME + jar (of the house)'
    if off: return 'OFFICE/man'
    return 'NAME (no jar)'
d['kind']=[kind(t,tm) for t,tm in zip(d.toks,d.template)]
def eng(t):
    out=[]
    for s in t:
        if s in vm.index and vm.loc[s,'short']: out.append(vm.loc[s,'short'])
        elif s=='000': out.append('[lost]')
        else: out.append('['+s+']')
    return ' '.join(out)
f=d[d.foreign].copy()
f['reading']=[eng(t) for t in f.toks]
f['text']=[' '.join(t) for t in f.toks]
f[['id','site','region','type','symbol','text','kind','reading']].to_csv(f'{OUTD}/foreign_read_whole.csv',index=False)
print(f[['id','site','type','text','kind','reading']].to_string())
# compare shares by object kind
def share(df,label):
    n=len(df); c=df.kind.value_counts()
    print(label,n,{k:f'{v} ({v/n:.0%})' for k,v in c.items()})
    return n,c
home=d[~d.foreign].drop_duplicates('text')
fseal_sq=f[f.type.str.startswith('SEAL:S')|(f.type=='SEAL')|f.type.str.startswith('SEAL:R')]
fseal_cy=f[f.type.str.startswith('SEAL:C')]
fnon=f[~f.type.str.startswith('SEAL')]
hseal=home[home.type.str.startswith('SEAL')]
hpot=home[home.type.str.startswith('POT')]; htag=home[home.cls.isin(['tag','tabB','tabI'])]
print()
share(fseal_sq,'foreign square seals'); share(fseal_cy,'foreign round seals/cylinders'); share(fnon,'foreign non-seals')
share(hseal,'home seals (distinct texts)'); share(hpot,'home pots'); share(htag,'home tags+tablets')
from scipy.stats import fisher_exact
def test(a,b,lab):
    la=(a.kind.isin(['LOT','MIXED name+lot'])).sum(); lb=(b.kind.isin(['LOT','MIXED name+lot'])).sum()
    r,p=fe(la,len(a)-la,lb,len(b)-lb)
    print(f'{lab}: lot-bearing {la}/{len(a)} ({la/len(a):.0%}) vs {lb}/{len(b)} ({lb/len(b):.0%}); x{r:.2f} P={p:.4f}')
test(f[f.type.str.startswith('SEAL')],hseal,'foreign seals vs home seals')
test(fseal_sq,hseal,'foreign square seals vs home seals')
test(fseal_cy,hseal,'foreign round seals vs home seals')
def jar(a,b,lab):
    ja=(a.kind=='NAME + jar (of the house)').sum()+(a.kind=='MIXED name+lot').sum()*0
    la=sum(1 for t in a.toks if t and t[-1]=='740'); lb=sum(1 for t in b.toks if t and t[-1]=='740')
    r,p=fe(la,len(a)-la,lb,len(b)-lb); print(f'{lab}: ends in jar {la}/{len(a)} vs {lb}/{len(b)}; ratio {r:.2f}; P(more)={p:.4f}; P(fewer)={fisher_exact([[la,len(a)-la],[lb,len(b)-lb]],alternative="less")[1]:.4f}')
jar(f[f.type.str.startswith('SEAL')],hseal,'foreign seals vs home seals')
jar(fseal_sq,hseal,'foreign square seals vs home seals')
jar(fseal_cy,hseal,'foreign round seals vs home seals')
# trade words: signs that are counted-goods/trade vocabulary (dozen 055, string 048, tree family, box 590, sale 892, given 890, sail 500, ship/measure 705)
TRADE={'055','048','390','392','405','406','407','590','892','890','500','705','838','413','806'}
def tw(a): return sum(1 for t in a.toks if TRADE&set(t))
for nm_,a,b in [('foreign seals vs home seals',f[f.type.str.startswith('SEAL')],hseal),('foreign square seals vs home seals',fseal_sq,hseal),('foreign round seals vs home seals',fseal_cy,hseal)]:
    x,y=tw(a),tw(b); r,p=fe(x,len(a)-x,y,len(b)-y); print(f'trade words {nm_}: {x}/{len(a)} ({x/len(a):.0%}) vs {y}/{len(b)} ({y/len(b):.0%}); x{r:.2f} P={p:.4f}')
