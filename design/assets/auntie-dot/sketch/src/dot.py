"""Auntie Dot sketch: hand-drawn front curves -> a toy-pawn 3D sketch model -> any view.

Reuses the Recruiter Ricky sketch library (assets/ricky/sketch/src/ricky.py): Bezier sampling, profiles, round
bodies (`revolved`, `ellipsoid`, `tube`), mark lifting and the camera. The render is copied from there with one
change: each part may carry its own pose transform (head tilt, sway), so the marks follow their part.

Front view units: y down, axis x 150, sole y 340 (GROUND). Metres per unit are set by the camera calibration in
build.py (0.9 x Kit on screen), not here.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ASSETS, "ricky", "sketch", "src"))
import ricky as R  # noqa: E402
from ricky import (GROUND, Part, ring, revolved, ellipsoid, tube, lift_mark, path_points, profile, r_at,  # noqa
                   cam, hull, poly, line, oval, text, svg_doc, bounds, LIGHT)

# ---------------------------------------------------------------- palette (seats/lena-park.md rows)
ROW = {
    5: "#7A4A2E",   # wood: shoes (Kit and Ricky wear the same)
    11: "#7A5596",  # hq-roof: cardigan / dress (chair call)
    13: "#F0B43C",  # gold: Copium mark on the Skill card
    15: "#F2C79E",  # skin
    22: "#2B1E16",  # ink
    23: "#FFF8EE",  # panel: hair and bun (chair call); buttons; the Skill card
    24: "#E9D3B4",  # panel-edge: Skill card edge
    27: "#C8C0D8",  # ghost-faded: the old headset round her neck (chair call)
}
INK = ROW[22]
SHADE_K = R.SHADE_K   # 0.85, neutral grey multiplier
shade = R.shade
CREAM = R.CREAM
NOTE = R.NOTE

# ---------------------------------------------------------------- body map landmarks (front view units)
LM = {
    "bun_top": 40,
    "hair_top": 70,      # top of the hair cap (skull + 4)
    "hairline": 88,      # front hairline at the centre
    "temple": 112,       # hairline at the temples (sides)
    "brow": 113,
    "eye": 126,          # eye line; the ear points sit on it
    "eye_x": (132, 168),
    "ear_x": (93, 207),
    "mouth": (134, 140, 166, 160),   # mouth zone x0, y0, x1, y1
    "chin": 172,
    "neck": 180,         # neck line: the headset band rests here
    "cups": 194,         # headset cup centres (on the collarbones, at the band ends)
    "cup_x": (117, 183),
    "shoulder": 206,     # arm root
    "shoulder_x": (90, 210),
    "chest": 214,
    "hands": 262,        # folded hands (rest)
    "belly": 280,        # widest point of the pear
    "hem": 316,
    "ankle": 326,
    "sole": 340,
}

# ---------------------------------------------------------------- hand-drawn half outlines (right half, x >= 150)
HEAD_HALF = "M150,74 C184,74 206,96 206,126 C206,156 184,172 150,172"
CAP_HALF = "M150,70 C187,70 210,95 210,126 C210,157 186,176 150,176"
BODY_PEAR = ("M166,176 C186,178 200,186 207,200 "          # small sloping shoulders
             "C219,224 232,252 232,280 "                  # the round pear: widest at the belly
             "C232,304 214,316 188,316 L150,316")
# Explore alternatives
BODY_CAPSULE = "M164,176 C190,176 206,190 206,214 L206,290 C206,308 196,316 180,316 L150,316"
BODY_BELL = "M166,176 C186,178 198,188 202,204 C210,240 224,290 234,322 C236,330 224,332 200,332 L150,332"
BODY_EGG = "M160,176 C196,178 226,218 226,262 C226,300 202,318 150,318"
BODY_BOX = "M168,176 C200,176 222,180 224,196 L224,300 C224,314 214,316 200,316 L150,316"

# ---------------------------------------------------------------- front marks (drawn by hand)
HAIRLINE = ("M95,116 C98,108 103,103 109,100 C112,96 118,93 124,92 C130,88 140,88 150,89 "   # soft waves: hair,
            "C160,88 170,88 176,92 C182,93 188,96 191,100 C197,103 202,108 205,116")         # not a hat brim
FACE = HAIRLINE + " L205,178 L95,178 Z"   # skin below the hairline
PARTING = "M150,90 C150,82 150,76 150,71"
COMB = ["M112,99 C118,88 128,80 140,75", "M128,91 C134,84 140,79 146,74",            # strands swept up and
        "M188,99 C182,88 172,80 160,75", "M172,91 C166,84 160,79 154,74"]             # back into the bun
NAPE = "M92,118 L208,118 C208,148 196,166 176,172 C162,176 138,176 124,172 C104,166 92,148 92,124 Z"
BROWS = ["M123,113 C127,110 135,109 140,111", "M160,111 C165,109 173,110 177,113"]
SMILE = "M137,148 C142,156 158,156 163,148"                    # closed warm smile (rest)
TALK = "M137,146 C145,149 155,149 163,146 C161,156 156,161 150,161 C144,161 139,156 137,146 Z"
LAUGH = ["M129,145 C128,149 129,152 131,154", "M171,145 C172,149 171,152 169,154"]   # smile creases
HAPPY_EYES = ["M125,128 C128,121 136,121 139,128", "M161,128 C164,121 172,121 175,128"]
PLACKET = "M150,184 L150,314"
BUTTONS = [(150, 214), (150, 238)]
POCKETS = ["M108,272 L134,274 L133,292 C131,298 112,297 110,292 Z",
           "M192,272 L166,274 L167,292 C169,298 188,297 190,292 Z"]


# ---------------------------------------------------------------- transforms
def rot_z(a, pivot=(0.0, 0.0, 0.0)):
    """Roll in the front plane (X, H) by a degrees about a pivot. Positive = her head to the viewer's right."""
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    px, ph, pz = pivot

    def f(q):
        x, h, z = q[0] - px, q[1] - ph, q[2] - pz
        return (px + x * c + h * s, ph - x * s + h * c, pz + z)
    return f


def rot_x(a, pivot=(0.0, 0.0, 0.0)):
    """Nod: positive tips the top forward (toward +Z)."""
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    px, ph, pz = pivot

    def f(q):
        x, h, z = q[0] - px, q[1] - ph, q[2] - pz
        return (px + x, ph + h * c - z * s, pz + h * s + z * c)
    return f


def chain(*fs):
    def f(q):
        for g in fs:
            if g:
                q = g(q)
        return q
    return f


def box(name, color, c, w, h, d, tilt=0.0, bias=0.0):
    """A thin box (the Skill card), centred at c, tilted back by `tilt` degrees about X."""
    rx = rot_x(-tilt, c)
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                pts.append(rx((c[0] + sx * w / 2, c[1] + sy * h / 2, c[2] + sz * d / 2)))
    nrm = [(0, 0, 1)] * len(pts)
    return Part(name, color, [pts], [nrm], bias=bias)


# ---------------------------------------------------------------- the model
def model(o=None):
    """Build Auntie Dot. o: options for the explore thumbnails, the expressions and the poses."""
    o = dict(o or {})
    C = {"body": ROW[11], "skin": ROW[15], "hair": ROW[23], "headset": ROW[27], "shoe": ROW[5], "leg": ROW[15],
         "button": ROW[23]}
    C.update(o.get("colors", {}))
    body_half = o.get("body", BODY_PEAR)
    bun = o.get("bun", "topback")          # topback, top, nape, double, none
    glasses = o.get("glasses", False)
    arms = o.get("arms", "folded")         # folded, sides, talk, card
    face = o.get("face", "smile")          # smile, talk, happy
    headset = o.get("headset", "neck")     # neck, none
    head_s = o.get("head_s", 1.0)
    head_tilt = o.get("head_tilt", 0.0)    # roll, degrees
    head_nod = o.get("head_nod", 0.0)
    legs = o.get("legs", True)
    parts = []
    no_head = o.get("no_head", False)
    hf = chain(rot_x(head_nod, (0, GROUND - LM["chin"], 0)), rot_z(head_tilt, (0, GROUND - LM["chin"] - 6, 0)))

    def sc_path(d):
        if head_s == 1.0:
            return d
        return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
                      lambda m: f"{150 + (float(m.group(1)) - 150) * head_s:.1f},"
                                f"{172 - (172 - float(m.group(2))) * head_s:.1f}", d)

    # ---- head: skin head, hair cap (with the face marks), bun, ears
    head = revolved("head", C["skin"], sc_path(HEAD_HALF), depth=0.92, step=3)
    head.flat = True
    head.pxf = hf
    parts.append(head)
    cap = hair_cap(sc_path(CAP_HALF), C["hair"], int(172 - (172 - LM["temple"]) * head_s))
    marks = [("face", sc_path(FACE), C["skin"], None, 0), ("line", sc_path(HAIRLINE), None, INK, 2.2)]
    marks += [("line", sc_path(d), None, INK, 1.5) for d in COMB]
    marks += [("line", sc_path(d), None, INK, 2.6) for d in BROWS]
    if face == "happy":
        marks += [("line", sc_path(d), None, INK, 3.6) for d in HAPPY_EYES]
    else:
        for (x, y) in [(LM["eye_x"][0], LM["eye"]), (LM["eye_x"][1], LM["eye"])]:
            x, y = 150 + (x - 150) * head_s, 172 - (172 - y) * head_s
            marks.append(("fill", oval(x, y, 6.5, 8.5), INK, None, 0))
            marks.append(("fill", oval(x + 2, y - 3.2, 2.0, 2.4), ROW[23], None, 0))
    if face == "talk":
        marks.append(("fill", sc_path(TALK), INK, None, 0))
    else:
        marks.append(("line", sc_path(SMILE), None, INK, 3.2))
    if glasses:
        for x in LM["eye_x"]:
            x = 150 + (x - 150) * head_s
            marks.append(("line", oval(x, 172 - (172 - LM["eye"]) * head_s, 12, 11), None, INK, 2.2))
        marks.append(("line", sc_path("M144,124 C147,121 153,121 156,124"), None, INK, 2.2))
    cap.marks = marks
    cap.face_host = head.host
    cap.pxf = hf
    parts.append(cap)
    hb_ = hair_back(sc_path(CAP_HALF), C["hair"], int(172 - (172 - LM["temple"]) * head_s), head_s)
    cap.cull_from = len(cap.pieces)             # the back hair joins the cap: one outline, no seam
    cap.pieces += hb_.pieces
    cap.normals += hb_.normals
    hy = 172 - (172 - LM["eye"]) * head_s
    for s in (-1, 1):
        e = ellipsoid("ear", C["skin"], (s * 56 * head_s, GROUND - hy - 2, -4), (5, 10, 7))
        e.pxf = hf
        parts.append(e)
    buns = {"topback": [((0, 60, -18), (25, 21, 23))], "top": [((0, 52, -2), (24, 20, 22))],
            "nape": [((0, 152, -52), (22, 19, 18))], "double": [((-40, 82, -10), (17, 15, 16)),
                                                                 ((40, 82, -10), (17, 15, 16))],
            "none": []}[bun]
    for (bx, by, bz), rad in buns:
        by = 172 - (172 - by) * head_s
        b = ellipsoid("bun", C["hair"], (bx * head_s, GROUND - by, bz * head_s), rad, bias=-0.4)
        b.pxf = hf
        parts.append(b)

    if no_head:
        parts = []
    # ---- neck, body (cardigan dress) with placket, buttons, pockets
    parts.append(revolved("neck", C["skin"], "M167,166 C167,172 167,178 167,190", depth=0.9, bias=-4))
    bd = revolved("body", C["body"], body_half, depth=0.85, step=4)
    bm = [("line", PLACKET, None, INK, 1.6)]
    bm += [("fill", oval(x, y, 4.2, 4.2), C["button"], INK, 1.2) for x, y in BUTTONS]
    bm += [("fill", d, C["body"], INK, 1.4) for d in POCKETS]
    bd.marks = bm
    parts.append(bd)
    bprof = profile(body_half)

    def surf_z(x, y, out=0.0):
        r = r_at(bprof, y)
        rz = r * 0.85
        return rz * math.sqrt(max(1 - (x / max(r, 1e-3)) ** 2, 0.0)) + out

    # ---- headset round the neck: band behind the neck on the shoulders, one cup each side under the chin
    if headset == "neck":
        hb = GROUND - LM["neck"]
        cxs = LM["cup_x"][1] - 150
        czs = surf_z(cxs, LM["cups"], 5.0)
        band = []
        for k in range(0, 25):
            a = math.radians(-112 + 224 * k / 24)        # 0 = straight back, behind the neck
            band.append((38 * math.sin(a), hb - 3 * max(0.0, -math.cos(a)), -33 * math.cos(a)))
        # each end runs forward and down over the collarbone into the top of its cup
        e0, e1 = band[0], band[-1]
        head_pts = [(-cxs, GROUND - LM["cups"] + 9, czs - 3), (-cxs - 3, GROUND - LM["cups"] + 13, (e0[2] + czs) / 2)]
        tail_pts = [(cxs + 3, GROUND - LM["cups"] + 13, (e1[2] + czs) / 2), (cxs, GROUND - LM["cups"] + 9, czs - 3)]
        bpts = head_pts + band + tail_pts
        bt = tube("band", C["headset"], bpts, [3.6] * len(bpts), n=10)
        bt.after = "body"
        bt.occluder = ((0.0, hb, 0.0), 21.0)     # the neck hides the part of the band behind it
        parts.append(bt)
        for s in (-1, 1):
            tilt = math.radians(-22)      # the flat face looks forward and a little up: resting on the collarbone
            rot = (lambda x, y, z, t=tilt: (x, y * math.cos(t) - z * math.sin(t), y * math.sin(t) + z * math.cos(t)))
            parts.append(ellipsoid("cup", C["headset"], (s * cxs, GROUND - LM["cups"], czs), (12.5, 12.5, 6.5),
                                   bias=1.2, rot=rot))

    # ---- arms: continuous sleeve from inside the body, hand balls
    for s in (-1, 1):
        sh = (s * 52, GROUND - LM["shoulder"], 0)
        a = arms
        if a == "talk" and s == 1:
            a = "folded"
        if a == "card" and s == 1:
            a = "folded_one"
        if a == "folded":
            el = (s * 80, GROUND - 238, 20)
            wr = (s * 46, GROUND - 260, surf_z(46, 260, 8))
            hd = (s * 18, GROUND - LM["hands"], surf_z(18, LM["hands"], 9))
        elif a == "folded_one":
            el = (s * 80, GROUND - 238, 20)
            wr = (s * 46, GROUND - 260, surf_z(46, 260, 8))
            hd = (s * 14, GROUND - LM["hands"] + 2, surf_z(14, LM["hands"], 10))
        elif a == "sides":
            el = (s * (r_at(bprof, 236) + 6), GROUND - 236, 4)
            wr = (s * (r_at(bprof, 262) + 9), GROUND - 262, 8)
            hd = (s * (r_at(bprof, 274) + 10), GROUND - 274, 10)
        elif a == "talk":   # her right hand up beside the face, palm out
            el = (s * 96, GROUND - 236, 14)
            wr = (s * 96, GROUND - 196, 22)
            hd = (s * 94, GROUND - 180, 24)
        elif a == "card":   # her right hand forward, holding the Skill card out
            el = (s * 72, GROUND - 238, 46)
            wr = (s * 50, GROUND - 236, 94)
            hd = (s * 42, GROUND - 234, 104)
        cuff = el
        parts.append(tube("sleeve", C["body"], [sh, el, wr], [11.5, 11.0, 10.0], bias=0.4))
        parts.append(ellipsoid("hand", C["skin"], hd, (10, 10.5, 10), bias=0.6))
        if a == "card":
            parts.append(box("card", ROW[23], (hd[0] + s * 4, hd[1] + 22, hd[2] + 8), 30, 42, 3, tilt=8, bias=0.2))
            parts.append(ellipsoid("coin", ROW[13], (hd[0] + s * 4, hd[1] + 28, hd[2] + 10.5), (8, 8, 1.5), bias=0.4))

    # ---- legs and shoes
    if legs:
        top = LM["hem"] - 8
        for s in (-1, 1):
            parts.append(revolved("leg", C["leg"], f"M161,{top} C161,{top + 6} 161,{LM['ankle'] - 4} 161,{LM['ankle']}",
                                  depth=1.0, cx=s * 22, bias=-8))
    for s in (-1, 1):
        parts.append(ellipsoid("shoe", C["shoe"], (s * 23, GROUND - 332, 8), (13, 8, 19), bias=-6))
    return parts


def hair_cap(capd, color, ylow):
    """Hair cap = skull + 4 down to the temple line, swept back (one convex piece per ring band)."""
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


def hair_back(capd, color, ytop, head_s=1.0):
    """Hair at the back of the head, pulled up into the bun: from the temple line down to the nape.
    Only the ring points behind a line that runs from the temple (z -2) down behind the ear to the nape
    (z -43 at the chin), so the side view shows the hairline running down behind the ear."""
    prof = profile(capd)
    rings = []
    y = ytop - 3
    ybot = 172 - (172 - 170) * head_s
    while y <= ybot:
        r = r_at(prof, y)
        zc = -2 - (y - ytop) * 0.68
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
        for c in range(8):                      # 8 sub-arcs per band, so each can be culled on its own
            a, b = c * 5, c * 5 + 6
            pieces.append(p0[a:b] + p1[a:b])
            normals.append(n0[a:b] + n1[a:b])
    p = Part("hairback", color, pieces, normals, bias=0.35)
    return p


def split(p):
    """One part per piece, so each tube segment sorts by its own depth (the band behind the neck)."""
    out = []
    for pc, nm in zip(p.pieces, p.normals):
        q = Part(p.name, p.color, [pc], [nm], bias=p.bias)
        out.append(q)
    return out


# ---------------------------------------------------------------- render (ricky.render + per-part pose)
def render(parts, yaw=0.0, pitch=0.0, s=1.0, ox=0.0, oy=0.0, ink_w=5.0, mono=None, shade_on=True, mark_scale=1.0,
           xf=None):
    P0, N = cam(yaw, pitch)

    def PP(p):
        f = chain(getattr(p, "pxf", None), xf)
        return lambda q: P0(f(q))
    order = []
    for p in parts:
        P = PP(p)
        allp = [q for pc in p.pieces for q in pc]
        dep = sum(P(q)[2] for q in allp) / max(len(allp), 1)
        order.append([dep + p.bias * 3, p])
    by = {p.name: d for d, p in order}
    for t in order:
        f = getattr(t[1], "after", None)
        if f and f in by:
            t[0] = by[f] + 0.01
    order.sort(key=lambda t: t[0])
    out = []
    for _, p in order:
        P = PP(p)
        polys, lits = [], []
        occ = getattr(p, "occluder", None)
        if occ:
            uc, vc, dc = P(occ[0])
        cf = getattr(p, "cull_from", None)
        for idx, (pc, nm) in enumerate(zip(p.pieces, p.normals)):
            if cf is not None and idx >= cf and sum(N(n)[2] for n in nm) / len(nm) < 0.0:
                continue
            if occ:
                cu = sum(P(q)[0] for q in pc) / len(pc)
                cd = sum(P(q)[2] for q in pc) / len(pc)
                if cd < dc and abs(cu - uc) < occ[1]:
                    continue
            polys.append(hull([P(q)[:2] for q in pc]))
            if nm and shade_on and not mono:
                lit = [P(q)[:2] for q, n in zip(pc, nm) if sum(a * b for a, b in zip(N(n), LIGHT)) > -0.15]
                if len(lit) >= 3:
                    lits.append(hull(lit))
        col = mono or p.color
        if p.ink:
            out += [f'<path d="{poly(h, s, ox, oy)}" fill="{INK if not mono else mono}" '
                    f'stroke="{INK if not mono else mono}" stroke-width="{ink_w * 2:.2f}" stroke-linejoin="round"/>'
                    for h in polys if len(h) >= 3]
        if mono:
            out += [f'<path d="{poly(h, s, ox, oy)}" fill="{mono}" stroke="none"/>' for h in polys if len(h) >= 3]
            continue
        if getattr(p, "flat", False):
            lits = []
        base = shade(col) if (shade_on and lits) else col
        out += [f'<path d="{poly(h, s, ox, oy)}" fill="{base}" stroke="{base}" stroke-width="0.6"/>'
                for h in polys if len(h) >= 3]
        out += [f'<path d="{poly(h, s, ox, oy)}" fill="{col}" stroke="{col}" stroke-width="0.6"/>'
                for h in lits if len(h) >= 3]
        host = getattr(p, "host", None)
        for kind, d, fill, stroke, sw in p.marks:
            hst = getattr(p, "face_host", host) if kind == "face" else host
            pts, nrm = lift_mark(hst, d, back=(kind == "back"))
            vis = [N(n)[2] for n in nrm]
            if sum(1 for v in vis if v > 0.02) < 0.3 * len(vis):
                continue
            if kind == "line":
                run, runs = [], []
                for q, v in zip(pts, vis):
                    if v > 0.02:
                        run.append(P(q)[:2])
                    elif run:
                        runs.append(run)
                        run = []
                if run:
                    runs.append(run)
                for r_ in runs:
                    if len(r_) >= 2:
                        out.append(f'<path d="{line(r_, s, ox, oy)}" fill="none" stroke="{stroke}" '
                                   f'stroke-width="{sw * mark_scale * s:.2f}" stroke-linecap="round"/>')
                continue
            sp = []
            for q, v in zip(pts, vis):
                u, w, _ = P(q)
                if v <= 0.02:
                    u, w = R.limb_point(hst, q, yaw, u, P)
                sp.append((u, w))
            st = (f' stroke="{stroke}" stroke-width="{sw * mark_scale * s:.2f}" stroke-linejoin="round"'
                  if stroke else ' stroke="none"')
            out.append(f'<path d="{poly(sp, s, ox, oy)}" fill="{fill}"{st}/>')
    return "".join(out)


def pbounds(parts, yaw=0.0, pitch=0.0, xf=None):
    P0, _ = cam(yaw, pitch)
    xs, ys = [], []
    for p in parts:
        f = chain(getattr(p, "pxf", None), xf)
        for pc in p.pieces:
            for q in pc:
                x, y, _ = P0(f(q))
                xs.append(x)
                ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)
