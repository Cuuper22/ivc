#!/usr/bin/env python3
"""Exact conditional phonetic/segmentation search; no new archaeological evidence.

The fish expansion is a HYPOTHESIS. Dictionary attestations are independent
language facts; attaching their meanings to Indus signs is NOT independent.
Search counts are exact for the explicitly delimited model, not probabilities.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math, re
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CAMPAIGN = HERE.parent
MW = ROOT / 'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'
DRAV = CAMPAIGN / 'evidence_inventory/dravidian_lexical_examples.json'
FISH = {'59':'60','65':'66','67':'68','72':'73'}
NUMERIC = {'86','87','89','95','96'}

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def lexical_inventory():
    """All alphabetic MW key1 headwords, preserving SLP1 case and references.

    A fish-gloss filter is a declared semantic PRIOR, not an Indus observation.
    Its literal rule and selected source passages are written to the inventory.
    """
    words, fish, records = {}, {}, 0
    pattern = re.compile(r'\ba\s+(?:(?:kind|species|sort)\s+of\s+)?fish\b', re.I)
    for _, elem in ET.iterparse(MW, events=['end']):
        if not re.fullmatch(r'H[1-4][AB]?', elem.tag):
            continue
        records += 1
        key = elem.findtext('./h/key1')
        if key and re.fullmatch('[A-Za-z]+', key):
            body_el = elem.find('body')
            body = ' '.join(body_el.itertext()) if body_el is not None else ''
            ref = {'headword':key, 'entry_id':elem.findtext('./tail/L'),
                   'printed_page_column':elem.findtext('./tail/pc')}
            words.setdefault(key, ref)
            if pattern.search(body):
                fish[key] = ref | {'source_passage':body}
        elem.clear()
    return words, fish, records, pattern.pattern

def extension_edges(words):
    """Every nonempty root/extension split; no length/vocabulary cutoff.

    This permits meaning-bearing roots and a consistently pronounced marker.
    Both the root and expanded form must occur as dictionary headwords.
    Headword extension alone is NOT proof of productive inflection.
    """
    edges = {'append':collections.defaultdict(set), 'prepend':collections.defaultdict(set)}
    vocab = set(words)
    for word in sorted(vocab):
        for i in range(1,len(word)):
            if word[:i] in vocab:
                edges['append'][word[i:]].add(word[:i])
            if word[i:] in vocab:
                edges['prepend'][word[:i]].add(word[i:])
    return edges

def perm(n,k):
    return math.prod(range(n-k+1,n+1)) if n>=k else 0

def sound_solver(examples, fixed=None, max_unit=8, silent=()):
    """Exact joint unit-boundary and reusable sign-to-string CSP.

    Each example is (sign tuple, supplied phonetic string). Only declared
    classifiers may be empty. Global homophony allowed; no per-object repair.
    """
    examples = sorted(examples, key=lambda z:(len(z[0]),len(z[1]),z))
    solutions=[]
    def one(signs, word, mapping, i=0, j=0):
        if i==len(signs):
            if j==len(word): yield mapping
            return
        sign=signs[i]
        if sign in mapping:
            token=mapping[sign]
            if word.startswith(token,j):
                yield from one(signs,word,mapping,i+1,j+len(token))
            return
        for size in range(0 if sign in silent else 1,min(max_unit,len(word)-j)+1):
            yield from one(signs,word,mapping|{sign:word[j:j+size]},i+1,j+size)
    def step(index,mapping):
        if index==len(examples):
            solutions.append(mapping);return
        signs,word=examples[index]
        for candidate in one(signs,word,mapping):step(index+1,candidate)
    step(0,dict(fixed or {}))
    return solutions

def control():
    # Constructed diagnostic only. No invented form enters Indus evidence.
    train=[(('A','B'),'kami'),(('A','C'),'katu'),(('D','B'),'sami')]
    free=sound_solver(train,max_unit=3)
    anchored=sound_solver(train+[(('A',),'ka')],max_unit=3)
    mixed=sound_solver(train+[(('A',),'ka'),(('N','D','B'),'sami')],
                       fixed={'N':''},silent={'N'},max_unit=3)
    broken=sound_solver(train+[(('A',),'ka'),(('D','C'),'sata')],max_unit=3)
    assert len(anchored)==len(mixed)==1 and not broken
    predictions=sorted({x['D']+x['C'] for x in free})
    assert predictions==['satu']
    return {'evidence_class':'constructed_control_not_Indus','training':train,
            'unanchored_segmentations':free,'independent_A_ka_anchor':anchored,
            'mixed_classifier_control':mixed,'withheld_D_C_predictions':predictions,
            'withheld_D_C_true':'satu','incompatible_D_C_sata_solutions':len(broken)}

def summarize_search(edges, fish):
    summaries=[]; examples=[]
    for orientation,by_marker in edges.items():
        for anchor in ['none','base59_fish','all_four_fish','all_eight_fish','all_eight_fish_homophony']:
            systems=0; markers=0; scored=[]
            for marker,roots in by_marker.items():
                relevant=roots & set(fish)
                if anchor.startswith('all_eight'):
                    relevant={r for r in relevant if (r+marker if orientation=='append' else marker+r) in fish}
                if anchor=='none':n=perm(len(roots),4)
                elif anchor=='base59_fish':n=len(relevant)*perm(len(roots)-1,3)
                elif anchor.endswith('homophony'):n=len(relevant)**4
                else:n=perm(len(relevant),4)
                if not n:continue
                systems+=n;markers+=1
                # Minimal fixed transliteration-character cost, no exceptions.
                ordered=sorted(roots,key=lambda x:(len(x),x))
                if anchor.endswith('homophony'):chosen=[min(relevant,key=lambda x:(len(x),x))]*4
                elif anchor in ('all_four_fish','all_eight_fish'):chosen=sorted(relevant,key=lambda x:(len(x),x))[:4]
                elif anchor=='base59_fish':
                    first=min(relevant,key=lambda x:(len(x),x))
                    chosen=[first]+[x for x in ordered if x!=first][:3]
                else:chosen=ordered[:4]
                cost=sum(map(len,chosen))+len(marker)+5
                scored.append((cost,marker,chosen,n))
            scored.sort()
            summaries.append({'language':'Sanskrit_dictionary_conditional',
                'orientation':orientation,'semantic_prior':anchor,
                'distinct_base_readings':not anchor.endswith('homophony'),'compatible_markers':markers,
                'compatible_systems_exact':systems,
                'minimum_description_cost':scored[0][0] if scored else None,
                'cost_definition':'one unit per stored source-transliteration character +5 reusable assignments; fixed graphic grammar cost omitted equally',
                'phonetic_correctness_targets':0})
            # Output witnesses are a display subset; counts used ALL roots/splits.
            for cost,marker,chosen,n in scored[:8]:
                mapping={base:root for base,root in zip(FISH,chosen)}|{'211':marker}
                for base,marked in FISH.items():
                    mapping[marked]=(mapping[base]+marker if orientation=='append' else marker+mapping[base])
                examples.append({'id':f'D-MW-{orientation}-{anchor}-{len(examples):03}',
                    'language':'Sanskrit_conditional','orientation':orientation,
                    'semantic_prior':anchor,'mapping':mapping,'cost':cost,
                    'systems_at_this_marker':n,'prerequisites':['A fish expansion conjecture',
                    'Indus words realize MW headword spellings without historical sound changes',
                    ('four fish bases may be homophones with separate anonymous classes' if anchor.endswith('homophony') else 'four fish bases have distinct lexical values'),
                    'dictionary membership is relevant despite different chronology'],
                    'source_words':chosen+[mapping[x] for x in FISH.values()]})
    return summaries,examples

def tamil_search(forms):
    compounds=[f for f in forms if len(f['segmentation_as_printed'])>1]
    candidates=[]
    for f in compounds:
        seg=f['segmentation_as_printed'];root=seg[-1]
        marker=seg[0];link=''.join(seg[1:-1])
        mapping={base:root for base in FISH}|{'211':marker}
        mapping.update({marked:marker+link+root for marked in FISH.values()})
        category=('fish' if 'fish' in f['gloss'] else 'star')
        candidates.append({'id':f'D-TAMIL-{len(candidates):02}',
            'language':'Tamil_comparative_conditional','orientation':'prepend',
            'mapping':mapping,'linking_segment':link,
            'link_rule':('add source-attested m before mīṉ after ai' if link else None),
            'semantic_category_prior':category,'lexical_record':f,
            'homophony':'four base signs share a sound; separate anonymous classifiers preserve their distinctions',
            'cost':len(root)+len(marker)+len(link)+2+4+(1 if link else 0),
            'prerequisites':['A fish expansion conjecture','base fish signs read Tamil mīṉ',
                'all four fish variants share a lexical pronunciation',
                'source stored order base–211 realized as qualifier–root within word',
                'Tamil compound is chronologically relevant to Indus']})
    ablations=[{'prior':p,'remaining_systems':sum(p=='none' or c['semantic_category_prior']==p for c in candidates)}
               for p in ['none','fish','star']]
    return candidates,ablations

def read_block(seq,candidate):
    """Freeze all roles, map recurring forms, preserve every unknown token.

    Reordering only applies to the declared base+211 compound. No free reversal
    or phonetic/zero switching for troublesome individual occurrences.
    """
    out=[];i=0;mapping=candidate['mapping']
    while i<len(seq):
        s=seq[i]
        if s in FISH and i+1<len(seq) and seq[i+1]=='211':
            root=mapping[s];marker=mapping['211']
            text=(root+marker if candidate['orientation']=='append'
                  else marker+candidate.get('linking_segment','')+root)
            out.append({'source_signs':[s,'211'],'role':'logogram+phonetic_marker','candidate_sound':text})
            i+=2;continue
        if s in mapping:
            out.append({'source_signs':[s],'role':'logophonetic' if s!='211' else 'phonetic_marker',
                        'candidate_sound':mapping[s]})
        elif s in NUMERIC and ((i>0 and seq[i-1]=='328') or (i+1<len(seq) and seq[i+1]=='328')):
            out.append({'source_signs':[s],'role':'candidate_nonphonetic_stroke_class',
                        'unread':f'<STROKE:{s}>'})
        else:
            out.append({'source_signs':[s],'role':'unresolved','unread':f'<M77:{s}>'})
        i+=1
    return out

def corpus_application(candidates,obs,pairs):
    applications=[]; summaries=[]
    strict=[r for r in obs if r['strict']]
    for c in candidates:
        complete_types=set();partial_types=set();standalone_marker_types=set();pair_agreement=[]
        for r in strict:
            seq=r['tokens_stored']
            if not any(s in c['mapping'] for s in seq):continue
            parts=read_block(seq,c)
            complete=all('candidate_sound' in p for p in parts)
            (complete_types if complete else partial_types).add(tuple(seq))
            if any(p['source_signs']==['211'] for p in parts):standalone_marker_types.add(tuple(seq))
            # Every output is a candidate partial reading, never scored truth.
            applications.append({'candidate_id':c['id'],'row_id':r['row_id'],
                'object_id':r['object_id'],'source_record':r['source_record'],
                'expression_key':r['exact_expression_key'],'source_sequence':seq,
                'segmentation':parts,'complete_under_hypothesis':complete,
                'correctness_independently_scorable':False})
        for p in pairs:
            a=read_block(p['compact'],c);b=read_block(p['expanded'],c)
            render=lambda x:[z.get('candidate_sound',z.get('unread')) for z in x]
            pair_agreement.append({'compact':p['compact'],'expanded':p['expanded'],
                'same_decoding':render(a)==render(b),
                'classification':'consequence_of_assumed_equivalence_not_validation'})
        summaries.append({'candidate_id':c['id'],'complete_expression_types':len(complete_types),
            'partial_expression_types':len(partial_types),'standalone_211_expression_types':len(standalone_marker_types),
            'six_premise_pairs':pair_agreement,'independent_phonetic_targets':0,
            'warning':'coverage is NOT correctness or decipherment coverage'})
    return applications,summaries

def test_bound_fish_marker(obs):
    """A literal, global bound-fish-morpheme restriction has observed failures.

    Lines are never silently concatenated. A whole-object fish requirement is
    tested separately so a 211-only line is not treated as an isolated object.
    """
    groups=collections.defaultdict(list)
    for row in obs:groups[row['object_id']].append(row)
    fish_signs=set(FISH)|set(FISH.values())
    cases=[];adjacent=0;nonadjacent=0
    for row in obs:
        if not row['strict']:continue
        seq=row['tokens_stored']
        for i,s in enumerate(seq):
            if s!='211':continue
            if i>0 and seq[i-1] in FISH:adjacent+=1
            else:
                nonadjacent+=1
                cases.append({'row_id':row['row_id'],'object_id':row['object_id'],
                    'sequence':seq,'position':i,'source_record':row['source_record']})
    fish_free=[]
    for oid,rr in groups.items():
        if not all(r['strict'] for r in rr):continue
        tokens=[s for r in rr for s in r['tokens_stored']]
        if '211' in tokens and not set(tokens)&fish_signs:
            fish_free.append({'object_id':oid,'rows':[{'row_id':r['row_id'],
                'face_code':r['face_code'],'line_code':r['line_code'],
                'sequence':r['tokens_stored'],'source_record':r['source_record']} for r in rr]})
    return {'claim_tested':'Every211 occurrence is a bound morpheme on one of four fish bases',
        'adjacent_base_then_211_occurrences':adjacent,
        'nonadjacent_211_occurrences':nonadjacent,
        'complete_objects_with_211_and_no_core_fish_sign':len(fish_free),
        'fish_free_objects':fish_free,'nonadjacent_witnesses':cases,
        'decision':'global bound-core-fish-only model contradicted; local fish compounding and marker used with other roots remain open',
        'limitation':'The fish set is the four bases tested by this campaign, not an exhaustive graphical or lexical fish inventory.'}

def main():
    out=HERE/'outputs';out.mkdir(exist_ok=True)
    words,fish,records,fish_rule=lexical_inventory()
    edges=extension_edges(words)
    summaries,mw_candidates=summarize_search(edges,fish)
    sample_forms=json.loads(DRAV.read_text())
    full_tamil=CAMPAIGN/'evidence_inventory/tamil_compounds.json'
    if full_tamil.exists():
        corrected=next(r for r in json.loads(full_tamil.read_text())['records'] if r['entry_id']=='tamil_app_280_26')
        for f in sample_forms:
            if f['form']=='kuru-mīṉ':
                f['initial_transcription_superseded']=f['form']
                f['form']=corrected['printed_form_transcription']
                f['segmentation_as_printed']=corrected['segmentation_as_printed']
                f['normalization_source']=str(full_tamil.relative_to(ROOT))+'#tamil_app_280_26'
    tamil,ablations=tamil_search(sample_forms)
    forms=list(words)
    alphabet=sorted(set(''.join(forms)))
    table=str.maketrans(''.join(alphabet),''.join(alphabet[1:]+alphabet[:1]))
    rotated={w.translate(table) for w in forms}
    rotated_edges=extension_edges(rotated)
    # Matched whole-search control under bijective sound renaming.
    invariance=all(len(roots)==len(rotated_edges[o][m.translate(table)])
        for o,e in edges.items() for m,roots in e.items())
    assert invariance
    rows=[json.loads(x) for x in (CAMPAIGN/'shared/observations.jsonl').read_text().splitlines()]
    raw_pairs=json.loads((ROOT/'research/data/semantic_search_20260906/modifier_context_pairs.json').read_text())
    pairs=[p for p in raw_pairs if p['family']=='four_surrounding_strokes' and p['side']=='after' and p['extra']==211 and str(p['base']) in FISH]
    assert len(pairs)==6
    # Retain alternatives without exporting every huge lexical cross product.
    representatives=[]
    for orientation in ['append','prepend']:
        for anchor in ['none','all_four_fish']:
            representatives.append(next(c for c in mw_candidates if c['orientation']==orientation and c['semantic_prior']==anchor))
    representatives+=tamil
    for orientation in ['append','prepend']:
        for anchor in ['all_eight_fish','all_eight_fish_homophony']:
            found=[c for c in mw_candidates if c['orientation']==orientation and c['semantic_prior']==anchor]
            if found:representatives.append(found[0])
    applications,coverage=corpus_application(representatives,rows,pairs)
    with (out/'candidate_partial_readings.jsonl').open('w') as f:
        for r in applications:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    inventory={'mw_path':str(MW.relative_to(ROOT)),'mw_sha256':sha(MW),
        'xml_entries':records,'distinct_alphabetic_headwords':len(words),
        'direct_fish_gloss_headwords':len(fish),'fish_prior_rule':fish_rule,
        'fish_gloss_records':fish,'dravidian_path':str(DRAV.relative_to(ROOT)),
        'source_warning':'Headwords independent of Indus; all proposed sign attachments conditional. MW late attestation and selected Tamil compounds cannot identify ancient language.',
        'excluded_as_independent':['archived words.csv proposed readings','archived xlits.csv proposed phonetics',
            'lexicons.json manually selected supplements','vidyut generated morphology treated as generated only',
            'quarantined external-object metadata','failed Meluhha object bridges']}
    dump(out/'linguistic_inventory.json',inventory)
    dump(out/'mw_extension_counts.json',{'search':summaries,'by_marker':{
        o:[{'marker':m,'root_count':len(rs),'fish_root_count':len(rs & set(fish))}
           for m,rs in sorted(e.items()) if len(rs)>=4 or rs & set(fish)] for o,e in edges.items()},
        'omitted_marker_rows':'markers with fewer than4 roots and zero fish roots: they generate zero systems in every tested configuration'})
    for c in mw_candidates:
        c['source_references']=[words[w] for w in c.pop('source_words')]
    dump(out/'explicit_systems.json',{'mw_representatives':mw_candidates,'tamil_systems':tamil,
        'anonymous_rivals':[{'system':'unresolved-language logograms L59/L65/L67/L72 + operation Q',
            'sound_assignments':None,'rule':'marked fish=Q(base); separate base+211=Q(base)',
            'parameters':'four referent labels and one reusable operation'},
            {'system':'nonphonetic classifier/operation','sound_assignments':{},
             'rule':'fish variants are category labels;211=nonphonetic operation Q',
             'parameters':'same four labels and one operation'}]})
    dump(out/'pair_dependencies.json',pairs)
    bound_test=test_bound_fish_marker(rows)
    dump(out/'bound_marker_scope_test.json',bound_test)
    dump(out/'coverage_not_accuracy.json',coverage)
    dump(out/'controls.json',{'segmentation':control(),'full_lexicon_sound_relabeling':{
        'alphabet_size':len(alphabet),'same_root_counts_for_every_marker':invariance,
        'original_marker_counts':{o:len(e) for o,e in edges.items()},
        'relabeling':dict(zip(alphabet,alphabet[1:]+alphabet[:1])),
        'interpretation':'Exact symmetry for THIS extension/membership objective with renamed lexicon. Does not claim all linguistic evidence is invariant.'}})
    constraints={'D31':'executed:192k-scale independent Sanskrit lexicon; source-verified Tamil comparative forms; unresolved language retained',
        'D32':'executed:roots/logograms, fused signs, phonetic211, silent classifier rival and C stroke-role exclusion',
        'D33':'executed:all root/extension splits, both orders, shared marker, repeated global mappings; exact segmentation CSP control',
        'D34':'executed:zero/one/four fish-gloss priors; Tamil fish/star priors. B supplies exclusions but no lexical anchor',
        'D35':'executed:two named linguistic systems, anonymous and nonphonetic rivals; full lexical sound-relabel control',
        'D36':'executed candidate propagation; independent phonetic correctness evaluation blocked by zero target pronunciations. Six equal forms are assumed premises, not heldout validation',
        'D37':'executed:explicit mappings, semantic/orthographic prerequisites, exact source citations and unread spans exported'}
    summary={'namespace':'Mahadevan1977','source_pairs':len(pairs),'base_families':len(FISH),
        'mw_search':summaries,'tamil_anchor_ablations':ablations,
        'representative_systems_applied':len(representatives),'candidate_partial_reading_rows':len(applications),
        'bound_core_fish_only_contradictions':bound_test['complete_objects_with_211_and_no_core_fish_sign'],
        'independent_sound_values_accepted':0,'new_language_identifications':0,
        'semantic_anchor_status':'B has no independently identified lexical referent; all named attachments are priors',
        'historical_sound_correspondences':'none introduced; modern/lexical forms kept explicit and conditional',
        'prior_exposure':'retrospective; sources and all six candidate pairs previously inspected',
        'plan_execution':constraints}
    dump(out/'summary.json',summary)
    source_paths=[str(MW.relative_to(ROOT)),str(DRAV.relative_to(ROOT)),
        'research/data/semantic_search_20260906/modifier_context_pairs.json',
        'research/campaigns/integrated_20260906/shared/observations.jsonl']
    candidate_records=[]
    for c in representatives:
        candidate_records.append({'id':c['id'],'route':'D','status':'conditional','claim_type':'sound_assignment',
            'rule':{'mapping':c['mapping'],'orientation':c['orientation'],'decoder':'run_route_d.py:read_block'},
            'namespace':'Mahadevan1977','context':'four fish bases and marked forms;211 reusable phonetic component',
            'prerequisites':c['prerequisites'],'support':{'independent_lexical_forms':True,'independent_sign_sound_pairs':0},
            'contradictions':['no known target pronunciation permits direct correctness test',
                'allographs/homophony and compound boundaries not independently established'],
            'alternatives':['other emitted lexical systems','anonymous operation','nonphonetic classifier'],
            'parameters':c['mapping'],'complexity':c['cost'],
            'predictions':['fixed repeated form readings in candidate_partial_readings.jsonl',
                'new fish family70/71 needs root reading; operation alone predicts no sound'],
            'source_paths':source_paths,'prior_exposure':'retrospective, hypothesis-defining pairs excluded from independent accuracy'})
    dump(out/'candidates.json',candidate_records)
    print(json.dumps({'mw_headwords':len(words),'fish_prior_headwords':len(fish),
        'mw_search':summaries,'tamil_ablations':ablations,'applied_systems':len(representatives),
        'partial_reading_rows':len(applications),'sound_values_accepted':0},indent=2))

if __name__=='__main__':main()
