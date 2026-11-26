# Builds the sheet images and evidence crops from the Blender renders (render_ricky.py) and the three.js renders
# (shoot_ingame.mjs). Run last: python3 make_sheets.py   (from ghostie/v7/make_sheets.py)
import json, os
import numpy as np
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
INK = (43, 30, 22); BG = (0xFD, 0xE6, 0xC8)
CP = json.load(open('crop_points.json')); IR = json.load(open('ingame_report.json'))
os.makedirs('crops', exist_ok=True)

def label(im, text, xy=(8, 6)):
    d = ImageDraw.Draw(im); d.rectangle((xy[0] - 4, xy[1] - 2, xy[0] + 6 * len(text) + 4, xy[1] + 13), fill=(255, 248, 238)); d.text(xy, text, fill=INK); return im
def row(names, box, out, labels=None, bg=BG):
    tiles = [Image.open(n + '.png').convert('RGB').crop(box) for n in names]
    W = Image.new('RGB', (sum(t.width for t in tiles), tiles[0].height), bg)
    for i, t in enumerate(tiles): W.paste(t, (i * t.width, 0)); label(W, (labels or names)[i], (i * t.width + 10, 8))
    W.save(out); return W

# ---- turnaround, phone, hop
row(['turn-front', 'turn-34', 'turn-side', 'turn-back'], (90, 20, 810, 1160), 'turnaround.png', ['front', '3/4', 'side', 'back'])
row(['phone-front', 'phone-34', 'phone-mid-front', 'ingame-phone'], (90, 20, 810, 1160), 'phone.png',
    ['phone, front (Blender)', 'phone, 3/4', 'half-way (frac 0.5)', 'phone, three.js (game engine)'])
row(['hop-rest', 'hop-squash', 'hop-air', 'hop-land'], (90, 20, 810, 1160), 'hop.png',
    ['rest', 'take-off: squash (bounce only)', 'air: stretch, arms out, +0.16 m', 'land: squash (bounce only)'])

# ---- drain strip (three.js): labels over each step
dr = Image.open('_drain-raw.png').convert('RGB'); labs = IR['drain']['labels']
names = ['Ricky (suit row 17)', 'step 1: row 11, legs fade, "o", lifts', 'step 2: row 27, white-ish, no legs', 'step 3: row 16, smaller, floats', 'swap: the locked headset Ghostie']
for (x, y), t in zip(labs, names): label(dr, t, (max(4, x - 3 * len(t)), 40))
dr.save('drain-strip.png')

# ---- compare-ingame.png: Blender | three.js | |difference| x4
rep = {}
for b, g, out in (('turn-34.png', 'ingame.png', 'compare-ingame.png'), ('turn-front.png', 'ingame-front.png', 'compare-ingame-front.png')):
    A = np.asarray(Image.open(b).convert('RGB')).astype(int); Bm = np.asarray(Image.open(g).convert('RGB')).astype(int)
    D = np.abs(A - Bm).max(axis=2)
    rep[g[:-4]] = {'mean': round(float(D.mean()), 2), 'pct_over_40': round(float((D > 40).mean() * 100), 2)}
    dimg = Image.fromarray(np.clip(255 - D * 4, 0, 255).astype(np.uint8)).convert('RGB')
    W = Image.new('RGB', (A.shape[1] * 3 + 16, A.shape[0]), 'white')
    for i, im in enumerate([Image.open(b).convert('RGB'), Image.open(g).convert('RGB'), dimg]): W.paste(im, (i * (A.shape[1] + 8), 0))
    label(W, 'Blender EEVEE (%s)' % b, (12, 10)); label(W, 'three.js r170 (%s)' % g, (A.shape[1] + 20, 10))
    label(W, '|difference| x4: mean %.2f/255, %.2f%% px > 40' % (rep[g[:-4]]['mean'], rep[g[:-4]]['pct_over_40']), (2 * A.shape[1] + 28, 10))
    W.save(out)
json.dump(rep, open('compare_report.json', 'w'), indent=1)

# ---- lineups: greyscale (luminance, = grey.png), x3 and 1x crops round Kit, the Ghosties and Ricky
def grey(src, dst):
    p = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    Image.fromarray((s * 255).round().astype(np.uint8)).save(dst)
for g in ('grass', 'path'):
    grey('lineup-%s.png' % g, 'lineup-%s-grey.png' % g)
    k, r = IR['lineup-' + g]['px_kit'], IR['lineup-' + g]['px_ricky']
    x0 = min(k['x0'], r['x0']) - 210; x1 = max(k['x1'], r['x1']) + 40; y0 = min(k['y0'], r['y0']) - 40; y1 = max(k['y1'], r['y1']) + 25
    hh = max(75, (y1 - y0) // 2 + 4); ww = max(170, int(hh * 340 / 150)); cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; box = (cx - ww, cy - hh, cx + ww, cy + hh)
    for suf in ('', '-grey'):
        im = Image.open('lineup-%s%s.png' % (g, suf)).convert('RGB').crop(box)
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf)); im.save('lineup-%s%s-crop-1x.png' % (g, suf))
    # hair proof: Ricky's face at the game camera, x3 (and the hair/eye mask beside it)
    e = IR['lineup-' + g]; fx = (r['x0'] + r['x1']) // 2; fy = int(e['rickyEyeTopY'])
    fb = (fx - 30, fy - 30, fx + 30, fy + 18)
    a = Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).resize((180 * 2, 144 * 2), Image.NEAREST)
    m = Image.open('_lineup-%s-hairmask.png' % g).convert('RGB').crop(fb).resize((180 * 2, 144 * 2), Image.NEAREST)
    W = Image.new('RGB', (a.width * 2 + 10, a.height + 30), 'white'); W.paste(a, (0, 30)); W.paste(m, (a.width + 10, 30))
    d = ImageDraw.Draw(W); hy = (e['hair']['hairLowestInEyeColumnsPx'] - fb[1]) * 6 + 30; ey = (e['hair']['eyeTopPx'] - fb[1]) * 6 + 30
    for yy, c in ((hy, (220, 0, 0)), (ey, (0, 0, 220))): d.line((a.width + 10, yy, W.width, yy), fill=c, width=1)
    label(W, 'game camera, x6 (%s)' % g, (6, 6)); label(W, 'mask: hair red, eyes blue; lines: hair low %d px, eye top %d px (gap %d px at 1x)' % (
        e['hair']['hairLowestInEyeColumnsPx'], e['hair']['eyeTopPx'], e['hair']['gapPx']), (a.width + 14, 6))
    W.save('crops/gamecam-face-hair-%s.png' % g)
    # the x3 crop the chair asked for
    Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).resize((180, 144), Image.NEAREST).resize((180, 144)).save('crops/_tmp.png')
    Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).resize((60 * 3, 48 * 3), Image.NEAREST).save('crops/gamecam-face-x3-%s.png' % g)
os.remove('crops/_tmp.png')
Image.open('lineup-grass-phone.png').convert('RGB').crop(tuple(np.array([-170, -75, 170, 75]) + np.array([(IR['lineup-grass']['px_ricky']['x0'] + IR['lineup-grass']['px_ricky']['x1']) // 2, (IR['lineup-grass']['px_ricky']['y0'] + IR['lineup-grass']['px_ricky']['y1']) // 2] * 2))).resize((1020, 450), Image.NEAREST).save('crops/gamecam-phone-x3.png')

# ---- evidence crops (2x nearest) at the points projected by render_ricky.py
def crop(view, key, half, out, scale=2, dy=0, dx=0):
    x, y = CP[view][key]; x += dx; y += dy; im = Image.open(view + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('turn-front', 'face', 120, 'face-front-x2', dy=-25)
crop('turn-front', 'collar', 80, 'collar-knot-front-x2', dy=12)
crop('turn-front', 'tie', 110, 'tie-shirt-v-front-x2', dy=20)
crop('turn-front', 'shoulderL', 90, 'shoulder-join-front-L-x2', dy=40)
crop('turn-front', 'shoulderR', 90, 'shoulder-join-front-R-x2', dy=40)
crop('turn-34', 'shoulderL', 90, 'shoulder-join-34-near-x2', dy=40)
crop('turn-34', 'handL', 60, 'hand-cuff-34-x2')
crop('turn-side', 'shoulderL', 110, 'arm-side-x2', dy=60)
crop('turn-side', 'crown', 110, 'band-side-x2', dy=50)
crop('turn-back', 'crown', 120, 'hair-back-x2', dy=70)
crop('turn-front', 'crown', 120, 'hair-front-x2', dy=70)
crop('turn-34', 'crown', 120, 'hair-34-x2', dy=70)
crop('turn-front', 'cupR', 60, 'cup-mic-right-front-x2', dy=15)
crop('turn-front', 'cupL', 60, 'cup-left-front-x2')
crop('phone-front', 'elbowR', 110, 'phone-elbow-front-x2', dy=-40)
crop('phone-front', 'handR', 80, 'phone-hand-cup-front-x2')
crop('phone-34', 'handR', 80, 'phone-hand-cup-34-x2')
crop('turn-front', 'hem', 120, 'hem-legs-front-x2', dy=70)
crop('turn-side', 'feet', 80, 'shoes-side-x2', dy=-10)
for nm in ('_close-face', '_close-headset', '_close-tie', '_close-shoulder', '_close-top'):
    Image.open(nm + '.png').convert('RGB').save('crops/' + nm.lstrip('_') + '.png')

# ---- compare-sketch.png: each sheet view next to the matching 3D view (S1)
SK = Image.open('../sketch/ricky-sheet.png').convert('RGB'); s_ = SK.width / 2016.0
pairs = [('front', (40, 140, 320, 610), 'turn-front'), ('3/4', (345, 140, 615, 610), 'turn-34'), ('side', (640, 140, 880, 610), 'turn-side'),
         ('back', (905, 140, 1185, 610), 'turn-back'), ('phone', (950, 800, 1180, 1110), 'phone-front'), ('hop (air)', (1690, 800, 1820, 1110), 'hop-air'),
         ('drain', (20, 790, 860, 1110), None), ('game camera', (1600, 1195, 1780, 1415), None)]
TW, TH = 330, 440
W = Image.new('RGB', (TW * 2 * 4 + 60, (TH + 30) * 2 + 10), 'white')
for i, (nm, box, r3) in enumerate(pairs):
    a = SK.crop(tuple(int(v * s_) for v in box)); a.thumbnail((TW, TH))
    if r3: b = Image.open(r3 + '.png').convert('RGB').crop((120, 20, 780, 1160))
    elif nm == 'drain': b = Image.open('drain-strip.png').convert('RGB')
    else: b = Image.open('crops/gamecam-face-hair-grass.png').convert('RGB').crop((0, 30, 360, 318))
    b.thumbnail((TW, TH))
    cx, cy = (i % 4) * (2 * TW + 15), (i // 4) * (TH + 30) + 24
    W.paste(a, (cx, cy)); W.paste(b, (cx + TW, cy)); label(W, '%s: sketch | 3D' % nm, (cx + 8, cy - 20))
W.save('compare-sketch.png')
print('sheets ok', rep)
