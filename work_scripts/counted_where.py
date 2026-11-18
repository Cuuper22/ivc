"""Where each counted thing lives. One row per counted thing (sign + frame), shares over objects where it is counted.
Output work_data/counted/where.csv"""
import sys; sys.path.insert(0,'/home/antigravity/Cuuper22/ivc/work_scripts')
from counted_common import *
d=pd.read_csv(f'{ROOT}/work_data/counted/instances_resolved.csv',dtype=str,keep_default_na=False)
allr=pd.read_csv(DATA,dtype=str,keep_default_na=False)
def flags(df):
    df=df.copy()
    df['seal']=df.type.str.startswith('SEAL'); df['tabC']=df.type=='TAB:C'; df['tabB']=df.type=='TAB:B'; df['tabI']=df.type=='TAB:I'
    df['pot']=df.type.str.startswith('POT'); df['tag']=df.type.str.startswith('TAG'); df['tool']=df.type.isin(['IMPL','ROD'])
    df['harF']=(df.site=='Harappa')&df['area-section'].str.startswith('F'); df['gran']=(df.site=='Harappa')&(df['area-section']=='FGranery')
    df['har']=df.site=='Harappa'; df['moh']=df.site=='Mohenjo-daro'; df['lothal']=df.site=='Lothal'
    df['cu']=df.material=='Copper'; df['fai']=df.material=='Faience'; df['ste']=df.material=='Steatite'; df['clay']=df.material.isin(['Clay','Terracotta'])
    df['animal']=df.symbol.str.split(':').str[0]; df['noanimal']=df.animal.isin(['-','None'])
    return df
allr=flags(allr); d=flags(d)
cols=['seal','tabC','tabB','tabI','pot','tag','tool','harF','gran','har','moh','lothal','cu','fai','ste','clay','noanimal']
base=allr[cols].mean().round(3)
print('BASELINE all objects',base.to_dict())
out=[]
for frame in('B','A'):
    X=d[d.frame==frame].drop_duplicates(['id','sign'])
    for s,g in X.groupby('sign'):
        if len(g)<10: continue
        r=dict(sign=s,frame=frame,n=len(g)); r.update({c:round(g[c].mean(),2) for c in cols})
        a=pd.to_numeric(g.area,errors='coerce'); a=a[a>0]; r['med_area']=round(a.median()) if len(a) else None
        out.append(r)
W=pd.DataFrame(out).sort_values(['frame','n'],ascending=[True,False]); W.to_csv(f'{ROOT}/work_data/counted/where.csv',index=False)
pd.set_option('display.width',300)
print(W.to_string(index=False))
