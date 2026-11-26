# Builds the sheet images, the evidence crops and the 1x face numbers from the Blender renders (render_juno.py) and the
# three.js renders (shoot_ingame.mjs). Run last: python3 make_sheets.py   (from brett/v1/make_sheets.py)
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
row(['turn-front', 'turn-34', 'turn-side', 'turn-back'], BOX, 'turnaround.png', ['front (rest: cup in both hands)', '3/4', 'side', 'back'])
row(['hand-front', 'hand-34', 'hand-side', 'ingame-hand'], BOX, 'hand-over.png',
    ['hand over: her right arm forward, cup on the palm', 'hand over, 3/4', 'hand over, side', 'hand over, three.js (game engine)'])
row(['wave-1', 'wave-2', 'wave-3', 'wave-34', 'ingame-wave'], BOX, 'wave.png',
    ['wave 1 (cup in her left hand)', 'wave 2 (talk)', 'wave 3', 'wave 2, 3/4', 'wave 2, three.js (game engine)'])
row(['write-front', 'write-34', 'write-side', 'write-then', 'ingame-write'], BOX, 'writing.png',
    ['writing: cup up, marker, head down 14, eyes down', 'writing, 3/4', 'writing, side', "then: 'here you go' (dry face)", 'writing, three.js (game engine)'])
row(['expr-rest', 'expr-laugh', 'expr-talk', 'expr-dry', 'expr-writing'], (0, 0, 900, 900), 'expressions.png',
    ['rest: calm smile (closed line)', 'laugh (Ricky mouth)', 'talk (Ricky mouth)', 'dry: one brow, smirk', 'writing: eyes down'])
# the cup at card size: alone (two sizes) and in her hands
a = Image.open('cup-card.png').convert('RGB'); b = Image.open('cup-card-small.png').convert('RGB'); c = Image.open('_close-cup.png').convert('RGB').resize((800, 800))
W = Image.new('RGB', (a.width + b.width + c.width + 40, 840), 'white'); W.paste(a, (0, 30)); W.paste(b, (a.width + 20, 30)); W.paste(c, (a.width + b.width + 40, 30))
label(W, 'cup alone, 600x800 (cup about 560 px tall)', (8, 8)); label(W, 'card size, 240x320 (cup about 200 px)', (a.width + 24, 8)); label(W, 'in her hands (rest)', (a.width + b.width + 48, 8))
W.save('cup-closeup.png')

# ---- compare-ingame: Blender | three.js | |difference| x4 (same pose: rest)
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

# ---- lineups: greyscale (luminance = grey.png), x3 and 1x crops round Kit, Ricky, Dot, Brett, the Ghosties, the ATS and Juno
def lum(p):
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    return np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
def grey(src, dst):
    p = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
    Image.fromarray((lum(p) * 255).round().astype(np.uint8)).save(dst)
LBOX = {'grass': (670, 390, 970, 715), 'path': (525, 325, 1135, 560)}
FACE = {}
for g in ('grass', 'path'):
    grey('lineup-%s.png' % g, 'lineup-%s-grey.png' % g)
    for suf in ('', '-grey'):
        im = Image.open('lineup-%s%s.png' % (g, suf)).convert('RGB').crop(LBOX[g])
        im.resize((im.width * 3, im.height * 3), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf)); im.save('lineup-%s%s-crop-1x.png' % (g, suf))
    e = IR['lineup-' + g]; d_ = e['px_juno']; fx = (d_['x0'] + d_['x1']) // 2; fy = int(e['hair']['eyeTopPx'])
    fb = (fx - 24, fy - 30, fx + 24, fy + 16)
    FACE[g] = {}
    for ex, tag, src in (('rest', '', ''), ('laugh', '_laugh', '-laugh'), ('talk', '_talk', '-talk'), ('dry', '_dry', '-dry'), ('write', '_write', '-write')):
        hm = e['hair' + tag]; col_img = 'lineup-%s%s.png' % (g, src)
        a = Image.open(col_img).convert('RGB').crop(fb).resize((48 * 6, 46 * 6), Image.NEAREST)
        m = Image.open('_lineup-%s-hairmask%s.png' % (g, src)).convert('RGB').crop(fb).resize((48 * 6, 46 * 6), Image.NEAREST)
        W = Image.new('RGB', (a.width * 2 + 10, a.height + 46), 'white'); W.paste(a, (0, 46)); W.paste(m, (a.width + 10, 46))
        dr = ImageDraw.Draw(W)
        if hm['eyeTopPx'] < 1e8:
            for yy, c_ in (((hm['hairLowestInEyeColumnsPx'] - fb[1]) * 6 + 46 + 6, (220, 0, 0)), ((hm['eyeTopPx'] - fb[1]) * 6 + 46, (0, 0, 220))):
                dr.line((a.width + 10, yy, W.width, yy), fill=c_, width=1)
        fh = hm['forehead']
        label(W, 'game camera, x6 (%s, %s)' % (g, ex), (6, 6))
        label(W, 'mask: hair + hairline ink + strands red, brows orange, eyes blue, mouth ink green, teeth cyan', (a.width + 14, 6))
        label(W, 'forehead band %s-%s px (min-max over %d brow columns); hair low %s, eye top %s' % (
            fh['minPx'], fh['maxPx'], fh['columns'], hm['hairLowestInEyeColumnsPx'], hm['eyeTopPx'] if hm['eyeTopPx'] < 1e8 else '-'), (a.width + 14, 24))
        W.save('crops/gamecam-face-mask-%s-%s.png' % (ex, g))
        for suf, tg in (('', ''), ('-grey', '-grey')):
            if suf: grey(col_img, '_tmp_grey.png'); srcim = '_tmp_grey.png'
            else: srcim = col_img
            Image.open(srcim).convert('RGB').crop(fb).resize((48 * 3, 46 * 3), Image.NEAREST).save('crops/gamecam-face-x3%s-%s-%s.png' % (tg, ex, g))
        Image.open(col_img).convert('RGB').crop(fb).save('crops/gamecam-face-1x-%s-%s.png' % (ex, g))
        # the mouth read at 1x: dark mouth ink (green), teeth (cyan); luma from the colour render at the same pixels
        col = np.asarray(Image.open(col_img).convert('RGB')).astype(float) / 255; L = lum(col) * 255
        mk = np.asarray(Image.open('_lineup-%s-hairmask%s.png' % (g, src)).convert('RGB')).astype(int)
        green = (mk[..., 1] > 150) & (mk[..., 0] < 90) & (mk[..., 2] < 90); cyan = (mk[..., 1] > 150) & (mk[..., 2] > 150) & (mk[..., 0] < 90)
        blue = (mk[..., 2] > 150) & (mk[..., 0] < 90) & (mk[..., 1] < 90); white = (mk > 200).all(axis=2); red = (mk[..., 0] > 150) & (mk[..., 1] < 90) & (mk[..., 2] < 90)
        mouth = green | cyan; r = {'forehead_band_px': [fh['minPx'], fh['medianPx'], fh['maxPx'], fh['columns']]}
        if mouth.any():
            ys, xs = np.where(mouth); win = np.zeros_like(white); win[ys.min() - 3:ys.max() + 4, xs.min() - 3:xs.max() + 4] = True
            r.update({'mouth_ink_px': int(green.sum()), 'teeth_px': int(cyan.sum()), 'box_wxh_px': [int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)],
                      'mouth_ink_luma': round(float(L[green].mean()), 1) if green.any() else None, 'teeth_luma': round(float(L[cyan].mean()), 1) if cyan.any() else None,
                      'skin_luma_round_it': round(float(L[white & win].mean()), 1) if (white & win).any() else None,
                      'gap_below_eye_bottom_px': int(ys.min() - hm['eyePixels']['y1']) if blue.any() else None})
        else: r.update({'mouth_ink_px': 0, 'teeth_px': 0, 'note': 'the line is below 1 px at 1x and does not resolve'})
        if blue.any(): r['eye_luma'] = round(float(L[blue].mean()), 1)
        # side hair vs the eyes: the lowest hair or hair-edge-ink pixel OUTSIDE the eye columns, on the face (above the eye
        # bottom + 4 px), against the eye top. Positive = the hair is above the eye top.
        if blue.any():
            ep = hm['eyePixels']; ys, xs = np.where(red)
            head = (ys < ep['y1'] + 4) & (xs > ep['x0'] - 22) & (xs < ep['x1'] + 22)
            side = head & ((xs < ep['x0'] - 2) | (xs > ep['x1'] + 2))
            lo = int(ys[side].max()) if side.any() else None
            r.update({'side_hair_lowest_px': lo, 'eye_top_px': ep['y0'], 'side_hair_above_eye_top_px': (ep['y0'] - lo) if lo is not None else None,
                      'hair_in_eye_columns_above_eye_top_px': hm['gapPx']})
        FACE[g][ex] = r
if os.path.exists('_tmp_grey.png'): os.remove('_tmp_grey.png')
json.dump(FACE, open('face_report.json', 'w'), indent=1)
# face checks side by side: x3 colour and grey, rest / laugh / talk / dry / write, grass and path
tiles = []
for g in ('grass', 'path'):
    for tg in ('', '-grey'):
        tiles.append([Image.open('crops/gamecam-face-x3%s-%s-%s.png' % (tg, ex, g)).convert('RGB') for ex in ('rest', 'laugh', 'talk', 'dry', 'write')])
tw, th = tiles[0][0].size
W = Image.new('RGB', (tw * 5 + 40, (th + 22) * 4 + 22), 'white')
for r_, rowt in enumerate(tiles):
    for c_, t in enumerate(rowt): W.paste(t, (c_ * (tw + 10), 22 + r_ * (th + 22)))
    label(W, ['grass, colour', 'grass, grey', 'path, colour', 'path, grey'][r_] + ': rest, laugh, talk, dry, writing (x3 of 1x)', (4, 4 + r_ * (th + 22)))
W.save('gamecam-face-x3.png')
# the beats at the game camera, x3 (grass and path)
for g in ('grass', 'path'):
    d_ = IR['lineup-' + g]['px_juno']; b = (d_['x0'] - 30, d_['y0'] - 10, d_['x1'] + 30, d_['y1'] + 10)
    for nm in ('', '-hand', '-wave1', '-wave2', '-wave3', '-write', '-handover', '-laugh', '-talk'):
        Image.open('lineup-%s%s.png' % (g, nm)).convert('RGB').crop(b).resize(((b[2] - b[0]) * 3, (b[3] - b[1]) * 3), Image.NEAREST).save('crops/gamecam-%s-%s-x3.png' % (g, nm[1:] or 'rest'))
BEATS = ['rest', 'hand', 'wave1', 'wave2', 'wave3', 'write', 'handover', 'laugh', 'talk']
tl = [[Image.open('crops/gamecam-%s-%s-x3.png' % (g, k)).convert('RGB') for k in BEATS] for g in ('grass', 'path')]
tw = max(t.width for r_ in tl for t in r_); th = max(t.height for r_ in tl for t in r_)
W = Image.new('RGB', ((tw + 8) * len(BEATS), (th + 22) * 2), 'white')
for r_, rowt in enumerate(tl):
    for c_, t in enumerate(rowt): W.paste(t, (c_ * (tw + 8), 20 + r_ * (th + 22))); label(W, ('grass: ' if r_ == 0 else 'path: ') + BEATS[c_], (c_ * (tw + 8) + 4, 2 + r_ * (th + 22)))
W.save('gamecam-beats-x3.png')

# ---- evidence crops (2x nearest) at the points projected by render_juno.py
def crop(view, key, half, out, scale=2, dy=0, dx=0):
    x, y = CP[view][key]; x += dx; y += dy; im = Image.open(view + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('turn-front', 'face', 120, 'face-front-x2')
crop('turn-front', 'forehead', 110, 'hair-front-x2', dy=-20)
crop('turn-34', 'forehead', 110, 'forehead-34-x2', dy=-10)
crop('turn-34b', 'forehead', 110, 'forehead-34b-x2', dy=-10)
crop('turn-back', 'nape', 130, 'hair-back-x2', dy=-40)
crop('turn-side', 'face', 110, 'face-side-x2', dx=20)
crop('turn-side', 'earL', 90, 'hairline-ear-side-x2')
crop('turn-34', 'earL', 80, 'ear-34-far-x2')
crop('turn-34b', 'earR', 80, 'ear-34b-far-x2')
crop('turn-front', 'puff', 100, 'puff-front-x2')
crop('turn-side', 'puff', 100, 'puff-side-x2')
crop('turn-front', 'neck', 80, 'neck-front-x2', dy=10)
crop('turn-front', 'bib', 110, 'bib-front-x2')
crop('turn-front', 'tie', 100, 'tie-front-x2')
crop('turn-back', 'bow', 100, 'bow-back-x2')
crop('turn-front', 'shoulderL', 80, 'shoulder-join-front-L-x2', dy=20)
crop('turn-front', 'shoulderR', 80, 'shoulder-join-front-R-x2', dy=20)
crop('turn-34', 'shoulderL', 80, 'shoulder-join-34-x2', dy=20)
crop('turn-front', 'elbowL', 70, 'cuff-front-L-x2')
crop('turn-front', 'handL', 70, 'hand-front-L-x2')
crop('turn-front', 'cup', 90, 'cup-front-x2')
crop('turn-front', 'hem', 130, 'skirt-hem-front-x2', dy=10)
crop('turn-34', 'hem', 130, 'skirt-hem-34-x2', dy=10)
crop('turn-side', 'feet', 80, 'shoes-side-x2', dy=-10)
crop('hand-front', 'cup', 90, 'handover-cup-front-x2')
crop('hand-side', 'cup', 90, 'handover-cup-side-x2')
crop('hand-front', 'handL', 90, 'handover-free-hand-x2')
crop('wave-2', 'handR', 90, 'wave-hand-x2')
crop('wave-2', 'elbowR', 90, 'wave-elbow-x2')
crop('write-front', 'cup', 90, 'write-cup-marker-x2')
crop('write-34', 'cup', 90, 'write-cup-marker-34-x2')
for nm in [f[:-4] for f in os.listdir('.') if f.startswith('_close-') and f.endswith('.png')]:
    Image.open(nm + '.png').convert('RGB').save('crops/' + nm.lstrip('_') + '.png')

# ---- compare-sketch.png: each sheet view next to the matching 3D view (sketch boxes in juno-sheet.png pixels)
SK = Image.open('../sketch/juno-sheet.png').convert('RGB')
pairs = [('front', (47, 190, 395, 908), 'turn-front'), ('3/4', (458, 190, 758, 908), 'turn-34'), ('side', (853, 190, 1137, 908), 'turn-side'),
         ('back', (1248, 190, 1643, 908), 'turn-back'), ('hand over', (24, 1027, 695, 1580), 'hand-over.png'), ('wave', (743, 1027, 1438, 1580), 'wave.png'),
         ('writing', (1485, 1027, 2180, 1580), 'writing.png'), ('expressions', (2283, 1011, 2891, 1548), 'expressions.png'),
         ('silhouette 64', (24, 1706, 474, 2054), 'sil'), ('cup at card size', (24, 2196, 632, 2386), 'cup'),
         ('game camera x3', (24, 2544, 1406, 3097), 'gamecam'), ('face check x3', (1754, 2575, 2275, 2907), 'gamecam-face-x3.png')]
TW, TH = 360, 440
W = Image.new('RGB', (TW * 2 * 4 + 60, (TH + 30) * 3 + 10), 'white')
for i, (nm, box, r3) in enumerate(pairs):
    a = SK.crop(box); a.thumbnail((TW, TH))
    if r3 == 'sil':
        s1, s2 = Image.open('silhouette-64-x4.png').convert('RGB'), Image.open('silhouette-64-34-x4.png').convert('RGB')
        b = Image.new('RGB', (s1.width + s2.width + 30, 256 + 100), 'white'); b.paste(Image.open('silhouette-64.png').convert('RGB'), (10, 10))
        b.paste(Image.open('silhouette-64-34.png').convert('RGB'), (s1.width + 20, 10)); b.paste(s1, (0, 90)); b.paste(s2, (s1.width + 20, 90))
    elif r3 == 'cup':
        b = Image.new('RGB', (840, 800), 'white'); b.paste(Image.open('cup-card.png').convert('RGB'), (0, 0)); b.paste(Image.open('cup-card-small.png').convert('RGB'), (600, 240))
    elif r3 == 'gamecam':
        b = Image.open('gamecam-beats-x3.png').convert('RGB')
    elif r3.endswith('.png'): b = Image.open(r3).convert('RGB')
    else: b = Image.open(r3 + '.png').convert('RGB').crop(BOX)
    b.thumbnail((TW, TH))
    cx, cy = (i % 4) * (2 * TW + 15), (i // 4) * (TH + 30) + 24
    W.paste(a, (cx, cy)); W.paste(b, (cx + TW, cy)); label(W, '%s: sketch | 3D' % nm, (cx + 8, cy - 20))
W.save('compare-sketch.png')
# sketch-vs-3D crops at 2x of the turnaround views
for nm, box, r3 in pairs[:4]:
    a = SK.crop(box); b = Image.open(r3 + '.png').convert('RGB').crop(BOX); a = a.resize((int(a.width * b.height / a.height), b.height))
    Wc = Image.new('RGB', (a.width + b.width + 10, b.height), 'white'); Wc.paste(a, (0, 0)); Wc.paste(b, (a.width + 10, 0))
    Wc.save('crops/compare-%s.png' % nm.replace('/', ''))
print('sheets ok', rep, json.dumps(FACE))
