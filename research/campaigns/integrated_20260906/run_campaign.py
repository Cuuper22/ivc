#!/usr/bin/env python3
"""Reproduce a selected research route or the integrated campaign, locally."""
import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
COMMANDS={
    'foundation':[HERE/'shared/foundation.py'],
    'a':[HERE/'route_a/run_route_a.py',HERE/'route_a/adjudicate_composition.py',HERE/'route_a/build_report.py'],
    'b':[HERE/'route_b/run_route_b.py',HERE/'route_b/stratify_fish_composition.py'],
    'c':[HERE/'route_c/run_numerical_programs.py'],
    'd':[HERE/'route_d/run_all.py'],
    'integration':[HERE/'run_integration.py'],
    'package':[HERE/'consolidate.py'],
}


def run(route):
    for script in COMMANDS[route]:
        print(f'RUN {script.relative_to(ROOT)}',flush=True)
        subprocess.run([sys.executable,str(script)],cwd=ROOT,check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--route',choices=['all',*COMMANDS],default='all')
    args=parser.parse_args()
    if args.route!='all':
        run(args.route)
        return
    run('foundation')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(run,r) for r in ['a','b','c','d']]
        for future in futures:future.result()
    run('integration')
    run('package')


if __name__=='__main__':main()
