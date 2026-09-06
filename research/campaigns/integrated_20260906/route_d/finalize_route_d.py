#!/usr/bin/env python3
"""Expose final connected candidates in coordinator contract; record execution."""
import hashlib,json
from pathlib import Path
from run_route_d import HERE,ROOT

def main():
    out=HERE/'outputs';candidates=json.loads((out/'candidates.json').read_text())
    candidates=[c for c in candidates if c['id']!='D-KA-CONDITIONAL' and not c['id'].startswith('D-TAMIL-JOINT')]
    control=json.loads((out/'semantic_category_control.json').read_text())
    fish=next(r for r in control['runs'] if r['category']=='fish' and r['mode']=='full_category')
    roots=fish['search']['append']['markers'][0]['roots']
    candidates.append({'id':'D-KA-CONDITIONAL','route':'D','status':'conditional','claim_type':'sound_assignment',
        'rule':{'211':'ka','base_59_65_67_72':{'choose_distinct_from':roots},
            'marked_60_66_68_73':'base_reading + ka'},'namespace':'Mahadevan1977',
        'context':'four fish-base/marked pairs, postposed211 spelling hypothesis',
        'prerequisites':['all8Indus signs name lexical fish categories',
            'the four base signs have distinct lexical pronunciations',
            'literal identity with a MW alphabetic headword is permitted',
            'productive211 append operation from RouteA is valid'],
        'support':{'MW_fish_root_pairs':6,'root_assignments':360,'permitted_marker_strings':['ka']},
        'contradictions':['No independent Indus fish-name anchors',
            'Bird-control search also uniquely selects ka',
            'Allowing homophony admits22marker strings',
            'adding independent concatenative roof operation leaves0fullfish lexical squares'],
        'alternatives':['generic Sanskrit lexical extension','homophonic mixed script','Tamil contextual morphology','anonymous classifier'],
        'parameters':{'marker':1,'distinct_root_assignments':4},'complexity':'5shared assignments; no object exceptions',
        'predictions':['fixed ka on every claimed211 within licensed fish construction; not a pronunciation correctness test'],
        'source_paths':['outputs/mw_extension_counts.json','outputs/semantic_category_control.json','outputs/semantic_category_source_entries.json'],
        'prior_exposure':'retrospective, A pairs define hypothesis; all semantic filters declared priors'})
    full=json.loads((out/'tamil_full_joint_search.json').read_text())
    for s in full['explicit_mixed_systems']:
        candidates.append({'id':s['id'],'route':'D','status':'conditional','claim_type':'sound_assignment',
            'rule':{'mapping':s['mapping'],'decoder':'tamil_joint_search.py:decode_lattice',
                'operations':s['morphological_operations']},'namespace':'Mahadevan1977',
            'context':'59/65/60/66 lattice, separate roof87 andticks211;70/71only anonymous structure',
            'prerequisites':['A roof87 andticks211 operational equivalences',
                'fish glyph59 reads comparative Tamil mīṉ',
                'qualifier meanings selected from the source lexical triangle',
                'one canonical qualifier order across all spellings',
                'source-conditioned boundary/allomorph realization; no productive historical law established'],
            'support':{'source_lexical_triangle':s['source_lexical_records'],
                'executed_spelling_forms':s['four_spellings'],'independent_phonetic_targets':0},
            'contradictions':['strict sound-by-sign linear concatenation fails',
                'swapping87/211modifier identities produces another compatible system',
                'no generalization of lexical surface rules beyond supplied words yet'],
            'alternatives':['other emitted Tamil systems','87quantity+fish with211nonphonetic role','anonymous operators'],
            'parameters':s['mapping'],'complexity':s['repair_cost'],
            'predictions':['worked267–99compound parses','1380/2452equivalent abstract parses with root70 unread'],
            'source_paths':['outputs/tamil_full_joint_search.json','outputs/tamil_joint_worked_readings.json',
                'outputs/new_fish_family_propagation.json'],
            'prior_exposure':'retrospective, A observations and semantic priors are not independent confirmations'})
    (out/'candidates.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n')
    manifest={'run_command':'python research/campaigns/integrated_20260906/route_d/run_all.py',
        'executed_programs':['run_route_d.py','search_modifier_lattice.py','semantic_category_control.py','tamil_joint_search.py','test_counted_fish_composition.py','finalize_route_d.py'],
        'results':{'conditional_candidate_records':len(candidates),'independent_phonetic_values_accepted':0,
            'full_tamil_distinct_mixed_systems':full['distinct_mixed_phonetic_systems']},
        'files':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(HERE.rglob('*')) if p.is_file() and p.suffix in ('.py','.json','.jsonl') and p.name!='execution_manifest.json'},
        'next_experiment':'Use existing2275/1008roof relation and retained67–336–89–211suffix to test local-root versus whole-field scope for87/211. Keep7283/4019doubtful IDs in a separate sensitivity lane. Counted-fish composition has already failed to obtain support outside267–99under exact, one-edit and partial tests.'}
    (out/'execution_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest['results']))

if __name__=='__main__':main()
