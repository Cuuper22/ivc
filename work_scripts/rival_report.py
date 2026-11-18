"""Print the side-by-side tables from the pun-test JSON files (work_data/lexicons/pun_results_*.json). Run from /home/antigravity/Cuuper22/ivc."""
import json, sys
def fmt(sm): return f"{sm['hits']}/{sm['slots_with_picture_word']} (chance {sm['expected_len']:.2f}, P {sm['P_len']:.1e})"
if len(sys.argv) > 1 and sys.argv[1] == "detail": mode_list = ()
else: mode_list = ("core", "allsyn")
for mode in mode_list:
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

# per-sign detail: python3 work_scripts/rival_report.py detail core "Munda pooled" narrow_L3
if len(sys.argv) > 4 and sys.argv[1] == 'detail':
    r = json.load(open(f'work_data/lexicons/pun_results_{sys.argv[2]}.json'))
    for lab, v in r.items():
        if sys.argv[3].lower() not in lab.lower(): continue
        d = v[sys.argv[4]]; print(f"=== {lab} [{sys.argv[4]}] {d['summary']}")
        for s, sl in d['slots'].items():
            print(f"  {s:8s} picture words({sl['n_words']}): {sl['words'][:7]}  chance(same-length) {sl['p_len']:.3f}  {'HIT' if sl['hit'] else 'no hit'}")
            for w, la in list(d['looks'][s].items())[:4]:
                for h, g in la[:2]: print(f"       {w}  ~  {h}: {g[:80]}")
