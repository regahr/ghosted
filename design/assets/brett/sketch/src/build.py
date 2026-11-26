"""Build explore.png, body-map.png, brett-sheet.png and silhouette-64.png for Brett Bullet-Points.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
Reads only: kit/turn-front.png, ricky/v1/turn-front.png, ghostie/v7/turn-front.png, ats9000/v1/turn-front.png,
auntie-dot/v1/turn-front.png, ghostie/v7/lineup-grass.png (Kit tile) and auntie-dot/v1/lineup-grass.png (Kit, Ricky,
3 Ghosties, the ATS and Dot: real renders).
Writes only into ../, ./ (and ./_tmp, ../crops).
Code reused: Ricky sketch library (ricky.py), Dot render with per-part poses (dot.py), Dot build.py helpers (grey
formula, ratio, camera calibration, tiles, lineup, silhouette), the ATS calibration method.
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
from brett import *  # noqa

TMP = os.path.join(HERE, "_tmp")
CROPS = os.path.join(OUT, "crops")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CROPS, exist_ok=True)

KIT_FRONT = os.path.join(ASSETS, "kit", "turn-front.png")
RICKY_FRONT = os.path.join(ASSETS, "ricky", "v1", "turn-front.png")
GH_FRONT = os.path.join(ASSETS, "ghostie", "v7", "turn-front.png")
ATS_FRONT = os.path.join(ASSETS, "ats9000", "v1", "turn-front.png")
DOT_FRONT = os.path.join(ASSETS, "auntie-dot", "v1", "turn-front.png")
GH_LINEUP = os.path.join(ASSETS, "ghostie", "v7", "lineup-grass.png")      # Kit alone: tile crop
FAM_LINEUP = os.path.join(ASSETS, "auntie-dot", "v1", "lineup-grass.png")  # Kit, Ricky, 3 Ghosties, ATS, Dot
LINEUP_BOX = (640, 400, 960, 720)
BRETT_SPOT = (884, 624)        # free grass right of Dot, below Ricky (feet centre, full frame)
KIT_FEET_Y = 498               # Kit's feet in the lineup (ricky/v1/measure.md: Kit y 424-498)
DOT_SPOT_Y = 661               # Dot's feet (auntie-dot/v1/measure.md); Dot is 72 px there vs 68 px at Kit's spot
KIT_TILE = "80x110+847+396"    # Kit in ghostie/v7/lineup-grass.png (as the Ricky and Dot sheets, 14 px taller)

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # kit/ingame.html L156: fov 26, 26 m, 900 px = 74.97
OUTLINE = 1.6
KIT_PX = 75.0                  # ricky/v1/measure.md L17
TARGET = 1.05 * KIT_PX         # brief.md L24: about 1.05 x Kit on screen = 78.75 px (the figure; halo apart)
CAM = (20.0, 42.0)
CAM_NET = (5.0, 42.0)          # lineup characters turn 15 deg to the camera (ricky/v1/ingame.html L303)
KIT_M = 0.977                  # kit/build_report.json

# ---- camera calibration (ATS / Dot method): metres per unit so the figure (no halo) is 78.75 px facing the camera
_b = pbounds(model(dict(CARRY, halo="none")), *CAM_NET)
HU = _b[3] - _b[1]
M_PER_U = (TARGET - 2 * OUTLINE) / (PX_PER_M * HU)
GS = PX_PER_M * M_PER_U
H_M = (GROUND - LM["top"]) * M_PER_U
HALO_M = (GROUND - LM["halo"] + 6) * M_PER_U
GREEN = "#B5D67A"
RED = "#E0533D"
MAG = "#C2185B"   # note colour for attachment points (not a character colour)


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
    """Brett at the game camera (with his chin-up carriage), 1x, feet centre at (w/2, h-14). Returns (1x, x3)."""
    m = model(dict(CARRY, **(opts or {})))
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
    one, _ = cam_png(f"measure-{int(yaw)}-{(opts or {}).get('halo', 'above')}", opts, 140, 140, None, yaw)
    x0, y0, x1, y1 = alpha_bbox(one)
    return y1 - y0 + 1, x1 - x0 + 1


def kit_tile(name, h=96):
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(GH_LINEUP, "-crop", KIT_TILE, "+repage", one)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def lineup(name="lineup", grey=False):
    """Dot v1 lineup crop (Kit, Ricky, 3 Ghosties, ATS, Dot: real renders) with the Brett estimate on free grass.
    Perspective: Dot is 72 px at her spot vs 68 px at Kit's (auntie-dot/v1/measure.md), so the scale grows with
    the feet row; Brett is scaled the same way for his spot."""
    k = 1 + (72 / 68 - 1) * (BRETT_SPOT[1] - KIT_FEET_Y) / (DOT_SPOT_Y - KIT_FEET_Y)
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(FAM_LINEUP).crop(LINEUP_BOX).save(base)
    w, h = 110, 120
    one, _ = cam_png(f"{name}-brett", None, w, h, gs=GS * k)
    shp = write(f"{name}-shadow.svg", w, h, shadow(w / 2, h - 13, 21, 7, 0.28))
    shpng = os.path.join(TMP, f"{name}-shadow.png")
    sh("-background", "none", shp, shpng)
    x = BRETT_SPOT[0] - LINEUP_BOX[0] - w / 2
    y = BRETT_SPOT[1] - LINEUP_BOX[1] - (h - 14)
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
G_BMGD = {"vest": ROW[2], "shirt": ROW[2], "pants": ROW[2]}   # BMGD #6FBF73 is not a row: shown with row 2
THUMBS = [
    ("1 wedge, swoop, halo, red vest", {}),
    ("2 capsule all green (BMGD)", {"body": VEST_CAPSULE, "hair": "flat", "cap": CAP_LOW, "vest": False,
                                    "colors": {"shirt": ROW[2], "pants": ROW[2]}}),
    ("3 bean, slick, profile frame", {"body": VEST_BEAN, "hair": "slick", "cap": CAP_LOW, "halo": "frame"}),
    ("4 box, cream vest", {"body": VEST_BOX, "hair": "swoop", "cap": CAP_LOW, "colors": {"vest": ROW[12]}}),
    ("5 wedge, apricot, hips", {"arms": "hips", "colors": {"vest": ROW[6]}}),
    ("6 wedge, oxford shirt only", {"vest": False, "colors": {"shirt": ROW[8]}}),
    ("7 capsule, frame, red", {"body": VEST_CAPSULE, "halo": "frame"}),
    ("8 wedge, brown hair", {"colors": {"hair": ROW[25]}}),
    ("9 bean, apricot, halo", {"body": VEST_BEAN, "colors": {"vest": ROW[6]}}),
    ("10 wedge, no halo", {"halo": "none", "arms": "hips"}),
]
DIRS = [
    ("A. THE WEDGE (pick)", {},
     ["Chest out, square shoulders, narrow waist: wide at", "the TOP, the opposite of Ricky's bell and Dot's pear.",
      "Blond swoop, red sweater vest over a white shirt,", "the green ring floating above: the LinkedIn",
      "networker. Grin = white teeth over an ink smile", "line; with his chin-up carriage it reads as a grin",
      "at 1x (body map E). The ring reads as a halo."]),
    ("B. CAPSULE + HALO (BMGD hint)", {"body": VEST_CAPSULE, "hair": "flat", "cap": CAP_LOW,
                                       "colors": {"vest": ROW[12]}},
     ["The hint as given, in a cream vest. At the game", "camera it reads as 'Kit in a cream jumper': the",
      "same capsule as Kit. Cream sits close to the lawn", "and the path in value (see notes)."]),
    ("C. PROFILE FRAME", {"body": VEST_BEAN, "hair": "slick", "cap": CAP_LOW, "halo": "frame"},
     ["The ring stands up behind the head, like the", "#OpenToWork photo frame. It reads at pitch 42, but",
      "as a ring ROUND the head, which is what Ricky's", "lilac headset band already looks like in the lineup.",
      "From the back it hides the whole head."]),
]


def explore():
    W, H = 2700, 1880
    i = [text(30, 50, "GHOSTED: Brett Bullet-Points, explore (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: local references, 10 rough thumbnails, 3 directions, one pick. "
              "Hand-drawn Bezier half outlines lifted to round bodies (Ricky sketch library); palette rows only.", 18)]
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, the locked family; no web)", 20, "bold", NOTE))
    for k, lab in enumerate(["Kit v5 (hero)", "Ricky v1", "Ghostie v7", "ATS-9000 v1", "Auntie Dot v1"]):
        i.append(text(30 + k * 200, ry + 330, lab, 15))
    i.append(text(1080, ry + 345, "Dot v1 lineup at the game camera (x1.5): the whole family on grass", 15))
    ty = 520
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x3, 26 m, "
                  "pitch 42, net yaw 5), at 1.05 x Kit.", 20, "bold", NOTE))
    tw = 264
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 6, ty + 34, lab, 14, "bold"))
        i.append(render(model(o), 0, 0, 0.66, x + tw / 2, ty + 270, 2.2, mark_scale=0.8))
        i.append(shadow(x + tw / 2, ty + 272, 56, 6))
    dy = 1200
    i.append(text(30, dy, "DIRECTIONS (3), developed: front, 3/4, back; then the game camera (x3): Brett left, "
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
            i.append(frame(x, dy + 12, x + dw - 20, dy + 560, NOTE, 4))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    for k, src in enumerate([KIT_FRONT, RICKY_FRONT, GH_FRONT, ATS_FRONT, DOT_FRONT]):
        t = os.path.join(TMP, f"ref-{k}.png")
        sh(src, "-resize", "x290", t)
        comp(png, t, 30 + k * 200, ry + 25)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(FAM_LINEUP, "-crop", "330x230+640+430", "+repage", "-filter", "point", "-resize", "150%", lu)
    comp(png, lu, 1080, ry + 5)
    for n, (lab, o) in enumerate(THUMBS):
        _, x3 = cam_png(f"ex-thumb-{n}", o, 80, 110, GREEN)
        comp(png, x3, 30 + n * tw + 12, ty + 290)
    _, kit3 = kit_tile("ex-kit", 110)
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
    """3D landmark and attachment points (X, H, Z), from the same numbers as brett.model()."""
    return {
        "eye_l": (surf_pt(LM["eye_x"][0], LM["eye"], HEAD_HALF, 0.92), NOTE),
        "eye_r": (surf_pt(LM["eye_x"][1], LM["eye"], HEAD_HALF, 0.92), NOTE),
        "mouth": (surf_pt(150, 114, HEAD_HALF, 0.92), NOTE),
        "hairline": (surf_pt(150, LM["hairline"], CAP_HALF, 0.92), NOTE),
        "ear_l": ((-55, GROUND - LM["eye"] - 1, -4), NOTE),  # noqa
        "ear_r": ((55, GROUND - LM["eye"] - 1, -4), NOTE),
        "halo": ((0, GROUND - LM["halo"], 0), MAG),
        "collar": (surf_pt(150, 156, VEST_WEDGE, 0.78), MAG),
        "v_point": (surf_pt(150, LM["v_point"], VEST_WEDGE, 0.78), NOTE),
        "hand_l": ((-76, GROUND - LM["hand"], 6), NOTE),
        "hand_r": ((76, GROUND - LM["hand"], 6), NOTE),
        "hem": (surf_pt(150, LM["hem"] - 2, VEST_WEDGE, 0.78), NOTE),
        "feet": ((0, GROUND - 331, 9), NOTE),
    }


HF = rot_x(CARRY["head_nod"], (0, GROUND - LM["chin"], 0))     # the chin-up carriage (as brett.model)
HEAD_KEYS = ("eye_l", "eye_r", "mouth", "hairline", "ear_l", "ear_r", "halo")


def gamecam_marks():
    P, _ = cam(*CAM_NET)
    out = {}
    for k, (q, c) in lm3d().items():
        if k in HEAD_KEYS:
            q = HF(q)
        out[k] = (P(q)[0] * GS, P(q)[1] * GS, c)
    return out


def hair_gap():
    """At the game camera (net yaw 5): the lowest hair point in each eye column vs the eye top, in px (1x).
    Hair = the hairline edge on the face + every point of the swoop tube."""
    P0, _ = cam(*CAM_NET)
    P = lambda q: P0(HF(q))
    sw = [p for p in model() if p.name == "swoop"][0]
    swp = [P(q) for pc in sw.pieces for q in pc]
    res = {}
    for k, ex in (("left", LM["eye_x"][0]), ("right", LM["eye_x"][1])):
        eu = P(surf_pt(ex, LM["eye"], HEAD_HALF, 0.92))[0]
        eye_top_v = P(surf_pt(ex, LM["eye"] - 9, HEAD_HALF, 0.92))[1] * GS
        pts = path_points(HAIRLINE, 40)
        hy = min(pts, key=lambda p: abs(p[0] - ex))[1]
        line_v = P(surf_pt(ex, hy, CAP_HALF, 0.92))[1] * GS
        col = [v for (u, v, d) in swp if abs(u - eu) < 7 and d > 0]
        swoop_v = max(col) * GS if col else None
        low = max(line_v, swoop_v or -1e9)
        res[k] = {"hairline_y": round(hy, 1), "gap_px": round(eye_top_v - low, 2),
                  "swoop_gap_px": round(eye_top_v - swoop_v, 2) if swoop_v is not None else None}
    return res


def grin_px():
    """Grin box at 1x on the game camera (net yaw 5)."""
    P0, _ = cam(*CAM_NET)
    P = lambda q: P0(HF(q))
    cap = [p for p in model() if p.name == "hair"][0]
    from ricky import lift_mark
    pts, _ = lift_mark(cap.face_host, GRIN)
    uv = [(P(q)[0] * GS, P(q)[1] * GS) for q in pts]
    us, vs = [u for u, v in uv], [v for u, v in uv]
    eye_bot = P(surf_pt(LM["eye_x"][0], LM["eye"] + 9, HEAD_HALF, 0.92))[1] * GS
    return {"w": round(max(us) - min(us), 1), "h": round(max(vs) - min(vs), 1),
            "below_eye_px": round(min(vs) - eye_bot, 1)}


def body_map():
    W, H = 2600, 2160
    i = [text(30, 50, "GHOSTED: Brett Bullet-Points body map v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions in head-heights, landmarks, attachment points (halo, "
              "collar, thumb, fingers), and a check at the game camera (26 m, pitch 42).", 18)]
    s = 2.2
    fx, gy0 = 400, 175
    gy = lambda y: gy0 + y * s
    fxx = lambda x: fx + (x - 150) * s
    i.append(text(30, 125, "A. FRONT (upright, symmetric)", 20, "bold", NOTE))
    rows = [("halo centre (floats)", LM["halo"]), ("top of swoop", LM["top"]), ("top of hair cap", LM["crown"]),
            ("hairline (centre)", LM["hairline"]), ("eye line = ear points", LM["eye"]), ("mouth (grin)", 114),
            ("chin", LM["chin"]), ("neck line = shirt collar", LM["neck"]), ("shoulder joint (arm root)", LM["shoulder"]),
            ("chest (widest)", LM["chest"]), ("vest V point", LM["v_point"]), ("vest hem = waist", LM["hem"]),
            ("knee", LM["knee"]), ("sole", LM["sole"])]
    x_end = fx + 190 * s
    for lab, y in rows:
        i.append(guide(fx - 90 * s - 20, x_end, gy(y)))
        i.append(text(x_end + 8, gy(y) + 5, f"{lab}  y {y}", 15,
                      "bold" if ("eye" in lab or "halo" in lab or "collar" in lab) else "normal", NOTE))
    i.append(shadow(fx, gy(342), 110, 12))
    i.append(render(model(), 0, 0, s, fx, gy(GROUND), 5))
    for x in LM["ear_x"]:
        i.append(dot(fxx(x), gy(LM["eye"] + 1), 7))
    i.append(dot(fxx(150), gy(LM["halo"]), 7, MAG))
    i.append(dot(fxx(150), gy(LM["neck"] + 4), 7, MAG))
    for x in LM["shoulder_x"]:
        i.append(dot(fxx(x), gy(LM["shoulder"]), 7, MAG))
    x0, y0, x1, y1 = LM["mouth"]
    i.append(f'<path d="M{fxx(x0)},{gy(y0)} L{fxx(x1)},{gy(y0)} L{fxx(x1)},{gy(y1)} L{fxx(x0)},{gy(y1)} Z" '
             f'fill="none" stroke="{NOTE}" stroke-width="3" stroke-dasharray="8,6"/>')
    rx = 50
    hh = LM["chin"] - LM["top"]
    ticks = [LM["top"], LM["chin"], LM["chin"] + hh, LM["sole"]]
    i.append(f'<path d="M{rx},{gy(ticks[0])} L{rx},{gy(ticks[-1])}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    for t in ticks:
        i.append(f'<path d="M{rx - 10},{gy(t)} L{rx + 10},{gy(t)}" fill="none" stroke="{NOTE}" stroke-width="3"/>')
    nh = (LM["sole"] - LM["top"]) / hh
    i.append(text(rx + 14, gy(LM["top"] + hh / 2), "1 head", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["chin"] + hh / 2), "2", 15, "bold", NOTE))
    i.append(text(rx + 14, gy(LM["sole"] - 4), f"{nh:.2f}", 15, "bold", NOTE))

    # B. side
    sx = 1250
    i.append(text(sx - 150, 125, "B. SIDE (same lines)", 20, "bold", NOTE))
    for lab, y in rows:
        i.append(guide(sx - 150, sx + 170, gy(y), 0.35))
    i.append(shadow(sx, gy(342), 80, 10))
    i.append(render(model(), 90, 0, s, sx, gy(GROUND), 5))

    # C. hands: thumb and fingers (attachment)
    hx, hy0 = 1660, 1010
    i.append(text(hx - 40, hy0 - 40, "C. HANDS: the thumb and the fingers (front, x2.2)", 20, "bold", NOTE))
    i.append(text(hx - 40, hy0 - 16, "Ball hand; thumb and fingers are small capsules from the top of the ball.", 15))
    hand_jobs = []
    for k, (o, lab) in enumerate([({"arms": "thumb", "face": "wink"}, "LIKE: thumb up"),
                                  ({"arms": "count1"}, "bullet 1"), ({"arms": "count3"}, "bullet 3")]):
        cx_ = hx + 60 + k * 300
        hand_jobs.append((k, o, cx_))
        i.append(text(cx_ - 60, hy0 + 305, lab, 16, "bold"))
    # D. notes
    nx = 1650
    notes = [(f"PROPORTIONS (head = top of swoop to chin = {hh} units)", True),
             (f"Whole figure {LM['sole'] - LM['top']} units = {nh:.2f} heads (Kit 2.71, Ricky 2.67,", False),
             ("  Dot 2.27): the tallest of the humans, a peer.", False),
             (f"Size: 1.05 x Kit on screen = {TARGET:.2f} px (figure, no halo);", False),
             (f"  estimate {H_M:.2f} m to the swoop top (1 u = {M_PER_U * 1000:.2f} mm),", False),
             (f"  {HALO_M:.2f} m to the halo top.", False),
             ("Head 108 wide (skull 98 tall); hair cap 118 wide.", False),
             ("Body: a WEDGE. 32 wide at the neck, 148 at the chest", False),
             ("  (y 188), 72 at the waist (y 252); chinos 40 wide each.", False),
             ("", False),
             ("LANDMARKS", True),
             ("Hairline: high and clean, y 62 centre, y 84-88 at the", False),
             ("  temples; side part on his right (viewer-left).", False),
             ("Swoop: one rolled wave from the part, up and over", False),
             ("  to his left; its lowest point y 57 at x 120, above the hairline.", False),
             ("Eye line y 94; eyes x 132 / 168 (ink ovals + glint).", False),
             ("Ears: on the eye line at the head sides (x 95 / 205).", False),
             ("Mouth zone x 120-180, y 102-126: a wide grin = white teeth", False),
             ("  (row 23) over an ink smile line, corners up. Not a bar.", False),
             ("Neck: chin y 144, shirt collar at the neck line y 152.", False),
             ("Shoulder joint: x 92 / 208, y 176 (X +-56 inside the", False),
             ("  vest). Shirt sleeve out of the armhole, then the hand.", False),
             ("", False),
             ("ATTACHMENT POINTS (magenta)", True),
             ("Halo: level ring, centre on the head axis, y 0 (16", False),
             ("  above the swoop top). Ring 76 x 60 across, tube 12.", False),
             ("  Follows the head (position, roll); stays LEVEL under a nod.", False),
             ("Collar: open shirt collar on the neck line, the vest", False),
             ("  V from the collar to y 198. No tie (Kit, Ricky have one).", False),
             ("Thumb / fingers: on the top of the hand ball.", False),
             ("", False),
             ("CARRIAGE (in game): chin up 10 deg about the chin", True),
             ("Smug, and it turns the grin to the camera: at 1x the", False),
             ("  grin reads as teeth only with it (see E). The model", False),
             ("  sheet turnaround stays neutral for the build.", False)]
    for k, (ln, b) in enumerate(notes):
        i.append(text(nx, 150 + k * 25, ln, 17, "bold" if b else "normal", NOTE if b else INK))

    # E. game camera
    E = (30, 1110)
    i.append(text(E[0], E[1], "E. GAME CAMERA CHECK (x3, 1x at right). Left: Brett estimate. Middle: landmark dots "
                  "(blue: eyes, mouth, hairline, ears, V, hands, hem, feet;", 18, "bold", NOTE))
    i.append(text(E[0], E[1] + 24, "magenta: halo centre, collar). Right: Kit, real v7 render. Net yaw 5 (lineup "
                  "facing), pitch 42.", 18, "bold", NOTE))
    gap = hair_gap()
    gr = grin_px()
    hm = gamecam_marks()
    hpx, _ = measure_px({"halo": "none"})
    hpx2, _ = measure_px()
    lines = [f"Hair vs eyes at 1x: lowest hair in the eye columns is {gap['left']['gap_px']:.1f} px (left) and "
             f"{gap['right']['gap_px']:.1f} px (right) ABOVE the eye top. The swoop alone: "
             f"{gap['left']['swoop_gap_px']:.1f} / {gap['right']['swoop_gap_px']:.1f} px above.",
             f"Grin at 1x: {gr['w']:.1f} x {gr['h']:.1f} px, starting {gr['below_eye_px']:.1f} px under the eyes. "
             f"Teeth (row 23) over an ink smile line with the corners up: reads as a grin, not a beard (dark or white).",
             f"Halo centre {hm['eye_l'][1] - hm['halo'][1]:.1f} px above the eyes; the ring shows as an open ellipse over "
             f"the hair (pitch 42), green with the ink edge.",
             f"Height: {hpx} px without the halo (target {TARGET:.2f}), {hpx2} px with it. Kit is 75 px.",
             "Read: a green ring over a blond swoop, a peach face with two dots and a white grin, a red wedge",
             "with a white V and white sleeves, navy legs. Nothing green on the body."]
    for k, ln in enumerate(lines):
        i.append(text(E[0], E[1] + 470 + k * 24, ln, 16, "bold" if k == 4 else "normal"))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    def mk(ox, oy):
        return "".join(f'<ellipse cx="{ox + u:.2f}" cy="{oy + v:.2f}" rx="0.9" ry="0.9" fill="{c}" stroke="none"/>'
                       for u, v, c in hm.values())
    one, x3 = cam_png("bm-cam", None, 80, 110, GREEN)
    _, x3m = cam_png("bm-cam-mark", None, 80, 110, GREEN, mark=mk)
    k1, kit3 = kit_tile("bm-kit", 110)
    comp(png, x3, E[0], E[1] + 50)
    comp(png, x3m, E[0] + 260, E[1] + 50)
    comp(png, kit3, E[0] + 520, E[1] + 50)
    comp(png, one, E[0] + 800, E[1] + 50)
    comp(png, k1, E[0] + 890, E[1] + 50)
    # face close-up at 1x scaled x6 (the grin read)
    fc = os.path.join(TMP, "bm-face-x6.png")
    sh(one, "-crop", "36x30+22+36", "+repage", "-filter", "point", "-resize", "600%", fc)
    comp(png, fc, E[0] + 990, E[1] + 50)
    for k, o, cx_ in hand_jobs:     # hand close-ups: full figure at x2.2, cropped round the raised hand
        m = model(o)
        hd = [p for p in m if p.name == "hand"][0]
        P0, _ = cam(0, 0)
        hp = [P0(q) for q in hd.pieces[0]]
        hu = (min(q[0] for q in hp) + max(q[0] for q in hp)) / 2
        hv = (min(q[1] for q in hp) + max(q[1] for q in hp)) / 2
        S, ox, oy = 2.2, 400, 800
        sv = write(f"bm-hand-{k}.svg", 800, 900, render(m, 0, 0, S, ox, oy, 5), CREAM)
        full = os.path.join(TMP, f"bm-hand-{k}.png")
        sh(sv, full)
        u, v = int(ox + hu * S), int(oy + hv * S)
        crop = os.path.join(TMP, f"bm-hand-{k}-crop.png")
        sh(full, "-crop", f"240x260+{u - 120}+{v - 150}", "+repage", crop)
        comp(png, crop, cx_ - 120, hy0 + 20)
    i2 = text(E[0] + 990, E[1] + 250, "face at 1x, x6 (nearest): white grin, eyes clear", 15, "bold", NOTE)
    lab = write("bm-facelab.svg", 600, 30, i2.replace(f'y="{E[1] + 250}"', 'y="20"').replace(f'x="{E[0] + 990}"', 'x="0"'))
    labp = os.path.join(TMP, "bm-facelab.png")
    sh("-background", "none", lab, labp)
    comp(png, labp, E[0] + 990, E[1] + 240)
    info = {k: (round(u, 1), round(v, 1)) for k, (u, v, c) in hm.items()}
    json.dump({"gamecam_marks_px_from_feet_origin": info, "hair_gap_px": gap, "grin_px": grin_px(),
               "m_per_u": M_PER_U, "height_m": H_M, "halo_top_m": HALO_M, "target_px": TARGET,
               "px_no_halo": int(hpx), "px_with_halo": int(hpx2)},
              open(os.path.join(TMP, "bodymap.json"), "w"), indent=1)
    return png, info, gap


# ============================================================ SHEET
PAL = [(7, "sweater vest (the big area)"), (23, "shirt: sleeves, collar, V; teeth; eye glint"),
       (15, "skin: head, ears, neck, hands"), (12, "hair: the blond swoop"), (26, "chinos"), (5, "shoes"),
       (2, "the #OpenToWork HALO: the ONE green thing"), (22, "ink: outline, eyes, brows, mouth edge")]


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
    w, h = int(170 * s), int(170 * s)
    ox, oy = w / 2, (GROUND + 6) * s
    sv = write(f"{name}.svg", w, h, render(model(opts), 0, 0, s, ox, oy, 4), CREAM)
    png = os.path.join(TMP, f"{name}.png")
    sh(sv, png)
    return png


def lift(dy):
    return lambda q: (q[0], q[1] + dy, q[2])


def sheet():
    W, H = 2900, 2700
    i = [text(30, 50, "GHOSTED: Brett Bullet-Points model sheet v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnaround (the side part and the swoop are the only asymmetry). "
              "Body map v1 landmarks. Direction A (the wedge). Palette rows only.", 18)]
    s1, g1 = 2.0, 880
    xs = [250, 650, 1050, 1450]
    labs = ["FRONT", "3/4 (front turned to viewer-left)", "SIDE (facing viewer-left)", "BACK"]
    rows = [("halo", LM["halo"]), ("top of swoop", LM["top"]), ("hairline (centre)", LM["hairline"]),
            ("eye line = ear points", LM["eye"]), ("neck line = collar", LM["neck"]),
            ("shoulder joint", LM["shoulder"]), ("chest (widest)", LM["chest"]), ("vest hem = waist", LM["hem"]),
            ("knee", LM["knee"]), ("sole", LM["sole"])]
    for lab, y in rows:
        yy = g1 - (GROUND - y) * s1
        i.append(guide(60, 1660, yy, 0.45))
        i.append(text(1670, yy + 5, lab, 15, "bold" if ("eye" in lab or "halo" in lab) else "normal", NOTE))
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
             "- Toy pawn, the WEDGE: chest out, square",
             f"  shoulders, narrow waist; {(LM['sole'] - LM['top']) / (LM['chin'] - LM['top']):.2f} heads. "
             "1.05 x Kit.",
             "- Hair: high clean hairline, side part, one",
             "  blond swoop up and over. Nothing near the eyes.",
             "- Halo: a level green ring floating above the",
             "  swoop, centred on the head axis; it follows",
             "  the head. The only green on him (+ ink edge).",
             "- Red sweater vest over a white shirt: open",
             "  collar, no tie, white V, white sleeves.",
             "- Grin: white teeth over an ink smile line.",
             "- In game: chin up 10 deg (smug; opens the grin).",
             "- Joins: shirt sleeve out of the vest armhole,",
             "  then the ball hand (3-mesh build, notes)."]
    for k, ln in enumerate(rules):
        i.append(text(px_, 520 + k * 23, ln, 16, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))

    # ---- row 2: motion
    y2, g2, s2 = 990, 1540, 1.3
    i.append(text(30, y2, "CONFIDENT IDLE: hands on hips; chest puffs, chin up", 18, "bold", NOTE))
    i.append(text(30, y2 + 24, "carriage chin up 10 deg; puff: lean back 3 deg and rise 3 u; about 2 s a cycle; feet planted",
                  14))
    idle = [({"arms": "hips", "head_nod": -10}, None, "rest"),
            ({"arms": "hips", "head_nod": -10}, chain(rot_x(-3), lift(3)), "puff"),
            ({"arms": "hips", "head_nod": -10}, None, "settle")]
    for k, (o, xf, lab) in enumerate(idle):
        x = 130 + k * 240
        i.append(shadow(x, g2 + 5, 70, 9))
        i.append(render(model(o), 0, 0, 1.1, x, g2, 3.2, xf=xf))
        i.append(text(x - 25, g2 + 40, lab, 14, "bold"))
    tx_ = 760
    i.append(text(tx_, y2, "THE LIKE (week 12): his right fist out to the side, thumb up, wink", 18, "bold", NOTE))
    i.append(text(tx_, y2 + 24, "(red: shoulder, elbow, wrist; the other hand stays at his side)", 14))
    thumb = {"arms": "thumb", "face": "wink", "head_nod": -10}
    for k, yw in enumerate((0, 35)):
        x = tx_ + 170 + k * 300
        i.append(shadow(x, g2 + 5, 80, 9))
        i.append(render(model(thumb), yw, 0, s2, x, g2, 3.5))
    for (X, Hh) in [(-56, GROUND - LM["shoulder"]), (-88, GROUND - 212), (-96, GROUND - 184)]:
        i.append(dot(tx_ + 170 + X * s2, g2 - Hh * s2, 6, RED))
    cx_ = 1560
    i.append(text(cx_, y2, "TALKING IN BULLETS: his right hand counts 1, 2, 3", 18, "bold", NOTE))
    i.append(text(cx_, y2 + 24, "a finger pops up on each bullet; mouth open; the other hand on the hip", 14))
    for k in range(3):
        x = cx_ + 120 + k * 240
        i.append(shadow(x, g2 + 5, 70, 9))
        i.append(render(model({"arms": f"count{k + 1}", "face": "talk", "head_nod": -10}), 0, 0, 1.1, x, g2, 3.2))
        i.append(text(x - 50, g2 + 40, f"• bullet {k + 1}", 14, "bold"))
    ex_ = 2290
    i.append(text(ex_, y2, "EXPRESSIONS (front)", 18, "bold", NOTE))
    for k, lab in enumerate(["rest: the grin", "talk", "the like: wink", "secretly lost"]):
        i.append(text(ex_ + (k % 2) * 290, y2 + 50 + (k // 2) * 275, lab, 15, "bold"))

    # ---- row 3: silhouette, lineup, game camera
    y3 = 1680
    i.append(text(30, y3, "64 px SILHOUETTE (front, 3/4; 1x and x4)", 18, "bold", NOTE))
    i.append(text(700, y3, "LINEUP AT THE GAME CAMERA (x2): Brett estimate on the real Dot v1 grass with Kit,", 18,
                  "bold", NOTE))
    i.append(text(700, y3 + 22, "Ricky, Dot, 3 Ghosties and the ATS. Colour, then grey (Lena's formula).", 15))
    i.append(text(2120, y3, "GAME CAMERA NEXT TO KIT (x3): rest, like, Kit", 18, "bold", NOTE))
    i.append(text(2120, y3 + 22, "grey below; 1x at the bottom", 15))
    vals = [f"vest 7 vs grass 1: {ratio(ROW[7], '#B5D67A'):.2f}:1; vs path 3: {ratio(ROW[7], '#EBD3A6'):.2f}:1",
            f"vest 7 vs Kit shirt 14: {ratio(ROW[7], '#2F6FDB'):.2f}:1 (hue red vs blue); vs Ricky 17: "
            f"{ratio(ROW[7], '#2E2C3D'):.2f}:1; vs Dot 11: {ratio(ROW[7], '#7A5596'):.2f}:1",
            f"halo 2 vs grass 1: {ratio(ROW[2], '#B5D67A'):.2f}:1 (low: the ink edge carries it); halo 2 vs hair 12: "
            f"{ratio(ROW[2], ROW[12]):.2f}:1",
            f"shirt 23 vs vest 7: {ratio(ROW[23], ROW[7]):.2f}:1; hair 12 vs skin 15: {ratio(ROW[12], ROW[15]):.2f}:1 "
            f"(low: ink hairline)",
            f"teeth 23 vs skin 15: {ratio(ROW[23], ROW[15]):.2f}:1 + ink smile line; chinos 26 vs vest 7: "
            f"{ratio(ROW[26], ROW[7]):.2f}:1"]
    for k, v in enumerate(vals):
        i.append(text(700, y3 + 715 + k * 26, v, 17))
    i.append(text(700, y3 + 715 + 5 * 26 + 10, "In grey: a light swoop and a light V on a mid-dark wedge, dark legs. "
                  "Kit mid-grey, Ricky near-black, Dot dark pear with a white dome, ATS mid, Ghosties white.", 17,
                  "bold"))
    hpx, wpx = measure_px({"halo": "none"})
    hpx2, _ = measure_px()
    sz = ["SIZE (estimate; Viet's blockout sets it):",
          f"Target 1.05 x Kit 75 px = {TARGET:.2f} px tall.",
          f"This tile: {hpx} x {wpx} px without the halo,",
          f"{hpx2} px with it, facing the camera.",
          f"1 u = {M_PER_U * 1000:.2f} mm: about {H_M:.2f} m to the swoop",
          f"top, {HALO_M:.2f} m to the halo top (Kit {KIT_M} m)."]
    for k, ln in enumerate(sz):
        i.append(text(2120, y3 + 875 + k * 22, ln, 15, "bold" if k == 0 else "normal", NOTE if k == 0 else INK))
    svg = write("brett-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "brett-sheet.png")
    sh(svg, png)

    for k, o in enumerate([{}, {"face": "talk"}, {"face": "wink"}, {"face": "lost"}]):
        hc = head_crop(f"face-{k}", dict(o, halo="above"), 1.25)
        comp(png, hc, ex_ + (k % 2) * 290, y2 + 60 + (k // 2) * 275)
    s1x, s4 = silhouette("sil-front", 0)
    q1x, q4 = silhouette("sil-34", 35)
    comp(png, s1x, 40, y3 + 30)
    comp(png, q1x, 130, y3 + 30)
    comp(png, s4, 40, y3 + 120)
    comp(png, q4, 360, y3 + 120)
    sh(s1x, os.path.join(OUT, "silhouette-64.png"))
    lc1, lc2, k = lineup("lineup-colour")
    lg1, lg2, _ = lineup("lineup-grey", grey=True)
    comp(png, lc2, 700, y3 + 45)
    comp(png, lg2, 700 + 650, y3 + 45)
    one, x3 = cam_png("sheet-cam", None, 80, 110, GREEN)
    onet, x3t = cam_png("sheet-cam-like", thumb, 80, 110, GREEN)
    k1, kit3 = kit_tile("sheet-kit", 110)
    comp(png, x3, 2120, y3 + 40)
    comp(png, x3t, 2370, y3 + 40)
    comp(png, kit3, 2620, y3 + 40)
    for src, x in ((x3, 2120), (x3t, 2370), (kit3, 2620)):
        g = src.replace(".png", "-grey.png")
        grey_img(src, g)
        comp(png, g, x, y3 + 390)
    comp(png, one, 2130, y3 + 735)
    comp(png, onet, 2230, y3 + 735)
    comp(png, k1, 2330, y3 + 735)
    return png, (hpx, wpx, hpx2), k


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    print(f"M_PER_U {M_PER_U:.5f} m, height {H_M:.3f} m, halo top {HALO_M:.3f} m, GS {GS:.4f}")
    if "explore" in what:
        print(explore())
    if "bodymap" in what:
        print(body_map())
    if "sheet" in what:
        print(sheet())
