"""Build explore.png, body-map.png, ricky-sheet.png and silhouette-64.png for Recruiter Ricky.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
Reads only: kit/turn-front.png, kit/turn-side.png, ghostie/v7/front-variants.png, ghostie/v7/lineup-grass.png,
and the Ghostie sketch parts (ghostie/sketch/src/ghost.py). Writes only into ../ and ./ (and ./_tmp, ../crops).
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ASSETS = os.path.abspath(os.path.join(OUT, "..", ".."))
sys.path.insert(0, HERE)
from ricky import *  # noqa

sys.path.insert(0, os.path.join(ASSETS, "ghostie", "sketch", "src"))
import ghost as G  # noqa

TMP = os.path.join(HERE, "_tmp")
CROPS = os.path.join(OUT, "crops")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CROPS, exist_ok=True)

KIT_FRONT = os.path.join(ASSETS, "kit", "turn-front.png")
KIT_SIDE = os.path.join(ASSETS, "kit", "turn-side.png")
GH_VAR = os.path.join(ASSETS, "ghostie", "v7", "front-variants.png")
LINEUP = os.path.join(ASSETS, "ghostie", "v7", "lineup-grass.png")
LINEUP_BOX = (641, 397, 1001, 597)     # v7 make_sheets.py box (661,397,961,537), widened for free grass

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # kit/ingame.html L156: fov 26, 26 m, 900 px tall
GS = PX_PER_M * M_PER_U                                 # game-camera px per unit at 1x
CAM = (20.0, 42.0)
OUTLINE = 1.6
KIT_PX = 72.0      # Kit's real ink height in v7/lineup-grass.png (y 424-496), incl. the tuft
GH_UNIT = 0.57 / 265 / M_PER_U    # Ghostie: 0.57 m crown to hem (37 px wide in the v7 lineup / 75 px per m)
GH_FLOAT = 0.22 / M_PER_U         # ghost_toon.json float_rest_m


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


def box(x0, y0, x1, y1, c=NOTE, w=3):
    return f'<path d="M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z" fill="none" stroke="{c}" stroke-width="{w}"/>'


def shadow(cx, cy, rx, ry, o=0.16):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#2B1E16" fill-opacity="{o}" stroke="none"/>')


def grey_img(src, dst):
    """Same luminance formula as ghostie/v7/make_sheets.py (Lena's gate)."""
    p = np.asarray(Image.open(src).convert("RGB")).astype(float) / 255
    lin = np.where(p <= 0.04045, p / 12.92, ((p + 0.055) / 1.055) ** 2.4)
    Y = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
    s = np.where(Y <= 0.0031308, 12.92 * Y, 1.055 * np.power(Y, 1 / 2.4) - 0.055)
    Image.fromarray((s * 255).round().astype(np.uint8)).convert("RGB").save(dst)


def lum(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ============================================================ poses and drain steps
def squash(sx, sy):
    return lambda q: (q[0] * sx, q[1] * sy, q[2] * sx)


DRAIN = [
    ("Ricky", {}),
    ("step 1: colour drains, legs fade, lifts",
     {"colors": {"suit": ROW[11], "leg": ROW[27], "shoe": ROW[27], "mic": ROW[27]}, "legs": 0.55, "lift": 14,
      "mouth": "small"}),
    ("step 2: white, no legs, no mouth, floats",
     {"colors": {"suit": ROW[27], "skin": ROW[16], "hand": ROW[16], "head_acc": ROW[27]},
      "hair": "none", "legs": 0, "mouth": "none", "mic": False, "lift": 44, "merge": 1,
      "jacket": "M162,140 C192,146 212,160 216,178 C220,204 222,232 224,254 C224,266 212,272 196,270 "
                "C184,276 166,278 150,276"}),
]


def render_with(parts, yaw, pitch, s, ox, oy, ink_w, xf=None, **kw):
    return render(parts, yaw, pitch, s, ox, oy, ink_w, xf=xf, **kw)


def ghostie_front(x, ground_y, s_units, variant="both"):
    """The locked Ghostie front (sketch v2 parts), scaled to Ricky's units; hem floats 0.22 m.
    Returns (svg, gy) where gy(y) maps a Ghostie front-view y to the screen."""
    gs = GH_UNIT * s_units
    hem_y = ground_y - GH_FLOAT * s_units
    inner = [G.path(G.FRONT_BODY, G.BODY, G.INK, 5), G.path(G.FRONT_SHADE, G.SHADE), G.eyes_svg(G.EYES)]
    if variant in ("both", "tie"):
        inner.append(G.tie_svg(150, 5))
    if variant in ("both", "headset"):
        inner.append(G.headset_svg(5))
    ty = hem_y - G.LM["hem"] * gs
    svg = (f'<g transform="translate({x - 150 * gs:.2f},{ty:.2f}) scale({gs:.4f})">' + "".join(inner) + "</g>")
    return svg, (lambda y: ty + y * gs), (lambda gx: x + (gx - 150) * gs)


# ============================================================ game-camera tiles
def cam_scale():
    """Metric estimate vs the screen target. Returns (metric px, calibrated px per unit)."""
    x0, y0, x1, y1 = bounds(model(), *CAM)
    metric = (y1 - y0) * GS + 2 * OUTLINE
    target = 1.05 * KIT_PX
    return metric, GS * target / metric


GSC = None


def cam_png(name, opts=None, w=80, h=96, bg=None, xf=None, yaw=CAM[0], mark=None):
    """Ricky at the game camera, 1x pixels, feet centre at (w/2, h-12). Returns (1x path, x3 path, info)."""
    m = model(opts)
    ox, oy = w / 2, h - 14
    inner = shadow(ox, oy + 2, 17, 6, 0.22) if bg else ""
    inner += render_with(m, yaw, CAM[1], cam_scale()[1], ox, oy, OUTLINE, xf=xf, mark_scale=1.0)
    if mark:
        inner += mark(ox, oy)
    sv = write(f"{name}.svg", w, h, inner, bg)
    one = os.path.join(TMP, f"{name}-1x.png")
    if bg:
        sh(sv, one)
    else:
        sh("-background", "none", sv, one)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def lineup(name="lineup", grey=False):
    """v7 lineup crop (Kit + 3 Ghosties, real renders) with the Ricky estimate placed on free grass."""
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(LINEUP).crop(LINEUP_BOX).save(base)
    one, _ = cam_png(f"{name}-ricky", None, 90, 110)
    sh_ = write(f"{name}-shadow.svg", 90, 110, shadow(45, 98, 17, 6, 0.28))
    shp = os.path.join(TMP, f"{name}-shadow.png")
    sh("-background", "none", sh_, shp)
    comp(base, shp, 130, 72)
    comp(base, one, 130, 72)
    out1 = os.path.join(TMP, f"{name}-1x.png")
    sh(base, out1)
    if grey:
        grey_img(out1, out1)
    out3 = os.path.join(TMP, f"{name}-x3.png")
    sh(out1, "-filter", "point", "-resize", "300%", out3)
    return out1, out3


# ============================================================ EXPLORE
THUMBS = [
    ("1 bell jacket, pompadour", {}),
    ("2 box suit, slick hair", {"jacket": JACKET_BOX, "hair": "slick"}),
    ("3 power suit (wide top)", {"jacket": JACKET_TRI, "hair": "side"}),
    ("4 capsule (BMGD seat)", {"jacket": JACKET_CAP}),
    ("5 cone skirt (Viet seat)", {"jacket": JACKET_CONE, "hair": "slick"}),
    ("6 egg body, big head", {"jacket": JACKET_EGG, "head_s": 1.12, "hair": "slick"}),
    ("7 bell, bald", {"hair": "none"}),
    ("8 bell, side part, small head", {"hair": "side", "head_s": 0.9}),
    ("9 power suit, big head", {"jacket": JACKET_TRI, "head_s": 1.12}),
    ("10 box suit, bald, no mic", {"jacket": JACKET_BOX, "hair": "none", "mic": False}),
]
DIRS = [
    ("A. BELL JACKET (pick)", {}, ["Round head on a soft bell jacket:", "the same toy-pawn family as Kit.",
                                    "The jacket hem and the round top", "already echo the Ghostie, so the",
                                    "drain is a short morph."]),
    ("B. POWER SUIT", {"jacket": JACKET_TRI, "hair": "side"},
     ["Wide top, narrow hem: says 'sales'.", "Sharp shoulders fight Kit's round", "family, and the drain must flip a",
      "triangle into a dome. Side part", "breaks the symmetric front."]),
    ("C. CAPSULE", {"jacket": JACKET_CAP},
     ["Closest to Kit's body. At the game", "camera he reads as 'a dark Kit':", "only value tells them apart.",
      "Safe, but no shape of his own."]),
]


def explore():
    W, H = 2600, 1800
    i = [text(30, 50, "GHOSTED: Recruiter Ricky, explore (Illustrator, 2026-11-25)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: references, 10 rough thumbnails, 3 directions, one pick. "
              "Hand-drawn Bezier half outlines lifted to round bodies; palette rows only.", 18)]
    # references
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, no web)", 20, "bold", NOTE))
    i.append(text(30, ry + 330, "Kit v5 front + side (hero, 0.95 m)", 15))
    i.append(text(560, ry + 330, "Ghostie v7, locked (drain end): tie, glasses, headset", 15))
    i.append(text(1500, ry + 345, "v7 lineup at the game camera (x2): Kit + 3 Ghosties", 15))
    # thumbnails
    ty = 520
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x3, 26 m, "
                  "pitch 42, yaw 20).", 20, "bold", NOTE))
    tw = 254
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 6, ty + 34, lab, 14, "bold"))
        m = model(o)
        i.append(render(m, 0, 0, 0.62, x + tw / 2, ty + 270, 2.2, mark_scale=0.8))
        i.append(shadow(x + tw / 2, ty + 272, 50, 6))
    # directions
    dy = 1160
    i.append(text(30, dy, "DIRECTIONS (3), developed: front, 3/4, back; then the game camera (x3), Ricky left, "
                  "Kit right (real v7 render)", 20, "bold", NOTE))
    dw = 860
    for n, (lab, o, notes) in enumerate(DIRS):
        x = 30 + n * dw
        i.append(text(x + 10, dy + 40, lab, 20, "bold", NOTE if n == 0 else INK))
        for k, yw in enumerate((0, 35, 180)):
            i.append(render(model(o), yw, 0, 0.72, x + 80 + k * 140, dy + 340, 2.4, mark_scale=0.9))
            i.append(shadow(x + 80 + k * 140, dy + 342, 56, 7))
        for k, ln in enumerate(notes):
            i.append(text(x + 10, dy + 400 + k * 22, ln, 16))
        if n == 0:
            i.append(box(x, dy + 12, x + dw - 20, dy + 530, NOTE, 4))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    # references
    kf = os.path.join(TMP, "ref-kit-front.png")
    sh(KIT_FRONT, "-crop", "620x1080+140+20", "+repage", "-resize", "x290", kf)
    ks = os.path.join(TMP, "ref-kit-side.png")
    sh(KIT_SIDE, "-crop", "620x1080+140+20", "+repage", "-resize", "x290", ks)
    gv = os.path.join(TMP, "ref-ghostie.png")
    sh(GH_VAR, "-crop", "1800x640+0+120", "+repage", "-resize", "x290", gv)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(LINEUP, "-crop", "360x150+641+397", "+repage", "-filter", "point", "-resize", "200%", lu)
    comp(png, kf, 30, ry + 25)
    comp(png, ks, 290, ry + 25)
    comp(png, gv, 560, ry + 25)
    comp(png, lu, 1500, ry + 25)
    # thumbnail game-camera tiles
    for n, (lab, o) in enumerate(THUMBS):
        _, x3 = cam_png(f"ex-thumb-{n}", o, 70, 92, "#B5D67A")
        comp(png, x3, 30 + n * tw + 22, ty + 290)
    # direction game-camera tiles + Kit crop x3
    kit3 = os.path.join(TMP, "kit-cam-x3.png")
    sh(LINEUP, "-crop", "70x92+852+412", "+repage", "-filter", "point", "-resize", "300%", kit3)
    for n, (lab, o, notes) in enumerate(DIRS):
        _, x3 = cam_png(f"ex-dir-{n}", o, 70, 92, "#B5D67A")
        comp(png, x3, 30 + n * dw + 440, dy + 60)
        comp(png, kit3, 30 + n * dw + 640, dy + 60)
    return png


# ============================================================ BODY MAP
def gamecam_marks(ox, oy, opts=None):
    """Landmark dots at the game camera (1x), from the same projection as the render."""
    P, _ = cam(*CAM)
    GK = cam_scale()[1]
    head = profile("M150,53 C187,53 209,75 209,104 C209,133 186,153 150,153")
    jk = profile(JACKET_HALF)

    def surf(x, y, prof, d):
        X = x - 150
        r = r_at(prof, y)
        X = max(-r, min(r, X))
        z = r * d * math.sqrt(max(1 - (X / max(r, 1e-3)) ** 2, 0))
        u, v, _ = P((X, GROUND - y, z))
        return ox + u * GK, oy + v * GK
    pts = {
        "eye_l": surf(132, LM["eye"], head, 0.92), "eye_r": surf(168, LM["eye"], head, 0.92),
        "mouth": surf(150, 122, head, 0.92),
        "cup_l": (ox + P((-61, GROUND - 100, -2))[0] * GK, oy + P((-61, GROUND - 100, -2))[1] * GK),
        "cup_r": (ox + P((61, GROUND - 100, -2))[0] * GK, oy + P((61, GROUND - 100, -2))[1] * GK),
        "band_top": (ox + P((0, GROUND - 32, -6))[0] * GK, oy + P((0, GROUND - 32, -6))[1] * GK),
        "knot": surf(150, LM["knot"], jk, 0.82), "tie_v": surf(150, LM["tie_v"], jk, 0.82),
        "hand_l": (ox + P((-79, GROUND - 246, 8))[0] * GK, oy + P((-79, GROUND - 246, 8))[1] * GK),
        "hand_r": (ox + P((79, GROUND - 246, 8))[0] * GK, oy + P((79, GROUND - 246, 8))[1] * GK),
        "hem": surf(150, LM["hem"] - 2, jk, 0.82),
        "feet": (ox + P((0, GROUND - 330, 9))[0] * GK, oy + P((0, GROUND - 330, 9))[1] * GK),
    }
    return pts


def body_map():
    W, H = 2600, 2000
    i = [text(30, 50, "GHOSTED: Recruiter Ricky body map v1 (Illustrator, 2026-11-25)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions in head-heights, landmarks, attachment points, "
              "the drain mapping to the Ghostie, and a check at the game camera (26 m, pitch 42, yaw 20).", 18)]
    # ---- A. front, big
    s = 2.3
    fx, gy0 = 360, 140
    gy = lambda y: gy0 + y * s
    fxx = lambda x: fx + (x - 150) * s
    i.append(text(30, 125, "A. FRONT (upright, symmetric)", 20, "bold", NOTE))
    rows = [("top of quiff", LM["top"]), ("crown (hair cap)", LM["crown"]), ("eye line = ear points", LM["eye"]),
            ("mouth zone", 129), ("chin / neck line, collar top", LM["neck"]), ("knot top", LM["knot"]),
            ("shoulder joint (arm root)", LM["shoulder"]), ("chest", LM["chest"]), ("tie V point", LM["tie_v"]),
            ("hand centre (cuff above)", LM["hand"]), ("jacket hem", LM["hem"]),
            ("ankle", LM["ankle"]), ("sole", LM["sole"])]
    x_end = fx + 190 * s
    for lab, y in rows:
        i.append(guide(fx - 170 * s / 2.3 - 20, x_end, gy(y)))
        i.append(text(x_end + 8, gy(y) + 5, f"{lab}  y {y}", 15, "bold" if "eye" in lab or "neck" in lab else "normal",
                      NOTE))
    m = model()
    i.append(shadow(fx, gy(342), 110, 12))
    i.append(render(m, 0, 0, s, fx, gy(GROUND), 5))
    # attachment dots
    for x in LM["ear_x"]:
        i.append(dot(fxx(x), gy(100), 7))
    i.append(dot(fxx(150), gy(32), 7))
    i.append(dot(fxx(150), gy(LM["neck"]), 7))
    i.append(dot(fxx(150), gy(LM["knot"]), 6))
    for x in LM["shoulder_x"]:
        i.append(dot(fxx(x + (0 if x > 150 else 0)), gy(LM["shoulder"]), 7, "#E0533D"))
    # mouth zone
    x0, y0, x1, y1 = LM["mouth"]
    i.append(f'<path d="M{fxx(x0)},{gy(y0)} L{fxx(x1)},{gy(y0)} L{fxx(x1)},{gy(y1)} L{fxx(x0)},{gy(y1)} Z" '
             f'fill="none" stroke="{NOTE}" stroke-width="3" stroke-dasharray="8,6"/>')
    # head-height ruler
    rx = 60
    hh = LM["chin"] - LM["top"]
    ticks = [LM["top"], LM["top"] + hh, LM["top"] + 2 * hh, LM["sole"]]
    i.append(f'<path d="M{rx},{gy(ticks[0])} L{rx},{gy(ticks[-1])}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    for t in ticks:
        i.append(f'<path d="M{rx - 10},{gy(t)} L{rx + 10},{gy(t)}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    i.append(text(rx + 14, gy(LM["top"] + hh / 2), "1 head", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["top"] + 1.5 * hh), "2", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["top"] + 2.35 * hh), "2.67", 15, "bold", NOTE))

    # ---- B. side
    sx = 1330
    i.append(text(sx - 150, 125, "B. SIDE (same lines)", 20, "bold", NOTE))
    for lab, y in rows:
        i.append(guide(sx - 140, sx + 150, gy(y), 0.35))
    i.append(shadow(sx, gy(342), 70, 10))
    i.append(render(model(), 90, 0, s, sx, gy(GROUND), 5))
    for y in (100,):
        i.append(dot(sx - 0 * s, gy(y), 7))
    i.append(dot(sx + 6 * s, gy(32), 7))

    # ---- C. notes (right)
    nx = 1620
    notes = [("PROPORTIONS (head = top of quiff to chin = 114 units)", True),
             ("Height 304 units = 1.00 m = 1.05 x Kit (0.95 m).", False),
             ("2.67 head-heights (Kit 2.71: the same family).", False),
             ("Head 112 wide; jacket 136 at the shoulders, 148 at the hem.", False),
             ("Legs 50 (hem to ankle), shoes 22: short, like Kit.", False),
             ("", False),
             ("LANDMARKS", True),
             ("Eye line y 98; eyes x 132 / 168 (ink ovals + glint).", False),
             ("Ears: on the eye line at the head sides (x 94 / 206),", False),
             ("  small; the headset cups cover them.", False),
             ("Mouth zone x 125-175, y 110-134: a wide grin.", False),
             ("  It fades in drain step 2 (a ghost never replies).", False),
             ("Neck: hidden. Chin y 150 = neck line; a white shirt", False),
             ("  collar rings the neck (value break, all views).", False),
             ("Shoulder joint (red): x 84 / 216, y 176. The arm", False),
             ("  root. Sleeve to the cuff at the wrist y 234.", False),
             ("Hands: skin balls at y 246, beside the hem.", False),
             ("Feet: shoes y 320-340, toes forward.", False),
             ("", False),
             ("ATTACHMENT POINTS (blue)", True),
             ("Headset band: centred over the crown, top y 32,", False),
             ("  in the ear plane (6 units behind the centre).", False),
             ("Headset cups: ONE ON EACH EAR POINT,", False),
             ("  centre x 89 / 211, y 100. Mic boom from the", False),
             ("  right cup (viewer-left) to the mouth corner.", False),
             ("Tie: centred on x 150, knot top y 160 under the", False),
             ("  shirt collar at the neck line y 152; V point y 232,", False),
             ("  inside the shirt V (V point y 238).", False)]
    for k, (ln, b) in enumerate(notes):
        i.append(text(nx, 160 + k * 25, ln, 17, "bold" if b else "normal", NOTE if b else INK))

    # ---- D. game camera
    D = (1620, 880)
    i.append(text(D[0], D[1], "D. GAME CAMERA CHECK (x3). Left: Ricky estimate. Middle: same, landmark dots", 20,
                  "bold", NOTE))
    i.append(text(D[0], D[1] + 24, "(blue: eyes, mouth, knot, tie V, hands, hem, feet; red: cups, band top). "
                  "Right: Kit, real v7 render.", 16))
    i.append(text(D[0], D[1] + 350, "Scale: drawn at 1.05 x Kit's real screen height (76 px); see notes.md.", 16))
    # ---- E. drain mapping: Ricky landmarks -> Ghostie landmarks
    E = (30, 1010)
    i.append(text(E[0], E[1], "E. DRAIN MAPPING: each Ricky landmark becomes a Ghostie landmark "
                  "(same metres; Ghostie from its locked body map)", 20, "bold", NOTE))
    es = 2.3
    ground = E[1] + 70 + 340 * es * 1.0
    rxc, gxc = 330, 1080
    i.append(shadow(rxc, ground + 4, 110, 12))
    i.append(render(model(), 0, 0, es, rxc, ground, 5))
    gsvg, gyf, gxf = ghostie_front(gxc, ground, es)
    i.append(shadow(gxc, ground + 4, 90, 10))
    i.append(gsvg)
    ry = lambda y: ground - (GROUND - y) * es
    rx = lambda x: rxc + (x - 150) * es
    pairs = [("eye line", (150, LM["eye"]), (150, G.LM["eye"])),
             ("ear points = cups", (211, 100), (244, G.LM["eye"])),
             ("neck line, collar", (171, LM["neck"]), (173, G.LM["neck"])),
             ("knot top", (158, LM["knot"]), (159, G.LM["knot"])),
             ("tie V point", (150, LM["tie_v"]), (150, G.LM["tie_v"])),
             ("jacket hem -> hem lobes", (222, LM["hem"] - 6), (262, G.LM["hem"] - 9))]
    for k, (lab, (ax_, ay_), (bx_, by_)) in enumerate(pairs):
        x0, y0 = rx(ax_), ry(ay_)
        x1, y1 = gxf(bx_), gyf(by_)
        i.append(f'<path d="M{x0:.1f},{y0:.1f} C{x0 + 220:.1f},{y0:.1f} {x1 - 260:.1f},{y1:.1f} {x1:.1f},{y1:.1f}" '
                 f'fill="none" stroke="{NOTE}" stroke-width="2.5" stroke-opacity="0.8"/>')
        i.append(dot(x0, y0, 6))
        i.append(dot(x1, y1, 6))
        i.append(text((x0 + x1) / 2 + 40, (y0 + y1) / 2 - 6 + (22 if lab == "knot top" else 0), lab, 15, "bold", NOTE))
    tx = 1330
    tab = [("Ricky (front units)", "Ghostie (its body map)", True),
           ("eye line y 98 (1.00 m figure)", "eye line y 118", False),
           ("cups on the ear points x 89/211", "cups on the ear points x 56/244", False),
           ("band centred over the crown", "band centred over the crown", False),
           ("shirt collar at the neck line y 152", "small collar at the neck line y 166", False),
           ("tie centred, knot top y 160", "tie centred, knot top y 170", False),
           ("tie V point y 232", "tie V point y 258", False),
           ("jacket hem y 268 (round)", "hem: 5 soft lobes y 301", False),
           ("wide grin, mouth zone", "mouth zone EMPTY (fades in step 2)", False),
           ("legs + shoes", "gone (fade in step 1, off in step 2)", False),
           ("mic boom", "gone (faded in step 1, off in step 2)", False),
           ("hair (row 25)", "gone: the quiff melts into the dome", False)]
    for k, (a, c, bold) in enumerate(tab):
        i.append(text(tx, E[1] + 280 + k * 30, a, 16, "bold" if bold else "normal", NOTE if bold else INK))
        i.append(text(tx + 330, E[1] + 280 + k * 30, c, 16, "bold" if bold else "normal", NOTE if bold else INK))
    i.append(text(tx, E[1] + 280 + 13 * 30, "Rule kept: no accessory moves to dodge the camera. Cups stay on the", 16))
    i.append(text(tx, E[1] + 280 + 14 * 30, "ears and the tie stays centred under a collar in every drain step.", 16))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    # game camera tiles with landmark dots
    marks = gamecam_marks(40, 96 - 14)

    def mk(ox, oy):
        o = []
        for k, (u, v) in marks.items():
            c = "#E0533D" if k.startswith("cup") or k == "band_top" else NOTE
            o.append(f'<ellipse cx="{u:.2f}" cy="{v:.2f}" rx="0.9" ry="0.9" fill="{c}" stroke="none"/>')
        return "".join(o)
    _, x3 = cam_png("bm-cam", None, 80, 96, "#B5D67A")
    _, x3m = cam_png("bm-cam-mark", None, 80, 96, "#B5D67A", mark=mk)
    kit3 = os.path.join(TMP, "bm-kit-x3.png")
    sh(LINEUP, "-crop", "80x96+847+410", "+repage", "-filter", "point", "-resize", "300%", kit3)
    comp(png, x3, D[0], D[1] + 40)
    comp(png, x3m, D[0] + 250, D[1] + 40)
    comp(png, kit3, D[0] + 500, D[1] + 40)
    info = {k: (round(u - 40, 1), round(v - 82, 1)) for k, (u, v) in marks.items()}
    return png, info


# ============================================================ SHEET
PAL = [(17, "suit, trousers"), (15, "skin: head, hands"), (25, "hair"), (16, "shirt V, collar, cuffs, teeth"),
       (10, "ACCENT: headset + tie"), (5, "shoes"), (22, "ink: outline, eyes, mouth"),
       (11, "drain step 1 suit"), (27, "drain step 2 suit, faded headset")]


def silhouette(name, yaw, px=64):
    m = model()
    x0, y0, x1, y1 = bounds(m, yaw, 0)
    s = (px - 2) / (y1 - y0)
    w = int(math.ceil((x1 - x0) * s)) + 4
    inner = render(m, yaw, 0, s, -x0 * s + 2, -y0 * s + 1, 0.01, mono=INK)
    sv = write(f"{name}.svg", w, px, inner, "#FFFFFF")
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(sv, one)
    x4 = os.path.join(TMP, f"{name}-x4.png")
    sh(one, "-filter", "point", "-resize", "400%", "-bordercolor", INK, "-border", "1", x4)
    return one, x4


def sheet():
    W, H = 2800, 2560
    i = [text(30, 50, "GHOSTED: Recruiter Ricky model sheet v1 (Illustrator, 2026-11-25)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnaround. Body map v1 landmarks. Direction A (bell jacket). "
              "Hand-drawn Bezier half outlines lifted to round bodies; palette rows only.", 18)]
    # ---- 1. turnaround
    s1, g1 = 1.9, 820
    xs = [250, 650, 1050, 1450]
    labs = ["FRONT", "3/4 (front turned to viewer-left)", "SIDE (facing viewer-left)", "BACK"]
    rows = [("top of quiff", LM["top"]), ("eye line = ear points = cups", LM["eye"]), ("neck line, collar", LM["neck"]),
            ("shoulder joint", LM["shoulder"]), ("jacket hem", LM["hem"]), ("sole", LM["sole"])]
    for lab, y in rows:
        yy = g1 - (GROUND - y) * s1
        i.append(guide(60, 1660, yy, 0.45))
        i.append(text(1670, yy + 5, lab, 15, "bold" if "eye" in lab else "normal", NOTE))
    for x, lab, yw in zip(xs, labs, (0, 35, 90, 180)):
        i.append(text(x - 170, 125, lab, 17, "bold"))
        i.append(shadow(x, g1 + 6, 120 if yw != 90 else 80, 12))
        i.append(render(model(), yw, 0, s1, x, g1, 4.5))
    # palette + rules
    px_ = 1990
    i.append(text(px_, 125, "PALETTE (existing rows only, seats/lena-park.md)", 17, "bold"))
    for k, (r, use) in enumerate(PAL):
        y = 145 + k * 40
        i.append(f'<path d="M{px_},{y} L{px_ + 30},{y} L{px_ + 30},{y + 30} L{px_},{y + 30} Z" fill="{ROW[r]}" '
                 f'stroke="{INK}" stroke-width="2"/>')
        i.append(text(px_ + 42, y + 21, f"{r} {ROW[r]}  {use}", 16))
    i.append(text(px_, 145 + 9 * 40 + 10, f"Shade: base x {SHADE_K} (neutral grey multiplier).", 16))
    rules = ["SHAPE RULES",
             "- Toy pawn, 2.67 heads (Kit 2.71). 1.00 m.",
             "- Round head, eye line = ear line = cups.",
             "- Bell jacket: soft shoulders, flares a little.",
             "- Headset: band centred over the crown,",
             "  one cup on EACH ear, mic from the right cup.",
             "- Tie centred under the shirt collar, inside",
             "  the shirt V. Accent row 10 on both.",
             "- Value break vs Kit: white shirt V, collar",
             "  ring, cuffs + the light accent on a dark suit.",
             "- Joins: a shoulder ball at each arm root;",
             "  sleeve, then a white cuff, then the hand."]
    for k, ln in enumerate(rules):
        i.append(text(px_, 560 + k * 23, ln, 16, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))

    # ---- 2. drain strip, phone gesture, hop
    y2, g2, s2 = 930, 1520, 1.25
    i.append(text(30, y2, "DRAIN (front, same metres): colour drains to white, legs fade, he floats; headset and tie "
                  "stay on the same landmarks", 18, "bold", NOTE))
    dxs = [170, 470, 770, 1070]
    for k, (lab, o) in enumerate(DRAIN):
        i.append(shadow(dxs[k], g2 + 5, 75, 9, 0.16 - 0.04 * k))
        sc = (1.0, 0.95, 0.85)[k]
        i.append(render_with(model(o), 0, 0, s2, dxs[k], g2, 3.5, xf=squash(sc, sc)))
        i.append(text(dxs[k] - 140, y2 + 34, lab, 14, "bold" if k == 0 else "normal"))
    gsvg, _, _ = ghostie_front(dxs[3], g2, s2)
    i.append(shadow(dxs[3], g2 + 5, 60, 8, 0.08))
    i.append(gsvg)
    i.append(text(dxs[3] - 140, y2 + 34, "step 3: the locked Ghostie (v7)", 14, "bold"))
    i.append(text(dxs[3] - 140, y2 + 52, "(shown with both parts: see notes)", 13))
    for k in range(3):
        xa = dxs[k] + 105
        i.append(f'<path d="M{xa},{g2 - 220} L{xa + 80},{g2 - 220}" fill="none" stroke="{NOTE}" stroke-width="4"/>')
        i.append(f'<path d="M{xa + 80},{g2 - 228} L{xa + 92},{g2 - 220} L{xa + 80},{g2 - 212} Z" fill="{NOTE}" '
                 f'stroke="none"/>')
    # phone gesture
    px2 = 1330
    i.append(text(px2, y2, "ON THE PHONE: right hand to the right cup", 18, "bold", NOTE))
    i.append(text(px2, y2 + 24, "(shoulder ball, elbow out, wrist, hand on the cup)", 14))
    for k, yw in enumerate((0, 35)):
        x = px2 + 150 + k * 290
        i.append(shadow(x, g2 + 5, 80, 9))
        i.append(render(model({"arm": "phone"}), yw, 0, s2, x, g2, 3.5))
    # joint dots on the front phone pose
    for (X, Hh) in [(-65, GROUND - LM["shoulder"]), (-101, GROUND - 200), (-87, GROUND - 130)]:
        i.append(dot(px2 + 150 + X * s2, g2 - Hh * s2, 6, "#E0533D"))
    # hop
    hx = 2100
    i.append(text(hx, y2, "HOP (like Kit): squash, stretch up, squash", 18, "bold", NOTE))
    i.append(text(hx, y2 + 24, "squash only on the bounce (Kit rule)", 14))
    hop = [(squash(1.08, 0.9), {}, 0), (squash(0.95, 1.07), {"arm": "hop_up", "lift": 0}, 46),
           (squash(1.08, 0.9), {}, 0)]
    for k, (xf, o, up) in enumerate(hop):
        x = hx + 110 + k * 220
        i.append(shadow(x, g2 + 5, 70 - (20 if up else 0), 8))
        i.append(render_with(model(o), 0, 0, 1.0, x, g2 - up, 3, xf=xf))

    # ---- 3. silhouette, lineup, game camera
    y3 = 1640
    i.append(text(30, y3, "64 px SILHOUETTE (front, 3/4; 1x and x4)", 18, "bold", NOTE))
    i.append(text(720, y3, "LINEUP AT THE GAME CAMERA (x2): Ricky estimate on real v7 grass with Kit and 3 Ghosties. "
                  "Colour, then greyscale (Lena's formula).", 18, "bold", NOTE))
    i.append(text(2230, y3, "GAME CAMERA, NEXT TO KIT (x3, 1x)", 18, "bold", NOTE))
    # value facts
    vals = [f"suit 17 vs Kit trousers 26: {ratio(ROW[17], '#2F3E5C'):.2f}:1 (close: the risk)",
            f"shirt 16 vs suit 17: {ratio(ROW[16], ROW[17]):.2f}:1",
            f"accent 10 vs suit 17: {ratio(ROW[10], ROW[17]):.2f}:1",
            f"accent 10 vs Kit tie 7 (#D4503A): {ratio(ROW[10], '#D4503A'):.2f}:1, hue lilac vs red",
            f"accent 10 vs heal orange #F2994A: {ratio(ROW[10], '#F2994A'):.2f}:1, hue lilac vs orange"]
    for k, v in enumerate(vals):
        i.append(text(720, 2160 + k * 26, v, 17))
    i.append(text(720, 2160 + 5 * 26 + 10, "In grey, Ricky reads as a near-black bell with a white V, light cups and "
                  "light hands; Kit reads as a mid-grey body.", 17, "bold"))
    met, _ = cam_scale()
    sz = ["SIZE AT THE GAME CAMERA (open, see notes):",
          f"Drawn at the target: 1.05 x Kit's real {KIT_PX:.0f} px",
          f"= {1.05 * KIT_PX:.0f} px tall. My metric estimate (75 px/m)",
          f"gives {met:.0f} px: the real Kit reaches 13 px above",
          "its own 1 m pole (v7 ingame_report kitTop).",
          "Viet's blockout measures and sets the scale."]
    for k, ln in enumerate(sz):
        i.append(text(2230, y3 + 450 + k * 22, ln, 15, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))
    svg = write("ricky-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "ricky-sheet.png")
    sh(svg, png)

    s1x, s4 = silhouette("sil-front", 0)
    q1x, q4 = silhouette("sil-34", 35)
    comp(png, s1x, 40, y3 + 30)
    comp(png, q1x, 110, y3 + 30)
    comp(png, s4, 40, y3 + 120)
    comp(png, q4, 230 + 120, y3 + 120)
    sh(s1x, os.path.join(OUT, "silhouette-64.png"))
    lc1, _ = lineup("lineup-colour")
    lg1, _ = lineup("lineup-grey", grey=True)
    lc2 = os.path.join(TMP, "lineup-colour-x2.png")
    lg2 = os.path.join(TMP, "lineup-grey-x2.png")
    sh(lc1, "-filter", "point", "-resize", "200%", lc2)
    sh(lg1, "-filter", "point", "-resize", "200%", lg2)
    comp(png, lc2, 720, y3 + 30)
    comp(png, lg2, 1470, y3 + 30)
    one, x3 = cam_png("sheet-cam", None, 80, 96, "#B5D67A")
    kit3 = os.path.join(TMP, "sheet-kit-x3.png")
    sh(LINEUP, "-crop", "80x96+847+410", "+repage", "-filter", "point", "-resize", "300%", kit3)
    kit1 = os.path.join(TMP, "sheet-kit-1x.png")
    sh(LINEUP, "-crop", "80x96+847+410", "+repage", kit1)
    comp(png, x3, 2230, y3 + 30)
    comp(png, kit3, 2490, y3 + 30)
    comp(png, one, 2310, y3 + 340)
    comp(png, kit1, 2570, y3 + 340)
    return png


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    if "explore" in what:
        print(explore())
    if "bodymap" in what:
        print(body_map())
    if "sheet" in what:
        print(sheet())
