"""Brett Bullet-Points sketch: hand-drawn front curves -> a toy-pawn 3D sketch model -> any view.

Reuses the Ricky sketch library (assets/ricky/sketch/src/ricky.py: Bezier sampling, profiles, round bodies, mark
lifting, camera) and the Auntie Dot render with per-part pose transforms (assets/auntie-dot/sketch/src/dot.py).

Front view units: y down, axis x 150, sole y 340 (GROUND). Metres per unit come from the camera calibration in
build.py (1.05 x Kit on screen), not from here.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ASSETS, "ricky", "sketch", "src"))
sys.path.insert(0, os.path.join(ASSETS, "auntie-dot", "sketch", "src"))
import ricky as R  # noqa: E402
from ricky import (GROUND, Part, ring, revolved, ellipsoid, tube, profile, r_at, path_points,  # noqa
                   cam, hull, poly, line, oval, text, svg_doc, LIGHT)
from dot import render, pbounds, rot_x, rot_z, chain  # noqa: E402

# ---------------------------------------------------------------- palette (seats/lena-park.md rows)
ROW = {
    2: "#7FA65A",   # grass-deep: the #OpenToWork halo (chair call; the ONE green thing, with an ink edge)
    5: "#7A4A2E",   # wood: shoes (the family: Kit, Ricky, Dot)
    6: "#F4A672",   # cafe-wall (explore only)
    7: "#D4503A",   # cafe-roof: the sweater vest (my pick)
    8: "#A8C4DC",   # ats-wall (explore only)
    12: "#FFE8A6",  # cream: hair (blond swoop) (my pick)
    15: "#F2C79E",  # skin
    22: "#2B1E16",  # ink
    23: "#FFF8EE",  # panel: shirt (sleeves, collar, V), teeth, eye glint
    25: "#4A3226",  # hair (explore only)
    26: "#2F3E5C",  # trousers: chinos (as Kit's legs)
}
INK = ROW[22]
CARRY = {"head_nod": -10.0}   # his in-game carriage: chin up 10 deg (smug; it also opens the grin to the camera)
SHADE_K = R.SHADE_K
shade = R.shade
CREAM = R.CREAM
NOTE = R.NOTE

# ---------------------------------------------------------------- body map landmarks (front view units)
LM = {
    "halo": 0,           # halo centre line (floats above the swoop)
    "top": 16,           # top of the swoop (the wave tube)
    "crown": 32,         # top of the hair cap (volume on top)
    "hairline": 62,      # front hairline at the centre
    "temple": 84,        # hairline at the temples
    "brow": 80,
    "eye": 94,           # eye line; the ear points sit on it
    "eye_x": (132, 168),
    "ear_x": (95, 205),
    "mouth": (120, 102, 180, 126),   # mouth zone x0, y0, x1, y1 (the grin)
    "chin": 144,
    "neck": 152,         # neck line = shirt collar
    "shoulder": 176,     # arm root
    "shoulder_x": (92, 208),
    "chest": 188,        # widest point of the wedge
    "v_point": 198,      # bottom of the vest V
    "hand": 254,         # hands (rest)
    "hem": 252,          # vest hem = waist
    "crotch": 266,
    "knee": 298,
    "ankle": 324,
    "sole": 340,
}

# ---------------------------------------------------------------- hand-drawn half outlines (right half, x >= 150)
HEAD_HALF = "M150,46 C183,46 204,68 204,97 C204,126 182,144 150,144"
CAP_HALF = "M150,32 C189,32 210,62 209,97 C208,128 185,148 150,148"     # volume on top: the coif
CAP_LOW = "M150,42 C187,42 208,66 208,97 C208,128 185,148 150,148"      # explore: close crop
WAVE = [(-30, 50, 34), (-10, 36, 38), (16, 30, 34), (40, 36, 22), (54, 50, 4)]   # the swoop: from the part,
WAVE_R = [9, 13, 14, 12, 8]                                                    # up and over to his left
VEST_WEDGE = ("M164,150 C188,151 208,157 216,168 "          # neck to the square shoulder
              "C224,180 224,194 218,206 "                    # chest out: the widest point is high
              "C208,226 196,242 186,252 L150,252")           # tapers to a narrow waist
VEST_D = 0.64                                        # the vest is flatter front-to-back than wide
HIPS = "M150,246 C176,246 188,248 188,256 C188,264 180,268 150,268"
# Explore alternatives
VEST_CAPSULE = "M162,150 C190,150 206,166 206,190 L206,236 C206,250 196,256 178,256 L150,256"
VEST_BEAN = "M162,150 C194,152 214,174 212,204 C210,232 198,256 170,258 L150,258"
VEST_BOX = "M166,150 C204,150 220,152 222,166 L222,244 C222,252 214,254 200,254 L150,254"

# ---------------------------------------------------------------- front marks (drawn by hand)
HAIRLINE = ("M97,88 C99,76 107,68 118,64 C128,61 136,62 142,63 C150,62 162,60 174,61 "
            "C188,63 199,72 203,88")                    # high, clean hairline: nothing near the eyes
FACE = HAIRLINE + " L205,150 L95,150 Z"
PART = "M126,63 C124,55 126,48 131,43"                   # side part (his right, viewer-left)
SWOOP_LINES = ["M134,54 C150,44 170,42 190,50", "M140,62 C156,54 174,52 194,60"]
BROWS = ["M121,79 C126,74 135,73 141,76", "M159,76 C165,73 174,74 179,79"]
BROWS_SMUG = ["M121,78 C126,72 135,71 141,74", "M159,77 C165,76 174,77 179,80"]
BROWS_LOST = ["M122,81 C127,79 135,76 141,73", "M159,73 C165,76 173,79 178,81"]
GRIN = "M124,106 C138,110 162,110 176,106 C170,118 160,121 150,121 C140,121 130,118 124,106 Z"   # teeth crescent
GRIN_LINE = "M122,106 C130,122 170,122 178,106"     # ink smile line under the teeth, corners up
TEETH_LINE = "M131,119 C143,121 157,121 169,119"
TALK = "M131,110 C144,112 156,112 169,110 C167,123 159,130 150,130 C141,130 133,123 131,110 Z"
TALK_TEETH = "M134,112 C145,114 155,114 166,112 C165,116 135,116 134,112 Z"
LOST_MOUTH = "M136,120 C141,116 146,122 150,118 C154,114 159,120 164,117"     # the grin cracks: a wobble
WINK = "M161,95 C164,90 172,90 175,95"
SHIRT_V = "M134,151 C140,154 160,154 166,151 C163,170 157,186 150,198 C143,186 137,170 134,151 Z"
SKIN_V = "M142,153 C146,155 154,155 158,153 C156,160 153,166 150,170 C147,166 144,160 142,153 Z"   # open top button
COLLAR = ["M150,156 C143,151 135,148 127,149 C128,156 131,162 136,168 C140,164 145,160 150,156 Z",
          "M150,156 C157,151 165,148 173,149 C172,156 169,162 164,168 C160,164 155,160 150,156 Z"]
V_RIB = ["M133,150 C139,170 145,186 150,199", "M167,150 C161,170 155,186 150,199"]
HEM_RIB = "M111,244 C130,248 170,248 189,244"


# ---------------------------------------------------------------- the model
def model(o=None):
    """Build Brett. o: options for the explore thumbnails, the expressions and the poses."""
    o = dict(o or {})
    C = {"vest": ROW[7], "shirt": ROW[23], "skin": ROW[15], "hair": ROW[12], "halo": ROW[2], "pants": ROW[26],
         "shoe": ROW[5]}
    C.update(o.get("colors", {}))
    vest_half = o.get("body", VEST_WEDGE)
    halo = o.get("halo", "above")         # above, frame (vertical ring behind the head), none
    hair = o.get("hair", "wave")          # wave, swoop, flat, slick, none
    arms = o.get("arms", "rest")          # rest, hips, thumb, count1, count2, count3
    face = o.get("face", "grin")          # grin, talk, wink, lost
    vest = o.get("vest", True)
    head_tilt = o.get("head_tilt", 0.0)
    head_nod = o.get("head_nod", 0.0)
    no_head = o.get("no_head", False)
    hf = chain(rot_x(head_nod, (0, GROUND - LM["chin"], 0)), rot_z(head_tilt, (0, GROUND - LM["chin"] - 6, 0)))
    parts = []

    # ---- head: skin head, hair cap (with the face marks), swoop, ears
    head = revolved("head", C["skin"], HEAD_HALF, depth=0.92, step=3)
    head.flat = True
    head.pxf = hf
    parts.append(head)
    cap = hair_cap(o.get("cap", CAP_HALF), C["hair"], LM["temple"])
    marks = [("face", FACE, C["skin"], None, 0), ("line", HAIRLINE, None, INK, 2.2)]
    if hair in ("swoop", "wave"):
        marks.append(("line", PART, None, INK, 1.8))
    brows = {"lost": BROWS_LOST, "wink": BROWS_SMUG}.get(face, BROWS)
    marks += [("line", d, None, INK, 2.8) for d in brows]
    for k, x in enumerate(LM["eye_x"]):
        if face == "wink" and k == 1:
            marks.append(("line", WINK, None, INK, 3.4))
            continue
        ey = o.get("eye_y", LM["eye"])
        marks.append(("fill", oval(x, ey, 6.5, 9.0), INK, None, 0))
        marks.append(("fill", oval(x + 2, ey - 3.4, 2.0, 2.4), ROW[23], None, 0))
    if face in ("grin", "wink") and o.get("old_grin"):     # explore only: the first, edged white grin
        marks.append(("fill", o["old_grin"], ROW[23], INK, 1.0))
    elif face in ("grin", "wink"):
        marks.append(("fill", GRIN, ROW[23], None, 0))       # teeth (row 23), no edge of their own
        marks.append(("line", GRIN_LINE, None, INK, 3.0))    # the smile line carries the shape
        if o.get("teeth_line", False):
            marks.append(("line", TEETH_LINE, None, INK, 0.9))
    elif face == "talk":
        marks.append(("fill", TALK, INK, None, 0))
        marks.append(("fill", TALK_TEETH, ROW[23], None, 0))
    elif face == "lost":
        marks.append(("line", LOST_MOUTH, None, INK, 2.6))
    cap.marks = marks
    cap.face_host = head.host
    cap.pxf = hf
    parts.append(cap)
    hb = hair_back(o.get("cap", CAP_HALF), C["hair"], LM["temple"])
    cap.cull_from = len(cap.pieces)
    cap.pieces += hb.pieces
    cap.normals += hb.normals
    for s in (-1, 1):
        e = ellipsoid("ear", C["skin"], (s * 55, GROUND - LM["eye"] - 1, -4), (5, 10, 7))
        e.pxf = hf
        parts.append(e)
    # the swoop: one soft roll, swept up and over from the side part to his left (viewer-right)
    if hair == "wave":
        cap_top = o.get("cap", None)
        wv, wr_ = smooth(o.get("wave", WAVE), o.get("wave_r", WAVE_R))
        w = tube("swoop", C["hair"], [(x, GROUND - y, z) for x, y, z in wv], wr_, n=14, bias=0.6)
        w.pxf = hf
        parts.append(w)
    if hair in ("swoop", "flat", "slick"):
        c, rad, tilt = {"swoop": ((8, 44, 10), (46, 15, 36), 7), "flat": ((0, 38, 2), (48, 12, 40), 0),
                        "slick": ((0, 50, -6), (52, 8, 46), 0)}[hair]
        c, rad, tilt = o.get("hair_spec", (c, rad, tilt))
        t = math.radians(tilt)
        rot = (lambda x, y, z, t=t: (x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t), z))
        sw = ellipsoid("swoop", C["hair"], (c[0], GROUND - c[1], c[2]), rad, bias=0.6, rot=rot)
        sw.pxf = hf
        parts.append(sw)
    # the #OpenToWork halo: floats above the crown, level, centred on the head axis (a child of the head)
    if halo == "above":
        for nm, a0, a1, b in (("halo_back", 0.5, 1.5, 0.0), ("halo_front", -0.5, 0.5, 0.2)):
            pts = []
            for k in range(17):
                a = math.pi * (a0 + (a1 - a0) * k / 16)
                pts.append((38 * math.sin(a), GROUND - LM["halo"], 30 * math.cos(a)))
            h = tube(nm, C["halo"], pts, [6.0] * len(pts), n=12, bias=b)
            hc = hf((0.0, GROUND - LM["halo"], 0.0))
            h.pxf = chain(hf, rot_x(-head_nod, hc))
            parts.append(h)
    elif halo == "frame":   # a vertical ring behind the head, like the profile-photo frame
        for nm, a0, a1 in (("frame_l", 0.0, 1.0), ("frame_r", 1.0, 2.0)):
            pts = []
            for k in range(17):
                a = math.pi * (a0 + (a1 - a0) * k / 16)
                pts.append((66 * math.sin(a), GROUND - 96 + 66 * math.cos(a), -48))
            h = tube(nm, C["halo"], pts, [6.0] * len(pts), n=12, bias=-2)
            h.pxf = hf
            parts.append(h)

    if no_head:
        parts = [p for p in parts if p.name.startswith("halo")]
    # ---- neck, vest (with the shirt V, collar), hips, sleeves
    parts.append(revolved("neck", C["skin"], "M166,136 C166,144 166,152 166,162", depth=0.9, bias=-4))
    body_col = C["vest"] if vest else C["shirt"]
    bd = revolved("vest", body_col, vest_half, depth=VEST_D, step=4)
    bm = [("fill", SHIRT_V, C["shirt"], INK, 1.4), ("fill", SKIN_V, C["skin"], None, 0)]
    bm += [("line", d, None, INK, 1.6) for d in V_RIB]
    bm += [("fill", c, C["shirt"], INK, 1.3) for c in COLLAR]
    bm.append(("line", HEM_RIB, None, INK, 1.4))
    bd.marks = bm
    parts.append(bd)
    parts.append(revolved("hips", C["pants"], HIPS, depth=0.8, bias=-2))
    vprof = profile(vest_half)

    def surf_z(x, y, out=0.0):
        r = r_at(vprof, y)
        return r * VEST_D * math.sqrt(max(1 - (x / max(r, 1e-3)) ** 2, 0.0)) + out

    for s in (-1, 1):
        sh = (s * 56, GROUND - LM["shoulder"], 0)
        a = arms
        fingers = 0
        thumb = False
        if a in ("thumb",) and s == 1:
            a = "rest"
        if a.startswith("count") and s == 1:
            a = "hips"
        if a == "rest":
            el = (s * 74, GROUND - 212, 0)
            wr = (s * 76, GROUND - 244, 4)
            hd = (s * 76, GROUND - LM["hand"], 6)
        elif a == "hips":        # power pose: elbows out, fists on the waist
            el = (s * 96, GROUND - 214, -4)
            wr = (s * 62, GROUND - 240, 4)
            hd = (s * 50, GROUND - 246, 10)
        elif a == "thumb":       # his right fist forward at chest height, thumb up: the Like
            el = (s * 88, GROUND - 212, 10)
            wr = (s * 96, GROUND - 184, 18)
            hd = (s * 96, GROUND - 172, 20)
            thumb = True
        elif a.startswith("count"):  # his right hand up beside the chest, fingers up one by one
            el = (s * 84, GROUND - 216, 12)
            wr = (s * 84, GROUND - 186, 26)
            hd = (s * 82, GROUND - 176, 28)
            fingers = int(a[-1])
        parts.append(tube("sleeve", C["shirt"], [sh, el, wr], [12.0, 11.0, 10.0], bias=0.4))
        parts.append(ellipsoid("hand", C["skin"], hd, (10.5, 10.5, 10), bias=0.6))
        if thumb:
            parts.append(tube("thumb", C["skin"], [(hd[0], hd[1] + 4, hd[2] + 3), (hd[0], hd[1] + 26, hd[2] + 3)],
                              [6.2, 5.6], n=10, bias=0.9))
        for f in range(fingers):
            fx = hd[0] + (f - (fingers - 1) / 2) * 6.5
            parts.append(tube("finger", C["skin"], [(fx, hd[1] + 6, hd[2] + 3), (fx, hd[1] + 21, hd[2] + 3)],
                              [3.0, 2.8], n=8, bias=0.9))

    # ---- legs and shoes (chinos)
    for s in (-1, 1):
        parts.append(revolved("leg", C["pants"], f"M164,{LM['crotch'] - 8} C164,{LM['knee']} 163,{LM['ankle'] - 6} "
                                                 f"163,{LM['ankle']}", depth=1.0, cx=s * 20, bias=-8))
        parts.append(ellipsoid("shoe", C["shoe"], (s * 21, GROUND - 331, 9), (13.5, 9, 21), bias=-6))
    return parts


def smooth(pts, radii, k=6):
    """Catmull-Rom through the hand-placed wave points: k samples per span, radii linear."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    out, rr = [], []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(k):
            t = j / k
            out.append(tuple(0.5 * (2 * p1[d] + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t * t
                                    + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t ** 3) for d in range(3)))
            rr.append(radii[i - 1] + (radii[i] - radii[i - 1]) * t)
    out.append(tuple(pts[-1]))
    rr.append(radii[-1])
    return out, rr


def hair_cap(capd, color, ylow):
    prof = profile(capd)
    rings = []
    y = prof[0][0]
    while y <= ylow:
        r = r_at(prof, y)
        rings.append(ring(0, GROUND - y, 0, max(r, 0.5), max(r * 0.92, 0.5)))
        y += 3
    pieces = [p0 + p1 for (p0, _), (p1, _) in zip(rings, rings[1:])]
    normals = [n0 + n1 for (_, n0), (_, n1) in zip(rings, rings[1:])]
    p = Part("hair", color, pieces, normals, bias=0.5)
    p.after = "head"
    p.host = {"prof": prof, "depth": 0.92, "cx": 0.0, "cz": 0.0, "rscale": 1.0, "sy": 1.0, "lift": 0.0}
    return p


def hair_back(capd, color, ytop):
    """Short back and sides: from the temple line down behind the ear to the nape (y 132)."""
    prof = profile(capd)
    rings = []
    y = ytop - 3
    while y <= 134:
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
