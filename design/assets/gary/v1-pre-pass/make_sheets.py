# GHOSTED - Gary v1: screen measures (mask renders at 1x) and the sheets. Run after shoot.mjs:  python3 make_sheets.py
# Mask classes (ingame.html applyLook 'mask'): cap + brim red, eye ink blue, brows orange, gold (beak, legs) green,
# body white, the rest grey, ink hull black, background magenta.
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); D = HERE
SK = os.path.join(HERE, '..', 'sketch')
REP = json.load(open(os.path.join(D, 'ingame_report.json')))
BUILD = json.load(open(os.path.join(D, 'gary_build_report.json')))
os.makedirs(os.path.join(D, 'crops'), exist_ok=True)
try: FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 22); FS = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 17)
except Exception: FONT = FS = ImageFont.load_default()
BG = (253, 230, 200)
def img(n): return Image.open(os.path.join(D, n + '.png')).convert('RGB')
def arr(n): return np.asarray(img(n)).astype(int)
def classes(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return {'cap': (R > 200) & (G < 90) & (B < 90), 'eye': (B > 200) & (R < 60) & (G < 60),
            'brow': (R > 200) & (G > 90) & (G < 215) & (B < 110), 'gold': (G > 200) & (R < 60) & (B < 60),
            'body': (R > 230) & (G > 230) & (B > 230), 'mag': (R > 200) & (G < 60) & (B > 200)}
def bbox(m): ys, xs = np.where(m); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

def face(mask_name):
    C = classes(arr(mask_name)); L = REP[mask_name]['gary']
    cx = (L['eye_l'][0] + L['eye_r'][0]) / 2; x0, x1 = int(cx - 16), int(cx + 17)
    y0, y1 = int(L['cap_top'][1] - 6), int(L['beak_tip'][1] + 6)
    sub = {k: v[y0:y1, x0:x1] for k, v in C.items()}
    r = {'box': [x0, y0, x1, y1]}
    eye = sub['eye']; ey = np.where(eye.any(axis=1))[0]
    if len(ey):
        # each eye: split the eye columns at the face centre
        mid = int(cx - x0); per = []
        for c0, c1 in ((0, mid), (mid, eye.shape[1])):
            e = eye[:, c0:c1]; ys = np.where(e.any(axis=1))[0]; xs = np.where(e.any(axis=0))[0]
            if len(ys):
                top = int(ys.min()); cols = np.arange(c0 + xs.min(), c0 + xs.max() + 1)
                capcol = np.where(sub['cap'][:top, cols].any(axis=1))[0]
                per.append({'h_px': int(ys.max() - ys.min() + 1), 'w_px': int(xs.max() - xs.min() + 1), 'px': int(e.sum()),
                            'cap_low_above_eye_top_px': int(top - capcol.max() - 1) if len(capcol) else None})
        r['eyes'] = per
        r['cap_clear_min_px'] = min(p['cap_low_above_eye_top_px'] for p in per if p['cap_low_above_eye_top_px'] is not None)
    g = sub['gold']; gy = np.where(g.any(axis=1))[0]; gx = np.where(g.any(axis=0))[0]
    if len(gy): r['beak_wxh_px'] = [int(gx.max() - gx.min() + 1), int(gy.max() - gy.min() + 1)]
    return r

M = {}
for g in ('grass', 'path'):
    kb = bbox(~classes(arr('_kit-' + g))['mag']); gb = bbox(~classes(arr('_mask-' + g))['mag'])
    M[g] = {'kit_bbox': kb, 'kit_h_px': kb[3] - kb[1] + 1, 'gary_bbox': gb, 'gary_h_px': gb[3] - gb[1] + 1, 'gary_w_px': gb[2] - gb[0] + 1,
            'ratio_h': round((gb[3] - gb[1] + 1) / (kb[3] - kb[1] + 1), 3), 'face': face('_mask-' + g)}
for nm in ('hold', 'sorry', 'happy', 'land'): M['grass_' + nm] = {'face': face('_mask-grass-' + nm)}
fb = bbox(~classes(arr('_mask-fly-grass'))['mag'])
M['fly_level'] = {'bbox': fb, 'w_px': fb[2] - fb[0] + 1, 'h_px': fb[3] - fb[1] + 1}
U = BUILD['unit_mm'] / 1000
M['world'] = {'stand_h_m': round(209 * U, 3), 'kit_m': 0.977, 'span_bind_m': round(BUILD['span_u_bind'] * U, 3),
              'span_x_kit': round(BUILD['span_u_bind'] * U / 0.977, 3)}
M['tris'] = {'visible_by_beat': BUILD['visible_by_beat'], 'visible_max': BUILD['visible_max'], 'triangles': BUILD['triangles'],
             'three_visible_rest': REP['lineup-grass']['garyTris']}
json.dump(M, open(os.path.join(D, 'measure.json'), 'w'), indent=1)

# ---------------------------------------------------------------- sheet helpers (= Panel v1)
def label(im, text, xy=(12, 8), f=None): ImageDraw.Draw(im).text(xy, text, fill=(43, 30, 22), font=f or FONT); return im
def trim(im, pad=30, bg=None):
    a = np.asarray(im).astype(int); b = a[3, 3] if bg is None else np.array(bg)
    m = (np.abs(a - b).sum(axis=2) > 12); ys, xs = np.where(m)
    if not len(ys): return im
    return im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))
def fit_h(im, h): return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
def grid(rows, title, gap=16, bg=BG):
    W = max(sum(i.width for i in r) + gap * (len(r) + 1) for r in rows)
    H = 50 + sum(max(i.height for i in r) + gap for r in rows) + gap
    out = Image.new('RGB', (W, H), bg); label(out, title); y = 50
    for r in rows:
        x = gap
        for i in r: out.paste(i, (x, y)); x += i.width + gap
        y += max(i.height for i in r) + gap
    return out
def tile(name, cap, h=420, crop=True, src=None):
    im = src if src is not None else img(name); im = trim(im) if crop else im; im = fit_h(im, h)
    t = Image.new('RGB', (im.width, im.height + 30), BG); t.paste(im, (0, 0)); label(t, cap, (6, im.height + 4), FS); return t
def x3(name, box, k=3, grey=False):
    im = img(name).crop(box)
    if grey: im = im.convert('L').convert('RGB')
    return im.resize((im.width * k, im.height * k), Image.NEAREST)
def save(im, n): im.save(os.path.join(D, n))

save(grid([[tile('turn-' + n, c, 460) for n, c in (('front', 'front'), ('34', '3/4'), ('side', 'side (his left)'), ('back', 'back'))]],
          'Gary v1: turnaround (three.js game renderer, card camera). Rest: wings folded, bag closed.'), 'turnaround.png')
img('hero').save(os.path.join(D, 'hero.png'))
save(grid([[tile('fly-' + k, c, 330) for k, c in (('flap_up', 'up (50)'), ('flap_level', 'level (5)'), ('flap_down', 'down (-35)'))],
           [tile('flyfront-' + k, c, 260) for k, c in (('flap_up', 'up, front'), ('flap_level', 'level, front'), ('flap_down', 'down, front'))]],
          'Gary v1: the 0.6 s flap loop, 3 keys. Legs tucked, pitch 10 nose down, letter in the beak.'), 'flight.png')
save(grid([[tile('beat-' + k, c, 330) for k, c in (('land_hop', '2 land: a little hop'), ('hold', '3 hold out the letter'), ('sorry', "4a NO: soft 'sorry' tilt"),
                                                   ('happy_hop', '4b YES: happy hop'), ('fly_off', '5 fly off'))],
           [tile('beat-hold-front', 'hold, front', 330), tile('beat-sorry-front', 'sorry, front', 330)]],
          'Gary v1: delivery beats (key poses; timings are for the game build)'), 'beats.png')
save(grid([[tile('expr-' + e, c, 330, False) for e, c in (('rest', 'rest: soft'), ('happy', 'happy (yes)'), ('sorry', 'sorry (no), head tilt'), ('oops', 'oops (bumbling)'))]],
          'Gary v1: expressions (eyes + brows only; the beak is the only thing below the eyes)'), 'expressions.png')
save(grid([[tile('grey-' + n, c, 420) for n, c in (('front', 'grey front'), ('34', 'grey 3/4'), ('side', 'grey side'))]],
          'Gary v1: grey render (one grey for every lit material; ink, cream and stamp kept)'), 'grey.png')
sil = []
for n in ('sil-front', 'sil-34', 'sil-side', 'sil-fly', '_sil-grass'):
    im = img(n)
    if n.startswith('_'):
        a = np.asarray(im).astype(int); mag = (a[..., 0] > 200) & (a[..., 1] < 60) & (a[..., 2] > 200)
        im = Image.fromarray(np.where(mag[..., None], 255, 0).astype('uint8').repeat(3, axis=2))
    sil.append(fit_h(trim(im, 4, (255, 255, 255)), 64))
row1 = [s.convert('L').point(lambda v: 0 if v < 128 else 255).convert('RGB') for s in sil]
row2 = [s.resize((s.width * 3, s.height * 3), Image.NEAREST) for s in row1]
save(grid([row1, row2], '64 px silhouettes: front, 3/4, side, flight, game camera; then x3', bg=(255, 255, 255)), 'silhouette-64.png')

# lineups: colour + grey, 1x and x3 crops round Kit, Gary and the flyer
def lbox(g):
    kb = M[g]['kit_bbox']; gb = M[g]['gary_bbox']; f = REP['lineup-' + g]['fly']
    xs = [kb[0], kb[2], gb[0], gb[2], f['tip_L'][0], f['tip_R'][0]]; ys = [kb[1], kb[3], gb[1], gb[3], f['cap_top'][1]]
    return (int(min(xs) - 30), int(min(ys) - 30), int(max(xs) + 30), int(max(ys) + 25))
for g in ('grass', 'path'):
    im = img('lineup-' + g); im.convert('L').convert('RGB').save(os.path.join(D, 'lineup-%s-grey.png' % g))
    bx = lbox(g)
    im.crop(bx).save(os.path.join(D, 'lineup-%s-crop-1x.png' % g)); x3('lineup-' + g, bx).save(os.path.join(D, 'lineup-%s-crop-x3.png' % g))
    img('lineup-%s-grey' % g).crop(bx).save(os.path.join(D, 'lineup-%s-grey-crop-1x.png' % g)); x3('lineup-%s-grey' % g, bx).save(os.path.join(D, 'lineup-%s-grey-crop-x3.png' % g))
# in game: Gary next to Kit at the game camera, beats, x3 and 1x
def kbox(g, rep='lineup-'):
    kb = M[g]['kit_bbox']; gb = M[g]['gary_bbox']
    return (min(kb[0], gb[0]) - 14, min(kb[1], gb[1]) - 30, max(kb[2], gb[2]) + 40, max(kb[3], gb[3]) + 10)
tiles = []
for g in ('grass', 'path'):
    for n, c in (('', 'rest'), ('-hold', 'hold'), ('-sorry', 'sorry'), ('-happy', 'happy hop'), ('-land', 'land hop')):
        b = kbox(g); t3 = x3('lineup-' + g + n, b); t1 = img('lineup-' + g + n).crop(b)
        t = Image.new('RGB', (t3.width, t3.height + t1.height + 36), BG); t.paste(t3, (0, 0)); t.paste(t1, (0, t3.height + 4))
        label(t, c, (t1.width + 12, t3.height + 8), FS); tiles.append(t)
save(grid([tiles[:5], tiles[5:]], 'Gary v1 in game (three.js, 26 m, pitch 42, yaw 20): x3 above, 1x below. Next to Kit. Grass, then path.'), 'gamecam-beats.png')
img('lineup-grass').crop(lbox('grass')).save(os.path.join(D, 'ingame.png'))
# faces at the game camera x6 (colour, grey, mask)
fr = []
for rep, col in (('_mask-grass', 'lineup-grass'), ('_mask-grass-sorry', 'lineup-grass-sorry'), ('_mask-grass-happy', 'lineup-grass-happy'), ('_mask-path', 'lineup-path')):
    b = tuple(M[rep[6:] if rep[6:] in M else 'grass_' + rep[12:]]['face']['box']) if False else tuple(face(rep)['box'])
    a1, a2, a3 = x3(col, b, 6), x3(col, b, 6, grey=True), x3(rep, b, 6); fr.append((a1, a2, a3))
    a1.save(os.path.join(D, 'crops', 'face-%s.png' % col)); a3.save(os.path.join(D, 'crops', 'face-mask-%s.png' % rep[1:]))
save(grid([[a for a, _, _ in fr], [b for _, b, _ in fr], [c for _, _, c in fr]],
          'Gary face at the game camera, x6 of 1x: grass rest, grass sorry, grass happy, path rest. Rows: colour, grey, mask (cap red, eyes blue).'), 'gamecam-face-x6.png')

# compare with the sketch: the accepted sheet (display coords x 2900/1736) next to the 3D at the same view
S = Image.open(os.path.join(SK, 'gary-sheet.png')).convert('RGB'); k = S.width / 1736
def sk(box): return S.crop(tuple(int(v * k) for v in box))
pairs = [(sk((20, 100, 250, 470)), img('turn-front'), 'front'), (sk((250, 100, 515, 470)), img('turn-34'), '3/4'),
         (sk((505, 100, 775, 470)), img('turn-side'), 'side'), (sk((775, 100, 1000, 470)), img('turn-back'), 'back'),
         (sk((20, 580, 250, 790)), img('fly-flap_up'), 'flap up'), (sk((330, 610, 620, 790)), img('fly-flap_level'), 'flap level'),
         (sk((430, 860, 570, 1040)), img('beat-hold'), 'hold'), (sk((610, 860, 740, 1040)), img('beat-sorry'), 'sorry'),
         (sk((760, 850, 950, 1040)), img('beat-happy_hop'), 'happy hop'),
         (sk((1200, 550, 1390, 725)), img('expr-rest'), 'face rest'), (sk((1200, 750, 1390, 920)), img('expr-sorry'), 'face sorry'),
         (sk((1165, 1780, 1235, 1850)).resize((210, 210), Image.NEAREST), img('lineup-grass').crop(kbox('grass')).resize((210, 210), Image.NEAREST), 'game cam 1x (x3)')]
rows = []
for a, b, c in pairs:
    a = fit_h(trim(a, 6) if not c.startswith('game') else a, 300); b = fit_h(trim(b, 20) if not c.startswith('game') else b, 300)
    t = Image.new('RGB', (a.width + b.width + 30, 336), BG); t.paste(a, (0, 0)); t.paste(b, (a.width + 30, 0)); label(t, c + ': sketch | 3D', (4, 306), FS); rows.append(t)
save(grid([rows[:4], rows[4:9], rows[9:]], 'Compare: the accepted sketch (left of each pair) and the 3D (right)'), 'compare-sketch.png')
# the in-game compare: sketch game-camera tiles (x3 rows) next to the 3D at x3
save(grid([[tile(None, 'sketch: game camera x3 (grass)', 300, False, sk((15, 1715, 1045, 1915))), tile(None, '3D: game camera x3 (grass): rest, hold, sorry, happy, land', 300, False,
            Image.fromarray(np.hstack([np.asarray(fit_h(x3('lineup-grass' + n, kbox('grass')), 300)) for n in ('', '-hold', '-sorry', '-happy', '-land')])))]],
          'Compare in game: sketch tiles and the 3D render at the same camera'), 'compare-ingame.png')
# x2 crops of each card panel for the whole-picture check
for n in ('turn-front', 'turn-34', 'turn-side', 'turn-back', 'beat-hold', 'beat-sorry', 'beat-happy_hop', 'beat-land_hop', 'beat-fly_off', 'fly-flap_level', 'hero'):
    im = trim(img(n), 10); im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(os.path.join(D, 'crops', n + '-x2.png'))
print(json.dumps({k: v for k, v in M.items() if k != 'tris'}, indent=1)); print(json.dumps(M['tris']['visible_by_beat']))
