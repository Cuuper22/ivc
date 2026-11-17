import sys
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from holes_common import *
ls=lines(True)
for sg in sys.argv[1:]:
    print('=====',sg)
    for L in ls:
        if sg in L['toks']:
            print(L['cisi'],L['site'][:6],L['type'],L['area'][:10],L['animal'],f"f{L['face']}l{L['line']}",'-'.join(L['toks']),'|',' '.join((snd(s) or '?') for s in L['toks']))
