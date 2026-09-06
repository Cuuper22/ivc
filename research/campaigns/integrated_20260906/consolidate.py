#!/usr/bin/env python3
"""Join executed route outputs, evidence dependencies and continuation state.

Packaging does not execute a research experiment or promote a claim.
"""
from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def read(path):return json.loads((HERE/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):(HERE/path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')


def main():
    required=read('shared/candidate_contract.json')['required_fields']
    candidates=[];issues=[]
    for route in ['route_a','route_b','route_c','route_d/outputs']:
        for candidate in read(route+'/candidates.json'):
            missing=[k for k in required if k not in candidate]
            if missing:issues.append({'candidate':candidate.get('id'),'missing_fields':missing})
            item=dict(candidate,record_file=str((HERE/route/'candidates.json').relative_to(ROOT)))
            item['source_paths_resolved']=[]
            for raw in candidate.get('source_paths',[]):
                path=raw.split(':',1)[0]
                choices=[ROOT/path,HERE/route/path,HERE/route.replace('/outputs','')/path]
                found=next((p.resolve() for p in choices if p.is_file()),None)
                if found:
                    item['source_paths_resolved'].append(str(found.relative_to(ROOT)))
                else:
                    issues.append({'candidate':candidate.get('id'),'unresolved_source_path':raw})
            candidates.append(item)
    ids=[c['id'] for c in candidates]
    if len(ids)!=len(set(ids)):issues.append({'duplicate_candidate_ids':True})
    write('candidate_ledger.json',{'accepted_readings_added':0,'candidates':candidates,
        'status_note':'supported_scope_limited denotes a route-local observation, not accepted decipherment',
        'contract_issues':issues})
    dependencies=[]
    for candidate in candidates:
        for source in candidate['source_paths_resolved']:
            dependencies.append({'from':source,'to':candidate['id'],'type':'source_or_derived_input',
                'independence':'not an additional independent observation when another route reuses it'})
        if candidate['route']=='D':
            dependencies.append({'from':'A-FISH211','to':candidate['id'],
                'type':'conditional_orthographic_prerequisite',
                'independence':'dictionary membership cannot validate its own assumed spelling equations'})
            if candidate['id'].startswith('D-TAMIL-JOINT'):
                dependencies.append({'from':'A-ROOF87','to':candidate['id'],
                    'type':'conditional_orthographic_prerequisite',
                    'independence':'source lexical compounds do not independently establish the sign-to-modifier attachment'})
    write('claim_dependencies.json',{'candidate_nodes':ids,'edges':dependencies,
        'cross_route_tasks':[
            {'id':'I-PICTURE','from':['A-FISH211'],'to':'raw field-symbol targets',
             'output':'integration/cross_route_predictions.json','role':'predict under a specified spelling model'},
            {'id':'I-CUP','from':['A-FISH211','A-ROOF87'],'to':'observed companion cup counts',
             'output':'integration/cross_route_predictions.json','role':'test joint field/equivalence assumptions'},
            {'id':'I-SCOPE','from':['A-FISH211','A-ROOF87','C_REPEAT_FISH_87'],
             'to':'C_ROOF_COUNT_SCOPE','output':'route_c/roof_count_scope_programs.json',
             'role':'test literal duplication versus one modifier on the whole field'},
            {'id':'I-PHONETIC-LATTICE','from':['A-FISH211','A-ROOF87'],
             'to':'conditional two-modifier lexical systems','output':'route_d/outputs/two_modifier_lattice.json',
             'role':'enforce one global sequence order and shared modifiers'},
            {'id':'I-ANCHOR-EXCLUSION','from':['B-358-LITERAL','B-COFACE-363'],
             'to':'D lexical prior policy','output':'route_b/semantic_anchors.json',
             'role':'exclude automatic literal animal-name anchors; no accepted sound anchor supplied'}],
        'feedback_policy':'proposals may flow back; a consequence never supplies independent confirmation of its premise',
        'shared_witness':'M77:1551:0 appears in tick, roof/count and lexical chains; count it once per observed target'})
    summaries={r:read(r+'/summary.json') for r in ['route_a','route_b','route_c']}
    summaries['route_d']=read('route_d/outputs/summary.json')
    summaries['integration']=read('integration/summary.json')
    write('results_index.json',{'route_summaries':summaries,
        'candidate_count':len(candidates),'new_accepted_translations':0,'new_accepted_sound_values':0,
        'new_accepted_language_identifications':0,'new_accepted_numerical_values':0})
    ledger=ROOT/'research/data/claim_ledger/claims.json'
    write('accepted_claims.json',{'newly_accepted_claims':[],
        'existing_ledger_path':str(ledger.relative_to(ROOT)), 'existing_ledger_sha256':sha(ledger),
        'decision':'No proposed operational, lexical, phonetic or language reading promoted.',
        'research_status':'executed campaign; connected decoding objective remains unresolved'})
    entrypoints=[p for p in HERE.rglob('*.py') if '__pycache__' not in p.parts]
    manifests=['shared/snapshot.json','evidence_inventory/source_manifest.json',
        'evidence_inventory/recovery_manifest.json','candidate_ledger.json','results_index.json',
        'claim_dependencies.json','accepted_claims.json','task_status.json','continuation.json']
    write('package_manifest.json',{'starting_commit':read('shared/snapshot.json')['starting_commit'],
        'source_snapshot':read('shared/snapshot.json')['source_sha256'],
        'entrypoints':{str(p.relative_to(ROOT)):sha(p) for p in sorted(entrypoints)},
        'records':{p:sha(HERE/p) for p in manifests},
        'execution_note':'Route outputs were executed individually during this session. consolidate.py only packages them; run_campaign.py is the reproduction wrapper.',
        'provenance_issues':issues})
    print(json.dumps({'candidates':len(candidates),'contract_issues':issues,'readings_promoted':0},indent=2))


if __name__=='__main__':main()
