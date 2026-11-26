"""Build explore.png, body-map.png, panel-sheet.png and silhouette-64.png for The Panel.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
Reads only the locked cast renders (kit, ricky/v1, ghostie/v7, ats9000/v1, auntie-dot/v1, brett/v1, juno/v1) and the
real Juno v1 lineup renders juno/v1/lineup-grass.png and lineup-path.png (the whole family, Juno included).
Writes only into ../, ./_tmp and ../crops.
Code reused: Juno sketch (juno.py: head, cap, face curves) and Juno/Brett build.py helpers (grey formula, ratio,
perspective at a spot, tiles, lineup, silhouette, face check), the Ricky library and the Dot render.
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
from panel import *  # noqa
from ricky import lift_mark  # noqa

TMP = os.path.join(HERE, "_tmp")
CROPS = os.path.join(OUT, "crops")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CROPS, exist_ok=True)

REFS = [("Kit v5", "kit/turn-front.png"), ("Ricky v1", "ricky/v1/turn-front.png"),
        ("Ghostie v7", "ghostie/v7/turn-front.png"), ("ATS-9000 v1", "ats9000/v1/turn-front.png"),
        ("Auntie Dot v1", "auntie-dot/v1/turn-front.png"), ("Brett v1", "brett/v1/hero.png"),
        ("Juno v1", "juno/v1/hero.png")]
LU = {"grass": os.path.join(ASSETS, "juno", "v1", "lineup-grass.png"),
      "path": os.path.join(ASSETS, "juno", "v1", "lineup-path.png")}
BG = {"grass": "#BDD662", "path": "#EFCA8C"}          # sampled ground in the Juno v1 renders (lit)
KIT_CROP = "60x88+856+412"                            # Kit in both Juno v1 lineups (shirt x 867-905, y 459-483)
KIT_FEET = (31, 84)                                   # Kit's feet in that crop
# set spots (floor centre of the table, full frame) and the box of the lineup crop
SPOT = {"grass": (1065, 640), "path": (745, 610)}
CROP = {"grass": (760, 380, 1240, 780), "path": (520, 340, 1000, 740)}
KIT_FEET_Y = 498
DOT_SPOT_Y = 661

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # 74.97 px per m (kit/ingame.html L156)
OUTLINE = 1.6
GS = PX_PER_M * M_PER_U                                   # px per unit at 1x
CAM = (5.0, 42.0)                                         # net yaw 5 (root turned 15 to the yaw-20 camera), pitch 42
KIT_M = 0.977
KIT_HEAD_M = KIT_M / 2.71                                 # Kit is 2.71 heads (juno/sketch/src/build.py L424)
KIT_Z = 300                                               # Kit stands 0.7 m in front of the table front edge
RED = "#E0533D"
MAG = "#C2185B"


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
    out = np.dstack([g, g, g, np.asarray(im)[..., 3]])
    Image.fromarray(out, "RGBA").save(dst)


def lum(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def persp(feet_y):
    """Scale at a feet row, from Dot's two measures (72 px at y 661 vs 68 px at Kit's y 498)."""
    return 1 + (72 / 68 - 1) * (feet_y - KIT_FEET_Y) / (DOT_SPOT_Y - KIT_FEET_Y)


def kit_png(ground=None):
    """Kit cut from the real Juno v1 path render (clean ground round him): flood-fill the path from the crop border
    (tolerance 30), then his contact shadow below the knees (tolerance 120). The tiles draw their own shadow."""
    out = os.path.join(TMP, "kit-cut.png")
    if os.path.exists(out):
        return out
    raw = os.path.join(TMP, "kit-raw.png")
    sh(LU["path"], "-crop", KIT_CROP, "+repage", raw)
    a = np.asarray(Image.open(raw).convert("RGB")).astype(int)
    hh, ww = a.shape[:2]
    ref = a[2, 2]
    d = np.abs(a - ref).sum(-1)
    gone = np.zeros((hh, ww), bool)
    stack = [(y, x) for y in range(hh) for x in (0, ww - 1)] + [(y, x) for x in range(ww) for y in (0, hh - 1)]
    while stack:
        y, x = stack.pop()
        if gone[y, x] or d[y, x] >= 30:
            continue
        gone[y, x] = True
        stack += [(y + dy, x + dx) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= y + dy < hh and 0 <= x + dx < ww]
    d2 = np.abs(a - a[1, ww - 2]).sum(-1)          # the Cafe's cast shadow at the top-right of the crop
    stack = [(1, ww - 2)]
    while stack:
        y, x = stack.pop()
        if gone[y, x] and (y, x) != (1, ww - 2) or d2[y, x] >= 30:
            continue
        gone[y, x] = True
        stack += [(y + dy, x + dx) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= y + dy < hh and 0 <= x + dx < ww and not gone[y + dy, x + dx]]
    stack = [(y, x) for y in range(72, hh) for x in range(ww) if gone[y, x]]
    seen = gone.copy()
    while stack:
        y, x = stack.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 72 <= yy < hh and 0 <= xx < ww and not seen[yy, xx] and d[yy, xx] < 120:
                seen[yy, xx] = True
                stack.append((yy, xx))
    keep = ~seen                                   # keep only Kit: the largest opaque component (drops edge slivers)
    lab = np.zeros((hh, ww), int)
    sizes = {}
    n = 0
    for y0 in range(hh):
        for x0 in range(ww):
            if keep[y0, x0] and not lab[y0, x0]:
                n += 1
                st, lab[y0, x0], c = [(y0, x0)], n, 0
                while st:
                    y, x = st.pop()
                    c += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        yy, xx = y + dy, x + dx
                        if 0 <= yy < hh and 0 <= xx < ww and keep[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = n
                            st.append((yy, xx))
                sizes[n] = c
    big = max(sizes, key=sizes.get)
    alpha = np.where(lab == big, 255, 0).astype(np.uint8)
    Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA").save(out)
    return out


def kit_on(base, x_feet, y_feet, k=1.0):
    """Kit with a soft contact shadow, feet at (x_feet, y_feet) in base."""
    shp = os.path.join(TMP, "kit-shadow.png")
    if not os.path.exists(shp):
        sv = write("kit-shadow.svg", 40, 16, shadow(20, 8, 17, 6, 0.28))
        sh("-background", "none", sv, shp)
    comp(base, shp, x_feet - 20, y_feet - 8)
    comp(base, kit_png(), x_feet - KIT_FEET[0], y_feet - KIT_FEET[1])


def set_svg(sc, w, h, ox, oy, gs, yaw=CAM[0], pitch=CAM[1], bg=None, extra=""):
    inner = shadow(ox, oy + 2, 160 * gs / GS * 0.5, 18 * gs / GS * 0.5, 0.18) if bg else ""
    inner += render_scene(sc, yaw, pitch, gs, ox, oy, OUTLINE) + extra
    return inner


def cam_tile(name, o=None, w=200, h=184, bg=None, kit=None, gs=None, sc=None, bot=66):
    """The set at the game camera, 1x; table floor centre at (w/2, h-50). kit: 'grass'/'path' puts Kit in front."""
    gs = gs or GS
    sc = sc or scene(o)
    ox, oy = w / 2, h - bot
    sv = write(f"{name}.svg", w, h, set_svg(sc, w, h, ox, oy, gs, bg=bg), bg)
    one = os.path.join(TMP, f"{name}-1x.png")
    if bg:
        sh(sv, one)
    else:
        sh("-background", "none", sv, one)
    if kit:
        P, _ = cam(*CAM)
        u, v, _ = P((-40, 0, KIT_Z))
        kit_on(one, ox + u * gs, oy + v * gs)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def lineup(name, ground, grey=False, o=None):
    """The real Juno v1 lineup render (the whole family) with the set estimate on a free spot and Kit in front."""
    spot = SPOT[ground]
    k = persp(spot[1])
    box = CROP[ground]
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(LU[ground]).crop(box).save(base)
    w, h = 260, 200
    one, _ = cam_tile(f"{name}-set", o, w, h, None, gs=GS * k, bot=52)
    shp = write(f"{name}-shadow.svg", w, h, shadow(w / 2, h - 52 + 4, 84 * k, 26 * k, 0.26))
    shpng = os.path.join(TMP, f"{name}-shadow.png")
    sh("-background", "none", shp, shpng)
    x = spot[0] - box[0] - w / 2
    y = spot[1] - box[1] - (h - 52)
    comp(base, shpng, x, y)
    comp(base, one, x, y)
    P, _ = cam(*CAM)
    u, v, _ = P((-40, 0, KIT_Z))
    kit_on(base, spot[0] - box[0] + u * GS * k, spot[1] - box[1] + v * GS * k)
    out1 = os.path.join(TMP, f"{name}-1x.png")
    sh(base, out1)
    if grey:
        grey_img(out1, out1)
    out2 = os.path.join(TMP, f"{name}-x2.png")
    sh(out1, "-filter", "point", "-resize", "200%", out2)
    return out1, out2, k


# ============================================================ EXPLORE
A = {}
THUMBS = [
    ("1 bow + flat-top + cube, panel table", A),
    ("2 BMGD literal: 2 sphere heads + box", {"cf": {"hair": "sphere", "body": BODY_SPHERE},
                                             "wb": {"hair": "sphere", "body": BODY_SPHERE}, "table": ROW[5]}),
    ("3 cloud hair + flat-top + cube", {"cf": {"hair": "cloud"}}),
    ("4 beehive + spiky + cube", {"cf": {"hair": "beehive"}, "wb": {"hair": "spiky"}}),
    ("5 bow + spiky + tall slab", {"wb": {"hair": "spiky"}, "box": {"box": "slab"}}),
    ("6 the pick on a wood table (row 5)", {"table": ROW[5]}),
    ("7 bow + flat-top + monitor", {"box": {"box": "monitor"}}),
    ("8 cloud + spiky + monitor, wood", {"cf": {"hair": "cloud"}, "wb": {"hair": "spiky"},
                                         "box": {"box": "monitor"}, "table": ROW[5]}),
    ("9 beehive + flat-top + slab", {"cf": {"hair": "beehive"}, "box": {"box": "slab"}}),
    ("10 swap: CF plinth 4, WB steel 9", {"cf": {"colors": {"top": ROW[4]}}, "wb": {"colors": {"top": ROW[9]}}}),
]
DIRS = [
    ("A. BOW, FLAT-TOP, BLACK CUBE (pick)", A,
     ["Three shapes at a glance: a round head with a", "cream bow (Culture Fit), a square flat-top and",
      "glasses with a marker (Whiteboard), a plain black", "cube with a cream 'camera off' icon. The light",
      "panel-edge table (row 24) makes the black cube", "the strongest value in the set, so the joke reads.",
      "Lilac cardigan vs navy vest + light-blue shirt:", "no locked-cast row as a big area."]),
    ("B. BMGD LITERAL: SPHERE HEADS", THUMBS[1][1],
     ["The hint as given: two bare sphere heads and a", "box on a wood table. At the game camera the two",
      "heads are the same ball: they read apart by", "colour only, which the brief rules out. The box", "melts into the wood table in grey (2.2:1)."]),
    ("C. CLOUD, SPIKES, MONITOR, WOOD", THUMBS[7][1],
     ["Big cloud hair, spiky tech hair, a black monitor", "on a wood table. The monitor reads as a real",
      "screen (a laptop prop, not a person). The cloud", "hair spreads beside the face (temple rule risk)",
      "and the spikes break the toy-pawn calm."]),
]


def explore():
    W, H = 2760, 2140
    i = [text(30, 50, "GHOSTED: The Panel, explore (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: local references, 10 rough thumbnails, 3 directions, one pick. "
              "Hand-drawn Bezier half outlines lifted to round bodies (Juno / Ricky sketch code); palette rows only.",
              18)]
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, the locked cast; no web)", 20, "bold", NOTE))
    for k, (lab, _) in enumerate(REFS):
        i.append(text(30 + k * 150, ry + 300, lab, 15))
    i.append(text(1110, ry + 330, "Juno v1 lineup at the game camera (x1.5): the whole cast on grass", 15))
    ty = 500
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x2, 26 m, "
                  "pitch 42, net yaw 5).", 20, "bold", NOTE))
    tw = 270
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 4, ty + 34, lab, 13, "bold"))
        i.append(render_scene(scene(o), 0, 0, 0.4, x + tw / 2, ty + 230, 1.8, mark_scale=0.8))
    dy = 1010
    i.append(text(30, dy, "DIRECTIONS (3), developed: front and 3/4; then the game camera (x3) with Kit in front "
                  "(real Juno v1 render cut-out)", 20, "bold", NOTE))
    dw = 905
    for n, (lab, o, notes) in enumerate(DIRS):
        x = 30 + n * dw
        i.append(text(x + 10, dy + 40, lab, 20, "bold", NOTE if n == 0 else INK))
        i.append(render_scene(scene(o), 0, 0, 0.62, x + 210, dy + 330, 2.2, mark_scale=0.9))
        i.append(render_scene(scene(o), 35, 0, 0.62, x + 620, dy + 330, 2.2, mark_scale=0.9))
        for k, ln in enumerate(notes):
            i.append(text(x + 10, dy + 930 + k * 22, ln, 16))
        if n == 0:
            i.append(frame(x, dy + 12, x + dw - 20, dy + 1110, NOTE, 4))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    for k, (_, src) in enumerate(REFS):
        t = os.path.join(TMP, f"ref-{k}.png")
        sh(os.path.join(ASSETS, src), "-resize", "140x260", t)
        comp(png, t, 30 + k * 150, ry + 25)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(LU["grass"], "-crop", "420x240+600+390", "+repage", "-filter", "point", "-resize", "150%", lu)
    comp(png, lu, 1110, ry - 10)
    for n, (lab, o) in enumerate(THUMBS):
        one, _ = cam_tile(f"ex-thumb-{n}", o, 170, 140, BG["grass"], bot=34)
        x2 = one.replace("-1x", "-x2")
        sh(one, "-filter", "point", "-resize", "200%", x2)
        sh(x2, "-resize", "260x", x2)
        comp(png, x2, 30 + n * tw + 5, ty + 250)
    for n, (lab, o, notes) in enumerate(DIRS):
        _, x3 = cam_tile(f"ex-dir-{n}", o, 200, 184, BG["grass"], kit="grass")
        comp(png, x3, 30 + n * dw + 150, dy + 370)
    return png


# ============================================================ BODY MAP
def surf_pt(x, y, half, depth, out=0.0):
    prof = profile(half)
    X = x - 150
    r = r_at(prof, y)
    X = max(-r, min(r, X))
    z = r * depth * math.sqrt(max(1 - (X / max(r, 1e-3)) ** 2, 0)) + out
    return (X, GROUND - y, z)


def place_f(who, lean=0.0, nod=HEAD_SET):
    hf = rot_x(nod, (0, GROUND - LM["chin"], 0))
    return chain(hf, rot_x(lean, (0, LOCAL_TABLE_H + 10, -10)), translate(SEATS[who], DH, SEAT_Z))


def face_check(who, face="rest", nod=HEAD_SET, lean=0.0):
    """At the game camera (net yaw 5, pitch 42), px at 1x: forehead band per brow column, the lowest side hair vs
    the eye top, the mouth box and its gap under the eyes, and the flat-top front edge vs the hairline."""
    P0, _ = cam(*CAM)
    f = place_f(who, lean, nod)
    v = lambda q: P0(f(q))[1] * GS
    hl = J.path_points(HAIRLINE, 40)
    res = {"band": {}}
    for k, bx in (("left_brow", 131), ("centre", 150), ("right_brow", 169)):
        hy = min(hl, key=lambda p: abs(p[0] - bx))[1]
        brow_top = 84.0 if k != "centre" else 86.0
        res["band"][k] = round(v(surf_pt(bx, brow_top, CAP_HALF, 0.92)) - v(surf_pt(bx, hy, CAP_HALF, 0.92)), 2)
    eye_top = v(surf_pt(132, 104 - 8.5, CAP_HALF, 0.92))
    side = [p for p in hl if p[0] < 124 or p[0] > 176]
    low = max(side, key=lambda p: p[1])
    res["temple_above_eye_top_px"] = round(eye_top - v(surf_pt(low[0], low[1], CAP_HALF, 0.92)), 2)
    eye_bot = v(surf_pt(132, 104 + 8.5, CAP_HALF, 0.92))
    low_, up_ = person(who, {"face": face, "head_nod": nod, "lean": lean})
    cap = [p for p in up_ if p.name == "hair"][0]
    d = {"grin": LAUGH, "talk": TALK, "rest": SMILE if who == "cf" else FLAT}.get(face, SMILE)
    pts, _ = lift_mark(cap.face_host, d)
    uv = [(P0(f(q))[0] * GS, P0(f(q))[1] * GS) for q in pts]
    us, vs = [a for a, b in uv], [b for a, b in uv]
    res["mouth"] = {"w": round(max(us) - min(us), 1), "h": round(max(vs) - min(vs), 1),
                    "below_eye_px": round(min(vs) - eye_bot, 1),
                    "above_chin_px": round(v(surf_pt(150, 150, HEAD_HALF, 0.92)) - max(vs), 1)}
    if who == "wb":
        res["flattop_front_above_hairline_px"] = round(v(surf_pt(150, LM["hairline"], CAP_HALF, 0.92)) -
                                                       v((0, GROUND - 60, 34)), 2)
    return res


def body_map():
    W, H = 2800, 2050
    i = [text(30, 50, "GHOSTED: The Panel, body map v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions, landmarks, the table and seat heights, attachment points "
              "(bow + band, flat-top, glasses, pens, marker, box icon), and a check at the game camera (26 m, pitch 42).",
              18)]
    s = 1.55
    fx, gy0 = 820, 160
    floor = gy0 + 420 * s
    gy = lambda H_: floor - H_ * s
    i.append(text(30, 125, "A. FRONT (upright, symmetric; world heights in units, 1 u = 3.33 mm)", 20, "bold", NOTE))
    rows = [("head top (cap) 1.26 m", 340 - LM["crown"] + DH), ("hairline", 340 - LM["hairline"] + DH),
            ("eye line = ear points", 340 - 104 + DH), ("chin", 340 - LM["chin"] + DH),
            ("shoulder joint", 340 - LM["shoulder"] + DH), ("forearms + hands on the table", TABLE_TOP + 10),
            ("TABLE TOP 0.733 m = 0.75 x Kit", TABLE_TOP), ("seat (hidden)", 150), ("floor", 0)]
    for lab, Hh in rows:
        i.append(guide(40, fx + 360 * s, gy(Hh)))
        i.append(text(fx + 365 * s, gy(Hh) + 5, f"{lab}  H {Hh:.0f}", 15,
                      "bold" if ("eye" in lab or "TABLE" in lab) else "normal", NOTE))
    sc = scene()
    i.append(render_scene(sc, 0, 0, s, fx, floor, 3.5))
    P, _ = cam(0, 0)
    marks = []
    for who in ("cf", "wb"):
        cx = SEATS[who]
        for xx in (-55, 55):
            marks.append((cx + xx, 340 - 105 + DH, NOTE))
        sw_ = 56 if who == "cf" else 60
        for xx in (-sw_, sw_):
            marks.append((cx + xx, 340 - LM["shoulder"] + DH, NOTE))
    marks += [(SEATS["cf"], 340 - 46 + DH, MAG), (SEATS["wb"], 340 - 49 + DH, MAG),
              (SEATS["box"], TABLE_TOP + BOX[1] / 2, MAG), (SEATS["wb"] + 22, 340 - 198 + DH, MAG)]
    for (x, Hh, c) in marks:
        i.append(dot(fx + x * s, gy(Hh), 6, c))
    # Kit at the same scale, standing in front (a size check)
    i.append(text(40, gy(KIT_M * 300) - 10, "Kit 0.977 m (to scale)", 14, "bold", NOTE))

    # B. side view: one person, the chair and the table, depth
    sx = 2000
    i.append(text(sx - 260, 125, "B. SIDE (Whiteboard alone + table + chair): the depth", 20, "bold", NOTE))
    side = {"low": [], "table": table(), "up": [], "icon": None}
    l, u = person("wb", {})
    side["low"] = l + [p for p in chairs() if abs(p.pxf((0, 0, 0))[0] if getattr(p, 'pxf', None) else 0) < 1e9]
    side["low"] = l + chairs()[3:6]
    side["up"] = u
    i.append(render_scene(side, 90, 0, s, sx, floor, 3.5))
    sn = ["z (toward you): table front edge +90, back edge -90;", "torso axis -140 (its front -92, at the back edge);",
          "chair back -192. Forearms lie ON the table top", "(z -78 to -26), hands meet at z -26."]
    for k, ln in enumerate(sn):
        i.append(text(sx - 260, floor + 40 + k * 22, ln, 15))

    # C. notes
    nx = 30
    ny = floor + 130
    notes = [("PROPORTIONS", True),
             ("Heads: the Juno head (96 u = 0.32 m tall, 108 wide): the same size as Kit's head (0.977 / 2.71 =", False),
             ("  0.36 m). Read of the brief: the seated head is Kit-SIZED (see notes.md Open 1).", False),
             ("Seated: shoulders 24 u (8 cm) above the table top, chin 56 u above it, cap top 1.26 m.", False),
             ("Table 600 x 30 x 180 u (2.0 x 0.1 x 0.6 m, BMGD) + a front panel and two side panels (a 'panel' desk).", False),
             ("The box: 100 x 90 x 80 u (0.33 x 0.30 x 0.27 m) on the table top, right seat, back to the back edge.", False),
             ("", False),
             ("LANDMARKS (blue)", True),
             ("Eye line H 326; eyes at x +-18 from each head axis; ears on the eye line at the head sides (+-55).", False),
             ("Hairline high and clean (y 64 frame = H 366): nothing on the forehead, nothing beside the eyes.", False),
             ("Shoulder joints +-56 (Culture Fit, soft round) / +-60 (Whiteboard, square). Elbows rest on the table.", False),
             ("Mouth zone x 138-162, y 122-140 (frame). Rest: closed line. Grin / talk: Ricky style.", False),
             ("", False),
             ("ATTACHMENT POINTS (magenta)", True),
             ("Culture Fit: cream band over the crown ear to ear (behind the hairline, z -16); bow CENTRED on the", False),
             ("  crown (y 46); low bun at the nape (hidden at the front).", False),
             ("Whiteboard: flat-top block on the skull (y 38-60, z -46..+34), front edge 4 u above the hairline;", False),
             ("  glasses on the eye line, arms to the ear points; pocket (2 pens) on his left chest.", False),
             ("  Marker: in his RIGHT hand (viewer's left): lies on the table at rest, upright (click), forward (point).", False),
             ("The Camera-Off One: the icon is a decal centred on the box front (0.82 of the face); swap: camera /", False),
             ("  mic / off. Lean pivot: the box's bottom front edge.", False)]
    for k, (ln, b) in enumerate(notes):
        i.append(text(nx, ny + k * 24, ln, 16, "bold" if b else "normal", NOTE if b else INK))

    # E. game camera
    E = (1400, ny + 40)
    i.append(text(E[0], E[1], "E. GAME CAMERA CHECK (x3). Left: the set + Kit in front. Right: landmark dots.", 18,
                  "bold", NOTE))
    fcf, fwb = face_check("cf"), face_check("wb")
    P0, _ = cam(*CAM)
    pr = lambda who, q: P0(place_f(who)(q))
    head_px = {w: round((pr(w, (0, GROUND - 154, 0))[1] - pr(w, (0, GROUND - 52, 0))[1]) * GS, 1)
               for w in ("cf", "wb")}
    lines = [f"Head (cap top to chin) at 1x: Culture Fit {head_px['cf']} px, Whiteboard {head_px['wb']} px; "
             f"Kit's head (0.36 m) about {KIT_HEAD_M * PX_PER_M * math.cos(math.radians(42)):.0f} px by the same measure.",
             f"Forehead band at 1x: CF {fcf['band']['left_brow']}/{fcf['band']['centre']}/{fcf['band']['right_brow']} px, "
             f"WB {fwb['band']['left_brow']}/{fwb['band']['centre']}/{fwb['band']['right_brow']} px (rule 4+).",
             f"Temples: side hair {fcf['temple_above_eye_top_px']} px above the eye top; flat-top front edge "
             f"{fwb['flattop_front_above_hairline_px']} px above the hairline.",
             "Read: a round head with a cream bow over a lilac cardigan, a square brown flat-top with glasses",
             "over a navy vest, a black cube with a cream icon, on a pale table; Kit in front, smaller."]
    for k, ln in enumerate(lines):
        i.append(text(E[0], E[1] + 600 + k * 22, ln, 15, "bold" if k == 3 else "normal"))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)
    # Kit to scale on the front view (real render, height 0.977 m)
    kt = os.path.join(TMP, "bm-kit.png")
    sh(os.path.join(ASSETS, "kit", "turn-front.png"), "-fuzz", "6%", "-transparent", "%[pixel:p{2,2}]", "-trim", "+repage", "-resize",
       f"x{int(KIT_M * 300 * s)}", kt)
    kw_ = Image.open(kt).size[0]
    comp(png, kt, 60, gy(KIT_M * 300))
    # game camera tiles
    _, x3 = cam_tile("bm-cam", None, 200, 184, BG["grass"], kit="grass")
    comp(png, x3, E[0], E[1] + 30)
    hm = []
    for (x, Hh, c) in marks:
        u, v_, _ = P0((x, Hh, SEAT_Z + 40 if abs(x - SEATS["box"]) > 1 else BOX_Z))
        hm.append((u * GS, v_ * GS, c))

    def mk():
        return "".join(f'<ellipse cx="{100 + u:.2f}" cy="{118 + v_:.2f}" rx="1.1" ry="1.1" fill="{c}" stroke="none"/>'
                       for u, v_, c in hm)
    sc0 = scene()
    sv = write("bm-cam-mark.svg", 200, 184, set_svg(sc0, 200, 184, 100, 118, GS, bg=BG["grass"], extra=mk()),
               BG["grass"])
    one = os.path.join(TMP, "bm-cam-mark-1x.png")
    sh(sv, one)
    x3m = os.path.join(TMP, "bm-cam-mark-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3m)
    comp(png, x3m, E[0] + 620, E[1] + 30)
    json.dump({"face_cf": fcf, "face_wb": fwb, "head_px": head_px, "gs": GS},
              open(os.path.join(TMP, "bodymap.json"), "w"), indent=1)
    return png, fcf, fwb, head_px


# ============================================================ SHEET
PAL = [(24, "table + chairs (one mesh): panel-edge"), (22, "the Camera-Off box; ink outline, eyes, mouths, glasses"),
       (12, "box icon; CF bow + band, blouse V"), (10, "Culture Fit cardigan + sleeves"),
       (26, "Whiteboard vest; legs (hidden)"), (8, "Whiteboard shirt: sleeves, collar, V"),
       (25, "hair: both (CF swept back + bun, WB flat-top)"), (15, "skin"), (23, "marker body, pocket, teeth, glints"),
       (21, "marker cap, red pen"), (9, "blue pen (tiny)"), (6, "CF cheeks (tiny)")]


def silhouette(name, sc, yaw, pitch, px=64):
    x0, y0, x1, y1 = scene_bounds(sc, yaw, pitch)
    s = (px - 2) / (y1 - y0)
    w = int(math.ceil((x1 - x0) * s)) + 4
    inner = render_scene(sc, yaw, pitch, s, -x0 * s + 2, -y0 * s + 1, 0.01, mono=INK)
    sv = write(f"{name}.svg", w, px, inner, "#FFFFFF")
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(sv, one)
    x4 = os.path.join(TMP, f"{name}-x4.png")
    sh(one, "-filter", "point", "-resize", "400%", "-bordercolor", INK, "-border", "1", x4)
    return one, x4


def head_crop(name, who, o, s=1.2):
    """A head-and-shoulders crop, front, of one person."""
    l, u = person(who, o)
    sc = {"low": [], "table": [], "up": u, "icon": None}
    w, h = int(190 * s), int(200 * s)
    P, _ = cam(0, 0)
    cx = SEATS[who]
    top_H = 340 - 20 + DH
    inner = render_scene(sc, 0, 0, s, w / 2 - cx * s, top_H * s + 10, 3.5)
    sv = write(f"{name}.svg", w, h, inner, CREAM)
    png = os.path.join(TMP, f"{name}.png")
    sh(sv, png)
    return png


def only(who, o=None, chair=True):
    o = o or {}
    if who == "box":
        bp, icon = camera_box(o)
        return {"low": [], "table": [], "up": bp, "icon": icon}
    l, u = person(who, o)
    ch = chairs()[0:3] if who == "cf" else chairs()[3:6]
    return {"low": l + (ch if chair else []), "table": [], "up": u, "icon": None}


def slab(who, w=230):
    """A short piece of the table top under one person (context for the motion and expression panels)."""
    return [fbox("tabletop", ROW[24], (SEATS[who], TABLE_TOP - TABLE_T / 2, 0), w, TABLE_T, TABLE_D)]


def upper(who, o, with_slab=True):
    l, u = person(who, o)
    return {"low": [], "table": slab(who) if with_slab else [], "up": u, "icon": None}


def sheet():
    W, H = 3000, 3800
    i = [text(30, 50, "GHOSTED: The Panel, model sheet v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnarounds (rest). Body map v1 landmarks. Direction A. Palette rows "
              "only. Poses and tilts are in their own panels.", 18)]
    # ---- row 1: the set turnaround
    s1, g1 = 0.62, 470
    i.append(text(30, 125, "THE SET: FRONT, 3/4, SIDE, BACK", 18, "bold", NOTE))
    for k, (yw, lab) in enumerate([(0, "front"), (35, "3/4"), (90, "side"), (180, "back")]):
        x = 230 + k * 470
        i.append(shadow(x, g1 + 4, 200 if yw != 90 else 70, 10))
        i.append(render_scene(scene(), yw, 0, s1, x, g1, 2.4))
        i.append(text(x - 30, g1 + 40, lab, 16, "bold"))
    px_ = 2000
    i.append(text(px_, 125, "PALETTE (existing rows only, seats/lena-park.md)", 17, "bold"))
    for k, (r, use) in enumerate(PAL):
        y = 140 + k * 34
        i.append(f'<path d="M{px_},{y} L{px_ + 26},{y} L{px_ + 26},{y + 26} L{px_},{y + 26} Z" fill="{ROW[r]}" '
                 f'stroke="{INK}" stroke-width="2"/>')
        i.append(text(px_ + 36, y + 19, f"{r} {ROW[r]}  {use}", 15))
    i.append(text(px_, 140 + len(PAL) * 34 + 8, "Shade: base x 0.85 (neutral grey multiplier).", 15))

    # ---- row 2: each one alone, 4 views
    y2, g2 = 560, 1010
    i.append(text(30, y2, "EACH ONE ALONE (with the chair, no table): front, 3/4, side, back. Culture Fit | "
                  "Whiteboard | the Camera-Off One (on the table top line)", 18, "bold", NOTE))
    xk = 110
    for who in ("cf", "wb", "box"):
        for k, yw in enumerate((0, 35, 90, 180)):
            sc = only(who)
            P, _ = cam(yw, 0)
            u0 = P((SEATS[who], 0, SEAT_Z if who != "box" else BOX_Z))[0]
            ss = 1.0 if who != "box" else 1.3
            oy = g2 if who != "box" else g2 - 60 + TABLE_TOP * ss
            if who == "box":
                i.append(guide(xk - 80, xk + 80, g2 - 60, 0.6, 2))
            i.append(render_scene(sc, yw, 0, ss, xk - u0 * ss, oy, 3.2))
            xk += 205 if who != "box" else 190
        xk += 40

    # ---- row 3: motion (upper bodies on a piece of the table)
    y3, g3 = 1090, 1440
    i.append(text(30, y3, "MOTION (front; red: the pivot). Upper bodies on a piece of the table. Rest head set: chin-up 8 deg.", 18, "bold", NOTE))
    mot = [("cf", {}, "CF rest"), ("cf", {"head_nod": 6, "face": "grin"}, "CF nod (-8 to +6)"),
           ("cf", {"head_tilt": 12, "face": "tilt", "arms": "chin"}, "CF tilt 12 + hand"),
           ("wb", {"arms": "click1"}, "WB marker up"), ("wb", {"arms": "click2", "face": "talk"}, "WB *click*"),
           ("wb", {"arms": "point", "face": "talk"}, "WB point (at you, 3/4)")]
    sm = 0.95
    for k, (who, o, lab) in enumerate(mot):
        x = 130 + k * 250
        yw = 25 if "point" in lab else 0
        P, _ = cam(yw, 0)
        u0 = P((SEATS[who], 0, SEAT_Z))[0]
        oy = g3 + 20 + TABLE_TOP * sm - 60
        i.append(render_scene(upper(who, o), yw, 0, sm, x - u0 * sm, oy, 3.0))
        i.append(text(x - 80, g3 + 50, lab, 15, "bold"))
        if "nod" in lab or "tilt" in lab:
            i.append(dot(x, oy - (340 - LM["chin"] + DH) * sm, 6, RED))
        if "click" in lab:
            Pm, _ = cam(0, 0)
            bx = x + (-52 + 2) * sm
            by = oy - (LOCAL_TABLE_H + DH + 62 + 46) * sm
            for a in (-40, 0, 40):
                ca, sa = math.cos(math.radians(a - 90)), math.sin(math.radians(a - 90))
                i.append(f'<path d="M{bx + 14 * ca:.1f},{by + 14 * sa:.1f} L{bx + 26 * ca:.1f},{by + 26 * sa:.1f}" '
                         f'stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    bxx = 1560
    i.append(text(bxx, y3, "THE BOX BLINKS (decal swap, about 0.5 s on / 0.5 s off)", 18, "bold", NOTE))
    for k, (ic, lab) in enumerate([("cam", "camera off"), ("off", "blink: dark"), ("mute", "muted")]):
        sc = only("box", {"icon": ic})
        x = bxx + 90 + k * 190
        oy = g3 - 10 + TABLE_TOP * 1.3
        i.append(render_scene(sc, 0, 0, 1.3, x - SEATS["box"] * 1.3, oy, 3.2))
        i.append(text(x - 50, g3 + 50, lab, 15, "bold"))
    lean = {"cf": {"lean": 14, "face": "talk"}, "wb": {"lean": 14, "face": "talk"}, "box": {"lean": 12}}
    lx = 2220
    i.append(text(lx, y3, "ALL LEAN IN: 'any questions for us?'", 18, "bold", NOTE))
    i.append(text(lx, y3 + 22, "pivot: elbow line (people), bottom front edge (box)", 14))
    i.append(render_scene(scene(lean), 90, 0, 0.6, lx + 170, g3 + 30, 2.4))
    i.append(render_scene(scene(), 90, 0, 0.6, lx + 500, g3 + 30, 2.4))
    i.append(text(lx + 90, g3 + 55, "lean 14 (side)", 14, "bold"))
    i.append(text(lx + 430, g3 + 55, "rest (side)", 14, "bold"))

    # ---- row 4: expressions + silhouettes
    y4 = 1560
    i.append(text(30, y4, "EXPRESSIONS (front). Mouths: closed line or Ricky style (dark fill, teeth band). "
                  "No fringe; nothing beside the eyes.", 18, "bold", NOTE))
    exprs = [("cf", {}, "CF rest: smile"), ("cf", {"face": "grin"}, "CF nod: 'love that!'"),
             ("cf", {"face": "tilt"}, "CF tilt: 'hmm, vibes'"), ("cf", {"face": "talk"}, "CF: 'where do you see...'"),
             ("wb", {}, "WB rest: flat line"), ("wb", {"face": "talk"}, "WB talk"),
             ("wb", {"face": "skeptic"}, "WB: one brow up")]
    sx_ = 2160
    i.append(text(sx_, y4, "64 px SILHOUETTE (set: front, 3/4, game", 18, "bold", NOTE))
    i.append(text(sx_, y4 + 22, "camera). 1x, then x2.", 18, "bold", NOTE))

    # ---- row 5: lineups (4 across, x1.5)
    y5 = 1930
    i.append(text(30, y5, "LINEUPS AT THE GAME CAMERA (x1.5): the set estimate + Kit in front, on the real Juno v1 renders "
                  "(whole cast). Path render: colour, grey. Grass render (set on the path strip beside the cast): "
                  "colour, grey.", 18, "bold", NOTE))
    vals = [f"box 22 vs table 24: {ratio(ROW[22], ROW[24]):.2f}:1 (the strongest value step in the set); "
            f"box 22 vs wood 5 would be {ratio(ROW[22], ROW[5]):.2f}:1.  Icon 12 vs box 22: {ratio(ROW[12], ROW[22]):.2f}:1.",
            f"table 24 vs grass 1: {ratio(ROW[24], '#B5D67A'):.2f}:1; vs path 3: {ratio(ROW[24], '#EBD3A6'):.2f}:1 "
            f"(low: the table reads by its ink edge and the shaded front panel).",
            f"CF lilac 10 vs table 24: {ratio(ROW[10], ROW[24]):.2f}:1; vs hair 25: {ratio(ROW[10], ROW[25]):.2f}:1; "
            f"bow 12 vs hair 25: {ratio(ROW[12], ROW[25]):.2f}:1; lilac 10 vs Dot 11: {ratio(ROW[10], ROW[11]):.2f}:1.",
            f"WB vest 26 vs table 24: {ratio(ROW[26], ROW[24]):.2f}:1; shirt 8 vs vest 26: {ratio(ROW[8], ROW[26]):.2f}:1; "
            f"vest 26 vs Ricky 17: {ratio(ROW[26], ROW[17]):.2f}:1; shirt 8 vs Kit 14: {ratio(ROW[8], '#2F6FDB'):.2f}:1."]
    for k, v in enumerate(vals):
        i.append(text(30, y5 + 660 + k * 24, v, 16))

    # ---- row 6: game camera tiles
    y6 = 2790
    i.append(text(30, y6, "GAME CAMERA WITH KIT IN FRONT (x3, 1x below): rest, CF nod, WB point, box muted, all lean in. "
                  "Grass.", 18, "bold", NOTE))
    # ---- row 7: face check
    y7 = 3460
    i.append(text(30, y7, "FACE CHECK AT THE GAME CAMERA (x3 of the 1x faces; row 2 grey): CF rest, CF grin, WB rest, "
                  "WB talk", 18, "bold", NOTE))
    svg = write("panel-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "panel-sheet.png")
    sh(svg, png)

    for k, (who, o, lab) in enumerate(exprs):
        hc = head_crop(f"face-{k}", who, o, 1.15)
        x = 30 + k * 300
        comp(png, hc, x + 30, y4 + 30)
        lp = write(f"face-lab-{k}.svg", 280, 24, text(0, 18, lab, 15, "bold"))
        lpp = os.path.join(TMP, f"face-lab-{k}.png")
        sh("-background", "none", lp, lpp)
        comp(png, lpp, x + 30, y4 + 270)
    sils = [silhouette("sil-front", scene(), 0, 0), silhouette("sil-34", scene(), 35, 0),
            silhouette("sil-cam", scene(), CAM[0], CAM[1])]
    xx = sx_
    for one, x4 in sils:
        comp(png, one, xx, y4 + 40)
        xx += Image.open(one).size[0] + 16
    sh(sils[0][0], os.path.join(OUT, "silhouette-64.png"))
    xx = sx_
    yy = y4 + 120
    for n, (one, x4) in enumerate(sils):
        x2 = one.replace("-1x", "-x2")
        sh(one, "-filter", "point", "-resize", "200%", "-bordercolor", INK, "-border", "1", x2)
        comp(png, x2, xx, yy)
        xx += Image.open(x2).size[0] + 14
    lg = [lineup("lu-path-colour", "path"), lineup("lu-path-grey", "path", grey=True),
          lineup("lu-grass-colour", "grass"), lineup("lu-grass-grey", "grass", grey=True)]
    for k, (o1, o2, kk) in enumerate(lg):
        t = os.path.join(TMP, f"lu-fit-{k}.png")
        sh(o1, "-filter", "point", "-resize", "150%", t)
        sh(t, "-resize", "720x", t)
        comp(png, t, 30 + k * 740, y5 + 40)
    poses = [(None, "rest"), ({"cf": {"head_nod": 6, "face": "grin"}}, "nod"),
             ({"wb": {"arms": "point", "face": "talk"}}, "point"), ({"box": {"icon": "mute"}}, "muted"),
             (lean, "lean")]
    for k, (o, lab) in enumerate(poses):
        one, x3 = cam_tile(f"sheet-cam-{k}", o, 200, 184, BG["grass"], kit="grass")
        sh(x3, "-resize", "78%", x3)
        comp(png, x3, 30 + k * 590, y6 + 30)
        comp(png, one, 30 + k * 590, y6 + 30 + 440)
    # face check x3
    fy = y7 + 30
    fl = [("cf", {}, "CF rest"), ("cf", {"cf": {"face": "grin"}}, "CF grin"), ("wb", {}, "WB rest"),
          ("wb", {"wb": {"face": "talk"}}, "WB talk")]
    P0, _ = cam(*CAM)
    for k, (who, o, lab) in enumerate(fl):
        one, _ = cam_tile(f"face-cam-{k}", o, 200, 184, BG["grass"])
        hu, hv, _ = P0(place_f(who)((0, GROUND - 104, 40)))
        cx, cy = int(100 + hu * GS) - 20, int(118 + hv * GS) - 22
        f3 = os.path.join(TMP, f"face-cam-{k}-x3.png")
        sh(one, "-crop", f"40x36+{cx}+{cy}", "+repage", "-filter", "point", "-resize", "300%", f3)
        comp(png, f3, 30 + k * 140, fy)
        g = f3.replace(".png", "-grey.png")
        grey_img(f3, g)
        comp(png, g, 30 + k * 140, fy + 118)
    fcf, fwb = face_check("cf"), face_check("wb")
    fcg, fwt = face_check("cf", "grin"), face_check("wb", "talk")
    fcn = face_check("cf", "grin", nod=6)
    fcl = face_check("cf", "talk", lean=14)
    ftxt = [f"Forehead band at 1x: CF {fcf['band']['left_brow']} / {fcf['band']['centre']} / "
            f"{fcf['band']['right_brow']} px; WB {fwb['band']['left_brow']} / {fwb['band']['centre']} / "
            f"{fwb['band']['right_brow']} px; CF nod down (+6): {fcn['band']['centre']} px; lean 14: {fcl['band']['centre']} px. "
            "Rule: 4 px or more.",
            f"Temples: the lowest side hair is {fcf['temple_above_eye_top_px']} px above the eye top (same cap on both). "
            f"WB flat-top front edge: {fwb['flattop_front_above_hairline_px']} px above the hairline (on the skull).",
            f"Mouths at 1x (w x h px, gap under the eyes): CF smile {fcf['mouth']['w']} x {fcf['mouth']['h']}, "
            f"{fcf['mouth']['below_eye_px']}; CF grin {fcg['mouth']['w']} x {fcg['mouth']['h']}, "
            f"{fcg['mouth']['below_eye_px']}; WB flat {fwb['mouth']['w']} x {fwb['mouth']['h']}, "
            f"{fwb['mouth']['below_eye_px']}; WB talk {fwt['mouth']['w']} x {fwt['mouth']['h']}, {fwt['mouth']['below_eye_px']}.",
            "Every mouth is small (7 px wide at most), centred under the eyes, and never spans the jaw: a mouth, not a "
            "beard band.",
            "The rest lines are sub-pixel at 1x (as Juno v1): in game the idle face should use the TALK mouth at the game "
            "camera (Juno card-7 rule)."]
    for k, ln in enumerate(ftxt):
        i2 = write(f"face-txt-{k}.svg", 2300, 26, text(0, 19, ln, 16, "bold" if k == 3 else "normal"))
        p2 = os.path.join(TMP, f"face-txt-{k}.png")
        sh("-background", "none", i2, p2)
        comp(png, p2, 620, fy + 10 + k * 34)
    json.dump({"cf": fcf, "wb": fwb, "cf_grin": fcg, "wb_talk": fwt, "cf_nod14": fcn, "cf_lean14": fcl,
               "lineup_k": [x[2] for x in lg]}, open(os.path.join(TMP, "facecheck.json"), "w"), indent=1)
    return png


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    print(f"GS {GS:.4f} px/u")
    if "explore" in what:
        print(explore())
    if "bodymap" in what:
        print(body_map())
    if "sheet" in what:
        print(sheet())
