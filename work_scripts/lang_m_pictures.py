#!/usr/bin/env python3
"""lang_m step 1: PICTURES. Every sign -> the concrete thing(s) its drawing shows, by a fixed rule on the shape words.

Input : work_data/sign_shapes.csv (Wells/Lipi number, plain-words description of the drawing). Nothing else is read.
Output: work_data/lang_m/pictures.csv  (sign, nouns 'a|b', rule note, description)

RULE (fixed before any score exists)
  1. Only the first sentence of the description is used (later sentences add cages, hats, brackets).
  2. Words inside quotes or a '(x? y?)' aside count too: they are the describer naming the thing ('garlic' motif, (arrow? spear?)).
  3. A concrete-noun vocabulary (THINGS below, a general list of drawable things, each with its spelling variants) is matched as
     whole words. Body parts used to describe a drawing (arms, legs of a person, head, wings, tail, whiskers, hat, handles) are not things.
     A thing-word used to describe the SHAPE of a head ('jar handles for a head', 'flag for a head') is not a thing in the picture.
  4. A sign is DROPPED as vague when: the description starts 'Unknown'; or its only thing-word sits in an 'X or <geometric word>'
     alternative ('leaf or diamond'); or no thing-word is found (strokes, U, X, H, boxes, triangles, parentheses ...).
  5. Number signs (stroke counts) are dropped (they are numbers, not pictures).
"""
import csv, re, os, collections
ROOT = '/home/claude/ivc'
OUT = f'{ROOT}/work_data/lang_m'; os.makedirs(OUT, exist_ok=True)

# canonical noun -> spellings that may appear in a shape description
THINGS = {
    'person': ['person', 'persons', 'people', 'man', 'men'], 'fish': ['fish'], 'bird': ['bird', 'birds'], 'duck': ['duck'],
    'jar': ['jar'], 'leaf': ['leaf', 'leaves'], 'tree': ['tree', 'trees'], 'plant': ['plant'], 'flower': ['flowering'],
    'sapling': ['sapling'], 'branch': ['branch', 'branching'], 'wheel': ['wheel', 'wheels'], 'bow': ['bow', 'bows'],
    'arrow': ['arrow', 'arrows'], 'spear': ['spear'], 'pitchfork': ['pitchfork', 'pitchforks', 'pitckfork'], 'table': ['table'],
    'deer': ['deer'], 'cow': ['cow', "cow's"], 'spider': ['spider'], 'wheat': ['wheat'], 'garlic': ['garlic'], 'heart': ['heart'],
    'ladder': ['ladder'], 'flag': ['flag', 'flags'], 'staff': ['staff', 'staves'], 'stick': ['stick'], 'burden': ['burden', 'burdens'],
    'pond': ['pond'], 'lyre': ['lyre'], 'paw': ['paw'], 'cat': ['cat', "cat's"], 'mountain': ['mountain'], 'wave': ['wave'],
    'pincers': ['pincer', 'pincers'], 'sun': ['sun'], 'rake': ['rake'], 'antenna': ['antenna', 'antennae'],
}
SPELL = {s: k for k, v in THINGS.items() for s in v}
GEOM = {'diamond', 'triangle', 'rectangle', 'square', 'box', 'circle', 'oval', 'u', 'x', 'h', 'm', 'a', 'w', 't', 'caret', 'lambda',
        'parenthesis', 'parentheses', 'grid', 'trapezoid', 'bowtie', 'stroke', 'strokes', 'line', 'lines'}
NUMBER_SIGNS = {f'{i:03d}' for i in list(range(1, 36)) + [44, 45, 46, 48, 49, 51, 55, 57, 58]}


def log(*a): print('[lang_m_pictures]', *a, flush=True)


def nouns_of(desc):
    first = desc.split('. ')[0]
    asides = ' '.join(re.findall(r"'([^']+)'", desc) + re.findall(r'\(([^)]*\?[^)]*)\)', desc))
    text = (first + ' ' + asides).lower()
    text = re.sub(r"[a-z']+( handles)? for a head", ' ', text)
    if text.strip().startswith('unknown'): return [], 'vague: unknown'
    # 'X or <geometric>' alternatives: drop that thing-word
    alt = set()
    for a, b in re.findall(r"([a-z']+) or ([a-z']+)", text):
        if a in SPELL and b in GEOM: alt.add(SPELL[a])
        if b in SPELL and a in GEOM: alt.add(SPELL[b])
    found = []
    for w in re.findall(r"[a-z']+", text):
        w2 = w.strip("'")
        k = SPELL.get(w) or SPELL.get(w2)
        if k and k not in found: found.append(k)
    keep = [k for k in found if k not in alt]
    if not keep: return [], ('vague: thing only as an alternative to a shape' if found else 'no thing-word')
    return keep, 'ok'


rows = list(csv.DictReader(open(f'{ROOT}/work_data/sign_shapes.csv', encoding='utf-8')))
out = []; why = collections.Counter()
for r in rows:
    s = r['lipi_wells_number']; desc = r['shape_description']
    if s in NUMBER_SIGNS: why['number sign'] += 1; continue
    n, note = nouns_of(desc)
    why[note] += 1
    if n: out.append(dict(sign=s, nouns='|'.join(n), note=note, desc=desc))
with open(f'{OUT}/pictures.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['sign', 'nouns', 'note', 'desc']); w.writeheader(); w.writerows(out)
log(f'{len(rows)} described signs -> {len(out)} with a picture noun; reasons: {dict(why)}')
log('nouns used:', collections.Counter(n for o in out for n in o['nouns'].split('|')).most_common())
