#!/usr/bin/env python3
"""GULF job step 1: score every round seal we already hold for the unit [stroke(s)][person].
PREDICTION fixed before running (from the job brief): if [stroke][person] is a number of persons, other counts (2,3,4) appear;
if a fixed title/name element, the stroke stays 'one' (001, or the dozen sign 055); if chance, absent.
Writes work_data/gulf/ours_scored.csv and prints the summary. Plain csv + stdlib only.
"""
import csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHORT = ['001','002','003','004','005','055']; TALL = ['031','032','033','034','035','036']
PERSON = ['090','091','093','095']
rows = list(csv.DictReader(open(f'{ROOT}/work_data/round/round_list.csv', dtype=None) if False else open(f'{ROOT}/work_data/round/round_list.csv')))
phr = [r['phrase'] for r in csv.DictReader(open(f'{ROOT}/work_data/phrases/phrase_list.csv'))]
phr_t = [tuple(p.split('-')) for p in phr]
def has_run(t, p):
    return any(tuple(t[i:i+len(p)]) == p for i in range(len(t)-len(p)+1))
out = []
for r in rows:
    t = [x for x in r['text'].split('-') if x]
    n = len(t)
    unit = [(i, t[i], t[i+1]) for i in range(n-1) if t[i] in SHORT and t[i+1] in PERSON]
    unit_tall = [(i, t[i], t[i+1]) for i in range(n-1) if t[i] in TALL and t[i+1] in PERSON]
    rev = [(i, t[i], t[i+1]) for i in range(n-1) if t[i] in PERSON and t[i+1] in SHORT+TALL]
    ph = [ '-'.join(p) for p in phr_t if len(p) >= 2 and has_run(t, p)]
    out.append(dict(id=r['id'], where=r['tier'], site=r['site'], animal=r['animal'], text=r['text'], n_signs=n,
        unit_short_person=';'.join(f'{a}-{b}@{i+1}of{n}' for i,a,b in unit),
        unit_tall_person=';'.join(f'{a}-{b}@{i+1}of{n}' for i,a,b in unit_tall),
        person_then_stroke=';'.join(f'{a}-{b}' for i,a,b in rev),
        has_person=int(any(x in PERSON for x in t)),
        person_last=int(n>0 and t[-1] in PERSON),
        has_740=int('740' in t), ends_740=int(n>0 and t[-1]=='740'),
        home_phrases=';'.join(ph)))
os.makedirs(f'{ROOT}/work_data/gulf', exist_ok=True)
with open(f'{ROOT}/work_data/gulf/ours_scored.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
def show(name, sel):
    s = [o for o in out if sel(o) and o['n_signs']>=2]
    print(f"{name}: {len(s)} texts with >=2 signs; unit(short+person) {sum(bool(o['unit_short_person']) for o in s)}; "
          f"tall+person {sum(bool(o['unit_tall_person']) for o in s)}; person present {sum(o['has_person'] for o in s)}; "
          f"person last {sum(o['person_last'] for o in s)}; 740 present {sum(o['has_740'] for o in s)}; 740 last {sum(o['ends_740'] for o in s)}; "
          f"home phrase present {sum(bool(o['home_phrases']) for o in s)}")
show('all round (home+abroad+unknown)', lambda o: True)
show('abroad', lambda o: o['where']=='abroad')
show('unknown-site', lambda o: o['where']=='unknown site')
show('abroad+unknown', lambda o: o['where'] in ('abroad','unknown site'))
show('home round', lambda o: o['where']=='home')
print()
for o in out:
    if o['unit_short_person'] or o['unit_tall_person'] or o['home_phrases']:
        print(o['id'], o['where'], o['site'], o['animal'], o['text'], '| unit', o['unit_short_person'], '| tall', o['unit_tall_person'], '| phrases', o['home_phrases'])
# bull counts
fr = [o for o in out if o['where'] in ('abroad','unknown site') and o['n_signs']>=2]
b = lambda o: o['animal']=='SHORTHORN'
print('\nforeign round >=2 signs:', len(fr), 'bull', sum(map(b,fr)))
print('unit seals bull:', sum(b(o) for o in fr if o['unit_short_person']), 'of', sum(bool(o['unit_short_person']) for o in fr))
print('stroke signs used in the unit:', sorted({u.split('-')[0].split('@')[0] for o in out for u in o['unit_short_person'].split(';') if u}))
