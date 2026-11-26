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
