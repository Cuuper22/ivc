#!/usr/bin/env python3
"""Stage C: a new word for each value whose stage-B better test went against (167, 233, 335, 645, 832), and a rival
word for 595 (stage A found it counted with short strokes, not the chest's tall ones).  Written before running.
Note: the object kinds of 595, 335, 645 and 832 on new texts were printed while writing this stage, so none of the
predictions below uses object kind for those signs.  Writes stage_c.csv."""
from sound_v3_common import *
C = {
 '167': ('kā', 'shoulder pole with slings at both ends (1417); the upside-down U with a ring at each end is the pole; kaḷam kā "keeper of the threshing floor"',
         'a closing class word like the load-carriers: 167 stands in the frames of the carriers 151-158', 'fresh', lambda: frame_swap('167', PORTER)),
 '233': ('kavar-mīn', 'Branch-star: the barred fish is 415 kavar + 220 mīn written as one sign',
         'a Mohenjo-daro deed house: on new texts it sits on copper tablets more than chance', 'fresh', lambda: on_kind('233', 'ctab')),
 '335': ('ūr', 'town, village (752); M on a box = walls on a platform; kōṭṭai ūr "fort town"',
         'a place word closing a name: on new texts the jar or maka 760 follows it', 'fresh', lambda: adjacent('335', {'740', '760'}, 'next', 'Mu')),
 '645': ('kar̤añcu', 'a gold weight (1348); X counted seven on the gold object M-2129',
         'a weight unit takes its number after it (like kuṉṟi 480): on new texts a count follows it', 'fresh', lambda: next_count('645')),
 '832': ('maṇi', 'gem, bead (Ta. kaṇ-maṇi "pupil of the eye; jewel"); the eye WITH a pupil',
         'a bead word: on new texts it sits at the bead towns Chanhu-daro and Lothal more than chance', 'fresh',
         lambda: share(np.array([st in ('Chanhu-daro', 'Lothal') for x, k, st in kfaces('Mu')]), np.array([st in ('Chanhu-daro', 'Lothal') for x, k, st in kfaces('Mu') if '832' in x]), 'faces at Chanhu-daro or Lothal (Mu)')),
 '595': ('paṭṭaṟai', 'anvil, smithy, forge (3865); rival to peṭṭi',
         'a smithy word: on new texts it shares a face with the smith 391, the copper eyes or the kuṉṟi weight more than chance', 'partly seen (its copper-object share on new texts was printed)', lambda: cooccur('595', {'391', '790', '832', '850', '480'}, 'Mu')),
}
if __name__ == '__main__':
    rows = []
    for i, (s, (w, why, pred, fr, fn)) in enumerate(C.items(), 1):
        print(f'({i}/{len(C)})', end=' '); r = run('C', s, w, pred, fn); r.update(fresh=fr, dedr=why); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT3}/stage_c.csv', index=False); print('\nsummary:', df.outcome.value_counts().to_dict())
