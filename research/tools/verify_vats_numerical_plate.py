"""Render selected original publication plates, preserving scan provenance."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as ET
import fitz
out=Path('/tmp/ivc-vats-plate');out.mkdir(exist_ok=True)
base='evidence/tmp/032_002_861_603_slot_source_normalization/'
manifest=[]
for name in ['vats_plates_djvu.txt','vats_plates_scandata.xml','vats_excavations_at_harappa_vol2_plates.pdf']:
    data=subprocess.check_output(['git','show','HEAD:'+base+name],timeout=150)
    (out/name).write_bytes(data)
    manifest.append({'repository_path':base+name,'file':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
doc=fitz.open(out/'vats_excavations_at_harappa_vol2_plates.pdf')
root=ET.parse(out/'vats_plates_scandata.xml').getroot()
scans=[{'leaf':int(p.attrib['leafNum']),'number':p.findtext('pageNumber'),'type':p.findtext('pageType'),'access':p.findtext('addToAccessFormats')} for p in root.findall('.//pageData/page')]
(out/'scan_pages.json').write_text(json.dumps(scans,indent=2))
hits=[]
for i,p in enumerate(doc):
    t=p.get_text()
    if any(k in t.upper() for k in ['XCVIII','XCIX']) or ('553' in t and ('554' in t or '555' in t)):
        hits.append({'page_index':i,'text':t})
# Scan pagination supplies a second route if embedded text is sparse.
for p in scans:
    if (p['number'] or '').strip().upper() in ['XCVIII','XCIX']:
        hits.append({'scan_leaf':p['leaf'],'label':p['number']})
(out/'plate_candidates.json').write_text(json.dumps({'pdf_pages':len(doc),'hits':hits},indent=2))
indices=sorted(set(h['page_index'] for h in hits if 'page_index' in h))
if not indices:
    leaves=[h['scan_leaf'] for h in hits if 'scan_leaf' in h]
    indices=sorted({i for l in leaves for i in range(l-2,l+2) if 0<=i<len(doc)})
for i in indices[:12]:
    doc[i].get_pixmap(matrix=fitz.Matrix(2.5,2.5)).save(out/f'vats_page_{i:03d}.png')
print(json.dumps({'pages':len(doc),'rendered':indices[:12],'hits':hits},indent=2))
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
# The full source PDF is already in the repository; do not duplicate it in the artifact.
(out/'vats_excavations_at_harappa_vol2_plates.pdf').unlink()
