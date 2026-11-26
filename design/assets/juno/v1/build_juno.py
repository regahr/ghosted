# GHOSTED - Juno the barista, v1: blockout and final model, built to the accepted sketch (assets/juno/sketch).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_juno.py -- [blockout] [H=1.12] [out=<dir>]
# Brief: design/acceptance/juno/brief.md. Direction and join decisions: direction.md. Based on brett/v1/build_brett.py.
# Shapes: the outlines and marks come from the sketch's hand-drawn Bezier paths (../sketch/src/juno.py), read here.
# Sketch units: x right (centred X = x - 150), y down (sole y 340, puff top y 10), Z forward. 1 unit = H / 330 m.
# Blender: Z-up, Juno faces -Y. glTF: Y-up (faces +Z in three.js).
# Nodes: root > float > bounce > rig (body_root, torso, head, arm_L_up, arm_L_lo, arm_R_up, arm_R_lo) > body, decals
#        (skinned, the 2 non-swap meshes); swap parts: eyes, brows, mouths, the 4 cups (one per hold), the marker.
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import juno as J
R = J.R
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
H_M = 1.12          # puff top to sole (sketch estimate; the blockout measure sets it -> measure.md)
OUT = HERE
for a in ARGV:
    if a.startswith('H='): H_M = float(a[2:])
    if a.startswith('out='): OUT = os.path.join(HERE, a[4:]); os.makedirs(OUT, exist_ok=True)
NAME = 'juno_blockout' if BLOCKOUT else 'juno'
PI = math.pi
U = H_M / 330.0
ROW = J.ROW
PAL = {'top': ROW[5], 'apron': ROW[6], 'tie': ROW[7], 'skin': ROW[15], 'hair': ROW[25], 'legs': ROW[26], 'shoe': ROW[5],
       'cup': ROW[23], 'ink': ROW[22], 'white': ROW[23]}
BASIC = ['ink', 'white']
NEUTRAL = [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]]   # Kit's bands2 (neutral grey 178 shade band)
CUPS = ('cup_rest', 'cup_hand', 'cup_wave', 'cup_write')
TOONJ = {'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC,
         'outline_nodes': ['body', 'marker'] + list(CUPS), 'contact_shadow': {'rx': 0.27 * H_M, 'ry': 0.22 * H_M, 'opacity': 0.25}}

def s2l(h):
    h = h.lstrip('#'); out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255; out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0
scn = bpy.context.scene; COL = scn.collection
MATS = {}
def mat(name):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*s2l(PAL[name]), 1); b.inputs['Roughness'].default_value = 0.8
    m['hex'] = PAL[name]; MATS[name] = m; return m

def B(X, y, Z):
    """Sketch (centred X, y down, Z forward) -> Blender metres."""
    return Vector((X * U, -Z * U, (340.0 - y) * U))
def S(v):
    """Blender metres -> sketch (X, y, Z)."""
    return (v.x / U, 340.0 - v.z / U, -v.y / U)

# ================================================================ mesh accumulator (= Brett, Dot)
class Acc:
    def __init__(s, bone='torso'): s.V, s.N, s.F, s.FM, s.VB, s.bone = [], [], [], [], [], bone
    def v(s, p, n, bone=None):
        s.V.append(Vector(p)); s.N.append(Vector(n).normalized()); s.VB.append(bone or s.bone); return len(s.V) - 1
    def f(s, ids, m): s.F.append(list(ids)); s.FM.append(m)
BODY = Acc()
SHELLS = {}
def shell(name):
    class _C:
        def __enter__(c): c.v0, c.f0 = len(BODY.V), len(BODY.F); return c
        def __exit__(c, *a): SHELLS[name] = (c.v0, len(BODY.V), c.f0, len(BODY.F))
    return _C()
def bands(acc, rings, mats, flip=False):
    for r in range(len(rings) - 1):
        A, Bn = rings[r], rings[r + 1]; n = len(A)
        for j in range(n):
            j1 = (j + 1) % n; q = [A[j], A[j1], Bn[j1], Bn[j]]
            acc.f(q[::-1] if flip else q, mats[r])
def fan(acc, pole, ring, m, flip=False):
    n = len(ring)
    for j in range(n):
        t = [pole, ring[(j + 1) % n], ring[j]]
        acc.f(t[::-1] if flip else t, m)
def arc(pts):
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    return L
def at_len(pts, L, s):
    s = max(0.0, min(L[-1], s))
    for i in range(len(L) - 1):
        if L[i] <= s <= L[i + 1]:
            f = (s - L[i]) / max(L[i + 1] - L[i], 1e-9)
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
    return pts[-1]

# ================================================================ HEAD + HAIR CAP: one surface (join: continuous skin)
HALF = [0, 28, 56, 80, 100, 125, 152] if not BLOCKOUT else [0, 45, 90, 135]
TH_H = [math.radians(a) for a in HALF] + [PI] + [math.radians(-a) for a in reversed(HALF[1:])]
TH_H = sorted(TH_H, key=lambda t: (t if t >= 0 else t + 2 * PI))
HP = R.path_points(J.HEAD_HALF, 80); HL = arc(HP)
HEAD_D = 0.92
SKULL_C = 106.0                                  # skull centre (front-view y) for the radial cap projection
def _polar(path):
    pts = [(x - 150.0, y) for x, y in R.path_points(path, 80) if x >= 150.0]
    return sorted((math.atan2(r, SKULL_C - y), math.hypot(r, SKULL_C - y)) for r, y in pts)
CAP_POL = _polar(J.CAP_HALF)
def cap_rho(phi):
    for (a0, r0), (a1, r1) in zip(CAP_POL, CAP_POL[1:]):
        if a0 <= phi <= a1: return r0 + (r1 - r0) * (phi - a0) / max(a1 - a0, 1e-9)
    return CAP_POL[0][1] if phi < CAP_POL[0][0] else CAP_POL[-1][1]
def head_rz(s, f=0.0):
    x, y = at_len(HP, HL, s); r = x - 150.0
    if f > 0:
        phi = math.atan2(r, SKULL_C - y); rho = cap_rho(phi)
        r = r + (rho * math.sin(phi) - r) * f; y = y + ((SKULL_C - rho * math.cos(phi)) - y) * f
    return r, y
def head_pt(th, s, f=0.0):
    r, y = head_rz(s, f)
    return B(r * math.sin(th), y, HEAD_D * r * math.cos(th))
def head_n(th, s, f=0.0):
    e = 0.02
    if s < 0.5: return Vector((0, 0, 1))
    if s > HL[-1] - 0.5: return Vector((0, 0, -1))
    pt = head_pt(th + e, s, f) - head_pt(th - e, s, f); ps = head_pt(th, min(s + 0.4, HL[-1]), f) - head_pt(th, s - 0.4, f)
    n = ps.cross(pt).normalized()
    c = head_pt(th, s, f); ax = Vector((0, 0, c.z))
    return n if n.dot(c - ax) > 0 else -n
def s_of_y(y):
    for i in range(len(HP) - 1):
        if HP[i][1] <= y <= HP[i + 1][1] and HP[i + 1][1] > HP[i][1]:
            f = (y - HP[i][1]) / (HP[i + 1][1] - HP[i][1]); return HL[i] + (HL[i + 1] - HL[i]) * f
    return HL[-1]
# Hairline: front-view y of the hair edge by column angle (deg from the front). Sketch HAIRLINE: y 64 at the centre,
# 84-88 at the head sides in front of the ears (above the eye top 95.5). In 3D it stays ABOVE the ear (ear top y 95) at
# the ear column, then drops behind the ear to the nape at y 140 (sketch hair_back, nape y 142).
# No-fringe rule (bible): forehead band >= 4 px at 1x from the hair edge (ink counted as hair) to the brow top.
HAIRLINE_FRONT = 64.0
for a in ARGV:
    if a.startswith('HF='): HAIRLINE_FRONT = float(a[3:])
_d = 64.0 - HAIRLINE_FRONT
HAIRLINE = [(0, 64.0 - _d), (28, 65.5 - _d), (56, 72.0 - _d * 0.7), (80, 82.0 - _d * 0.3), (90, 86.0), (100, 88.0),
            (125, 114.0), (152, 134.0), (180, 140.0)]
def hair_y(th):
    d = abs(math.degrees((th + PI) % (2 * PI) - PI))
    for (a0, y0), (a1, y1) in zip(HAIRLINE, HAIRLINE[1:]):
        if a0 <= d <= a1: return y0 + (y1 - y0) * (d - a0) / (a1 - a0)
    return HAIRLINE[-1][1]
INK_BAND = 2.6
S_END = HL[-1] - 7.0
NH = 3 if BLOCKOUT else 4
SKIN_F = [0, 0.5, 1.0] if BLOCKOUT else [0, 0.33, 0.66, 1.0]
HAIRLINE_PTS = {}
with shell('head'):
    BODY.bone = 'head'
    pole = BODY.v(B(0, 52.0, 0), (0, 0, 1))                       # cap top (sketch CAP_HALF y 52)
    hair_rings, skin_rings = [], []
    for k in range(1, NH):
        ring = []
        for th in TH_H:
            sh = s_of_y(hair_y(th)); s = sh * (k / NH) ** 0.8
            ring.append(BODY.v(head_pt(th, s, 1.0), head_n(th, s, 1.0)))
        hair_rings.append(ring)
    edge = [BODY.v(head_pt(th, s_of_y(hair_y(th))), head_n(th, s_of_y(hair_y(th)))) for th in TH_H]
    inkr = [BODY.v(head_pt(th, s_of_y(hair_y(th)) + INK_BAND), head_n(th, s_of_y(hair_y(th)) + INK_BAND)) for th in TH_H]
    for th in TH_H: HAIRLINE_PTS[round(math.degrees(th), 1)] = list(head_pt(th, s_of_y(hair_y(th))))
    for k in range(len(SKIN_F)):
        ring = []
        for th in TH_H:
            s0 = s_of_y(hair_y(th)) + INK_BAND; s = s0 + (S_END - s0) * SKIN_F[k]
            ring.append(BODY.v(head_pt(th, s), head_n(th, s)))
        skin_rings.append(ring)
    chin = BODY.v(head_pt(0, HL[-1]), (0, 0, -1))
    fan(BODY, pole, hair_rings[0], 'hair', flip=True)
    bands(BODY, hair_rings + [edge], ['hair'] * (NH - 1))
    bands(BODY, [edge, inkr], ['ink'])
    bands(BODY, [inkr] + skin_rings[1:], ['skin'] * (len(SKIN_F) - 1))
    fan(BODY, chin, skin_rings[-1], 'skin')

def ellipsoid(c, rad, cols, lats, m, bone=None, acc=None):
    """c, rad in sketch units (X, y-down, Z); lats in degrees (from -90 bottom to 90 top, exclusive)."""
    acc = acc or BODY
    top = acc.v(B(c[0], c[1] - rad[1], c[2]), (0, 0, 1), bone)
    bot = acc.v(B(c[0], c[1] + rad[1], c[2]), (0, 0, -1), bone)
    rings = []
    for la in sorted(lats, reverse=True):
        a = math.radians(la); ring = []
        for j in range(cols):
            t = 2 * PI * j / cols; ux, uy, uz = math.cos(a) * math.sin(t), math.sin(a), math.cos(a) * math.cos(t)
            p = B(c[0] + rad[0] * ux, c[1] - rad[1] * uy, c[2] + rad[2] * uz)
            nb = Vector((ux / rad[0], -uz / rad[2], uy / rad[1]))
            ring.append(acc.v(p, nb, bone))
        rings.append(ring)
    fan(acc, top, rings[0], m, flip=True); bands(acc, rings, [m] * (len(rings) - 1)); fan(acc, bot, rings[-1], m)
# ears (layered, half sunk, on the eye line): sketch (+-55, y 105, Z -4), radii (5, 10, 7)
with shell('ears'):
    for s in (1, -1):
        ring = []
        for j in range(8):
            t = 2 * PI * j / 8; ry_, rz_ = 10 * math.cos(t), 7 * math.sin(t)
            ring.append(BODY.v(B(s * 55.0, 105 - ry_, -4 + rz_), Vector((s * 0.35, -math.sin(t), math.cos(t))).normalized(), 'head'))
        fan(BODY, BODY.v(B(s * 60.0, 105, -4), (s, 0, 0), 'head'), ring, 'skin')
        fan(BODY, BODY.v(B(s * 47.0, 105, -4), (-s, 0, 0), 'head'), ring, 'skin')

# ================================================================ PUFF (layered ball, top-back) + SCRUNCHIE (low torus)
with shell('puff'):
    ellipsoid((0, 40, -18), (36, 30, 32), 8 if not BLOCKOUT else 6, [52, 18, -18, -52] if not BLOCKOUT else [30, -30], 'hair', 'head')
with shell('scrunchie'):
    NU, NV = (8, 4) if not BLOCKOUT else (6, 3)
    rings = []
    for i in range(NU):
        a = 2 * PI * (i + 0.5) / NU; cx, cz = 22.0 * math.sin(a), -14.0 + 18.0 * math.cos(a)
        ox, oz = math.sin(a) / 22.0, math.cos(a) / 18.0; ol = math.hypot(ox, oz); ox, oz = ox / ol, oz / ol
        ids = []
        for j in range(NV):
            b = 2 * PI * j / NV + PI / 4
            dx, dyu, dz = ox * math.cos(b), math.sin(b), oz * math.cos(b)
            ids.append(BODY.v(B(cx + 4.8 * dx, 62.0 - 4.8 * dyu, cz + 4.8 * dz), (dx, -dz, dyu), 'head'))
        rings.append(ids)
    bands(BODY, rings + [rings[0]], ['tie'] * NU, flip=True)

# ================================================================ NECK (separate, sunk)
with shell('neck'):
    rings = []
    for (y, r) in ((142.0, 15.0), (168.0, 13.5)):
        ids = []
        for k in range(8):
            t = 2 * PI * k / 8; ids.append(BODY.v(B(r * math.sin(t), y, 0.9 * r * math.cos(t)), (math.sin(t), -math.cos(t), 0), 'torso'))
        rings.append(ids)
    bands(BODY, rings, ['skin'], flip=True)

# ================================================================ BODY: the hourglass (sketch BODY_HG), depth 0.8
NCOL = 14 if not BLOCKOUT else 10
TH = [2 * PI * (j + 0.5) / NCOL for j in range(NCOL)]
JP = R.path_points(J.BODY_HG, 30)
JP = JP[:JP.index(min(JP, key=lambda p: math.dist(p, (204.0, 300.0)))) + 1]   # stop near the hem corner
JL = arc(JP); BODY_D = J.BODY_D
TIE_Y = (235.0, 241.0); TIE_OUT = 1.8
def jpt(th, s, out=0.0):
    x, y = at_len(JP, JL, s); r = x - 150.0 + out
    return B(r * math.sin(th), y, BODY_D * r * math.cos(th))
def jn(th, s):
    e = 0.02; pt = jpt(th + e, s) - jpt(th - e, s); ps = jpt(th, min(s + 0.4, JL[-1])) - jpt(th, max(s - 0.4, 0))
    n = ps.cross(pt).normalized(); c = jpt(th, s)
    return n if n.dot(c - Vector((0, 0, c.z))) > 0 else -n
def s_at_y(y):
    for i in range(len(JP) - 1):
        if JP[i][1] <= y <= JP[i + 1][1] and JP[i + 1][1] > JP[i][1]:
            f = (y - JP[i][1]) / (JP[i + 1][1] - JP[i][1]); return JL[i] + (JL[i + 1] - JL[i]) * f
    return JL[-1]
VY = [158.0, 166, 180, 198, 216, 235, 241, 256, 274, 290] if not BLOCKOUT else [158.0, 172, 198, 222, 235, 241, 266, 290]
J_S = [s_at_y(y) for y in VY] + [JL[-1]]
with shell('body'):
    BODY.bone = 'torso'
    rings = []
    for y, s in zip(VY + [None], J_S):
        o = TIE_OUT if y in TIE_Y else 0.0
        rings.append([BODY.v(jpt(th, s, o), jn(th, s)) for th in TH])
    mats_ = ['tie' if (VY[i], VY[i + 1] if i + 1 < len(VY) else None) == TIE_Y else 'top' for i in range(len(rings) - 1)]
    bands(BODY, rings, mats_)
    fan(BODY, BODY.v(B(0, 300.5, 0), (0, 0, -1)), rings[-1], 'top')
VPROF = [p for p in R.profile(J.BODY_HG) if p[0] < 299.0]
def zf(x, y, out=0.0):
    r = R.r_at(VPROF, y); return r * BODY_D * math.sqrt(max(1 - (x / max(r, 1e-3)) ** 2, 0.0)) + out

# ================================================================ BOW + TAILS (layered, at the back, on the torso)
with shell('bow'):
    wy = 238.0; rw = R.r_at(VPROF, wy) + TIE_OUT; bz = -rw * BODY_D - 2.5
    nb = 6 if not BLOCKOUT else 4
    for s in (1, -1):
        ellipsoid((s * 9, wy - 2, bz), (9, 6, 3.5), nb, [0], 'tie', 'torso')
        tube_pts = [B(s * 3, wy, bz + 0.5), B(s * 8, wy + 22, bz - 0.5)]
        d = (tube_pts[1] - tube_pts[0]).normalized(); u = d.cross(Vector((0, 1, 0))).normalized(); w = d.cross(u).normalized()
        rr = []
        for p, r in zip(tube_pts, (2.6 * U, 2.2 * U)):
            rr.append([BODY.v(p + (u * math.cos(2 * PI * k / 4 + PI / 4) + w * math.sin(2 * PI * k / 4 + PI / 4)) * r,
                              u * math.cos(2 * PI * k / 4 + PI / 4) + w * math.sin(2 * PI * k / 4 + PI / 4), 'torso') for k in range(4)])
        bands(BODY, rr, ['tie'], flip=True)
        fan(BODY, BODY.v(tube_pts[1] + d * 1.5 * U, d, 'torso'), rr[1], 'tie', flip=True)
    ellipsoid((0, wy - 1, bz - 1), (4.2, 4.2, 3.5), nb, [0], 'tie', 'torso')

# ================================================================ ARMS (join: sunk sleeve root, rigid cuff ball, hand ball)
# Bone lengths fixed (upper 36, forearm to the hand centre 58); each beat is a two-bone reach to the sketch's targets.
ARM_SIDES = 6
ARM = {}
L_UP, L_LO = 36.0, 58.0
for s, side in ((1, 'L'), (-1, 'R')):           # L = her left = viewer-right = +X
    S_ = (s * 54.0, 186.0, 0.0)
    a1 = math.radians(15); E_ = (S_[0] + s * L_UP * math.sin(a1), S_[1] + L_UP * math.cos(a1), 0.0)
    a2 = math.radians(8); H_ = (E_[0] + s * L_LO * math.sin(a2), E_[1] + L_LO * math.cos(a2), 0.0)
    ARM[side] = {'S': B(*S_), 'E': B(*E_), 'H': B(*H_), 'sx': s}
HAND_R = 10.0
for side, a in ARM.items():
    with shell('arm_' + side):
        bu, bl = 'arm_%s_up' % side, 'arm_%s_lo' % side
        dd = (a['E'] - a['S']).normalized()
        tube_s = [a['S'] - dd * 4 * U, a['E']]
        # sleeve (brown), flat cap buried in the body; its end is inside the cuff ball
        u = dd.cross(Vector((0, 1, 0))).normalized(); w = dd.cross(u).normalized()
        def ringp(c, r, bone, n=ARM_SIDES, d=dd, u=u, w=w):
            return [BODY.v(c + (u * math.cos(2 * PI * k / n) + w * math.sin(2 * PI * k / n)) * r, u * math.cos(2 * PI * k / n) + w * math.sin(2 * PI * k / n), bone) for k in range(n)]
        r0 = ringp(tube_s[0], 12.0 * U, bu); r1 = ringp(tube_s[1], 10.5 * U, bu)
        bands(BODY, [r0, r1], ['top'], flip=True); fan(BODY, BODY.v(tube_s[0], -dd, bu), r0, 'top', flip=False)
        X, y, Z = S(a['E'])
        ellipsoid((X, y, Z), (11.0, 11.0, 11.0), ARM_SIDES, [35, -35] if not BLOCKOUT else [0], 'top', bu)   # the cuff
        d2 = (a['H'] - a['E']).normalized(); u2 = d2.cross(Vector((0, 1, 0))).normalized(); w2 = d2.cross(u2).normalized()
        f0 = ringp(a['E'] + d2 * 4 * U, 8.2 * U, bl, d=d2, u=u2, w=w2); f1 = ringp(a['H'] - d2 * 6 * U, 7.4 * U, bl, d=d2, u=u2, w=w2)
        bands(BODY, [f0, f1], ['skin'], flip=True)                                                          # forearm
        X, y, Z = S(a['H'])
        ellipsoid((X, y, Z), (HAND_R, 10.5, 9.5), ARM_SIDES, [40, -15] if not BLOCKOUT else [0], 'skin', bl)  # ball hand

# ================================================================ LEGS + SHOES (body_root)
with shell('legs'):
    for s in (1, -1):
        rings = []
        for (y, r) in ((284.0, 13.0), (330.0, 12.0)):
            ids = []
            for k in range(6):
                t = 2 * PI * k / 6; ids.append(BODY.v(B(s * 20 + r * math.sin(t), y, r * math.cos(t)), (math.sin(t), -math.cos(t), 0), 'body_root'))
            rings.append(ids)
        bands(BODY, rings, ['legs'], flip=True)
        ellipsoid((s * 21, 332.0, 9), (13.0, 8.5, 19), 8 if not BLOCKOUT else 6, [20, -30] if not BLOCKOUT else [0], 'shoe', 'body_root')

def orient_acc(acc):
    n = 0
    for i, f in enumerate(acc.F):
        a, b, c = acc.V[f[0]], acc.V[f[1]], acc.V[f[2]]; fn = (b - a).cross(c - a)
        if len(f) == 4: fn = fn + (c - a).cross(acc.V[f[3]] - a)
        an = sum((acc.N[k] for k in f), Vector())
        if fn.dot(an) < 0: acc.F[i] = f[::-1]; n += 1
    return n
REWOUND = orient_acc(BODY)

# ================================================================ build meshes
def make_mesh(name, acc, smooth=True):
    used = sorted(set(i for f in acc.F for i in f)); remap = {o: n for n, o in enumerate(used)}
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(acc.V[i]) for i in used], [], [[remap[i] for i in f] for f in acc.F])
    names = sorted(set(acc.FM), key=lambda m: list(PAL).index(m))
    for m in names: me.materials.append(mat(m))
    me.polygons.foreach_set('material_index', [names.index(m) for m in acc.FM])
    me.polygons.foreach_set('use_smooth', [smooth] * len(me.polygons)); me.update()
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob)
    return ob, remap, used
body, BREMAP, BUSED = make_mesh('body', BODY)
bm = bmesh.new(); bm.from_mesh(body.data); bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY'); bm.to_mesh(body.data); bm.free(); body.data.update()
bm = bmesh.new(); bm.from_mesh(body.data); bm.normal_update()
nonman = sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary)
boundary = sum(1 for e in bm.edges if e.is_boundary)
inward = 0
for f in bm.faces:
    an = sum((BODY.N[BUSED[v.index]] for v in f.verts), Vector())
    if f.normal.dot(an) < 0: inward += 1
bm.free()
body.data.normals_split_custom_set_from_vertices([tuple(BODY.N[i]) for i in BUSED])
body.data.update()
# Outline weight (Kit method, 'outline_wc' -> glTF COLOR_0): the neck ink fades where it enters the body top
v0n, v1n = SHELLS['neck'][0], SHELLS['neck'][1]
body.data.color_attributes.new('outline_wc', 'FLOAT_COLOR', 'POINT')
_ca = body.data.color_attributes['outline_wc']
for nv, ov in enumerate(BUSED):
    w = 1.0
    if v0n <= ov < v1n: w = 1.0 if S(BODY.V[ov])[1] < 150 else 0.0
    if SHELLS['body'][0] <= ov < SHELLS['body'][1] and S(BODY.V[ov])[1] < 159.0: w = 0.0
    _ca.data[nv].color = (w, w, w, 1.0)
_ci = body.data.color_attributes.find('outline_wc')
body.data.color_attributes.active_color_index = _ci; body.data.color_attributes.render_color_index = _ci

# ================================================================ DECALS (projected on the analytic head, cap and body)
VPROF_M = [(150.0, 24.0)] + [(y, max(r, 24.0)) if y < 168 else (y, r) for y, r in VPROF]
SURF = {'head': (R.profile(J.HEAD_HALF), HEAD_D), 'cap': (R.profile(J.CAP_HALF), HEAD_D), 'body': (VPROF_M, BODY_D)}
def front_hit(tree, X, y, off):
    prof, dep = SURF[tree]
    r = R.r_at(prof, y); Xc = max(-r * 0.999, min(r * 0.999, X)); Z = dep * math.sqrt(max(r * r - Xc * Xc, 0.0))
    e = 0.25; r1, r0 = R.r_at(prof, y + e), R.r_at(prof, y - e); drdy = (r1 - r0) / (2 * e)
    gX, gy, gZ = 2 * Xc, -2 * r * drdy, 2 * Z / dep ** 2
    nb = Vector((gX, -gZ, -gy)).normalized()
    return B(Xc, y, Z) + nb * off * U, nb
DEC = Acc('torso')
SWAP_NAMES = ('eyes_open', 'eyes_happy', 'eyes_down', 'brows_rest', 'brows_dry', 'mouth_smile', 'mouth_laugh', 'mouth_talk', 'mouth_smirk')
SWAP = {k: Acc('head') for k in SWAP_NAMES}
def clean(pts):
    out = []
    for p in pts:
        if not out or math.dist(p, out[-1]) > 0.3: out.append(p)
    if math.dist(out[0], out[-1]) < 0.3: out.pop()
    return out
def fan_card(acc, tree, pts2d, off, m, bone=None, centre=None):
    cx, cy = centre or (sum(p[0] for p in pts2d) / len(pts2d), sum(p[1] for p in pts2d) / len(pts2d))
    c = acc.v(front_hit(tree, cx - 150, cy, off)[0], (0, -1, 0), bone)
    ring = [acc.v(front_hit(tree, x - 150, y, off)[0], (0, -1, 0), bone) for x, y in pts2d]
    for j in range(len(ring)): acc.f([c, ring[j], ring[(j + 1) % len(ring)]], m)
def line_card(acc, tree, pts, width, off, m, bone=None, closed=False):
    if closed: pts = pts + [pts[0]]
    L, Rr = [], []
    for i, p in enumerate(pts):
        if closed and i in (0, len(pts) - 1): a, b = pts[-2], pts[1]
        else: a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]; l = math.hypot(tx, ty)
        nx, ny = -ty / l * width / 2, tx / l * width / 2
        L.append(acc.v(front_hit(tree, p[0] + nx - 150, p[1] + ny, off)[0], (0, -1, 0), bone))
        Rr.append(acc.v(front_hit(tree, p[0] - nx - 150, p[1] - ny, off)[0], (0, -1, 0), bone))
    for i in range(len(pts) - 1): acc.f([L[i], L[i + 1], Rr[i + 1]], m); acc.f([L[i], Rr[i + 1], Rr[i]], m)
def bez_pts(d, n): return R.path_points(d, n)
def grid_card(acc, tree, pts2d, off, m, rows, cols=3, bone=None):
    """Rows of points across a closed shape, so the fill follows a curved host (Ricky / Brett method)."""
    ys = [p[1] for p in pts2d]; y0, y1 = min(ys), max(ys); n = len(pts2d); R_ = []
    for k in range(rows + 1):
        y = min(max(y0 + (y1 - y0) * k / rows, y0 + 0.05), y1 - 0.05); xs = []
        for i in range(n):
            (xa, ya), (xb, yb) = pts2d[i], pts2d[(i + 1) % n]
            if (ya - y) * (yb - y) <= 0 and ya != yb: xs.append(xa + (xb - xa) * (y - ya) / (yb - ya))
        xl, xr = min(xs), max(xs)
        R_.append([acc.v(front_hit(tree, xl + (xr - xl) * c / cols - 150, y, off)[0], (0, -1, 0), bone) for c in range(cols + 1)])
    for a_, b_ in zip(R_, R_[1:]):
        for c in range(cols):
            q = (a_[c], a_[c + 1], b_[c + 1], b_[c]); acc.f([q[0], q[1], q[2]], m); acc.f([q[0], q[2], q[3]], m)
EY = J.LM['eye']
# face (head bone): ink eyes with glints; happy (laugh) and down (writing) eyes are ink arcs
for ex in J.LM['eye_x']:
    fan_card(SWAP['eyes_open'], 'head', clean(bez_pts(R.oval(ex, EY, 6.5, 8.5), 3 if not BLOCKOUT else 2)), 0.4, 'ink')
    if not BLOCKOUT: fan_card(SWAP['eyes_open'], 'head', clean(bez_pts(R.oval(ex + 2, EY - 3.2, 2.0, 2.4), 2)), 0.6, 'white')
for d in J.HAPPY_EYES: line_card(SWAP['eyes_happy'], 'head', bez_pts(d, 4), 3.4, 0.4, 'ink')
for d in J.DOWN_EYES: line_card(SWAP['eyes_down'], 'head', bez_pts(d, 4), 3.4, 0.4, 'ink')
for nm, br in (('brows_rest', J.BROWS), ('brows_dry', J.BROWS_DRY)):
    for d in br: line_card(SWAP[nm], 'head', bez_pts(d, 3), 2.8, 0.4, 'ink')
# MOUTHS: rest = a closed smile line (chair call 6); laugh and talk = Ricky style (bible "Art rule: mouths"): a filled
# ink mouth with a white teeth band (row 23) along the top edge; dry = a one-sided smirk line
line_card(SWAP['mouth_smile'], 'head', bez_pts(J.SMILE, 4), 3.0, 0.5, 'ink')
line_card(SWAP['mouth_smirk'], 'head', bez_pts(J.SMIRK, 4), 3.0, 0.5, 'ink')
for nm, md, td, rows in (('mouth_laugh', J.LAUGH, J.LAUGH_TEETH, 3), ('mouth_talk', J.TALK, J.TALK_TEETH, 2)):
    grid_card(SWAP[nm], 'head', clean(bez_pts(md, 6)), 0.6, 'ink', rows)
    grid_card(SWAP[nm], 'head', clean(bez_pts(td, 6)), 0.85, 'white', 1)
# hair strand lines ON the cap (trimmed so they start on the hair, above the hairline ink)
def hair_edge_y_at(x):
    X = x - 150.0; best = None
    for th in [math.radians(t) for t in range(-100, 101)]:
        p = S(head_pt(th, s_of_y(hair_y(th))))
        if best is None or abs(p[0] - X) < abs(best[0] - X): best = p
    return best[1]
if not BLOCKOUT:
    for d in J.STRANDS:
        pts = [p for p in bez_pts(d, 4) if p[1] <= hair_edge_y_at(p[0]) - 3.5]
        if len(pts) >= 2: line_card(DEC, 'cap', pts, 1.6, 0.6, 'ink', bone='head')
    for (cx, cy) in J.CHEEKS:
        fan_card(DEC, 'head', clean(bez_pts(R.oval(cx, cy, 7, 4), 2)), 0.3, 'apron', bone='head')
# apron (torso): bib, straps, skirt, pocket; ink edges; the neckline
VOFF = 1.0
def outline(acc, tree, pts, w, off, closed=True): line_card(acc, tree, pts, w, off, 'ink', closed=closed)
BIB = "M128,198 L172,198 C173,212 175,224 176.5,234 L123.5,234 C125,224 127,212 128,198 Z"
bib = clean(bez_pts(BIB, 3))
grid_card(DEC, 'body', bib, VOFF, 'apron', 3 if not BLOCKOUT else 2, 3)
if not BLOCKOUT: outline(DEC, 'body', bib, 1.5, VOFF + 0.2)
STRAPS = ["M131,198 C134,184 138,172 141.5,163", "M169,198 C166,184 162,172 158.5,163"]
for d in STRAPS:
    pp = bez_pts(d, 2)
    if not BLOCKOUT: line_card(DEC, 'body', pp, 7.4, VOFF, 'ink')
    line_card(DEC, 'body', pp, 5.0, VOFF + 0.2, 'apron')
SKIRT = "M111,241 L189,241 C197,257 203,272 206,288 C188,294 112,294 94,288 C97,272 103,257 111,241 Z"
skirt = clean(bez_pts(SKIRT, 3))
grid_card(DEC, 'body', skirt, VOFF, 'apron', 4 if not BLOCKOUT else 2, 6 if not BLOCKOUT else 3)
if not BLOCKOUT: outline(DEC, 'body', skirt, 1.6, VOFF + 0.2)
POCKET = "M134,254 L166,254 L165,269 C160,273 140,273 135,269 Z"
pk = clean(bez_pts(POCKET, 2))
if not BLOCKOUT: fan_card(DEC, 'body', [(x + (x - 150) * 0.08, y + (y - 262) * 0.12) for x, y in pk], VOFF + 0.3, 'ink')
fan_card(DEC, 'body', pk, VOFF + 0.5, 'tie')
if not BLOCKOUT: line_card(DEC, 'body', bez_pts(J.NECKLINE, 3), 1.4, VOFF, 'ink')
LAND = {'eye_top': front_hit('head', J.LM['eye_x'][0] - 150, EY - 8.5, 0.4)[0], 'mouth': front_hit('head', 0, 130, 0.5)[0],
        'brow': front_hit('head', -19, 85, 0.4)[0]}
decals, DREMAP, DUSED = make_mesh('decals', DEC, smooth=False)
swaps = {k: make_mesh(k, a, smooth=False) for k, a in SWAP.items()}
BODYTREE = BVHTree.FromPolygons([tuple(v) for v in BODY.V], BODY.F)
def orient_out(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.normal_update()
    for f in bm.faces:
        c = f.calc_center_median(); loc, nrm, _, _ = BODYTREE.find_nearest(c)
        if f.normal.dot(nrm) < 0: f.normal_flip()
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
orient_out(decals)
for k, (o, _, _) in swaps.items(): orient_out(o)

# ================================================================ RIG
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root
bnc = bpy.data.objects.new('bounce', None); COL.objects.link(bnc); bnc.parent = flt
arm_d = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm_d); COL.objects.link(rig); rig.parent = bnc
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
b0 = arm_d.edit_bones.new('body_root'); b0.head = (0, 0, 0); b0.tail = (0, 0, 20 * U)
bt = arm_d.edit_bones.new('torso'); bt.head = (0, 0, 0); bt.tail = B(0, 200, 0); bt.parent = b0
bh = arm_d.edit_bones.new('head'); bh.head = B(0, 152, 0); bh.tail = B(0, 60, 0); bh.parent = bt
for side, a in ARM.items():
    bu = arm_d.edit_bones.new('arm_%s_up' % side); bu.head = a['S']; bu.tail = a['E']; bu.parent = bt
    bl = arm_d.edit_bones.new('arm_%s_lo' % side); bl.head = a['E']; bl.tail = a['H']; bl.parent = bu; bl.use_connect = False
bpy.ops.object.mode_set(mode='OBJECT')
def skin(ob, acc, used):
    ob.parent = rig
    mod = ob.modifiers.new('skin', 'ARMATURE'); mod.object = rig
    groups = {}
    for nv, ov in enumerate(used):
        bn = acc.VB[ov]
        if bn not in groups: groups[bn] = ob.vertex_groups.new(name=bn)
        groups[bn].add([nv], 1.0, 'REPLACE')
skin(body, BODY, BUSED); skin(decals, DEC, DUSED)
DEFAULT_ON = ('eyes_open', 'brows_rest', 'mouth_smile')
for k, (o, _, used) in swaps.items():
    skin(o, SWAP[k], used); o['variant'] = k; o['default_visible'] = k in DEFAULT_ON
for k, v in LAND.items(): decals[k + '_rest_blender'] = list(v)

# ---------------------------------------------------------------- poses: two-bone reach, stored as axis + angle (Brett)
def solve(side, T, pole):
    a = ARM[side]; S0, E, H = a['S'], a['E'], a['H']
    L1, L2 = (E - S0).length, (H - E).length; d = min((T - S0).length, L1 + L2 - 1e-4); dT = (T - S0).normalized()
    aa = (L1 * L1 - L2 * L2 + d * d) / (2 * d); hh = math.sqrt(max(L1 * L1 - aa * aa, 0.0))
    pp = (pole - dT * pole.dot(dT)).normalized(); E2 = S0 + dT * aa + pp * hh
    R1 = (E - S0).rotation_difference(E2 - S0); H1 = S0 + R1 @ (H - S0)
    R2w = (H1 - E2).rotation_difference(T - E2)
    ax2 = R1.inverted() @ R2w.axis
    return {'arm_%s_up' % side: [*R1.axis, math.degrees(R1.angle)], 'arm_%s_lo' % side: [*ax2, math.degrees(R2w.angle)]}
def arm(side, hand, elbow):
    s = ARM[side]['sx']; T = B(*hand); EL = B(*elbow)
    return solve(side, T, EL - ARM[side]['S']), T
TARGETS = {}
def hold(name, side, hand, elbow):
    p, T = arm(side, hand, elbow); TARGETS[(name, side)] = T; return p
r226 = R.r_at(VPROF, 226)
# the sketch's hand targets (juno.py model(), arms): 'cup' rest, 'sides', 'hand' (hand over), 'wave0-2', 'holdhigh', 'pen'
REST = {**hold('rest', 'L', (21, 226, zf(16, 226, 12)), (68, 214, 10)), **hold('rest', 'R', (-21, 226, zf(16, 226, 12)), (-68, 214, 10))}
SIDES_L = hold('sides', 'L', (R.r_at(VPROF, 254) + 9, 254, 8), (R.r_at(VPROF, 214) + 8, 214, 0))
HAND_R = hold('hand', 'R', (-42, 212, 78), (-70, 214, 22))
POSES = {'rest': REST, 'hand': {**SIDES_L, **HAND_R}}
CUP1_L = hold('wave', 'L', (19, 228, zf(17, 228, 13)), (68, 214, 10))
for k in range(3):
    POSES['wave%d' % (k + 1)] = {**CUP1_L, **hold('wave%d' % (k + 1), 'R', (-(86 + 13 * k), 163, 14), (-84, 214, 4))}
HIGH_L = hold('write', 'L', (21, 208, zf(20, 210, 20)), (70, 216, 14))
PEN_R = hold('write', 'R', (-12, 205, zf(14, 210, 36)), (-68, 218, 22))
POSES['write'] = {**HIGH_L, **PEN_R, 'head': [1.0, 0.0, 0.0, 14.0]}
POSES['handover'] = dict(POSES['hand'])
flt['poses_float_blender'] = POSES
flt['height_m'] = H_M; flt['unit_m'] = U
flt['expressions'] = {'rest': ['eyes_open', 'brows_rest', 'mouth_smile'], 'laugh': ['eyes_happy', 'brows_rest', 'mouth_laugh'],
                      'talk': ['eyes_open', 'brows_rest', 'mouth_talk'], 'dry': ['eyes_open', 'brows_dry', 'mouth_smirk'],
                      'writing': ['eyes_down', 'brows_rest', 'mouth_smile']}
flt['beat_defaults'] = {'rest': {'expr': 'rest', 'cup': 'cup_rest'}, 'hand': {'expr': 'rest', 'cup': 'cup_hand'},
                        'wave1': {'expr': 'rest', 'cup': 'cup_wave'}, 'wave2': {'expr': 'talk', 'cup': 'cup_wave'},
                        'wave3': {'expr': 'rest', 'cup': 'cup_wave'}, 'write': {'expr': 'writing', 'cup': 'cup_write', 'marker': True},
                        'handover': {'expr': 'dry', 'cup': 'cup_hand'}, '': {'expr': 'rest', 'cup': None}}

def pose(name=None):
    for pb in rig.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    P = dict(flt['poses_float_blender'][name].to_dict()) if name else {}
    for bn, (x, y, z, deg) in P.items():
        M = rig.data.bones[bn].matrix_local.to_3x3().inverted()
        rig.pose.bones[bn].rotation_quaternion = Quaternion(M @ Vector((x, y, z)), math.radians(deg))
    bpy.context.view_layer.update()
def deform(bn):
    pb = rig.pose.bones[bn]; return pb.matrix @ rig.data.bones[bn].matrix_local.inverted()
def hand_now(side):
    return deform('arm_%s_lo' % side) @ ARM[side]['H']
ERR = {}
for (nm, side), T in TARGETS.items():
    pose('wave1' if nm == 'wave' else 'rest' if nm == 'rest' else 'hand' if nm in ('hand', 'sides') else nm)
    ERR['%s_%s_mm' % (nm, side)] = round((hand_now(side) - T).length * 1000, 2)

# ================================================================ CUPS (one swap part per hold) + MARKER
# The cup (sketch CUP_HALF / LID_HALF): a 10-sided frustum, 34 tall, r 10 at the bottom to r 13 at the top, a domed
# lid with a rim (r 15). Local frame: h up from the cup centre, Z toward the viewer. Built in the beat's pose frame at
# the sketch's cup position, then taken back to the bind pose of the bone that holds it (Brett's thumb method).
CUP_N = 10 if not BLOCKOUT else 8
def cup_r(h): return 10.0 + 3.0 * (h + 17.0) / 34.0
# "You are not a PDF." - hand-drawn ink strokes (polylines, not a font; chair call 4). Glyph boxes: u right, v down,
# v 0 = cap top, v 1 = baseline, x-height at v 0.4.
GLYPH = {
    'Y': (0.62, [[(0, 0), (0.31, 0.46), (0.62, 0)], [(0.31, 0.46), (0.31, 1)]]),
    'o': (0.5, [[(0.25, 0.4), (0.48, 0.52), (0.48, 0.88), (0.25, 1), (0.02, 0.88), (0.02, 0.52), (0.25, 0.4)]]),
    'u': (0.48, [[(0, 0.4), (0, 0.84), (0.14, 1), (0.34, 0.98), (0.48, 0.8)], [(0.48, 0.4), (0.48, 1)]]),
    'a': (0.5, [[(0.46, 0.5), (0.28, 0.4), (0.06, 0.48), (0, 0.8), (0.16, 1), (0.36, 0.95), (0.48, 0.74)], [(0.48, 0.42), (0.5, 1)]]),
    'r': (0.38, [[(0, 0.4), (0, 1)], [(0, 0.62), (0.14, 0.44), (0.38, 0.42)]]),
    'e': (0.46, [[(0.02, 0.7), (0.44, 0.68), (0.38, 0.47), (0.2, 0.4), (0.03, 0.52), (0.02, 0.84), (0.2, 1), (0.44, 0.93)]]),
    'n': (0.48, [[(0, 0.4), (0, 1)], [(0, 0.6), (0.16, 0.42), (0.38, 0.44), (0.48, 0.62), (0.48, 1)]]),
    't': (0.4, [[(0.14, 0.12), (0.14, 0.88), (0.26, 1), (0.4, 0.94)], [(0, 0.42), (0.36, 0.4)]]),
    'P': (0.5, [[(0, 1), (0, 0), (0.34, 0.02), (0.5, 0.16), (0.48, 0.34), (0.3, 0.48), (0, 0.48)]]),
    'D': (0.54, [[(0, 0), (0, 1), (0.28, 0.98), (0.52, 0.72), (0.52, 0.28), (0.28, 0.02), (0, 0)]]),
    'F': (0.46, [[(0.46, 0), (0, 0), (0, 1)], [(0, 0.48), (0.36, 0.48)]]),
    '.': (0.12, [[(0.02, 0.9), (0.1, 1)]]),
    ' ': (0.3, [])}
TEXT_LINES = [("You are", 309.5, -0.6), ("not a", 316.8, 0.5), ("PDF.", 324.2, 0.3)]   # (line, baseline y, dx)
CAP_H, TRACK, STROKE = 4.6, 0.9, 0.75
def text_strokes():
    """Strokes in the cup front's flat frame (u along the surface from the front centre, y down, sketch units)."""
    out = []
    for txt, base, dx in TEXT_LINES:
        widths = [GLYPH[c][0] * CAP_H for c in txt]; total = sum(widths) + TRACK * (len(txt) - 1); x = -total / 2 + dx
        for c, w in zip(txt, widths):
            for st in GLYPH[c][1]: out.append([(x + u * CAP_H, base - CAP_H + v * CAP_H) for u, v in st])
            x += w + TRACK
    return out
STROKES = text_strokes()
def facet_pt(th, h, off):
    """A point ON the cup's facet plane at angle th (from the front), height h; lifted off along the facet normal."""
    step = 2 * PI / CUP_N; tc = round(th / step) * step
    r = cup_r(h) * math.cos(PI / CUP_N) / math.cos(th - tc)
    return (r * math.sin(th) + off * math.sin(tc), h, r * math.cos(th) + off * math.cos(tc))
def split_at_ridges(pts):
    """Insert a point wherever a stroke crosses a facet ridge, so no strip triangle spans two facets (no sinking)."""
    step = 2 * PI / CUP_N; out = [pts[0]]
    for (u0, y0), (u1, y1) in zip(pts, pts[1:]):
        t0, t1 = u0 / cup_r(317 - y0), u1 / cup_r(317 - y1)
        k0, k1 = math.floor((t0 + step / 2) / step), math.floor((t1 + step / 2) / step)
        if k0 != k1:
            for k in range(min(k0, k1) + 1, max(k0, k1) + 1):
                tr = (k - 0.5) * step; f = (tr - t0) / (t1 - t0) if t1 != t0 else 0.5
                if 0 < f < 1: out.append((u0 + (u1 - u0) * f, y0 + (y1 - y0) * f))
        out.append((u1, y1))
    return out
def build_cup(acc, centre, tilt_deg, bone, text=True):
    """centre: sketch (X, y, Z) of the cup centre. tilt: degrees, the top leans back toward her (-Z)."""
    ct, st = math.cos(math.radians(tilt_deg)), math.sin(math.radians(tilt_deg))
    def W(p, n=None):
        x, h, z = p; h2, z2 = h * ct - z * st, h * st + z * ct          # rotate about X: + tilt moves the top to -Z
        P = B(centre[0] + x, centre[1] - h2, centre[2] + z2)
        if n is None: return P
        nx, nh, nz = n; nh2, nz2 = nh * ct - nz * st, nh * st + nz * ct
        return P, Vector((nx, -nz2, nh2)).normalized()
    def V(p, n): P, N = W(p, n); return acc.v(P, N, bone)
    ang = [2 * PI * (j + 0.5) / CUP_N for j in range(CUP_N)]
    def ring(h, r, nh=0.0): return [V((r * math.sin(a), h, r * math.cos(a)), (math.sin(a), nh, math.cos(a))) for a in ang]
    bot = ring(-17.0, 10.0, -0.1); top = ring(15.6, cup_r(15.6), -0.1)
    bands(acc, [top, bot], ['cup'])
    fan(acc, V((0, -17.0, 0), (0, -1, 0)), bot, 'cup')
    rim0 = ring(15.4, 13.2, -0.2); rim1 = ring(19.5, 15.0, 0.3)
    bands(acc, [rim1, rim0], ['cup'])
    fan(acc, V((0, 22.0, 0), (0, 1, 0)), rim1, 'cup', flip=True)
    if text and not BLOCKOUT:
        for stp in STROKES:
            pts = split_at_ridges(stp); L_, R_ = [], []
            for i, (u, y) in enumerate(pts):
                a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
                tx, ty = b[0] - a[0], b[1] - a[1]; l = math.hypot(tx, ty) or 1
                nx, ny = -ty / l * STROKE / 2, tx / l * STROKE / 2
                for (uu, yy), lst in (((u + nx, y + ny), L_), ((u - nx, y - ny), R_)):
                    h = 317.0 - yy; th = uu / cup_r(h)
                    lst.append(acc.v(W(facet_pt(th, h, 0.18)), (0, -1, 0), bone))
            for i in range(len(pts) - 1): acc.f([L_[i], L_[i + 1], R_[i + 1]], 'ink'); acc.f([L_[i], R_[i + 1], R_[i]], 'ink')
CUP_AT = {   # (pose, holding bone, cup centre (sketch X, y, Z), tilt) from juno.py model()
    'cup_rest': ('rest', 'torso', (0.0, 224.0, zf(0, 226, 16)), 0.0),
    'cup_hand': ('hand', 'arm_R_lo', None, 0.0),
    'cup_wave': ('wave1', 'arm_L_lo', None, 0.0),
    'cup_write': ('write', 'arm_L_lo', None, 10.0)}
CUP_ACC = {k: Acc(v[1]) for k, v in CUP_AT.items()}
MARK = Acc('arm_R_lo')
def to_bind(acc, v0, bn):
    D = deform(bn); Di = D.inverted(); Rn = Di.to_3x3()
    for i in range(v0, len(acc.V)): acc.V[i] = Di @ acc.V[i]; acc.N[i] = (Rn @ acc.N[i]).normalized()
for k, (pn, bn, c, tilt) in CUP_AT.items():
    pose(pn)
    if c is None:
        hx, hy, hz = S(hand_now('R' if bn == 'arm_R_lo' else 'L'))
        if k == 'cup_hand': c = (hx, hy - 10.0 - 17.0, hz + 1.0)                   # on the palm
        elif k == 'cup_wave': c = (hx - 16.0, hy - 5.0, hz + 3.0)                   # held from her left side
        else: c = (hx - 15.0, hy - 6.0, hz + 6.0)                                   # up at the chest
    CUP_AT[k] = (pn, bn, c, tilt)
    build_cup(CUP_ACC[k], c, tilt, bn)
    to_bind(CUP_ACC[k], 0, bn)
# the marker (write beat, her right hand): from the fist to the cup front
pose('write')
hx, hy, hz = S(hand_now('R')); cwx, cwy, cwz = CUP_AT['cup_write'][2]
m0 = B(hx + 3, hy - 3, hz + 3); m1 = B(cwx - 6.5, cwy - 2.0, cwz + 11.5)
d = (m1 - m0).normalized(); u = d.cross(Vector((0, 1, 0))).normalized(); w = d.cross(u).normalized()
mr = [[MARK.v(p + (u * math.cos(2 * PI * k / 4 + PI / 4) + w * math.sin(2 * PI * k / 4 + PI / 4)) * 2.7 * U,
              u * math.cos(2 * PI * k / 4 + PI / 4) + w * math.sin(2 * PI * k / 4 + PI / 4)) for k in range(4)] for p in (m0, m1)]
bands(MARK, mr, ['tie'], flip=True); fan(MARK, MARK.v(m0 - d * 1.2 * U, -d), mr[0], 'tie'); fan(MARK, MARK.v(m1 + d * 1.8 * U, d), mr[1], 'ink', flip=True)
to_bind(MARK, 0, 'arm_R_lo')
pose(None)
props = {}
for k, acc in list(CUP_ACC.items()) + [('marker', MARK)]:
    orient_acc(acc)
    ob, _, used = make_mesh(k, acc); ob.data.normals_split_custom_set_from_vertices([tuple(acc.N[i]) for i in used]); ob.data.update()
    skin(ob, acc, used); ob['variant'] = k; ob['default_visible'] = k == 'cup_rest'; props[k] = ob
# text faces: flat (they are on flat facets)
for k in CUPS:
    me = props[k].data; ink_i = [i for i, m in enumerate(me.materials) if m.name == 'ink']
    if ink_i: me.polygons.foreach_set('use_smooth', [p.material_index not in ink_i for p in me.polygons])

# ================================================================ REPORT + EXPORT
def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {'body': tris(body), 'decals': tris(decals)}
for k, (o, _, _) in swaps.items(): counts[k] = tris(o)
for k, o in props.items(): counts[k] = tris(o)
base = counts['body'] + counts['decals']
EXPR = flt['expressions'].to_dict()
vis = {}
for beat, bd in flt['beat_defaults'].to_dict().items():
    if not beat: continue
    e = EXPR[bd['expr']]
    vis[beat] = base + sum(counts[x] for x in e) + (counts[bd['cup']] if bd.get('cup') else 0) + (counts['marker'] if bd.get('marker') else 0)
for ex in EXPR: vis['rest + ' + ex] = base + sum(counts[x] for x in EXPR[ex]) + counts['cup_rest']
counts['visible'] = vis
counts['body_by_part'] = {nm: sum(len(f) - 2 for f in BODY.F[f0:f1]) for nm, (v0, v1, f0, f1) in SHELLS.items()}
counts['cup_text_tris'] = counts['cup_rest'] - (2 * CUP_N + CUP_N + 2 * CUP_N + CUP_N)
checks = {'body_nonmanifold_edges': nonman, 'body_boundary_edges (neck tube ends, body top ring, leg ends, sleeve roots, tails)': boundary,
          'body_faces_against_analytic_normals': inward, 'height_m (sole to puff top)': H_M, 'unit_mm': round(U * 1000, 3),
          'hand_to_target_mm': ERR, 'faces_rewound_to_analytic_normals': REWOUND, 'hairline_front_view_y_by_deg': HAIRLINE,
          'skin_unweighted': sum(1 for v in body.data.vertices if not v.groups),
          'cup_centres_sketch': {k: [round(c, 1) for c in v[2]] for k, v in CUP_AT.items()}, 'strokes': len(STROKES)}
meshes = [o.name for o in bpy.data.objects if o.type == 'MESH']
report = {'triangles': counts, 'meshes': {'all': meshes, 'non_swap (<= 3)': ['body', 'decals'], 'swap': list(swaps) + list(props)},
          'checks': checks, 'poses': {k: v for k, v in POSES.items()}}
print('JUNO_REPORT', json.dumps(counts['visible']), json.dumps(counts['body_by_part']), json.dumps(checks))
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump(TOONJ, open(os.path.join(OUT, 'juno_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, bnc, rig, body, decals] + [s_[0] for s_ in swaps.values()] + list(props.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False, export_vertex_color='ACTIVE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('JUNO_DONE')
