"""DEDR grep: python3 holes_dedr.py 'regex' [maxhits] ; looks at Tamil-headed entries (first 400 chars)."""
import re, sys, unicodedata
P = '/home/claude/ivc/work_data/lexicons/dedr/dedr_entries.tsv'
E = [l.rstrip('\n').split('\t', 1) for l in open(P, encoding='utf8')]
def grep(rx, k=14, n=230, anyhead=False):
    r = re.compile(rx, re.I); out = []
    for no, t in E:
        if (anyhead or t.startswith('Ta.')) and r.search(t[:400]): out.append((no, t[:n]))
        if len(out) >= k: break
    return out
def entry(no, n=600):
    for a, t in E:
        if a == str(no): return t[:n]
if __name__ == '__main__':
    for no, t in grep(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 14): print(no, t)
