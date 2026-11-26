# GHOSTED - ATS-9000 v1: blockout and final model, built to the accepted sketch v2 (assets/ats9000/sketch).
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_ats.py -- [blockout|test] [H=1.25] [out=<dir>]
# First: python3 make_textures.py (tex/*.png). Brief: design/acceptance/ats9000/build-brief-3d.md. Joins: direction.md.
# Shapes: the profiles come from the sketch's hand-drawn Bezier paths (../sketch/src/ats.py), read here.
# Sketch units: X = x - 150 (+X = viewer-right = the robot's LEFT), y down (ground y 340), Z forward. 1 u = H / 334 m.
# Blender: Z-up, the robot faces -Y. glTF: Y-up (faces +Z in three.js).
# Nodes: root > float > bounce > body (static), screen, stamp_pivot > stamp; root > cv (prop, hidden by default).
import bpy, bmesh, math, json, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import ats as A
ARGV = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
BLOCKOUT = 'blockout' in ARGV
TEST = 'test' in ARGV
H_M = 1.22          # total height, ground to the antenna ball top; set by the blockout measure (measure.md: 1.25 m gave 93 px)
OUT = HERE
for a in ARGV:
    if a.startswith('H='): H_M = float(a[2:])
    if a.startswith('out='): OUT = os.path.join(HERE, a[4:]); os.makedirs(OUT, exist_ok=True)
NAME = 'ats_test' if TEST else 'ats_blockout' if BLOCKOUT else 'ats'
PI = math.pi
U = H_M / 334.0
BEV = 0.0 if BLOCKOUT else 0.02 / U            # chair call 5: bevel the box edges about 0.02 m (in units)
TEX = os.path.join(HERE, 'tex')

PAL = {'robot': A.ROW[18], 'neckcore': A.ROW[18], 'ink': A.ROW[22], 'neck': A.ROW[22], 'ball': A.ROW[13], 'decal': A.ROW[22], 'screen': A.ROW[22],
       'scan': A.ROW[12], 'hub': A.ROW[18], 'belt': A.ROW[22], 'paper': A.ROW[23]}
IMG = {'screen': 'screen.png', 'scan': 'scan.png', 'hub': 'hub.png', 'belt': 'belt.png', 'paper': 'cv.png'}
ALPHA = ['scan', 'hub', 'screen']
BASIC = ['ink', 'neck', 'decal', 'screen', 'scan', 'hub', 'belt', 'paper']
NEUTRAL = [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]]     # Kit's bands2 (neutral grey 178 shade band)

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
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*s2l(PAL[name]), 1); b.inputs['Roughness'].default_value = 0.8
    if name in IMG:
        im = bpy.data.images.load(os.path.join(TEX, IMG[name])); im.pack()
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = im; t.extension = 'REPEAT'; t.interpolation = 'Linear'
        nt.links.new(t.outputs['Color'], b.inputs['Base Color'])
        if name in ALPHA:
            gt = nt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.5
            nt.links.new(t.outputs['Alpha'], gt.inputs[0]); nt.links.new(gt.outputs[0], b.inputs['Alpha'])
    m['hex'] = PAL[name]; m['image'] = IMG.get(name, ''); MATS[name] = m; return m

def B(X, y, Z):
    """Sketch (X centred, y down, Z forward) -> Blender metres."""
    return Vector((X * U, -Z * U, (340.0 - y) * U))
def Bd(dX, dy, dZ):
    """A sketch direction -> a Blender direction (normalised)."""
    return Vector((dX, -dZ, -dy)).normalized()

# ================================================================ mesh accumulator: faces carry per-corner normal + uv
class Acc:
    def __init__(s): s.F = []                      # (corners [(pos, nrm, uv)], material, part)
    def f(s, corners, m, part): s.F.append(([(Vector(p), Vector(n).normalized(), tuple(uv)) for p, n, uv in corners], m, part))
ACC = {'body': Acc(), 'stamp': Acc(), 'screen': Acc(), 'cv': Acc()}

def make_mesh(name, acc):
    key = {}; V = []; faces = []; lnrm = []; luv = []; mats = []; parts = {}
    for corners, m, part in acc.F:
        ids = []
        for p, n, uv in corners:
            k = (round(p.x, 6), round(p.y, 6), round(p.z, 6))
            if k not in key: key[k] = len(V); V.append(p)
            ids.append(key[k])
        faces.append(ids); lnrm += [n for _, n, _ in corners]; luv += [uv for _, _, uv in corners]; mats.append(m)
        parts[part] = parts.get(part, 0) + len(corners) - 2
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in V], [], faces)
    names = [m for m in PAL if m in set(mats)]
    for m in names: me.materials.append(mat(m))
    me.polygons.foreach_set('material_index', [names.index(m) for m in mats])
    uvl = me.uv_layers.new(name='UVMap')
    for i, uv in enumerate(luv): uvl.data[i].uv = uv
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons)); me.update()
    me.normals_split_custom_set([tuple(n) for n in lnrm]); me.update()
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob); ob['tris_by_part'] = parts
    return ob

# ================================================================ geometry helpers
def simplify(pts, deg):
    """Keep the points where the outline turns: a new point after each `deg` of turning (corners get points, straight
    runs and gentle bows get few). pts: a closed outline."""
    n = len(pts); out = [0]; acc = 0.0
    def ang(i):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        a1 = math.atan2(b[1] - a[1], b[0] - a[0]); a2 = math.atan2(c[1] - b[1], c[0] - b[0])
        return abs((a2 - a1 + PI) % (2 * PI) - PI)
    for i in range(1, n):
        acc += ang(i)
        if acc >= math.radians(deg) * 0.999: out.append(i); acc = 0.0
    return [pts[i] for i in out]
def area2(P): return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2
def ccw(P):
    """Counter-clockwise in a (right, up) frame."""
    return P if area2(P) > 0 else P[::-1]
def offset2d(P, d):
    """Move a CCW (right, up) outline inward by d (a mitred offset)."""
    n = len(P); out = []
    for i in range(n):
        p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % n]
        def inn(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1; return (-dy / L, dx / L)
        n1, n2 = inn(p0, p1), inn(p1, p2); m = (n1[0] + n2[0], n1[1] + n2[1]); ml = math.hypot(*m) or 1; m = (m[0] / ml, m[1] / ml)
        ch = max(0.5, m[0] * n1[0] + m[1] * n1[1]); out.append((p1[0] + m[0] * d / ch, p1[1] + m[1] * d / ch))
    return out
def outnorm(P, i):
    """Outward 2D normal at vertex i of a CCW outline (smooth: the average of the two edge normals)."""
    n = len(P); p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % n]
    def on(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1; return (dy / L, -dx / L)
    a, b = on(p0, p1), on(p1, p2)
    if (a[0] * b[0] + a[1] * b[1]) < math.cos(math.radians(50)): return None      # a hard corner: split
    m = (a[0] + b[0], a[1] + b[1]); ml = math.hypot(*m) or 1; return (m[0] / ml, m[1] / ml)
def edgenorm(P, i):
    n = len(P); a, b = P[i], P[(i + 1) % n]; dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1; return (dy / L, -dx / L)

def prism(acc, part, P, to3, w0, w1, axis, m_side, m_cap, bev=0.0, caps=(True, True), uv_side=None):
    """Extrude a closed 2D outline P (CCW in its (r, s) frame) from w0 to w1 along `axis`.
    to3(r, s, w) -> Blender point; axis: Blender direction of +w. Sides are smooth along the outline (split at hard
    corners); with bev > 0 each cap edge gets a 45 deg chamfer of width bev (the cap is the outline inset by bev).
    uv_side(i, t) -> (u, v) for side faces (i: outline index, t: 0 at w0 .. 1 at w1)."""
    n = len(P); sm = [outnorm(P, i) for i in range(n)]
    def n3(nr): return (to3(nr[0], nr[1], 0) - to3(0, 0, 0)).normalized()
    ax = axis.normalized()
    Pin = offset2d(P, bev) if bev > 0 else P
    rings = []                      # (outline, w, kind)
    if bev > 0: rings = [(Pin, w0, 'cap'), (P, w0 + bev, 'side'), (P, w1 - bev, 'side'), (Pin, w1, 'cap')]
    else: rings = [(P, w0, 'side'), (P, w1, 'side')]
    def vn(i, j, k, kind):
        """The corner normal of side face (edge i -> i+1) at outline vertex j on ring k."""
        # chamfer faces are flat-shaded (their own face normal): a smooth chamfer normal interpolated along a long straight
        # run crosses the toon terminator part-way and draws a hard step in the edge band (head 3/4, first final render)
        # (only on long straight runs; round corners keep smooth chamfer normals so the band turns the corner cleanly)
        long_run = math.dist(P[i], P[(i + 1) % n]) > 15.0
        e = edgenorm(P, i) if (sm[j] is None or (kind != 'side' and long_run)) else sm[j]
        base = n3(e)
        if kind == 'chamfer0': return (base - ax).normalized()
        if kind == 'chamfer1': return (base + ax).normalized()
        return base
    for k in range(len(rings) - 1):
        (Pa, wa, _), (Pb, wb, _) = rings[k], rings[k + 1]
        kind = 'side' if bev == 0 or k == 1 else ('chamfer0' if k == 0 else 'chamfer1')
        msel = m_side
        for i in range(n):
            j = (i + 1) % n
            ta = (wa - w0) / (w1 - w0); tb = (wb - w0) / (w1 - w0)
            def uv(ii, t): return uv_side(ii, t) if uv_side else (0.5, 0.5)
            c = [(to3(*Pa[i], wa), vn(i, i, k, kind), uv(i, ta)), (to3(*Pa[j], wa), vn(i, j, k, kind), uv(i + 1, ta)),
                 (to3(*Pb[j], wb), vn(i, j, k + 1, kind), uv(i + 1, tb)), (to3(*Pb[i], wb), vn(i, i, k + 1, kind), uv(i, tb))]
            # wind so the face points outward
            fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0])
            if fn.dot(c[0][1]) < 0: c = c[::-1]
            acc.f(c, msel, part)
    if caps[0]:
        c = [(to3(*p, w0), -ax, (0.5, 0.5)) for p in rings[0][0]]
        fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0])
        acc.f(c if fn.dot(-ax) > 0 else c[::-1], m_cap, part)
    if caps[1]:
        c = [(to3(*p, w1), ax, (0.5, 0.5)) for p in rings[-1][0]]
        fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0])
        acc.f(c if fn.dot(ax) > 0 else c[::-1], m_cap, part)

def front_outline(d, deg):
    """A front-view path (x, y down) -> CCW outline in (X, up) = (x - 150, -y). The paths are mirror-symmetric about
    x 150 and start at the top centre: simplify the right half (top centre -> bottom centre) and mirror it, so the
    outline stays exactly symmetric."""
    P = [(x - 150.0, -y) for x, y in A.path_points(d, 24)]
    half = [P[0]]                                    # top centre, then the right side down to the bottom centre
    for i in range(1, len(P)):
        if P[i][0] < 0:
            a, b = P[i - 1], P[i]; t = a[0] / (a[0] - b[0]); half.append((0.0, a[1] + (b[1] - a[1]) * t)); break
        half.append(P[i])
    n = len(half); keep = [0]; acc = 0.0
    for i in range(1, n - 1):
        a, b, c = half[i - 1], half[i], half[i + 1]
        a1 = math.atan2(b[1] - a[1], b[0] - a[0]); a2 = math.atan2(c[1] - b[1], c[0] - b[0])
        acc += abs((a2 - a1 + PI) % (2 * PI) - PI)
        if acc >= math.radians(deg) * 0.999: keep.append(i); acc = 0.0
    keep.append(n - 1)
    R = [half[i] for i in keep]
    L = [(-x, y) for x, y in R[-2:0:-1]]
    return ccw(R + L)
def front_to3(X, ny, Z): return B(X, -ny, Z)

def cylinder(acc, part, c0, c1, r, n, m_side, m_cap, caps=(True, True), phase=0.0):
    """A cylinder between Blender points c0 and c1."""
    d = (c1 - c0).normalized(); a = Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))
    u = d.cross(a).normalized(); w = d.cross(u).normalized()
    R = [u * math.cos(2 * PI * k / n + phase) + w * math.sin(2 * PI * k / n + phase) for k in range(n)]
    for k in range(n):
        k1 = (k + 1) % n
        c = [(c0 + R[k] * r, R[k], (0, 0)), (c0 + R[k1] * r, R[k1], (0, 0)), (c1 + R[k1] * r, R[k1], (0, 0)), (c1 + R[k] * r, R[k], (0, 0))]
        fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0])
        acc.f(c if fn.dot(R[k]) > 0 else c[::-1], m_side, part)
    for cc, nn, on in ((c0, -d, caps[0]), (c1, d, caps[1])):
        if not on: continue
        c = [(cc + R[k] * r, nn, (0, 0)) for k in range(n)]
        fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0])
        acc.f(c if fn.dot(nn) > 0 else c[::-1], m_cap, part)

def sphere(acc, part, c, r, cols, lats, m):
    rings = []
    for la in lats:
        a = math.radians(la); rings.append([Vector((math.cos(a) * math.cos(2 * PI * j / cols), math.cos(a) * math.sin(2 * PI * j / cols), math.sin(a))) for j in range(cols)])
    top, bot = Vector((0, 0, 1)), Vector((0, 0, -1))
    for j in range(cols):
        j1 = (j + 1) % cols
        acc.f([(c + top * r, top, (0, 0)), (c + rings[0][j] * r, rings[0][j], (0, 0)), (c + rings[0][j1] * r, rings[0][j1], (0, 0))][::-1], m, part)
        for k in range(len(rings) - 1):
            A_, B_ = rings[k], rings[k + 1]
            acc.f([(c + A_[j] * r, A_[j], (0, 0)), (c + B_[j] * r, B_[j], (0, 0)), (c + B_[j1] * r, B_[j1], (0, 0)), (c + A_[j1] * r, A_[j1], (0, 0))], m, part)
        acc.f([(c + bot * r, bot, (0, 0)), (c + rings[-1][j1] * r, rings[-1][j1], (0, 0)), (c + rings[-1][j] * r, rings[-1][j], (0, 0))], m, part)

def quad(acc, part, pts, nrm, m, uvs=((0, 0), (1, 0), (1, 1), (0, 1))):
    c = [(p, nrm, uv) for p, uv in zip(pts, uvs)]
    fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0])
    acc.f(c if fn.dot(nrm) > 0 else c[::-1], m, part)
def front_poly(acc, part, P2, Z, m):
    """A flat front-facing decal polygon (front-view x, y) at depth Z (sketch units)."""
    nrm = Bd(0, 0, 1); c = [(B(x - 150, y, Z), nrm, (0.5, 0.5)) for x, y in P2]
    fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0]); acc.f(c if fn.dot(nrm) > 0 else c[::-1], m, part)
def line_quad(acc, part, x0, y0, x1, y1, w, Z, m, back=False):
    nrm = Bd(0, 0, -1 if back else 1); nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny); nx, ny = nx / L * w / 2, ny / L * w / 2
    quad(acc, part, [B(x0 + nx - 150, y0 + ny, Z), B(x1 + nx - 150, y1 + ny, Z), B(x1 - nx - 150, y1 - ny, Z), B(x0 - nx - 150, y0 - ny, Z)], nrm, m)

DEG = 30 if BLOCKOUT else 15.0           # outline sampling: a point per this much turning
SIDES = 8 if BLOCKOUT else 12            # rings, core, hub

# ================================================================ HEAD (bevelled monitor box), Z -34..34
body = ACC['body']
HEADP = front_outline(A.HEAD, 30 if BLOCKOUT else 18.0)
prism(body, 'head', HEADP, front_to3, -A.HEAD_Z, A.HEAD_Z, Bd(0, 0, 1), 'robot', 'robot', bev=BEV)
if not TEST:
    # back vents (decals on the head back)
    for v in A.HEAD_VENTS:
        (x0, y0), (x1, y1) = A.path_points(v, 1)[:2]
        line_quad(body, 'decals', x0, y0, x1, y1, 2.4, -A.HEAD_Z - 0.4, 'decal', back=True)

# ================================================================ BODY (bevelled mailbox arch), Z -50..50, lip, slot, hatch
if not TEST:
    BODYP = front_outline(A.BODY, DEG)
    prism(body, 'body', BODYP, front_to3, -A.BODY_Z, A.BODY_Z, Bd(0, 0, 1), 'robot', 'robot', bev=BEV)
    LIPP = ccw([(x - 150.0, -y) for x, y in A.path_points(A.LIP, 1)])
    prism(body, 'lip', LIPP, front_to3, A.BODY_Z - 6, A.BODY_Z + 12, Bd(0, 0, 1), 'robot', 'robot', caps=(False, True))
    # the lip's front edge in ink (sketch: the tray is drawn with an ink outline; the hull draws only the silhouette)
    for (a, b) in (((97, 262), (203, 262)), ((102, 254), (97, 262)), ((198, 254), (203, 262))):
        line_quad(body, 'decals', a[0], a[1], b[0], b[1], 1.6, A.BODY_Z + 12 + 0.4, 'decal')
    SLOTP = [(x, y) for x, y in simplify([(x, y) for x, y in A.path_points(A.SLOT, 6)], 45)]
    front_poly(body, 'decals', SLOTP, A.BODY_Z + 0.5, 'decal')
    # back hatch outline (decal lines on the body back)
    hx0, hx1, hy0, hy1 = 110, 190, 236, 284
    for (a, b) in (((hx0, hy0), (hx1, hy0)), ((hx1, hy0), (hx1, hy1)), ((hx1, hy1), (hx0, hy1)), ((hx0, hy1), (hx0, hy0))):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); ex, ey = dx / L * 0.9, dy / L * 0.9
        line_quad(body, 'decals', a[0] - ex, a[1] - ey, b[0] + ex, b[1] + ey, 1.8, -A.BODY_Z - 0.4, 'decal', back=True)

# ================================================================ NECK: grey core (open, sunk into head and body) + 3 ink rings
if not TEST:
    (yb, rc), (yt, _) = A.NECK_CORE
    cylinder(body, 'neck_core', B(0, yb, 0), B(0, yt, 0), rc * U, SIDES, 'neckcore', 'neckcore', caps=(False, False), phase=PI / SIDES)
    for k, ((y0, r0), (y1, r1)) in enumerate(A.NECK_RINGS):
        cylinder(body, 'neck_rings', B(0, y0, 0), B(0, y1, 0), r0 * U, SIDES, 'neck', 'neck', phase=PI / SIDES)

# ================================================================ TREADS: stadium belts (ink, scrolling cleats) + hub decals
TR = 18.0; ZB, ZF, YC = -40.0, 56.0, 322.0          # back and front nose centres (sketch tread pieces), axle line
SEG = 4 if BLOCKOUT else 6                           # segments per nose half-circle
def stadium():
    P = []                                           # (Z, up) CCW: bottom run, front nose, top run, back nose
    for k in range(SEG + 1):
        a = -PI / 2 + PI * k / SEG; P.append((ZF + TR * math.cos(a), -YC + TR * math.sin(a)))
    for k in range(SEG + 1):
        a = PI / 2 + PI * k / SEG; P.append((ZB + TR * math.cos(a), -YC + TR * math.sin(a)))
    return P
TP = ccw(stadium())
LOOP = [0.0]
for i in range(len(TP)): LOOP.append(LOOP[-1] + math.dist(TP[i], TP[(i + 1) % len(TP)]))
CLEAT = 12.0                                         # cleat pitch (units along the belt)
for s in ((1, -1) if not TEST else (1,)):
    x0, x1 = A.TREAD_X
    X0, X1 = (x0 - 150, x1 - 150) if s > 0 else (-(x1 - 150), -(x0 - 150))
    to3 = lambda zz, up, X: B(X, -up, zz)
    prism(body, 'treads', TP, to3, X0, X1, Vector((1, 0, 0)), 'belt', 'ink',
          uv_side=lambda i, t: (LOOP[i] / CLEAT, t))
    # hub discs on the outer face: octagons enclosing the r 10 disc; each maps the full hub texture
    Xo = (X1 if s > 0 else X0) + s * 0.4; nrm = Vector((s, 0, 0)); rr = 10.0 / math.cos(PI / 8)
    for hz, hy in A.HUBS:
        pts = []; uvs = []
        for k in range(8):
            a = 2 * PI * (k + 0.5) / 8; pts.append(B(Xo, hy - rr * math.sin(a), hz + rr * math.cos(a)))
            uvs.append((0.5 + 0.5 * rr / 10 * math.cos(a) * s, 0.5 + 0.5 * rr / 10 * math.sin(a)))
        c = [(p, nrm, uv) for p, uv in zip(pts, uvs)]
        fn = (c[1][0] - c[0][0]).cross(c[2][0] - c[0][0]); body.f(c if fn.dot(nrm) > 0 else c[::-1], 'hub', 'hubs')

# ================================================================ SHOULDER HUB (robot's LEFT = +X), antenna
if not TEST:
    hx0, hx1 = A.HUB_X; pv = A.LM['pivot']
    cylinder(body, 'shoulder_hub', B(hx0 - 150 + 4, pv, 0), B(hx1 - 150, pv, 0), 15 * U, SIDES, 'robot', 'robot', caps=(False, True), phase=PI / SIDES)
    dot = []
    for k in range(6):
        a = 2 * PI * k / 6; dot.append(B(hx1 - 150 + 0.4, pv - 5 * math.sin(a), 5 * math.cos(a)))
    body.f([(p, Vector((1, 0, 0)), (0.5, 0.5)) for p in dot][::-1] if ((dot[1] - dot[0]).cross(dot[2] - dot[0])).x < 0 else
           [(p, Vector((1, 0, 0)), (0.5, 0.5)) for p in dot], 'decal', 'decals')
    # the hub's ink rim on its outer face (sketch: the hub disc has an ink stroke), so the hub reads on the grey body
    for k in range(SIDES):
        a0, a1 = 2 * PI * k / SIDES + PI / SIDES, 2 * PI * (k + 1) / SIDES + PI / SIDES
        rim = [B(hx1 - 150 + 0.4, pv - r * math.sin(a), r * math.cos(a)) for r, a in ((15.0, a0), (15.0, a1), (12.6, a1), (12.6, a0))]
        quad(body, 'decals', rim, Vector((1, 0, 0)), 'decal')
    bx, by, bz = A.ANT_BASE; tx, ty, tz = A.ANT_TIP
    cylinder(body, 'antenna', B(bx - 150, by + 6, bz), B(bx - 150, by - 4, bz), 7 * U, 8, 'robot', 'robot', caps=(False, True))
    cylinder(body, 'antenna', B(bx - 150, by - 3, bz), B(tx - 150, ty + 4, tz), 2.6 * U, 6, 'ink', 'ink', caps=(False, False))
    BALL_C = B(tx - 150, ty - A.ANT_BALL_R * 0.6, tz)
    sphere(body, 'antenna', BALL_C, A.ANT_BALL_R * U, 8, [45, 0, -45] if not BLOCKOUT else [30, -30], 'ball')

# ================================================================ STAMP ARM (one rigid mesh, built at theta 0 = hanging straight down)
stamp = ACC['stamp']
if not TEST:
    zy = lambda z, up, x: B(x - 150, -up, z)
    BARP = ccw(simplify([(z, -y) for z, y in A.path_points(A.ARM_BAR, 24)], 45))
    prism(stamp, 'bar', BARP, zy, A.ARM_X[0], A.ARM_X[1], Vector((1, 0, 0)), 'robot', 'robot')
    BLKP = ccw(simplify([(z, -y) for z, y in A.path_points(A.STAMP_BLOCK, 24)], 45))
    prism(stamp, 'block', BLKP, zy, A.BLOCK_X[0], A.BLOCK_X[1], Vector((1, 0, 0)), 'robot', 'robot')   # its profile corners are already round (r 3)
    # the rubber: the sketch pad (y 330-338), as wide as the block so no block bevel corner peeks out beside it
    RUBP = ccw([(-24.5, -329.5), (24.5, -329.5), (24.5, -338.0), (-24.5, -338.0)])     # inside the block's round corners
    prism(stamp, 'rubber', RUBP, zy, A.BLOCK_X[0] + 0.3, A.BLOCK_X[1] - 0.3, Vector((1, 0, 0)), 'ink', 'ink', caps=(True, True))

# ================================================================ SCREEN (2 quads on the head front): eyes atlas + scan line
scr = ACC['screen']
SX0, SX1, SY0, SY1 = 80, 220, 74, 136
nz = Bd(0, 0, 1)
ZS = A.HEAD_Z + 0.6
quad(scr, 'screen', [B(SX0 - 150, SY1, ZS), B(SX1 - 150, SY1, ZS), B(SX1 - 150, SY0, ZS), B(SX0 - 150, SY0, ZS)], nz, 'screen',
     uvs=((0, 0.8), (1, 0.8), (1, 1.0), (0, 1.0)))           # the idle cell (top fifth of the atlas, Blender v up)
quad(scr, 'scan', [B(SX0 - 150, SY1, ZS + 0.2), B(SX1 - 150, SY1, ZS + 0.2), B(SX1 - 150, SY0, ZS + 0.2), B(SX0 - 150, SY0, ZS + 0.2)], nz, 'scan',
     uvs=((0, 0), (1, 0), (1, 1), (0, 1)))

# ================================================================ CV prop (built at "out": half in the slot is the game's move)
cvacc = ACC['cv']
CVX0, CVX1, CVY0, CVY1 = 118, 182, 245, 248
CV_L = 76.0
if not TEST:
    z0, z1 = A.BODY_Z - 4, A.BODY_Z + CV_L                   # the back end starts just inside the slot
    top = [B(CVX0 - 150, CVY0, z1), B(CVX1 - 150, CVY0, z1), B(CVX1 - 150, CVY0, z0), B(CVX0 - 150, CVY0, z0)]
    quad(cvacc, 'cv', top, Vector((0, 0, 1)), 'paper', uvs=((0, 0), (0.5, 0), (0.5, 1), (0, 1)))   # text reads from the front
    bot = [B(CVX0 - 150, CVY1, z0), B(CVX1 - 150, CVY1, z0), B(CVX1 - 150, CVY1, z1), B(CVX0 - 150, CVY1, z1)]
    quad(cvacc, 'cv', bot, Vector((0, 0, -1)), 'paper', uvs=((0.02, 0.02),) * 4)
    for (pa, pb, nn) in (((CVX0, z1), (CVX1, z1), Vector((0, -1, 0))), ((CVX1, z1), (CVX1, z0), Vector((1, 0, 0))), ((CVX0, z0), (CVX0, z1), Vector((-1, 0, 0)))):
        quad(cvacc, 'cv', [B(pa[0] - 150, CVY0, pa[1]), B(pb[0] - 150, CVY0, pb[1]), B(pb[0] - 150, CVY1, pb[1]), B(pa[0] - 150, CVY1, pa[1])], nn, 'paper', uvs=((0.02, 0.02),) * 4)

# ================================================================ objects, nodes
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root
bnc = bpy.data.objects.new('bounce', None); COL.objects.link(bnc); bnc.parent = flt
OB = {}
for nm in ('body', 'screen'):
    OB[nm] = make_mesh(nm, ACC[nm]); OB[nm].parent = bnc
PIVOT = B(0, A.LM['pivot'], 0)
if ACC['stamp'].F:
    piv = bpy.data.objects.new('stamp_pivot', None); COL.objects.link(piv); piv.parent = bnc; piv.location = PIVOT
    for i, (corners, m, part) in enumerate(ACC['stamp'].F):
        ACC['stamp'].F[i] = ([(p - PIVOT, n, uv) for p, n, uv in corners], m, part)
    OB['stamp'] = make_mesh('stamp', ACC['stamp']); OB['stamp'].parent = piv
    piv.rotation_mode = 'XYZ'
    def set_theta(deg): piv.rotation_euler = (-math.radians(deg), 0, 0)      # + swings the lower end forward (-Y)
    set_theta(A.REST_DEG)
if ACC['cv'].F:
    OB['cv'] = make_mesh('cv', ACC['cv']); OB['cv'].parent = root
    OB['cv']['prop'] = True; OB['cv']['default_visible'] = False

# motion data (Blender axes; the game reads them from the float node's extras)
flt['height_m'] = H_M; flt['unit_m'] = U
flt['stamp'] = {'node': 'stamp_pivot', 'axis_blender': [1, 0, 0], 'sign': -1, 'rest_deg': A.REST_DEG, 'windup_deg': A.WIND_DEG,
                'slam_deg': A.SLAM_DEG, 'note': 'rotation.x = sign * radians(theta); + swings the stamp forward; one hinge at the hub axis'}
flt['screen'] = {'states': ['idle', 'reading', 'found', 'notfit', 'loading'], 'cell_v': 0.2,
                 'three_offset_y': {s: round(0.2 * k, 3) for k, s in enumerate(['idle', 'reading', 'found', 'notfit', 'loading'])},
                 'scan_three_offset_y': {'rest': 0.0, 'sweep_top': round((126 - 74) / 62 - (80 - 74) / 62, 4),
                                         'sweep_bottom': round((126 - 74) / 62 - (130 - 74) / 62, 4)},
                 'scan_visible_in': ['idle', 'reading'], 'never_angry': True}
flt['treads'] = {'belt_material': 'belt', 'cleat_pitch_m': CLEAT * U, 'u_per_m': 1 / (CLEAT * U), 'hub_material': 'hub',
                 'hub_radius_m': 10 * U, 'note': 'belt: map.offset.x += distance / cleat_pitch; hub: map.center (0.5, 0.5), map.rotation = -distance / hub_radius'}
flt['antenna'] = {'material': 'ball', 'on': A.ROW[13], 'off_mult': 0.62}
flt['cv'] = {'node': 'cv', 'slide_axis_blender': [0, 1, 0], 'travel_m': (CV_L + 4) * U, 'stamped_uv_offset_x': 0.5,
             'note': 'starts out on the lip (Z 46..126); slides back into the slot by travel_m, then hides; the stamped cell is u + 0.5'}

# ================================================================ report + export
def tris(ob): ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)
counts = {k: tris(o) for k, o in OB.items()}
counts['visible_robot (body + stamp + screen)'] = sum(counts.get(k, 0) for k in ('body', 'stamp', 'screen'))
parts = {k: dict(o['tris_by_part']) for k, o in OB.items()}
report = {'triangles': counts, 'by_part': parts, 'meshes': {'non_swap (<= 3)': [k for k in ('body', 'stamp', 'screen') if k in OB],
          'prop': ['cv'] if 'cv' in OB else []}, 'height_m': H_M, 'unit_mm': round(U * 1000, 3), 'bevel_m': round(BEV * U, 4),
          'outline_points': {'head': len(HEADP), 'body': len(BODYP) if not TEST else None, 'tread': len(TP)},
          'materials': {k: [m.name for m in o.data.materials] for k, o in OB.items()}}
print('ATS_REPORT', json.dumps(counts))
json.dump(report, open(os.path.join(OUT, NAME + '_build_report.json'), 'w'), indent=1)
json.dump({'band_colors': {k: NEUTRAL for k in PAL if k not in BASIC}, 'basic_materials': BASIC, 'alpha_materials': ALPHA,
           'outline_nodes': ['body', 'stamp'], 'no_outline_materials': ['decal', 'hub'],
           'contact_shadow': {'rx': 0.36, 'ry': 0.30, 'opacity': 0.25}}, open(os.path.join(OUT, 'ats_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, bnc] + list(OB.values()) + ([bpy.data.objects['stamp_pivot']] if 'stamp' in OB else []): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, NAME + '.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT',
                          export_normals=True, export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + '.blend'))
print('ATS_DONE')
