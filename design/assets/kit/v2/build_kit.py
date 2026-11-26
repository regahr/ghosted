# GHOSTED - Kit, the hero. Builds Kit from an empty scene, exports kit.glb and saves kit.blend.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P build_kit.py
# Units: metres. Blender is Z-up, Kit faces -Y; the glTF export is Y-up (Kit faces +Z in three.js).
# Rig (Emil): root > bounce (pivot at feet) > body > head > face_<expr>, sprout; body > briefcase.
import bpy, bmesh, math, json, os
from mathutils import Vector, Matrix, Quaternion, Euler
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
PI = math.pi

# ---------------------------------------------------------------- palette (sRGB hex)
PAL = {
    'shirt': '#2F6FDB', 'skin': '#F2C79E', 'hair': '#4A3226', 'tie': '#E0533D', 'legs': '#2F3E5C',
    'wood': '#7A4A2E',      # shoes + briefcase (Lena #5 wood)
    'panel': '#FFF8EE',     # collar, badge card (Lena #23)
    'gold': '#F0B43C',      # lanyard, clasps (Lena #13)
    'ink': '#2B1E16',       # eyes, brows, mouth, outline (Lena #22)
    'white': '#FFF8EE',     # eye highlights (panel)
    'cheek': '#F4A672',     # cheeks (Lena #6 cafe-wall)
    'tongue': '#D4503A',    # tongue (Lena #7 cafe-roof)
    'sweat': '#A8C4DC',     # sweat drop (Lena #8 ats-wall)
}
# Toon spec shared with ingame.html (written to toon.json). Terminators sit on texel edges of a 32-texel
# gradient map so three.js MeshToonMaterial and the Blender ramp switch at exactly the same N.L.
TOON = {
    'texels': 32,
    'bands2': [[-1.0, 178], [0.125, 255]],               # props: shadow below N.L 0.125
    'bands3': [[-1.0, 178], [0.0625, 217], [0.5, 255]],   # skin: shadow / mid / lit
    'skin_materials': ['skin'],
    'basic_materials': ['ink', 'white', 'cheek', 'tongue', 'sweat'],   # flat, unlit face parts
    # light = design/render.html charStage: lights(scene, 1, '#fff6e8', '#e9c49a', 3, 25)
    'sun': {'color': '#fff3dc', 'intensity': 2.6, 'elev': 62, 'az': 25},
    'hemi': {'sky': '#fff6e8', 'ground': '#e9c49a', 'intensity': 0.9},
    'ambient': {'color': '#ffffff', 'intensity': 0.25},
    'outline': {'color': '#2B1E16', 'width_m': 0.007},
    'contact_shadow': {'color': '#2B1E16', 'opacity': 0.25, 'rx': 0.26, 'ry': 0.21},
    'tone_mapping': 'Neutral', 'exposure': 1.0,
}

def s2l(h):
    h = h.lstrip('#'); out = []
    for i in (0, 2, 4):
        c = int(h[i:i+2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out

# ---------------------------------------------------------------- scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.preferences.filepaths.save_version = 0
scn = bpy.context.scene
COL = scn.collection

MATS = {}
def mat(name):
    """Export material: Principled BSDF base colour only (the game applies toon). render_kit.py swaps the
    node tree for the Blender toon shader."""
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*s2l(PAL[name]), 1)
    b.inputs['Roughness'].default_value = 0.8
    m['hex'] = PAL[name]
    MATS[name] = m; return m

def new_obj(name, bm, mats, smooth=True, sharp_angle=None):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(mat(m))
    for p in me.polygons: p.use_smooth = smooth
    if sharp_angle is not None: me.set_sharp_from_angle(angle=math.radians(sharp_angle))
    ob = bpy.data.objects.new(name, me); COL.objects.link(ob); return ob

# ---------------------------------------------------------------- geometry helpers
def frame_from_z(z):
    z = Vector(z).normalized()
    x = Vector((1, 0, 0)) if abs(z.x) < 0.9 else Vector((0, 1, 0))
    x = (x - z * x.dot(z)).normalized(); y = z.cross(x); return x, y, z

def ring_faces(bm, rings, mat_idx=None, closed=True):
    """rings: list (bottom->top) of vertex lists (len 1 = pole). Winding gives outward normals for CCW rings."""
    faces = []
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        n = max(len(a), len(b)); rng = n if closed else n - 1
        for j in range(rng):
            j1 = (j + 1) % n
            va = [a[0], a[0]] if len(a) == 1 else [a[j], a[j1]]
            vb = [b[0], b[0]] if len(b) == 1 else [b[j1], b[j]]
            vs = []
            for v in (va[0], va[1], vb[0], vb[1]):
                if v not in vs: vs.append(v)
            f = bm.faces.new(vs)
            if mat_idx is not None: f.material_index = mat_idx(i)
            faces.append(f)
    return faces

def lathe(bm, profile, segs, origin=(0, 0, 0), axis=(0, 0, 1), sx=1.0, sy=1.0, mat_idx=None, phase=0.0):
    """profile: list of (h, r) along axis, bottom->top; r == 0 makes a pole."""
    ex, ey, ez = frame_from_z(axis); o = Vector(origin); rings = []
    for h, r in profile:
        if r == 0: rings.append([bm.verts.new(o + ez * h)]); continue
        ring = []
        for j in range(segs):
            a = 2 * PI * j / segs + phase
            ring.append(bm.verts.new(o + ex * (r * math.cos(a) * sx) + ey * (r * math.sin(a) * sy) + ez * h))
        rings.append(ring)
    return ring_faces(bm, rings, mat_idx)

def ellipsoid(bm, c, rx, ry, rz, segs=10, rings=7, axis=(0, 0, 1)):
    prof = [(-rz * math.cos(PI * i / rings), math.sin(PI * i / rings) if 0 < i < rings else 0) for i in range(rings + 1)]
    prof = [(h, r) for h, r in prof]
    ex, ey, ez = frame_from_z(axis); o = Vector(c); rr = []
    for h, r in prof:
        if r == 0: rr.append([bm.verts.new(o + ez * h)]); continue
        rr.append([bm.verts.new(o + ex * (rx * r * math.cos(2 * PI * j / segs)) + ey * (ry * r * math.sin(2 * PI * j / segs)) + ez * h) for j in range(segs)])
    return ring_faces(bm, rr)

def tube(bm, pts, radii, sides=6, cap_start=True, tip=True):
    pts = [Vector(p) for p in pts]; rings = []
    t0 = (pts[1] - pts[0]).normalized(); ex, ey, _ = frame_from_z(t0)
    for i, p in enumerate(pts):
        if i == 0: t = pts[1] - pts[0]
        elif i == len(pts) - 1: t = pts[i] - pts[i - 1]
        else: t = pts[i + 1] - pts[i - 1]
        t = t.normalized()
        ex = (ex - t * ex.dot(t)).normalized(); ey = t.cross(ex)   # parallel transport
        if tip and i == len(pts) - 1: rings.append([bm.verts.new(p)]); continue
        rings.append([bm.verts.new(p + ex * (radii[i] * math.cos(2 * PI * j / sides)) + ey * (radii[i] * math.sin(2 * PI * j / sides))) for j in range(sides)])
    if cap_start: rings.insert(0, [bm.verts.new(pts[0] - t0 * radii[0] * 0.3)])
    return ring_faces(bm, rings)

def star_fill(bm, outline, centre, k=2, y=0.0):
    """Fill a star-shaped CCW outline (x, z) with a polar grid of k rings; lies in plane y."""
    c = Vector((centre[0], y, centre[1])); cv = bm.verts.new(c); rings = []
    for m in range(1, k + 1):
        rings.append([bm.verts.new(Vector((centre[0] + (px - centre[0]) * m / k, y, centre[1] + (pz - centre[1]) * m / k))) for px, pz in outline])
    n = len(outline)
    for i in range(n):
        bm.faces.new((cv, rings[0][i], rings[0][(i + 1) % n]))
    for m in range(k - 1):
        for i in range(n):
            i1 = (i + 1) % n
            bm.faces.new((rings[m][i], rings[m + 1][i], rings[m + 1][i1], rings[m][i1]))

def ellipse_pts(cx, cz, rx, rz, n=16, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * PI * i / n), cz + rz * math.sin(a0 + 2 * PI * i / n)) for i in range(n)]

def stroke(bm, pts, w, y=0.0, taper=0.55):
    """Ribbon along a 2D polyline in (x, z) with rounded, tapered ends. w = full width (scalar or list)."""
    pts = [Vector((p[0], p[1])) for p in pts]
    ws = w if isinstance(w, list) else [w] * len(pts)
    t0 = (pts[1] - pts[0]).normalized(); t1 = (pts[-1] - pts[-2]).normalized()
    h0, h1 = ws[0] / 2, ws[-1] / 2
    P = [pts[0] - t0 * h0 * 0.9, pts[0] - t0 * h0 * 0.5] + pts + [pts[-1] + t1 * h1 * 0.5, pts[-1] + t1 * h1 * 0.9]
    W = [ws[0] * 0.38, ws[0] * 0.82] + ws + [ws[-1] * 0.82, ws[-1] * 0.38]
    L, R = [], []
    for i, p in enumerate(P):
        t = (P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]).normalized()
        n = Vector((-t.y, t.x))
        l = p + n * W[i] / 2; r = p - n * W[i] / 2
        L.append(bm.verts.new((l.x, y, l.y))); R.append(bm.verts.new((r.x, y, r.y)))
    for i in range(len(P) - 1):
        bm.faces.new((R[i], R[i + 1], L[i + 1], L[i]))

def arc_pts(cx, cz, r, a_from, a_to, n=10, rz=None):
    rz = rz if rz is not None else r
    return [(cx + r * math.cos(a_from + (a_to - a_from) * i / n), cz + rz * math.sin(a_from + (a_to - a_from) * i / n)) for i in range(n + 1)]

def bake(ob):
    """Apply all modifiers by replacing mesh data with the evaluated mesh."""
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev); old = ob.data
    ob.modifiers.clear(); ob.data = me; bpy.data.meshes.remove(old)

def project_onto(ob, target, offset, thick=0.0, mode='PROJECT', axis='Y'):
    sw = ob.modifiers.new('sw', 'SHRINKWRAP'); sw.target = target; sw.offset = offset
    if mode == 'PROJECT':
        sw.wrap_method = 'PROJECT'; sw.use_project_x = axis == 'X'; sw.use_project_y = axis == 'Y'; sw.use_project_z = axis == 'Z'
        sw.use_negative_direction = True; sw.use_positive_direction = True
    else:
        sw.wrap_method = 'NEAREST_SURFACEPOINT'
    if thick:
        so = ob.modifiers.new('so', 'SOLIDIFY'); so.thickness = thick; so.offset = 1.0; so.use_even_offset = True
    bake(ob)
    bad = [v for v in ob.data.vertices if v.co.y < -0.22]
    assert not bad, 'projection missed for %s: %d verts' % (ob.name, len(bad))
    if thick:   # the inner layer lies on the shirt and is never seen: remove it (saves triangles)
        bm = bmesh.new(); bm.from_mesh(ob.data)
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.normal.y > 0.35], context='FACES')
        bm.to_mesh(ob.data); bm.free()

def join(objs, name):
    base = objs[0]
    with bpy.context.temp_override(active_object=base, selected_editable_objects=objs, object=base):
        bpy.ops.object.join()
    base.name = name; base.data.name = name; return base

def set_origin(ob, p):
    p = Vector(p); ob.data.transform(Matrix.Translation(-p)); ob.location = p

def parent(ch, par):
    bpy.context.view_layer.update()
    mw = ch.matrix_world.copy(); ch.parent = par; ch.matrix_world = mw

# ================================================================ BODY
HC = Vector((0, 0, 0.775)); HR = 0.18           # head centre / radius -> 0.955 m top, 2.65 head-heights
TSY = 0.88                                       # torso front-back squash

# torso: trousers (legs colour) + shirt with a hem lip. (h, r) bottom -> top
TORSO = [(0.150, 0.0), (0.154, 0.068), (0.168, 0.112), (0.192, 0.138), (0.232, 0.148),
         (0.236, 0.172), (0.247, 0.191), (0.262, 0.189), (0.300, 0.193), (0.365, 0.196), (0.430, 0.187),
         (0.488, 0.170), (0.532, 0.146), (0.563, 0.115), (0.578, 0.072), (0.582, 0.0)]
bm = bmesh.new()
lathe(bm, TORSO, 16, sy=TSY, mat_idx=lambda i: 0 if i < 4 else 1, phase=PI / 16)
torso = new_obj('torso', bm, ['legs', 'shirt'])

def torso_r(h):
    for (h0, r0), (h1, r1) in zip(TORSO, TORSO[1:]):
        if h0 <= h <= h1: return r0 + (r1 - r0) * (h - h0) / max(h1 - h0, 1e-6)
    return 0.0

# collar: a ring the head rests in (inner edge tucked inside the torso)
COLLAR = [(0.559, 0.104), (0.566, 0.113), (0.585, 0.101), (0.602, 0.083), (0.611, 0.070), (0.604, 0.055)]
bm = bmesh.new(); lathe(bm, COLLAR, 14, sy=0.92, phase=PI / 14)
collar = new_obj('collar', bm, ['panel'])

# collar points: two flat flaps lying on the chest, projected onto the torso
def flap(sx):
    bm = bmesh.new()
    o = [(0.006, 0.571), (0.045, 0.570), (0.086, 0.561), (0.064, 0.534), (0.034, 0.500), (0.008, 0.540)]
    o = [(x * sx, z) for x, z in o]
    if sx > 0: o = o[::-1]   # make CCW seen from the front
    star_fill(bm, o, (0.040 * sx, 0.550), k=2, y=-0.3)
    ob = new_obj('flap', bm, ['panel']); project_onto(ob, torso, 0.0035, 0.004); return ob
flaps = [flap(1), flap(-1)]

# tie: knot + blade with a point, hugging the shirt
bm = bmesh.new(); ellipsoid(bm, (0, -torso_r(0.552) * TSY - 0.007, 0.551), 0.019, 0.012, 0.017, segs=8, rings=4)
knot = new_obj('knot', bm, ['tie'])
bm = bmesh.new()
blade = [(0.0, 0.405), (0.025, 0.428), (0.024, 0.47), (0.018, 0.51), (0.012, 0.537), (-0.012, 0.537), (-0.018, 0.51), (-0.024, 0.47), (-0.025, 0.428)]
star_fill(bm, blade, (0.0, 0.47), k=3, y=-0.3)
blade_ob = new_obj('blade', bm, ['tie']); project_onto(blade_ob, torso, 0.003, 0.0055)

# lanyard (two gold straps) + badge card with a blue stripe + gold clip, on Kit's right chest (-X)
lan = []
for a, b in [((-0.112, 0.548), (-0.090, 0.488)), ((-0.050, 0.540), (-0.078, 0.488))]:
    bm = bmesh.new(); stroke(bm, [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b], 0.008, y=-0.3)
    ob = new_obj('lanyard', bm, ['gold']); project_onto(ob, torso, 0.0015, 0.002); lan.append(ob)
bm = bmesh.new()
cx, cz, bw, bh = -0.085, 0.452, 0.050, 0.064
def rrect(cx, cz, w, h, r, n=3):
    pts = []
    for qx, qz, a0 in [(1, 1, 0), (-1, 1, PI / 2), (-1, -1, PI), (1, -1, 1.5 * PI)]:
        ccx, ccz = cx + qx * (w / 2 - r), cz + qz * (h / 2 - r)
        for i in range(n + 1): a = a0 + (PI / 2) * i / n; pts.append((ccx + r * math.cos(a), ccz + r * math.sin(a)))
    return pts
star_fill(bm, rrect(cx, cz, bw, bh, 0.008, 2), (cx, cz), k=1, y=-0.3)
card = new_obj('card', bm, ['panel']); project_onto(card, torso, 0.0045, 0.004)
bm = bmesh.new(); star_fill(bm, rrect(cx, cz + 0.017, bw - 0.012, 0.012, 0.003, 2), (cx, cz + 0.017), k=1, y=-0.3)
stripe = new_obj('stripe', bm, ['shirt']); project_onto(stripe, torso, 0.0086)
bm = bmesh.new(); ellipsoid(bm, (cx, 0, cz + bh / 2 + 0.002), 0.008, 0.006, 0.007, segs=6, rings=3)
clip = new_obj('clip', bm, ['gold'])
clip.data.transform(Matrix.Translation((0, -(torso_r(cz + bh / 2) * TSY) * math.cos(math.asin(min(0.99, abs(cx) / torso_r(cz + bh / 2)))) - 0.009, 0)))

# arms: tapered sleeves with a cuff lip; mitten hands with a thumb bump
def arm(S, W, name, sleeve_segs=8):
    S, W = Vector(S), Vector(W); d = (W - S); L = d.length; d.normalize()
    prof = [(-0.03, 0.0), (-0.02, 0.040), (0.02, 0.054), (0.09, 0.052), (L - 0.035, 0.045), (L - 0.012, 0.046), (L - 0.004, 0.050), (L + 0.004, 0.046), (L + 0.008, 0.0)]
    bm = bmesh.new(); lathe(bm, prof, sleeve_segs, origin=S, axis=d, phase=PI / 8)
    sl = new_obj(name + '_sleeve', bm, ['shirt'])
    # mitten: ellipsoid along the arm, flattened, with the thumb pulled forward
    hc = W + d * 0.036
    bm = bmesh.new(); ellipsoid(bm, hc, 0.037, 0.030, 0.045, segs=8, rings=6, axis=d)
    fwd = Vector((0, -1, 0)); fwd = (fwd - d * fwd.dot(d)).normalized()
    for v in bm.verts:
        rel = v.co - hc; f = rel.dot(fwd); u = rel.dot(d)
        if f > 0.012 and u > -0.02:             # thumb bump on the front, upper half of the mitten
            v.co += fwd * 0.012 * min(1, (f - 0.012) / 0.015) * (1 - max(0, u) / 0.05)
    hd = new_obj(name + '_hand', bm, ['skin'])
    return sl, hd, hc
SL = Vector((0.124, 0.0, 0.528)); SR = Vector((-0.124, 0.0, 0.528))
WL = Vector((0.236, -0.012, 0.338))      # Kit's left: carries the briefcase
WR = Vector((-0.212, -0.058, 0.352))     # Kit's right: relaxed, a little forward
slL, hdL, HCL = arm(SL, WL, 'armL'); slR, hdR, HCR = arm(SR, WR, 'armR')

# legs + shoes with a toe
legs = []
for sx in (1, -1):
    bm = bmesh.new(); lathe(bm, [(0.040, 0.034), (0.20, 0.046)], 8, origin=(0.074 * sx, 0, 0))
    legs.append(new_obj('leg', bm, ['legs']))
    # shoe: flat sole, rounded upper, low toe
    SH = [(0.0, 0.0), (0.0, 0.84), (0.016, 1.0), (0.044, 0.92), (0.066, 0.66), (0.078, 0.0)]
    bm = bmesh.new(); lathe(bm, SH, 8, origin=(0.074 * sx, -0.026, 0.002), sx=0.054, sy=0.088)
    legs.append(new_obj('shoe', bm, ['wood']))

# ================================================================ BRIEFCASE (held by the left mitten)
b_ang = math.radians(35)            # broad face turned 35 deg from side-on toward the front
n_face = Vector((math.cos(b_ang), -math.sin(b_ang), 0)); u_ax = Vector((math.sin(b_ang), math.cos(b_ang), 0))
BW, BH, BD = 0.23, 0.165, 0.066
grip = HCL.copy()
h_r, h_t = 0.032, 0.0075                          # handle arc radius / tube radius
top_z = grip.z - h_r
bc = Vector((grip.x, grip.y, top_z - BH / 2))
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.0)
bmesh.ops.scale(bm, vec=(BD, BW, BH), verts=bm.verts)
bmesh.ops.bevel(bm, geom=list(bm.edges), offset=0.016, segments=2, affect='EDGES', profile=0.5)
rot = Matrix.Rotation(-b_ang, 4, 'Z')
bmesh.ops.transform(bm, matrix=Matrix.Translation(bc) @ rot, verts=bm.verts)
case = new_obj('case', bm, ['wood'], smooth=True, sharp_angle=50)
parts_bc = [case]
bm = bmesh.new()
hb = Vector((grip.x, grip.y, top_z))
arc = [hb + u_ax * (h_r * math.cos(PI * i / 6)) + Vector((0, 0, h_r * math.sin(PI * i / 6))) for i in range(7)]
arc = [arc[0] - Vector((0, 0, 0.012))] + arc + [arc[-1] - Vector((0, 0, 0.012))]
tube(bm, arc, [h_t] * len(arc), sides=5, cap_start=False, tip=False)
handle = new_obj('handle', bm, ['wood'])
for su in (-1, 1):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(0.018, 0.02, 0.012), verts=bm.verts)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((grip.x, grip.y, top_z + 0.004)) + u_ax * (su * h_r)) @ rot, verts=bm.verts)
    parts_bc.append(new_obj('mount', bm, ['wood'], smooth=False))
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(BD + 0.008, 0.022, 0.016), verts=bm.verts)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector((bc.x, bc.y, top_z - 0.022)) + u_ax * (su * 0.062)) @ rot, verts=bm.verts)
    parts_bc.append(new_obj('clasp', bm, ['gold'], smooth=False))
parts_bc.append(handle)

# ================================================================ HEAD + HAIR
bm = bmesh.new()
segs = 22
# rings are denser where the head is seen (below the hair) and sparse under the hair cap
PHIS = [180, 166, 154, 143, 132, 121, 110, 99, 88, 77, 66, 55, 44, 28, 0]
prof = [(HR * math.cos(math.radians(p)), HR * math.sin(math.radians(p)) if 0 < p < 180 else 0) for p in PHIS]
lathe(bm, prof, segs, origin=HC, phase=PI / 2)     # a vertex column on the face centre line
head = new_obj('head', bm, ['skin'])

def hair_edge(th):
    """Hair boundary as polar angle from the crown (deg) for azimuth th (deg, 0 = front, + toward Kit's left)."""
    a = abs(((th + 180) % 360) - 180)
    g = lambda c, d, w: d * math.exp(-((th - c) / w) ** 2)
    if a <= 58:   # side-swept fringe: 4 soft locks, deeper toward Kit's right
        return 46.0 + max(g(-40, 15, 9.5), g(-14, 18, 9.5), g(12, 15, 9.5), g(36, 10, 9.5), 0)
    if a <= 74:   # temple: the edge drops quickly, so the side reads as a sideburn line, not a helmet rim
        t = (a - 58) / 16; t = t * t * (3 - 2 * t); return 46 + (93 - 46) * t
    t = (a - 74) / 106; t = t * t * (3 - 2 * t)
    nape = max(g(180, 7, 12), g(-180, 7, 12), g(150, 6, 10), g(-150, 6, 10))
    return 93 + 11 * t + nape

# head faces fully covered by the hair cap are never seen: delete them
bm = bmesh.new(); bm.from_mesh(head.data); kill = []
for f in bm.faces:
    ok = True
    for v in f.verts:
        rel = v.co - HC; ph = math.degrees(math.acos(max(-1, min(1, rel.z / rel.length))))
        th = math.degrees(math.atan2(rel.x, -rel.y))
        if ph > hair_edge(th) - 7: ok = False; break
    if ok: kill.append(f)
bmesh.ops.delete(bm, geom=kill, context='FACES'); bm.to_mesh(head.data); bm.free()

HAIR_SEGS = 28
bm = bmesh.new(); rings_v = []
S_LIST = [1.0, 0.9, 0.7, 0.42, 0.18]
def hdir(th, ph):
    t, p = math.radians(th), math.radians(ph)
    return Vector((math.sin(p) * math.sin(t), -math.sin(p) * math.cos(t), math.cos(p)))
# denser columns across the fringe (7.3 deg) so the locks stay round; sparser at the back (22 deg)
ths = [-76 + 152 * j / 18 for j in range(19)] + [76 + (360 - 152) * (j + 1) / 10 for j in range(9)]
ths = sorted(((t + 180) % 360) - 180 for t in ths)
# tuck ring: the edge curls in under the cap, inside the head (no gap, no visible shell edge)
rings_v.append([bm.verts.new(HC + hdir(th, hair_edge(th) + 6.0) * (HR - 0.003)) for th in ths])
for s in S_LIST:
    ring = []
    for th in ths:
        ph = hair_edge(th) * s
        a_ = abs(((th + 180) % 360) - 180)
        lock = 0.006 * (hair_edge(th) - (50 if a_ <= 62 else hair_edge(th))) / 20.0 * s    # lock tips bulge
        r = HR + 0.016 + lock + 0.008 * (1 - s) ** 2                       # fuller crown
        if s == 1.0: r = HR + 0.009 + lock * 0.5
        ring.append(bm.verts.new(HC + hdir(th, ph) * r))
    rings_v.append(ring)
rings_v.append([bm.verts.new(HC + Vector((0, 0.004, HR + 0.024)))])
# ring order around +Z must be CCW: ths increase from -Y toward +X, which is CCW seen from above
ring_faces(bm, rings_v)
hair = new_obj('hair', bm, ['hair'])

# ================================================================ SPROUT (pivot at its root on the crown)
root_dir = hdir(180, 10); SP_ROOT = HC + root_dir * (HR + 0.018)
# a springy curl that leans to Kit's left, so it reads from the front, the side and the 26 m camera
_cd = Vector((0.80, 0.60, 0))    # curl direction: to Kit's left and back, so front, 3/4, side and back all show the curl
sp_pts = [(0, 0, -0.016), (0.0, 0, 0.012), (-0.004, 0, 0.040), (0.000, 0, 0.068), (0.014, 0, 0.092), (0.036, 0, 0.102), (0.054, 0, 0.094), (0.059, 0, 0.079)]
SPK = 1.32   # sized to read at the 26 m follow camera (Kit is ~50 px tall there)
sp_pts = [tuple((_cd * p[0] + Vector((0, 0, p[2]))) * SPK) for p in sp_pts]
sp_rad = [0.021, 0.0195, 0.0165, 0.0135, 0.011, 0.0088, 0.0065, 0.0025]
bm = bmesh.new(); tube(bm, [SP_ROOT + Vector(p) for p in sp_pts], sp_rad, sides=6)
sprout = new_obj('sprout', bm, ['hair'])
set_origin(sprout, SP_ROOT)

# sprout clearance per pose: every vertex above the root ring must stay outside the hair shell
def sprout_clear(rot, scl):
    q = (Matrix.Rotation(math.radians(rot[0]), 4, 'X') @ Matrix.Rotation(math.radians(rot[1]), 4, 'Y'))
    mn = 9.0
    for v in sprout.data.vertices:
        if v.co.z < 0.035: continue         # the root is buried in the hair by design
        lc = v.co.copy(); lc.z *= scl
        p = SP_ROOT + (q @ lc.to_4d()).to_3d()
        mn = min(mn, (p - HC).length - (HR + 0.016))
    return round(mn * 1000, 1)

# ================================================================ FACE SETS (decals on the head surface)
def on_head(ob, offset):
    me = ob.data
    for v in me.vertices:
        x, z = v.co.x, v.co.z - HC.z
        y = -math.sqrt(max(HR * HR - x * x - z * z, 1e-6))
        v.co = Vector((x, y - 0.003, v.co.z))
    sw = ob.modifiers.new('sw', 'SHRINKWRAP'); sw.target = head; sw.wrap_method = 'NEAREST_SURFACEPOINT'; sw.offset = offset
    bake(ob)

def decal(name, build, material, layer=0):
    bm = bmesh.new(); build(bm)
    for v in bm.verts: v.co.z += HC.z
    ob = new_obj(name, bm, [material]); on_head(ob, 0.0009 + 0.0009 * layer); return ob

EX = 0.058; EZ = -0.008
def eyes_oval(rx, rz, hl=1, big=False):
    parts = []
    for sx in (-1, 1):
        parts.append(decal('eye', lambda bm, sx=sx: star_fill(bm, ellipse_pts(sx * EX, EZ, rx, rz, 16), (sx * EX, EZ)), 'ink'))
        for k in range(hl):
            hx, hz, hr = sx * EX + 0.30 * rx, EZ + 0.38 * rz, 0.26 * min(rx, rz) + 0.0015
            if k == 1: hx, hz, hr = sx * EX - 0.25 * rx, EZ - 0.35 * rz, 0.15 * min(rx, rz) + 0.001
            parts.append(decal('hl', lambda bm, hx=hx, hz=hz, hr=hr: star_fill(bm, ellipse_pts(hx, hz, hr, hr, 10), (hx, hz), k=1), 'white', 1))
    return parts

def brows(z, tilt_deg, w=0.034, arch=0.004, th=0.0065):
    parts = []
    for sx in (-1, 1):
        t = math.radians(tilt_deg)               # + tilt raises the inner end
        pts = []
        for i in range(5):
            u = -0.5 + i / 4
            x = sx * EX + u * w; zz = z + arch * (1 - (2 * u) ** 2) - u * sx * w * math.tan(t)
            pts.append((x, zz))
        if sx < 0: pts = pts
        parts.append(decal('brow', lambda bm, pts=pts: stroke(bm, pts, [th * 0.75, th, th * 1.05, th, th * 0.75]), 'ink'))
    return parts

def smile(r, span, z=-0.050, th=0.0068, x=0.0):
    a0 = -PI / 2 - span / 2; a1 = -PI / 2 + span / 2
    pts = arc_pts(x, z + r, r, a0, a1, 10)
    return [decal('mouth', lambda bm: stroke(bm, pts, th), 'ink')]

def cheeks():
    return [decal('cheek', lambda bm, sx=sx: star_fill(bm, ellipse_pts(sx * 0.092, -0.036, 0.019, 0.0115, 14), (sx * 0.092, -0.036)), 'cheek') for sx in (-1, 1)]

def sweat_drop():
    bm = bmesh.new()
    prof = [(0.0, 0.0), (0.004, 0.008), (0.010, 0.0118), (0.018, 0.0105), (0.026, 0.0068), (0.034, 0.0028), (0.040, 0.0)]
    d = Vector((0.80, -0.40, 0.45)).normalized(); c = HC + d * (HR + 0.03)
    lathe(bm, prof, 10, origin=c - Vector((0, 0, 0.018)), axis=(0.12, 0, 1))
    return new_obj('sweat', bm, ['sweat'])

EXPR = {}
EXPR['hopeful'] = dict(parts=lambda: eyes_oval(0.0165, 0.0255, 1) + brows(0.050, 6) + smile(0.025, 0.80 * PI) + cheeks(),
                       sprout=(0, 0, 0), sprout_scale=1.0)
EXPR['ghosted'] = dict(parts=lambda: eyes_oval(0.0085, 0.0085, 0) + brows(0.040, 0, w=0.030, arch=0.0)
                       + [decal('mouth', lambda bm: stroke(bm, [(-0.012, -0.052), (0.0, -0.0525), (0.012, -0.052)], 0.0062), 'ink')]
                       + [sweat_drop()], sprout=(0, 78, 0), sprout_scale=0.92)
def caret_eyes():
    out = []
    for sx in (-1, 1):
        pts = arc_pts(sx * EX, EZ - 0.010, 0.0175, 0.18 * PI, 0.82 * PI, 8)
        out.append(decal('eye', lambda bm, pts=pts: stroke(bm, pts, 0.0062), 'ink'))
    return out
EXPR['rejected'] = dict(parts=lambda: caret_eyes() + brows(0.048, 10, w=0.030) + smile(0.032, 0.92 * PI, z=-0.056) + [sweat_drop()],
                        sprout=(0, 34, 0), sprout_scale=0.96)
EXPR['focused'] = dict(parts=lambda: eyes_oval(0.0160, 0.0125, 1) + brows(0.036, -16, w=0.034, arch=0.0)
                       + [decal('mouth', lambda bm: stroke(bm, [(0.004, -0.050), (0.013, -0.0505), (0.022, -0.0515)], 0.006), 'ink')],
                       sprout=(-8, 0, 0), sprout_scale=1.0)
def d_mouth():
    o = arc_pts(0.0, -0.036, 0.030, PI, 2 * PI, 12, rz=0.031) + [(0.015, -0.036), (0.0, -0.036), (-0.015, -0.036)]
    parts = [decal('mouth', lambda bm: star_fill(bm, o, (0.0, -0.050), k=2), 'ink')]
    parts.append(decal('tongue', lambda bm: star_fill(bm, ellipse_pts(0.0, -0.058, 0.016, 0.0075, 12), (0.0, -0.058), k=1), 'tongue', 1))
    return parts
EXPR['offer_joy'] = dict(parts=lambda: eyes_oval(0.0205, 0.030, 2) + brows(0.056, 8, w=0.032, arch=0.006) + d_mouth() + cheeks(),
                         sprout=(0, 0, 0), sprout_scale=1.32)

# ghosted: droop as far as the hair allows (keep >= 3 mm clear of the hair shell)
for ang in range(80, 20, -2):
    if sprout_clear((0, ang, 0), 0.92) >= 3.0: break
EXPR['ghosted']['sprout'] = (0, ang, 0)
face_objs = {}
for name, spec in EXPR.items():
    ps = spec['parts']()
    ob = join(ps, 'face_' + name)
    ob['sprout_rot_deg'] = list(spec['sprout']); ob['sprout_scale'] = spec['sprout_scale']
    ob['default_visible'] = name == 'hopeful'
    qb = Euler([math.radians(a) for a in spec['sprout']]).to_quaternion()
    ob['sprout_quat_three_xyzw'] = [qb.x, qb.z, -qb.y, qb.w]     # Blender Z-up -> three.js Y-up
    ob['sprout_scale_three_y'] = spec['sprout_scale']
    face_objs[name] = ob

# ================================================================ CHECKS (before joining, world space)
def bvh(ob):
    dg = bpy.context.evaluated_depsgraph_get(); return BVHTree.FromObject(ob, dg)
checks = {}
def overlap(a, b): return len(bvh(a).overlap(bvh(b)))
checks['briefcase_vs_torso'] = overlap(case, torso)
checks['briefcase_vs_legs_shoes'] = sum(overlap(case, l) for l in legs)
checks['briefcase_vs_sleeveL'] = overlap(case, slL)
checks['briefcase_vs_handR'] = overlap(case, hdR)
checks['handR_vs_torso'] = overlap(hdR, torso)
checks['handL_vs_torso'] = overlap(hdL, torso)
checks['handle_inside_handL'] = overlap(handle, hdL) > 0   # the mitten wraps the handle (wanted)
checks['blade_vs_flaps'] = sum(overlap(blade_ob, f) for f in flaps)
checks['card_vs_tie'] = overlap(card, blade_ob)
checks['head_vs_collar_contact'] = overlap(head, collar)
# face parts must sit below the hair edge and outside the head
def face_clear(ob):
    worst = 99.0; dmin = 9.0
    for v in ob.data.vertices:
        p = ob.matrix_world @ v.co; rel = p - HC
        if rel.length > HR + 0.012: continue      # the 3D sweat drop floats beside the head (checked below)
        ph = math.degrees(math.acos(max(-1, min(1, rel.z / rel.length))))
        th = math.degrees(math.atan2(rel.x, -rel.y))
        worst = min(worst, ph - hair_edge(th))
    return round(worst, 1)
for n, ob in face_objs.items(): checks['face_%s_deg_below_hair_edge' % n] = face_clear(ob)
for n in ('ghosted', 'rejected'):
    ob = face_objs[n]; far = [(ob.matrix_world @ v.co - HC).length for v in ob.data.vertices if (ob.matrix_world @ v.co - HC).length > HR + 0.012]
    checks['sweat_%s_min_gap_to_hair_mm' % n] = round((min(far) - (HR + 0.016)) * 1000, 1)

for n, spec in EXPR.items(): checks['sprout_%s_min_clearance_mm' % n] = sprout_clear(spec['sprout'], spec['sprout_scale'])

# ================================================================ MERGE + RIG
body = join([torso, collar, knot, blade_ob, card, stripe, clip, slL, hdL, slR, hdR] + flaps + lan + legs, 'body')
headm = join([head, hair], 'head')
brief = join(parts_bc, 'briefcase')
for ob in (body, headm, brief, sprout): ob.data.name = ob.name

root = bpy.data.objects.new('root', None); COL.objects.link(root)
bounce = bpy.data.objects.new('bounce', None); COL.objects.link(bounce); bounce.parent = root
body.parent = bounce
set_origin(headm, (0, 0, 0.600)); parent(headm, body)
set_origin(brief, grip); parent(brief, body)
parent(sprout, headm)
for ob in face_objs.values():
    set_origin(ob, (0, 0, 0.600)); parent(ob, headm)
# rest pose: alive, not stiff - head tilts toward the briefcase and lifts a little (Emil E1)
headm.rotation_euler = (math.radians(-3), math.radians(5), math.radians(-4))
for n, ob in face_objs.items():
    ob.hide_render = ob.hide_viewport = not ob['default_visible']

bpy.context.view_layer.update()
# triangle counts
def tris(ob):
    me = ob.data; me.calc_loop_triangles(); return len(me.loop_triangles)
counts = {o.name: tris(o) for o in (body, headm, sprout, brief)}
counts['hero_total'] = sum(counts.values())
counts['body_plus_head'] = counts['body'] + counts['head']
counts.update({o.name: tris(o) for o in face_objs.values()})
report = {'triangles': counts, 'checks': checks, 'toon': TOON,
          'hero_height_m': round(max((headm.matrix_world @ v.co).z for v in headm.data.vertices), 3),
          'head_heights': round(max((headm.matrix_world @ v.co).z for v in headm.data.vertices) / (2 * HR), 2)}
print('KIT_REPORT', json.dumps(report, indent=1))
json.dump(report, open(os.path.join(HERE, 'build_report.json'), 'w'), indent=1)
json.dump(TOON, open(os.path.join(HERE, 'toon.json'), 'w'), indent=1)

# ================================================================ EXPORT
bpy.ops.object.select_all(action='DESELECT')
for ob in face_objs.values(): ob.hide_viewport = False
for ob in [root, bounce, body, headm, brief, sprout] + list(face_objs.values()): ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(HERE, 'kit.glb'), export_format='GLB', use_selection=True,
                          export_yup=True, export_apply=True, export_extras=True, export_materials='EXPORT',
                          export_cameras=False, export_lights=False, export_animations=False)
for ob in face_objs.values(): ob.hide_viewport = not ob['default_visible']
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'kit.blend'))
print('KIT_DONE')
