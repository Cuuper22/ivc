#!/usr/bin/env python3
"""JOB 3b: FRAMEBOOK.md (repo root) from work_data/frame/corpus_jobs.csv. Examples drawn by seed 17, spread over sites
(round robin over the sites holding that kind, biggest site first). No words for signs: pictures and jobs only."""
from frame2_common import *
from frame2_pictures import pic, pic_book, BLIND

R = pd.read_csv(f'{OUT2}/corpus_jobs.csv', dtype=str).fillna('')
V2B = dict(zip(*[pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')[c] for c in ('sign', 'v2_base')]))
SHORTJOB = {'OPEN': 'front', 'SLOT': 'slot', 'CREST': 'crest', 'PERSONAL': '', 'NUM_NAME': 'name number', 'NUM_SHORT': 'number',
            'NUM_TALL': 'tall number', 'MEASURE': 'measure', 'AFTER_M': 'after-measure', 'THING': 'counted', 'NAME_BACK': 'name back',
            'PLACE': 'place', 'CLOSER': 'closer', 'TITLE': 'title'}


def words(signs):
    out = []
    for s in signs.split('-'):
        j = SHORTJOB.get(V2B.get(s, 'PERSONAL'), '')
        out.append(f'[{pic_book(s)}{" · " + j if j else ""}]')
    return ' '.join(out)


ORDER = ['name text', 'loose name text', 'opener + count line', 'bare count line', 'record', 'measure line', 'title alone', 'front alone', 'one picture', 'other', 'damaged']
ABOUT = {
    'name text': 'A name with its ending: [front word + slot]? [name signs] [closer] [title]?. The main seal text.',
    'loose name text': 'Holds a closer or title but breaks the strict order somewhere (a name sign after the closer, two closers, a front word inside).',
    'opener + count line': 'A front word and its slot, then a count and a counted thing, with no name and no ending: [front][slot][number][counted thing]. The second kind of seal.',
    'bare count line': 'Only a count and a counted thing: [number][counted thing]. On tablets this is the cup with tall strokes; on seals a short count with a tree or a porter.',
    'record': 'A name text, its closer, then a count line after it. Mostly copper tablets.',
    'measure line': 'A measure sign with its follower or a number, sometimes closed: [measure][after-measure or number][closer]?',
    'title alone': 'One closer or title sign standing alone.',
    'front alone': 'A front word (with its slot) standing alone.',
    'one picture': 'One sign on a copper tablet, the sign that copies the picture on the other side.',
    'other': 'Undamaged texts that fit none of the patterns above.',
    'damaged': 'A lost or unclear sign or a broken edge. Restorations are in work_data/frame/corpus_jobs.csv.',
}
rng = np.random.default_rng(17)
L = []
w = L.append
w('# FRAMEBOOK: the Indus corpus written in jobs')
w('')
w('A word-free book of every inscription in the first catalogue (5,679 inscribed faces), built 2026-11-17 by `work_scripts/frame2_corpus.py` and `frame2_book.py`. Each sign is written as a picture-word (what it looks like) with its job after a dot. Nothing here says what any sign means or how it sounds.')
w('')
w('## Key (half a page)')
w('')
w('- **Sign**: one drawn character, cited by its catalogue number (740 = the jar picture). Texts are given in reading order.')
w('- **Picture-word**: a short name for what the sign looks like: the things two or three blind describers agreed on for the matching second-catalogue drawing (`work_data/pictures/pictures_blind.csv`, through the crosswalk; two things joined by `/` when both were agreed), and otherwise a name from the catalogue shape descriptions (all stroke numbers are named by count). The sign number is always given beside the example, so variants that share a picture-word stay apart. `[jar · closer]` = the jar picture, doing the closer job. A bare `[fish]` with no job = an ordinary name sign.')
w('- **Jobs (frame v2)**: each sign has one job, learned from where it stands, never from a meaning:')
for c in V2_CLASSES: w(f'  - **{V2_PLAIN[c]}** (`{c}`)')
w('- **Object kinds**: seals (stone stamps), tablets (small incised or moulded plaques), copper tablets, tags and sealings (clay lumps pressed on goods), pots (marks on pottery), other objects.')
w('- **Text kind**: which pattern of the grammar a whole text fits (list below).')
w('')
w('## The grammar, in plain words')
w('')
w('1. A text may open with a **front word** (signs 861, 817, 820, 920, 692, 550 and a few more). A front word is followed by its own **slot** sign (002, 060, 741, 742, 368, 365).')
w('2. After the front, either a **name** or a **count line** follows.')
w('3. A **name** is one to three signs: usually a **crest** first (a fish sign 220/231/233/235/240, or 803/806/140), then name parts, sometimes a **name back** sign just before the end. The two tall strokes (032) live inside names, mostly right before a fish.')
w('4. A name is shut by a **closer** (740, 520, porters 151/154/158). After the jar there may be one **after-jar title** (400, 090, 527, 621, 679 and a few others). 520 and the porters never follow 740; they stand in its place.')
w('5. A **count line** is a **number** followed by a **counted thing** (trees 390/405/407, porter with jars 156, cup 700). Short strokes count trees and porters on seals; tall strokes count cups on tablets.')
w('6. A **measure** sign is followed by its own follower (033, 760, 690) and often by a closer.')
w('7. A **record** (mostly copper tablets) is a whole name text followed by a count line.')
w('8. Which job may follow which differs by object: after the closer, a title comes three times as often on tablets as on seals; pots are one or two signs; copper tablets carry records and single picture-signs.')
w('')
w('## Text kinds: counts by object kind')
w('')
ct = pd.crosstab(R.text_kind, R.object_kind)
cols = [c for c in ['seals', 'tablets', 'copper tablets', 'tags and sealings', 'pots', 'other objects'] if c in ct.columns]
w('| text kind | ' + ' | '.join(cols) + ' | all |')
w('|---|' + '---|' * (len(cols) + 1))
for k in ORDER:
    if k in ct.index: w(f'| {k} | ' + ' | '.join(str(int(ct.loc[k, c])) for c in cols) + f' | {int(ct.loc[k].sum())} |')
w('')
for k in ORDER:
    sub = R[R.text_kind == k]
    if not len(sub): continue
    w(f'## {k} ({len(sub)} faces)')
    w('')
    w(ABOUT[k])
    w('')
    sites = sub.site.value_counts().index.tolist()
    pick = []
    pools = {s: list(rng.permutation(sub[sub.site == s].index)) for s in sites}
    while len(pick) < 10 and any(pools.values()):
        for s in sites:
            if pools[s] and len(pick) < 10: pick.append(pools[s].pop())
    bysite = collections.defaultdict(list)
    for i in pick: bysite[R.loc[i, 'site']].append(i)
    for s in sites:
        if not bysite[s]: continue
        w(f'**{s}**')
        w('')
        for i in bysite[s]:
            r = R.loc[i]
            line = f'- `{r.signs}` ({r.object_kind}, {r.cisi}): {words(r.signs)}'
            if k == 'damaged' and r.restorations: line += f'  · restored: {r.restorations}'
            w(line)
        w('')
open(f'{ROOT}/FRAMEBOOK.md', 'w').write('\n'.join(L) + '\n')
log(f'FRAMEBOOK.md written: {len(L)} lines')
