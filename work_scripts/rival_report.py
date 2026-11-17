"""Print the side-by-side tables from the pun-test JSON files (work_data/lexicons/pun_results_*.json). Run from /home/claude/ivc."""
import json, sys
def fmt(sm): return f"{sm['hits']}/{sm['slots_with_picture_word']} (chance {sm['expected_len']:.2f}, P {sm['P_len']:.1e})"
for mode in ('core', 'allsyn'):
    r = json.load(open(f'work_data/lexicons/pun_results_{mode}.json'))
    print(f'\n##### picture words: {mode}')
    for need in ('narrow', 'broad'):
        print(f'\n--- slot meanings: {need}')
        print(f"{'language':44s} {'entries':>8s} | {'3 letters':34s} | {'4 letters':34s} | {'whole word':34s} | {'2 letters':34s}")
        for lab, v in r.items():
            print(f"{lab:44s} {v['n']:8d} | " + ' | '.join(f"{fmt(v[f'{need}_L{L}']['summary']):34s}" for L in (3, 4, 0, 2)))
    print('\n--- cut to 3000 entries (narrow slot meanings), mean over 30 draws: hits / chance / median P')
    for lab, v in r.items():
        sz = v.get('sized', {})
        print(f"{lab:44s} " + ' | '.join((f"L{L}: {z['hits']}/{z['expected']} P{z['P_median']:.1e} ({z['slots']} slots)" if z else f"L{L}: n/a (<3000)") for L, z in sz.items()))
