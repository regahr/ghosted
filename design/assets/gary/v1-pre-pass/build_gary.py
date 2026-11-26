# GHOSTED - Gary the pigeon postman v1, built to the accepted sketch (assets/gary/sketch, direction A).
# Pipeline = Panel v1 (Blender build -> glb -> ingame.html in three.js).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_gary.py -- [blockout]
# Numbers come from the sketch model (../sketch/src/gary.py, body-map.md): 1 u = 2.2929 mm (sketch build.py M_PER_U).
# World u: X right (+X = his LEFT), H up, Z toward the viewer (his front). Blender: (X, -Z, H) * U. glTF: Y up, +Z front.
# Meshes (3 non-swap): body, wing_L, wing_R. Swaps: eyes, brows, envelope (beak / wing), bag flap (closed / open).
# Joins and hardest parts: direction.md.
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import gary as G
from ricky import path_points
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
OUT = os.path.join(HERE, 'blockout') if BLOCKOUT else HERE
NAME = 'gary_blockout' if BLOCKOUT else 'gary'
U = 0.0022928883107889452
PI = math.pi
ROW = G.ROW
PAL = {'body': ROW[8], 'wing': ROW[9], 'cap': ROW[26], 'gold': ROW[13], 'bag': ROW[5], 'strap': ROW[5],
       'ink': ROW[22], 'cream': ROW[23], 'stamp': ROW[7]}
BASIC = ['ink', 'cream', 'stamp']
NEUTRAL = [[-1.0, [217, 217, 217]], [0.0001, [255, 255, 255]]]      # shade = base x 0.85 (sketch notes)
TOONJ = {'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC,
         'contact_shadow': {'rx': 0.16, 'ry': 0.13, 'opacity': 0.25}}

def s2l(h):
    h = h.lstrip('#'); out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255; out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene; COL = scn.collection
MATS = {}
def mat(name):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*s2l(PAL[name]), 1); b.inputs['Roughness'].default_value = 0.8
    m['hex'] = PAL[name]; MATS[name] = m; return m

def BV(p): return Vector((p[0] * U, -p[2] * U, p[1] * U))      # world u point -> Blender m
def BD(v): return Vector((v[0], -v[2], v[1]))                   # world u direction -> Blender
BDM = Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0)))                # u -> Blender (proper rotation)

# ---------------------------------------------------------------- vector helpers (u space)
def add(a, b, k=1.0): return (a[0] + k * b[0], a[1] + k * b[1], a[2] + k * b[2])
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def nrm(v): l = math.sqrt(sum(c * c for c in v)) or 1.0; return tuple(c / l for c in v)
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def dotp(a, b): return sum(x * y for x, y in zip(a, b))
def basis(ex, ey_hint):
    ex = nrm(ex); ey = nrm(add(ey_hint, ex, -dotp(ey_hint, ex))); return ex, ey, cross(ex, ey)
def bmat(B): return Matrix(((B[0][0], B[1][0], B[2][0]), (B[0][1], B[1][1], B[2][1]), (B[0][2], B[1][2], B[2][2])))
def brot(B):
    ex, ey, ez = B
    return lambda p: (p[0] * ex[0] + p[1] * ey[0] + p[2] * ez[0], p[0] * ex[1] + p[1] * ey[1] + p[2] * ez[1],
                      p[0] * ex[2] + p[1] * ey[2] + p[2] * ez[2])
def rxf(deg):   # sketch rx: + = the top goes toward the viewer (+Z)
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return lambda p: (p[0], p[1] * c - p[2] * s, p[1] * s + p[2] * c)
def ryf(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return lambda p: (p[0] * c + p[2] * s, p[1], -p[0] * s + p[2] * c)
def about(f, piv): return lambda p: add(f(sub(p, piv)), piv)
def chain(*fs):
    def g(p):
        for f in fs: p = f(p)
        return p
    return g
def tr(d): return lambda p: add(p, d)
IDENT = lambda p: p

# ---------------------------------------------------------------- mesh accumulator (= Panel v1)
class Acc:
    def __init__(s, bone): s.V, s.F, s.FM, s.FS, s.VB, s.OW, s.FR, s.bone = [], [], [], [], [], [], [], bone
    def v(s, p, bone=None, ow=1.0):
        s.V.append(tuple(p)); s.VB.append(bone or s.bone); s.OW.append(ow); return len(s.V) - 1
    def f(s, ids, m, smooth=True, ref=None): s.F.append(list(ids)); s.FM.append(m); s.FS.append(smooth); s.FR.append(ref)

def ellipsoid(acc, c, r, cols, lats, m, xf=IDENT, bone=None, rot=None, ow=1.0, smooth=True):
    rings = []
    for i in range(1, lats):
        th = PI * i / lats; ring = []
        for j in range(cols):
            ph = 2 * PI * j / cols
            p = (r[0] * math.sin(th) * math.sin(ph), r[1] * math.cos(th), r[2] * math.sin(th) * math.cos(ph))
            if rot: p = rot(p)
            ring.append(acc.v(xf(add(c, p)), bone, ow))
        rings.append(ring)
    top, bot = (0, r[1], 0), (0, -r[1], 0)
    if rot: top, bot = rot(top), rot(bot)
    pt = acc.v(xf(add(c, top)), bone, ow); pb = acc.v(xf(add(c, bot)), bone, ow)
    n = cols
    for j in range(n): acc.f([pt, rings[0][(j + 1) % n], rings[0][j]][::-1], m, smooth)
    for k in range(len(rings) - 1):
        A, B_ = rings[k], rings[k + 1]
        for j in range(n): acc.f([A[j], B_[j], B_[(j + 1) % n], A[(j + 1) % n]], m, smooth)
    for j in range(n): acc.f([pb, rings[-1][j], rings[-1][(j + 1) % n]][::-1], m, smooth)

def frame(d):
    d = Vector(d).normalized(); up = Vector((0, 1, 0)) if abs(d.y) < 0.9 else Vector((1, 0, 0))
    a = d.cross(up).normalized(); b = a.cross(d).normalized(); return a, b

def tube(acc, pts, radii, sides, m, xf=IDENT, bone=None, cap_end=False, ow=1.0):
    rings = []
    for i, p in enumerate(pts):
        d = Vector(pts[min(i + 1, len(pts) - 1)]) - Vector(pts[max(i - 1, 0)]); a, b = frame(d); ring = []
        for j in range(sides):
            t = 2 * PI * j / sides; q = Vector(p) + (a * math.cos(t) + b * math.sin(t)) * radii[i]
            ring.append(acc.v(xf(tuple(q)), bone, ow))
        rings.append(ring)
    for k in range(len(rings) - 1):
        A, B_ = rings[k], rings[k + 1]
        for j in range(sides): acc.f([A[j], A[(j + 1) % sides], B_[(j + 1) % sides], B_[j]], m)
    if cap_end: acc.f(rings[-1], m, False)

def box(acc, c, size, m, xf=IDENT, bone=None, skip=(), ow=1.0, ref=None):
    x, y, z = c; hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    v = {k: acc.v(xf((x + k[0] * hx, y + k[1] * hy, z + k[2] * hz)), bone, ow)
         for k in [(sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]}
    faces = {'top': [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)], 'bottom': [(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)],
             'front': [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)], 'back': [(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)],
             'right': [(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)], 'left': [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)]}
    for k, f in faces.items():
        if k not in skip: acc.f([v[q] for q in f], m, False, ref)

def revolved(acc, prof, cols, m, xf=IDENT, bone=None, ow=1.0, close_bottom=True):
    """prof: [(H, r)] top to bottom; the first r may be 0 (a top pole)."""
    rings = []
    for h, r in prof:
        if r < 1e-6: rings.append([acc.v(xf((0, h, 0)), bone, ow)]); continue
        rings.append([acc.v(xf((r * math.sin(2 * PI * j / cols), h, r * math.cos(2 * PI * j / cols))), bone, ow) for j in range(cols)])
    for k in range(len(rings) - 1):
        A, B_ = rings[k], rings[k + 1]
        if len(A) == 1:
            for j in range(cols): acc.f([A[0], B_[j], B_[(j + 1) % cols]], m)
        else:
            for j in range(cols): acc.f([A[j], B_[j], B_[(j + 1) % cols], A[(j + 1) % cols]], m)
    if close_bottom: acc.f(rings[-1][::-1], m, False)

# ---------------------------------------------------------------- the sketch numbers
BODY_C, BODY_R, BODY_TILT = G.BODY_C, G.BODY_R, G.BODY_TILT
HEAD_C, HEAD_R, HEAD_D = G.HEAD_C, G.HEAD_R, 0.95
HEAD_RR = (HEAD_R, HEAD_R, HEAD_R * HEAD_D)
NECK_PIV = (0.0, float(G.LM['neck']), 10.0)
BODY_PIV = (0.0, 90.0, 0.0)
EYE_K = 1.15                     # chair call 3: eyes 15 % bigger
BROW_LIFT = 2.0                  # the bigger eyes reach 1 u under the sketch brows: brows 2 u up

def body_surface(d, out=0.0):
    inv = rxf(-BODY_TILT); lx, ly, lz = inv(d); r = BODY_R
    k = math.sqrt((lx / r[0]) ** 2 + (ly / r[1]) ** 2 + (lz / r[2]) ** 2)
    loc = (lx / k, ly / k, lz / k)
    n = nrm(rxf(BODY_TILT)((loc[0] / r[0] ** 2, loc[1] / r[1] ** 2, loc[2] / r[2] ** 2)))
    p = rxf(BODY_TILT)(loc)
    return add(add(BODY_C, p), n, out), n

def head_proj(x, y, off):
    """front-frame face mark (x, y) -> a point on the head ball, pushed out along the normal."""
    X = x - 150.0; H = 340.0 - y
    rx, ry, rz = HEAD_RR
    q = 1 - (X / rx) ** 2 - ((H - HEAD_C[1]) / ry) ** 2
    zz = rz * math.sqrt(max(q, 0.0))
    n = nrm((X / rx ** 2, (H - HEAD_C[1]) / ry ** 2, zz / rz ** 2))
    return add((X, H, HEAD_C[2] + zz), n, off)

def subpaths(d): return ['M' + s for s in d.split('M') if s.strip()]
def fill_pts(acc, pts, m, proj, off, xf, bone):
    if len(pts) > 2 and math.dist(pts[0], pts[-1]) < 0.01: pts = pts[:-1]
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    c = acc.v(xf(proj(cx, cy, off)), bone, 0.0); ids = [acc.v(xf(proj(x, y, off)), bone, 0.0) for x, y in pts]
    ref = xf(proj(cx, cy, off - 10))
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    for i in range(len(ids)):
        tri = [c, ids[i], ids[(i + 1) % len(ids)]]; acc.f(tri, m, True, ref)
def fill(acc, d, m, proj, off, xf=IDENT, bone=None, n=3):
    for sp in subpaths(d): fill_pts(acc, path_points(sp, n), m, proj, off, xf, bone)
def line(acc, d, w, m, proj, off, xf=IDENT, bone=None, n=3):
    for sp in subpaths(d):
        pts = path_points(sp, n); Lp, Rp = [], []
        for i, p in enumerate(pts):
            a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1; nx, ny = -dy / l * w / 2, dx / l * w / 2
            Lp.append(acc.v(xf(proj(p[0] + nx, p[1] + ny, off)), bone, 0.0)); Rp.append(acc.v(xf(proj(p[0] - nx, p[1] - ny, off)), bone, 0.0))
        ref = xf(proj(pts[len(pts) // 2][0], pts[len(pts) // 2][1], off - 10))
        for i in range(len(pts) - 1): acc.f([Lp[i], Lp[i + 1], Rp[i + 1], Rp[i]], m, True, ref)
def ovalpts(x, y, rx, ry, n=12): return [(x + rx * math.sin(2 * PI * k / n), y - ry * math.cos(2 * PI * k / n)) for k in range(n)]
def scale_path(d, cx, cy, k, dy=0.0):
    import re
    out, i = [], 0
    for t in re.split(r'([ ,MCLZ])', d):
        if re.fullmatch(r'-?\d+(\.\d+)?', t or ''):
            v = float(t); out.append('%g' % ((cx + (v - cx) * k) if i % 2 == 0 else (cy + (v - cy) * k + dy))); i += 1
        else: out.append(t)
    return ''.join(out)

NC = 8 if BLOCKOUT else 12
# ================================================================ BODY mesh (bones: body, head, leg_L, leg_R)
BODY = Acc('torso')
ellipsoid(BODY, BODY_C, BODY_R, 10 if not BLOCKOUT else 8, 8 if not BLOCKOUT else 5, 'body', rot=rxf(BODY_TILT))
# tail: a flat fan low at the back, sunk into the egg (sketch: (0, H 56, Z -82), r (30, 7, 34), tilt -18)
ellipsoid(BODY, (0, BODY_C[1] - 22, BODY_C[2] - BODY_R[2] - 8), (30, 7, 34), 6, 4, 'wing', rot=rxf(-18))
# neck blend (no ink at the front, so no collar line): fills the gap under the back of the head
n0 = len(BODY.V)
ellipsoid(BODY, (0, 136, -6), (27, 20, 26), 6, 3, 'body', bone='head')
for i in range(n0, len(BODY.V)): BODY.OW[i] = 1.0 if BODY.V[i][2] < -8 else 0.0
# head ball: the ink fades out under the chin (no neck line, sketch)
h0 = len(BODY.V)
ellipsoid(BODY, HEAD_C, HEAD_RR, 10 if not BLOCKOUT else 8, 8 if not BLOCKOUT else 4, 'body', bone='head')
for i in range(h0, len(BODY.V)):
    H, Z = BODY.V[i][1], BODY.V[i][2]
    t = min(max((H - 128.0) / 16.0, 0.0), 1.0); BODY.OW[i] = 1.0 if Z < -10 else t
# beak: a 6-sided gold cone from the face, forward and down; cere = a cream decal fan on top
HZ = HEAD_C[2] + HEAD_RR[2]
tube(BODY, [(0, 150, HZ - 6), (0, 144, HZ + 12), (0, 137, HZ + 28)], [8.5, 5.6, 0.8], 6, 'gold', bone='head', cap_end=True)
fill_pts(BODY, ovalpts(150, 340 - 155.5, 5.0, 2.6, 6), 'cream', head_proj, 1.2, IDENT, 'head')
# cap (kepi): set back on the crown, band bottom 10 u under the head top, tilted back 14 deg about that point
TOP = HEAD_C[1] + HEAD_R
CAP_PIV = (0, TOP - 10, HEAD_C[2])
capf = chain(about(rxf(-14), CAP_PIV))
CAP_PROF = [(340 - 131.0 + 0.0, 0.0), (340 - 131.5, 26.0), (340 - 134.0, 33.5), (340 - 140.0, 33.0), (340 - 152.0, 28.0)]
revolved(BODY, CAP_PROF, 10, 'cap', chain(tr((0, 0, HEAD_C[2])), capf), 'head')
ellipsoid(BODY, (0, TOP - 10 + 1.5, HEAD_C[2] + 27), (21, 2.6, 12), 8, 2, 'ink', capf, 'head', rot=rxf(-6))
def cap_front(x, y, off):   # a point on the cap band front (front frame), before the tilt
    H = 340 - y; X = x - 150; r = 31.5
    return (X, H, HEAD_C[2] + math.sqrt(max(r * r - X * X, 0)) + off)
fill_pts(BODY, ovalpts(150, 340 - (TOP - 10 + 11), 6.5, 4.6, 8), 'cream', cap_front, 2.0, capf, 'head')
# legs and feet (gold), rigid on the leg bones (bind = stand)
for s, side in ((-1, 'R'), (1, 'L')):
    tube(BODY, [(s * 17, 34, 6), (s * 17, 5, 10)], [3.8, 3.4], 5, 'gold', bone='leg_' + side)
    ellipsoid(BODY, (s * 17, 4, 17), (8.5, 3.6, 12), 6, 2, 'gold', bone='leg_' + side)
# mail bag on his LEFT belly front (box in the body mesh; the flap is a swap)
BAG_P, _ = body_surface(nrm((0.42, -0.42, 0.80)), 9)
bagf = chain(ryf(24), tr(BAG_P))
box(BODY, (0, 0, 0), (38, 30, 15), 'bag', bagf, 'torso')
# strap: a sash ribbon on the body, no ink hull (hardest part 2: it crosses his left side at the wing line, not low)
KEYS = [(-0.55, 0.85, 0.0), (-0.28, 0.55, 0.80), (0.12, 0.22, 0.97), (0.40, -0.05, 0.92), (0.97, 0.05, 0.25),
        (0.80, 0.12, -0.60), (0.05, 0.42, -0.90), (-0.45, 0.80, -0.40)]
def crom(P, t):
    n = len(P); i = int(math.floor(t)) % n; u = t - math.floor(t)
    p0, p1, p2, p3 = P[(i - 1) % n], P[i], P[(i + 1) % n], P[(i + 2) % n]
    return tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u * u +
                        (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u ** 3) for k in range(3))
NS = 20
SP = [body_surface(nrm(crom(KEYS, len(KEYS) * k / NS)), 1.6) for k in range(NS)]
Lr, Rr = [], []
for k in range(NS):
    p, n = SP[k]; tng = nrm(sub(SP[(k + 1) % NS][0], SP[(k - 1) % NS][0])); side = nrm(cross(n, tng))
    Lr.append(BODY.v(add(p, side, 2.7), 'torso', 0.0)); Rr.append(BODY.v(add(p, side, -2.7), 'torso', 0.0))
for k in range(NS):
    j = (k + 1) % NS; BODY.f([Lr[k], Rr[k], Rr[j], Lr[j]], 'strap', True, add(SP[k][0], SP[k][1], -10))
STRAP_SIDE = [p for p, _ in SP]

# ================================================================ WINGS (bind = spread, flap 0): arm + hand + 3 feathers
ARM, HAND = G.WING_ARM, G.WING_HAND
ROOT = {s: (s * 42.0, 104.0, -10.0) for s in (-1, 1)}
WINGS = {}
def wing_geo(s):
    acc = Acc('wing_%s_up' % ('L' if s > 0 else 'R')); lo = 'wing_%s_lo' % ('L' if s > 0 else 'R')
    root = ROOT[s]; da = (s * 1.0, 0.0, 0.0); B = basis(da, (0, 1, 0))
    wrist = add(root, da, ARM); tip = add(wrist, da, HAND)
    c8, l3 = (6, 3) if BLOCKOUT else (8, 3)
    ellipsoid(acc, add(root, da, ARM / 2), (ARM / 2 + 8, 6.5, 19), c8, l3, 'wing', rot=brot(B), bone=acc.bone)
    ellipsoid(acc, add(wrist, da, HAND / 2 - 6), (HAND / 2 + 2, 5.5, 16), c8, l3, 'wing', rot=brot(B), bone=lo)
    for ang in (-24, 0, 24):
        a = math.radians(ang); d = nrm(add(tuple(c * math.cos(a) for c in B[0]), tuple(c * math.sin(a) for c in B[2])))
        ellipsoid(acc, add(add(tip, da, -12), d, 12), (13, 4.2, 6.5), 6, 2, 'wing', rot=brot(basis(d, B[1])), bone=lo)
    WINGS[s] = {'acc': acc, 'root': root, 'wrist': wrist, 'tip': tip, 'B': B, 'up': acc.bone, 'lo': lo}
for s in (-1, 1): wing_geo(s)

# ---- wing poses: target bases (u space) -> bone rotations (Blender float space; = Panel v1 storage)
def rot_u(Bt, Bb): return bmat(Bt) @ bmat(Bb).transposed()
def to_bl(R): return BDM @ R @ BDM.transposed()
def aa(R): q = R.to_quaternion(); return [*q.axis, math.degrees(q.angle)] if q.angle > 1e-6 else [1.0, 0.0, 0.0, 0.0]
def wing_pose(s, da, th_a, dh, th_h):
    W = WINGS[s]; Bb = W['B']
    Ba, Bh = basis(da, th_a), basis(dh, th_h)
    R1 = rot_u(Ba, Bb); Rh = rot_u(Bh, Bb)
    R2w = Rh @ R1.inverted()
    q1 = to_bl(R1).to_quaternion(); q2 = to_bl(R2w).to_quaternion()
    ax2 = to_bl(R1).inverted() @ q2.axis
    wrist = add(W['root'], nrm(da), ARM)
    pose = {W['up']: [*q1.axis, math.degrees(q1.angle)], W['lo']: [*ax2, math.degrees(q2.angle)]}
    return pose, {'R1': R1, 'Rh': Rh, 'wrist': wrist, 'tip': add(wrist, nrm(dh), HAND), 'dh': nrm(dh)}
def spread(s, flap):
    a = math.radians(flap); d = (s * math.cos(a), math.sin(a), -0.12); th = (-s * math.sin(a), math.cos(a), 0.0)
    return wing_pose(s, d, th, d, th)
FOLD_OUT = 11.0
def fold(s):
    # hardest part 1: tucked back and in. The arm runs forward-down from a root 10 u behind the body centre, the hand
    # lies back along it; both lie flat on the body side (thickness axis = the body normal), so from the front only a
    # thin blue edge shows inside the body outline.
    root = ROOT[s]
    wt, _ = body_surface(nrm((s * 0.66, -0.12, 0.58)), FOLD_OUT)
    da = nrm(sub(wt, root)); wrist = add(root, da, ARM)
    tt, _ = body_surface(nrm((s * 0.58, -0.28, -0.76)), FOLD_OUT)
    dh = nrm(sub(tt, wrist))
    _, na = body_surface(nrm(sub(add(root, da, ARM / 2), BODY_C)))
    _, nh = body_surface(nrm(sub(add(wrist, dh, HAND / 2), BODY_C)))
    return wing_pose(s, da, na, dh, nh)
def hold(s):   # his right wing reaches forward; the finger feathers hold the letter in front of the chest (sketch)
    return wing_pose(s, nrm((s * 0.20, 0.02, 0.98)), (s * 1.0, 0.0, 0.0), nrm((-s * 0.92, -0.12, 0.38)), (0.0, 1.0, 0.0))

WP = {}
for s in (-1, 1):
    side = 'L' if s > 0 else 'R'
    for nm, fn in (('fold', lambda s=s: fold(s)), ('up', lambda s=s: spread(s, 50)), ('level', lambda s=s: spread(s, 5)),
                   ('down', lambda s=s: spread(s, -35)), ('half', lambda s=s: spread(s, 30)), ('cheer', lambda s=s: spread(s, 55))):
        WP[(side, nm)] = fn()
    if s < 0: WP[('R', 'hold')] = hold(s)

# ---- legs: tucked in flight (sketch: hip -> foot back and up)
def leg_rot(s):
    v1 = BD(sub((s * 17, 5, 10), (s * 17, 34, 6))); v2 = BD(sub((s * 15, 24, -24), (s * 15, 34, -4)))
    q = v1.rotation_difference(v2); return [*q.axis, math.degrees(q.angle)]
LEGT = {'leg_L': leg_rot(1), 'leg_R': leg_rot(-1)}

# ================================================================ SWAPS
SWAP = {}
def sw(k, bone): a = Acc(bone); SWAP[k] = a; return a
EY = G.EYE_Y
ER = (6.5 * EYE_K, 8.5 * EYE_K)
def eyes(acc, er):
    for x in G.EYE_X:
        fill_pts(acc, ovalpts(x, EY, *er), 'ink', head_proj, 0.8, IDENT, 'head')
        fill_pts(acc, ovalpts(x + 2 * EYE_K, EY - 3.2 * EYE_K, 2.0 * EYE_K, 2.4 * EYE_K, 6), 'cream', head_proj, 1.3, IDENT, 'head')
eyes(sw('eyes_open', 'head'), ER)
eyes(sw('eyes_oops', 'head'), (7.5 * EYE_K, 9.5 * EYE_K))
a = sw('eyes_happy', 'head')
for d, x in zip(G.HAPPY_EYES, G.EYE_X): line(a, scale_path(d, x, EY, EYE_K), 3.4 * EYE_K, 'ink', head_proj, 0.8, IDENT, 'head', 3)
a = sw('eyes_sorry', 'head')   # half lids: the eye with its top covered by a body-colour lid and an ink lid line
eyes(a, ER)
for d, x in zip(G.HALF_LIDS, G.EYE_X):
    ld = scale_path(d, x, EY, EYE_K); lp = path_points(ld, 4); ly = sum(p[1] for p in lp) / len(lp)
    top = [p for p in ovalpts(x, EY, ER[0] + 1.0, ER[1] + 1.0, 10) if p[1] < ly]
    top.sort(key=lambda p: p[0])
    fill_pts(a, [(lp[0][0] - 1, ly)] + top + [(lp[-1][0] + 1, ly)], 'body', head_proj, 1.6, IDENT, 'head')
    line(a, ld, 3.0, 'ink', head_proj, 1.9, IDENT, 'head', 3)
for k, br in (('brows_rest', G.BROWS), ('brows_sorry', G.BROWS_SORRY), ('brows_up', G.BROWS_UP)):
    a = sw(k, 'head')
    for d in br: line(a, scale_path(d, 150, 170, 1.0, -BROW_LIFT), 2.6, 'ink', head_proj, 0.9, IDENT, 'head', 3)
EXPR = {'rest': ['eyes_open', 'brows_rest'], 'happy': ['eyes_happy', 'brows_rest'],
        'sorry': ['eyes_sorry', 'brows_sorry'], 'oops': ['eyes_oops', 'brows_up']}

def envelope(acc, xf, bone):
    box(acc, (0, 0, 0), (50, 34, 2.5), 'cream', xf, bone)
    box(acc, (15, 8, 1.6), (11, 12, 1.0), 'stamp', xf, bone, skip=('back', 'bottom', 'top', 'left', 'right'), ow=0.0, ref=xf((15, 8, -5)))
    pts = [(-23, 15), (0, 1), (23, 15)]
    for i in range(2):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]; dx, dy = x1 - x0, y1 - y0; l = math.hypot(dx, dy); nx, ny = -dy / l * 0.9, dx / l * 0.9
        q = [acc.v(xf(p), bone, 0.0) for p in ((x0 + nx, y0 + ny, 1.45), (x1 + nx, y1 + ny, 1.45), (x1 - nx, y1 - ny, 1.45), (x0 - nx, y0 - ny, 1.45))]
        acc.f(q, 'ink', False, xf((0, 8, -5)))
# socket 1: the beak (head bone, bind = rest head)
envelope(sw('env_beak', 'head'), chain(rxf(-35), tr((0, 125, HZ + 30))), 'head')
# socket 2: the right wing fingers in the hold pose, stored in the hand bone's bind space
Hd = WP[('R', 'hold')][1]; W = WINGS[-1]
tipP = add(Hd['tip'], Hd['dh'], 4)
envw = chain(rxf(-38), tr((tipP[0] + 2, tipP[1] + 6, tipP[2] + 6)))
RhT = Hd['Rh'].transposed()
def to_hand_bind(p):
    d = RhT @ Vector(sub(p, Hd['wrist'])); return add(W['wrist'], tuple(d))
envelope(sw('env_wing', W['lo']), chain(envw, to_hand_bind), W['lo'])
# bag flap: closed, or open with a letter showing
box(sw('flap_closed', 'torso'), (0, 8.5, 8.6), (39, 15, 2.2), 'bag', bagf, 'torso')
a = sw('flap_open', 'torso')
box(a, (0, 0, 0), (39, 15, 2.2), 'bag', chain(tr((0, 7.5, 0)), rxf(-110), tr((0, 15, 7.6)), bagf), 'torso')
box(a, (-6, 17, 0), (26, 16, 2), 'cream', bagf, 'torso', skip=('bottom',))

# ================================================================ build meshes (= Panel v1)
def make_mesh(name, acc):
    used = sorted(set(i for f in acc.F for i in f)); remap = {o: n for n, o in enumerate(used)}
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(BV(acc.V[i])) for i in used], [], [[remap[i] for i in f] for f in acc.F])
    names = sorted(set(acc.FM), key=lambda m: list(PAL).index(m))
    for m in names: me.materials.append(mat(m))
    me.polygons.foreach_set('material_index', [names.index(m) for m in acc.FM])
    me.polygons.foreach_set('use_smooth', acc.FS); me.update()
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()   # face i = acc.F[i] (from_pydata order)
    shells = [f for f in bm.faces if acc.FR[f.index] is None]
    bmesh.ops.recalc_face_normals(bm, faces=shells)
    for f in bm.faces:
        r = acc.FR[f.index]
        if r is None: continue
        f.normal_update()
        if f.normal.dot(f.calc_center_median() - BV(r)) < 0: f.normal_flip()
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY')
    bm.to_mesh(me); bm.free()
    me.color_attributes.new('outline_wc', 'FLOAT_COLOR', 'POINT')
    ca = me.color_attributes['outline_wc']
    for nv, ov in enumerate(used): w = acc.OW[ov]; ca.data[nv].color = (w, w, w, 1.0)
    me.update()
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob)
    return ob, used

root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root
arm_d = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm_d); COL.objects.link(rig); rig.parent = flt
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
def eb(name, h, t, parent=None):
    b = arm_d.edit_bones.new(name); b.head = h; b.tail = t
    if parent: b.parent = arm_d.edit_bones[parent]
eb('torso', BV(BODY_PIV), BV((0, 150, 0)))
eb('head', BV(NECK_PIV), BV((0, 200, 10)), 'torso')
for s, side in ((-1, 'R'), (1, 'L')):
    W = WINGS[s]; eb(W['up'], BV(W['root']), BV(W['wrist']), 'torso'); eb(W['lo'], BV(W['wrist']), BV(W['tip']), W['up'])
    eb('leg_' + side, BV((s * 17, 34, 6)), BV((s * 17, 5, 10)), 'torso')
bpy.ops.object.mode_set(mode='OBJECT')
def skin(ob, acc, used):
    ob.parent = rig; mod = ob.modifiers.new('skin', 'ARMATURE'); mod.object = rig; groups = {}
    for nv, ov in enumerate(used):
        bn = acc.VB[ov] or acc.bone
        if bn not in groups: groups[bn] = ob.vertex_groups.new(name=bn)
        groups[bn].add([nv], 1.0, 'REPLACE')
OBJ = {}
for name, acc in [('body', BODY), ('wing_R', WINGS[-1]['acc']), ('wing_L', WINGS[1]['acc'])] + list(SWAP.items()):
    ob, used = make_mesh(name, acc); skin(ob, acc, used); OBJ[name] = ob
    if name in SWAP: ob['variant'] = name

# poses (Blender float space axis + deg; children in the parent's REST frame, = Panel v1)
def wings(l, r): return {**WP[('L', l)][0], **WP[('R', r)][0]}
PITCH = {'torso': [1.0, 0.0, 0.0, 10.0]}        # nose down 10 in flight
TUCK = dict(LEGT)
POSES = {
    'rest': wings('fold', 'fold'),
    'flap_up': {**wings('up', 'up'), **PITCH, **TUCK}, 'flap_level': {**wings('level', 'level'), **PITCH, **TUCK},
    'flap_down': {**wings('down', 'down'), **PITCH, **TUCK},
    'land_hop': wings('half', 'half'),
    'hold': wings('fold', 'hold'),
    'sorry': {**wings('fold', 'hold'), 'head': [0.0, 1.0, 0.0, -14.0]},
    'happy_hop': wings('cheer', 'cheer'),
    'fly_off': {**wings('up', 'up'), **TUCK, **PITCH},
}
# beat defaults: pose, expression, envelope socket, bag flap, lift (u)
BEATS = {
    'rest': {'pose': 'rest', 'expr': 'rest', 'env': None, 'flap': 'flap_closed', 'lift': 0},
    'flap_up': {'pose': 'flap_up', 'expr': 'rest', 'env': 'env_beak', 'flap': 'flap_closed', 'lift': 0},
    'flap_level': {'pose': 'flap_level', 'expr': 'rest', 'env': 'env_beak', 'flap': 'flap_closed', 'lift': 0},
    'flap_down': {'pose': 'flap_down', 'expr': 'rest', 'env': 'env_beak', 'flap': 'flap_closed', 'lift': 0},
    'land_hop': {'pose': 'land_hop', 'expr': 'oops', 'env': 'env_beak', 'flap': 'flap_closed', 'lift': 14},
    'hold': {'pose': 'hold', 'expr': 'rest', 'env': 'env_wing', 'flap': 'flap_open', 'lift': 0},
    'sorry': {'pose': 'sorry', 'expr': 'sorry', 'env': 'env_wing', 'flap': 'flap_open', 'lift': 0},
    'happy_hop': {'pose': 'happy_hop', 'expr': 'happy', 'env': None, 'flap': 'flap_closed', 'lift': 22},
    'fly_off': {'pose': 'fly_off', 'expr': 'rest', 'env': None, 'flap': 'flap_closed', 'lift': 30},
}
flt['poses_float_blender'] = POSES; flt['beats'] = BEATS; flt['expressions'] = EXPR; flt['unit_m'] = U
# landmarks in bind space (Blender m) + bone: eye tops, cap lowest front point, beak tip, cap top, feet
LMB = {'eye_l': ['head', list(BV(head_proj(G.EYE_X[1], EY, 0)))], 'eye_r': ['head', list(BV(head_proj(G.EYE_X[0], EY, 0)))],
       'eye_top': ['head', list(BV(head_proj(150, EY - ER[1], 0)))],
       'cap_top': ['head', list(BV(capf((0, 340 - 131.0, HEAD_C[2]))))], 'brim_front': ['head', list(BV(capf((0, TOP - 10 + 1.5, HEAD_C[2] + 39))))],
       'beak_tip': ['head', list(BV((0, 137, HZ + 28)))], 'chin': ['head', list(BV(head_proj(150, 340 - 122, 0)))],
       'feet': ['torso', list(BV((0, 0, 10)))], 'bag': ['torso', list(BV(BAG_P))],
       'tip_L': [WINGS[1]['lo'], list(BV(add(WINGS[1]['tip'], (1, 0, 0), 13)))], 'tip_R': [WINGS[-1]['lo'], list(BV(add(WINGS[-1]['tip'], (-1, 0, 0), 13)))]}
flt['landmarks_bind'] = LMB

def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {k: tris(o) for k, o in OBJ.items()}
base = counts['body'] + counts['wing_R'] + counts['wing_L']
vis = {}
for b, d in BEATS.items():
    vis[b] = base + sum(counts[x] for x in EXPR[d['expr']]) + (counts[d['env']] if d['env'] else 0) + counts[d['flap']]
report = {'triangles': counts, 'visible_by_beat': vis, 'visible_max': max(vis.values()), 'base_non_swap': base,
          'meshes': {'non_swap (<= 3)': ['body', 'wing_R', 'wing_L'], 'swap': list(SWAP)}, 'unit_mm': round(U * 1000, 4),
          'span_u_bind': WINGS[1]['tip'][0] + 13 - (WINGS[-1]['tip'][0] - 13), 'poses': POSES}
print('GARY_REPORT', json.dumps(vis), json.dumps(counts))
os.makedirs(OUT, exist_ok=True)
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump(TOONJ, open(os.path.join(OUT, 'gary_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, rig] + list(OBJ.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False, export_vertex_color='ACTIVE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('GARY_DONE')
