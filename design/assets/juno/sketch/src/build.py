"""Build explore.png, body-map.png, juno-sheet.png and silhouette-64.png for Juno the barista.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
Reads only: kit/turn-front.png, ricky/v1/turn-front.png, ghostie/v7/turn-front.png, ats9000/v1/turn-front.png,
auntie-dot/v1/turn-front.png, brett/v1/hero.png, ghostie/v7/lineup-grass.png (Kit tile), and the real renders
brett/v1/lineup-grass.png and brett/v1/lineup-path.png (Dot v1's scene with Brett: Kit, Ricky, 3 Ghosties, the ATS,
Dot and Brett).
Writes only into ../, ./ (and ./_tmp, ../crops).
Code reused: Ricky sketch library (ricky.py), Dot render with per-part poses (dot.py), Brett build.py helpers (grey
formula, ratio, camera calibration, tiles, lineup, silhouette, hair gap), the ATS calibration method.
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
from juno import *  # noqa
from ricky import lift_mark  # noqa

TMP = os.path.join(HERE, "_tmp")
CROPS = os.path.join(OUT, "crops")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CROPS, exist_ok=True)

KIT_FRONT = os.path.join(ASSETS, "kit", "turn-front.png")
RICKY_FRONT = os.path.join(ASSETS, "ricky", "v1", "turn-front.png")
GH_FRONT = os.path.join(ASSETS, "ghostie", "v7", "turn-front.png")
ATS_FRONT = os.path.join(ASSETS, "ats9000", "v1", "turn-front.png")
DOT_FRONT = os.path.join(ASSETS, "auntie-dot", "v1", "turn-front.png")
BRETT_FRONT = os.path.join(ASSETS, "brett", "v1", "hero.png")
GH_LINEUP = os.path.join(ASSETS, "ghostie", "v7", "lineup-grass.png")      # Kit alone: tile crop
LU_GRASS = os.path.join(ASSETS, "brett", "v1", "lineup-grass.png")        # the whole family on grass
LU_PATH = os.path.join(ASSETS, "brett", "v1", "lineup-path.png")          # the whole family on the path
GRASS_BOX = (600, 380, 1000, 720)
PATH_BOX = (520, 300, 1020, 640)
GRASS_SPOT = (870, 606)        # free grass right of Dot, below Ricky (feet centre, full frame)
PATH_SPOT = (690, 560)         # free path below Dot and Brett
KIT_FEET_Y = 498               # Kit's feet (ricky/v1/measure.md: Kit y 424-498)
DOT_SPOT_Y = 661               # Dot's feet (auntie-dot/v1/measure.md); Dot is 72 px there vs 68 px at Kit's spot
KIT_TILE = "80x110+847+396"    # Kit in ghostie/v7/lineup-grass.png

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # kit/ingame.html L156: fov 26, 26 m, 900 px = 74.97
OUTLINE = 1.6
KIT_PX = 75.0                  # ricky/v1/measure.md L17
TARGET = 1.0 * KIT_PX          # brief.md L21: about 1.0 x Kit on screen (puff included)
CAM = (20.0, 42.0)
CAM_NET = (5.0, 42.0)          # lineup characters turn 15 deg to the camera (ricky/v1/ingame.html L303)
KIT_M = 0.977                  # kit/build_report.json
GREEN = "#B5D67A"              # row 1 grass
PATHC = "#EBD3A6"              # row 3 path
RED = "#E0533D"
MAG = "#C2185B"   # note colour for attachment points (not a character colour)

# ---- camera calibration (ATS / Dot / Brett method): metres per unit so the figure is 75 px facing the camera
_b = pbounds(model(), *CAM_NET)
HU = _b[3] - _b[1]
M_PER_U = (TARGET - 2 * OUTLINE) / (PX_PER_M * HU)
GS = PX_PER_M * M_PER_U
H_M = (GROUND - LM["puff_top"]) * M_PER_U
HEAD_TOP_M = (GROUND - LM["crown"]) * M_PER_U


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
def cam_png(name, opts=None, w=80, h=110, bg=None, yaw=CAM_NET[0], mark=None, xf=None, gs=None):
    """Juno at the game camera, 1x, feet centre at (w/2, h-14). Returns (1x, x3)."""
    m = model(opts)
    ox, oy = w / 2, h - 14
    inner = shadow(ox, oy + 2, 19, 6, 0.22) if bg else ""
    inner += render(m, yaw, CAM[1], gs or GS, ox, oy, OUTLINE, xf=xf)
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
    one, _ = cam_png(f"measure-{int(yaw)}", opts, 140, 140, None, yaw)
    x0, y0, x1, y1 = alpha_bbox(one)
    return y1 - y0 + 1, x1 - x0 + 1


def kit_tile(name):
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(GH_LINEUP, "-crop", KIT_TILE, "+repage", one)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def persp(feet_y):
    """Scale at a feet row, from Dot's two measures (72 px at y 661 vs 68 px at Kit's y 498)."""
    return 1 + (72 / 68 - 1) * (feet_y - KIT_FEET_Y) / (DOT_SPOT_Y - KIT_FEET_Y)


def lineup(name, src, box, spot, grey=False, opts=None):
    """A real Brett v1 lineup render (the whole family) with the Juno estimate on a free spot."""
    k = persp(spot[1])
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(src).crop(box).save(base)
    w, h = 110, 120
    one, _ = cam_png(f"{name}-juno", opts, w, h, gs=GS * k)
    shp = write(f"{name}-shadow.svg", w, h, shadow(w / 2, h - 13, 20, 7, 0.28))
    shpng = os.path.join(TMP, f"{name}-shadow.png")
    sh("-background", "none", shp, shpng)
    x = spot[0] - box[0] - w / 2
    y = spot[1] - box[1] - (h - 14)
    comp(base, shpng, x, y)
    comp(base, one, x, y)
    out1 = os.path.join(TMP, f"{name}-1x.png")
    sh(base, out1)
    if grey:
        grey_img(out1, out1)
    out2 = os.path.join(TMP, f"{name}-x2.png")
    sh(out1, "-filter", "point", "-resize", "200%", out2)
    return out1, out2, k


# ============================================================ EXPLORE
THUMBS = [
    ("1 hourglass, puff, bib apron", {}),
    ("2 capsule + apron box (BMGD)", {"body": BODY_CAPSULE, "hair": "crop", "apron": "bib",
                                      "colors": {"top": ROW[23], "apron": ROW[7]}}),
    ("3 column, long apron, scarf", {"body": BODY_COLUMN, "hair": "scarf", "arms": "sides"}),
    ("4 mug: hand on hip = handle", {"body": BODY_MUG, "arms": "mughandle", "hair": "crop"}),
    ("5 hourglass, space buns", {"hair": "buns"}),
    ("6 teardrop, low bun", {"body": BODY_TEAR, "hair": "back"}),
    ("7 hourglass, all apricot", {"colors": {"top": ROW[6], "apron": ROW[23]}}),
    ("8 hourglass, red apron", {"colors": {"apron": ROW[7], "tie": ROW[5]}}),
    ("9 capsule, waist apron, puff", {"body": BODY_CAPSULE, "apron": "waist"}),
    ("10 column, cream top, puff", {"body": BODY_COLUMN, "colors": {"top": ROW[12]}, "arms": "sides"}),
]
DIRS = [
    ("A. THE HOURGLASS (pick)", {},
     ["Wide at the shoulders, pinched at the apron tie,", "wide at the hem: an hourglass, new in the family",
      "(Kit capsule, Ricky bell, Dot pear, Brett wedge).", "A dark coffee-brown top carries the read on grass",
      "and path; the apricot bib apron and a red tie, bow", "and scrunchie are the cafe rows. Hair pulled back",
      "into a high puff: a clean forehead, and a round", "dark top that no one else has."]),
    ("B. CAPSULE + APRON BOX (BMGD)", {"body": BODY_CAPSULE, "hair": "crop",
                                       "colors": {"top": ROW[23], "apron": ROW[7]}},
     ["The hint as given: a capsule with a red apron box", "on a light top. At the game camera it is Kit's",
      "capsule with Brett's red on the front and white", "sleeves: it reads as a Brett cousin."]),
    ("C. COLUMN + HEAD SCARF", {"body": BODY_COLUMN, "hair": "scarf", "arms": "sides"},
     ["A tall slim column with a long apron, a red", "head scarf knotted on top. Barista-true, but at",
      "pitch 42 the scarf is a red cap over the face:", "red top + brown body is Brett's split upside", "down, and the column is near the ATS box."]),
]


def explore():
    W, H = 2700, 1880
    i = [text(30, 50, "GHOSTED: Juno the barista, explore (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: local references, 10 rough thumbnails, 3 directions, one pick. "
              "Hand-drawn Bezier half outlines lifted to round bodies (Ricky sketch library); palette rows only.", 18)]
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, the locked family; no web)", 20, "bold", NOTE))
    for k, lab in enumerate(["Kit v5 (hero)", "Ricky v1", "Ghostie v7", "ATS-9000 v1", "Auntie Dot v1", "Brett v1"]):
        i.append(text(30 + k * 170, ry + 330, lab, 15))
    i.append(text(1080, ry + 345, "Brett v1 lineup at the game camera (x1.5): the whole family on grass", 15))
    ty = 520
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x3, 26 m, "
                  "pitch 42, net yaw 5), at 1.0 x Kit.", 20, "bold", NOTE))
    tw = 264
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 6, ty + 34, lab, 14, "bold"))
        i.append(render(model(o), 0, 0, 0.66, x + tw / 2, ty + 270, 2.2, mark_scale=0.8))
        i.append(shadow(x + tw / 2, ty + 272, 56, 6))
    dy = 1200
    i.append(text(30, dy, "DIRECTIONS (3), developed: front, 3/4, back; then the game camera (x3): Juno left, "
                  "Kit right (real v7 render)", 20, "bold", NOTE))
    dw = 880
    for n, (lab, o, notes) in enumerate(DIRS):
        x = 30 + n * dw
        i.append(text(x + 10, dy + 40, lab, 20, "bold", NOTE if n == 0 else INK))
        for k, yw in enumerate((0, 35, 180)):
            i.append(render(model(o), yw, 0, 0.72, x + 70 + k * 125, dy + 350, 2.4, mark_scale=0.9))
            i.append(shadow(x + 70 + k * 125, dy + 352, 60, 7))
        for k, ln in enumerate(notes):
            i.append(text(x + 10, dy + 410 + k * 22, ln, 16))
        if n == 0:
            i.append(frame(x, dy + 12, x + dw - 20, dy + 600, NOTE, 4))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    for k, src in enumerate([KIT_FRONT, RICKY_FRONT, GH_FRONT, ATS_FRONT, DOT_FRONT, BRETT_FRONT]):
        t = os.path.join(TMP, f"ref-{k}.png")
        sh(src, "-resize", "160x290", t)
        comp(png, t, 30 + k * 170, ry + 25)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(LU_GRASS, "-crop", "380x240+620+420", "+repage", "-filter", "point", "-resize", "150%", lu)
    comp(png, lu, 1080, ry - 10)
    for n, (lab, o) in enumerate(THUMBS):
        _, x3 = cam_png(f"ex-thumb-{n}", o, 80, 110, GREEN)
        comp(png, x3, 30 + n * tw + 12, ty + 290)
    _, kit3 = kit_tile("ex-kit")
    for n, (lab, o, notes) in enumerate(DIRS):
        _, x3 = cam_png(f"ex-dir-{n}", o, 80, 110, GREEN)
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
    """3D landmark and attachment points (X, H, Z), from the same numbers as juno.model()."""
    wr = r_at(profile(BODY_HG), LM["waist"]) + 1.5
    return {
        "eye_l": (surf_pt(LM["eye_x"][0], LM["eye"], CAP_HALF, 0.92), NOTE),
        "eye_r": (surf_pt(LM["eye_x"][1], LM["eye"], CAP_HALF, 0.92), NOTE),
        "mouth": (surf_pt(150, 130, CAP_HALF, 0.92), NOTE),
        "hairline": (surf_pt(150, LM["hairline"], CAP_HALF, 0.92), NOTE),
        "ear_l": ((-55, GROUND - LM["eye"] - 1, -4), NOTE),
        "ear_r": ((55, GROUND - LM["eye"] - 1, -4), NOTE),
        "puff": ((0, GROUND - LM["puff"], -18), MAG),
        "scrunchie": ((0, GROUND - 62, -14), MAG),
        "neck": (surf_pt(150, LM["neck"], BODY_HG, BODY_D), NOTE),
        "bib": (surf_pt(150, 198, BODY_HG, BODY_D), MAG),
        "tie": (surf_pt(150, LM["waist"], BODY_HG, BODY_D, 1.5), MAG),
        "bow": ((0, GROUND - LM["waist"], -wr * BODY_D - 3), MAG),
        "hand_l": ((-16, GROUND - 226, surf_pt(134, 226, BODY_HG, BODY_D)[2] + 13), NOTE),
        "hand_r": ((16, GROUND - 226, surf_pt(166, 226, BODY_HG, BODY_D)[2] + 13), NOTE),
        "cup": ((0, GROUND - 224, surf_pt(150, 226, BODY_HG, BODY_D)[2] + 15), MAG),
        "hem": (surf_pt(150, LM["hem"], BODY_HG, BODY_D), NOTE),
        "feet": ((0, GROUND - 332, 9), NOTE),
    }


def gamecam_marks():
    P, _ = cam(*CAM_NET)
    out = {}
    for k, (q, c) in lm3d().items():
        out[k] = (P(q)[0] * GS, P(q)[1] * GS, c)
    return out


def face_check(nod=0.0):
    """At the game camera (net yaw 5), in px at 1x:
    - forehead band: hairline edge to brow top, in each brow column and at the centre;
    - temples: the lowest hairline point outside the eye columns vs the eye top;
    - mouth: the closed smile below the eye bottom, and its size."""
    P0, _ = cam(*CAM_NET)
    hf = rot_x(nod, (0, GROUND - LM["chin"], 0))
    P = lambda q: P0(hf(q))
    v = lambda q: P(q)[1] * GS
    hl = path_points(HAIRLINE, 40)
    res = {"band": {}}
    for k, bx in (("left_brow", 131), ("centre", 150), ("right_brow", 169)):
        hy = min(hl, key=lambda p: abs(p[0] - bx))[1]
        brow_top = 84.0 if k != "centre" else 86.0
        res["band"][k] = round(v(surf_pt(bx, brow_top, CAP_HALF, 0.92)) - v(surf_pt(bx, hy, CAP_HALF, 0.92)), 2)
    eye_top = v(surf_pt(LM["eye_x"][0], LM["eye"] - 8.5, CAP_HALF, 0.92))
    side = [p for p in hl if p[0] < 124 or p[0] > 176]
    low = max(side, key=lambda p: p[1])
    res["temple_low_y"] = round(low[1], 1)
    res["temple_above_eye_top_px"] = round(eye_top - v(surf_pt(low[0], low[1], CAP_HALF, 0.92)), 2)
    eye_bot = v(surf_pt(LM["eye_x"][0], LM["eye"] + 8.5, CAP_HALF, 0.92))
    cap = [p for p in model() if p.name == "hair"][0]
    pts, _ = lift_mark(cap.face_host, SMILE)
    uv = [(P(q)[0] * GS, P(q)[1] * GS) for q in pts]
    us, vs = [u for u, w in uv], [w for u, w in uv]
    res["smile"] = {"w": round(max(us) - min(us), 1), "h": round(max(vs) - min(vs), 1),
                    "below_eye_px": round(min(vs) - eye_bot, 1)}
    pts, _ = lift_mark(cap.face_host, LAUGH)
    uv = [(P(q)[0] * GS, P(q)[1] * GS) for q in pts]
    us, vs = [u for u, w in uv], [w for u, w in uv]
    res["laugh"] = {"w": round(max(us) - min(us), 1), "h": round(max(vs) - min(vs), 1),
                    "below_eye_px": round(min(vs) - eye_bot, 1)}
    return res


def body_map():
    W, H = 2600, 2200
    i = [text(30, 50, "GHOSTED: Juno the barista, body map v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions in head-heights, landmarks, attachment points (puff, "
              "scrunchie, apron bib, straps, tie, bow, cup, marker), and a check at the game camera (26 m, pitch 42).",
              18)]
    s = 2.2
    fx, gy0 = 400, 160
    gy = lambda y: gy0 + y * s
    fxx = lambda x: fx + (x - 150) * s
    i.append(text(30, 125, "A. FRONT (upright, symmetric)", 20, "bold", NOTE))
    rows = [("top of the puff", LM["puff_top"]), ("top of the hair cap", LM["crown"]),
            ("hairline (centre)", LM["hairline"]), ("temple hair (lowest)", LM["temple"]),
            ("eye line = ear points", LM["eye"]), ("mouth", 130), ("chin", LM["chin"]), ("neckline", LM["neck"]),
            ("shoulder joint (arm root)", LM["shoulder"]), ("chest = bib top", LM["chest"]),
            ("cup (rest, held)", 224), ("waist = apron tie", LM["waist"]), ("hem", LM["hem"]), ("sole", LM["sole"])]
    x_end = fx + 190 * s
    for lab, y in rows:
        i.append(guide(fx - 90 * s - 20, x_end, gy(y)))
        i.append(text(x_end + 8, gy(y) + 5, f"{lab}  y {y}", 15,
                      "bold" if ("eye" in lab or "hairline" in lab or "tie" in lab) else "normal", NOTE))
    i.append(shadow(fx, gy(342), 110, 12))
    i.append(render(model(), 0, 0, s, fx, gy(GROUND), 5))
    for x in LM["ear_x"]:
        i.append(dot(fxx(x), gy(LM["eye"] + 1), 7))
    for x in LM["shoulder_x"]:
        i.append(dot(fxx(x), gy(LM["shoulder"]), 7, MAG))
    i.append(dot(fxx(150), gy(LM["puff"]), 7, MAG))
    i.append(dot(fxx(150), gy(LM["waist"]), 7, MAG))
    i.append(dot(fxx(150), gy(198), 7, MAG))
    x0, y0, x1, y1 = LM["mouth"]
    i.append(f'<path d="M{fxx(x0)},{gy(y0)} L{fxx(x1)},{gy(y0)} L{fxx(x1)},{gy(y1)} L{fxx(x0)},{gy(y1)} Z" '
             f'fill="none" stroke="{NOTE}" stroke-width="3" stroke-dasharray="8,6"/>')
    # the forehead band: a bracket from the hairline to the brows
    i.append(f'<path d="M{fxx(150)},{gy(LM["hairline"])} L{fxx(150)},{gy(86)}" fill="none" stroke="{MAG}" '
             f'stroke-width="4"/>')
    rx = 50
    hh = LM["chin"] - LM["puff_top"]
    ticks = [LM["puff_top"], LM["chin"], LM["sole"]]
    i.append(f'<path d="M{rx},{gy(ticks[0])} L{rx},{gy(ticks[-1])}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    for t in ticks:
        i.append(f'<path d="M{rx - 10},{gy(t)} L{rx + 10},{gy(t)}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    nh = (LM["sole"] - LM["puff_top"]) / hh
    i.append(text(rx + 14, gy(LM["puff_top"] + hh / 2), "1 head", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["sole"] - 4), f"{nh:.2f}", 15, "bold", NOTE))

    # B. side and back
    sx = 1180
    i.append(text(sx - 150, 125, "B. SIDE and BACK (same lines)", 20, "bold", NOTE))
    for lab, y in rows:
        i.append(guide(sx - 150, sx + 420, gy(y), 0.35))
    i.append(shadow(sx, gy(342), 80, 10))
    i.append(render(model(), 90, 0, s, sx, gy(GROUND), 5))
    i.append(shadow(sx + 300, gy(342), 90, 10))
    i.append(render(model(), 180, 0, s * 0.8, sx + 300, gy(GROUND), 4))
    i.append(dot(sx + 300, gy(LM["waist"]) - (GROUND - LM["waist"]) * s * 0.0, 0, MAG))

    # C. the cup and hands: close-ups
    cx0, cy0 = 1700, 1030
    i.append(text(cx0 - 40, cy0 - 40, "C. THE CUP and the HOLDS (front, x2.2 crops)", 20, "bold", NOTE))
    i.append(text(cx0 - 40, cy0 - 16, "Cup: tapered cylinder, 26 wide x 34 tall + lid. Ball hands hold it from "
                  "the sides or under it.", 15))
    hold_jobs = []
    for k, (o, lab) in enumerate([({}, "rest: two hands"), ({"arms": "hand"}, "hand over: on the palm"),
                                  ({"arms": "write", "face": "focus"}, "write: cup up, marker")]):
        cxk = cx0 + 60 + k * 300
        hold_jobs.append((k, o, cxk))
        i.append(text(cxk - 80, cy0 + 305, lab, 16, "bold"))

    # D. notes
    nx = 1650
    notes = [(f"PROPORTIONS (head = top of the puff to the chin = {hh} units)", True),
             (f"Whole figure {LM['sole'] - LM['puff_top']} units = {nh:.2f} heads; without the puff", False),
             (f"  {(LM['sole'] - LM['crown']) / (LM['chin'] - LM['crown']):.2f} heads (Kit 2.71, Ricky 2.67, "
              "Brett 2.53, Dot 2.27).", False),
             (f"Size: 1.0 x Kit on screen = {TARGET:.0f} px, puff included;", False),
             (f"  estimate {H_M:.2f} m to the puff top (1 u = {M_PER_U * 1000:.2f} mm).", False),
             ("Skull 108 wide, 96 tall (y 58-154). Puff 72 wide, 60 tall.", False),
             ("Body: an HOURGLASS. 120 wide at the shoulder (y 186),", False),
             ("  82 at the apron tie (y 238), 134 at the hem (y 294).", False),
             ("  Depth 0.8 of the width.", False),
             ("", False),
             ("LANDMARKS", True),
             ("Hairline: high and clean, y 64 at the centre, y 84-88 at", False),
             ("  the head sides, in front of the ears. Hair pulled back:", False),
             ("  2 strand lines ON the hair sweep up to the puff.", False),
             ("Forehead band (magenta bracket): hairline 64 to brow 86.", False),
             ("Eye line y 104; eyes x 132 / 168 (ink ovals + glint).", False),
             ("Ears: on the eye line at the head sides (x 96 / 204).", False),
             ("Mouth zone x 138-162, y 122-140. Rest: a closed smile", False),
             ("  line. Laugh / talk: Ricky style (dark fill, teeth band).", False),
             ("Neck: chin y 154, round neckline y 162.", False),
             ("Shoulder joint x 96 / 204, y 186. Sleeves rolled to the", False),
             ("  elbow (brown cuff), skin forearms, ball hands.", False),
             ("", False),
             ("ATTACHMENT POINTS (magenta)", True),
             ("Puff: centred on the head axis, top-back (centre y 40,", False),
             ("  z -18). Scrunchie: a red ring at its base, y 62.", False),
             ("Bib: from the chest y 198 to the tie, straps up to the", False),
             ("  neckline. Skirt apron: tie y 242 to the hem, red pocket.", False),
             ("Apron tie: a red cord round the waist y 238; the bow", False),
             ("  and two tails at the BACK, centred (as a real apron).", False),
             ("Cup: in her hands. Rest: centred in front of the apron,", False),
             ("  y 224. The marker: in her right hand, writing only.", False)]
    for k, (ln, b) in enumerate(notes):
        i.append(text(nx, 150 + k * 25, ln, 17, "bold" if b else "normal", NOTE if b else INK))

    # E. game camera
    E = (30, 1110)
    i.append(text(E[0], E[1], "E. GAME CAMERA CHECK (x3; 1x at right). Left: Juno estimate. Middle: landmark dots "
                  "(blue: eyes, mouth, hairline, ears, neck, hands, hem, feet;", 18, "bold", NOTE))
    i.append(text(E[0], E[1] + 24, "magenta: puff, scrunchie, bib, tie, bow (hidden at the back), cup). Right: Kit, "
                  "real v7 render. Net yaw 5 (lineup facing), pitch 42.", 18, "bold", NOTE))
    fc = face_check()
    hm = gamecam_marks()
    hpx, wpx = measure_px()
    lines = [f"Forehead band at 1x (hairline edge to brow top): {fc['band']['left_brow']:.1f} px (left brow), "
             f"{fc['band']['centre']:.1f} px (centre), {fc['band']['right_brow']:.1f} px (right brow). Rule: 4 px or more.",
             f"Temples: the lowest side hair (y {fc['temple_low_y']}) is {fc['temple_above_eye_top_px']:.1f} px ABOVE "
             f"the eye top, outside the eye columns. Nothing on the forehead, nothing down beside the eyes.",
             f"Mouth at 1x: the closed smile is {fc['smile']['w']:.1f} x {fc['smile']['h']:.1f} px, "
             f"{fc['smile']['below_eye_px']:.1f} px below the eyes; the laugh (Ricky style) "
             f"{fc['laugh']['w']:.1f} x {fc['laugh']['h']:.1f} px.",
             f"Height: {hpx} x {wpx} px (target {TARGET:.0f}, puff included). Kit is 75 px.",
             "Read: a dark round puff with a red ring, a peach face with two eyes and a small smile, a dark-brown",
             "hourglass with an apricot apron front, a red tie at the waist, a white cup in both hands, navy legs."]
    for k, ln in enumerate(lines):
        i.append(text(E[0], E[1] + 470 + k * 24, ln, 16, "bold" if k == 4 else "normal"))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    def mk(ox, oy):
        return "".join(f'<ellipse cx="{ox + u:.2f}" cy="{oy + v:.2f}" rx="0.9" ry="0.9" fill="{c}" stroke="none"/>'
                       for k, (u, v, c) in hm.items() if k != "bow")
    one, x3 = cam_png("bm-cam", None, 80, 110, GREEN)
    _, x3m = cam_png("bm-cam-mark", None, 80, 110, GREEN, mark=mk)
    k1, kit3 = kit_tile("bm-kit")
    comp(png, x3, E[0], E[1] + 50)
    comp(png, x3m, E[0] + 260, E[1] + 50)
    comp(png, kit3, E[0] + 520, E[1] + 50)
    comp(png, one, E[0] + 800, E[1] + 50)
    comp(png, k1, E[0] + 890, E[1] + 50)
    fcx = os.path.join(TMP, "bm-face-x6.png")
    sh(one, "-crop", "36x30+22+42", "+repage", "-filter", "point", "-resize", "600%", fcx)
    comp(png, fcx, E[0] + 990, E[1] + 50)
    lab = write("bm-facelab.svg", 600, 30, text(0, 20, "face at 1x, x6 (nearest): forehead clear, smile", 15,
                                                "bold", NOTE))
    labp = os.path.join(TMP, "bm-facelab.png")
    sh("-background", "none", lab, labp)
    comp(png, labp, E[0] + 990, E[1] + 240)
    for k, o, cxk in hold_jobs:     # cup close-ups: full figure at x2.2, cropped round the cup
        m = model(o)
        cp = [p for p in m if p.name == "cup"][0]
        P0, _ = cam(0, 0)
        f = cp.pxf
        hp = [P0(f(q)) for pc in cp.pieces for q in pc]
        hu = (min(q[0] for q in hp) + max(q[0] for q in hp)) / 2
        hv = (min(q[1] for q in hp) + max(q[1] for q in hp)) / 2
        S, ox, oy = 2.2, 400, 800
        sv = write(f"bm-hold-{k}.svg", 800, 900, render(m, 0, 0, S, ox, oy, 5), CREAM)
        full = os.path.join(TMP, f"bm-hold-{k}.png")
        sh(sv, full)
        u, v = int(ox + hu * S), int(oy + hv * S)
        crop = os.path.join(TMP, f"bm-hold-{k}-crop.png")
        sh(full, "-crop", f"260x260+{u - 130}+{v - 140}", "+repage", crop)
        comp(png, crop, cxk - 130, cy0 + 20)
    info = {k: (round(u, 1), round(v, 1)) for k, (u, v, c) in hm.items()}
    json.dump({"gamecam_marks_px_from_feet_origin": info, "face_check_px": fc,
               "face_check_writing_nod14_px": face_check(14.0),
               "m_per_u": M_PER_U, "height_m": H_M, "target_px": TARGET, "px": int(hpx), "px_w": int(wpx)},
              open(os.path.join(TMP, "bodymap.json"), "w"), indent=1)
    return png, info, fc


# ============================================================ SHEET
PAL = [(5, "top, sleeves, skirt; shoes: the dark read"), (6, "apron: bib, straps, skirt; cheeks"),
       (7, "apron tie + back bow, pocket, scrunchie, marker"), (25, "hair: the puff"),
       (15, "skin: head, ears, neck, forearms, hands"), (26, "leggings"), (23, "the cup and lid; teeth; eye glint"),
       (22, "ink: outline, eyes, brows, mouth, cup text")]


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


def head_crop(name, opts, s=1.3):
    w, h = int(170 * s), int(175 * s)
    ox, oy = w / 2, (GROUND + 2) * s
    sv = write(f"{name}.svg", w, h, render(model(opts), 0, 0, s, ox, oy, 4), CREAM)
    png = os.path.join(TMP, f"{name}.png")
    sh(sv, png)
    return png


def cup_card(name, s=7.0):
    """The cup at card size, front: the line is real text (in 3D a decal)."""
    parts = cup((0, 0, 0), ROW[23], text=False)
    w, h = 300, 320
    inner = render(parts, 0, 0, s, w / 2, h / 2 + 10, 3.5)
    lines = [("You are", 98), ("not a", 136), ("PDF.", 176)]
    for t, y in lines:
        inner += (f'<text x="{w / 2}" y="{y + 10}" font-family="Marker Felt, Chalkboard, Comic Sans MS, Helvetica" '
                  f'font-size="34" fill="{INK}" text-anchor="middle">{t}</text>')
    inner += (f'<path d="M{w / 2 - 34},{205} C{w / 2 - 20},{213} {w / 2 + 6},{213} {w / 2 + 30},{203}" fill="none" '
              f'stroke="{ROW[7]}" stroke-width="4" stroke-linecap="round"/>')
    sv = write(f"{name}.svg", w, h, inner, CREAM)
    png = os.path.join(TMP, f"{name}.png")
    sh(sv, png)
    return png


def lift(dy):
    return lambda q: (q[0], q[1] + dy, q[2])


def face_tiles(tag, bg, gs_k=1.0):
    """Face crops at the game camera: 1x tile, then the face at x3 (and grey), for rest, laugh and talk."""
    out = []
    for o, lab in (({}, "rest"), ({"face": "laugh"}, "laugh"), ({"face": "talk"}, "talk")):
        one, _ = cam_png(f"face-{tag}-{lab}", o, 80, 110, bg, gs=GS * gs_k)
        f3 = os.path.join(TMP, f"face-{tag}-{lab}-x3.png")
        sh(one, "-crop", "40x34+20+40", "+repage", "-filter", "point", "-resize", "300%", f3)
        out.append((lab, one, f3))
    return out


def sheet():
    W, H = 2900, 3180
    i = [text(30, 50, "GHOSTED: Juno the barista, model sheet v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnaround (rest: the cup in both hands). Body map v1 landmarks. "
              "Direction A (the hourglass). Palette rows only.", 18)]
    s1, g1 = 2.0, 880
    xs = [250, 650, 1050, 1450]
    labs = ["FRONT", "3/4 (front turned to viewer-left)", "SIDE (facing viewer-left)", "BACK"]
    rows = [("top of the puff", LM["puff_top"]), ("hairline (centre)", LM["hairline"]),
            ("eye line = ear points", LM["eye"]), ("neckline", LM["neck"]), ("shoulder joint", LM["shoulder"]),
            ("waist = apron tie", LM["waist"]), ("hem", LM["hem"]), ("sole", LM["sole"])]
    for lab, y in rows:
        yy = g1 - (GROUND - y) * s1
        i.append(guide(60, 1660, yy, 0.45))
        i.append(text(1670, yy + 5, lab, 15, "bold" if ("eye" in lab or "tie" in lab) else "normal", NOTE))
    for x, lab, yw in zip(xs, labs, (0, 35, 90, 180)):
        i.append(text(x - 170, 125, lab, 17, "bold"))
        i.append(shadow(x, g1 + 6, 120 if yw != 90 else 85, 12))
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
             "- Toy pawn, the HOURGLASS: round shoulders,",
             "  pinched at the apron tie, flared hem. 1.0 x Kit.",
             "- Hair pulled back into a high round puff with",
             "  a red scrunchie. High clean hairline; strand",
             "  lines ON the hair only. No fringe.",
             "- Coffee-brown top (rolled sleeves) and skirt;",
             "  apricot bib apron; red tie, back bow, pocket.",
             "- The cup: white, lid, a written line. Text at",
             "  card size; just a cup at the game camera.",
             "- Mouth: rest = closed smile line; laugh and",
             "  talk = Ricky style (dark fill, teeth band).",
             "- Joins: sleeve, brown cuff ball at the elbow,",
             "  skin forearm, ball hand (notes)."]
    for k, ln in enumerate(rules):
        i.append(text(px_, 520 + k * 23, ln, 16, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))

    # ---- row 2: motion
    y2, g2 = 990, 1540
    i.append(text(30, y2, "HAND OVER A CUP: her right arm forward, cup on the palm", 18, "bold", NOTE))
    i.append(text(30, y2 + 24, "(red: shoulder, elbow, wrist). Front, 3/4, side. Smile; the other hand at her side", 14))
    hand = {"arms": "hand"}
    for k, yw in enumerate((0, 35, 90)):
        x = 130 + k * 230
        i.append(shadow(x, g2 + 5, 70, 9))
        i.append(render(model(hand), yw, 0, 1.15, x, g2, 3.2))
    for (X, Hh) in [(-54, GROUND - LM["shoulder"]), (-66, GROUND - 212), (-46, GROUND - 212)]:
        i.append(dot(130 + X * 1.15, g2 - Hh * 1.15, 6, RED))
    tx_ = 760
    i.append(text(tx_, y2, "A SMALL WAVE: her right hand up by the shoulder, 3 frames", 18, "bold", NOTE))
    i.append(text(tx_, y2 + 24, "the hand rocks out and back (about 0.3 s a beat); the cup stays in the left hand", 14))
    for k in range(3):
        x = tx_ + 110 + k * 230
        i.append(shadow(x, g2 + 5, 70, 9))
        i.append(render(model({"arms": f"wave{k + 1}", "face": "smile" if k != 1 else "talk"}), 0, 0, 1.15, x, g2,
                        3.2))
        i.append(text(x - 30, g2 + 40, f"wave {k + 1}", 14, "bold"))
    cx_ = 1500
    i.append(text(cx_, y2, "WRITING ON THE CUP: cup up in the left hand, marker", 18, "bold", NOTE))
    i.append(text(cx_, y2 + 24, "in the right; head down 14 deg, eyes down; then she turns it to you", 14))
    for k, (o, yw, lab) in enumerate([({"arms": "write", "face": "focus"}, 0, "write (front)"),
                                      ({"arms": "write", "face": "focus"}, 35, "write (3/4)"),
                                      ({"arms": "hand", "face": "dry"}, 0, "then: 'here you go'")]):
        x = cx_ + 100 + k * 230
        i.append(shadow(x, g2 + 5, 70, 9))
        i.append(render(model(o), yw, 0, 1.15, x, g2, 3.2))
        i.append(text(x - 60, g2 + 40, lab, 14, "bold"))
    ex_ = 2290
    i.append(text(ex_, y2, "EXPRESSIONS (front)", 18, "bold", NOTE))
    exprs = [({}, "rest: calm smile"), ({"face": "laugh"}, "laugh (Ricky mouth)"), ({"face": "dry"}, "dry: one brow"),
             ({"face": "focus", "head_nod": 0.0}, "writing: eyes down")]
    for k, (o, lab) in enumerate(exprs):
        i.append(text(ex_ + (k % 2) * 300, y2 + 50 + (k // 2) * 275, lab, 15, "bold"))

    # ---- row 3: silhouette, cup card, lineups
    y3 = 1680
    i.append(text(30, y3, "64 px SILHOUETTE (front, 3/4; 1x and x4)", 18, "bold", NOTE))
    i.append(text(30, y3 + 480, "THE CUP AT CARD SIZE (front)", 18, "bold", NOTE))
    i.append(text(30, y3 + 502, "the line is real text (a decal in 3D); at the game camera it is just a cup", 14))
    i.append(text(700, y3, "LINEUPS AT THE GAME CAMERA (x2): Juno estimate on the real Brett v1 renders with Kit, "
                  "Ricky, Dot, Brett, 3 Ghosties and the ATS.", 18, "bold", NOTE))
    i.append(text(700, y3 + 22, "Grass: colour, grey. Path: colour, grey (Lena's formula).", 15))
    vals = [f"top 5 vs grass 1: {ratio(ROW[5], GREEN):.2f}:1; vs path 3: {ratio(ROW[5], PATHC):.2f}:1 "
            f"(the dark read). Hair 25 vs grass: {ratio(ROW[25], GREEN):.2f}:1",
            f"apron 6 vs grass 1: {ratio(ROW[6], GREEN):.2f}:1; vs path 3: {ratio(ROW[6], PATHC):.2f}:1 (low: it sits "
            f"inside the brown, apron 6 vs top 5: {ratio(ROW[6], ROW[5]):.2f}:1)",
            f"tie 7 vs apron 6: {ratio(ROW[7], ROW[6]):.2f}:1; vs top 5: {ratio(ROW[7], ROW[5]):.2f}:1; cup 23 vs "
            f"apron 6: {ratio(ROW[23], ROW[6]):.2f}:1; cup 23 vs top 5: {ratio(ROW[23], ROW[5]):.2f}:1",
            f"hair 25 vs skin 15: {ratio(ROW[25], ROW[15]):.2f}:1; top 5 vs Brett vest 7: {ratio(ROW[5], ROW[7]):.2f}:1;"
            f" vs Kit 14: {ratio(ROW[5], '#2F6FDB'):.2f}:1; vs Ricky 17: {ratio(ROW[5], '#2E2C3D'):.2f}:1; vs Dot 11: "
            f"{ratio(ROW[5], '#7A5596'):.2f}:1"]
    for k, v in enumerate(vals):
        i.append(text(700, y3 + 735 + k * 26, v, 16))
    i.append(text(700, y3 + 735 + 4 * 26 + 8, "In grey: a dark puff, a light face, a dark hourglass with a mid-light "
                  "apron front and a white cup, dark legs.", 17, "bold"))

    # ---- row 4: game camera next to Kit, face check
    y4 = 2560
    i.append(text(30, y4, "GAME CAMERA NEXT TO KIT (x3): rest, hand over, wave, write, Kit; grass then path; 1x at the "
                  "right", 18, "bold", NOTE))
    i.append(text(1760, y4, "FACE CHECK AT THE GAME CAMERA (x3 of the 1x face): grass, path, grey", 18, "bold", NOTE))
    hpx, wpx = measure_px()
    sz = ["SIZE (estimate; Viet's blockout sets it):", f"Target 1.0 x Kit = {TARGET:.0f} px, puff included.",
          f"This tile: {hpx} x {wpx} px facing the camera.",
          f"1 u = {M_PER_U * 1000:.2f} mm: about {H_M:.2f} m to the puff top,",
          f"{HEAD_TOP_M:.2f} m to the hair cap (Kit {KIT_M} m)."]
    for k, ln in enumerate(sz):
        i.append(text(330, y3 + 540 + k * 21, ln, 15, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))
    svg = write("juno-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "juno-sheet.png")
    sh(svg, png)

    for k, (o, lab) in enumerate(exprs):
        hc = head_crop(f"face-{k}", o, 1.25)
        comp(png, hc, ex_ + (k % 2) * 300, y2 + 58 + (k // 2) * 275)
    s1x, s4 = silhouette("sil-front", 0)
    q1x, q4 = silhouette("sil-34", 35)
    comp(png, s1x, 40, y3 + 30)
    comp(png, q1x, 130, y3 + 30)
    comp(png, s4, 40, y3 + 110)
    comp(png, q4, 340, y3 + 110)
    sh(s1x, os.path.join(OUT, "silhouette-64.png"))
    cc = cup_card("cup-card")
    sh(cc, "-resize", "60%", cc)
    comp(png, cc, 40, y3 + 515)
    lg = [lineup("lu-grass-colour", LU_GRASS, GRASS_BOX, GRASS_SPOT),
          lineup("lu-grass-grey", LU_GRASS, GRASS_BOX, GRASS_SPOT, grey=True),
          lineup("lu-path-colour", LU_PATH, PATH_BOX, PATH_SPOT),
          lineup("lu-path-grey", LU_PATH, PATH_BOX, PATH_SPOT, grey=True)]
    # grass crops are 400x340 -> x2 = 800x680; path 500x340 -> 1000x680. Fit 4 across at x0.5 of x2 = 1x... use x2/2
    xpos = 700
    for k, (o1, o2, kk) in enumerate(lg):
        t = os.path.join(TMP, f"lu-fit-{k}.png")
        sh(o2, "-resize", "x680", "-resize", "54%", t)
        comp(png, t, xpos, y3 + 45)
        xpos += Image.open(t).size[0] + 10
    # game camera tiles (x3) and 1x
    poses = [(None, "rest"), ({"arms": "hand"}, "hand"), ({"arms": "wave3"}, "wave"),
             ({"arms": "write", "face": "focus"}, "write")]
    xg = 30
    for bg, tag in ((GREEN, "g"), (PATHC, "p")):
        for k, (o, lab) in enumerate(poses):
            one, x3 = cam_png(f"sheet-cam-{tag}-{k}", o, 80, 110, bg)
            sh(x3, "-resize", "75%", x3)
            comp(png, x3, xg + k * 185, y4 + 30 + (0 if tag == "g" else 255))
            comp(png, one, xg + 4 * 185 + 200 + k * 85, y4 + 30 + (0 if tag == "g" else 255))
        k1, kit3 = kit_tile("sheet-kit")
        sh(kit3, "-resize", "75%", kit3)
        comp(png, kit3, xg + 4 * 185, y4 + 30 + (0 if tag == "g" else 255))
        comp(png, k1, xg + 4 * 185 + 200 + 4 * 85, y4 + 30 + (0 if tag == "g" else 255))
    # face check x3: grass rest/laugh/talk, path rest, grey of each
    fx = 1760
    fg = face_tiles("g", GREEN)
    fp = face_tiles("p", PATHC)
    for k, (lab, one, f3) in enumerate(fg + fp[:1]):
        comp(png, f3, fx + k * 128, y4 + 30)
        g = f3.replace(".png", "-grey.png")
        grey_img(f3, g)
        comp(png, g, fx + k * 128, y4 + 140)
    labs_ = write("face-labels.svg", 600, 24, "".join(text(k * 128, 18, t, 14, "bold") for k, t in
                                                      enumerate(["rest", "laugh", "talk", "rest (path)"])))
    lp = os.path.join(TMP, "face-labels.png")
    sh("-background", "none", labs_, lp)
    comp(png, lp, fx, y4 + 250)
    fc = face_check()
    ftxt = [f"Forehead band {fc['band']['left_brow']:.1f} / {fc['band']['centre']:.1f} / "
            f"{fc['band']['right_brow']:.1f} px (rule 4+);",
            f"temple hair {fc['temple_above_eye_top_px']:.1f} px above the eye top;",
            f"smile {fc['smile']['below_eye_px']:.1f} px below the eyes, {fc['smile']['w']:.0f} px wide."]
    ft = write("face-txt.svg", 640, 80, "".join(text(0, 18 + k * 22, t, 15) for k, t in enumerate(ftxt)))
    ftp = os.path.join(TMP, "face-txt.png")
    sh("-background", "none", ft, ftp)
    comp(png, ftp, fx, y4 + 285)
    return png, (hpx, wpx), [x[2] for x in lg]


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    print(f"M_PER_U {M_PER_U:.5f} m, height {H_M:.3f} m, GS {GS:.4f}")
    if "explore" in what:
        print(explore())
    if "bodymap" in what:
        print(body_map())
    if "sheet" in what:
        print(sheet())
