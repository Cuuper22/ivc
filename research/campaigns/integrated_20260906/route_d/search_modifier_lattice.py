#!/usr/bin/env python3
"""Joint roof/ticks phonetic-modifier square on independently sourced words.

59=r, 65=roof(r),60=ticks(r),66=ticks(roof(r)),211=ticks component.
Every lexical form must be present; no new word is generated as evidence.
This is conditional on semantics AND productive phonetic graphical operators.
"""
import itertools,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def extensions(root,word):
    if word!=root and word.startswith(root):yield ('append',word[len(root):])
    if word!=root and word.endswith(root):yield ('prepend',word[:-len(root)])

def apply(op,word):
    return word+op[1] if op[0]=='append' else op[1]+word

def search(words,roots=None):
    words=set(words);solutions=[]
    for root in sorted(words if roots is None else roots):
        operations=sorted({op for word in words for op in extensions(root,word)})
        for roof,tick in itertools.product(operations,repeat=2):
            roof_word=apply(roof,root);tick_word=apply(tick,root)
            double=apply(tick,roof_word)
            if double not in words:continue
            solutions.append({'base':root,'roof_operator':roof,'ticks_operator':tick,
                '211_surface':tick[1],'mapping':{'59':root,'65':roof_word,'60':tick_word,'66':double},
                'different_operator_sounds':roof[1]!=tick[1],
                'commuting_sound_operators':double==apply(roof,tick_word),
                'description_cost':len(root)+len(roof[1])+len(tick[1])+3})
    return sorted(solutions,key=lambda x:(x['description_cost'],x['base'],x['roof_operator'],x['ticks_operator']))

def main():
    inventory=json.loads((HERE/'outputs/linguistic_inventory.json').read_text())
    fish=inventory['fish_gloss_records'];mw=search(fish)
    tamil_source=HERE.parent/'evidence_inventory/dravidian_lexical_examples.json'
    tamil_records=json.loads(tamil_source.read_text())
    tamil_words={''.join(f['segmentation_as_printed']) for f in tamil_records}
    tamil=search(tamil_words,{'mīṉ'})
    for row in mw:
        row['source_lexical_records']={s:fish[w] for s,w in row['mapping'].items()}
    out={'hypothesis':'two productive concatenative phonetic operators on the59/65/60/66 graphical square',
        'semantic_prerequisite':'allfour square nodes lexical fish terms; no such Indus semantic anchor accepted',
        'mw_exact_solutions':len(mw),'mw_distinct_marker_sounds':sorted({x['211_surface'] for x in mw}),
        'mw_solutions':mw,'tamil_initial_subset_exact_solutions':len(tamil),
        'tamil_initial_subset_solutions':tamil,
        'tamil_subset_words':sorted(tamil_words),
        'source_paths':[inventory['mw_path'],str(tamil_source.relative_to(HERE.parents[3]))],
        'limits':['Dictionary nonoccurrence is not evidence of an impossible ancient word.',
            'Source compounds are selected, later forms; zero applies to held lexicon and exact concatenation only.',
            'Roof may be a semantic classifier instead of an independently pronounced operation.'],
        'next_mechanism':'source-attested contextual allomorphy, charged separately from exact concatenation'}
    (HERE/'outputs/two_modifier_lattice.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if not k.endswith('_solutions') or isinstance(v,int)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
