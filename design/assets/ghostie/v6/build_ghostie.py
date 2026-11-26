# GHOSTED - the Ghostie (ghost recruiter NPC), v6: the final model, built to the accepted sketch v2.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_ghostie.py [-- body_only]
# Brief: design/acceptance/ghostie/build-brief-v6.md. Direction and join decisions: direction.md.
# Shapes: every outline comes from the sketch's hand-drawn Bezier paths (../sketch/src/ghost.py), read here, not retyped.
# Units: metres. Blender is Z-up and the ghost faces -Y; the glTF export is Y-up (the ghost faces +Z in three.js).
# Sketch front-view units: x right (viewer-right = arm_L = +X), y down. 1 unit = 0.47 / 265 m (v5 size kept).
# Nodes: root > float > rig (body_root, arm_L, arm_R) > body (skinned, the only non-swap mesh);
#        float > eyes, acc_tie, acc_glasses, acc_headset (swap parts).
import bpy, bmesh, math, json, os, sys, re
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sketch', 'src'))
import ghost as G   # the sketch source: FRONT_BODY, S_BODY, LM, EYES, tie_paths, collar_paths
BODY_ONLY = '--' in sys.argv and 'body_only' in sys.argv[sys.argv.index('--'):]
PI = math.pi

PAL = {'ghost': '#F8F4EA', 'acc': '#C8C0D8', 'tie': '#C9A6D6', 'ink': '#2B1E16'}   # Lena rows 16, 27, 10, 22
GHOST_TOON = {
    'band_colors': {k: [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]] for k in ('ghost', 'acc', 'tie')},
    'basic_materials': ['ink'],
    'outline_nodes': ['body', 'acc_headset'],   # v6: the headset carries its own hull (no ink-ring geometry)
    'float_rest_m': None, 'variants': ['tie', 'glasses', 'headset'],
    'contact_shadow': {'rx': 0.20, 'ry': 0.17, 'opacity_at_rest': 0.22},
}
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
def mesh_obj(name, verts, faces, mats, fmat=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
    for m in mats: me.materials.append(mat(m))
    if fmat: me.polygons.foreach_set('material_index', fmat)
    me.polygons.foreach_set('use_smooth', [smooth] * len(me.polygons))
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob); return ob
def tris(ob):
    ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)

# ================================================================ sketch curves
U = 0.47 / 265.0
Y_LOBE = 316.0                       # lowest hem lobe (front-view y); z = 0 there
def zf(y): return (Y_LOBE - y) * U
def xf(x): return (x - 150.0) * U

def parse(d):
    """Cubic segments of an M/C/L/Z path, as lists of 4 (x, y) points."""
    toks = re.findall(r'[MCLZ]|-?\d+(?:\.\d+)?', d); segs = []; i = 0; cur = None; cmd = None
    while i < len(toks):
        t = toks[i]
        if t in 'MCLZ': cmd = t; i += 1; continue
        if cmd == 'M': cur = (float(t), float(toks[i + 1])); i += 2
        elif cmd == 'C':
            p = [(float(toks[i + k]), float(toks[i + k + 1])) for k in (0, 2, 4)]; segs.append([cur] + p); cur = p[2]; i += 6
        elif cmd == 'L':
            p = (float(t), float(toks[i + 1])); segs.append([cur, cur, p, p]); cur = p; i += 2
    return segs
def bez(s, t):
    a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
    return (a * s[0][0] + b * s[1][0] + c * s[2][0] + d * s[3][0], a * s[0][1] + b * s[1][1] + c * s[2][1] + d * s[3][1])
def poly(segs, n=60):
    out = [segs[0][0]]
    for s in segs: out += [bez(s, k / n) for k in range(1, n + 1)]
    return out
def x_at_y(pts, y):
    """x on a polyline that is monotonic in y."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if min(y0, y1) <= y <= max(y0, y1) and y1 != y0: return x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    raise ValueError(y)
def arc(pts):
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    return L
def at_len(pts, L, s):
    for i in range(len(L) - 1):
        if L[i] <= s <= L[i + 1]:
            f = (s - L[i]) / max(L[i + 1] - L[i], 1e-9); return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
    return pts[-1]

FS = parse(G.FRONT_BODY); SS = parse(G.S_BODY)
DOME_F = poly([FS[0]], 400)                    # (150,36) -> (244,134)
SHOULDER_F = poly([FS[1]], 200)                # (244,134) -> (252,190)
ARM_F = poly(FS[2:5], 200)                     # (252,190) -> tip -> (254,260)
BELOW_F = poly([FS[5]], 100)                   # (254,260) -> (262,292)
SIDE_D = poly(SS[0:2], 400)                    # (150,36) -> (232,140) -> (240,294): half-depth
def W(y):
    if y <= 134: return x_at_y(DOME_F, y) - 150
    if y <= 190: return x_at_y(SHOULDER_F, y) - 150
    if y <= 260: return 102.0 + 2.0 * (y - 190) / 70     # the body side under the arm (camera.py: "straight under the arm")
    return x_at_y(BELOW_F, min(y, 292)) - 150
def D(y): return x_at_y(SIDE_D, min(max(y, 36.0001), 294)) - 150
N_SE = 2.2                                     # cross-section superellipse exponent (2 = ellipse; a little fuller sheet)
def se(th, w, d):
    s, c = math.sin(th), math.cos(th); p = 2.0 / N_SE
    return (math.copysign(abs(s) ** p, s) * w, -math.copysign(abs(c) ** p, c) * d)   # (x, y_blender); th 0 = front (-Y)

# ================================================================ BODY: ring lattice (direction.md section 3)
# Dome rows at equal arc length on the sketch's front dome curve, so the front outline gets even vertex spacing.
LD = arc(DOME_F); N_DOME = 8
# v6 test 2: rows at equal TURNING angle of the front outline (each outline vertex turns by 90/8 deg), not equal arc
def heading(p, q): return math.atan2(q[1] - p[1], q[0] - p[0])
TURN = [0.0]
for a_, b_, c_ in zip(DOME_F, DOME_F[1:], DOME_F[2:]): TURN.append(TURN[-1] + abs(heading(b_, c_) - heading(a_, b_)))
TURN.append(TURN[-1])
dome_rows = []
for k in range(1, N_DOME + 1):
    tgt = TURN[-1] * (k - 0.5) / N_DOME if k < N_DOME else None
    if tgt is None: dome_rows.append(DOME_F[-1][1]); continue
    i_ = next(i for i, t in enumerate(TURN) if t >= tgt); dome_rows.append(DOME_F[i_][1])
ROWS = dome_rows + [180.0, 190.0, 260.0]
COLS16 = [j * 2 * PI / 16 for j in range(16)]
COLS8 = [j * 2 * PI / 8 for j in range(8)]
V = []; F = []; vid = {}
def addv(p, key=None):
    V.append(Vector(p)); i = len(V) - 1
    if key is not None: vid[key] = i
    return i
pole = addv((0, 0, zf(36)), 'pole')
ring_ids = []
for r, y in enumerate(ROWS):
    cols = COLS8 if r < 2 else COLS16
    ids = []
    for j, th in enumerate(cols):
        x, yb = se(th, W(y) * U, D(y) * U); ids.append(addv((x, yb, zf(y)), ('r', r, j)))
    ring_ids.append(ids)
def quad(a, b, c, d): F.append([a, b, c, d])
n0 = len(ring_ids[0])
for j in range(n0): F.append([pole, ring_ids[0][(j + 1) % n0], ring_ids[0][j]])
for r in range(len(ROWS) - 1):
    A, B = ring_ids[r], ring_ids[r + 1]
    if len(A) == len(B):
        for j in range(len(A)):
            # skip the 2x2 arm patches (rows 190-225-260, columns 3..4 and 12..13 of 16 = 67.5..112.5 deg each side)
            if ROWS[r] == 190.0 and (j in (3, 4) or j in (11, 12)): continue   # the arm openings (2 faces wide, 1 tall)
            j1 = (j + 1) % len(A); quad(A[j], A[j1], B[j1], B[j])
    else:   # 8 -> 16
        for j in range(len(A)):
            j1 = (j + 1) % len(A); a, b = A[j], A[j1]; Bl, Bm, Br = B[2 * j], B[2 * j + 1], B[(2 * j + 2) % len(B)]
            F.append([a, Bl, Bm]); F.append([a, Bm, b]); F.append([b, Bm, Br])
# Hem: 5 lobes, notches at +-26, +-126 and 180 deg (3 lobes seen from the front, a notch centred at the back).
NOTCH = [-180, -150, -26, 26, 150, 180]   # back notches at +-150: the sketch BACK view (x 94/206), off the side silhouette
LOBE_N = {(-180, -150): 4, (-150, -26): 13, (-26, 26): 6, (26, 150): 13, (150, 180): 4}   # about every 9 deg
A_LOBE = 15.0                                   # notch y 301, lobe bottom y 316 (sketch)
W_HEM, D_HEM = 112.0, 90.0                      # front x 262 (FRONT_BODY), side x 240 (S_BODY)
hem = []; hem_th = []
for a, b in zip(NOTCH, NOTCH[1:]):
    n = LOBE_N[(a, b)]
    for k in range(n):
        u = k / n; th = math.radians(a + (b - a) * u)
        amp = A_LOBE * min(1.0, ((b - a) / 52.0) ** 0.6)              # narrow back lobes are shallower, so they stay round
        # the side lobes hang lowest at about 63 deg (sketch FRONT: lobe bottom near x 240), so at the side silhouette
        # (90 deg) the hem already curls up: a round bottom corner, not a square one
        u0 = 0.5
        if (a, b) == (26, 150): u0 = 0.30
        if (a, b) == (-150, -26): u0 = 0.70
        uw = 0.5 * u / u0 if u <= u0 else 0.5 + 0.5 * (u - u0) / (1 - u0)
        y = 301.0 + amp * ((1 - math.cos(2 * PI * uw)) / 2) ** 0.65   # a soft V at the notch, a round lobe bottom
        bulge = 1.0 + 0.02 * math.sin(PI * u)                 # the lobe bellies out a little (sketch C266,310)
        x, yb = se(th, W_HEM * U * bulge, D_HEM * U * bulge); hem.append(addv((x, yb, zf(y)))); hem_th.append(th)
# stitch row 260 (16 columns at th_j) to the hem ring (sorted by angle, starting at -180 = the back)
last = ring_ids[-1]
def ang(th): return (th + PI) % (2 * PI) - PI
cols_sorted = sorted(range(16), key=lambda j: ang(COLS16[j]))
top = [(ang(COLS16[j]), last[j]) for j in cols_sorted]
bot = [(ang(t), h) for t, h in zip(hem_th, hem)]
i = k = 0; nt, nb = len(top), len(bot)
while i < nt or k < nb:   # merge two closed angle-sorted rings into a triangle strip
    ti, tn = top[i % nt], top[(i + 1) % nt]; bk, bn = bot[k % nb], bot[(k + 1) % nb]
    a_t = tn[0] + (2 * PI if i + 1 >= nt else 0); a_b = bn[0] + (2 * PI if k + 1 >= nb else 0)
    if k < nb and (i >= nt or a_b <= a_t): F.append([ti[1], bn[1], bk[1]]); k += 1
    else: F.append([ti[1], tn[1], bk[1]]); i += 1

# ---------------------------------------------------------------- ARMS: tubes on the opened patches (continuous skin)
# Bone pivots (front units). arm_L waves: its pivot sits up and in from the shoulder, so the arm top lifts and swings out
# and the tip lands where the sheet WAVE puts it (about x 298, y 184). arm_R only droops in the rest pose: its pivot is
# the bottom of the arm root, so the drop stretches the shoulder and never folds the underside into the body.
PIV_F = {'arm_L': (215.0, 185.0), 'arm_R': (253.0, 258.0)}
LA = arc(ARM_F)
tip_i = max(range(len(ARM_F)), key=lambda i: math.dist(ARM_F[i], (250.0, 225.0))); TIP_F = ARM_F[tip_i]   # the tip: farthest from the root centre
TOP_P = ARM_F[:tip_i + 1]; BOT_P = ARM_F[tip_i:][::-1]
LT, LB = arc(TOP_P), arc(BOT_P)
ARM_RINGS = [(0.24, 31.0), (0.55, 27.0), (0.84, 19.0)]      # (fraction along the outline to the tip, half-depth units)
def ring_pts(f, hd, sx):
    T = at_len(TOP_P, LT, LT[-1] * f); B = at_len(BOT_P, LB, LB[-1] * f)
    if f < 0.3: B = (B[0] + 1.2, B[1] + 1.6)   # the first underside vertex sits a touch out on the corner, so the 90 deg
                                               # turn from the underside into the body side splits over 2 vertices
    C = ((T[0] + B[0]) / 2, (T[1] + B[1]) / 2); hh = math.dist(T, B) / 2
    ax = ((T[0] - B[0]) / (2 * hh), (T[1] - B[1]) / (2 * hh))          # unit, front-view coords (y down)
    out = []
    for k in range(6):                                                 # 0 top, 1 top-front, 2 bottom-front, 3 bottom, 4 bottom-back, 5 top-back
        ph = k * PI / 3; c, s = math.cos(ph), math.sin(ph); p = 2.0 / N_SE
        cu = math.copysign(abs(c) ** p, c) * hh; sv = math.copysign(abs(s) ** p, s) * hd
        x = C[0] + ax[0] * cu; y = C[1] + ax[1] * cu
        out.append(Vector((sx * xf(x), -sv * U, zf(y))))               # front = -Y
    return out
arm_info = {}
for sx, nm in ((1, 'arm_L'), (-1, 'arm_R')):
    jc = 4 if sx > 0 else 12; jf = 3 if sx > 0 else 13; jb = 5 if sx > 0 else 11   # column at the side, its front, its back
    r190, r260 = ROWS.index(190.0), ROWS.index(260.0)
    R = ring_ids
    loop = [R[r190][jc], R[r190][jf], R[r260][jf], R[r260][jc], R[r260][jb], R[r190][jb]]
    rings = [loop]; ring_w = [[0.42, 0.38, 0.15, 0.12, 0.15, 0.38]]   # opening: the shoulder side follows a little, the underside less
    for f, hd in ARM_RINGS:
        rings.append([addv(p) for p in ring_pts(f, hd, sx)]); ring_w.append([{0.24: 0.85, 0.55: 1.0, 0.84: 1.0}[f]] * 6)
    tip = addv((sx * xf(TIP_F[0]), 0.0, zf(TIP_F[1])))
    for a_, b_ in zip(rings, rings[1:]):
        for k in range(6):
            k1 = (k + 1) % 6; q = [a_[k], a_[k1], b_[k1], b_[k]]; F.append(q if sx > 0 else q[::-1])
    for k in range(6):
        k1 = (k + 1) % 6; t = [rings[-1][k], rings[-1][k1], tip]; F.append(t if sx > 0 else t[::-1])
    arm_info[nm] = {'rings': rings, 'w': ring_w, 'tip': tip, 'piv': Vector((sx * xf(PIV_F[nm][0]), 0.0, zf(PIV_F[nm][1])))}
# hidden cavity: one fan from the hem to a pole inside. It turns the hem vertex normals down, so the ink hull closes
# under the hem (the open-hem test had no ink line at the bottom: tests/body1/sheet.png).
cav = addv((0.0, 0.0, 0.16))
for k in range(len(hem)): F.append([hem[k], hem[(k + 1) % len(hem)], cav])
HEM_IDS = list(hem)
# drop unused vertices (none expected)
used = set(i for f in F for i in f)
remap = {}; NV = []
for i, v in enumerate(V):
    if i in used: remap[i] = len(NV); NV.append(v)
F = [[remap[i] for i in f] for f in F]
body = mesh_obj('body', NV, F, ['ghost'])
hem_set = set(remap[i] for i in HEM_IDS)
bm = bmesh.new(); bm.from_mesh(body.data)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4], quad_method='BEAUTY')
bm.to_mesh(body.data); bm.free(); body.data.update()
body.data.polygons.foreach_set('use_smooth', [True] * len(body.data.polygons))
for e in body.data.edges:                       # a hard hem lip: the outer skin keeps its own normals (v4/v5 method)
    if e.vertices[0] in hem_set and e.vertices[1] in hem_set: e.use_edge_sharp = True
for nm in arm_info:
    ai = arm_info[nm]; ai['rings'] = [[remap[i] for i in r] for r in ai['rings']]; ai['tip'] = remap[ai['tip']]
# orientation check (recipe.mesh-orientability-check): normals point away from the body axis on average
bm = bmesh.new(); bm.from_mesh(body.data); bm.normal_update()
inward = sum(1 for f in bm.faces if f.normal.dot(f.calc_center_median() - Vector((0, 0, f.calc_center_median().z))) < 0)
boundary = sum(1 for e in bm.edges if e.is_boundary); nonman = sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary)
bm.free()
# ---------------------------------------------------------------- shading normals (0 triangles)
# The toon band shows every normal step. So the body's shading normals come from a dense smooth proxy of the same body
# (the same W(y), D(y) and superellipse, 96 columns, no arms): the dome terminator is smooth, and the arm root takes the
# body-side normal, so the root reads as one flat body tone (paint-over mark 2). The mix fades out along the arm, so the
# arm tip keeps its own round normals. The ink hull does not use these normals (it is built from the geometry).
pv, pf = [], []
PY = [36.0 + (292.0 - 36.0) * (k / 140) ** 1.0 for k in range(1, 141)]
pv.append((0, 0, zf(36)))
for y in PY:
    for j in range(96):
        x, yb = se(2 * PI * j / 96, W(y) * U, D(y) * U); pv.append((x, yb, zf(y)))
for j in range(96): pf.append([0, 1 + (j + 1) % 96, 1 + j])
for r in range(len(PY) - 1):
    for j in range(96):
        a = 1 + r * 96; b = a + 96; j1 = (j + 1) % 96; pf.append([a + j, a + j1, b + j1, b + j])
proxy = mesh_obj('normal_proxy', pv, pf, ['ghost'])
bmp = bmesh.new(); bmp.from_mesh(proxy.data); bmesh.ops.recalc_face_normals(bmp, faces=bmp.faces); bmp.to_mesh(proxy.data); bmp.free()
proxy.data.polygons.foreach_set('use_smooth', [True] * len(proxy.data.polygons))
mixg = body.vertex_groups.new(name='normal_mix')
arm_mix = {}
for nm, ai in arm_info.items():
    for r, m_ in zip(ai['rings'], (1.0, 0.75, 0.3, 0.0)):
        for i in r: arm_mix[i] = m_
    arm_mix[ai['tip']] = 0.0
cav_i = remap[cav]
for v in body.data.vertices:
    if v.index == cav_i: continue
    mixg.add([v.index], arm_mix.get(v.index, 1.0), 'REPLACE')
dt = body.modifiers.new('normals', 'DATA_TRANSFER'); dt.object = proxy; dt.use_loop_data = True
dt.data_types_loops = {'CUSTOM_NORMAL'}; dt.loop_mapping = 'POLYINTERP_NEAREST'; dt.vertex_group = 'normal_mix'
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='normals')
body.vertex_groups.remove(body.vertex_groups['normal_mix'])
bpy.data.objects.remove(proxy)
body_bm = bmesh.new(); body_bm.from_mesh(body.data); body_bm.normal_update()
TREE = BVHTree.FromBMesh(body_bm)
checks = {'body_inward_faces (arm faces may lean)': inward, 'body_boundary_edges (the open hem only)': boundary, 'body_nonmanifold_edges': nonman,
          'dome_rows_y': [round(y, 1) for y in dome_rows], 'arm_tip_front_units': [round(c, 1) for c in TIP_F]}

def sdist(p):
    loc, nrm, _, d = TREE.find_nearest(p); return d if (p - loc).dot(nrm) >= 0 else -d
def front_hit(x_u, y_u, off):
    """The body point seen from the front at sketch (x, y), pushed off along the surface normal."""
    loc, nrm, _, _ = TREE.ray_cast(Vector((xf(x_u), -1.0, zf(y_u))), Vector((0, 1, 0)))
    return loc + nrm * off, nrm

# ================================================================ EYES: the sketch ovals (rx 8.5, ry 13) on the eye line y 118
EYE_N = 12; ev = []; ef = []
for (ex, ey) in G.EYES:
    c, _ = front_hit(ex, ey, 0.0021); ci = len(ev); ev.append(c)
    rim = []
    for k in range(EYE_N):
        a = 2 * PI * k / EYE_N; p, _ = front_hit(ex + 8.5 * math.cos(a), ey - 13.0 * math.sin(a), 0.0012); rim.append(len(ev)); ev.append(p)
    for k in range(EYE_N): ef.append([ci, rim[(k + 1) % EYE_N], rim[k]])
eyes = mesh_obj('eyes', ev, ef, ['ink'], smooth=False)

def orient_out(ob):
    """Face every polygon away from the body (a surface decal must face out)."""
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.normal_update()
    for f in bm.faces:
        c = f.calc_center_median(); loc, nrm, _, _ = TREE.find_nearest(c)
        if f.normal.dot(nrm) < 0: f.normal_flip()
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
orient_out(eyes)

def offset2d(pts, d):
    """Offset a closed CCW-or-CW polygon outward by d (miter, front-view units)."""
    n = len(pts); area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2
    sgn = 1 if area > 0 else -1; out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nrm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1; return (sgn * dy / L, -sgn * dx / L)
        n1, n2 = nrm(p0, p1), nrm(p1, p2); m = (n1[0] + n2[0], n1[1] + n2[1]); ml = math.hypot(*m) or 1; m = (m[0] / ml, m[1] / ml)
        cosh = max(0.35, m[0] * n1[0] + m[1] * n1[1]); out.append((p1[0] + m[0] * d / cosh, p1[1] + m[1] * d / cosh))
    return out

LAND = {}
if not BODY_ONLY:
    # ============================================================ TIE + COLLAR (sketch tie_paths / collar_paths, centred x 150)
    tv, tf, tm = [], [], []
    def card(outline2d, tri_idx, off, mi):
        base = len(tv)
        for (x, y) in outline2d: tv.append(front_hit(x, y, off)[0])
        for t in tri_idx: tf.append([base + i for i in t]); tm.append(mi)
    neck = G.LM['neck']; ty = neck + 4
    k_d, b_d = G.tie_paths(150, ty)
    ks = parse(k_d); knot = [sg[0] for sg in ks] + [ks[-1][3]]   # 4 corners: TL, TR, BR, BL
    bsegs = parse(b_d)
    left = [bez(bsegs[0], t) for t in (0, 1 / 3, 2 / 3, 1)]   # (145,189) .. (136,244)
    vpt = bsegs[1][3]; right = [bez(bsegs[3], t) for t in (0, 1 / 3, 2 / 3, 1)][::-1]  # right side, top to bottom
    blade = left + [vpt] + right[::-1]                      # left down, V, right up (closed)
    # blade triangulation: rows top..bottom with a centre ridge vertex per row
    def blade_card(lft, rgt, v, off, mi):
        base = len(tv); rows = []
        for (xl, yl), (xr, yr) in zip(lft, rgt):
            rows.append([len(tv), len(tv) + 1, len(tv) + 2])
            for p in ((xl, yl), ((xl + xr) / 2, (yl + yr) / 2), (xr, yr)): tv.append(front_hit(p[0], p[1], off)[0])
        vi = len(tv); tv.append(front_hit(v[0], v[1], off)[0])
        for a, b in zip(rows, rows[1:]):
            for q in ((a[0], a[1], b[1], b[0]), (a[1], a[2], b[2], b[1])): tf.append([q[0], q[1], q[2]]); tf.append([q[0], q[2], q[3]]); tm.extend([mi, mi])
        b = rows[-1]; tf.append([b[0], b[1], vi]); tf.append([b[1], b[2], vi]); tm.extend([mi, mi])
    INKW = 2.2   # ink edge width, front units (sketch stroke 0.75 x 5 = 3.75, half outside)
    # ink first (under), colour on top
    lft_i = offset2d(left + [vpt] + right[::-1], INKW)
    nL = len(left); lft_ink = lft_i[:nL]; v_ink = lft_i[nL]; rgt_ink = lft_i[nL + 1:][::-1]
    lft_ink[0] = (lft_ink[0][0], lft_ink[0][1] - 1.0); rgt_ink[0] = (rgt_ink[0][0], rgt_ink[0][1] - 1.0)
    blade_card(lft_ink, rgt_ink, v_ink, 0.0046, 1)
    blade_card(left, right, vpt, 0.0054, 0)
    card(offset2d(knot, INKW), [(0, 1, 2), (0, 2, 3)], 0.0062, 1)
    card(knot, [(0, 1, 2), (0, 2, 3)], 0.0070, 0)
    for wing in G.collar_paths(150, neck):
        ws = parse(wing); corners = [s[0] for s in ws]       # 4 corners per wing (the path's 4 Bezier ends)
        card(offset2d(corners, 1.6), [(0, 1, 2), (0, 2, 3)], 0.0030, 1)
        card(corners, [(0, 1, 2), (0, 2, 3)], 0.0038, 2)
    acc_tie = mesh_obj('acc_tie', tv, tf, ['tie', 'ink', 'ghost'], fmat=tm, smooth=False); orient_out(acc_tie)
    LAND['collar_top'] = front_hit(150, neck, 0.004)[0]; LAND['knot_top'] = front_hit(150, ty, 0.007)[0]
    LAND['v_point'] = front_hit(vpt[0], vpt[1], 0.0054)[0]
    for k, v in LAND.items(): acc_tie[k + '_float_blender'] = list(v)

    # ============================================================ GLASSES: round rims on the eyes, a lilac band inside an ink band
    GL_N = 12; R_IN, R_MID, R_OUT = 15.0, 18.6, 23.0          # units; the eye is 13 tall, so the rim clears it
    gv, gf, gm = [], [], []
    for (ex, ey) in G.EYES:
        loops = []
        for r, off in ((R_IN, 0.0026), (R_MID, 0.0026), (R_OUT, 0.0022)):
            ids = []
            for k in range(GL_N):
                a = 2 * PI * (k + 0.5) / GL_N; ids.append(len(gv)); gv.append(front_hit(ex + r * math.cos(a), ey - r * math.sin(a), off)[0])
            loops.append(ids)
        for (A_, B_), mi in (((loops[0], loops[1]), 0), ((loops[1], loops[2]), 1)):
            for k in range(GL_N):
                k1 = (k + 1) % GL_N; gf += [[A_[k], A_[k1], B_[k1]], [A_[k], B_[k1], B_[k]]]; gm += [mi, mi]
    # bridge: an ink bar between the rims, just above the eye centre (sketch: an arc 3-8 units above)
    bx = 150 - G.EYES[0][0] - R_OUT + 1.0
    base = len(gv)
    for (x, y) in ((150 - bx, 113), (150 + bx, 113), (150 + bx, 108), (150 - bx, 108)): gv.append(front_hit(x, y, 0.0024)[0])
    gf += [[base, base + 1, base + 2], [base, base + 2, base + 3]]; gm += [1, 1]
    acc_glasses = mesh_obj('acc_glasses', gv, gf, ['acc', 'ink'], fmat=gm, smooth=False); orient_out(acc_glasses)

    # ============================================================ HEADSET: 2 cups on the ear points + a ridge band over the crown
    EAR_Y = G.LM['eye']; CUP_R, CUP_H, CUP_TOP = 19.0, 0.020, 0.74   # cup radius (units), height (m), top radius factor
    hv, hf, hm = [], [], []
    cup_top_z = None
    for sx in (1, -1):
        ex = 150 + sx * W(EAR_Y)
        c0 = Vector((sx * W(EAR_Y) * U, 0.0, zf(EAR_Y)))
        loc, nrm, _, _ = TREE.find_nearest(c0)
        nrm = Vector((nrm.x, 0.0, nrm.z)).normalized()          # level: the cup axis lies in the coronal plane
        up = Vector((0, 0, 1)); t1 = (up - nrm * up.dot(nrm)).normalized(); t2 = nrm.cross(t1)
        base, topr = [], []
        for k in range(8):
            a = 2 * PI * (k + 0.5) / 8; d = t1 * math.cos(a) + t2 * math.sin(a)
            p = loc + d * CUP_R * U
            l2, n2, _, _ = TREE.find_nearest(p); base.append(len(hv)); hv.append(l2 + nrm * 0.0008)
        H = max((hv[i] - loc).dot(nrm) for i in base) + CUP_H
        for k in range(8):
            a = 2 * PI * (k + 0.5) / 8; d = t1 * math.cos(a) + t2 * math.sin(a)
            topr.append(len(hv)); hv.append(loc + nrm * H + d * CUP_R * U * CUP_TOP)
        for k in range(8):
            k1 = (k + 1) % 8; hf.append([base[k], base[k1], topr[k1], topr[k]]); hm.append(0)
        hf += [[topr[0], topr[k], topr[k + 1]] for k in range(1, 7)]; hm += [1] * 6   # the pad is ink: the cup reads face-on
        cup_top_z = (loc + t1 * CUP_R * U).z
    # band: stations on the front outline (the coronal section of the body) from one cup top over the crown to the other
    BAND_HALF_W, BAND_H = 0.0075, 0.0085
    y_end = EAR_Y - CUP_R + 2.0
    ld = arc(DOME_F); s_end = None
    pts_r = [p for p in DOME_F if p[1] <= y_end]
    Lr = arc(pts_r); NSEG_HALF = 5
    stations = []
    for k in range(NSEG_HALF, 0, -1):
        x, y = at_len(pts_r, Lr, Lr[-1] * k / NSEG_HALF); stations.append((-(x - 150), y))
    stations.append((0.0, 36.0))
    for k in range(1, NSEG_HALF + 1):
        x, y = at_len(pts_r, Lr, Lr[-1] * k / NSEG_HALF); stations.append((x - 150, y))
    sid = []
    for (x, y) in stations:
        S = Vector((x * U, 0.0, zf(y)))
        loc, nrm, _, _ = TREE.find_nearest(S); nrm = Vector((nrm.x, 0, nrm.z)).normalized()
        ids = []
        for sy in (-1, 1):
            q = loc + Vector((0, sy * BAND_HALF_W, 0)); l2, n2, _, _ = TREE.find_nearest(q); ids.append(len(hv)); hv.append(l2 + n2 * 0.0006)
        ids.insert(1, len(hv)); hv.append(loc + nrm * BAND_H)          # [front-bottom, ridge, back-bottom]
        sid.append(ids)
    for a, b in zip(sid, sid[1:]):
        hf += [[a[0], b[0], b[1], a[1]], [a[1], b[1], b[2], a[2]]]; hm += [0, 0]
    acc_headset = mesh_obj('acc_headset', hv, hf, ['acc', 'ink'], fmat=hm, smooth=True)
    bm = bmesh.new(); bm.from_mesh(acc_headset.data)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3], quad_method='BEAUTY', ngon_method='BEAUTY')
    bm.to_mesh(acc_headset.data); bm.free()
    acc_headset.data.polygons.foreach_set('use_smooth', [True] * len(acc_headset.data.polygons))
    orient_out(acc_headset)
    acc_headset['cups_level_z_m'] = round(cup_top_z, 5)

# ================================================================ RIG + SKIN (join 3)
FLOAT = 0.22; GHOST_TOON['float_rest_m'] = FLOAT
REST_TILT = -4.0                                  # deg about Blender Y: the top leans to the viewer-left (sheet REST POSE)
REST_ARM_R_DROOP = 14.0                           # deg: arm_R hangs lower in the in-game rest pose (sheet REST POSE)
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root; flt.location = (0, 0, FLOAT)
flt.rotation_mode = 'XYZ'; flt.rotation_euler = (0, math.radians(REST_TILT), 0)
arm_d = bpy.data.armatures.new('rig'); rig = bpy.data.objects.new('rig', arm_d); COL.objects.link(rig); rig.parent = flt
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
b0 = arm_d.edit_bones.new('body_root'); b0.head = (0, 0, 0.0); b0.tail = (0, 0, zf(36))
for nm, ai in arm_info.items():
    b = arm_d.edit_bones.new(nm); b.head = ai['piv']; b.tail = body.data.vertices[ai['tip']].co.copy(); b.parent = b0
bpy.ops.object.mode_set(mode='OBJECT')
body.parent = rig
mod = body.modifiers.new('skin', 'ARMATURE'); mod.object = rig
g0 = body.vertex_groups.new(name='body_root'); gA = {nm: body.vertex_groups.new(name=nm) for nm in arm_info}
wmap = {}
# the shoulder row above the opening (row 180) and the side columns of the dome's last row follow the arm a little
SHOULDER_W = {}
for sx, nm in ((1, 'arm_L'), (-1, 'arm_R')):
    cols = (2, 3, 4, 5, 6) if sx > 0 else (10, 11, 12, 13, 14)
    for j in cols:
        w = {2: .04, 3: .12, 4: .25, 5: .12, 6: .04, 10: .04, 11: .12, 12: .25, 13: .12, 14: .04}[j]
        if w: SHOULDER_W[remap[ring_ids[ROWS.index(180.0)][j]]] = (nm, w)
for nm, ai in arm_info.items():
    for r, ws in zip(ai['rings'], ai['w']):
        for i, w in zip(r, ws): wmap[i] = (nm, w)
    wmap[ai['tip']] = (nm, 1.0)
for k_, v_ in SHOULDER_W.items():
    if k_ not in wmap: wmap[k_] = v_
for v in body.data.vertices:
    if v.index in wmap:
        nm, w = wmap[v.index]; gA[nm].add([v.index], w, 'REPLACE')
        if w < 1.0: g0.add([v.index], 1.0 - w, 'REPLACE')
    else: g0.add([v.index], 1.0, 'REPLACE')
checks['skin_unweighted_vertices (must be 0)'] = sum(1 for v in body.data.vertices if sum(g.weight for g in v.groups) <= 1e-6)
def wave_axis(nm):   # signed so that a positive rotation raises the tip (float space, Blender axes)
    ai = arm_info[nm]; d = (body.data.vertices[ai['tip']].co - ai['piv']).normalized(); h = d.cross(Vector((0, 0, 1))).normalized()
    return h if (Quaternion(h, 0.3) @ d).z > d.z else -h
flt['wave_axis_float_blender'] = {nm: list(wave_axis(nm)) for nm in arm_info}
flt['rest_arm_R_droop_deg'] = REST_ARM_R_DROOP
flt['arm_root_centre_float_blender'] = {nm: [sx * xf(250.0), 0.0, zf(225.0)] for sx, nm in ((1, 'arm_L'), (-1, 'arm_R'))}   # the tip = the arm vertex farthest from here (= the build's TIP_F rule)
flt['float_rest_m'] = FLOAT
flt['motion'] = 'Emil: y +/-0.06 m 2.4 s, x +/-0.03 m 3.7 s, yaw +/-8 deg 5.1 s; wave arm_L 0..+40 deg; rest: float tilt and arm_R droop'
swap = [eyes] + ([] if BODY_ONLY else [acc_tie, acc_glasses, acc_headset])
for o in swap: o.parent = flt
if not BODY_ONLY:
    for o in (acc_tie, acc_glasses, acc_headset): o['variant'] = o.name[4:]; o['default_visible'] = (o is acc_tie)
for nm, ai in arm_info.items():
    body[nm + '_tip_index'] = ai['tip']

# ================================================================ REPORT + EXPORT
bpy.context.view_layer.update()
counts = {o.name: tris(o) for o in [body] + swap}
base_t = counts['body'] + counts['eyes']; counts['base_body_arms_eyes'] = base_t
if not BODY_ONLY: counts['variant_totals'] = {v: base_t + counts['acc_' + v] for v in ('tie', 'glasses', 'headset')}
checks['eyes_offset_mm_min'] = round(min(sdist(v.co) for v in eyes.data.vertices) * 1000, 2)
if not BODY_ONLY:
    for o in (acc_tie, acc_glasses, acc_headset):
        checks[o.name + '_vertex_offset_mm_min'] = round(min(sdist(v.co) for v in o.data.vertices) * 1000, 2)
    checks['tie_landmarks_z_m'] = {k: round(v.z, 4) for k, v in LAND.items()}
meshes = [o.name for o in bpy.data.objects if o.type == 'MESH']
report = {'triangles': counts, 'meshes': {'all': meshes, 'non_swap (V5 <= 3)': ['body (skinned: body_root, arm_L, arm_R)'],
          'swap_parts': [o.name for o in swap]}, 'checks': checks,
          'rest_pose': {'float_tilt_deg_blender_y': REST_TILT, 'arm_R_droop_deg': REST_ARM_R_DROOP, 'mesh': 'upright, symmetric'},
          'ghost_toon': GHOST_TOON}
print('GHOST_REPORT', json.dumps(counts), json.dumps(checks))
json.dump(report, open(os.path.join(HERE, 'build_report.json'), 'w'), indent=1)
json.dump(GHOST_TOON, open(os.path.join(HERE, 'ghost_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, rig, body] + swap: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, 'ghostie.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=False, export_extras=True, export_materials='EXPORT', export_skins=True,
                          export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'ghostie.blend'))
print('GHOST_DONE')
