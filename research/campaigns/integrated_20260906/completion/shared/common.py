"""Frozen reconstruction interfaces; observations never become guessed readings."""
from pathlib import Path
import collections, hashlib, json

CAMPAIGN = Path(__file__).resolve().parents[2]
OUT = CAMPAIGN/'completion'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def write(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def load_rows():
    return [json.loads(x) for x in (CAMPAIGN/'shared/observations.jsonl').read_text().splitlines()]

def raw_key(row):
    # Includes uncertain signs and unknown spans verbatim. Empty lines cannot
    # connect all objects, and blanks inside a line remain distinguishable.
    slots=row['raw_slots']; end=max((i for i,x in enumerate(slots) if x),default=-1)
    return tuple(slots[:end+1])

def partition(rows, targets, extra_objects=()):
    target_set=set(targets)
    keys={raw_key(r) for r in rows if r['row_id'] in target_set and r['tokens_stored']}
    blocked=set(extra_objects)|{r['object_id'] for r in rows if r['row_id'] in target_set or (raw_key(r) and raw_key(r) in keys)}
    return {'target_row_ids':sorted(target_set),'train_row_ids':[r['row_id'] for r in rows if r['object_id'] not in blocked], 'excluded_object_ids':sorted(blocked), 'exact_raw_patterns':[list(k) for k in sorted(keys)],'exposure':'retrospective; previous research and conversation already exposed these data'}

def build_masks(rows=None):
    rows=rows or load_rows()
    # Distinct complete raw expressions assigned to folds. Components and other
    # spellings may remain; all copies and companion faces are excluded.
    masks={}
    for f in range(5):
        targets=[r['row_id'] for r in rows if r['tokens_stored'] and int(digest(raw_key(r))[:12],16)%5==f]
        masks['recombination_'+str(f)]=partition(rows,targets)
    targets=[r['row_id'] for r in rows if any(x.lstrip('*') in ('70','71') for x in r['tokens_stored'])]
    masks['unseen_family_70_71']=partition(rows,targets)
    medium_objects={r['object_id'] for r in rows if str(r['raw_fields']['inscobj'])=='3'}
    targets=[r['row_id'] for r in rows if r['object_id'] in medium_objects and r['tokens_stored']]
    masks['medium_3']=partition(rows,targets,medium_objects)
    packet={'schema':'ivc.reconstructed.masks.v1','source_sha256':rows[0]['source_sha256'],'masks':masks,'selection':'fixed before reconstruction joint fitting; full raw-expression groups, explicit family and medium transfer','mask_digest':digest(masks)}
    write(OUT/'shared/masks.json',packet)
    return packet

def distinct_rows(rows):
    # One expression/context type, retain sources separately in original data.
    result={}
    for r in rows:
        k=(raw_key(r),str(r['raw_fields'].get('inscobj')),str(r['raw_fields'].get('dir')))
        result.setdefault(k,r)
    return list(result.values())

if __name__=='__main__':
    packet=build_masks()
    print({k:(len(v['train_row_ids']),len(v['target_row_ids'])) for k,v in packet['masks'].items()})
