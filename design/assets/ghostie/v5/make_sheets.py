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

# ---- evidence crops (2x nearest) at the join points projected by render_ghostie.py
os.makedirs('crops', exist_ok=True)
def crop(view, key, half, out, scale=2, src=None, dy=0):
    x, y = CP[view][key]; y += dy; im = Image.open((src or view) + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((2 * half * scale, 2 * half * scale), Image.NEAREST).save('crops/' + out + '.png')
crop('_close-front', 'eyeR', 70, 'eye-on-surface-front')
crop('_close-front', 'bridge', 150, 'glasses-on-surface-front', scale=1)
crop('_close-headset', 'cup', 110, 'headset-cup-on-surface')
crop('_close-headset', 'crown', 110, 'headset-band-over-crown', dy=40)
crop('_close-tie', 'tie', 90, 'tie-on-surface')
crop('turn-side', 'tie', 50, 'tie-side-profile')
Image.open('_close-under.png').convert('RGB').crop((0, 500, 1200, 900)).save('crops/hem-thickness-under.png')
crop('turn-34', 'hem_notch', 80, 'hem-notch-34')
crop('turn-front', 'armL', 70, 'arm-root-front')
crop('turn-back', 'armR', 70, 'arm-root-back')
crop('turn-side', 'armL', 70, 'arm-end-on-side')
crop('_close-wave', 'armL', 140, 'arm-wave-blender', scale=1)
Image.open('_ingame-wave.png').convert('RGB').save('crops/arm-wave-threejs.png')
crop('turn-34', 'eyeL', 60, 'eye-far-34')
print('sheets ok', rep)
# ---- v4: tie next to Kit's tie (same pixel scale per metre is not the point; the read of knot + blade + point is)
kit = Image.open('../kit/turn-34.png').convert('RGB').crop((300, 500, 460, 720)).resize((320, 440), Image.LANCZOS)
tx, ty = CP['hero']['tie']; gh = Image.open('hero.png').convert('RGB').crop((tx - 170, ty - 240, tx + 170, ty + 240)).resize((312, 440), Image.LANCZOS)
W = Image.new('RGB', (320 + 312 + 24, 470), 'white'); W.paste(kit, (0, 30)); W.paste(gh, (344, 30))
label(W, "Kit (assets/kit/turn-34.png)", (8, 8)); label(W, 'Ghostie v5 (hero.png)', (352, 8))
W.save('crops/tie-vs-kit.png'); print('tie-vs-kit ok')
