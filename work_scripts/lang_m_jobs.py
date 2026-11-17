#!/usr/bin/env python3
"""lang_m step 2: JOBS. Every pictured sign -> one job class, from the template parser only (no word lists).

Faces: first catalogue (Lipi) + second catalogue (Mahadevan 1977) texts with no partner in the first, as parsed by gloss2.parse_face
(loaded through v2_common).  For each sign we count the parser roles over all its occurrences, and, where the parser calls it a
counted thing, which stroke series stands next to it (short / tall / stacked).

CLASS RULE (fixed before scoring; follows the class rule of blind2_build.py, split finer with the measured stroke facts):
  - fewer than 3 occurrences in all faces              -> dropped (no job measured)
  - counted (role 'counted', 'load-crop', 'load-thing') on at least 25% of its occurrences and at least 3 times:
        series most often beside it: tall  -> MEASURE   (counted with full-height strokes: container / measure)
                                     short -> COUNTED   (counted with short strokes: living thing / produce)
                                     stacked -> TIME    (stacked strokes; the calendar-like counts)
  - otherwise the top parser role:  opener -> OPENER; crest -> CREST; self -> NAME (personal name part); tag -> TAG (name ending part);
        ending / relation / tail / poss / load-carried -> TITLE (ending / title after the name)
        counted (under 25%) -> as above by series;  count, load-count, lost, none -> dropped.
  There is no PLACE class: the parser has no slot for place words, so no sign is put there.
Output: work_data/lang_m/jobs.csv (sign, nouns, job, occurrences, role counts, series counts)
"""
import sys, os, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_common as v
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/lang_m'
def log(*a): print('[lang_m_jobs]', *a, flush=True)

faces = [(tuple(x), p['roles']) for x, p, _, _ in v.faces_all('LM')]
log(f'{len(faces)} faces (Lipi + unpartnered Mahadevan)')
roles = collections.defaultdict(collections.Counter); series = collections.defaultdict(collections.Counter); occ = collections.Counter()
for x, R in faces:
    for i, (s, r) in enumerate(zip(x, R)):
        occ[s] += 1; roles[s][r] += 1
        if r in ('counted', 'load-crop', 'load-thing'):
            for j in (i - 1, i + 1):
                if 0 <= j < len(x) and x[j] in v.CNT and v.CNT[x[j]][0] in ('short', 'tall', 'stacked'):
                    series[s][v.CNT[x[j]][0]] += 1; break
SER = {'tall': 'MEASURE', 'short': 'COUNTED', 'stacked': 'TIME'}
TOP = {'opener': 'OPENER', 'crest': 'CREST', 'self': 'NAME', 'tag': 'TAG', 'ending': 'TITLE', 'relation': 'TITLE', 'tail': 'TITLE',
       'poss': 'TITLE', 'load-carried': 'TITLE'}

def job(s):
    if occ[s] < 3: return None
    cnt = sum(roles[s][k] for k in ('counted', 'load-crop', 'load-thing'))
    if cnt >= 3 and cnt / occ[s] >= 0.25 and series[s]: return SER[series[s].most_common(1)[0][0]]
    top = roles[s].most_common(1)[0][0]
    if top in TOP: return TOP[top]
    if top in ('counted', 'load-crop', 'load-thing') and series[s]: return SER[series[s].most_common(1)[0][0]]
    return None

pics = list(csv.DictReader(open(f'{OUT}/pictures.csv', encoding='utf-8')))
out = []
for p in pics:
    j = job(p['sign'])
    if j: out.append(dict(sign=p['sign'], nouns=p['nouns'], job=j, occ=occ[p['sign']],
                          roles=';'.join(f'{k}:{n}' for k, n in roles[p['sign']].most_common()),
                          series=';'.join(f'{k}:{n}' for k, n in series[p['sign']].most_common())))
with open(f'{OUT}/jobs.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
log(f'{len(pics)} pictured signs -> {len(out)} with a job; by job:', dict(collections.Counter(o["job"] for o in out)))
