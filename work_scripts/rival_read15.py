"""Read the 15 seals of language_candidates.md with the sound values each rival's best pun gives (signs with no pun stay blank).
Value tables come from pun_results_core.json hits (3-letter, narrow) read one by one; Dravidian values are those of language_candidates.md."""
SEALS = {'M-185': '220-520', 'M-1912': '003-220-520', 'H-148': '235-240-520', 'K-32': '231-520', 'M-294': '003-220-740', 'H-669': '032-220-740',
         'M-1669': '390-740', 'C-17': '100-740', 'H-502': '032-220-740-090', 'L-41': '817-002-233-740-090', 'Ns-5': '820-002-016-220-740-090',
         'H-1056': '003-220-740-090-400', 'M-1312': '220-740-400', 'H-514': '820-002-016-220-151', 'M-1828': '142-156'}
NUM = {'001', '002', '003', '004', '005', '016', '017', '012', '013', '014', '031', '032', '033', '034'}; OPEN = {'817', '820', '861'}
VAL = {
 'Dravidian': {'740': 'kuti(house)', '090': 'al(manager)', '400': 'cir(junior)', '520': 'vel(chief)', '142': 'ko(king)', '151': 'ka(keeper)', '156': 'ka(keeper)', '220': 'min(star)',
               '235': 'min(star)', '240': 'min(star)', '233': 'min(star)', '231': 'min(star)', '390': 'maram(warrior)', '100': 'mutu(elder)'},
 'Munda (Santali/Mundari)': {'740': 'chanda(family dues)', '400': 'chabha(small)', '520': 'barki(chief wife)', '151': 'aras(keep)', '156': 'aras(keep)', '142': 'lat(lord, English loan)'},
 'Sanskrit (MW + Turner)': {'740': 'kuta(house, family)', '400': 'kanittha(small)', '090': 'bharitr(sustainer, master)'},
 'Sumerian (Halloran)': {'142': 'subar(subordinate of king)'},
 'Burushaski': {}, 'Elamite': {},
}
for lang, V in VAL.items():
    ok = 0; lines = []
    for sid, sg in SEALS.items():
        toks = sg.split('-'); core = [t for t in toks if t not in NUM and t not in OPEN]
        have = [t for t in core if t in V]
        full = len(have) == len(core)
        ok += full
        lines.append(f"  {sid:7s} {sg:24s} {' '.join(V.get(t, '?') if t not in NUM and t not in OPEN else '.' for t in toks)}   {'READABLE' if full else 'gaps'}")
    print(f"\n{lang}: {ok} of 15 seals have a value for every non-number, non-opener sign")
    print('\n'.join(lines))
