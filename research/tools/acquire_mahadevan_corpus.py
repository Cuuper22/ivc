"""Acquire publicly readable scholarly concordance records. Stop on access denial.
The exact collection is used by indusscript.in's public Browse interface.
No accounts, user records, login tokens, or authentication bypass are used.
"""
import hashlib,json,pathlib,time,urllib.request,urllib.parse,urllib.error
OUT=pathlib.Path('/tmp/ivc-mahadevan');OUT.mkdir(exist_ok=True)
manifest=[]
def fetch(url,name):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (public concordance research)'})
    try:
        with urllib.request.urlopen(req,timeout=45) as f:
            b=f.read(30000000);ct=f.headers.get('Content-Type');final=f.url
        (OUT/name).write_bytes(b)
        manifest.append({'url':url,'file':name,'final_url':final,'bytes':len(b),'content_type':ct,'sha256':hashlib.sha256(b).hexdigest()})
        return b
    except Exception as e:
        manifest.append({'url':url,'file':name,'error':str(e)});return None
base='https://firestore.googleapis.com/v1/projects/theindusscript/databases/(default)/documents/indusarray'
page_token=None;docs=[]
for page in range(100):
    params={'pageSize':300}
    if page_token:params['pageToken']=page_token
    b=fetch(base+'?'+urllib.parse.urlencode(params),f'concordance_page_{page:03d}.json')
    if b is None:break
    payload=json.loads(b);docs.extend(payload.get('documents',[]));page_token=payload.get('nextPageToken')
    print('Page',page,'records',len(docs),flush=True)
    if not page_token:break
    time.sleep(.25)
(OUT/'concordance_documents.json').write_text(json.dumps(docs,ensure_ascii=False))
for name,url in {
    'IM77-Manual.pdf':'https://rmrl.in/wp-content/uploads/IM77-Manual.pdf',
    'intro.pdf':'https://rmrl.in/wp-content/uploads/intro.pdf',
    'AssetManifest.json':'https://indusscript.in/assets/AssetManifest.json',
}.items():fetch(url,name)
(OUT/'acquisition_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Complete:',len(docs),'records',flush=True)
print(json.dumps(manifest,indent=2),flush=True)
