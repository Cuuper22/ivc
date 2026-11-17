#!/usr/bin/env python3
"""Alternative English renderer for the NAME part of a reading (no word value is changed).

WHAT IT DOES (plain words)
  The old renderer (corpus_build2.name_tokens / np_spelled_text) writes a name as a hyphen chain, numerals and measures included:
      Of the Bamboo-star-High-star-Twelve house.      Of the Two-Arrow-Boxed-cotton house.      Of the three kalam Ivory house.
  This renderer shows a name as ONE unit made of word-parts, each part separated by a space, with the number or measure that
  belongs to a part glossed beside it in brackets:
      Of the Bamboo-star High-star (twelve) house.    Of the Arrow (two) Boxed-cotton house.   Of the (three kalam) Ivory house.
  "child of" (the 752 / 760 sign) is written as a comma clause:  High-star, child of Hill-share.
  The English word of every part is still chosen by the slot rules of corpus_build2 (SW name / count / final / open, SHORT); this file only
  changes how the parts of a NAME are laid out. Only NAME pieces are touched; counts of goods, openers and endings keep their old text.
  The layout depends only on the SIGNS' structural role (word / number / measure / child-of), never on which word a sign carries, so the
  same layout rules apply identically to the real table and to every scrambled table.

HOW TO USE
  import render_names as rn
  rn.use_new(cb)            # patch corpus_build2 (module cb) so build() emits marked name pieces
  text = rn.finish(cb.build(x, r, kind)[0])      # turn the marked pieces into the new layout
  rn.use_old(cb)            # put the old renderer back (finish() is then not needed)
  Python  rn.demo()  prints a few examples old vs new.

Layout rules (in order)
  1. each word part (W) is shown as written by the slot rules, parts separated by one space;
  2. a spelled number that belongs to a part (Two-King, King-Twelve, Five-keeper) goes in brackets after the part: King (two);
  3. a measure count inside a name (three kalam) stays a bracketed gloss where it stands: (three kalam);
  4. a lone number between name parts is a bracketed gloss: (two);
  5. child-of: ', child of X' after another part, or 'Child of X' at the start."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus_build2 as _cb

S_ITEM, S_FLD = '\x01', '\x1f'
_OLD = {}


def _cap(w): return w[:1].upper() + w[1:]
def _pack(items): return '\x02' + S_ITEM.join(S_FLD.join(i) for i in items) + '\x03'


def _new_name_tokens(x, idx, R, kind, slot='name'):
    """name pieces as marked items; for slot != 'name' (goods words) the old text is kept"""
    cb = _cb
    if slot != 'name': return _OLD['name_tokens'](x, idx, R, kind, slot)
    items = []; idx = list(idx)
    for q in idx:
        s = x[q]
        if s == '390' and items and q - 1 in idx and x[q - 1] == '590' and items[-1][0] == 'W':
            items[-1] = ('W', 'Boxed-cotton', '0', ''); continue                  # same fixed house name as the old renderer
        if s in ('752', '760'):
            if items and items[-1][0] == 'W': items[-1] = ('W', items[-1][1], '1', items[-1][3])
            else: items.append(('K', '', '0', ''))
        else: items.append(('W', _cap(cb.eng(s, slot)), '0', ''))
    return _pack(items)


def _new_np_spelled(pc):
    cb = _cb
    t = pc['thing']; num = cb.numword(pc['v']).lower()
    if t == '060' and pc['order'] == 'both':
        return _pack([('W', cb.eng(t, 'name').capitalize() if False else 'Within', '0', num + ',' + cb.numword(pc['v2']).lower())])
    nw = _cap(cb.eng(t, 'name'))
    nums = [num] + ([cb.numword(pc['v2']).lower()] if pc['order'] == 'both' else [])
    return _pack([('W', nw, '0', ','.join(nums))])


def _new_np_count(pc):
    return _OLD['np_count_text'](pc) + '\x05'          # marked; stripped again by finish() unless it sits inside a name


def use_new(cb=None):
    cb = cb or _cb
    for k in ('name_tokens', 'np_spelled_text', 'np_count_text'):
        _OLD.setdefault(k, getattr(cb, k))
    cb.name_tokens = _new_name_tokens; cb.np_spelled_text = _new_np_spelled; cb.np_count_text = _new_np_count


def use_old(cb=None):
    cb = cb or _cb
    for k, v in _OLD.items(): setattr(cb, k, v)


_NUMW = '|'.join([_cap(w) for w in _cb.WORDS] + [r'\d+'])
_G = r'\x02[^\x03]*\x03'
_B = r'(?:' + _NUMW + r')(?![A-Za-z0-9])'
_M = r'(?:' + '|'.join(list(_cb.WORDS) + [_cap(w) for w in _cb.WORDS] + ['n']) + r')[^\x02\x03\x05;:]*?\x05'
_UNIT = r'(?:' + _G + '|' + _M + '|' + _B + ')'
_RUN = re.compile(_UNIT + r'(?:[- ]' + _UNIT + r')*')
_PIECE = re.compile('(' + _G + ')|(' + _M + ')|(' + _B + ')')


def _render_run(run):
    out = []; pend = False
    def add(s, comma=False):
        if not out: out.append(s)
        else: out.append((', ' if comma else ' ') + s)
    for m in _PIECE.finditer(run):
        if m.group(1):
            for it in m.group(1)[1:-1].split(S_ITEM):
                k, txt, ch, nums = it.split(S_FLD)
                if k == 'K': pend = True; continue
                s = txt
                if nums: s += ' (' + ', '.join(nums.split(',')) + ')'
                child = ch == '1' or pend
                if child:
                    s = ('child of ' if out else 'Child of ') + s
                pend = False
                add(s, comma=child and bool(out))
        elif m.group(2): add('(' + m.group(2).rstrip('\x05').strip() + ')')
        else: add('(' + m.group(3).lower() + ')')
    return ''.join(out)


def finish(text):
    """turn marked name pieces into the new layout; strip marks elsewhere"""
    def rep(m):
        run = m.group(0)
        if '\x02' not in run: return run.replace('\x05', '')
        return _render_run(run)
    t = _RUN.sub(rep, text)
    t = t.replace('\x05', '')
    assert not re.search('[\x01-\x05\x1f]', t), repr(t)
    return t


def demo():
    from sound_v4_common import d, lex, parse_face
    want = ['235-240-055-151', '700-820-002-231-705-033-520', '240-482-752-740', '705-500-741-001-055-220-740-090', '861-002-032-070-590-390-740', '706-033-923-740']
    by = {'-'.join(x): (x, k) for x, k in zip(d.tok, d.kind)}
    for w in want:
        if w not in by: continue
        x, k = by[w]; r = parse_face(x, lex)
        use_old(); old = _cb.build(x, r, k)[0]
        use_new(); new = finish(_cb.build(x, r, k)[0]); use_old()
        print(f'{w}\n   old: {old}\n   new: {new}')


if __name__ == '__main__': demo()
