#!/usr/bin/env python3
"""Short picture-words for signs (what the sign LOOKS like, from work_data/sign_shapes.csv; no meanings).
Signs not in the hand list get the first words of their shape description; signs with no description get 'sign NNN'."""
import pandas as pd, re
ROOT = '/home/claude/ivc'
_sh = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).fillna('')
SHAPE = dict(zip(_sh.lipi_wells_number, _sh.shape_description))
PIC = {
    '740': 'jar', '741': 'jar with mark', '742': 'jar variant', '745': 'jar variant 745', '746': 'jar variant 746',
    '002': 'two strokes', '001': 'one stroke', '003': 'three strokes', '004': 'four strokes', '005': 'five strokes',
    '006': 'six strokes', '007': 'seven strokes', '012': 'two stacked strokes', '013': 'three stacked strokes',
    '014': 'four stacked strokes', '015': 'five stacked strokes', '016': 'six stacked strokes', '017': 'seven stacked strokes',
    '018': 'eight stacked strokes', '031': 'one tall stroke', '032': 'two tall strokes', '033': 'three tall strokes',
    '034': 'four tall strokes', '035': 'five tall strokes', '036': 'six tall strokes',
    '220': 'fish', '231': 'fish with stroke', '233': 'barred fish', '235': 'capped fish', '236': 'caged capped fish',
    '240': 'whiskered fish', '241': 'caged whiskered fish', '226': 'fish with four ticks', '222': 'bracketed fish', '243': 'hatched capped fish',
    '400': 'comb', '520': 'spear', '090': 'man', '091': 'two men', '097': 'bracketed man', '095': 'man with stick',
    '820': 'wheel', '861': 'diamond', '817': 'diamond variant', '920': 'bracket with leaf', '692': 'outlined X',
    '060': 'short-tall stroke pair', '590': 'box with bar', '595': 'barred box', '705': 'U with stroke', '706': 'U with stroke variant',
    '700': 'cup', '703': 'cup with three strokes', '390': 'tree', '405': 'tree variant 405', '406': 'tree variant 406', '407': 'tree variant 407',
    '798': 'leaf with pincers', '415': 'pitchfork', '416': 'double pitchfork', '176': 'sitting person with ticks', '175': 'sitting person',
    '803': 'leaf on tree', '806': 'leaf on tree variant', '100': 'three-headed person', '760': 'branched U', '752': 'branched U variant',
    '368': 'winged stroke', '365': 'winged stroke variant', '255': 'odd animal', '140': 'person with raised arm', '550': 'pincers',
    '556': 'pincers with stroke', '555': 'pincers variant', '840': 'two leaves', '900': 'bracket', '904': 'double bracket',
    '151': 'porter', '154': 'porter with jars', '155': 'porter 155', '156': 'porter with jars 156', '158': 'porter with jars 158',
    '161': 'porter with diamond', '153': 'porter 153', '690': 'nested chevrons', '575': 'trapezoid with box', '142': 'person with staff',
    '061': 'reversed lambda', '063': 'reversed lambda variant', '527': 'hatched box', '904': 'double bracket', '435': 'stroke with diagonal',
    '125': 'archer', '892': 'bow and arrow', '055': 'eight-stroke block', '388': 'hatched heart', '384': 'heart', '382': 'heart with stroke',
    '717': 'paw', '350': 'line with teeth', '354': 'line with teeth variant', '503': 'striped triangle', '455': 'three triangles',
    '440': 'open rectangle', '615': 'grid', '790': 'leaf', '832': 'leaf with stroke', '850': 'leaf variant', '831': 'leaf with diagonals',
    '460': 'three tall triangles', '070': 'stroke with arms', '072': 'stroke with arms variant', '923': 'outlined bracket',
    '480': 'tall caret', '066': 'tall caret with mark', '632': 'tall rectangle with strokes', '630': 'tall rectangle 630', '625': 'tall rectangle',
    '621': 'barred tall rectangle', '413': 'ear with crossbars', '165': 'joined brackets', '482': 'outlined caret with diamond',
    '484': 'hatched caret', '335': 'joined M', '336': 'joined M variant', '337': 'joined M 337', '171': 'T with leaf',
    '845': 'two hatched leaves', '104': 'person with caret', '877': 'diamond with four diamonds', '880': 'diamond with four diamonds 880',
    '679': 'X with table', '530': 'open bowtie', '540': 'bowtie', '545': 'bowtie with triangle', '554': 'open bowtie 554',
    '320': 'sign 320', '921': 'bracket with arc', '906': 'paired brackets', '065': 'stroke with hook', '297': 'rays',
    '374': 'curved plant', '111': 'person with U', '130': 'person with pitchfork', '500': 'divided triangle', '064': 'forked stroke',
    '565': 'closed X', '360': 'H', '315': 'H variant', '317': 'ladder', '510': 'square with lines', '511': 'square with lines 511',
    '853': 'diamond with arms', '190': 'spider', '772': 'U with forked arm', '773': 'U with forked arm 773', '927': 'double bracket 927',
    '371': 'garlic', '605': 'hatched tall box', '645': 'X', '812': 'leaf with hatched square', '408': 'measure 408', '426': 'sign 426',
    '465': 'A with comb', '466': 'A with comb', '467': 'A with comb', '468': 'A with comb', '469': 'A with comb', '470': 'A with comb',
    '471': 'A with comb', '472': 'A with comb', '473': 'A with comb', '474': 'A with comb', '475': 'A with comb', '269': 'big brackets',
    '782': 'picture sign 782', '780': 'picture sign 780', '341': 'deer sign', '753': 'hare sign', '417': 'sign 417', '838': 'sign 838',
}


def pic(s):
    if s in PIC: return PIC[s]
    if s in ('000', 'ALT'): return 'lost sign'
    t = SHAPE.get(s, '')
    if not t: return f'sign {s}'
    t = re.split(r'[,.;(]', t)[0].strip()
    w = t.split()
    return (' '.join(w[:4])).lower() + f' {s}'


# Blind pictures (work_data/pictures/pictures_blind.csv: things agreed by 2 or 3 blind describers for the second-catalogue
# drawings), mapped to first-catalogue numbers through the crosswalk (the rank-1 partner of each first-catalogue sign).
# pic_book(s) = the blind picture (up to two agreed things, joined by '/') where the sign has one, else pic(s).
def _blind():
    try:
        cw = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
        cw = cw[cw.rank_for_lipi_sign == '1']
        pb = pd.read_csv(f'{ROOT}/work_data/pictures/pictures_blind.csv', dtype=str).fillna('')
        pb = dict(zip(pb.glyph.astype(str), pb.agreed_things))
        out = {}
        for l, m_ in zip(cw.lipi, cw.mahadevan):
            try: v = pb.get(str(int(float(m_))), '')
            except ValueError: v = ''
            if v: out[l] = '/'.join(v.split(';')[:2])
        return out
    except FileNotFoundError:
        return {}


BLIND = _blind()


def pic_book(s):
    return BLIND.get(s) or pic(s)
