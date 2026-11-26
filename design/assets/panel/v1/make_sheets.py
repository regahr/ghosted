# GHOSTED - The Panel v1: screen measures (mask renders at 1x) and the sheets. Run after shoot.mjs:
#   python3 make_sheets.py [blockout]
# Mask classes (ingame.html applyLook 'mask'): hair + hairline ink red, eye ink blue, brows orange, mouth ink green,
# teeth cyan, skin white, the rest grey, ink hull black, background magenta.
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = 'blockout' in sys.argv
DIR = next((a[4:] for a in sys.argv if a.startswith('dir=')), None)
D = os.path.join(HERE, DIR) if DIR else os.path.join(HERE, 'blockout') if BLOCK else HERE
SK = os.path.join(HERE, '..', 'sketch')
REP = json.load(open(os.path.join(D, 'ingame_report.json')))
os.makedirs(os.path.join(D, 'crops'), exist_ok=True)
try: FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 22); FS = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 17)
except Exception: FONT = FS = ImageFont.load_default()
BG = (253, 230, 200)

def img(n): return Image.open(os.path.join(D, n + '.png')).convert('RGB')
def arr(n): return np.asarray(img(n)).astype(int)

def classes(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return {'hair': (R > 200) & (G < 90) & (B < 90), 'eye': (B > 200) & (R < 60) & (G < 60),
            'brow': (R > 200) & (G > 90) & (G < 215) & (B < 110), 'mouth': (G > 200) & (R < 60) & (B < 60),
            'teeth': (G > 200) & (B > 200) & (R < 60), 'skin': (R > 230) & (G > 230) & (B > 230),
            'hull': (R < 30) & (G < 30) & (B < 30)}

def face_measure(mask_name, colour_name, rep_name):
    a = arr(mask_name); C = classes(a); col = arr(colour_name) if colour_name else None
    luma = (0.299 * col[..., 0] + 0.587 * col[..., 1] + 0.114 * col[..., 2]) if col is not None else None
    out = {}
    for who in ('cf', 'wb'):
        L = REP[rep_name]['panel'][who]
        ex = [L['eye_l'][0], L['eye_r'][0]]; x0, x1 = int(min(ex) - 14), int(max(ex) + 15)
        y0, y1 = int(L['cap_top'][1] - 6), int(L['chin'][1] + 8)
        sub = {k: v[y0:y1, x0:x1] for k, v in C.items()}
        lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[y0:y1, x0:x1]
        r = {'head_px_cap_top_to_chin': round(L['chin'][1] - L['cap_top'][1], 1), 'box': [x0, y0, x1, y1]}
        # forehead band per brow column: skin rows between the lowest hair pixel above the brow and the brow top
        bands = []
        for c in range(sub['brow'].shape[1]):
            by = np.where(sub['brow'][:, c])[0]
            if len(by) == 0: continue
            bt = by.min(); hy = np.where(sub['hair'][:bt, c])[0]
            if len(hy) == 0: continue
            bands.append(int(bt - hy.max() - 1))
        r['forehead_band_px'] = [min(bands), int(np.median(bands)), max(bands), len(bands)] if bands else None
        ey = np.where(sub['eye'].any(axis=1))[0]; exs = np.where(sub['eye'].any(axis=0))[0]
        if len(ey) < 2:   # happy (arc) eyes do not resolve as blue at 1x: use the eye landmarks (+-2 px)
            ly = (L['eye_l'][1] + L['eye_r'][1]) / 2 - y0; ey = np.array([int(ly - 2), int(ly + 2)])
            exs = np.array([int(L['eye_l'][0] - x0 - 2), int(L['eye_r'][0] - x0 + 2)]); r['eyes_from_landmarks'] = True
        if len(ey):
            eye_top, eye_bot = int(ey.min()), int(ey.max()); r['eye_top_bottom_y'] = [eye_top + y0, eye_bot + y0]
            # hair in the eye columns above the eye top; hair beside the face (temple columns: 4 px outside each eye)
            hc = np.where(sub['hair'][:, exs.min():exs.max() + 1].any(axis=1))[0]
            r['hair_low_in_eye_columns_above_eye_top_px'] = int(eye_top - hc.max()) if len(hc) else None
            side = []
            for c0, c1 in ((max(exs.min() - 6, 0), exs.min()), (exs.max() + 1, min(exs.max() + 7, sub['hair'].shape[1]))):
                hs = np.where(sub['hair'][:eye_bot + 1, c0:c1].any(axis=1))[0]
                if len(hs): side.append(int(eye_top - hs.max()))
            r['side_hair_low_above_eye_top_px'] = min(side) if side else None
            mm = sub['mouth'] | sub['teeth']; my = np.where(mm.any(axis=1))[0]; mx = np.where(mm.any(axis=0))[0]
            if len(my):
                r['mouth_wxh_px'] = [int(mx.max() - mx.min() + 1), int(my.max() - my.min() + 1)]
                r['mouth_dark_px'] = int(sub['mouth'].sum()); r['teeth_px'] = int(sub['teeth'].sum())
                r['mouth_gap_below_eyes_px'] = int(my.min() - eye_bot - 1)
                # skin under the mouth, per mouth column: rows of skin from the mouth bottom down to the chin ink / edge
                under = []
                for c in range(mx.min(), mx.max() + 1):
                    ys = np.where(mm[:, c])[0]
                    if not len(ys): continue
                    k = ys.max() + 1; n = 0
                    while k < sub['skin'].shape[0] and lum[k, c] > 170 and not mm[k, c]: n += 1; k += 1
                    under.append(n)
                r['light_rows_under_mouth_px_min_median'] = [int(min(under)), int(np.median(under))]
                if luma is not None:
                    reg = luma[y0:y1, x0:x1]
                    r['mouth_luma'] = int(reg[sub['mouth']].mean()) if sub['mouth'].any() else None
                    r['skin_luma'] = int(reg[sub['skin']].mean())
            else:
                r['mouth_wxh_px'] = [0, 0]; r['mouth_dark_px'] = 0
        out[who] = r
    return out

def bbox_nonmag(n):
    a = arr(n); m = ~((a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] > 200)); ys, xs = np.where(m)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

M = {}
for g in ('grass', 'path'):
    kb = bbox_nonmag('_kit-' + g); M['kit_' + g] = {'bbox': kb, 'height_px': kb[3] - kb[1] + 1,
                                                    'kit_head_px_est (0.36 m / 0.977 m of the height)': round((kb[3] - kb[1] + 1) * 0.36 / 0.977, 1)}
    M['idle_' + g] = face_measure('_mask-' + g, 'lineup-' + g, '_mask-' + g)
    M['set_bbox_' + g] = bbox_nonmag('_mask-' + g)
if not BLOCK:
    for nm in ('nod', 'tilt', 'lean', 'rest-lines', 'grin', 'point'):
        M['grass_' + nm] = face_measure('_mask-grass-' + nm, 'lineup-grass-' + nm if os.path.exists(os.path.join(D, 'lineup-grass-' + nm + '.png')) else None, '_mask-grass-' + nm)
    for nm in ('nod', 'grin'):
        M['path_' + nm] = face_measure('_mask-path-' + nm, None, '_mask-path-' + nm)
json.dump(M, open(os.path.join(D, 'measure.json'), 'w'), indent=1)

# ---------------------------------------------------------------- sheet helpers
def label(im, text, xy=(12, 8), f=None):
    d = ImageDraw.Draw(im); d.text(xy, text, fill=(43, 30, 22), font=f or FONT); return im
def trim(im, pad=30, bg=None):
    a = np.asarray(im).astype(int); b = a[3, 3] if bg is None else np.array(bg)
    m = (np.abs(a - b).sum(axis=2) > 12); ys, xs = np.where(m)
    if not len(ys): return im
    return im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))
def fit_h(im, h): return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
def grid(rows, title, gap=16, bg=BG):
    W = max(sum(i.width for i in r) + gap * (len(r) + 1) for r in rows)
    H = 50 + sum(max(i.height for i in r) + gap for r in rows) + gap
    out = Image.new('RGB', (W, H), bg); label(out, title)
    y = 50
    for r in rows:
        x = gap
        for i in r: out.paste(i, (x, y)); x += i.width + gap
        y += max(i.height for i in r) + gap
    return out
def tile(name, cap, h=420, crop=True):
    im = img(name); im = trim(im) if crop else im; im = fit_h(im, h)
    t = Image.new('RGB', (im.width, im.height + 30), BG); t.paste(im, (0, 0)); label(t, cap, (6, im.height + 4), FS); return t
def x3(name, box, k=3, grey=False):
    im = img(name).crop(box)
    if grey: im = im.convert('L').convert('RGB')
    return im.resize((im.width * k, im.height * k), Image.NEAREST)
def save(im, n): im.save(os.path.join(D, n))

def lineup_crop_box(g):
    b = M['set_bbox_' + g]; kb = M['kit_' + g]['bbox']
    x0, y0, x1, y1 = min(b[0], kb[0]) - 30, min(b[1], kb[1]) - 25, max(b[2], kb[2]) + 30, max(b[3], kb[3]) + 25
    return (x0, y0, x1, y1)

# grey lineups + 1x / x3 crops (colour and grey)
for g in ('grass', 'path'):
    im = img('lineup-' + g); im.convert('L').convert('RGB').save(os.path.join(D, 'lineup-%s-grey.png' % g))
    bx = lineup_crop_box(g)
    im.crop(bx).save(os.path.join(D, 'lineup-%s-crop-1x.png' % g)); x3('lineup-' + g, bx).save(os.path.join(D, 'lineup-%s-crop-x3.png' % g))
    img('lineup-%s-grey' % g).crop(bx).save(os.path.join(D, 'lineup-%s-grey-crop-1x.png' % g)); x3('lineup-%s-grey' % g, bx).save(os.path.join(D, 'lineup-%s-grey-crop-x3.png' % g))

def face_box(rep, who, pad=(14, 10)):
    L = REP[rep]['panel'][who]; ex = [L['eye_l'][0], L['eye_r'][0]]
    return (int(min(ex) - pad[0] - 4), int(L['cap_top'][1] - pad[1]), int(max(ex) + pad[0] + 5), int(L['chin'][1] + pad[1] + 2))

if BLOCK:
    rows = [[tile('turn-front', 'front', 380), tile('turn-34', '3/4', 380)],
            [x3('lineup-grass', lineup_crop_box('grass')), x3('lineup-path', lineup_crop_box('path'))],
            [x3('_mask-grass', face_box('_mask-grass', w), 6) for w in ('cf', 'wb')] + [x3('lineup-grass', face_box('_mask-grass', w), 6) for w in ('cf', 'wb')]]
    save(grid(rows, 'The Panel BLOCKOUT (three.js game renderer): front, 3/4; game camera x3 (grass, path); faces x6 (mask, colour)'), 'blockout-sheet.png')
    print(json.dumps(M, indent=1)); sys.exit()

# ---------------------------------------------------------------- final sheets
# set turnaround + each person's front and 3/4 + the box
rows = [[tile(n, c, 330) for n, c in (('turn-front', 'set front'), ('turn-34', 'set 3/4'), ('turn-side', 'set side'), ('turn-back', 'set back'))],
        [tile(n, c, 360) for n, c in (('cf-front', 'Culture Fit front'), ('cf-34', 'Culture Fit 3/4'), ('wb-front', 'Whiteboard front'), ('wb-34', 'Whiteboard 3/4'), ('box-front', 'the box'))]]
save(grid(rows, 'The Panel v1: turnaround (three.js game renderer, card camera). Rest: card faces with the rest lines.'), 'turnaround.png')
rows = [[tile(n, c, 330) for n, c in (('m-cf-rest', 'CF rest'), ('m-cf-nod', 'CF nod (+14: -8 to +6), grin'), ('m-cf-tilt', 'CF tilt 12 + hands under the chin'))],
        [tile(n, c, 330) for n, c in (('m-wb-up', 'WB marker up'), ('m-wb-click', 'WB *click* (talk)'), ('m-wb-point', 'WB point (at you, 3/4)'))],
        [tile(n, c, 260) for n, c in (('m-box-camoff', 'box: camera off'), ('m-box-dark', 'blink: dark'), ('m-box-muted', 'muted'))],
        [tile(n, c, 300) for n, c in (('m-rest-side', 'rest (side)'), ('m-lean-side', 'all lean in (side): 14 / 14 / box 12'), ('m-lean-34', 'all lean in (3/4)'))]]
save(grid(rows, 'The Panel v1: motion (three.js). Pivots: chin (head), elbow line (people lean), bottom front edge (box).'), 'motion.png')
rows = [[tile('expr-' + n, c, 300, False) for n, c in (('cf-rest', 'CF rest: smile'), ('cf-grin', "CF nod: 'love that!' (Ricky grin)"), ('cf-tilt', "CF tilt: 'hmm, vibes'"), ('cf-talk', "CF: 'where do you see...' (talk)"))],
        [tile('expr-' + n, c, 300, False) for n, c in (('wb-rest', 'WB rest: flat line'), ('wb-talk', 'WB talk'), ('wb-skeptic', 'WB: one brow up'))]]
save(grid(rows, 'The Panel v1: expressions (front). Mouths: closed line or Ricky style. No fringe; nothing beside the eyes.'), 'expressions.png')
rows = [[tile('grey-front', 'grey front', 380), tile('grey-34', 'grey 3/4', 380)]]
save(grid(rows, 'The Panel v1: grey render (one grey for every lit material; ink kept)'), 'grey.png')
# silhouettes at 64 px high (front, 3/4, game camera), then x2
sil = []
for n in ('sil-front', 'sil-34', '_sil-grass'):
    im = img(n)
    if n.startswith('_'):
        a = np.asarray(im).astype(int); mag = (a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] > 200)
        im = Image.fromarray(np.where(mag[..., None], 255, 0).astype('uint8').repeat(3, axis=2))
    im = trim(im, 4, (255, 255, 255)); sil.append(fit_h(im, 64))
row1 = [s.convert('L').point(lambda v: 0 if v < 128 else 255).convert('RGB') for s in sil]
row2 = [s.resize((s.width * 2, s.height * 2), Image.NEAREST) for s in row1]
save(grid([row1, row2], '64 px silhouettes: front, 3/4, game camera; then x2', bg=(255, 255, 255)), 'silhouette-64.png')
# in-game: the set + Kit at the game camera, 1x and x3, motion beats
bx = lineup_crop_box('grass')
beats = [('lineup-grass', 'idle (talk)'), ('lineup-grass-nod', 'CF nod'), ('lineup-grass-tilt', 'CF tilt'), ('lineup-grass-click', 'WB click'),
         ('lineup-grass-point', 'WB point'), ('lineup-grass-dark', 'box blink: dark'), ('lineup-grass-muted', 'box muted'), ('lineup-grass-lean', 'all lean in')]
tiles = []
for n, c in beats:
    t3 = x3(n, bx); t1 = img(n).crop(bx)
    t = Image.new('RGB', (t3.width, t3.height + t1.height + 40), BG); t.paste(t3, (0, 0)); t.paste(t1, (0, t3.height + 4)); label(t, c, (t1.width + 12, t3.height + 8), FS); tiles.append(t)
save(grid([tiles[:4], tiles[4:]], 'The Panel v1 in game (three.js, 26 m, pitch 42, yaw 20): x3 above, 1x below. Kit in front. Grass.'), 'gamecam-beats.png')
img('lineup-grass').crop(bx).save(os.path.join(D, 'ingame.png'))
# faces at the game camera x3 (colour, grey) and x6 masks
fr = []
for rep, col in (('_mask-grass', 'lineup-grass'), ('_mask-grass-rest-lines', 'lineup-grass-rest-lines'), ('_mask-grass-nod', 'lineup-grass-nod'), ('_mask-path', 'lineup-path')):
    for w in ('cf', 'wb'):
        b = face_box(rep, w); fr.append((x3(col, b), x3(col, b, grey=True), x3(rep, b)))
rows = [[a for a, _, _ in fr], [b for _, b, _ in fr], [c for _, _, c in fr]]
save(grid(rows, 'Faces at the game camera, x3 of 1x: grass idle (talk), grass rest lines, grass CF nod grin, path idle. CF then WB. Rows: colour, grey, mask.'), 'gamecam-face-x3.png')
for rep in ('_mask-grass', '_mask-grass-nod', '_mask-path', '_mask-grass-grin'):
    for w in ('cf', 'wb'):
        x3(rep, face_box(rep, w), 6).save(os.path.join(D, 'crops', 'face-mask-%s-%s.png' % (rep[6:], w)))
        col = 'lineup-' + rep[6:]
        if os.path.exists(os.path.join(D, col + '.png')): x3(col, face_box(rep, w), 6).save(os.path.join(D, 'crops', 'face-%s-%s.png' % (rep[6:], w)))
# compare with the sketch: crops of the accepted sheet next to the 3D at the same view
S = Image.open(os.path.join(SK, 'panel-sheet.png')).convert('RGB'); k = S.width / 1708
def sk(box): return S.crop(tuple(int(v * k) for v in box))
pairs = [(sk((15, 120, 245, 280)), img('turn-front'), 'set front'), (sk((285, 120, 515, 280)), img('turn-34'), 'set 3/4'),
         (sk((625, 120, 745, 280)), img('turn-side'), 'side'), (sk((820, 120, 1050, 280)), img('turn-back'), 'back'),
         (sk((10, 340, 215, 585)), img('cf-front'), 'CF front'), (sk((500, 340, 660, 585)), img('wb-front'), 'WB front'),
         (sk((15, 1600, 285, 1850)), img('lineup-grass').crop(bx), 'game camera (sketch x3 / 3D 1x)')]
rows = []
for a, b, c in pairs:
    a = fit_h(trim(a, 6), 300); b = fit_h(trim(b, 20) if not c.startswith('game') else b, 300)
    t = Image.new('RGB', (a.width + b.width + 30, 336), BG); t.paste(a, (0, 0)); t.paste(b, (a.width + 30, 0)); label(t, c + ': sketch | 3D', (4, 306), FS); rows.append(t)
save(grid([rows[:4], rows[4:]], 'Compare: the accepted sketch (left of each pair) and the 3D (right)'), 'compare-sketch.png')
# x2 crops of each card panel for the whole-picture check
for n in ('turn-front', 'turn-34', 'turn-side', 'turn-back', 'cf-front', 'cf-34', 'wb-front', 'wb-34', 'm-wb-point', 'm-cf-tilt', 'm-lean-side'):
    im = trim(img(n), 10); im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(os.path.join(D, 'crops', n + '-x2.png'))
print(json.dumps(M, indent=1))
