#!/usr/bin/env python3
"""Execute explicit conditional route exchanges on original held observations."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'shared'))
from common import load_rows,write,digest
from run_joint import A,C,module
D=module('Dexchange',HERE/'route_d/run_completion_d.py')

def main():
    rows=load_rows();count_models=json.loads((HERE/'route_c/program_search.json').read_text())
    counts=C.load_records()
    role_model=min((m for m in count_models if m['program'].get('field')=='fish_items'),key=lambda m:m['objective_bits'])
    independent=min((m for m in count_models if m['program']['kind']=='independent'),key=lambda m:m['objective_bits'])
    named=json.loads((HERE/'route_d/phonetic_alternatives.json').read_text())
    if isinstance(named,dict):named=list(named.values())
    models=[json.loads((HERE/'route_d'/f'{l}_{o}.json').read_text()) for l in ('tamil','sanskrit') for o in ('append','prepend')]
    # Use an explicitly retained phonetic rival as well as the preferred mixed
    # model. No phonetic value or numeral interpretation is promoted.
    for m in named:
        if isinstance(m,dict) and 'language' in m:models.append(m)
    examples=[r for r in rows if r['object_id'] in ('M77:2275','M77:1008','M77:1380','M77:2452','M77:1147')]
    predictions=[]
    for m in models:
        frozen=digest(m)
        for r in examples:
            seq=A.transform(r['tokens_stored'],'roof87_tick211')
            roles={s:'numeric' for s in C.FISH}
            plain=D.decode(m,seq);conditioned=D.decode(m,seq,roles)
            predictions.append({'row_id':r['row_id'],'raw':r['tokens_stored'],'conditional_spelling':seq,'language':m['language'],'orientation':m['orientation'],'marker_role':m.get('marker_role'),'C_program':role_model['program'],'C_status':'conditional losing rival; fish marks as numerical items is not established','role_assignments':roles,'ordinary':plain,'C_conditioned':conditioned,'ordinary_lexical_prior_bits':D.lexical_residual_bits(m,seq),'conditioned_lexical_prior_bits':D.lexical_residual_bits(m,seq,roles),'unread_spans_preserved':True,'frozen_model_before':frozen,'frozen_model_after':digest(m)})
    source=json.loads((HERE/'sources/1380_2452_adjudication.json').read_text())
    result={'status':'executed_reconstructed_rerun','C_to_D':predictions,'C_role_model_train_objective':role_model['objective_bits'],'C_independent_train_objective':independent['objective_bits'],'changed_decodings':sum(p['ordinary']!=p['C_conditioned'] for p in predictions),'B_to_D':{'source':'sources/1380_2452_adjudication.json','universal_whole_expression_literal_species_allowed':False,'conditional_on':source['prerequisites'],'positive_lexical_anchors':[],'effect':'No whole-expression species anchor may be supplied as independent supervision. Fish-root dictionary hypotheses remain conditional, and are not whole-inscription translations.'},'A_to_C':{'execution':'joint/* candidate fits use original count targets conditioned on each candidate expanded front; role/field/operator alternatives remain in route_c/program_search.json'},'D_to_A':{'execution':'joint/linguistic_coupling/* optimizes shared spelling program under frozen conditional linguistic priors and scores raw held channels separately'},'evidence_counting':'These are alternative interpretations of shared observations, not additional independent confirmations.'}
    write(HERE/'cross_route_predictions.json',result)
    print({'C_to_D_executed':len(predictions),'changed_decodings':result['changed_decodings']})

if __name__=='__main__':main()
