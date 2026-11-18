"""Item 3 scan. From cdli_east_atf.jsonl (texts with Dilmun/Magan/Meluhha): Umma texts, and any text with a jar word on a line with, or within 2 lines of, an eastern name.
Jar words: dug, dug-sag-gan, sag-gan, sag-gan-na? (checked as substrings dug / sag-gan / sa-ga-an), also ma2 (boat)."""
import json, re, csv, collections
D=[json.loads(l) for l in open('/home/antigravity/Cuuper22/ivc/work_data/abroad3/cdli_east_atf.jsonl')]
EAST=re.compile(r'dilmun|ma2?-gan|magan|me-luh-ha|me-lu-ha|me-lu-uh-ha|meluhha',re.I)
JAR=re.compile(r'(?<![a-z0-9])(dug|sag-gan|sa-ga-an|dug-sag-gan|ka-sa|gur-sag-gal|dug-ka|ugu-dug)(?![a-z0-9])',re.I)
CLOTH=re.compile(r'tug2|gada|siki|ku3?-?sig17|tug2-|{tug2}',re.I)
BOAT=re.compile(r'ma2',re.I)
print(len(D),'texts;',collections.Counter((x['prov'] or '')[:12] for x in D).most_common(8))
print(collections.Counter(x['period'] for x in D).most_common(8))
rows=[]
for x in D:
    L=[l for l in (x['atf'] or '').replace('\r','').split('\n') if re.match(r'^\d+',l)]
    for i,l in enumerate(L):
        if EAST.search(l):
            win=' / '.join(L[max(0,i-2):i+3])
            rows.append(dict(id='P%06d'%x['id'],des=x['designation'],period=x['period'],prov=x['prov'],line=l[:140],jar=bool(JAR.search(win)),cloth=bool(CLOTH.search(win)),boat=bool(BOAT.search(l)),jarline=bool(JAR.search(l))))
import pandas as pd
r=pd.DataFrame(rows); r.to_csv('/home/antigravity/Cuuper22/ivc/work_data/abroad3/cdli_east_lines.csv',index=False)
print(len(r),'eastern lines in',r.id.nunique(),'texts')
um=r[r.prov.fillna('').str.contains('Umma')]
print('Umma:',um.id.nunique(),'texts')
pd.set_option('display.width',250,'display.max_colwidth',110,'display.max_rows',300)
print(um[['id','des','period','line','jar','cloth','boat']].to_string())
print('\nANY provenience, same-line jar word with eastern name:')
print(r[r.jarline][['id','des','period','prov','line']].to_string())
print('\nANY provenience, jar word within 2 lines + cloth word:')
print(r[(r.jar)&(r.cloth)][['id','des','period','prov','line']].to_string())
