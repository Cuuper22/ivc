#!/usr/bin/env python3
"""lang_m shared pieces. Fixed before scoring; ONE redesign after the first trial run saturated (picture word = any gloss with the term in
its first 6 words, keyword anywhere in the first 12 words, every sign counted separately: Tamil and Sanskrit both hit 103-149 of 149 signs
and every control sat at the same level, so the test had no power). The redesign tightened both gloss windows and scores distinct
(picture, job) units; it was applied to every language alike and chosen before any language-to-language comparison was looked at.
picture-noun gloss terms (how a dictionary word is recognised as the word for a pictured thing), job keyword sets (narrow / wide,
the same for every language; German copies for the German-glossed Elamite dictionary), the outside noun list for control 2,
the three sound-distance settings, dictionary loading and the sound-alike index.

Sound distance (on the normalised form, vowel length ignored, see lang_m_lexicons.py):
  strict : same normalised form (a homophone up to vowel length and diacritics)
  medium : same consonant skeleton (vowels free)
  loose  : consonant skeletons share a one-deletion form (one consonant changed, added or dropped), for skeletons of 2+ consonants;
           1-consonant skeletons stay at 'medium'.
Picture word: an entry with a picture term as a whole word among the first 3 words of its gloss (the plain word for the thing).
Job hit: a DIFFERENT entry within the sound distance of a picture word, not itself glossed with that picture's terms (that would be the
same word, not a pun), whose gloss (first 5 words: its main sense) contains a job keyword as a whole word (plural -s / -es allowed).
"""
import re, csv, collections, unicodedata
import numpy as np
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/lang_m'

PIC_EN = {
    'person': 'man person human male', 'fish': 'fish', 'bird': 'bird', 'duck': 'duck', 'jar': 'jar pot pitcher waterpot',
    'leaf': 'leaf', 'tree': 'tree', 'plant': 'plant', 'flower': 'flower blossom', 'sapling': 'sapling shoot', 'branch': 'branch bough',
    'wheel': 'wheel', 'bow': 'bow', 'arrow': 'arrow', 'spear': 'spear lance', 'pitchfork': 'fork pitchfork trident', 'table': 'table stool',
    'deer': 'deer antelope stag', 'cow': 'cow ox bull', 'spider': 'spider', 'wheat': 'wheat', 'garlic': 'garlic', 'heart': 'heart',
    'ladder': 'ladder', 'flag': 'flag banner', 'staff': 'staff rod', 'stick': 'stick', 'burden': 'burden load', 'pond': 'pond pool',
    'lyre': 'lyre harp', 'paw': 'paw', 'cat': 'cat', 'mountain': 'mountain hill', 'wave': 'wave', 'pincers': 'pincers tongs',
    'sun': 'sun', 'rake': 'rake', 'antenna': 'antenna feeler horn'}
PIC_DE = {
    'person': 'mann mensch', 'fish': 'fisch', 'bird': 'vogel', 'duck': 'ente', 'jar': 'krug topf gefass', 'leaf': 'blatt', 'tree': 'baum',
    'plant': 'pflanze', 'flower': 'blume blute', 'sapling': 'schossling setzling', 'branch': 'zweig ast', 'wheel': 'rad', 'bow': 'bogen',
    'arrow': 'pfeil', 'spear': 'speer lanze', 'pitchfork': 'gabel', 'table': 'tisch', 'deer': 'hirsch gazelle', 'cow': 'kuh rind stier',
    'spider': 'spinne', 'wheat': 'weizen', 'garlic': 'knoblauch', 'heart': 'herz', 'ladder': 'leiter', 'flag': 'fahne', 'staff': 'stab',
    'stick': 'stock', 'burden': 'last', 'pond': 'teich', 'lyre': 'leier', 'paw': 'pfote', 'cat': 'katze', 'mountain': 'berg',
    'wave': 'welle', 'pincers': 'zange', 'sun': 'sonne', 'rake': 'rechen', 'antenna': 'fuhler horn'}
# outside concrete nouns for control 2 (none is a job keyword); English and German
OUTSIDE = [('water', 'wasser'), ('fire', 'feuer'), ('stone', 'stein'), ('rope', 'seil'), ('knife', 'messer'), ('axe', 'axt'),
           ('boat', 'boot'), ('cart', 'wagen'), ('horse', 'pferd'), ('dog', 'hund'), ('snake', 'schlange'), ('frog', 'frosch'),
           ('elephant', 'elefant'), ('tiger', 'tiger'), ('buffalo', 'buffel'), ('crab', 'krebs'), ('scorpion', 'skorpion'), ('ant', 'ameise'),
           ('bee', 'biene'), ('egg', 'ei'), ('hand', 'hand'), ('foot', 'fuss'), ('eye', 'auge'), ('ear', 'ohr'), ('nose', 'nase'),
           ('mouth', 'mund'), ('tooth', 'zahn'), ('hair', 'haar'), ('bone', 'knochen'), ('blood', 'blut'), ('skin', 'haut'), ('net', 'netz'),
           ('mat', 'matte'), ('door', 'tur'), ('wall', 'mauer'), ('road', 'weg'), ('river', 'fluss'), ('sand', 'sand'), ('salt', 'salz'),
           ('oil', 'ol'), ('milk', 'milch'), ('honey', 'honig'), ('cloth', 'tuch'), ('thread', 'faden'), ('needle', 'nadel'),
           ('drum', 'trommel'), ('bell', 'glocke'), ('ring', 'ring'), ('bead', 'perle'), ('shell', 'muschel'), ('feather', 'feder'),
           ('nest', 'nest'), ('root', 'wurzel'), ('grass', 'gras'), ('thorn', 'dorn'), ('rain', 'regen'), ('cloud', 'wolke'),
           ('wind', 'wind'), ('ash', 'asche'), ('clay', 'ton'), ('copper', 'kupfer'), ('gold', 'gold')]

KW = {  # job -> (narrow, wide additions), English
    'OPENER': ('seal mark sign office temple god palace', 'lord king deity holy sacred city state authority command order property own owner'),
    'CREST': ('star clan house lineage family tribe', 'caste kin race ancestor totem god goddess sun moon planet constellation home household'),
    'NAME': ('son daughter child beloved gift good great young', 'name brave strong fair beautiful wise lucky fortune joy bright shining noble dear little small big star god'),
    'TAG': ('son child offspring descendant junior elder', 'person man one people servant dear born younger older'),
    'TITLE': ('chief lord servant keeper guard master ruler king headman', 'man junior elder owner agent officer steward priest warrior soldier slave attendant leader manager house belonging'),
    'MEASURE': ('measure vessel share quarter weight portion', 'unit capacity basket sack bag pot jar cup load half part ration quantity volume'),
    'COUNTED': ('animal cattle sheep goat grain crop', 'head produce fruit harvest rice barley wheat seed worker labourer slave person cow bundle bunch'),
    'TIME': ('day month year season moon', 'time night festival period cycle week morning evening'),
}
KW_DE = {
    'OPENER': ('siegel zeichen marke amt tempel gott palast', 'herr konig gottheit heilig stadt staat befehl eigentum besitz besitzer'),
    'CREST': ('stern sippe haus geschlecht familie stamm', 'kaste verwandte ahn ahne gott gottin sonne mond planet sternbild heim haushalt'),
    'NAME': ('sohn tochter kind geliebt geschenk gut gross jung', 'name tapfer stark schon weise gluck freude hell glanzend edel lieb klein stern gott'),
    'TAG': ('sohn kind nachkomme junger alter altester', 'person mann leute diener geboren'),
    'TITLE': ('hauptling herr diener huter wachter meister herrscher konig vorsteher', 'mann junger alter besitzer beamter verwalter priester krieger soldat sklave fuhrer haus'),
    'MEASURE': ('mass gefass anteil viertel gewicht portion', 'einheit korb sack beutel topf krug becher last halfte teil ration menge'),
    'COUNTED': ('tier vieh rind schaf ziege getreide korn', 'kopf ertrag frucht ernte reis gerste weizen saat arbeiter sklave person kuh bundel'),
    'TIME': ('tag monat jahr jahreszeit mond', 'zeit nacht fest periode woche morgen abend'),
}
JOBS = list(KW)
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


def plain(t):
    t = unicodedata.normalize('NFD', t.lower())
    return ''.join(c for c in t if not unicodedata.combining(c)).replace('ß', 'ss')
def words(gl, n): return re.findall(r'[a-z]+', plain(gl))[:n]
def has_any(ws, terms):
    for w in ws:
        if w in terms or (w.endswith('s') and w[:-1] in terms) or (w.endswith('es') and w[:-2] in terms): return True
    return False


class Lex:
    """one dictionary: arrays of entry id, norm form, skeleton, gloss; sound-alike indexes; gloss flags."""
    def __init__(self, name):
        self.name = name; self.de = name in GERMAN
        rows = [l.rstrip('\n').split('\t') for l in open(f'{OUT}/lex/{name}.tsv', encoding='utf-8')]
        self.eid = [r[0] for r in rows]; self.hw = [r[1] for r in rows]; self.nf = [r[2] for r in rows]
        self.sk = [r[3] for r in rows]; self.gl = [r[4] for r in rows]
        self.n = len(rows); self.nentries = len(set(self.eid))
        inv6 = collections.defaultdict(set); inv12 = collections.defaultdict(set)
        for i, g in enumerate(self.gl):
            for k, w in enumerate(words(g, 5)):
                forms = {w} | ({w[:-1]} if w.endswith('s') else set()) | ({w[:-2]} if w.endswith('es') else set())
                for f_ in forms:
                    inv12[f_].add(i)
                    if k < 3: inv6[f_].add(i)
        pic = PIC_DE if self.de else PIC_EN; kw = KW_DE if self.de else KW
        self.pic_terms = {k: set(v.split()) for k, v in pic.items()}
        self.pic_terms.update({f'OUT:{e}': {(d if self.de else e)} for e, d in OUTSIDE})
        self.pic_flag = {k: set().union(*[inv6.get(t, set()) for t in ts]) for k, ts in self.pic_terms.items()}
        self.is_pic = {k: sorted(v) for k, v in self.pic_flag.items()}
        self.kwkeys = [(j, b) for j in JOBS for b in BREADTHS]
        self.kwmat = np.zeros((self.n, len(self.kwkeys)), dtype=bool)
        for c, (j, b) in enumerate(self.kwkeys):
            nar, wid = kw[j]; terms = set(nar.split()) | (set(wid.split()) if b == 'wide' else set())
            for t in terms:
                for i in inv12.get(t, ()): self.kwmat[i, c] = True
        self.eid_arr = np.array(self.eid)
        self.by_nf = collections.defaultdict(list); self.by_sk = collections.defaultdict(list); self.by_del = collections.defaultdict(list)
        for i in range(self.n):
            self.by_nf[self.nf[i]].append(i); self.by_sk[self.sk[i]].append(i)
            for key in self.dels(self.sk[i]): self.by_del[key].append(i)

    @staticmethod
    def dels(s):
        if len(s) < 2: return {('=', s)}
        return {('=', s)} | {('-', s[:k] + s[k + 1:]) for k in range(len(s))} | {('+', s)}

    def near_form(self, nf, dist):
        """indexes of words whose sound is within `dist` of a normalised form nf."""
        if dist == 'strict': return self.by_nf.get(nf, [])
        sk = re.sub(r'[aeiou]', '', nf)
        if dist == 'medium' or len(sk) < 2: return self.by_sk.get(sk, [])
        out = set()
        mine = {('-', sk[:k] + sk[k + 1:]) for k in range(len(sk))}
        for key in mine:  # deletion of mine == deletion of theirs (substitution) or == theirs whole (theirs one shorter)
            out.update(self.by_del.get(key, []))
            out.update(i for i in self.by_sk.get(key[1], []))
        for i in self.by_del.get(('-', sk), []): out.add(i)   # theirs one longer
        out.update(self.by_sk.get(sk, []))
        return [i for i in out if len(self.sk[i]) >= 2 or self.sk[i] == sk]
