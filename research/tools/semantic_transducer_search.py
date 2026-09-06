#!/usr/bin/env python3
"""Search a frozen Indus corpus for compositional reading hypotheses.

The outputs are candidate relations, NEVER translations. Exact matching contexts
can contain different words or quantities. Opposite faces are not assumed to be
synonyms. Runs are deterministic and use only the Python standard library.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip, hashlib, itertools, json
from pathlib import Path

EXPECTED_SHA256 = '6a0c597986783c5da8fbcb0afc3268a2c6a9f042a9b81746ebc4f89158efbd01'
# Visual hypotheses based on the public publisher's glyph drawings. These are
# deliberately NOT substitutions applied to the underlying source transcription.
TICK_PAIRS = [(59,60),(65,66),(67,68),(70,71),(72,73),(89,88),
              (141,143),(162,164),(178,179),(204,207),(219,220),
              (249,250),(277,278),(280,281),(284,285),(287,289),
              (290,291),(307,308),(387,388),(389,390),(391,392),(403,404)]
ROOF_PAIRS = [(59,65),(137,138),(141,142),(158,159),(162,163),
              (204,206),(328,334),(410,411)]
# (composite, base, visible candidate component). Exact forms may differ under
# superposition. This list tests a literal concatenation hypothesis, not a claim
# that drawn parts must be pronounced separately.
PARTS = [(2,1,87),(22,1,162),(25,1,86),(30,1,261),(31,1,373),
         (32,1,328),(36,1,141),(52,51,86),(80,77,77),(172,171,171),
         (173,171,171),(329,328,99),(330,328,102),(343,342,97),
         (344,342,99),(345,342,102),(403,373,373),(405,403,171),
         (407,403,137),(416,415,87),(417,415,137)]


def decode(v):
    if 'stringValue' in v: return v['stringValue']
    if 'integerValue' in v: return int(v['integerValue'])
    if 'arrayValue' in v: return [decode(x) for x in v['arrayValue'].get('values', [])]
    if 'nullValue' in v: return None
    if 'booleanValue' in v: return v['booleanValue']
    raise ValueError('Unsupported source field: '+str(v))


def load(path):
    raw=path.read_bytes()
    if path.suffix=='.gz': raw=gzip.decompress(raw)
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=EXPECTED_SHA256: raise ValueError('Input differs from frozen acquisition')
    rows=[]
    for doc in json.loads(raw):
        r={k:decode(v) for k,v in doc['fields'].items()}
        slots=[str(r[f'S{i}']) for i in range(1,15)]
        if slots!=r['texts']: raise ValueError('Redundant source fields disagree')
        seq=tuple(x for x in slots if x)
        r['seq']=seq
        r['clean']=(bool(seq) and r['dir'] in ('1','2','3')
          and all(x.isdigit() and 1<=int(x)<=417 for x in seq)
          and len(seq)==int(r['posnum'])==int(r['signnum'])
          and all(slots[:len(seq)]))
        rows.append(r)
    return rows,digest


def witness(r):
    return {k:r[k] for k in ('index','textnum','sideline','inscobj','locus','level','dir')}|{'sequence':r['seq']}


def run(source, output):
    rows,digest=load(source)
    clean=[r for r in rows if r['clean']]
    sequences=frozenset(r['seq'] for r in clean)
    byseq=defaultdict(list); objects=defaultdict(list)
    for r in clean: byseq[r['seq']].append(r)
    for r in rows: objects[r['textnum']].append(r)
    vocabulary=[str(i) for i in range(1,418)]
    occurrence=defaultdict(list)
    for s in sorted(sequences):
        for i,t in enumerate(s): occurrence[int(t)].append((s,i))

    def relation(short,long,**extra):
        return dict(compact=short,expanded=long,
                    compact_witnesses=[witness(r) for r in byseq[short]],
                    expanded_witnesses=[witness(r) for r in byseq[long]],**extra)

    modifier_hits=[]
    for family,pairs in [('four_surrounding_strokes',TICK_PAIRS),('roof',ROOF_PAIRS)]:
        for base,modified in pairs:
            for s,i in occurrence[modified]:
                for extra in vocabulary:
                    for side,exp in [('before',(extra,str(base))),('after',(str(base),extra))]:
                        target=s[:i]+exp+s[i+1:]
                        if target in sequences:
                            modifier_hits.append(relation(s,target,family=family,base=base,
                                modified=modified,extra=int(extra),side=side,
                                unchanged_context_length=len(s)-1,position=i))
    ranking=[]
    for family in ('four_surrounding_strokes','roof'):
        for side in ('before','after'):
            for extra in range(1,418):
                hits=[h for h in modifier_hits if h['family']==family and h['side']==side and h['extra']==extra]
                if hits:
                    ranking.append(dict(family=family,extra=extra,side=side,
                        base_count=len({h['base'] for h in hits}),pairs=len(hits),
                        pairs_with_two_unchanged_signs=sum(h['unchanged_context_length']>=2 for h in hits),
                        distinct_contexts=len({(tuple(h['compact'][:h['position']]),
                            tuple(h['compact'][h['position']+1:])) for h in hits})))
    ranking.sort(key=lambda x:(-x['base_count'],-x['pairs_with_two_unchanged_signs'],-x['pairs'],x['extra'],x['side']))
    literal=[]
    for composite,base,part in PARTS:
        for s,i in occurrence[composite]:
            for expansion in sorted({(str(base),str(part)),(str(part),str(base))}):
                target=s[:i]+expansion+s[i+1:]
                if target in sequences:
                    literal.append(relation(s,target,composite=composite,base=base,part=part,
                        unchanged_context_length=len(s)-1))

    face_maps=defaultdict(set)
    for tid,rr in sorted(objects.items()):
        # Tens encode faces; single-digit codes are lines, NOT distinct faces.
        # Use only explicitly numbered faces with exactly one recorded line.
        faces=defaultdict(list)
        for r in rr:
            face=int(r['sideline'])//10
            if face>0: faces[face].append(r)
        usable=[ff[0] for ff in faces.values() if len(ff)==1 and ff[0]['clean']]
        for a,b in itertools.combinations(usable,2):
            if a['seq']==b['seq']:continue
            if len(a['seq'])>len(b['seq']): a,b=b,a
            if len(a['seq'])<=2 and len(b['seq'])>len(a['seq']):
                face_maps[(a['seq'],b['seq'])].add(tid)
    aliases=[]; alias_contexts=[]
    for (a,b),tids in sorted(face_maps.items()):
        aliases.append(dict(short=a,long=b,source_objects=sorted(tids),
            status='coface_candidate_not_asserted_synonymous'))
        for s in sorted(sequences):
            for i in range(len(s)-len(b)+1):
                if s[i:i+len(b)]!=b or len(s)==len(b):continue
                short=s[:i]+a+s[i+len(b):]
                if short not in sequences:continue
                outside={r['textnum'] for r in byseq[s]+byseq[short]}-tids
                if outside:
                    alias_contexts.append(relation(short,s,source_short=a,source_long=b,
                        source_objects=sorted(tids),outside_objects=sorted(outside)))

    repeats=[]
    for s in sorted(sequences):
        for i in range(len(s)-1):
            if s[i]!=s[i+1]:continue
            for n in range(2,min(len(s)-i,7)+1):
                if any(t!=s[i] for t in s[i:i+n]):break
                for marker in vocabulary:
                    if marker==s[i]:continue
                    for side,exp in [('before',(marker,s[i])),('after',(s[i],marker))]:
                        target=s[:i]+exp+s[i+n:]
                        if target in sequences:
                            repeats.append(relation(target,s,repeated=s[i],repeat_count=n,
                                candidate_marker=marker,side=side,
                                unchanged_context_length=len(s)-n))
    fish_diagnostics=[]
    for base,modified in TICK_PAIRS[:5]:
        for sign in (base,modified):
            oo=occurrence[sign]
            fish_diagnostics.append(dict(sign=sign,base=base,modified=sign==modified,
                occurrences_in_unique_sequences=len(oo),
                previous=dict(Counter(s[i-1] if i else '^' for s,i in oo)),
                next=dict(Counter(s[i+1] if i+1<len(s) else '$' for s,i in oo))))
    payload={
      'summary.json':{'input_sha256':digest,'records':len(rows),'strict_lines':len(clean),
        'unique_sequences':len(sequences),'status':'exploratory_reading_search_no_decipherment',
        'graphical_modifier_pairs':len(TICK_PAIRS)+len(ROOF_PAIRS),
        'literal_component_hypotheses':len(PARTS),'literal_component_matches':len(literal),
        'linked_face_candidate_pairs':len(face_maps),'linked_face_extra_context_matches':len(alias_contexts),
        'repeat_marker_matches':len(repeats),'phonetic_values_established':0,
        'semantic_values_established':0,
        'interpretation':'Context substitution alone does not establish synonymy; no phonetic target was supplied or recovered.'},
      'graphic_hypotheses.json':{'tick_pairs':TICK_PAIRS,'roof_pairs':ROOF_PAIRS,'literal_parts':PARTS,
         'source':'https://indusscript.in/assets/images/{id}.png',
         'status':'visual hypotheses; not automatic normalization of original signs'},
      'modifier_ranking.json':ranking,'modifier_context_pairs.json':modifier_hits,
      'literal_component_pairs.json':literal,'coface_candidates.json':aliases,
      'coface_external_context_pairs.json':alias_contexts,'repeat_marker_pairs.json':repeats,
      'fish_context_profiles.json':fish_diagnostics,
    }
    output.mkdir(parents=True,exist_ok=True)
    for name,value in payload.items():
        (output/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    return payload['summary.json'],ranking[:12]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    summary,ranking=run(args.input,args.output)
    print(json.dumps({'summary':summary,'top_modifiers':ranking},indent=2))
