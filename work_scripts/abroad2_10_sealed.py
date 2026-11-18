"""Second way in, item 1. Prediction first: among Girsu/Lagash/Umma tablets mentioning Meluhha or Guabba, a minority (<30%) are sealed, and nearly all sealed ones carry a cuneiform legend (Ur III administrative seals); an uninscribed/pictorial seal on a wool or cloth tablet would be rare (0-2 cases).
Pulls CDLI search JSON, keeps seals/impressions fields."""
import json, time, urllib.parse, urllib.request, re, csv
OUT='/home/antigravity/Cuuper22/ivc/work_data/abroad2'
def get(u):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ivc-research'}),timeout=90).read()
        except Exception: time.sleep(2+3*k)
T=['me-luh-ha','me-luh-ha{ki}','me-lu-ha','me-luh-hi','gu2-ab-ba{ki}','gu2-ab-ba','e2-duru5 me-luh-ha','e2-duru5-me-luh-ha{ki}','gu-ab-ba{ki}']
seen={}
for t in T:
    p=1
    while p<=40:
        raw=get(f'https://cdli.earth/search?atf_transliteration={urllib.parse.quote(t)}&format=json&page={p}')
        if not raw: break
        try: arr=json.loads(raw)
        except Exception: break
        if not arr: break
        for a in arr: seen.setdefault(a['id'],a)
        print(t,p,len(arr),len(seen),flush=True)
        if len(arr)<25: break
        p+=1
json.dump(list(seen.values()),open(f'{OUT}/cdli_meluhha_guabba_full.json','w'),default=str)
print('total',len(seen))
