#!/usr/bin/env python3
"""Job 2 of the fifth pass: the next 25 signs that block the most faces, plus 405/407 as thread/cloth.
Order kept for every sign: picture (sign_shapes.csv and the second catalogue's glyph drawing) and slot (first/mid/
last share on Lipi distinct texts) were printed, nothing else; the word was chosen; the predictions below were
written into this file before anything was computed on the new texts.  'fresh' = a kind of fact not printed for the
sign while choosing (and not in an earlier report); 'seen' = a kind that was.
Link notes built for this job (sound_v5_link.py and the crosswalk):
 - the second catalogue draws 405, 406 and 407 as one tree (M169); a rule learned from what follows the tree
   splits them no better than always guessing 405 (55 of 102 against 50), so on the new texts M169 is tested as
   the one tree family (it is stored as '405').
 - the bracketed seven 048 (M113) is absent from the new texts; 048 is tested on first-catalogue facts not printed before.
 - the second catalogue merges 525/526 into the guard 527 (M254), 838 into produce 806 (M389), 821 into the wheel
   820 (M391), 370 into 371 (M397), 491 into 495 (M205), 519 into 910 (M292): each merge is itself a word guess
   (the variant carries the main sign's word) and is tested with a frame test (same left and right neighbours).
Writes work_data/sound_v5/gains_v4wide.csv and job2_tests.csv."""
from sound_v5_common import *
from sound_v4_values import V4, TIER4
from sound_v4_job2 import same_face
GOODS = {'ctab', 'mtab', 'tag', 'pot', 'tool', 'rod', 'bangle', 'other'}
FIBRE = {'390', '405', '406', '407'}
HORN2 = {'Zebu', 'Buff', 'Gaur', 'Bull', 'Goat'}
SHARE = {'861', '817', '877'}


def lots_before(s, cat='LM'):
    """a count of 3 or more stands right before s, against the same share before any sign."""
    k = n = K = N = 0
    for x, P, st, g in faces_all(cat):
        for i, a in enumerate(x):
            hit = i > 0 and x[i - 1] in VAL and VAL[x[i - 1]] >= 3
            N += 1; K += hit
            if a == s: n += 1; k += hit
    if n < 3: return None
    return res(k / n > K / N, binomtest(k, n, K / N, alternative='greater').pvalue, f'a count of 3+ right before it {k}/{n} = {k / n:.0%} against {K / N:.1%} ({cat})')


def animal_any(S, animals):
    se = objs[objs.seal & ~objs.noanimal]
    return share(se.animal.isin(animals), se[se.signs.apply(lambda z: bool(z & S))].animal.isin(animals), f'seals with {"/".join(sorted(S))} showing {"/".join(sorted(animals))}')


def same_face_set(S, T, cat='LM'):
    rows = kfaces(cat)
    return share([bool(T & set(x)) for x, k, st in rows], [bool(T & (set(x) - S)) for x, k, st in rows if S & set(x)], f'faces with {"/".join(sorted(S))} that carry {sorted(T)[:5]} ({cat})')


# sign: (picture, slot, [(stage, word, English, DEDR, prediction, basis, test)])
J = {
 '407': ('simple tree with branches (M169, drawn as one sign with 405/406)', 'last 34 / mid 18', [
   ('A', 'tuṇi', 'cloth, a piece of cloth', '3305', 'cloth is issued in amounts: the other face of a many-faced object with 407 carries a number or cup', 'fresh', lambda: reverse_has('407', NUMCUP)),
   ('B', 'tuṇi', 'cloth', '3305', 'the tree family on new texts (M169) sits on goods objects (tablets, tags, pots, tools) more than all new-text faces', 'seen', lambda: on_kind('405', GOODS, 'Mu'))]),
 '405': ('simple tree with branches (M169)', 'last 29 / mid 23', [
   ('A', 'nūl', 'thread, yarn', '3726', 'thread is counted in lots: on new texts (tree family M169) a count of 3 or more stands right before it', 'seen', lambda: lots_before('405', 'Mu')),
   ('B', 'nūl', 'thread', '3726', 'issued in amounts: the other face of a many-faced object with 405 carries a number or cup', 'fresh', lambda: reverse_has('405', NUMCUP))]),
 '692': ('X drawn in outline (crossed bars)', 'first 36 of 46', [
   ('A', 'kūṭṭam', 'assembly, council (crossing = joining)', '1882', 'an institution of the whole land: 692 turns up at more sites than signs of its frequency', 'fresh', lambda: multi_site('692', 'LM')),
   ('B', 'kūṭṭam', 'assembly', '1882', 'office seals are big: seals with 692 are bigger than seals with the same number of signs', 'fresh', lambda: seal_size('692', True, True))]),
 '165': ('loop with an inner swoop (M319)', 'first 6 / mid 6 / last 4', [
   ('A', 'poḻutu', 'sun, day', '4552', 'days are counted like things: counts beside it are short strokes (both catalogues)', 'fresh', lambda: count_series('165', 'short', 'LM')),
   ('B', 'poḻutu', 'day', '4552', 'a day count on a ration tablet: the other face of a many-faced object with 165 carries a number or cup', 'fresh', lambda: reverse_has('165', NUMCUP))]),
 '645': ('plain X (M137)', 'mid 9 / first 3 / last 3', [
   ('A', 'kar̤añcu', 'a gold weight (1/6 oz)', '1348', 'the gold hoards: Mohenjo-daro objects with 645 lie in the DK area', 'fresh', lambda: moh_area('645', 'DK')),
   ('B', 'kar̤añcu', 'a gold weight', '1348', 'weights are counted: a number stands two places before or after 645', 'fresh', lambda: two_away('645', set(VAL), (-2, 2)))]),
 '167': ('arch with a ring at each foot: a balance beam with two pans (M321)', 'first 2 / last 4', [
   ('A', 'tūkku', 'weighing, a weighed amount', '3376', 'n kalam weighed: a number stands two places before 167 (first catalogue)', 'fresh', lambda: two_away('167', set(VAL), (-2,), 'L')),
   ('B', 'tūkku', 'weighed', '3376', 'a weighed issue: the other face of a many-faced object with 167 carries a number or cup', 'fresh', lambda: reverse_has('167', NUMCUP))]),
 '711': ('U-vessel with hatched slanting base (M341)', 'mid 3', [
   ('A', 'vaḷḷam', 'a grain measure (vessel)', '5316', 'a container measure: counts after it are tall strokes (both catalogues)', 'fresh', lambda: count_series('711', 'tall', 'LM', 'after')),
   ('B', 'vaḷḷam', 'grain measure', '5316', 'measure, count, cup: the cup 700 stands two places after 711', 'seen', lambda: two_away('711', {'700'}, (2,)))]),
 '236': ('fish with a caret hat (the Bamboo sign) caged by four strokes (M66)', 'mid 9 / last 7', [
   ('A', 'vēy-kūṭu', 'bamboo crate, bamboo basket', '5541 vēy + 1883 kūṭu', 'a container: counts beside it are tall strokes (both catalogues)', 'fresh', lambda: count_series('236', 'tall', 'LM')),
   ('B', 'vēy-kūṭu', 'bamboo crate', '5541 + 1883', 'counted goods: new-text faces with it carry a number more than faces overall', 'fresh', lambda: with_count('236', 'Mu'))]),
 '048': ('seven strokes in brackets (M113; absent from new texts)', 'mid 5 / last 1', [
   ('A', 'er̤uvar', 'the Seven (a body of seven)', '910', 'the Seven is a house with agents: the man 090 stands two places after 048 (048-jar-man)', 'fresh', lambda: two_away('048', {'090'}, (2,), 'L')),
   ('B', 'er̤uvar', 'the Seven', '910', 'a trading body: trade-tag words (dozen 055, given 890, sale 892, fish 220) on the same face (first catalogue)', 'fresh', lambda: cooccur('048', {'055', '890', '892', '220'}, 'L'))]),
 '832': ('leaf/eye with a stroke inside: an eye with its pupil (M375)', 'mid 10 / last 8 / first 6', [
   ('A', 'kaṇkāṇi', 'overseer (kaṇ eye + kāṇ see)', '1443', 'an overseer outranks: seals with 832 are bigger than seals with the same number of signs', 'fresh', lambda: seal_size('832', True, True)),
   ('B', 'kaṇkāṇi', 'overseer', '1443', 'a title in the possessive place: faces with 832 carry the jar less than faces overall', 'fresh', lambda: no_jar('832', 'L'))]),
 '526': ('small hatched box with corner strokes, same drawing code as the guard 527 (M254 = 527)', 'last 9 of 9', [
   ('A', 'kāval', 'guard (variant of 527)', '1416', 'one word with the guard: 526 stands in the frames of 527/525', 'fresh', lambda: frame_swap('526', {'527', '525'})),
   ('B', 'kāval', 'guard', '1416', 'a title in the possessive place: faces with 526 carry the jar less than faces overall', 'fresh', lambda: no_jar('526', 'L'))]),
 '525': ('hatched box with strokes (M254 = guard 527)', 'mid 5 / last 1', [
   ('A', 'kāval', 'guard (variant of 527)', '1416', 'one word with the guard: 525 stands in the frames of 527/526', 'fresh', lambda: frame_swap('525', {'527', '526'})),
   ('B', 'kāval', 'guard', '1416', 'a title in the possessive place: faces with 525 carry the jar less than faces overall', 'fresh', lambda: no_jar('525', 'L'))]),
 '868': ('diamond with a small diamond on top (the share sign 817/861) plus an inner line (M275)', 'last 2 of 2', [
   ('A', 'kāṇi', 'share, holding (variant of 817/861)', '1444', 'one word with the share signs: 868 stands in the frames of 861/817/877', 'fresh', lambda: frame_swap('868', SHARE)),
   ('B', 'kāṇi', 'share', '1444', 'a counted holding: new-text faces with 868 carry a number', 'fresh', lambda: with_count('868', 'Mu'))]),
 '222': ('fish between brackets with a sprig (M62)', 'mid 7 / first 1', [
   ('A', 'kuḷa-mīn', 'Tank-star / tank fish (fish between two banks)', '1828 kuḷam', 'a name element: new-text faces with 222 carry the jar more than faces overall', 'fresh', lambda: same_face('222', {'740'}, 'Mu')),
   ('B', 'kuḷa-mīn', 'Tank-star', '1828', 'a house name: Mohenjo-daro house-mates share it', 'fresh', lambda: house_share('222', where='any', seals=False))]),
 '161': ('person with two loads, triangle head: the load-carrier (M14)', 'last 10 of 11', [
   ('A', 'kā', 'keeper, carrier (variant of the carriers 151-158)', 'base', 'stands in the jar\'s place: faces with 161 carry the jar less than faces overall (both catalogues)', 'fresh', lambda: no_jar('161', 'LM')),
   ('B', 'kā', 'keeper', 'base', 'one word with the carriers: 161 stands in the frames of the other carriers', 'fresh', lambda: frame_swap('161', PORTER - {'161'}))]),
 '495': ('curved horn with bands (M205, drawn as one sign with 491)', 'first 9 / mid 9', [
   ('A', 'kompu', 'horn, tusk; horn-blower (the old "branch" word read off the picture as horn)', '2115', 'a horn word: seals with 495/491 show a horned beast other than the unicorn (zebu, buffalo, gaur, short-horned bull, goat) more than beast seals overall', 'fresh', lambda: animal_any({'495', '491'}, HORN2)),
   ('B', 'kompu', 'horn', '2115', 'one sign with 491: 495 stands in the frames of 491', 'fresh', lambda: frame_swap('495', {'491'}))]),
 '491': ('curved horn with bands (M205 = 495)', 'first 9 / mid 2', [
   ('A', 'kompu', 'horn (variant of 495)', '2115', 'one sign with 495: 491 stands in the frames of 495', 'fresh', lambda: frame_swap('491', {'495'})),
   ('B', 'kompu', 'horn', '2115', 'a horn-named house: Mohenjo-daro house-mates share 491/495', 'fresh', lambda: house_share('491', pred=lambda o: bool(o.signs & {'491', '495'}), seals=False))]),
 '460': ('three tall triangles: three peaks (M230)', 'mid 25 / first 1', [
   ('A', 'mukkōṭu', 'Three-peaks (a place name)', '2200 kōṭu peak', 'a place word: 460 stands in the frames of the hill 503', 'fresh', lambda: frame_swap('460', {'503'})),
   ('B', 'mukkōṭu', 'Three-peaks', '2200', 'a place-named house: Mohenjo-daro house-mates share it', 'fresh', lambda: house_share('460', where='any', seals=False))]),
 '838': ('leaf with a branched stem inside (M389 = produce 806)', 'mid 7 / first 3', [
   ('A', 'viḷai', 'produce, crop (variant of 806, as the second catalogue draws it)', '5427', 'one word with produce: 838 stands in the frames of 806', 'fresh', lambda: frame_swap('838', {'806'})),
   ('B', 'viḷai', 'produce', '5427', 'produce is counted: a number stands two places before 838 (n [unit] produce)', 'fresh', lambda: two_away('838', set(VAL), (-2,)))]),
 '370': ('stroke through a ring with a dot: a spindle with its whorl (M397, merged with 371)', 'first 5 of 7', [
   ('A', 'katir', 'spindle (Tamil Lexicon p. 712 sense 6); also ear of grain, ray', 'TL p.712; DEDR 1194', 'a spinner\'s word: faces with 370/371 carry a fibre sign (390, 405, 406, 407) more than faces overall', 'fresh', lambda: same_face_set({'370', '371'}, FIBRE, 'LM')),
   ('B', 'katir', 'spindle', 'TL p.712', 'one sign with 371: 370 stands in the frames of 371', 'fresh', lambda: frame_swap('370', {'371'}))]),
 '565': ('two crossed fletched arrows (M224)', 'last 7 of 11', [
   ('A', 'maṟavaṉ', 'warrior (crossed arrows = fighting)', '4763 maṟam', 'a title in the possessive place: faces with 565 carry the jar less than faces overall (both catalogues)', 'fresh', lambda: no_jar('565', 'LM')),
   ('B', 'maṟavaṉ', 'warrior', '4763', 'a rank title: 565 stands in the frames of the chief 520', 'fresh', lambda: frame_swap('565', {'520'}))]),
 '519': ('a ticked stalk between dotted brackets: a fenced plant (M292 = 910)', 'first 4 / mid 4', [
   ('A', 'tōṭṭam', 'garden, fenced plot', 'Ta. tōṭṭam (not found in local DEDR)', 'a land word: faces with 519 carry field/hill/sheaf/quarter words (615, 503, 845, 061) (both catalogues)', 'fresh', lambda: same_face('519', {'615', '503', '845', '061'}, 'LM')),
   ('B', 'tōṭṭam', 'garden', '', 'one sign with 910 (the second catalogue merges them): 519 stands in the frames of 910', 'fresh', lambda: frame_swap('519', {'910'}))]),
 '850': ('plain diamond (M261)', 'mid 12 / first 7 / last 3', [
   ('A', 'kāṇi', 'share (the bare diamond; new word after kaṇ/kaṉ)', '1444', 'a counted holding: on new texts a count follows 850', 'fresh', lambda: next_count('850')),
   ('B', 'kāṇi', 'share', '1444', 'one word with the share signs: 850 stands in the frames of 861/817', 'fresh', lambda: frame_swap('850', {'861', '817'}))]),
 '347': ('deer facing right', 'first 1 / mid 1 (8 faces, copies)', [
   ('A', 'māṉ', 'deer (a name or a hide good)', '4780', 'a counted good: the other face of a many-faced object with 347 carries a number or cup', 'fresh', lambda: reverse_has('347', NUMCUP)),
   ('B', 'māṉ', 'deer', '4780', 'a counted good: a number on the same face (first catalogue)', 'fresh', lambda: cooccur('347', set(VAL), 'L'))]),
 '821': ('lens with an X inside: a spoked wheel (M391 = wheel 820)', 'first 4 / mid 4 / last 1', [
   ('A', 'kāl', 'quarter (variant of the wheel 820)', '1468', 'one word with the wheel: 821 stands in the frames of 820', 'fresh', lambda: frame_swap('821', {'820'})),
   ('B', 'kāl', 'quarter', '1468', 'kāl iru: the two-stroke 002 follows 821 (first catalogue)', 'fresh', lambda: adjacent('821', {'002'}, 'next', 'L'))]),
 '792': ('no drawing in the shape table; Wells 790s are the leaf/lens family (790 maṇi)', 'first 3 / mid 4', [
   ('A', 'maṇi', 'gem, bead (variant of 790); as a house name "Gem"', '4672', 'one word with 790: 792 stands in the frames of 790', 'fresh', lambda: frame_swap('792', {'790'})),
   ('B', 'maṇi', 'Gem (house name)', '4672', 'a house name: Mohenjo-daro house-mates share it', 'fresh', lambda: house_share('792', where='any', seals=False))]),
}

if __name__ == '__main__':
    g, gd, gs = gains(TIER4)
    pd.DataFrame([dict(sign=s, faces=n, distinct=len(gd[s]), seal_faces=gs[s], tier_v4=TIER4.get(s, '-'), sound_v4=V4.get(s, ('', ''))[0])
                  for s, n in g.most_common()]).to_csv(f'{OUT5}/gains_v4wide.csv', index=False)
    rows = []; n = sum(len(v[2]) for v in J.values()); i = 0
    print(f'job 2: {len(J)} signs, {n} predictions, written before this run', flush=True)
    for s, (pic, slot, L) in J.items():
        for st, w, en, ref, pred, fr, fn in L:
            i += 1; print(f'({i}/{n})', end=' ')
            r = run(st, s, w, pred, fn); r.update(english=en, dedr=ref, fresh=fr, picture=pic, gain=g.get(s, 0)); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT5}/job2_tests.csv', index=False)
    print('\nsummary:', df.outcome.value_counts().to_dict())
