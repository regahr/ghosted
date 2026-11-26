# S1 proof: draws the sketch's FRONT_BODY outline (blue) over the Blender front render, projected through the same camera.
import math, sys, os, re
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sketch', 'src'))
import ghost as G
U = 0.47 / 265; FLOAT = 0.22
def zf(y): return (316 - y) * U
C = (0, -2.7, 0.62); T = (0, 0, 0.40)
f = [T[i] - C[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)); f = [v / n for v in f]
up = (0, 0, 1); r = [f[1] * up[2] - f[2] * up[1], f[2] * up[0] - f[0] * up[2], f[0] * up[1] - f[1] * up[0]]
n = math.sqrt(sum(v * v for v in r)); r = [v / n for v in r]
u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
def proj(x, y, W=900, Hh=1200, fov=22):
    P = ((x - 150) * U, 0.0, zf(y) + FLOAT); d = [P[i] - C[i] for i in range(3)]
    xc = sum(d[i] * r[i] for i in range(3)); yc = sum(d[i] * u[i] for i in range(3)); zc = sum(d[i] * f[i] for i in range(3))
    t = math.tan(math.radians(fov) / 2); return (W / 2 * (1 + xc / (zc * t * W / Hh)), Hh / 2 * (1 - yc / (zc * t)))
def pts(d):
    toks = re.findall(r'[MCLZ]|-?\d+(?:\.\d+)?', d); out = []; cur = None; i = 0; cmd = None
    while i < len(toks):
        tk = toks[i]
        if tk in 'MCLZ': cmd = tk; i += 1; continue
        if cmd == 'M': cur = (float(tk), float(toks[i + 1])); out.append(cur); i += 2
        elif cmd == 'C':
            p = [(float(toks[i + k]), float(toks[i + k + 1])) for k in (0, 2, 4)]
            for s in range(1, 21):
                t_ = s / 20; a, b, c, e = (1 - t_) ** 3, 3 * t_ * (1 - t_) ** 2, 3 * t_ * t_ * (1 - t_), t_ ** 3
                out.append((a * cur[0] + b * p[0][0] + c * p[1][0] + e * p[2][0], a * cur[1] + b * p[0][1] + c * p[1][1] + e * p[2][1]))
            cur = p[2]; i += 6
    return out
for src, path, out in (('turn-front.png', G.FRONT_BODY, 'crops/overlay-sketch-front.png'), ('wave-40-front.png', G.FRONT_WAVE, 'crops/overlay-sketch-wave.png')):
    im = Image.open(src).convert('RGB'); dr = ImageDraw.Draw(im)
    P = [proj(*p) for p in pts(path)]; dr.line(P + [P[0]], fill=(29, 99, 200), width=2)
    for (ex, ey) in G.EYES: q = proj(ex, ey); dr.ellipse((q[0] - 3, q[1] - 3, q[0] + 3, q[1] + 3), outline=(29, 99, 200), width=2)
    im.crop((60, 180, 840, 980)).save(out)
print('overlay ok')
