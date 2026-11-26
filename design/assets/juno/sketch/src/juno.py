"""Juno the barista sketch: hand-drawn front curves -> a toy-pawn 3D sketch model -> any view.

Reuses the Ricky sketch library (assets/ricky/sketch/src/ricky.py: Bezier sampling, profiles, round bodies, mark
lifting, camera), the Auntie Dot render with per-part pose transforms (assets/auntie-dot/sketch/src/dot.py) and the
Brett hair cap / back hair helpers (assets/brett/sketch/src/brett.py).

Front view units: y down, axis x 150, sole y 340 (GROUND). Metres per unit come from the camera calibration in
build.py (1.0 x Kit on screen), not from here.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ASSETS, "ricky", "sketch", "src"))
sys.path.insert(0, os.path.join(ASSETS, "auntie-dot", "sketch", "src"))
sys.path.insert(0, os.path.join(ASSETS, "brett", "sketch", "src"))
import ricky as R  # noqa: E402
from ricky import (GROUND, Part, ring, revolved, ellipsoid, tube, profile, r_at, path_points,  # noqa
                   cam, hull, poly, line, oval, text, svg_doc, LIGHT)
from dot import render, pbounds, rot_x, rot_z, chain  # noqa: E402
from brett import hair_cap  # noqa: E402

# ---------------------------------------------------------------- palette (seats/lena-park.md rows)
ROW = {
    2: "#7FA65A",   # grass-deep (explore only)
    5: "#7A4A2E",   # wood: the coffee-brown top and sleeves, shoes (the dark element that carries the read)
    6: "#F4A672",   # cafe-wall: the apron (bib + skirt), cheeks
    7: "#D4503A",   # cafe-roof: apron ties + back bow, pocket, scrunchie, marker (small accents)
    12: "#FFE8A6",  # cream (explore only)
    13: "#F0B43C",  # gold (explore only)
    15: "#F2C79E",  # skin
    22: "#2B1E16",  # ink
    23: "#FFF8EE",  # panel: the cup and lid, teeth, eye glint
    25: "#4A3226",  # hair: the puff
    26: "#2F3E5C",  # trousers: leggings (the family legs)
}
INK = ROW[22]
SHADE_K = R.SHADE_K
shade = R.shade
CREAM = R.CREAM
NOTE = R.NOTE

# ---------------------------------------------------------------- body map landmarks (front view units)
LM = {
    "puff_top": 10,      # top of the hair puff
    "puff": 40,          # puff centre
    "crown": 52,         # top of the hair cap (hair slicked back)
    "hairline": 64,      # front hairline at the centre (high, clean)
    "temple": 84,        # lowest hair at the sides, in front of the ears (above the eye top 95.5)
    "brow": 88,
    "eye": 104,          # eye line; the ear points sit on it
    "eye_x": (132, 168),
    "ear_x": (96, 204),
    "mouth": (138, 122, 162, 140),   # mouth zone
    "chin": 154,
    "neck": 162,         # neckline of the top
    "shoulder": 186,     # arm root
    "shoulder_x": (96, 204),
    "chest": 196,        # bib top, the upper width
    "waist": 238,        # the apron tie: narrowest
    "hem": 294,          # skirt and apron hem: the lower width
    "knee": 310,
    "ankle": 326,
    "sole": 340,
}

# ---------------------------------------------------------------- hand-drawn half outlines (right half, x >= 150)
HEAD_HALF = "M150,58 C183,58 204,79 204,108 C204,137 182,154 150,154"
CAP_HALF = "M150,52 C188,52 209,77 208,108 C207,139 185,158 150,158"
BODY_HG = ("M162,158 C184,160 202,168 208,182 "          # neck to a soft round shoulder
           "C214,194 212,208 204,220 "                     # upper width at the chest, then in
           "C198,228 192,234 191,240 "                     # the waist pinch at the apron tie
           "C197,256 210,274 217,290 "                     # the skirt flares out
           "C220,298 208,300 192,300 L150,300")            # soft hem
BODY_D = 0.8
# explore alternatives
BODY_CAPSULE = "M162,158 C190,158 206,174 206,198 L206,280 C206,294 196,300 178,300 L150,300"
BODY_COLUMN = "M160,158 C184,160 196,170 198,186 L196,312 C196,320 188,322 176,322 L150,322"
BODY_MUG = "M160,158 C196,160 208,166 208,180 L206,290 C206,298 198,300 184,300 L150,300"
BODY_TEAR = "M160,158 C178,160 190,172 194,192 C204,230 216,262 216,284 C216,298 204,300 186,300 L150,300"

# ---------------------------------------------------------------- front marks (drawn by hand)
HAIRLINE = ("M99,88 C101,78 106,72 115,68 C125,64 137,63 150,64 C163,63 175,64 185,68 "
            "C194,72 199,78 201,88")                    # high, clean, swept back: nothing on the forehead
FACE = HAIRLINE + " L201,98 L99,98 Z"   # skin over the cap below the hairline (the cap ends at y 86)
STRANDS = ["M121,66 C127,59 137,55 147,53", "M179,66 C173,59 163,55 153,53"]   # swept up and back to the puff
BROWS = ["M121,89 C126,85 135,84 141,87", "M159,87 C165,84 174,85 179,89"]
BROWS_DRY = ["M121,88 C126,82 135,80 141,83", "M159,89 C165,88 174,88 179,90"]   # one brow up
SMILE = "M140,128 C145,134 155,134 160,128"                 # calm closed smile (rest)
SMIRK = "M141,131 C147,133 154,132 160,127"                 # dry: one corner up
LAUGH = "M136,124 C144,126 156,126 164,124 C162,135 157,141 150,141 C143,141 138,135 136,124 Z"   # Ricky style
LAUGH_TEETH = "M138,124.8 C145,126.6 155,126.6 162,124.8 C161.6,128.6 138.4,128.6 138,124.8 Z"
TALK = "M141,126 C146,127.5 154,127.5 159,126 C158,134 154,138 150,138 C146,138 142,134 141,126 Z"
TALK_TEETH = "M142.5,126.6 C146,127.8 154,127.8 157.5,126.6 C157,129.4 143,129.4 142.5,126.6 Z"
HAPPY_EYES = ["M125,106 C128,99 136,99 139,106", "M161,106 C164,99 172,99 175,106"]
DOWN_EYES = ["M125,104 C128,109 136,109 139,104", "M161,104 C164,109 172,109 175,104"]   # looking down: lids
CHEEKS = [(126, 121), (174, 121)]
NECKLINE = "M136,162 C142,168 158,168 164,162"
BIB = "M128,198 L172,198 C173,212 175,226 177,236 L123,236 C125,226 127,212 128,198 Z"
STRAPS = ["M128,198 L134,198 C137,184 141,172 144,163 L139,162 C136,172 131,184 128,198 Z",
          "M172,198 L166,198 C163,184 159,172 156,163 L161,162 C164,172 169,184 172,198 Z"]
SKIRT = "M111,242 L189,242 C197,258 204,274 208,290 C188,296 112,296 92,290 C96,274 103,258 111,242 Z"
POCKET = "M134,254 L166,254 L165,270 C160,274 140,274 135,270 Z"
HEM_LINE = "M88,292 C120,298 180,298 212,292"
# the cup (local: revolved round x 150, H from 6 to 40; centre H 23)
CUP_HALF = "M163,300 C162.6,310 161.4,322 160,334"
LID_HALF = "M150,295 C160,295 165,296 165,298 C165.5,300 165,302 164,302"
CUP_C = 23.0
CUP_TEXT = ["M143,309 C145,307 147,311 149,309 C151,307 153,311 155,309 C156,308 157,309 158,309",
            "M142,315 C144,313 146,317 148,315 C150,313 152,317 154,315 C155,314 156,315 157,315",
            "M144,321 C146,319 148,323 150,321 C152,319 154,323 156,321"]


def translate(dx, dy, dz):
    return lambda q: (q[0] + dx, q[1] + dy, q[2] + dz)


def cup(at, color=None, text=True, tilt=0.0):
    """The cup with its line, centred at `at` (X, H, Z). tilt: lean in degrees about X (toward the viewer)."""
    c = color or ROW[23]
    body = revolved("cup", c, CUP_HALF, depth=1.0, step=3)
    body.marks = [("line", d, None, INK, 1.1) for d in CUP_TEXT] if text else []
    lid = revolved("lid", c, LID_HALF, depth=1.0, step=1)
    f = chain(translate(0, -CUP_C, 0), rot_x(tilt), translate(*at))
    for p in (body, lid):
        p.pxf = f
        p.bias = 0.8
    lid.after = "cup"
    return [body, lid]


def surf_z(prof, x, y, depth=BODY_D, out=0.0):
    r = r_at(prof, y)
    return r * depth * math.sqrt(max(1 - (x / max(r, 1e-3)) ** 2, 0.0)) + out


# ---------------------------------------------------------------- the model
def model(o=None):
    """Build Juno. o: options for the explore thumbnails, the expressions and the poses."""
    o = dict(o or {})
    C = {"top": ROW[5], "apron": ROW[6], "tie": ROW[7], "skin": ROW[15], "hair": ROW[25], "legs": ROW[26],
         "shoe": ROW[5], "cup": ROW[23]}
    C.update(o.get("colors", {}))
    body_half = o.get("body", BODY_HG)
    hair = o.get("hair", "puff")          # puff, back, buns, scarf, crop
    apron = o.get("apron", "bib")         # bib, waist, none
    ties = o.get("ties", True)
    arms = o.get("arms", "cup")           # cup, sides, hand, wave0..2, write, mughandle
    face = o.get("face", "smile")         # smile, laugh, dry, focus, talk
    head_tilt = o.get("head_tilt", 0.0)
    head_nod = o.get("head_nod", 4.0 if arms == "write" else 0.0)
    if arms == "write":
        head_nod = o.get("head_nod", 14.0)
    hf = chain(rot_x(head_nod, (0, GROUND - LM["chin"], 0)), rot_z(head_tilt, (0, GROUND - LM["chin"] - 6, 0)))
    parts = []

    # ---- head: skin head, hair cap with the face marks, the puff and its scrunchie, ears
    head = revolved("head", C["skin"], HEAD_HALF, depth=0.92, step=3)
    head.flat = True
    head.pxf = hf
    parts.append(head)
    hair_col = C["tie"] if hair == "scarf" else C["hair"]
    cap = hair_cap(CAP_HALF, hair_col, LM["temple"] + 2)
    marks = [("face", FACE, C["skin"], None, 0), ("line", HAIRLINE, None, INK, 2.2)]
    if hair != "scarf":
        marks += [("line", d, None, INK, 1.3) for d in STRANDS]
    for (x, y) in CHEEKS:
        marks.append(("fill", oval(x, y, 7, 4), C["apron"] if C["apron"] != C["skin"] else ROW[6], None, 0))
    brows = BROWS_DRY if face == "dry" else BROWS
    marks += [("line", d, None, INK, 2.6) for d in brows]
    if face == "laugh":
        marks += [("line", d, None, INK, 3.4) for d in HAPPY_EYES]
    elif face == "focus":
        marks += [("line", d, None, INK, 3.4) for d in DOWN_EYES]
    else:
        for x in LM["eye_x"]:
            marks.append(("fill", oval(x, LM["eye"], 6.5, 8.5), INK, None, 0))
            marks.append(("fill", oval(x + 2, LM["eye"] - 3.2, 2.0, 2.4), ROW[23], None, 0))
    if face == "laugh":
        marks.append(("fill", LAUGH, INK, None, 0))
        marks.append(("fill", LAUGH_TEETH, ROW[23], None, 0))
    elif face == "talk":
        marks.append(("fill", TALK, INK, None, 0))
        marks.append(("fill", TALK_TEETH, ROW[23], None, 0))
    elif face == "dry":
        marks.append(("line", SMIRK, None, INK, 2.8))
    else:
        marks.append(("line", SMILE, None, INK, 2.8))
    cap.marks = marks
    cap.face_host = cap.host   # the face fill lies on the same surface as the hairline ink (pitch 42 agrees)
    cap.pxf = hf
    parts.append(cap)
    hb = hair_back(CAP_HALF, hair_col, LM["temple"])
    cap.cull_from = len(cap.pieces)
    cap.pieces += hb.pieces
    cap.normals += hb.normals
    for s in (-1, 1):
        e = ellipsoid("ear", C["skin"], (s * 55, GROUND - LM["eye"] - 1, -4), (5, 10, 7))
        e.pxf = hf
        parts.append(e)
    blobs = {"puff": [((0, LM["puff"], -18), (36, 30, 32))],
             "back": [((0, 128, -54), (26, 24, 22))],
             "buns": [((-36, 60, -8), (19, 18, 18)), ((36, 60, -8), (19, 18, 18))],
             "scarf": [((0, 46, 10), (11, 9, 9)), ((-11, 42, 12), (8, 6, 5)), ((11, 42, 12), (8, 6, 5))],
             "crop": []}[hair]
    for k, ((bx, by, bz), rad) in enumerate(blobs):
        col = C["tie"] if hair == "scarf" else C["hair"]
        b = ellipsoid("puff", col, (bx, GROUND - by, bz), rad, bias=-0.5 if hair != "scarf" else 1.0)
        b.pxf = hf
        parts.append(b)
    if hair == "puff":   # the scrunchie: a red ring where the puff meets the head
        pts = []
        for k in range(25):
            a = 2 * math.pi * k / 24
            pts.append((22 * math.sin(a), GROUND - 62, -14 + 18 * math.cos(a)))
        sc = tube("scrunchie", C["tie"], pts, [5.0] * len(pts), n=10, bias=-0.3)
        sc.pxf = hf
        parts.append(sc)

    # ---- neck, body (coffee-brown top + skirt) with the apron marks
    parts.append(revolved("neck", C["skin"], "M164,146 C164,152 164,160 164,170", depth=0.9, bias=-4))
    bd = revolved("body", C["top"], body_half, depth=BODY_D, step=4)
    bm = [("line", NECKLINE, None, INK, 1.4)]
    if apron == "bib":
        bm += [("fill", d, C["apron"], INK, 1.3) for d in STRAPS]
        bm.append(("fill", BIB, C["apron"], INK, 1.4))
    if apron in ("bib", "waist"):
        bm.append(("fill", SKIRT, C["apron"], INK, 1.4))
        bm.append(("fill", POCKET, C["tie"], INK, 1.2))
    bm.append(("line", HEM_LINE, None, INK, 1.2))
    bd.marks = bm
    parts.append(bd)
    bprof = profile(body_half)

    # the apron tie: a red cord round the waist, a bow at the back
    if ties and apron != "none":
        wy = LM["waist"]
        rw = r_at(bprof, wy) + 1.5
        pts = []
        for k in range(33):
            a = 2 * math.pi * k / 32
            pts.append((rw * math.sin(a), GROUND - wy, rw * BODY_D * math.cos(a)))
        parts.append(tube("tie", C["tie"], pts, [2.8] * len(pts), n=8, bias=0.3))
        bz = -rw * BODY_D - 3
        for s in (-1, 1):
            parts.append(ellipsoid("bow", C["tie"], (s * 9, GROUND - wy + 2, bz), (9, 6, 3.5), bias=-0.2))
            parts.append(tube("bowtail", C["tie"], [(s * 3, GROUND - wy, bz), (s * 7, GROUND - wy - 14, bz - 1),
                                                    (s * 9, GROUND - wy - 24, bz - 1)], [2.6, 2.4, 2.2], n=8))
        parts.append(ellipsoid("bowknot", C["tie"], (0, GROUND - wy, bz - 1), (4, 4, 3.5), bias=0.1))

    # ---- arms: rolled sleeves (brown to the elbow), skin forearms, ball hands; the cup in a hand
    zf = lambda x, y, out=0.0: surf_z(bprof, x, y, BODY_D, out)
    cup_at = None
    cup_tilt = 0.0
    marker = None
    for s in (-1, 1):
        sh = (s * 54, GROUND - LM["shoulder"], 0)
        a = arms
        if a in ("hand",) and s == 1:
            a = "sides"
        if a.startswith("wave") and s == 1:
            a = "cup1"
        if a == "write" and s == 1:
            a = "holdhigh"
        if a == "write" and s == -1:
            a = "pen"
        if a == "mughandle":
            a = "hip" if s == 1 else "sides"
        if a == "cup":            # rest: both hands hold the cup in front of the apron
            el = (s * 66, GROUND - 216, 12)
            wr = (s * 26, GROUND - 226, zf(26, 226, 10))
            hd = (s * 16, GROUND - 226, zf(16, 226, 13))
            cup_at = (0, GROUND - 224, zf(0, 226, 15))
        elif a == "cup1":         # one hand holds the cup in front (during the wave)
            el = (s * 66, GROUND - 216, 12)
            wr = (s * 28, GROUND - 228, zf(28, 228, 10))
            hd = (s * 17, GROUND - 228, zf(17, 228, 14))
            cup_at = (3, GROUND - 222, zf(3, 226, 18))
        elif a == "sides":
            el = (s * (r_at(bprof, 214) + 6), GROUND - 214, 2)
            wr = (s * (r_at(bprof, 244) + 10), GROUND - 244, 6)
            hd = (s * (r_at(bprof, 254) + 11), GROUND - 254, 8)
        elif a == "hip":
            el = (s * 92, GROUND - 216, -4)
            wr = (s * 58, GROUND - 236, 4)
            hd = (s * 48, GROUND - 240, 10)
        elif a == "hand":         # her right arm forward, the cup on the palm: handing it over
            el = (s * 66, GROUND - 212, 24)
            wr = (s * 46, GROUND - 212, 70)
            hd = (s * 42, GROUND - 212, 80)
            cup_at = (s * 42, GROUND - 212 + 10 + 17, 82)
        elif a.startswith("wave"):  # her right hand up beside the shoulder, palm out; rocks in 3 frames
            k = int(a[-1]) - 1
            el = (s * 82, GROUND - 210, 8)
            wr = (s * (86 + 8 * k), GROUND - 176, 12)
            hd = (s * (86 + 13 * k), GROUND - 163, 14)
        elif a == "holdhigh":     # her left hand holds the cup up at the chest
            el = (s * 68, GROUND - 214, 16)
            wr = (s * 32, GROUND - 210, zf(32, 210, 16))
            hd = (s * 20, GROUND - 208, zf(20, 210, 22))
            cup_at = (6, GROUND - 202, zf(6, 210, 28))
            cup_tilt = -10.0
        elif a == "pen":          # her right hand writes on the cup front
            el = (s * 66, GROUND - 216, 22)
            wr = (s * 26, GROUND - 210, zf(26, 210, 30))
            hd = (s * 14, GROUND - 206, zf(14, 210, 38))
            marker = [(hd[0] + 4, hd[1] + 4, hd[2] + 2), (hd[0] + 14, hd[1] + 12, hd[2] - 2)]
        parts.append(tube("sleeve", C["top"], [sh, tuple((sh[j] * 0.35 + el[j] * 0.65) for j in range(3)), el],
                          [12.0, 11.0, 10.5], bias=0.4))
        parts.append(ellipsoid("cuff", C["top"], el, (11, 11, 11), bias=0.45))
        parts.append(tube("forearm", C["skin"], [el, wr], [8.2, 7.6], bias=0.35))
        parts.append(ellipsoid("hand", C["skin"], hd, (10, 10.5, 9.5), bias=0.6))
    if cup_at is not None:
        parts += cup(cup_at, C["cup"], tilt=cup_tilt)
    if marker:
        parts.append(tube("marker", C["tie"], marker, [2.8, 2.6], n=8, bias=1.0))

    # ---- legs and shoes
    for s in (-1, 1):
        parts.append(revolved("leg", C["legs"], f"M163,{LM['hem'] - 6} C163,{LM['knee']} 162,{LM['ankle'] - 6} "
                                                f"162,{LM['ankle']}", depth=1.0, cx=s * 20, bias=-8))
        parts.append(ellipsoid("shoe", C["shoe"], (s * 21, GROUND - 332, 9), (13, 8.5, 19), bias=-6))
    return parts


def hair_back(capd, color, ytop):
    """Slicked back and sides: from the temple line down behind the ear to the nape (y 140)."""
    prof = profile(capd)
    rings = []
    y = ytop - 3
    while y <= 142:
        r = r_at(prof, y)
        zc = -2 - (y - ytop) * 0.9
        rx, rz = max(r, 0.5), max(r * 0.92, 0.5)
        if zc < rz:
            a0 = math.acos(max(-1.0, min(1.0, zc / rz)))
            pts, nrm = [], []
            for k in range(41):
                a = a0 + (2 * math.pi - 2 * a0) * k / 40
                sa, ca = math.sin(a), math.cos(a)
                pts.append((rx * sa, GROUND - y, rz * ca))
                nrm.append((sa / rx, 0.0, ca / rz))
            rings.append((pts, nrm))
        y += 1.5
    pieces, normals = [], []
    for (p0, n0), (p1, n1) in zip(rings, rings[1:]):
        for c in range(8):
            a, b = c * 5, c * 5 + 6
            pieces.append(p0[a:b] + p1[a:b])
            normals.append(n0[a:b] + n1[a:b])
    return Part("hairback", color, pieces, normals, bias=0.35)
