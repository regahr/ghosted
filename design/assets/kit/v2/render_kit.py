# GHOSTED - Kit renders. Opens kit.blend (made by build_kit.py), swaps the export materials for the toon
# shader, adds the ink outline, lights and cameras, and renders every sheet image.
# Run: Blender -b kit.blend -P render_kit.py [-- only=<name,...>]
# The toon shader reproduces three.js MeshToonMaterial + the render.html character light exactly:
#   colour = NeutralToneMap( base * (band(N.L) * sun + hemi(N.up) + ambient) / pi )
# band(N.L) comes from Shader-to-RGB of a white Diffuse BSDF and a constant ColorRamp (2 bands, 3 on skin).
# The sun casts no shadow map, so there is no acne and no streaks; the ground contact is an ink blob,
# the same one the game draws (Lena: CircleGeometry, ink 25%).
import bpy, math, json, os, sys
import numpy as np
from mathutils import Vector, Euler

HERE = os.path.dirname(bpy.data.filepath)
TOON = json.load(open(os.path.join(HERE, 'toon.json')))
ONLY = None
if '--' in sys.argv:
    for a in sys.argv[sys.argv.index('--') + 1:]:
        if a.startswith('only='): ONLY = a[5:].split(',')
PI = math.pi
scn = bpy.context.scene
bpy.context.preferences.filepaths.save_version = 0

def s2l1(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hex2srgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def s2l(h): return [s2l1(c) for c in hex2srgb(h)]
def l2s1(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def neutral_tm(c):  # three.js r170 NeutralToneMapping, exposure 1
    c = list(c); x = min(c); off = x - 6.25 * x * x if x < 0.08 else 0.04
    c = [v - off for v in c]; peak = max(c)
    if peak < 0.76: return c
    d = 0.24; newp = 1 - d * d / (peak + d - 0.76); c = [v * newp / peak for v in c]
    g = 1 - 1 / (0.15 * (peak - newp) + 1); return [v * (1 - g) + newp * g for v in c]

# ---------------------------------------------------------------- node group: Neutral tone mapping
def make_tm_group():
    g = bpy.data.node_groups.new('NeutralTM', 'ShaderNodeTree')
    g.interface.new_socket('Color', in_out='INPUT', socket_type='NodeSocketVector')
    g.interface.new_socket('Color', in_out='OUTPUT', socket_type='NodeSocketVector')
    N, L = g.nodes, g.links
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput')
    def m(op, a, b=None, c=None):
        n = N.new('ShaderNodeMath'); n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: L.new(v, n.inputs[i])
        return n.outputs[0]
    def vm(op, a, b=None, scale=None):
        n = N.new('ShaderNodeVectorMath'); n.operation = op
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (tuple, list)): n.inputs[i].default_value = v
            else: L.new(v, n.inputs[i])
        if scale is not None:
            if isinstance(scale, (int, float)): n.inputs['Scale'].default_value = scale
            else: L.new(scale, n.inputs['Scale'])
        return n.outputs[0]
    def sep(v):
        s = N.new('ShaderNodeSeparateXYZ'); L.new(v, s.inputs[0]); return s.outputs
    def comb(a):
        c = N.new('ShaderNodeCombineXYZ')
        for i in range(3): L.new(a, c.inputs[i])
        return c.outputs[0]
    c = gi.outputs[0]; r, gg, b = sep(c)
    x = m('MINIMUM', m('MINIMUM', r, gg), b)
    lt = m('LESS_THAN', x, 0.08)
    a = m('SUBTRACT', x, m('MULTIPLY', m('MULTIPLY', x, x), 6.25))
    off = m('ADD', m('MULTIPLY', lt, a), m('MULTIPLY', m('SUBTRACT', 1.0, lt), 0.04))
    c1 = vm('SUBTRACT', c, comb(off))
    r1, g1, b1 = sep(c1)
    peak = m('MAXIMUM', m('MAXIMUM', r1, g1), b1)
    pk = m('MAXIMUM', peak, 0.7601)
    newp = m('SUBTRACT', 1.0, m('DIVIDE', 0.0576, m('SUBTRACT', pk, 0.52)))
    c2 = vm('SCALE', c1, scale=m('DIVIDE', newp, pk))
    gfac = m('SUBTRACT', 1.0, m('DIVIDE', 1.0, m('ADD', m('MULTIPLY', m('SUBTRACT', pk, newp), 0.15), 1.0)))
    c3 = vm('ADD', vm('SCALE', c2, scale=m('SUBTRACT', 1.0, gfac)), vm('SCALE', comb(newp), scale=gfac))
    sel = m('LESS_THAN', peak, 0.76)
    out = vm('ADD', vm('SCALE', c1, scale=sel), vm('SCALE', c3, scale=m('SUBTRACT', 1.0, sel)))
    L.new(out, go.inputs[0])
    return g
TM = make_tm_group()

SUN = TOON['sun']; HEMI = TOON['hemi']; AMB = TOON['ambient']
sun_lin = [v * SUN['intensity'] for v in s2l(SUN['color'])]
sky = [v * HEMI['intensity'] for v in s2l(HEMI['sky'])]; gnd = [v * HEMI['intensity'] for v in s2l(HEMI['ground'])]
amb = [v * AMB['intensity'] for v in s2l(AMB['color'])]
T = TOON['texels']

def toon_tree(m, base_hex, bands):
    m.use_nodes = True; nt = m.node_tree; N, L = nt.nodes, nt.links; N.clear()
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    dif = N.new('ShaderNodeBsdfDiffuse'); dif.inputs['Color'].default_value = (1, 1, 1, 1)
    s2r = N.new('ShaderNodeShaderToRGB'); L.new(dif.outputs[0], s2r.inputs[0])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
    els = ramp.color_ramp.elements
    while len(els) < len(bands): els.new(0.5)
    for el, (t, v) in zip(els, bands):
        el.position = max(0.0, t); val = v / 255; el.color = (val, val, val, 1)
    L.new(s2r.outputs['Color'], ramp.inputs['Fac'])
    bw = N.new('ShaderNodeRGBToBW'); L.new(ramp.outputs['Color'], bw.inputs[0])
    sunv = N.new('ShaderNodeVectorMath'); sunv.operation = 'SCALE'; sunv.inputs[0].default_value = sun_lin
    L.new(bw.outputs[0], sunv.inputs['Scale'])
    geo = N.new('ShaderNodeNewGeometry'); sp = N.new('ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sp.inputs[0])
    w = N.new('ShaderNodeMath'); w.operation = 'MULTIPLY_ADD'; w.inputs[1].default_value = 0.5; w.inputs[2].default_value = 0.5
    L.new(sp.outputs['Z'], w.inputs[0])
    hv = N.new('ShaderNodeVectorMath'); hv.operation = 'SCALE'; hv.inputs[0].default_value = [s - g for s, g in zip(sky, gnd)]
    L.new(w.outputs[0], hv.inputs['Scale'])
    h2 = N.new('ShaderNodeVectorMath'); h2.operation = 'ADD'; h2.inputs[1].default_value = [g + a for g, a in zip(gnd, amb)]
    L.new(hv.outputs[0], h2.inputs[0])
    irr = N.new('ShaderNodeVectorMath'); irr.operation = 'ADD'; L.new(sunv.outputs[0], irr.inputs[0]); L.new(h2.outputs[0], irr.inputs[1])
    alb = N.new('ShaderNodeVectorMath'); alb.operation = 'MULTIPLY'; alb.inputs[1].default_value = [c / PI for c in s2l(base_hex)]
    L.new(irr.outputs[0], alb.inputs[0])
    tm = N.new('ShaderNodeGroup'); tm.node_tree = TM; L.new(alb.outputs[0], tm.inputs[0])
    L.new(tm.outputs[0], em.inputs['Color']); L.new(em.outputs[0], out.inputs['Surface'])

def flat_tree(m, lin_rgb, cull=False):
    m.use_nodes = True; nt = m.node_tree; N = nt.nodes; N.clear()
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*lin_rgb, 1); nt.links.new(em.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = cull

for m in list(bpy.data.materials):
    if 'hex' not in m.keys(): continue
    name = m.name
    if name in TOON['basic_materials']: flat_tree(m, neutral_tm(s2l(m['hex'])))
    else: toon_tree(m, m['hex'], TOON['bands3'] if name in TOON['skin_materials'] else TOON['bands2'])

INK = bpy.data.materials.new('outline_ink'); flat_tree(INK, neutral_tm(s2l(TOON['outline']['color'])), cull=True)

def add_outline(ob, width):
    n = len(ob.data.materials)
    for _ in range(n): ob.data.materials.append(INK)
    so = ob.modifiers.new('outline', 'SOLIDIFY')
    so.thickness = -width; so.offset = -1.0; so.use_flip_normals = True; so.use_rim = False
    so.material_offset = n; so.use_even_offset = False; so.use_quality_normals = True
for nm in ('body', 'head', 'briefcase', 'sprout'):
    add_outline(bpy.data.objects[nm], TOON['outline']['width_m'])

# ---------------------------------------------------------------- world, film, colour
scn.render.engine = 'BLENDER_EEVEE_NEXT'
scn.eevee.taa_render_samples = 32
scn.view_settings.view_transform = 'Standard'; scn.view_settings.look = 'None'
scn.view_settings.exposure = 0; scn.view_settings.gamma = 1
scn.render.film_transparent = True
scn.render.filter_size = 1.2
world = bpy.data.worlds.new('w'); scn.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
BG_HEX = '#FDE6C8'
scn.use_nodes = True; ct = scn.node_tree; ct.nodes.clear()
rl = ct.nodes.new('CompositorNodeRLayers'); ao = ct.nodes.new('CompositorNodeAlphaOver'); co = ct.nodes.new('CompositorNodeComposite')
ao.inputs[1].default_value = (*s2l(BG_HEX), 1)
ct.links.new(rl.outputs['Image'], ao.inputs[2]); ct.links.new(ao.outputs[0], co.inputs[0])

# sun: same direction as render.html charStage (three.js Y-up -> Blender Z-up: (x, y, z) -> (x, -z, y))
el, az = math.radians(SUN['elev']), math.radians(SUN['az'])
Lt = Vector((math.sin(az) * math.cos(el), math.sin(el), math.cos(az) * math.cos(el)))
Lb = Vector((Lt.x, -Lt.z, Lt.y)).normalized()
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 1 / 0.254638671875   # makes Shader-to-RGB read N.L exactly
sd.angle = 0.0; sd.use_shadow = False; sd.color = (1, 1, 1)
so = bpy.data.objects.new('sun', sd); scn.collection.objects.link(so)
so.rotation_mode = 'QUATERNION'; so.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Lb)

# contact shadow blob (ink 25% over the background, pre-mixed in sRGB like the browser does)
cs = TOON['contact_shadow']
bg_s = hex2srgb(BG_HEX); ink_s = hex2srgb(cs['color'])
blob_s = [b * (1 - cs['opacity']) + i * cs['opacity'] for b, i in zip(bg_s, ink_s)]
bpy.ops.mesh.primitive_circle_add(vertices=40, radius=1.0, fill_type='NGON', location=(0.03, -0.01, -0.008))
blob = bpy.context.object; blob.name = 'contact_shadow'; blob.scale = (cs['rx'], cs['ry'], 1)
bm_ = bpy.data.materials.new('blob'); flat_tree(bm_, [s2l1(c) for c in blob_s]); blob.data.materials.append(bm_)
blob.parent = bpy.data.objects['root']

cam_d = bpy.data.cameras.new('cam'); cam_d.sensor_fit = 'VERTICAL'; cam_d.lens_unit = 'FOV'
cam = bpy.data.objects.new('cam', cam_d); scn.collection.objects.link(cam); scn.camera = cam
cam_d.clip_start = 0.05; cam_d.clip_end = 100

ROOT = bpy.data.objects['root']; SPROUT = bpy.data.objects['sprout']
FACES = {o.name[5:]: o for o in bpy.data.objects if o.name.startswith('face_')}

def set_expr(name):
    for n, o in FACES.items(): o.hide_render = o.hide_viewport = (n != name)
    f = FACES[name]; SPROUT.rotation_mode = 'XYZ'
    SPROUT.rotation_euler = Euler([math.radians(a) for a in f['sprout_rot_deg']])
    SPROUT.scale = (1, 1, f['sprout_scale'])

def shoot(name, w, h, angle_deg, cam_pos, target, fov=22, expr='hopeful', blob_on=True, compose=True):
    if ONLY and name not in ONLY: return
    set_expr(expr); ROOT.rotation_euler = (0, 0, math.radians(angle_deg))
    blob.hide_render = not blob_on
    cam.location = Vector(cam_pos); cam_d.angle_y = math.radians(fov)
    d = Vector(target) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    scn.render.resolution_x, scn.render.resolution_y = w, h; scn.render.resolution_percentage = 100
    scn.render.use_compositing = compose
    scn.render.image_settings.file_format = 'PNG'; scn.render.image_settings.color_mode = 'RGB' if compose else 'RGBA'
    scn.render.filepath = os.path.join(HERE, name + '.png')
    bpy.ops.render.render(write_still=True); print("RENDERED", name)

# camera = render.html charStage: fov 22, (0, 0.6, 3.4) looking at (0, 0.5, 0) -> Blender (0, -3.4, 0.6)
TURN_CAM = ((0, -3.4, 0.6), (0, 0, 0.5))
for nm, ang in [('turn-front', 0), ('turn-34', -35), ('turn-side', -90), ('turn-back', 180)]:
    shoot(nm, 900, 1200, ang, *TURN_CAM)
for e in ['hopeful', 'ghosted', 'rejected', 'focused', 'offer_joy']:
    shoot('expr-' + e.replace('_', '-'), 600, 600, -8, (0, -1.55, 0.90), (0, 0, 0.845), expr=e)
shoot('hero', 1200, 1200, -28, (0, -3.4, 1.15), (0, 0, 0.53))
shoot('_mask34', 900, 1200, -35, *TURN_CAM, blob_on=False, compose=False)
shoot('_maskfront', 900, 1200, 0, *TURN_CAM, blob_on=False, compose=False)

# ---------------------------------------------------------------- silhouette-64 and grey
def load_px(path):
    im = bpy.data.images.load(path); w, h = im.size
    a = np.empty(w * h * 4, np.float32); im.pixels.foreach_get(a); bpy.data.images.remove(im)
    return a.reshape(h, w, 4)
def save_px(path, arr):
    h, w = arr.shape[:2]; im = bpy.data.images.new('o', w, h, alpha=True)
    im.pixels.foreach_set(arr.astype(np.float32).ravel()); im.filepath_raw = path; im.file_format = 'PNG'; im.save()
    bpy.data.images.remove(im)
def area_resize(img, nh, nw):
    h, w = img.shape
    ys = (np.arange(nh + 1) * h / nh).astype(int); xs = (np.arange(nw + 1) * w / nw).astype(int)
    out = np.zeros((nh, nw), np.float32)
    for i in range(nh):
        for j in range(nw): out[i, j] = img[ys[i]:max(ys[i + 1], ys[i] + 1), xs[j]:max(xs[j + 1], xs[j] + 1)].mean()
    return out

def silhouette(mask_name, out_name):
    mpath = os.path.join(HERE, mask_name + '.png')
    if not os.path.exists(mpath): return
    a = load_px(mpath)[..., 3]
    ys, xs = np.where(a > 0.5); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    crop = a[y0:y1, x0:x1]; nh = 64; nw = max(1, round((x1 - x0) * nh / (y1 - y0)))
    small = area_resize(crop, nh, nw)
    pad = 6; W = nw + 2 * pad
    out = np.ones((nh, W, 4), np.float32); v = 1 - small
    out[:, pad:pad + nw, 0] = v; out[:, pad:pad + nw, 1] = v; out[:, pad:pad + nw, 2] = v
    save_px(os.path.join(HERE, out_name + '.png'), out)
    save_px(os.path.join(HERE, out_name + '-x4.png'), np.repeat(np.repeat(out, 4, 0), 4, 1))   # nearest-neighbour preview
    os.remove(mpath); print('SIL', out_name, nw, nh)
if not ONLY or 'silhouette' in ONLY or '_maskfront' in ONLY:
    silhouette('_maskfront', 'silhouette-64'); silhouette('_mask34', 'silhouette-64-34')
tpath = os.path.join(HERE, 'turn-34.png')
if os.path.exists(tpath) and (not ONLY or 'grey' in ONLY or 'turn-34' in ONLY):
    p = load_px(tpath); lin = np.where(p[..., :3] <= 0.04045, p[..., :3] / 12.92, ((p[..., :3] + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    out = np.ones_like(p); out[..., 0] = out[..., 1] = out[..., 2] = s
    save_px(os.path.join(HERE, 'grey.png'), out); print('GREY done')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'kit_render.blend'))
