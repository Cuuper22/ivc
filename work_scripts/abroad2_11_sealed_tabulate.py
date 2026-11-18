"""Item 1 table. Prediction (from abroad2_10): <30% of Meluhha/Guabba tablets sealed; sealed ones mostly cuneiform-legend; 0-2 uninscribed/pictorial seals on wool/cloth tablets."""
import json, re, csv, collections
OUT='/home/antigravity/Cuuper22/ivc/work_data/abroad2'
A=json.load(open(f'{OUT}/cdli_meluhha_guabba_full.json'))
def nm(x,k): 
    m=re.search(r"'%s': '([^']*)'"%k,str(x)); return m.group(1) if m else ''
rows=[]
for a in A:
    atf=(a.get('inscription') or {}).get('atf','') or ''
    prov=nm(a.get('provenience'),'provenience')
    per=nm(a.get('period'),'name'); dt=a.get('dates_referenced') or ''
    mel=bool(re.search(r'me-l[uú]h?-?(?:uh-)?h[ai]|me-luh|meluhha',atf,re.I))
    gua=bool(re.search(r'gu2?-ab-ba\{ki\}|gu2?-ab-ba',atf,re.I))
    if not (mel or (gua and ('Girsu' in prov or 'Umma' in prov))): continue
    if not re.search(r'Girsu|Lagash|Umma|Zabalam|Nigin',prov): continue
    seals=[s for s in (a.get('seals') or []) if (s.get('seal') or {}).get('seal_no')!='S999999']
    imps=a.get('impressions') or []
    sealtxt=[l for l in atf.split('\n') if re.match(r'\s*(@seal|#tr\.en: seal|\$ seal)',l,re.I) or 'seal' in l.lower()[:40] and l.startswith('$')]
    kis='kiszib3' in atf or 'kišib' in atf
    rows.append(dict(id='P%06d'%a['id'],des=a['designation'],prov=prov,period=per,date=dt,mel=mel,gua=gua,
        seals=len(seals),imps=len(imps),seal_lines=' | '.join(sealtxt)[:120],kiszib=kis,
        type=nm(a.get('artifact_type'),'artifact_type'),
        genre=';'.join(re.findall(r"'genre': '([^']*)'",str(a.get('genres')))),
        wool=bool(re.search(r'siki|tug2|gada|usz-bar|uš-bar',atf)),
        first=' / '.join(l.strip() for l in atf.split('\n')[4:8])[:140]))
with open(f'{OUT}/sealed_candidates_all.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('artifacts in Girsu/Lagash/Umma with Meluhha or Guabba:',len(rows))
print(collections.Counter((r['prov'][:8],r['period'][:10]) for r in rows).most_common(10))
real=[r for r in rows if r['seals']>0 or r['imps']>0]
print('with a non-dummy seal or impression record in CDLI:',len(real))
sl=[r for r in rows if r['seal_lines']]
print('with a seal line in ATF:',len(sl),'; with kiszib3 (a sealed-document formula, "sealed by"):',sum(r['kiszib'] for r in rows))
print('mention Meluhha:',sum(r['mel'] for r in rows),'Guabba only:',sum(1 for r in rows if r['gua'] and not r['mel']))
print('textile/wool words present:',sum(r['wool'] for r in rows))
for r in rows:
    if (r['seals'] or r['imps'] or r['seal_lines']) and r['mel']: print(r['id'],r['des'],r['period'][:8],r['seals'],r['imps'],r['seal_lines'],'|',r['first'][:90])
