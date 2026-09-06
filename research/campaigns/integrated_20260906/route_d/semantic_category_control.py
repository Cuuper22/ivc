#!/usr/bin/env python3
"""Same selected four-root/shared-marker search on other MW noun categories."""
import collections,itertools,json,math,random,re,xml.etree.ElementTree as ET
from pathlib import Path
from run_route_d import HERE,MW,extension_edges,perm

def inventory():
    result={k:{} for k in ('fish','bird','tree','animal')}
    rules={k:re.compile(r'\ban?\s+(?:(?:kind|species|sort)\s+of\s+)?'+k+r'\b',re.I) for k in result}
    for _,elem in ET.iterparse(MW,events=['end']):
        if not re.fullmatch(r'H[1-4][AB]?',elem.tag):continue
        key=elem.findtext('./h/key1');bodyel=elem.find('body')
        if key and re.fullmatch('[A-Za-z]+',key) and bodyel is not None:
            body=' '.join(bodyel.itertext())
            for category,rule in rules.items():
                if rule.search(body):
                    result[category][key]={'entry_id':elem.findtext('./tail/L'),
                        'page_column':elem.findtext('./tail/pc'),'passage':body}
        elem.clear()
    return result,{k:v.pattern for k,v in rules.items()}

def search(words):
    result={}
    for orientation,markers in extension_edges(words).items():
        viable=[]
        for marker,roots in markers.items():
            if len(roots)<4:continue
            roots=sorted(roots,key=lambda x:(len(x),x))
            viable.append({'marker':marker,'distinct_roots':len(roots),
                'root_assignments':perm(len(roots),4),
                'minimum_same_description_cost':sum(map(len,roots[:4]))+len(marker)+5,
                'roots':roots})
        viable.sort(key=lambda x:(x['minimum_same_description_cost'],x['marker']))
        result[orientation]={'eligible_markers':len(viable),
            'compatible_systems_exact':sum(x['root_assignments'] for x in viable),
            'markers':viable}
    return result

def main():
    categories,rules=inventory();n=len(categories['fish']);runs=[]
    for category,words in categories.items():
        runs.append({'category':category,'mode':'full_category','headword_count':len(words),'search':search(words)})
        if category=='fish' or len(words)<n:continue
        for seed in range(20260906,20260922):
            subset=random.Random(seed).sample(sorted(words),n)
            runs.append({'category':category,'mode':'fish_size_matched','seed':seed,
                'headword_count':n,'search':search(subset)})
    summary={'same_test':'four distinct base roots; root and expanded form both in named semantic category; shared nonempty211; both orientations; same cost',
        'source_path':str(MW.relative_to(HERE.parents[3])),
        'category_sizes':{k:len(v) for k,v in categories.items()},'filter_rules':rules,
        'runs':runs,'interpretation':'A rival category admitting ka shows ka is not fish-specific in this lexical membership test. Size-matched draws retain semantic category but do not preserve extension-edge degree.',
        'limits':'No category is an independently grounded Indus meaning; these are matched selection diagnostics, not language tests or phonetic correctness scores.'}
    (HERE/'outputs/semantic_category_control.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (HERE/'outputs/semantic_category_source_entries.json').write_text(json.dumps(categories,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'category_sizes':summary['category_sizes'],'full_category_searches':[r for r in runs if r['mode']=='full_category'],
        'matched_summary':{cat:{'runs':sum(r['category']==cat and r['mode']=='fish_size_matched' for r in runs),
        'runs_with_append_ka':sum(r['category']==cat and r['mode']=='fish_size_matched' and any(x['marker']=='ka' for x in r['search']['append']['markers']) for r in runs)}
        for cat in ['bird','tree','animal']}},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
