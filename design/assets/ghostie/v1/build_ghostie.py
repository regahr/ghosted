# GHOSTED - the Ghostie (ghost recruiter NPC). Builds it from an empty scene, exports ghostie.glb, saves ghostie.blend.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_ghostie.py
# Units: metres. Blender is Z-up and the ghost faces -Y; the glTF export is Y-up (the ghost faces +Z in three.js).
# Nodes: root > float > body, eyes, arm_L, arm_R, acc_tie, acc_glasses, acc_headset (one accessory shown per variant).
# Budget (checklist V5): body + eyes + arms + one accessory <= 300 triangles. It is instanced up to ~24.
# Same pipeline as Kit (assets/kit/build_kit.py): Principled base colour only in the glTF, the game applies toon.
import bpy, bmesh, math, json, os
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi

# ---------------------------------------------------------------- palette (sRGB hex)
PAL = {
    'ghost': '#F8F4EA',   # Lena palette #16 ghost (bible: opaque off-white)
    'acc':   '#C8C0D8',   # Illustrator section 4: faded accessory colour (NOT in Lena's 24 yet: L3 open item)
    'ink':   '#2B1E16',   # Lena palette #22 ink: eye dots (and the outline, set in kit/toon.json)
}
# Ghost toon extras on top of kit/toon.json (same thresholds; only the band colours differ).
# Illustrator section 5: the ghost's shadow band is lavender, not grey. The band value multiplies the sun light, so a
# tinted band gives a cool shadow under the same warm light as Kit. Accessories use Kit's plain 2-band ramp.
GHOST_TOON = {
    'band_colors': {
        'ghost': [[-1.0, [184, 170, 255]], [0.0001, [255, 255, 255]]],   # Kit's 2-band thresholds (see changes.md)
        'acc':   [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]],
    },
    'basic_materials': ['ink'],
    'outline_nodes': ['body', 'arm_L', 'arm_R'],   # accessories: no ink line (faded, and open shells)
    'float_rest_m': None, 'variants': ['tie', 'glasses', 'headset'],
    'contact_shadow': {'rx': 0.20, 'ry': 0.17, 'opacity_at_rest': 0.22},
}

def s2l(h):
    h = h.lstrip('#'); out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out

# ---------------------------------------------------------------- scene reset
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

# ================================================================ SIZE
# Opinion (design lead): body 0.46 m from lobe tip to crown, floating 0.22 m -> crown at 0.68 m, 70% of Kit (0.977 m).
# Illustrator asked for ~1.0 Kit head-height (0.36 m). At the 26 m camera that is ~20 px and the accessory is
# ~2 px, so it is scaled up to stay readable while still clearly smaller than Kit (see changes.md).
HB = 0.46
FLOAT = 0.22
GHOST_TOON['float_rest_m'] = FLOAT
SEG = 16                                    # radial segments; vertex column j=0 faces front (-Y)

def dirv(th):                               # th = 0 -> front (-Y), +90 deg -> +X (the ghost's left)
    return Vector((math.sin(th), -math.cos(th), 0))

# ================================================================ BODY: lathe teardrop with a gentle shoulder
# profile (z, r), crown -> waist: an elliptic dome (crown 0.46, shoulder 0.32) and a near-vertical side that the hem
# flares out from. The first ring has 8 vertices (it is small, near the crown) and feeds the 16-vertex rings through a
# 3-triangle-per-step transition; the saved triangles buy one more dome ring, so the crown outline turns ~22 deg per
# ring instead of ~25-35 deg (v1 sheet showed hard corners on the crown).
CROWN = 0.470; SHOULDER = 0.310; DOME_R = 0.188
PROFILE = [(SHOULDER + (CROWN - SHOULDER) * math.cos(math.radians(f)), DOME_R * math.sin(math.radians(f)))
           for f in (24, 48, 70, 90)] + [(0.130, 0.204)]
RING_N = [8, 16, 16, 16, 16]
# 4-scallop hem, k = j % 4: lobes are wide rounded tabs (3 low vertices), notches are V's that tuck in.
HEM = {0: (0.000, 0.238), 1: (0.008, 0.234), 2: (0.040, 0.212), 3: (0.008, 0.234)}
HEM_T = 0.020        # hem thickness (radial) - the sheet has a real edge
HEM_LIFT = 0.007     # the inner edge of the rim sits a little higher, so the rim faces down-and-out
CAVITY = 0.205       # inner pole height: the ghost is hollow under the hem, closed by a concave cap

def ring(n, z, r, jstep=1):
    return [bm.verts.new(dirv(2 * PI * j / n) * r + Vector((0, 0, z))) for j in range(n)]
def band(a, b):
    """a (upper or lower) and b rings; len(b) is len(a) or 2*len(a)."""
    na, nb = len(a), len(b)
    for i in range(na):
        i1 = (i + 1) % na
        if na == nb:
            bm.faces.new([a[i], b[i], b[i1]]); bm.faces.new([a[i], b[i1], a[i1]])
        else:
            m0, m1, m2 = b[2 * i], b[2 * i + 1], b[(2 * i + 2) % nb]
            bm.faces.new([a[i], m0, m1]); bm.faces.new([a[i], m1, a[i1]]); bm.faces.new([a[i1], m1, m2])

bm = bmesh.new()
crown = bm.verts.new((0, 0, CROWN))
rings = [ring(n, z, r) for n, (z, r) in zip(RING_N, PROFILE)]
hem = []
for j in range(SEG):
    z, r = HEM[j % 4]; hem.append(bm.verts.new(dirv(2 * PI * j / SEG) * r + Vector((0, 0, z))))
inner = []          # 8 vertices: one under each lobe centre and each notch (j even)
for j in range(0, SEG, 2):
    z, r = HEM[j % 4]; inner.append(bm.verts.new(dirv(2 * PI * j / SEG) * (r - HEM_T) + Vector((0, 0, z + HEM_LIFT))))
cav = bm.verts.new((0, 0, CAVITY))
for i in range(len(rings[0])): bm.faces.new([crown, rings[0][i], rings[0][(i + 1) % len(rings[0])]])
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
    """Point on the body surface hit by a horizontal ray toward the axis at height z, pushed off along the face normal."""
    d = dirv(th); o = d * 1.0 + Vector((0, 0, z))
    loc, nrm, _, _ = TREE.ray_cast(o, -d)
    return loc + nrm * off, nrm

def surf_uv(thc, zc, u, v, off, r_ref=0.20):
    return surf(thc + u / r_ref, zc + v, off)

def orient(bm, faces_out):
    """faces_out: list of (face, wanted outward vector). Flip faces whose normal points the other way."""
    for f, w in faces_out:
        f.normal_update()
        if f.normal.dot(w) < 0: f.normal_flip()

# ================================================================ EYES: 2 ink dots ON the surface (no mouth)
# Each eye sits ON the body's vertex column j=+-1 (22.5 deg) and inside one face row (between the waist ring z 0.130
# and the shoulder ring z 0.310), so the dot and the glasses frame never span a crease of the faceted surface.
EYE_TH = math.radians(22.5); EYE_Z = 0.262; EYE_RX = 0.0190; EYE_RZ = 0.0280
EYE_OFF_RIM = 0.0012; EYE_OFF_C = 0.0022
bm = bmesh.new(); eye_faces = []
for s in (-1, 1):
    c, cn = surf(s * EYE_TH, EYE_Z, EYE_OFF_C); cv = bm.verts.new(c)
    rim = [bm.verts.new(surf_uv(s * EYE_TH, EYE_Z, EYE_RX * math.cos(2 * PI * k / 8), EYE_RZ * math.sin(2 * PI * k / 8), EYE_OFF_RIM)[0]) for k in range(8)]
    for k in range(8):
        f = bm.faces.new([cv, rim[k], rim[(k + 1) % 8]]); eye_faces.append((f, cn))
orient(bm, eye_faces)
eyes = new_obj('eyes', bm, 'ink')

# ================================================================ ARMS: stubby nubs, pivot on the body surface
ARM_N = 5   # 5 sides: 15 triangles per arm (budget)
ARM_TH = math.radians(88); ARM_Z = 0.165
def arm_axis(s):
    out = dirv(s * ARM_TH)
    a = out * math.cos(math.radians(24)) + Vector((0, 0, -math.sin(math.radians(24))))   # 24 deg down
    a = a + Vector((0, -0.06, 0)); return a.normalized()                                # and a touch forward
ARM_PROF = [(-0.050, 0.024), (0.022, 0.034), (0.072, 0.0)]   # tapered flap, like a sheet corner   # (t along axis from the pivot, r); last = rounded tip pole
arms = {}; arm_pivots = {}
for s, nm in ((1, 'arm_L'), (-1, 'arm_R')):
    piv, _ = surf(s * ARM_TH, ARM_Z, 0.0); ax = arm_axis(s)
    ex = ax.cross(Vector((0, 0, 1))).normalized(); ey = ax.cross(ex).normalized()
    bm = bmesh.new(); rr = []
    for t, r in ARM_PROF:
        if r == 0: rr.append([bm.verts.new(piv + ax * t)]); continue
        rr.append([bm.verts.new(piv + ax * t + ex * (r * math.cos(2 * PI * k / ARM_N)) + ey * (r * math.sin(2 * PI * k / ARM_N))) for k in range(ARM_N)])
    fo = []
    for k in range(ARM_N):
        k1 = (k + 1) % ARM_N
        f = bm.faces.new([rr[0][k], rr[0][k1], rr[1][k1], rr[1][k]]); fo.append((f, f.calc_center_median() - (piv + ax * 0.004)))
        f = bm.faces.new([rr[1][k], rr[1][k1], rr[2][0]]); fo.append((f, f.calc_center_median() - (piv + ax * 0.02)))
    orient(bm, fo)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
    arms[nm] = new_obj(nm, bm, 'ghost'); arm_pivots[nm] = (piv, ax)

# ================================================================ ACCESSORIES (faded #C8C0D8), each sits ON the surface
# Shells are open at the back: the base edge rests on the surface (offset ACC_BASE), the front face stands ACC_TOP off
# it. Every vertex is placed by a ray onto the real (faceted) body, then checked by sampling (see checks below).
ACC_BASE = 0.0004

def shell(bm, pts_top, pts_base, front_tris, boundary, normals, centre, skip_walls=()):
    """pts_*: Vector lists. front_tris: index triples. boundary: closed index loop. Walls along each boundary edge."""
    T = [bm.verts.new(p) for p in pts_top]; B = [bm.verts.new(p) for p in pts_base]; fo = []
    for a, b, c in front_tris:
        f = bm.faces.new([T[a], T[b], T[c]]); fo.append((f, (normals[a] + normals[b] + normals[c])))
    n = len(boundary)
    for i in range(n):
        a, b = boundary[i], boundary[(i + 1) % n]
        if (a, b) in skip_walls or (b, a) in skip_walls: continue
        f = bm.faces.new([T[a], T[b], B[b], B[a]])
        mid = (pts_top[a] + pts_top[b]) / 2; fo.append((f, mid - centre))
    orient(bm, fo)
    return T

def uv_shell(bm, thc, zc, uv, off_top, front_tris, boundary, skip_walls=()):
    top, base, nrm = [], [], []
    for u, v in uv:
        p, n = surf_uv(thc, zc, u, v, off_top); top.append(p); nrm.append(n)
        base.append(surf_uv(thc, zc, u, v, ACC_BASE)[0])
    mu = sum(u for u, _ in uv) / len(uv); mv = sum(v for _, v in uv) / len(uv)
    c, _ = surf_uv(thc, zc, mu, mv, 0.0)
    shell(bm, top, base, front_tris, boundary, nrm, c, skip_walls)

# -- tie: knot + blade, both split on the front centre line (the body has a vertex ridge there)
TIE_Z = 0.166
bm = bmesh.new()
knot = [(-0.017, 0.012), (0.0, 0.013), (0.017, 0.012), (0.011, -0.012), (0.0, -0.013), (-0.011, -0.012)]
uv_shell(bm, 0.0, TIE_Z, knot, 0.0050, [(0, 1, 4), (0, 4, 5), (1, 2, 3), (1, 3, 4)], [0, 1, 2, 3, 4, 5])
blade = [(-0.011, -0.012), (0.0, -0.013), (0.011, -0.012), (0.022, -0.078), (0.0, -0.098), (-0.022, -0.078)]
uv_shell(bm, 0.0, TIE_Z, blade, 0.0032, [(0, 1, 4), (0, 4, 5), (1, 2, 3), (1, 3, 4)], [0, 1, 2, 3, 4, 5],
         skip_walls=((0, 1), (1, 2)))           # the blade's top edge butts against the knot's bottom wall
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_tie = new_obj('acc_tie', bm, 'acc')

# -- glasses: two hex frames ringing the eye dots + a bridge that follows the centre ridge
GL_RI, GL_RO, GL_OFF = 0.0350, 0.0460, 0.0030
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
        f = bm.faces.new([O[k], O[k1], I[k1], I[k]]); fo.append((f, nr[k]))
        f = bm.faces.new([O[k], O[k1], OB[k1], OB[k]]); fo.append((f, (o_top[k] + o_top[k1]) / 2 - c))
    orient(bm, fo)
# bridge between the inner frame edges, with a vertex on the centre ridge
gap_u = 0.20 * EYE_TH - GL_RO * math.cos(PI / 6) + 0.003   # ends tuck 3 mm under the frames
br = [(-gap_u, 0.004), (0.0, 0.004), (gap_u, 0.004), (gap_u, -0.004), (0.0, -0.004), (-gap_u, -0.004)]
pts = [surf_uv(0.0, EYE_Z, u, v, GL_OFF - 0.0006) for u, v in br]
V = [bm.verts.new(p) for p, _ in pts]; fo = []
for q in ([V[0], V[1], V[4], V[5]], [V[1], V[2], V[3], V[4]]):
    f = bm.faces.new(q); fo.append((f, pts[1][1]))
orient(bm, fo)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_glasses = new_obj('acc_glasses', bm, 'acc')

# -- headset (mono): the band starts on the bare side one ring above the shoulder (budget) and runs over the crown
#    to the ear cup. It is a band over the crown that lies along the body's vertex columns (j=4 and j=12), so it follows the
#    real faceted surface with no chord cutting in; one ear cup on the ghost's left (+X).
HS_W, HS_OFF = 0.0115, 0.0034
bm = bmesh.new()
# the band's stations are the body vertices on the x-z plane above the shoulder (columns j=4 and j=12, and the crown)
col = [v for v in body.data.vertices if abs(v.co.y) < 1e-6 and v.co.z >= SHOULDER - 1e-6]
stations = sorted([v for v in col if v.co.x < -1e-6 and v.co.z > SHOULDER + 0.03], key=lambda v: v.co.z) + [v for v in col if abs(v.co.x) < 1e-6] + \
           sorted([v for v in col if v.co.x > 1e-6], key=lambda v: -v.co.z)
side = Vector((0, 1, 0))
top, base, nr = [], [], []
for v in stations:
    n = v.normal.copy()
    for sg in (-1, 1):
        top.append(v.co + side * sg * HS_W + n * HS_OFF); base.append(v.co + side * sg * HS_W + n * ACC_BASE); nr.append(n)
T = [bm.verts.new(p) for p in top]; B = [bm.verts.new(p) for p in base]; fo = []
for i in range(len(stations) - 1):
    a0, a1, b0, b1 = 2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3
    f = bm.faces.new([T[a0], T[a1], T[b1], T[b0]]); fo.append((f, nr[a0] + nr[b0]))
    for x, y in ((a0, b0), (a1, b1)):
        f = bm.faces.new([T[x], T[y], B[y], B[x]]); fo.append((f, side * (1 if x % 2 else -1)))
f = bm.faces.new([T[0], T[1], B[1], B[0]]); fo.append((f, top[0] - top[2]))   # end wall on the bare side
orient(bm, fo)
# ear cup: hex puck centred under the band end on +X
CUP_R, CUP_OFF, CUP_Z = 0.034, 0.0085, stations[-1].co.z   # centred on the band end, which it hides
cth = math.radians(90)
ct, cb, cn = [], [], []
for k in range(6):
    a = 2 * PI * k / 6 + PI / 2   # pointy top: the top and bottom corners lie on the column ridge
    p, n = surf_uv(cth, CUP_Z, CUP_R * math.cos(a), CUP_R * math.sin(a), CUP_OFF); ct.append(p); cn.append(n)
    cb.append(surf_uv(cth, CUP_Z, CUP_R * math.cos(a), CUP_R * math.sin(a), ACC_BASE)[0])
cc, _ = surf(cth, CUP_Z, 0.0)
shell(bm, ct, cb, [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5)], [0, 1, 2, 3, 4, 5], cn, cc)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_headset = new_obj('acc_headset', bm, 'acc')
for o in (acc_tie, acc_glasses, acc_headset): o.data.polygons.foreach_set('use_smooth', [False] * len(o.data.polygons))

# ================================================================ CHECKS (numbers; the crops are the proof)
def sample_tris(ob, faces_filter=None, n=6):
    me = ob.data; me.calc_loop_triangles(); out = []
    for lt in me.loop_triangles:
        if faces_filter and not faces_filter(me.polygons[lt.polygon_index]): continue
        a, b, c = (me.vertices[i].co for i in lt.vertices)
        for i in range(n + 1):
            for j in range(n + 1 - i):
                k = n - i - j; out.append((a * i + b * j + c * k) / n)
    return out
def rng(vals): return [round(min(vals) * 1000, 2), round(max(vals) * 1000, 2)]
checks = {}
checks['eyes_offset_mm_min_max (must be > 0, sits on surface)'] = rng([sdist(p) for p in sample_tris(eyes)])
def is_front(poly, o):
    c = poly.center; _, n = surf_near(c); return poly.normal.dot(n) > 0.6
def surf_near(p):
    loc, nrm, _, _ = TREE.find_nearest(p); return loc, nrm
for o in (acc_tie, acc_glasses, acc_headset):
    checks[o.name + '_front_faces_offset_mm_min_max (visible faces, must be > 0)'] = rng([sdist(p) for p in sample_tris(o, lambda pl: is_front(pl, o))])
    checks[o.name + '_wall_faces_offset_mm_min_max (base edge may sink: hidden contact line)'] = rng([sdist(p) for p in sample_tris(o, lambda pl: not is_front(pl, o))])
    allp = [sdist(p) for p in sample_tris(o)]
    vb = [sdist(v.co) for v in o.data.vertices]
    checks[o.name + '_all_faces_offset_mm_min_max (must be >= -0.5)'] = rng(allp)
    checks[o.name + '_vertex_offset_mm_min_max'] = rng(vb)
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]
    base = [v.co for v in o.data.vertices][:ARM_N]
    checks[nm + '_base_ring_depth_mm (must be < 0: base hidden in body)'] = rng([sdist(p) for p in base])
    # wave extremes (Emil: arm swings +/-20 deg): base ring must stay inside the body
    worst = -1
    for axis in (Vector((0, 0, 1)), ax.cross(Vector((0, 0, 1))).normalized()):
        for ang in (-20, 20):
            R = Matrix.Rotation(math.radians(ang), 3, axis)
            worst = max(worst, max(sdist(piv + R @ (p - piv)) for p in base))
    checks[nm + '_base_ring_worst_mm_at_wave_+-20deg (must be < 0)'] = round(worst * 1000, 2)
# arm vs ear cup clearance
cup_pts = [v.co for v in acc_headset.data.vertices]
checks['earcup_to_armL_min_gap_mm'] = round(min((p - q).length for p in cup_pts for q in [v.co for v in arms['arm_L'].data.vertices]) * 1000, 1)
checks['hem_thickness_mm'] = HEM_T * 1000
checks['hem_scallops'] = 4
checks['hem_notch_depth_mm'] = (HEM[2][0] - HEM[0][0]) * 1000
# eye dots inside the glasses frames (no overlap)
checks['eye_to_glasses_inner_edge_min_gap_mm'] = round((GL_RI * math.cos(PI / 6) - EYE_RZ) * 1000, 1)

# ================================================================ RIG + EXPORT
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root; flt.location = (0, 0, FLOAT)
for o in [body, eyes, acc_tie, acc_glasses, acc_headset]: o.parent = flt
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]; o.data.transform(Matrix.Translation(-piv)); o.location = piv; o.parent = flt
    o['pivot_axis_blender'] = list(ax)
for nm in ('acc_tie', 'acc_glasses', 'acc_headset'): bpy.data.objects[nm]['variant'] = nm[4:]
for o in (acc_tie, acc_glasses, acc_headset): o['default_visible'] = (o is acc_tie)
flt['float_rest_m'] = FLOAT
flt['motion'] = 'Emil: y +/-0.06 m 2.4 s, x +/-0.03 m 3.7 s, yaw +/-8 deg 5.1 s (animate float.position / root yaw)'

bpy.context.view_layer.update()
counts = {o.name: tris(o) for o in [body, eyes, arms['arm_L'], arms['arm_R'], acc_tie, acc_glasses, acc_headset]}
base_t = counts['body'] + counts['eyes'] + counts['arm_L'] + counts['arm_R']
counts['base_body_eyes_arms'] = base_t
counts['variant_totals'] = {v: base_t + counts['acc_' + v] for v in ('tie', 'glasses', 'headset')}
report = {'triangles': counts, 'checks': checks, 'size': {'body_height_m': HB, 'float_m': FLOAT, 'crown_m': FLOAT + CROWN,
          'hem_width_m': round(2 * HEM[0][1], 3), 'kit_height_m': 0.977}, 'ghost_toon': GHOST_TOON}
print('GHOST_REPORT', json.dumps(report, indent=1))
json.dump(report, open(os.path.join(HERE, 'build_report.json'), 'w'), indent=1)
json.dump(GHOST_TOON, open(os.path.join(HERE, 'ghost_toon.json'), 'w'), indent=1)

bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, body, eyes, acc_tie, acc_glasses, acc_headset] + list(arms.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, 'ghostie.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=True, export_extras=True, export_materials='EXPORT',
                          export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'ghostie.blend'))
print('GHOST_DONE')
