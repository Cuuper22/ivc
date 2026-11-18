"""Pick candidate seals (all signs have a working sound) per animal and print sound + English glosses sign by sign (table: work_data/sound_v3/values_v3.csv, then sound_values.ALL_SOUNDS)."""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from sound_values import ALL_SOUNDS
V=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/sound_v3/values_v3.csv',dtype=str,keep_default_na=False).set_index('sign')
def snd(s):
    if s in V.index and V.loc[s,'sound']: return V.loc[s,'sound'],V.loc[s,'english']
    if s in ALL_SOUNDS: return ALL_SOUNDS[s]
    return None
b=pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/animal/animal_base.csv',dtype=str,keep_default_na=False)
def full(t): 
    x=t.split('-'); return all(snd(s) for s in x) and len(x)>=2
b['ok']=b.reading_order_text.map(full)
if __name__=='__main__':
    for a in sys.argv[1:]:
        s=b[(b.animal==a)&b.ok]; print('==',a,len(s))
        for _,r in s.head(14).iterrows():
            print(r.cisi,r.site,r.symbol,r.region[:8],r.reading_order_text,'|',' '.join(snd(x)[0] for x in r.reading_order_text.split('-')),'|',' · '.join(snd(x)[1].split(',')[0] for x in r.reading_order_text.split('-')))
