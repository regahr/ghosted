# GHOSTED - The Panel v1: table + Ms. Culture Fit + Mr. Whiteboard + the Camera-Off box, built to the accepted sketch
# (assets/panel/sketch, direction A). Pipeline = Juno v1 (Blender build -> glb -> ingame.html in three.js).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_panel.py -- [blockout]
# Numbers come from the sketch model (../sketch/src/panel.py, juno.py): 1 u = 1/300 m. World u: X right, H up,
# Z toward the player (front view). Blender: (X, -Z, H) * U. glTF: Y up, the set faces +Z in three.js.
# Meshes (4 non-swap): table (with chairs), cf, wb, box. Swaps: eyes, brows, mouths, marker poses, box icons.
# Joins and hardest parts: direction.md.
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Quaternion, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import panel as PN
import juno as J
from ricky import path_points, profile, r_at
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
OUT = os.path.join(HERE, 'blockout') if BLOCKOUT else HERE
if any(a.startswith('out=') for a in ARGV): OUT = os.path.join(HERE, next(a[4:] for a in ARGV if a.startswith('out=')))
NAME = 'panel_blockout' if BLOCKOUT else 'panel'
U = 1 / 300.0
PI = math.pi
ROW = PN.ROW
PAL = {'table': ROW[24], 'post': ROW[22], 'box': ROW[22], 'skin': ROW[15], 'hair': ROW[25], 'lilac': ROW[10],
       'cream': ROW[12], 'navy': ROW[26], 'shirt': ROW[8], 'cheek': ROW[6], 'pen_red': ROW[21], 'pen_blue': ROW[9],
       'pocket': ROW[23], 'markercap': ROW[21], 'marker': ROW[23],
       'ink': ROW[22], 'hairink': ROW[22], 'white': ROW[23], 'icon': ROW[12]}
BASIC = ['ink', 'hairink', 'white', 'icon']
NEUTRAL = [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]]
TOONJ = {'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC,
         'contact_shadow': {'rx': 1.18, 'ry': 0.52, 'opacity': 0.25}}

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

def BV(p):  # world u (X, H, Z) -> Blender metres
    return Vector((p[0] * U, -p[2] * U, p[1] * U))

# ================================================================ mesh accumulator
class Acc:
    def __init__(s, bone): s.V, s.F, s.FM, s.FS, s.VB, s.OW, s.bone = [], [], [], [], [], [], bone
    def v(s, p, bone=None, ow=1.0):
        s.V.append(tuple(p)); s.VB.append(bone or s.bone); s.OW.append(ow); return len(s.V) - 1
    def f(s, ids, m, smooth=True): s.F.append(list(ids)); s.FM.append(m); s.FS.append(smooth)
    def tris(s): return sum(len(f) - 2 for f in s.F)

# local part frames: a function (X, H, Z) -> world (X, H, Z)
def rot_x(deg, piv):   # positive: the top goes toward the player (+Z), the face turns down
    a = math.radians(deg); c, s_ = math.cos(a), math.sin(a)
    def f(p):
        h, z = p[1] - piv[1], p[2] - piv[2]
        return (p[0], piv[1] + h * c - z * s_, piv[2] + h * s_ + z * c)
    return f
def chain(*fs):
    def g(p):
        for f in fs: p = f(p)
        return p
    return g
IDENT = lambda p: p

def ellipsoid(acc, c, r, cols, lats, m, xf=IDENT, bone=None, rot=None, ow=1.0, smooth=True):
    rings = []
    for i in range(1, lats):
        th = PI * i / lats; ring = []
        for j in range(cols):
            ph = 2 * PI * j / cols
            p = (r[0] * math.sin(th) * math.sin(ph), r[1] * math.cos(th), r[2] * math.sin(th) * math.cos(ph))
            if rot: p = rot(p)
            ring.append(acc.v(xf((c[0] + p[0], c[1] + p[1], c[2] + p[2])), bone, ow))
        rings.append(ring)
    top = (0, r[1], 0); bot = (0, -r[1], 0)
    if rot: top, bot = rot(top), rot(bot)
    pt = acc.v(xf((c[0] + top[0], c[1] + top[1], c[2] + top[2])), bone, ow)
    pb = acc.v(xf((c[0] + bot[0], c[1] + bot[1], c[2] + bot[2])), bone, ow)
    n = cols
    for j in range(n): acc.f([pt, rings[0][(j + 1) % n], rings[0][j]][::-1], m, smooth)
    for k in range(len(rings) - 1):
        A, B_ = rings[k], rings[k + 1]
        for j in range(n): acc.f([A[j], B_[j], B_[(j + 1) % n], A[(j + 1) % n]], m, smooth)
    for j in range(n): acc.f([pb, rings[-1][j], rings[-1][(j + 1) % n]][::-1], m, smooth)

def frame(d):
    d = Vector(d).normalized(); up = Vector((0, 1, 0)) if abs(d.y) < 0.9 else Vector((1, 0, 0))
    a = d.cross(up).normalized(); b = a.cross(d).normalized(); return a, b

def tube(acc, pts, radii, sides, m, xf=IDENT, bone=None, cap_end=False, cap_start=False, ow=1.0, phase=0.0):
    rings = []
    for i, p in enumerate(pts):
        d = Vector(pts[min(i + 1, len(pts) - 1)]) - Vector(pts[max(i - 1, 0)])
        a, b = frame(d); ring = []
        for j in range(sides):
            t = 2 * PI * (j + phase) / sides
            q = Vector(p) + (a * math.cos(t) + b * math.sin(t)) * radii[i]
            ring.append(acc.v(xf(tuple(q)), bone, ow))
        rings.append(ring)
    for k in range(len(rings) - 1):
        A, B_ = rings[k], rings[k + 1]
        for j in range(sides): acc.f([A[j], A[(j + 1) % sides], B_[(j + 1) % sides], B_[j]], m)
    if cap_end: acc.f(rings[-1], m, False)
    if cap_start: acc.f(rings[0][::-1], m, False)

def box(acc, c, size, m, xf=IDENT, bone=None, skip=(), ow=1.0, inset_top=0.0):
    """Flat box. skip: faces to leave out ('bottom', 'back', ...). inset_top: a chamfer ring on the top edges."""
    x, y, z = c; hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    def P(sx, sy, sz, ins=0.0, dy=0.0): return acc.v(xf((x + sx * (hx - ins), y + sy * hy + dy, z + sz * (hz - ins))), bone, ow)
    if inset_top <= 0:
        v = {k: P(*k) for k in [(sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]}
        faces = {'top': [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)], 'bottom': [(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)],
                 'front': [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)], 'back': [(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)],
                 'right': [(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)], 'left': [(-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)]}
        for k, f in faces.items():
            if k not in skip: acc.f([v[q] for q in f], m, False)
        return
    # chamfered top: bottom ring, side-top ring (inset_top below the top), top ring (inset)
    order = [(-1, -1), (1, -1), (1, 1), (-1, 1)]   # (sx, sz) counter-clockwise seen from above (+H)
    bot = [P(sx, -1, sz) for sx, sz in order]
    mid = [P(sx, 1, sz, 0.0, -inset_top) for sx, sz in order]
    top = [P(sx, 1, sz, inset_top) for sx, sz in order]
    for i in range(4):
        j = (i + 1) % 4
        acc.f([bot[i], mid[i], mid[j], bot[j]][::-1], m, False)
        acc.f([mid[i], top[i], top[j], mid[j]][::-1], m, False)
    acc.f(top[::-1][::-1], m, False)
    if 'bottom' not in skip: acc.f(bot[::-1], m, False)

# ================================================================ the set layout (sketch panel.py)
TT = PN.TABLE_TOP; TW, TD, TTH = PN.TABLE_W, PN.TABLE_D, PN.TABLE_T
SEAT_Z, DH = PN.SEAT_Z, PN.DH
SEATS = PN.SEATS
TABLE = Acc('set')
# top slab
box(TABLE, (0, TT - TTH / 2, 0), (TW, TTH, TD), 'table', skip=('bottom',))
# front panel (hides the legs) and two side panels: a 'panel' desk, inset under the top
box(TABLE, (0, (TT - TTH) / 2 + 3, TD / 2 - 12), (TW - 24, TT - TTH - 6, 6), 'table', skip=('top', 'bottom'))
for s in (-1, 1):
    box(TABLE, (s * (TW / 2 - 14), (TT - TTH) / 2 + 3, -4), (6, TT - TTH - 6, TD - 24), 'table', skip=('top', 'bottom'))
# chairs (behind the people): seat, back, one dark post
for who in ('cf', 'wb'):
    sx = SEATS[who]
    box(TABLE, (sx, 143, SEAT_Z - 18), (84, 8, 80), 'table', skip=('bottom',))
    box(TABLE, (sx, 196, SEAT_Z - 54), (80, 92, 7), 'table', skip=('bottom',))
    box(TABLE, (sx, 70, SEAT_Z - 18), (9, 140, 9), 'post', skip=('top', 'bottom'))

# ================================================================ the people
HEAD_PROF = profile(J.HEAD_HALF, 40); CAP_PROF = profile(J.CAP_HALF, 40)
HEAD_D0 = 0.92
JAW = float(next((a[4:] for a in ARGV if a.startswith('jaw=')), 0.0))     # extra depth of the lower face (game-camera mouth gap)
CHINW = float(next((a[6:] for a in ARGV if a.startswith('chinw=')), 0.35))   # ink hull weight on the lower front face
MS = float(next((a[3:] for a in ARGV if a.startswith('ms=')), 4.0))       # mouths raised by MS u more than the sketch
def HEAD_D(y):
    t = min(max((y - 108.0) / 30.0, 0.0), 1.0); t = t * t * (3 - 2 * t)
    return HEAD_D0 + JAW * t
def r_head(y): return r_at(HEAD_PROF, y) if y >= HEAD_PROF[0][0] else 0.0
def r_cap(y): return r_at(CAP_PROF, y) if y >= CAP_PROF[0][0] else 0.0
# hairline: front-view y of the hair edge by column angle (deg from the front). Sketch: y 64 at the centre, 86 at the
# sides in front of the ears (ear top y 95), then down behind the ear to the nape.
HAIRLINE = [(0, 64.0), (30, 66.0), (60, 73.0), (80, 82.0), (95, 87.0), (115, 104.0), (140, 128.0), (180, 138.0)]
def hair_y(deg):
    d = abs((deg + 180) % 360 - 180)
    for (a0, y0), (a1, y1) in zip(HAIRLINE, HAIRLINE[1:]):
        if a0 <= d <= a1: return y0 + (y1 - y0) * (d - a0) / (a1 - a0)
    return HAIRLINE[-1][1]
NCOL = 8 if BLOCKOUT else 14   # 12 read as a polygon at card size (first final)
CHIN = (0.0, 340 - 154.0, 0.0)          # head pivot (local H 186, the chin)
HEAD_SET = float(next((a[3:] for a in ARGV if a.startswith('hs=')), 8.0))   # rest head: chin up (sketch face-check fix: 8 deg)
def L(x, y, z=0.0): return (x - 150.0, 340.0 - y, z)   # sketch front frame -> person local (X, H, Z)

def head_pt(x_off, y, deg, rfun, out=0.0):
    t = math.radians(deg); r = rfun(y) + out
    return (r * math.sin(t), 340.0 - y, HEAD_D(y) * r * math.cos(t))

def build_head(acc, who, hxf):
    cols = [360.0 * j / NCOL for j in range(NCOL)]
    rings = []   # each: (list of vids, material of the band ABOVE it)
    cap_f = [0.4, 0.75, 1.0] if not BLOCKOUT else [0.5, 1.0]
    skin_f = [0.25, 0.5, 0.75, 0.93] if not BLOCKOUT else [0.33, 0.7, 0.93]
    top_y = CAP_PROF[0][0]
    def ring(fn): return [acc.v(hxf(fn(c)), 'head') for c in cols]
    for f in cap_f:
        rings.append((ring(lambda c, f=f: head_pt(0, top_y + (hair_y(c) - 2.6 - top_y) * f, c, r_cap)), 'hair'))
    rings.append((ring(lambda c: head_pt(0, hair_y(c), c, r_head, 0.4)), 'hairink'))
    for f in skin_f:
        rings.append((ring(lambda c, f=f: head_pt(0, hair_y(c) + (154.0 - hair_y(c)) * f, c, r_head)), 'skin'))
        for j, c in enumerate(cols):   # the chin: a thinner ink line, so a mouth never merges with it (game camera)
            y = hair_y(c) + (154.0 - hair_y(c)) * f; dc = abs((c + 180) % 360 - 180)
            if y > 126 and dc < 75: acc.OW[rings[-1][0][j]] = CHINW
    pt = acc.v(hxf(L(150, top_y)), 'head'); pb = acc.v(hxf(L(150, 154.0)), 'head', CHINW)
    n = NCOL
    for j in range(n): acc.f([pt, rings[0][0][j], rings[0][0][(j + 1) % n]], 'hair')
    for k in range(len(rings) - 1):
        A, Bm = rings[k][0], rings[k + 1][0]; m = rings[k + 1][1]
        for j in range(n): acc.f([A[j], Bm[j], Bm[(j + 1) % n], A[(j + 1) % n]], m)
    for j in range(n): acc.f([pb, rings[-1][0][(j + 1) % n], rings[-1][0][j]], 'skin')
    # ears: layered, half sunk, on the eye line
    for s in (-1, 1):
        ellipsoid(acc, (s * 55, 340 - 105, -4), (5, 10, 7), 6 if not BLOCKOUT else 4, 3, 'skin', hxf, 'head')

# ---- decals: projected on the analytic head (front frame x, y) and torso
def head_proj(x, y, off):
    X = x - 150.0; r = max(r_head(y), abs(X) + 0.01)
    hd_ = HEAD_D(y); zz = hd_ * math.sqrt(max(r * r - X * X, 0.0))
    n = Vector((X / r, 0.0, zz / (hd_ * hd_ * r) if r > 0 else 1.0)).normalized()
    return (X + n.x * off, 340.0 - y, zz + n.z * off)
def body_proj_fn(prof):
    def f(x, y, off):
        r = r_at(prof, y); r = max(r, 26.0) if y < 168 else r
        X = x - 150.0; zz = PN.BODY_D * math.sqrt(max(r * r - X * X, 0.0))
        return (X, 340.0 - y, zz + off)
    return f
def subpaths(d): return ['M' + s for s in d.split('M') if s.strip()]
def fill(acc, d, m, proj, off, xf, bone, n=12):
    for sp in subpaths(d):
        pts = path_points(sp, n)
        if len(pts) > 2 and math.dist(pts[0], pts[-1]) < 0.01: pts = pts[:-1]
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        c = acc.v(xf(proj(cx, cy, off)), bone, 0.0)
        ids = [acc.v(xf(proj(x, y, off)), bone, 0.0) for x, y in pts]
        area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        for i in range(len(ids)):
            tri = [c, ids[i], ids[(i + 1) % len(ids)]]
            acc.f(tri if area < 0 else tri[::-1], m)
def line(acc, d, w, m, proj, off, xf, bone, n=6, closed=False):
    for sp in subpaths(d):
        pts = path_points(sp, n)
        if closed and math.dist(pts[0], pts[-1]) > 0.01: pts = pts + [pts[0]]
        L_, R_ = [], []
        for i, p in enumerate(pts):
            a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1
            nx, ny = -dy / l * w / 2, dx / l * w / 2
            L_.append(acc.v(xf(proj(p[0] + nx, p[1] + ny, off)), bone, 0.0))
            R_.append(acc.v(xf(proj(p[0] - nx, p[1] - ny, off)), bone, 0.0))
        for i in range(len(pts) - 1):
            acc.f([L_[i], L_[i + 1], R_[i + 1], R_[i]], m)

def oval(x, y, rx, ry): return J.R.oval(x, y, rx, ry) if hasattr(J.R, 'oval') else PN.oval(x, y, rx, ry)

PEOPLE = {}; SWAP = {}; ARMS = {}
def up(d, k):
    import re
    out, n = [], 0
    for t in re.split(r'([ ,MCLZ])', d):
        if re.fullmatch(r'-?\d+(\.\d+)?', t or ''):
            out.append(t if n % 2 == 0 else '%g' % (float(t) - k)); n += 1
        else: out.append(t)
    return ''.join(out)
for _k in ('SMILE', 'LAUGH', 'LAUGH_TEETH', 'TALK', 'TALK_TEETH', 'FLAT', 'SMIRK_R'): setattr(PN, _k, up(getattr(PN, _k), MS))
# the grin is 0.8 as tall (about its top edge), so its bottom sits as high as the talk mouth's (chair call 5: skin under it)
def squash(d, y0, k):
    import re
    out, n = [], 0
    for t in re.split(r'([ ,MCLZ])', d):
        if re.fullmatch(r'-?\d+(\.\d+)?', t or ''):
            out.append(t if n % 2 == 0 else '%g' % (y0 + (float(t) - y0) * k)); n += 1
        else: out.append(t)
    return ''.join(out)
_y0 = min(p[1] for p in path_points(PN.LAUGH, 4))
PN.LAUGH, PN.LAUGH_TEETH = squash(PN.LAUGH, _y0, 0.8), squash(PN.LAUGH_TEETH, _y0, 0.8)
def person(who):
    acc = Acc(who + '_lean')
    sx = SEATS[who]
    place = lambda p: (p[0] + sx, p[1] + DH, p[2] + SEAT_Z)
    hxf = chain(rot_x(-HEAD_SET, CHIN), place)
    hb = who + '_head'
    # head + cap (continuous skin), ears
    build_head(acc, who, hxf)
    for v in range(len(acc.VB)): acc.VB[v] = hb
    top, inner = ('lilac', 'cream') if who == 'cf' else ('navy', 'shirt')
    if who == 'cf':
        # low bun at the nape, a cream band over the crown ear to ear, a bow centred on the crown
        ellipsoid(acc, (0, 340 - 128, -54), (24, 22, 20), 6, 4, 'hair', hxf, hb)
        hc = 340 - 106
        pts = [(58.5 * math.sin(math.radians(a)), hc + 57.5 * math.cos(math.radians(a)), -16) for a in range(-84, 85, 28)]
        tube(acc, pts, [3.4] * len(pts), 4, 'cream', hxf, hb, phase=0.5)
        for s in (-1, 1):
            a = 0.35
            rot = lambda p, s=s: (p[0] * math.cos(a) - s * p[1] * math.sin(a), s * p[0] * math.sin(a) + p[1] * math.cos(a), p[2])
            ellipsoid(acc, (s * 17, 340 - 46, -12), (17, 12, 8), 6 if not BLOCKOUT else 4, 4, 'cream', hxf, hb, rot=rot)
        ellipsoid(acc, (0, 340 - 48, -9), (7, 7, 6), 5, 3, 'cream', hxf, hb)
    else:
        # flat-top: a bevelled block on the skull, y 35-60 (blockout 22 u read as a mortarboard in 3/4; 28 u read as a tall hat at the game camera: 25 u); its
        # front-bottom edge 4 u above the hairline (y 60)
        box(acc, (0, 340 - 47.5, -6), (102, 25, 80), 'hair', hxf, hb, inset_top=0 if BLOCKOUT else 4.0)
    # neck (separate, sunk)
    tube(acc, [L(150, 146), L(150, 172)], [14, 14], 6, 'skin', place, who + '_lean')
    # torso: the sketch body profile revolved, depth 0.78, from the neck opening down to the seat
    half = PN.BODY_CF if who == 'cf' else PN.BODY_WB
    bprof = profile(half, 40)
    tcols = 8 if BLOCKOUT else 10
    ys = [158.0, 172, 196, 228, 258] if not BLOCKOUT else [158.0, 190, 240]
    rings = []
    for y in ys:
        r = r_at(bprof, y); ring = []
        for j in range(tcols):
            t = 2 * PI * (j + 0.5) / tcols
            ring.append(acc.v(place((r * math.sin(t), 340 - y, PN.BODY_D * r * math.cos(t)))))
        rings.append(ring)
    pt = acc.v(place(L(150, 156.0))); pb = acc.v(place(L(150, 268.0)))
    for j in range(tcols): acc.f([pt, rings[0][j], rings[0][(j + 1) % tcols]], top)
    for k in range(len(rings) - 1):
        A, Bm = rings[k], rings[k + 1]
        for j in range(tcols): acc.f([A[j], Bm[j], Bm[(j + 1) % tcols], A[(j + 1) % tcols]], top)
    for j in range(tcols): acc.f([pb, rings[-1][(j + 1) % tcols], rings[-1][j]], top)
    # legs under the table (hidden at the front and at the game camera): thigh, shin, shoe
    for s in (-1, 1):
        hip = (s * 22, 150 - DH + 14, 0); knee = (s * 24, 150 - DH + 12, 70); ank = (s * 24, 14 - DH, 78)
        tube(acc, [hip, knee], [17, 15], 5, 'navy', place, 'set')      # legs stay put in the lean (bone 'set')
        tube(acc, [knee, ank], [13, 12], 5, 'navy', place, 'set')
        ellipsoid(acc, (s * 24, 8 - DH, 88), (12, 8, 17), 5, 3, 'post', place, 'set')
    # body decals (fills with no ink edge, sketch)
    bp = body_proj_fn(bprof)
    if who == 'cf':
        fill(acc, PN.V_CF, 'cream', bp, 0.6, place, None, 2)
        line(acc, "M150,192 L150,214", 1.4, 'ink', bp, 0.8, place, None, 2)
        for x, y in PN.CF_BUTTONS: fill(acc, oval(x, y, 3, 3), 'ink', bp, 0.8, place, None, 1)
    else:
        fill(acc, PN.WB_V, 'shirt', bp, 0.6, place, None, 2)
        for d in PN.WB_COLLAR: fill(acc, d, 'shirt', bp, 0.9, place, None, 1)
        fill(acc, PN.WB_POCKET, 'pocket', bp, 0.6, place, None, 1)
        line(acc, PN.WB_POCKET, 1.4, 'ink', bp, 0.9, place, None, 1, closed=True)
        for d, c in PN.WB_PENS: line(acc, d, 2.6, 'pen_red' if c == 21 else 'pen_blue', bp, 1.1, place, None, 2)
    # head decals in the person mesh: cheeks (CF), glasses (WB)
    if who == 'cf':
        for (x, y) in J.CHEEKS: fill(acc, oval(x, y + 2, 7, 4), 'cheek', head_proj, 0.5, hxf, hb, 2)
    else:
        for d in PN.GLASSES: line(acc, d, 2.4, 'ink', head_proj, 1.6, hxf, hb, 3)
    # arms: sleeve tube (sunk at the shoulder), ball cuff at the elbow, forearm, ball hand (rigid, on bones)
    sw = 56 if who == 'cf' else 60
    sleeve = 'lilac' if who == 'cf' else 'shirt'; fore = 'lilac' if who == 'cf' else 'skin'
    T = PN.LOCAL_TABLE_H
    for s, side in ((-1, 'R'), (1, 'L')):          # s -1: viewer's left = the person's RIGHT hand
        sh = (s * sw, 154.0, 0.0); el = (s * 70, T + 11, 62.0); wr = (s * 34, T + 9, 106.0); hd = (s * 16, T + 10, 114.0)
        up, lo = '%s_arm_%s_up' % (who, side), '%s_arm_%s_lo' % (who, side)
        sh_in = tuple(sh[i] + (el[i] - sh[i]) * -0.12 for i in range(3))
        tube(acc, [sh_in, el], [13.0, 11.0], 6, sleeve, place, up)
        ellipsoid(acc, el, (11.5, 11.5, 11.5), 6, 3, sleeve, place, lo)
        tube(acc, [el, wr], [9.0, 8.2], 6, fore, place, lo)
        ellipsoid(acc, hd, (10, 10.5, 9.5), 6, 4, 'skin', place, lo)
        ARMS[(who, side)] = {'S': BV(place(sh)), 'E': BV(place(el)), 'H': BV(place(hd)), 'up': up, 'lo': lo}
    PEOPLE[who] = acc
    # ---- swaps (head bone): eyes, brows, mouths
    def sw_acc(k): a = Acc(hb); SWAP[who + '_' + k] = a; return a
    a = sw_acc('eyes_open')
    for x in (132, 168):
        fill(a, oval(x, 104, 6.5, 8.5), 'ink', head_proj, 0.8, hxf, hb, 3)
        fill(a, oval(x + 2, 100.8, 2.0, 2.4), 'white', head_proj, 1.2, hxf, hb, 1)
    if who == 'cf':
        a = sw_acc('eyes_happy')
        for d in PN.HAPPY_EYES: line(a, d, 3.4, 'ink', head_proj, 0.8, hxf, hb, 3)
        a = sw_acc('brows_rest')
        for d in J.BROWS: line(a, d, 2.6, 'ink', head_proj, 0.8, hxf, hb, 3)
        a = sw_acc('brows_tilt')
        for d in PN.BROWS_CF_TILT: line(a, d, 2.6, 'ink', head_proj, 0.8, hxf, hb, 3)
        a = sw_acc('mouth_smile'); line(a, PN.SMILE, 2.8, 'ink', head_proj, 0.8, hxf, hb, 4)
        a = sw_acc('mouth_grin')
        m_, t_ = PN.LAUGH, PN.LAUGH_TEETH; fill(a, m_, 'ink', head_proj, 0.8, hxf, hb, 3); fill(a, t_, 'white', head_proj, 1.2, hxf, hb, 2)
    else:
        a = sw_acc('brows_rest')
        for d in PN.BROWS_WB: line(a, d, 2.8, 'ink', head_proj, 0.8, hxf, hb, 2)
        a = sw_acc('brows_up')
        for d in PN.BROWS_WB_UP: line(a, d, 2.8, 'ink', head_proj, 0.8, hxf, hb, 4)
        a = sw_acc('mouth_flat'); line(a, PN.FLAT, 2.8, 'ink', head_proj, 0.8, hxf, hb, 4)
    a = sw_acc('mouth_talk')
    m_, t_ = PN.TALK, PN.TALK_TEETH; fill(a, m_, 'ink', head_proj, 0.8, hxf, hb, 3); fill(a, t_, 'white', head_proj, 1.2, hxf, hb, 2)
    a = sw_acc('mouth_smirk'); line(a, PN.SMIRK_R, 2.8, 'ink', head_proj, 0.8, hxf, hb, 4)
    return place

PLACE = {w: person(w) for w in ('cf', 'wb')}

# ================================================================ the box (Camera-Off One) + icon swaps
BX, BY, BZ = PN.BOX
BOXC = (SEATS['box'], TT + BY / 2, PN.BOX_Z)
BOXA = Acc('box')
box(BOXA, BOXC, (BX, BY, BZ), 'box', skip=('bottom',))
FZ = BOXC[2] + BZ / 2
def icon_proj(x, y, off): return (BOXC[0] + x, BOXC[1] + y, FZ + off)    # icon units: u on the face, y up
def ifill(acc, pts, m, off):
    c = acc.v(icon_proj(sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts), off), None, 0.0)
    ids = [acc.v(icon_proj(x, y, off), None, 0.0) for x, y in pts]
    for i in range(len(ids)): acc.f([c, ids[i], ids[(i + 1) % len(ids)]], m)
def istrip(acc, pts, w, m, off):
    Lp, Rp = [], []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1; nx, ny = -dy / l * w / 2, dx / l * w / 2
        Lp.append(acc.v(icon_proj(p[0] + nx, p[1] + ny, off), None, 0.0)); Rp.append(acc.v(icon_proj(p[0] - nx, p[1] - ny, off), None, 0.0))
    for i in range(len(pts) - 1): acc.f([Rp[i], Rp[i + 1], Lp[i + 1], Lp[i]], m)
def slash(acc):
    a, b = (-30, -27), (30, 27)
    dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy); nx, ny = -dy / l, dx / l
    for k in (-1, 1): istrip(acc, [(a[0] + k * nx * 6, a[1] + k * ny * 6), (b[0] + k * nx * 6, b[1] + k * ny * 6)], 4.5, 'box', 1.2)
    istrip(acc, [a, b], 7.5, 'icon', 1.4)
ICON_CAM = Acc('box')
ifill(ICON_CAM, [(-30, -15), (8, -15), (8, 15), (-30, 15)], 'icon', 0.8)
ifill(ICON_CAM, [(8, 0), (28, -13), (28, 13)], 'icon', 0.8)
slash(ICON_CAM)
ICON_MUTE = Acc('box')
cap = [(-9, 22)] + [(9 * math.cos(PI - PI * k / 6), 22 + 9 * math.sin(PI * k / 6) * 0.9) for k in range(7)] + [(9, -2)] + \
      [(9 * math.cos(-PI * k / 6), -2 - 9 * math.sin(PI * k / 6) * 0.9) for k in range(1, 6)] + [(-9, -2)]
ifill(ICON_MUTE, [(-9, -2), (-9, 22)] + [(9 * math.cos(PI - PI * k / 6), 22 + 8 * math.sin(PI * k / 6)) for k in range(1, 6)] +
      [(9, 22), (9, -2)] + [(9 * math.cos(-PI * k / 6), -2 - 8 * math.sin(PI * k / 6)) for k in range(1, 6)], 'icon', 0.8)
istrip(ICON_MUTE, [(16 * math.cos(math.radians(a)), 2 + 16 * math.sin(math.radians(a))) for a in range(180, 361, 30)], 4.5, 'icon', 0.8)
istrip(ICON_MUTE, [(0, -14), (0, -24)], 4.5, 'icon', 0.8)
istrip(ICON_MUTE, [(-11, -25), (11, -25)], 4.5, 'icon', 0.8)
slash(ICON_MUTE)
SWAP['icon_camoff'] = ICON_CAM; SWAP['icon_muted'] = ICON_MUTE

# ================================================================ poses (two-bone reach, = Juno solve) + marker swaps
def solve(who, side, T, pole):
    a = ARMS[(who, side)]; S0, E, H = a['S'], a['E'], a['H']
    L1, L2 = (E - S0).length, (H - E).length; d = min((T - S0).length, L1 + L2 - 1e-4); dT = (T - S0).normalized()
    aa = (L1 * L1 - L2 * L2 + d * d) / (2 * d); hh = math.sqrt(max(L1 * L1 - aa * aa, 0.0))
    pp = (pole - dT * pole.dot(dT)).normalized(); E2 = S0 + dT * aa + pp * hh
    R1 = (E - S0).rotation_difference(E2 - S0); H1 = S0 + R1 @ (H - S0)
    R2w = (H1 - E2).rotation_difference(T - E2)
    ax2 = R1.inverted() @ R2w.axis
    pose = {a['up']: [*R1.axis, math.degrees(R1.angle)], a['lo']: [*ax2, math.degrees(R2w.angle)]}
    to_bind = lambda pw: E + R1.inverted() @ (R2w.inverted() @ (pw - E2))   # posed world -> bind (lower arm)
    return pose, to_bind, (T - (E2 + R2w @ (H1 - E2))).length
POSES = {}; MARK = {}; ERR = {}
def arm_pose(who, side, hd, el):
    return solve(who, side, BV(PLACE[who](hd)), BV(PLACE[who](el)) - ARMS[(who, side)]['S'])
T = PN.LOCAL_TABLE_H
# WB: marker up (click), point; CF: both hands under the chin (tilt)
p_up, bind_up, e1 = arm_pose('wb', 'R', (-52, T + 62, 84), (-72, T + 11, 60))
p_pt, bind_pt, e2 = arm_pose('wb', 'R', (-34, T + 37, 124), (-66, T + 26, 54))
cR, _, e3 = arm_pose('cf', 'R', (-24, 340 - 156, 46), (-60, T + 11, 66))
cL, _, e4 = arm_pose('cf', 'L', (24, 340 - 156, 46), (60, T + 11, 66))
ERR = {'wb_up': e1 / U, 'wb_point': e2 / U, 'cf_chin_R': e3 / U, 'cf_chin_L': e4 / U}
X_AX = [1.0, 0.0, 0.0]
POSES = {
    'cf_nod': {'cf_head': [*X_AX, 14.0]},
    'cf_tilt': {'cf_head': [0.0, 1.0, 0.0, -12.0], **cR, **cL},
    'wb_up': p_up, 'wb_click': p_up, 'wb_point': p_pt,
    # the heads counter-turn 12 deg chin-up in the lean, so the faces stay on the player (first final: the lean tipped
    # the faces down and the mouths met the chin line at 1x)
    'lean': {'cf_lean': [*X_AX, 14.0], 'wb_lean': [*X_AX, 14.0], 'box': [*X_AX, 12.0], 'cf_head': [*X_AX, -12.0], 'wb_head': [*X_AX, -12.0]},
}
def marker(acc, a, b, to_bind=None):
    xf = (lambda p: p) if to_bind is None else None
    da = Vector(b) - Vector(a); tip = tuple(Vector(b) + da.normalized() * 9)
    pts = [a, b]
    def wpt(p):  # person-local -> world u, then to bind if needed
        w = PLACE['wb'](p)
        if to_bind is None: return w
        q = to_bind(BV(w)); return (q.x / U, q.z / U, -q.y / U)
    tube(acc, pts, [3.6, 3.6], 6, 'marker', wpt, 'wb_arm_R_lo', cap_start=True)
    tube(acc, [b, tip], [4.2, 4.2], 6, 'markercap', wpt, 'wb_arm_R_lo', cap_end=True)
hd = (-16, T + 10, 114)
MK = {k: Acc('wb_arm_R_lo') for k in ('marker_rest', 'marker_up', 'marker_point')}
marker(MK['marker_rest'], (hd[0] + 6, hd[1] + 2, hd[2] + 4), (hd[0] + 34, hd[1] + 2, hd[2] + 10))
hu = (-52, T + 62, 84); marker(MK['marker_up'], (hu[0] + 2, hu[1] + 6, hu[2] + 2), (hu[0] + 2, hu[1] + 34, hu[2] + 2), bind_up)
hp = (-34, T + 37, 124); marker(MK['marker_point'], (hp[0] + 2, hp[1] + 1, hp[2] + 6), (hp[0] + 6, hp[1] + 3, hp[2] + 36), bind_pt)
SWAP.update(MK)

# ================================================================ build meshes
def make_mesh(name, acc):
    used = sorted(set(i for f in acc.F for i in f)); remap = {o: n for n, o in enumerate(used)}
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(BV(acc.V[i])) for i in used], [], [[remap[i] for i in f] for f in acc.F])
    names = sorted(set(acc.FM), key=lambda m: list(PAL).index(m))
    for m in names: me.materials.append(mat(m))
    me.polygons.foreach_set('material_index', [names.index(m) for m in acc.FM])
    me.polygons.foreach_set('use_smooth', acc.FS); me.update()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY')
    bm.verts.ensure_lookup_table()
    ow_of = lambda v: acc.OW[used[v.index]]
    shells = [f for f in bm.faces if all(ow_of(v) > 0.5 for v in f.verts)]
    bmesh.ops.recalc_face_normals(bm, faces=shells)
    for f in bm.faces:
        if f not in shells:
            f.normal_update()
            if f.normal.y > 0: f.normal_flip()
    bm.to_mesh(me); bm.free()
    me.color_attributes.new('outline_wc', 'FLOAT_COLOR', 'POINT')
    ca = me.color_attributes['outline_wc']
    for nv, ov in enumerate(used): w = acc.OW[ov]; ca.data[nv].color = (w, w, w, 1.0)
    me.color_attributes.active_color_index = 0; me.color_attributes.render_color_index = 0
    me.update()
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob)
    return ob, used

# ================================================================ RIG
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root
arm_d = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm_d); COL.objects.link(rig); rig.parent = flt
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
def eb(name, h, t, parent=None):
    b = arm_d.edit_bones.new(name); b.head = h; b.tail = t
    if parent: b.parent = arm_d.edit_bones[parent]
    return b
eb('set', (0, 0, 0), (0, 0, 0.2))
for who in ('cf', 'wb'):
    pl = PLACE[who]
    eb(who + '_lean', BV(pl((0, 140, -10))), BV(pl((0, 200, -10))), 'set')
    eb(who + '_head', BV(pl(CHIN)), BV(pl((0, 280, 0))), who + '_lean')
    for side in ('R', 'L'):
        a = ARMS[(who, side)]
        eb(a['up'], a['S'], a['E'], 'set'); eb(a['lo'], a['E'], a['H'], a['up'])
eb('box', BV((SEATS['box'], TT, PN.BOX_Z + BZ / 2)), BV((SEATS['box'], TT + 60, PN.BOX_Z + BZ / 2)), 'set')
bpy.ops.object.mode_set(mode='OBJECT')
def skin(ob, acc, used):
    ob.parent = rig
    mod = ob.modifiers.new('skin', 'ARMATURE'); mod.object = rig
    groups = {}
    for nv, ov in enumerate(used):
        bn = acc.VB[ov] or acc.bone
        if bn not in groups: groups[bn] = ob.vertex_groups.new(name=bn)
        groups[bn].add([nv], 1.0, 'REPLACE')
OBJ = {}
for name, acc in [('table', TABLE), ('cf', PEOPLE['cf']), ('wb', PEOPLE['wb']), ('box_body', BOXA)] + list(SWAP.items()):
    ob, used = make_mesh(name, acc); skin(ob, acc, used); OBJ[name] = ob
    if name in SWAP: ob['variant'] = name

flt['poses_float_blender'] = POSES
flt['unit_m'] = U
EXPR = {
    'cf': {'rest': ['eyes_open', 'brows_rest', 'mouth_smile'], 'talk': ['eyes_open', 'brows_rest', 'mouth_talk'],
           'grin': ['eyes_happy', 'brows_rest', 'mouth_grin'], 'tilt': ['eyes_open', 'brows_tilt', 'mouth_smirk']},
    'wb': {'rest': ['eyes_open', 'brows_rest', 'mouth_flat'], 'talk': ['eyes_open', 'brows_rest', 'mouth_talk'],
           'skeptic': ['eyes_open', 'brows_up', 'mouth_smirk']},
}
flt['expressions'] = EXPR
LMB = {}
for who in ('cf', 'wb'):
    hx = chain(rot_x(-HEAD_SET, CHIN), PLACE[who]); hb = who + '_head'
    LMB[who] = {'cap_top': [hb, list(BV(hx(L(150, CAP_PROF[0][0]))))], 'hairline': [hb, list(BV(hx(head_proj(150, 64, 0))))],
                'eye_l': [hb, list(BV(hx(head_proj(132, 104, 0))))], 'eye_r': [hb, list(BV(hx(head_proj(168, 104, 0))))],
                'mouth': [hb, list(BV(hx(head_proj(150, 126, 0))))], 'chin': [hb, list(BV(hx(head_proj(150, 152, 0))))],
                'ear_l': [hb, list(BV(hx(L(95, 105, -4))))], 'ear_r': [hb, list(BV(hx(L(205, 105, -4))))]}
LMB['set'] = {'table_front_top': ['set', list(BV((0, TT, TD / 2)))], 'table_front_bottom': ['set', list(BV((0, 0, TD / 2)))],
              'box_icon': ['box', list(BV((BOXC[0], BOXC[1], FZ)))], 'box_top': ['box', list(BV((BOXC[0], TT + BY, FZ)))]}
flt['landmarks_bind'] = LMB
flt['landmarks_u'] = {'cf_head': list(PLACE['cf'](CHIN)), 'wb_head': list(PLACE['wb'](CHIN)), 'seats': dict(SEATS), 'table_top': TT,
                      'table': [TW, TTH, TD], 'box': [*BOXC, BX, BY, BZ]}

# ================================================================ REPORT + EXPORT
def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {k: tris(o) for k, o in OBJ.items()}
base = counts['table'] + counts['cf'] + counts['wb'] + counts['box_body']
def vis(cf, wb, mk, icon):
    t = base + sum(counts['cf_' + x] for x in EXPR['cf'][cf]) + sum(counts['wb_' + x] for x in EXPR['wb'][wb]) + counts[mk]
    return t + (counts[icon] if icon else 0)
visible = {'game idle (talk, talk, marker_rest, camoff)': vis('talk', 'talk', 'marker_rest', 'icon_camoff'),
           'card rest': vis('rest', 'rest', 'marker_rest', 'icon_camoff'),
           'cf grin + wb point + muted': vis('grin', 'talk', 'marker_point', 'icon_muted'),
           'max (grin, talk, point, muted)': max(vis(c, w, m, i) for c in EXPR['cf'] for w in EXPR['wb']
                                                for m in ('marker_rest', 'marker_up', 'marker_point') for i in ('icon_camoff', 'icon_muted', None))}
by_part = {'head (cap + skin + ears), each': None}
report = {'triangles': counts, 'visible': visible, 'base_non_swap': base,
          'meshes': {'non_swap (<= 4)': ['table', 'cf', 'wb', 'box_body'], 'swap': list(SWAP)},
          'ik_error_u': ERR, 'unit_mm': round(U * 1000, 3), 'poses': POSES}
print('PANEL_REPORT', json.dumps(visible), json.dumps(counts))
os.makedirs(OUT, exist_ok=True)
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump(TOONJ, open(os.path.join(OUT, 'panel_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, rig] + list(OBJ.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False, export_vertex_color='ACTIVE')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('PANEL_DONE')
