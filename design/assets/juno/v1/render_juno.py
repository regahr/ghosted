# GHOSTED - Juno renders (copied from brett/v1/render_brett.py). Opens juno.blend (made by build_juno.py), swaps the export materials
# for the toon shader, adds the ink outline, lights and cameras, and renders every sheet image.
# Run: Blender -b juno.blend -P render_juno.py [-- only=<name,...>] [blockout] [out=<dir>]
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
GT = json.load(open(os.path.join(HERE, 'juno_toon.json')))
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

