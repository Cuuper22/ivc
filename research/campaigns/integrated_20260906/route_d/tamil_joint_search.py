#!/usr/bin/env python3
"""Full held Tamil compound inventory: two graphic operators and morphology.

Zero direct phonetic anchors. Concrete morphological alternatives retain exact
observed compound surfaces. Context realizations are charged dictionary rules,
not asserted productive historical sound laws.
"""
import collections,itertools,json
from pathlib import Path
from search_modifier_lattice import search
from run_route_d import HERE,FISH,read_block

def decode_lattice(seq,system):
    """Interpret fused/separate operators with one global canonical order.

    ROOT identity is explicit. Repeated operators are unsupported instead of
    silently idempotent. Unknown signs break this local construction.
    """
    graph={'59':(), '65':('ROOF',), '60':('TICK',), '66':('ROOF','TICK'),
           '70':(), '71':('TICK',)}
    mapping=system['mapping'];out=[];i=0
    while i<len(seq):
        start=i;mods=[]
        while i<len(seq) and seq[i]=='87':mods.append('ROOF');i+=1
        if i==len(seq) or seq[i] not in graph:
            out.extend({'unread':f'<M77:{s}>'} for s in seq[start:i])
            if i<len(seq):out.append({'unread':f'<M77:{seq[i]}>'});i+=1
            continue
        root_id='70' if seq[i] in ('70','71') else '59'
        mods.extend(graph[seq[i]]);i+=1
        while i<len(seq) and seq[i]=='211':mods.append('TICK');i+=1
        if len(mods)!=len(set(mods)):
            out.append({'unresolved_repeated_operation':seq[start:i]});continue
        if root_id=='70':
            out.append({'source_signs':seq[start:i],'root':'<UNREAD_ROOT70>',
                'operators':sorted(mods),'candidate_surface':None,
                'phonetic_limit':'spelling operation transferred; root70 and its contextual pronunciation remain unknown'})
            continue
        mark=('66' if len(mods)==2 else '65' if mods==['ROOF'] else '60' if mods==['TICK'] else '59')
        out.append({'source_signs':seq[start:i],'root':'mīṉ','operators':sorted(mods),
                    'candidate_surface':mapping[mark]})
    return out

def main():
    source=HERE.parent/'evidence_inventory/tamil_compounds.json'
    inventory=json.loads(source.read_text())
    rows=[r for r in inventory['records'] if r['form_status']=='visually_transcribed']
    for r in rows:
        if r['segmentation_as_printed'] is None:
            form=r['printed_form_transcription']
            assert form.endswith('mīṉ')
            r['segmentation_for_search']=[form[:-len('mīṉ')],'mīṉ']
            r['search_boundary_basis']='candidate split at exact recurring mīṉ suffix; no printed hyphen'
        else:r['segmentation_for_search']=r['segmentation_as_printed']
    final=[r for r in rows if r['segmentation_for_search'][-1]=='mīṉ']
    words={''.join(r['segmentation_for_search']) for r in rows}|{'mīṉ'}
    exact=search(words,{'mīṉ'})
    # Surface serialization of a straight sound-by-sign rendering of A's rules
    # has root in the middle:87+59+211 or globally211+59+87.
    direct=[s for s in exact if s['roof_operator'][0]!=s['ticks_operator'][0]]
    # Candidate link slots are only independently PRINTED one-consonant
    # components. Removing them is a charged morphological analysis.
    link_segments={'m','k','v'}
    stone={'kaṉ':'STONE','kal':'STONE','kallu':'STONE'}
    def underlying(row):
        parts=row['segmentation_for_search'][:-1]
        return tuple(stone.get(p,p) for p in parts if p not in link_segments)
    singles=collections.defaultdict(list)
    for r in final:
        u=underlying(r)
        if len(u)==1:singles[u[0]].append(r)
    triangles=[]
    for r in final:
        u=underlying(r)
        if len(u)!=2 or not all(x in singles for x in u):continue
        for first,second in itertools.product(singles[u[0]],singles[u[1]]):
            triangles.append({'modifier_keys':u,'double':r,'first':first,'second':second,
                'source_supported_lemma_relation':('STONE via DEDR1298 source brackets' if 'STONE' in u else None),
                'boundary_segment_analysis':'printed single m/k/v segments treated as candidate context-dependent linkers; no productive law asserted'})
    systems=[]
    for triangle in triangles:
        for swap in [False,True]:
            roof=triangle['second'] if swap else triangle['first']
            ticks=triangle['first'] if swap else triangle['second']
            sounds=lambda r:''.join(r['segmentation_for_search'])
            mapping={'59':'mīṉ','65':sounds(roof),'60':sounds(ticks),'66':sounds(triangle['double']),
                '87':('kal' if underlying(roof)[0]=='STONE' else underlying(roof)[0]),
                '211':('kal' if underlying(ticks)[0]=='STONE' else underlying(ticks)[0])}
            # The two modifiers must be gathered before canonical lexical
            # ordering; naive concatenation does not satisfy all three forms.
            system={'id':f'D-TAMIL-JOINT-{len(systems):02}',
                'mapping':mapping,'morphological_operations':{'87':'add ROOF modifier to fish expression',
                    '211':'add TICK modifier to fish expression','canonical_order':list(triangle['modifier_keys'])},
                'source_lexical_records':triangle,
                'repair_cost':{'fixed_modifier_order_rule':1,'link_segment_context_rules':1,
                    'stone_family_context_realization_rule':int('STONE' in triangle['modifier_keys'])},
                'strict_linear_phonetic_87_59_211':mapping['87']+mapping['59']+mapping['211'],
                'correctness_independently_scorable':False}
            system['four_spellings']=[{'stored_sequence':x,'executed_parse':decode_lattice(x,system)}
                for x in [['66'],['87','60'],['65','211'],['87','59','211']]]
            assert all(x['executed_parse'][0]['candidate_surface']==mapping['66'] for x in system['four_spellings'])
            duplicate=next((s for s in systems if s['mapping']==mapping),None)
            if duplicate is not None:
                duplicate.setdefault('alternative_source_lexical_records',[]).append(triangle)
            else:systems.append(system)
    ablations=[]
    for category in ['unrestricted','fish','star']:
        eligible=[r for r in final if category=='unrestricted' or category in r['compound_senses']]
        ablations.append({'semantic_prior':category,'lexical_rows':len(eligible),
            'distinct_qualifier_surfaces':len({''.join(r['segmentation_for_search'][:-1]) for r in eligible}),
            'qualifier_source_rows':[r['entry_id'] for r in eligible]})
    result={'source_path':str(source.relative_to(HERE.parents[3])),'source_claimed_counts':inventory['source_claimed_counts'],
        'source_rows':len(inventory['records']),'exact_eligible_rows':len(rows),
        'mīṉ_final_exact_rows':len(final),'uncertain_excluded':len(inventory['records'])-len(rows),
        'single_modifier_ablations':ablations,'exact_concatenative_two_modifier_systems':len(exact),
        'exact_concatenative_solutions':exact,'strict_linear_87_59_211_solutions':len(direct),
        'contextual_morphology_source_triangles':len(triangles),
        'distinct_lexical_surface_triangles':len({tuple(''.join(t[x]['segmentation_for_search']) for x in ['first','second','double']) for t in triangles}),
        'distinct_mixed_phonetic_systems':len(systems),'explicit_mixed_systems':systems,
        'not_independent_confirmation':'All spelling equality is a consequence of A operations and chosen lexical states. No source object is independently named stone/cock/fish, ghee/sky/star, or mīṉ.',
        'rivals':['87=two-long-stroke quantity in a context-specific counting construction;211 unknown nonphonetic operator',
            '87 and211 are anonymous classifiers on fish-like base, with no pronunciation',
            'roof and ticks are graphical distinctions not productive phonetic additions'],
        'scope':'Only59/65/60/66 lattice. Bases67/68/72/73 remain unread unless separately constrained.'}
    (HERE/'outputs/tamil_full_joint_search.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    # Explicit worked interpretations of the three observed common-prefix forms.
    witnesses={'66':['M77:7249:0','M77:7251:0','M77:7255:0','M77:7267:0','M77:7269:0'],
        '87-60':['M77:6211:0'],'87-59-211':['M77:1551:0']}
    obs=[json.loads(x) for x in (HERE.parent/'shared/observations.jsonl').read_text().splitlines()]
    obs_by_seq=collections.defaultdict(list)
    for row in obs:
        if row['strict']:obs_by_seq[tuple(row['tokens_stored'])].append(row)
    worked=[]
    for s in systems:
        for seq in [('267','99','66'),('267','99','87','60'),('267','99','87','59','211')]:
            worked.append({'candidate_id':s['id'],'original_sequence':seq,
                'source_rows':[{'row_id':r['row_id'],'source_record':r['source_record']} for r in obs_by_seq[seq]],
                'executed_parse':decode_lattice(seq,s),
                'unread_prefix':['267','99'],'candidate_reading':f"<M77:267> <M77:99> {s['mapping']['66']}",
                'phonetic_accuracy':None,'dependencies':['A roof87 rule','A ticks211 rule','Tamil lexical triangle',
                    'charged canonical modifier-order rule','charged contextual surface rules']})
    (HERE/'outputs/tamil_joint_worked_readings.json').write_text(json.dumps(worked,ensure_ascii=False,indent=2)+'\n')
    propagation=[]
    for s in systems:
        pair=[]
        for seq in [('65','70','211'),('87','59','71')]:
            pair.append({'source_sequence':seq,'source_rows':[r['row_id'] for r in obs_by_seq[seq]],
                'executed_parse':decode_lattice(seq,s)})
        strip=lambda parts:[{k:v for k,v in p.items() if k!='source_signs'} for p in parts]
        equal=strip(pair[0]['executed_parse'])==strip(pair[1]['executed_parse'])
        assert equal
        propagation.append({'candidate_id':s['id'],'parses':pair,
            'equal_abstract_readings':equal,'new_sound_value_for70':None,
            'meaning':'Joint operation predicts equivalent structure across new fish base; no new root pronunciation is forced.'})
    (HERE/'outputs/new_fish_family_propagation.json').write_text(json.dumps(propagation,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['exact_concatenative_solutions','explicit_mixed_systems']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
