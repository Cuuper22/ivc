#!/usr/bin/env python3
"""Scores the blind test. Reads work_data/blind/grades.csv (item, grade, reason) and work_data/blind/KEY_do_not_open.csv.

Prints, for each of the four tables (real, S1 free shuffle, S2 shuffle inside slot class, S3 shuffle inside frequency band):
  the share of lines graded sense / odd / nonsense (all objects, then split by object kind);
and, per inscription, the paired comparison of the real line against each scramble's line: how often real is graded better,
the same, or worse (sense > odd > nonsense), with an exact two-sided sign test P (ties dropped) and the one-sided P for "real better".
Run: python3 blind_score.py            (only after grades.csv exists)"""
import csv, sys, collections
from math import comb
D = '/home/claude/ivc/work_data/blind'
RANK = {'sense': 2, 'odd': 1, 'nonsense': 0}
TABLES = ['real', 'S1', 'S2', 'S3']
NAMES = {'real': 'real table', 'S1': 'S1 free shuffle', 'S2': 'S2 shuffle within slot class', 'S3': 'S3 shuffle within frequency band'}

def sign_test(better, worse):
    n = better + worse
    if n == 0: return float('nan'), float('nan')
    def tail(k): return sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n      # P(X >= k) with p = 1/2
    one = tail(better)
    two = min(1.0, 2 * min(tail(better), tail(worse)))
    return one, two
def pct(a, n): return f'{100 * a / n:5.1f}%' if n else '  n/a'

key = list(csv.DictReader(open(f'{D}/KEY_do_not_open.csv', newline='')))
grades = {}
for r in csv.DictReader(open(f'{D}/grades.csv', newline='')):
    g = r['grade'].strip().lower()
    if g not in RANK: sys.exit(f'item {r["item"]}: grade "{r["grade"]}" is not sense / odd / nonsense')
    grades[r['item'].strip()] = g
missing = [k['item'] for k in key if k['item'] not in grades]
if missing: sys.exit(f'{len(missing)} items have no grade, first few: {missing[:10]}')
print(f'[blind_score] {len(key)} lines graded.\n')

rows = [dict(item=k['item'], face=k['face id'], kind=k['object kind'], table=k['which table'], g=grades[k['item']]) for k in key]
kinds = sorted({r['kind'] for r in rows})

def shares(sel, label):
    print(label)
    print(f'  {"table":34s} {"lines":>5s} {"sense":>8s} {"odd":>8s} {"nonsense":>9s}')
    for t in TABLES:
        g = [r['g'] for r in sel if r['table'] == t]; c = collections.Counter(g)
        print(f'  {NAMES[t]:34s} {len(g):5d} {pct(c["sense"], len(g)):>8s} {pct(c["odd"], len(g)):>8s} {pct(c["nonsense"], len(g)):>9s}')
shares(rows, 'SHARE OF EACH GRADE, all object kinds')
print('  Meaning: of the lines made by that table, the share the reader graded sense / odd / nonsense. If the word list is right, the real table\n  should have a clearly higher sense share than the scrambles; similar shares mean the words add nothing the rules and slots do not already give.\n')

by = collections.defaultdict(dict)
for r in rows: by[r['face']][r['table']] = r
def paired(faces, scr):
    b = s = w = 0
    for f in faces:
        a, c = RANK[by[f]['real']['g']], RANK[by[f][scr]['g']]
        if a > c: b += 1
        elif a == c: s += 1
        else: w += 1
    return b, s, w
def paired_report(faces, label):
    print(label)
    print(f'  {"real compared with":34s} {"better":>6s} {"same":>5s} {"worse":>5s} {"P one-sided":>12s} {"P two-sided":>12s}')
    for scr in TABLES[1:]:
        b, s, w = paired(faces, scr); one, two = sign_test(b, w)
        print(f'  {NAMES[scr]:34s} {b:6d} {s:5d} {w:5d} {one:12.4f} {two:12.4f}')
allfaces = sorted(by)
paired_report(allfaces, f'PAIRED, real vs each scramble, per inscription ({len(allfaces)} inscriptions)')
print('  Meaning: "better" = the real line was graded higher than the scramble\'s line of the same inscription (sense > odd > nonsense); "same" = equal grades;\n'
      '  "worse" = the scramble was graded higher. P = chance of a split at least this lopsided toward real being better ("one-sided", exact sign test on the\n'
      '  better-vs-worse counts, ties dropped, chance = 50/50) or in either direction ("two-sided"). Small one-sided P points to: the real words read better than\n'
      '  wrongly dealt words. P near 0.5 or a "worse" excess points to: the word list adds no sense beyond the rules.\n')

print('SPLIT BY OBJECT KIND')
for k in kinds:
    faces = [f for f in allfaces if by[f]['real']['kind'] == k]
    print()
    shares([r for r in rows if r['kind'] == k], f'-- {k} ({len(faces)} inscriptions): share of each grade')
    paired_report(faces, f'-- {k}: paired real vs scramble')
print('\n  Meaning: the same two tables as above, for one object kind at a time. Kinds with few inscriptions give lopsided percentages and large P by size alone; read them as counts.')
