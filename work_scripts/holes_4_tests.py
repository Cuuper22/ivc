#!/usr/bin/env python3
"""First-try tests for the eight signs.  PREDICTIONS were fixed (written here) before this script was first run, 2026-11-17.

060  uḷ "in" (locative; DEDR 698)  -> see holes_3_060.py (predictions there).
692  teru "street" (DEDR 3422), a place head like gate 550 / quarter 820, not a time word like month 920.
     P692a: after 692-060 the ward jars (741/742/745) are under 15% of cases (month 920 has 76%).
     P692b: 692 shares a line with another place head (550, 820) less than chance, and with the month 920 not more than chance
            (a day-of-month reading would put 692 with 920).
     P692c: 692 sits in the two big planned cities (Mohenjo-daro + Harappa) at 0.88 or more (all lines 0.82).
     P692d (second catalogue, Mahadevan 150): first in the line in 70% or more; 123 (=060) right after it in 60% or more.
525  katavu "door" (DEDR 1187), the 52x box-with-bars family 525/526/527 is one word that stands only after the gate word 550.
     P525a: 525, 526, 527 never share a line; each stands directly after 550 in 75% or more of its uses.
     P525b: 525 is followed by the comb 400 (ciṟ "small/junior") in 70% or more of uses, and is on tablets only; 527 (same slot) is on seals.
     P525c (second catalogue): Mahadevan partner of 525 has the Mahadevan partner of 550 on its left in 70% or more.
335  kūṭu "bin, grain receptacle" (DEDR 1883); 711 pāṉai "pot, a measure" (DEDR 4124).
     P335a: 335 is on tablets (Lipi types TAB) at a higher share than all lines (0.37): 55% or more.
     P335b: 335 follows 575 (kōṭṭai) in 40% or more of its uses and is followed by 711 or jar 740/760 (container or house word) in 70% or more.
     P711a: the count right after 711 is a tall stroke (container series) in 80% or more of counted uses (base 35%).
     P711b: in the grain frame 413-575-335-_-count-_ the slot of 711 is filled only by 711 or the jar 740, never by a different kind of sign.
     P711c: 711 and the jar 740 are both followed by a count of 2 or 3 in the grain frame: all counts after the slot are 2 or 3.
842  tuṇai "helper, companion, second" (DEDR 3308), a closer in the place of the jar.
     P842a: 842 is last in the line in 5 of 5 and the line has no jar.
     P842b: lines ending in 842 are second lines of two-line seals at a higher rate than jar closers are.
     P842c: median face area of 842 seals is 640 mm2 or smaller (comb 420, carrier 495, jar 645).
     P842d: it is a closer family member: preceded by a sign that is a name-end/last-slot sign (slot_table 'last' >= .3) in 3 of 5.
611  kuṭai "umbrella, royal parasol" (DEDR 1663): a name part (house/ruler name), not a title and not a place.
     P611a: not a place: of its uses at most 1/3 at one site.  P611b: not a title: left neighbour is a name word, never.
     P611c: kāl (820) is on its left in 2 or more of 6, a title/jar or aracu on its right.
645  kuṟi "mark, tally" (DEDR 1847): a counted unit and name-part; on goods, not seals.
     P645a: non-seal objects 50% or more (all lines 0.53 non-seal).  P645b: a count is directly before it in 40% or more (13/28 earlier).
     P645c: it sits in the slot of the chief 255 in a fixed seal frame (645-070-741-150-267-840-032 against 255-070-...).
     P645d: on pots the count before it is 1 or 2.
"""
import sys, collections, math, statistics
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from holes_common import *
import pandas as pd
ls = lines(True)
N = len(ls)
FISH = {'220','235','240','233','231','226','236'}
WARD = {'741','742','745'}
out = []
def P(s): out.append(s); print(s)
def binom_p(k, n, p0):
    """one-sided P(X>=k) for X~Bin(n,p0)"""
    s = 0.0
    for i in range(k, n + 1): s += math.comb(n, i) * p0 ** i * (1 - p0) ** (n - i)
    return s
def right_of(a, ls_=ls):
    return [(i, p) for i, L in enumerate(ls_) for p, s in enumerate(L['toks']) if s == a]

# ---------------- 692
P('=== 692 teru "street"')
c = collections.Counter(); n = 0
for head in ['692', '920', '550', '820']:
    n = 0; w = 0
    for L in ls:
        t = L['toks']
        for p in range(len(t) - 2):
            if t[p] == head and t[p + 1] == '060':
                n += 1; w += t[p + 2] in WARD
    P(f'P692a  after {head}-060 a ward jar follows: {w} of {n} ({w/max(n,1):.2f})')
heads = ['692', '920', '550', '820']
lineset = {h: {i for i, L in enumerate(ls) if h in L['toks']} for h in heads}
for a, b in [('692', '550'), ('692', '820'), ('692', '920'), ('550', '820'), ('920', '550'), ('920', '820')]:
    both = len(lineset[a] & lineset[b]); exp = len(lineset[a]) * len(lineset[b]) / N
    P(f'P692b  lines with {a} and {b}: {both}; expected by chance {exp:.1f}')
U = right_of('692'); k = sum(1 for i, _ in U if ls[i]['site'] in ('Mohenjo-daro', 'Harappa'))
base = sum(1 for L in ls if L['site'] in ('Mohenjo-daro', 'Harappa')) / N
P(f'P692c  692 in Mohenjo-daro + Harappa: {k} of {len(U)} = {k/len(U):.2f}; all lines {base:.2f}; one-sided binomial P {binom_p(k, len(U), base):.4f}')
M = mah_lines(); first = after = tot = 0
for r in M:
    t = r['toks']
    for p, s in enumerate(t):
        if s == 150:
            tot += 1; first += p == 0; after += (p + 1 < len(t) and t[p + 1] == 123)
P(f'P692d  Mahadevan 150: {tot} uses, first in line {first} ({first/tot:.2f}), 123 right after {after} ({after/tot:.2f})')

# ---------------- 525 family
P('=== 525 katavu "door" (525/526/527)')
for s in ['525', '526', '527']:
    U = right_of(s); a550 = sum(1 for i, p in U if p > 0 and ls[i]['toks'][p - 1] == '550')
    kd = collections.Counter(kind(ls[i]['type']) for i, _ in U)
    nx = collections.Counter((ls[i]['toks'][p + 1] if p + 1 < len(ls[i]['toks']) else '$') for i, p in U)
    P(f'P525a  {s}: {len(U)} uses, directly after 550: {a550} ({a550/max(len(U),1):.2f}); kinds {dict(kd)}; next {dict(nx.most_common(4))}')
sh = sum(1 for L in ls if '525' in L['toks'] and ('526' in L['toks'] or '527' in L['toks']))
sh2 = sum(1 for L in ls if '526' in L['toks'] and '527' in L['toks'])
P(f'P525a  lines with two of the three signs: 525&(526|527) {sh}; 526&527 {sh2}')
import csv
cw = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
mp = {}
for s in ['525', '526', '527', '550', '400']:
    r = cw[cw.lipi == s]
    mp[s] = [int(x) for x in r.mahadevan.tolist()]
P(f'P525c  crosswalk partners {mp}')
if mp['525']:
    m525 = set(mp['525']); m550 = set(mp['550']); m400 = set(mp['400'])
    tot = l550 = r400 = 0
    for r in M:
        t = r['toks']
        for p, s in enumerate(t):
            if s in m525:
                tot += 1; l550 += (p > 0 and t[p - 1] in m550); r400 += (p + 1 < len(t) and t[p + 1] in m400)
    P(f'P525c  Mahadevan {sorted(m525)}: {tot} uses, 550-partner on its left {l550}, comb-partner on its right {r400}')

# ---------------- 335 / 711
P('=== 335 kūṭu "bin" and 711 pāṉai "pot"')
for s in ['335', '711']:
    U = right_of(s); tab = sum(1 for i, _ in U if kind(ls[i]['type']) == 'TAB')
    tb = sum(1 for L in ls if kind(L['type']) == 'TAB') / N
    P(f'P335a  {s}: on tablets {tab} of {len(U)} = {tab/len(U):.2f}; all lines {tb:.2f}; binomial P {binom_p(tab, len(U), tb):.2e}')
U = right_of('335'); a575 = sum(1 for i, p in U if p > 0 and ls[i]['toks'][p - 1] == '575')
nx = sum(1 for i, p in U if p + 1 < len(ls[i]['toks']) and ls[i]['toks'][p + 1] in ('711', '740', '760'))
P(f'P335b  335: after 575 {a575} of {len(U)} = {a575/len(U):.2f}; followed by 711/740/760 {nx} of {len(U)} = {nx/len(U):.2f}')
U = right_of('711'); tallset = {f'{k:03d}' for k in range(31, 36)}; shortset = {f'{k:03d}' for k in range(1, 9)}
tall = short = 0
for i, p in U:
    t = ls[i]['toks']
    if p + 1 < len(t):
        if t[p + 1] in tallset: tall += 1
        elif t[p + 1] in shortset: short += 1
base = 0.35
P(f'P711a  count after 711: tall {tall}, short {short}; tall share {tall/max(tall+short,1):.2f} (all counts 0.35); binomial P {binom_p(tall, tall+short, base):.2e}')
frame = collections.Counter(); cnts = collections.Counter(); tail = collections.Counter()
for L in ls:
    t = L['toks']
    for p in range(len(t) - 3):
        if t[p:p + 3] == ('413', '575', '335'):
            frame[t[p + 3]] += 1
            if p + 4 < len(t): cnts[t[p + 4]] += 1
            if p + 5 < len(t): tail[t[p + 5]] += 1
P(f'P711b  slot after 413-575-335 filled by: {dict(frame)}; count after it: {dict(cnts)}; sign after the count: {dict(tail)}')
P(f'P711c  every count after the slot is 032 or 033: {all(k in ("032","033","000") for k in cnts)}')

# ---------------- 842
P('=== 842 tuṇai "helper"')
U = right_of('842')
P(f'P842a  uses {len(U)}, last in line {sum(1 for i,p in U if p==len(ls[i]["toks"])-1)}, jar in the line {sum(1 for i,_ in U if "740" in ls[i]["toks"])}')
CLOSERS = {'740', '520', '400', '090', '151', '153', '154', '155', '156', '157', '158'}
def second_line_rate(pred):
    k = n = 0
    for L in ls:
        if kind(L['type']) != 'SEAL' or not L['toks']: continue
        if pred(L['toks'][-1]):
            n += 1; k += L['line'] >= 2
    return k, n
k, n = second_line_rate(lambda s: s in CLOSERS)
P(f'P842b  seal lines ending in a known closer that are line 2 or later: {k} of {n} = {k/n:.3f}; lines ending in 842 that are line 2+: ' + str(sum(1 for i,_ in U if ls[i]['line']>=2)) + ' of ' + str(len(U)))
areas = []
raw = pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv', dtype=str).fillna('')
for i, _ in U:
    r = raw[raw.id.str.startswith(ls[i]['obj'] + '.')].iloc[0]
    try: areas.append(float(r['horizontal(mm)']) * float(r['vertical(mm)']))
    except: pass
P(f'P842c  face areas of the 842 seals (mm2): {[round(a) for a in areas]}; median {statistics.median(areas) if areas else None}')
st = pd.read_csv(f'{ROOT}/work_data/slot_table.csv', dtype=str).set_index('sign')
for i, p in U:
    s = ls[i]['toks'][p - 1]
    r = st.loc[s] if s in st.index else None
    P(f'P842d  {ls[i]["cisi"]}: sign before = {s}; slot-table last share {r["last"] if r is not None else "n/a"} (texts {r["texts"] if r is not None else "n/a"})')

# ---------------- 611
P('=== 611 kuṭai')
U = right_of('611')
P(f'P611a  sites {dict(collections.Counter(ls[i]["site"] for i,_ in U))}')
for i, p in U:
    t = ls[i]['toks']
    P(f'P611   {ls[i]["cisi"]} {ls[i]["type"]} {ls[i]["site"]}: ' + '-'.join(f'{s}[{snd(s) or "?"}]' for s in t) + f'   (611 at place {p+1} of {len(t)})')
# ---------------- 645
P('=== 645 kuṟi')
U = right_of('645'); ns = sum(1 for i, _ in U if kind(ls[i]['type']) != 'SEAL'); bs = sum(1 for L in ls if kind(L['type']) != 'SEAL') / N
P(f'P645a  non-seal {ns} of {len(U)} = {ns/len(U):.2f}; all lines {bs:.2f}; binomial P {binom_p(ns, len(U), bs):.2e}')
cb = sum(1 for i, p in U if p > 0 and ls[i]['toks'][p - 1] in CNT)
P(f'P645b  count directly before: {cb} of {len(U)} = {cb/len(U):.2f}')
fr = [(L['cisi'], '-'.join(L['toks'])) for L in ls if '070' in L['toks'] and '741' in L['toks'] and '267' in L['toks']]
P(f'P645c  frame ...070-741-150-267-840-032 : {fr}')
pots = [('-'.join(ls[i]['toks'])) for i, _ in U if kind(ls[i]['type']) == 'POT']
P(f'P645d  pot lines with 645: {pots}')
open(f'{HOLES}/tests_first_try.txt', 'w').write('\n'.join(out))
