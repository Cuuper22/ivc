"""Item 4. For each non-dummy CDLI composite-seal record tied to a Girsu/Lagash/Umma tablet naming Guabba or Meluhha:
fetch the CDLI seal page, record legend transliteration (if any), and whether a photo / line-art exists.
Prediction first: all seal records whose legend is missing are still ordinary Ur III cuneiform cylinders (seen as photo or line-art);
none is an Indus-type or other foreign pictorial seal."""
import json, re, urllib.request, csv, time, os
OUT='/home/claude/ivc/work_data/abroad3'; os.makedirs(OUT+'/seals',exist_ok=True)
A=json.load(open('/home/claude/ivc/work_data/abroad2/cdli_meluhha_guabba_full.json'))
UA={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/124'}
def get(u,binary=False):
    for k in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
            return r if binary else r.decode('utf8','replace')
        except Exception as e: err=str(e); time.sleep(2)
    return None
seals={}
for x in A:
    for y in (x.get('seals') or []):
        if y['seal_no']=='S999999': continue
        seals.setdefault((y['seal_no'],y['seal']['id']),[]).append((x['id'],x['designation']))
print(len(seals),'distinct non-dummy seal records on',sum(len(v) for v in seals.values()),'tablet links')
rows=[]
for (no,sid),tabs in sorted(seals.items()):
    h=get(f'https://cdli.earth/artifacts/{sid}')
    if h is None: rows.append(dict(seal=no,sid=sid,tablets=';'.join(f'P{a} {b}' for a,b in tabs),page='FAIL')); continue
    txt=re.sub(r'<[^>]+>',' ',h); txt=re.sub(r'\s+',' ',txt)
    photo=bool(get(f'https://cdli.earth/dl/photo/P{sid:06d}.jpg',True)) if False else None
    imgs=sorted(set(re.findall(r'https://cdli\.earth/dl/[a-z_]+/P\d+[^"\' ]*',h)))
    ok=[]
    for u in imgs:
        b=get(u,True)
        if b and b[:3]==b'\xff\xd8\xff' or (b and b[:4]==b'\x89PNG'):
            fn=f"{OUT}/seals/{no}_{u.rsplit('/',2)[-2]}.{'png' if b[:4]==b'\x89PNG' else 'jpg'}"; open(fn,'wb').write(b); ok.append(fn)
    atf=re.search(r'(1\.[^<]{0,300})',h)
    m=re.search(r'Transliteration(.{0,400})',txt)
    rows.append(dict(seal=no,sid=sid,tablets=';'.join(f'P{a} {b}' for a,b in tabs),page='ok',img_links=len(imgs),img_saved=len(ok),files=';'.join(ok),
        title=re.search(r'<title>\s*([^<]*)',h).group(1).strip()[:80],has_translit=bool(m),translit=(m.group(1)[:200] if m else '')))
    print(rows[-1]['seal'],rows[-1]['title'],'imgs',len(imgs),'saved',len(ok),flush=True)
with open(OUT+'/seal_records_24.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=sorted({k for r in rows for k in r})); w.writeheader(); w.writerows(rows)
