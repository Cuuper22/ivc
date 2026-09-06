#!/usr/bin/env python3
"""Executed text-picture-text model competition on the frozen M77 evidence.

Raw fs80 categories are the targets. Their last digit is not decoded, and no
symbol code is translated into a word of the script. Every training observation
is a complete catalogue face; partial rows enter compatibility tests separately.
"""
from __future__ import annotations
import collections as co
import hashlib
import itertools as it
import json
import math
import os
from pathlib import Path
import sys

# Shared research container: avoid a BLAS thread pool per route agent.
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[variable]='1'

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SHARED=HERE.parent/'shared'
sys.path.insert(0,str(SHARED))
from foundation import load_observations, stable, task_partition, compatible

SOURCE='research/data/mahadevan_20260905/concordance_documents.json.gz'
EXPOSURE='Retrospective constrained search; source corpus and defining examples already exposed.'

def write(name,x):
    (HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')

def site(oid):
    n=int(oid.split(':')[-1])
    return 'Mohenjodaro' if n<4000 else 'Harappa' if n<6000 else 'Chanhudaro' if n<7000 else 'Lothal' if n<8000 else 'Kalibangan' if n<9000 else 'Other_or_West_Asia'

def face_key(f): return tuple(tuple(x) for x in f['lines'])
def features(f):
    result=set()
    for line in f['lines']:
        for n in (1,2,3):
            for i in range(len(line)-n+1):
                frag=tuple(line[i:i+n]);result.add(('any',frag))
                if i==0:result.add(('initial',frag))
                if i+n==len(line):result.add(('terminal',frag))
    return result

def evidence(f):
    return {k:f[k] for k in ('face_id','object_id','row_ids','lines','strict','raw_fs80','medium','locus','level')}

def load():
    rows=load_observations(); objects=co.defaultdict(list); rr=co.defaultdict(list)
    for row in rows:rr[(row['object_id'],row['face_code'])].append(row)
    faces=[]
    for (oid,fc),rs in sorted(rr.items()):
        rs.sort(key=lambda r:r['line_code'])
        f={'face_id':f'{oid}:face{fc}','object_id':oid,'face_code':fc,
           'row_ids':[r['row_id'] for r in rs],
           'lines':[r['tokens_stored'] for r in rs if r['tokens_stored']],
           'all_rows':[r['tokens_stored'] for r in rs],
           'strict':bool(any(r['tokens_stored'] for r in rs)) and all(r['strict'] for r in rs if r['tokens_stored']),
           'partial':any(r['tokens_stored'] and not r['strict'] for r in rs),
           'raw_fs80':sorted({int(r['raw_fields']['fs80']) for r in rs}),
           'medium':rs[0]['raw_fields']['inscobj'],'site':site(oid),
           'locus':rs[0]['raw_fields']['locus'],'level':rs[0]['raw_fields']['level'],
           'directions':[r['direction_code_raw'] for r in rs],
           'source_record_refs':[r['source_record'] for r in rs]}
        faces.append(f);objects[oid].append(f)
    return rows,faces,objects

def network(faces,objects):
    """A typed hypergraph; repeated text edges do not assert physical identity."""
    text_groups=co.defaultdict(list);motif_groups=co.defaultdict(list);pairs=[]
    for f in faces:
        if f['strict']:text_groups[face_key(f)].append(f)
        for fs in f['raw_fs80']:
            if fs not in (0,999):motif_groups[fs].append(f['face_id'])
    short_long=[]
    for oid,ff in objects.items():
        for a,b in it.combinations(ff,2):
            pairs.append({'object_id':oid,'faces':[a['face_id'],b['face_id']],'relation':'same_object_distinct_faces'})
            if not a['strict'] or not b['strict']:continue
            if sum(map(len,a['lines']))>sum(map(len,b['lines'])):a,b=b,a
            if sum(map(len,a['lines']))<=2 and sum(map(len,b['lines']))>sum(map(len,a['lines'])):
                short_long.append({'short':evidence(a),'long':evidence(b),'relation':'paired_short_long_not_equivalence'})
    repeated=[]
    for seq,ff in text_groups.items():
        motifs=co.defaultdict(set)
        for f in ff:
            for fs in f['raw_fs80']:
                if fs not in (0,999):motifs[fs].add(f['object_id'])
        if len(motifs)>1:
            repeated.append({'lines':seq,'raw_motifs':{k:sorted(v) for k,v in motifs.items()},'faces':[f['face_id'] for f in ff]})
    copper_edges=[]
    for oid,ff in objects.items():
        if ff[0]['medium']!='5':continue
        for a in ff:
            if not a['lines']:continue
            for b in ff:
                for fs in b['raw_fs80']:
                    if fs not in (0,999):
                        copper_edges.append({'text':evidence(a),'motif_face_id':b['face_id'],'raw_fs80':fs,
                                             'same_face':a['face_id']==b['face_id']})
    write('correspondence_network.json',{
        'source':SOURCE,'face_nodes':[evidence(f)|{'directions':f['directions'],'source_record_refs':f['source_record_refs']} for f in faces],
        'same_object_edges':pairs,
        'repeated_complete_face_text_groups':[{'lines':s,'face_ids':[f['face_id'] for f in ff]} for s,ff in text_groups.items() if len(ff)>1],
        'repeated_raw_motif_groups':[{'raw_fs80':fs,'face_ids':ff} for fs,ff in motif_groups.items() if len(ff)>1],
        'identity_policy':'same object keyed M77; other catalogues not added; repeated complete strings are grouped expressions, not proved matrix copies',
        'multiline_policy':'line lists retained; no cross-line adjacency; whole faces required for strict fits'})
    write('short_long_relations.json',short_long)
    write('same_text_different_picture.json',repeated)
    write('copper_correspondences.json',copper_edges)
    return text_groups,short_long,copper_edges,{'faces':len(faces),'strict_faces':sum(f['strict'] for f in faces),
        'strict_multiline_faces':sum(f['strict'] and len(f['lines'])>1 for f in faces),
        'same_object_face_pairs':len(pairs),'short_long_object_pairs':len(short_long),
        'distinct_short_long_pairs':len({(face_key(x['short']),face_key(x['long'])) for x in short_long}),
        'same_complete_text_different_raw_motif_groups':len(repeated),
        'copper_objects':sum(ff[0]['medium']=='5' for ff in objects.values()),'copper_text_picture_edges':len(copper_edges)}

def copper_models(edges,short_long):
    strict=[e for e in edges if e['text']['strict']]
    types={ (face_key(e['text']),e['raw_fs80']):e for e in strict }
    bytext=co.defaultdict(set);bymotif=co.defaultdict(set)
    for (s,fs),e in types.items():bytext[s].add(fs);bymotif[fs].add(s)
    # Bidirectionally injective referent model needs a matching; a classifier
    # allows multiple strings to denote the same picture category.
    from scipy.optimize import linear_sum_assignment
    import numpy as np
    ss=list(bytext); mm=list(bymotif);matrix=np.zeros((len(ss),len(mm)))
    for i,s in enumerate(ss):
        for j,m in enumerate(mm):matrix[i,j]=float(m in bytext[s])
    aa,bb=linear_sum_assignment(-matrix)
    maximum_bijection=int(matrix[aa,bb].sum())
    conflicts=[{'lines':s,'raw_fs80':sorted(fs),'witnesses':[e for (x,m),e in types.items() if x==s]} for s,fs in bytext.items() if len(fs)>1]
    shortmap=co.defaultdict(dict)
    for r in short_long:
        if r['short']['medium']=='5':shortmap[face_key(r['short'])][face_key(r['long'])]=r
    connected=[]
    for sh,longs in shortmap.items():
        pictures={fs for lo in longs for fs in bytext[lo]}
        connected.append({'short_lines':sh,'long_lines':list(longs),'raw_picture_union':sorted(pictures),
                          'source_pairs':list(longs.values())})
    write('copper_referent_competition.json',{
        'strict_text_picture_objects':len({e['text']['object_id'] for e in strict}),
        'distinct_text_raw_picture_edges':len(types),'distinct_complete_text_faces':len(ss),'distinct_raw_picture_codes':len(mm),
        'one_to_one_referent_maximum_fit':maximum_bijection,
        'one_to_one_referent_minimum_exceptions':len(types)-maximum_bijection,
        'deterministic_text_to_picture_maximum_fit':len(ss),
        'deterministic_text_to_picture_minimum_exceptions':len(types)-len(ss),
        'same_text_different_picture':conflicts,'short_long_picture_bridges':connected,
        'rivals':{
            'literal_referent':'Complete text denotes exact pictured entity; multiple raw picture codes may still be graphical variants, so exceptions at raw-code resolution are not automatic semantic contradictions.',
            'related_category':'Many texts and depictions allowed per shared broad category; category labels are unanchored.',
            'complementary_fields':'Text can encode a documentary component while picture marks a second category.',
            'production_context':'Latent production group emits both text family and picture; without documented independent production labels it can duplicate every categorical semantic likelihood.'},
        'identifiability':'Renaming each anonymous text/picture latent state to a workshop state leaves the observation likelihood and parameter count unchanged. This is an identifiability limit of these particular latent-category models, not a claim that historical production caused the pattern.',
        'prior_exposure':EXPOSURE})
    return types,bytext

def component_search(faces,objects):
    """Text component -> raw motif under exact-expression and context controls.

    Single-class observations with one complete longest face; the target motif
    is excluded from features. Copies collapse per expression, motif, site and
    medium. Multiline features never span a line boundary.
    """
    examples=[];dedup={}
    for oid,ff in objects.items():
        known={m for f in ff for m in f['raw_fs80'] if m not in (0,999) and m//10 not in (35,17,37,39,46,90,91,92,93)}
        usable=[f for f in ff if f['strict']]
        if len(known)!=1 or not usable:continue
        maximum=max(sum(map(len,f['lines'])) for f in usable)
        longest=[f for f in usable if sum(map(len,f['lines']))==maximum]
        if len(longest)!=1:continue
        f=longest[0];label=next(iter(known));key=(face_key(f),label,f['site'],f['medium'])
        if key in dedup:dedup[key]['object_ids'].append(oid);continue
        e={'lines':f['lines'],'row_ids':f['row_ids'],'object_ids':[oid],
           'label':label,'site':f['site'],'medium':f['medium'],'locus':f['locus'],
           'features':features(f),'textkey':stable(f['lines'])}
        dedup[key]=e;examples.append(e)
    bylabel=co.defaultdict(set)
    for e in examples:bylabel[e['label']].add(e['textkey'])
    # A category needs multiple independent expression families to be scored.
    examples=[e for e in examples if len(bylabel[e['label']])>=3]
    allfeatures=sorted(set().union(*(e['features'] for e in examples)))
    byfeature=co.defaultdict(list)
    for e in examples:
        for f in e['features']:byfeature[f].append(e)
    rankings=[]
    for feat,es in byfeature.items():
        # Count distinct expression/motif types; catalogue copies have no vote.
        counts=co.Counter({})
        for k,label in {(e['textkey'],e['label']) for e in es}:counts[label]+=1
        n=sum(counts.values())
        if n<3:continue
        label,count=counts.most_common(1)[0]
        rankings.append({'position':feat[0],'component':feat[1],'raw_motif':label,'support_expression_types':count,
                         'all_expression_motif_types':n,'purity':count/n,
                         'object_ids':sorted({o for e in es if e['label']==label for o in e['object_ids']}),
                         'counterexample_object_ids':sorted({o for e in es if e['label']!=label for o in e['object_ids']})})
    rankings.sort(key=lambda r:(-r['purity'],-r['support_expression_types'],len(r['component']),r['component']))
    write('component_motif_candidates.json',rankings)
    # Matched-flexibility models. Fixed regularization; no tuned winner per fold.
    import numpy as np
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression
    labels=sorted({e['label'] for e in examples});li={x:i for i,x in enumerate(labels)}
    yy=np.array([li[e['label']] for e in examples]);n=len(yy)
    feats=[]
    for mode in ('metadata','components','combined'):
        ds=[]
        for e in examples:
            d={'constant':1}
            if mode!='components':
                d.update({'site='+e['site']:1,'medium='+e['medium']:1,'site_medium='+e['site']+'_'+e['medium']:1})
            if mode!='metadata':
                d.update({p+':'+','.join(s):1 for p,s in e['features']})
            ds.append(d)
        vec=DictVectorizer();xx=vec.fit_transform(ds);feats.append((mode,xx))
    # Keep target exact text family together even where full object signatures differ.
    folds=np.array([int(e['textkey'][:12],16)%5 for e in examples])
    scores={}; predictions=[]; fitcost={}
    for mode,xx in feats:
        prob=np.zeros((n,len(labels)))
        parameters=[]
        for fold in range(5):
            test=folds==fold;train=~test
            # Also remove complete target objects; input uses one example per
            # object, but explicit set removal documents the permitted boundary.
            blocked={o for i,e in enumerate(examples) if test[i] for o in e['object_ids']}
            train &= np.array([not blocked.intersection(e['object_ids']) for e in examples])
            clf=LogisticRegression(C=0.2,max_iter=350,solver='lbfgs')
            clf.fit(xx[train],yy[train]);pred=clf.predict_proba(xx[test]);prob[np.ix_(test,clf.classes_)]=pred
            parameters.append(int(clf.coef_.size+clf.intercept_.size))
        true=prob[np.arange(n),yy]
        scores[mode]={'observed_target_types':n,'correct':int((prob.argmax(axis=1)==yy).sum()),
                     'log_loss_bits':float(-np.log2(np.maximum(true,1e-12)).sum()),
                     'mean_log_loss_bits':float(-np.log2(np.maximum(true,1e-12)).mean()),
                     'nominal_parameters_per_fold':parameters,
                     'parameter_penalty_bits_per_fold':[p*math.log2(n)/2 for p in parameters],
                     'penalty_status':'BIC-style nominal upper complexity accounting; shrinkage effective dimension not claimed'}
        for i,e in enumerate(examples):
            predictions.append({'model':mode,'object_ids':e['object_ids'],'row_ids':e['row_ids'],'lines':e['lines'],
                'actual_raw_fs80':e['label'],'predicted_raw_fs80':labels[int(prob[i].argmax())],
                'actual_probability':float(true[i]),'fold':int(folds[i]),'family_key':e['textkey']})
    write('motif_prediction_comparison.json',{'scores':scores,'classes':labels,
        'evaluation':'recombination: exact complete face expression held out; repeated copies collapsed by expression/motif/site/medium; one longest face per object; all other faces hidden',
        'permitted_inputs':'sign presence, within-line 1..3-sign components and their initial/terminal position; site and medium where selected',
        'not_established':'Predictive information about a raw motif code does not identify a sign meaning or distinguish a latent workshop category.',
        'prior_exposure':EXPOSURE})
    write('motif_prediction_records.json',predictions)
    return scores,rankings

def candidate(id,status,typ,rule,context,support,contradictions,prerequisites,alternatives,predictions,parameters=0,complexity=None):
    return {'id':id,'route':'B','status':status,'claim_type':typ,'rule':rule,'namespace':'Mahadevan1977',
            'context':context,'prerequisites':prerequisites,'support':support,'contradictions':contradictions,
            'alternatives':alternatives,'parameters':parameters,'complexity':complexity or {'lookup_entries':parameters},
            'predictions':predictions,'source_paths':[SOURCE,'research/campaigns/integrated_20260906/shared/observations.jsonl'], 'prior_exposure':EXPOSURE}

def published_typology():
    """Directly inspected Fig1a/b; typological reconstructions, not new objects.

    Counts are author-reported catalogued copies; each type gets one vote in the
    model comparison. Shape is A/B/C only: full type IDs also encode text/motif
    and therefore cannot be used as independent contextual predictors.
    """
    counts={'A1a':6,'A1b':1,'A2':6,'A3a':3,'A3b':1,'A4':2,'A5':3,'A6':1,'A7':3,'A8':1,'A9':4,'A10':1,'A11':2,
       'B1':8,'B2':1,'B3':2,'B4':9,'B5':2,'B6':16,'B7':14,'B8':8,'B9':5,'B10':1,'B11':28,'B12':1,'B13':8,'B14':2,
       'B15a':4,'B15b':2,'B16':5,'B17a':6,'B17b':3,'B18':5,'B19':14,
       'C1':3,'C2':2,'C3':3,'C4a':6,'C4b':1,'C5a':9,'C5b':2,'C6':7,'C7':1,'C8':3,'C9':1,'C10':1}
    motif={'A1a':'backward-looking deer','A1b':'backward-looking deer','A2':'composite deer with human face and buffalo horns',
      'A3a':'endless-knot motif','A3b':'endless-knot motif','B1':'unicorn with manger','B2':'zebu with manger','B3':'zebu with manger',
      'B4':'water buffalo with manger','B5':'rhinoceros with manger','B6':'elephant with manger','B7':'hare with bush',
      'B8':'markhor-like goat or composite animal','B9':'markhor-like goat or composite animal','B10':'composite animal with opposed foreparts',
      'B11':'composite markhor-horned animal','B12':'zebu-horned tiger','B13':'composite zebu-horned tiger/buffalo',
      'B14':'composite zebu-horned elephant/rhinoceros','B15a':'composite dog/rhinoceros with urus horns',
      'B15b':'composite dog/rhinoceros with urus horns','B16':'composite dog/rhinoceros with urus horns',
      'B17a':'composite camel/rhinoceros with snake tail','B17b':'composite camel/rhinoceros with snake tail',
      'B18':'composite camel/rhinoceros with snake tail','B19':'horned anthropomorphic archer','C1':'shield or double-axe motif'}
    nodes=[]
    for tid,n in counts.items():
        channel='unknown' if tid in ('A8','C10') else 'mixed_text_picture' if tid=='B12' else 'picture' if tid in motif else 'text'
        nodes.append({'type_id':'Parpola2008:'+tid,'shape_class':tid[0],
            'author_reported_object_count':n,'reverse_channel':channel,
            'motif_description':motif.get(tid),'motif_description_status':'published iconographic interpretation; species alternatives retained',
            'reconstruction_status':'typological reconstruction from multiple objects; broken-line elements tentative',
            'extra_obverse_line':tid in ('A3b','B15b','B17b'),'extra_reverse_line':tid in ('A1b','B12'),
            'orientation_variant':tid in ('C4b','C5b'),
            'source_pdf_index':2 if tid.startswith('A') or tid in ['B'+str(i) for i in range(1,12)] else 3})
    exact_links=[('A2','C4a'),('A2','C4b'),('B1','C1'),('B5','A11'),('B7','C2'),('B9','C5a'),('B9','C5b'),('B10','A7'),('B19','C6')]
    relations=[{'a':a,'b':b,'relation':'published_shared_long_obverse_text',
                'interpretation':'reverse picture and reverse text are alternants paired with a common long field; no synonymy asserted'} for a,b in exact_links]
    relations.append({'a':'B6','b':'B12','relation':'published_obverse_B6_equals_reverse_text_B12',
        'different_pictures':['elephant','horned tiger'],'same_face_text_and_picture_on_B12':True})
    for a,b in [('A1a','A1b'),('A3a','A3b'),('B2','B3'),('B8','B9'),('B15a','B15b'),('B15a','B16'),('B17a','B17b'),('B17a','B18')]:
        relations.append({'a':a,'b':b,'relation':'published_shared_motif_with_different_or_extended_text'})
    relations.append({'a':'C5a','b':'C6','relation':'published_shared_short_pictogram','notes':'links markhor-associated B9 and archer-associated B19; paper pp135–136 explicitly discusses it'})
    known=[x for x in nodes if x['reverse_channel']!='unknown']
    expected={'A':'text','B':'picture','C':'text'}
    form_correct=sum(x['reverse_channel']==expected[x['shape_class']] for x in known)
    default=co.Counter(x['reverse_channel'] for x in known).most_common(1)[0]
    result={'source':'evidence_inventory/recovered/Parpola_2008_copper.pdf','source_sha256':hashlib.sha256((HERE.parent/'evidence_inventory/recovered/Parpola_2008_copper.pdf').read_bytes()).hexdigest(),
        'nodes':nodes,'relations':relations,'type_count':len(nodes),'published_object_total':sum(counts.values()),
        'independence':'46 reconstructed types; 217 reported copies are not 217 independent tests; no automatic join to M77 or CISI objects',
        'shape_only_reverse_channel_prediction':{'rule':expected,'known_types':len(known),'correct':form_correct,
            'constant_baseline_label':default[0],'constant_baseline_correct':default[1],
            'exceptions':[x['type_id'] for x in known if x['reverse_channel']!=expected[x['shape_class']]],
            'meaning':'Object shape helps explain whether the second field is pictured or written; this does not assign its referent or identify a workshop.',
            'scope':'source typology only; shape categories are independently defined by morphology, whereas full A1/B12/C5 labels cannot be predictors'},
        'prior_exposure':'Figures and author interpretation already used by previous campaign; source recovered by exact hash this campaign.'}
    write('published_copper_type_network.json',result)
    return {'published_copper_type_nodes':len(nodes),'published_copper_relation_edges':len(relations),
            'shape_reverse_channel_types_correct':form_correct,'shape_reverse_channel_types_scored':len(known)}

def decisive_tests(rows,faces,objects,types,bytext):
    singles={tuple(f['lines'][0]):f for f in faces if f['strict'] and len(f['lines'])==1}
    allseq=co.defaultdict(list)
    for f in faces:
        if f['strict']:allseq[face_key(f)].append(f)
    # Freeze one selected copper contrast and a simple transfer rule, then test
    # every other already-held occurrence. The result is retrospective, not blind.
    core=('204','245','358','342');base=('204','245','342')
    def motif_witnesses(seq,contains=False):
        out=[]
        for f in faces:
            if not f['strict']:continue
            hit=any(any(tuple(line[i:i+len(seq)])==seq for i in range(len(line)-len(seq)+1)) for line in f['lines']) if contains else face_key(f)==(seq,)
            if not hit:continue
            mot=[{'face_id':g['face_id'],'raw_fs80':m} for g in objects[f['object_id']] for m in g['raw_fs80'] if m not in (0,999)]
            out.append(evidence(f)|{'motifs':mot})
        return out
    discovery=[x for x in motif_witnesses(core) if x['medium']=='5']
    holdout=[x for x in motif_witnesses(core,True) if x['medium']!='5']
    standalone=[x for x in motif_witnesses(('358',),True) if x['medium']!='5' and x['motifs']]
    parts=task_partition(rows,{r for x in holdout for r in x['row_ids']})
    transfer={'candidate_id':'B-358-LITERAL','frozen_rule':'358 identifies the raw145/147 picture category in every containing construction; longer block204–245–358–342 retains that category under appended12.',
        'defining_complete_copper_objects':discovery,'noncopper_component_tests':standalone,'block_extension_tests':holdout,
        'target_partition':{k:v for k,v in parts.items() if k!='train_row_ids'},
        'result':'Universal component-to-picture and category-preserving block-extension predictions fail if these differing raw picture categories denote distinct referents. A textual designation could still be unrelated to the pictorial referent.',
        'unseen_family':'new constructions containing358, excluding complete copper core copies',
        'medium_transfer':'copper5 to seals1/sealings2; separate from within-medium fit',
        'raw_code_semantics':'145/147 and13 kept exact; interpretations of 14 vs01 require separate codebook grounding'}
    write('frozen_358_transfer.json',transfer)
    # Exact three-face contrasts retain doubtful signs; no concatenation or repair.
    triple=[]
    for ids in [('M77:4581','M77:4591'),('M77:3315','M77:3414'),('M77:2901','M77:3360','M77:3414')]:
        triple.append({'objects':[{'object_id':oid,'faces':[evidence(f) for f in objects[oid]]} for oid in ids]})
    write('decisive_object_contrasts.json',triple)
    # Find all insertion/deletion or replacement contrasts between complete faces
    # with a known object-level motif. This supplies semantic contributions
    # across nonidentical expressions, with no free line joins.
    d=co.defaultdict(list)
    for f in faces:
        if not f['strict'] or len(f['lines'])!=1:continue
        motifs={m for g in objects[f['object_id']] for m in g['raw_fs80'] if m not in (0,999)}
        if len(motifs)==1:d[tuple(f['lines'][0])].append((f,next(iter(motifs))))
    contrasts=[]
    ss=sorted(d)
    for i,a in enumerate(ss):
        if len(a)<2:continue
        for b in ss[i+1:]:
            if abs(len(a)-len(b))>1:continue
            matches=[]
            if len(a)==len(b):
                dif=[j for j,(x,y) in enumerate(zip(a,b)) if x!=y]
                if len(dif)==1:matches=[{'operation':'replace','position':dif[0],'left':a[dif[0]],'right':b[dif[0]]}]
            else:
                short,long=(a,b) if len(a)<len(b) else (b,a)
                matches=[{'operation':'insert','position':j,'left':None,'right':long[j]} for j in range(len(long)) if long[:j]+long[j+1:]==short]
            if not matches:continue
            matched=[]
            for fa,ma in d[a]:
                for fb,mb in d[b]:
                    if fa['object_id']==fb['object_id']:continue
                    if (fa['site'],fa['medium'])==(fb['site'],fb['medium']):
                        matched.append({'a':fa['face_id'],'b':fb['face_id'],'raw_motifs':[ma,mb],
                            'same_locus':fa['locus']==fb['locus'],'same_level':fa['level']==fb['level']})
            if matched:contrasts.append({'left':a,'right':b,'alignments':matches,
                'matched_site_medium_object_pairs':matched,
                'distinct_raw_motif_pairs':sorted({tuple(z['raw_motifs']) for z in matched}),
                'unit':'one expression-pair contrast; number of catalogue objects is not independent replication'})
    write('matched_component_contrasts.json',contrasts)
    cands=[
      candidate('B-COFACE-363','underdetermined','structural_constraint',
        'The short363 is paired with two long expression families. Their picture-linked copies involve different raw codes139 and520; do not equate each pairing with a specific pictured referent.',
        'Copper tablets; whole faces; exact catalogue readings',
        ['M77:2901:10','M77:2901:20','M77:3360:10','M77:3360:20','M77:3414:10','M77:3414:20','M77:3373:10','M77:3373:29','M77:2914:10','M77:2914:29'],[],
        ['Catalogue distinction362/363','Paired faces correctly assigned','Raw motif families139 and520 actually pictorially distinct'],
        ['Broad shared referent','Shared category or authority plus variable description','Production grouping','One questionable catalogue short sign'],
        ['A universal363=one specific depicted species predicts equal species across the two long families and fails under distinct-species decoding.'],2),
      candidate('B-358-LITERAL','rejected','lexical_meaning',
        'Universal358=the copper145/147 pictorial category, preserved in every construction.',
        'All containing inscriptions, including copper-to-seal transfer',
        [r for x in discovery for r in x['row_ids']],
        [r for x in standalone for r in x['row_ids']],
        ['Direct literal text-picture relation','145/147 represent a common category distinct from13'],
        ['Copper-specific label','Documentary field unrelated to animal','Same designation accompanied by different emblems'],
        [{'target':'M77:7244:0','predicted_raw_fs80':[145,147],'observed_raw_fs80':13}],1),
      candidate('B-LATENT-CATEGORY','underdetermined','structural_constraint',
        'A fitted anonymous category linking text families to pictures can be renamed as a production-group category with identical likelihood and parameter count.',
        'Latent categorical models with no independent documented production-group observations',
        ['copper_referent_competition.json'],[],[],
        ['Literal/category meaning','Production context','Complementary documentary fields'],
        ['An independent production indicator or transferable component relation is required to distinguish these particular rivals.'],0),
      candidate('B-COPPER-LITERAL-PICTURE','rejected','lexical_meaning',
        'Every complete copper text names exactly the animal species depicted on its object.',
        'Literal species model, not a broader deity/category designation',
        ['M77:3328:10','M77:3336:10','M77:3368:10'],
        ['M77:1704:20'],
        ['Literal species naming','Parpola2008 B6/B12 text identity and different pictorial species'],
        ['The same deity or category represented in multiple forms','Complementary fields','Production context'],
        [{'target':'M77:1704:20','text_stored':['336','89','296','342','98'],'predicted':'elephant','observed':'horned tiger; text appears on the same face as the animal'}],1),
      candidate('B-REPRESENTATION-CHANNEL','supported_scope_limited','structural_constraint',
        'In the published typology, shape classB predicts picture-only reverse, classesA/C text-only reverse:37 of44 legible reconstructed types fit; same long fields link alternative reverse channels.',
        'Parpola2008 reconstructed copper types only; descriptive contextual prediction, not new semantic decipherment',
        ['Parpola2008:A2','Parpola2008:C4a','Parpola2008:B5','Parpola2008:A11','Parpola2008:B19','Parpola2008:C6'],
        ['Parpola2008:A1a','Parpola2008:A1b','Parpola2008:A2','Parpola2008:A3a','Parpola2008:A3b','Parpola2008:B12','Parpola2008:C1'],
        ['Only shape-level A/B/C variables used; full type labels would leak text and pictures','Author reconstructed types correctly grouped'],
        ['Production conventions','Semantically related alternative representations','Complementary documentary fields'],
        [{'rule':{'A':'text','B':'picture','C':'text'},'correct_types':37,'scored_types':44,'constant_baseline_correct':26}],3),
      candidate('B-THREE-FIELDS','conditional','structural_constraint',
        'Objects4581 and4591 preserve the same four-stroke cup face and same doubtful middle expression while their short first faces differ137 versus59.',
        'Two three-faced miniature tablets; doubtful119 retained',
        ['M77:4581:10','M77:4581:20','M77:4581:30','M77:4591:10','M77:4591:20','M77:4591:30'],[],
        ['Doubtful middle119 does not conceal a semantic difference','Catalogue face assignments'],
        ['Complementary category selector','Two spellings','Distinct quantities with missing units','Production context'],
        ['Any deterministic middle+cup→short model needs an exception or another observed variable.'],0)]
    for c in cands:
        if c['id'] in ('B-COFACE-363','B-COPPER-LITERAL-PICTURE','B-REPRESENTATION-CHANNEL'):
            c['source_paths'].append('research/campaigns/integrated_20260906/evidence_inventory/recovered/Parpola_2008_copper.pdf')
    write('candidates.json',cands)
    write('semantic_anchors.json',{'lexical_anchors':[],'sound_anchors':[],
        'exclusions':[{'candidate_id':'B-358-LITERAL','exclude':'Unconditional literal category assignment358=ox-antelope from copper picture alone','counterexample':'M77:7244:0','scope':'under direct depiction hypothesis'}],
        'anonymous_relations':['B-COFACE-363','B-LATENT-CATEGORY','B-THREE-FIELDS'],
        'not_licensed':'No phonetic lexicon filtering by animal names; no blanket synonymy for paired faces.'})
    return {'matched_component_contrast_types':len(contrasts),'358_defining_complete_copper_objects':len(discovery),
            '358_non_copper_picture_bearing_constructions':len(standalone),'358_complete_block_extension_targets':len(holdout)}

def main():
    rows,faces,objects=load()
    tg,sl,ce,summary=network(faces,objects)
    types,bt=copper_models(ce,sl)
    summary.update(decisive_tests(rows,faces,objects,types,bt))
    summary.update(published_typology())
    scores,rankings=component_search(faces,objects)
    summary.update({'source_sha256':rows[0]['source_sha256'],'motif_scores':scores,
                    'component_candidates_with_three_expression_types':len(rankings),
                    'lexical_anchors_established':0,'phonetic_anchors_established':0,'prior_exposure':EXPOSURE})
    write('summary.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
