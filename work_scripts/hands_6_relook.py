#!/usr/bin/env python3
"""HANDS step 2a: second look (2026-11-17) at the 8 twin pairs judged same/near-same hand in jobs/out/twins.md, from relook_sheet_1/2.jpg.
Judgements were typed after viewing; features per the fixed list in hands_2_pairs.py."""
import sys; sys.path.insert(0, "/home/antigravity/Cuuper22/ivc/work_scripts")
from hands_common import *
R = [('T3','H-62','M-1108','Harappa','Mohenjo-daro','text signs same forms, spacing and proportions; animal different (slender vs heavy zebu dewlap); stand hatched box alike','near'),
('T4','H-451','M-879','Harappa','Mohenjo-daro','text strokes and layout alike; both unicorn with stand hatched box on pedestal; M-879 dark','near'),
('T10','H-49','M-401','Harappa','Mohenjo-daro','text only compared (M-401 is a bar): same grid sign, same strokes and spacing','near'),
('T14','L-35','L-55','Lothal','Lothal','same four signs in same sizes and spacing; L-55 has no animal; both text cuts match','same'),
('T21','M-874','M-1305','Mohenjo-daro','Mohenjo-daro','text only (M-1305 is a bar): same three signs, same proportions','near'),
('T27','M-187','M-193','Mohenjo-daro','Mohenjo-daro','text strokes alike; animal both unicorn with face-like stand; M-187 dark','near'),
('T28','K-19','M-224','Kalibangan','Mohenjo-daro','same unicorn pose, same horn ornament, same cup stand, same five strokes; tree top differs (fuller on K-19)','near'),
('T29','K-19','M-404','Kalibangan','Mohenjo-daro','text only (M-404 is a bar): same five strokes and spacing; tree like M-224 more than K-19','near')]
D = pd.DataFrame(R, columns=['pair', 'a', 'b', 'site_a', 'site_b', 'features', 'call'])
D['cross_city'] = D.site_a != D.site_b
D.to_csv(f'{OUT}/twin_relook.csv', index=False)
print(D.call.value_counts().to_dict(), 'cross-city', int(D.cross_city.sum()))
