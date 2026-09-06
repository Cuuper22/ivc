#!/usr/bin/env python3
"""Bounded source-witness stratification of A's roof/tick composition.

No motif-model refit. Metadata are explanatory rivals, never independent
confirmations of the source text used to select these expressions.
"""
from __future__ import annotations
import collections as co
import itertools as it
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'shared'))
from foundation import load_observations,stable

def site(oid):
    n=int(oid.split(':')[-1])
    return 'Mohenjo-daro' if n<4000 else 'Harappa' if n<6000 else 'Chanhudaro' if n<7000 else 'Lothal' if n<8000 else 'Kalibangan' if n<9000 else 'Other/West Asia'

def main():
    rows=load_observations();byseq=co.defaultdict(list);objects=co.defaultdict(list);faces=co.defaultdict(list)
    for r in rows:
        objects[r['object_id']].append(r);faces[(r['object_id'],r['face_code'])].append(r)
        if r['strict']:byseq[tuple(r['tokens_stored'])].append(r)
    def witness(r):
        raw=r['raw_fields'];rs=objects[r['object_id']]
        return {'row_id':r['row_id'],'object_id':r['object_id'],'sequence_stored':r['tokens_stored'],
          'site':site(r['object_id']),'object_class_raw':raw['inscobj'],
          'object_class_label':{'1':'seal','2':'sealing','3':'miniature tablet','4':'pottery','5':'copper tablet','7':'ivory/bone rod'}.get(raw['inscobj'],raw['inscobj']),
          'locus_raw':raw['locus'],'level_raw':raw['level'],'direction_raw':raw['dir'],'face_raw_fs80':raw['fs80'],
          'complete_single_line_face':len(faces[(r['object_id'],r['face_code'])])==1,
          'other_observations':[{'row_id':x['row_id'],'tokens_stored':x['tokens_stored'],'strict':x['strict'],
            'raw_fs80':x['raw_fields']['fs80']} for x in rs if x['row_id']!=r['row_id']],
          'exact_whole_object_text_key':stable([(x['face_code'],x['line_code'],x['tokens_stored']) for x in sorted(rs,key=lambda z:(z['face_code'],z['line_code']))]),
          'source_record':r['source_record']}
    declared=[
      ('roof87_frame348',('65','348','342'),('87','59','348','342'),'roof65→87–59; defining exact frame'),
      ('roof87_frame48',('65','48','342'),('87','59','48','342'),'roof65→87–59; defining exact frame'),
      ('tick211_frame171',('171','60'),('171','59','211'),'tick60→59–211; defining exact frame'),
      ('tick211_frame2679987',('267','99','87','60'),('267','99','87','59','211'),'tick60→59–211; defining exact frame'),
      ('roof87_marked_transfer',('267','99','66'),('267','99','87','60'),'implied roof66→87–60; marked-family transfer'),
      ('joint_base70_transfer',('65','70','211'),('87','59','71'),'joint roof65→87–59 and tick71→70–211; same proposed normal form'),
      ('roof102_rival_frame162',('65','249','162','342'),('102','59','249','162','342'),'alternative roof65→102–59'),
      ('roof102_rival_frame169',('65','249','169','342'),('102','59','249','169','342'),'alternative roof65→102–59')]
    results=[]
    for id,a,b,role in declared:
        aa=[witness(r) for r in byseq[a]];bb=[witness(r) for r in byseq[b]]
        comparisons=[]
        for x,y in it.product(aa,bb):
            comparisons.append({'left_row_id':x['row_id'],'right_row_id':y['row_id'],
              'same_site':x['site']==y['site'],
              'same_medium':x['object_class_raw']==y['object_class_raw'],
              'same_site_medium':(x['site'],x['object_class_raw'])==(y['site'],y['object_class_raw']),
              'same_site_locus':(x['site'],x['locus_raw'])==(y['site'],y['locus_raw']),
              'same_site_locus_known_level':(x['site'],x['locus_raw'],x['level_raw'])==(y['site'],y['locus_raw'],y['level_raw']) and x['level_raw']!='0',
              'same_catalogue_direction':x['direction_raw']==y['direction_raw'],
              'same_known_raw_picture':x['face_raw_fs80']==y['face_raw_fs80'] and x['face_raw_fs80'] not in (0,999,351),
              'same_site_medium_known_picture':(x['site'],x['object_class_raw'],x['face_raw_fs80'])==(y['site'],y['object_class_raw'],y['face_raw_fs80']) and x['face_raw_fs80'] not in (0,999,351)})
        results.append({'contrast_id':id,'candidate_operation':role,'left_sequence':a,'right_sequence':b,
          'left_witnesses':aa,'right_witnesses':bb,'comparisons':comparisons,
          'matched_masks_with_at_least_one_witness_pair':[k for k in comparisons[0] if k not in ('left_row_id','right_row_id') and any(z[k] for z in comparisons)],
          'independence':'one selected expression-pair contrast; object-pair cross-products are not independent replications'})
    lattice={
      'both_modifications_fused':('267','99','66'),
      'roof_expanded_tick_fused':('267','99','87','60'),
      'both_expanded':('267','99','87','59','211'),
      'repeated_fish_rival':('267','99','59','59','211')}
    lattice_rows=[]
    for form,seq in lattice.items():
        ww=[witness(r) for r in byseq[seq]]
        lattice_rows.append({'form':form,'sequence':seq,'witnesses':ww,
           'object_count':len({x['object_id'] for x in ww}),
           'whole_object_text_groups':len({x['exact_whole_object_text_key'] for x in ww}),
           'expression_type_count':1 if ww else 0,
           'site_medium_strata':sorted({(x['site'],x['object_class_label']) for x in ww})})
    out={'question':'Can observed site, medium, picture or production context explain A roof/tick composition?',
      'source_paths':['research/data/semantic_search_20260906/modifier_context_pairs.json',
        'research/campaigns/integrated_20260906/route_a/structured_alignments.json',
        'research/campaigns/integrated_20260906/shared/observations.jsonl'],
      'candidate_dependency':'A supplied operations and exact target sequences; these are not independently rediscovered semantic anchors.',
      'contrasts':results,'26799_construction':lattice_rows,
      'decisions':[
        {'hypothesis':'Roof87 spelling difference in its two original exact frames is independent of object medium.',
         'decision':'unsupported','reason':'Both original expanded forms are copper tablets; compact forms are seal/sealing. The closer2821/2906 pair shares locus31 and level−10 but differs medium.'},
        {'hypothesis':'Explicit roof87 occurs only on copper tablets.',
         'decision':'rejected_in_transfer','counterexamples':['M77:6211:0','M77:1551:0','M77:2452:0']},
        {'hypothesis':'The entire26799 composition is demonstrated within a fixed site.',
         'decision':'false','reason':'Fused, partly expanded, fully expanded and repeated-fish forms occupy Lothal, Chanhudaro, Mohenjo-daro and Harappa respectively.'},
        {'hypothesis':'Tick211 fusion is determined by city, broad medium or raw picture code.',
         'decision':'rejected_for_the171_frame','counterexample':['M77:1177:0','M77:3103:0'],
         'reason':'Both are Mohenjo-daro seals, direction1,raw picture13. Locus and level differ, leaving local production or phase confounding.'},
        {'hypothesis':'Joint roof/tick alternation is determined by site, broad medium or catalogue direction.',
         'decision':'rejected_for_the_base70_pair','counterexample':['M77:1380:0','M77:2452:0'],
         'reason':'Both are Mohenjo-daro seals,direction1; loci and levels differ. Raw pictures251 versus13 differ, so motif invariance is not supported.'},
        {'hypothesis':'The operation is proved semantic/grammatical rather than local production convention.',
         'decision':'underdetermined','reason':'There are no documented workshop identities. Coarse metadata explanations fail in selected contrasts, but locality/phase remains uncontrolled and matched orthography does not entail synonymy.'}],
      'scope':'Exact catalogue expressions; no free reversals, no line concatenation, no imputation of companion faces.',
      'prior_exposure':'Retrospective bounded adjudication of A-selected candidates. No classifier refit or new dataset.'}
    (HERE/'fish_composition_context.json').write_text(json.dumps(out,indent=2)+'\n')
    summary={'exact_contrasts':len(results),'same_site_medium_contrasts':[r['contrast_id'] for r in results if 'same_site_medium' in r['matched_masks_with_at_least_one_witness_pair']],
        'same_site_medium_picture_contrasts':[r['contrast_id'] for r in results if 'same_site_medium_known_picture' in r['matched_masks_with_at_least_one_witness_pair']],
        'lattice_expression_types':len(lattice_rows),'lattice_sites':[r['site_medium_strata'] for r in lattice_rows]}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
