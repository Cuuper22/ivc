"""The picture-word pun test, identical for every language, run on the full dictionaries in work_data/lexicons/tsv/.
Run from /home/claude/ivc:  python3 work_scripts/rival_pun_test.py [out.json]
Rule (same as lang_pun_chance.py): for each of 9 pictures, a PICTURE WORD is a dictionary entry whose first gloss names the pictured thing.
A HIT = some OTHER entry whose headword shares the first L letters (diacritics, case and punctuation removed) and whose gloss carries the
meaning the SLOT needs. Chance for a slot = the share of ALL entries of the same dictionary (same key length) that have such a look-alike,
so a bigger dictionary raises its own chance. With k picture words for one picture the chance is 1-(1-p)^k (every synonym is paid for).
Variants: L=3 (strict), L=2 (loose), L=4, whole word (exact homophone); slot words 'narrow' (the original nine) or 'broad' (wider synonyms)
and a size-matched run that cuts every dictionary to the same number of entries."""
import re, sys, json, random, unicodedata, collections, math
TSV = 'work_data/lexicons/tsv'
def norm(w):
    w = unicodedata.normalize('NFKD', w.lower())
    return re.sub(r'[^a-z]', '', ''.join(c for c in w if not unicodedata.combining(c)))
SLOTS = ['jar', 'man', 'fish', 'seven', 'comb', 'spear', 'staff', 'carrier', 'tree']
# what the slot needs: (narrow = the nine regexes of lang_pun_chance.py, broad = wider synonyms), English and German
NEED = {
 'en': {'narrow': dict(jar=r"\b(house|household|family|lineage|clan)\b", man=r"\b(rule|rules|ruler|manage|master)\b", fish=r"\bstars?\b",
                       seven=r"\b(rise|ascend)\b", comb=r"\b(small|young|younger|junior)\b", spear=r"\b(chief|king|ruler|lord)\b",
                       staff=r"\b(king|chief|lord|emperor)\b", carrier=r"\b(guard|protect|protection|keep)\b", tree=r"\b(warrior|valour|bravery)\b"),
        'broad':  dict(jar=r"\b(house|household|family|lineage|clan|race|tribe|kin|kindred|dwelling|home|hearth|village|caste|descent)\b",
                       man=r"\b(rule|rules|ruler|manage|manager|master|lord|owner|headman|leader|govern|chief|head)\b", fish=r"\b(stars?|planet|constellation)\b",
                       seven=r"\b(rise|rises|ascend|arise|mount|climb|go up|raise|lift)\b", comb=r"\b(small|young|younger|youngest|junior|little|minor|inferior|lesser|child)\b",
                       spear=r"\b(chief|king|ruler|lord|headman|leader|noble|prince|captain|master)\b", staff=r"\b(king|chief|lord|emperor|ruler|prince|sovereign|monarch)\b",
                       carrier=r"\b(guard|protect|protection|keep|keeper|watch|defend|preserve|store)\b", tree=r"\b(warrior|valour|bravery|brave|hero|soldier|fight|war|courage)\b")},
 'de': {'narrow': dict(jar=r"\b(haus|haushalt|familie|geschlecht|sippe|clan)", man=r"\b(herrsch|herrscher|verwalt|gebieter|meister)", fish=r"\b(stern|gestirn)",
                       seven=r"\b(aufgehen|aufsteigen|aufgang|steigen|sich erheben)", comb=r"\b(klein|jung|jünger|junior|gering)", spear=r"\b(häuptling|könig|fürst|herrscher|herr)\b",
                       staff=r"\b(könig|häuptling|herr|herrscher|kaiser)", carrier=r"\b(wächter|bewach|schütz|schutz|hüt|bewahr)", tree=r"\b(krieger|tapfer|mut)"),
        'broad':  dict(jar=r"\b(haus|haushalt|familie|geschlecht|sippe|clan|stamm|verwandt|heim|wohn|dorf)", man=r"\b(herrsch|herrscher|verwalt|gebieter|meister|besitzer|führer|leiter|chef|oberhaupt)",
                       fish=r"\b(stern|gestirn|planet|sternbild)", seven=r"\b(aufgehen|aufsteigen|aufgang|steigen|sich erheben|erheben|hinauf)", comb=r"\b(klein|jung|jünger|junior|gering|kind|minder)",
                       spear=r"\b(häuptling|könig|fürst|herrscher|herr|anführer|edel|prinz)", staff=r"\b(könig|häuptling|herr|herrscher|kaiser|fürst)",
                       carrier=r"\b(wächter|bewach|schütz|schutz|hüt|bewahr|wache|verwahr)", tree=r"\b(krieger|tapfer|mut|held|soldat|kampf|krieg)")}}
# what the picture is: first gloss must NAME the thing (generic sense, no 'a kind of')
PICT = {
 'en': dict(jar=r"^(?:an? |the )?(?:[\w-]+ ){0,2}(?:water-?pot|pot|jar|pitcher|jug|vessel)\b(?! of| for|ful|-?shaped)",
            man=r"^(?:an? |the )?(?:man|male|husband|human being|male person|male human)\b(?!-)",
            fish=r"^(?:an? |the )?(?:big |large |small )?fish\b(?!-)(?! (?:hawk|eagle|net|trap))", seven=r"^(?:the )?(?:numeral )?seven\b",
            comb=r"^(?:an? |the )?(?:[\w-]+ ){0,1}comb\b(?!ing)", spear=r"^(?:an? |the )?(?:[\w-]+ ){0,1}(?:spear|lance|javelin|pike|trident)\b",
            staff=r"^(?:an? |the )?(?:[\w-]+ ){0,1}(?:staff|rod|stick|sceptre|scepter|cane|cudgel)\b",
            carrier=r"(?:carrying[- ]pole|shoulder[- ]pole|pole (?:for|to|with) carry|carrying[- ]yoke|yoke|palanquin|palkee)", tree=r"^(?:an? |the )?tree\b(?! of| for)"),
 'de': dict(jar=r"^(?:ein |der |das |die )?(?:krug|topf|gefäß|gefäss|kanne|wasserkrug)\b", man=r"^(?:ein |der )?(?:mann|mensch|gatte|ehemann)\b", fish=r"^(?:ein |der )?fisch\b",
            seven=r"^(?:die )?(?:zahl )?(?:sieben|7)\b", comb=r"^(?:ein |der )?kamm\b", spear=r"^(?:ein |der |die )?(?:speer|lanze)\b",
            staff=r"^(?:ein |der )?(?:stab|stock|szepter|zepter)\b", carrier=r"(?:tragstange|tragjoch|joch|tragholz)", tree=r"^(?:ein |der )?baum\b")}
def load(names, lang):
    rows = []
    for n in names:
        for l in open(f'{TSV}/{n}.tsv', encoding='utf8'):
            h, g = l.rstrip('\n').split('\t')
            k = norm(h)
            if len(k) >= 2: rows.append((h, g, k))
    return rows
def keyf(k, L): return k if L == 0 else k[:L]       # L=0 means whole word
def analyse(rows, lang, need='narrow', L=3, extra_pic=None):
    """per slot: picture words found, whether any has a slot-right look-alike, chance (all lengths / same key length), the look-alikes"""
    N = len(rows); NE = NEED[lang][need]; out = {}
    kc = [keyf(k, L) for _, _, k in rows]
    for s in SLOTS:
        R = re.compile(NE[s]); P = re.compile(PICT[lang][s])
        match = [bool(R.search(g)) for _, g, _ in rows]
        idx = collections.defaultdict(list)
        for i, m in enumerate(match):
            if m: idx[kc[i]].append(i)
        by_len = collections.defaultdict(lambda: [0, 0]); allp = 0
        for i in range(N):
            f = any(j != i for j in idx.get(kc[i], ()))
            by_len[len(kc[i])][0] += 1; by_len[len(kc[i])][1] += f; allp += f
        p_all = allp / N
        pics = collections.OrderedDict()                      # picture word (headword) -> its rows
        for i in range(N):
            if P.search(rows[i][1]) or (extra_pic and rows[i][0] in extra_pic.get(s, ())): pics.setdefault(rows[i][0], []).append(i)
        q_all = q_len = 1.0; hit_words = []; looks = {}
        for hw, ids in pics.items():
            la = [(rows[j][0], rows[j][1]) for i in ids for j in idx.get(kc[i], ()) if j != i]
            b = by_len[len(kc[ids[0]])]; p_l = b[1] / b[0] if b[0] else 0
            q_all *= (1 - p_all); q_len *= (1 - p_l)
            if la: hit_words.append(hw); looks[hw] = la[:6]
        out[s] = dict(n_words=len(pics), hit=bool(hit_words), p_all=1 - q_all if pics else 0.0, p_len=1 - q_len if pics else 0.0,
                      hit_words=hit_words[:15], words=list(pics)[:15], looks=looks, pic_gloss={hw: rows[ids[0]][1] for hw, ids in list(pics.items())[:15]})
    return out
def pb_tail(ps, x):
    dist = [1.0]
    for p in ps:
        nd = [0.0] * (len(dist) + 1)
        for i, v in enumerate(dist): nd[i] += v * (1 - p); nd[i + 1] += v * p
        dist = nd
    return sum(dist[x:])
def summarize(res):
    got = sum(r['hit'] for r in res.values()); present = [r for r in res.values() if r['n_words'] > 0]
    e_all = sum(r['p_all'] for r in present); e_len = sum(r['p_len'] for r in present)
    return dict(slots_with_picture_word=len(present), hits=got, expected_all=round(e_all, 2), expected_len=round(e_len, 2),
                P_all=pb_tail([r['p_all'] for r in present], got), P_len=pb_tail([r['p_len'] for r in present], got))
def size_matched(rows, lang, need, L, size, draws=20, extra_pic=None, seed=5):
    """cut the dictionary to `size` entries (picture entries always kept) and rerun; mean over draws"""
    rnd = random.Random(seed); H = []; E = []; EL = []
    allpic = set()
    for s in SLOTS:
        P = re.compile(PICT[lang][s]); allpic |= {i for i, (_, g, _) in enumerate(rows) if P.search(g)}
    rest = [i for i in range(len(rows)) if i not in allpic]
    if len(rest) + len(allpic) <= size: return None
    for _ in range(draws):
        keep = sorted(allpic | set(rnd.sample(rest, size - len(allpic))))
        sub = [rows[i] for i in keep]
        sm = summarize(analyse(sub, lang, need, L, extra_pic))
        H.append(sm['hits']); E.append(sm['expected_all']); EL.append(sm['expected_len'])
    return dict(hits=round(sum(H) / len(H), 2), expected_all=round(sum(E) / len(E), 2), expected_len=round(sum(EL) / len(EL), 2), size=size)

# ---- the languages and what to run -------------------------------------------------------------------------------
GROUPS = collections.OrderedDict([   # label -> (dictionaries pooled, gloss language)
 ('Dravidian (Tamil side of DEDR)',          (['dravidian_tamil_dedr'], 'en')),
 ('Santali, Campbell 1899',                  (['santali_campbell'], 'en')),
 ('Santali, Bodding vol 5 (R-end)',          (['santali_bodding_v5'], 'en')),
 ('Santali, Wiktionary',                     (['santali_wiktionary'], 'en')),
 ('Mundari, Bhadra 1931',                    (['mundari_bhadra'], 'en')),
 ('Munda pooled (Santali x3 + Mundari)',     (['santali_campbell', 'santali_bodding_v5', 'santali_wiktionary', 'mundari_bhadra'], 'en')),
 ('Burushaski, Lorimer Werchikwar 1962',     (['burushaski_werchikwar_yasin'], 'en')),
 ('Burushaski, Barken (Hunza, A-B only)',    (['burushaski_barken_hunza'], 'en')),
 ('Sumerian, Halloran lexicon',              (['sumerian_halloran'], 'en')),
 ('Sumerian, Wiktionary',                    (['sumerian_wiktionary'], 'en')),
 ('Sumerian pooled',                         (['sumerian_halloran', 'sumerian_wiktionary'], 'en')),
 ('Elamite, Hinz-Koch 1987 (German)',        (['elamite_hinzkoch'], 'de')),
 ('Indo-Aryan, Turner CDIAL (OIA heads)',    (['indoaryan_turner'], 'en')),
 ('Sanskrit, Monier-Williams',               (['sanskrit_monier_williams'], 'en')),
 ('Indo-Aryan pooled (Turner + MW)',         (['indoaryan_turner', 'sanskrit_monier_williams'], 'en')),
])
# the picture words the earlier run chose by hand (Dravidian) and the Sanskrit run (IAST), added to the regex-found set
HAND = {'Dravidian (Tamil side of DEDR)': dict(jar=['kuṭam'], man=['āḷ'], fish=['mīṉ'], seven=['ēr̤u'], comb=['cīppu'], spear=['vēl'], staff=['kōl'], carrier=['kā'], tree=['maram'])}
if __name__ == '__main__':
    import os
    only = sys.argv[2:] ; res_all = {}
    for label, (names, lang) in GROUPS.items():
        if not all(os.path.exists(f'{TSV}/{n}.tsv') for n in names): print('skip (missing)', label); continue
        if only and not any(o.lower() in label.lower() for o in only): continue
        rows = load(names, lang); res_all[label] = {'n': len(rows)}
        for need in ('narrow', 'broad'):
            for L in (3, 2, 4, 0):
                r = analyse(rows, lang, need, L, HAND.get(label)); sm = summarize(r)
                res_all[label][f'{need}_L{L}'] = dict(summary=sm, slots={k: {kk: vv for kk, vv in v.items() if kk != 'looks'} for k, v in r.items()}, looks={k: v['looks'] for k, v in r.items()})
        print(f"{label:42s} n={len(rows):7d} narrow L3 hits {res_all[label]['narrow_L3']['summary']['hits']} exp {res_all[label]['narrow_L3']['summary']['expected_all']}/{res_all[label]['narrow_L3']['summary']['expected_len']}", flush=True)
    json.dump(res_all, open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/rival_pun_results.json', 'w'), ensure_ascii=False, indent=1)
