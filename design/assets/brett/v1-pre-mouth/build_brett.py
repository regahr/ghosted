# GHOSTED - Brett Bullet-Points, v1: blockout and final model, built to the accepted sketch (assets/brett/sketch).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_brett.py -- [blockout] [H=1.23] [out=<dir>]
# Brief: design/acceptance/brett/brief.md. Direction and join decisions: direction.md. Based on auntie-dot/v1/build_dot.py.
# Shapes: the outlines and marks come from the sketch's hand-drawn Bezier paths (../sketch/src/brett.py), read here.
# Sketch units: x right (centred X = x - 150), y down (sole y 340, swoop top y 16), Z forward. 1 unit = H / 324 m.
# Blender: Z-up, Brett faces -Y. glTF: Y-up (faces +Z in three.js).
# Nodes: root > float > bounce > rig (body_root, torso, head, halo, arm_L_up, arm_L_lo, arm_R_up, arm_R_lo) > body, decals
#        (skinned, the 2 non-swap meshes); swap parts: eyes, brows, mouths, thumb, fingers.
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import brett as Bt
R = Bt.R
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
H_M = 1.235         # swoop top to sole: blockout 1.23 m gave 77 / 78 px at Kit's spot (target 78.75); 1.25 m -> measure.md
OUT = HERE
for a in ARGV:
    if a.startswith('H='): H_M = float(a[2:])
    if a.startswith('out='): OUT = os.path.join(HERE, a[4:]); os.makedirs(OUT, exist_ok=True)
NAME = 'brett_blockout' if BLOCKOUT else 'brett'
PI = math.pi
U = H_M / 324.0
ROW = Bt.ROW
PAL = {'vest': ROW[7], 'shirt': ROW[23], 'skin': ROW[15], 'hair': ROW[12], 'pants': ROW[26], 'shoe': ROW[5],
       'halo': ROW[2], 'ink': ROW[22], 'white': ROW[23]}
BASIC = ['ink', 'white']
NEUTRAL = [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]]   # Kit's bands2 (neutral grey 178 shade band)
TOONJ = {'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC,
         'outline_nodes': ['body'], 'contact_shadow': {'rx': 0.26 * H_M, 'ry': 0.21 * H_M, 'opacity': 0.25}}

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

# ================================================================ mesh accumulator (= Dot)
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
# Columns: non-uniform, so a column sits just behind each ear (104 deg) and the hairline can drop behind the ear.
HALF = [0, 25, 50, 72, 90, 104, 120, 145] if not BLOCKOUT else [0, 45, 90, 135]
TH_H = [math.radians(a) for a in HALF] + [PI] + [math.radians(-a) for a in reversed(HALF[1:])]
TH_H = sorted(TH_H, key=lambda t: (t if t >= 0 else t + 2 * PI))
HP = R.path_points(Bt.HEAD_HALF, 80); HL = arc(HP)
HEAD_D = 0.92
SKULL_C = 95.0                                   # skull centre (front-view y) for the radial cap projection
def _polar(path):
    pts = [(x - 150.0, y) for x, y in R.path_points(path, 80) if x >= 150.0]
    out = sorted((math.atan2(r, SKULL_C - y), math.hypot(r, SKULL_C - y)) for r, y in pts)
    return out
CAP_POL = _polar(Bt.CAP_HALF)
def cap_rho(phi):
    for (a0, r0), (a1, r1) in zip(CAP_POL, CAP_POL[1:]):
        if a0 <= phi <= a1: return r0 + (r1 - r0) * (phi - a0) / max(a1 - a0, 1e-9)
    return CAP_POL[0][1] if phi < CAP_POL[0][0] else CAP_POL[-1][1]
def head_rz(s, f=0.0):
    """Front-view (radius, y) at arc s on the skull; f blends to the hair cap (radial projection of CAP_HALF)."""
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
# Hairline: front-view y of the hair edge by column angle (deg from the front). Sketch HAIRLINE: y 62 at the centre,
# 84-88 at the temples (front view). In 3D it stays ABOVE the ear (ear top y 83) at the ear column, then drops behind
# the ear to the nape at y 132 (sketch hair_back; builder note: no notch at the far ear).
# Chair rule (2026-11-26, from Rega's feedback on Ricky and Dot): no fringe at the game camera; a clear forehead band of
# at least 4 px at 1x between the hair edge (ink included) and the brows. The sketch's 62 gave 4 px with the ink counted
# as skin, so the front hairline is raised to 56 (measure.md "Forehead band").
HAIRLINE = [(0, 56.0), (25, 57.5), (50, 64.0), (72, 74.0), (90, 79.0), (104, 81.0), (120, 106.0), (145, 124.0), (180, 132.0)]
def hair_y(th):
    d = abs(math.degrees((th + PI) % (2 * PI) - PI))
    for (a0, y0), (a1, y1) in zip(HAIRLINE, HAIRLINE[1:]):
        if a0 <= d <= a1: return y0 + (y1 - y0) * (d - a0) / (a1 - a0)
    return HAIRLINE[-1][1]
INK_BAND = 2.6
S_END = HL[-1] - 7.0
NH = 3 if BLOCKOUT else 4
SKIN_F = [0, 0.5, 1.0] if BLOCKOUT else [0, 0.28, 0.55, 0.8, 1.0]   # 4 skin bands: a rounder jaw
# Tried and dropped (2nd try at the side-profile ticks, stopped by the 'no blind iterations' rule): skin rings at fixed
# face rows (y 70 / 81.5 / 104.5 / 123.5) crossed the per-column fallback rings at the temples, where the hairline is
# lower, and folded faces (ink triangles on the cheek). See selfcheck.md weak point 1.
HAIRLINE_PTS = {}
with shell('head'):
    BODY.bone = 'head'
    pole = BODY.v(B(0, 32.0, 0), (0, 0, 1))                       # cap top (sketch CAP_HALF y 32)
    hair_rings, skin_rings = [], []
    for k in range(1, NH):
        ring = []
        for th in TH_H:
            sh = s_of_y(hair_y(th)); s = sh * (k / NH) ** 0.8
            ring.append(BODY.v(head_pt(th, s, 1.0), head_n(th, s, 1.0)))
        hair_rings.append(ring)
    # the hair thins to the skin AT the hairline (no overhang; Dot lesson); the ink band on the skin carries the edge
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
# ears (layered, half sunk, on the eye line): sketch (+-55, y 93, Z -4), radii (5, 10, 7); pole axis points out
with shell('ears'):
    for s in (1, -1):
        ring = []
        for j in range(8):
            t = 2 * PI * j / 8; ry_, rz_ = 10 * math.cos(t), 7 * math.sin(t)
            ring.append(BODY.v(B(s * 56.0, 93 - ry_, -4 + rz_), Vector((s * 0.35, -math.sin(t), math.cos(t))).normalized(), 'head'))
        fan(BODY, BODY.v(B(s * 61.0, 93, -4), (s, 0, 0), 'head'), ring, 'skin')
        fan(BODY, BODY.v(B(s * 48.0, 93, -4), (-s, 0, 0), 'head'), ring, 'skin')

# ================================================================ SWOOP (layered roll on the cap): tube through WAVE
def perp(d):
    a = Vector((0, 1, 0)) if abs(d.y) < 0.9 else Vector((1, 0, 0))
    u = d.cross(a).normalized(); return u, d.cross(u).normalized()
def tube_rings(pts, radii, n, bone, m, cap_a=True, cap_b=True, acc=None, cap_ring=True):
    """A tube through pts (Blender), round caps at both ends. Ring frames follow the path (parallel transport)."""
    acc = acc or BODY
    dirs = []
    for i in range(len(pts)):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]; dirs.append((b - a).normalized())
    u, w = perp(dirs[0]); frames = []
    for d in dirs:
        u = (u - d * u.dot(d)).normalized(); w = d.cross(u).normalized(); frames.append((u, w))
    def ring(c, r, d, fr, nax=0.0):
        uu, ww = fr; ids = []
        for k in range(n):
            t = 2 * PI * k / n; rd = uu * math.cos(t) + ww * math.sin(t)
            ids.append(acc.v(c + rd * r, rd * math.sqrt(1 - nax ** 2) + d * nax, bone))
        return ids
    rings = []
    if cap_a is True:
        d0 = dirs[0]; pa = acc.v(pts[0] - d0 * radii[0], -d0, bone)
        if cap_ring: rings.append(ring(pts[0] - d0 * radii[0] * 0.7071, radii[0] * 0.7071, d0, frames[0], -0.7071))
    for p, r, d, fr in zip(pts, radii, dirs, frames): rings.append(ring(p, r, d, fr))
    if cap_b is True and cap_ring:
        d1 = dirs[-1]; rings.append(ring(pts[-1] + d1 * radii[-1] * 0.7071, radii[-1] * 0.7071, d1, frames[-1], 0.7071))
    bands(acc, rings, [m] * (len(rings) - 1), flip=True)
    if cap_a is True: fan(acc, pa, rings[0], m, flip=False)
    elif cap_a == 'flat': fan(acc, acc.v(pts[0], -dirs[0], bone), rings[0], m)
    if cap_b is True: fan(acc, acc.v(pts[-1] + dirs[-1] * radii[-1], dirs[-1], bone), rings[-1], m, flip=True)
    elif cap_b == 'flat': fan(acc, acc.v(pts[-1], dirs[-1], bone), rings[-1], m)
with shell('swoop'):
    # sketch WAVE with its root lifted 6 and set back 4 (and the next point 3 / 2): it rises up and back from the part
    # and stays above the raised hairline (chair rule: the swoop goes up and back, not down over the forehead)
    WAVE3 = [(-28, 44, 30)] + [(-10, 33, 36)] + list(Bt.WAVE[2:])
    wv, wr = Bt.smooth(WAVE3, Bt.WAVE_R, k=1 if BLOCKOUT else 2)
    tube_rings([B(*p) for p in wv], [r * U for r in wr], 6 if BLOCKOUT else 7, 'head', 'hair', cap_ring=False)

# ================================================================ HALO (#OpenToWork ring): torus on the halo bone
HALO_C = (0.0, 0.0, 0.0); HALO_RX, HALO_RZ, HALO_T = 38.0, 30.0, 6.0
with shell('halo'):
    NU, NV = (10, 4) if BLOCKOUT else (12, 5)
    rings = []
    for i in range(NU):
        a = 2 * PI * i / NU
        cx, cz = HALO_RX * math.sin(a), HALO_RZ * math.cos(a)
        tx, tz = HALO_RX * math.cos(a), -HALO_RZ * math.sin(a)                  # tangent
        ox, oz = tz, -tx; ol = math.hypot(ox, oz); ox, oz = ox / ol, oz / ol      # outward in the ring plane
        if ox * cx + oz * cz < 0: ox, oz = -ox, -oz
        ids = []
        for j in range(NV):
            b = 2 * PI * j / NV
            dx, dyu, dz = ox * math.cos(b), math.sin(b), oz * math.cos(b)        # dyu: up
            p = B(cx + HALO_T * dx, HALO_C[1] - HALO_T * dyu, cz + HALO_T * dz)
            ids.append(BODY.v(p, (dx, -dz, dyu), 'halo'))
        rings.append(ids)
    bands(BODY, rings + [rings[0]], ['halo'] * NU, flip=True)

# ================================================================ NECK (separate, sunk)
with shell('neck'):
    rings = []
    for (y, r) in ((130.0, 16.0), (156.0, 13.0)):     # tapers into the vest opening (r 14)
        ids = []
        for k in range(8):
            t = 2 * PI * k / 8; ids.append(BODY.v(B(r * math.sin(t), y, 0.9 * r * math.cos(t)), (math.sin(t), -math.cos(t), 0), 'torso'))
        rings.append(ids)
    bands(BODY, rings, ['skin'], flip=True)

# ================================================================ VEST: the wedge (sketch VEST_WEDGE), depth 0.64
TH = [2 * PI * j / (10 if BLOCKOUT else 16) for j in range(10 if BLOCKOUT else 16)]
JP = R.path_points(Bt.VEST_WEDGE, 30)
JP = JP[:JP.index(min(JP, key=lambda p: math.dist(p, (186.0, 252.0)))) + 1]   # stop at the hem corner (186, 252)
JL = arc(JP); VEST_D = Bt.VEST_D
def jpt(th, s):
    x, y = at_len(JP, JL, s); r = x - 150.0
    return B(r * math.sin(th), y, VEST_D * r * math.cos(th))
def jn(th, s):
    e = 0.02; pt = jpt(th + e, s) - jpt(th - e, s); ps = jpt(th, min(s + 0.4, JL[-1])) - jpt(th, max(s - 0.4, 0))
    n = ps.cross(pt).normalized(); c = jpt(th, s)
    return n if n.dot(c - Vector((0, 0, c.z))) > 0 else -n
def s_at_y(y):
    for i in range(len(JP) - 1):
        if JP[i][1] <= y <= JP[i + 1][1] and JP[i + 1][1] > JP[i][1]:
            f = (y - JP[i][1]) / (JP[i + 1][1] - JP[i][1]); return JL[i] + (JL[i + 1] - JL[i]) * f
    return JL[-1]
VY = [150.0, 156, 168, 188, 214, 238] if BLOCKOUT else [150.0, 153, 160, 172, 192, 222]
J_S = [s_at_y(y) for y in VY] + [JL[-1]]
with shell('vest'):
    BODY.bone = 'torso'
    rings = [[BODY.v(jpt(th, s), jn(th, s)) for th in TH] for s in J_S]
    bands(BODY, rings, ['vest'] * (len(rings) - 1))
    fan(BODY, BODY.v(B(0, 252, 0), (0, 0, -1)), rings[-1], 'vest')
VPROF = [p for p in R.profile(Bt.VEST_WEDGE) if p[0] < 251.9] + [(252.0, 36.0)]
def surf_z(x, y, out=0.0):
    r = R.r_at(VPROF, y); return r * VEST_D * math.sqrt(max(1 - (x / max(r, 1e-3)) ** 2, 0.0)) + out

# ================================================================ HIPS (chinos band under the hem), depth 0.8
HPP = R.path_points(Bt.HIPS, 30); HPL = arc(HPP)
def hpt(th, s):
    x, y = at_len(HPP, HPL, s); r = x - 150.0
    return B(r * math.sin(th), y, 0.8 * r * math.cos(th))
with shell('hips'):
    THh = [2 * PI * j / 10 for j in range(10)]
    ss = [HPL[-1] * f for f in ((0.18, 0.5, 0.8) if not BLOCKOUT else (0.25, 0.75))]
    rings = []
    for s in ss:
        ids = []
        for th in THh:
            p = hpt(th, s); c = Vector((0, 0, p.z)); ids.append(BODY.v(p, (p - c).normalized()))
        rings.append(ids)
    bands(BODY, rings, ['pants'] * (len(rings) - 1))
    fan(BODY, BODY.v(B(0, 268, 0), (0, 0, -1)), rings[-1], 'pants')

# ================================================================ ARMS (join: sunk sleeve root, rigid ball elbow, hand ball)
ARM_SIDES = 6 if BLOCKOUT else 7
ARM = {}
for s, side in ((1, 'L'), (-1, 'R')):           # L = his left = viewer-right = +X
    S_ = (s * 56, 176.0, 0.0); E_ = (s * 74, 212.0, 0.0); W_ = (s * 76, 244.0, 4.0); Hd = (s * 76, 254.0, 6.0)   # brett.py "rest"
    ARM[side] = {'S': B(*S_), 'E': B(*E_), 'W': B(*W_), 'H': B(*Hd), 'sx': s}
HAND_R = 10.5
for side, a in ARM.items():
    with shell('arm_' + side):
        tube_rings([a['S'], a['E']], [12.0 * U, 11.0 * U], ARM_SIDES, 'arm_%s_up' % side, 'shirt', cap_a='flat')
        endp = a['H'] + (a['W'] - a['H']).normalized() * 7.0 * U       # the sleeve end sinks into the hand ball
        tube_rings([a['E'], a['W'], endp], [11.0 * U, 10.2 * U, 10.0 * U], ARM_SIDES, 'arm_%s_lo' % side, 'shirt', cap_b='flat')
        X, y, Z = S(a['H'])
        ellipsoid((X, y, Z), (HAND_R, HAND_R, 10), ARM_SIDES if not BLOCKOUT else 6, [45, 0, -45] if not BLOCKOUT else [0], 'skin', 'arm_%s_lo' % side)   # a round fist

# ================================================================ LEGS + SHOES (body_root: planted in the idle)
with shell('legs'):
    for s in (1, -1):
        rings = []
        for (y, r) in ((256.0, 14.0), (328.0, 13.0)):
            ids = []
            for k in range(6):
                t = 2 * PI * k / 6; ids.append(BODY.v(B(s * 20 + r * math.sin(t), y, r * math.cos(t)), (math.sin(t), -math.cos(t), 0), 'body_root'))
            rings.append(ids)
        bands(BODY, rings, ['pants'] * (len(rings) - 1), flip=True)
        ellipsoid((s * 21, 329.0, 9), (13.5, 8.5, 21), 8 if not BLOCKOUT else 6, [20, -30], 'shoe', 'body_root')   # sole 337.5

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
# Outline weight (Kit method: colour attribute 'outline_wc', glTF COLOR_0, read by ingame.html and render_brett.py).
# The neck ink fades to 0 at its buried end, so the neck line where it enters the vest is thin (a full-width ring there
# merged with the collar edges into a dark 'bow tie').
v0n, v1n = SHELLS['neck'][0], SHELLS['neck'][1]
NECK_Y = {}
body.data.color_attributes.new('outline_wc', 'FLOAT_COLOR', 'POINT')
_ca = body.data.color_attributes['outline_wc']
for nv, ov in enumerate(BUSED):
    w = 1.0
    if v0n <= ov < v1n: w = 1.0 if S(BODY.V[ov])[1] < 140 else 0.0
    if SHELLS['vest'][0] <= ov < SHELLS['vest'][1] and S(BODY.V[ov])[1] < 151.0: w = 0.0   # the vest top ring (round the neck): no ink wedge at the neckline
    _ca.data[nv].color = (w, w, w, 1.0)
_ci = body.data.color_attributes.find('outline_wc')
body.data.color_attributes.active_color_index = _ci; body.data.color_attributes.render_color_index = _ci

# ================================================================ DECALS (projected on the analytic head, cap and vest)
# The vest top ring is r 14 at y 150 (inside the neck): the collar marks there need a surface in FRONT of the neck
# (neck front Z 14.4), so the vest profile used for the marks is never narrower than r 26 above y 156.
VPROF_M = [(140.0, 26.0)] + [(y, max(r, 26.0)) if y < 156 else (y, r) for y, r in VPROF]
SURF = {'head': (R.profile(Bt.HEAD_HALF), HEAD_D), 'cap': (R.profile(Bt.CAP_HALF), HEAD_D), 'vest': (VPROF_M, VEST_D)}
def shell_tree(names):
    F = [f for nm in names for f in BODY.F[SHELLS[nm][2]:SHELLS[nm][3]]]
    tris = []
    for f in F: tris += [f] if len(f) == 3 else [[f[0], f[1], f[2]], [f[0], f[2], f[3]]]
    return BVHTree.FromPolygons([tuple(v) for v in BODY.V], tris)
# Decals sit on the ANALYTIC surface (it is never below the facets, so a decal triangle cannot sink between rings).
# Tried and dropped: a ray hit on the faceted mesh put the vertices ON the facets, and every decal triangle that
# spanned a ridge sank under it (broken eyes, brows and V; build note in selfcheck.md).
RAY_HEAD = None
RAY_ON = False
def front_hit(tree, X, y, off):
    global RAY_HEAD
    if tree == 'head' and RAY_ON:                # off: see the note at SKIN_F
        if RAY_HEAD is None: RAY_HEAD = shell_tree(['head'])
        hit = RAY_HEAD.ray_cast(B(X, y, 300.0), Vector((0, 1, 0)))
        if hit[0] is not None:
            n = hit[1] if hit[1].y < 0 else -hit[1]
            return hit[0] + n * off * U, n
    prof, dep = SURF[tree]
    r = R.r_at(prof, y); Xc = max(-r * 0.999, min(r * 0.999, X)); Z = dep * math.sqrt(max(r * r - Xc * Xc, 0.0))
    e = 0.25; r1, r0 = R.r_at(prof, y + e), R.r_at(prof, y - e); drdy = (r1 - r0) / (2 * e)
    gX, gy, gZ = 2 * Xc, -2 * r * drdy, 2 * Z / dep ** 2
    nb = Vector((gX, -gZ, -gy)).normalized()
    return B(Xc, y, Z) + nb * off * U, nb
DEC = Acc('torso')
SWAP_NAMES = ('eyes_open', 'eyes_wink', 'brows_rest', 'brows_smug', 'brows_lost', 'mouth_grin', 'mouth_talk', 'mouth_lost')
SWAP = {k: Acc('head') for k in SWAP_NAMES}
HANDS = {k: Acc('arm_R_lo') for k in ('thumb', 'fingers_1', 'fingers_2', 'fingers_3')}
def clean(pts):
    out = []
    for p in pts:
        if not out or math.dist(p, out[-1]) > 0.3: out.append(p)
    if math.dist(out[0], out[-1]) < 0.3: out.pop()
    return out
def offset2d(pts, d):
    n = len(pts); area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2
    sg = 1 if area > 0 else -1; out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nr(a, b):
            ddx, ddy = b[0] - a[0], b[1] - a[1]; L = math.hypot(ddx, ddy) or 1; return (sg * ddy / L, -sg * ddx / L)
        n1, n2 = nr(p0, p1), nr(p1, p2); m = (n1[0] + n2[0], n1[1] + n2[1]); ml = math.hypot(*m) or 1; m = (m[0] / ml, m[1] / ml)
        ch = max(0.9, m[0] * n1[0] + m[1] * n1[1]); out.append((p1[0] + m[0] * d / ch, p1[1] + m[1] * d / ch))
    return out
def fan_card(acc, tree, pts2d, off, m, bone=None, centre=None):
    cx, cy = centre or (sum(p[0] for p in pts2d) / len(pts2d), sum(p[1] for p in pts2d) / len(pts2d))
    c = acc.v(front_hit(tree, cx - 150, cy, off)[0], (0, -1, 0), bone)
    ring = [acc.v(front_hit(tree, x - 150, y, off)[0], (0, -1, 0), bone) for x, y in pts2d]
    for j in range(len(ring)): acc.f([c, ring[j], ring[(j + 1) % len(ring)]], m)
def strip_card(acc, tree, top, bot, off, m, bone=None):
    """A filled band between two polylines with the same point count (a crescent)."""
    T = [acc.v(front_hit(tree, x - 150, y, off)[0], (0, -1, 0), bone) for x, y in top]
    Bo = [acc.v(front_hit(tree, x - 150, y, off)[0], (0, -1, 0), bone) for x, y in bot]
    for i in range(len(T) - 1): acc.f([T[i], T[i + 1], Bo[i + 1]], m); acc.f([T[i], Bo[i + 1], Bo[i]], m)
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
def bez_pts(d, n):
    return R.path_points(d, n)
EY = Bt.LM['eye']
# face (head bone): eyes with glints; the wink closes his left eye (x 168)
for k, ex in enumerate(Bt.LM['eye_x']):
    for nm in ('eyes_open', 'eyes_wink'):
        if nm == 'eyes_wink' and k == 1:
            line_card(SWAP[nm], 'head', bez_pts(Bt.WINK, 4), 3.4, 0.4, 'ink'); continue
        fan_card(SWAP[nm], 'head', clean(bez_pts(R.oval(ex, EY, 6.5, 9.0), 3)), 0.4, 'ink')
        if not BLOCKOUT: fan_card(SWAP[nm], 'head', clean(bez_pts(R.oval(ex + 2, EY - 3.4, 2.0, 2.4), 2)), 0.6, 'white')
for nm, br in (('brows_rest', Bt.BROWS), ('brows_smug', Bt.BROWS_SMUG), ('brows_lost', Bt.BROWS_LOST)):
    for d in br: line_card(SWAP[nm], 'head', bez_pts(d, 3), 2.8, 0.4, 'ink')
# the GRIN (chair call 5): white teeth crescent with no edge, over an ink smile line with the corners up
GRIN_TOP = bez_pts("M124,106 C138,110 162,110 176,106", 6 if not BLOCKOUT else 4)
GRIN_BOT = list(reversed(bez_pts("M176,106 C170,118 160,121 150,121 C140,121 130,118 124,106", 3 if not BLOCKOUT else 2)))
def resample(pts, n):
    L = arc(pts); return [at_len(pts, L, L[-1] * i / (n - 1)) for i in range(n)]
NG = 7 if not BLOCKOUT else 5
strip_card(SWAP['mouth_grin'], 'head', resample(GRIN_TOP, NG), resample(GRIN_BOT, NG), 0.5, 'white')
GRIN_W = 3.0
line_card(SWAP['mouth_grin'], 'head', bez_pts(Bt.GRIN_LINE, 6 if not BLOCKOUT else 4), GRIN_W, 0.7, 'ink')
fan_card(SWAP['mouth_talk'], 'head', clean(bez_pts(Bt.TALK, 3)), 0.5, 'ink')
fan_card(SWAP['mouth_talk'], 'head', clean(bez_pts(Bt.TALK_TEETH, 2)), 0.7, 'white')
line_card(SWAP['mouth_lost'], 'head', bez_pts(Bt.LOST_MOUTH, 3), 2.6, 0.5, 'ink')
# the side part (on the cap; trimmed above the hair taper at the hairline)
if not BLOCKOUT:
    pp = [p for p in bez_pts(Bt.PART, 4) if p[1] <= 53.0]
    line_card(DEC, 'cap', pp, 1.8, 0.6, 'ink', bone='head')
# vest marks (torso): shirt V (white, ink edge), skin V, V ribs, collar wings (white, ink edge), hem rib
def edged(acc, tree, d, fill, edge_w, off, n=3):
    pts = clean(bez_pts(d, n))
    if edge_w: fan_card(acc, tree, offset2d(pts, edge_w), off, 'ink')
    fan_card(acc, tree, pts, off + 0.25, fill)
VOFF = 1.0          # lifted: the vest chords (16 columns) must not cut the marks
# the shirt V as two strips (left edge, centre line, right edge): small triangles, so no part of it sinks under the
# 16-column vest (one big fan did: the vest showed through as a red diamond)
def v_strips(acc, dx, tip, off, m, n=7):
    Lp = resample(list(reversed(bez_pts("M150,198 C143,186 137,170 134,151", 6))), n)
    Rp = resample(bez_pts("M166,151 C163,170 157,186 150,198", 6), n)
    Lp = [(x - dx * (1 - i / (n - 1)), y) for i, (x, y) in enumerate(Lp)]; Rp = [(x + dx * (1 - i / (n - 1)), y) for i, (x, y) in enumerate(Rp)]
    Lp[-1] = (150.0, 198.0 + tip); Rp[-1] = (150.0, 198.0 + tip)
    Cp = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + (3.0 - dx if i == 0 else 0)) for i, (a, b) in enumerate(zip(Lp, Rp))]
    strip_card(acc, 'vest', Lp, Cp, off, m); strip_card(acc, 'vest', Cp, Rp, off, m)
v_strips(DEC, 0.0, 0.0, VOFF + 0.25, 'shirt')
if not BLOCKOUT:
    fan_card(DEC, 'vest', clean(bez_pts(Bt.SKIN_V, 2)), VOFF + 0.8, 'skin')
    for d in Bt.V_RIB: line_card(DEC, 'vest', bez_pts(d, 3), 1.6, VOFF + 0.8, 'ink')   # over the V edge: its ink
    # Collar wings: one fan each, thin ink edge. Tried and dropped (stop rule): strips between the top and lower edges
    # lost the wing tip and let the vest show through. Open weak point: a dark ink wedge at each wing's top corner.
    for d in Bt.COLLAR: edged(DEC, 'vest', d, 'shirt', 0.7, VOFF + 1.1, n=2)
    line_card(DEC, 'vest', bez_pts(Bt.HEM_RIB, 4), 1.4, VOFF, 'ink')
LAND = {'eye_top': front_hit('head', Bt.LM['eye_x'][0] - 150, EY - 9.0, 0.4)[0],
        'mouth': front_hit('head', 0, 114, 0.5)[0], 'v_point': front_hit('vest', 0, 198, 1.0)[0]}
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
bh = arm_d.edit_bones.new('head'); bh.head = B(0, 146, 0); bh.tail = B(0, 60, 0); bh.parent = bt
bha = arm_d.edit_bones.new('halo'); bha.head = B(*HALO_C); bha.tail = B(0, -30, 0); bha.parent = bh
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
DEFAULT_ON = ('eyes_open', 'brows_rest', 'mouth_grin')
for k, (o, _, used) in swaps.items():
    skin(o, SWAP[k], used); o['variant'] = k; o['default_visible'] = k in DEFAULT_ON
for k, v in LAND.items(): decals[k + '_rest_blender'] = list(v)

# ---------------------------------------------------------------- poses: two-bone reach, stored as axis + angle (Dot)
def solve(side, T, pole):
    a = ARM[side]; S0, E, H = a['S'], a['E'], a['H']
    L1, L2 = (E - S0).length, (H - E).length; d = min((T - S0).length, L1 + L2 - 1e-4); dT = (T - S0).normalized()
    aa = (L1 * L1 - L2 * L2 + d * d) / (2 * d); hh = math.sqrt(max(L1 * L1 - aa * aa, 0.0))
    pp = (pole - dT * pole.dot(dT)).normalized(); E2 = S0 + dT * aa + pp * hh
    R1 = (E - S0).rotation_difference(E2 - S0); H1 = S0 + R1 @ (H - S0)
    R2w = (H1 - E2).rotation_difference(T - E2)
    ax2 = R1.inverted() @ R2w.axis
    return ({'arm_%s_up' % side: [*R1.axis, math.degrees(R1.angle)], 'arm_%s_lo' % side: [*ax2, math.degrees(R2w.angle)]},
            {'R1': R1, 'R2w': R2w, 'E2': E2, 'S': S0})
# hips (the idle): both fists on the waist, elbows out (brett.py "hips")
# a bit higher and in than brett.py (50, 246): the elbows go further out
HIPS_T = {s: B(s * 46, 240, 12) for s in (1, -1)}; HIPS_EL = {s: B(s * 96, 214, -4) for s in (1, -1)}
hipsL, _ = solve('L', HIPS_T[1], HIPS_EL[1] - ARM['L']['S'])
hipsR, _ = solve('R', HIPS_T[-1], HIPS_EL[-1] - ARM['R']['S'])
idle = {**hipsL, **hipsR}
# the Like: his right fist out at the side, thumb up (brett.py "thumb"); the left arm stays at rest
LIKE_T = B(-96, 172, 20); LIKE_EL = B(-88, 212, 10)
like, LIKE_X = solve('R', LIKE_T, LIKE_EL - ARM['R']['S'])
# bullets: his right hand up beside the chest (brett.py "count"), the left fist on the hip
BUL_T = B(-82, 176, 28); BUL_EL = B(-84, 216, 12)
bul, BUL_X = solve('R', BUL_T, BUL_EL - ARM['R']['S'])
bullets = {**hipsL, **bul}
POSES = {'idle': idle, 'like': like, 'bullets': bullets}
CARRY = {'head': [1.0, 0.0, 0.0, -10.0], 'halo': [1.0, 0.0, 0.0, 10.0]}       # chin up 10 deg; the halo stays level
PUFF = {'torso': [1.0, 0.0, 0.0, -3.0], 'rise_units': 3.0}                     # lean back 3 deg about the feet, rise 3 u
flt['poses_float_blender'] = POSES
flt['carry_float_blender'] = CARRY
flt['puff'] = {'torso_float_blender': PUFF['torso'], 'rise_m': PUFF['rise_units'] * U, 'period_s': 2.0,
               'rule': 'idle: hands on hips; puff = torso -3 deg about the feet (back) + rise 3 units; legs and shoes stay on body_root'}
flt['height_m'] = H_M; flt['unit_m'] = U
flt['expressions'] = {'rest': ['eyes_open', 'brows_rest', 'mouth_grin'], 'talk': ['eyes_open', 'brows_rest', 'mouth_talk'],
                      'wink': ['eyes_wink', 'brows_smug', 'mouth_grin'], 'lost': ['eyes_open', 'brows_lost', 'mouth_lost']}
flt['beat_defaults'] = {'idle': {'expr': 'rest'}, 'like': {'expr': 'wink', 'hand': 'thumb'}, 'bullets': {'expr': 'talk', 'hand': 'fingers_3'}}

# ================================================================ THUMB and FINGERS (swap parts on arm_R_lo, built in the beat's frame)
def unposer(X_):
    def un(p):
        q = X_['R2w'].inverted() @ (p - X_['E2']) + X_['E2']
        return X_['R1'].inverted() @ (q - X_['S']) + X_['S']
    return un
def build_hand(name, parts, X_):
    acc = HANDS[name]; un = unposer(X_); v0 = len(acc.V)
    for a, b, r0, r1, n in parts: tube_rings([B(*a), B(*b)], [r0 * U, r1 * U], n, 'arm_R_lo', 'skin', acc=acc, cap_a=False, cap_ring=False)   # the root is inside the fist
    Rn = X_['R1'].inverted() @ X_['R2w'].inverted()
    for i in range(v0, len(acc.V)): acc.V[i] = un(acc.V[i]); acc.N[i] = Rn @ acc.N[i]
tx, ty, tz = S(LIKE_T)
build_hand('thumb', [((tx, ty - 4, tz + 3), (tx, ty - 26, tz + 3), 6.2, 5.6, 6)], LIKE_X)
bx, by, bz = S(BUL_T)
for nf in (1, 2, 3):
    build_hand('fingers_%d' % nf, [((bx + (f - (nf - 1) / 2) * 6.5, by - 6, bz + 3), (bx + (f - (nf - 1) / 2) * 6.5, by - 21, bz + 3), 3.0, 2.8, 4)
                                   for f in range(nf)], BUL_X)
hands = {}
for k, acc in HANDS.items():
    orient_acc(acc)
    ob, _, used = make_mesh(k, acc); ob.data.normals_split_custom_set_from_vertices([tuple(acc.N[i]) for i in used]); ob.data.update()
    skin(ob, acc, used); ob['variant'] = k; ob['default_visible'] = False; hands[k] = ob

def pose(name=None, carry=False, puff=0.0):
    for pb in rig.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    P = dict(flt['poses_float_blender'][name].to_dict()) if name else {}
    if carry: P.update(dict(flt['carry_float_blender'].to_dict()))
    if puff: P['torso'] = list(PUFF['torso'][:3]) + [PUFF['torso'][3] * puff]
    for bn, (x, y, z, deg) in P.items():
        M = rig.data.bones[bn].matrix_local.to_3x3().inverted()
        rig.pose.bones[bn].rotation_quaternion = Quaternion(M @ Vector((x, y, z)), math.radians(deg))
    if puff: rig.pose.bones['torso'].location = (0, PUFF['rise_units'] * U * puff, 0)
    bpy.context.view_layer.update()
def hand_now():
    pb = rig.pose.bones['arm_R_lo']; return (rig.matrix_world @ pb.matrix) @ (rig.data.bones['arm_R_lo'].matrix_local.inverted() @ ARM['R']['H'])
def bone_world_axis(bn, v):
    pb = rig.pose.bones[bn]; return ((rig.matrix_world @ pb.matrix).to_3x3() @ (rig.data.bones[bn].matrix_local.to_3x3().inverted() @ Vector(v))).normalized()
pose('like'); like_err = (hand_now() - LIKE_T).length
pose('bullets'); bul_err = (hand_now() - BUL_T).length
pose('idle'); hL = rig.pose.bones['arm_L_lo']; hips_err = ((rig.matrix_world @ hL.matrix) @ (rig.data.bones['arm_L_lo'].matrix_local.inverted() @ ARM['L']['H']) - HIPS_T[1]).length
# carriage check: the ring's up axis after the chin-up must equal world up; the eye must move forward-up (chin up)
pose(None); eye0 = (rig.matrix_world @ rig.pose.bones['head'].matrix) @ (rig.data.bones['head'].matrix_local.inverted() @ LAND['eye_top'])
pose(None, carry=True)
halo_up = bone_world_axis('halo', (0, 0, 1)); head_up = bone_world_axis('head', (0, 0, 1))
eye1 = (rig.matrix_world @ rig.pose.bones['head'].matrix) @ (rig.data.bones['head'].matrix_local.inverted() @ LAND['eye_top'])
hc0 = B(*HALO_C); hc1 = (rig.matrix_world @ rig.pose.bones['halo'].matrix) @ (rig.data.bones['halo'].matrix_local.inverted() @ hc0)
pose(None)

# ================================================================ REPORT + EXPORT
def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {'body': tris(body), 'decals': tris(decals)}
for k, (o, _, _) in swaps.items(): counts[k] = tris(o)
for k, o in hands.items(): counts[k] = tris(o)
base = counts['body'] + counts['decals']
def vis(eyes, brows, mouth, hand=None): return base + counts[eyes] + counts[brows] + counts[mouth] + (counts[hand] if hand else 0)
counts['visible'] = {'rest / idle (grin)': vis('eyes_open', 'brows_rest', 'mouth_grin'),
                     'like (wink + thumb)': vis('eyes_wink', 'brows_smug', 'mouth_grin', 'thumb'),
                     'bullets (talk + 3 fingers)': vis('eyes_open', 'brows_rest', 'mouth_talk', 'fingers_3'),
                     'talk': vis('eyes_open', 'brows_rest', 'mouth_talk'), 'lost': vis('eyes_open', 'brows_lost', 'mouth_lost')}
counts['body_by_part'] = {nm: sum(len(f) - 2 for f in BODY.F[f0:f1]) for nm, (v0, v1, f0, f1) in SHELLS.items()}
checks = {'body_nonmanifold_edges': nonman, 'body_boundary_edges (neck tube ends, vest top ring, hips top, leg ends)': boundary,
          'body_faces_against_analytic_normals': inward, 'height_m (sole to swoop top)': H_M, 'unit_mm': round(U * 1000, 3),
          'like_hand_centre_to_target_mm': round(like_err * 1000, 2), 'bullets_hand_centre_to_target_mm': round(bul_err * 1000, 2),
          'hips_left_hand_to_target_mm': round(hips_err * 1000, 2), 'faces_rewound_to_analytic_normals': REWOUND,
          'hairline_front_view_y_by_deg': HAIRLINE, 'skin_unweighted': sum(1 for v in body.data.vertices if not v.groups),
          'carry_halo_up_vs_world_up_deg': round(math.degrees(halo_up.angle(Vector((0, 0, 1)))), 3),
          'carry_head_up_vs_world_up_deg': round(math.degrees(head_up.angle(Vector((0, 0, 1)))), 3),
          'carry_eye_move_mm (x, y fwd=-, z up)': [round(v * 1000, 1) for v in (eye1 - eye0)],
          'carry_halo_centre_move_mm': [round(v * 1000, 1) for v in (hc1 - hc0)]}
meshes = [o.name for o in bpy.data.objects if o.type == 'MESH']
report = {'triangles': counts, 'meshes': {'all': meshes, 'non_swap (<= 3)': ['body', 'decals'],
          'swap': list(swaps) + list(hands)}, 'checks': checks, 'poses': {k: v for k, v in POSES.items()}, 'carry': CARRY}
print('BRETT_REPORT', json.dumps(counts['visible']), json.dumps(counts['body_by_part']), json.dumps(checks))
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump(TOONJ, open(os.path.join(OUT, 'brett_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, bnc, rig, body, decals] + [s_[0] for s_ in swaps.values()] + list(hands.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False, export_vertex_color='ACTIVE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('BRETT_DONE')
