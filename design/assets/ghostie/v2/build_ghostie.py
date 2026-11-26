# GHOSTED - the Ghostie (ghost recruiter NPC), v2. Builds it from an empty scene, exports ghostie.glb, saves ghostie.blend.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_ghostie.py
# Units: metres. Blender is Z-up and the ghost faces -Y; the glTF export is Y-up (the ghost faces +Z in three.js).
# Nodes: root > float > body, eyes, arm_L, arm_R, acc_tie, acc_glasses, acc_headset (one accessory shown per variant).
# Budget (checklist V5, chair amendment 2): body + eyes + arms + one accessory <= 450 visible triangles.
# v2 = the 8 fixes of acceptance/ghostie/fix-brief-v2.md (see changes.md). v1 is archived in v1/.
import bpy, bmesh, math, json, os
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi

PAL = {
    'ghost': '#F8F4EA',   # Lena palette #16 ghost
    'acc':   '#C8C0D8',   # Lena palette #27 ghost-faded (added at the v1 gate)
    'tie':   '#C9A6D6',   # Lena palette #10 hq-wall (Recruiter HQ lilac): one step darker than #27, fix 5
    'ink':   '#2B1E16',   # Lena palette #22 ink: eye dots (and the outline, kit/toon.json)
}
# Kit's toon thresholds and Kit's neutral shade band (fix 6: Lena's rule, shade bands are neutral grey only).
GHOST_TOON = {
    'band_colors': {
        'ghost': [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]],
        'acc':   [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]],
        'tie':   [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]],
    },
    'basic_materials': ['ink'],
    'outline_nodes': ['body', 'arm_L', 'arm_R', 'acc_headset'],   # tie: ink backing plate (geometry); glasses: none
    'float_rest_m': None, 'variants': ['tie', 'glasses', 'headset'],
    'contact_shadow': {'rx': 0.20, 'ry': 0.17, 'opacity_at_rest': 0.22},
}

def s2l(h):
    h = h.lstrip('#'); out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
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

def new_obj(name, bm, matname, smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(mat(matname))
    for p in me.polygons: p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob); return ob

def tris(ob):
    ob.data.calc_loop_triangles(); return len(ob.data.loop_triangles)

HB = 0.47
FLOAT = 0.22
GHOST_TOON['float_rest_m'] = FLOAT
SEG = 14     # 14 columns: the side outline wobbles 2.5% (cos 12.9 deg); the triangles go to profile rings instead

def dirv(th):                               # th = 0 -> front (-Y), +90 deg -> +X (the ghost's left)
    return Vector((math.sin(th), -math.cos(th), 0))

# ================================================================ BODY (fix 1: rounder outline)
# The silhouette of a lathe seen from the side is its profile, so the v2 triangles go into profile rings, not columns:
# the crown is a 14-gon fan (v1: 8) and the dome has 5 rings + shoulder (15 deg turns, v1: 22-34 deg), the skirt has
# 2 rings that bow out into the flare (v1: 1). The hem ring has 28 vertices (7 per scallop) so the scallops are round (fix 3).
CROWN = 0.470; SHOULDER = 0.310; DOME_R = 0.188
DOME = [(SHOULDER + (CROWN - SHOULDER) * math.cos(math.radians(f)), DOME_R * math.sin(math.radians(f))) for f in (15, 30, 45, 60, 75, 90)]
SKIRT = [(0.200, 0.192), (0.100, 0.206)]
PROFILE = DOME + SKIRT
HEM_N = 28
HEM_A = 0.034        # scallop depth (notch height above lobe bottom)
HEM_R0, HEM_R1 = 0.238, 0.216   # radius at lobe bottom / at notch (the notch tucks in)
def hem_zr(th):
    """4 round scallops: lobe centres at 0, 90, 180, 270 deg. ((1 - cos 4th) / 2) ** 1.4 is flat at the lobe bottom and
    round (zero slope) at the notch top, so neither end is a V."""
    w = ((1 - math.cos(4 * th)) / 2) ** 1.4
    return HEM_A * w, HEM_R0 + (HEM_R1 - HEM_R0) * w
HEM_T = 0.020; HEM_LIFT = 0.007; CAVITY = 0.205

def band(a, b):
    """Connect ring a to ring b; len(b) = k * len(a) (k = 1, 2, 4...) or len(a) = k * len(b)."""
    if len(a) > len(b):
        flip = True; a, b = b, a
    else: flip = False
    na, nb = len(a), len(b); k = nb // na
    for i in range(na):
        i1 = (i + 1) % na
        for m in range(k):
            f = [a[i], b[(k * i + m) % nb], b[(k * i + m + 1) % nb]]
            bm.faces.new(f[::-1] if flip else f)
        f = [a[i], b[(k * i + k) % nb], a[i1]]
        bm.faces.new(f[::-1] if flip else f)

bm = bmesh.new()
crown = bm.verts.new((0, 0, CROWN))
rings = [[bm.verts.new(dirv(2 * PI * j / SEG) * r + Vector((0, 0, z))) for j in range(SEG)] for z, r in PROFILE]
hem = []
for j in range(HEM_N):
    th = 2 * PI * j / HEM_N; z, r = hem_zr(th); hem.append(bm.verts.new(dirv(th) * r + Vector((0, 0, z))))
inner = []
for j in range(0, HEM_N, 4):      # 7 inner rim vertices
    th = 2 * PI * j / HEM_N; z, r = hem_zr(th); inner.append(bm.verts.new(dirv(th) * (r - HEM_T) + Vector((0, 0, z + HEM_LIFT))))
cav = bm.verts.new((0, 0, CAVITY))
for i in range(SEG): bm.faces.new([crown, rings[0][i], rings[0][(i + 1) % SEG]])
for ra, rb in zip(rings[:-1], rings[1:]): band(ra, rb)
band(rings[-1], hem)
band(inner, hem)
for i in range(len(inner)): bm.faces.new([inner[i], cav, inner[(i + 1) % len(inner)]])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
hs, ins = set(hem), set(inner)
for e in bm.edges:
    v0, v1 = e.verts
    if (v0 in hs and v1 in hs) or (v0 in ins and v1 in ins): e.smooth = False
body = new_obj('body', bm, 'ghost')
body_bm = bmesh.new(); body_bm.from_mesh(body.data); body_bm.normal_update()
TREE = BVHTree.FromBMesh(body_bm)

def sdist(p):
    loc, nrm, _, d = TREE.find_nearest(p)
    return d if (p - loc).dot(nrm) >= 0 else -d
def surf(th, z, off):
    d = dirv(th); o = d * 1.0 + Vector((0, 0, z))
    loc, nrm, _, _ = TREE.ray_cast(o, -d)
    return loc + nrm * off, nrm
def surf_near(p):
    loc, nrm, _, _ = TREE.find_nearest(p); return loc, nrm
def surf_uv(thc, zc, u, v, off, r_ref=0.20):
    return surf(thc + u / r_ref, zc + v, off)
def orient(bm, faces_out):
    for f, w in faces_out:
        f.normal_update()
        if f.normal.dot(w) < 0: f.normal_flip()

# ================================================================ EYES: 2 ink dots, 12 sides (fix 1), on the surface
# Each eye sits on the vertex column j=+-1 (25.7 deg), inside the face row between the skirt ring z 0.200 and the
# shoulder ring z 0.310, so the dot and the glasses frame never span a crease of the faceted body.
EYE_TH = 2 * PI / SEG;   # column j=+-1 (25.7 deg)
EYE_TH = EYE_TH; EYE_Z = 0.262; EYE_RX = 0.0190; EYE_RZ = 0.0280; EYE_N = 12
EYE_OFF_RIM = 0.0012; EYE_OFF_C = 0.0022
bm = bmesh.new(); eye_faces = []
for s in (-1, 1):
    c, cn = surf(s * EYE_TH, EYE_Z, EYE_OFF_C); cv = bm.verts.new(c)
    rim = [bm.verts.new(surf_uv(s * EYE_TH, EYE_Z, EYE_RX * math.cos(2 * PI * k / EYE_N), EYE_RZ * math.sin(2 * PI * k / EYE_N), EYE_OFF_RIM)[0]) for k in range(EYE_N)]
    for k in range(EYE_N):
        f = bm.faces.new([cv, rim[k], rim[(k + 1) % EYE_N]]); eye_faces.append((f, cn))
orient(bm, eye_faces)
eyes = new_obj('eyes', bm, 'ink')

# ================================================================ ARMS (fix 2): round mittens that leave the body square-on
# v1 flaps hugged the body (24 deg down, tapered), so their ink was hidden at the root and they vanished in 3/4.
# v2: the mitten leaves the surface nearly at a right angle and is widest 30 mm out, so its own outline closes in air;
# 80 mm long, so it still breaks the 3/4 silhouette.
ARM_N = 8
ARM_TH = math.radians(92); ARM_Z = 0.160
def arm_axis(s):
    out = dirv(s * ARM_TH)
    a = out * math.cos(math.radians(12)) + Vector((0, 0, -math.sin(math.radians(12))))
    a = a + Vector((0, 0.36, 0)); return a.normalized()   # 20 deg back: no default view sees the mitten end-on
ARM_PROF = [(-0.045, 0.024), (0.044, 0.036), (0.068, 0.0)]   # base (in body), widest, round tip (8 sides)
arms = {}; arm_pivots = {}
for s, nm in ((1, 'arm_L'), (-1, 'arm_R')):
    piv, _ = surf(s * ARM_TH, ARM_Z, 0.0); ax = arm_axis(s)
    ex = ax.cross(Vector((0, 0, 1))).normalized(); ey = ax.cross(ex).normalized()
    bm = bmesh.new(); rr = []
    for t, r in ARM_PROF:
        if r == 0: rr.append([bm.verts.new(piv + ax * t)]); continue
        rr.append([bm.verts.new(piv + ax * t + ex * (r * math.cos(2 * PI * k / ARM_N)) + ey * (r * 0.85 * math.sin(2 * PI * k / ARM_N))) for k in range(ARM_N)])
    fo = []
    for ri in range(len(rr) - 1):
        a, b = rr[ri], rr[ri + 1]
        for k in range(ARM_N):
            k1 = (k + 1) % ARM_N
            q = [a[k], a[k1], b[0]] if len(b) == 1 else [a[k], a[k1], b[k1], b[k]]
            f = bm.faces.new(q); cen = f.calc_center_median()
            fo.append((f, cen - (piv + ax * ax.dot(cen - piv)) + ax * (0.5 if len(b) == 1 else 0)))
    orient(bm, fo)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
    arms[nm] = new_obj(nm, bm, 'ghost'); arm_pivots[nm] = (piv, ax)

# ================================================================ ACCESSORIES (Lena #27 ghost-faded)
ACC_BASE = 0.0004
def shell(bm, pts_top, pts_base, front_tris, boundary, normals, centre, closed=False):
    T = [bm.verts.new(p) for p in pts_top]; B = [bm.verts.new(p) for p in pts_base]; fo = []
    for a, b, c in front_tris:
        f = bm.faces.new([T[a], T[b], T[c]]); fo.append((f, (normals[a] + normals[b] + normals[c])))
        if closed:
            f = bm.faces.new([B[a], B[b], B[c]]); fo.append((f, -(normals[a] + normals[b] + normals[c])))
    n = len(boundary)
    for i in range(n):
        a, b = boundary[i], boundary[(i + 1) % n]
        f = bm.faces.new([T[a], T[b], B[b], B[a]])
        mid = (pts_top[a] + pts_top[b]) / 2; fo.append((f, mid - centre))
    orient(bm, fo)
def uv_shell(bm, thc, zc, uv, off_top, front_tris, boundary, closed=False, off_base=ACC_BASE):
    top, base, nrm = [], [], []
    for u, v in uv:
        p, n = surf_uv(thc, zc, u, v, off_top); top.append(p); nrm.append(n)
        base.append(surf_uv(thc, zc, u, v, off_base)[0])
    mu = sum(u for u, _ in uv) / len(uv); mv = sum(v for _, v in uv) / len(uv)
    c, _ = surf_uv(thc, zc, mu, mv, 0.0)
    shell(bm, top, base, front_tris, boundary, nrm, c, closed)

# -- tie (fix 5): on the chest, below the arm line. An inverted hull cannot outline a part this thin (the body hides
#    the hull), so the ink edge is geometry: an ink plate 2.5 mm wider than the tie lies under it at 1.6 mm.
TIE_Z = 0.128
tie = [(-0.018, 0.012), (0.0, 0.013), (0.018, 0.012), (0.008, -0.011), (0.023, -0.088), (0.0, -0.110), (-0.023, -0.088), (-0.008, -0.011), (0.0, -0.012)]   # long: reads vertical (a tie), not a mouth
#        0 TL          1 TC          2 TR          3 neck R        4 blade R        5 tip          6 blade L         7 neck L        8 neck C
tie_tris = [(0, 1, 8), (0, 8, 7), (1, 2, 3), (1, 3, 8), (7, 8, 5), (7, 5, 6), (8, 3, 4), (8, 4, 5)]
bm = bmesh.new()
uv_shell(bm, 0.0, TIE_Z, tie, 0.0045, tie_tris, [0, 1, 2, 3, 4, 5, 6, 7], off_base=0.0022)
n_tie = len(bm.faces)
def grow_poly(pts, d=0.0025):
    """Mitred outward offset of the closed outline pts[0..7] (CCW or CW); the inner neck vertex 8 stays."""
    n = len(pts); area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)); sg = 1 if area > 0 else -1
    out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        def nrm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); return (sg * dy / L, -sg * dx / L)
        n1, n2 = nrm(p0, p1), nrm(p1, p2); mx, my = n1[0] + n2[0], n1[1] + n2[1]; L = math.hypot(mx, my)
        mx, my = mx / L, my / L; c = max(0.5, mx * n1[0] + my * n1[1])
        out.append((p1[0] + mx * d / c, p1[1] + my * d / c))
    return out
grown = grow_poly(tie[:8]) + [tie[8]]
plate = [surf_uv(0.0, TIE_Z, u, v, 0.0016) for u, v in grown]
PV = [bm.verts.new(p) for p, _ in plate]; fo = []
for t in tie_tris:
    f = bm.faces.new([PV[i] for i in t]); f.material_index = 1; fo.append((f, plate[t[0]][1]))
orient(bm, fo)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_tie = new_obj('acc_tie', bm, 'tie'); acc_tie.data.materials.append(mat('ink'))

# -- glasses: two hex frames ringing the eye dots + a bridge on the centre ridge; flat print 1.5 mm off the surface
GL_RI, GL_RO, GL_OFF = 0.0350, 0.0460, 0.0015
bm = bmesh.new()
for s in (-1, 1):
    thc = s * EYE_TH; o_top, o_base, i_top, nr = [], [], [], []
    for k in range(6):
        a = 2 * PI * k / 6 + PI / 6
        p, n = surf_uv(thc, EYE_Z, GL_RO * math.cos(a), GL_RO * math.sin(a), GL_OFF); o_top.append(p); nr.append(n)
        o_base.append(surf_uv(thc, EYE_Z, GL_RO * math.cos(a), GL_RO * math.sin(a), ACC_BASE)[0])
        i_top.append(surf_uv(thc, EYE_Z, GL_RI * math.cos(a), GL_RI * math.sin(a), GL_OFF)[0])
    O = [bm.verts.new(p) for p in o_top]; OB = [bm.verts.new(p) for p in o_base]; I = [bm.verts.new(p) for p in i_top]
    c, _ = surf(thc, EYE_Z, 0.0); fo = []
    for k in range(6):
        k1 = (k + 1) % 6
        f = bm.faces.new([O[k], O[k1], I[k1], I[k]]); fo.append((f, nr[k]))   # v2: no walls (budget for the arm collars)
    orient(bm, fo)
gap_u = 0.20 * EYE_TH - GL_RO * math.cos(PI / 6) + 0.003
br = [(-gap_u, 0.004), (0.0, 0.004), (gap_u, 0.004), (gap_u, -0.004), (0.0, -0.004), (-gap_u, -0.004)]
pts = [surf_uv(0.0, EYE_Z, u, v, GL_OFF - 0.0003) for u, v in br]
V = [bm.verts.new(p) for p, _ in pts]; fo = []
for q in ([V[0], V[1], V[4], V[5]], [V[1], V[2], V[3], V[4]]):
    f = bm.faces.new(q); fo.append((f, pts[1][1]))
orient(bm, fo)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_glasses = new_obj('acc_glasses', bm, 'acc')

# -- headset (fix 4): the band lies 1.2 mm on the body's own vertex columns, so at the crown it covers only the inner
#    1.2 mm of the 7 mm ink line, and its own ink hull continues the crown outline. Bigger ear cup (r 46 mm, 8 sides).
HS_W, HS_OFF = 0.0120, 0.0006
bm = bmesh.new()
# stations: the band runs on the face midline at +-90 deg (between columns 3|4 and 10|11). A lathe quad is a flat
# trapezoid, so a straight band segment between ring heights lies exactly on the face: no chord cuts in.
class St:
    def __init__(s, co, n): s.co, s.normal = co, n
V_ = body.data.vertices
def ring_mid(ri, j0):
    a_, b_ = V_[1 + ri * SEG + j0], V_[1 + ri * SEG + (j0 + 1) % SEG]
    return St((a_.co + b_.co) / 2, (a_.normal + b_.normal).normalized())
NR = len(DOME)
stations = [ring_mid(ri, 10) for ri in range(NR - 1, -1, -1) if PROFILE[ri][0] > SHOULDER + 0.03] + [St(V_[0].co.copy(), V_[0].normal.copy())] + \
           [ring_mid(ri, 3) for ri in range(NR)]
side = Vector((0, 1, 0)); T = []; fo = []
for v in stations:
    n = v.normal
    for sg in (-1, 1): T.append(bm.verts.new(v.co + side * sg * HS_W + n * HS_OFF))
for i in range(len(stations) - 1):
    f = bm.faces.new([T[2 * i], T[2 * i + 1], T[2 * i + 3], T[2 * i + 2]]); fo.append((f, stations[i].normal + stations[i + 1].normal))
orient(bm, fo)
CUP_R, CUP_OFF, CUP_N = 0.046, 0.0090, 8
CUP_Z = stations[-1].co.z
cth = math.radians(90); ct, cb, cn = [], [], []
for k in range(CUP_N):
    a = 2 * PI * k / CUP_N + PI / 2
    p, n = surf_uv(cth, CUP_Z, CUP_R * math.cos(a), CUP_R * math.sin(a), CUP_OFF); ct.append(p); cn.append(n)
    cb.append(surf_uv(cth, CUP_Z, CUP_R * math.cos(a), CUP_R * math.sin(a), ACC_BASE)[0])
cc, _ = surf(cth, CUP_Z, 0.0)
shell(bm, ct, cb, [(0, k, k + 1) for k in range(1, CUP_N - 1)], list(range(CUP_N)), cn, cc)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_headset = new_obj('acc_headset', bm, 'acc')
for o in (acc_tie, acc_glasses, acc_headset): o.data.polygons.foreach_set('use_smooth', [False] * len(o.data.polygons))

# ================================================================ REST POSE (fix 7: node rotations only)
def rot_about(axis, deg): return Quaternion(axis.normalized(), math.radians(deg))
ARM_REST = {}
for nm, (up, fwd) in {'arm_L': (13, 0), 'arm_R': (-9, 8)}.items():
    piv, ax = arm_pivots[nm]; h = ax.cross(Vector((0, 0, 1))).normalized()
    q = rot_about(h, up)
    if (q @ ax).z * (1 if up > 0 else -1) < ax.z * (1 if up > 0 else -1): q = rot_about(h, -up)   # make "up" raise the tip
    if fwd:
        qf = rot_about(Vector((0, 0, 1)), fwd)
        if (qf @ (q @ ax)).y > (q @ ax).y: qf = rot_about(Vector((0, 0, 1)), -fwd)                 # forward = toward -Y
        q = qf @ q
    ARM_REST[nm] = q
FLOAT_ROLL, FLOAT_LEAN = 5.0, 3.0

# ================================================================ ARM COLLARS (fix 2): ink where the mitten meets the body
# An inverted hull cannot draw the root line: there the hull lies inside the body. So the root line is geometry, an ink
# band 6 mm wide on the body around the rest-pose intersection of mitten and body (6 quads per arm).
bm = bmesh.new(); fo = []
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]; Rq = ARM_REST[nm].to_matrix()
    vs = [piv + Rq @ (v.co - piv) for v in o.data.vertices]
    base, wide = vs[:ARM_N], vs[ARM_N:2 * ARM_N]
    axr = Rq @ ax; inner_pts, outer_pts = [], []
    for k in range(ARM_N):
        lo, hi = base[k], wide[k]
        for _ in range(40):
            mid = (lo + hi) / 2
            if sdist(mid) < 0: lo = mid
            else: hi = mid
        loc, nrm = surf_near(hi)
        radial = (loc - (piv + axr * axr.dot(loc - piv))); radial = (radial - nrm * radial.dot(nrm)).normalized()
        inner_pts.append(loc + nrm * 0.0012)
        l2, n2 = surf_near(loc + radial * 0.0060); outer_pts.append(l2 + n2 * 0.0012)
    I_ = [bm.verts.new(p) for p in inner_pts]; O_ = [bm.verts.new(p) for p in outer_pts]
    for k in range(ARM_N):
        k1 = (k + 1) % ARM_N
        f = bm.faces.new([I_[k], I_[k1], O_[k1], O_[k]]); fo.append((f, surf_near(f.calc_center_median())[1]))
orient(bm, fo)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
collars = new_obj('arm_collars', bm, 'ink')
collars.data.polygons.foreach_set('use_smooth', [False] * len(collars.data.polygons))

# ================================================================ CHECKS (numbers; the crops are the proof)
def sample_tris(ob, faces_filter=None, n=6, M=None):
    me = ob.data; me.calc_loop_triangles(); out = []
    for lt in me.loop_triangles:
        if faces_filter and not faces_filter(me.polygons[lt.polygon_index]): continue
        a, b, c = ((M @ me.vertices[i].co) if M else me.vertices[i].co for i in lt.vertices)
        for i in range(n + 1):
            for j in range(n + 1 - i):
                k = n - i - j; out.append((a * i + b * j + c * k) / n)
    return out
def rng(vals): return [round(min(vals) * 1000, 2), round(max(vals) * 1000, 2)]
def is_front(poly):
    _, n = surf_near(poly.center); return poly.normal.dot(n) > 0.6
checks = {}
checks['eyes_offset_mm_min_max (must be > 0)'] = rng([sdist(p) for p in sample_tris(eyes)])
checks['arm_collars_offset_mm_min_max (must be > 0)'] = rng([sdist(p) for p in sample_tris(collars)])
for o in (acc_tie, acc_glasses, acc_headset):
    checks[o.name + '_front_faces_offset_mm_min_max (visible, must be > 0)'] = rng([sdist(p) for p in sample_tris(o, is_front)])
    checks[o.name + '_all_faces_offset_mm_min_max'] = rng([sdist(p) for p in sample_tris(o)])
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]; Rq = ARM_REST[nm].to_matrix()
    base = [piv + Rq @ (v.co - piv) for v in o.data.vertices][:ARM_N]
    checks[nm + '_base_ring_depth_mm_at_rest (must be < 0)'] = rng([sdist(p) for p in base])
    worst = -1
    for axis in (Vector((0, 0, 1)), ax.cross(Vector((0, 0, 1))).normalized()):
        for ang in (-20, 20):
            R = Matrix.Rotation(math.radians(ang), 3, axis) @ Rq
            worst = max(worst, max(sdist(piv + R @ (v.co - piv)) for v in list(o.data.vertices)[:ARM_N]))
    checks[nm + '_base_ring_worst_mm_at_rest_+-20deg (must be < 0)'] = round(worst * 1000, 2)
    tipring = [piv + Rq @ (v.co - piv) for v in list(o.data.vertices)[ARM_N:2 * ARM_N]]
    checks[nm + '_widest_ring_clearance_mm (gap from body, for the ink)'] = rng([sdist(p) for p in tipring])
cup_pts = [v.co for v in acc_headset.data.vertices]
armL_rest = [arm_pivots['arm_L'][0] + ARM_REST['arm_L'].to_matrix() @ (v.co - arm_pivots['arm_L'][0]) for v in arms['arm_L'].data.vertices]
checks['earcup_to_armL_min_gap_mm'] = round(min((p - q).length for p in cup_pts for q in armL_rest) * 1000, 1)
checks['tie_top_z_vs_arm_root_z_m'] = [round(TIE_Z + 0.013, 3), ARM_Z]
checks['hem_thickness_mm'] = HEM_T * 1000
checks['hem_scallops'] = 4; checks['hem_notch_depth_mm'] = HEM_A * 1000
checks['eye_to_glasses_inner_edge_min_gap_mm'] = round((GL_RI * math.cos(PI / 6) - EYE_RZ) * 1000, 1)

# ================================================================ RIG + EXPORT
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root; flt.location = (0, 0, FLOAT)
flt.rotation_mode = 'XYZ'; flt.rotation_euler = (math.radians(FLOAT_LEAN), math.radians(FLOAT_ROLL), 0)   # lean to viewer, roll
for o in [body, eyes, collars, acc_tie, acc_glasses, acc_headset]: o.parent = flt
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]; o.data.transform(Matrix.Translation(-piv)); o.location = piv; o.parent = flt
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = ARM_REST[nm]
    o['pivot_axis_blender'] = list(ax)
for o in (acc_tie, acc_glasses, acc_headset): o['variant'] = o.name[4:]; o['default_visible'] = (o is acc_tie)
flt['float_rest_m'] = FLOAT
flt['motion'] = 'Emil: y +/-0.06 m 2.4 s, x +/-0.03 m 3.7 s, yaw +/-8 deg 5.1 s; keep the rest roll/lean (compose yaw on top)'

bpy.context.view_layer.update()
counts = {o.name: tris(o) for o in [body, eyes, collars, arms['arm_L'], arms['arm_R'], acc_tie, acc_glasses, acc_headset]}
base_t = counts['body'] + counts['eyes'] + counts['arm_collars'] + counts['arm_L'] + counts['arm_R']
counts['base_body_eyes_arms'] = base_t
counts['variant_totals'] = {v: base_t + counts['acc_' + v] for v in ('tie', 'glasses', 'headset')}
report = {'triangles': counts, 'checks': checks, 'size': {'body_height_m': HB, 'float_m': FLOAT, 'crown_m': FLOAT + CROWN,
          'hem_width_m': round(2 * HEM_R0, 3), 'kit_height_m': 0.977}, 'rest_pose': {'float_lean_deg': FLOAT_LEAN, 'float_roll_deg': FLOAT_ROLL,
          'arm_L_up_deg': 13, 'arm_R_down_deg': 9, 'arm_R_forward_deg': 8}, 'ghost_toon': GHOST_TOON}
print('GHOST_REPORT', json.dumps(report['triangles']))
json.dump(report, open(os.path.join(HERE, 'build_report.json'), 'w'), indent=1)
json.dump(GHOST_TOON, open(os.path.join(HERE, 'ghost_toon.json'), 'w'), indent=1)

bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, body, eyes, collars, acc_tie, acc_glasses, acc_headset] + list(arms.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, 'ghostie.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=True, export_extras=True, export_materials='EXPORT',
                          export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'ghostie.blend'))
print('GHOST_DONE')
