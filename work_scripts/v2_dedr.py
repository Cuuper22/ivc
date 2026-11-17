#!/usr/bin/env python3
"""DEDR helper for the second sound pass. usage:
  python3 v2_dedr.py n 1305 1376        -> full text of entries
  python3 v2_dedr.py w kalam tiṅkaḷ     -> entries whose Tamil part has the word as a token
  python3 v2_dedr.py g 'measure of capacity'  -> entries whose Tamil part contains the English phrase"""
import re, sys, unicodedata
sys.path.insert(0, __import__('os').path.dirname(__file__))
from sound_dedr import E, ta_part, look
D = dict(E)
if __name__ == '__main__':
    mode, args = sys.argv[1], sys.argv[2:]
    for a in args:
        if mode == 'n': print(a, D.get(a, '')[:900]); print()
        elif mode == 'w':
            r = look(a, 260); print(f'== {a}: {len(r)}'); [print(' ', k, t) for k, t in r[:6]]
        else:
            r = [(k, t) for k, t in E if a.lower() in ta_part(t).lower()]
            print(f'== {a}: {len(r)}')
            for k, t in r[:25]:
                tp = ta_part(t); i = tp.lower().find(a.lower()); print(' ', k, tp[max(0, i - 120):i + 60])
