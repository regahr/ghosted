"""ATS-9000 sketch v2 (direction B "Mailbox Bot" + a neck): hand-drawn Bezier profiles -> extruded / turned parts.

Every shape starts as a hand-written cubic Bezier profile (front view x/y, y down, axis x 150, ground y 340; or a side
profile in Z/y). Python extrudes or turns them so the four views, the game camera and the motion panels all agree.
It is a sketch aid for the 3D builder, not the 3D model. Helpers (bez, path_points, cam, hull, text, svg_doc) are
copied from assets/ricky/sketch/src/ricky.py. v1 (direction A) is archived in assets/ats9000/sketch-v1-A/.
"""
import math
import re

GROUND = 340.0
M_PER_U = 0.00373         # overwritten by the camera calibration in build.py (91 px facing the camera); 1 u = 3.73 mm

# ---------------------------------------------------------------- palette (seats/lena-park.md rows; same as v1)
ROW = {
    12: "#FFE8A6",  # cream: eyes, scan line
    13: "#F0B43C",  # gold: antenna ball
    18: "#8E9BA8",  # robot: body, head, neck core, slot lip, hub, stamp block
    21: "#B23A26",  # red-ink: TEXT ONLY, the printed words NOT A FIT on the CV prop
    22: "#2B1E16",  # ink: outline, screen, slot, neck rings (bellows), treads, stamp rubber
    23: "#FFF8EE",  # panel: CV prop paper only
}
INK = ROW[22]
SHADE_K = 0.85
CREAM = "#FDE6C8"   # card background (same as the Ricky / Ghostie sheets)
NOTE = "#1D63C8"    # guides and notes, not a character colour


def shade(hexc, k=SHADE_K):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (round(r * k), round(g * k), round(b * k))


# ---------------------------------------------------------------- body map landmarks (front view units)
LM = {
    "ant_top": 6,         # top of the antenna ball
    "head_top": 60,       # head top = antenna base
    "screen_top": 74,
    "eye": 102,           # eye line (screen)
    "scan_rest": 126,     # scan line rest
    "screen_bot": 136,
    "head_bot": 150,      # chin = neck top
    "neck_bot": 200,      # neck bottom = body top (arch crown)
    "pivot": 224,         # stamp pivot (shoulder hub axis)
    "slot": 247,          # CV slot centre line (the mouth)
    "body_bot": 304,      # body bottom = tread top line
    "axle": 322,          # tread axle line (hub centres)
    "ground": 340,
}
EYE_X = (120, 180)
HEAD_Z = 34               # head depth +-34: a shallow "monitor" head, so the neck shows from pitch 42

# ---------------------------------------------------------------- hand-drawn profiles
# head: a soft monitor box, sides bowed out by 1 unit
HEAD = ("M150,60 L216,60 C230,60 238,70 238,84 C239,104 239,120 236,134 C234,144 227,150 216,150 "
        "L84,150 C73,150 66,144 64,134 C61,120 61,104 62,84 C62,70 70,60 84,60 Z")
SCREEN = ("M92,74 L208,74 C215,74 220,79 220,86 L220,124 C220,131 215,136 208,136 L92,136 "
          "C85,136 80,131 80,124 L80,86 C80,79 85,74 92,74 Z")
HEAD_VENTS = ["M108,92 L192,92", "M108,104 L192,104", "M108,116 L192,116"]   # back of the head
# neck: accordion "rubber bellows", 3 ink rings on a robot-grey core (dark band = reads at 1x) (turned; (y, r) bottom to top)
NECK_CORE = [(206, 17), (146, 17)]
NECK_RINGS = [[(193, 26), (185, 26)], [(178, 26), (170, 26)], [(163, 26), (155, 26)]]
# body: a mailbox arch (a round crown that the neck sits on), straight sides, flat hem
BODY = ("M150,200 C188,200 222,214 223,240 C224,262 225,280 225,294 C225,300 221,304 215,304 "
        "L85,304 C79,304 75,300 75,294 C75,280 76,262 77,240 C78,214 112,200 150,200 Z")
BODY_Z = 50
SLOT = ("M108,240 L192,240 C196,240 198,242 198,246 L198,250 C198,253 196,254 192,254 L108,254 "
        "C104,254 102,253 102,250 L102,246 C102,242 104,240 108,240 Z")
LIP = "M102,254 L198,254 L203,262 L97,262 Z"     # the tray under the slot (front view), Z 44..62
HATCH = ("M114,236 L186,236 C189,236 190,237 190,240 L190,280 C190,283 189,284 186,284 L114,284 "
         "C111,284 110,283 110,280 L110,240 C110,237 111,236 114,236 Z")                # back hatch
# tread: side profile in (Z, y); a stadium, front end longer (tank nose)
TREAD_X = (194, 234)      # the robot's left tread (x); the right tread is mirrored (66-106)
HUBS = [(-40, 322), (8, 322), (56, 322)]

# stamp arm (robot's left = viewer-right in the front view); side profiles in (Z, y), pivot (Z 0, y 224)
HUB_X = (212, 246)        # shoulder hub, a short cylinder on the X axis, r 15
ARM_X = (246, 260)        # the bar
BLOCK_X = (242, 266)      # the stamp block; 8 units clear of the tread (x 234)
ARM_BAR = "M-9,224 C-9,219 9,219 9,224 L9,300 C9,304 -9,304 -9,300 Z"
STAMP_BLOCK = ("M-22,298 L22,298 C25,298 27,300 27,303 L27,326 C27,329 25,330 22,330 L-22,330 "
               "C-25,330 -27,329 -27,326 L-27,303 C-27,300 -25,298 -22,298 Z")
STAMP_RUBBER = "M-25,330 L25,330 L25,338 L-25,338 Z"
REST_DEG, WIND_DEG, SLAM_DEG = 45.0, 140.0, 0.0

# antenna: robot's right top corner (viewer-left); socket, springy stalk, gold ball
ANT_BASE = (80, 62, -16)  # x, y, z
ANT_TIP = (66, 22, -16)
ANT_BALL_R = 10

# ---------------------------------------------------------------- Bezier helpers (ricky.py)
def bez(p0, p1, p2, p3, n=16):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def path_points(d, n=10):
    toks = re.findall(r"[MCLZ]|-?\d+(?:\.\d+)?", d)
    pts, cur, i, cmd = [], None, 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MCLZ":
            cmd = t
            i += 1
            continue
        if cmd == "M":
            cur = (float(t), float(toks[i + 1]))
            pts.append(cur)
            i += 2
            cmd = "L"
        elif cmd == "L":
            cur = (float(t), float(toks[i + 1]))
            pts.append(cur)
            i += 2
        elif cmd == "C":
            p1 = (float(toks[i]), float(toks[i + 1]))
            p2 = (float(toks[i + 2]), float(toks[i + 3]))
            p3 = (float(toks[i + 4]), float(toks[i + 5]))
            pts += bez(cur, p1, p2, p3, n)[1:]
            cur = p3
            i += 6
    # drop the closing duplicate and repeated points
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    if len(out) > 2 and abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    return out


def scale_path(d, sx, sy, cx=150.0, cy=0.0):
    def f(m):
        x, y = float(m.group(1)), float(m.group(2))
        return f"{cx + (x - cx) * sx:.2f},{cy + (y - cy) * sy:.2f}"
    return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", f, d)


def oval(cx, cy, rx, ry):
    k = 0.5523
    return (f"M{cx},{cy - ry} C{cx + k * rx},{cy - ry} {cx + rx},{cy - k * ry} {cx + rx},{cy} "
            f"C{cx + rx},{cy + k * ry} {cx + k * rx},{cy + ry} {cx},{cy + ry} "
            f"C{cx - k * rx},{cy + ry} {cx - rx},{cy + k * ry} {cx - rx},{cy} "
            f"C{cx - rx},{cy - k * ry} {cx - k * rx},{cy - ry} {cx},{cy - ry} Z")


def pill(cx, cy, w, h):
    r = min(w, h) / 2
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    k = 0.5523 * r
    return (f"M{x0 + r},{y0} L{x1 - r},{y0} C{x1 - r + k},{y0} {x1},{y0 + r - k} {x1},{y0 + r} "
            f"L{x1},{y1 - r} C{x1},{y1 - r + k} {x1 - r + k},{y1} {x1 - r},{y1} L{x0 + r},{y1} "
            f"C{x0 + r - k},{y1} {x0},{y1 - r + k} {x0},{y1 - r} L{x0},{y0 + r} C{x0},{y0 + r - k} {x0 + r - k},{y0} {x0 + r},{y0} Z")


# ---------------------------------------------------------------- 3D parts (X right, H up, Z front)
class Face:
    def __init__(self, pts, kind="side", marks=None, seam=None, color=None):
        self.pts, self.kind, self.marks, self.seam, self.color = pts, kind, marks or [], seam or set(), color


class Part:
    def __init__(self, name, color, faces, bias=0.0, ink=True, smooth_caps=False):
        self.name, self.color, self.faces, self.bias, self.ink = name, color, faces, bias, ink
        self.xf = None
        self.smooth_caps = smooth_caps


def to3(plane, u, v, w):
    if plane == "xy":
        return (u - 150.0, GROUND - v, w)
    if plane == "zy":
        return (w - 150.0, GROUND - v, u)
    raise ValueError(plane)


def prism(name, color, d, plane, a, b, marks_a=None, marks_b=None, seam_u=None, n=8, bias=0.0, ink=True):
    """Extrude a convex profile. plane 'xy': profile (x, y) front view, extruded along Z from a to b.
    plane 'zy': profile (Z, y) side view, extruded along x (front-view x units) from a to b.
    marks: list of (kind, path, fill, stroke, width) drawn on cap a (w=a) or cap b (w=b)."""
    prof = path_points(d, n)
    ca = [to3(plane, u, v, a) for u, v in prof]
    cb = [to3(plane, u, v, b) for u, v in prof]
    seam = set()
    if seam_u is not None:
        for k in range(len(prof)):
            p, q = prof[k], prof[(k + 1) % len(prof)]
            if any(abs(p[0] - s) < 1e-6 and abs(q[0] - s) < 1e-6 for s in seam_u):
                seam.add(k)
    faces = [Face(ca, "cap", _marks(plane, marks_a, a - 0.4 * (1 if b > a else -1)), seam),
             Face(cb, "cap", _marks(plane, marks_b, b + 0.4 * (1 if b > a else -1)), seam)]
    for k in range(len(prof)):
        k2 = (k + 1) % len(prof)
        if k in seam:
            faces.append(Face([ca[k], ca[k2], cb[k2], cb[k]], "seam"))
        else:
            faces.append(Face([ca[k], ca[k2], cb[k2], cb[k]], "side"))
    return Part(name, color, faces, bias, ink)


def _marks(plane, marks, w):
    out = []
    for kind, d, fill, stroke, sw in (marks or []):
        pts = [to3(plane, u, v, w) for u, v in path_points(d, 8)]
        out.append((kind, pts, fill, stroke, sw))
    return out


def turned(name, color, rings, cx=0.0, cz=0.0, n=24, top_marks=None, bias=0.0):
    """A body of revolution about a vertical axis at (cx, cz). rings: (y, r) from bottom to top."""
    R = []
    for y, r in rings:
        R.append([(cx + r * math.sin(2 * math.pi * k / n), GROUND - y, cz + r * math.cos(2 * math.pi * k / n))
                  for k in range(n)])
    faces = [Face(R[0][::-1], "cap"), Face(R[-1], "cap", top_marks or [])]
    for r0, r1 in zip(R, R[1:]):
        for k in range(n):
            faces.append(Face([r0[k], r0[(k + 1) % n], r1[(k + 1) % n], r1[k]], "side"))
    return Part(name, color, faces, bias)


def disc(cx, h, cz, r, n=24):
    return [(cx + r * math.sin(2 * math.pi * k / n), h, cz + r * math.cos(2 * math.pi * k / n)) for k in range(n)]


def tube(name, color, p0, p1, r, n=10, bias=0.0):
    d = [p1[i] - p0[i] for i in range(3)]
    ld = math.sqrt(sum(c * c for c in d))
    d = [c / ld for c in d]
    a = (0.0, 0.0, 1.0) if abs(d[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = (d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0])
    lu = math.sqrt(sum(c * c for c in u))
    u = [c / lu for c in u]
    v = (d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0])
    ring = lambda p: [tuple(p[j] + r * (math.cos(2 * math.pi * k / n) * u[j] + math.sin(2 * math.pi * k / n) * v[j])
                            for j in range(3)) for k in range(n)]
    A, B = ring(p0), ring(p1)
    faces = [Face(A[::-1], "cap"), Face(B, "cap")]
    for k in range(n):
        faces.append(Face([A[k], A[(k + 1) % n], B[(k + 1) % n], B[k]], "side"))
    return Part(name, color, faces, bias)


def sphere(name, color, c, r, n=10, bias=0.0):
    faces = []
    for i in range(n):
        t0, t1 = math.pi * i / n, math.pi * (i + 1) / n
        for k in range(2 * n):
            p0, p1 = 2 * math.pi * k / (2 * n), 2 * math.pi * (k + 1) / (2 * n)
            q = lambda t, p: (c[0] + r * math.sin(t) * math.sin(p), c[1] + r * math.cos(t), c[2] + r * math.sin(t) * math.cos(p))
            faces.append(Face([q(t0, p0), q(t1, p0), q(t1, p1), q(t0, p1)], "side"))
    return Part(name, color, faces, bias)


def cyl_x(name, color, cy, cz, r, x0, x1, marks_out=None, bias=0.0):
    """Cylinder on the X axis (front-view x0..x1), centre (y cy, Z cz)."""
    return prism(name, color, oval(cz, cy, r, r), "zy", x0, x1, marks_b=marks_out, bias=bias)


# ---------------------------------------------------------------- transforms
def rot_x(theta_deg, pivot_h, pivot_z):
    """Rotate about the X axis through (H, Z) = pivot; positive swings the lower end FORWARD (+Z)."""
    t = math.radians(theta_deg)
    c, s = math.cos(t), math.sin(t)

    def f(q):
        X, H, Z = q
        h, z = H - pivot_h, Z - pivot_z
        # a point straight below the pivot (h < 0, z = 0) moves to +z for theta > 0
        h2 = h * c + z * s
        z2 = -h * s + z * c
        return (X, pivot_h + h2, pivot_z + z2)
    return f


def translate(dx=0.0, dh=0.0, dz=0.0):
    return lambda q: (q[0] + dx, q[1] + dh, q[2] + dz)


def compose(*fs):
    def f(q):
        for g in fs:
            if g:
                q = g(q)
        return q
    return f


# ---------------------------------------------------------------- the model
EXPR = {
    "idle": "pill eyes",
    "reading": "flat eyes, scan line sweeping",
    "found": "happy arcs: KEYWORD FOUND",
    "notfit": "eyes low and soft: sorry, NOT A FIT",
    "loading": "three dots",
}


def screen_marks(expr="idle", scan=LM["scan_rest"]):
    e = LM["eye"]
    m = [("fill", SCREEN, INK, None, 0)]
    if expr == "idle":
        for x in EYE_X:
            m.append(("fill", pill(x, e, 20, 30), ROW[12], None, 0))
    elif expr == "reading":
        for x in EYE_X:
            m.append(("fill", pill(x, e + 2, 24, 8), ROW[12], None, 0))
    elif expr == "found":
        for x in EYE_X:
            m.append(("line", f"M{x - 13},{e + 7} C{x - 9},{e - 12} {x + 9},{e - 12} {x + 13},{e + 7}", None, ROW[12], 6))
    elif expr == "notfit":
        for x in EYE_X:
            m.append(("fill", f"M{x - 12},{e + 1} C{x - 12},{e + 16} {x + 12},{e + 16} {x + 12},{e + 1} Z", ROW[12], None, 0))
    elif expr == "loading":
        for x in (128, 150, 172):
            m.append(("fill", oval(x, e, 6, 6), ROW[12], None, 0))
    if scan is not None:
        m.append(("line", f"M88,{scan} L212,{scan}", None, ROW[12], 3))
    return m


def model(o=None):
    """Build the ATS-9000 v2. o: options for the motion panels and the screen states."""
    o = dict(o or {})
    expr = o.get("expr", "idle")
    scan = o.get("scan", LM["scan_rest"])
    theta = o.get("theta", REST_DEG)        # stamp arm swing; 0 = straight down, + = forward
    ant_on = o.get("ant_on", True)
    cv = o.get("cv", None)                  # None, "out", "half": a CV sliding into the slot
    spin = o.get("spin", 0.0)               # hub spoke angle (treads roll)
    neck = o.get("neck", True)
    parts = []

    # ---- body (mailbox arch) with the slot (the mouth) and its lip tray
    parts.append(prism("body", ROW[18], BODY, "xy", -BODY_Z, BODY_Z,
                       marks_a=[("line", HATCH, None, INK, 1.8)],
                       marks_b=[("fill", SLOT, INK, None, 0)]))
    parts.append(prism("lip", ROW[18], LIP, "xy", BODY_Z - 6, BODY_Z + 12, bias=0.5))

    # ---- neck: accordion bellows (grey core + 3 ink rings)
    if neck:
        parts.append(turned("neck_core", ROW[18], NECK_CORE, n=16, bias=-0.5))
        for k, rg in enumerate(NECK_RINGS):
            parts.append(turned(f"neck_ring{k}", INK, rg, n=20, bias=5.0 + 0.5 * k))
        # the rings draw in order bottom -> top (a stack)
    else:
        parts.append(prism("neck_block", INK, "M124,148 L176,148 L176,204 L124,204 Z", "xy", -30, 30, bias=-500))

    # ---- head (monitor) with the screen
    parts.append(prism("head", ROW[18], HEAD, "xy", -HEAD_Z, HEAD_Z,
                       marks_a=[("line", v, None, INK, 2.2) for v in HEAD_VENTS],
                       marks_b=screen_marks(expr, scan)))

    # ---- a CV sliding into the slot (prop): a thin sheet, flat, entering along -Z
    if cv:
        L = {"out": 76, "half": 36}[cv]
        sheet = prism("cv", ROW[23], f"M{BODY_Z},245 L{BODY_Z + L},245 L{BODY_Z + L},248 L{BODY_Z},248 Z", "zy",
                      118, 182, bias=3)
        parts.append(sheet)
        for k in range(3):      # ink text lines on the sheet (thin strips on its top)
            z0 = BODY_Z + 10 + 14 * k
            if z0 + 8 < BODY_Z + L:
                parts.append(prism("cvline", INK, f"M{z0},244.2 L{z0 + 6},244.2 L{z0 + 6},245 L{z0},245 Z", "zy",
                                   126, 174 - 12 * (k % 2), bias=3.2, ink=False))

    # ---- treads (ink)
    for s in (-1, 1):
        x0, x1 = TREAD_X if s > 0 else (300 - TREAD_X[1], 300 - TREAD_X[0])
        hubs = []
        for hz, hy in HUBS:
            hubs.append(("fill", oval(hz, hy, 10, 10), ROW[18], INK, 1.6))
            a = math.radians(spin)
            hubs.append(("line", f"M{hz - 7 * math.cos(a):.2f},{hy - 7 * math.sin(a):.2f} "
                                 f"L{hz + 7 * math.cos(a):.2f},{hy + 7 * math.sin(a):.2f}", None, INK, 2.0))
        pieces = [("tread_back", "M-40,304 L-48,304 L-48,340 L-40,340 C-50,340 -58,332 -58,322 C-58,312 -50,304 -40,304 Z", 0.0, {-48}),
                  ("tread_mid", "M-48,304 L50,304 L50,340 L-48,340 Z", -1000.0, {-48, 50}),
                  ("tread_front", "M50,304 L56,304 C66,304 74,312 74,322 C74,332 66,340 56,340 L50,340 Z", 0.0, {50})]
        for nm, d, bias, seam in pieces:
            mk = [(k, d2, f, st, w) for k, d2, f, st, w in hubs if _hub_in(d2, nm)]
            kw = {"marks_b": mk} if s > 0 else {"marks_a": mk}
            parts.append(prism(nm, INK, d, "zy", x0, x1, seam_u=seam, bias=bias, **kw))

    # ---- antenna (robot's right top corner = viewer-left)
    bx, by, bz = ANT_BASE
    tx, ty, tz = ANT_TIP
    p0 = (bx - 150, GROUND - by, bz)
    p1 = (tx - 150, GROUND - ty, tz)
    parts.append(tube("socket", shade(ROW[18]), (p0[0], p0[1] - 4, p0[2]), (p0[0], p0[1] + 6, p0[2]), 7, bias=0.2))
    parts.append(tube("stalk", INK, p0, p1, 2.6, n=8, bias=0.3))
    ball = ROW[13] if ant_on else shade(ROW[13], 0.62)
    parts.append(sphere("ball", ball, (p1[0], p1[1] + ANT_BALL_R * 0.6, p1[2]), ANT_BALL_R, bias=0.4))

    # ---- stamp arm (robot's left = viewer-right)
    ph, pz = GROUND - LM["pivot"], 0.0
    sw = rot_x(theta, ph, pz)
    parts.append(cyl_x("hub", ROW[18], LM["pivot"], 0, 15, *HUB_X,
                       marks_out=[("fill", oval(0, LM["pivot"], 5, 5), INK, None, 0)]))
    bar = prism("bar", ROW[18], ARM_BAR, "zy", *ARM_X, bias=0.1)
    blk = prism("block", ROW[18], STAMP_BLOCK, "zy", *BLOCK_X, bias=0.2)
    rub = prism("rubber", INK, STAMP_RUBBER, "zy", BLOCK_X[0] + 1, BLOCK_X[1] - 1, bias=0.15)
    for p in (bar, blk, rub):
        p.xf = sw
        p.after = "hub"
        parts.append(p)
    blk.after = "bar"
    return parts


def _hub_in(d, nm):
    m = re.match(r"M(-?\d+(?:\.\d+)?),", d)
    z = float(m.group(1))
    if nm == "tread_back":
        return z < -30
    if nm == "tread_front":
        return z > 40
    return -30 <= z <= 40


# ---------------------------------------------------------------- projection and drawing (ricky.py cam)
LIGHT = (0.45, 0.55, 0.70)   # camera space: from the viewer's upper right (ricky.py)
LIT_T = 0.6                  # 2-band toon: faces under this get the grey multiplier (box sides read apart)


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
    return P


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


def poly(pts, s=1.0, ox=0.0, oy=0.0, close=True):
    return "M" + " L".join(f"{x * s + ox:.2f},{y * s + oy:.2f}" for x, y in pts) + (" Z" if close else "")


def _newell(pts):
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        nx += (a[1] - b[1]) * (a[2] + b[2])
        ny += (a[2] - b[2]) * (a[0] + b[0])
        nz += (a[0] - b[0]) * (a[1] + b[1])
    ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return nx / ln, ny / ln, nz / ln


def _view(yaw, pitch):
    """World vector pointing from the object toward the camera."""
    ps, pp = math.radians(yaw), math.radians(pitch)
    # inverse of cam(): tow axis = (sin ps cos pp, sin pp, cos ps cos pp)
    return (math.sin(ps) * math.cos(pp), math.sin(pp), math.cos(ps) * math.cos(pp))


def _cam_dir(n, yaw, pitch):
    ps, pp = math.radians(yaw), math.radians(pitch)
    X, H, Z = n
    x1 = X * math.cos(ps) - Z * math.sin(ps)
    z1 = X * math.sin(ps) + Z * math.cos(ps)
    up = H * math.cos(pp) - z1 * math.sin(pp)
    tow = z1 * math.cos(pp) + H * math.sin(pp)
    return x1, up, tow


def render(parts, yaw=0.0, pitch=0.0, s=1.0, ox=0.0, oy=0.0, ink_w=4.0, mono=None, xf=None, crease=True,
           mark_scale=1.0):
    """SVG of the model. s: px per unit; (ox, oy): screen position of (X=0, H=0)."""
    P = cam(yaw, pitch)
    order = []
    for p in parts:
        f = compose(p.xf, xf)
        faces = [[f(q) for q in fc.pts] for fc in p.faces]
        allp = [q for fc in faces for q in fc]
        cen = tuple(sum(q[j] for q in allp) / len(allp) for j in range(3))
        dep = P(cen)[2]
        order.append([dep + p.bias * 3, p, faces, cen, f])
    by = {t[1].name: t[0] for t in order}
    for t in order:
        a = getattr(t[1], "after", None)
        if a and a in by and t[0] < by[a]:
            t[0] = by[a] + 0.01
    order.sort(key=lambda t: t[0])
    out = []
    for _, p, faces, cen, f in order:
        vis = []
        for fc, pts in zip(p.faces, faces):
            n = _newell(pts)
            fcen = tuple(sum(q[j] for q in pts) / len(pts) for j in range(3))
            if sum((fcen[j] - cen[j]) * n[j] for j in range(3)) < 0:
                n = tuple(-c for c in n)
            cd = _cam_dir(n, yaw, pitch)
            if cd[2] > 1e-4:
                vis.append((fc, pts, cd))
        if not vis:
            continue
        sp_all = [P(q)[:2] for _, pts, _ in vis for q in pts]
        h = hull(sp_all)
        col = mono or p.color
        if p.ink and len(h) >= 3:
            out.append(f'<path d="{poly(h, s, ox, oy)}" fill="{mono or INK}" stroke="{mono or INK}" '
                       f'stroke-width="{ink_w * 2:.2f}" stroke-linejoin="round"/>')
        if mono:
            out.append(f'<path d="{poly(h, s, ox, oy)}" fill="{mono}" stroke="none"/>')
            continue
        vis.sort(key=lambda t: sum(P(q)[2] for q in t[1]) / len(t[1]))
        for fc, pts, cd in vis:
            lit = sum(a * b for a, b in zip(cd, LIGHT)) > LIT_T
            c = col if lit else shade(col)
            sp = [P(q)[:2] for q in pts]
            out.append(f'<path d="{poly(sp, s, ox, oy)}" fill="{c}" stroke="{c}" stroke-width="0.9" '
                       f'stroke-linejoin="round"/>')
        if crease:
            for fc, pts, cd in vis:
                if fc.kind != "cap" or p.smooth_caps:
                    continue
                sp = [P(q)[:2] for q in pts]
                k = len(sp)
                segs, run = [], []
                for i in range(k):
                    if i in fc.seam:
                        if run:
                            segs.append(run)
                        run = []
                        continue
                    if not run:
                        run = [sp[i]]
                    run.append(sp[(i + 1) % k])
                if run:
                    segs.append(run)
                if not fc.seam and segs:
                    out.append(f'<path d="{poly(sp, s, ox, oy)}" fill="none" stroke="{INK}" '
                               f'stroke-width="{ink_w * 0.55:.2f}" stroke-linejoin="round"/>')
                else:
                    for r_ in segs:
                        out.append(f'<path d="{poly(r_, s, ox, oy, False)}" fill="none" stroke="{INK}" '
                                   f'stroke-width="{ink_w * 0.55:.2f}" stroke-linejoin="round"/>')
        for fc, pts, cd in vis:
            for kind, mp, fill, stroke, sw in fc.marks:
                sp = [P(f(q))[:2] for q in mp]
                if kind == "fill":
                    st = (f' stroke="{stroke}" stroke-width="{sw * mark_scale * s:.2f}" stroke-linejoin="round"'
                          if stroke else ' stroke="none"')
                    out.append(f'<path d="{poly(sp, s, ox, oy)}" fill="{fill}"{st}/>')
                else:
                    out.append(f'<path d="{poly(sp, s, ox, oy, False)}" fill="none" stroke="{stroke}" '
                               f'stroke-width="{max(sw * mark_scale * s, 0.6):.2f}" stroke-linecap="round" '
                               f'stroke-linejoin="round"/>')
    return "".join(out)


def bounds(parts, yaw=0.0, pitch=0.0):
    P = cam(yaw, pitch)
    xs, ys = [], []
    for p in parts:
        f = compose(p.xf)
        for fc in p.faces:
            for q in fc.pts:
                x, y, _ = P(f(q))
                xs.append(x)
                ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def project(q, yaw=0.0, pitch=0.0):
    return cam(yaw, pitch)(q)[:2]


def front_pt(x, y, z=0.0):
    return (x - 150.0, GROUND - y, z)


def text(x, y, t, size=16, weight="normal", fill=INK, anchor="start"):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{t}</text>')


def svg_doc(w, h, inner, bg=None):
    # ImageMagick's MSVG loses group transforms after <text>, <rect> or dashed paths: draw those last (ricky.py).
    texts = re.findall(r"<text[^>]*>[^<]*</text>", inner)
    inner = re.sub(r"<text[^>]*>[^<]*</text>", "", inner)
    late = re.findall(r"<rect[^>]*/>|<path[^>]*stroke-dasharray[^>]*/>", inner)
    inner = re.sub(r"<rect[^>]*/>|<path[^>]*stroke-dasharray[^>]*/>", "", inner)
    inner = inner + "".join(late) + "".join(texts)
    b = f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}" stroke="none"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{b}{inner}</svg>')
