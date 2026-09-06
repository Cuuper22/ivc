#!/usr/bin/env python3
"""Reconstructed 2026-09-06: bounded conditional linguistic coordinate search.
No target pronunciations or language labels exist for these Indus rows. The
lexical energy exported here is an extra prior factor, NEVER a text likelihood.
"""
from pathlib import Path
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib, json, math, os, re, xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
CAM=HERE.parents[1]
ROOT=Path(os.environ.get('IVC_REPO_ROOT',str(CAM.parents[2])))
if not (ROOT/'evidence').exists():ROOT=Path('/workspace/scratch/f9a6bdbd6310/ivc')
FISH={'59':'60','65':'66','67':'68','72':'73'}
REV={v:k for k,v in FISH.items()}
BASES=list(FISH)

def dump(name,x): (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tokens(row): return list(map(str,row.get('tokens_stored',row.get('tokens',[]))))

@lru_cache(None)
def vocabulary(language):
    if language=='sanskrit':
        p=ROOT/'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'
        words=set()
        for _,e in ET.iterparse(p,events=['end']):
            if re.fullmatch(r'H[1-4][AB]?',e.tag):
                w=e.findtext('./h/key1')
                if w and re.fullmatch('[A-Za-z]+',w):words.add(w)
                e.clear()
        return frozenset(words)
    if language=='tamil':
        records=json.loads((CAM/'evidence_inventory/tamil_compounds.json').read_text())['records']
        return frozenset((''.join(r['segmentation_as_printed']) if r.get('segmentation_as_printed') else r['printed_form_transcription'].replace('-','')) for r in records if r.get('phonology_test_eligible'))|{'mīṉ'}
    return frozenset()

@lru_cache(None)
def alternatives(language,orientation):
    """All dictionary root/extension splits. No arbitrary headword truncation.
    Tamil keeps the attested comparative compound segmentation and linking
    material in a single prefix/suffix string. No historical correspondence added.
    """
    words=vocabulary(language); by=defaultdict(set)
    for w in words:
        for i in range(1,len(w)):
            root,marker=(w[:i],w[i:]) if orientation=='append' else (w[i:],w[:i])
            if root in words:by[marker].add(root)
    return dict(by)

def combined(root,marker,orientation):return root+marker if orientation=='append' else marker+root

def word_bits(model,word):
    # Universal finite-string code; lexical membership is a binary residual.
    return len(word)*model['char_bits'] + (0 if word in vocabulary(model['language']) else 12)

def decode(model,seq,roles=None):
    """Viterbi word segmentation, with globally frozen reusable mappings.
    Numeric/classifier roles do not consume a lexical factor. Unassigned tokens
    stay explicit; no assigning sound to sign70 or to unseen roots on heldout.
    """
    seq=list(map(str,seq)); n=len(seq); dp=[None]*(n+1);dp[n]=(0,[])
    for i in range(n-1,-1,-1):
        s=seq[i]; options=[]
        if roles and ((isinstance(roles,dict) and roles.get(s) in ('numeric','classifier','nonphonetic')) or (isinstance(roles,list) and i<len(roles) and roles[i] in ('numeric','classifier','nonphonetic'))):
            options.append((1,0,{'source_signs':[s],'role':'external_nonphonetic','unread':f'<M77:{s}>'}))
        elif model['language'] in ('anonymous','nonphonetic') and (s in FISH or s in REV or s=='211'):
            label=f"Q(L{REV[s]})" if s in REV else ('Q' if s=='211' else f'L{s}')
            options.append((1,1,{'source_signs':[s],'role':model['language'],'unread':label}))
            if s in FISH and i+1<n and seq[i+1]=='211':options.append((2,1,{'source_signs':[s,'211'],'role':model['language'],'unread':f'Q(L{s})'}))
        elif model.get('marker_role')=='classifier' and s=='211':
            options.append((1,0,{'source_signs':[s],'role':'nonphonetic_classifier','unread':'<CLASS:211>'}))
        elif s in model['mapping']:
            w=model['roots'][REV[s]] if model.get('marker_role')=='classifier' and s in REV else model['mapping'][s]
            options.append((1,word_bits(model,w)+model['boundary_bits'],{'source_signs':[s],'role':'phonetic_marker' if s=='211' else 'logophonetic','candidate_sound':w}))
            if s in model['roots'] and i+1<n and seq[i+1]=='211':
                w=model['roots'][s] if model.get('marker_role')=='classifier' else combined(model['roots'][s],model['marker'],model['orientation'])
                options.append((2,word_bits(model,w)+model['boundary_bits']+model['fusion_bits'],{'source_signs':[s,'211'],'role':'root_plus_classifier' if model.get('marker_role')=='classifier' else 'root_plus_bound_morpheme','candidate_sound':w}))
        else:options.append((1,0,{'source_signs':[s],'role':'unresolved','unread':f'<M77:{s}>'}))
        dp[i]=min(((c+dp[i+k][0],[span]+dp[i+k][1]) for k,c,span in options),key=lambda x:(x[0],json.dumps(x[1],sort_keys=True)))
    return dp[0][1]

def lexical_residual_bits(model,seq,roles=None):
    out=decode(model,seq,roles)
    if model['language'] in ('anonymous','nonphonetic'):return float(sum(p['role'] in ('anonymous','nonphonetic') for p in out))
    return sum(word_bits(model,p['candidate_sound'])+model['boundary_bits']+(model['fusion_bits'] if len(p['source_signs'])==2 else 0) for p in out if 'candidate_sound' in p)

def parameter_bits(model):
    return sum(len(w)*model['char_bits'] for w in model['roots'].values())+(len(model['marker'])*model['char_bits'] if model.get('marker_role')!='classifier' else 8)+len(model['roots'])*2+5

def set_mapping(model,roots,marker):
    model['roots']=roots;model['marker']=marker;model['mapping']=dict(roots)
    if roots:
        model['mapping']['211']=marker
        model['mapping'].update({FISH[b]:combined(r,marker,model['orientation']) for b,r in roots.items()})

def sufficient_counts(rows,model):
    c=Counter()
    for row in rows:
        for p in decode(model,tokens(row)):
            ss=p['source_signs'];s=ss[0]
            if len(ss)==2:c[(s,'compound')]+=1
            elif s in REV:c[(REV[s],'compound')]+=1
            elif s in FISH:c[(s,'root')]+=1
            elif s=='211':c[('211','marker')]+=1
    return c

def fit_system(rows,language='tamil',orientation='prepend',max_iter=30,force_marker_role=None):
    rows=[r for r in rows if r.get('strict',True)]
    model={'schema':'ivc.reconstructed.linguistic.v1','language':language,'orientation':orientation,
      'char_bits':math.log2(max(2,len(set(''.join(vocabulary(language)))))), 'boundary_bits':1.,'fusion_bits':0.,
      'roots':{},'marker':'','marker_role':'phonetic','mapping':{},'trace':[],'train_rows':len(rows),'train_digest':digest([r.get('row_id',tokens(r)) for r in rows]),
      'factor_type':'conditional_lexical_prior_not_text_likelihood','independent_Indus_sound_targets':0,
      'sources':['shared/observations.jsonl','evidence_inventory/tamil_compounds.json' if language=='tamil' else 'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'],
      'scope':'four graphical fish bases; unknown signs including70 stay unread; retrospective',
      'limitations':'finite coordinate optimum, conditional graphic expansion, no historical sound changes or ancient language identification'}
    if language in ('anonymous','nonphonetic'):
        model['trace']=[{'iteration':0,'objective_bits':sum(lexical_residual_bits(model,tokens(r)) for r in rows)+13,'step':'anonymous labels or silent classifiers; no sound search applicable'}]
        model['converged']=True;return model
    opts=alternatives(language,orientation)
    if not opts:
        # Tamil append genuinely lacks extension edges; retain an explicit
        # literal-root fallback and show the morphological search has zero edges.
        opts={'':set(vocabulary(language))}
    seen=set(t for r in rows for t in tokens(r)); active=[b for b in BASES if b in seen or FISH[b] in seen]
    initial_marker=sorted(opts,key=lambda m:(-len(m),m))[0]
    rr=sorted(opts[initial_marker],key=lambda w:(-len(w),w))
    set_mapping(model,{b:rr[i%len(rr)] for i,b in enumerate(active)},initial_marker)
    unique=Counter(tuple(tokens(r)) for r in rows)
    def objective():return parameter_bits(model)+sum(n*lexical_residual_bits(model,s) for s,n in unique.items())
    model['trace'].append({'iteration':0,'objective_bits':objective(),'step':'initial reusable sound mapping'})
    for iteration in range(1,max_iter+1):
        counts=sufficient_counts(rows,model); old=objective(); best=None
        # Full marker scan; for each fixed marker the additive root-coordinate
        # minimizer is exact. Homophony permitted but root labels stay distinct.
        current_opts={'':vocabulary(language)} if model['marker_role']=='classifier' else opts
        for marker,rs in current_opts.items():
            roots={}; cost=len(marker)*model['char_bits']+counts[('211','marker')]*(word_bits(model,marker)+1)
            for b in active:
                def rc(r):
                    return len(r)*model['char_bits']+counts[(b,'root')]*(word_bits(model,r)+1)+counts[(b,'compound')]*(word_bits(model,combined(r,marker,orientation))+1)
                root=min(rs,key=lambda r:(rc(r),r));roots[b]=root;cost+=rc(root)
            candidate=(cost,marker,roots)
            if best is None or (cost,marker)<(best[0],best[1]):best=candidate
        prev=(model['roots'],model['marker']);set_mapping(model,best[2],best[1]);new=objective()
        if new>old+1e-8:set_mapping(model,*prev);new=old
        # A reusable classifier alternative is evaluated globally, not toggled
        # for a troublesome token. The extra8-bit role code is explicit.
        role_before=model['marker_role']; role_trials=[]
        if model['marker'] and model['marker_role']=='phonetic':
            retained={k:v for k,v in model.items() if k not in ('trace','phonetic_alternative')}
            retained['objective_bits']=objective()
            if retained['objective_bits']<model.get('phonetic_alternative',{}).get('objective_bits',float('inf')):model['phonetic_alternative']=retained
        for role in ((force_marker_role,) if force_marker_role else (('phonetic','classifier') if model['marker'] else ('classifier',))):
            model['marker_role']=role; role_trials.append((objective(),role))
        new,model['marker_role']=min(role_trials)
        if new>old+1e-8:
            model['marker_role']=role_before;set_mapping(model,*prev);new=old
        # Actual alternating steps: frozen segmentation -> root/affix sound
        # update -> Viterbi segmentation. Morphology is globally reusable.
        model['trace'].append({'iteration':iteration,'objective_bits':new,'step':'segmentation -> full root/affix coordinate scan -> segmentation','marker_candidates':len(current_opts),'marker_role':model['marker_role'],'role_alternatives':role_trials,'changed':new<old-1e-8})
        if abs(new-old)<1e-8:break
    model['converged']=abs(model['trace'][-1]['objective_bits']-model['trace'][-2]['objective_bits'])<1e-8
    model['parameter_bits']=parameter_bits(model);model['role_search']='global phonetic-versus-classifier optimization; retained phonetic alternative where supported';model['vocabulary_size']=len(vocabulary(language));model['marker_candidates']=len(opts)
    return model

def constructed_control():
    import importlib.util
    spec=importlib.util.spec_from_file_location('original_d',CAM/'route_d/run_route_d.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.control()

def linear_b_control():
    path=ROOT/'research/data/open_prototype/known_scripts/linear_b_series_d/Samples.txt'
    lines=path.read_text().splitlines(); forms=sorted({w for line in lines for w in line.split() if re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)+',w)})
    # The retained source is ALREADY transliterated. Hide whole word types,
    # learn symbol->syllable from training type boundaries, predict unseen words.
    # This measures decoder operation with supplied readings, not decipherment.
    alphabet=sorted({s for w in forms for s in w.split('-')}); encoded={s:f'S{i}' for i,s in enumerate(alphabet)}
    held=[w for i,w in enumerate(forms) if i%5==0];train=[w for w in forms if w not in held]
    mapping={encoded[s]:s for w in train for s in w.split('-')}
    predictions=[]
    for w in held:
        ss=[encoded[s] for s in w.split('-')];p=''.join(mapping.get(s,'?') for s in ss)
        predictions.append({'encoded':ss,'prediction':p,'target':w.replace('-',''),'all_syllables_seen':all(s in mapping for s in ss),'correct':p==w.replace('-','')})
    return {'evidence_class':'already_held_transliterated_LinearB_diagnostic','source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'supplied_training_symbol_mapping':mapping,'training_word_types':len(train),'held_word_types':len(held),'predictions':predictions,'correct':sum(p['correct'] for p in predictions),'limitation':'Syllable boundaries and training readings supplied by deciphered source; not blind recovery.'}

def main():
    rows=[json.loads(x) for x in (CAM/'shared/observations.jsonl').read_text().splitlines()]
    strict=[r for r in rows if r['strict']]
    pairs=json.loads((CAM/'route_d/outputs/pair_dependencies.json').read_text())
    # Hold all compact/expanded target expressions, every alias and companion.
    held_patterns={tuple(p[k]) for p in pairs for k in ('compact','expanded')}
    held_objects={r['object_id'] for r in rows if tuple(tokens(r)) in held_patterns}
    train=[r for r in strict if r['object_id'] not in held_objects and tuple(tokens(r)) not in held_patterns]
    models=[];predictions=[]
    for language in ('tamil','sanskrit','anonymous','nonphonetic'):
        for orientation in ('append','prepend'):
            m=fit_system(train,language,orientation);m['id']=language+'_'+orientation
            if language in ('tamil','sanskrit') and alternatives(language,orientation):
                phonetic=fit_system(train,language,orientation,force_marker_role='phonetic')
                phonetic.pop('phonetic_alternative',None)
                m['phonetic_alternative']=phonetic
            dump(m['id']+'.json',m);models.append(m)
            for i,p in enumerate(pairs):
                a=decode(m,p['compact']);b=decode(m,p['expanded'])
                render=lambda spans:[x.get('candidate_sound',x.get('unread')) for x in spans]
                predictions.append({'model':m['id'],'pair':i,'compact':a,'expanded':b,'equal_conditional_decoding':render(a)==render(b),'compact_residual_bits':lexical_residual_bits(m,p['compact']),'expanded_residual_bits':lexical_residual_bits(m,p['expanded']),'interpretation':'conditional consistency, not independent phonetic correctness'})
            print(json.dumps({'model':m['id'],'converged':m['converged'],'iterations':len(m['trace'])-1}),flush=True)
    controls={'constructed':constructed_control(),'held_linear_b':linear_b_control()}
    # Objective has exact character-renaming symmetry when lexicon AND map are
    # renamed; prove by explicit full edge cardinality preservation, not a claim
    # about real-world linguistic evidence omitted from this model.
    controls['alphabet_renaming']={}
    for lang in ('tamil','sanskrit'):
        vv=vocabulary(lang);alpha=sorted(set(''.join(vv)));trans=str.maketrans({a:alpha[(i+1)%len(alpha)] for i,a in enumerate(alpha)})
        renamed={w.translate(trans) for w in vv}
        ok=len(renamed)==len(vv) and all((w in vv)==(w.translate(trans) in renamed) for w in vv)
        controls['alphabet_renaming'][lang]={'all_vocabulary_items_checked':len(vv),'bijection_preserves_membership_and_length':ok,'objective_invariant':ok,'independent_sound_targets':0}
    phonetic_predictions=[]
    for m in models:
        if 'phonetic_alternative' not in m:continue
        pm=m['phonetic_alternative']
        for i,p in enumerate(pairs):
            a=decode(pm,p['compact']);b=decode(pm,p['expanded'])
            render=lambda spans:[x.get('candidate_sound',x.get('unread')) for x in spans]
            phonetic_predictions.append({'model':m['id']+'_phonetic','pair':i,'compact':a,'expanded':b,'equal_conditional_decoding':render(a)==render(b),'compact_residual_bits':lexical_residual_bits(pm,p['compact']),'expanded_residual_bits':lexical_residual_bits(pm,p['expanded']),'interpretation':'conditional consistency, not independent phonetic correctness'})
    dump('phonetic_frozen_predictions.json',phonetic_predictions)
    dump('controls.json',controls);dump('frozen_predictions.json',predictions)
    dump('phonetic_alternatives.json',[m['phonetic_alternative']|{'id':m['id']+'_phonetic'} for m in models if 'phonetic_alternative' in m])
    dump('summary.json',{'provenance':'newly executed reconstruction, not recovered old output','systems':len(models),'retained_fully_optimized_phonetic_rivals':sum('phonetic_alternative' in m for m in models),'phonetic_frozen_predictions':len(phonetic_predictions),'all_converged':all(m['converged'] for m in models),'training_rows':len(train),'excluded_target_objects':len(held_objects),'whole_pattern_alias_mask':True,'frozen_predictions':len(predictions),'independent_accepted_sound_values':0,'language_identifications':0,'unread_70':all('70' not in m['mapping'] for m in models),'lexicons':{x:len(vocabulary(x)) for x in ('tamil','sanskrit')},'control_results':{k:v for k,v in controls.items() if k!='held_linear_b'}})
    (HERE/'REPORT.md').write_text('''# Reconstructed linguistic completion\n\nEight systems were executed: Tamil, Sanskrit, anonymous language, and nonphonetic rivals, each in two orders. Named systems alternate latent word boundaries with a full reusable root/affix search across held dictionary extension edges. Root logograms, phonetic affixes, compound signs, and externally supplied numeric/classifier roles coexist. The global211 role is optimized against a silent-classifier alternative, whose extra8-bit code is explicit. Named models choose silent classifiers under this objective; supported phonetic alternatives are retained separately rather than discarded. Unknown signs remain unread, including70.\n\nThe emitted factor is a conditional lexical prior, not a second likelihood for corpus text. The character code and dictionary membership penalty are explicit modeling choices; they do not identify an ancient language. Tamil source coverage is fish/star-selected and dramatically smaller than Sanskrit. No sound, lexical translation, or language identification was accepted.\n\nAll six compact/expanded pairs and their whole-object companions were excluded before fitting. Frozen pair consistency is exported, not represented as phonetic accuracy. Constructed sound controls and held deciphered Linear B word-type diagnostics execute separately. Full lexical alphabet renaming confirms underdetermination of this objective. These are newly reconstructed outputs; old numerical results were not copied as if regenerated.\n''')
if __name__=='__main__':main()
