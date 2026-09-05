"""Retrieve public Indus Research Centre application resources, without authentication.
No translations are inferred here. Preserve URLs, HTTP outcomes, and hashes.
"""
import hashlib,json,pathlib,re,urllib.request,urllib.parse,concurrent.futures
OUT=pathlib.Path('/tmp/ivc-public-corpus');OUT.mkdir(exist_ok=True)
log=[]
def get(url,name):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research corpus audit)'})
        with urllib.request.urlopen(req,timeout=35) as f:
            b=f.read(25000000);ct=f.headers.get('Content-Type');final=f.url
        (OUT/name).write_bytes(b)
        entry={'url':url,'final_url':final,'file':name,'content_type':ct,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};log.append(entry)
        return b.decode('utf-8',errors='replace')
    except Exception as e:
        log.append({'url':url,'file':name,'error':str(e)});return ''
html=get('https://indusscript.in/','index.html')
urls=sorted({urllib.parse.urljoin('https://indusscript.in/',u) for u in re.findall(r'(?:src|href)=[\"\']([^\"\']+\.(?:js|css)(?:\?[^\"\']*)?)[\"\']',html)})
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(lambda pair:get(pair[1],f'asset_{pair[0]}_'+pathlib.PurePosixPath(urllib.parse.urlparse(pair[1]).path).name),enumerate(urls)))
get('https://indusscript.in/robots.txt','robots.txt')
(OUT/'manifest.json').write_text(json.dumps(log,indent=2))
print(json.dumps(log,indent=2))
