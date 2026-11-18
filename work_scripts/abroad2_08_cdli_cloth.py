"""Search CDLI for cloth words tied to Meluhha / Dilmun / Magan / the East. Prediction first: if Indus cotton cloth was a recognised import, some Ur III or Akkadian text names a cloth with an eastern adjective (tug2 me-luh-ha, tug2 dilmun, tug2 ma-gan). Result stored in work_data/abroad2/cdli_cloth_east.csv"""
import json, time, urllib.parse, urllib.request, csv, re
OUT='/home/antigravity/Cuuper22/ivc/work_data/abroad2'
def get(u):
    for k in range(4):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ivc-research'}),timeout=60).read()
        except Exception: time.sleep(2+3*k)
Q=['tug2 me-luh-ha','tug2 dilmun{ki}','gada dilmun','tug2 dilmun','tug2 ma-gan{ki}','gada ma-gan','tug2 elam','siki me-luh-ha','gada me-luh-ha','tug2-me-luh-ha','tug2 kur-ra','tug2 ma-da']
rows=[]
for q in Q:
    p=1
    while p<=4:
        raw=get(f'https://cdli.earth/search?atf_transliteration={urllib.parse.quote(q)}&format=json&page={p}')
        if not raw: break
        try: arr=json.loads(raw)
        except Exception: break
        if not arr: break
        for a in arr:
            atf=(a.get('inscription') or {}).get('atf','') or ''
            for i,l in enumerate(atf.split('\n')):
                if re.search(r'dilmun|ma-gan|me-luh|elam',l,re.I) and re.search(r'tug2|gada|siki|usz-bar|uš-bar',l+' '+(atf.split('\n')[i-1] if i else ''),re.I):
                    rows.append(dict(q=q,id=a['id'],des=a['designation'],period=re.sub(r".*'name': '([^']*)'.*",r'\1',str(a.get('period'))),line=l.strip()[:140]))
        print(q,p,len(arr),flush=True)
        if len(arr)<25: break
        p+=1
seen=set(); out=[]
for r in rows:
    k=(r['id'],r['line'])
    if k in seen: continue
    seen.add(k); out.append(r)
with open(f'{OUT}/cdli_cloth_east.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['q','id','des','period','line']); w.writeheader(); w.writerows(out)
print(len(out))
for r in out[:60]: print(r['id'],r['des'][:25],r['period'][:14],'|',r['line'])
