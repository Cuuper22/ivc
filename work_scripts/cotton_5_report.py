"""Writes jobs/out/cotton_house.md from the prose below plus the reading tables in cotton_out/."""
import pandas as pd
O = '/home/antigravity/Cuuper22/ivc/work_scripts/cotton_out'
dy = pd.read_csv(f'{O}/readings_dyers.csv', dtype=str, keep_default_na=False)
ka = pd.read_csv(f'{O}/readings_karanpura.csv', dtype=str, keep_default_na=False)
def tab(df):
    s = '| object id | museum no. | findspot | type, material | text (reading order) | sounds | English |\n|---|---|---|---|---|---|---|\n'
    for r in df.itertuples():
        fs = r.findspot.replace('|', '/').strip()
        s += f'| {r.id} | {r.cisi} | {fs} | {r.type}, {r.material} | `{r.text}` | {r.sounds} | {r.english.replace("|","/")} |\n'
    return s
head = open('/home/antigravity/Cuuper22/ivc/work_scripts/cotton_report_head.md').read()
tail = open('/home/antigravity/Cuuper22/ivc/work_scripts/cotton_report_tail.md').read()
out = head + '\n## 4. Karanpura, read whole (8 faces: 5 whorls, 2 seals, 1 pot)\n\n' + tab(ka) + tail.split('@@DYERS@@')[0] + tab(dy) + tail.split('@@DYERS@@')[1]
open('/home/antigravity/Cuuper22/ivc/jobs/out/cotton_house.md', 'w').write(out)
print(len(out))
