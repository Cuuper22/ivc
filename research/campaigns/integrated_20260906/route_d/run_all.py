#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
for program in ['run_route_d.py','search_modifier_lattice.py','semantic_category_control.py','tamil_joint_search.py','test_counted_fish_composition.py','finalize_route_d.py']:
    with (here/(program.removesuffix('.py')+'_stdout.json')).open('w') as stream:
        subprocess.run([sys.executable,str(here/program)],check=True,stdout=stream)
    print(program+' completed',flush=True)
