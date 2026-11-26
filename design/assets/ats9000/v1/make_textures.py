# GHOSTED - ATS-9000 v1 textures (run with the system python3 before build_ats.py): python3 make_textures.py
# Palette rows only (seats/lena-park.md, sketch/src/ats.py ROW). Shapes from sketch/src/ats.py screen_marks().
#   tex/screen.png  5 cells stacked top -> bottom: idle, reading, found, notfit, loading (512 x 256 each).
#                   The cell maps the screen rect x 80-220, y 74-136 (sketch units); alpha 0 outside the rounded screen.
#   tex/scan.png    the scan line (cream 7.5 u, x 88-212; was 3 u, which broke into dashes at 1x) on alpha 0; repeats in V, the game scrolls it.
#   tex/hub.png     a hub disc: grey 18, ink rim, ink spoke; alpha 0 outside the disc. Every disc maps the full square,
#                   so one UV rotation about the centre turns all six.
#   tex/belt.png    ink with one cleat line (grey 18 x 0.85, the neutral shade) per tile; repeats along the belt loop.
#   tex/cv.png      the CV prop: 2 cells (left: plain CV, right: stamped with the red-ink text NOT A FIT).
import os, sys
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sketch', 'src'))
import ats as A
OUT = os.path.join(H, 'tex'); os.makedirs(OUT, exist_ok=True)
SS = 4
def rgb(h, a=255): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)
INK, CREAM, GOLD, GREY, PAPER, RED = (rgb(A.ROW[k]) for k in (22, 12, 13, 18, 23, 21))
SHADE_GREY = tuple(round(c * 0.85) for c in GREY[:3]) + (255,)
STATES = ['idle', 'reading', 'found', 'notfit', 'loading']
SX0, SX1, SY0, SY1 = 80.0, 220.0, 74.0, 136.0       # screen rect (sketch units)
CW, CH = 512, 256

def cell(state):
    W, Hh = CW * SS, CH * SS; im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fx = lambda x: (x - SX0) / (SX1 - SX0) * W; fy = lambda y: (y - SY0) / (SY1 - SY0) * Hh
    # rounded screen (SCREEN path: corner radius 12 u)
    d.rounded_rectangle((0, 0, W - 1, Hh - 1), radius=int(12 / (SX1 - SX0) * W), fill=INK)
    e = A.LM['eye']
    def pill(cx, cy, w, h):
        r = min(fx(cx + w / 2) - fx(cx - w / 2), fy(cy + h / 2) - fy(cy - h / 2)) / 2
        d.rounded_rectangle((fx(cx - w / 2), fy(cy - h / 2), fx(cx + w / 2), fy(cy + h / 2)), radius=r, fill=CREAM)
    def poly(pts): d.polygon([(fx(x), fy(y)) for x, y in pts], fill=CREAM)
    def bez(p0, p1, p2, p3, n=40):
        return [tuple((1 - t) ** 3 * a + 3 * t * (1 - t) ** 2 * b + 3 * t * t * (1 - t) * c + t ** 3 * dd for a, b, c, dd in zip(p0, p1, p2, p3))
                for t in [i / n for i in range(n + 1)]]
    if state == 'idle':
        for x in A.EYE_X: pill(x, e, 20, 30)
    elif state == 'reading':
        for x in A.EYE_X: pill(x, e + 2, 24, 8)
    elif state == 'found':          # happy arcs (stroke 6 u)
        for x in A.EYE_X:
            pts = bez((x - 13, e + 7), (x - 9, e - 12), (x + 9, e - 12), (x + 13, e + 7))
            for (cx, cy) in bez((x - 13, e + 7), (x - 9, e - 12), (x + 9, e - 12), (x + 13, e + 7), 400):   # a round 6 u brush
                rx, ry = fx(cx + 3) - fx(cx), fy(cy + 3) - fy(cy); d.ellipse((fx(cx) - rx, fy(cy) - ry, fx(cx) + rx, fy(cy) + ry), fill=CREAM)
    elif state == 'notfit':         # low, soft half-moons (sorry, never angry)
        for x in A.EYE_X: poly([(x - 12, e + 1)] + bez((x - 12, e + 1), (x - 12, e + 16), (x + 12, e + 16), (x + 12, e + 1)))
    elif state == 'loading':
        for x in (128, 150, 172): d.ellipse((fx(x - 6), fy(e - 6), fx(x + 6), fy(e + 6)), fill=CREAM)
    return im.resize((CW, CH), Image.LANCZOS)

atlas = Image.new('RGBA', (CW, CH * 5), (0, 0, 0, 0))
for i, s in enumerate(STATES): atlas.paste(cell(s), (0, i * CH))
atlas.save(os.path.join(OUT, 'screen.png'))

# scan line: one tile = the screen height (62 u); the line 7.5 u tall (about 2 px at the game camera), x 88-212; rest y 126
SCAN_H = 7.5
W, Hh = CW * SS, CH * SS; im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
fx = lambda x: (x - SX0) / (SX1 - SX0) * W; fy = lambda y: (y - SY0) / (SY1 - SY0) * Hh
y = A.LM['scan_rest']; d.rounded_rectangle((fx(88), fy(y - SCAN_H / 2), fx(212), fy(y + SCAN_H / 2)), radius=fy(y + SCAN_H / 2) - fy(y), fill=CREAM)
im.resize((CW, CH), Image.LANCZOS).save(os.path.join(OUT, 'scan.png'))

# hub disc (sketch: oval r 10, grey 18, ink stroke 1.6, spoke 7 u each side, ink 2.0)
S = 128 * SS; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = S / 20.0
d.ellipse((0, 0, S - 1, S - 1), fill=INK); d.ellipse((1.8 * k, 1.8 * k, S - 1.8 * k, S - 1.8 * k), fill=GREY)
d.line((3 * k, S / 2, S - 3 * k, S / 2), fill=INK, width=int(2.2 * k))
im.resize((128, 128), Image.LANCZOS).save(os.path.join(OUT, 'hub.png'))

# belt: 64 x 16 tile, one cleat (6 px of 64) across; U runs along the loop
im = Image.new('RGBA', (64, 16), INK); d = ImageDraw.Draw(im); d.rectangle((29, 0, 34, 15), fill=SHADE_GREY)
im.save(os.path.join(OUT, 'belt.png'))

# CV prop: 2 cells side by side (256 x 320 each, portrait paper 64 x 80 u); text lines in ink; cell 2 adds the stamp
def cv(stamped):
    W, Hh = 256 * SS, 320 * SS; im = Image.new('RGBA', (W, Hh), PAPER); d = ImageDraw.Draw(im); u = W / 64.0
    d.rectangle((6 * u, 7 * u, 30 * u, 11 * u), fill=INK)                       # name line
    for k, (x1) in enumerate([58, 52, 56, 46, 54, 50, 40]):
        yy = (18 + 7.5 * k) * u; d.rectangle((6 * u, yy, x1 * u, yy + 2.2 * u), fill=INK)
    if stamped:
        f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Black.ttf', int(7.0 * u))
        t = 'NOT A FIT'; bb = d.textbbox((0, 0), t, font=f); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        box = Image.new('RGBA', (int(tw + 8 * u), int(th + 8 * u)), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
        bd.rectangle((0, 0, box.width - 1, box.height - 1), outline=RED, width=int(1.6 * u))
        bd.text((4 * u - bb[0], 4 * u - bb[1]), t, font=f, fill=RED)
        box = box.rotate(8, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(box, (int((W - box.width) / 2), int(44 * u)))
    return im.resize((256, 320), Image.LANCZOS)
im = Image.new('RGBA', (512, 320)); im.paste(cv(False), (0, 0)); im.paste(cv(True), (256, 0)); im.save(os.path.join(OUT, 'cv.png'))
print('textures ok', os.listdir(OUT))
