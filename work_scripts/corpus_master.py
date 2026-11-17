#!/usr/bin/env python3
"""Merge the value tables into one master table: work_data/values_master.csv

Inputs : work_data/sound_v4/values_v4.csv   (fourth pass, 98 values)
         work_data/holes/values_eight.csv   (the eight silent signs + two taken-as-given)
         clash answers from clash_335.py / clash_527.py (set in CLASH below)
Columns: sign, sound, english, dedr, status, report, alt_sound, alt_english, alt_report, short, note
status : strict  = building on (or base) and the fact that promoted it was fresh (or a base value)
         wide    = building on, but promoted on a fact that had been visible while choosing, or taken from the
                   eight-signs report, or a sign read by the same-word rule (525/526)
         testing / paused as in the reports
Same-sign conflicts between the two tables (beyond the two clashes): the word whose status is higher wins
(strict > wide > testing > paused); tie -> the fourth-pass word.  The loser goes in alt_*.
dedr   : only a number that is written in a report AND whose entry in the local DEDR copy has the sound among its Tamil
         words; or a number the reports give for that word (eight-signs table, kalam 1305); otherwise empty.
short  : the short English the corpus builder uses (derived from english; manual list SHORT_FIX for the awkward ones).
"""
import sys, os, re, csv, collections
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = '/home/claude/ivc'
from sound_dedr import look

V4 = pd.read_csv(f'{ROOT}/work_data/sound_v4/values_v4.csv', dtype=str).fillna('')
V8 = pd.read_csv(f'{ROOT}/work_data/holes/values_eight.csv', dtype=str).fillna('')
RANK = {'strict': 3, 'wide': 2, 'testing': 1, 'paused': 0}

rows = {}   # sign -> dict
for r in V4.itertuples():
    tier = r.tier_v4
    st = 'strict' if tier in ('base', 'building') and r.basis != 'seen' else 'wide' if tier == 'building' else tier
    rows[r.sign] = dict(sign=r.sign, sound=r.sound, english=r.english, dedr='', status=st, report='sound_list_v4.md', alt_sound='', alt_english='',
                        alt_report='', note=r.note[:160] if tier != 'base' else '')
# the eight-signs table
eight = []
for r in V8.itertuples():
    signs = r.sign.split('/')
    st = 'wide' if r.status.startswith('building') else 'testing'
    for s in signs:
        eight.append(dict(sign=s, sound=r.sound, english=r.english, dedr=r.dedr, status=st, report='eight_signs.md', alt_sound='', alt_english='', alt_report='',
                          note=r.status[:160]))
for e in eight:
    s = e['sign']
    if s not in rows:
        rows[s] = e; continue
    cur = rows[s]
    if RANK[e['status']] > RANK[cur['status']]:   # eight-signs word wins; fourth-pass word goes to alt
        e['alt_sound'], e['alt_english'], e['alt_report'] = cur['sound'], cur['english'], cur['report']; rows[s] = e
    else:
        cur['alt_sound'], cur['alt_english'], cur['alt_report'] = e['sound'], e['english'], e['report']

# 060: the eight-signs report ran the grammar test (locative leads, genitive second); its word is the winner here
_c = rows['060']
if _c['sound'] != 'uḷ':
    _o = [e for e in eight if e['sign'] == '060'][0]
    _o.update(alt_sound=_c['sound'], alt_english=_c['english'], alt_report=_c['report']); rows['060'] = _o
for _r in rows.values():
    if _r['alt_sound'] == '?': _r['alt_sound'] = _r['alt_english'] = _r['alt_report'] = ''

# ---- the two clash answers (work_data/clash/*.csv, clash_335.py, clash_527.py) ----
def clash(sign, win_sound, win_en, win_dedr, win_status, lose_sound, lose_en, lose_dedr, note):
    cur = rows.get(sign, dict(sign=sign, sound='', english='', dedr='', status='', report='', alt_sound='', alt_english='', alt_report='', note=''))
    cur.update(sound=win_sound, english=win_en, dedr=win_dedr, status=win_status, report='clash_335/527 (jobs/out/corpus_english.md)',
               alt_sound=lose_sound, alt_english=lose_en, alt_report=f'eight_signs.md / sound_list_v4.md (DEDR {lose_dedr})', note=note)
    rows[sign] = cur

clash('335', 'ūr', 'town', '', rows['335']['status'] or 'strict', 'kūṭu', 'bin, grain receptacle', '1883',
      'CLASH 335: ur wins (jar/maka after 62% vs 9.7%, 4 of 6 new texts; no tall count 0 of 26); bin wins only on the one Harappa grain formula')
for s in ('525', '526', '527'):
    clash(s, 'kāval', 'guard (vāy kāval "gate-guard"); 525/526 are drawings of the same word', '1416' if s == '527' else '1416',
          'strict' if s == '527' else 'wide', 'katavu', 'door', '1187',
          'CLASH 527: kaaval wins (jar on 11% vs 33%, last 83% vs 29%, count beside 5% vs 24%, name part before gate; new texts 7 of 9 last)')
rows['527']['status'] = 'strict'

# ---- DEDR numbers: harvested from the reports, kept only if the local DEDR entry has the sound ----
harvest = collections.defaultdict(set)
for f in ('sound_list.md', 'sound_list_v2.md', 'sound_list_v3.md', 'sound_list_v4.md', 'long_texts.md', 'goods.md', 'beads_cotton.md', 'cotton_house.md'):
    for line in open(f'{ROOT}/jobs/out/{f}', encoding='utf-8'):
        m = re.match(r'\|\s*(\d{3})\s*\|', line)
        if m:
            for x in re.findall(r'\[(\d{3,4})\]', line) + re.findall(r'DEDR (\d{3,4})', line): harvest[m.group(1)].add(x)
KNOWN = {'705': '1305', '706': '1305', '413': '1193', '540': '4032', '097': ''}   # 705/706 stated in sound_list_v4.md; 413, 540 stated in reports
def clean(snd): return re.sub(r'[()\-]', '', snd).strip()
for s, r in rows.items():
    if r['dedr']: continue
    if s in KNOWN and KNOWN[s]: r['dedr'] = KNOWN[s]; continue
    snd = clean(r['sound'])
    if not snd or ' ' in snd or snd == '?': continue
    hits = {k for k, t in look(snd, 5)}                         # entries whose Tamil words hold the sound
    cand = [x for x in harvest.get(s, ()) if x in {k for k, t in look(snd, 5)}]
    if cand: r['dedr'] = '/'.join(sorted(cand))

# ---- short English for the corpus builder ----
SHORT_FIX = {
 '001': 'one', '002': 'two', '003': 'three', '004': 'four', '005': 'five', '006': 'six', '007': 'seven',
 '048': 'the Seven', '055': 'dozen', '060': 'in', '061': 'quarter', '070': 'arrow', '090': 'manager', '091': 'the pair', '095': 'staff-bearer',
 '097': 'bondsman', '100': 'elder', '104': 'goldsmith', '125': 'Hunter', '137': 'cultivator', '140': 'lady', '142': 'king', '165': 'day',
 '171': 'full measure', '175': 'tax', '176': 'tax', '220': 'Star', '226': 'fish-crate', '231': 'First-star', '233': 'scabbard-fish', '235': 'Bamboo-star',
 '240': 'High-star', '255': 'chief', '320': 'ration measure', '335': 'town', '350': 'name-front', '368': 'banner', '382': 'King', '384': 'King', '388': 'King',
 '390': 'warrior', '391': 'smith', '400': 'junior', '405': 'kindred', '407': 'herd', '413': 'grain', '415': 'Branch', '416': 'grain-heap', '417': 'carrying-pole',
 '435': 'rod', '440': 'received', '455': 'arrow', '460': 'Three-peaks', '463': 'Three-peaks', '480': 'seed-weight', '482': 'hill-share', '495': 'branch',
 '500': 'sail', '501': 'heap', '503': 'hill', '520': 'chief', '525': 'guard', '526': 'guard', '527': 'guard', '530': 'proclamation', '540': 'rice measure', '550': 'gate', '555': 'gate',
 '575': 'great measure', '585': 'maiden', '590': 'chest', '595': 'forge', '605': 'granary', '611': 'Umbrella', '615': 'field', '617': "king's servant",
 '630': 'many', '632': 'many', '636': 'many', '645': 'mark', '679': 'throne', '690': 'bound', '692': 'district', '700': 'cup', '705': 'kalam', '706': 'kalam',
 '711': 'pot', '717': 'servant', '740': 'house', '741': 'first-ward house', '742': 'second-ward house', '745': 'third-ward house', '752': 'child of', '760': 'child of',
 '790': 'gem', '798': 'descendant', '803': 'house', '806': 'produce', '817': 'share', '820': 'quarter', '824': 'price', '831': 'millet', '832': 'place', '838': 'bone',
 '840': 'pair', '842': 'deputy', '845': 'sheaf-bundle', '850': 'eye', '861': 'share', '877': 'four shares', '890': 'given', '892': 'sale', '900': 'month', '904': 'two months',
 '920': 'month', '923': 'crescent-horn', '236': 'Bamboo-star cluster', '167': 'tablet-word', '368': 'banner', '530': 'proclamation',
}
for s, r in rows.items():
    if s in SHORT_FIX: r['short'] = SHORT_FIX[s]
    elif r['sound'] == '(n)' or s in [str(i) for i in range(465, 476)]: r['short'] = 'n loads'
    elif s in ('012', '013', '014', '015', '016', '017', '018', '031', '032', '033', '034', '035', '036'): r['short'] = r['english']
    elif s in ('151', '153', '154', '155', '156', '157', '158'): r['short'] = 'keeper'
    else: r['short'] = re.split(r'[;(,"]', r['english'])[0].strip()

cols = ['sign', 'sound', 'english', 'dedr', 'status', 'report', 'alt_sound', 'alt_english', 'alt_report', 'short', 'note']
out = pd.DataFrame([rows[s] for s in sorted(rows)])[cols]
out.to_csv(f'{ROOT}/work_data/values_master.csv', index=False)
print('master rows', len(out), out.status.value_counts().to_dict(), '| with DEDR', int((out.dedr != '').sum()), '| with alt word', int((out.alt_sound != '').sum()))
