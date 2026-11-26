# GHOSTED - Auntie Dot, v1: blockout and final model, built to the accepted sketch (assets/auntie-dot/sketch).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_dot.py -- [blockout] [H=1.00] [out=<dir>]
# Brief: design/acceptance/auntie-dot/brief.md. Direction and join decisions: direction.md. Based on ricky/v1/build_ricky.py.
# Shapes: the outlines and marks come from the sketch's hand-drawn Bezier paths (../sketch/src/dot.py), read here.
# Sketch units: x right (centred X = x - 150), y down (sole y 340, bun top y 40), Z forward. 1 unit = H / 300 m.
# Blender: Z-up, Dot faces -Y. glTF: Y-up (faces +Z in three.js).
# Nodes: root > float > bounce > rig (body_root, torso, head, arm_L_up, arm_L_lo, arm_R_up, arm_R_lo) > body, decals
#        (skinned, the 2 non-swap meshes); swap parts eyes_open, eyes_happy, mouth_smile, mouth_talk; prop card.
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import dot as D
R = D.R
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
H_M = 0.98          # bun top to sole: blockout 1.00 m gave 68 px, the final (10-column bun) 69 px; 0.98 m -> measure.md
OUT = HERE
for a in ARGV:
    if a.startswith('H='): H_M = float(a[2:])
    if a.startswith('out='): OUT = os.path.join(HERE, a[4:]); os.makedirs(OUT, exist_ok=True)
NAME = 'dot_blockout' if BLOCKOUT else 'dot'
PI = math.pi
U = H_M / 300.0
ROW = D.ROW
PAL = {'dress': ROW[11], 'skin': ROW[15], 'hair': ROW[23], 'acc': ROW[27], 'shoe': ROW[5], 'card': ROW[23],
       'cardedge': ROW[24], 'gold': ROW[13], 'ink': ROW[22], 'white': ROW[23], 'brow': ROW[22],
       'hairink': ROW[22]}       # hairink = the hairline ink band (own material: the game-camera mask measures it)
BASIC = ['ink', 'white', 'brow', 'hairink']
NEUTRAL = [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]]   # Kit's bands2 (neutral grey 178 shade band)
TOONJ = {'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC,
         'outline_nodes': ['body', 'card'], 'contact_shadow': {'rx': 0.30 * H_M, 'ry': 0.25 * H_M, 'opacity': 0.25}}

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

# ================================================================ mesh accumulator
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
def open_bands(acc, rings, m):
    """Quads between consecutive OPEN rings (a tube along a path: each ring is one cross-section)."""
    for r in range(len(rings) - 1):
        A, Bn = rings[r], rings[r + 1]; n = len(A)
        for j in range(n):
            j1 = (j + 1) % n; acc.f([A[j], A[j1], Bn[j1], Bn[j]], m)
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

# ================================================================ HEAD + HAIR: one surface (join: continuous skin)
# Columns: non-uniform, so a column sits just behind each ear (104 deg) and the hairline can drop behind the ear.
HALF = [0, 25, 50, 72, 90, 104, 120, 145] if not BLOCKOUT else [0, 45, 90, 135]
TH_H = [math.radians(a) for a in HALF] + [PI] + [math.radians(-a) for a in reversed(HALF[1:])]
TH_H = sorted(TH_H, key=lambda t: (t if t >= 0 else t + 2 * PI))       # 0 .. 2pi round the head
COLS = 8 if BLOCKOUT else 16
TH = [2 * PI * j / COLS for j in range(COLS)]                           # theta 0 = front, +90 = her left (+X)
HP = R.path_points(D.HEAD_HALF, 80); HL = arc(HP)
HEAD_D = 0.92
def head_pt(th, s):
    x, y = at_len(HP, HL, s); r = x - 150.0
    return B(r * math.sin(th), y, HEAD_D * r * math.cos(th))
def head_n(th, s):
    e = 0.02
    if s < 0.5: return Vector((0, 0, 1))
    if s > HL[-1] - 0.5: return Vector((0, 0, -1))
    pt = head_pt(th + e, s) - head_pt(th - e, s); ps = head_pt(th, min(s + 0.4, HL[-1])) - head_pt(th, s - 0.4)
    n = ps.cross(pt).normalized()
    c = head_pt(th, s); ax = Vector((0, 0, c.z))
    return n if n.dot(c - ax) > 0 else -n
def s_of_y(y):
    for i in range(len(HP) - 1):
        if HP[i][1] <= y <= HP[i + 1][1] and HP[i + 1][1] > HP[i][1]:
            f = (y - HP[i][1]) / (HP[i + 1][1] - HP[i][1]); return HL[i] + (HL[i + 1] - HL[i]) * f
    return HL[-1]
# Hairline: front-view y of the hair edge by column angle (deg from the front). Sketch HAIRLINE (soft waves, y 88-89
# at the centre, 112-116 at the temples); it stays above the ear (top y 118) until the column behind the ear (104),
# then curves down behind the ear to the nape (chair call 2; sketch notes "curve the side hairline down").
# NO FRINGE (Rega ts 1795658373.096399 and ts 1795658703.410809): the FRONT is as the sketch (y 89, Rega: "this part
# is fine"); the SIDES are pulled up and back: the temple hair stays far above the eye line (eye top y 117.5) and the
# hair drops only behind the ear (ear back at ~102 deg), from the 120-deg column on (was: 113-115 at 90-104 deg, and
# down to 143 at 120 deg, which ran down beside the eyes at the game camera).
HAIRLINE = [(0, 89.0), (25, 89.0), (50, 94.0), (72, 98.0), (90, 100.0), (104, 103.0), (120, 117.0), (145, 150.0), (180, 167.0)]
def hair_y(th):
    d = abs(math.degrees((th + PI) % (2 * PI) - PI))
    for (a0, y0), (a1, y1) in zip(HAIRLINE, HAIRLINE[1:]):
        if a0 <= d <= a1: return y0 + (y1 - y0) * (d - a0) / (a1 - a0)
    return HAIRLINE[-1][1]
HAIR_OFF = 4.0                                   # the cap is the skull + 4 (sketch CAP_HALF)
INK_BAND = 2.6                                   # hairline ink on the skin side (sketch HAIRLINE stroke 2.2)
S_END = HL[-1] - 7.0                             # last skin ring; then a fan to the chin pole
NH = 2 if BLOCKOUT else 4
SKIN_F = [0, 0.5, 1.0] if BLOCKOUT else [0, 0.3, 0.56, 0.8, 1.0]
def hair_pt(th, s, off=HAIR_OFF): return head_pt(th, s) + head_n(th, s) * off * U
def hair_n(th, s):
    if s < 0.5: return Vector((0, 0, 1))
    e = 0.02; pt = hair_pt(th + e, s) - hair_pt(th - e, s); ps = hair_pt(th, s + 0.4) - hair_pt(th, s - 0.4)
    n = ps.cross(pt).normalized(); return n if n.dot(head_n(th, s)) > 0 else -n
HAIRLINE_PTS = {}
with shell('head'):
    BODY.bone = 'head'
    pole = BODY.v(hair_pt(0, 0), hair_n(0, 0))
    hair_rings, skin_rings = [], []
    for k in range(1, NH):
        ring = []
        for th in TH_H:
            sh = s_of_y(hair_y(th)); s = sh * (k / NH) ** 0.85
            ring.append(BODY.v(hair_pt(th, s), hair_n(th, s)))
        hair_rings.append(ring)
    edge = [BODY.v(head_pt(th, s_of_y(hair_y(th))), head_n(th, s_of_y(hair_y(th)))) for th in TH_H]
    inkr = [BODY.v(head_pt(th, s_of_y(hair_y(th)) + INK_BAND), head_n(th, s_of_y(hair_y(th)) + INK_BAND)) for th in TH_H]
    for th in TH_H: HAIRLINE_PTS[round(math.degrees(th), 1)] = list(head_pt(th, s_of_y(hair_y(th))))
    for k in range(0, len(SKIN_F)):
        ring = []
        for th in TH_H:
            s0 = s_of_y(hair_y(th)) + INK_BAND; s = s0 + (S_END - s0) * SKIN_F[k]
            ring.append(BODY.v(head_pt(th, s), head_n(th, s)))
        skin_rings.append(ring)
    chin = BODY.v(head_pt(0, HL[-1]), (0, 0, -1))
    fan(BODY, pole, hair_rings[0], 'hair', flip=True)
    # the hair thins to the skin AT the hairline (no overhang: an overhang drew a second, thin hull line above the
    # hairline in both renderers, and a 1-unit lip flipped its triangles); the ink band on the skin carries the edge
    bands(BODY, hair_rings + [edge], ['hair'] * (NH - 1))
    bands(BODY, [edge, inkr], ['hairink'])                              # the hairline ink band (chair call 2)
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
# bun (layered, sunk into the crown): sketch centre (0, y 60, Z -18), radii (25, 21, 23)
with shell('bun'):
    ellipsoid((0, 60, -18), (25, 21, 23), 8 if BLOCKOUT else 10, [30, -30] if BLOCKOUT else [52, 15, -30], 'hair', 'head')
# ears (layered, half sunk, on the eye line): sketch (+-56, y 128, Z -4), radii (5, 10, 7)
# The ear's pole axis points OUT (along X), so the side view shows a round ear, not a diamond.
with shell('ears'):
    for s in (1, -1):
        ring = []
        for j in range(8):
            t = 2 * PI * j / 8; ry_, rz_ = 10 * math.cos(t), 7 * math.sin(t)
            ring.append(BODY.v(B(s * 57.5, 128 - ry_, -4 + rz_), Vector((s * 0.35, -math.sin(t), math.cos(t))).normalized(), 'head'))
        fan(BODY, BODY.v(B(s * 61.5, 128, -4), (s, 0, 0), 'head'), ring, 'skin')
        fan(BODY, BODY.v(B(s * 50.0, 128, -4), (-s, 0, 0), 'head'), ring, 'skin')
# neck (separate, sunk): a short skin tube from inside the head to inside the body top
with shell('neck'):
    rings = []
    for (y, r) in ((158.0, 17.0), (192.0, 17.0)):
        ids = []
        for k in range(8):
            t = 2 * PI * k / 8; ids.append(BODY.v(B(r * math.sin(t), y, 0.9 * r * math.cos(t)), (math.sin(t), -math.cos(t), 0), 'torso'))
        rings.append(ids)
    bands(BODY, rings, ['skin'], flip=True)

# ================================================================ BODY: the pear (sketch BODY_PEAR), depth 0.85
JP = R.path_points(D.BODY_PEAR, 30)
JP = JP[:JP.index(min(JP, key=lambda p: math.dist(p, (188.0, 316.0)))) + 1]   # stop at the hem corner (188, 316)
JL = arc(JP); BODY_DEP = 0.85
def jpt(th, s):
    x, y = at_len(JP, JL, s); r = x - 150.0
    return B(r * math.sin(th), y, BODY_DEP * r * math.cos(th))
def jn(th, s):
    e = 0.02; pt = jpt(th + e, s) - jpt(th - e, s); ps = jpt(th, min(s + 0.4, JL[-1])) - jpt(th, max(s - 0.4, 0))
    n = ps.cross(pt).normalized(); c = jpt(th, s)
    return n if n.dot(c - Vector((0, 0, c.z))) > 0 else -n
def s_at_y(y):
    for i in range(len(JP) - 1):
        if JP[i][1] <= y <= JP[i + 1][1] and JP[i + 1][1] > JP[i][1]:
            f = (y - JP[i][1]) / (JP[i + 1][1] - JP[i][1]); return JL[i] + (JL[i + 1] - JL[i]) * f
    return JL[-1]
s280 = s_at_y(280)
if BLOCKOUT: J_S = [s_at_y(y) for y in (176, 200, 240)] + [s280, JL[-1]]
else: J_S = [s_at_y(y) for y in (176, 187, 201, 222, 250)] + [s280, s280 + (JL[-1] - s280) * 0.55, JL[-1]]
with shell('body'):
    BODY.bone = 'torso'
    rings = [[BODY.v(jpt(th, s), jn(th, s)) for th in TH] for s in J_S]
    bands(BODY, rings, ['dress'] * (len(rings) - 1))
    fan(BODY, BODY.v(B(0, 316, 0), (0, 0, -1)), rings[-1], 'dress')
BPROF = [p for p in R.profile(D.BODY_PEAR) if p[0] < 315.9] + [(316.0, 38.0)]
def surf_z(x, y, out=0.0):
    r = R.r_at(BPROF, y); return r * BODY_DEP * math.sqrt(max(1 - (x / max(r, 1e-3)) ** 2, 0.0)) + out

# ================================================================ ARMS (join: sunk sleeve root, rigid ball elbow, hand ball)
ARM_SIDES = 6 if BLOCKOUT else 8
ARM = {}
for s, side in ((1, 'L'), (-1, 'R')):           # L = her left = viewer-right = +X
    S_ = (s * 52, 206.0, 0.0); E_ = (s * 80, 238.0, 20.0)
    W_ = (s * 46, 260.0, surf_z(46, 260, 8)); Hd = (s * 18, 262.0, surf_z(18, 262, 9))     # dot.py model() "folded"
    ARM[side] = {'S': B(*S_), 'E': B(*E_), 'W': B(*W_), 'H': B(*Hd), 'sx': s}
def perp(d):
    a = Vector((0, 1, 0)) if abs(d.y) < 0.9 else Vector((1, 0, 0))
    u = d.cross(a).normalized(); return u, d.cross(u).normalized()
def tube_rings(pts, radii, n, bone, m, cap_a=True, cap_b=True, acc=None):
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
        rings.append(ring(pts[0] - d0 * radii[0] * 0.7071, radii[0] * 0.7071, d0, frames[0], -0.7071))
    for p, r, d, fr in zip(pts, radii, dirs, frames): rings.append(ring(p, r, d, fr))
    if cap_b is True:
        d1 = dirs[-1]; rings.append(ring(pts[-1] + d1 * radii[-1] * 0.7071, radii[-1] * 0.7071, d1, frames[-1], 0.7071))
    bands(acc, rings, [m] * (len(rings) - 1), flip=True)
    if cap_a is True: fan(acc, pa, rings[0], m, flip=False)
    elif cap_a == 'flat': fan(acc, acc.v(pts[0], -dirs[0], bone), rings[0], m)        # a buried end: a flat fan
    if cap_b is True: fan(acc, acc.v(pts[-1] + dirs[-1] * radii[-1], dirs[-1], bone), rings[-1], m, flip=True)
    elif cap_b == 'flat': fan(acc, acc.v(pts[-1], dirs[-1], bone), rings[-1], m)
for side, a in ARM.items():
    with shell('arm_' + side):
        # upper sleeve: round end buried in the body at the arm root, to the elbow ball (r 11.5 -> 11)
        tube_rings([a['S'], a['E']], [11.5 * U, 11.0 * U], ARM_SIDES, 'arm_%s_up' % side, 'dress', cap_a='flat')
        # forearm: elbow ball, through the sketch wrist, on to the hand (the sleeve end meets the hand ball: no gap)
        endp = a['H'] + (a['W'] - a['H']).normalized() * 7.0 * U      # the sleeve end sinks into the hand ball
        tube_rings([a['E'], a['W'], endp], [11.0 * U, 10.2 * U, 10.0 * U], ARM_SIDES, 'arm_%s_lo' % side, 'dress', cap_b='flat')
        X, y, Z = S(a['H'])
        ellipsoid((X, y, Z), (10, 10.5, 10), ARM_SIDES if not BLOCKOUT else 6, [35, -25] if not BLOCKOUT else [0], 'skin', 'arm_%s_lo' % side)

# ================================================================ LEGS + SHOES (body_root: they stay planted in the sway)
with shell('legs'):
    for s in (1, -1):
        rings = []
        for (y, r) in ((304.0, 11.0), (328.0, 10.5)):
            ids = []
            for k in range(6):
                t = 2 * PI * k / 6; ids.append(BODY.v(B(s * 22 + r * math.sin(t), y, r * math.cos(t)), (math.sin(t), -math.cos(t), 0), 'body_root'))
            rings.append(ids)
        bands(BODY, rings, ['skin'], flip=True)
        ellipsoid((s * 23, 329.5, 8), (13, 8, 19), 8 if not BLOCKOUT else 6, [20, -30], 'shoe', 'body_root')   # sole 337.5: the hull stays above the ground blob

# ================================================================ HEADSET round the NECK (torso): band + a cup on each collarbone
CXS = 183 - 150; CY = 194.0; CZS = surf_z(CXS, CY, 5.0)
with shell('band'):
    NB = 8 if BLOCKOUT else 9
    band = []
    for k in range(NB + 1):
        a = math.radians(-112 + 224 * k / NB)                       # 0 = straight back
        band.append((38 * math.sin(a), 180 + 3 * max(0.0, -math.cos(a)), -33 * math.cos(a)))   # dot.py: y 180..181
    e0, e1 = band[0], band[-1]
    head_pts = [(-CXS, CY - 4, CZS - 1), (-CXS - 2, CY - 11, (e0[2] + CZS) / 2)]   # the end sinks into the cup
    tail_pts = [(CXS + 2, CY - 11, (e1[2] + CZS) / 2), (CXS, CY - 4, CZS - 1)]
    BP = [B(*p) for p in head_pts + band + tail_pts]
    BAND_R = 3.6
    rings = []
    for i, p in enumerate(BP):
        d = (BP[min(i + 1, len(BP) - 1)] - BP[max(i - 1, 0)]).normalized()
        up = Vector((0, 0, 1)); u = (up - d * up.dot(d)).normalized(); w = d.cross(u).normalized(); ids = []
        for k in range(4):
            t = 2 * PI * k / 4 + PI / 4; rd = u * math.cos(t) + w * math.sin(t); ids.append(BODY.v(p + rd * BAND_R * U, rd))
        rings.append(ids)
    open_bands(BODY, rings, 'acc')
with shell('cups'):
    CUP = {}
    tilt = math.radians(-22)     # the flat face looks forward and 22 deg up (resting on the collarbone)
    def cup_local(dx, dH, dZ):
        return (dx, dH * math.cos(tilt) - dZ * math.sin(tilt), dH * math.sin(tilt) + dZ * math.cos(tilt))
    for s in (1, -1):
        cn = 8 if not BLOCKOUT else 6; rings = []
        for (rr, zz, kz) in ((12.5, -3.0, 0.15), (10.5, 3.25, 0.8)):
            ids = []
            for j in range(cn):
                t = 2 * PI * (j + 0.5) / cn; dx, dH, dZ = cup_local(rr * math.sin(t), rr * math.cos(t), zz)
                nx, nH, nZ = cup_local(math.sin(t) * (1 - kz), math.cos(t) * (1 - kz), kz)
                ids.append(BODY.v(B(s * CXS + dx, CY - dH, CZS + dZ), Vector((nx, -nZ, nH))))
            rings.append(ids)
        bands(BODY, rings, ['acc'], flip=True)
        fx, fH, fZ = cup_local(0, 0, 3.9); fn = cup_local(0, 0, 1)
        fan(BODY, BODY.v(B(s * CXS + fx, CY - fH, CZS + fZ), Vector((fn[0], -fn[2], fn[1]))), rings[-1], 'acc', flip=True)
        bx, bH, bZ = cup_local(0, 0, -4.0); bn = cup_local(0, 0, -1)
        fan(BODY, BODY.v(B(s * CXS + bx, CY - bH, CZS + bZ), Vector((bn[0], -bn[2], bn[1]))), rings[0], 'acc', flip=False)
        CUP[s] = B(s * CXS, CY, CZS)

def orient_acc(acc):
    """Wind every accumulated face to agree with the analytic (outward) normals of its vertices."""
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
# triangulate now (fixed diagonals), so the Blender ink hull and the three.js hull are built from the same triangles
# as the surface (a quad split two ways let the hull poke through the twisted hair quads behind the ears)
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

# ================================================================ DECALS (projected on the analytic head, hair cap and body)
SURF = {'head': (R.profile(D.HEAD_HALF), HEAD_D), 'cap': (R.profile(D.CAP_HALF), HEAD_D), 'body': (BPROF, BODY_DEP)}
def front_hit(tree, X, y, off):
    """The decal point on the ANALYTIC surface seen from the front at (X, y), lifted along the surface normal."""
    prof, dep = SURF[tree]
    r = R.r_at(prof, y); Xc = max(-r * 0.999, min(r * 0.999, X)); Z = dep * math.sqrt(max(r * r - Xc * Xc, 0.0))
    e = 0.25; r1, r0 = R.r_at(prof, y + e), R.r_at(prof, y - e); drdy = (r1 - r0) / (2 * e)
    gX, gy, gZ = 2 * Xc, -2 * r * drdy, 2 * Z / dep ** 2
    nb = Vector((gX, -gZ, -gy)).normalized()
    return B(Xc, y, Z) + nb * off * U, nb
DEC = Acc('torso')
SWAP = {k: Acc('head') for k in ('eyes_open', 'eyes_happy', 'mouth_smile', 'mouth_talk')}
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
        ch = max(0.4, m[0] * n1[0] + m[1] * n1[1]); out.append((p1[0] + m[0] * d / ch, p1[1] + m[1] * d / ch))
    return out
def fan_card(acc, tree, pts2d, off, m, bone=None):
    cx = sum(p[0] for p in pts2d) / len(pts2d); cy = sum(p[1] for p in pts2d) / len(pts2d)
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
NSEG = 2 if BLOCKOUT else 3
# face (head bone): eyes with glints (swap: open / happy), brows, the swept strands on the hair cap
for (ex, ey) in [(D.LM['eye_x'][0], D.LM['eye']), (D.LM['eye_x'][1], D.LM['eye'])]:
    fan_card(SWAP['eyes_open'], 'head', clean(R.path_points(R.oval(ex, ey, 6.5, 8.5), 3)), 0.4, 'ink')
    if not BLOCKOUT: fan_card(SWAP['eyes_open'], 'head', clean(R.path_points(R.oval(ex + 2, ey - 3.2, 2.0, 2.4), 2)), 0.6, 'white')
for d in D.HAPPY_EYES: line_card(SWAP['eyes_happy'], 'head', R.path_points(d, 4), 3.4, 0.4, 'ink')
if not BLOCKOUT:
    for d in D.BROWS: line_card(DEC, 'head', R.path_points(d, 3), 2.6, 0.4, 'brow', bone='head')
    for i_, d in enumerate(D.COMB):   # the strands (Rega ts 1795658703.410809: "this part is fine"); outer ones start inside the temple edge
        pts_ = R.path_points(d, 3)
        if i_ in (0, 2): pts_ = [(pts_[0][0] + (pts_[1][0] - pts_[0][0]) * 0.45, pts_[0][1] + (pts_[1][1] - pts_[0][1]) * 0.45)] + pts_[1:]
        line_card(DEC, 'cap', pts_, 1.6, 0.6, 'ink', bone='head')
# mouths (swap parts): the rest smile is a thin curved line (chair call 3: small and curved)
SMILE_W = 2.6
line_card(SWAP['mouth_smile'], 'head', R.path_points(D.SMILE, 6 if not BLOCKOUT else 3), SMILE_W, 0.5, 'ink')
fan_card(SWAP['mouth_talk'], 'head', clean(R.path_points(D.TALK, 3)), 0.5, 'ink')
# body (torso): placket, 2 buttons (row 23 with ink), 2 pockets (ink outline)
if not BLOCKOUT:
    line_card(DEC, 'body', R.path_points("M150,186 L150,312", 6), 1.6, 1.2, 'ink')   # lifted 1.2: the 21-unit chords must not sink into the facets
    for (bx, by) in D.BUTTONS:
        fan_card(DEC, 'body', clean(R.path_points(R.oval(bx, by, 5.4, 5.4), 2)), 0.6, 'ink')
        fan_card(DEC, 'body', clean(R.path_points(R.oval(bx, by, 4.2, 4.2), 2)), 0.8, 'white')
    for d in D.POCKETS: line_card(DEC, 'body', clean(R.path_points(d, 2)), 1.5, 0.4, 'ink', closed=True)
else:
    for (bx, by) in D.BUTTONS: fan_card(DEC, 'body', clean(R.path_points(R.oval(bx, by, 5.4, 5.4), 1)), 0.6, 'white')
LAND = {'eye_top': front_hit('head', D.LM['eye_x'][0] - 150, D.LM['eye'] - 8.5, 0.4)[0],
        'mouth': front_hit('head', 0, 154, 0.5)[0], 'button_top': front_hit('body', 0, 214, 0.8)[0]}
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
bh = arm_d.edit_bones.new('head'); bh.head = B(0, 178, 0); bh.tail = B(0, 100, 0); bh.parent = bt
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
for k, (o, _, used) in swaps.items():
    skin(o, SWAP[k], used); o['variant'] = k; o['default_visible'] = k in ('eyes_open', 'mouth_smile')
for k, v in LAND.items(): decals[k + '_rest_blender'] = list(v)

# ---------------------------------------------------------------- poses: two-bone reach, stored as axis + angle (Ricky)
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
# talk: her right hand (viewer-left, -X) up beside the face, palm out; head roll 8 deg to the viewer's right
TALK_T = B(-94, 180, 24); TALK_EL = B(-96, 236, 14)
talk, _ = solve('R', TALK_T, TALK_EL - ARM['R']['S'])
talk['head'] = [0.0, 1.0, 0.0, 8.0]
# card: her right arm forward, the Skill card in the hand, face to the player; 2 deg lean (torso about the feet)
CARD_T = B(-42, 234, 104); CARD_EL = B(-72, 238, 46)
card_p, CARD_X = solve('R', CARD_T, CARD_EL - ARM['R']['S'])
card_p['torso'] = [1.0, 0.0, 0.0, 2.0]
POSES = {'talk': talk, 'card': card_p}
flt['poses_float_blender'] = POSES
flt['sway'] = {'torso_axis_blender': [0, 1, 0], 'amp_deg': 4.0, 'period_s': 2.5, 'head_follow': -0.5,
               'rule': 'torso +-4 deg about the feet (legs and shoes stay on body_root); the head lags by half'}
flt['height_m'] = H_M; flt['unit_m'] = U
flt['expressions'] = {'rest': ['eyes_open', 'mouth_smile'], 'talk': ['eyes_open', 'mouth_talk'], 'happy': ['eyes_happy', 'mouth_smile']}

# ================================================================ CARD (prop, skinned to arm_R_lo; built in the rest frame)
CARDA = Acc('arm_R_lo')
if not BLOCKOUT:
    hd = S(CARD_T); cc = (hd[0] - 4, hd[1] - 22, hd[2] + 8)       # dot.py: centre 22 above the hand, s*4 out, 8 forward
    tl = math.radians(-8)                                           # tilted back 8 deg
    def cardp(dx, dy, dz):                                          # local (X, y-down, Z) -> posed sketch point
        y2 = dy * math.cos(tl) + dz * math.sin(tl); z2 = -dy * math.sin(tl) + dz * math.cos(tl)
        return B(cc[0] + dx, cc[1] + y2, cc[2] + z2)
    def unpose(p):            # posed (card pose, before the lean) -> rest frame of the forearm
        X_ = CARD_X; q = X_['R2w'].inverted() @ (p - X_['E2']) + X_['E2']
        return X_['R1'].inverted() @ (q - X_['S']) + X_['S']
    W2, H2, T2 = 15.0, 21.0, 1.5
    corners = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1): corners[(sx, sy, sz)] = cardp(sx * W2, sy * H2, sz * T2)
    def quad(keys, m, nrm):
        ids = [CARDA.v(unpose(corners[k]), nrm) for k in keys]; CARDA.f(ids, m)
    quad([(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)], 'card', (0, -1, 0))        # face (to the player)
    quad([(1, -1, -1), (-1, -1, -1), (-1, 1, -1), (1, 1, -1)], 'card', (0, 1, 0))     # back
    quad([(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)], 'cardedge', (0, 0, 1)) # top
    quad([(-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1)], 'cardedge', (0, 0, -1))   # bottom
    quad([(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)], 'cardedge', (-1, 0, 0))
    quad([(1, -1, 1), (1, -1, -1), (1, 1, -1), (1, 1, 1)], 'cardedge', (1, 0, 0))
    # the Copium disc on the face (row 13): sketch centre 6 above the card centre
    c0 = CARDA.v(unpose(cardp(0, -6, T2 + 0.4)), (0, -1, 0)); ring = []
    for j in range(10):
        t = 2 * PI * j / 10; ring.append(CARDA.v(unpose(cardp(8 * math.cos(t), -6 + 8 * math.sin(t), T2 + 0.4)), (0, -1, 0)))
    for j in range(10): CARDA.f([c0, ring[j], ring[(j + 1) % 10]], 'gold')
    cardob, _, cused = make_mesh('card', CARDA, smooth=False)
    # wind each face to its stored normal in the rest frame
    bm = bmesh.new(); bm.from_mesh(cardob.data); bm.normal_update(); bm.faces.ensure_lookup_table()
    R1i = CARD_X['R1'].inverted(); R2i = CARD_X['R2w'].inverted()
    for f in bm.faces:
        n_ = sum((CARDA.N[cused[v.index]] for v in f.verts), Vector()); n_ = R1i @ (R2i @ n_)
        if f.normal.dot(n_) < 0: f.normal_flip()
    bm.to_mesh(cardob.data); bm.free(); cardob.data.update()
    skin(cardob, CARDA, cused); cardob['prop'] = 'skill card: shown only in the card beat'; cardob['default_visible'] = False

def pose(name=None, sway=0.0):
    for pb in rig.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0)
    P = dict(flt['poses_float_blender'][name].to_dict()) if name else {}
    if sway:
        P['torso'] = [0, 1, 0, sway]; P['head'] = [0, 1, 0, -0.5 * sway]
    for bn, (x, y, z, deg) in P.items():
        M = rig.data.bones[bn].matrix_local.to_3x3().inverted()
        rig.pose.bones[bn].rotation_quaternion = Quaternion(M @ Vector((x, y, z)), math.radians(deg))
    bpy.context.view_layer.update()
# checks: the posed right hand centre vs the talk / card targets (before the card lean)
def hand_now():
    pb = rig.pose.bones['arm_R_lo']; return (rig.matrix_world @ pb.matrix) @ (rig.data.bones['arm_R_lo'].matrix_local.inverted() @ ARM['R']['H'])
pose('talk'); talk_err = (hand_now() - TALK_T).length
P_ = dict(POSES['card']); del P_['torso']
for pb in rig.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0)
for bn, (x, y, z, deg) in P_.items():
    M = rig.data.bones[bn].matrix_local.to_3x3().inverted(); rig.pose.bones[bn].rotation_quaternion = Quaternion(M @ Vector((x, y, z)), math.radians(deg))
bpy.context.view_layer.update(); card_err = (hand_now() - CARD_T).length
pose(None)

# ================================================================ REPORT + EXPORT
def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {'body': tris(body), 'decals': tris(decals)}
for k, (o, _, _) in swaps.items(): counts[k] = tris(o)
if not BLOCKOUT: counts['card'] = tris(cardob)
counts['visible_rest (body + decals + eyes_open + mouth_smile)'] = counts['body'] + counts['decals'] + counts['eyes_open'] + counts['mouth_smile']
counts['visible_talk'] = counts['body'] + counts['decals'] + counts['eyes_open'] + counts['mouth_talk']
counts['visible_card (rest + card)'] = counts['visible_rest (body + decals + eyes_open + mouth_smile)'] + counts.get('card', 0)
counts['visible_happy'] = counts['body'] + counts['decals'] + counts['eyes_happy'] + counts['mouth_smile']
counts['body_by_part'] = {nm: sum(len(f) - 2 for f in BODY.F[f0:f1]) for nm, (v0, v1, f0, f1) in SHELLS.items()}
checks = {'body_nonmanifold_edges': nonman, 'body_boundary_edges (neck tube ends, body top ring, leg ends, band ends)': boundary,
          'body_faces_against_analytic_normals': inward, 'height_m': H_M, 'unit_mm': round(U * 1000, 3),
          'talk_hand_centre_to_target_mm': round(talk_err * 1000, 2), 'card_hand_centre_to_target_mm': round(card_err * 1000, 2),
          'faces_rewound_to_analytic_normals': REWOUND, 'hairline_front_view_y_by_deg': HAIRLINE,
          'skin_unweighted': sum(1 for v in body.data.vertices if not v.groups), 'smile_width_units': SMILE_W,
          'card_pose_elbow_sketch': [round(v, 1) for v in S(CARD_X['E2'])]}
meshes = [o.name for o in bpy.data.objects if o.type == 'MESH']
report = {'triangles': counts, 'meshes': {'all': meshes, 'non_swap (<= 3)': ['body', 'decals'],
          'swap': list(swaps), 'prop': ['card'] if not BLOCKOUT else []}, 'checks': checks,
          'poses': {k: v for k, v in POSES.items()}}
print('DOT_REPORT', json.dumps(counts), json.dumps(checks))
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump(TOONJ, open(os.path.join(OUT, 'dot_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, bnc, rig, body, decals] + [s_[0] for s_ in swaps.values()] + ([cardob] if not BLOCKOUT else []): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('DOT_DONE')
