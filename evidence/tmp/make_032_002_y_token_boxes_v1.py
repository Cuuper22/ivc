"""Draws candidate token boxes on stored 032-002-Y signband crops.

This script carries an inline table of eight witness rows (M-722, H-444, M-49, M-21,
M-375, H-597, C-10, C-60), each with a stored source crop, its catalog text, and
hand-placed pixel boxes for the 032/002/Y tail signs. It opens each crop with PIL,
draws the colored boxes and labels plus a title bar, and saves the overlays and a
contact sheet under tmp/032_002_y_token_box_scaffold_v1. It also writes a per-box CSV
report and a summary JSON under data/open_prototype/reports. The output is a scaffold
for human token adjudication: every row is a candidate with its own status and
confidence, not an accepted token identity.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import csv, json
root = Path.cwd()
out = root/'tmp/032_002_y_token_box_scaffold_v1'
out.mkdir(parents=True, exist_ok=True)
report = root/'data/open_prototype/reports/campaign_032_002_y_token_box_scaffold_v1.csv'
rows = [
    dict(cisi='M-722', source_image='tmp/032_002_y_source_function_batch/M722_target_817_signband_closeup.png', text='+740-585-240-220-032-002-817+', y='817/P385', status='candidate_pass', confidence='medium', note='Tail group visually adjacent on one signband; 817/P385 leaf at right edge; needs independent token adjudication.', boxes=[('032/P145','red',(500,35,575,265)),('002/P122','blue',(575,35,645,265)),('817/P385','green',(640,5,775,315))]),
    dict(cisi='H-444', source_image='tmp/032_002_y_source_function_batch/H444_non240_861_signband_closeup.png', text='+241-220-032-002-861+', y='861/P385', status='candidate_pass', confidence='medium', note='Public crop gives clear same-line cluster; tail boxes follow P385/P122/P145 shape sequence in physical order.', boxes=[('861/P385','green',(25,35,185,330)),('002/P122','blue',(185,45,285,245)),('032/P145','red',(285,40,405,270))]),
    dict(cisi='M-49', source_image='tmp/032_002_y_source_function_batch/M49_target_300_fullpanel_a.png', text='+527-550-240-220-032-002-300-350-032-190+', y='300/P205', status='candidate_pass', confidence='medium', note='Target non-core branch: 032/P145, 002/P122, and 300/P205 form a visible adjacent central cluster; downstream 350-032-190 continues leftward in physical order.', boxes=[('032/P145','red',(455,110,530,310)),('002/P122','blue',(385,115,455,305)),('300/P205','green',(285,105,390,310))]),
    dict(cisi='M-21', source_image='tmp/032_002_y_source_function_batch/M21_outside_861_fullpanel_a.png', text='+350-001-740-362-692-032-002-861+', y='861/P385', status='candidate_pass', confidence='medium', note='Mayig row has local tail as P145-P122-P385; full panel shows adjacent left-side P385/P122/P145 physical cluster.', boxes=[('032/P145','red',(245,95,330,300)),('002/P122','blue',(165,95,245,280)),('861/P385','green',(55,70,165,305))]),
    dict(cisi='M-375', source_image='tmp/032_002_y_source_function_batch/M375_non240_820_signband_closeup.png', text='+740-100-233-220-032-002-820+', y='820/P378', status='candidate_pass', confidence='medium_low', note='Right-edge branch cluster is visible but Y wheel/820 is partly cut by crop edge; source panel should be recut wider before final acceptance.', boxes=[('032/P145','red',(535,105,615,335)),('002/P122','blue',(615,90,705,310)),('820/P378','green',(705,70,838,330))]),
    dict(cisi='H-597', source_image='tmp/032_002_y_source_function_batch/H597_outside_861_signband_closeup.png', text='+740-390-590-070-032-002-861+', y='861/P385', status='candidate_pass', confidence='medium_low', note='Dark-background signband shows adjacent right-side tail cluster; P122/P145 separation needs stronger crop before final acceptance.', boxes=[('032/P145','red',(515,185,605,430)),('002/P122','blue',(605,185,690,420)),('861/P385','green',(690,165,812,450))]),
    dict(cisi='C-10', source_image='tmp/chanhudaro_mackay_1943/crops_final/C10_non240_817_plateLI_no29_signband.png', text='+740-231-220-032-002-817+', y='817/P385', status='candidate_pass_lowres', confidence='low', note='Mackay plate is low contrast but the final adjacent cluster is boxable; use as source-realness pressure, not final token identity.', boxes=[('032/P145','red',(330,20,410,240)),('002/P122','blue',(410,20,490,230)),('817/P385','green',(490,0,645,260))]),
    dict(cisi='C-60', source_image='tmp/chanhudaro_mackay_1943/crops_final/C60_outside_861_plateLII_no24_signband.png', text='+740-176-032-002-861+', y='861/P385', status='candidate_weak', confidence='low', note='Same-line signband is present, but the public crop is too degraded for confident token identity. Count row-level source visibility, not token-level acceptance.', boxes=[('032/P145','red',(210,5,285,145)),('002/P122','blue',(285,5,355,145)),('861/P385','green',(355,0,470,150))]),
]
colors = {'red': (255, 30, 30), 'blue': (30, 90, 255), 'green': (30, 180, 80)}
try:
    font = ImageFont.truetype('arial.ttf', 18)
    small = ImageFont.truetype('arial.ttf', 14)
except Exception:
    font = ImageFont.load_default(); small = font
manifest=[]
thumbs=[]
for r in rows:
    src = root/r['source_image']
    im = Image.open(src).convert('RGB')
    draw = ImageDraw.Draw(im)
    for label, color_name, box in r['boxes']:
        color = colors[color_name]
        draw.rectangle(box, outline=color, width=4)
        x1,y1,x2,y2 = box
        draw.text((x1+3, max(0,y1-22)), label, fill=color, font=small)
    title = f"{r['cisi']} {r['text']} status={r['status']}"
    pad = 36
    canvas = Image.new('RGB', (im.width, im.height + pad), 'white')
    canvas.paste(im, (0,pad))
    ImageDraw.Draw(canvas).text((6,8), title, fill=(0,0,0), font=small)
    out_path = out / f"{r['cisi'].replace('-','')}_token_boxes.png"
    canvas.save(out_path)
    rflat = {k:v for k,v in r.items() if k!='boxes'}
    rflat['source_image_abs'] = str(src.resolve())
    rflat['overlay_image'] = str(out_path.resolve())
    for label, color_name, box in r['boxes']:
        manifest.append({**rflat, 'token_label': label, 'box_color': color_name, 'x1':box[0], 'y1':box[1], 'x2':box[2], 'y2':box[3]})
    thumb = canvas.copy(); thumb.thumbnail((900,360)); thumbs.append((r['cisi'], thumb))
with report.open('w', newline='', encoding='utf-8') as f:
    fields = ['cisi','text','y','status','confidence','note','source_image','source_image_abs','overlay_image','token_label','box_color','x1','y1','x2','y2']
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(manifest)
w = 940
h = sum(t.height+30 for _,t in thumbs)+20
sheet = Image.new('RGB', (w,h), 'white')
d = ImageDraw.Draw(sheet)
y=10
for cisi, thumb in thumbs:
    d.text((10,y), cisi, fill=(0,0,0), font=font)
    y += 24
    sheet.paste(thumb, (20,y)); y += thumb.height + 26
sheet_path = out/'token_box_scaffold_contact_sheet.png'
sheet.save(sheet_path)
summary = {
    'rows': len(rows),
    'tokens': len(manifest),
    'report': str(report.resolve()),
    'contact_sheet': str(sheet_path.resolve()),
    'status_counts': {s: sum(1 for r in rows if r['status']==s) for s in sorted(set(r['status'] for r in rows))}
}
(root/'data/open_prototype/reports/campaign_032_002_y_token_box_scaffold_v1_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
