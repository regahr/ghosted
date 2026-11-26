# GHOSTED - ATS-9000 renders (from ricky/v1/render_ricky.py). Opens ats.blend (made by build_ats.py), swaps the export
# materials for Kit's toon shader, adds the ink outline, lights and cameras, and renders every sheet image.
# Run: Blender -b ats.blend -P render_ats.py [-- only=<name,...>] [blockout] [out=<dir>]
# Same toon formula, light, outline and contact shadow as Kit (assets/kit/render_kit.py, assets/kit/toon.json):
#   colour = NeutralToneMap( base * (band(N.L) * sun + hemi(N.up) + ambient) / pi )
# Unlit (basic) materials: NeutralToneMap(base); textured ones: NeutralToneMap(texture), alpha cut at 0.5.
import bpy, math, json, os, sys
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(bpy.data.filepath)
SCRIPT = os.path.dirname(os.path.abspath(__file__))
TOON = json.load(open(os.path.join(SCRIPT, '..', '..', 'kit', 'toon.json')))
GT = json.load(open(os.path.join(HERE, 'ats_toon.json')))
ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ONLY = None
OUTDIR = HERE
for a in ARGS:
    if a.startswith('only='): ONLY = a[5:].split(',')
    if a.startswith('out='): OUTDIR = os.path.join(HERE, a[4:]); os.makedirs(OUTDIR, exist_ok=True)
BLOCK = 'blockout' in ARGS
TEST = 'test' in ARGS
PI = math.pi
scn = bpy.context.scene
bpy.context.preferences.filepaths.save_version = 0

def s2l1(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def hex2srgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def s2l(h): return [s2l1(c) for c in hex2srgb(h)]
def neutral_tm(c):  # three.js r170 NeutralToneMapping, exposure 1
    c = list(c); x = min(c); off = x - 6.25 * x * x if x < 0.08 else 0.04
    c = [v - off for v in c]; peak = max(c)
    if peak < 0.76: return c
    d = 0.24; newp = 1 - d * d / (peak + d - 0.76); c = [v * newp / peak for v in c]
    g = 1 - 1 / (0.15 * (peak - newp) + 1); return [v * (1 - g) + newp * g for v in c]

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

def toon_tree(m, base_hex, bands):
    m.use_nodes = True; nt = m.node_tree; N, L = nt.nodes, nt.links; N.clear()
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    dif = N.new('ShaderNodeBsdfDiffuse'); dif.inputs['Color'].default_value = (1, 1, 1, 1)
    s2r = N.new('ShaderNodeShaderToRGB'); L.new(dif.outputs[0], s2r.inputs[0])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'; ramp.color_ramp.color_mode = 'RGB'
    els = ramp.color_ramp.elements
    while len(els) < len(bands): els.new(0.5)
    for el, (t, v) in zip(els, bands):
        el.position = max(0.0, t); el.color = (v[0] / 255, v[1] / 255, v[2] / 255, 1)
    L.new(s2r.outputs['Color'], ramp.inputs['Fac'])
    sunv = N.new('ShaderNodeVectorMath'); sunv.operation = 'MULTIPLY'; sunv.inputs[1].default_value = sun_lin
    L.new(ramp.outputs['Color'], sunv.inputs[0])
    geo = N.new('ShaderNodeNewGeometry'); sp = N.new('ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sp.inputs[0])
    w = N.new('ShaderNodeMath'); w.operation = 'MULTIPLY_ADD'; w.inputs[1].default_value = 0.5; w.inputs[2].default_value = 0.5
    L.new(sp.outputs['Z'], w.inputs[0])
    hv = N.new('ShaderNodeVectorMath'); hv.operation = 'SCALE'; hv.inputs[0].default_value = [s - g for s, g in zip(sky, gnd)]
    L.new(w.outputs[0], hv.inputs['Scale'])
    h2 = N.new('ShaderNodeVectorMath'); h2.operation = 'ADD'; h2.inputs[1].default_value = [g + a for g, a in zip(gnd, amb)]
    L.new(hv.outputs[0], h2.inputs[0])
    irr = N.new('ShaderNodeVectorMath'); irr.operation = 'ADD'; L.new(sunv.outputs[0], irr.inputs[0]); L.new(h2.outputs[0], irr.inputs[1])
    alb = N.new('ShaderNodeVectorMath'); alb.operation = 'MULTIPLY'; alb.inputs[1].default_value = [c / PI for c in s2l(base_hex)]
    alb.name = 'albedo'
    L.new(irr.outputs[0], alb.inputs[0])
    tm = N.new('ShaderNodeGroup'); tm.node_tree = TM; L.new(alb.outputs[0], tm.inputs[0])
    L.new(tm.outputs[0], em.inputs['Color']); L.new(em.outputs[0], out.inputs['Surface'])

def flat_tree(m, lin_rgb, cull=False):
    m.use_nodes = True; nt = m.node_tree; N = nt.nodes; N.clear()
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*lin_rgb, 1); nt.links.new(em.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = cull

MAPS = {}
def tex_tree(m, alpha):
    """Unlit textured: NeutralTM(texture). A Mapping node (named 'map') carries the game's UV offset / rotation."""
    img = None
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE': img = n.image
    nt = m.node_tree; N, L = nt.nodes, nt.links; N.clear()
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    uv = N.new('ShaderNodeUVMap'); mp = N.new('ShaderNodeMapping'); mp.name = 'map'; mp.vector_type = 'POINT'
    t = N.new('ShaderNodeTexImage'); t.image = img; t.extension = 'REPEAT'; t.interpolation = 'Linear'
    L.new(uv.outputs[0], mp.inputs['Vector']); L.new(mp.outputs[0], t.inputs['Vector'])
    tm = N.new('ShaderNodeGroup'); tm.node_tree = TM; L.new(t.outputs['Color'], tm.inputs[0]); L.new(tm.outputs[0], em.inputs['Color'])
    if alpha:
        gt = N.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.5; L.new(t.outputs['Alpha'], gt.inputs[0])
        tr = N.new('ShaderNodeBsdfTransparent'); mx = N.new('ShaderNodeMixShader')
        L.new(gt.outputs[0], mx.inputs[0]); L.new(tr.outputs[0], mx.inputs[1]); L.new(em.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs['Surface'])
    else: L.new(em.outputs[0], out.inputs['Surface'])
    MAPS[m.name] = mp

for m in list(bpy.data.materials):
    if 'hex' not in m.keys(): continue
    if m.get('image'): tex_tree(m, m.name in GT['alpha_materials'])
    elif m.name in GT['basic_materials']: flat_tree(m, neutral_tm(s2l(m['hex'])))
    else: toon_tree(m, m['hex'], GT['band_colors'][m.name])

def set_map(name, off=(0.0, 0.0), rot=0.0):
    """three.js texture.offset / rotation (centre 0.5, 0.5) -> the Blender Mapping node (UV v is flipped by glTF)."""
    mp = MAPS.get(name)
    if not mp: return
    c = math.cos(-rot); s = math.sin(-rot)
    # sample = R (uv - c) + c + o  in Blender uv (v up); three offset (ox, oy) on v_gltf = 1 - v  ->  (ox, -oy)
    cx, cy = 0.5, 0.5; lx = cx - (c * cx - s * cy) + off[0]; ly = cy - (s * cx + c * cy) - off[1]
    mp.inputs['Location'].default_value = (lx, ly, 0); mp.inputs['Rotation'].default_value = (0, 0, -rot)

INK = bpy.data.materials.new('outline_ink'); flat_tree(INK, neutral_tm(s2l(TOON['outline']['color'])), cull=True)
def add_outline(ob, width):
    n = len(ob.data.materials)
    skip = [i for i, mm in enumerate(ob.data.materials) if mm.name in GT['no_outline_materials']]
    vg = ob.vertex_groups.new(name='hull')
    keep = set()
    for p in ob.data.polygons:
        if p.material_index not in skip: keep.update(p.vertices)
    vg.add(list(keep), 1.0, 'REPLACE')
    for _ in range(n): ob.data.materials.append(INK)
    so = ob.modifiers.new('outline', 'SOLIDIFY')
    so.thickness = -width; so.offset = -1.0; so.use_flip_normals = True; so.use_rim = False
    so.material_offset = n; so.use_even_offset = False; so.use_quality_normals = True
    so.vertex_group = 'hull'; so.thickness_vertex_group = 0.0
for nm in GT['outline_nodes']:
    if nm in bpy.data.objects: add_outline(bpy.data.objects[nm], TOON['outline']['width_m'])

scn.render.engine = 'BLENDER_EEVEE_NEXT'
scn.eevee.taa_render_samples = 32
scn.view_settings.view_transform = 'Standard'; scn.view_settings.look = 'None'
scn.view_settings.exposure = 0; scn.view_settings.gamma = 1
scn.render.film_transparent = True
scn.render.filter_size = 1.2
world = bpy.data.worlds.new('w'); scn.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
BG_HEX = '#FDE6C8'
scn.use_nodes = True; ct = scn.node_tree; ct.nodes.clear()
rl = ct.nodes.new('CompositorNodeRLayers'); ao = ct.nodes.new('CompositorNodeAlphaOver'); co = ct.nodes.new('CompositorNodeComposite')
ao.inputs[1].default_value = (*s2l(BG_HEX), 1)
ct.links.new(rl.outputs['Image'], ao.inputs[2]); ct.links.new(ao.outputs[0], co.inputs[0])
el, az = math.radians(SUN['elev']), math.radians(SUN['az'])
Lt = Vector((math.sin(az) * math.cos(el), math.sin(el), math.cos(az) * math.cos(el)))
Lb = Vector((Lt.x, -Lt.z, Lt.y)).normalized()
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 1 / 0.254638671875
sd.angle = 0.0; sd.use_shadow = False; sd.color = (1, 1, 1)
so = bpy.data.objects.new('sun', sd); scn.collection.objects.link(so)
so.rotation_mode = 'QUATERNION'; so.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Lb)
cs = GT['contact_shadow']
bg_s = hex2srgb(BG_HEX); ink_s = hex2srgb(TOON['contact_shadow']['color'])
blob_s = [b * (1 - cs['opacity']) + i * cs['opacity'] for b, i in zip(bg_s, ink_s)]
bpy.ops.mesh.primitive_circle_add(vertices=40, radius=1.0, fill_type='NGON', location=(0.0, 0.0, -0.002))
blob = bpy.context.object; blob.name = 'contact_shadow'; blob.scale = (cs['rx'], cs['ry'], 1)
bm_ = bpy.data.materials.new('blob'); flat_tree(bm_, [s2l1(c) for c in blob_s]); blob.data.materials.append(bm_)
ROOT = bpy.data.objects['root']; blob.parent = ROOT

cam_d = bpy.data.cameras.new('cam'); cam_d.sensor_fit = 'VERTICAL'; cam_d.lens_unit = 'FOV'
cam = bpy.data.objects.new('cam', cam_d); scn.collection.objects.link(cam); scn.camera = cam
cam_d.clip_start = 0.05; cam_d.clip_end = 100
FLT = bpy.data.objects['float']
PIV = bpy.data.objects.get('stamp_pivot'); CV = bpy.data.objects.get('cv')
BALL = bpy.data.materials.get('ball')
U = FLT['unit_m']; HM = FLT['height_m']
ST = FLT['screen'].to_dict(); STAMP = FLT['stamp'].to_dict(); CVD = FLT['cv'].to_dict()
CV_REST = CV.location.copy() if CV else None
if CV: CV.hide_render = True

def set_state(screen='idle', scan='rest', theta=None, cv=None, cv_stamped=False, hub=0.0, belt=0.0, ant_on=True):
    set_map('screen', (0, ST['three_offset_y'][screen]))
    scan_y = ST['scan_three_offset_y'].get(scan, 0.0) if isinstance(scan, str) else scan
    set_map('scan', (0, scan_y))
    if 'scan' in MAPS:
        sc = bpy.data.objects['screen']
        idx = [i for i, mm in enumerate(sc.data.materials) if mm.name == 'scan']
        bpy.data.materials['scan'].node_tree.nodes['map'].mute = False
    SCAN_ON[0] = screen in ST['scan_visible_in']
    set_map('hub', rot=hub); set_map('belt', (belt, 0))
    if PIV: PIV.rotation_euler = (STAMP['sign'] * math.radians(STAMP['rest_deg'] if theta is None else theta), 0, 0)
    if CV:
        CV.hide_render = cv is None
        if cv is not None: CV.location = CV_REST + Vector(CVD['slide_axis_blender']) * CVD['travel_m'] * cv
        set_map('paper', (0.5 if cv_stamped else 0.0, 0))
    if BALL and 'albedo' in BALL.node_tree.nodes:
        k = 1.0 if ant_on else 0.62
        BALL.node_tree.nodes['albedo'].inputs[1].default_value = [c / PI * k for c in s2l(BALL['hex'])]
    # the scan line hides in found / notfit / loading (sheet SCREEN STATES): mute its material
    if 'scan' in bpy.data.materials:
        m = bpy.data.materials['scan']; out = [n for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'][0]
        mx = [n for n in m.node_tree.nodes if n.type == 'MIX_SHADER'][0]
        gt = [n for n in m.node_tree.nodes if n.type == 'MATH'][0]
        gt.inputs[1].default_value = 0.5 if SCAN_ON[0] else 2.0
    bpy.context.view_layer.update()
SCAN_ON = [True]

CROPS = {}
def W(X, y, Z):
    return ROOT.matrix_world @ Vector((X * U, -Z * U, (340 - y) * U))
def crop_points():
    pts = {'screen': W(0, 105, 35), 'neck': W(0, 175, 26), 'slot': W(0, 247, 50), 'hub': W(80, 224, 0),
           'antenna': W(-84, 20, -16), 'tread_L': W(64, 322, 8), 'tread_R': W(-64, 322, 8), 'head_top': W(0, 60, 0),
           'stamp_block': None, 'head_corner_L': W(88, 60, 34), 'body_crown': W(0, 200, 0)}
    if PIV:
        stp = bpy.data.objects['stamp']; pts['stamp_block'] = stp.matrix_world @ Vector((104 * U, 0, -90 * U))
    return {k: v for k, v in pts.items() if v is not None}

def shoot(name, w, h, angle_deg, cam_pos, target, fov=22, blob_on=True, compose=True, **state):
    if ONLY and name not in ONLY: return
    set_state(**state); ROOT.rotation_euler = (0, 0, math.radians(angle_deg))
    blob.hide_render = not blob_on
    cam.location = Vector(cam_pos); cam_d.angle_y = math.radians(fov)
    d = Vector(target) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    scn.render.resolution_x, scn.render.resolution_y = w, h; scn.render.resolution_percentage = 100
    scn.render.use_compositing = compose
    scn.render.image_settings.file_format = 'PNG'; scn.render.image_settings.color_mode = 'RGB' if compose else 'RGBA'
    scn.render.filepath = os.path.join(OUTDIR, name + '.png')
    bpy.ops.render.render(write_still=True); print("RENDERED", name)
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update(); CROPS[name] = {}
    for k, v in crop_points().items():
        p = world_to_camera_view(scn, cam, v); CROPS[name][k] = [round(p.x * w), round((1 - p.y) * h)]

S_ = HM / 1.25
TURN = ((0, -4.6 * S_, 0.80 * S_), (0, 0, 0.64 * S_))
if TEST:
    for i, s in enumerate(ST['states']):
        shoot('t-' + s, 600, 400, 0, (0, -1.6, 1.05), (0, 0, 1.00), fov=22, screen=s, scan='rest')
    shoot('t-34-hub', 600, 400, -60, (0, -1.6, 0.6), (0, 0, 0.30), fov=26, hub=0.8, belt=0.3)
else:
    for nm, ang in [('turn-front', 0), ('turn-34', -35), ('turn-side', -90), ('turn-back', 180)]:
        shoot(nm, 900, 1200, ang, *TURN)
    if not BLOCK:
        shoot('hero', 1200, 1200, -28, (0, -4.2 * S_, 1.62 * S_), (0, 0, 0.62 * S_))
        # stamp: side view (the arm side faces the camera), rest 45, wind-up 140, slam 0
        for k, th in (('rest', STAMP['rest_deg']), ('windup', STAMP['windup_deg']), ('slam', STAMP['slam_deg'])):
            shoot('stamp-' + k, 900, 1200, -90, *TURN, theta=th)
            shoot('stamp34-' + k, 900, 1200, 35, *TURN, fov=26, theta=th)
        # slot: a CV slides into the slot (pose view from above the lip, yaw 25)
        SLOTCAM = ((0, -3.2 * S_, 1.55 * S_), (0, 0, 0.42 * S_))
        for k, f, sc, stp in (('out', 0.0, 'idle', False), ('half', 0.5, 'reading', False), ('in', 1.0, 'reading', False), ('stamped', 0.0, 'notfit', True)):
            shoot('slot-' + k, 900, 1000, -25, *SLOTCAM, cv=f, screen=sc, scan='sweep_top' if sc == 'reading' else 'rest', cv_stamped=stp,
                  theta=0.0 if stp else None)
        # screens: the 5 states, close on the head; the scan line sweep (reading)
        HEADCAM = ((0, -2.0 * S_, 1.08 * S_), (0, 0, 1.03 * S_))
        for s in ST['states']:
            shoot('screen-' + s, 800, 560, -8, *HEADCAM, fov=24, screen=s)
        for k in ('sweep_top', 'rest', 'sweep_bottom'):
            shoot('scan-' + k, 800, 560, -8, *HEADCAM, fov=24, screen='reading', scan=k)
        # treads and antenna: hub spin, belt scroll, ball blink
        TRCAM = ((0, -2.4 * S_, 0.55 * S_), (0, 0, 0.18 * S_))
        shoot('tread-a', 900, 600, -55, *TRCAM, fov=24, hub=0.0, belt=0.0)
        shoot('tread-b', 900, 600, -55, *TRCAM, fov=24, hub=0.785, belt=0.5)
        ANTCAM = ((0, -1.7 * S_, 1.35 * S_), (0, 0, 1.13 * S_))
        shoot('ant-on', 600, 600, -20, *ANTCAM, fov=24, ant_on=True)
        shoot('ant-off', 600, 600, -20, *ANTCAM, fov=24, ant_on=False)
        shoot('_close-neck', 1200, 1200, -20, (0, -1.9 * S_, 0.95 * S_), (0, 0, 0.62 * S_))
        shoot('_close-top', 1200, 1200, -20, (0, -1.6 * S_, 2.30 * S_), (0, 0, 0.95 * S_))
        shoot('_mask-front', 900, 1200, 0, *TURN, blob_on=False, compose=False)
        shoot('_mask-34', 900, 1200, -35, *TURN, blob_on=False, compose=False)
    set_state()

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
    mpath = os.path.join(OUTDIR, mask_name + '.png')
    if not os.path.exists(mpath): return
    a = load_px(mpath)[..., 3]
    ys, xs = np.where(a > 0.5); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    crop = a[y0:y1, x0:x1]; nh = 64; nw = max(1, round((x1 - x0) * nh / (y1 - y0)))
    small = area_resize(crop, nh, nw); pad = 6; Wd = nw + 2 * pad
    out = np.ones((nh, Wd, 4), np.float32); v = 1 - small
    out[:, pad:pad + nw, 0] = v; out[:, pad:pad + nw, 1] = v; out[:, pad:pad + nw, 2] = v
    save_px(os.path.join(OUTDIR, out_name + '.png'), out)
    save_px(os.path.join(OUTDIR, out_name + '-x4.png'), np.repeat(np.repeat(out, 4, 0), 4, 1))
    os.remove(mpath); print('SIL', out_name, nw, nh)
silhouette('_mask-front', 'silhouette-64'); silhouette('_mask-34', 'silhouette-64-34')
tpath = os.path.join(OUTDIR, 'turn-34.png')
if os.path.exists(tpath) and not BLOCK and not TEST:
    p = load_px(tpath); lin = np.where(p[..., :3] <= 0.04045, p[..., :3] / 12.92, ((p[..., :3] + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    out = np.ones_like(p); out[..., 0] = out[..., 1] = out[..., 2] = s
    save_px(os.path.join(OUTDIR, 'grey.png'), out); print('GREY done')
old = {}
cp = os.path.join(OUTDIR, 'crop_points.json')
if os.path.exists(cp): old = json.load(open(cp))
old.update(CROPS); json.dump(old, open(cp, 'w'), indent=1)
