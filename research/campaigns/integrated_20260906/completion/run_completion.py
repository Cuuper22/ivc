#!/usr/bin/env python3
"""Runnable reconstruction stages. Raw source and accepted ledger stay fixed."""
import argparse,concurrent.futures,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from restore_payload import restore
restore()
ENV=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
def run(script,*args):
    subprocess.run([sys.executable,str(HERE/script),*args],env=ENV,check=True,cwd=HERE.parent)
def stage(name):
    if name=='shared':run('shared/common.py')
    elif name=='a':run('route_a/run.py');run('route_a/run_contextual.py')
    elif name in ('b','c'):run('route_'+name+'/run.py')
    elif name=='d':run('route_d/run_completion_d.py')
    elif name=='sources':run('sources/run.py')
    elif name in ('joint','linguistic'):
        tasks=list(json.loads((HERE/'shared/masks.json').read_text())['masks'])
        def task(t):run('run_joint.py','--stage','abc' if name=='joint' else 'd','--task',t)
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(7,os.cpu_count() or 1)) as pool:list(pool.map(task,tasks))
    elif name=='consolidate':run('cross_route.py');run('finalize_reconstruction.py')
    elif name=='verify':run('finalize_reconstruction.py','--stage','verify')

if __name__=='__main__':
    choices=['shared','a','b','c','d','sources','joint','linguistic','consolidate','verify']
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=choices+['all'],default='verify');args=p.parse_args()
    for s in choices if args.stage=='all' else [args.stage]:stage(s)
