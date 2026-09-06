"""Restore losslessly packed research artifacts after a fresh Git checkout."""
import gzip,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def restore():
    restored=0
    for entry in json.loads((HERE/'payload_manifest.json').read_text())['files']:
        target=HERE/entry['path']
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==entry['sha256']:continue
        raw=gzip.decompress(b''.join((HERE/p).read_bytes() for p in entry['parts']))
        if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:raise ValueError('Payload mismatch: '+entry['path'])
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);restored+=1
    return restored
if __name__=='__main__':print('Restored',restore(),'research files')
