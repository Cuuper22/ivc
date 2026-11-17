"""Item 1. The photograph of Ashmolean 1931.120 (Umma sealing).
Route that worked: the harappa.com page opened in the laptop's in-app browser pane (the workspace shell gets a Cloudflare 403 from harappa.com).
Image files on that page: /sites/default/files/styles/large/public/umma-seal-impression.jpg (front, 969x800) and ...-back.jpg (957x800).
The pane screenshot was copied to work_data/abroad3/umma_front_screenshot.jpg (792 px wide); this script makes the enlarged crops that were read.
Prediction first: the strokes show one row of five signs in the order 127 705 002 004 390 (right to left on the sealing)."""
from PIL import Image, ImageOps
D='/home/claude/ivc/work_data/abroad3/'
im=Image.open(D+'umma_front_screenshot.jpg').convert('L')
def crop(box,k,name,eq=False):
    c=im.crop(box); c=ImageOps.equalize(c) if eq else ImageOps.autocontrast(c,cutoff=1)
    c.resize((c.width*k,c.height*k),Image.LANCZOS).save(D+name)
crop((120,225,540,410),3,'umma_inscription_x3_contrast.png')
crop((330,230,600,400),5,'umma_right_x5.png',True)
crop((100,300,360,420),5,'umma_left_x5.png')
