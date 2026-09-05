"""Retrieve published glyph illustrations and inventory local source witnesses."""
from pathlib import Path
import concurrent.futures,hashlib,json,subprocess
out=Path('/tmp/ivc-numerical-witnesses');out.mkdir(exist_ok=True)
(out/'repository_tree.txt').write_text(subprocess.check_output(['git','ls-tree','-r','HEAD'],text=True))
ids=sorted(set([1,8,48,51,59,65,67,72,123,130,149,150,162,169,171,176,211,245,254,267,287,293,294,296,328,336,342,343,347,387,389,391,402,403]+list(range(86,110))))
def fetch(i):
    name=f'Mahadevan_{i:03d}.png';url=f'https://indusscript.in/assets/images/{i}.png';p=out/name
    try:
        subprocess.run(['curl','-fLsS','--max-time','20','--retry','0',url,'-o',str(p)],check=True,capture_output=True,timeout=25)
        b=p.read_bytes()
        if not b.startswith(b'\x89PNG'):raise ValueError('Not a PNG')
        return {'file':name,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    except Exception as e:
        p.unlink(missing_ok=True);return {'file':name,'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:log=list(ex.map(fetch,ids))
(out/'glyph_manifest.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
