#!/usr/bin/env python3
"""Executed Route C: neutral fields, relative-unit graphs, arithmetic prediction.

No new evidence. Mahadevan IDs only. Strict and partial views remain separate.
All evaluations are retrospective; none is an archaeological blind test.
"""
from __future__ import annotations
import argparse, collections, csv, fractions, hashlib, itertools, json, math, sys
from pathlib import Path

LONG = {"86": 1, "87": 2, "89": 3, "95": 4, "96": 5}
COUNT_SIGN = {v:k for k,v in LONG.items()}
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

def write(name, data):
    (OUT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n")

def row_ref(r):
    return {k:r[k] for k in ("index","textnum","sideline","inscobj","locus","level","dir","strict")} | {
        "stored_tokens":list(r["seq"]), "display_tokens":list(reversed(r["seq"])),
        "exclusion_reasons":r["exclusion_reasons"], "namespace":"Mahadevan1977",
        "row_id":f"M77:{r['textnum']}:{r['sideline']}","object_id":f"M77:{r['textnum']}"}

def load():
    rows=list(csv.DictReader((ROOT/'research/data/mahadevan_20260905/concordance_rows.csv').open()))
    for r in rows:
        r['seq']=tuple(r[f'S{i}'] for i in range(1,15) if r[f'S{i}'])
        r['face']=int(r['sideline'])//10 if int(r['sideline'])>=10 else None
    return rows

def neutral_observations(rows):
    obs=[]
    for r in rows:
        for i,t in enumerate(r['seq']):
            if t.lstrip('*') not in LONG: continue
            obs.append(row_ref(r)|{
                'stored_token_index':i, 'raw_sign':t,
                'graphical_group':'long_parallel_strokes',
                'visible_strokes_if_catalogue_reading_correct':LONG[t.lstrip('*')],
                'doubtful':t.startswith('*'),
                'neighbor_before':r['seq'][i-1] if i else None,
                'neighbor_after':r['seq'][i+1] if i+1<len(r['seq']) else None,
                'role_alternatives':['cardinal_quantity','ordered_category','nominal_category','other_sign'],
                'semantic_value':None})
    write('numerical_observations.json',obs)
    return obs

def parse_face(rr):
    """Preserve line boundaries; no concatenation, face order, or unknown=zero."""
    rr=sorted(rr,key=lambda r:int(r['sideline']))
    groups=[(j,i,LONG[t]) for j,r in enumerate(rr) for i,t in enumerate(r['seq']) if t in LONG]
    frame=tuple(tuple('N' if t in LONG else t for t in r['seq']) for r in rr)
    return {'sources':[row_ref(r) for r in rr], 'frame':frame,
            'groups':groups, 'count_sum':sum(g[2] for g in groups) if groups else None,
            'single_count':groups[0][2] if len(groups)==1 else None,
            'strict':all(r['strict']=='1' for r in rr),
            'cup':len(rr)==1 and len(rr[0]['seq'])==2 and rr[0]['seq'][0] in LONG and rr[0]['seq'][1]=='328',
            'line_count':len(rr), 'face':rr[0]['face']}

def record_fields(rows):
    byobj=collections.defaultdict(list)
    for r in rows: byobj[r['textnum']].append(r)
    objects=[]; qlinks=[]; cuplinks=[]
    for oid,rr in sorted(byobj.items()):
        facegroups=collections.defaultdict(list)
        for r in rr:
            if r['face'] is not None: facegroups[r['face']].append(r)
        faces=[parse_face(fr) for _,fr in sorted(facegroups.items())]
        if len(faces)<2: continue
        obj={'textnum':oid,'inscobj':rr[0]['inscobj'],'locus':rr[0]['locus'],'level':rr[0]['level'],
             'faces':faces, 'unassigned_rows':[row_ref(r) for r in rr if r['face'] is None]}
        objects.append(obj)
        for a,b in itertools.combinations(faces,2):
            if a['strict'] and b['strict'] and a['single_count'] is not None and b['single_count'] is not None:
                qlinks.append({'textnum':oid,'inscobj':obj['inscobj'],'locus':obj['locus'],'level':obj['level'],
                    'a':a,'b':b,'ratio_b_over_a_if_equal':str(fractions.Fraction(a['single_count'],b['single_count']))})
        for cup in (f for f in faces if f['cup'] and f['strict']):
            for other in faces:
                if other is cup: continue
                cuplinks.append({'textnum':oid,'inscobj':obj['inscobj'],'locus':obj['locus'],'level':obj['level'],
                  'observed_cup_count':cup['single_count'],'cup':cup,'other':other,
                  'other_faces':[f for f in faces if f is not cup and f is not other],
                  'strict_pair':other['strict'], 'has_third_face':len(faces)>2})
    write('linked_record_fields.json',objects)
    write('single_count_crossface_constraints.json',qlinks)
    write('cup_field_records.json',cuplinks)
    return objects,qlinks,cuplinks

def frame_key(face): return json.dumps(face['frame'],separators=(',',':'))

def unit_graph(links, conditioning):
    """Conditional equality is tested, never assumed as an observation.

    n_A U_A=n_B U_B; U_B/U_A=n_A/n_B. A free scale survives in each
    connected component. Edge contradictions survive repetition collapse.
    """
    adj=collections.defaultdict(list); unique={}
    for x in links:
        context=tuple(x[k] for k in conditioning)
        a=json.dumps((context,x['a']['frame']));b=json.dumps((context,x['b']['frame']))
        n=x['a']['single_count'];m=x['b']['single_count']
        key=(a,b,n,m)
        unique.setdefault(key,[]).append(x['textnum'])
    for (a,b,n,m),ids in unique.items():
        q=fractions.Fraction(n,m)
        adj[a].append((b,q,ids));adj[b].append((a,1/q,ids))
    values={};components=[];conflicts=[]
    for root in sorted(adj):
        if root in values:continue
        values[root]=fractions.Fraction(1);todo=[root];nodes=[];edges=set()
        while todo:
            a=todo.pop();nodes.append(a)
            for b,q,ids in adj[a]:
                edges.add((min(a,b),max(a,b),tuple(ids)))
                pred=values[a]*q
                if b not in values: values[b]=pred;todo.append(b)
                elif values[b]!=pred:
                    conflict={'a':a,'b':b,'objects':ids,'required_b_over_a':str(q),
                              'already_implied_b_over_a':str(values[b]/values[a])}
                    if a<=b: conflicts.append(conflict)
        components.append({'nodes':nodes,'node_count':len(nodes),'distinct_edge_groups':len(edges),
            'scale_degrees_of_freedom':1,
            'spanning_tree_ratios_not_a_solution_if_component_conflicted':{k:str(values[k]) for k in nodes}})
    return {'conditioning':conditioning,'observed_object_pairs':len(links),'unique_equations':len(unique),
            'descriptor_unit_parameters':len(adj),'components':components,'contradictions':conflicts,
            'absolute_unit_identifiable':False,
            'interpretation':'Even consistent ratios depend on equal-value and quantity-role hypotheses; a forest of once-used descriptor pairs cannot distinguish arithmetic from categorical lookup.'}

def templates(rows):
    frames=collections.defaultdict(list)
    for r in rows:
        if r['strict']!='1':continue
        g=[(i,LONG[t]) for i,t in enumerate(r['seq']) if t in LONG]
        if len(g)!=1:continue
        i,n=g[0];frame=r['seq'][:i]+('N',)+r['seq'][i+1:]
        frames[frame].append((n,r))
    result=[]
    for frame,rr in frames.items():
        counts=collections.defaultdict(list)
        for n,r in rr:counts[n].append(row_ref(r))
        result.append({'frame_stored':frame,'frame_display':list(reversed(frame)),
            'observed_counts':sorted(counts),'sources_by_count':dict(counts)})
    result.sort(key=lambda r:(-len(r['observed_counts']),r['frame_stored']))
    write('one_group_templates.json',result)
    return result

def editdist(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        nd=[i]
        for j,y in enumerate(b,1):nd.append(min(nd[-1]+1,d[j]+1,d[j-1]+(x!=y)))
        d=nd
    return d[-1]

def compression(rows):
    """Candidate n*x shorthand, allowing one separately charged context edit.
    Presence is positive evidence only. Absence is never a negative inscription.
    Permuted numerical labels diagnose whether graphic cardinal matching matters.
    """
    unique=collections.defaultdict(list)
    for r in rows:
        if r['strict']=='1':unique[r['seq']].append(row_ref(r))
    runs=[]
    for s,sources in unique.items():
        i=0
        while i<len(s):
            j=i+1
            while j<len(s) and s[j]==s[i]:j+=1
            if j-i>=2 and s[i] not in LONG:
                runs.append((s,i,j,sources))
            i=j
    # Context matching is held fixed while numerical-value labels are permuted.
    candidates=[]
    for s,i,j,sources in runs:
        base=s[i];n=j-i
        if n not in COUNT_SIGN:continue
        context=s[:i]+('X',)+s[j:]
        if len(context)-1<2:continue
        for t,tsources in unique.items():
            for k in range(len(t)-1):
                pair=t[k:k+2]
                if pair[0]==base and pair[1] in LONG: marker=pair[1];order='base_then_count_stored'
                elif pair[1]==base and pair[0] in LONG:marker=pair[0];order='count_then_base_stored'
                else:continue
                tc=t[:k]+('X',)+t[k+2:]
                d=editdist(context,tc)
                if d>1:continue
                candidates.append({'expanded_stored':s,'compressed_stored':t,'base':base,
                    'repeat_count':n,'marker':marker,'graphical_count':LONG[marker],
                    'cardinal_agrees':LONG[marker]==n,'context_edit_cost':d,'order':order,
                    'expanded_sources':sources,'compressed_sources':tsources})
    # Matched complete selection statistic across all five-number assignments.
    permutations=[]
    for vals in itertools.permutations(range(1,6)):
        mapping=dict(zip(LONG,vals))
        hits=[x for x in candidates if mapping[x['marker']]==x['repeat_count']]
        permutations.append({'mapping':mapping,'exact_hits':sum(x['context_edit_cost']==0 for x in hits),
            'all_hits':len(hits),'distinct_bases':len({x['base'] for x in hits})})
    write('repeat_compression_candidates.json',candidates)
    write('repeat_compression_label_controls.json',permutations)
    real=[x for x in candidates if x['cardinal_agrees']]
    return {'eligible_repeated_runs':len(runs),'candidate_alignments':len(candidates),
        'exact_cardinal_hits':sum(x['context_edit_cost']==0 for x in real),'cardinal_hits_with_one_edit':len(real),
        'cardinal_distinct_bases':len({x['base'] for x in real}),
        'permutations_tested':len(permutations),
        'permutations_at_least_as_many_hits':sum(p['all_hits']>=len(real) for p in permutations),
        'warning':'A repeat/marker match is not established equivalence. Same object or formula copies remain one observed alignment.'}

def soft(pred):
    z=[math.exp(-((k-pred)**2)/2) for k in range(1,6)];s=sum(z)
    return [v/s for v in z]

def cat_probs(values):
    c=collections.Counter(values);return [(c[i]+.5)/(len(values)+2.5) for i in range(1,6)]

def score(probs,y):return -math.log(max(probs[y-1],1e-12))

def train_model(train,name):
    if name=='nonnumerical_constant_three': return {'parameters':0,'a':0.,'b':3.}
    if name=='nonnumerical_fitted_constant':
        best=min((sum(score(soft(b),r['y']) for r in train),b) for b in [-4.,-3.,-2.,-1.,0.,1.,2.,3.,4.])
        return {'parameters':1,'a':0.,'b':best[1],'searched_programs':9}
    if name=='categorical_global': return {'parameters':4,'p':cat_probs([r['y'] for r in train])}
    if name in ('categorical_count','categorical_class_count','categorical_front'):
        keys={'categorical_count':lambda r:(r['x'],),'categorical_class_count':lambda r:(r['inscobj'],r['x']),
              'categorical_front':lambda r:(r['front'],)}
        groups=collections.defaultdict(list)
        for r in train:groups[keys[name](r)].append(r['y'])
        return {'parameters':4*len(groups),'groups':{k:cat_probs(v) for k,v in groups.items()},
                'fallback':cat_probs([r['y'] for r in train]),'key':keys[name]}
    if name=='arithmetic_equal':return {'parameters':0,'a':1.,'b':0.}
    aa=[.25,1/3,.5,1.,1.5,2.,3.,4.] if name=='arithmetic_multiplier' else [0.,.25,1/3,.5,1.,1.5,2.,3.,4.]
    bb=[0.] if name=='arithmetic_multiplier' else [-4.,-3.,-2.,-1.,0.,1.,2.,3.,4.]
    best=min(((sum(score(soft(a*r['x']+b),r['y']) for r in train),a,b) for a in aa for b in bb))
    return {'parameters':1 if name=='arithmetic_multiplier' else 2,'a':best[1],'b':best[2],
            'searched_programs':len(aa)*len(bb)}

def predict(m,r):
    if 'p' in m:return m['p']
    if 'groups' in m:return m['groups'].get(m['key'](r),m['fallback'])
    return soft(m['a']*r['x']+m['b'])

def prediction_evaluation(cuplinks):
    # Deduplicate exact paired face layouts, not approximate sign families.
    records={}
    for r in cuplinks:
        if not r['strict_pair'] or r['other']['single_count'] is None or r['other']['cup']:continue
        front=frame_key(r['other']);raw=json.dumps([x['stored_tokens'] for x in r['other']['sources']])
        key=(raw,r['observed_cup_count'],r['inscobj'])
        records.setdefault(key,{'x':r['other']['single_count'],'y':r['observed_cup_count'],
            'front':front,'raw_front':raw,'inscobj':r['inscobj'],'sources':[]})['sources'].append(r['textnum'])
    data=list(records.values());write('prediction_records.json',data)
    names=['nonnumerical_constant_three','nonnumerical_fitted_constant','arithmetic_equal','arithmetic_multiplier','arithmetic_affine','categorical_global',
           'categorical_count','categorical_class_count','categorical_front']
    results=[]; predictions=[]
    for name in names:
        full=train_model(data,name)
        ll=sum(score(predict(full,r),r['y']) for r in data)
        result={'program':name,'observations':len(data),'parameters':full['parameters'],
            'fit_nll_nats':ll,'approximate_bic_sensitivity_nats':ll+.5*full['parameters']*math.log(max(len(data),2)),
            'complexity_warning':'Approximate NLL+k*log(n)/2 sensitivity only; finite grid/rule selection costs are not a matched MDL code. No promotion uses this score.'}
        if 'a' in full:result|={'a':full['a'],'b':full['b']}
        if name=='arithmetic_affine' and full['a']==0:result['interpretation']='Fitted slope zero: input-independent smooth category prediction, no inferred arithmetic relation.'
        if name=='nonnumerical_constant_three':result['interpretation']='Post-hoc fixed3 comparator, chosen to expose zero-slope affine equivalence; not a prospectively selected baseline win.'
        for task in ['pair_recombination','unseen_descriptor_family']:
            good=0;nll=0.;n=0
            for i,r in enumerate(data):
                target_objects=set(r['sources'])
                train=[s for j,s in enumerate(data) if j!=i and not target_objects.intersection(s['sources'])
                    and (s['raw_front'],s['y'])!=(r['raw_front'],r['y'])
                    and (task=='pair_recombination' or s['front']!=r['front'])]
                if not train:continue
                m=train_model(train,name);p=predict(m,r);prediction=1+max(range(5),key=lambda k:p[k])
                good+=prediction==r['y'];nll+=score(p,r['y']);n+=1
                predictions.append({'program':name,'task':task,'target_sources':r['sources'],
                    'allowed_x':r['x'],'allowed_descriptor':r['front'],'allowed_class':r['inscobj'],
                    'observed':r['y'],'prediction':prediction,'probabilities_1_to_5':p,
                    'training_pair_count':len(train),
                    'excluded_object_ids':['M77:'+x for x in sorted(set(z for s in data if s not in train for z in s['sources']))],
                    'mask_definition':'whole target objects and exact paired-expression aliases; family task additionally excludes normalized descriptor frame',
                    'exposure':'retrospective previously exposed corpus'})
            result[task]={'correct':good,'n':n,'mean_nll_nats':nll/n if n else None}
        results.append(result)
    write('program_predictions.json',predictions);write('program_comparison.json',results)
    return results

def grouping_programs(cuplinks):
    """Compete addition, multiplication, selection and count-class programs.
    Additional groups are observed; none is invented to repair scalar equations.
    """
    records={}
    for r in cuplinks:
        f=r['other']
        if not r['strict_pair'] or not f['groups'] or f['cup']:continue
        raw=[x['stored_tokens'] for x in f['sources']]
        key=json.dumps((raw,r['observed_cup_count']))
        rec=records.setdefault(key,{'sources':[],'front_sources':f['sources'],
            'groups':f['groups'],'observed_cup_count':r['observed_cup_count'],
            'line_count':f['line_count']})
        rec['sources'].append(r['textnum'])
    predictions=[]
    for r in records.values():
        nn=[g[2] for g in r['groups']]
        p={'sum':sum(nn),'product':math.prod(nn),'maximum':max(nn),
            'first_stored_group':nn[0],'last_stored_group':nn[-1],
            'nonnumerical_constant_three':3}
        predictions.append(r|{'program_predictions':p})
    result={'records':len(records),'records_with_multiple_groups':sum(len(r['groups'])>1 for r in records.values()),
        'scores':{k:{'correct':sum(r['program_predictions'][k]==r['observed_cup_count'] for r in predictions),
                    'n':len(records),'fitted_parameters':0}
                  for k in ['sum','product','maximum','first_stored_group','last_stored_group','nonnumerical_constant_three']},
        'predictions':predictions,
        'warning':'Stored group order does not establish reading direction. Alternative order is globally specified, not chosen per object. Fixed programs make exact predictions; no absent combinations scored.'}
    write('grouping_programs.json',result)
    return result

def partial_extensions(cuplinks):
    targets=[]
    for r in cuplinks:
        if r['strict_pair'] and not r['has_third_face'] and r['other']['line_count']==1:continue
        if any('0' in s['stored_tokens'] or any(t.startswith('*') for t in s['stored_tokens']) for s in r['other']['sources']):
            compatibility='Visible known signs retained; doubtful/unknown slots have not been completed. No exact front identity asserted.'
        else:compatibility='All represented line boundaries and separate faces retained.'
        targets.append(r|{'compatibility_note':compatibility})
    write('partial_and_multiface_extensions.json',targets)
    return targets

def partial_compatibility(cuplinks):
    sys.path.insert(0,str(OUT.parent/'shared'))
    from foundation import load_observations, compatible
    observed={r['row_id']:r for r in load_observations()}
    strict=collections.defaultdict(list)
    for r in cuplinks:
        if r['strict_pair'] and r['other']['line_count']==1 and not r['other']['cup']:
            strict[tuple(r['other']['sources'][0]['stored_tokens'])].append(r)
    results=[]
    for r in cuplinks:
        if r['strict_pair'] or r['other']['line_count']!=1:continue
        source=r['other']['sources'][0];obs=observed[source['row_id']]
        known=sum(t['kind']=='sign' for t in obs['observations'])
        if known<3:continue
        matches=[]
        for seq,links in strict.items():
            if compatible(obs['observations'],[int(x) for x in seq],admit_doubtful=True):
                cc=sorted({l['observed_cup_count'] for l in links})
                matches.append({'compatible_complete_stored':seq,'known_reverse_counts':cc,
                    'new_count_if_same_expression':r['observed_cup_count'] not in cc,
                    'complete_source_objects':sorted({l['textnum'] for l in links})})
        if matches:results.append({'partial_source':source,'observed_cup_count':r['observed_cup_count'],
            'other_faces':r['other_faces'],'compatible_complete_candidates':matches,
            'inference_status':'existential compatibility only; no completion becomes observed training data'})
    write('partial_field_compatibility.json',results)
    return results

def multiline_programs(rows):
    """Test two globally declared line-order programs, never edit source lines.
    This includes face0 (single physical face with several numbered lines).
    An exact inline witness is a candidate layout equivalence, not an identity.
    """
    groups=collections.defaultdict(list);single=collections.defaultdict(list)
    for r in rows:
        groups[(r['textnum'],int(r['sideline'])//10)].append(r)
        if r['strict']=='1':single[r['seq']].append(row_ref(r))
    records=[];eligible=0
    for (oid,face),rr in groups.items():
        if len(rr)<2 or not all(r['strict']=='1' for r in rr):continue
        if not any(t in LONG for r in rr for t in r['seq']):continue
        eligible+=1
        rr=sorted(rr,key=lambda r:int(r['sideline']))
        for name,order in [('catalogue_line_order',rr),('globally_reversed_line_order',rr[::-1])]:
            candidate=tuple(t for r in order for t in r['seq'])
            sources=[s for s in single.get(candidate,[]) if s['textnum']!=oid]
            if sources:records.append({'object_id':'M77:'+oid,'face_code':face,'program':name,
                'source_lines':[row_ref(r) for r in rr], 'predicted_inline_stored':candidate,
                'observed_inline_witnesses':sources,
                'status':'candidate grouping/layout equivalence; same referent and cardinal interpretation not established'})
    result={'strict_multiline_stroke_faces':eligible,'globally_declared_order_programs':2,
            'matches':records,'no_free_per_object_line_reversal':True}
    write('multiline_grouping_programs.json',result)
    return result

def controls():
    # Mechanism diagnostic: recover a shared multiplier and detect inconsistent loop.
    fake=[{'x':x,'y':2*x,'front':str(x),'inscobj':'control'} for x in (1,2)]
    m=train_model(fake,'arithmetic_multiplier')
    return {'constructed_multiplier_recovered':m['a']==2.,'fitted_multiplier':m['a'],
            'not_indus_evidence':True,
            'category_gauge':'Any bijection of anonymous count classes and corresponding lookup outputs leaves categorical predictions invariant.',
            'unit_gauge':'All U values multiplied by a common positive constant preserve within-component equal-quantity equations.'}

def export_candidates(cuplinks):
    fish=set('59 60 61 62 65 66 67 68 69 70 72 73 74 76 211'.split())
    write('fish_211_cup_records.json',[r for r in cuplinks if any(fish.intersection(s['stored_tokens']) for s in r['other']['sources'])])
    def candidate(id,status,kind,rule,context,support,contradictions,alternatives,parameters,predictions,paths,prerequisites=()):
        return {'id':id,'route':'C','status':status,'claim_type':kind,'rule':rule,
            'namespace':'Mahadevan1977','context':context,'prerequisites':list(prerequisites),
            'support':support,'contradictions':contradictions,'alternatives':alternatives,
            'parameters':parameters,'complexity':'See executable program, explicit parameter counts and approximate-complexity warning; no ledger promotion from fit.',
            'predictions':predictions,'source_base':'repository_root',
            'source_paths':[str((OUT/p).resolve().relative_to(ROOT)) for p in paths],
            'prior_exposure':'Entire frozen corpus previously exposed; evaluations and controls retrospective.'}
    candidates=[
      candidate('C_LONG_FIELD_LOCALITY','supported_scope_limited','structural_constraint',
        'Among 330 strict exact one-long-group templates, count substitution occurs in four: bare N and three cup-containing templates.',
        'Strict exact full-line contexts; no inferred synonymy or absent-combination negatives.',
        ['one_group_templates.json: 330 templates; four variable'],[],['Larger contexts may hide productive substitution; nominal categories may be count-fixed.'],0,
        ['A global count-substitution rule requires additional evidence beyond these four frames.'],['one_group_templates.json','numerical_observations.json']),
      candidate('C_CUP_CARDINAL_VS_CATEGORY','underdetermined','operational_meaning',
        'Parse cup 328 plus long-stroke group as an independently variable field; cardinal/ordinal/nominal interpretations remain observational alternatives.',
        '267 cup/other-face records, including partial and third-face observations.',
        ['cup_field_records.json','Prior 85-paired-object census reused'],[],
        ['Cardinal amount','Ordinal category','Nominal class','Complementary administrative field'],
        {'count_classes':5,'absolute_unit':None},
        ['No pronunciation, physical unit or count arithmetic follows from class labels.'],['cup_field_records.json','../../../docs/mahadevan_crossface_constraints_20260905.md']),
      candidate('C_DESCRIPTOR_UNIT_CONVERSION','rejected','operational_meaning',
        'Each descriptor has one fixed positive unit, and linked single-count faces express equal quantities.',
        '29 strict single-count face-pairs; 24 unique global equations.',
        ['Conditional graph has 31 descriptor units and 12 arbitrary scales.'],
        ['M77:4444 and M77:4456 require Ucup/U119frame=2/3; M77:5498 requires 1; object-class conditioning retains the conflict.'],
        ['Complementary fields','Locus-specific lookup units','Unobserved context','Nonnumerical strokes'],
        {'global_descriptor_units':31,'global_free_component_scales':12,'locus_conditioned_units':47,'locus_conditioned_free_scales':24},
        ['Locus repair removes contradiction while increasing independent scales; it does not independently establish arithmetic.'],['relative_unit_graphs.json','single_count_crossface_constraints.json'],
        ['Each visible count has cardinal value n times its descriptor unit.','Face equality applies.']),
      candidate('C_FRONT_TO_CUP_ARITHMETIC','rejected','operational_meaning',
        'Predict cup count using a shared multiplier or affine transform of the front long-stroke count.',
        '11 distinct strict single-count noncup/cup records, whole target objects and exact paired copies excluded per fold.',
        ['The intended multiplier is recoverable on a compact constructed control.'],
        ['Fold-refit constant NLL 1.182 beats multiplier 1.918 and affine 1.274 on both retrospective tasks; affine full fit has zero slope.'],
        ['Independent count field','Conditional category model'],
        {'multipliers_searched':8,'affine_programs_searched':81,'constant_programs_searched':9},
        ['No shared arithmetic relation identified; grouped sums/products similarly fail to distinguish numerical meaning.'],['program_comparison.json','program_predictions.json','grouping_programs.json']),
      candidate('C_REPEAT_FISH_87','conditional','operational_meaning',
        'Two repeated 59 signs may be written 87+59 in the stored 267–99…211 frame.',
        'All 98 repeated non-long-sign runs searched; at least two context tokens; exact or one context edit.',
        ['M77:4232:0 has267–99–59–59–211;M77:1551:0 has267–99–87–59–211.'],[],
        ['Count-class/category substitution','Unrelated fish expression','Family-specific writing operation'],
        {'graphical_numbers':5,'label_permutations':120},
        ['One base and one frame only; 24 of 120 number-label permutations have at least the same hit count.'],['repeat_compression_candidates.json','repeat_compression_label_controls.json'],
        ['The two expressions encode the same operation/referent, which is not independently established.']),
      candidate('C_MULTILINE_2516','provisional','graphical_equivalence',
        'Catalogue-order lines [86]/[211] may form the same grouped record as inline [86,211].',
        '16 strict multiline stroke-bearing faces; two globally declared line-order programs.',
        ['M77:2516:1 and M77:2516:2; inline witnesses M77:4474:20 and M77:4518:20.'],[],
        ['Separate complementary fields happen to share signs','Independent category formula'],0,
        ['If independently shown to encode the same record, this supports a line-break spelling operation, not a numerical pronunciation.'],['multiline_grouping_programs.json']),
      candidate('C_PARTIAL_119_THIRD_FIELD','conditional','structural_constraint',
        'If doubtful 119 is confirmed, the 176–342–87–119 family has reverse counts 2, 3 and 4, with additional third fields 137 or 59 on the count-4 examples.',
        'Partial compatibility preserves unknown spans and doubtful identities; no imputed training data.',
        ['M77:4581:20 and M77:4591:20 uniquely match this complete family among existing cup fronts.'],[],
        ['Doubtful sign is not 119','Third field changes referent','Independent production/category effect'],0,
        ['Inspect held sources for 4581/4591 exactly at doubtful 119 and face assignment; preserve both third labels.'],['partial_field_compatibility.json'],
        ['Doubtful 119 reading and catalogue face assignments are correct.'])]
    write('candidates.json',candidates)

def main():
    rows=load();obs=neutral_observations(rows);objects,qlinks,cuplinks=record_fields(rows)
    tt=templates(rows);comp=compression(rows);graphs=[]
    for cond in ([],['inscobj'],['inscobj','locus'],['inscobj','locus','level']):graphs.append(unit_graph(qlinks,cond))
    write('relative_unit_graphs.json',graphs)
    evaluation=prediction_evaluation(cuplinks);grouping=grouping_programs(cuplinks);partial=partial_extensions(cuplinks)
    compatibility=partial_compatibility(cuplinks)
    multiline=multiline_programs(rows)
    export_candidates(cuplinks)
    from run_roof_count_program import main as run_roof_scope
    roof_scope=run_roof_scope(rows=rows,emit=False)
    result={'source':'research/data/mahadevan_20260905/concordance_rows.csv',
        'source_sha256':hashlib.sha256((ROOT/'research/data/mahadevan_20260905/concordance_rows.csv').read_bytes()).hexdigest(),
        'rows':len(rows),'visible_or_doubtful_long_stroke_occurrences':len(obs),
        'explicit_multiple_face_objects':len(objects),'single_count_face_pairs':len(qlinks),
        'cup_other_face_records':len(cuplinks),'partial_or_multiface_cup_records':len(partial),
        'strict_one_count_templates':len(tt),'templates_with_more_than_one_count':sum(len(t['observed_counts'])>1 for t in tt),
        'compression':comp,'controls':controls(),'grouping_program_scores':grouping['scores'],
        'partial_field_rows_with_complete_compatibles':len(compatibility),
        'strict_multiline_stroke_faces_tested':multiline['strict_multiline_stroke_faces'],
        'multiline_inline_correspondences':len(multiline['matches']),
        'roof_count_scope_programs':roof_scope,
        'affine_result_interpretation':'Slope zero discards front count; no arithmetic discovery.',
        'evaluation':'program_comparison.json',
        'no_new_meaning_accepted':True,'steps_executed':[25,26,27,28,29,30]}
    write('summary.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
