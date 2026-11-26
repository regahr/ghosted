# Builds expr-gamecam-strip.png (5 expressions at the 26 m follow camera) and expr-card-strip.png (160 px cards).
# Run after shoot_ingame.mjs and render_kit.py: python3 make_strips.py
import json, os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
E = ['hopeful', 'ghosted', 'rejected', 'focused', 'offer_joy']
r = json.load(open('ingame_report.json'))
S, BG, INK = 3, (0xFB, 0xE7, 0xCC), (43, 30, 22)
tiles = []
for e in E:
    info = r['gamecam_' + e]; im = Image.open('_gc_%s.png' % e).convert('RGB')
    cx, cy = info['cx'], info['cy']; tiles.append(im.crop((cx - 38, cy - 46, cx + 46, cy + 40)))
    os.remove('_gc_%s.png' % e)
tw, th = 84 * S, 86 * S
W = Image.new('RGB', (5 * tw + 4 * 12, th + 120), BG); d = ImageDraw.Draw(W)
for i, c in enumerate(tiles):
    x = i * (tw + 12)
    W.paste(c.resize((tw, th), Image.NEAREST), (x, 0))
    W.paste(c, (x, th + 8))                                   # native pixels, as the player sees them
    d.text((x + 96, th + 30), E[i].replace('_', '-'), fill=INK)
    d.text((x + 96, th + 48), 'top: 3x, left: 1x', fill=INK)
W.save('expr-gamecam-strip.png')
C = 160
W = Image.new('RGB', (C * 5 + 4 * 8, C), (0xFD, 0xE6, 0xC8))
for i, n in enumerate(E):
    W.paste(Image.open('expr-' + n.replace('_', '-') + '.png').convert('RGB').resize((C, C), Image.LANCZOS), (i * (C + 8), 0))
W.save('expr-card-strip.png')
print('strips ok')
for name in ('ingame-world', 'ingame-world-grass'):
    info = r[name]; im = Image.open(name + '.png').convert('RGB'); cx, cy = info['cx'], info['cy']
    im.crop((cx - 70, cy - 60, cx + 70, cy + 60)).resize((420, 360), Image.NEAREST).save(name + '-crop-x3.png')
print('crops ok')

# ---- v4 evidence crops (2x, nearest) for every join the gate checks: crops/*.png
os.makedirs('crops', exist_ok=True)
CP = json.load(open('crop_points.json'))
def crop(view, key, half, out, scale=2, src=None):
    x, y = CP[view][key]; im = Image.open((src or view) + '.png').convert('RGB')
    im.crop((x - half, y - half, x + half, y + half)).resize((4 * half * scale // 2, 4 * half * scale // 2), Image.NEAREST).save('crops/' + out + '.png')
for v, tag in [('turn-front', 'front'), ('turn-back', 'back'), ('turn-side', 'side'), ('turn-34', '34'), ('hero', 'hero')]:
    crop(v, 'grip', 95, 'grip-' + tag)
crop('turn-side', 'sleeveL', 90, 'sleeve-side')
crop('turn-back', 'hems', 110, 'hems-back')
crop('turn-side', 'templeL', 70, 'temple-side')
# the 3/4 silhouette, rows 40-63, at 8x, plus a row report: background gap between leg and case?
sil = Image.open('silhouette-64-34.png').convert('L'); w_, h_ = sil.size
sil.crop((0, 40, w_, 64)).resize((w_ * 8, 24 * 8), Image.NEAREST).save('crops/sil34-rows40-63.png')
rows = {}
for yy in range(48, 63):
    line = ''.join('#' if sil.getpixel((xx, yy)) < 128 else '.' for xx in range(w_))
    runs = [r for r in line.split('.') if r]
    rows[yy] = {'pixels': line, 'dark_runs': len(runs)}
json.dump(rows, open('crops/sil34-rows.json', 'w'), indent=1)
print('crops ok')
# before/after crops at the same window (v2/v3 renders kept in v2/ and v3/)
def compare(view, key, half, files, out, labels):
    x, y = CP[view][key]; tiles = []
    for f in files:
        if os.path.exists(f): tiles.append(Image.open(f).convert('RGB').crop((x - half, y - half, x + half, y + half)).resize((4 * half, 4 * half), Image.NEAREST))
    W = Image.new('RGB', (len(tiles) * (4 * half + 8), 4 * half + 24), 'white'); d = ImageDraw.Draw(W)
    for i, t in enumerate(tiles): W.paste(t, (i * (4 * half + 8), 24)); d.text((i * (4 * half + 8) + 4, 6), labels[i], fill=INK)
    W.save('crops/' + out + '.png')
compare('turn-side', 'sleeveL', 90, ['v2/turn-side.png', 'v3/turn-side.png', 'turn-side.png'], 'sleeve-side-v2-v3-v4', ['v2', 'v3 (cap open)', 'v4'])
compare('turn-side', 'templeL', 70, ['v3/turn-side.png', 'turn-side.png'], 'temple-side-v3-v4', ['v3', 'v4'])
for v, tag in [('turn-front', 'front'), ('turn-back', 'back'), ('turn-side', 'side'), ('hero', 'hero')]:
    compare(v, 'grip', 95, ['v3/' + v + '.png', v + '.png'], 'grip-%s-v3-v4' % tag, ['v3 (v3 grip position)', 'v4'])
print('compare crops ok')
# ---- v5 (arm fix) proof crops
def arm_compare(view, tag):
    (x1, y1), (x2, y2) = CP[view]['sleeveL'], CP[view]['grip']
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 + 40; half = 170
    tiles = [Image.open(f).convert('RGB').crop((cx - half, cy - half, cx + half, cy + half)).resize((2 * half * 2 // 2 * 1, 2 * half), Image.NEAREST) for f in ('v4/%s.png' % view, '%s.png' % view)]
    W = Image.new('RGB', (2 * (2 * half) + 8, 2 * half + 24), 'white'); d = ImageDraw.Draw(W)
    for i, t in enumerate(tiles): W.paste(t, (i * (2 * half + 8), 24)); d.text((i * (2 * half + 8) + 4, 6), ['v4', 'v5'][i] + ' ' + view, fill=INK)
    W.save('crops/arm-%s-v4-v5.png' % tag)
arm_compare('turn-front', 'front'); arm_compare('turn-back', 'back')
for v, tag in [('turn-front', 'front'), ('turn-back', 'back'), ('turn-side', 'side'), ('turn-34', '34'), ('hero', 'hero')]:
    crop(v, 'grip', 95, 'grip-%s-v5' % tag)
sil.crop((0, 40, w_, 64)).resize((w_ * 8, 24 * 8), Image.NEAREST).save('crops/sil34-rows-v5.png')
print('v5 crops ok')
