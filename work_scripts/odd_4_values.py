#!/usr/bin/env python3
"""Writes work_data/values_master2.csv: values_master.csv plus four slot columns (one English word per slot).
 name = the word used when the sign stands inside a name;  count = in a count line on goods (tablet, tag, pot ...);
 final = text-final after a name (a title);  open = at the front of a text (opener).
 Empty cell = use `short` as before. Words were fixed from the slot census (odd_1_slots.py) and the name-sense tests (odd_2_names.py)
 BEFORE the new draw of 60 (odd_6_draw.py)."""
import pandas as pd
ROOT = '/home/claude/ivc'
M = pd.read_csv(f'{ROOT}/work_data/values_master.csv', dtype=str).fillna('')
for c in ('short_name', 'short_count', 'short_final', 'short_open', 'slot_note'): M[c] = ''
SL = {
 '904': dict(short_name='Dark-moon', short_count='two months', slot_note='iru-tiṅkaḷ: iru = two and black (as iru-mīn); name word beside star signs (fish with it 23/46 against 29.5%); count word "two months"'),
 '900': dict(short_name='Moon', short_count='month', slot_note='tiṅkaḷ moon (name) / month (count line)'),
 '824': dict(short_name='Worth', short_count='price', short_open='worth', slot_note='vilai price; text-final after sale 892 on tablets; at the front before two on seals it works like the share openers'),
 '840': dict(short_name='Peer', short_count='pair', slot_note='iṇai: pair (bangles, counts) / equal, peer (names)'),
 '055': dict(short_name='Twelve', short_count='dozen', slot_note='paṉṉiru: dozen in counts / the Twelve in names (ends the name 21/45 against 0/17 in counts)'),
 '690': dict(short_name='Ally', short_count='bound', slot_note='piṇai: bound (count) / ally, union (names)'),
 '806': dict(short_name='Bounty', short_count='produce', slot_note='viḷai: produce in load tags / bounty in names (fish with it 60% against 29.5%)'),
 '501': dict(short_name='Throng', short_count='heap', slot_note='kumi: heap (count) / throng, multitude (name)'),
 '368': dict(short_name='Banner', short_count='banner', short_final='standard-bearer', slot_note='koṭi: banner; text-final after a name = the standard-bearer'),
 '861': dict(short_name='Tribute', short_count='share', short_open='share', slot_note='kāṇi: share (count, opener) / due, tribute (name; kāṇikkai). First name word Holding went against (land words 8/120 against 6.1%); Tribute: beside transaction words on new texts 5/21 against 4.0%'),
 '060': dict(short_name='Inner', slot_note='uḷ: in (opener joiner); Inner- as a name prefix away from the openers; "within" between two numbers'),
 '741': dict(short_name='First-ward'), '742': dict(short_name='Second-ward'), '745': dict(short_name='Third-ward'),
 '405': dict(short_name='Kindred', short_count='kindred'),
}
for s in ('151', '152', '153', '154', '155', '156', '157', '158'):
    SL[s] = dict(short_name='Keeper', short_count='porter', short_final='keeper', slot_note='kā: keeper in names and as a closing title; porter when counted on goods; counted on a seal it is a title (Three-keeper)')
for s, kw in SL.items():
    if s not in set(M.sign):
        M.loc[len(M)] = {c: '' for c in M.columns} | dict(sign=s, status='strict', sound='kā', short='keeper', english='keeper', report='odd_readings.md'); 
    for k, v in kw.items(): M.loc[M.sign == s, k] = v
# ---- fold in: sign 390 cotton fix and the fifth pass (jobs/out/sound_list_v5.md, work_data/sound_v5/values_v5.csv)
def setv(s, **kw):
    if s not in set(M.sign): M.loc[len(M)] = {c: '' for c in M.columns} | dict(sign=s)
    for k, v in kw.items(): M.loc[M.sign == s, k] = v
setv('390', sound='parutti', english='cotton', short='cotton', short_count='cotton', short_name='Cotton', status='strict', slot_note='cotton (DEDR 3976); 590-390 together = the house name Boxed-cotton; 390 alone after a count = cotton as a counted good')
for s in ('233', '060', '435', '388', '240', '097', '923', '104'): setv(s, status='strict')          # wide made strict in the fifth pass
V5 = pd.read_csv(f'{ROOT}/work_data/sound_v5/values_v5.csv', dtype=str).fillna('')
setv('923', sound='maruppu', english='ivory, tusk', short='ivory', note='fifth pass: tusk (DEDR 4720)')
setv('692', sound='kūṭṭam', english='assembly, council', short='Assembly', status='wide')
setv('711', sound='vaḷḷam', english='grain measure', short='grain measure', status='wide')
for s in ('370', '371'): setv(s, sound='katir', english='spindle', short='spindle', status='wide')
for s, snd, sh in (('161', 'kā', 'keeper'), ('347', 'kalai', 'stag'), ('491', 'kompu', 'horn'), ('495', 'kompu', 'horn'), ('519', 'vēli', 'fence'), ('565', 'maṟavaṉ', 'warrior'), ('868', 'araikkāṇi', 'half-share'), ('850', 'kāṇi', 'share'), ('838', 'viḷai', 'produce')):
    setv(s, sound=snd, english=sh, short=sh, status='wide')
for s in ('405', '645', '236'): setv(s, status='testing')
M.to_csv(f'{ROOT}/work_data/values_master2.csv', index=False)
print('values_master2.csv:', len(M), 'signs;', int((M.short_name != "").sum()), 'with slot words')
