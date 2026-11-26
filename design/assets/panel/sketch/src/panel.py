"""The Panel sketch: table + Ms. Culture Fit + Mr. Whiteboard + the Camera-Off One, as a toy-pawn 3D sketch model.

Reuses the Juno sketch (assets/juno/sketch/src/juno.py: head, hair cap, face curves), the Ricky library (Bezier
profiles, round bodies, camera), the Dot render (per-part poses) and the Brett hair cap.

World units: 1 u = 1/300 m (as Juno v1, 3.333 mm). H = height above the floor, z toward the viewer at yaw 0.
Each person is drawn in Juno's front frame (sole y 340) and lifted by DH onto the chair behind the table.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ASSETS, "juno", "sketch", "src"))
import juno as J  # noqa: E402
from juno import (GROUND, Part, revolved, ellipsoid, tube, profile, r_at, cam, oval, text, svg_doc,  # noqa
                  render, pbounds, rot_x, rot_z, chain, hair_cap, hair_back, HEAD_HALF, CAP_HALF, HAIRLINE, FACE,
                  BROWS, SMILE, LAUGH, LAUGH_TEETH, TALK, TALK_TEETH, CHEEKS, INK, CREAM, NOTE, shade)
from ricky import poly, hull, LIGHT  # noqa: E402

M_PER_U = 1 / 300.0
ROW = {
    5: "#7A4A2E", 6: "#F4A672", 8: "#A8C4DC", 9: "#3D6B99", 10: "#C9A6D6", 12: "#FFE8A6", 15: "#F2C79E",
    17: "#2E2C3D", 21: "#B23A26", 22: "#2B1E16", 23: "#FFF8EE", 24: "#E9D3B4", 25: "#4A3226", 26: "#2F3E5C",
    2: "#7FA65A", 4: "#E59F64", 11: "#7A5596", 18: "#8E9BA8",
}

# ---------------------------------------------------------------- the set layout (world units)
TABLE_W, TABLE_D, TABLE_T = 600, 180, 30       # 2.0 x 0.6 x 0.1 m (BMGD hint)
TABLE_TOP = 220                                 # 0.733 m = 0.75 x Kit 0.977 m (chair call)
SEAT_Z = -140                                   # torso axis, 50 u behind the table back edge (z -90)
DH = 90                                         # person lift: Juno-frame H + 90 = world H
SEATS = {"cf": -200, "wb": 0, "box": 200}       # left to right at the front view
BOX = (100, 90, 80)                             # the Camera-Off One: 0.33 x 0.30 x 0.27 m
BOX_Z = -40

# person-frame landmarks (Juno front frame, y down, sole 340) -> world H = 340 - y + DH
LM = {"head_top": 58, "crown": 52, "hairline": 64, "brow": 88, "eye": 104, "mouth": 130, "chin": 154,
      "neck": 162, "shoulder": 186, "table": 340 - (TABLE_TOP - DH), "seat": 340 - (150 - DH)}
LOCAL_TABLE_H = TABLE_TOP - DH                  # 130
LOCAL_BACK_Z = -90 - SEAT_Z                     # 50: the table back edge in the person frame

BODY_CF = "M162,158 C186,160 204,168 210,184 C216,200 214,226 210,250 C208,262 196,268 182,268 L150,268"
BODY_WB = "M160,158 C192,158 212,163 214,178 L212,256 C212,264 204,268 190,268 L150,268"
BODY_SPHERE = "M150,150 C186,150 210,176 210,212 C210,250 186,268 150,268"   # BMGD literal (explore)
BODY_D = 0.78

# face marks (Juno front frame). Mouths sit 5 u higher than Juno's: at pitch 42 a seated head shows less chin, so
# the mouth keeps a clear skin gap above the chin outline (no beard read).
MOUTH_UP = 5.0
HEAD_SET = -8.0   # rest: the head is set chin-up 8 deg (attentive); at pitch 42 this keeps skin between mouth and chin


def up5(d):
    out, k = [], 0
    for t in re.split(r"([ ,MCLZ])", d):
        if re.fullmatch(r"-?\d+(\.\d+)?", t or ""):
            out.append(t if k % 2 == 0 else f"{float(t) - MOUTH_UP:g}")
            k += 1
        else:
            out.append(t)
    return "".join(out)


SMILE, LAUGH, LAUGH_TEETH, TALK, TALK_TEETH = (up5(d) for d in (SMILE, LAUGH, LAUGH_TEETH, TALK, TALK_TEETH))
FLAT = up5("M141,129 C147,130.5 153,130.5 159,129")                      # Whiteboard rest: a closed flat line
SMIRK_R = up5("M141,130 C147,131.5 154,131 160,126")                      # one corner up
BROWS_WB = ["M120,88 L141,86", "M159,86 L180,88"]                    # straight, heavier
BROWS_WB_UP = ["M120,86 C126,80 135,79 141,82", "M159,86 L180,88"]   # skeptical: one brow up
BROWS_CF_TILT = ["M121,86 C126,81 135,80 141,83", "M159,87 C165,84 174,85 179,89"]
GLASSES = [oval(132, 104, 13, 11), oval(168, 104, 13, 11), "M145,102 C147,99.5 153,99.5 155,102",
           "M119,102 L101,99", "M181,102 L199,99"]
HAPPY_EYES = J.HAPPY_EYES
V_CF = "M136,160 L164,160 L150,190 Z"                                # cream blouse V
CF_BUTTONS = [(150, 200), (150, 216)]
WB_V = "M138,160 L162,160 L150,184 Z"                                # light-blue shirt V under the vest
WB_COLLAR = ["M150,166 L136,158 L131,170 L143,176 Z", "M150,166 L164,158 L169,170 L157,176 Z"]
WB_POCKET = "M164,190 L184,190 L184,206 L164,206 Z"
WB_PENS = [("M169,184 L169,196", 21), ("M177,184 L177,196", 9)]


def translate(dx, dy, dz):
    return lambda q: (q[0] + dx, q[1] + dy, q[2] + dz)


def fbox(name, color, c, w, h, d, bias=0.0, ink=True):
    """A box with one piece per face (own normal: toon top vs sides), back faces culled."""
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


def cap_arcs(capd, color, ylow):
    """The hair cap (skull down to the temple line) as ring ARCS, back-facing arcs culled. The Juno / Brett cap uses
    full rings: once the head tips back, the rear of the lowest ring shows across the eyes."""
    prof = profile(capd)
    rings = []
    y = prof[0][0]
    while y <= ylow:
        r = r_at(prof, y)
        rx, rz = max(r, 0.5), max(r * 0.92, 0.5)
        pts, nrm = [], []
        for k in range(41):
            a = 2 * math.pi * k / 40
            sa, ca = math.sin(a), math.cos(a)
            pts.append((rx * sa, GROUND - y, rz * ca))
            nrm.append((sa, 0.35, ca))
        rings.append((pts, nrm))
        y += 3
    pieces, normals = [], []
    for (p0, n0), (p1, n1) in zip(rings, rings[1:]):
        for c in range(8):
            a, b = c * 5, c * 5 + 6
            pieces.append(p0[a:b] + p1[a:b])
            normals.append(n0[a:b] + n1[a:b])
    p = Part("hair", color, pieces, normals, bias=0.5)
    p.after = "head"
    p.cull_from = 0
    p.host = {"prof": prof, "depth": 0.92, "cx": 0.0, "cz": 0.0, "rscale": 1.0, "sy": 1.0, "lift": 0.0}
    return p


# ---------------------------------------------------------------- one seated person (Juno front frame)
def person(who, o):
    """who: 'cf' or 'wb'. o: face, head_nod, head_tilt, arms, lean, hair, body. Returns (low, up) part lists."""
    face = o.get("face", "rest")
    nod, tilt = o.get("head_nod", HEAD_SET), o.get("head_tilt", 0.0)
    hf = chain(rot_x(nod, (0, GROUND - LM["chin"], 0)), rot_z(tilt, (0, GROUND - LM["chin"] - 6, 0)))
    C = {"skin": ROW[15]}
    if who == "cf":
        C.update(top=ROW[10], inner=ROW[12], hair=ROW[25], acc=ROW[12], legs=ROW[26])
    else:
        C.update(top=ROW[26], inner=ROW[8], hair=ROW[25], acc=ROW[21], legs=ROW[26])
    C.update(o.get("colors", {}))
    hair = o.get("hair", "bow" if who == "cf" else "flattop")
    up, low = [], []

    # head + hair cap + face marks
    head = revolved("head", C["skin"], HEAD_HALF, depth=0.92, step=3)
    head.flat = True
    head.pxf = hf
    up.append(head)
    if hair == "sphere":                      # BMGD literal: a bare sphere head with a face
        cap = revolved("hair", C["skin"], CAP_HALF, depth=0.92, step=3)
        cap.host = cap.host
        marks = []
        cap.face_host = cap.host
    else:
        cap = cap_arcs(CAP_HALF, C["hair"], 86 + 2)
        marks = [("face", FACE, C["skin"], None, 0), ("line", HAIRLINE, None, INK, 2.2)]
        cap.face_host = cap.host
    for (x, y) in CHEEKS:
        if who == "cf":
            marks.append(("fill", oval(x, y + 2, 7, 4), ROW[6], None, 0))
    if who == "cf":
        brows = BROWS_CF_TILT if face == "tilt" else BROWS
    else:
        brows = BROWS_WB_UP if face == "skeptic" else BROWS_WB
    marks += [("line", d, None, INK, 2.8 if who == "wb" else 2.6) for d in brows]
    if face == "grin" and who == "cf":
        marks += [("line", d, None, INK, 3.4) for d in HAPPY_EYES]
    else:
        for x in (132, 168):
            marks.append(("fill", oval(x, 104, 6.5, 8.5), INK, None, 0))
            marks.append(("fill", oval(x + 2, 100.8, 2.0, 2.4), ROW[23], None, 0))
    if who == "wb" and hair != "sphere":
        marks += [("line", d, None, INK, 2.2) for d in GLASSES]
    if face == "grin":
        marks += [("fill", LAUGH, INK, None, 0), ("fill", LAUGH_TEETH, ROW[23], None, 0)]
    elif face == "talk":
        marks += [("fill", TALK, INK, None, 0), ("fill", TALK_TEETH, ROW[23], None, 0)]
    elif face in ("tilt", "skeptic"):
        marks.append(("line", SMIRK_R, None, INK, 2.8))
    elif who == "wb":
        marks.append(("line", FLAT, None, INK, 2.8))
    else:
        marks.append(("line", SMILE, None, INK, 2.8))
    cap.marks = marks
    cap.pxf = hf
    up.append(cap)
    if hair != "sphere":
        hb = hair_back(CAP_HALF, C["hair"], 86)
        cap.pieces += hb.pieces
        cap.normals += hb.normals
    for s in (-1, 1):
        e = ellipsoid("ear", C["skin"], (s * 55, GROUND - 105, -4), (5, 10, 7))
        e.pxf = hf
        up.append(e)
    if hair == "bow":       # low bun at the nape + a cream headband with a bow centred on the crown
        b = ellipsoid("bun", C["hair"], (0, GROUND - 128, -54), (24, 22, 20), bias=-0.5)
        b.pxf = hf
        up.append(b)
        hc = GROUND - 106
        pts = [(58.5 * math.sin(math.radians(a)), hc + 57.5 * math.cos(math.radians(a)), -16)
               for a in range(-84, 85, 12)]
        band = tube("band", C["acc"], pts, [3.4] * len(pts), n=8, bias=0.6)
        band.pxf = hf
        up.append(band)
        for s in (-1, 1):
            lobe = ellipsoid("bow", C["acc"], (s * 17, GROUND - 46, -12), (17, 12, 8), bias=0.8,
                             rot=lambda x, y, z, s=s: (x * math.cos(0.35) - s * y * math.sin(0.35),
                                                       s * x * math.sin(0.35) + y * math.cos(0.35), z))
            lobe.pxf = hf
            up.append(lobe)
        kn = ellipsoid("bowknot", C["acc"], (0, GROUND - 48, -9), (7, 7, 6), bias=1.0)
        kn.pxf = hf
        up.append(kn)
    elif hair == "cloud":   # explore: a big round cloud on top
        b = ellipsoid("cloud", C["hair"], (0, GROUND - 52, -14), (62, 34, 48), bias=-0.4)
        b.pxf = hf
        up.append(b)
    elif hair == "beehive":
        b = ellipsoid("hive", C["hair"], (0, GROUND - 30, -16), (36, 40, 34), bias=-0.4)
        b.pxf = hf
        up.append(b)
    elif hair == "flattop":   # a flat block on top, sunk into the cap: front-bottom edge y 60, 4 u above the hairline, on the skull
        ft = fbox("flattop", C["hair"], (0, GROUND - 49, -6), 104, 22, 80, bias=0.2)
        ft.pxf = hf
        up.append(ft)
    elif hair == "spiky":
        for k, a in enumerate(range(-50, 51, 25)):
            sp = tube("spike", C["hair"], [(a * 0.9, GROUND - 56, -6), (a * 1.3, GROUND - 82, -10)], [12, 3], n=8)
            sp.pxf = hf
            up.append(sp)

    # neck + torso: split at the table top (upper drawn after the table, lower before it)
    up.append(revolved("neck", C["skin"], "M164,146 C164,152 164,160 164,170", depth=0.9, bias=-4))
    half = o.get("body", BODY_CF if who == "cf" else BODY_WB)
    tu = revolved("torso", C["top"], half, depth=BODY_D, step=4, y1=LM["table"])
    tl = revolved("torso_low", C["top"], half, depth=BODY_D, step=4, y0=LM["table"] - 4)
    if who == "cf":
        tu.marks = [("fill", V_CF, C["inner"], None, 0), ("line", "M150,192 L150,214", None, INK, 1.2)] + \
                   [("fill", oval(x, y, 3, 3), INK, None, 0) for x, y in CF_BUTTONS]
    else:
        tu.marks = [("fill", WB_V, C["inner"], None, 0)] + [("fill", d, C["inner"], None, 0) for d in WB_COLLAR] + \
                   [("fill", WB_POCKET, ROW[23], INK, 1.2)] + [("line", d, None, ROW[c], 2.4) for d, c in WB_PENS]
    up.append(tu)
    low.append(tl)
    bprof = profile(half)

    # arms: sleeve to the elbow (resting on the table), skin forearm, ball hand
    T = LOCAL_TABLE_H
    arms = o.get("arms", "rest")
    marker = None
    sw = 56 if who == "cf" else 60
    for s in (-1, 1):
        sh = (s * sw, GROUND - LM["shoulder"], 0)
        a = arms
        if arms in ("click1", "click2", "point") and s == 1:
            a = "rest1"
        if a in ("rest", "rest1"):
            el = (s * 70, T + 11, 62)
            wr = (s * 34, T + 9, 106)
            hd = (s * (16 if a == "rest" else 22), T + 10, 114)
            if who == "wb" and s == -1 and arms == "rest":       # the marker lies in his right hand
                marker = [(hd[0] + 6, hd[1] + 2, hd[2] + 4), (hd[0] + 34, hd[1] + 2, hd[2] + 10)]
        elif a in ("click1", "click2"):                          # forearm up, the marker upright, cap on top
            el = (s * 72, T + 11, 60)
            wr = (s * 56, T + 52, 80)
            hd = (s * 52, T + 62, 84)
            marker = [(hd[0] + 2, hd[1] + 6, hd[2] + 2), (hd[0] + 2, hd[1] + 34, hd[2] + 2)]
        elif a == "point":                                       # arm forward, the marker points at you
            el = (s * 66, T + 26, 54)
            wr = (s * 40, T + 36, 112)
            hd = (s * 34, T + 37, 124)
            marker = [(hd[0] + 2, hd[1] + 1, hd[2] + 6), (hd[0] + 6, hd[1] + 3, hd[2] + 36)]
        elif a == "chin":                                        # Culture Fit tilt: hand under the chin
            el = (s * 60, T + 11, 66)
            wr = (s * 34, T + 46, 70)
            hd = (s * 24, GROUND - 156, 46)
        up.append(tube("sleeve", C["top"] if who == "cf" else C["inner"],
                       [sh, tuple(sh[j] * 0.4 + el[j] * 0.6 for j in range(3)), el], [13.0, 12.0, 11.0], bias=0.4))
        up.append(ellipsoid("cuff", C["top"] if who == "cf" else C["inner"], el, (11.5, 11.5, 11.5), bias=0.45))
        up.append(tube("forearm", C["skin"] if who == "wb" else C["top"], [el, wr], [9.0, 8.2], bias=0.5))
        up.append(ellipsoid("hand", C["skin"], hd, (10, 10.5, 9.5), bias=0.7))
    if marker:
        mk = tube("marker", ROW[23], marker, [3.6, 3.6], n=8, bias=1.2)
        cap_end = marker[-1]
        d = [marker[1][j] - marker[0][j] for j in range(3)]
        ln = math.sqrt(sum(c * c for c in d))
        tip = tuple(cap_end[j] + d[j] / ln * 9 for j in range(3))
        mc = tube("markercap", C["acc"] if who == "wb" else ROW[21], [cap_end, tip], [4.2, 4.2], n=8, bias=1.4)
        up += [mk, mc]

    # under the table: thighs forward, shins down, shoes (hidden at the front views)
    for s in (-1, 1):
        hip = (s * 22, 150 - DH + 14, 0)
        knee = (s * 24, 150 - DH + 12, 70)
        ank = (s * 24, 14 - DH, 78)
        low.append(tube("thigh", C["legs"], [hip, knee], [17, 15], bias=0))
        low.append(tube("shin", C["legs"], [knee, ank], [13, 12], bias=0))
        low.append(ellipsoid("shoe", ROW[22], (s * 24, 8 - DH, 88), (12, 8, 17)))
    lean = o.get("lean", 0.0)
    place = chain(rot_x(lean, (0, LOCAL_TABLE_H + 10, -10)), translate(SEATS[who], DH, SEAT_Z))
    hrot = chain(rot_x(nod), rot_z(tilt), rot_x(lean))     # the same pose, for normals (no pivot)
    brot = rot_x(lean)
    for p in up + low:
        p.nrot = hrot if getattr(p, "pxf", None) is hf else brot
        p.pxf = chain(getattr(p, "pxf", None), place)
    return low, up


def posed(parts):
    """Copies of the parts with their normals turned by their pose, so culling and toon light follow the pose."""
    out = []
    for p in parts:
        f = getattr(p, "nrot", None)
        if f is None:
            out.append(p)
            continue
        q = Part(p.name, p.color, p.pieces, [[f(n) for n in nm] if nm else nm for nm in p.normals], p.marks,
                 p.bias, p.ink, p.stroke)
        for k, v in p.__dict__.items():
            if k not in ("normals",):
                setattr(q, k, v)
        q.normals = [[f(n) for n in nm] if nm else nm for nm in p.normals]
        out.append(q)
    return out


# ---------------------------------------------------------------- the table (+ chairs: one mesh)
def table(color=None):
    c = color or ROW[24]
    parts = [fbox("tabletop", c, (0, TABLE_TOP - TABLE_T / 2, 0), TABLE_W, TABLE_T, TABLE_D),
             fbox("tablefront", c, (0, (TABLE_TOP - TABLE_T) / 2 + 6, TABLE_D / 2 - 14), TABLE_W - 24,
                  TABLE_TOP - TABLE_T - 12, 8),
             fbox("tableside", c, (-TABLE_W / 2 + 14, (TABLE_TOP - TABLE_T) / 2, 0), 12, TABLE_TOP - TABLE_T,
                  TABLE_D - 20),
             fbox("tableside", c, (TABLE_W / 2 - 14, (TABLE_TOP - TABLE_T) / 2, 0), 12, TABLE_TOP - TABLE_T,
                  TABLE_D - 20)]
    return parts


def chairs(color=None):
    c = color or ROW[24]
    out = []
    for k in ("cf", "wb"):
        x = SEATS[k]
        out.append(fbox("seat", c, (x, 146, SEAT_Z + 10), 96, 12, 90))
        out.append(fbox("chairback", c, (x, 180, SEAT_Z - 52), 92, 80, 10))
        out.append(fbox("chairpost", ROW[22], (x, 70, SEAT_Z + 10), 12, 140, 12))
    return out


# ---------------------------------------------------------------- the Camera-Off One
ICON_CAM = [  # (kind, list of 2D points in face units -1..1 (x right, y up))
    ("fill", [(-0.52, -0.30), (0.18, -0.30), (0.18, 0.30), (-0.52, 0.30)]),          # camera body
    ("fill", [(0.18, -0.08), (0.52, -0.30), (0.52, 0.30), (0.18, 0.08)]),            # lens cone
    ("slash", [(-0.62, -0.56), (0.62, 0.56)]),
]
ICON_MUTE = [
    ("fill", [(-0.16, -0.05), (0.16, -0.05), (0.16, 0.42), (0.0, 0.52), (-0.16, 0.42)]),   # mic head
    ("line", [(-0.32, 0.05), (-0.30, -0.18), (0.0, -0.30), (0.30, -0.18), (0.32, 0.05)]),  # mic cup
    ("line", [(0.0, -0.30), (0.0, -0.48)]),
    ("line", [(-0.18, -0.50), (0.18, -0.50)]),
    ("slash", [(-0.56, -0.58), (0.56, 0.58)]),
]


def camera_box(o):
    """o: icon ('cam', 'mute', 'off'), lean, style ('cube', 'slab', 'monitor')."""
    style = o.get("box", "cube")
    w, h, d = BOX
    if style == "slab":
        w, h, d = 70, 150, 50
    parts = [fbox("box", ROW[22], (SEATS["box"], TABLE_TOP + h / 2, BOX_Z), w, h, d, bias=0.3)]
    if style == "monitor":
        parts = [fbox("box", ROW[22], (SEATS["box"], TABLE_TOP + 30 + 45, BOX_Z), 120, 90, 14, bias=0.3),
                 fbox("stand", ROW[22], (SEATS["box"], TABLE_TOP + 15, BOX_Z), 20, 30, 10, bias=0.2)]
        w, h, d = 120, 90, 14
    lean = o.get("lean", 0.0)
    f = rot_x(lean, (SEATS["box"], TABLE_TOP, BOX_Z + d / 2))
    for p in parts:
        p.pxf = f
    icon = {"face_c": (SEATS["box"], (TABLE_TOP + 75) if style == "monitor" else TABLE_TOP + h / 2,
                       BOX_Z + d / 2 + 0.8), "half": (w / 2 * 0.82, h / 2 * 0.82), "xf": f,
            "kind": o.get("icon", "cam")}
    return parts, icon


def icon_svg(icon, yaw, pitch, s, ox, oy):
    """The cream icon on the box front, lifted onto the face plane and projected (drawn last)."""
    P, N = cam(yaw, pitch)
    if icon["kind"] == "off" or N((0, 0, 1))[2] <= 0.05:
        return ""
    (cx, cy, cz), (hw, hh), f = icon["face_c"], icon["half"], icon["xf"]
    pr = lambda u, v: P(f((cx + u * hw, cy + v * hh, cz)))
    out = []
    shapes = ICON_CAM if icon["kind"] == "cam" else ICON_MUTE
    col = ROW[12]
    for kind, pts in shapes:
        q = [pr(u, v) for u, v in pts]
        dd = " ".join(f"{'M' if k == 0 else 'L'}{ox + a[0] * s:.2f},{oy + a[1] * s:.2f}" for k, a in enumerate(q))
        if kind == "fill":
            out.append(f'<path d="{dd} Z" fill="{col}" stroke="none"/>')
        elif kind == "line":
            out.append(f'<path d="{dd}" fill="none" stroke="{col}" stroke-width="{7 * s:.2f}" '
                       f'stroke-linecap="round"/>')
        else:   # the slash: ink gap under a cream bar
            out.append(f'<path d="{dd}" fill="none" stroke="{ROW[22]}" stroke-width="{12 * s:.2f}" '
                       f'stroke-linecap="round"/>')
            out.append(f'<path d="{dd}" fill="none" stroke="{col}" stroke-width="{6 * s:.2f}" '
                       f'stroke-linecap="round"/>')
    return "".join(out)


# ---------------------------------------------------------------- the whole set
def scene(o=None):
    """Returns dict(low, table, up, icon). o: {'cf': {...}, 'wb': {...}, 'box': {...}, 'table': hex, 'only': key}."""
    o = dict(o or {})
    only = o.get("only")
    low, up = [], []
    for k in ("cf", "wb"):
        if only and only != k:
            continue
        l, u = person(k, o.get(k, {}))
        low += l
        up += u
    tb = [] if only else table(o.get("table"))
    if not only or only == "chairs":
        low += chairs(o.get("table"))
    icon = None
    if not only or only == "box":
        bp, icon = camera_box(o.get("box", {}))
        up += bp
    return {"low": low, "table": tb, "up": up, "icon": icon}


def render_scene(sc, yaw, pitch, s, ox, oy, ink_w, mono=None, mark_scale=1.0):
    """Layered painter: at front-ish views the bodies below the table go first, then the table, then the upper
    bodies on top; at back views the table goes first."""
    kw = dict(mono=mono, mark_scale=mark_scale)
    sc = dict(sc, low=posed(sc["low"]), up=posed(sc["up"]))
    back = math.cos(math.radians(yaw)) < -0.05
    if back:
        out = render(sc["table"], yaw, pitch, s, ox, oy, ink_w, **kw) + \
            render(sc["low"] + sc["up"], yaw, pitch, s, ox, oy, ink_w, **kw)
    else:
        out = render(sc["low"], yaw, pitch, s, ox, oy, ink_w, **kw) + \
            render(sc["table"], yaw, pitch, s, ox, oy, ink_w, **kw) + \
            render(sc["up"], yaw, pitch, s, ox, oy, ink_w, **kw)
    if sc["icon"] and not mono:
        out += icon_svg(sc["icon"], yaw, pitch, s, ox, oy)
    return out


def scene_bounds(sc, yaw, pitch):
    return pbounds(sc["low"] + sc["table"] + sc["up"], yaw, pitch)
