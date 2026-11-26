# GHOSTED - the Ghostie (ghost recruiter NPC), v3. Builds it from an empty scene, exports ghostie.glb, saves ghostie.blend.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_ghostie.py
# Units: metres. Blender is Z-up and the ghost faces -Y; the glTF export is Y-up (the ghost faces +Z in three.js).
# Nodes: root > float > body, arm_L, arm_R (the 3 non-swap meshes, V5), eyes, acc_tie, acc_glasses, acc_headset (swap parts).
# Budget (checklist V5, chair amendment 3): body + eyes + arms + one accessory <= 600 visible triangles.
# v3 = acceptance/ghostie/fix-brief-v3.md (see changes.md). v1 and v2 are archived in v1/ and v2/.
import bpy, bmesh, math, json, os
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi

PAL = {
    'ghost': '#F8F4EA',   # Lena #16 ghost
    'acc':   '#C8C0D8',   # Lena #27 ghost-faded (glasses, headset)
    'tie':   '#C9A6D6',   # Lena #10 hq-wall (tie; chair ruling v3 keeps it)
    'ink':   '#2B1E16',   # Lena #22 ink
}
GHOST_TOON = {
    'band_colors': {k: [[-1.0, [178, 178, 178]], [0.0001, [255, 255, 255]]] for k in ('ghost', 'acc', 'tie')},
    'basic_materials': ['ink'],
    'outline_nodes': ['body', 'arm_L', 'arm_R'],
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

HB = 0.47; FLOAT = 0.22
GHOST_TOON['float_rest_m'] = FLOAT
SEG = 12
def dirv(th): return Vector((math.sin(th), -math.cos(th), 0))   # th 0 = front (-Y), +90 = +X (ghost's left)

# ================================================================ BODY (fix 3, fix 4)
# A lathe's side outline is always a vertex column, i.e. the profile (x cos <= 15 deg), so 12 columns cost no outline
# corners; the triangles go to the profile: 9 dome rings every 10 deg of the elliptic dome (v2: 6 rings, 15 deg).
CROWN = 0.470; SHOULDER = 0.310; DOME_R = 0.190
DOME = [(SHOULDER + (CROWN - SHOULDER) * math.cos(math.radians(f)), DOME_R * math.sin(math.radians(f))) for f in (10, 20, 30, 40, 50, 60, 70, 90)]   # 80 dropped: the dome is flattest there (curvature b/a^2 < a/b^2)
SKIRT = [(0.205, 0.197), (0.085, 0.213)]   # s2 bows out, the hem tucks back in under it: the bottom corner curls instead of ending in a point
PROFILE = DOME + SKIRT
# Hem: 5 scallops x 12 vertices (60). The notch top has 5 vertices on a curve (v2: 2 with a flat top). With 5 lobes (one at
# the front) the 2 front notches sit at +-36 deg and the side outline at +-90 falls on a rising flank, not on a lobe tip,
# so the outer corners turn up instead of ending in a point. Lobes do not flare (lobe radius = skirt radius).
HEM_N = 60; HEM_A = 0.034; HEM_R0, HEM_R1 = 0.199, 0.193
def hem_zr(th):
    w = (1 - math.cos(5 * th)) / 2          # v4: plain cosine, so the notch apex is as round as the lobe (v3: ** 1.6 peaked it)
    return HEM_A * w, HEM_R0 + (HEM_R1 - HEM_R0) * w
HEM_T = 0.016; HEM_LIFT = 0.006; CAVITY = 0.205

def band(bm, a, b):
    if len(a) > len(b): flip = True; a, b = b, a
    else: flip = False
    na, nb = len(a), len(b); k = nb // na
    for i in range(na):
        i1 = (i + 1) % na
        for m in range(k):
            f = [a[i], b[(k * i + m) % nb], b[(k * i + m + 1) % nb]]; bm.faces.new(f[::-1] if flip else f)
        f = [a[i], b[(k * i + k) % nb], a[i1]]; bm.faces.new(f[::-1] if flip else f)

bm = bmesh.new()
crown = bm.verts.new((0, 0, CROWN))
rings = [[bm.verts.new(dirv(2 * PI * j / SEG) * r + Vector((0, 0, z))) for j in range(SEG)] for z, r in PROFILE]
hem = []
for j in range(HEM_N):
    th = 2 * PI * j / HEM_N; z, r = hem_zr(th); hem.append(bm.verts.new(dirv(th) * r + Vector((0, 0, z))))
inner = []   # v4: no rim ring; the hidden cavity is one fan from the hem to the cavity pole (24 triangles moved to the arms)
cav = bm.verts.new((0, 0, CAVITY))
for i in range(SEG): bm.faces.new([crown, rings[0][i], rings[0][(i + 1) % SEG]])
for ra, rb in zip(rings[:-1], rings[1:]): band(bm, ra, rb)
band(bm, rings[-1], hem)
for i in range(HEM_N): bm.faces.new([hem[i], cav, hem[(i + 1) % HEM_N]])
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
hs, ins = set(hem), set(inner)
for e in bm.edges:
    v0, v1 = e.verts
    if (v0 in hs and v1 in hs) or (v0 in ins and v1 in ins): e.smooth = False
body = new_obj('body', bm, 'ghost')
body_bm = bmesh.new(); body_bm.from_mesh(body.data); body_bm.normal_update()
TREE = BVHTree.FromBMesh(body_bm)

def sdist(p):
    loc, nrm, _, d = TREE.find_nearest(p); return d if (p - loc).dot(nrm) >= 0 else -d
def surf(th, z, off):
    d = dirv(th); loc, nrm, _, _ = TREE.ray_cast(d * 1.0 + Vector((0, 0, z)), -d); return loc + nrm * off, nrm
def surf_near(p):
    loc, nrm, _, _ = TREE.find_nearest(p); return loc, nrm
def surf_uv(thc, zc, u, v, off, r_ref=0.20): return surf(thc + u / r_ref, zc + v, off)
def orient(bm, faces_out):
    for f, w in faces_out:
        f.normal_update()
        if f.normal.dot(w) < 0: f.normal_flip()

# ================================================================ EYES (fix 6): 12-sided dots on the face midlines
# +-15 deg is the centre of the flat face between columns 0 and +-1, so the dot and the 8-sided glasses frame lie on one
# flat face (no crease) and the eyes sit 10.7 deg further in than v2 (25.7 deg).
EYE_TH = math.radians(15.0); EYE_Z = 0.305;   # v4: +0.047 m (10% of body height) so the arms sit below them on screen at 26 m
_ = 0; EYE_RX = 0.0185; EYE_RZ = 0.0275; EYE_N = 12
bm = bmesh.new(); fo = []
for s in (-1, 1):
    c, cn = surf(s * EYE_TH, EYE_Z, 0.0022); cv = bm.verts.new(c)
    rim = [bm.verts.new(surf_uv(s * EYE_TH, EYE_Z, EYE_RX * math.cos(2 * PI * k / EYE_N), EYE_RZ * math.sin(2 * PI * k / EYE_N), 0.0012)[0]) for k in range(EYE_N)]
    for k in range(EYE_N):
        f = bm.faces.new([cv, rim[k], rim[(k + 1) % EYE_N]]); fo.append((f, cn))
orient(bm, fo)
eyes = new_obj('eyes', bm, 'ink')

# ================================================================ ARMS (fix 1): flat tapered flaps with a round tip
# Thin front-to-back (14 mm), wide in the droop plane (72 mm at the root -> 0 at a round tip). They droop 30 deg in the
# geometry, the root is low (z 0.120, v2 0.160) and they point 15 deg back. No collar: the flap's faces meet the body
# directly, so there is no extra part at the join.
ARM_N = 6
ARM_TH = math.radians(80); ARM_Z = 0.095   # v4: 10 deg forward of the side, so the tips also sit lower on the top-down screen
# v4: a curved spine. The flap leaves the body at 20 deg droop and bends to 62 deg at the tip, so the tip hangs down and out
# (below the eyes on screen at 26 m). The profile closes over 4 rings into a pole, so the tip is round, not a wedge.
DROOP0, DROOP1 = 24, 76
BACK = {'arm_L': 0, 'arm_R': 0}   # v4: no back sweep. A swept flap ran along the body and left an ink spur (v3 variants);
# a flap that leaves along the surface normal departs at once, and its tip sits lower on screen at the 26 m camera.
ARM_PROF = [(-0.058, 0.022, 0.008), (0.000, 0.026, 0.009), (0.026, 0.029, 0.009), (0.048, 0.025, 0.008), (0.064, 0.015, 0.006), (0.074, 0.0, 0.0)]
#            t along spine, half-width (droop plane), half-thickness
DROOP = DROOP0
arms = {}; arm_pivots = {}
for s_, nm in ((1, 'arm_L'), (-1, 'arm_R')):
    out = dirv(s_ * ARM_TH)
    def dir_at(t):
        dr = math.radians(DROOP0 + (DROOP1 - DROOP0) * max(0.0, t / 0.074) ** 1.5)
        d = out * math.cos(dr) + Vector((0, 0, -math.sin(dr)))
        return (Quaternion(Vector((0, 0, 1)), math.radians(BACK[nm]) * s_) @ d).normalized()
    piv, _ = surf(s_ * ARM_TH, ARM_Z, 0.0)
    fwd = Vector((0, -1, 0)); d0 = dir_at(0.0)
    # spine: integrate the bending direction from the pivot (root ring goes straight back along d0)
    pts = {}; p = piv.copy(); tprev = 0.0
    for t, _, _ in ARM_PROF:
        if t <= 0: pts[t] = piv + d0 * t; continue
        steps = 8
        for k in range(steps):
            ta = tprev + (t - tprev) * k / steps; tb = tprev + (t - tprev) * (k + 1) / steps
            p = p + dir_at((ta + tb) / 2) * (tb - ta)
        pts[t] = p.copy(); tprev = t
    bm = bmesh.new(); rr = []
    for t, hw, ht in ARM_PROF:
        d = dir_at(max(t, 0.0)); ew = d.cross(fwd).normalized(); et = d.cross(ew).normalized()
        c = pts[t]
        if hw == 0: rr.append([bm.verts.new(c)]); continue
        rr.append([bm.verts.new(c + ew * (hw * math.cos(2 * PI * k / ARM_N)) + et * (ht * math.sin(2 * PI * k / ARM_N))) for k in range(ARM_N)])
    fo = []
    for ri in range(len(rr) - 1):
        a_, b_ = rr[ri], rr[ri + 1]
        ca = sum((v.co for v in a_), Vector()) / len(a_); cb_ = sum((v.co for v in b_), Vector()) / len(b_)
        for k in range(ARM_N):
            k1 = (k + 1) % ARM_N
            q = [a_[k], a_[k1], b_[0]] if len(b_) == 1 else [a_[k], a_[k1], b_[k1], b_[k]]
            f = bm.faces.new(q); cen = f.calc_center_median()
            fo.append((f, cen - (ca + cb_) / 2 + ((cb_ - ca).normalized() * 0.01 if len(b_) == 1 else Vector())))
    orient(bm, fo)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
    arms[nm] = new_obj(nm, bm, 'ghost'); arm_pivots[nm] = (piv, d0)
    arm_pivots[nm + '_tip'] = pts[ARM_PROF[-1][0]]

# ================================================================ ACCESSORIES
# -- tie (v4 fix 4): the right way round. A small knot sits low on the front, off-centre at +46 deg (z 0.165, below the eye
#    line). The blade climbs over the left shoulder and widens (14 -> 34 mm), crossing the column ridges at 60 and 90 deg
#    as stations (no chord cuts in). Past the shoulder it lifts off the body and ends in a wide pointed tip in the air:
#    the "blown by a fast exit" joke, and the tie silhouette. Ink: the blade's side walls are ink and an ink plate 1.6 mm
#    wider lies under the surface part, so the long sides carry a dark edge from every angle.
TIE_SURF = [(44, 0.170, 0.012), (50, 0.200, 0.020), (56, 0.232, 0.028), (60, 0.252, 0.033), (66, 0.285, 0.040), (73, 0.322, 0.047), (80, 0.352, 0.053)]
ST = [(math.radians(a), z, w) for a, z, w in TIE_SURF]
def tie_geometry(bm):
    cs = [surf(th, z, 0.0) for th, z, _ in ST]
    C = [c for c, _ in cs]; N = [n for _, n in cs]; W = [w for _, _, w in ST]
    # lifted part: continue along the last tangent, rising off the body along the normal
    tan = (C[-1] - C[-2]).normalized(); nl = N[-1]
    # flying part: up and out past the shoulder, its face turned to the front (normal ~ -Y) so the wide tip reads in the
    # front and 3/4 views (v4 first run: it lay in the body's tangent plane and was seen edge-on)
    up_out = (tan * 0.6 + nl * 0.8).normalized()
    C += [C[-1] + up_out * 0.020, C[-1] + up_out * 0.042]
    fn = Vector((0, -1, 0)); fn = (fn - up_out * fn.dot(up_out)).normalized()
    N += [fn, fn]; W += [0.058, 0.058]
    lifted = [False] * len(ST) + [True, True]
    tip = C[-1] + up_out * 0.040; nl = fn; tan = up_out
    TOP, BOT = 0.0085, 0.0058
    T, B, Pp = [], [], []
    for i in range(len(C)):
        tn = (C[min(i + 1, len(C) - 1)] - C[max(i - 1, 0)]).normalized(); lat = N[i].cross(tn).normalized()
        row_t, row_b, row_p = [], [], []
        for sg in (-1, 1):
            if lifted[i]:
                q = C[i] + lat * sg * W[i] / 2; row_t.append(q + N[i] * 0.003); row_b.append(q - N[i] * 0.003)
            else:
                q, qn = surf_near(C[i] + lat * sg * W[i] / 2); row_t.append(q + qn * TOP); row_b.append(q + qn * BOT)
                qp, qpn = surf_near(C[i] + lat * sg * (W[i] / 2 + 0.0016)); row_p.append(qp + qpn * 0.0050)
        T.append([bm.verts.new(x) for x in row_t]); B.append([bm.verts.new(x) for x in row_b]); Pp.append([bm.verts.new(x) for x in row_p])
    TT = bm.verts.new(tip + nl * 0.003); TB = bm.verts.new(tip - nl * 0.003)
    fo = []
    def face(vs, mi, want):
        f = bm.faces.new(vs); f.material_index = mi; fo.append((f, want)); return f
    for i in range(len(C) - 1):
        nrm = N[i] + N[i + 1]; tn = (C[i + 1] - C[i]).normalized(); lat = N[i].cross(tn).normalized()
        face([T[i][0], T[i][1], T[i + 1][1], T[i + 1][0]], 0, nrm)
        face([T[i][0], T[i + 1][0], B[i + 1][0], B[i][0]], 1, -lat)       # ink side walls (the long sides)
        face([T[i][1], T[i + 1][1], B[i + 1][1], B[i][1]], 1, lat)
        if lifted[i] or lifted[i + 1]:
            face([B[i][0], B[i][1], B[i + 1][1], B[i + 1][0]], 0, -nrm)   # underside of the flying part
        if Pp[i] and Pp[i + 1]:
            face([Pp[i][0], Pp[i][1], Pp[i + 1][1], Pp[i + 1][0]], 1, nrm)  # ink plate under the surface part
    face([T[-1][0], T[-1][1], TT], 0, nl); face([B[-1][0], B[-1][1], TB], 0, -nl)
    lat = nl.cross(tan).normalized()
    face([T[-1][0], TT, TB, B[-1][0]], 1, -lat); face([T[-1][1], TT, TB, B[-1][1]], 1, lat)
    # knot: a small trapezoid block over the blade start (ink walls, tie top)
    c0, n0 = cs[0]; tn0 = (C[1] - C[0]).normalized(); lat0 = n0.cross(tn0).normalized()
    kc = [(c0 - tn0 * 0.020, 0.024), (c0 - tn0 * 0.004, 0.034), (c0 + tn0 * 0.014, 0.020)]   # knot: a 34 mm wide, 34 mm tall block
    KT, KB = [], []
    for c, w in kc:
        rt, rb = [], []
        for sg in (-1, 1):
            q, qn = surf_near(c + lat0 * sg * w / 2); rt.append(bm.verts.new(q + qn * 0.0115)); rb.append(bm.verts.new(q + qn * 0.0040))
        KT.append(rt); KB.append(rb)
    for r in range(len(KT) - 1):
        face([KT[r][0], KT[r][1], KT[r + 1][1], KT[r + 1][0]], 0, n0)
        face([KT[r][0], KT[r + 1][0], KB[r + 1][0], KB[r][0]], 1, -lat0); face([KT[r][1], KT[r + 1][1], KB[r + 1][1], KB[r][1]], 1, lat0)
    face([KT[0][0], KT[0][1], KB[0][1], KB[0][0]], 1, -tn0); face([KT[-1][0], KT[-1][1], KB[-1][1], KB[-1][0]], 1, tn0)
    orient(bm, fo)
    return tip
bm = bmesh.new()
TIE_TIP = tie_geometry(bm)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_tie = new_obj('acc_tie', bm, 'tie'); acc_tie.data.materials.append(mat('ink'))

# -- glasses (fix 5): 8-sided frames on the flat eye faces + a bridge with a vertex on the front ridge (column 0)
GL_RI, GL_RO, GL_OFF, GL_N = 0.0340, 0.0450, 0.0015, 8
bm = bmesh.new()
for s in (-1, 1):
    thc = s * EYE_TH; O, I, nr = [], [], []
    for k in range(GL_N):
        a = 2 * PI * k / GL_N + PI / GL_N
        p, n = surf_uv(thc, EYE_Z, GL_RO * math.cos(a), GL_RO * math.sin(a), GL_OFF); O.append(bm.verts.new(p)); nr.append(n)
        I.append(bm.verts.new(surf_uv(thc, EYE_Z, GL_RI * math.cos(a), GL_RI * math.sin(a), GL_OFF)[0]))
    fo = []
    for k in range(GL_N):
        k1 = (k + 1) % GL_N; f = bm.faces.new([O[k], O[k1], I[k1], I[k]]); fo.append((f, nr[k]))
    orient(bm, fo)
gap_u = 0.20 * EYE_TH - GL_RO * math.cos(PI / GL_N) + 0.003
br = [(-gap_u, 0.004), (0.0, 0.004), (gap_u, 0.004), (gap_u, -0.004), (0.0, -0.004), (-gap_u, -0.004)]
pts = [surf_uv(0.0, EYE_Z, u, v, GL_OFF - 0.0003) for u, v in br]
V = [bm.verts.new(p) for p, _ in pts]; fo = []
for q in ([V[0], V[1], V[4], V[5]], [V[1], V[2], V[3], V[4]]):
    f = bm.faces.new(q); fo.append((f, pts[1][1]))
orient(bm, fo)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) == 4])
acc_glasses = new_obj('acc_glasses', bm, 'acc')

# -- headset (fix 5): band 0.6 mm on the vertex columns at +-90 deg (j=3, j=9; flat faces, no chord cuts in) and a round
#    12-sided ear cup with its own closed ink hull.
HS_W, HS_OFF = 0.0120, 0.0006
bm = bmesh.new()
colv = [v for v in body.data.vertices if abs(v.co.y) < 1e-6 and v.co.z >= SHOULDER - 1e-6]
stations = sorted([v for v in colv if v.co.x < -1e-6 and v.co.z > SHOULDER + 0.03], key=lambda v: v.co.z) + \
           [v for v in colv if abs(v.co.x) < 1e-6] + sorted([v for v in colv if v.co.x > 1e-6], key=lambda v: -v.co.z)
side = Vector((0, 1, 0)); T = []; fo = []
for v in stations:
    for sg in (-1, 1): T.append(bm.verts.new(v.co + side * sg * HS_W + v.normal * HS_OFF))
for i in range(len(stations) - 1):
    f = bm.faces.new([T[2 * i], T[2 * i + 1], T[2 * i + 3], T[2 * i + 2]]); fo.append((f, stations[i].normal + stations[i + 1].normal))
orient(bm, fo)
acc_headset_band = new_obj('acc_headset_band', bm, 'acc')   # own child node: no ink hull (its hull drew a 2nd crown line)
bm = bmesh.new()
CUP_R, CUP_OFF, CUP_N = 0.040, 0.0080, 12
CUP_Z = stations[-1].co.z; cth = math.radians(90)
# the cup top is a flat disc (a fan over a curved patch sagged 11 mm in the first v3 run); the walls take up the curve
cc, ncup = surf(cth, CUP_Z, 0.0)
basep = [surf_uv(cth, CUP_Z, CUP_R * math.cos(2 * PI * k / CUP_N), CUP_R * math.sin(2 * PI * k / CUP_N), 0.0004)[0] for k in range(CUP_N)]
H = max((p - cc).dot(ncup) for p in basep) + CUP_OFF
cb = [bm.verts.new(p) for p in basep]
ct = [bm.verts.new(p + ncup * (H - (p - cc).dot(ncup))) for p in basep]
cn = [ncup] * CUP_N; fo = []
f = bm.faces.new(ct); fo.append((f, cn[0] + cn[CUP_N // 2]))
# v4 fix 5: one ink stroke - an annulus on the cup's top edge (r -3 mm .. +1.2 mm, 0.4 mm above the flat top). The cup has
# no inverted hull any more, so there is no second, offset stroke and no pale sliver between two strokes.
PO = [bm.verts.new(ct[k].co + ncup * 0.0004 + (ct[k].co - (cc + ncup * H)).normalized() * 0.0012) for k in range(CUP_N)]
PI_ = [bm.verts.new(ct[k].co + ncup * 0.0004 - (ct[k].co - (cc + ncup * H)).normalized() * 0.0030) for k in range(CUP_N)]
for k in range(CUP_N):
    k1 = (k + 1) % CUP_N; f = bm.faces.new([PI_[k], PI_[k1], PO[k1], PO[k]]); f.material_index = 1; fo.append((f, ncup))
for k in range(CUP_N):
    k1 = (k + 1) % CUP_N
    f = bm.faces.new([ct[k], ct[k1], cb[k1], cb[k]]); fo.append((f, (ct[k].co + ct[k1].co) / 2 - cc))
orient(bm, fo)
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) >= 4])
acc_headset = new_obj('acc_headset', bm, 'acc'); acc_headset.data.materials.append(mat('ink'))
for o in (acc_tie, acc_glasses, acc_headset, acc_headset_band): o.data.polygons.foreach_set('use_smooth', [False] * len(o.data.polygons))

# ================================================================ REST POSE (Emil; fix-brief-v3: roll flipped)
def rot_about(axis, deg): return Quaternion(axis.normalized(), math.radians(deg))
ARM_REST = {}
for nm, (up, fwd) in {'arm_L': (6, 0), 'arm_R': (-3, 8)}.items():
    piv, ax = arm_pivots[nm]; h = ax.cross(Vector((0, 0, 1))).normalized()
    q = rot_about(h, up)
    if ((q @ ax).z - ax.z) * up < 0: q = rot_about(h, -up)
    if fwd:
        qf = rot_about(Vector((0, 0, 1)), fwd)
        if (qf @ (q @ ax)).y > (q @ ax).y: qf = rot_about(Vector((0, 0, 1)), -fwd)
        q = qf @ q
    ARM_REST[nm] = q
FLOAT_LEAN, FLOAT_ROLL_BLENDER_Y = 3.0, -5.0     # Blender -Y = three.js +Z: +5 deg roll on three z lifts the arm_L side

# ================================================================ CHECKS
def sample_tris(ob, faces_filter=None, n=6):
    me = ob.data; me.calc_loop_triangles(); out = []
    for lt in me.loop_triangles:
        if faces_filter and not faces_filter(me.polygons[lt.polygon_index]): continue
        a, b, c = (me.vertices[i].co for i in lt.vertices)
        for i in range(n + 1):
            for j in range(n + 1 - i):
                k = n - i - j; out.append((a * i + b * j + c * k) / n)
    return out
def rng(v): return [round(min(v) * 1000, 2), round(max(v) * 1000, 2)]
def is_front(poly):
    """A visible top face: every corner stands > 1 mm off the body (walls and bases touch it)."""
    return min(sdist(poly.id_data.vertices[i].co) for i in poly.vertices) > 0.001
checks = {}
for o in (acc_tie, acc_headset, acc_headset_band):
    me = o.data; worst = min(((sdist(p), tuple(round(x, 3) for x in p)) for p in sample_tris(o, is_front)), key=lambda t: t[0])
    print('WORST', o.name, worst)
checks['eyes_offset_mm (must be > 0)'] = rng([sdist(p) for p in sample_tris(eyes)])
for o in (acc_tie, acc_glasses, acc_headset, acc_headset_band):
    checks[o.name + '_front_faces_offset_mm (visible, must be > 0)'] = rng([sdist(p) for p in sample_tris(o, is_front)])
    checks[o.name + '_all_faces_offset_mm'] = rng([sdist(p) for p in sample_tris(o)])
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]; Rq = ARM_REST[nm].to_matrix()
    base = [piv + Rq @ (v.co - piv) for v in list(o.data.vertices)[:ARM_N]]
    checks[nm + '_root_ring_depth_mm_at_rest (must be < 0)'] = rng([sdist(p) for p in base])
    worst = -1
    for axis in (Vector((0, 0, 1)), ax.cross(Vector((0, 0, 1))).normalized()):
        for ang in (-20, 20):
            R = Matrix.Rotation(math.radians(ang), 3, axis) @ Rq
            worst = max(worst, max(sdist(piv + R @ (v.co - piv)) for v in list(o.data.vertices)[:ARM_N]))
    checks[nm + '_root_ring_worst_mm_at_rest_+-20deg (must be < 0)'] = round(worst * 1000, 2)
    tipz = max((piv + Rq @ (v.co - piv)).z for v in o.data.vertices)
    checks[nm + '_highest_point_z_m (below eye line 0.258-0.0275)'] = round(tipz, 3)
checks['hem_notch_top_curve_heights_pct (5 vertices, centre = notch)'] = [round(100 * hem_zr(2 * PI * j / HEM_N)[0] / HEM_A) for j in (4, 5, 6, 7, 8)]
checks['hem_scallops'] = 5
checks['hem_lobe_radius_vs_skirt_m'] = [HEM_R0, SKIRT[-1][1]]
checks['eye_to_glasses_inner_edge_min_gap_mm'] = round((GL_RI * math.cos(PI / GL_N) - EYE_RZ) * 1000, 1)
checks['tie_knot_theta_deg_z'] = [round(math.degrees(ST[0][0]), 1), ST[0][1]]
checks['tie_tip_air_gap_mm (tip off the body)'] = round(sdist(TIE_TIP) * 1000, 1)
checks['arm_tip_z_m (rest geometry)'] = {nm: round(arm_pivots[nm + '_tip'].z, 3) for nm in ('arm_L', 'arm_R')}

# ================================================================ RIG + EXPORT
root = bpy.data.objects.new('root', None); COL.objects.link(root)
flt = bpy.data.objects.new('float', None); COL.objects.link(flt); flt.parent = root; flt.location = (0, 0, FLOAT)
flt.rotation_mode = 'XYZ'; flt.rotation_euler = (math.radians(FLOAT_LEAN), math.radians(FLOAT_ROLL_BLENDER_Y), 0)
for o in [body, eyes, acc_tie, acc_glasses, acc_headset]: o.parent = flt
acc_headset_band.parent = acc_headset
for nm, o in arms.items():
    piv, ax = arm_pivots[nm]; o.data.transform(Matrix.Translation(-piv)); o.location = piv; o.parent = flt
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = ARM_REST[nm]; o['pivot_axis_blender'] = list(ax)
for o in (acc_tie, acc_glasses, acc_headset): o['variant'] = o.name[4:]; o['default_visible'] = (o is acc_tie)
flt['float_rest_m'] = FLOAT
flt['motion'] = 'Emil: y +/-0.06 m 2.4 s, x +/-0.03 m 3.7 s, yaw +/-8 deg 5.1 s; compose yaw on the rest lean/roll'

bpy.context.view_layer.update()
counts = {o.name: tris(o) for o in [body, eyes, arms['arm_L'], arms['arm_R'], acc_tie, acc_glasses, acc_headset]}
counts['acc_headset'] += tris(acc_headset_band); counts['acc_headset_note'] = 'cup + ink ring + band (child node acc_headset_band)'
base_t = counts['body'] + counts['eyes'] + counts['arm_L'] + counts['arm_R']
counts['base_body_eyes_arms'] = base_t
counts['variant_totals'] = {v: base_t + counts['acc_' + v] for v in ('tie', 'glasses', 'headset')}
meshes = [o.name for o in bpy.data.objects if o.type == 'MESH']
report = {'triangles': counts, 'meshes': {'all': meshes, 'non_swap (V5 <= 3)': ['body', 'arm_L', 'arm_R'],
          'swap_parts': ['eyes', 'acc_tie', 'acc_glasses', 'acc_headset (+ child acc_headset_band)']}, 'checks': checks,
          'rest_pose': {'float_lean_deg_x': FLOAT_LEAN, 'float_roll_deg_three_z': -FLOAT_ROLL_BLENDER_Y, 'arm_droop_geometry_deg': DROOP,
                        'arm_L_up_deg': 6, 'arm_R_down_deg': 3, 'arm_R_forward_deg': 8, 'arm_back_deg': BACK},
          'ghost_toon': GHOST_TOON}
print('GHOST_REPORT', json.dumps(counts))
json.dump(report, open(os.path.join(HERE, 'build_report.json'), 'w'), indent=1)
json.dump(GHOST_TOON, open(os.path.join(HERE, 'ghost_toon.json'), 'w'), indent=1)
bpy.ops.object.select_all(action='DESELECT')
for o in [root, flt, body, eyes, acc_tie, acc_glasses, acc_headset, acc_headset_band] + list(arms.values()): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, 'ghostie.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=True, export_extras=True, export_materials='EXPORT',
                          export_cameras=False, export_lights=False, export_animations=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'ghostie.blend'))
print('GHOST_DONE')
