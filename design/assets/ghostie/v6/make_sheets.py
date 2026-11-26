# Builds the sheet images and evidence crops from the Blender renders (render_ghostie.py) and the three.js renders
# (shoot_ingame.mjs). Run last: python3 make_sheets.py
import json, os
import numpy as np
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
INK = (43, 30, 22); BG = (0xFD, 0xE6, 0xC8)
CP = json.load(open('crop_points.json')); IR = json.load(open('ingame_report.json'))

def label(im, text, xy=(8, 6)):
    d = ImageDraw.Draw(im); d.rectangle((xy[0] - 4, xy[1] - 2, xy[0] + 7 * len(text), xy[1] + 14), fill=(255, 248, 238)); d.text(xy, text, fill=INK); return im

# ---- variants.png: the 3 variants side by side (Blender, same 3/4 camera)
tiles = [Image.open('_var-%s.png' % v).convert('RGB') for v in ('tie', 'glasses', 'headset')]
W = Image.new('RGB', (sum(t.width for t in tiles), tiles[0].height), BG)
for i, t in enumerate(tiles): W.paste(t, (i * t.width, 0)); label(W, ['tie', 'glasses', 'headset'][i], (i * t.width + 12, 10))
W.save('variants.png')

# ---- compare-ingame.png: Blender | three.js | |difference| x4, plus the numbers
rep = {}
for b, g, out in (('turn-34.png', 'ingame.png', 'compare-ingame.png'), ('turn-front.png', 'ingame-front.png', 'compare-ingame-front.png')):
    A = np.asarray(Image.open(b).convert('RGB')).astype(int); B = np.asarray(Image.open(g).convert('RGB')).astype(int)
    D = np.abs(A - B).max(axis=2)
    rep[g[:-4]] = {'mean': round(float(D.mean()), 2), 'pct_over_40': round(float((D > 40).mean() * 100), 2)}
    dimg = Image.fromarray(np.clip(255 - D * 4, 0, 255).astype(np.uint8)).convert('RGB')
    W = Image.new('RGB', (A.shape[1] * 3 + 16, A.shape[0]), 'white')
    for i, im in enumerate([Image.open(b).convert('RGB'), Image.open(g).convert('RGB'), dimg]): W.paste(im, (i * (A.shape[1] + 8), 0))
    label(W, 'Blender EEVEE (%s)' % b, (12, 10)); label(W, 'three.js r170 (%s)' % g, (A.shape[1] + 20, 10))
    label(W, '|difference| x4 (white = same). mean %.2f / 255, %.2f%% px > 40' % (rep[g[:-4]]['mean'], rep[g[:-4]]['pct_over_40']), (2 * A.shape[1] + 28, 10))
    W.save(out)
json.dump(rep, open('compare_report.json', 'w'), indent=1)

# ---- lineup greyscale (Lena's gate: luminance, the same formula as grey.png) + 3x crops
def grey(src, dst):
    p = np.asarray(Image.open(src).convert('RGB')).astype(float) / 255
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    Image.fromarray((s * 255).round().astype(np.uint8)).save(dst)
for g in ('grass', 'path'):
    grey('lineup-%s.png' % g, 'lineup-%s-grey.png' % g)
    info = IR['lineup-' + g]; xs = [info['kitTop'][0], info['ghostTop'][0]]
    x0, x1 = min(xs) - 40, max(xs) + 60; cx, cy = (x0 + x1) // 2, info['kitTop'][1] + 30
    box = (cx - 150, cy - 70, cx + 150, cy + 70)
    for suf in ('', '-grey'):
        Image.open('lineup-%s%s.png' % (g, suf)).crop(box).resize((900, 420), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf))

# ---- evidence crops (2x nearest) at the points projected by render_ghostie.py (v6 keys)
os.makedirs('crops', exist_ok=True)
def crop(view, key, half, out, scale=2, src=None, dy=0):
    x, y = CP[view][key]; y += dy; im = Image.open((src or view) + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('_close-front', 'eyeR', 70, 'eye-on-surface-front')
crop('_close-front', 'bridge', 170, 'glasses-on-surface-front', scale=1)
crop('_close-headset', 'cup', 120, 'headset-cup-on-surface')
crop('_close-headset', 'crown', 140, 'headset-band-over-crown', dy=60)
crop('front-headset', 'crown', 90, 'headset-band-front', dy=40)
crop('_close-tie', 'tie', 150, 'tie-on-surface', scale=1)
crop('turn-side', 'tie', 60, 'tie-side-profile')
crop('turn-front', 'tipL', 110, 'arm-root-front')
crop('turn-front', 'tipR', 110, 'arm-root-front-R')
crop('turn-back', 'tipR', 110, 'arm-root-back')
crop('turn-34', 'tipR', 90, 'far-arm-nub-34')
crop('turn-34', 'tipL', 110, 'near-arm-34')
crop('turn-side', 'tipL', 110, 'arm-end-on-side')
crop('_close-wave', 'tipL', 220, 'arm-wave-blender', scale=1)
crop('rest-front', 'tipR', 110, 'arm-rest-droop')
Image.open('_close-under.png').convert('RGB').crop((0, 500, 1200, 900)).save('crops/hem-under.png')
Image.open('turn-front.png').convert('RGB').crop((100, 230, 800, 470)).resize((1400, 480), Image.NEAREST).save('crops/dome-front-x2.png')
Image.open('turn-34.png').convert('RGB').crop((100, 230, 800, 470)).resize((1400, 480), Image.NEAREST).save('crops/dome-34-x2.png')
Image.open('turn-back.png').convert('RGB').crop((100, 760, 800, 900)).resize((1400, 280), Image.NEAREST).save('crops/hem-back-x2.png')
Image.open('turn-front.png').convert('RGB').crop((100, 760, 800, 900)).resize((1400, 280), Image.NEAREST).save('crops/hem-front-x2.png')
Image.open('_ingame-wave.png').convert('RGB').save('crops/arm-wave-threejs.png')
crop('turn-34', 'eyeL', 60, 'eye-far-34')
print('sheets ok', rep)
# ---- v4: tie next to Kit's tie (same pixel scale per metre is not the point; the read of knot + blade + point is)
kit = Image.open('../../kit/turn-34.png').convert('RGB').crop((300, 500, 460, 720)).resize((320, 440), Image.LANCZOS)
tx, ty = CP['hero']['tie']; gh = Image.open('hero.png').convert('RGB').crop((tx - 170, ty - 240, tx + 170, ty + 240)).resize((312, 440), Image.LANCZOS)
W = Image.new('RGB', (320 + 312 + 24, 470), 'white'); W.paste(kit, (0, 30)); W.paste(gh, (344, 30))
label(W, "Kit (assets/kit/turn-34.png)", (8, 8)); label(W, 'Ghostie v6 (hero.png)', (352, 8))
W.save('crops/tie-vs-kit.png'); print('tie-vs-kit ok')

# ---- 1x crops (as the player sees them) and the card-size front strip
for g in ('grass', 'path'):
    info = IR['lineup-' + g]; xs = [info['kitTop'][0], info['ghostTop'][0]]
    x0, x1 = min(xs) - 40, max(xs) + 60; cx, cy = (x0 + x1) // 2, info['kitTop'][1] + 30
    Image.open('lineup-%s.png' % g).crop((cx - 150, cy - 70, cx + 150, cy + 70)).save('lineup-%s-crop-1x.png' % g)
tiles = [Image.open('front-%s.png' % v).convert('RGB') for v in ('tie', 'glasses', 'headset')]
W = Image.new('RGB', (sum(t.width for t in tiles), tiles[0].height), BG)
for i, t in enumerate(tiles): W.paste(t, (i * t.width, 0)); label(W, ['tie', 'glasses', 'headset'][i] + ' (front)', (i * t.width + 12, 10))
W.save('front-variants.png'); print('front strip ok')

# ---- 1x crops of the wave lineups and a 9x crop of each ghost at the game camera
for g in ('grass',):
    info = IR['lineup-' + g]; xs = [info['kitTop'][0], info['ghostTop'][0]]
    x0, x1 = min(xs) - 40, max(xs) + 60; cx, cy = (x0 + x1) // 2, info['kitTop'][1] + 30
    for suf in ('-wave40',):
        Image.open('lineup-%s%s.png' % (g, suf)).crop((cx - 150, cy - 70, cx + 150, cy + 70)).resize((900, 420), Image.NEAREST).save('lineup-%s%s-crop-x3.png' % (g, suf))
for i, e in enumerate(IR['lineup-grass']['eyeVsArm']):
    x, y = round((e['tipL'][0] + e['tipR'][0]) / 2), round(e['eyeCentreY'])
    Image.open('lineup-grass.png').convert('RGB').crop((x - 25, y - 22, x + 25, y + 28)).resize((450, 450), Image.NEAREST).save('crops/gamecam-%s-x9.png' % e['ghost'])
    Image.open('lineup-grass-wave40.png').convert('RGB').crop((x - 25, y - 22, x + 25, y + 28)).resize((450, 450), Image.NEAREST).save('crops/gamecam-%s-wave40-x9.png' % e['ghost'])

# ---- compare-sketch.png: each sheet view next to the matching 3D view (checklist S1)
SK = Image.open('../sketch/ghostie-sheet.png').convert('RGB'); s_ = 1.1754
pairs = [('front', (25, 150, 370, 580), 'turn-front'), ('3/4', (420, 150, 770, 580), 'turn-34'), ('side', (815, 150, 1110, 580), 'turn-side'),
         ('back', (1200, 150, 1560, 580), 'turn-back'), ('tie', (25, 720, 310, 1060), 'front-tie'), ('glasses', (350, 720, 630, 1060), 'front-glasses'),
         ('headset', (675, 720, 955, 1060), 'front-headset'), ('wave +40', (1100, 720, 1400, 1060), 'wave-40-front'), ('rest pose', (1560, 720, 1850, 1060), 'rest-front')]
TW, TH = 360, 440
W = Image.new('RGB', (TW * 2 * 3 + 40, (TH + 30) * 3 + 10), 'white')
for i, (nm, box, r3) in enumerate(pairs):
    a = SK.crop(tuple(int(v * s_) for v in box)); a.thumbnail((TW, TH))
    b = Image.open(r3 + '.png').convert('RGB'); bw, bh = b.size
    b = b.crop((int(bw * 0.06), int(bh * 0.15), int(bw * 0.94), int(bh * 0.80)) if bw == 900 else (int(bw * 0.06), int(bh * 0.13), int(bw * 0.94), int(bh * 0.78))); b.thumbnail((TW, TH))
    cx, cy = (i % 3) * (2 * TW + 20), (i // 3) * (TH + 30) + 24
    W.paste(a, (cx, cy)); W.paste(b, (cx + TW, cy)); label(W, '%s: sketch | 3D (%s.png)' % (nm, r3), (cx + 8, cy - 20))
W.save('compare-sketch.png'); print('compare-sketch ok')
