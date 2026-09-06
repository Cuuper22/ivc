#!/usr/bin/env python3
"""Conditional roof/count/tick interaction: explicit scope and rival parses.

The graphic roof66->87,60 hypothesis comes from Route A's current inspection.
All source spellings below are independently read from the held corpus.
"""
import collections, json
from run_numerical_programs import load, row_ref, write, OUT

RULES=[(('65',),('87','59'),'roof_plain'),
       (('66',),('87','60'),'roof_marked'),
       (('60',),('59','211'),'tick_plain'),
       (('66',),('65','211'),'tick_roof')]

def successors(seq, duplicate=False):
    result=[]
    for source,target,name in RULES:
        for i in range(len(seq)-len(source)+1):
            if seq[i:i+len(source)]==source:result.append((seq[:i]+target+seq[i+len(source):],name))
    if duplicate:
        for i in range(len(seq)-1):
            if seq[i]=='87' and seq[i+1] in {'59','60','65','66'}:
                result.append((seq[:i]+(seq[i+1],seq[i+1])+seq[i+2:],'87_duplicates_next_glyph'))
    return result

def normal_forms(seq,duplicate):
    todo=[(seq,[])];seen=set();final={}
    while todo:
        s,path=todo.pop()
        if s in seen:continue
        seen.add(s);ss=successors(s,duplicate)
        if not ss:final[s]=path
        else:todo.extend((t,path+[name]) for t,name in ss)
    return [{'normal_form_stored':s,'one_derivation':p} for s,p in sorted(final.items())]

def scoped_field(seq):
    """Explicit alternative: Q scopes over the contiguous fish field once.

    Bare fish=one written item; roof=two items;87=factor2;Q=one field tag.
    Multiple adjacent fish items are added only inside this declared fish field.
    This is a conditional grammar, not inferred referential or metrical equality.
    """
    seq=list(seq);quantity=0;tags=0;i=0;unknown=[];components=[]
    atom={'59':(1,0),'60':(1,1),'65':(2,0),'66':(2,1)}
    while i<len(seq):
        factor=1
        if seq[i]=='87' and i+1<len(seq) and seq[i+1] in atom:factor=2;i+=1
        t=seq[i]
        if t in atom:
            n,q=atom[t];quantity+=factor*n;tags+=q
            components.append({'glyph':t,'factor':factor,'written_base_items':factor*n,'intrinsic_Q':q})
        elif t=='211':tags+=1
        else:unknown.append(t)
        i+=1
    return {'base':'59','written_base_items':quantity,'Q_count':tags,'unknown_tokens':unknown,
            'components':components,'semantic_quantity':None,
            'role_warning':'Written repetition cardinality is not automatically an amount, grammatical number, or physical measure.'}

def main(rows=None, emit=True):
    rows=load() if rows is None else rows
    byseq=collections.defaultdict(list)
    for r in rows:
        if r['strict']=='1':byseq[r['seq']].append(row_ref(r))
    roofpairs=[]
    for s,refs in byseq.items():
        for t,rule in successors(s):
            if rule.startswith('roof') and t in byseq:
                roofpairs.append({'rule':rule,'source_stored':s,'target_stored':t,
                    'source_rows':refs,'target_rows':byseq[t],
                    'literal_duplication_normal_forms':normal_forms(s,True),
                    'expanded_string_observation_status':[
                        {'normal_form_stored':x['normal_form_stored'],
                         'status':'observed' if tuple(x['normal_form_stored']) in byseq else 'unknown_unobserved_not_negative',
                         'source_rows':byseq.get(tuple(x['normal_form_stored']),[])} for x in normal_forms(s,True)]})
    fields=[('66',),('87','60'),('87','59','211'),('59','59','211'),('65','59','211'),('104','59','211')]
    network=[]
    for field in fields:
        seq=('267','99')+field
        network.append({'stored_sequence':seq,'sources':byseq.get(seq,[]),
            'orthographic_normal_forms_without_numeric_duplication':normal_forms(field,False),
            'literal_glyph_duplication_normal_forms':normal_forms(field,True),
            'field_scoped_Q_program':scoped_field(field)})
    result={'status':'conditional candidate interaction; no equivalence promoted',
        'namespace':'Mahadevan1977','source_base':'repository_root',
        'source_paths':['research/data/mahadevan_20260905/concordance_rows.csv'],
        'prerequisites':['A roof65->87,59','A proposed roof66->87,60','A tick60->59,211 and66->65,211',
            'C proposed87 duplication or factor2','Within-field scope and same-referent assumptions remain hypotheses'],
        'exact_roof_pairs':roofpairs,'fish_frame_network':network,
        'scope_diamond':{'start':['66'],'orthographic_normal_forms':normal_forms(('66',),False),
            'with_literal_glyph_duplication':normal_forms(('66',),True),
            'conclusion':'Without duplication the four spelling rules have one normal form 87,59,211. Literal 87 duplicates a following marked glyph and creates two distinct terminal strings:59,59,211 versus59,211,59,211. The naive unique-normal-form program is therefore not confluent; this alone does not prove different meanings. A Q operator scoped over the count field repairs this conditional confluence failure; numerical meaning is not thereby established.'},
        'rival65_warning':'Under roof65=two written59, the observed65,59,211 has three written base items if adjacent atoms are grouped. It cannot also be treated as an arbitrary alternative marker for the same two-item field without a new boundary/meaning rule.',
        'rival104_warning':'104,59,211 is observed in the same frame but104 has no assigned numerical value; contextual fit alone cannot equate it.',
        'categorical_rival':{'program':'TreatR andQ as commuting field features. SpellR asroof or87; spellQ asticks or211. The one repeated59 form can be an alternate spelling ofR in this local frame.',
            'same_core_observed_spelling_predictions':True,
            'arithmetic_extra_assumptions':['R denotes multiplication by2 in quantity rather than a conventional orthographic/category operation.','Adjacent59 atoms share the same counted referent.','Q preserves the counted unit and is field-scoped.'],
            'identifiability':'The available core does not force a numerical reading over the equally scoped categorical writing operation.'},
        'next_discriminating_predictions':[
            'The other two exact roof65/87,59 contexts conditionally predict repeated59,59 spellings; no such full-string witness is currently present, so these are unknown rather than failures.',
            'An existing independently linked87,60 versus59,211,59,211 or59,59,211 pair would discriminate literal-glyph from field-scoped duplication.',
            'A count change2->3 or a second repeated base with the same scope would discriminate productive arithmetic from the local categoricalR convention.'],
        'prior_exposure':'Retrospective integration of previously examined corpus and currentA hypotheses; no blind test.'}
    write('roof_count_scope_programs.json',result)
    candidates=json.loads((OUT/'candidates.json').read_text())
    candidates=[x for x in candidates if x['id']!='C_ROOF_COUNT_SCOPE']
    candidates.append({'id':'C_ROOF_COUNT_SCOPE','route':'C','status':'conditional','claim_type':'operational_meaning',
        'rule':'Treat roof/prefix87 as a factor2 over a fish field and ticks/suffix211 as a field-scoped operatorQ. Compare literal glyph duplication and an anonymous categoricalR/Q spelling grammar.',
        'namespace':'Mahadevan1977','context':'Four exact roof pairs and six observed267–99 fish-frame spellings.',
        'prerequisites':result['prerequisites'],
        'support':['The four orthographic rewrites converge at87,59,211. Four core spellings permit the same field features:two written59 items andoneQ.'],
        'contradictions':['Literal87 glyph duplication makes the roof/tick diamond nonconfluent:59,59,211 versus59,211,59,211.',
            'Treating same-frame65,59,211 as the same two-item record also conflicts with roof65 contributingtwo written items unless a new boundary or meaning rule is supplied.',
            'New paired roof witnesses4493 and4556 have cup counts4 and2; equal-face fixed-unit scalar models contradict their assumed front equivalence.'],
        'alternatives':['Commuting categoricalR/Q writing operations','Different referents in superficially matching frames','A scope or boundary grammar that permits alternate literal normal forms'],
        'parameters':{'orthographic_rules':4,'numeric_factor':2,'field_scope_rule':1},
        'complexity':'Factor2 and common counted referent are additional semantic assumptions over the anonymous categorical operation; no likelihood advantage has been established.',
        'predictions':result['next_discriminating_predictions'],
        'source_base':'repository_root',
        'source_paths':['research/campaigns/integrated_20260906/route_c/roof_count_scope_programs.json',
            'research/data/mahadevan_20260905/concordance_rows.csv'],
        'prior_exposure':result['prior_exposure']})
    write('candidates.json',candidates)
    summary={'exact_roof_pairs':len(roofpairs),'core_spellings_with_witnesses':sum(bool(x['sources']) for x in network),
        'orthographic_normal_forms':len(result['scope_diamond']['orthographic_normal_forms']),
        'literal_duplication_normal_forms':len(result['scope_diamond']['with_literal_glyph_duplication'])}
    if emit:print(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':main()
