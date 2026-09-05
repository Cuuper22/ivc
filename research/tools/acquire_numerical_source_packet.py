"""Copy only explicitly selected existing repository witnesses, with hashes."""
from pathlib import Path
import subprocess,hashlib,json,concurrent.futures
out=Path('/tmp/ivc-source-packet');out.mkdir(exist_ok=True)
lines=subprocess.check_output(['git','ls-tree','-r','HEAD'],text=True).splitlines()
paths=[x.split('\t',1)[1] for x in lines]
objects=['H-306','H-326','H-904','H-924','H-925','H-926','H-1313','H-1923','M-331']
selected=[p for p in paths if (p.startswith('evidence/tmp/cisi_xml/') and p.endswith('_djvu.txt')) or ('/seal_images/' in p and any(Path(p).name.startswith(x+'_') for x in objects))]
def copy(p):
    b=subprocess.check_output(['git','show','HEAD:'+p],timeout=90)
    name=Path(p).name;(out/name).write_bytes(b)
    return {'repository_path':p,'file':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
# Serialize lazy git object retrieval; concurrent git fetches can contend on pack locks.
manifest=[copy(p) for p in selected]
(out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
