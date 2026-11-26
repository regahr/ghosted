"""Recruiter Ricky sketch: hand-drawn front curves -> a toy-pawn 3D sketch model -> any view.

Every shape starts as a hand-written cubic Bezier half outline or front mark (front view, y down, axis x 150,
sole y 340, hair top y 36: 304 units = 1.00 m). Python lifts them onto round bodies so the four views, the game
camera, the drain and the gestures all agree. It is a sketch aid for the 3D builder, not the 3D model.
"""
import math
import re

M_PER_U = 1.0 / 304.0
GROUND = 340.0

# ---------------------------------------------------------------- palette (seats/lena-park.md rows)
ROW = {
    5: "#7A4A2E",   # wood: shoes
    10: "#C9A6D6",  # hq-wall: Ricky accent (headset + tie); also the Ghostie tie
    11: "#7A5596",  # hq-roof: drain step 1 suit
    15: "#F2C79E",  # skin
    16: "#F8F4EA",  # ghost: shirt V, collar, cuffs, teeth; drain end body
    17: "#2E2C3D",  # recruiter suit
    22: "#2B1E16",  # ink
    25: "#4A3226",  # hair
    27: "#C8C0D8",  # ghost-faded: drain step 2 suit, Ghostie headset
}
INK = ROW[22]
SHADE_K = 0.85      # neutral grey multiplier for the shade side (brief: "shade a neutral grey multiplier only")
CREAM = "#FDE6C8"   # card background (same as the Ghostie sheet)
NOTE = "#1D63C8"    # guides and notes, not a character colour


def shade(hexc, k=SHADE_K):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (round(r * k), round(g * k), round(b * k))


# ---------------------------------------------------------------- body map landmarks (front view units)
LM = {
    "top": 36,          # top of the quiff
    "crown": 53,        # top of the hair cap (skull + 3)
    "eye": 98,          # eye line; the ear points sit on it
    "ear_x": (89, 211), # ear points (head side + 1); cups centre at x 89 / 211
    "mouth": (125, 110, 175, 134),   # mouth zone x0, y0, x1, y1 (wide smile)
    "chin": 150,
    "neck": 152,        # neck line = collar top
    "knot": 160,        # knot top
    "shoulder": 176,    # shoulder joint centre (arm root)
    "shoulder_x": (82, 218),
    "chest": 200,
    "tie_v": 232,
    "shirt_v": 238,
    "wrist": 234,
    "hand": 246,
    "hem": 268,         # jacket hem
    "knee": 296,
    "ankle": 318,
    "sole": 340,
}

# ---------------------------------------------------------------- hand-drawn half outlines (right half, x >= 150)
HEAD_HALF = ("M150,56 C185,56 206,76 206,104 "
             "C206,132 184,150 150,150")
JACKET_HALF = ("M168,148 C190,150 210,158 214,174 "     # soft shoulder line
               "C218,198 220,230 223,254 "              # the jacket flares a little: a bell
               "C224,264 216,268 204,268 L150,268")
# Explore alternatives (thumbnails only)
JACKET_BOX = "M168,148 C204,148 224,150 226,166 C226,200 226,240 226,262 C226,268 220,268 210,268 L150,268"
JACKET_TRI = "M168,148 C210,146 240,154 240,170 C234,200 214,236 196,262 C194,268 188,268 182,268 L150,268"
JACKET_CAP = "M160,146 C186,146 204,164 204,196 C204,230 204,250 198,262 C192,272 176,272 150,272"
JACKET_CONE = "M164,148 C180,150 190,158 192,170 C204,200 224,240 244,266 C244,270 230,272 206,272 L150,272"
JACKET_EGG = "M164,150 C204,152 236,180 238,218 C240,256 214,276 150,278"

# ---------------------------------------------------------------- front marks (full shapes, drawn by hand)
EYES = [(132, 98), (168, 98)]
BROWS = ["M121,83 C126,78 136,77 141,80", "M159,80 C164,77 174,78 179,83"]
SMILE = "M125,111 C138,114 162,114 175,111 C171,126 161,134 150,134 C139,134 129,126 125,111 Z"
TEETH = "M128,112.5 C140,115.5 160,115.5 172,112.5 C171,117.5 129,117.5 128,112.5 Z"
FACE = ("M95,92 C99,78 112,71 128,71 C139,71 146,74 150,76 C154,74 161,71 172,71 "
        "C188,71 201,78 205,92 L205,152 L95,152 Z")     # skin seen below the hairline (on the cap surface)
NAPE = "M93,86 L207,86 C209,118 198,136 178,144 C163,149 137,149 122,144 C102,136 91,118 93,92 Z"
HAIR_PART = "M124,58 C134,50 166,50 176,58"
SHIRT_V = "M131,152 C142,155 158,155 169,152 C166,184 159,214 150,238 C141,214 134,184 131,152 Z"
COLLAR = ["M150,156 C143,151 136,149 129,150 C130,156 133,162 137,167 C141,164 146,160 150,156 Z",
          "M150,156 C157,151 164,149 171,150 C170,156 167,162 163,167 C159,164 154,160 150,156 Z"]
TIE_KNOT = "M142,159 L158,159 L155,171 L145,171 Z"
TIE_BLADE = "M145.5,172 C144,188 141,204 139,216 L150,232 L161,216 C159,204 156,188 154.5,172 Z"
BUTTON = (150, 250)
LAPELS = ["M131,152 C134,184 141,214 150,238", "M169,152 C166,184 159,214 150,238"]


# ---------------------------------------------------------------- Bezier helpers
def bez(p0, p1, p2, p3, n=16):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def path_points(d, n=14):
    """Sample an M/C/L/Z path into a polyline (list of (x, y))."""
    toks = re.findall(r"[MCLZ]|-?\d+(?:\.\d+)?", d)
    pts, cur, i, cmd = [], None, 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MCLZ":
            cmd = t
            i += 1
            if t == "Z":
                if pts:
                    pts.append(pts[0])
            continue
        if cmd == "M":
            cur = (float(t), float(toks[i + 1]))
            pts.append(cur)
            i += 2
            cmd = "L"
        elif cmd == "L":
            nxt = (float(t), float(toks[i + 1]))
            for k in range(1, n + 1):
                pts.append((cur[0] + (nxt[0] - cur[0]) * k / n, cur[1] + (nxt[1] - cur[1]) * k / n))
            cur = nxt
            i += 2
        elif cmd == "C":
            p1 = (float(toks[i]), float(toks[i + 1]))
            p2 = (float(toks[i + 2]), float(toks[i + 3]))
            p3 = (float(toks[i + 4]), float(toks[i + 5]))
            pts += bez(cur, p1, p2, p3, n)[1:]
            cur = p3
            i += 6
    return pts


def profile(half, n=20):
    """Half-width r(y) from a hand-drawn right half outline."""
    pts = [(y, x - 150) for x, y in path_points(half, n) if x >= 150]
    pts.sort()
    return pts


def r_at(prof, y):
    if y <= prof[0][0]:
        return max(prof[0][1], 0.0) if y >= prof[0][0] - 0.5 else 0.0
    for (y0, r0), (y1, r1) in zip(prof, prof[1:]):
        if y0 <= y <= y1:
            return r0 + (r1 - r0) * (y - y0) / max(y1 - y0, 1e-6)
    return prof[-1][1]


# ---------------------------------------------------------------- 3D parts (points: X right, H up, Z front)
class Part:
    def __init__(self, name, color, pieces, normals=None, marks=None, bias=0.0, ink=True, stroke=None):
        self.name, self.color, self.pieces = name, color, pieces      # pieces: list of point clouds (convex)
        self.normals = normals or [None] * len(pieces)
        self.marks = marks or []
        self.bias = bias
        self.ink = ink
        self.stroke = stroke    # for curve parts: (width) drawn as a polyline


def ring(cx, h, cz, rx, rz, n=24):
    pts, nrm = [], []
    for k in range(n):
        a = 2 * math.pi * k / n
        s, c = math.sin(a), math.cos(a)
        pts.append((cx + rx * s, h, cz + rz * c))
        nrm.append((s / max(rx, 1e-3), 0.0, c / max(rz, 1e-3)))
    return pts, nrm


def revolved(name, color, half, depth=0.9, cx=0.0, cz=0.0, y0=None, y1=None, step=4, rscale=1.0, cap=True,
             marks=None, bias=0.0, sy=1.0, lift=0.0):
    prof = profile(half)
    ya, yb = prof[0][0], prof[-1][0]
    ya = ya if y0 is None else max(ya, y0)
    yb = yb if y1 is None else min(yb, y1)
    ys = [ya + (yb - ya) * k / max(1, int((yb - ya) / step)) for k in range(int((yb - ya) / step) + 1)]
    rings = []
    for y in ys:
        r = r_at(prof, y) * rscale
        rings.append(ring(cx, (GROUND - y) * sy + lift, cz, max(r, 0.5), max(r * depth, 0.5)))
    pieces, normals = [], []
    for (p0, n0), (p1, n1) in zip(rings, rings[1:]):
        pieces.append(p0 + p1)
        normals.append(n0 + n1)
    host = {"prof": prof, "depth": depth, "cx": cx, "cz": cz, "rscale": rscale, "sy": sy, "lift": lift}
    p = Part(name, color, pieces, normals, marks, bias)
    p.host = host
    return p


def ellipsoid(name, color, c, rad, n=14, bias=0.0, rot=None):
    pts, nrm = [], []
    for i in range(1, n):
        th = math.pi * i / n
        for k in range(2 * n):
            ph = 2 * math.pi * k / (2 * n)
            ux, uy, uz = math.sin(th) * math.sin(ph), math.cos(th), math.sin(th) * math.cos(ph)
            x, y, z = rad[0] * ux, rad[1] * uy, rad[2] * uz
            nx, ny, nz = ux / rad[0], uy / rad[1], uz / rad[2]
            if rot:
                x, y, z = rot(x, y, z)
                nx, ny, nz = rot(nx, ny, nz)
            pts.append((c[0] + x, c[1] + y, c[2] + z))
            nrm.append((nx, ny, nz))
    pts += [(c[0], c[1] + rad[1], c[2]), (c[0], c[1] - rad[1], c[2])]
    nrm += [(0, 1, 0), (0, -1, 0)]
    return Part(name, color, [pts], [nrm], bias=bias)


def _perp(d):
    a = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = (d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0])
    lu = math.sqrt(sum(c * c for c in u))
    u = tuple(c / lu for c in u)
    v = (d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0])
    return u, v


def tube(name, color, pts, radii, n=16, bias=0.0, colors=None):
    """A tube along 3D points; one convex piece per segment. colors: optional per-segment colour list."""
    circles = []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        ld = math.sqrt(sum(c * c for c in d)) or 1.0
        d = tuple(c / ld for c in d)
        u, v = _perp(d)
        cp, cn = [], []
        for k in range(n):
            t = 2 * math.pi * k / n
            nn = tuple(math.cos(t) * u[j] + math.sin(t) * v[j] for j in range(3))
            cp.append(tuple(p[j] + radii[i] * nn[j] for j in range(3)))
            cn.append(nn)
        circles.append((cp, cn))
    pieces = [c0[0] + c1[0] for c0, c1 in zip(circles, circles[1:])]
    normals = [c0[1] + c1[1] for c0, c1 in zip(circles, circles[1:])]
    p = Part(name, color, pieces, normals, bias=bias)
    p.seg_colors = colors
    # end caps (round): small spheres
    return p


def lift_mark(host, d, off=0.6, n=10, back=False):
    """Front 2D mark path -> 3D points on the host's round surface (plus normals)."""
    pts, nrm = [], []
    for x, y in path_points(d, n):
        r = r_at(host["prof"], y) * host["rscale"]
        X = x - 150 - host["cx"]
        X = max(-r, min(r, X))
        rz = r * host["depth"]
        z = rz * math.sqrt(max(1 - (X / max(r, 1e-3)) ** 2, 0.0))
        if back:
            z = -z
        nx, nz = X / max(r, 1e-3) ** 2, z / max(rz, 1e-3) ** 2
        ln = math.sqrt(nx * nx + nz * nz) or 1.0
        nx, nz = nx / ln, nz / ln
        pts.append((X + host["cx"] + off * nx, (GROUND - y) * host["sy"] + host["lift"], z + host["cz"] + off * nz))
        nrm.append((nx, 0.0, nz))
    return pts, nrm


# ---------------------------------------------------------------- the model
def model(o=None):
    """Build Ricky. o: options dict for the explore thumbnails, the drain steps and the poses."""
    o = dict(o or {})
    C = {"suit": ROW[17], "skin": ROW[15], "hair": ROW[25], "acc": ROW[10], "head_acc": ROW[10],
         "shirt": ROW[16], "shoe": ROW[5], "leg": ROW[17], "hand": ROW[15], "tie": ROW[10]}
    C.update(o.get("colors", {}))
    jacket = o.get("jacket", JACKET_HALF)
    lift = o.get("lift", 0.0)           # float height (units)
    legs = o.get("legs", 1.0)           # 1 = full, 0.5 = fading, 0 = gone
    mouth = o.get("mouth", "smile")     # smile, small, none
    hair = o.get("hair", "pomp")        # pomp, none, slick, side
    head_s = o.get("head_s", 1.0)
    mic = o.get("mic", True)
    arm = o.get("arm", "rest")          # rest, phone, hop_up
    merge = o.get("merge", 0.0)         # drain step 2: neck fills, hem softens
    parts = []

    # head (+ hair cap with the face marks on it)
    hy = 98.0
    head_half = HEAD_HALF
    if head_s != 1.0:
        def sc(m):
            x, y = float(m.group(1)), float(m.group(2))
            return f"{150 + (x - 150) * head_s:.1f},{150 - (150 - y) * head_s:.1f}"
        head_half = re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", sc, HEAD_HALF)
    head = revolved("head", C["skin"], head_half, depth=0.92, step=3, lift=lift)
    parts.append(head)
    capd = "M150,53 C187,53 209,75 209,104 C209,133 186,153 150,153"
    if head_s != 1.0:
        capd = re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
                      lambda m: f"{150 + (float(m.group(1)) - 150) * head_s:.1f},{150 - (150 - float(m.group(2))) * head_s:.1f}",
                      capd)
    face_marks = []
    capc = C["hair"] if hair != "none" else C["skin"]
    cap = hair_cap(capd, capc, lift, hair)
    if hair != "none":
        face_marks.append(("face", FACE, C["skin"], None, 0.4))
        face_marks.append(("back", NAPE, capc, None, 0))
    for b in BROWS:
        face_marks.append(("line", b, None, INK, 3.0))
    for (x, y) in EYES:
        face_marks.append(("fill", oval(x, y, 6.5, 9.5), INK, None, 0))
        face_marks.append(("fill", oval(x + 2, y - 3.5, 2.0, 2.4), ROW[16], None, 0))
    if mouth == "smile":
        face_marks.append(("fill", SMILE, INK, None, 0))
        face_marks.append(("fill", TEETH, ROW[16], None, 0))
    elif mouth == "small":
        face_marks.append(("fill", oval(150, 121, 7, 5), INK, None, 0))
    cap.marks = face_marks
    cap.face_host = head.host
    head.flat = True
    parts.append(cap)
    # ears (under the cups)
    for s in (-1, 1):
        parts.append(ellipsoid("ear", C["skin"], (s * 56, GROUND - hy + lift - 2, -2), (5, 10, 7)))

    # headset: band over the crown (in the ear plane, slightly behind), a cup on each ear point
    if C.get("head_acc"):
        band = []
        for k in range(0, 21):
            a = math.pi * k / 20
            band.append((-63 * math.cos(a), GROUND - (hy - 8) + lift + 58 * math.sin(a), -6))
        parts.append(tube("band", C["head_acc"], band, [3.6] * len(band), n=10))
        for s in (-1, 1):
            parts.append(ellipsoid("cup", C["head_acc"], (s * 61, GROUND - hy + lift - 2, -2), (7, 17, 13), bias=0.3))
        if mic:
            mp = [(-62, GROUND - 110 + lift, 6), (-57, GROUND - 121 + lift, 20), (-46, GROUND - 126 + lift, 34)]
            parts.append(tube("mic", C.get("mic", C["head_acc"]), mp, [1.8] * 3, n=8, bias=0.4))
            parts.append(ellipsoid("micball", C.get("mic", C["head_acc"]), (-44, GROUND - 126 + lift, 36), (4.5, 4.5, 4.5), bias=0.5))

    # neck (hidden under the collar) and jacket with the shirt V, collar, tie and button
    nk = revolved("neck", C["skin"], "M168,138 C168,146 168,150 168,158", depth=0.9, lift=lift, bias=-4)
    parts.append(nk)
    jk = revolved("jacket", C["suit"], jacket, depth=0.82, step=4, lift=lift)
    jm = [("fill", SHIRT_V, C["shirt"], INK, 1.4)]
    jm += [("line", d, None, INK, 1.6) for d in LAPELS]
    jm += [("fill", c, C["shirt"], INK, 1.3) for c in COLLAR]
    jm.append(("fill", TIE_BLADE, C["tie"], INK, 1.8))
    jm.append(("fill", TIE_KNOT, C["tie"], INK, 1.8))
    jm.append(("fill", oval(*BUTTON, 3.2, 3.2), INK, None, 0))
    jk.marks = jm
    if merge:
        jk.bias = -0.5
    parts.append(jk)

    # arms: shoulder ball (the join), sleeve, shirt cuff, hand
    ax = r_at(profile(jacket), LM["shoulder"] + 6) - 6
    dx = ax - 60
    for s in (-1, 1):
        sh = (s * (66 + dx), GROUND - LM["shoulder"] + lift, 0)
        if arm == "phone" and s == -1:          # Ricky's right hand on the right cup (viewer-left in front)
            el = (s * dx + s * 102, GROUND - 200 + lift, 16)
            wr = (s * dx + s * 88, GROUND - 130 + lift, 12)
            hd = (s * dx + s * 77, GROUND - 104 + lift, 4)
        elif arm == "hop_up":
            el = (s * dx + s * 88, GROUND - 190 + lift, 4)
            wr = (s * dx + s * 98, GROUND - 204 + lift, 6)
            hd = (s * dx + s * 104, GROUND - 210 + lift, 6)
        else:
            el = (s * dx + s * 76, GROUND - 206 + lift, 2)
            wr = (s * dx + s * 78, GROUND - 230 + lift, 6)
            hd = (s * dx + s * 79, GROUND - 246 + lift, 8)
        cuff = tuple(wr[j] + (hd[j] - wr[j]) * 0.3 for j in range(3))
        parts.append(ellipsoid("shoulder", C["suit"], sh, (13, 13, 12), bias=-0.2))
        parts.append(tube("sleeve", C["suit"], [sh, el, wr], [13.5, 12.5, 11.5], bias=0.1))
        parts.append(tube("cuff", C["shirt"], [wr, cuff], [11.0, 10.0], bias=0.15))
        parts.append(ellipsoid("hand", C["hand"], hd, (10.5, 11, 10.5), bias=0.2))

    # legs and shoes
    if legs > 0:
        top = LM["hem"] - 6
        bot = LM["ankle"] if legs >= 1 else LM["hem"] + (LM["ankle"] - LM["hem"]) * legs
        for s in (-1, 1):
            parts.append(revolved("leg", C["leg"], f"M163,{top} C163,{top + 10} 162,{bot - 10} 162,{bot}",
                                  depth=1.0, cx=s * 21, lift=lift, bias=-8))
            if legs >= 1:
                parts.append(ellipsoid("shoe", C["shoe"], (s * 22, GROUND - 330 + lift, 9), (14, 10, 21), bias=-6))
    return parts


def hair_cap(capd, color, lift, hair):
    """Hair cap = the skull + 3 down to the temples, hugging the back of the head down to the nape,
    plus the pompadour roll as one more convex piece of the same part (one outline, no inner line)."""
    prof = profile(capd)
    pieces, normals, rings = [], [], []
    ytop = prof[0][0]
    ylow = 88 if hair != "none" else 60
    y = ytop
    while y <= ylow:
        r = r_at(prof, y)
        rr, cz = r, 0.0
        rings.append(ring(0, GROUND - y + lift, cz, max(rr, 0.5), max(rr * 0.92, 0.5)))
        y += 3
    for (p0, n0), (p1, n1) in zip(rings, rings[1:]):
        if hair == "none":
            break
        pieces.append(p0 + p1)
        normals.append(n0 + n1)
    if hair in ("pomp", "side", "slick"):
        c, rad = {"pomp": ((0, 50, 4), (33, 14, 27)), "side": ((14, 56, 12), (40, 12, 36)),
                  "slick": ((0, 60, -4), (44, 8, 44))}[hair]
        q = ellipsoid("q", color, (c[0], GROUND - c[1] + lift, c[2]), rad)
        pieces += q.pieces
        normals += q.normals
    p = Part("hair", color, pieces, normals, bias=0.5)
    p.after = "head"
    p.host = {"prof": prof, "depth": 0.92, "cx": 0.0, "cz": 0.0, "rscale": 1.0, "sy": 1.0, "lift": lift}
    return p


def oval(cx, cy, rx, ry):
    k = 0.5523
    return (f"M{cx},{cy - ry} C{cx + k * rx},{cy - ry} {cx + rx},{cy - k * ry} {cx + rx},{cy} "
            f"C{cx + rx},{cy + k * ry} {cx + k * rx},{cy + ry} {cx},{cy + ry} "
            f"C{cx - k * rx},{cy + ry} {cx - rx},{cy + k * ry} {cx - rx},{cy} "
            f"C{cx - rx},{cy - k * ry} {cx - k * rx},{cy - ry} {cx},{cy - ry} Z")


# ---------------------------------------------------------------- projection and drawing
LIGHT = (0.45, 0.55, 0.70)   # camera space: from the viewer's upper right, so the shade sits on the left


def cam(yaw, pitch):
    ps, pp = math.radians(yaw), math.radians(pitch)
    cps, sps, cpp, spp = math.cos(ps), math.sin(ps), math.cos(pp), math.sin(pp)

    def P(p):
        X, H, Z = p
        x1 = X * cps - Z * sps
        z1 = X * sps + Z * cps
        up = H * cpp - z1 * spp
        dep = z1 * cpp + H * spp
        return x1, -up, dep

    def N(n):
        X, H, Z = n
        x1 = X * cps - Z * sps
        z1 = X * sps + Z * cps
        up = H * cpp - z1 * spp
        tow = z1 * cpp + H * spp
        ln = math.sqrt(x1 * x1 + up * up + tow * tow) or 1.0
        return x1 / ln, up / ln, tow / ln
    return P, N


def hull(points):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def poly(pts, s=1.0, ox=0.0, oy=0.0):
    return "M" + " L".join(f"{x * s + ox:.2f},{y * s + oy:.2f}" for x, y in pts) + " Z"


def line(pts, s=1.0, ox=0.0, oy=0.0):
    return "M" + " L".join(f"{x * s + ox:.2f},{y * s + oy:.2f}" for x, y in pts)


def render(parts, yaw=0.0, pitch=0.0, s=1.0, ox=0.0, oy=0.0, ink_w=5.0, mono=None, grey=False,
           shade_on=True, mark_scale=1.0, xf=None):
    """SVG of the model. s scales units to output pixels; (ox, oy) is the screen origin of (X=0, H=0).
    mono: draw everything in one colour (silhouette)."""
    P0, N = cam(yaw, pitch)
    P = (lambda q: P0(xf(q))) if xf else P0
    order = []
    for p in parts:
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
        polys, lits = [], []
        for pc, nm in zip(p.pieces, p.normals):
            sp = [P(q)[:2] for q in pc]
            polys.append(hull(sp))
            if nm and shade_on and not mono:
                lit = [P(q)[:2] for q, n in zip(pc, nm)
                       if sum(a * b for a, b in zip(N(n), LIGHT)) > -0.15]
                if len(lit) >= 3:
                    lits.append(hull(lit))
        col = mono or p.color
        if p.ink:
            out += [f'<path d="{poly(h, s, ox, oy)}" fill="{INK if not mono else mono}" stroke="{INK if not mono else mono}" '
                    f'stroke-width="{ink_w * 2:.2f}" stroke-linejoin="round"/>' for h in polys if len(h) >= 3]
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
        # marks on this part's surface
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
                    u, w = limb_point(hst, q, yaw, u, P)
                sp.append((u, w))
            if kind in ("fill", "back", "face"):
                st = (f' stroke="{stroke}" stroke-width="{sw * mark_scale * s:.2f}" stroke-linejoin="round"'
                      if stroke else ' stroke="none"')
                out.append(f'<path d="{poly(sp, s, ox, oy)}" fill="{fill}"{st}/>')
            else:
                out.append(f'<path d="{line(sp, s, ox, oy)}" fill="none" stroke="{stroke}" '
                           f'stroke-width="{sw * mark_scale * s:.2f}" stroke-linecap="round"/>')
    return "".join(out)


def limb_point(host, q, yaw, u, P):
    """Hidden mark points slide along their ring to the silhouette edge (the side nearer u)."""
    X, H, Z = q
    y = GROUND - (H - host["lift"]) / host["sy"]
    r = max(r_at(host["prof"], y) * host["rscale"], 1e-3)
    rz = r * host["depth"]
    ps = math.radians(yaw)
    th0 = math.atan2(-r * math.cos(ps), rz * math.sin(ps)) if abs(ps) > 1e-6 else math.pi / 2
    best = None
    for th in (th0, th0 + math.pi):
        p = (host["cx"] + r * math.sin(th), H, host["cz"] + rz * math.cos(th))
        uu, vv, _ = P(p)
        if best is None or abs(uu - u) < abs(best[0] - u):
            best = (uu, vv)
    return best


def bounds(parts, yaw=0.0, pitch=0.0):
    P, _ = cam(yaw, pitch)
    xs, ys = [], []
    for p in parts:
        for pc in p.pieces:
            for q in pc:
                x, y, _ = P(q)
                xs.append(x)
                ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def project_front_point(x, y, host_prof=None, yaw=0.0, pitch=0.0, depth=0.92, on_surface=True, lift=0.0):
    """A front-view landmark (x, y) -> screen (u, v) for a view; on the head/jacket surface or on the z=0 slice."""
    P, _ = cam(yaw, pitch)
    X = x - 150
    z = 0.0
    if on_surface and host_prof:
        r = r_at(host_prof, y)
        X = max(-r, min(r, X))
        z = r * depth * math.sqrt(max(1 - (X / max(r, 1e-3)) ** 2, 0.0))
    u, v, _ = P((X, GROUND - y + lift, z))
    return u, v


def text(x, y, t, size=16, weight="normal", fill=INK, anchor="start"):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{t}</text>')


def svg_doc(w, h, inner, bg=None):
    # ImageMagick's MSVG loses group transforms after <text>, <rect> or dashed paths: draw those last.
    texts = re.findall(r"<text[^>]*>[^<]*</text>", inner)
    inner = re.sub(r"<text[^>]*>[^<]*</text>", "", inner)
    late = re.findall(r"<rect[^>]*/>|<path[^>]*stroke-dasharray[^>]*/>", inner)
    inner = re.sub(r"<rect[^>]*/>|<path[^>]*stroke-dasharray[^>]*/>", "", inner)
    inner = inner + "".join(late) + "".join(texts)
    b = f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}" stroke="none"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{b}{inner}</svg>')
