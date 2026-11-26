# GHOSTED - Recruiter Ricky, v1: blockout and final model, built to the accepted sketch (assets/ricky/sketch).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_ricky.py -- [blockout] [H=1.00] [out=<dir>]
# Brief: design/acceptance/ricky/build-brief-3d.md. Direction and join decisions: direction.md.
# Shapes: the outlines and marks come from the sketch's hand-drawn Bezier paths (../sketch/src/ricky.py), read here.
# Sketch units: x right (centred X = x - 150), y down (sole y 340), Z forward. 1 unit = H / 304 m.
# Blender: Z-up, Ricky faces -Y. glTF: Y-up (faces +Z in three.js).
# Nodes: root > float (drain lift) > bounce (hop squash, pivot at the soles) > rig (body_root, arm_L_up, arm_L_lo,
#        arm_R_up, arm_R_lo) > body (skinned, 1 non-swap mesh); bounce > decals (non-swap 2); bounce > mouth_grin,
#        mouth_o (swap parts).
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import ricky as R
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
H_M = 1.18          # set by the blockout measure, then trimmed 1 px: 79 px = 1.053 x Kit on screen (measure.md)
OUT = HERE
for a in ARGV:
    if a.startswith('H='): H_M = float(a[2:])
    if a.startswith('out='): OUT = os.path.join(HERE, a[4:]); os.makedirs(OUT, exist_ok=True)
NAME = 'ricky_blockout' if BLOCKOUT else 'ricky'
PI = math.pi
U = H_M / 304.0

PAL = {'suit': R.ROW[17], 'leg': R.ROW[17], 'shoe': R.ROW[5], 'skin': R.ROW[15], 'hair': R.ROW[25],
       'shirt': R.ROW[16], 'acc': R.ROW[10], 'mic': R.ROW[10], 'tie': R.ROW[10], 'ink': R.ROW[22],
       'brow': R.ROW[22], 'tieink': R.ROW[22], 'white': R.ROW[16]}
BASIC = ['ink', 'brow', 'tieink', 'white']
NEUTRAL = [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]]   # Kit's bands2 (neutral grey 178 shade band)
TOONJ = {'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC,
         'outline_nodes': ['body'], 'contact_shadow': {'rx': 0.31, 'ry': 0.25, 'opacity': 0.25},
         'drain': {'suit_rows': [R.ROW[17], R.ROW[11], R.ROW[27], R.ROW[16]],
                   'scale_at_end': 0.62, 'note': 'body scales 1 -> 0.62 (Ghostie size); suit and leg lerp 17 -> 11 -> 27 -> 16; skin and hair -> 16; headset -> 27; legs, shoes, mic, '
                           'brows, tie and mouth fade; float up; then the headset Ghostie swaps in'}}

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

# ================================================================ mesh accumulator
class Acc:
    def __init__(s): s.V, s.N, s.F, s.FM, s.VB, s.tags = [], [], [], [], [], {}
    def v(s, p, n, bone='body_root'):
        s.V.append(Vector(p)); s.N.append(Vector(n).normalized()); s.VB.append(bone); return len(s.V) - 1
    def f(s, ids, m): s.F.append(list(ids)); s.FM.append(m)
BODY = Acc()
SHELLS = {}          # shell name -> (first vertex, last vertex + 1, first face, last face + 1) for BVHs and counts

def shell(name):
    class _C:
        def __enter__(c): c.v0, c.f0 = len(BODY.V), len(BODY.F); return c
        def __exit__(c, *a): SHELLS[name] = (c.v0, len(BODY.V), c.f0, len(BODY.F))
    return _C()

def bands(acc, rings, mats, flip=False):
    """Quads between consecutive rings (same length, closed). mats: one material per band."""
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

COLS = 8 if BLOCKOUT else 16
TH = [2 * PI * j / COLS for j in range(COLS)]          # theta 0 = front (+Z sketch = -Y Blender), +90 = character's left (+X)

# ================================================================ HEAD + HAIR CAP: one surface (join: continuous skin)
HP = R.path_points(R.HEAD_HALF, 80); HL = arc(HP)
HEAD_D = 0.92
def head_pt(th, s):
    x, y = at_len(HP, HL, s); r = x - 150.0
    return B(r * math.sin(th), y, HEAD_D * r * math.cos(th))
def head_n(th, s):
    e = 0.02
    if s < 0.5: return Vector((0, 0, 1))
    pt = head_pt(th + e, s) - head_pt(th - e, s); ps = head_pt(th, s + e * 20) - head_pt(th, s - e * 20)
    n = ps.cross(pt).normalized()
    c = head_pt(th, s); ax = Vector((0, 0, c.z))
    return n if n.dot(c - ax) > 0 else -n
def s_of_y(y):
    for i in range(len(HP) - 1):
        if HP[i][1] <= y <= HP[i + 1][1]:
            f = (y - HP[i][1]) / max(HP[i + 1][1] - HP[i][1], 1e-9); return HL[i] + (HL[i + 1] - HL[i]) * f
    return HL[-1]
# Hairline (Rega ts 1795622664.391049: no fringe). Front-view y of the hair edge by column angle (deg from the front).
# The front stays well above the brows (y 77-83); the temples stay above the brows until behind the ear plane; then the
# edge runs down the back to the nape (sheet BACK view).
HAIRLINE = [(0, 63.0), (22.5, 64.0), (45, 66.0), (67.5, 70.0), (90, 75.0), (112.5, 96.0), (135, 115.0), (157.5, 123.0), (180, 125.0)]
def hair_y(th):
    d = abs(math.degrees((th + PI) % (2 * PI) - PI))
    for (a0, y0), (a1, y1) in zip(HAIRLINE, HAIRLINE[1:]):
        if a0 <= d <= a1: return y0 + (y1 - y0) * (d - a0) / (a1 - a0)
    return HAIRLINE[-1][1]
HAIR_OFF = 3.0                                   # the cap is the skull + 3 (sketch capd)
S_END = s_of_y(149.0)                            # the head's bottom ring sits inside the jacket top (hidden)
NH = 2 if BLOCKOUT else 5                        # hair rings from the crown to the hairline
NS = 3 if BLOCKOUT else 6                        # skin bands from the hairline to the chin
SKIN_F = [0, 0.34, 0.67, 1.0] if BLOCKOUT else [0, 0.22, 0.42, 0.60, 0.75, 0.88, 1.0]   # denser at the jaw curve
# The quiff is part of the cap (continuous skin): the cap thickness grows to a round roll at the top-front
# (sketch 'pomp': top y 36, about 66 wide, a little forward). No second shell, so no step or box edge.
QDIR = Vector((0, -0.17, 1)).normalized()
def hair_pt(th, s):
    n = head_n(th, s); ang = math.acos(max(-1.0, min(1.0, n.dot(QDIR))))
    return head_pt(th, s) + n * (HAIR_OFF + (0 if BLOCKOUT else 17.0 * math.exp(-(ang / 0.5) ** 2))) * U
def hair_n(th, s):
    if s < 0.5: return Vector((0, -0.17, 1)).normalized()
    e = 0.02; pt = hair_pt(th + e, s) - hair_pt(th - e, s); ps = hair_pt(th, s + 0.4) - hair_pt(th, s - 0.4)
    n = ps.cross(pt).normalized(); return n if n.dot(head_n(th, s)) > 0 else -n
with shell('head'):
    pole = BODY.v(hair_pt(0, 0), hair_n(0, 0))
    hair_rings, skin_rings = [], []
    for k in range(1, NH + 1):
        ring = []
        for th in TH:
            sh = s_of_y(hair_y(th)); s = sh * (k / NH) ** 0.9
            ring.append(BODY.v(hair_pt(th, s), hair_n(th, s)))
        hair_rings.append(ring)
    for k in range(0, NS + 1):
        ring = []
        for th in TH:
            sh = s_of_y(hair_y(th)); s = sh + (S_END - sh) * SKIN_F[k]
            ring.append(BODY.v(head_pt(th, s), head_n(th, s)))
        skin_rings.append(ring)
    fan(BODY, pole, hair_rings[0], 'hair', flip=True)
    bands(BODY, hair_rings, ['hair'] * (NH - 1))
    bands(BODY, [hair_rings[-1], skin_rings[0]], ['hair'])          # the lip (3 units, faces down)
    bands(BODY, skin_rings, ['skin'] * NS)
# Quiff (layered, sunk into the crown): sketch 'pomp' ellipsoid centre (0, y 50, Z 4), radii (33, 14, 27).
def ellipsoid(c, rad, cols, lats, m, bone='body_root', up=(0, 1, 0)):
    """c, rad in sketch units (X, y-down, Z); lats in degrees (from -90 bottom to 90 top, exclusive)."""
    top = BODY.v(B(c[0], c[1] - rad[1], c[2]), (0, 0, 1), bone)
    bot = BODY.v(B(c[0], c[1] + rad[1], c[2]), (0, 0, -1), bone)
    rings = []
    for la in sorted(lats, reverse=True):
        a = math.radians(la); ring = []
        for j in range(cols):
            t = 2 * PI * j / cols; ux, uy, uz = math.cos(a) * math.sin(t), math.sin(a), math.cos(a) * math.cos(t)
            p = B(c[0] + rad[0] * ux, c[1] - rad[1] * uy, c[2] + rad[2] * uz)
            nb = Vector((ux / rad[0], -uz / rad[2], uy / rad[1]))
            ring.append(BODY.v(p, nb, bone))
        rings.append(ring)
    fan(BODY, top, rings[0], m, flip=True); bands(BODY, rings, [m] * (len(rings) - 1)); fan(BODY, bot, rings[-1], m)
if BLOCKOUT:
    with shell('quiff'): ellipsoid((0, 52, 4), (33, 16, 27), 8, [25, -25], 'hair')

# ================================================================ JACKET: the bell (sketch JACKET_HALF), depth 0.82
JP = R.path_points(R.JACKET_HALF, 40)
JP = JP[:JP.index(min(JP, key=lambda p: math.dist(p, (204.0, 268.0)))) + 1]   # stop at the hem corner (204, 268)
JL = arc(JP); JACK_D = 0.82
def jpt(th, s):
    x, y = at_len(JP, JL, s); r = x - 150.0
    return B(r * math.sin(th), y, JACK_D * r * math.cos(th))
def jn(th, s):
    e = 0.02; pt = jpt(th + e, s) - jpt(th - e, s); ps = jpt(th, s + 0.4) - jpt(th, s - 0.4)
    n = ps.cross(pt).normalized(); c = jpt(th, s)
    return n if n.dot(c - Vector((0, 0, c.z))) > 0 else -n
def s_at_y(y):
    for i in range(len(JP) - 1):
        if JP[i][1] <= y <= JP[i + 1][1] and JP[i + 1][1] > JP[i][1]:
            f = (y - JP[i][1]) / (JP[i + 1][1] - JP[i][1]); return JL[i] + (JL[i + 1] - JL[i]) * f
    return JL[-1]
if BLOCKOUT: J_S = [s_at_y(y) for y in (148, 158, 176, 220, 258)] + [JL[-1]]
else: J_S = [s_at_y(y) for y in (148, 155, 166, 180, 215, 250, 262)] + [JL[-1] - 6.0, JL[-1]]
with shell('jacket'):
    rings = [[BODY.v(jpt(th, s), jn(th, s)) for th in TH] for s in J_S]
    bands(BODY, rings, ['suit'] * (len(rings) - 1))
    hem_c = BODY.v(B(0, 268, 0), (0, 0, -1))
    fan(BODY, hem_c, rings[-1], 'suit')
JACK_PROF = R.profile(R.JACKET_HALF)

# ================================================================ ARMS (join: sunk shoulder ball + rigid ball elbow)
ax_ = R.r_at(JACK_PROF, R.LM['shoulder'] + 6) - 6; dx = ax_ - 60           # = ricky.py model()
ARM_SIDES = 6 if BLOCKOUT else 8
ARM = {}
for s, side in ((1, 'L'), (-1, 'R')):                                     # L = character's left = viewer-right = +X
    # sketch path (ricky.py model) with the elbow, wrist and hand 4.5-5 units further out, so the sleeve hangs just clear
    # of the bell below the shoulder and its inner ink line shows (the sketch draws the sleeve over the jacket edge)
    S_ = (s * (66 + dx), R.LM['shoulder'], 0.0); E_ = (s * (dx + 80.5), 206.0, 1.0)
    W_ = (s * (dx + 83), 230.0, 3.5); Hd = (s * (dx + 84), 246.0, 5.0)
    ARM[side] = {'S': B(*S_), 'E': B(*E_), 'W': B(*W_), 'H': B(*Hd), 'sx': s}
def perp(d):
    a = Vector((0, 1, 0)) if abs(d.y) < 0.9 else Vector((1, 0, 0))
    u = d.cross(a).normalized(); return u, d.cross(u).normalized()
def capsule_rings(A, Bp, ra, rb, n, bone, m, cap_a=True, cap_b=True, end_pole=None, extra=None):
    """A tube from A to Bp with sphere caps. extra: [(point, radius, material)] rings after Bp (cuff)."""
    d = (Bp - A).normalized(); u, w = perp(d)
    def ring(c, r, nrm_axis=0.0):
        ids = []
        for k in range(n):
            t = 2 * PI * k / n; rd = u * math.cos(t) + w * math.sin(t)
            ids.append(BODY.v(c + rd * r, rd * math.sqrt(1 - nrm_axis ** 2) + d * nrm_axis, bone))
        return ids
    rings, mats = [], []
    if cap_a:
        pa = BODY.v(A - d * ra, -d, bone); rings.append(ring(A - d * ra * 0.7071, ra * 0.7071, -0.7071))
    rings.append(ring(A, ra)); rings.append(ring(Bp, rb))
    if cap_b: rings.append(ring(Bp + d * rb * 0.7071, rb * 0.7071, 0.7071))
    mats = [m] * (len(rings) - 1)
    for (c, r, mm) in (extra or []): rings.append(ring(c, r)); mats.append(mm)
    if cap_a: fan(BODY, pa, rings[0], m, flip=False)
    bands(BODY, rings, mats, flip=True)
    if cap_b: fan(BODY, BODY.v(Bp + d * rb, d, bone), rings[-1], m, flip=True)
    elif end_pole is not None: fan(BODY, BODY.v(end_pole, d, bone), rings[-1], (extra or [(0, 0, m)])[-1][2], flip=True)
for side, a in ARM.items():
    with shell('arm_' + side):
        # upper sleeve: shoulder ball (sunk in the jacket at the shoulder joint) to the elbow ball, r 13.5 -> 12.5
        capsule_rings(a['S'], a['E'], 13.5 * U, 12.5 * U, ARM_SIDES, 'arm_%s_up' % side, 'suit')
        # forearm: elbow ball, sleeve to the wrist (r 12.5 -> 11.5), then the white cuff (r 11), into the hand
        cuff_end = a['W'] + (a['H'] - a['W']) * 0.35
        capsule_rings(a['E'], a['W'], 12.5 * U, 11.5 * U, ARM_SIDES, 'arm_%s_lo' % side, 'suit', cap_a=True, cap_b=False,
                      end_pole=a['H'], extra=[(cuff_end, 10.6 * U, 'shirt')])
        # hand: a skin ball (sketch radii 10.5, 11, 10.5)
        hc = a['H']; X, y, Z = hc.x / U, 340.0 - hc.z / U, -hc.y / U
        ellipsoid((X, y, Z), (10.5, 11, 10.5), ARM_SIDES, [30, -30] if BLOCKOUT else [45, 0, -45], 'skin', bone='arm_%s_lo' % side)

# ================================================================ LEGS + SHOES (own materials: the drain fades them)
with shell('legs'):
    for s in (1, -1):
        rings = []
        for (y, r) in ((262.0, 12.5), (328.0, 11.0)):
            ids = []
            for k in range(6):
                t = 2 * PI * k / 6; ids.append(BODY.v(B(s * 21 + r * math.sin(t), y, r * math.cos(t)), (math.sin(t), -math.cos(t), 0)))
            rings.append(ids)
        bands(BODY, rings, ['leg'], flip=True)
        ellipsoid((s * 22, 330, 9), (14, 10, 21), ARM_SIDES, [25, -25], 'shoe')

# ================================================================ HEADSET (in the body mesh, body_root): band, cups, mic
HY = R.LM['eye']
with shell('cups'):
    CUP = {}
    for s in (1, -1):
        cn = 8
        rings = []
        for (X, k) in ((57.0, 1.0), (65.0, 0.80)):
            ids = []
            for j in range(cn):
                t = 2 * PI * (j + 0.5) / cn; ny, nz = math.sin(t), math.cos(t)
                p = B(s * X, HY + 2 - 17 * k * ny, -2 + 13 * k * nz)
                nb = Vector((s * (0.15 if k == 1 else 0.8), -nz, ny)).normalized()
                ids.append(BODY.v(p, nb))
            rings.append(ids)
        bands(BODY, rings, ['acc'], flip=(s < 0))
        fan(BODY, BODY.v(B(s * 67.5, HY + 2, -2), (s, 0, 0)), rings[-1], 'acc', flip=(s > 0))
        CUP[s] = B(s * 61, HY + 2, -2)
# the band: in the ear plane (Z -6), it hugs the hair cap and the quiff with a small clearance (body map C)
def orient_acc(acc):
    """Wind every accumulated face to agree with the analytic (outward) normals of its vertices."""
    n = 0
    for i, f in enumerate(acc.F):
        a, b, c = acc.V[f[0]], acc.V[f[1]], acc.V[f[2]]; fn = (b - a).cross(c - a)
        if len(f) == 4: fn = fn + (acc.V[f[3]] - a).cross(c - a) * 0 + (c - a).cross(acc.V[f[3]] - a)
        an = sum((acc.N[k] for k in f), Vector())
        if fn.dot(an) < 0: acc.F[i] = f[::-1]; n += 1
    return n
def bvh_of(names):
    vs, fs = [], []
    for nm in names:
        v0, v1, f0, f1 = SHELLS[nm]
        base = len(vs); vs += [BODY.V[i] for i in range(v0, v1)]
        fs += [[i - v0 + base for i in f] for f in BODY.F[f0:f1]]
    return BVHTree.FromPolygons(vs, fs)
REWOUND = orient_acc(BODY)
HEADTREE = bvh_of(['head', 'quiff'] if BLOCKOUT else ['head'])
BAND_R = 3.4                                         # band half-thickness (units)
NSEG = 8 if BLOCKOUT else 10
with shell('band'):
    secs = []; dist_ = []
    ctr = B(0, HY + 4, -6)
    for k in range(NSEG + 1):
        a = PI * k / NSEG; dirv = Vector((-math.cos(a), 0, math.sin(a)))
        far = ctr + dirv * 1.0
        hit, nrm, _, _ = HEADTREE.ray_cast(far, -dirv)
        dist_.append(((hit - ctr).length if hit else 60 * U) + (BAND_R + 1.5) * U)
    # a smooth arch (the sketch band: x 63, top y 32): a superellipse about ctr, scaled up just enough to clear the hug
    def arch(a, n=2.3): return 1.0 / ((abs(math.cos(a)) / (63 * U)) ** n + (abs(math.sin(a)) / (70 * U)) ** n) ** (1 / n)
    kk = max(1.0, max(d_ / arch(PI * k / NSEG) for k, d_ in enumerate(dist_) if 0 < k < NSEG))
    sm = [kk * arch(PI * k / NSEG) for k in range(NSEG + 1)]
    BAND_GAP_UNITS = [round((sm[k] - dist_[k]) / U, 1) for k in range(1, NSEG)]
    for k in range(NSEG + 1):
        a = PI * k / NSEG; dirv = Vector((-math.cos(a), 0, math.sin(a)))
        c = ctr + dirv * (60 * U if k in (0, NSEG) else sm[k])
        b = Vector((0, 1, 0))
        # flat-topped section (2 outer corners, 1 inner): seen edge-on from the side the band ends in a flat cap, not a spike
        ids = [BODY.v(c + dirv * 0.6 * BAND_R * U + b * BAND_R * U, (dirv + b * 0.6).normalized()),
               BODY.v(c + dirv * 0.6 * BAND_R * U - b * BAND_R * U, (dirv - b * 0.6).normalized()),
               BODY.v(c - dirv * 0.9 * BAND_R * U, -dirv)]
        secs.append(ids)
    bands(BODY, secs, ['acc'] * NSEG)
with shell('mic'):
    mp = [B(-60, 110, 4), B(-57, 121, 20), B(-46, 126, 33)]
    rings = []
    for i, p in enumerate(mp):
        d = (mp[min(i + 1, 2)] - mp[max(i - 1, 0)]).normalized(); u, w = perp(d); ids = []
        for k in range(4):
            t = 2 * PI * k / 4 + PI / 4; rd = u * math.cos(t) + w * math.sin(t); ids.append(BODY.v(p + rd * 2.4 * U, rd))
        rings.append(ids)
    bands(BODY, rings, ['mic'] * 2, flip=True)
    ellipsoid((-44, 126, 35), (4.6, 4.6, 4.6), 6, [0], 'mic')

REWOUND += orient_acc(BODY)
# ================================================================ build the body mesh
def make_mesh(name, acc, smooth=True):
    used = sorted(set(i for f in acc.F for i in f)); remap = {o: n for n, o in enumerate(used)}
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(acc.V[i]) for i in used], [], [[remap[i] for i in f] for f in acc.F])
    names = sorted(set(acc.FM), key=lambda m: list(PAL).index(m))
    for m in names: me.materials.append(mat(m))
    me.polygons.foreach_set('material_index', [names.index(m) for m in acc.FM])
    me.polygons.foreach_set('use_smooth', [smooth] * len(me.polygons)); me.update()
    if smooth:   # wind every face to agree with the analytic (outward) normals of its vertices
        bm = bmesh.new(); bm.from_mesh(me); bm.normal_update(); bm.verts.ensure_lookup_table(); nflip = 0
        for f in bm.faces:
            an = sum((acc.N[used[v.index]] for v in f.verts), Vector())
            if f.normal.dot(an) < 0: f.normal_flip(); nflip += 1
        bm.to_mesh(me); bm.free(); me['faces_rewound'] = nflip
        me.polygons.foreach_set('use_smooth', [True] * len(me.polygons)); me.update()
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob)
    return ob, remap, used
body, BREMAP, BUSED = make_mesh('body', BODY)
# orientation check: every face of every closed shell must face out; faces were wound by construction, verify here
bm = bmesh.new(); bm.from_mesh(body.data); bm.normal_update()
nonman = sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary)
boundary = sum(1 for e in bm.edges if e.is_boundary)
inward = {}
bm.faces.ensure_lookup_table()
for f in bm.faces:
    an = sum((BODY.N[BUSED[v.index]] for v in f.verts), Vector())
    if f.normal.dot(an) < 0: inward['faces'] = inward.get('faces', 0) + 1
bm.free()
# analytic shading normals (0 triangles): the toon band follows the ideal surface, not the facets
body.data.normals_split_custom_set_from_vertices([tuple(BODY.N[i]) for i in BUSED])
body.data.update()

# ================================================================ DECALS (projected on the head and the jacket)
HTREE, JTREE = 'head', 'jacket'
HEAD_PROF = R.profile(R.HEAD_HALF)
SURF = {'head': (HEAD_PROF, HEAD_D), 'jacket': (JACK_PROF, JACK_D)}
def front_hit(tree, X, y, off):
    """The decal point on the ANALYTIC surface (head or jacket revolve) seen from the front at (X, y), lifted along the
    surface normal. The analytic surface lies on or outside every facet, so a decal never sinks between facets."""
    prof, dep = SURF[tree]
    r = R.r_at(prof, y); Xc = max(-r * 0.999, min(r * 0.999, X)); Z = dep * math.sqrt(max(r * r - Xc * Xc, 0.0))
    e = 0.25; r1, r0 = R.r_at(prof, y + e), R.r_at(prof, y - e); drdy = (r1 - r0) / (2 * e)
    # F(X, y, Z) = X^2 + (Z/dep)^2 - r(y)^2 = 0  ->  grad = (2X, -2 r r'(y), 2Z/dep^2) in (X, y-down, Z)
    gX, gy, gZ = 2 * Xc, -2 * r * drdy, 2 * Z / dep ** 2
    nb = Vector((gX, -gZ, -gy)).normalized()            # to Blender: X, -Z, -y
    return B(Xc, y, Z) + nb * off * U, nb
DEC = Acc(); MOUTH = {'grin': Acc(), 'o': Acc()}
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
def clean(pts):
    out = []
    for p in pts:
        if not out or math.dist(p, out[-1]) > 0.3: out.append(p)
    if math.dist(out[0], out[-1]) < 0.3: out.pop()
    return out
def fan_card(acc, tree, pts2d, off, m):
    """pts2d: front-view (x, y) polygon (star-shaped). A centre fan, every vertex on the surface + off."""
    cx = sum(p[0] for p in pts2d) / len(pts2d); cy = sum(p[1] for p in pts2d) / len(pts2d)
    c = acc.v(front_hit(tree, cx - 150, cy, off)[0], (0, -1, 0)); ring = [acc.v(front_hit(tree, x - 150, y, off)[0], (0, -1, 0)) for x, y in pts2d]
    for j in range(len(ring)): acc.f([c, ring[j], ring[(j + 1) % len(ring)]], m)
def strip_card(acc, tree, pts2d, off, m, rows, cols=2, gamma=1.0):
    """A shape as rows of cols+1 points across (left .. right) on the surface; top and bottom rows may be points.
    gamma > 1 packs the rows toward the top (where the jacket surface turns fast)."""
    ys = [p[1] for p in pts2d]; y0, y1 = min(ys), max(ys); R_ = []
    n = len(pts2d)
    for k in range(rows + 1):
        y = y0 + (y1 - y0) * (k / rows) ** gamma; y = min(max(y, y0 + 0.05), y1 - 0.05)
        xs = []
        for i in range(n):
            (xa, ya), (xb, yb) = pts2d[i], pts2d[(i + 1) % n]
            if (ya - y) * (yb - y) <= 0 and ya != yb: xs.append(xa + (xb - xa) * (y - ya) / (yb - ya))
        xl, xr = min(xs), max(xs)
        R_.append([acc.v(front_hit(tree, xl + (xr - xl) * c / cols - 150, y, off)[0], (0, -1, 0)) for c in range(cols + 1)])
    for a, b in zip(R_, R_[1:]):
        for c in range(cols):
            q = (a[c], a[c + 1], b[c + 1], b[c]); acc.f([q[0], q[1], q[2]], m); acc.f([q[0], q[2], q[3]], m)
def line_card(acc, tree, d, width, off, m, n=4):
    pts = R.path_points(d, n); L, Rr = [], []
    for i, p in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]; tx, ty = b[0] - a[0], b[1] - a[1]; l = math.hypot(tx, ty)
        nx, ny = -ty / l * width / 2, tx / l * width / 2
        L.append(acc.v(front_hit(tree, p[0] + nx - 150, p[1] + ny, off)[0], (0, -1, 0)))
        Rr.append(acc.v(front_hit(tree, p[0] - nx - 150, p[1] - ny, off)[0], (0, -1, 0)))
    for i in range(len(pts) - 1): acc.f([L[i], L[i + 1], Rr[i + 1]], m); acc.f([L[i], Rr[i + 1], Rr[i]], m)
LAND = {}
# face (on the head): eyes with glints, brows
for (ex, ey) in R.EYES:
    fan_card(DEC, HTREE, clean(R.path_points(R.oval(ex, ey, 6.5, 9.5), 2)), 0.4, 'ink')
    if not BLOCKOUT: fan_card(DEC, HTREE, clean(R.path_points(R.oval(ex + 2, ey - 3.5, 2.0, 2.4), 1)), 0.6, 'white')
if not BLOCKOUT:
    for d in R.BROWS: line_card(DEC, HTREE, d, 3.0, 0.4, 'brow')
# mouths (swap parts)
strip_card(MOUTH['grin'], HTREE, clean(R.path_points(R.SMILE, 6)), 0.6, 'ink', 3, cols=3, gamma=0.8)
if not BLOCKOUT: strip_card(MOUTH['grin'], HTREE, clean(R.path_points(R.TEETH, 6)), 0.85, 'white', 1, cols=3)
fan_card(MOUTH['o'], HTREE, clean(R.path_points(R.oval(150, 121, 7, 5), 3)), 0.45, 'ink')
# shirt V, collar wings, tie, button (on the jacket); ink cards under the coloured cards
V2 = clean(R.path_points(R.SHIRT_V, 4))
if not BLOCKOUT: strip_card(DEC, JTREE, offset2d(V2, 1.3), 0.4, 'ink', 5, gamma=1.6)
strip_card(DEC, JTREE, V2, 0.6, 'shirt', 5, gamma=1.6)
if not BLOCKOUT:
    for cpath in R.COLLAR:
        corners = [(x, y + 3.0) for x, y in clean(R.path_points(cpath, 2))]   # each wing: a curved triangle, 3 units
        fan_card(DEC, JTREE, offset2d(corners, 0.9), 0.8, 'ink'); fan_card(DEC, JTREE, corners, 1.0, 'shirt')   # lower, off the steep neck top
BLADE = clean(R.path_points(R.TIE_BLADE, 3)); KNOT = [(142, 159), (158, 159), (155, 171), (145, 171)]
if not BLOCKOUT:
    strip_card(DEC, JTREE, offset2d(BLADE, 1.4), 1.1, 'tieink', 4); fan_card(DEC, JTREE, offset2d(KNOT, 1.4), 1.5, 'tieink')
strip_card(DEC, JTREE, BLADE, 1.3, 'tie', 4); fan_card(DEC, JTREE, KNOT, 1.7, 'tie')
if not BLOCKOUT: fan_card(DEC, JTREE, clean(R.path_points(R.oval(*R.BUTTON, 3.2, 3.2), 2)), 0.3, 'ink')
LAND['knot_top'] = front_hit(JTREE, 0, 159, 1.7)[0]; LAND['v_point'] = front_hit(JTREE, 0, 232, 1.3)[0]
LAND['collar_top'] = front_hit(JTREE, 0, 152, 1.2)[0]
decals, _, _ = make_mesh('decals', DEC, smooth=False)
mouths = {k: make_mesh('mouth_' + k, a, smooth=False)[0] for k, a in MOUTH.items()}
BODYTREE = BVHTree.FromPolygons([tuple(v) for v in BODY.V], BODY.F)
def orient_out(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.normal_update()
    for f in bm.faces:
        c = f.calc_center_median(); loc, nrm, _, _ = BODYTREE.find_nearest(c)
        if f.normal.dot(nrm) < 0: f.normal_flip()
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
for o in [decals] + list(mouths.values()): orient_out(o)

# ================================================================ RIG + SKIN
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root
bnc = bpy.data.objects.new('bounce', None); COL.objects.link(bnc); bnc.parent = flt
arm_d = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm_d); COL.objects.link(rig); rig.parent = bnc
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
b0 = arm_d.edit_bones.new('body_root'); b0.head = (0, 0, 0); b0.tail = (0, 0, (340 - 56) * U)
for side, a in ARM.items():
    bu = arm_d.edit_bones.new('arm_%s_up' % side); bu.head = a['S']; bu.tail = a['E']; bu.parent = b0
    bl = arm_d.edit_bones.new('arm_%s_lo' % side); bl.head = a['E']; bl.tail = a['H']; bl.parent = bu; bl.use_connect = False
bpy.ops.object.mode_set(mode='OBJECT')
body.parent = rig
mod = body.modifiers.new('skin', 'ARMATURE'); mod.object = rig
groups = {}
for nv, ov in enumerate(BUSED):
    bn = BODY.VB[ov]
    if bn not in groups: groups[bn] = body.vertex_groups.new(name=bn)
    groups[bn].add([nv], 1.0, 'REPLACE')
for o in [decals] + list(mouths.values()): o.parent = bnc
for k, o in mouths.items(): o['variant'] = 'mouth_' + k; o['default_visible'] = (k == 'grin')
for k, v in LAND.items(): decals[k + '_bounce_blender'] = list(v)

# ---------------------------------------------------------------- poses: a two-bone reach, stored as axis + angle
def solve(side, T, pole):
    a = ARM[side]; S, E, H = a['S'], a['E'], a['H']
    L1, L2 = (E - S).length, (H - E).length; d = min((T - S).length, L1 + L2 - 1e-4); dT = (T - S).normalized()
    aa = (L1 * L1 - L2 * L2 + d * d) / (2 * d); hh = math.sqrt(max(L1 * L1 - aa * aa, 0.0))
    pp = (pole - dT * pole.dot(dT)).normalized(); E2 = S + dT * aa + pp * hh
    R1 = (E - S).rotation_difference(E2 - S); H1 = S + R1 @ (H - S)
    R2w = (H1 - E2).rotation_difference(T - E2)
    ax2 = R1.inverted() @ R2w.axis
    return {'arm_%s_up' % side: [*R1.axis, math.degrees(R1.angle)], 'arm_%s_lo' % side: [*ax2, math.degrees(R2w.angle)],
            '_elbow': list(E2)}
# phone: the right hand (viewer-left, -X) to the outer lower face of the right cup (body map C; sheet ON THE PHONE)
PHONE_T = B(-75, 112, -4)          # behind the mic boom (which runs forward from Z 4), so the boom stays in view
POSES = {'phone': solve('R', PHONE_T, Vector((-1.0, 0.25, -0.35)))}
# hop (in the air): both arms out and up (sheet HOP middle frame)
hop = {}
for side, s in (('L', 1), ('R', -1)):
    hop.update({k: v for k, v in solve(side, B(s * 102, 212, 6), Vector((s * 1.0, 0.0, -1.0))).items() if not k.startswith('_')})
POSES['hop_up'] = hop
flt['poses_float_blender'] = {k: {b: v for b, v in p.items() if not b.startswith('_')} for k, p in POSES.items()}
flt['phone_hand_target_blender'] = list(PHONE_T)
flt['hop'] = {'squash_xyz_blender': [1.08, 1.08, 0.88], 'stretch_xyz_blender': [0.96, 0.96, 1.07], 'air_m': 0.16,
              'rule': 'squash only on the bounce (Kit), pivot at the soles (bounce node)'}
flt['drain'] = TOONJ['drain']
flt['height_m'] = H_M
def pose(name=None):
    for pb in rig.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0)
    if name:
        for bn, (x, y, z, deg) in flt['poses_float_blender'][name].items():
            M = rig.data.bones[bn].matrix_local.to_3x3().inverted()
            rig.pose.bones[bn].rotation_quaternion = Quaternion(M @ Vector((x, y, z)), math.radians(deg))
    bpy.context.view_layer.update()
# phone check: the posed hand centre vs the target
pose('phone'); dg = bpy.context.evaluated_depsgraph_get(); be = body.evaluated_get(dg); me = be.to_mesh()
hand_ids = [BREMAP[i] for i in range(SHELLS['arm_R'][0], SHELLS['arm_R'][1]) if BODY.VB[i] == 'arm_R_lo' and i in BREMAP]
hv = [me.vertices[i].co.copy() for i in hand_ids]; be.to_mesh_clear()
pb = rig.pose.bones['arm_R_lo']; hand_now = (rig.matrix_world @ pb.matrix) @ (rig.data.bones['arm_R_lo'].matrix_local.inverted() @ ARM['R']['H'])
pose(None)

# ================================================================ REPORT + EXPORT
def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {'body': tris(body), 'decals': tris(decals), 'mouth_grin': tris(mouths['grin']), 'mouth_o': tris(mouths['o'])}
counts['visible_rest (body + decals + mouth_grin)'] = counts['body'] + counts['decals'] + counts['mouth_grin']
shell_tris = {}
for nm, (v0, v1, f0, f1) in SHELLS.items():
    shell_tris[nm] = sum(len(f) - 2 for f in BODY.F[f0:f1])
counts['body_by_part'] = shell_tris
checks = {'body_nonmanifold_edges': nonman, 'body_boundary_edges (head bottom ring, jacket top ring, leg ends, band ends)': boundary,
          'faces_facing_in_by_shell': inward, 'height_m': H_M, 'unit_mm': round(U * 1000, 3),
          'phone_hand_centre_to_target_mm': round((hand_now - PHONE_T).length * 1000, 1),
          'decal_offsets_units': 'eyes, brows 0.4 / glints 0.6; mouth 0.6 / teeth 0.85; V ink 0.4 / shirt 0.6; collar ink 0.8 / 1.0; tie ink 1.1 / 1.3; knot 1.5 / 1.7',
          'faces_rewound_to_analytic_normals': REWOUND, 'band_extra_gap_to_hair_units': BAND_GAP_UNITS, 'band_scale': round(kk, 3), 'skin_unweighted': sum(1 for v in body.data.vertices if not v.groups)}
meshes = [o.name for o in bpy.data.objects if o.type == 'MESH']
report = {'triangles': counts, 'meshes': {'all': meshes, 'non_swap (<= 3)': ['body', 'decals'], 'swap': ['mouth_grin', 'mouth_o']},
          'checks': checks, 'hairline_front_view_y_by_deg': HAIRLINE, 'poses': flt['poses_float_blender'].to_dict()}
print('RICKY_REPORT', json.dumps(counts), json.dumps(checks))
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump(TOONJ, open(os.path.join(OUT, 'ricky_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, bnc, rig, body, decals] + list(mouths.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('RICKY_DONE')
