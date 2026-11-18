"""Commodity table from resolved counts: one row per counted thing (n>=12 owned 'n X' counts, or X n counts)."""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
import math
d=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
sh=shapes(); allr=pd.read_csv(DATA,dtype=str,keep_default_na=False)
rows=load(); occ=collections.Counter(s for r,t,b in rows for s in t)
d['value']=d.value.astype(int); d['tt']=d.type.str.split(':').str[0]
fol=lambda x:'END' if x=='END' else 'carrier' if x in CARR else 'jar' if x in('740','741') else 'comb' if x=='400' else 'count' if x in CNT else 'other'
d['nc']=d.nxt.map(fol)
out=[]
for frame in('B','A'):
    X=d[d.frame==frame].drop_duplicates(['id','sign','cs'])
    for s,g in X.groupby('sign'):
        if len(g)<12: continue
        v=g['count'].value_counts(); top=v.index[0]; ent=-sum(p*math.log2(p) for p in v/len(g))
        ser=g.series.value_counts(normalize=True)
        pe=lambda m:round(g.mat.eq(m).mean(),2) if 'mat' in g else 0
        g=g.assign(mat=g.material)
        sj=lambda k:round(g.site.eq(k).mean(),2)
        hf=((g.site=='Harappa')&g['area-section'].str.startswith('F')).mean()
        an=g.symbol.str.split(':').str[0].isin(['-','None']).mean()
        a=pd.to_numeric(g.area,errors='coerce'); a=a[a>0]
        out.append(dict(sign=s,frame=frame,shape=sh.get(s,'')[:45],n=len(g),occ=occ[s],top=top,top_share=round(v.iloc[0]/len(g),2),
            top3='; '.join(f'{k}:{x}' for k,x in v.head(3).items()),entropy=round(ent,2),nvals=len(v),
            S=round(ser.get('S',0),2),F=round(ser.get('F',0),2),T=round(ser.get('T',0),2),
            seal=round((g.tt=='SEAL').mean(),2),tab=round((g.tt=='TAB').mean(),2),tabC=round((g.type=='TAB:C').mean(),2),pot=round((g.tt=='POT').mean(),2),tag=round((g.tt=='TAG').mean(),2),
            har=sj('Harappa'),moh=sj('Mohenjo-daro'),loth=sj('Lothal'),harF=round(hf,2),cu=pe('Copper'),fai=pe('Faience'),noanimal=round(an,2),area=round(a.median()) if len(a) else None,
            END=round((g.nc=='END').mean(),2),carrier=round((g.nc=='carrier').mean(),2),jar=round((g.nc=='jar').mean(),2),comb=round((g.nc=='comb').mean(),2),oth=round((g.nc=='other').mean(),2)))
C=pd.DataFrame(out).sort_values(['frame','n'],ascending=[True,False]); C.to_csv(f'{ROOT}/work_data/counted/commodity_table.csv',index=False)
pd.set_option('display.width',320); pd.set_option('display.max_columns',50)
print(C.drop(columns=['shape','top3']).to_string(index=False))
