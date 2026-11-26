"""Build explore.png, body-map.png, gary-sheet.png and silhouette-64.png for Gary the pigeon postman.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
Reads only the locked cast renders (kit, ricky/v1, ghostie/v7, ats9000/v1, auntie-dot/v1, brett/v1, juno/v1, panel/v1),
the real Panel v1 lineup renders panel/v1/lineup-grass.png and lineup-path.png (the whole family), and the Kit cut-out
panel/sketch/src/_tmp/kit-cut.png (cut from the Juno v1 path render by the Panel sketch).
Writes only into ../, ./_tmp.
Code reused: Juno and Panel sketch build.py helpers (grey formula, ratio, camera calibration, perspective at a spot,
tiles, lineup, silhouette), the Ricky library and the Dot render.
"""
import json
import math
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ASSETS = os.path.abspath(os.path.join(OUT, "..", ".."))
sys.path.insert(0, HERE)
from gary import *  # noqa
from ricky import lift_mark  # noqa

TMP = os.path.join(HERE, "_tmp")
os.makedirs(TMP, exist_ok=True)

REFS = [("Kit v5", "kit/turn-front.png"), ("Ricky v1", "ricky/v1/turn-front.png"),
        ("Ghostie v7", "ghostie/v7/turn-front.png"), ("ATS-9000 v1", "ats9000/v1/turn-front.png"),
        ("Auntie Dot v1", "auntie-dot/v1/turn-front.png"), ("Brett v1", "brett/v1/hero.png"),
        ("Juno v1", "juno/v1/hero.png"), ("Panel v1", "panel/v1/turn-front.png")]
LU = {"grass": os.path.join(ASSETS, "panel", "v1", "lineup-grass.png"),
      "path": os.path.join(ASSETS, "panel", "v1", "lineup-path.png")}
CROP = {"grass": (600, 300, 1000, 560), "path": (430, 320, 1030, 580)}
SPOT = {"grass": (846, 502), "path": (712, 545)}          # Gary's feet, full frame (free ground)
FLY = {"grass": (690, 488), "path": (930, 590)}           # a flying Gary: ground point under him
KIT_SRC = os.path.join(ASSETS, "panel", "sketch", "src", "_tmp", "kit-cut.png")
KIT_PNG = os.path.join(TMP, "kit-cut.png")
KIT_FEET = (31, 84)
KIT_FEET_Y = 498
DOT_SPOT_Y = 661

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # 74.97 px per m (kit/ingame.html L156)
OUTLINE = 1.6
CAM = (5.0, 42.0)                                         # net yaw 5 (lineup-facing), pitch 42
CAM_FREE = (20.0, 42.0)                                   # facing the world axis (yaw 20)
KIT_M = 0.977
TARGET_M = 0.5 * KIT_M                                    # brief: 0.5 x Kit standing, cap included
GREEN, PATHC = "#B5D67A", "#EBD3A6"
RED, MAG = "#E0533D", "#C2185B"

_b = pbounds(gary(), 0, 0)
HU = _b[3] - _b[1]
M_PER_U = TARGET_M / HU
GS = PX_PER_M * M_PER_U
_w = pbounds(gary({"wings": "spread", "flap": 0}), 0, 0)
SPAN_M = (_w[2] - _w[0]) * M_PER_U
FLY_LIFT = 0.9 / M_PER_U                                  # 0.9 m up while flying in the lineups


def sh(*a):
    subprocess.run(["magick", *a], check=True)


def write(name, w, h, inner, bg=None):
    p = os.path.join(HERE, name)
    open(p, "w").write(svg_doc(w, h, inner, bg))
    return p


def comp(base, over, x, y):
    sh(base, over, "-geometry", f"+{int(x)}+{int(y)}", "-composite", base)


def guide(x0, x1, y, op=0.55, w=1.5):
    return (f'<path d="M{x0},{y:.1f} L{x1},{y:.1f}" fill="none" stroke="{NOTE}" stroke-width="{w}" '
            f'stroke-opacity="{op}"/>')


def dot(x, y, r=5, c=NOTE):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r}" ry="{r}" fill="{c}" stroke="#FFFFFF" stroke-width="1.5"/>'


def frame(x0, y0, x1, y1, c=NOTE, w=3):
    return f'<path d="M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z" fill="none" stroke="{c}" stroke-width="{w}"/>'


def shadow(cx, cy, rx, ry, o=0.16):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#2B1E16" fill-opacity="{o}" stroke="none"/>'


def grey_img(src, dst):
    """Same luminance formula as ghostie/v7/make_sheets.py (Lena's gate)."""
    im = Image.open(src).convert("RGBA")
    p = np.asarray(im.convert("RGB")).astype(float) / 255
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    g = (s * 255).round().astype(np.uint8)
    Image.fromarray(np.dstack([g, g, g, np.asarray(im)[..., 3]]), "RGBA").save(dst)


def lum(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def persp(feet_y):
    return 1 + (72 / 68 - 1) * (feet_y - KIT_FEET_Y) / (DOT_SPOT_Y - KIT_FEET_Y)


def alpha_bbox(png):
    a = np.asarray(Image.open(png).convert("RGBA"))[..., 3]
    ys, xs = np.nonzero(a > 40)
    return xs.min(), ys.min(), xs.max(), ys.max()


def kit_on(base, x_feet, y_feet):
    if not os.path.exists(KIT_PNG):
        shutil.copy(KIT_SRC, KIT_PNG)
    shp = os.path.join(TMP, "kit-shadow.png")
    if not os.path.exists(shp):
        sv = write("kit-shadow.svg", 40, 16, shadow(20, 8, 17, 6, 0.28))
        sh("-background", "none", sv, shp)
    comp(base, shp, x_feet - 20, y_feet - 8)
    comp(base, KIT_PNG, x_feet - KIT_FEET[0], y_feet - KIT_FEET[1])


# ============================================================ game camera
def cam_png(name, o=None, w=90, h=100, bg=None, yaw=CAM[0], gs=None, kit=False, mark=None, feet=None):
    """Gary at the game camera, 1x; ground point under him at `feet` (default (w*0.6, h-14)). kit: Kit at the left."""
    gs = gs or GS
    m = gary(o)
    ox, oy = feet or ((w * 0.68 if kit else w / 2), h - 14)
    lift = (o or {}).get("lift", 0.0)
    inner = shadow(ox, oy + 1, 15 * gs / GS * (0.7 if lift > 60 else 1), 5 * gs / GS, 0.24) if bg else ""
    inner += render(m, yaw, CAM[1], gs, ox, oy, OUTLINE)
    if mark:
        inner += mark(ox, oy)
    sv = write(f"{name}.svg", w, h, inner, bg)
    one = os.path.join(TMP, f"{name}-1x.png")
    if bg:
        sh(sv, one)
    else:
        sh("-background", "none", sv, one)
    if kit:
        kit_on(one, w * 0.24, h - 14)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def measure_px(o=None):
    one, _ = cam_png("measure", o, 200, 200)
    x0, y0, x1, y1 = alpha_bbox(one)
    return y1 - y0 + 1, x1 - x0 + 1


def lineup(name, ground, grey=False):
    """The real Panel v1 lineup render (the whole family, Kit at the centre) with Gary on a free spot, and a second
    Gary flying (0.9 m up, wings spread, envelope in the beak) over his ground shadow."""
    box = CROP[ground]
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(LU[ground]).crop(box).save(base)
    for tag, spot, o in (("stand", SPOT[ground], {}),
                         ("fly", FLY[ground], {"wings": "spread", "flap": 30, "env": "beak", "legs": "tuck",
                                               "pitch": 10, "lift": FLY_LIFT})):
        k = persp(spot[1])
        w, h = 160, 170
        sv = write(f"{name}-{tag}-sh.svg", w, h, shadow(w / 2, h - 14, 15 * k, 5 * k, 0.28 if tag == "stand" else 0.18))
        shp = os.path.join(TMP, f"{name}-{tag}-sh.png")
        sh("-background", "none", sv, shp)
        one, _ = cam_png(f"{name}-{tag}", o, w, h, None, gs=GS * k)
        x = spot[0] - box[0] - w / 2
        y = spot[1] - box[1] - (h - 14)
        comp(base, shp, x, y)
        comp(base, one, x, y)
    out1 = os.path.join(TMP, f"{name}-1x.png")
    sh(base, out1)
    if grey:
        grey_img(out1, out1)
    out2 = os.path.join(TMP, f"{name}-x2.png")
    sh(out1, "-filter", "point", "-resize", "200%", out2)
    return out1, out2


# ============================================================ EXPLORE
THUMBS = [
    ("1 egg, kepi, front bag", {}),
    ("2 BMGD literal: sphere, box wings", {"body": "sphere", "wings": "box", "cap": "none", "bag": "none"}),
    ("3 sphere, kepi, front bag", {"body": "sphere"}),
    ("4 upright pear, wide cap, side bag", {"body": "pear", "cap": "peak", "bag": "side"}),
    ("5 small head, grey wings, ink cap", {"head_k": 0.82, "colors": {"wing": ROW[18], "tail": ROW[18],
                                                                     "head": ROW[18], "cap": ROW[22], "bag": ROW[24],
                                                                     "strap": ROW[24]}}),
    ("6 big head (toy), kepi", {"head_k": 1.15}),
    ("7 wide cap ink, light bag", {"cap": "peak", "colors": {"cap": ROW[22], "bag": ROW[24], "strap": ROW[24]}}),
    ("8 no cap: bag + letter only", {"cap": "none", "env": "beak"}),
    ("9 visor only, grey wings", {"cap": "visor", "colors": {"wing": ROW[18], "tail": ROW[18]}}),
    ("10 sphere, box wings + post kit", {"body": "sphere", "wings": "box"}),
]
DIRS = [
    ("A. ROUND POSTIE (pick)", {},
     ["A tilted egg body (chest up, tail down), a round", "toy head, a gold beak, navy kepi set back on the",
      "crown, a wood satchel on the belly. Darker blue", "wings and tail carry the value on grass and path;",
      "the cap and bag say 'post'. The wing tip has 3", "finger feathers, so it can hold a letter like a hand."]),
    ("B. PIGEON-TRUE", {"head_k": 0.82, "colors": {"wing": ROW[18], "tail": ROW[18], "head": ROW[18],
                                                   "cap": ROW[22], "bag": ROW[24], "strap": ROW[24]}},
     ["Small grey head, grey wings, ink cap, a light", "panel-edge bag. More real pigeon, but grey 18 is", "the ATS robot row, the small head loses the eyes",
      "at the game camera, and the light bag sinks into", "the path."]),
    ("C. BMGD LITERAL + POST", {"body": "sphere", "wings": "box"},
     ["A sphere with a cone beak and 2 box wings, plus", "the kepi and bag. Cheap to build, but the box",
      "wings read as a backpack or arms, not wings, and", "a ball with no tail is a chick, not a pigeon."]),
]


def explore():
    W, H = 2700, 1720
    i = [text(30, 50, "GHOSTED: Gary the pigeon postman, explore (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: local references, 10 rough thumbnails, 3 directions, one pick. Designed "
              "curves lifted to round bodies (Ricky / Juno sketch library); palette rows only.", 18)]
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, the locked family; no web)", 20, "bold", NOTE))
    for k, (lab, _) in enumerate(REFS):
        i.append(text(30 + k * 150, ry + 300, lab, 14))
    i.append(text(1260, ry + 300, "Panel v1 lineup at the game camera (x1.5): the family on grass, Kit centre", 15))
    ty = 470
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x3, 26 m, pitch 42, "
                  "net yaw 5), 0.5 x Kit, with Kit.", 20, "bold", NOTE))
    tw = 264
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 6, ty + 34, lab, 13, "bold"))
        i.append(shadow(x + tw / 2, ty + 262, 56, 6))
        i.append(render(gary(o), 0, 0, 0.95, x + tw / 2, ty + 260, 2.2, mark_scale=0.8))
    dy = 1000
    i.append(text(30, dy, "DIRECTIONS (3), developed: front, 3/4, side; then the game camera (x3) next to Kit (real "
                  "render)", 20, "bold", NOTE))
    dw = 880
    for n, (lab, o, notes) in enumerate(DIRS):
        x = 30 + n * dw
        i.append(text(x + 10, dy + 40, lab, 20, "bold", NOTE if n == 0 else INK))
        for k, yw in enumerate((0, 35, 90)):
            i.append(shadow(x + 70 + k * 115, dy + 322, 48, 6))
            i.append(render(gary(o), yw, 0, 0.8, x + 70 + k * 115, dy + 320, 2.2, mark_scale=0.8))
        for k, ln in enumerate(notes):
            i.append(text(x + 10, dy + 390 + k * 22, ln, 16))
        if n == 0:
            i.append(frame(x, dy + 12, x + dw - 20, dy + 540, NOTE, 4))
    i.append(text(30, dy + 610, "PICK: A. It is the only one that reads 'bird plus post' at 37 px: the gold beak points "
                  "down-forward under two clear eyes, the navy cap is a dark top no one else has, the blue wings", 17))
    i.append(text(30, dy + 634, "and tail give the dark value that light blue-grey 8 lacks on grass (1.1:1), and the "
                  "satchel + strap is the postman read. Round, soft and a little clumsy: the kindest courier.", 17))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    for k, (lab, src) in enumerate(REFS):
        t = os.path.join(TMP, f"ref-{k}.png")
        sh(os.path.join(ASSETS, src), "-resize", "140x260", t)
        comp(png, t, 30 + k * 150, ry + 25)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(LU["grass"], "-crop", "560x220+260+220", "+repage", "-filter", "point", "-resize", "150%", lu)
    sh(lu, "-resize", "x270", lu)
    comp(png, lu, 1260, ry + 10)
    for n, (lab, o) in enumerate(THUMBS):
        _, x3 = cam_png(f"ex-thumb-{n}", o, 80, 100, GREEN, kit=True)
        comp(png, x3, 30 + n * tw + 12, ty + 290)
    for n, (lab, o, notes) in enumerate(DIRS):
        _, x3 = cam_png(f"ex-dir-{n}", o, 80, 100, GREEN, kit=True)
        _, p3 = cam_png(f"ex-dirp-{n}", o, 80, 100, PATHC, kit=True)
        comp(png, x3, 30 + n * dw + 380, dy + 55)
        comp(png, p3, 30 + n * dw + 380 + 245, dy + 55)
    return png


# ============================================================ BODY MAP
def head_pt(x, y, out=0.0, o=None):
    """A front-frame point on the head surface (rest pose) -> world."""
    prof = profile(HEAD_HALF)
    X = x - 150
    r = r_at(prof, y)
    X = max(-r, min(r, X))
    z = r * 0.95 * math.sqrt(max(1 - (X / max(r, 1e-3)) ** 2, 0)) + HEAD_C[2] + out
    return (X, GROUND - y, z)


def attach_pts():
    """Landmarks (blue) and attachment points (magenta), world (X, H, Z), from the numbers in gary.model()."""
    hz = HEAD_C[2] + HEAD_R * 0.95
    bp = body_surface(nrm((0.42, -0.42, 0.80)), 9)
    _, tip_hold, _ = wing(-1, "hold", ROW[9])
    _, tip_fold, _ = wing(-1, "fold", ROW[9])
    return {
        "eye_l": (head_pt(EYE_X[0], EYE_Y), NOTE), "eye_r": (head_pt(EYE_X[1], EYE_Y), NOTE),
        "ear_l": ((-EAR_X, LM["eye"], HEAD_C[2] - 6), NOTE), "ear_r": ((EAR_X, LM["eye"], HEAD_C[2] - 6), NOTE),
        "beak_root": ((0, 150, hz - 2), NOTE), "neck": ((0, LM["neck"], 40), NOTE),
        "chest": (body_surface(nrm((0, 0.35, 1))), NOTE),
        "wing_root_l": ((-47, 108, -8), NOTE), "wing_root_r": ((47, 108, -8), NOTE),
        "feet": ((0, 4, 17), NOTE), "tail": ((0, 50, -82), NOTE),
        "cap": ((0, 200, HEAD_C[2]), MAG), "badge": ((0, 199, HEAD_C[2] + 29), MAG),
        "bag": (bp, MAG), "env_beak": ((0, 128, hz + 30), MAG), "env_wing": (tip_hold, MAG),
    }


def cam_marks(yaw=CAM[0]):
    P, _ = cam(yaw, CAM[1])
    return {k: (P(q)[0] * GS, P(q)[1] * GS, c) for k, (q, c) in attach_pts().items()}


def face_check(o=None):
    """At the game camera (net yaw 5), px at 1x: the gap from the lowest cap or brim pixel to the eye top (centre
    column of each eye), the eye size, and the beak size and its gap below the eyes."""
    o = dict(o or {})
    P0, _ = cam(*CAM)
    m = gary(o)
    by = {p.name: p for p in m}

    def screen(p, q):
        f = getattr(p, "pxf", None)
        u, v, _ = P0(f(q) if f else q)
        return u * GS, v * GS

    head = by["head"]
    res = {}
    for k, ex in (("left", EYE_X[0]), ("right", EYE_X[1])):
        eye_top = screen(head, head_pt(ex, EYE_Y - 8.5))
        eye_bot = screen(head, head_pt(ex, EYE_Y + 8.5))
        low = -1e9
        for nm in ("cap", "brim", "badge"):
            p = by.get(nm)
            if not p:
                continue
            for pc in p.pieces:
                for q in pc:
                    u, v = screen(p, q)
                    if abs(u - eye_top[0]) < 2.5:
                        low = max(low, v)
        res[k] = {"cap_above_eye_top_px": round(eye_top[1] - low, 2), "eye_h_px": round(eye_bot[1] - eye_top[1], 2)}
    bk = by["beak"]
    vs = [screen(bk, q) for pc in bk.pieces for q in pc]
    res["beak"] = {"w_px": round(max(u for u, v in vs) - min(u for u, v in vs), 1),
                   "h_px": round(max(v for u, v in vs) - min(v for u, v in vs), 1)}
    return res


def body_map():
    W, H = 2600, 2050
    i = [text(30, 50, "GHOSTED: Gary the pigeon postman, body map v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions, landmarks, wing joints, attachment points (cap, brim, "
              "badge, bag, strap, envelope sockets), and a check at the game camera (26 m, pitch 42).", 18)]
    s = 2.6
    fx, g = 380, 760
    gy = lambda Hh: g - Hh * s
    rows = [("cap top", LM["cap_top"]), ("head top", LM["head_top"]), ("cap band (front edge)", LM["cap_band"]),
            ("eye line = ear points", LM["eye"]), ("beak root", LM["beak"]), ("chin / neck", LM["chin"]),
            ("wing root (shoulder)", LM["wing_root"]), ("belly (bag centre)", LM["belly"]), ("knee", LM["knee"]),
            ("sole", LM["sole"])]
    i.append(text(30, 125, "A. FRONT (upright, symmetric)", 20, "bold", NOTE))
    for lab, Hh in rows:
        i.append(guide(fx - 160, fx + 1100, gy(Hh), 0.35))
        i.append(text(fx + 1110, gy(Hh) + 5, f"{lab}  H {Hh}", 15, "bold" if "eye" in lab else "normal", NOTE))
    i.append(shadow(fx, g + 4, 100, 12))
    i.append(render(gary(), 0, 0, s, fx, g, 5))
    P, _ = cam(0, 0)
    for k, (q, c) in attach_pts().items():
        if k in ("tail", "env_wing", "env_beak"):
            continue
        u, v, _ = P(q)
        i.append(dot(fx + u * s, g + v * s, 7, c))
    # side
    sx = 900
    i.append(text(sx - 120, 125, "B. SIDE (facing left) and BACK", 20, "bold", NOTE))
    i.append(shadow(sx, g + 4, 110, 12))
    i.append(render(gary(), 90, 0, s, sx, g, 5))
    P9, _ = cam(90, 0)
    for k in ("wing_root_r", "tail", "bag", "cap", "beak_root", "feet"):
        q, c = attach_pts()[k]
        u, v, _ = P9(q)
        i.append(dot(sx + u * s, g + v * s, 7, c))
    i.append(shadow(sx + 400, g + 4, 90, 10))
    i.append(render(gary(), 180, 0, s * 0.8, sx + 400, g, 4))
    # head-heights bar
    rx_ = 60
    hh = LM["cap_top"] - LM["chin"]
    i.append(f'<path d="M{rx_},{gy(LM["cap_top"])} L{rx_},{gy(0)}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    for t in (LM["cap_top"], LM["chin"], 0):
        i.append(f'<path d="M{rx_ - 10},{gy(t)} L{rx_ + 10},{gy(t)}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    i.append(text(rx_ + 14, gy(LM["chin"] + hh / 2), "1 head", 15, "bold", NOTE))
    i.append(text(rx_ + 14, gy(6), f"{LM['cap_top'] / hh:.2f}", 15, "bold", NOTE))

    # C. wing joints and holds
    cy0 = 880
    i.append(text(30, cy0, "C. WINGS: 2 rigid segments each (arm 70 u, hand 100 u + 3 finger feathers); hinges at "
                  "the wing root and the wrist (red)", 20, "bold", NOTE))
    i.append(text(30, cy0 + 24, "fold (rest), spread (flight: span 2 x (44 + 70 + 100) = 428 u), hold (his right wing "
                  "reaches forward, the fingers hold the envelope in front of the chest)", 16))
    wj = [({}, 90, "fold (side)"), ({"wings": "spread", "flap": 0, "legs": "tuck"}, 0, "spread (front)"),
          ({"wings": "hold", "env": "wing"}, 35, "hold (3/4)"), ({"env": "beak"}, 35, "envelope in the beak (3/4)")]
    xs = [200, 700, 1300, 1800]
    sc = [1.6, 1.0, 1.6, 1.6]
    for (o, yw, lab), x, s2 in zip(wj, xs, sc):
        i.append(shadow(x, cy0 + 380, 70, 8))
        i.append(render(gary(o), yw, 0, s2, x, cy0 + 378, 3.5))
        i.append(text(x - 90, cy0 + 420, lab, 16, "bold"))
    Pf, _ = cam(0, 0)
    for q in [(-44, 106, 2), (-114, 106 - 0, 2 - 8.4)]:
        u, v, _ = Pf(q)
        i.append(dot(700 + u * 1.0, cy0 + 378 + v * 1.0, 6, RED))
    # D. notes
    nx = 1700
    notes = [(f"PROPORTIONS (head = cap top to chin = {hh} u)", True),
             (f"Standing {LM['cap_top']} u = {LM['cap_top'] / hh:.2f} heads, cap included.", False),
             (f"0.5 x Kit = {TARGET_M:.3f} m: 1 u = {M_PER_U * 1000:.2f} mm.", False),
             (f"Wingspan in flight {SPAN_M:.2f} m = {SPAN_M / KIT_M:.2f} x Kit.", False),
             ("Head: a ball, 76 u, centre H 160, 14 u forward.", False),
             ("Body: an egg 116 x 108 x 148 u, tilted 22 deg (chest", False),
             ("  up, tail end down). Tail: a flat fan at the back, low.", False),
             ("", False),
             ("LANDMARKS (blue)", True),
             ("Eyes on the eye line H 164, x 135 / 165: ink ovals + glint.", False),
             ("Ear points: the eye line at the head sides (x +-37),", False),
             ("  under the feathers: the cap band clears them.", False),
             ("Beak root H 150 on the face front; the cone points", False),
             ("  forward and 15 deg down. NO MOUTH: the beak is the", False),
             ("  only thing below the eyes.", False),
             ("Neck: the head sits on the body, no visible neck line.", False),
             ("Wing roots (shoulders) H 106-108, at the body sides.", False),
             ("Feet: gold, under the belly front, H 0-32.", False),
             ("", False),
             ("ATTACHMENT POINTS (magenta)", True),
             ("Cap: centred on the crown, set back and tilted back", False),
             ("  14 deg; band bottom 10 u under the head top. Brim", False),
             ("  at the front, ink. Badge: cream, cap front.", False),
             ("Bag: on his LEFT belly front, turned 24 deg out.", False),
             ("  Strap: one loop over his RIGHT shoulder, across", False),
             ("  the chest to the bag, round the back (real sash).", False),
             ("Envelope sockets: (1) the beak tip, the letter hangs", False),
             ("  below it; (2) the right wing's finger feathers.", False),
             ("  Swap parts, never both at once.", False)]
    for k, (ln, b) in enumerate(notes):
        i.append(text(nx, 150 + k * 24, ln, 17, "bold" if b else "normal", NOTE if b else INK))

    # E. game camera
    E = (30, 1370)
    i.append(text(E[0], E[1], "E. GAME CAMERA CHECK (x3; 1x at right). Gary next to Kit (real render); then the "
                  "landmark dots (blue) and attachment points (magenta) at net yaw 5, pitch 42.", 18, "bold", NOTE))
    fc = face_check()
    hpx, wpx = measure_px()
    fl = measure_px({"wings": "spread", "flap": 0, "legs": "tuck"})
    lines = [f"Eyes vs cap at 1x: the lowest cap or brim pixel is {fc['left']['cap_above_eye_top_px']:.1f} px "
             f"(left) / {fc['right']['cap_above_eye_top_px']:.1f} px (right) ABOVE the eye top. Each eye is "
             f"{fc['left']['eye_h_px']:.1f} px tall. Nothing covers the eyes.",
             f"Beak at 1x: {fc['beak']['w_px']:.1f} x {fc['beak']['h_px']:.1f} px, gold, a down-pointing wedge under "
             f"the eyes: it reads as a beak, not a mouth.",
             f"Height {hpx} x {wpx} px standing (Kit 75 px). Flight, wings level: {fl[1]} px wide "
             f"(Kit 75 px tall).",
             "Read: navy cap with a light badge, two eyes, gold beak, a light blue-grey ball body, blue wings at the",
             "sides, a brown satchel on the belly, gold feet."]
    for k, ln in enumerate(lines):
        i.append(text(E[0], E[1] + 380 + k * 24, ln, 16, "bold" if k == 3 else "normal"))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)
    hm = cam_marks()

    def mk(ox, oy):
        return "".join(f'<ellipse cx="{ox + u:.2f}" cy="{oy + v:.2f}" rx="0.8" ry="0.8" fill="{c}" stroke="none"/>'
                       for k, (u, v, c) in hm.items() if k not in ("tail", "env_wing", "env_beak", "feet"))
    one, x3 = cam_png("bm-cam", None, 100, 100, GREEN, kit=True)
    _, x3m = cam_png("bm-cam-mark", None, 100, 100, GREEN, mark=mk)
    p1, p3 = cam_png("bm-cam-p", None, 100, 100, PATHC, kit=True)
    comp(png, x3, E[0], E[1] + 40)
    comp(png, x3m, E[0] + 320, E[1] + 40)
    comp(png, p3, E[0] + 640, E[1] + 40)
    comp(png, one, E[0] + 960, E[1] + 40)
    comp(png, p1, E[0] + 1070, E[1] + 40)
    fcx = os.path.join(TMP, "bm-face-x6.png")
    sh(one, "-crop", "30x30+47+42", "+repage", "-filter", "point", "-resize", "800%", fcx)
    comp(png, fcx, E[0] + 1200, E[1] + 40)
    lab = write("bm-facelab.svg", 600, 30, text(0, 20, "head at 1x, x8 (nearest): cap clear of the eyes, beak", 15,
                                                "bold", NOTE))
    labp = os.path.join(TMP, "bm-facelab.png")
    sh("-background", "none", lab, labp)
    comp(png, labp, E[0] + 1200, E[1] + 290)
    info = {k: (round(u, 1), round(v, 1)) for k, (u, v, c) in hm.items()}
    json.dump({"gamecam_marks_px_from_feet": info, "face_check_px": fc, "m_per_u": M_PER_U, "span_m": SPAN_M,
               "px": int(hpx), "px_w": int(wpx), "flight_px_w": int(fl[1])},
              open(os.path.join(TMP, "bodymap.json"), "w"), indent=1)
    return png, info, fc


# ============================================================ SHEET
PAL = [(8, "body, head, neck: light blue-grey"), (9, "wings, tail: the darker value"),
       (26, "cap: navy"), (22, "ink: outline, eyes, brows, brim, envelope flap line"),
       (13, "beak, legs, feet: gold (small areas)"), (5, "mail bag, flap, strap: wood"),
       (23, "envelope, cap badge, cere, eye glint"), (7, "envelope stamp")]


def silhouette(name, o, yaw, px=64):
    m = gary(o)
    x0, y0, x1, y1 = pbounds(m, yaw, 0)
    s = (px - 2) / max(y1 - y0, (x1 - x0) * 0.6)
    w = int(math.ceil((x1 - x0) * s)) + 4
    hh = int(math.ceil((y1 - y0) * s)) + 2
    inner = render(m, yaw, 0, s, -x0 * s + 2, -y0 * s + 1, 0.01, mono=INK)
    sv = write(f"{name}.svg", w, max(hh, 8), inner, "#FFFFFF")
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(sv, one)
    x4 = os.path.join(TMP, f"{name}-x4.png")
    sh(one, "-filter", "point", "-resize", "400%", "-bordercolor", INK, "-border", "1", x4)
    return one, x4


def head_crop(name, o, s=2.6):
    w, h = int(120 * s), int(110 * s)
    sv = write(f"{name}.svg", w, h, render(gary(o), 0, 0, s, w / 2, h / 2 + 158 * s, 4.5), CREAM)
    png = os.path.join(TMP, f"{name}.png")
    sh(sv, png)
    return png


def sheet():
    W, H = 2900, 3600
    i = [text(30, 50, "GHOSTED: Gary the pigeon postman, model sheet v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnaround (rest: wings folded, bag on). Body map v1. Direction A "
              "(round postie). Palette rows only.", 18)]
    s1, g1 = 2.6, 760
    xs = [230, 640, 1060, 1470]
    labs = ["FRONT", "3/4 (front turned to viewer-left)", "SIDE (facing viewer-left)", "BACK"]
    rows = [("cap top", LM["cap_top"]), ("eye line", LM["eye"]), ("beak root", LM["beak"]),
            ("wing root", LM["wing_root"]), ("belly / bag", LM["belly"]), ("sole", 0)]
    for lab, Hh in rows:
        yy = g1 - Hh * s1
        i.append(guide(40, 1680, yy, 0.4))
        i.append(text(1690, yy + 5, lab, 15, "normal", NOTE))
    for x, lab, yw in zip(xs, labs, (0, 35, 90, 180)):
        i.append(text(x - 170, 125, lab, 17, "bold"))
        i.append(shadow(x, g1 + 5, 110, 12))
        i.append(render(gary(), yw, 0, s1, x, g1, 4.5))
    px_ = 1990
    i.append(text(px_, 125, "PALETTE (existing rows only, seats/lena-park.md)", 17, "bold"))
    for k, (r, use) in enumerate(PAL):
        y = 145 + k * 40
        i.append(f'<path d="M{px_},{y} L{px_ + 30},{y} L{px_ + 30},{y + 30} L{px_},{y + 30} Z" fill="{ROW[r]}" '
                 f'stroke="{INK}" stroke-width="2"/>')
        i.append(text(px_ + 42, y + 21, f"{r} {ROW[r]}  {use}", 16))
    i.append(text(px_, 145 + len(PAL) * 40 + 10, f"Shade: base x {SHADE_K} (neutral grey multiplier).", 16))
    rules = ["SHAPE RULES",
             "- Toy pigeon: a round head on a tilted egg body,",
             "  a flat tail fan, 0.5 x Kit standing (cap in).",
             "- Face: 2 ink eyes + glint, small brows, a gold",
             "  cone beak with a cream cere. No mouth, ever.",
             "- Kepi: navy, set back on the crown, tilted back;",
             "  ink brim, cream badge. Never over the eyes.",
             "- Wings: blue 9, two rigid segments + 3 finger",
             "  feathers; the fingers hold the envelope.",
             "- Satchel: wood, his left belly front; one strap",
             "  loop over his right shoulder.",
             "- Envelope: cream card, ink V flap, red stamp."]
    for k, ln in enumerate(rules):
        i.append(text(px_, 520 + k * 23, ln, 16, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))

    # ---- row 2: flight and motion (camera-like view: yaw 20, pitch 25)
    y2, g2 = 880, 1290
    i.append(text(30, y2, "FLIGHT: the 0.6 s flap loop (3 keys: up, level, down), legs tucked, body pitched 10 deg "
                  "nose down, letter in the beak. View: yaw 20, pitch 25.", 18, "bold", NOTE))
    fl = [({"wings": "spread", "flap": 50}, "up (0.0 s)"), ({"wings": "spread", "flap": 5}, "level (0.15 / 0.45 s)"),
          ({"wings": "spread", "flap": -35}, "down (0.3 s)")]
    for k, (o, lab) in enumerate(fl):
        o = dict(o, env="beak", legs="tuck", pitch=10, lift=40)
        x = 230 + k * 560
        i.append(shadow(x, g2 + 6, 60, 9))
        i.append(render(gary(o), 20, 25, 1.05, x, g2, 3.0))
        i.append(text(x - 60, g2 + 40, lab, 15, "bold"))
    y3, g3 = 1370, 1720
    i.append(text(30, y3, "DELIVERY BEATS (yaw 20, pitch 25): fly in, land hop, hold out the letter, then a NO "
                  "(sorry tilt) or a YES (happy hop), fly off", 18, "bold", NOTE))
    beats = [({"wings": "spread", "flap": 20, "env": "beak", "legs": "tuck", "pitch": 10, "lift": 70}, 20,
              "1 fly in (letter in beak)"),
             ({"wings": "half", "flap": 35, "env": "beak", "lift": 22}, 20, "2 land: a little hop"),
             ({"wings": "hold", "env": "wing"}, 20, "3 hold out the letter"),
             ({"wings": "hold", "env": "wing", "face": "sorry", "head_tilt": -14, "head_nod": 6}, 20,
              "4a NO: soft 'sorry' tilt"),
             ({"wings": "half", "flap": 45, "face": "happy", "lift": 30}, 20, "4b YES: happy hop"),
             ({"wings": "spread", "flap": 50, "legs": "tuck", "pitch": -8, "lift": 70}, 200, "5 fly off")]
    for k, (o, yw, lab) in enumerate(beats):
        x = 240 + k * 300
        i.append(shadow(x, g3 + 6, 52, 8))
        i.append(render(gary(o), yw, 25, 1.05, x, g3, 3.0))
        i.append(text(x - 110, g3 + 40, lab, 15, "bold"))
    # expressions
    ex_ = 2010
    i.append(text(ex_, y2, "EXPRESSIONS (front; eyes + brows only)", 18, "bold", NOTE))
    exprs = [({}, "rest: soft"), ({"face": "happy"}, "happy (yes)"), ({"face": "sorry", "head_tilt": -14}, "sorry (no)"),
             ({"face": "oops"}, "oops (bumbling)")]
    for k, (o, lab) in enumerate(exprs):
        i.append(text(ex_ + (k % 2) * 330, y2 + 40 + (k // 2) * 330, lab, 16, "bold"))

    # ---- row 4: silhouettes, lineups
    y4 = 1820
    i.append(text(30, y4, "64 px SILHOUETTES (front, 3/4, side, flight; 1x and x4)", 18, "bold", NOTE))
    i.append(text(900, y4, "LINEUPS AT THE GAME CAMERA (x2): Gary standing next to Kit and Gary flying (0.9 m up), on the "
                  "real Panel v1 renders (Kit, the Panel; on the path also Juno, Dot, Brett, Ricky, Ghosties, ATS).",
                  17, "bold", NOTE))
    i.append(text(900, y4 + 22, "Top: grass colour, grass grey. Bottom: path colour, path grey (Lena's formula).", 15))
    vals = [f"body 8 vs grass 1: {ratio(ROW[8], GREEN):.2f}:1; vs path 3: {ratio(ROW[8], PATHC):.2f}:1 (low: the ink "
            f"outline and the dark parts carry him)",
            f"wings 9 vs grass: {ratio(ROW[9], GREEN):.2f}:1; vs path: {ratio(ROW[9], PATHC):.2f}:1; vs body 8: "
            f"{ratio(ROW[9], ROW[8]):.2f}:1. Cap 26 vs body 8: {ratio(ROW[26], ROW[8]):.2f}:1",
            f"bag 5 vs grass: {ratio(ROW[5], GREEN):.2f}:1; vs body 8: {ratio(ROW[5], ROW[8]):.2f}:1. Beak 13 vs body "
            f"8: {ratio(ROW[13], ROW[8]):.2f}:1 (shape, not value). Envelope 23 vs wing 9: {ratio(ROW[23], ROW[9]):.2f}:1",
            f"body 8 vs ATS robot 18: {ratio(ROW[8], ROW[18]):.2f}:1 (lighter, and round, not boxes); vs Ghostie 16: "
            f"{ratio(ROW[8], '#F8F4EA'):.2f}:1"]
    for k, v in enumerate(vals):
        i.append(text(900, y4 + 840 + k * 24, v, 15))

    # ---- row 5: game camera next to Kit, face check
    y5 = 2830
    i.append(text(30, y5, "GAME CAMERA NEXT TO KIT (x3): rest, hold out, sorry, happy hop, flight; grass then path. "
                  "1x at the right.", 18, "bold", NOTE))
    fc = face_check()
    fcs = face_check({"face": "sorry", "head_tilt": -14, "head_nod": 6, "wings": "hold", "env": "wing"})
    hpx, wpx = measure_px()
    sz = [f"SIZE: {hpx} x {wpx} px standing at 1x (Kit 75 px) = {TARGET_M:.2f} m to the cap top.",
          f"Wingspan {SPAN_M:.2f} m = {SPAN_M / KIT_M:.2f} x Kit. 1 u = {M_PER_U * 1000:.2f} mm.",
          f"Eyes clear: lowest cap pixel {min(fc['left']['cap_above_eye_top_px'], fc['right']['cap_above_eye_top_px']):.1f}"
          f" px above the eye top at rest, {min(fcs['left']['cap_above_eye_top_px'], fcs['right']['cap_above_eye_top_px']):.1f}"
          f" px in the sorry tilt. Beak {fc['beak']['w_px']:.0f} x {fc['beak']['h_px']:.0f} px."]
    for k, ln in enumerate(sz):
        i.append(text(1950, y5 + 60 + k * 24, ln, 15))
    svg = write("gary-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "gary-sheet.png")
    sh(svg, png)

    for k, (o, lab) in enumerate(exprs):
        hc = head_crop(f"face-{k}", o)
        sh(hc, "-resize", "300x", hc)
        comp(png, hc, ex_ + (k % 2) * 330, y2 + 52 + (k // 2) * 330)
    sils = [(None, 0, "sil-front"), (None, 35, "sil-34"), (None, 90, "sil-side"),
            ({"wings": "spread", "flap": 20, "legs": "tuck"}, 0, "sil-fly")]
    x = 40
    for o, yw, nm in sils:
        one, x4 = silhouette(nm, o, yw)
        comp(png, one, x, y4 + 40)
        if nm == "sil-front":
            sh(one, os.path.join(OUT, "silhouette-64.png"))
        if nm == "sil-fly":
            sh(x4, "-resize", "820x", x4)
            comp(png, x4, 40, y4 + 420)
        else:
            comp(png, x4, {"sil-front": 40, "sil-34": 210, "sil-side": 390}[nm], y4 + 130)
        x += Image.open(one).size[0] + 120 if nm != "sil-side" else Image.open(one).size[0] * 4 + 40
    xf4 = os.path.join(TMP, "sil-fly-x4.png")
    lg = [lineup("lu-grass-colour", "grass"), lineup("lu-grass-grey", "grass", grey=True),
          lineup("lu-path-colour", "path"), lineup("lu-path-grey", "path", grey=True)]
    for k, (o1, o2) in enumerate(lg):
        t = os.path.join(TMP, f"lu-fit-{k}.png")
        sh(o2, "-resize", "x380", t)
        comp(png, t, 900 + (k % 2) * (Image.open(t).size[0] + 12), y4 + 40 + (k // 2) * 390)
    poses = [(None, "rest"), ({"wings": "hold", "env": "wing"}, "hold"),
             ({"wings": "hold", "env": "wing", "face": "sorry", "head_tilt": -14, "head_nod": 6}, "sorry"),
             ({"wings": "half", "flap": 45, "face": "happy", "lift": 30}, "happy"),
             ({"wings": "spread", "flap": 30, "env": "beak", "legs": "tuck", "pitch": 10, "lift": 140}, "fly")]
    for r_, (bg, tag) in enumerate(((GREEN, "g"), (PATHC, "p"))):
        for k, (o, lab) in enumerate(poses):
            one, x3 = cam_png(f"sheet-cam-{tag}-{k}", o, 110, 110 if lab != "fly" else 110, bg, kit=True)
            comp(png, x3, 30 + k * 345, y5 + 40 + r_ * 345)
            comp(png, one, 1760 + k * 118, y5 + 160 + r_ * 125) if False else None
    for r_, (bg, tag) in enumerate(((GREEN, "g"), (PATHC, "p"))):
        for k in range(len(poses)):
            comp(png, os.path.join(TMP, f"sheet-cam-{tag}-{k}-1x.png"), 1950 + k * 116, y5 + 150 + r_ * 125)
    return png, (hpx, wpx), fc, fcs


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    print(f"M_PER_U {M_PER_U * 1000:.3f} mm, HU {HU:.1f}, GS {GS:.4f}, span {SPAN_M:.3f} m")
    if "explore" in what:
        print(explore())
    if "bodymap" in what:
        print(body_map())
    if "sheet" in what:
        print(sheet())
