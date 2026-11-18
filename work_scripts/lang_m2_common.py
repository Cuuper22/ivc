#!/usr/bin/env python3
"""lang_m2: the machine language test, second run.  EVERY RULE IS FIXED HERE, written before any score of this run was computed.

UNITS (lang_m2_units.py)
  Pictures: work_data/pictures/pictures_blind.csv (Mahadevan drawing -> thing(s) named by at least 2 of 3 blind describers).
  Lipi sign -> Mahadevan drawing: work_data/lipi_mahadevan_crosswalk.csv, rank-1 pairs only (rank_for_lipi_sign == 1).
  Class: the 10-state hidden-state model class (column hmm10 of work_data/frame/classes.csv), with the eight moves the frame report
         found backed by corpus likelihood (621 161 527 241 -> after-jar title H10_8; 824 880 545 091 -> openers H10_9).
  Unit = (agreed picture noun set, machine class).  Two fixed variants: A = 3of3 pictures only; B = 3of3 + 2of3.
  No sign is dropped by hand (stroke signs keep whatever the describers named).
PICTURE WORD: a dictionary entry with one of the noun's gloss terms as a whole word among the first 3 words of its gloss (lang_m rule).
  Gloss terms of a noun = the noun itself plus the synonyms of the lang_m list (PIC_EN) whose term list contains that noun
  (man -> man person human male; jar -> jar pot pitcher waterpot; ...).  German terms for the German-glossed Elamite dictionary below.
SOUND-ALIKE: unchanged from lang_m: a word of a DIFFERENT entry within the sound distance (strict = same normalised form; medium =
  same consonant skeleton; loose = skeletons one consonant apart), not itself glossed with the noun's terms.  With the homonym-aware
  dictionaries (lang_m2_lexicons.py) the strict distance now finds same-spelled words of different entries.
JOB KEYWORDS per machine class (CLASS_KW): written from what each class IS in the frame (work_data/frame/log_classes.txt and the
  frame report table), the same for every language; narrow, and wide = narrow + additions.  Keyword hit: whole word among the first
  5 gloss words (plural -s/-es allowed).
SCORES per (dictionary or family) x (3 distances) x (2 breadths):
  hits  = number of units with at least one sound-alike carrying the unit's class keyword;
  share = sum over units of (sound-alikes carrying the unit's class keyword) / (all sound-alikes of the unit's picture words).
  Family: the family's dictionaries pooled (a unit hits if it hits in any; share pools the counts).
CONTROLS (P = (1 + runs scoring >= real) / (1 + runs)):
  C1 (2,000 runs) classes dealt at random among all units.
  C2 (2,000 runs) every picture noun replaced by a different outside drawable noun (one-to-one), classes kept.
  C3 (N3 = 500 runs per dictionary) the dictionary's sound forms dealt at random among its WORDS, a word being a dictionary entry:
     each entry hands its whole list of forms to another entry with the same number of rows (entries are dealt within groups of equal
     row count).  This keeps every entry's internal sound structure (DEDR prints one form several times inside one entry), the density
     of look-alikes and the gloss habits, and cuts every tie between sound and meaning across entries.  For flat lists (one row per
     entry) it is exactly the lang_m control.  The lang_m row-level deal is also run and reported as C3row (not used in the bar).
  C4 (2,000 runs) RIGHT CLASS AGAINST A WRONG CLASS FOR THE SAME PICTURE: every unit keeps its picture nouns and gets a class drawn
     at random from the classes its noun set does NOT take (drawn in proportion to how many units each class has, without two units
     of one noun set getting the same class while enough wrong classes remain).
     [Fixed after a two-dictionary smoke test, before the full run, for two reasons that are properties of the design, not of the
     scores: (1) dealing classes among units of one noun set leaves the score unchanged by construction (those units have the same
     sound-alikes, so a deal only swaps which unit is which: C4 mean = real to the third decimal); (2) the row-level C3 lets forms
     that DEDR repeats inside one entry loose into other entries, so the control's strict sound-alikes doubled (Tamil, 3,275 real
     against 6,621 dealt), which a homonym-aware test cannot use.]
STEP 6 SUMMARY, per family and variant:
  cells = (family's dictionaries + the pooled family) x 6 grid cells x 2 scores.  A cell "beats all controls" when its P < 0.05
  against C1, C2, C3 and C4.  Expected by chance: at most 0.05 x cells (the bar of the single least strict control); reported as
  that bound.  Also reported: cells beating C2 and C3 (the first test's Dravidian lean measure).
  COMBINED STATISTIC (fixed): Z3 = mean over the family's DICTIONARY cells (6 cells each, share score) of z = (real - mean C3) / sd C3.
  Its shuffle P: the same mean computed with each C3 run t in place of the real score (run t of every dictionary of the family
  together), P = (1 + runs with mean >= real mean) / (1 + N3).  Z1 and Z4 = the same against C1 and C4 (their draws are shared
  across the family's dictionaries draw by draw), reported beside it.
  BAR (fixed): a family clears it in variant B (the primary variant: more units) when Z3 has shuffle P < 0.05 / 7 (seven families)
  AND its count of cells beating all four controls is above 0.05 x cells.  Only then does step 8 (candidate list + decoys) run.
SWAPS (lang_m2_swaps.py): lang_m swap rule unchanged, pictures from the blind list (both variants), homonym-aware dictionaries.
"""
import re, csv, collections, unicodedata, os
import numpy as np
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/lang_m2'; LEX = '/tmp/lang_m2/lex'
os.makedirs(OUT, exist_ok=True)

PIC_EN_SYN = {   # lang_m picture term lists (gloss synonyms); a blind noun takes every list it appears in
    'person': 'man person human male', 'jar': 'jar pot pitcher waterpot', 'flower': 'flower blossom', 'sapling': 'sapling shoot',
    'branch': 'branch bough', 'spear': 'spear lance', 'pitchfork': 'fork pitchfork trident', 'table': 'table stool',
    'deer': 'deer antelope stag', 'cow': 'cow ox bull', 'flag': 'flag banner', 'staff': 'staff rod', 'burden': 'burden load',
    'pond': 'pond pool', 'lyre': 'lyre harp', 'mountain': 'mountain hill', 'pincers': 'pincers tongs', 'antenna': 'antenna feeler horn'}
def pic_terms_en(noun):
    t = {noun}
    for v in PIC_EN_SYN.values():
        if noun in v.split(): t |= set(v.split())
    return t
DE = {  # German gloss terms for the blind nouns (Elamite, Hinz-Koch), written from the noun alone
    'man': 'mann mensch', 'leaf': 'blatt', 'fish': 'fisch', 'comb': 'kamm', 'bow': 'bogen', 'tree': 'baum', 'jar': 'krug topf gefass',
    'cup': 'becher schale', 'rake': 'rechen harke', 'fork': 'gabel', 'box': 'kasten kiste', 'bird': 'vogel', 'arrow': 'pfeil',
    'hill': 'berg hugel', 'gate': 'tor', 'tent': 'zelt', 'door': 'tur', 'ladder': 'leiter', 'house': 'haus', 'flag': 'fahne',
    'horn': 'horn', 'window': 'fenster', 'eye': 'auge', 'table': 'tisch', 'bead': 'perle', 'seed': 'same saat', 'wheel': 'rad',
    'roof': 'dach', 'brick': 'ziegel', 'moon': 'mond', 'fan': 'facher', 'brush': 'burste pinsel', 'staff': 'stab', 'shield': 'schild',
    'stool': 'schemel hocker', 'hourglass': 'sanduhr', 'weight': 'gewicht', 'heart': 'herz', 'tripod': 'dreifuss', 'net': 'netz',
    'basket': 'korb', 'goat': 'ziege', 'deer': 'hirsch', 'insect': 'insekt', 'pillar': 'pfeiler saule', 'hook': 'haken',
    'cross': 'kreuz', 'spoon': 'loffel', 'pin': 'nadel stift', 'axe': 'axt beil', 'bed': 'bett', 'loom': 'webstuhl', 'anchor': 'anker',
    'teeth': 'zahn zahne', 'wing': 'flugel', 'grid': 'gitter', 'anvil': 'amboss', 'spider': 'spinne', 'star': 'stern',
    'hammer': 'hammer', 'book': 'buch', 'sun': 'sonne', 'rainbow': 'regenbogen', 'harp': 'harfe leier', 'arch': 'bogen',
    'cage': 'kafig', 'bud': 'knospe', 'spade': 'spaten', 'egg': 'ei', 'spindle': 'spindel', 'sail': 'segel', 'key': 'schlussel',
    'dumbbell': 'hantel'}

# outside drawable nouns for C2, English / German.  Any that is a blind picture noun or a keyword of any class is dropped by rule.
OUTSIDE = [('water', 'wasser'), ('fire', 'feuer'), ('stone', 'stein'), ('rope', 'seil'), ('knife', 'messer'), ('axe', 'axt'),
           ('boat', 'boot'), ('cart', 'wagen'), ('horse', 'pferd'), ('dog', 'hund'), ('snake', 'schlange'), ('frog', 'frosch'),
           ('elephant', 'elefant'), ('tiger', 'tiger'), ('buffalo', 'buffel'), ('crab', 'krebs'), ('scorpion', 'skorpion'), ('ant', 'ameise'),
           ('bee', 'biene'), ('egg', 'ei'), ('hand', 'hand'), ('foot', 'fuss'), ('eye', 'auge'), ('ear', 'ohr'), ('nose', 'nase'),
           ('mouth', 'mund'), ('tooth', 'zahn'), ('hair', 'haar'), ('bone', 'knochen'), ('blood', 'blut'), ('skin', 'haut'), ('net', 'netz'),
           ('mat', 'matte'), ('door', 'tur'), ('wall', 'mauer'), ('road', 'weg'), ('river', 'fluss'), ('sand', 'sand'), ('salt', 'salz'),
           ('oil', 'ol'), ('milk', 'milch'), ('honey', 'honig'), ('cloth', 'tuch'), ('thread', 'faden'), ('needle', 'nadel'),
           ('drum', 'trommel'), ('bell', 'glocke'), ('ring', 'ring'), ('bead', 'perle'), ('shell', 'muschel'), ('feather', 'feder'),
           ('nest', 'nest'), ('root', 'wurzel'), ('grass', 'gras'), ('thorn', 'dorn'), ('rain', 'regen'), ('cloud', 'wolke'),
           ('wind', 'wind'), ('ash', 'asche'), ('clay', 'ton'), ('copper', 'kupfer'), ('gold', 'gold'),
           ('rat', 'ratte'), ('lion', 'lowe'), ('monkey', 'affe'), ('camel', 'kamel'), ('bear', 'bar'), ('wolf', 'wolf'), ('fox', 'fuchs'),
           ('owl', 'eule'), ('crow', 'krahe'), ('parrot', 'papagei'), ('peacock', 'pfau'), ('turtle', 'schildkrote'), ('lizard', 'eidechse'),
           ('worm', 'wurm'), ('fly', 'fliege'), ('butterfly', 'schmetterling'), ('onion', 'zwiebel'), ('mango', 'mango'),
           ('lotus', 'lotos'), ('cotton', 'baumwolle'), ('wool', 'wolle'), ('leather', 'leder'), ('iron', 'eisen'), ('silver', 'silber'),
           ('sword', 'schwert'), ('shoe', 'schuh'), ('belt', 'gurtel'), ('lamp', 'lampe'), ('mirror', 'spiegel'), ('bowl', 'napf'),
           ('knot', 'knoten'), ('chain', 'kette'), ('cave', 'hohle'), ('island', 'insel'), ('lake', 'see'), ('well', 'brunnen'),
           ('sky', 'himmel'), ('smoke', 'rauch'), ('dust', 'staub'), ('mud', 'schlamm'), ('tongue', 'zunge'), ('finger', 'finger'),
           ('knee', 'knie'), ('neck', 'hals'), ('beard', 'bart'), ('nail', 'nagel'), ('tail', 'schwanz'), ('claw', 'kralle'),
           ('hoof', 'huf'), ('bean', 'bohne'), ('pepper', 'pfeffer'), ('nut', 'nuss'), ('lemon', 'zitrone'), ('pearl', 'perle'),
           ('tusk', 'stosszahn'), ('whip', 'peitsche'), ('saw', 'sage'), ('plough', 'pflug'), ('sickle', 'sichel'), ('yoke', 'joch'),
           ('oar', 'ruder'), ('raft', 'floss'), ('bridge', 'brucke'), ('tower', 'turm'), ('gourd', 'kurbis'), ('broom', 'besen'),
           ('bucket', 'eimer'), ('sieve', 'sieb'), ('pestle', 'stossel'), ('cradle', 'wiege'), ('pillow', 'kissen'), ('blanket', 'decke')]

# machine classes (HMM K=10): plain name, keywords EN narrow / wide additions, DE narrow / wide additions
CLASSES = {
    'H10_9': ('opener (front word)',
              'number share office place city town', 'count portion part lot department post duty village land region country quarter district seal mark',
              'zahl anteil amt ort stadt', 'teil los posten pflicht dorf land gegend bezirk siegel zeichen'),
    'H10_5': ('slot after an opener',
              'number two pair double second rank', 'grade class kind degree order count share couple twin',
              'zahl zwei paar doppelt zweite rang', 'grad klasse art stufe ordnung anteil zwilling'),
    'H10_6': ('front of a name (crest)',
              'clan lineage star emblem family tribe', 'house household caste kin ancestor totem sign banner constellation planet race descent',
              'sippe geschlecht stern wappen familie stamm', 'haus haushalt kaste verwandte ahn totem zeichen fahne sternbild planet abstammung'),
    'H10_2': ('number or person sign that starts a name or count',
              'person individual one number count head', 'man people soul body single each some few many',
              'person einzeln eins zahl kopf', 'mann leute seele korper jeder einige viele'),
    'H10_1': ('measure and box',
              'measure vessel box chest store weight', 'capacity container basket sack bag pot jar cup storehouse granary portion quantity volume',
              'mass gefass kasten kiste vorrat gewicht', 'korb sack beutel topf krug becher speicher teil menge'),
    'H10_7': ('what follows a measure (kin / fraction)',
              'son child offspring descendant part third', 'born kin family heir portion fraction share daughter grandson',
              'sohn kind nachkomme teil drittel', 'geboren verwandte familie erbe anteil bruchteil tochter enkel'),
    'H10_3': ('counted goods',
              'grain crop goods cattle cloth load', 'produce fruit harvest rice barley wheat seed bundle bale merchandise wares commodity animal sheep goat measure',
              'getreide korn ernte ware vieh tuch last', 'ertrag frucht reis gerste weizen saat bundel tier schaf ziege mass'),
    'H10_4': ('back of a name (before the closer)',
              'son younger junior elder little dear', 'beloved good great young self own born child boy girl fair bright',
              'sohn junger jungere alter klein lieb', 'geliebt gut gross jung selbst eigen geboren kind knabe madchen schon hell'),
    'H10_0': ('closer (possession, house, belonging)',
              'house belonging property own owner home', 'household dwelling abode possession estate family domain residence hut belong',
              'haus eigentum besitz eigen besitzer heim', 'haushalt wohnung wohnsitz gut familie hutte gehoren'),
    'H10_8': ('title after the jar (person and rank)',
              'chief lord servant master keeper guard ruler headman', 'man officer agent steward priest warrior soldier slave attendant leader manager king elder junior minister',
              'hauptling herr diener meister huter wachter herrscher vorsteher', 'mann beamter verwalter priester krieger soldat sklave fuhrer konig'),
}
CLS = list(CLASSES)
MOVES = {'621': 'H10_8', '161': 'H10_8', '527': 'H10_8', '241': 'H10_8', '824': 'H10_9', '880': 'H10_9', '545': 'H10_9', '091': 'H10_9'}
GERMAN = {'elamite_hinzkoch'}
FAMILIES = collections.OrderedDict([
    ('Dravidian', ['dedr_tamil', 'dedr_malayalam', 'dedr_kannada', 'dedr_telugu', 'tamil_wiktionary', 'telugu_wiktionary', 'kannada_wiktionary']),
    ('Munda', ['santali_campbell', 'santali_bodding5', 'santali_wiktionary', 'mundari_bhadra']),
    ('Indo-Aryan', ['sanskrit_mw', 'oia_turner', 'proto_indoiranian_wiktionary']),
    ('Sumerian', ['sumerian_halloran', 'sumerian_wiktionary']),
    ('Akkadian', ['akkadian_wiktionary']),
    ('Elamite', ['elamite_hinzkoch']),
    ('Burushaski', ['burushaski_lorimer']),
])
DISTS = ['strict', 'medium', 'loose']; BREADTHS = ['narrow', 'wide']
KEYS = [(d, b) for d in DISTS for b in BREADTHS]
N1, N2, N4 = 2000, 2000, 2000
N3 = int(os.environ.get('LANG_M2_N3', 500))
VARIANTS = {'A_3of3': {'3of3'}, 'B_3of3+2of3': {'3of3', '2of3'}}
PRIMARY = 'B_3of3+2of3'


def kw_terms(c, breadth, de=False):
    _, nE, wE, nD, wD = CLASSES[c]
    nar, wid = (nD, wD) if de else (nE, wE)
    return set(nar.split()) | (set(wid.split()) if breadth == 'wide' else set())
ALL_KW_EN = set().union(*[kw_terms(c, 'wide') for c in CLS])


def blind_nouns():
    return sorted({t for r in csv.DictReader(open(f'{ROOT}/work_data/pictures/pictures_blind.csv', encoding='utf-8'))
                   if r['level'] in ('3of3', '2of3') for t in r['agreed_things'].split(';') if t})
def outside_list():
    pics = set(); [pics.update(pic_terms_en(n)) for n in blind_nouns()]
    return [(e, d) for e, d in OUTSIDE if e not in pics and e not in ALL_KW_EN]


def plain(t):
    t = unicodedata.normalize('NFD', t.lower())
    return ''.join(c for c in t if not unicodedata.combining(c)).replace('ß', 'ss')
def words(gl, n): return re.findall(r'[a-z]+', plain(gl))[:n]


class Lex:
    """one dictionary: entry id, norm form, skeleton, gloss; sound-alike indexes; picture flags; class keyword matrix."""
    def __init__(self, name, nouns, outside):
        self.name = name; self.de = name in GERMAN
        rows = [l.rstrip('\n').split('\t') for l in open(f'{LEX}/{name}.tsv', encoding='utf-8')]
        self.eid = [r[0] for r in rows]; self.hw = [r[1] for r in rows]; self.nf = [r[2] for r in rows]
        self.sk = [r[3] for r in rows]; self.gl = [r[4] for r in rows]
        self.n = len(rows); self.nentries = len(set(self.eid))
        inv3 = collections.defaultdict(set); inv5 = collections.defaultdict(set)
        for i, g in enumerate(self.gl):
            for k, w in enumerate(words(g, 5)):
                forms = {w} | ({w[:-1]} if w.endswith('s') else set()) | ({w[:-2]} if w.endswith('es') else set())
                for f_ in forms:
                    inv5[f_].add(i)
                    if k < 3: inv3[f_].add(i)
        terms = {}
        for nn in nouns:
            terms[nn] = set(DE.get(nn, '').split()) if self.de else pic_terms_en(nn)
        for e, d in outside: terms[f'OUT:{e}'] = {d if self.de else e}
        self.pic_flag = {k: set().union(*[inv3.get(t, set()) for t in ts]) if ts else set() for k, ts in terms.items()}
        self.is_pic = {k: sorted(v) for k, v in self.pic_flag.items()}
        self.kwkeys = [(c, b) for c in CLS for b in BREADTHS]
        self.kwmat = np.zeros((self.n, len(self.kwkeys)), dtype=bool)
        for col, (c, b) in enumerate(self.kwkeys):
            for t in kw_terms(c, b, self.de):
                for i in inv5.get(t, ()): self.kwmat[i, col] = True
        self.eid_arr = np.array(self.eid)
        self.by_nf = collections.defaultdict(list); self.by_sk = collections.defaultdict(list); self.by_del = collections.defaultdict(list)
        for i in range(self.n):
            self.by_nf[self.nf[i]].append(i); self.by_sk[self.sk[i]].append(i)
            for key in self.dels(self.sk[i]): self.by_del[key].append(i)

    @staticmethod
    def dels(s):
        if len(s) < 2: return {('=', s)}
        return {('=', s)} | {('-', s[:k] + s[k + 1:]) for k in range(len(s))} | {('+', s)}

    def near_form(self, nf, dist):   # identical to lang_m_common.Lex.near_form
        if dist == 'strict': return self.by_nf.get(nf, [])
        sk = re.sub(r'[aeiou]', '', nf)
        if dist == 'medium' or len(sk) < 2: return self.by_sk.get(sk, [])
        out = set()
        mine = {('-', sk[:k] + sk[k + 1:]) for k in range(len(sk))}
        for key in mine:
            out.update(self.by_del.get(key, []))
            out.update(i for i in self.by_sk.get(key[1], []))
        for i in self.by_del.get(('-', sk), []): out.add(i)
        out.update(self.by_sk.get(sk, []))
        return [i for i in out if len(self.sk[i]) >= 2 or self.sk[i] == sk]
