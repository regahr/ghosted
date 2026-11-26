# Builds the sheet images and evidence crops from the Blender renders (render_ats.py) and the three.js renders
# (shoot_ingame.mjs). Run last: python3 make_sheets.py   (from ricky/v1/make_sheets.py)
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

# ---- turnaround, stamp, slot, screens, motion
row(['turn-front', 'turn-34', 'turn-side', 'turn-back'], (90, 120, 810, 1120), 'turnaround.png', ['front', '3/4', 'side', 'back'])
a = row(['stamp-rest', 'stamp-windup', 'stamp-slam'], (60, 120, 900, 1120), '_s1.png', ['side: rest 45 deg', 'side: wind-up 140 deg', 'side: slam 0 deg'])
b = row(['stamp34-rest', 'stamp34-windup', 'stamp34-slam', 'ingame-stamp-windup'], (60, 120, 900, 1120), '_s2.png',
        ['3/4: rest 45', '3/4: wind-up 140', '3/4: slam 0', 'three.js: wind-up 140 (side)'])
W = Image.new('RGB', (max(a.width, b.width), a.height + b.height), BG); W.paste(a, (0, 0)); W.paste(b, (0, a.height)); W.save('stamp.png')
row(['slot-out', 'slot-half', 'slot-in', 'slot-stamped', 'ingame-slot'], (120, 80, 780, 900), 'slot.png',
    ['CV out on the lip (idle)', 'half in (reading, scan line)', 'in: gone into the slot', 'after the slam: NOT A FIT (sorry eyes)', 'three.js: half in'])
a = row(['screen-idle', 'screen-reading', 'screen-found', 'screen-notfit', 'screen-loading'], (100, 60, 700, 500), '_s1.png',
        ['idle', 'reading', 'found', 'not fit', 'loading'])
b = row(['scan-sweep_top', 'scan-rest', 'scan-sweep_bottom'], (100, 60, 700, 500), '_s2.png',
        ['reading: scan line at the top', 'scan line (rest)', 'scan line at the bottom'])
W = Image.new('RGB', (a.width, a.height + b.height), BG); W.paste(a, (0, 0)); W.paste(b, (0, a.height)); W.save('screens.png')
a = row(['tread-a', 'tread-b'], (0, 0, 900, 600), '_s1.png', ['treads: hubs 0, belt 0', 'hubs turned 45 deg, belt scrolled half a cleat'])
b = row(['ant-on', 'ant-off'], (0, 0, 600, 600), '_s2.png', ['antenna ball on (gold 13)', 'antenna ball off (gold x0.62)'])
W = Image.new('RGB', (a.width + b.width, max(a.height, b.height)), BG); W.paste(a, (0, 0)); W.paste(b, (a.width, 0)); W.save('treads-antenna.png')
os.remove('_s1.png'); os.remove('_s2.png')

# ---- compare-ingame.png: Blender | three.js | |difference| x4
rep = {}
for b_, g, out in (('turn-34.png', 'ingame.png', 'compare-ingame.png'), ('turn-front.png', 'ingame-front.png', 'compare-ingame-front.png')):
    A = np.asarray(Image.open(b_).convert('RGB')).astype(int); Bm = np.asarray(Image.open(g).convert('RGB')).astype(int)
    D = np.abs(A - Bm).max(axis=2)
    rep[g[:-4]] = {'mean': round(float(D.mean()), 2), 'pct_over_40': round(float((D > 40).mean() * 100), 2)}
    dimg = Image.fromarray(np.clip(255 - D * 4, 0, 255).astype(np.uint8)).convert('RGB')
    W = Image.new('RGB', (A.shape[1] * 3 + 16, A.shape[0]), 'white')
    for i, im in enumerate([Image.open(b_).convert('RGB'), Image.open(g).convert('RGB'), dimg]): W.paste(im, (i * (A.shape[1] + 8), 0))
    label(W, 'Blender EEVEE (%s)' % b_, (12, 10)); label(W, 'three.js r170 (%s)' % g, (A.shape[1] + 20, 10))
    label(W, '|difference| x4: mean %.2f/255, %.2f%% px > 40' % (rep[g[:-4]]['mean'], rep[g[:-4]]['pct_over_40']), (2 * A.shape[1] + 28, 10))
    W.save(out)
json.dump(rep, open('compare_report.json', 'w'), indent=1)

# ---- lineups: greyscale (luminance), x3 and 1x crops round Kit, Ricky and the ATS; the neck at x3 and x6
def grey(src, dst):
    p = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    Image.fromarray((s * 255).round().astype(np.uint8)).save(dst)
for g in ('grass', 'path'):
    grey('lineup-%s.png' % g, 'lineup-%s-grey.png' % g)
    e = IR['lineup-' + g]; k, a_ = e['px_kit'], e['px_ats']
    x0 = min(k['x0'], a_['x0']) - 150; x1 = max(k['x1'], a_['x1']) + 150; y0 = min(k['y0'], a_['y0']) - 70; y1 = max(k['y1'], a_['y1']) + 25
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; hw, hh = max(200, (x1 - x0) // 2), max(90, (y1 - y0) // 2); box = (cx - hw, cy - hh, cx + hw, cy + hh)
    for suf in ('', '-grey'):
        im = Image.open('lineup-%s%s.png' % (g, suf)).convert('RGB').crop(box)
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf)); im.save('lineup-%s%s-crop-1x.png' % (g, suf))
    # the neck proof (brief "open risk"): the ATS alone, x3 and x6, colour, grey and the neck mask
    ax = (a_['x0'] + a_['x1']) // 2; nb = (ax - 40, a_['y0'] - 4, ax + 40, a_['y1'] + 4)
    tiles = []
    for src, t in (('lineup-%s.png' % g, 'colour x6'), ('lineup-%s-grey.png' % g, 'grey x6'), ('_lineup-%s-neckmask.png' % g, 'mask: rings red, core green, screen blue, slot yellow')):
        tiles.append((Image.open(src).convert('RGB').crop(nb).resize(((nb[2] - nb[0]) * 6, (nb[3] - nb[1]) * 6), Image.NEAREST), t))
    W = Image.new('RGB', (sum(t.width for t, _ in tiles) + 20, tiles[0][0].height + 26), 'white')
    x = 0
    for t, lab in tiles: W.paste(t, (x, 26)); label(W, lab, (x + 6, 6)); x += t.width + 10
    W.save('crops/gamecam-neck-x6-%s.png' % g)
    Image.open('lineup-%s.png' % g).convert('RGB').crop(nb).resize(((nb[2] - nb[0]) * 3, (nb[3] - nb[1]) * 3), Image.NEAREST).save('crops/gamecam-neck-x3-%s.png' % g)
    Image.open('lineup-%s.png' % g).convert('RGB').crop(nb).save('crops/gamecam-neck-1x-%s.png' % g)

# ---- evidence crops (2x nearest) at the points projected by render_ats.py
def crop(view, key, half, out, scale=2, dy=0, dx=0):
    x, y = CP[view][key]; x += dx; y += dy; im = Image.open(view + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('turn-front', 'screen', 130, 'screen-head-front-x2')
crop('turn-front', 'neck', 90, 'neck-front-x2')
crop('turn-34', 'neck', 90, 'neck-34-x2')
crop('turn-side', 'neck', 90, 'neck-side-x2')
crop('turn-front', 'slot', 110, 'slot-lip-front-x2')
crop('turn-34', 'slot', 110, 'slot-lip-34-x2')
crop('turn-front', 'hub', 90, 'stamp-hub-front-x2', dy=60)
crop('turn-34', 'stamp_block', 90, 'stamp-block-34-x2')
crop('turn-side', 'hub', 130, 'stamp-arm-side-x2', dy=80)
crop('turn-front', 'antenna', 80, 'antenna-front-x2', dy=40)
crop('turn-front', 'tread_L', 90, 'tread-left-front-x2')
crop('turn-side', 'tread_L', 130, 'tread-side-x2', dx=-60)
crop('turn-34', 'head_corner_L', 110, 'head-corner-34-x2', dy=60)
crop('turn-back', 'screen', 130, 'head-back-vents-x2')
crop('turn-back', 'slot', 120, 'body-back-hatch-x2')
crop('stamp-windup', 'stamp_block', 110, 'stamp-windup-clearance-x2')
for nm in ('_close-neck', '_close-top'):
    Image.open(nm + '.png').convert('RGB').save('crops/' + nm.lstrip('_') + '.png')

# ---- compare-sketch.png: each sheet view next to the matching 3D view
SK = Image.open('../sketch/ats-sheet.png').convert('RGB'); s_ = SK.width / 2800.0
pairs = [('front', (28, 141, 423, 761), 'turn-front.png', (90, 120, 810, 1120)), ('3/4', (451, 141, 846, 761), 'turn-34.png', (90, 120, 810, 1120)),
         ('side', (874, 141, 1241, 761), 'turn-side.png', (90, 120, 810, 1120)), ('back', (1269, 141, 1678, 761), 'turn-back.png', (90, 120, 810, 1120)),
         ('stamp', (691, 1029, 1354, 1396), 'stamp.png', None), ('slot', (1551, 1043, 2228, 1410), 'slot.png', None),
         ('screens', (28, 1495, 1241, 1748), 'screens.png', None), ('game camera', (2200, 1861, 2538, 2249), 'crops/gamecam-neck-x3-grass.png', None)]
TW, TH = 330, 440
W = Image.new('RGB', (TW * 2 * 4 + 60, (TH + 30) * 2 + 10), 'white')
for i, (nm, box, r3, rbox) in enumerate(pairs):
    a = SK.crop(tuple(int(v * s_) for v in box)); a.thumbnail((TW, TH))
    b = Image.open(r3).convert('RGB')
    if rbox: b = b.crop(rbox)
    b.thumbnail((TW, TH))
    cx, cy = (i % 4) * (2 * TW + 15), (i // 4) * (TH + 30) + 24
    W.paste(a, (cx, cy)); W.paste(b, (cx + TW, cy)); label(W, '%s: sketch | 3D' % nm, (cx + 8, cy - 20))
W.save('compare-sketch.png')
print('sheets ok', rep)
