"""sense_common.py -- shared helpers: text cleaning of glosses, the fixed category rules, the scoring core.
Categories (fixed list, mapped BY RULE, no hand judgment per word): number, measure, commodity, person, kin, place, time, deity, animal,
plant, tool, action, quality.  A sense gets every category that any of its first 5 content words triggers: first by the keyword lists
below (stem match), else by the WordNet lexicographer file of the word's first (most common) sense. A gloss starting with 'to ' is action."""
import re, unicodedata, sys
import numpy as np
CATS = ['number', 'measure', 'commodity', 'person', 'kin', 'place', 'time', 'deity', 'animal', 'plant', 'tool', 'action', 'quality']
KW = {
 'number': 'one two three four five six seven eight nine ten eleven twelve thirteen twenty thirty forty fifty hundred thousand times fold number numeral couple pair double twofold once twice both'.split(),
 'measure': 'measure weight capacity unit ration portion share quantity handful span cubit scale balance full amount volume length ounce pound bushel'.split(),
 'commodity': 'grain rice paddy millet wheat barley cotton thread oil ghee milk salt sugar cloth cotton gold silver copper metal iron bronze wage tax tribute price money wealth crop produce food goods sesame wood timber fiber fibre cattle-wealth rent fee payment pulse seed bean honey jaggery'.split(),
 'tool': 'pot vessel jar basket plough plow spade knife axe bow arrow spear sword weapon tool rope chain spindle boat ship cart wheel pole ladle lamp banner staff stick scabbard crate box chest bed throne instrument implement cup bowl pitcher net hook sickle hammer drum seal'.split(),
 'person': 'king chief lord master servant slave man woman maiden lady person people hero hunter archer farmer husbandman cultivator smith goldsmith carpenter potter weaver warrior soldier priest teacher elder junior leader head manager agent keeper guard attendant bondsman ruler official merchant trader washerman householder bard poet youth boy girl cowherd shepherd fisherman worker laborer labourer chieftain noble heir minister officer chief porter bearer'.split(),
 'kin': 'father mother son daughter brother sister wife husband child children kinsman kindred kin relative relation family lineage clan descendant offspring uncle aunt grandson grandchild nephew niece marry marriage tribe caste race progeny birth born sibling'.split(),
 'place': 'town village city house home abode place field land country region district street hill mountain river island fort forest garden road shore tank pond lake locality site quarter ward habitation dwelling hamlet city-state ground soil earth'.split(),
 'time': 'day month year season night dawn morning evening moon sun star planet constellation calendar time rain age era period festival lunar monsoon noon sunrise sunset autumn spring summer winter fortnight week hour'.split(),
 'deity': 'god goddess deity divine sacred temple worship sacrifice demon spirit skanda siva shiva vishnu kama devotion holy ritual altar shrine'.split(),
 'animal': 'fish bird cow bull ox buffalo deer stag goat sheep dog cat tiger elephant horse snake crocodile antelope peacock insect animal beast carp crab turtle fowl cattle lion'.split(),
 'plant': 'tree leaf leaves grass flower fruit plant bamboo branch root creeper herb shrub thorn palm banyan reed cotton-plant bud sprout seedling'.split(),
 'quality': 'big small great high low good bad old new young full many few strong beautiful hot cold white black red long short broad wide narrow thick thin heavy light sweet bitter fine excellent noble true false pure foolish wicked mean ugly equal whole entire much all each every some very'.split(),
}
LEX2CAT = {'noun.person': 'person', 'noun.animal': 'animal', 'noun.plant': 'plant', 'noun.food': 'commodity', 'noun.substance': 'commodity',
           'noun.possession': 'commodity', 'noun.time': 'time', 'noun.location': 'place', 'noun.quantity': 'measure', 'noun.artifact': 'tool',
           'noun.act': 'action', 'noun.event': 'action', 'noun.process': 'action', 'noun.motion': 'action', 'noun.attribute': 'quality',
           'noun.state': 'quality', 'noun.feeling': 'quality', 'noun.group': 'person'}
STOP = set('a an the of to in on at by for with from as and or is are be been being it its this that those these who which what one-who any some into out up down off over under than then so such not no also etc id cf esp usu usually especially especially fig lit used use act state thing things sort kind manner way person-who'.split())
STOP.discard('one')   # number word
STOP = STOP - set(KW['number'])
_stem = {}
for c, ws in KW.items():
    for w in ws: _stem.setdefault(w, c)
_wn = None
def wn():
    global _wn
    if _wn is None:
        import nltk; nltk.data.path.insert(0, '/tmp/nltk_data')
        from nltk.corpus import wordnet
        _wn = wordnet
    return _wn
def tok_cats(t, use_wn=True):
    out = set()
    for stem, c in _stem.items():
        if t == stem or (len(stem) >= 4 and (t.startswith(stem) or (len(t) >= 4 and stem.startswith(t) and len(t) >= len(stem) - 1))):
            out.add(c)
    if out or not use_wn: return out
    try:
        W = wn(); ss = W.synsets(t)
        if ss:
            ln = ss[0].lexname()
            if ln in LEX2CAT: out.add(LEX2CAT[ln])
            elif ln.startswith('verb.'): out.add('action')
            elif ln.startswith('adj'): out.add('quality')
        else:
            m = W.morphy(t)
            if m and m != t: return tok_cats(m, use_wn)
    except Exception:
        pass
    return out
def phrase_cats(ph, use_wn=True):
    p = ph.lower().strip()
    toks = [t for t in re.findall(r"[a-z]+", p) if t not in STOP]
    cats = set()
    if re.match(r'^to\s', p): cats.add('action')
    for t in toks[:5]: cats |= tok_cats(t, use_wn)
    return sorted(cats)
def strip_marks(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if c not in '̣̱̥̇̃́̀')
    s = re.sub(r"[^a-z̄ā-ſ]", '', s)
    return unicodedata.normalize('NFC', s)
def word_key(w):
    w = re.sub(r'\(.*?\)', '', w); w = w.replace('?', '').strip('- ').strip()
    return strip_marks(w)
def clean_gloss(g, maxw=8):
    """split a dictionary gloss into short sense phrases"""
    g = re.sub(r'\([^)]*\)', ' ', g); g = re.sub(r'\[[^\]]*\]', ' ', g)
    out = []
    for p in re.split(r'[;,]', g):
        p = re.sub(r'\s+', ' ', p).strip(' .:')
        p = re.sub(r'^(n|adj|adv|v|vt|vi|id|cf|esp|also|usu|pl|mfn)\.?\s+', '', p, flags=re.I)
        if not p or len(p) < 2: continue
        if re.search(r'[^\x00-\x7f]', p): continue            # non-Latin script left: not an English gloss
        if re.search(r'-pp-|-tt-|-v-|-nt-|\bKoll|\bsyn\b|combination of', p): continue
        p = ' '.join(p.split()[:maxw])
        out.append(p.lower())
    return out
