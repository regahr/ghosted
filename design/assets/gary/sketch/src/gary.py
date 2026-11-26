"""Gary the pigeon postman sketch: designed curves -> a toy 3D sketch model -> any view.

Reuses the Juno sketch library chain (assets/juno/sketch/src/juno.py -> Ricky library: Bezier profiles, round
bodies, mark lifting, camera; Dot render with per-part poses).

World: X right, H up (H = GROUND - y in the front frame), Z toward the viewer at yaw 0. Front frame: y down, axis
x 150, sole y 340. Metres per unit are set in build.py (standing height to the cap top = 0.5 x Kit).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ASSETS, "juno", "sketch", "src"))
import juno as J  # noqa: E402
from juno import (GROUND, Part, revolved, ellipsoid, tube, profile, r_at, cam, oval, text, svg_doc,  # noqa
                  render, pbounds, rot_x, rot_z, chain, INK, CREAM, NOTE, shade, SHADE_K)
from dot import split  # noqa: E402
from ricky import poly, hull, line, path_points, LIGHT  # noqa: E402

ROW = {
    5: "#7A4A2E", 7: "#D4503A", 8: "#A8C4DC", 9: "#3D6B99", 10: "#C9A6D6", 13: "#F0B43C", 18: "#8E9BA8",
    22: "#2B1E16", 23: "#FFF8EE", 24: "#E9D3B4", 26: "#2F3E5C",
}

# ---------------------------------------------------------------- body map numbers (world H, front frame y = 340 - H)
HEAD_C = (0.0, 160.0, 14.0)      # head centre (X, H, Z); head radius 38
HEAD_R = 38.0
HEAD_HALF = "M150,142 C175,142 188,159 188,180 C188,202 174,218 150,218"   # round head, y 142-218
CAP_HALF = "M150,131 C168,131 183,132 184,136 C184,140 181,146 178,152 L150,152"  # kepi: flat top, tapered band
CAP_PEAK_HALF = "M150,128 C172,128 192,129 193,133 C193,137 186,141 180,146 L178,152 L150,152"  # wide postal cap
BODY_C = (0.0, 78.0, 0.0)
BODY_R = (58.0, 54.0, 74.0)
BODY_TILT = -22.0                # front up, tail end down
LM = {
    "cap_top": 209, "head_top": 198, "cap_band": 188, "brow": 170, "eye": 164, "beak": 148, "chin": 122,
    "neck": 128, "wing_root": 106, "chest": 112, "belly": 52, "tail": 60, "knee": 30, "sole": 0,
}
EYE_X = (135, 165)
EAR_X = 37.0                     # ear points: on the eye line at the head sides (under the feathers)
# face marks, front frame
EYE_Y = 340 - LM["eye"]          # 176
BROWS = ["M127,164 C130,161 136,160 141,161", "M159,161 C164,160 170,161 173,164"]
BROWS_SORRY = ["M127,163 C131,163 136,160 141,156", "M159,156 C164,160 169,163 173,163"]
BROWS_UP = ["M127,160 C130,155 136,154 141,156", "M159,156 C164,154 170,155 173,160"]
HAPPY_EYES = ["M129,179 C131,171 139,171 141,179", "M159,179 C161,171 169,171 171,179"]
HALF_LIDS = ["M128.5,174 C132,172 138,172 141.5,174", "M158.5,174 C162,172 168,172 171.5,174"]
CHEEKS = [(127, 190), (173, 190)]

WING_ARM, WING_HAND = 70.0, 100.0    # rigid segments: root -> wrist -> tip; span = 2 x (44 + 70 + 100) = 428 u
WING_ROOT = (44.0, 106.0, 2.0)


# ---------------------------------------------------------------- small vector helpers
def add(a, b, k=1.0):
    return (a[0] + k * b[0], a[1] + k * b[1], a[2] + k * b[2])


def nrm(v):
    ln = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / ln for c in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dotp(a, b):
    return sum(x * y for x, y in zip(a, b))


def basis(ex, ey_hint):
    """Orthonormal basis: ex = length axis, ey ~ thickness axis, ez = the third (chord)."""
    ex = nrm(ex)
    ey = nrm(add(ey_hint, ex, -dotp(ey_hint, ex)))
    ez = cross(ex, ey)
    return ex, ey, ez


def brot(B):
    ex, ey, ez = B
    return lambda x, y, z: (x * ex[0] + y * ey[0] + z * ez[0], x * ex[1] + y * ey[1] + z * ez[1],
                            x * ex[2] + y * ey[2] + z * ez[2])


def rx(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return lambda x, y, z: (x, y * c - z * s, y * s + z * c)


def ry_pt(a, pivot=(0.0, 0.0, 0.0)):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))

    def f(q):
        x, y, z = q[0] - pivot[0], q[1] - pivot[1], q[2] - pivot[2]
        return (x * c + z * s + pivot[0], y + pivot[1], -x * s + z * c + pivot[2])
    return f


def translate(dx, dy, dz):
    return lambda q: (q[0] + dx, q[1] + dy, q[2] + dz)


def body_surface(d, out=0.0, c=BODY_C, r=BODY_R, tilt=BODY_TILT):
    """The point on the tilted body ellipsoid in world direction d from its centre, pushed out by `out`."""
    inv = rx(-tilt)
    lx, ly, lz = inv(*d)
    k = math.sqrt((lx / r[0]) ** 2 + (ly / r[1]) ** 2 + (lz / r[2]) ** 2)
    p = rx(tilt)(lx / k, ly / k, lz / k)
    n = nrm(p)
    return (c[0] + p[0] + out * n[0], c[1] + p[1] + out * n[1], c[2] + p[2] + out * n[2])


def fbox(name, color, c, w, h, d, bias=0.0, ink=True):
    """A box, one piece per face (own normal), back faces culled (Panel sketch)."""
    x, y, z = c
    hw, hh, hd = w / 2, h / 2, d / 2
    V = lambda sx, sy, sz: (x + sx * hw, y + sy * hh, z + sz * hd)
    faces = [((0, 1, 0), [V(-1, 1, -1), V(1, 1, -1), V(1, 1, 1), V(-1, 1, 1)]),
             ((0, -1, 0), [V(-1, -1, -1), V(1, -1, -1), V(1, -1, 1), V(-1, -1, 1)]),
             ((0, 0, 1), [V(-1, -1, 1), V(1, -1, 1), V(1, 1, 1), V(-1, 1, 1)]),
             ((0, 0, -1), [V(-1, -1, -1), V(1, -1, -1), V(1, 1, -1), V(-1, 1, -1)]),
             ((1, 0, 0), [V(1, -1, -1), V(1, 1, -1), V(1, 1, 1), V(1, -1, 1)]),
             ((-1, 0, 0), [V(-1, -1, -1), V(-1, 1, -1), V(-1, 1, 1), V(-1, -1, 1)])]
    p = Part(name, color, [f for _, f in faces], [[n] * 4 for n, _ in faces], bias=bias, ink=ink)
    p.cull_from = 0
    return p


def envelope(f, stamp=ROW[7], bias=1.2):
    """The envelope (swap part): 50 x 34 u card, a stamp at the top right, a V flap line. f: local -> world."""
    env = fbox("env", ROW[23], (0, 0, 0), 50, 34, 2.5, bias=bias)
    st = fbox("stamp", stamp, (15, 8, 1.2), 11, 12, 1.0, bias=bias + 0.05, ink=False)
    flap = tube("flap", INK, [(-23, 15, 1.6), (0, 1, 1.6), (23, 15, 1.6)], [0.9, 0.9, 0.9], n=6, bias=bias + 0.1)
    for p in (env, st, flap):
        p.pxf = f
    return [env, st, flap]


# ---------------------------------------------------------------- wings
def wing(s, pose, color, flap=0.0):
    """One wing (side s = -1 his right / viewer left at yaw 0, +1 his left). Two rigid segments, arm and hand, and 3
    finger feathers at the tip. pose: fold, spread (flap = degrees up), hold (reach forward, tip in front of the chest),
    half (hop balance), box (BMGD literal). Returns (parts, tip point, tip direction)."""
    root = (s * WING_ROOT[0], WING_ROOT[1], WING_ROOT[2])
    if pose == "box":
        p = fbox("wing", color, (s * 60, 86, -6), 12, 40, 70, bias=0.6)
        return [p], (s * 66, 66, -40), (0, 0, -1)
    if pose == "fold":
        root = (s * 47, 108, -8)
        da = nrm((s * 0.10, -0.34, 0.93))
        dh = nrm((s * 0.05, -0.13, -0.99))
        th_a = th_h = (s * 1.0, 0.0, 0.0)
        arm_len, hand_len = WING_ARM, WING_HAND
    elif pose in ("spread", "half"):
        a = math.radians(flap)
        da = dh = (s * math.cos(a), math.sin(a), -0.12)
        th_a = th_h = (-s * math.sin(a), math.cos(a), 0.0)
        arm_len, hand_len = WING_ARM, WING_HAND
    elif pose == "hold":
        da = nrm((s * 0.20, 0.02, 0.98))
        dh = nrm((-s * 0.92, -0.12, 0.38))
        th_a = (s * 1.0, 0.0, 0.0)
        th_h = (0.0, 1.0, 0.0)
        arm_len, hand_len = WING_ARM, WING_HAND
    da, dh = nrm(da), nrm(dh)
    wrist = add(root, da, arm_len)
    tip = add(wrist, dh, hand_len)
    out = []
    arm = ellipsoid("wing", color, add(root, da, arm_len / 2), (arm_len / 2 + 8, 6.5, 19), n=12,
                    rot=brot(basis(da, th_a)), bias=0.5)
    hand = ellipsoid("wing", color, add(wrist, dh, hand_len / 2 - 6), (hand_len / 2 + 2, 5.5, 16), n=12,
                     rot=brot(basis(dh, th_h)), bias=0.55 if pose != "fold" else 0.62)
    out += [arm, hand]
    B = basis(dh, th_h)
    for k, ang in enumerate((-24, 0, 24)):
        a = math.radians(ang)
        d = nrm(add(tuple(c * math.cos(a) for c in B[0]), tuple(c * math.sin(a) for c in B[2])))
        c0 = add(add(tip, dh, -12), d, 12)
        out.append(ellipsoid("feather", color, c0, (13, 4.2, 6.5), n=8, rot=brot(basis(d, th_h)),
                             bias=0.56 if pose != "fold" else 0.63))
    return out, add(tip, dh, 4), dh


# ---------------------------------------------------------------- the model
def model(o=None):
    """Build Gary. o: options for thumbnails, expressions and poses."""
    o = dict(o or {})
    C = {"body": ROW[8], "head": ROW[8], "wing": ROW[9], "tail": ROW[9], "beak": ROW[13], "feet": ROW[13],
         "cap": ROW[26], "brim": ROW[22], "bag": ROW[5], "strap": ROW[5], "badge": ROW[23]}
    C.update(o.get("colors", {}))
    body_k = o.get("body", "egg")        # egg (tilted), sphere (BMGD), pear (upright)
    head_k = o.get("head_k", 1.0)
    cap_k = o.get("cap", "kepi")         # kepi, peak, visor, none
    bag_k = o.get("bag", "front")        # front, side, none
    wings_k = o.get("wings", "fold")     # fold, spread, half, hold, box
    flap = o.get("flap", 0.0)
    env_k = o.get("env", "none")         # none, beak, wing, bag
    face = o.get("face", "rest")         # rest, happy, sorry, oops, blink
    legs = o.get("legs", "stand")        # stand, tuck
    tilt = o.get("head_tilt", 0.0)
    nod = o.get("head_nod", 0.0)
    parts = []

    # ---- body
    if body_k == "sphere":
        bc, br, bt = (0.0, 84.0, 0.0), (62.0, 62.0, 62.0), 0.0
    elif body_k == "pear":
        bc, br, bt = (0.0, 82.0, 4.0), (56.0, 66.0, 58.0), -6.0
    else:
        bc, br, bt = BODY_C, BODY_R, BODY_TILT
    parts.append(ellipsoid("body", C["body"], bc, br, n=16, rot=rx(bt)))
    bs = lambda d, out=0.0: body_surface(d, out, bc, br, bt)

    # ---- tail: a flat fan, low at the back
    if body_k != "sphere":
        parts.append(ellipsoid("tail", C["tail"], (0, bc[1] - 22, bc[2] - br[2] - 8), (30, 7, 34), n=10,
                               rot=rx(-18), bias=-1.0))
    # ---- neck + head (head pose: tilt about Z at the neck, nod about X)
    hc = (HEAD_C[0], HEAD_C[1], HEAD_C[2])
    piv = (0, LM["neck"], 10)
    hf = chain(rot_x(nod, piv), rot_z(tilt, piv))
    neck = ellipsoid("neck", C["body"], (0, 128, 12), (31, 26, 31), n=12, bias=0.1)
    neck.ink = False                     # blends head into body: no collar line
    parts.append(neck)
    head = revolved("head", C["head"], HEAD_HALF, depth=0.95, cz=hc[2], step=3, rscale=head_k,
                    lift=(1 - head_k) * 30, bias=0.3)
    head.pxf = hf
    marks = []
    if face == "happy":
        marks += [("line", d, None, INK, 3.4) for d in HAPPY_EYES]
    elif face == "blink":
        marks += [("line", d, None, INK, 3.0) for d in HALF_LIDS]
    else:
        er = (6.5, 8.5) if face != "oops" else (7.5, 9.5)
        for x in EYE_X:
            marks.append(("fill", oval(x, EYE_Y, *er), INK, None, 0))
            marks.append(("fill", oval(x + 2, EYE_Y - 3.2, 2.0, 2.4), ROW[23], None, 0))
        if face == "sorry":
            marks += [("line", d, None, INK, 2.4) for d in HALF_LIDS]
    brows = {"sorry": BROWS_SORRY, "oops": BROWS_UP}.get(face, BROWS)
    marks += [("line", d, None, INK, 2.4) for d in brows]
    head.marks = marks
    parts.append(head)

    # beak: a gold cone from the face, pointing forward and a little down (no mouth: the beak is the only thing below
    # the eyes)
    hz = hc[2] + HEAD_R * 0.95 * head_k
    hl = (1 - head_k) * 30
    beak = tube("beak", C["beak"], [(0, 150 + hl, hz - 6), (0, 147 + hl, hz + 6), (0, 142 + hl, hz + 18),
                                    (0, 137 + hl, hz + 28)], [8.5, 7.0, 4.0, 0.8], n=12, bias=0.9)
    beak.pxf = hf
    parts.append(beak)
    cere = ellipsoid("cere", ROW[23], (0, 154 + hl, hz - 1), (5.5, 3.2, 4), n=8, bias=0.95)
    cere.pxf = hf
    parts.append(cere)

    # ---- cap: set back on the crown, tilted back 14 deg so its front edge stays above the brows
    if cap_k != "none":
        top = hc[1] + HEAD_R * head_k + hl          # head top H
        piv_c = (0, top - 10, hc[2])
        cf = chain(rot_x(-14, piv_c), hf)
        lift = top - 10 - (GROUND - 152)            # band bottom sits 10 u under the head top
        if cap_k in ("kepi", "peak"):
            cp = revolved("cap", C["cap"], CAP_HALF if cap_k == "kepi" else CAP_PEAK_HALF, depth=1.0, cz=hc[2],
                          step=2, lift=lift, bias=1.0)
            cp.pxf = cf
            parts.append(cp)
        bh = top - 10
        brim = ellipsoid("brim", C["brim"], (0, bh + 1.5, hc[2] + 27), (21, 2.6, 12), n=10, rot=rx(-6), bias=1.1)
        brim.pxf = cf
        parts.append(brim)
        if cap_k in ("kepi", "peak"):
            badge = ellipsoid("badge", C["badge"], (0, bh + 11, hc[2] + 29.5), (6.5, 4.6, 1.8), n=8, rot=rx(-4),
                              bias=1.15)
            badge.pxf = cf
            parts.append(badge)

    # ---- wings
    tips = {}
    for s in (-1, 1):
        pose = wings_k
        if wings_k == "hold" and s == 1:
            pose = "fold"
        if wings_k == "spread" or wings_k == "half":
            wp, tp, td = wing(s, "spread", C["wing"], flap)
        else:
            wp, tp, td = wing(s, pose, C["wing"], flap)
        parts += wp
        tips[s] = (tp, td)

    # ---- legs and feet (gold)
    for s in (-1, 1):
        if legs == "tuck":
            parts.append(tube("leg", C["feet"], [(s * 15, 34, -4), (s * 15, 24, -24)], [3.6, 3.2], n=8, bias=-2))
            parts.append(ellipsoid("foot", C["feet"], (s * 15, 22, -32), (6, 3.5, 9), n=8, bias=-2))
        else:
            parts.append(tube("leg", C["feet"], [(s * 17, 32, 6), (s * 17, 5, 10)], [3.8, 3.4], n=8, bias=-3))
            parts.append(ellipsoid("foot", C["feet"], (s * 17, 4, 17), (8.5, 3.6, 12), n=8, bias=-2.5))

    # ---- mail bag: on his left belly front, strap round the body over his right shoulder
    if bag_k != "none":
        if bag_k == "front":
            bp = bs(nrm((0.42, -0.42, 0.80)), 9)
            yaw_b = 24
        else:
            bp = bs(nrm((0.95, -0.30, 0.10)), 10)
            yaw_b = 80
        bf = chain(ry_pt(yaw_b), translate(*bp))
        bag = fbox("bag", C["bag"], (0, 0, 0), 38, 30, 15, bias=1.3)
        bag.pxf = bf
        flapb = fbox("bagflap", C["bag"], (0, 8.5, 8.6), 39, 15, 2.2, bias=1.35)
        flapb.pxf = bf
        parts += [bag, flapb]
        if env_k == "bag":
            pe = fbox("env", ROW[23], (-6, 17, 0), 26, 16, 2, bias=1.32)
            pe.pxf = bf
            parts.append(pe)
        # the strap: a loop in the plane through his right shoulder and left hip (holds the Z axis)
        u = nrm((1.0, -1.15, 0.0))
        v = (0.0, 0.0, 1.0)
        pts = []
        for k in range(37):
            t = 2 * math.pi * k / 36
            d = nrm(add(tuple(c * math.cos(t) for c in u), tuple(c * math.sin(t) for c in v)))
            pts.append(bs(d, 2.0))
        strap = tube("strap", C["strap"], pts, [2.6] * len(pts), n=6, bias=0.2)
        parts += split(strap)            # one part per segment: the back half hides behind the body

    # ---- envelope (swap part)
    if env_k == "beak":
        f = chain(rx_pt(-35), translate(0, 125 + hl, hz + 30))
        for p in envelope(f):
            p.pxf = chain(f, hf)
            parts.append(p)
    elif env_k == "wing":
        tp, td = tips[-1]
        f = chain(rx_pt(-38), translate(tp[0] + 2, tp[1] + 6, tp[2] + 6))
        parts += envelope(f, bias=1.6)
    return parts


def rx_pt(a, pivot=(0.0, 0.0, 0.0)):
    r = rx(a)

    def f(q):
        x, y, z = r(q[0] - pivot[0], q[1] - pivot[1], q[2] - pivot[2])
        return (x + pivot[0], y + pivot[1], z + pivot[2])
    return f


def posed(parts, lift=0.0, pitch=0.0, pivot=(0.0, 90.0, 0.0)):
    """The whole bird: pitch (deg, + = nose down) about the body centre, then lift (hop / flight height)."""
    f = chain(rx_pt(pitch, pivot), translate(0, lift, 0))
    for p in parts:
        p.pxf = chain(getattr(p, "pxf", None), f)
    return parts


def gary(o=None):
    o = dict(o or {})
    return posed(model(o), o.get("lift", 0.0), o.get("pitch", 0.0))
