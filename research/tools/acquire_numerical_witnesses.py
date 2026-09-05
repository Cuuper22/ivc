"""Retrieve published glyph illustrations and inventory local source witnesses."""
from pathlib import Path
import concurrent.futures,hashlib,json,subprocess,urllib.request
out=Path('/tmp/ivc-numerical-witnesses');out.mkdir(exist_ok=True)
(out/'repository_tree.txt').write_text(subprocess.check_output(['git','ls-tree','-r','-l','HEAD'],text=True))
ids=[1,8,48,51,59,65,67,72,86,87,89,97,98,99,102,123,130,149,150,162,169,171,176,211,245,254,267,287,293,294,296,328,336,342,343,347,387,389,391,402,403]
def fetch(i):
    name=f'Mahadevan_{i:03d}.png';url=f'https://indusscript.in/assets/images/{i}.png'
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as f:b=f.read();ct=f.headers.get('Content-Type')
        if not b.startswith(b'\x89PNG'):raise ValueError('Not a PNG')
        (out/name).write_bytes(b)
        return {'file':name,'url':url,'bytes':len(b),'content_type':ct,'sha256':hashlib.sha256(b).hexdigest()}
    except Exception as e:return {'file':name,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:log=list(ex.map(fetch,ids))
(out/'glyph_manifest.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
