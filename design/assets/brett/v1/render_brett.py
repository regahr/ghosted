# GHOSTED - Brett renders (copied from auntie-dot/v1/render_dot.py). Opens brett.blend (made by build_brett.py), swaps the export materials
# for the toon shader, adds the ink outline, lights and cameras, and renders every sheet image.
# Run: Blender -b brett.blend -P render_brett.py [-- only=<name,...>] [blockout] [out=<dir>]
# Same toon formula, light, outline and contact shadow as Kit (assets/kit/render_kit.py, assets/kit/toon.json):
#   colour = NeutralToneMap( base * (band(N.L) * sun + hemi(N.up) + ambient) / pi )
# The only extension: a band can be a colour instead of a grey (ghost_toon.json). v6 keeps the neutral grey 178 band.
# ingame.html does the same with an RGB gradient map.
import bpy, math, json, os, sys
import numpy as np
from mathutils import Vector, Euler, Matrix, Quaternion

HERE = os.path.dirname(bpy.data.filepath)
SCRIPT = os.path.dirname(os.path.abspath(__file__))
TOON = json.load(open(os.path.join(SCRIPT, '..', '..', 'kit', 'toon.json')))
GT = json.load(open(os.path.join(HERE, 'brett_toon.json')))
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

def neutral_tm(c):  # three.js r170 NeutralToneMapping, exposure 1
    c = list(c); x = min(c); off = x - 6.25 * x * x if x < 0.08 else 0.04
    c = [v - off for v in c]; peak = max(c)
    if peak < 0.76: return c
    d = 0.24; newp = 1 - d * d / (peak + d - 0.76); c = [v * newp / peak for v in c]
    g = 1 - 1 / (0.15 * (peak - newp) + 1); return [v * (1 - g) + newp * g for v in c]

# ---------------------------------------------------------------- node group: Neutral tone mapping (copy of Kit's)
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
    """bands: [[threshold, [r, g, b] 0..255], ...]. Kit's tree, with the ramp colour multiplying the sun per channel
    (for a grey band this is exactly Kit's RGBToBW x sun)."""
    m.use_nodes = True; nt = m.node_tree; N, L = nt.nodes, nt.links; N.clear()
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    dif = N.new('ShaderNodeBsdfDiffuse'); dif.inputs['Color'].default_value = (1, 1, 1, 1)
    s2r = N.new('ShaderNodeShaderToRGB'); L.new(dif.outputs[0], s2r.inputs[0])
    ramp = N.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
    ramp.color_ramp.color_mode = 'RGB'
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
    if m.name in GT['basic_materials']: flat_tree(m, neutral_tm(s2l(m['hex'])))
    else: toon_tree(m, m['hex'], GT['band_colors'][m.name])
INK = bpy.data.materials.new('outline_ink'); flat_tree(INK, neutral_tm(s2l(TOON['outline']['color'])), cull=True)
def add_outline(ob, width):
    n = len(ob.data.materials)
    for _ in range(n): ob.data.materials.append(INK)
    so = ob.modifiers.new('outline', 'SOLIDIFY')
    so.thickness = -width; so.offset = -1.0; so.use_flip_normals = True; so.use_rim = False
    so.material_offset = n; so.use_even_offset = False; so.use_quality_normals = True
    ca = ob.data.color_attributes.get('outline_wc')
    if ca is not None:   # per-vertex outline width (Kit method): the neck ink fades where it enters the vest
        vals = [ca.data[i].color[0] for i in range(len(ob.data.vertices))]
        vg = ob.vertex_groups.new(name='outline_width')
        for i, w in enumerate(vals): vg.add([i], w, 'REPLACE')
        so.vertex_group = 'outline_width'; so.thickness_vertex_group = 0.0
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
cs = TOON['contact_shadow']
bg_s = hex2srgb(BG_HEX); ink_s = hex2srgb(cs['color'])
blob_s = [b * (1 - cs['opacity']) + i * cs['opacity'] for b, i in zip(bg_s, ink_s)]
bpy.ops.mesh.primitive_circle_add(vertices=40, radius=1.0, fill_type='NGON', location=(0.0, 0.0, -0.002))
blob = bpy.context.object; blob.name = 'contact_shadow'; blob.scale = (GT['contact_shadow']['rx'], GT['contact_shadow']['ry'], 1)
bm_ = bpy.data.materials.new('blob'); flat_tree(bm_, [s2l1(c) for c in blob_s]); blob.data.materials.append(bm_)
ROOT = bpy.data.objects['root']; blob.parent = ROOT


cam_d = bpy.data.cameras.new('cam'); cam_d.sensor_fit = 'VERTICAL'; cam_d.lens_unit = 'FOV'
cam = bpy.data.objects.new('cam', cam_d); scn.collection.objects.link(cam); scn.camera = cam
cam_d.clip_start = 0.05; cam_d.clip_end = 100
RIG = bpy.data.objects['rig']; FLT = bpy.data.objects['float']; BNC = bpy.data.objects['bounce']
BODY = bpy.data.objects['body']; DEC = bpy.data.objects['decals']
SWAP_NAMES = ('eyes_open', 'eyes_wink', 'brows_rest', 'brows_smug', 'brows_lost', 'mouth_grin', 'mouth_talk', 'mouth_wink', 'mouth_lost')
SWAPS = {k: bpy.data.objects.get(k) for k in SWAP_NAMES}
HANDS = {k: bpy.data.objects.get(k) for k in ('thumb', 'fingers_1', 'fingers_2', 'fingers_3')}
OUTDIR = HERE
for a in (sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []):
    if a.startswith('out='): OUTDIR = os.path.join(HERE, a[4:]); os.makedirs(OUTDIR, exist_ok=True)
H = FLT['height_m']; U = FLT['unit_m']; K = (H * 346.0 / 324.0) / 1.18      # cameras: Dot's frames scaled to Brett + halo

def pose(beat=None, frac=1.0, carry=False, puff=0.0, expr=None, hand=None):
    """name: idle / like / bullets (frac scales each arm angle: the in-between frames). carry: chin up 10 deg (the halo
    stays level). puff: 0..1 of the idle puff (torso -3 deg about the feet + rise 3 units). expr: rest / talk / wink /
    lost. hand: thumb / fingers_1..3 (swap parts)."""
    for pb in RIG.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    P = {k: list(v) for k, v in (FLT['poses_float_blender'][beat].to_dict().items() if beat else [])}
    for k in P: P[k][3] *= frac
    if carry: P.update({k: list(v) for k, v in FLT['carry_float_blender'].to_dict().items()})
    pf = FLT['puff'].to_dict()
    if puff: P['torso'] = list(pf['torso_float_blender'][:3]) + [pf['torso_float_blender'][3] * puff]
    for bn, v in P.items():
        x, y, z, deg = v; M = RIG.data.bones[bn].matrix_local.to_3x3().inverted()
        RIG.pose.bones[bn].rotation_quaternion = Quaternion(M @ Vector((x, y, z)), math.radians(deg))
    if puff: RIG.pose.bones['torso'].location = (0, pf['rise_m'] * puff, 0)
    bd = FLT['beat_defaults'].to_dict().get(beat or '', {})
    e = FLT['expressions'][expr or bd.get('expr', 'rest')]
    for k, o in SWAPS.items():
        if o: o.hide_render = k not in list(e)
    hd = hand if hand is not None else (bd.get('hand') if frac >= 0.999 else None)
    for k, o in HANDS.items():
        if o: o.hide_render = k != hd
    bpy.context.view_layer.update()

def bone_pt(bn, p):
    b = RIG.data.bones[bn]; pb = RIG.pose.bones[bn]
    return RIG.matrix_world @ pb.matrix @ (b.matrix_local.inverted() @ Vector(p))
def SK(X, y, Z): return Vector((X * U, -Z * U, (340 - y) * U))
CROPS = {}
def crop_points():
    pts = {}
    hp = lambda X, y, Z: bone_pt('head', SK(X, y, Z)); tp = lambda X, y, Z: bone_pt('torso', SK(X, y, Z))
    pts['face'] = hp(0, 100, 50); pts['mouth'] = hp(0, 114, 50); pts['eyeL'] = hp(18, 94, 50); pts['eyeR'] = hp(-18, 94, 50)
    pts['crown'] = hp(0, 40, 0); pts['swoop'] = hp(10, 36, 30); pts['halo'] = bone_pt('halo', SK(0, 0, 0))
    pts['earL'] = hp(55, 93, -4); pts['earR'] = hp(-55, 93, -4); pts['nape'] = hp(0, 125, -40); pts['part'] = hp(-22, 52, 40)
    pts['collar'] = tp(0, 156, 20); pts['vpoint'] = tp(0, 198, 30); pts['neck'] = tp(0, 150, 0); pts['hem'] = tp(0, 250, 20)
    for side in ('L', 'R'):
        up = RIG.data.bones['arm_%s_up' % side]; lo = RIG.data.bones['arm_%s_lo' % side]
        pts['shoulder' + side] = bone_pt('arm_%s_up' % side, up.head_local); pts['elbow' + side] = bone_pt('arm_%s_lo' % side, lo.head_local)
        pts['hand' + side] = bone_pt('arm_%s_lo' % side, lo.tail_local)
    pts['feet'] = bone_pt('body_root', SK(0, 330, 0)); pts['knee'] = bone_pt('body_root', SK(0, 298, 0))
    return pts

def shoot(name, w, h, angle_deg, cam_pos, target, fov=22, blob_on=True, compose=True, **pk):
    if ONLY and name not in ONLY: return
    pose(**pk); ROOT.rotation_euler = (0, 0, math.radians(angle_deg))
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

TURN = ((0, -4.0 * K, 0.74 * K), (0, 0, 0.60 * K))
BLOCK = 'blockout' in sys.argv
for nm, ang in [('turn-front', 0), ('turn-34', -35), ('turn-side', -90), ('turn-back', 180)]:
    shoot(nm, 900, 1200, ang, *TURN)
shoot('idle-rest', 900, 1200, 0, *TURN, beat='idle', carry=True)
shoot('like-front', 900, 1200, 0, *TURN, beat='like', carry=True)
shoot('bullets-3', 900, 1200, 0, *TURN, beat='bullets', carry=True, hand='fingers_3')
shoot('_mask-front', 900, 1200, 0, *TURN, blob_on=False, compose=False)
if not BLOCK:
    shoot('turn-34b', 900, 1200, 35, *TURN)
    shoot('hero', 1200, 1200, -28, (0, -4.0 * K, 1.45 * K), (0, 0, 0.60 * K), beat='idle', carry=True)
    shoot('idle-puff', 900, 1200, 0, *TURN, beat='idle', carry=True, puff=1.0)
    shoot('idle-settle', 900, 1200, 0, *TURN, beat='idle', carry=True, puff=0.5)
    shoot('idle-side', 900, 1200, -90, *TURN, beat='idle', carry=True, puff=1.0)
    shoot('like-mid', 900, 1200, 0, *TURN, beat='like', frac=0.5, carry=True)
    shoot('like-34', 900, 1200, -35, *TURN, beat='like', carry=True)
    shoot('like-side', 900, 1200, -90, *TURN, beat='like', carry=True)
    shoot('bullets-1', 900, 1200, 0, *TURN, beat='bullets', carry=True, hand='fingers_1')
    shoot('bullets-2', 900, 1200, 0, *TURN, beat='bullets', carry=True, hand='fingers_2')
    shoot('bullets-34', 900, 1200, -35, *TURN, beat='bullets', carry=True, hand='fingers_3')
    FACE = ((0, -1.30 * K, 1.02 * K), (0, 0, 0.86 * K))
    for nm, ex in (('expr-rest', 'rest'), ('expr-talk', 'talk'), ('expr-wink', 'wink'), ('expr-lost', 'lost')):
        shoot(nm, 900, 900, -10, *FACE, expr=ex)
    shoot('_close-face', 1200, 1200, -15, (0, -1.25 * K, 1.0 * K), (0, 0, 0.86 * K))
    shoot('_close-face-side', 1200, 1200, -90, (0, -1.25 * K, 0.9 * K), (0, 0, 0.86 * K))
    shoot('_close-halo', 1200, 1200, -20, (0, -1.3 * K, 1.35 * K), (0, 0, 0.98 * K), carry=True)
    shoot('_close-ear34', 1200, 1200, 35, (0, -1.3 * K, 0.95 * K), (0, 0, 0.86 * K))
    shoot('_close-ear34-far', 1200, 1200, -35, (0, -1.3 * K, 0.95 * K), (0, 0, 0.86 * K))
    shoot('_close-nape', 1200, 1200, 150, (0, -1.4 * K, 1.0 * K), (0, 0, 0.82 * K))
    shoot('_close-hands', 1200, 1200, -15, (0, -1.6 * K, 0.62 * K), (0, 0, 0.42 * K), beat='idle', carry=True)
    shoot('_close-like', 1200, 1200, -15, (0, -1.6 * K, 0.85 * K), (0, 0, 0.70 * K), beat='like', carry=True)
    shoot('_close-bullets', 1200, 1200, -15, (0, -1.6 * K, 0.80 * K), (0, 0, 0.62 * K), beat='bullets', carry=True, hand='fingers_3')
    shoot('_close-top', 1200, 1200, -20, (0, -1.1 * K, 2.1 * K), (0, 0, 0.80 * K), carry=True)
    shoot('_close-shoulder', 1200, 1200, -35, (0, -1.4 * K, 0.75 * K), (0, 0, 0.60 * K))
    shoot('_mask-34', 900, 1200, -35, *TURN, blob_on=False, compose=False)
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
    small = area_resize(crop, nh, nw); pad = 6; W = nw + 2 * pad
    out = np.ones((nh, W, 4), np.float32); v = 1 - small
    out[:, pad:pad + nw, 0] = v; out[:, pad:pad + nw, 1] = v; out[:, pad:pad + nw, 2] = v
    save_px(os.path.join(OUTDIR, out_name + '.png'), out)
    save_px(os.path.join(OUTDIR, out_name + '-x4.png'), np.repeat(np.repeat(out, 4, 0), 4, 1))
    os.remove(mpath); print('SIL', out_name, nw, nh)
silhouette('_mask-front', 'silhouette-64'); silhouette('_mask-34', 'silhouette-64-34')
tpath = os.path.join(OUTDIR, 'turn-34.png')
if os.path.exists(tpath) and not BLOCK:
    p = load_px(tpath); lin = np.where(p[..., :3] <= 0.04045, p[..., :3] / 12.92, ((p[..., :3] + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    out = np.ones_like(p); out[..., 0] = out[..., 1] = out[..., 2] = s
    save_px(os.path.join(OUTDIR, 'grey.png'), out); print('GREY done')
old = {}
cp = os.path.join(OUTDIR, 'crop_points.json')
if os.path.exists(cp): old = json.load(open(cp))
old.update(CROPS); json.dump(old, open(cp, 'w'), indent=1)
