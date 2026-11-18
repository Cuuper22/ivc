"""Item 3. CDLI Umma (and other) texts with goods from Dilmun / Magan / Meluhha and jars (dug, sag-gan, etc.), boats (ma2).
Prediction first: Umma texts that tie Dilmun/Magan/Meluhha to a jar word are few (under 10); a cloth-or-fibre word with them is rarer still;
the tie is mostly boats (ma2) and copper, not jars."""
import json, time, re, sys, urllib.parse, urllib.request, os, csv
OUT='/home/antigravity/Cuuper22/ivc/work_data/abroad3'; os.makedirs(OUT,exist_ok=True)
TERMS=['dilmun','dilmun{ki}','dilmun-na','ma2-gan','ma2-gan{ki}','ma-gan','ma-gan{ki}','magan','ma2-gan-na','me-luh-ha','me-luh-ha{ki}','me-lu-uh-ha','me-lu-ha']
def get(url):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ivc-research'}),timeout=90).read()
        except Exception: time.sleep(2+k*3)
    return None
seen={}
for t in TERMS:
    p=1
    while p<=60:
        raw=get(f'https://cdli.earth/search?atf_transliteration={urllib.parse.quote(t)}&format=json&page={p}')
        if not raw: print('fail',t,p); break
        try: arr=json.loads(raw)
        except Exception: print('bad json',t,p); break
        if not arr: break
        for a in arr: seen.setdefault(a['id'],a)
        print(t,p,len(arr),len(seen),flush=True)
        if len(arr)<25: break
        p+=1
rows=[]
with open(f'{OUT}/cdli_east_atf.jsonl','w') as f:
    for a in seen.values():
        f.write(json.dumps({'id':a['id'],'designation':a['designation'],'period':(a.get('period') or {}).get('period'),'prov':(a.get('provenience') or {}).get('provenience'),'atf':(a.get('inscription') or {}).get('atf','')})+'\n')
print('artifacts',len(seen))
