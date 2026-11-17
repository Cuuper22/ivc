"""Shared loader for the cotton-house job. Reading order = stored order reversed (goods_common.load does it).
Adds: object key, pair finder, the jar/count constants, and a chance-by-shuffle helper."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from goods_common import *
OUTC = f'{ROOT}/work_scripts/cotton_out'
os.makedirs(OUTC, exist_ok=True)
JAR = '740'
TALL = {'031','032','033','034','035','036'}   # full-height strokes 1..6 (container / lot series)
SHORT = {f'{i:03d}' for i in range(1, 8)}
COUNTS = set(CNT)
def faces():
    d = load()
    d['obj'] = d.id.str.split('.').str[0]
    d['face'] = d.id.str.split('.').str[1]
    return d
def has_pair(t, a, b):
    return [i for i in range(len(t) - 1) if t[i] == a and t[i + 1] == b]
def log(f, s):
    print(s)
    f.write(s + '\n')
