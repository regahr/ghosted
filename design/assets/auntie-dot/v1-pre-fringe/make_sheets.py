# Builds the sheet images and evidence crops from the Blender renders (render_dot.py) and the three.js renders
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

BOX = (120, 120, 780, 1160)
row(['turn-front', 'turn-34', 'turn-side', 'turn-back'], BOX, 'turnaround.png', ['front', '3/4', 'side', 'back'])
row(['sway-l', 'sway-0', 'sway-r', 'ingame-sway'], BOX, 'sway.png',
    ['sway -4 deg (head lags: -2)', 'sway 0', 'sway +4 deg (head +2)', 'sway +4, three.js (game engine)'])
row(['talk-front', 'talk-mid', 'talk-34', 'ingame-talk'], BOX, 'talk.png',
    ['talk: head 8 deg, hand up, mouth open', 'half-way (frac 0.5)', 'talk, 3/4', 'talk, three.js (game engine)'])
row(['card-front', 'card-mid', 'card-34', 'card-side', 'ingame-card'], (0, 120, 900, 1160), 'card.png',
    ['card: arm forward, 2 deg lean', 'half-way (frac 0.5)', 'card, 3/4', 'card, side', 'card, three.js (game engine)'])
row(['expr-rest', 'expr-talk', 'expr-happy'], (90, 0, 810, 860), 'expressions.png', ['rest: warm smile', 'talk', 'happy (the card)'])

# ---- compare-ingame: Blender | three.js | |difference| x4
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

# ---- lineups: greyscale (luminance = grey.png), x3 and 1x crops round Kit, Ricky, the Ghosties, the ATS and Dot
def lum(p):
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    return np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
def grey(src, dst):
    p = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
    Image.fromarray((lum(p) * 255).round().astype(np.uint8)).save(dst)
LBOX = {'grass': (670, 390, 970, 680), 'path': (615, 355, 1135, 560)}
SMILE = {}
for g in ('grass', 'path'):
    grey('lineup-%s.png' % g, 'lineup-%s-grey.png' % g)
    for suf in ('', '-grey'):
        im = Image.open('lineup-%s%s.png' % (g, suf)).convert('RGB').crop(LBOX[g])
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf)); im.save('lineup-%s%s-crop-1x.png' % (g, suf))
    # hair proof: Dot's face at the game camera, x6, with the hair / eye / smile mask beside it
    e = IR['lineup-' + g]; hm = e['hair']; d_ = e['px_dot']; fx = (d_['x0'] + d_['x1']) // 2; fy = int(hm['eyeTopPx'])
    fb = (fx - 24, fy - 26, fx + 24, fy + 14)
    a = Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).resize((48 * 6, 40 * 6), Image.NEAREST)
    m = Image.open('_lineup-%s-hairmask.png' % g).convert('RGB').crop(fb).resize((48 * 6, 40 * 6), Image.NEAREST)
    W = Image.new('RGB', (a.width * 2 + 10, a.height + 30), 'white'); W.paste(a, (0, 30)); W.paste(m, (a.width + 10, 30))
    dr = ImageDraw.Draw(W); hy = (hm['hairLowestInEyeColumnsPx'] - fb[1]) * 6 + 30 + 6; ey = (hm['eyeTopPx'] - fb[1]) * 6 + 30
    for yy, c in ((hy, (220, 0, 0)), (ey, (0, 0, 220))): dr.line((a.width + 10, yy, W.width, yy), fill=c, width=1)
    label(W, 'game camera, x6 (%s)' % g, (6, 6)); label(W, 'mask: hair red, eyes blue, smile green; hair low %d px, eye top %d px: gap %d px at 1x' % (
        hm['hairLowestInEyeColumnsPx'], hm['eyeTopPx'], hm['gapPx']), (a.width + 14, 6))
    W.save('crops/gamecam-face-hair-%s.png' % g)
    Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).resize((48 * 3, 40 * 3), Image.NEAREST).save('crops/gamecam-face-x3-%s.png' % g)
    Image.open('lineup-%s-grey.png' % g).convert('RGB').crop(fb).resize((48 * 3, 40 * 3), Image.NEAREST).save('crops/gamecam-face-x3-grey-%s.png' % g)
    Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).save('crops/gamecam-face-1x-%s.png' % g)
    # smile read: luminance of the smile pixels (mask green) in the colour render vs the skin round it and the eye ink
    col = np.asarray(Image.open('lineup-%s.png' % g).convert('RGB')).astype(float) / 255; L = lum(col) * 255
    mk = np.asarray(Image.open('_lineup-%s-hairmask.png' % g).convert('RGB')).astype(int)
    green = (mk[..., 1] > mk[..., 0] + 50) & (mk[..., 1] > mk[..., 2] + 50); blue = (mk[..., 2] > 150) & (mk[..., 0] < 90) & (mk[..., 1] < 90)
    white = (mk[..., 0] > 200) & (mk[..., 1] > 200) & (mk[..., 2] > 200)
    sp = hm['smilePixels']; win = np.zeros_like(white); win[sp['y0'] - 3:sp['y1'] + 4, sp['x0'] - 3:sp['x1'] + 4] = True
    skin = white & win & ~green
    SMILE[g] = {'smile_px': int(green.sum()), 'smile_box_wxh_px': [sp['x1'] - sp['x0'] + 1, sp['y1'] - sp['y0'] + 1],
                'smile_top_below_eye_bottom_px': hm['smileTopBelowEyeBottomPx'],
                'smile_luma_min': round(float(L[green].min()), 1), 'smile_luma_mean': round(float(L[green].mean()), 1),
                'skin_luma_mean_round_it': round(float(L[skin].mean()), 1), 'eye_luma_mean': round(float(L[blue].mean()), 1),
                'darkest_smile_px_vs_skin_contrast': round(float((L[skin].mean() / 255 + 0.05) / (L[green].min() / 255 + 0.05)), 2)}
json.dump(SMILE, open('smile_report.json', 'w'), indent=1)
# talk and card at the game camera, x3
for nm in ('lineup-grass-talk', 'lineup-grass-card'):
    im = Image.open(nm + '.png').convert('RGB'); d_ = IR['lineup-grass']['px_dot']
    b = (d_['x0'] - 40, d_['y0'] - 20, d_['x1'] + 40, d_['y1'] + 12); im.crop(b).resize(((b[2] - b[0]) * 3, (b[3] - b[1]) * 3), Image.NEAREST).save('crops/gamecam-%s-x3.png' % nm.split('-')[-1])

# ---- evidence crops (2x nearest) at the points projected by render_dot.py
def crop(view, key, half, out, scale=2, dy=0, dx=0):
    x, y = CP[view][key]; x += dx; y += dy; im = Image.open(view + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('turn-front', 'face', 120, 'face-front-x2', dy=-10)
crop('turn-front', 'crown', 120, 'hair-front-x2', dy=50)
crop('turn-34', 'crown', 120, 'hair-34-x2', dy=50)
crop('turn-back', 'crown', 130, 'hair-back-x2', dy=70)
crop('turn-side', 'earL', 110, 'hairline-ear-side-x2', dx=20)
crop('turn-34', 'earL', 90, 'hairline-ear-34-x2')
crop('turn-front', 'cupR', 70, 'cup-right-front-x2')
crop('turn-front', 'cupL', 70, 'cup-left-front-x2')
crop('turn-back', 'neck', 110, 'band-back-x2', dy=10)
crop('turn-side', 'neck', 110, 'band-side-x2', dy=10)
crop('turn-front', 'shoulderL', 90, 'shoulder-join-front-L-x2', dy=20)
crop('turn-front', 'shoulderR', 90, 'shoulder-join-front-R-x2', dy=20)
crop('turn-34', 'shoulderL', 90, 'shoulder-join-34-near-x2', dy=20)
crop('turn-front', 'elbowL', 70, 'elbow-front-L-x2')
crop('turn-front', 'button', 130, 'hands-front-x2', dy=50)
crop('turn-34', 'handL', 80, 'hand-34-x2')
crop('turn-side', 'handL', 90, 'arm-side-x2', dx=40, dy=-20)
crop('turn-front', 'hem', 120, 'hem-legs-front-x2', dy=70)
crop('turn-side', 'feet', 80, 'shoes-side-x2', dy=-10)
crop('talk-front', 'handR', 90, 'talk-hand-front-x2', dy=30)
crop('talk-34', 'handR', 90, 'talk-hand-34-x2', dy=30)
crop('card-front', 'handR', 100, 'card-hand-front-x2', dy=-30)
crop('card-34', 'handR', 100, 'card-hand-34-x2', dy=-30)
crop('card-side', 'handR', 110, 'card-hand-side-x2', dy=-20)
for nm in ('_close-face', '_close-headset', '_close-ear', '_close-nape', '_close-hands', '_close-top', '_close-card', '_close-talk'):
    Image.open(nm + '.png').convert('RGB').save('crops/' + nm.lstrip('_') + '.png')

# ---- compare-sketch.png: each sheet view next to the matching 3D view
SK = Image.open('../sketch/dot-sheet.png').convert('RGB'); s_ = SK.width / 2016.0
pairs = [('front', (40, 140, 305, 595), 'turn-front'), ('3/4', (320, 140, 580, 595), 'turn-34'), ('side', (600, 140, 860, 595), 'turn-side'),
         ('back', (870, 140, 1150, 595), 'turn-back'), ('sway', (10, 740, 555, 1045), 'sway.png'), ('talk', (575, 740, 985, 1045), 'talk.png'),
         ('card', (1150, 740, 1560, 1045), 'card.png'), ('expressions', (1575, 690, 2010, 870), 'expressions.png'),
         ('silhouette 64', (20, 1140, 370, 1395), 'sil'), ('game camera', (1470, 1150, 1995, 1650), 'gamecam')]
TW, TH = 330, 440
W = Image.new('RGB', (TW * 2 * 5 + 80, (TH + 30) * 2 + 10), 'white')
for i, (nm, box, r3) in enumerate(pairs):
    a = SK.crop(tuple(int(v * s_) for v in box)); a.thumbnail((TW, TH))
    if r3 == 'sil':
        s1, s2 = Image.open('silhouette-64-x4.png').convert('RGB'), Image.open('silhouette-64-34-x4.png').convert('RGB')
        b = Image.new('RGB', (s1.width + s2.width + 30, 256 + 100), 'white'); b.paste(Image.open('silhouette-64.png').convert('RGB'), (10, 10))
        b.paste(Image.open('silhouette-64-34.png').convert('RGB'), (s1.width + 20, 10)); b.paste(s1, (0, 90)); b.paste(s2, (s1.width + 20, 90))
    elif r3 == 'gamecam':
        b = Image.new('RGB', (600, 420), 'white')
        b.paste(Image.open('crops/gamecam-face-x3-grass.png').convert('RGB'), (0, 0)); b.paste(Image.open('crops/gamecam-face-x3-grey-grass.png').convert('RGB'), (150, 0))
        b.paste(Image.open('lineup-grass-crop-x3.png').convert('RGB').resize((450, 435)).crop((0, 0, 450, 280)), (0, 130))
    elif r3.endswith('.png'): b = Image.open(r3).convert('RGB')
    else: b = Image.open(r3 + '.png').convert('RGB').crop(BOX)
    b.thumbnail((TW, TH))
    cx, cy = (i % 5) * (2 * TW + 15), (i // 5) * (TH + 30) + 24
    W.paste(a, (cx, cy)); W.paste(b, (cx + TW, cy)); label(W, '%s: sketch | 3D' % nm, (cx + 8, cy - 20))
W.save('compare-sketch.png')
print('sheets ok', rep, json.dumps(SMILE))
