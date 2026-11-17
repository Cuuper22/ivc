"""OCR Lorimer's Werchikwar-English Vocabulary (1962, Yasin Burushaski), 204 scan pages, from the Internet Archive PDF.
The scan is a landscape sheet stored sideways: render at 300 dpi, rotate 90 degrees, tesseract page-segmentation 1 (finds the columns).
usage: python3 rival_ocr_werchikwar.py PDF OUTDIR   (prints progress; writes OUTDIR/pNNN.txt and OUTDIR/all.txt)"""
import sys, os, subprocess, glob
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
pdf, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
N = int(subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout.split("Pages:")[1].split()[0])
def page(p):
    f = f"{out}/p{p:03d}.txt"
    if os.path.exists(f) and os.path.getsize(f) > 0: return p
    png = f"{out}/tmp{p:03d}"
    subprocess.run(["pdftoppm", "-r", "300", "-f", str(p), "-l", str(p), "-gray", "-png", pdf, png], check=True)
    img = glob.glob(png + "*.png")[0]
    Image.open(img).rotate(-90, expand=True).save(img)
    t = subprocess.run(["tesseract", img, "-", "--psm", "1"], capture_output=True, text=True).stdout
    open(f, "w").write(t); os.remove(img)
    return p
done = 0
with ThreadPoolExecutor(2) as ex:
    for p in ex.map(page, range(1, N + 1)):
        done += 1
        if done % 10 == 0: print(f"OCR {done}/{N} pages", flush=True)
with open(f"{out}/all.txt", "w") as o:
    for p in range(1, N + 1): o.write(open(f"{out}/p{p:03d}.txt").read() + "\n")
print("done", N)
