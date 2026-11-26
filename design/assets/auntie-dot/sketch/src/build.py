"""Build explore.png, body-map.png, dot-sheet.png and silhouette-64.png for Auntie Dot.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
Reads only: kit/turn-front.png, ricky/v1/turn-front.png, ghostie/v7/turn-front.png, ats9000/v1/turn-front.png,
ghostie/v7/lineup-grass.png (Kit tile) and ats9000/v1/lineup-grass.png (Kit, Ricky, 3 Ghosties, ATS: real renders).
Writes only into ../, ./ (and ./_tmp, ../crops).
Code reused: Ricky sketch library (ricky.py, via dot.py), Ricky build.py helpers (grey formula, ratio, lineup,
silhouette), ATS build.py camera calibration (metres per unit from the on-screen target).
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
from dot import *  # noqa

TMP = os.path.join(HERE, "_tmp")
CROPS = os.path.join(OUT, "crops")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CROPS, exist_ok=True)

KIT_FRONT = os.path.join(ASSETS, "kit", "turn-front.png")
RICKY_FRONT = os.path.join(ASSETS, "ricky", "v1", "turn-front.png")
GH_FRONT = os.path.join(ASSETS, "ghostie", "v7", "turn-front.png")
ATS_FRONT = os.path.join(ASSETS, "ats9000", "v1", "turn-front.png")
GH_LINEUP = os.path.join(ASSETS, "ghostie", "v7", "lineup-grass.png")    # Kit alone: tile crop
FAM_LINEUP = os.path.join(ASSETS, "ats9000", "v1", "lineup-grass.png")   # Kit, Ricky, 3 Ghosties, ATS
LINEUP_BOX = (640, 400, 960, 640)
DOT_SPOT = (778, 534)          # free grass between the Ghosties, the ATS and Ricky (feet centre, full frame)
KIT_TILE = "80x96+847+410"     # Kit in ghostie/v7/lineup-grass.png (as the Ricky sheet)

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # kit/ingame.html L156: fov 26, 26 m, 900 px = 74.97
OUTLINE = 1.6
KIT_PX = 75.0                  # ricky/v1/measure.md: Kit 75 px in the lineup (same method for every character)
TARGET = 0.9 * KIT_PX          # brief.md L25: about 0.9 x Kit on screen = 67.5 px
CAM = (20.0, 42.0)
CAM_NET = (5.0, 42.0)          # lineup characters turn 15 deg to the camera (ricky/v1/ingame.html L303)
KIT_M = 0.977                  # kit/build_report.json

# ---- camera calibration (ATS method): metres per unit so the estimate is 67.5 px tall facing the camera
_b = pbounds(model(), *CAM_NET)
HU = _b[3] - _b[1]
M_PER_U = (TARGET - 2 * OUTLINE) / (PX_PER_M * HU)
GS = PX_PER_M * M_PER_U
H_M = (GROUND - LM["bun_top"]) * M_PER_U
GREEN = "#B5D67A"
RED = "#E0533D"


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


def arrow(x0, y, x1):
    return (f'<path d="M{x0},{y} L{x1 - 12},{y}" fill="none" stroke="{NOTE}" stroke-width="4"/>'
            f'<path d="M{x1 - 12},{y - 8} L{x1},{y} L{x1 - 12},{y + 8} Z" fill="{NOTE}" stroke="none"/>')


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


def alpha_bbox(png):
    a = np.asarray(Image.open(png).convert("RGBA"))[..., 3]
    ys, xs = np.nonzero(a > 40)
    return xs.min(), ys.min(), xs.max(), ys.max()


# ============================================================ game camera
def cam_png(name, opts=None, w=80, h=96, bg=None, yaw=CAM_NET[0], mark=None, xf=None):
    """Dot at the game camera, 1x pixels, feet centre at (w/2, h-14). Returns (1x path, x3 path)."""
    m = model(opts)
    ox, oy = w / 2, h - 14
    inner = shadow(ox, oy + 2, 19, 6, 0.22) if bg else ""
    inner += render(m, yaw, CAM[1], GS, ox, oy, OUTLINE, xf=xf)
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


def measure_px(opts=None, yaw=CAM_NET[0]):
    one, _ = cam_png(f"measure-{int(yaw)}", opts, 120, 120, None, yaw)
    x0, y0, x1, y1 = alpha_bbox(one)
    return y1 - y0 + 1, x1 - x0 + 1


def kit_tile(name):
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(GH_LINEUP, "-crop", KIT_TILE, "+repage", one)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def lineup(name="lineup", grey=False):
    """ATS v1 lineup crop (Kit, Ricky, 3 Ghosties, ATS: real renders) with the Dot estimate on free grass."""
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(FAM_LINEUP).crop(LINEUP_BOX).save(base)
    w, h = 100, 100
    one, _ = cam_png(f"{name}-dot", None, w, h)
    shp = write(f"{name}-shadow.svg", w, h, shadow(w / 2, h - 13, 21, 7, 0.28))
    shpng = os.path.join(TMP, f"{name}-shadow.png")
    sh("-background", "none", shp, shpng)
    x = DOT_SPOT[0] - LINEUP_BOX[0] - w / 2
    y = DOT_SPOT[1] - LINEUP_BOX[1] - (h - 14)
    comp(base, shpng, x, y)
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
    ("1 pear, top-back bun, folded", {}),
    ("2 capsule, top bun (BMGD)", {"body": BODY_CAPSULE, "bun": "top", "arms": "sides"}),
    ("3 tea cosy, nape bun, glasses", {"body": BODY_BELL, "bun": "nape", "glasses": True, "legs": False}),
    ("4 egg, double buns", {"body": BODY_EGG, "bun": "double", "arms": "sides"}),
    ("5 box coat, top bun, glasses", {"body": BODY_BOX, "bun": "top", "glasses": True, "arms": "sides"}),
    ("6 pear, nape bun, arms out", {"bun": "nape", "arms": "sides"}),
    ("7 pear, big head, glasses", {"head_s": 1.1, "glasses": True, "bun": "top"}),
    ("8 capsule, small head, folded", {"body": BODY_CAPSULE, "head_s": 0.9}),
    ("9 tea cosy, top-back bun", {"body": BODY_BELL, "legs": False}),
    ("10 egg, top bun, glasses", {"body": BODY_EGG, "bun": "top", "glasses": True}),
]
DIRS = [
    ("A. COTTAGE LOAF (pick)", {}, ["Big round head on a soft pear: the widest", "point is the belly, so she reads short and",
                                    "round, and still a toy pawn like Kit and", "Ricky. Folded hands = calm, kind, listening.",
                                    "Top-back bun clears the eyes and makes a", "clear bump on the 64 px silhouette."]),
    ("B. CAPSULE + BUN (BMGD hint)", {"body": BODY_CAPSULE, "bun": "top", "arms": "sides"},
     ["The hint as given. At the game camera it", "reads as 'a purple Kit with a bun': the", "same capsule as Kit, so only colour",
      "tells them apart. Arms out make it stiff."]),
    ("C. TEA COSY", {"body": BODY_BELL, "bun": "nape", "glasses": True, "legs": False},
     ["A bell to the ground, glasses, low bun.", "Very 'granny', but no feet breaks the pawn", "family, the nape bun hides behind the head",
      "at pitch 42, and the glasses ring the eyes", "at 1x (Ricky's fringe lesson)."]),
]


def explore():
    W, H = 2700, 1820
    i = [text(30, 50, "GHOSTED: Auntie Dot, explore (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: local references, 10 rough thumbnails, 3 directions, one pick. "
              "Hand-drawn Bezier half outlines lifted to round bodies (Ricky sketch library); palette rows only.", 18)]
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, the locked family; no web)", 20, "bold", NOTE))
    for k, lab in enumerate(["Kit v5 (hero)", "Ricky v1", "Ghostie v7", "ATS-9000 v1"]):
        i.append(text(30 + k * 235, ry + 330, lab, 15))
    i.append(text(1000, ry + 345, "ATS v1 lineup at the game camera (x2): the family on grass", 15))
    ty = 520
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x3, 26 m, "
                  "pitch 42, net yaw 5), at 0.9 x Kit.", 20, "bold", NOTE))
    tw = 254
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 6, ty + 34, lab, 14, "bold"))
        i.append(render(model(o), 0, 0, 0.66, x + tw / 2, ty + 270, 2.2, mark_scale=0.8))
        i.append(shadow(x + tw / 2, ty + 272, 56, 6))
    dy = 1160
    i.append(text(30, dy, "DIRECTIONS (3), developed: front, 3/4, back; then the game camera (x3): Dot left, "
                  "Kit right (real v7 render)", 20, "bold", NOTE))
    dw = 880
    for n, (lab, o, notes) in enumerate(DIRS):
        x = 30 + n * dw
        i.append(text(x + 10, dy + 40, lab, 20, "bold", NOTE if n == 0 else INK))
        for k, yw in enumerate((0, 35, 180)):
            i.append(render(model(o), yw, 0, 0.72, x + 70 + k * 125, dy + 340, 2.4, mark_scale=0.9))
            i.append(shadow(x + 70 + k * 125, dy + 342, 60, 7))
        for k, ln in enumerate(notes):
            i.append(text(x + 10, dy + 400 + k * 22, ln, 16))
        if n == 0:
            i.append(frame(x, dy + 12, x + dw - 20, dy + 545, NOTE, 4))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    for k, src in enumerate([KIT_FRONT, RICKY_FRONT, GH_FRONT, ATS_FRONT]):
        t = os.path.join(TMP, f"ref-{k}.png")
        sh(src, "-resize", "x290", t)
        comp(png, t, 30 + k * 235, ry + 25)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(FAM_LINEUP, "-crop", "400x220+600+405", "+repage", "-filter", "point", "-resize", "150%", lu)
    comp(png, lu, 1000, ry + 10)
    for n, (lab, o) in enumerate(THUMBS):
        _, x3 = cam_png(f"ex-thumb-{n}", o, 76, 92, GREEN)
        comp(png, x3, 30 + n * tw + 13, ty + 290)
    _, kit3 = kit_tile("ex-kit")
    for n, (lab, o, notes) in enumerate(DIRS):
        _, x3 = cam_png(f"ex-dir-{n}", o, 80, 96, GREEN)
        comp(png, x3, 30 + n * dw + 395, dy + 60)
        comp(png, kit3, 30 + n * dw + 625, dy + 60)
    return png


# ============================================================ BODY MAP
def surf_pt(x, y, half, depth, out=0.0):
    prof = profile(half)
    X = x - 150
    r = r_at(prof, y)
    X = max(-r, min(r, X))
    z = r * depth * math.sqrt(max(1 - (X / max(r, 1e-3)) ** 2, 0)) + out
    return (X, GROUND - y, z)


def lm3d():
    """3D landmark and attachment points (X, H, Z), from the same numbers as dot.model()."""
    bp = profile(BODY_PEAR)
    cxs = LM["cup_x"][1] - 150
    czs = r_at(bp, LM["cups"]) * 0.85 * math.sqrt(max(1 - (cxs / r_at(bp, LM["cups"])) ** 2, 0)) + 5.0
    return {
        "eye_l": (surf_pt(LM["eye_x"][0], LM["eye"], HEAD_HALF, 0.92), NOTE),
        "eye_r": (surf_pt(LM["eye_x"][1], LM["eye"], HEAD_HALF, 0.92), NOTE),
        "mouth": (surf_pt(150, 152, HEAD_HALF, 0.92), NOTE),
        "hairline": (surf_pt(150, LM["hairline"], CAP_HALF, 0.92), NOTE),
        "bun": ((0, GROUND - 60, -18), RED),
        "ear_l": ((-56, GROUND - LM["eye"] - 2, -4), NOTE),
        "ear_r": ((56, GROUND - LM["eye"] - 2, -4), NOTE),
        "band_back": ((0, GROUND - LM["neck"] - 3, -33), RED),
        "cup_l": ((-cxs, GROUND - LM["cups"], czs), RED),
        "cup_r": ((cxs, GROUND - LM["cups"], czs), RED),
        "button": (surf_pt(150, 214, BODY_PEAR, 0.85), NOTE),
        "hands": (surf_pt(150, LM["hands"], BODY_PEAR, 0.85, 9), NOTE),
        "hem": (surf_pt(150, LM["hem"] - 2, BODY_PEAR, 0.85), NOTE),
        "feet": ((0, GROUND - 332, 8), NOTE),
    }


def gamecam_marks():
    P, _ = cam(*CAM_NET)
    return {k: (P(q)[0] * GS, P(q)[1] * GS, c) for k, (q, c) in lm3d().items()}


def hair_gap():
    """At the game camera (net yaw 5): the lowest hair point in each eye column vs the eye top, in px (1x)."""
    P, _ = cam(*CAM_NET)
    res = {}
    for k, ex in (("left", LM["eye_x"][0]), ("right", LM["eye_x"][1])):
        # the hairline mark is a front arch; find its y at the eye column
        pts = [(x, y) for x, y in path_points(HAIRLINE, 40)]
        hy = min(pts, key=lambda p: abs(p[0] - ex))[1]
        hair_v = P(surf_pt(ex, hy, CAP_HALF, 0.92))[1] * GS
        eye_top_v = P(surf_pt(ex, LM["eye"] - 8.5, HEAD_HALF, 0.92))[1] * GS
        res[k] = (round(hy, 1), round(eye_top_v - hair_v, 2))
    return res


def body_map():
    W, H = 2600, 2080
    i = [text(30, 50, "GHOSTED: Auntie Dot body map v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions in head-heights, landmarks, attachment points (bun, "
              "headset round the NECK, card in hand), and a check at the game camera (26 m, pitch 42).", 18)]
    s = 2.3
    fx, gy0 = 380, 120
    gy = lambda y: gy0 + y * s
    fxx = lambda x: fx + (x - 150) * s
    i.append(text(30, 125, "A. FRONT (upright, symmetric)", 20, "bold", NOTE))
    rows = [("top of bun", LM["bun_top"]), ("top of hair", LM["hair_top"]), ("hairline (centre)", LM["hairline"]),
            ("temple hairline", LM["temple"]), ("eye line = ear points", LM["eye"]), ("mouth (smile)", 152),
            ("chin", LM["chin"]), ("neck line = headset band", LM["neck"]), ("cup centres (collarbones)", LM["cups"]),
            ("shoulder joint (arm root)", LM["shoulder"]), ("folded hands", LM["hands"]), ("belly (widest)", LM["belly"]),
            ("cardigan hem", LM["hem"]), ("sole", LM["sole"])]
    x_end = fx + 190 * s
    for lab, y in rows:
        i.append(guide(fx - 190 * s / 2.3 - 30, x_end, gy(y)))
        i.append(text(x_end + 8, gy(y) + 5, f"{lab}  y {y}", 15,
                      "bold" if ("eye" in lab or "band" in lab or "cup" in lab) else "normal", NOTE))
    i.append(shadow(fx, gy(342), 120, 12))
    i.append(render(model(), 0, 0, s, fx, gy(GROUND), 5))
    for x in LM["ear_x"]:
        i.append(dot(fxx(x), gy(LM["eye"] + 2), 7))
    for x in LM["cup_x"]:
        i.append(dot(fxx(x), gy(LM["cups"]), 7, RED))
    i.append(dot(fxx(150), gy(LM["neck"]), 7, RED))
    i.append(dot(fxx(150), gy(60), 7, RED))
    for x in LM["shoulder_x"]:
        i.append(dot(fxx(x), gy(LM["shoulder"]), 7, RED))
    x0, y0, x1, y1 = LM["mouth"]
    i.append(f'<path d="M{fxx(x0)},{gy(y0)} L{fxx(x1)},{gy(y0)} L{fxx(x1)},{gy(y1)} L{fxx(x0)},{gy(y1)} Z" '
             f'fill="none" stroke="{NOTE}" stroke-width="3" stroke-dasharray="8,6"/>')
    rx = 50
    hh = LM["chin"] - LM["bun_top"]
    ticks = [LM["bun_top"], LM["chin"], LM["chin"] + hh, LM["sole"]]
    i.append(f'<path d="M{rx},{gy(ticks[0])} L{rx},{gy(ticks[-1])}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    for t in ticks:
        i.append(f'<path d="M{rx - 10},{gy(t)} L{rx + 10},{gy(t)}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    nh = (LM["sole"] - LM["bun_top"]) / hh
    i.append(text(rx + 14, gy(LM["bun_top"] + hh / 2), "1 head", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["chin"] + hh / 2), "2", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["sole"] - 4), f"{nh:.2f}", 15, "bold", NOTE))

    # B. side
    sx = 1250
    i.append(text(sx - 150, 125, "B. SIDE (same lines)", 20, "bold", NOTE))
    for lab, y in rows:
        i.append(guide(sx - 150, sx + 160, gy(y), 0.35))
    i.append(shadow(sx, gy(342), 80, 10))
    i.append(render(model(), 90, 0, s, sx, gy(GROUND), 5))

    # C. top view, head lifted off
    tx, tyc = 1900, 1210
    i.append(text(tx - 280, 960, "C. TOP VIEW, head lifted off:", 20, "bold", NOTE))
    i.append(text(tx - 280, 984, "band behind the neck, a cup on each collarbone", 16))
    i.append(render(model({"no_head": True}), 0, 90, 1.6, tx, tyc, 4))
    i.append(text(tx - 40, tyc + 200, "front (face side)", 15, "normal", NOTE))
    i.append(text(tx - 20, tyc - 150, "back", 15, "normal", NOTE))

    # D. notes
    nx = 1620
    notes = [("PROPORTIONS (head = top of bun to chin = 132 units)", True),
             (f"Whole figure 300 units = {nh:.2f} heads (Kit 2.71, Ricky 2.67):", False),
             ("  shorter and rounder, same toy-pawn family.", False),
             (f"Size: 0.9 x Kit on screen = {TARGET:.1f} px; estimate {H_M:.2f} m (1 u = {M_PER_U * 1000:.2f} mm).", False),
             ("Head 112 wide (skull 98 tall); body: a pear, 32 wide at", False),
             ("  the neck, 164 at the belly (y 280); legs 18; shoes 16.", False),
             ("", False),
             ("LANDMARKS", True),
             ("Hairline: soft waves, y 88 at the centre, y 112 at the", False),
             ("  temples; strands swept up into the top-back bun.", False),
             ("Eye line y 126; eyes x 132 / 168 (ink ovals + glint).", False),
             ("Ears: on the eye line at the head sides (x 93 / 207),", False),
             ("  in the open: the headset is NOT on them.", False),
             ("Mouth zone x 134-166, y 140-160: warm smile; opens", False),
             ("  to talk. No creases (noise at 1x).", False),
             ("Neck: short, chin y 172 to the body top y 180.", False),
             ("Shoulder joint (red): x 90 / 210, y 206. Continuous", False),
             ("  sleeve from the body, then the hand ball.", False),
             ("Hands: folded on the belly at y 262 (rest pose).", False),
             ("", False),
             ("ATTACHMENT POINTS (red)", True),
             ("Bun: centre (0, y 60, 18 behind the head centre).", False),
             ("Headset band: round the NECK at the neck line y 180,", False),
             ("  behind the neck (back point y 183), on the shoulders.", False),
             ("Headset cups: ONE ON EACH COLLARBONE, at the band", False),
             ("  ends: centre x 117 / 183, y 194, faces forward.", False),
             ("  No mic. Faded row 27 (the Ghostie accessory colour).", False),
             ("Skill card: in her right hand (talk / card poses).", False)]
    for k, (ln, b) in enumerate(notes):
        i.append(text(nx, 150 + k * 25, ln, 17, "bold" if b else "normal", NOTE if b else INK))

    # E. game camera
    E = (30, 1060)
    i.append(text(E[0], E[1], "E. GAME CAMERA CHECK (x3, 1x below). Left: Dot estimate. Middle: landmark dots (blue: eyes, "
                  "mouth, hairline, ears, button, hands, hem, feet;", 18, "bold", NOTE))
    i.append(text(E[0], E[1] + 24, "red: bun, band back, cups). Right: Kit, real v7 render. Net yaw 5 (lineup facing), "
                  "pitch 42.", 18, "bold", NOTE))
    gap = hair_gap()
    hm = gamecam_marks()
    lines = [f"Hairline above the eye top at 1x: left {gap['left'][1]:.1f} px, right {gap['right'][1]:.1f} px "
             f"(the hair never crosses the eyes).",
             f"Bun centre {hm['eye_l'][1] - hm['bun'][1]:.1f} px above the eyes; it sits on the crown, behind.",
             f"Cups {hm['cup_l'][1] - hm['eye_l'][1]:.1f} px under the eyes, {hm['cup_l'][1] - hm['mouth'][1]:.1f} px "
             f"under the mouth: under the chin, not hidden by it.",
             f"Band back point: {hm['eye_l'][1] - hm['band_back'][1]:.1f} px above the eye line on screen, so the head "
             f"hides it (as it hides a real neck band). The band sides and the cups show.",
             "Read: a white bun on a white dome, a peach face with two dots and a smile, two lilac discs",
             "under the chin, a purple pear. The lilac reads as a ring at the neck (brief L24)."]
    for k, ln in enumerate(lines):
        i.append(text(E[0], E[1] + 420 + k * 24, ln, 16, "bold" if k == 4 else "normal"))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    def mk(ox, oy):
        return "".join(f'<ellipse cx="{ox + u:.2f}" cy="{oy + v:.2f}" rx="0.9" ry="0.9" fill="{c}" stroke="none"/>'
                       for u, v, c in hm.values())
    _, x3 = cam_png("bm-cam", None, 80, 96, GREEN)
    _, x3m = cam_png("bm-cam-mark", None, 80, 96, GREEN, mark=mk)
    k1, kit3 = kit_tile("bm-kit")
    one_t, _ = cam_png("bm-cam-talk", {"arms": "talk", "face": "talk", "head_tilt": 8}, 80, 96, GREEN)
    comp(png, x3, E[0], E[1] + 50)
    comp(png, x3m, E[0] + 260, E[1] + 50)
    comp(png, kit3, E[0] + 520, E[1] + 50)
    one, _ = cam_png("bm-cam", None, 80, 96, GREEN)
    comp(png, one, E[0] + 800, E[1] + 50)
    comp(png, k1, E[0] + 890, E[1] + 50)
    info = {k: (round(u, 1), round(v, 1)) for k, (u, v, c) in hm.items()}
    json.dump({"gamecam_marks_px_from_feet_origin": info, "hair_gap_px": gap, "m_per_u": M_PER_U, "height_m": H_M,
               "target_px": TARGET}, open(os.path.join(TMP, "bodymap.json"), "w"), indent=1)
    return png, info, gap


# ============================================================ SHEET
PAL = [(11, "cardigan dress, sleeves"), (15, "skin: head, hands, legs"), (23, "hair + bun, buttons, eye glint"),
       (27, "the OLD HEADSET round the neck (faded)"), (5, "shoes"), (22, "ink: outline, eyes, brows, mouth"),
       (13, "props: Copium mark on the Skill card"), (24, "props: Skill card edge (3D only)")]


def silhouette(name, yaw, px=64):
    m = model()
    x0, y0, x1, y1 = pbounds(m, yaw, 0)
    s = (px - 2) / (y1 - y0)
    w = int(math.ceil((x1 - x0) * s)) + 4
    inner = render(m, yaw, 0, s, -x0 * s + 2, -y0 * s + 1, 0.01, mono=INK)
    sv = write(f"{name}.svg", w, px, inner, "#FFFFFF")
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(sv, one)
    x4 = os.path.join(TMP, f"{name}-x4.png")
    sh(one, "-filter", "point", "-resize", "400%", "-bordercolor", INK, "-border", "1", x4)
    return one, x4


def head_crop(name, opts, s=2.0):
    """Face close-up: the whole model rendered, the SVG viewport is the head box."""
    w, h = int(150 * s), int(165 * s)
    ox, oy = w / 2, (GROUND - 30) * s
    sv = write(f"{name}.svg", w, h, render(model(opts), 0, 0, s, ox, oy, 4), CREAM)
    png = os.path.join(TMP, f"{name}.png")
    sh(sv, png)
    return png


def sway_xf(a):
    return rot_z(a, (0.0, 0.0, 0.0))


def sheet():
    W, H = 2900, 2620
    i = [text(30, 50, "GHOSTED: Auntie Dot model sheet v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnaround. Body map v1 landmarks. Direction A (cottage loaf). "
              "Hand-drawn Bezier half outlines lifted to round bodies; palette rows only.", 18)]
    s1, g1 = 2.0, 830
    xs = [250, 650, 1050, 1450]
    labs = ["FRONT", "3/4 (front turned to viewer-left)", "SIDE (facing viewer-left)", "BACK"]
    rows = [("top of bun", LM["bun_top"]), ("hairline (centre)", LM["hairline"]), ("eye line = ear points", LM["eye"]),
            ("neck line = headset band", LM["neck"]), ("shoulder joint", LM["shoulder"]), ("belly", LM["belly"]),
            ("hem", LM["hem"]), ("sole", LM["sole"])]
    for lab, y in rows:
        yy = g1 - (GROUND - y) * s1
        i.append(guide(60, 1660, yy, 0.45))
        i.append(text(1670, yy + 5, lab, 15, "bold" if ("eye" in lab or "band" in lab) else "normal", NOTE))
    for x, lab, yw in zip(xs, labs, (0, 35, 90, 180)):
        i.append(text(x - 170, 125, lab, 17, "bold"))
        i.append(shadow(x, g1 + 6, 130 if yw != 90 else 90, 12))
        i.append(render(model(), yw, 0, s1, x, g1, 4.5))
    px_ = 1990
    i.append(text(px_, 125, "PALETTE (existing rows only, seats/lena-park.md)", 17, "bold"))
    for k, (r, use) in enumerate(PAL):
        y = 145 + k * 40
        i.append(f'<path d="M{px_},{y} L{px_ + 30},{y} L{px_ + 30},{y + 30} L{px_},{y + 30} Z" fill="{ROW[r]}" '
                 f'stroke="{INK}" stroke-width="2"/>')
        i.append(text(px_ + 42, y + 21, f"{r} {ROW[r]}  {use}", 16))
    i.append(text(px_, 145 + len(PAL) * 40 + 10, f"Shade: base x {SHADE_K} (neutral grey multiplier).", 16))
    rules = ["SHAPE RULES",
             f"- Toy pawn, cottage loaf: big round head on a",
             f"  pear; 2.27 heads with the bun. 0.9 x Kit on screen.",
             "- Hair: a soft wavy hairline, strands swept up",
             "  into a top-back bun. Nothing crosses the eyes.",
             "- The OLD headset hangs round her NECK: band",
             "  behind the neck on the shoulders, a cup on",
             "  each collarbone. Never on the ears. No mic.",
             "- Cardigan dress: placket, 2 buttons, 2 pockets.",
             "- Rest pose: hands folded on the belly.",
             "- Joins: continuous sleeve out of the body,",
             "  then the hand ball (3-mesh build, notes)."]
    for k, ln in enumerate(rules):
        i.append(text(px_, 520 + k * 23, ln, 16, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))

    # ---- row 2: motion
    y2, g2, s2 = 950, 1480, 1.3
    i.append(text(30, y2, "IDLE SWAY (front): rock on the feet, +-4 deg; the head lags 2 deg", 18, "bold", NOTE))
    i.append(text(30, y2 + 24, "slow, about 2.5 s a cycle; the feet stay planted", 14))
    for k, a in enumerate((-4, 0, 4)):
        x = 150 + k * 250
        i.append(shadow(x, g2 + 5, 80, 9))
        i.append(render(model({"head_tilt": -a / 2}), 0, 0, s2, x, g2, 3.5, xf=sway_xf(a)))
        i.append(f'<path d="M{x},{g2 + 10} L{x},{g2 - 330}" fill="none" stroke="{NOTE}" stroke-width="1.5" '
                 f'stroke-dasharray="6,5"/>')
    tx_ = 820
    i.append(text(tx_, y2, "TALK BEAT: head tilts 8 deg, her right hand comes up, mouth opens", 18, "bold", NOTE))
    i.append(text(tx_, y2 + 24, "(red: shoulder, elbow, wrist; the other hand stays on the belly)", 14))
    talk = {"arms": "talk", "face": "talk", "head_tilt": 8}
    for k, yw in enumerate((0, 35)):
        x = tx_ + 170 + k * 300
        i.append(shadow(x, g2 + 5, 85, 9))
        i.append(render(model(talk), yw, 0, s2, x, g2, 3.5))
    for (X, Hh) in [(-52, GROUND - LM["shoulder"]), (-96, GROUND - 236), (-96, GROUND - 196)]:
        i.append(dot(tx_ + 170 + X * s2, g2 - Hh * s2, 6, RED))
    cx_ = 1640
    i.append(text(cx_, y2, "HAND OVER A SKILL CARD: her right arm reaches forward", 18, "bold", NOTE))
    i.append(text(cx_, y2 + 24, "card in the hand, face to the player; small lean (2 deg)", 14))
    card = {"arms": "card"}
    for k, yw in enumerate((0, 35)):
        x = cx_ + 170 + k * 300
        i.append(shadow(x, g2 + 5, 85, 9))
        i.append(render(model(card), yw, 0, s2, x, g2, 3.5, xf=rot_x(2)))
    ex_ = 2270
    i.append(text(ex_, y2, "EXPRESSIONS (front)", 18, "bold", NOTE))
    for k, lab in enumerate(["rest: warm smile", "talk", "happy (the card)"]):
        i.append(text(ex_ + k * 205, y2 + 60, lab, 15, "bold"))

    # ---- row 3: silhouette, lineup, game camera
    y3 = 1620
    i.append(text(30, y3, "64 px SILHOUETTE (front, 3/4; 1x and x4)", 18, "bold", NOTE))
    i.append(text(700, y3, "LINEUP AT THE GAME CAMERA (x2): Dot estimate on the real ATS v1 grass", 18, "bold", NOTE))
    i.append(text(700, y3 + 22, "with Kit, Ricky, 3 Ghosties and the ATS. Colour, then grey (Lena's formula).", 15))
    i.append(text(2120, y3, "GAME CAMERA NEXT TO KIT (x3): rest, talk, Kit", 18, "bold", NOTE))
    i.append(text(2120, y3 + 22, "grey below; 1x at the bottom", 15))
    vals = [f"cardigan 11 vs grass 1: {ratio(ROW[11], '#B5D67A'):.2f}:1",
            f"cardigan 11 vs Ricky suit 17: {ratio(ROW[11], '#2E2C3D'):.2f}:1; vs Kit shirt 14: "
            f"{ratio(ROW[11], '#2F6FDB'):.2f}:1",
            f"headset 27 vs cardigan 11: {ratio(ROW[27], ROW[11]):.2f}:1 (the lilac ring reads)",
            f"hair 23 vs skin 15: {ratio(ROW[23], ROW[15]):.2f}:1 (low: the hairline carries an ink line)",
            f"hair 23 vs Ghostie body 16: {ratio(ROW[23], '#F8F4EA'):.2f}:1 (same white family: see notes)",
            f"skin 15 vs cardigan 11: {ratio(ROW[15], ROW[11]):.2f}:1"]
    for k, v in enumerate(vals):
        i.append(text(700, y3 + 560 + k * 26, v, 17))
    i.append(text(700, y3 + 560 + 6 * 26 + 10, "In grey: a light dome with a light bun on a dark pear; the face is the "
                  "mid tone between. Kit is mid-grey, Ricky near-black, the ATS mid, the Ghosties white.", 17, "bold"))
    hpx, wpx = measure_px()
    sz = ["SIZE (estimate; Viet's blockout sets it):",
          f"Target 0.9 x Kit 75 px = {TARGET:.1f} px tall.",
          f"This tile: {hpx} x {wpx} px facing the camera.",
          f"Calibrated: 1 u = {M_PER_U * 1000:.2f} mm, so about {H_M:.2f} m",
          f"top of bun to sole (Kit is {KIT_M} m)."]
    for k, ln in enumerate(sz):
        i.append(text(2120, y3 + 780 + k * 22, ln, 15, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))
    svg = write("dot-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "dot-sheet.png")
    sh(svg, png)

    for k, o in enumerate([{}, {"face": "talk"}, {"face": "happy"}]):
        hc = head_crop(f"face-{k}", o, 1.3)
        comp(png, hc, ex_ + k * 205, y2 + 80)
    s1x, s4 = silhouette("sil-front", 0)
    q1x, q4 = silhouette("sil-34", 35)
    comp(png, s1x, 40, y3 + 30)
    comp(png, q1x, 130, y3 + 30)
    comp(png, s4, 40, y3 + 120)
    comp(png, q4, 360, y3 + 120)
    sh(s1x, os.path.join(OUT, "silhouette-64.png"))
    lc1, lc2 = lineup("lineup-colour")
    lg1, lg2 = lineup("lineup-grey", grey=True)
    comp(png, lc2, 700, y3 + 50)
    comp(png, lg2, 1380, y3 + 50)
    one, x3 = cam_png("sheet-cam", None, 80, 96, GREEN)
    onet, x3t = cam_png("sheet-cam-talk", talk, 80, 96, GREEN)
    k1, kit3 = kit_tile("sheet-kit")
    comp(png, x3, 2120, y3 + 40)
    comp(png, x3t, 2370, y3 + 40)
    comp(png, kit3, 2620, y3 + 40)
    for src, x in ((x3, 2120), (x3t, 2370), (kit3, 2620)):
        g = src.replace(".png", "-grey.png")
        grey_img(src, g)
        comp(png, g, x, y3 + 340)
    comp(png, one, 2130, y3 + 645)
    comp(png, onet, 2230, y3 + 645)
    comp(png, k1, 2330, y3 + 645)
    return png, (hpx, wpx)


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    print(f"M_PER_U {M_PER_U:.5f} m, height {H_M:.3f} m, GS {GS:.4f}")
    if "explore" in what:
        print(explore())
    if "bodymap" in what:
        print(body_map())
    if "sheet" in what:
        print(sheet())
