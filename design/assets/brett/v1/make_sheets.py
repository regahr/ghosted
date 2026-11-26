# Builds the sheet images and evidence crops from the Blender renders (render_brett.py) and the three.js renders
# (shoot_ingame.mjs). Run last: python3 make_sheets.py   (from auntie-dot/v1/make_sheets.py)
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

BOX = (100, 40, 800, 1160)
row(['turn-front', 'turn-34', 'turn-side', 'turn-back'], BOX, 'turnaround.png', ['front', '3/4', 'side', 'back'])
row(['idle-rest', 'idle-settle', 'idle-puff', 'idle-side', 'ingame-idle'], BOX, 'idle.png',
    ['idle: hands on hips, chin up 10', 'settle (puff 0.5)', 'puff: lean back 3, rise 3 u', 'puff, side', 'puff, three.js (game engine)'])
row(['like-front', 'like-mid', 'like-34', 'like-side', 'ingame-like'], BOX, 'like.png',
    ['the Like: fist out, thumb up, wink', 'half-way (frac 0.5)', 'like, 3/4', 'like, side', 'like, three.js (game engine)'])
row(['bullets-1', 'bullets-2', 'bullets-3', 'bullets-34', 'ingame-bullets'], BOX, 'bullets.png',
    ['- bullet 1 (mouth open)', '- bullet 2', '- bullet 3', 'bullets, 3/4', 'bullets, three.js (game engine)'])
row(['expr-rest', 'expr-talk', 'expr-wink', 'expr-lost'], (90, 0, 810, 860), 'expressions.png', ['rest: the grin', 'talk', 'wink (the Like)', 'secretly lost'])

# ---- compare-ingame: Blender | three.js | |difference| x4 (same pose: neutral, no carriage)
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

# ---- lineups: greyscale (luminance = grey.png), x3 and 1x crops round Kit, Ricky, Dot, the Ghosties, the ATS and Brett
def lum(p):
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    return np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
def grey(src, dst):
    p = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
    Image.fromarray((lum(p) * 255).round().astype(np.uint8)).save(dst)
LBOX = {'grass': (670, 390, 970, 715), 'path': (525, 325, 1135, 560)}
GRIN = {}
for g in ('grass', 'path'):
    grey('lineup-%s.png' % g, 'lineup-%s-grey.png' % g)
    for suf in ('', '-grey'):
        im = Image.open('lineup-%s%s.png' % (g, suf)).convert('RGB').crop(LBOX[g])
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf)); im.save('lineup-%s%s-crop-1x.png' % (g, suf))
    e = IR['lineup-' + g]; hm = e['hair']; d_ = e['px_brett_with_halo']; fx = (d_['x0'] + d_['x1']) // 2; fy = int(hm['eyeTopPx'])
    fb = (fx - 24, fy - 30, fx + 24, fy + 14)
    a = Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).resize((48 * 6, 44 * 6), Image.NEAREST)
    m = Image.open('_lineup-%s-hairmask.png' % g).convert('RGB').crop(fb).resize((48 * 6, 44 * 6), Image.NEAREST)
    W = Image.new('RGB', (a.width * 2 + 10, a.height + 46), 'white'); W.paste(a, (0, 46)); W.paste(m, (a.width + 10, 46))
    dr = ImageDraw.Draw(W); hy = (hm['hairLowestInEyeColumnsPx'] - fb[1]) * 6 + 46 + 6; ey = (hm['eyeTopPx'] - fb[1]) * 6 + 46
    for yy, c in ((hy, (220, 0, 0)), (ey, (0, 0, 220))): dr.line((a.width + 10, yy, W.width, yy), fill=c, width=1)
    fh = hm['forehead']
    label(W, 'game camera, x6 (%s)' % g, (6, 6))
    label(W, 'mask: hair + hairline ink red, brows orange, eyes blue, grin line green, teeth cyan, halo yellow', (a.width + 14, 6))
    label(W, 'hair low %d, eye top %d: gap %d px; forehead band %s-%s px (min-max over %d brow columns)' % (
        hm['hairLowestInEyeColumnsPx'], hm['eyeTopPx'], hm['gapPx'], fh['minPx'], fh['maxPx'], fh['columns']), (a.width + 14, 24))
    W.save('crops/gamecam-face-hair-%s.png' % g)
    for suf, tag in (('', ''), ('-grey', '-grey')):
        Image.open('lineup-%s%s.png' % (g, suf)).convert('RGB').crop(fb).resize((48 * 3, 44 * 3), Image.NEAREST).save('crops/gamecam-face-x3%s-%s.png' % (tag, g))
    Image.open('lineup-%s.png' % g).convert('RGB').crop(fb).save('crops/gamecam-face-1x-%s.png' % g)
    # the grin read at 1x: teeth (cyan in the mask) must be light, the smile line (green) dark and BELOW the teeth
    col = np.asarray(Image.open('lineup-%s.png' % g).convert('RGB')).astype(float) / 255; L = lum(col) * 255
    mk = np.asarray(Image.open('_lineup-%s-hairmask.png' % g).convert('RGB')).astype(int)
    green = (mk[..., 1] > 150) & (mk[..., 0] < 90) & (mk[..., 2] < 90); cyan = (mk[..., 1] > 150) & (mk[..., 2] > 150) & (mk[..., 0] < 90)
    blue = (mk[..., 2] > 150) & (mk[..., 0] < 90) & (mk[..., 1] < 90); white = (mk > 200).all(axis=2)
    sp = hm['teethPixels']; win = np.zeros_like(white); win[sp['y0'] - 3:sp['y1'] + 4, sp['x0'] - 3:sp['x1'] + 4] = True
    skin = white & win
    ys_t, ys_g = np.where(cyan)[0], np.where(green)[0]
    GRIN[g] = {'teeth_px': int(cyan.sum()), 'line_px': int(green.sum()),
               'grin_box_wxh_px': [max(sp['x1'], hm['grinLinePixels']['x1']) - min(sp['x0'], hm['grinLinePixels']['x0']) + 1,
                                   max(sp['y1'], hm['grinLinePixels']['y1']) - min(sp['y0'], hm['grinLinePixels']['y0']) + 1],
               'teeth_luma_mean': round(float(L[cyan].mean()), 1), 'line_luma_mean': round(float(L[green].mean()), 1) if green.any() else None,
               'skin_luma_mean_round_it': round(float(L[skin].mean()), 1), 'eye_luma_mean': round(float(L[blue].mean()), 1),
               'teeth_centre_y': round(float(ys_t.mean()), 2), 'line_centre_y': round(float(ys_g.mean()), 2) if green.any() else None,
               'grin_top_below_eye_bottom_px': hm['grinTopBelowEyeBottomPx']}
    # side hair vs the eyes (Rega ts 1795658703.410809): the lowest hair or hair-edge-ink pixel OUTSIDE the eye columns,
    # on the head (from the hair top down to the grin), against the eye top. Positive = the hair is above the eye top.
    red = (mk[..., 0] > 150) & (mk[..., 1] < 90) & (mk[..., 2] < 90)
    ep = hm['eyePixels']; ys, xs = np.where(red)
    head = (ys < hm['teethPixels']['y0']) & (xs > ep['x0'] - 22) & (xs < ep['x1'] + 22)
    side = head & ((xs < ep['x0'] - 2) | (xs > ep['x1'] + 2))
    lo = int(ys[side].max()) if side.any() else None
    GRIN[g]['side_hair_lowest_px'] = lo; GRIN[g]['eye_top_px'] = hm['eyeTopPx']; GRIN[g]['eye_bottom_px'] = ep['y1']
    GRIN[g]['side_hair_above_eye_top_px'] = (hm['eyeTopPx'] - lo) if lo is not None else None
    GRIN[g]['side_hair_lowest_x_px'] = int(xs[side][ys[side].argmax()]) if side.any() else None
    GRIN[g]['eye_columns_px'] = [ep['x0'], ep['x1']]
json.dump(GRIN, open('grin_report.json', 'w'), indent=1)
# the beats at the game camera, x3 (grass), and the no-carriage test
d_ = IR['lineup-grass']['px_brett_with_halo']
for nm in ('lineup-grass-idle', 'lineup-grass-like', 'lineup-grass-bullets', 'lineup-grass-nocarry', 'lineup-grass'):
    im = Image.open(nm + '.png').convert('RGB'); b = (d_['x0'] - 30, d_['y0'] - 10, d_['x1'] + 30, d_['y1'] + 10)
    im.crop(b).resize(((b[2] - b[0]) * 3, (b[3] - b[1]) * 3), Image.NEAREST).save('crops/gamecam-%s-x3.png' % nm.replace('lineup-grass', 'rest').replace('rest-', ''))
tiles = [Image.open('crops/gamecam-%s-x3.png' % k).convert('RGB') for k in ('rest', 'idle', 'like', 'bullets', 'nocarry')]
W = Image.new('RGB', (sum(t.width for t in tiles) + 40, tiles[0].height + 24), 'white')
for i, t in enumerate(tiles):
    W.paste(t, (i * (t.width + 10), 24)); label(W, ['rest (chin up)', 'idle (hands on hips)', 'the Like', 'bullets', 'test: no chin-up'][i], (i * (t.width + 10) + 4, 4))
W.save('gamecam-beats-x3.png')
# path beats too (Rega's mouth review: rest, the Like and bullets at the game camera on grass AND path)
d_ = IR['lineup-path']['px_brett_with_halo']; b = (d_['x0'] - 30, d_['y0'] - 10, d_['x1'] + 30, d_['y1'] + 10)
for nm, out in (('lineup-path', 'rest'), ('lineup-path-like', 'like'), ('lineup-path-bullets', 'bullets'), ('lineup-path-idle', 'idle')):
    Image.open(nm + '.png').convert('RGB').crop(b).resize(((b[2] - b[0]) * 3, (b[3] - b[1]) * 3), Image.NEAREST).save('crops/gamecam-path-%s-x3.png' % out)
tiles = [Image.open('crops/gamecam-%s-x3.png' % k).convert('RGB') for k in ('rest', 'like', 'bullets')] + \
        [Image.open('crops/gamecam-path-%s-x3.png' % k).convert('RGB') for k in ('rest', 'like', 'bullets')]
W = Image.new('RGB', (sum(t.width for t in tiles[:3]) + 20, max(t.height for t in tiles[:3]) + max(t.height for t in tiles[3:]) + 48), 'white')
x = 0
for i, t in enumerate(tiles[:3]): W.paste(t, (x, 20)); label(W, ['grass: rest grin', 'grass: the Like', 'grass: bullets'][i], (x + 4, 2)); x += t.width + 10
x = 0; y2 = max(t.height for t in tiles[:3]) + 44
for i, t in enumerate(tiles[3:]): W.paste(t, (x, y2)); label(W, ['path: rest grin', 'path: the Like', 'path: bullets'][i], (x + 4, y2 - 18)); x += t.width + 10
W.save('gamecam-mouths-x3.png')

# ---- evidence crops (2x nearest) at the points projected by render_brett.py
def crop(view, key, half, out, scale=2, dy=0, dx=0):
    x, y = CP[view][key]; x += dx; y += dy; im = Image.open(view + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('turn-front', 'face', 120, 'face-front-x2')
crop('turn-front', 'crown', 120, 'hair-front-x2', dy=10)
crop('turn-34', 'crown', 120, 'hair-34-x2', dy=10)
crop('turn-34b', 'crown', 120, 'hair-34b-x2', dy=10)
crop('turn-back', 'crown', 130, 'hair-back-x2', dy=40)
crop('turn-side', 'face', 110, 'face-side-x2', dx=20)
crop('turn-side', 'earL', 90, 'hairline-ear-side-x2')
crop('turn-34', 'earL', 80, 'ear-34-far-x2')
crop('turn-34b', 'earR', 80, 'ear-34b-far-x2')
crop('turn-front', 'halo', 110, 'halo-front-x2')
crop('turn-front', 'collar', 90, 'collar-front-x2', dy=10)
crop('turn-34', 'collar', 90, 'collar-34-x2', dy=10)
crop('turn-front', 'shoulderL', 80, 'shoulder-join-front-L-x2', dy=20)
crop('turn-front', 'shoulderR', 80, 'shoulder-join-front-R-x2', dy=20)
crop('turn-34', 'shoulderL', 80, 'shoulder-join-34-x2', dy=20)
crop('turn-front', 'elbowL', 70, 'elbow-front-L-x2')
crop('turn-front', 'handL', 70, 'hand-front-L-x2')
crop('turn-front', 'hem', 120, 'hem-legs-front-x2', dy=50)
crop('turn-side', 'feet', 80, 'shoes-side-x2', dy=-10)
crop('idle-rest', 'handL', 80, 'idle-hand-L-x2')
crop('idle-rest', 'handR', 80, 'idle-hand-R-x2')
crop('like-front', 'handR', 90, 'like-hand-front-x2', dy=-20)
crop('like-34', 'handR', 90, 'like-hand-34-x2', dy=-20)
crop('bullets-3', 'handR', 80, 'bullets-hand-front-x2', dy=-15)
crop('bullets-34', 'handR', 80, 'bullets-hand-34-x2', dy=-15)
for nm in [f[:-4] for f in os.listdir('.') if f.startswith('_close-') and f.endswith('.png')]:
    Image.open(nm + '.png').convert('RGB').save('crops/' + nm.lstrip('_') + '.png')

# ---- compare-sketch.png: each sheet view next to the matching 3D view
SK = Image.open('../sketch/brett-sheet.png').convert('RGB'); s_ = SK.width / 1988.0
pairs = [('front', (40, 90, 300, 615), 'turn-front'), ('3/4', (330, 90, 565, 615), 'turn-34'), ('side', (600, 90, 800, 615), 'turn-side'),
         ('back', (870, 90, 1130, 615), 'turn-back'), ('idle', (10, 680, 500, 1090), 'idle.png'), ('like', (520, 680, 1000, 1090), 'like.png'),
         ('bullets', (1070, 680, 1560, 1090), 'bullets.png'), ('expressions', (1565, 690, 1985, 1060), 'expressions.png'),
         ('silhouette 64', (20, 1140, 340, 1415), 'sil'), ('game camera', (1450, 1140, 1965, 1720), 'gamecam')]
TW, TH = 330, 440
W = Image.new('RGB', (TW * 2 * 5 + 80, (TH + 30) * 2 + 10), 'white')
for i, (nm, box, r3) in enumerate(pairs):
    a = SK.crop(tuple(int(v * s_) for v in box)); a.thumbnail((TW, TH))
    if r3 == 'sil':
        s1, s2 = Image.open('silhouette-64-x4.png').convert('RGB'), Image.open('silhouette-64-34-x4.png').convert('RGB')
        b = Image.new('RGB', (s1.width + s2.width + 30, 256 + 100), 'white'); b.paste(Image.open('silhouette-64.png').convert('RGB'), (10, 10))
        b.paste(Image.open('silhouette-64-34.png').convert('RGB'), (s1.width + 20, 10)); b.paste(s1, (0, 90)); b.paste(s2, (s1.width + 20, 90))
    elif r3 == 'gamecam':
        b = Image.new('RGB', (620, 470), 'white')
        b.paste(Image.open('crops/gamecam-rest-x3.png').convert('RGB'), (0, 0)); b.paste(Image.open('crops/gamecam-like-x3.png').convert('RGB'), (310, 0))
    elif r3.endswith('.png'): b = Image.open(r3).convert('RGB')
    else: b = Image.open(r3 + '.png').convert('RGB').crop(BOX)
    b.thumbnail((TW, TH))
    cx, cy = (i % 5) * (2 * TW + 15), (i // 5) * (TH + 30) + 24
    W.paste(a, (cx, cy)); W.paste(b, (cx + TW, cy)); label(W, '%s: sketch | 3D' % nm, (cx + 8, cy - 20))
W.save('compare-sketch.png')
print('sheets ok', rep, json.dumps(GRIN))
