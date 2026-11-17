"""Pull every CDLI text whose transliteration has me-luh-ha (Meluhha) in several spellings, keep the whole ATF,
and list the lines that mention cloth, wool, thread, weaving, wood, copper etc. next to a Meluhha line.
Prediction written first: if Meluhha cloth/cotton is a real trade item, some Ur III/Sargonic text has a cloth word within a few lines of Meluhha.
Output: work_data/abroad2/cdli_meluhha_atf.jsonl, cdli_meluhha_textile_lines.csv, log."""
import json, time, re, sys, urllib.parse, urllib.request, os, csv
OUT='/home/claude/ivc/work_data/abroad2'; os.makedirs(OUT,exist_ok=True)
TERMS=['me-luh-ha','me-luh-ha{ki}','me-lu-uh-ha','me-lu-ha','me-luh-ha-ke4','me-luh-hi','me-lu-ha{ki}','meluhha']
def get(url):
    for k in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ivc-research'}),timeout=60).read()
        except Exception as e:
            time.sleep(2+k*3)
    return None
seen={}
for t in TERMS:
    p=1
    while True:
        u=f'https://cdli.earth/search?atf_transliteration={urllib.parse.quote(t)}&format=json&page={p}'
        raw=get(u)
        if not raw: print('fail',t,p); break
        try: arr=json.loads(raw)
        except Exception: print('bad json',t,p); break
        if not arr: break
        new=0
        for a in arr:
            if a['id'] not in seen: seen[a['id']]=a; new+=1
        print(t,p,len(arr),'new',new,flush=True)
        if len(arr)<25 or p>40: break
        p+=1
rows=[]
with open(f'{OUT}/cdli_meluhha_atf.jsonl','w') as f:
    for a in seen.values():
        f.write(json.dumps({'id':a['id'],'designation':a['designation'],'period':a.get('period'),'provenience':a.get('provenience'),'atf':(a.get('inscription') or {}).get('atf','')},default=str)+'\n')
print('artifacts',len(seen))
