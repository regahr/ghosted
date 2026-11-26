"""Build body-map.png, ats-sheet.png and silhouette-64.png for the ATS-9000 v2 (direction B + neck).

Run in this folder: python3 build.py [bodymap] [sheet]   (v1 + explore: assets/ats9000/sketch-v1-A/)
Reads only: kit/turn-front.png, ricky/v1/turn-front.png, ghostie/v7/turn-front.png, ghostie/v7/lineup-grass.png,
ricky/v1/lineup-grass.png, concept/out/shots/02-hub.png and 05-ats-catch.png. Writes only into ../, ./_tmp and ../crops.
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
RUN = os.path.abspath(os.path.join(ASSETS, "..", ".."))
sys.path.insert(0, HERE)
import ats  # noqa
from ats import *  # noqa

TMP = os.path.join(HERE, "_tmp")
CROPS = os.path.join(OUT, "crops")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CROPS, exist_ok=True)

KIT_FRONT = os.path.join(ASSETS, "kit", "turn-front.png")
RICKY_FRONT = os.path.join(ASSETS, "ricky", "v1", "turn-front.png")
GH_FRONT = os.path.join(ASSETS, "ghostie", "v7", "turn-front.png")
GH_LINEUP = os.path.join(ASSETS, "ghostie", "v7", "lineup-grass.png")     # Kit alone (tile crop)
RK_LINEUP = os.path.join(ASSETS, "ricky", "v1", "lineup-grass.png")       # Kit + Ricky + 3 Ghosties
HUB = os.path.join(RUN, "concept", "out", "shots", "02-hub.png")
CATCH = os.path.join(RUN, "concept", "out", "shots", "05-ats-catch.png")

PX_PER_M = 900 / (2 * 26 * math.tan(math.radians(13)))   # kit/ingame.html: fov 26, 26 m, 900 px tall = 74.97
OUTLINE = 1.6
KIT_PX = 75.0              # ricky/v1/measure.md: Kit 75 px (y 424-498) in the lineup
TARGET = 1.21 * KIT_PX     # chair-calls.md 1: 1.21 x Kit, facing the camera (91 px)
CAM = (20.0, 42.0)         # sketch-brief.md "Game camera"
CAM_NET = (5.0, 42.0)      # lineup characters turn 15 deg to the camera (ricky/v1/ingame.html L303): 20 - 15
KIT_M = 0.977              # kit/build_report.json (ricky/sketch/ready.md row 3)
KIT_TURN_PX = (53, 1062)   # Kit ink top and sole in kit/turn-front.png (shadow below excluded; measured)

# ---- camera calibration: metres per unit so the metric estimate is 90 px tall in the lineup facing (CAM_NET)
_b = bounds(model(), *CAM_NET)   # facing the camera (chair call 1), as Kit 75 px and Ricky 79 px were measured
HU = _b[3] - _b[1]
ats.M_PER_U = (TARGET - 2 * OUTLINE) / (PX_PER_M * HU)
M_PER_U = ats.M_PER_U
GS = PX_PER_M * M_PER_U          # game-camera px per unit at 1x
H_M = (GROUND - LM["ant_top"]) * M_PER_U


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


def vguide(x, y0, y1, op=0.55, w=1.5):
    return (f'<path d="M{x:.1f},{y0} L{x:.1f},{y1}" fill="none" stroke="{NOTE}" stroke-width="{w}" '
            f'stroke-opacity="{op}"/>')


def dot(x, y, r=5, c=NOTE):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r}" ry="{r}" fill="{c}" stroke="#FFFFFF" stroke-width="1.5"/>'


def box(x0, y0, x1, y1, c=NOTE, w=3):
    return f'<path d="M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z" fill="none" stroke="{c}" stroke-width="{w}"/>'


def arrow(x0, y0, x1, y1, c=NOTE, w=3):
    a = math.atan2(y1 - y0, x1 - x0)
    hx1, hy1 = x1 - 12 * math.cos(a - 0.45), y1 - 12 * math.sin(a - 0.45)
    hx2, hy2 = x1 - 12 * math.cos(a + 0.45), y1 - 12 * math.sin(a + 0.45)
    return (f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'
            f'<path d="M{hx1:.1f},{hy1:.1f} L{x1:.1f},{y1:.1f} L{hx2:.1f},{hy2:.1f}" fill="none" stroke="{c}" '
            f'stroke-width="{w}" stroke-linejoin="round"/>')


def arc(cx, cy, r, a0, a1, c=NOTE, w=2.5):
    """Arc in screen degrees (0 = right, 90 = down)."""
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / 24)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / 24)))
           for k in range(25)]
    return (f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
            f'" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="7,5"/>')


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
    ys, xs = np.where(a > 40)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


# ============================================================ game-camera tiles
def cam_png(name, opts=None, w=110, h=120, bg=None, yaw=CAM[0], extra=None, mark=None):
    """The ATS at the game camera, 1x pixels, ground centre at (w/2, h-16). Returns (1x path, x3 path)."""
    m = model(opts)
    if extra:
        m += extra
    ox, oy = w / 2, h - 24
    inner = shadow(ox, oy + 2, 26, 9, 0.22) if bg else ""
    inner += render(m, yaw, CAM[1], GS, ox, oy, OUTLINE, mark_scale=1.0)
    if mark:
        inner += mark(ox, oy, yaw)
    sv = write(f"{name}.svg", w, h, inner, bg)
    one = os.path.join(TMP, f"{name}-1x.png")
    if bg:
        sh(sv, one)
    else:
        sh("-background", "none", sv, one)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-filter", "point", "-resize", "300%", x3)
    return one, x3


def measure_px(yaw):
    one, _ = cam_png(f"measure-{int(yaw)}", None, 140, 140, None, yaw)
    x0, y0, x1, y1 = alpha_bbox(one)
    return y1 - y0 + 1, x1 - x0 + 1


LINEUP_BOX = (620, 390, 960, 630)      # crop of ricky/v1/lineup-grass.png (Kit, Ricky, 3 Ghosties)
ATS_SPOT = (770, 604)                  # free grass, left of Ricky, right of the tree (feet centre, full frame)


def lineup(name="lineup", grey=False):
    base = os.path.join(TMP, f"{name}-base.png")
    Image.open(RK_LINEUP).crop(LINEUP_BOX).save(base)
    w, h = 130, 130
    one, _ = cam_png(f"{name}-ats", None, w, h, None, CAM_NET[0])
    shp = write(f"{name}-shadow.svg", w, h, shadow(w / 2, h - 22, 30, 10, 0.28))
    shpng = os.path.join(TMP, f"{name}-shadow.png")
    sh("-background", "none", shp, shpng)
    x = ATS_SPOT[0] - LINEUP_BOX[0] - w / 2
    y = ATS_SPOT[1] - LINEUP_BOX[1] - (h - 24)
    comp(base, shpng, x, y)
    comp(base, one, x, y)
    out1 = os.path.join(TMP, f"{name}-1x.png")
    sh(base, out1)
    if grey:
        grey_img(out1, out1)
    out2 = os.path.join(TMP, f"{name}-x2.png")
    sh(out1, "-filter", "point", "-resize", "200%", out2)
    return out1, out2


# ============================================================ BODY MAP
def lm_points():
    """3D landmark / attachment points (X, H, Z)."""
    hz = HEAD_Z + 0.5
    return {
        "screen": (front_pt(150, 105, hz), "screen centre (face zone)"),
        "eye_l": (front_pt(EYE_X[0], LM["eye"], hz), "eye"),
        "eye_r": (front_pt(EYE_X[1], LM["eye"], hz), "eye"),
        "neck_top": (front_pt(150, 159, 26.5), "neck top ring"),
        "neck_bot": (front_pt(150, 189, 26.5), "neck bottom ring"),
        "slot": (front_pt(150, LM["slot"], BODY_Z + 0.5), "CV slot centre (the mouth)"),
        "ant": (front_pt(ANT_BASE[0], ANT_BASE[1], ANT_BASE[2]), "antenna base"),
        "pivot": (front_pt(HUB_X[1], LM["pivot"], 0), "stamp pivot (shoulder hub)"),
        "tread_l": (front_pt(86, 322, 74), "tread nose (axle line)"),
        "tread_r": (front_pt(214, 322, 74), "tread nose (axle line)"),
    }


def gamecam_mark(ox, oy, yaw):
    out = []
    for k, (q, lab) in lm_points().items():
        u, v = project(q, yaw, CAM[1])
        out.append(f'<ellipse cx="{ox + u * GS:.2f}" cy="{oy + v * GS:.2f}" rx="1.3" ry="1.3" fill="#E0E0FF" '
                   f'stroke="{NOTE}" stroke-width="0.8"/>')
    return "".join(out)


def body_map():
    W, H = 2600, 1810
    i = [text(30, 50, "GHOSTED: ATS-9000 body map v2, direction B 'Mailbox Bot' + neck (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Rega ts 1795628417.229379: 'B looks cool to me, just need to give it a neck'. Proportions in "
              "head-heights, landmarks, attachment points, joins, and a check at the game camera (26 m, pitch 42).", 18)]
    s = 2.3
    fx, gy0 = 820, 140
    gy = lambda y: gy0 + y * s
    fxx = lambda x: fx + (x - 150) * s
    i.append(text(30, 125, "A. FRONT (upright; units: 1 u = %.2f mm; height %.2f m)" % (M_PER_U * 1000, H_M), 20, "bold", NOTE))
    rows = [("antenna ball top", LM["ant_top"]), ("head top; antenna base", LM["head_top"]),
            ("screen top", LM["screen_top"]), ("eye line", LM["eye"]), ("scan line rest", LM["scan_rest"]),
            ("screen bottom", LM["screen_bot"]), ("CHIN = NECK TOP", LM["head_bot"]),
            ("NECK BOTTOM = body crown", LM["neck_bot"]), ("STAMP PIVOT (hub axis)", LM["pivot"]),
            ("CV SLOT (the mouth)", LM["slot"]), ("TREAD LINE (body bottom)", LM["body_bot"]),
            ("axle line (hubs)", LM["axle"]), ("ground", LM["ground"])]
    x_end = fxx(300)
    for lab, y in rows:
        i.append(guide(fxx(30), x_end, gy(y)))
        i.append(text(x_end + 8, gy(y) + 5, f"{lab}  y {y}", 15, "bold" if lab.split()[0].isupper() else "normal", NOTE))
    i.append(shadow(fx, gy(342), 170, 14))
    i.append(render(model(), 0, 0, s, fx, gy(GROUND), 4.5))
    P = cam(0, 0)
    for k, (q, lab) in lm_points().items():
        u, v, _ = P(q)
        i.append(dot(fx + u * s, gy(GROUND) + v * s, 6))
    i.append(box(fxx(80), gy(74), fxx(220), gy(136), "#D93A8C", 2.5))
    i.append(box(fxx(100), gy(238), fxx(200), gy(256), "#D93A8C", 2.5))
    i.append(text(fxx(60), gy(372), "pink boxes: face zone = the screen (eyes + scan line); mouth = the CV slot.", 15, "bold", "#D93A8C"))
    i.append(text(fxx(60), gy(372) + 20, "The neck is a bellows: 3 ink rings on a grey core, 50 u tall (0.56 heads).", 15, "bold", "#D93A8C"))
    for (a, b, y, lab) in [(76, 224, 312, "body hem 150 u"), (66, 106, 352, "tread 40 u"), (212, 266, 352, "arm out 54 u"),
                           (62, 238, 56, "head 176 u")]:
        i.append(f'<path d="M{fxx(a):.1f},{gy(y):.1f} L{fxx(b):.1f},{gy(y):.1f}" stroke="{NOTE}" stroke-width="2"/>')
        i.append(text((fxx(a) + fxx(b)) / 2, gy(y) - 6, lab, 13, "normal", NOTE, "middle"))

    # B. side view with the swing arc
    sx0, sgy0 = 1980, 140
    sgy = lambda y: sgy0 + y * s
    i.append(text(1720, 125, "B. SIDE (robot's left, the stamp side; front = viewer-left)", 20, "bold", NOTE))
    for lab, y in [("head top", LM["head_top"]), ("chin = neck top", LM["head_bot"]), ("neck bottom", LM["neck_bot"]),
                   ("stamp pivot", LM["pivot"]), ("slot", LM["slot"]), ("tread line", 304), ("ground", 340)]:
        i.append(guide(sx0 - 230, sx0 + 220, sgy(y)))
        i.append(text(sx0 + 226, sgy(y) + 5, lab, 14, "normal", NOTE))
    i.append(shadow(sx0, sgy(342), 190, 14))
    i.append(render(model(), 90, 0, s, sx0, sgy(GROUND), 4.5))
    pu, pv, _ = cam(90, 0)(front_pt(HUB_X[1], LM["pivot"], 0))
    pcx, pcy = sx0 + pu * s, sgy(GROUND) + pv * s
    i.append(arc(pcx, pcy, 99 * s, 90 + SLAM_DEG, 90 + WIND_DEG, NOTE))
    i.append(dot(pcx, pcy, 7))
    i.append(text(sx0 - 230, sgy(GROUND) + 64, "stamp swing (dashed): one hinge on the X axis;", 14, "bold", NOTE))
    i.append(text(sx0 - 230, sgy(GROUND) + 84, f"rest {REST_DEG:.0f} deg forward, wind-up {WIND_DEG:.0f}, slam {SLAM_DEG:.0f}", 14, "normal", NOTE))
    i.append(text(sx0 - 230, sgy(GROUND) + 104, "head depth +-34 u: a shallow monitor, so the neck shows from above", 14, "normal", NOTE))

    cy = 1110
    i.append(text(1230, cy, "C. ATTACHMENT POINTS AND JOINS (each one decided; front-view x, y; Z + = front)", 20, "bold", NOTE))
    rows2 = [
        "screen: inset on the head front (Z 34), x 80-220, y 74-136; eyes 20 x 30 u at x 120 / 180, y 102 (decal / UV)",
        "neck: bellows on the body crown, centred: grey core r 17, y 146-206 (into head and body);",
        "    3 INK rings r 26, 8 u tall, at y 155-163, 170-178, 185-193. Fixed (no head turn); optional squash bob",
        "slot (the mouth): ink inset on the body front (Z 50), x 102-198, y 240-254; lip tray under it, Z 44-62",
        "antenna: socket on the head top, robot's RIGHT corner (x 80, Z -16); stalk tilts out to x 66, y 22; gold ball r 10",
        f"stamp arm: hub (X axis, r 15) on the robot's LEFT side, y 224, x 212-246; bar x 246-260; block x 242-266;",
        f"    rubber 8 u ink. ONE hinge. Rest {REST_DEG:.0f} deg (chair call 3), wind-up {WIND_DEG:.0f}, slam {SLAM_DEG:.0f} onto the CV",
        "treads: 2 ink belts, x 66-106 and 194-234, y 304-340, Z -58..74; hubs on the OUTER faces only",
        "body: mailbox arch, crown y 200, sides from y 240, hem x 75-225 at y 304, Z +-50",
        "back: 3 vent lines on the head back, a hatch outline on the body back (front and back never mix)",
    ]
    for k, r in enumerate(rows2):
        i.append(text(1230, cy + 34 + k * 24, r, 15))
    py = cy + 300
    hh = LM["head_bot"] - LM["head_top"]
    i.append(text(1230, py, "D. PROPORTIONS (1 head-height = head box, %d u = %.0f mm)" % (hh, hh * M_PER_U * 1000), 20, "bold", NOTE))
    props = [("total, ground to antenna ball", GROUND - LM["ant_top"]), ("head box", hh),
             ("neck", LM["neck_bot"] - LM["head_bot"]), ("body (crown to hem)", LM["body_bot"] - LM["neck_bot"]),
             ("treads", GROUND - LM["body_bot"]), ("head width", 176), ("body hem width", 150)]
    for k, (lab, u) in enumerate(props):
        i.append(text(1230, py + 32 + k * 24, f"{lab}: {u} u = {u / hh:.2f} heads = {u * M_PER_U:.2f} m", 15))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    ey = 1110
    lab_svg = [text(30, ey, "E. GAME CAMERA CHECK (x5): landmark dots projected with the same camera", 20, "bold", NOTE),
               text(30, ey + 24, "left: facing the camera (net yaw 5, chair call 1); right: turned (yaw 20)", 15, "normal", NOTE)]
    names = []
    for yw in (CAM_NET[0], CAM[0]):
        one, _ = cam_png(f"bm-cam-{int(yw)}", None, 110, 128, "#B5D67A", yw, mark=gamecam_mark)
        x5 = os.path.join(TMP, f"bm-cam-{int(yw)}-x5.png")
        sh(one, "-filter", "point", "-resize", "500%", x5)
        names.append(x5)
    lab = write("bm-labels.svg", W, H, "".join(lab_svg))
    labp = os.path.join(TMP, "bm-labels.png")
    sh("-background", "none", lab, labp)
    comp(png, labp, 0, 0)
    comp(png, names[0], 30, ey + 40)
    comp(png, names[1], 30 + 580, ey + 40)
    kit_px = (KIT_M / M_PER_U) * s
    kk = os.path.join(TMP, "bm-kit.png")
    scale = kit_px / (KIT_TURN_PX[1] - KIT_TURN_PX[0])
    sh(KIT_FRONT, "-resize", f"{scale * 100:.3f}%", kk)
    comp(png, kk, 40, int(gy(GROUND) - KIT_TURN_PX[1] * scale))
    note = write("bm-kitnote.svg", W, H, text(60, gy(GROUND) + 40, f"Kit (real render) at {KIT_M} m; ATS {H_M:.2f} m",
                                              15, "bold", NOTE))
    notep = os.path.join(TMP, "bm-kitnote.png")
    sh("-background", "none", note, notep)
    comp(png, notep, 0, 0)
    return png


# ============================================================ SHEET
def head_only(parts):
    return [p for p in parts if p.name in {"head", "socket", "stalk", "ball"}]


def cv_ground():
    """A CV lying on the ground under the stamp (prop for the slam frame)."""
    return prism("cv_ground", ROW[23], "M-30,335 L30,335 L30,338 L-30,338 Z", "zy", 230, 278, bias=-0.5)


def cv_card(x, y, s=1.0):
    """The stamped CV, flat, front-on: panel paper, ink lines, red-ink TEXT 'NOT A FIT' (text use only)."""
    o = [f'<path d="M{x},{y} L{x + 120 * s},{y} L{x + 120 * s},{y + 156 * s} L{x},{y + 156 * s} Z" fill="{ROW[23]}" '
         f'stroke="{INK}" stroke-width="3"/>']
    for k in range(7):
        o.append(f'<path d="M{x + 14 * s},{y + (20 + 18 * k) * s} L{x + (106 - 20 * (k % 2)) * s},{y + (20 + 18 * k) * s}" '
                 f'stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    cx, cy = x + 60 * s, y + 92 * s
    o.append(f'<path d="M{cx - 54 * s},{cy - 16 * s} L{cx + 54 * s},{cy - 24 * s} L{cx + 56 * s},{cy + 8 * s} '
             f'L{cx - 52 * s},{cy + 16 * s} Z" fill="none" stroke="{ROW[21]}" stroke-width="3.5"/>')
    o.append(f'<text x="{cx}" y="{cy + 3 * s}" font-family="Helvetica" font-size="{17 * s:.1f}" font-weight="bold" '
             f'fill="{ROW[21]}" text-anchor="middle" transform="rotate(-4 {cx} {cy})">NOT A FIT</text>')
    return "".join(o)


def sheet():
    W, H = 2800, 2640
    i = [text(30, 50, "GHOSTED: ATS-9000 model sheet v2, direction B 'Mailbox Bot' + neck (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral turnaround. Body map v2 landmarks. Hand-drawn Bezier profiles extruded / turned; "
              "palette rows only. The stamp arm and antenna sit on opposite sides by design.", 18)]
    s = 1.75
    gy0 = 150
    gy = lambda y: gy0 + y * s
    views = [("FRONT", 0), ("3/4 (front turned to viewer-left)", 35), ("SIDE (facing viewer-left)", 90), ("BACK", 180)]
    cols = [230, 640, 1060, 1480]
    for (lab, yw), cx in zip(views, cols):
        i.append(text(cx - 170, 130, lab, 17, "bold"))
    guides = [("antenna top", LM["ant_top"]), ("head top", LM["head_top"]), ("eye line", LM["eye"]),
              ("chin = neck top", LM["head_bot"]), ("neck bottom", LM["neck_bot"]), ("stamp pivot", LM["pivot"]),
              ("CV slot", LM["slot"]), ("tread line", LM["body_bot"]), ("ground", LM["ground"])]
    for lab, y in guides:
        i.append(guide(40, 1700, gy(y)))
        i.append(text(1706, gy(y) + 5, lab, 14, "normal", NOTE))
    m = model()
    for (lab, yw), cx in zip(views, cols):
        i.append(shadow(cx, gy(342), 150, 12))
        i.append(render(m, yw, 0, s, cx, gy(GROUND), 3.8))

    px, py = 1900, 120
    i.append(text(px, py, "PALETTE (v1 rows, seats/lena-park.md)", 17, "bold"))
    pal = [(18, "body, head, neck core, slot lip, hub, stamp block"),
           (22, "ink: outline, screen, slot, neck bellows, treads, rubber"),
           (12, "cream: eyes, scan line (13.3:1 on ink)"), (13, "gold: antenna ball (blink off = x0.62)"),
           (23, "panel: CV prop paper only"), (21, "red-ink: TEXT ONLY, 'NOT A FIT' on the CV (chair call 2)")]
    for k, (r, use) in enumerate(pal):
        y = py + 22 + k * 40
        i.append(f'<path d="M{px},{y} L{px + 30},{y} L{px + 30},{y + 30} L{px},{y + 30} Z" fill="{ROW[r]}" stroke="{INK}" stroke-width="1.5"/>')
        i.append(text(px + 42, y + 21, f"{r} {ROW[r]}  {use}", 15))
    i.append(text(px, py + 270, "Shade: base x 0.85 (neutral grey multiplier). No other colour.", 15))
    i.append(text(px, py + 310, "SHAPE RULES", 17, "bold"))
    rules = ["- Mailbox Bot: monitor head on an accordion neck,",
             "  on a mailbox-arch body, on ink treads; %.2f m." % H_M,
             "- Face = the screen: 2 cream pill eyes + a cream",
             "  scan line on ink. Head grown to 176 x 90 u.",
             "- Mouth = the CV slot on the body front, with a",
             "  lip tray. It may read as a grin (Rega: fine).",
             "- NECK: bellows, 3 ink rings on a grey core, 50 u.",
             "  Head only 68 u deep, so it shows from pitch 42.",
             "- Stamp arm on the robot's LEFT (one hinge), rest",
             "  45 deg; antenna on the RIGHT top corner.",
             "- Front: screen + slot. Back: vents + hatch.",
             "- Joins: neck (fixed; rings may bob), antenna",
             "  socket (spring), shoulder hub (hinge), treads",
             "  (fixed; belts and hubs scroll / spin).",
             "- 3D: bevel box edges ~0.02 m (chair call 5)."]
    for k, r in enumerate(rules):
        i.append(text(px, py + 336 + k * 21, r, 15))
    contrast = [("body 18 vs grass 1", ratio(ROW[18], "#B5D67A")), ("body 18 vs path 3", ratio(ROW[18], "#EBD3A6")),
                ("body 18 vs ink 22 (head/body vs neck)", ratio(ROW[18], INK)),
                ("cream 12 vs ink 22 (eyes)", ratio(ROW[12], INK)),
                ("gold 13 vs body 18", ratio(ROW[13], ROW[18])), ("treads 22 vs grass 1", ratio(INK, "#B5D67A"))]
    for k, (lab, r) in enumerate(contrast):
        i.append(text(px, py + 670 + k * 20, f"{lab}: {r:.2f}:1", 14))

    my = 960
    i.append(text(30, my, "MOTION PARTS (pose panels; joins in blue)", 20, "bold", NOTE))
    i.append(text(30, my + 34, "SCAN: the line sweeps the screen top to bottom, eyes go flat (reading)", 15, "bold"))
    for k, sy in enumerate((80, 105, 130)):
        hx = 120 + k * 200
        i.append(render(head_only(model({"expr": "reading", "scan": sy})), 0, 0, 1.0, hx, my + 400, 2.6))
        if k < 2:
            i.append(arrow(hx + 92, my + 160, hx + 112, my + 160))
    i.append(text(30, my + 260, "screen = one decal / UV on the head front; the line scrolls in V", 13, "normal", NOTE))
    sx = 690
    i.append(text(sx, my + 34, f"STAMP: rest {REST_DEG:.0f} deg, wind-up {WIND_DEG:.0f}, slam {SLAM_DEG:.0f} onto the CV ('NOT A FIT')", 15, "bold"))
    for k, (th, lab, cvq) in enumerate([(REST_DEG, "rest (ready)", False), (WIND_DEG, "wind-up", False), (SLAM_DEG, "slam", True)]):
        cxp = sx + 110 + k * 230
        mm = model({"theta": th, "expr": "notfit" if cvq else "idle"})
        if cvq:
            mm.append(cv_ground())
        i.append(shadow(cxp, my + 400, 80, 8))
        i.append(render(mm, 90, 0, 0.95, cxp, my + 400, 2.4))
        pu, pv, _ = cam(90, 0)(front_pt(HUB_X[1], LM["pivot"], 0))
        i.append(dot(cxp + pu * 0.95, my + 400 + pv * 0.95, 4))
        i.append(text(cxp - 40, my + 430, lab, 14))
    i.append(cv_card(sx + 690, my + 150, 1.0))
    i.append(text(sx + 690, my + 330, "the stamped CV (prop)", 13, "normal", NOTE))
    hx0 = 1560
    i.append(text(hx0, my + 34, "SLOT: a CV slides into the slot; the screen starts reading", 15, "bold"))
    for k, (cv, ex) in enumerate([("out", "idle"), ("half", "idle"), (None, "reading")]):
        cxp = hx0 + 110 + k * 220
        mm = model({"cv": cv, "expr": ex, "scan": 92 if ex == "reading" else LM["scan_rest"]})
        i.append(shadow(cxp, my + 410, 80, 8))
        i.append(render(mm, 25, 24, 0.95, cxp, my + 410, 2.4))
        if k < 2:
            i.append(arrow(cxp + 88, my + 150, cxp + 128, my + 150))
    i.append(text(hx0, my + 450, "pose view: yaw 25, pitch 24 (to see the sheet on the lip)", 13, "normal", NOTE))
    tx0 = 2340
    i.append(text(tx0, my + 34, "TREADS + ANTENNA", 15, "bold"))
    for k, (spin, on) in enumerate([(0, True), (45, False)]):
        cxp = tx0 + 100 + k * 220
        i.append(shadow(cxp, my + 410, 80, 8))
        i.append(render(model({"spin": spin, "ant_on": on}), 35, 0, 0.95, cxp, my + 410, 2.4))
    i.append(text(tx0, my + 440, "hubs spin + belt scrolls; ball blinks", 13, "normal", NOTE))
    i.append(text(tx0, my + 458, "gold (on) / gold x0.62 (off)", 13, "normal", NOTE))

    ey = 1450
    i.append(text(30, ey, "SCREEN STATES (variants; the body never changes; never angry)", 20, "bold", NOTE))
    for k, (ex, lab) in enumerate(EXPR.items()):
        hx = 140 + k * 250
        sc_ = 92 if ex == "reading" else (LM["scan_rest"] if ex == "idle" else None)
        i.append(render(head_only(model({"expr": ex, "scan": sc_})), 0, 0, 1.05, hx, ey + 410, 2.6))
        i.append(text(hx - 100, ey + 270, ex, 15, "bold"))
        i.append(text(hx - 100, ey + 290, lab, 13))
    i.append(text(30, ey + 330, "Voice line beat: 'KEYWORD SYNERGY NOT FOUND' = loading -> notfit (soft, sorry eyes), then the stamp. Never angry eyes.", 15))

    sy0 = 1840
    i.append(text(30, sy0, "64 px SILHOUETTE (front, 3/4, game camera; 1x and x3)", 18, "bold"))
    i.append(text(760, sy0, "LINEUP AT THE GAME CAMERA (x2): ATS estimate on real Ricky v1 grass with Kit, Ricky, 3 Ghosties. "
                  "Colour, then greyscale (Lena's formula).", 18, "bold"))
    i.append(text(2200, sy0, "GAME CAMERA NEXT TO KIT (x3, 1x)", 18, "bold"))
    svg = write("ats-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "ats-sheet.png")
    sh(svg, png)

    sil = silhouettes()
    for k, (one, x3) in enumerate(sil):
        comp(png, one, 40 + k * 225, sy0 + 20)
        comp(png, x3, 40 + k * 225, sy0 + 100)
    _, c2 = lineup("lineup-colour")
    _, g2 = lineup("lineup-grey", grey=True)
    comp(png, c2, 760, sy0 + 20)
    comp(png, g2, 760 + 700, sy0 + 20)
    kit3 = os.path.join(TMP, "kit-tile-x3.png")
    kit1 = os.path.join(TMP, "kit-tile-1x.png")
    sh(GH_LINEUP, "-crop", "110x128+831+390", "+repage", kit1)
    sh(kit1, "-filter", "point", "-resize", "300%", kit3)
    a1, a3 = cam_png("sheet-cam-5", None, 110, 128, "#B5D67A", CAM_NET[0])
    b1, b3 = cam_png("sheet-cam-20", None, 110, 128, "#B5D67A", CAM[0])
    comp(png, a3, 2200, sy0 + 20)
    comp(png, kit3, 2200 + 340, sy0 + 20)
    for k, t in enumerate((a1, b1, kit1)):
        comp(png, t, 2210 + k * 130, sy0 + 424)
    hp20, wp20 = measure_px(CAM[0])
    hp5, wp5 = measure_px(CAM_NET[0])
    notes = [f"Facing the camera (net yaw 5, chair call 1): ATS {hp5} px x {wp5};",
             f"  target 91 = 1.21 x Kit 75. Turned (yaw 20): {hp20} px x {wp20}.",
             f"World height {H_M:.2f} m (Kit 0.98 m). Metric estimate;",
             "Ricky's was 67 px vs 66 px real (ricky/v1/measure.md).",
             "Tiles: x3 ATS facing | x3 Kit; 1x: facing, yaw 20, Kit."]
    nsvg = write("sheet-camnote.svg", W, H, "".join(text(2200, sy0 + 580 + k * 20, t, 14) for k, t in enumerate(notes)))
    npng = os.path.join(TMP, "sheet-camnote.png")
    sh("-background", "none", nsvg, npng)
    comp(png, npng, 0, 0)
    lsvg = write("sheet-lunote.svg", W, H, "".join(text(760, sy0 + 520 + k * 20, t, 14) for k, t in enumerate([
        f"Kit 75 px, Ricky 79 px (real renders). ATS estimate {hp5} px facing the camera, on free grass nearer the camera (left of Ricky).",
        f"Grey: body 18 vs grass {ratio(ROW[18], '#B5D67A'):.2f}:1, so the ink outline, the ink treads, the ink screen and the slot carry the read.",
        "In grey: a mid-grey head and body split by the dark neck band, a dark face band, a dark slot, a dark base."])))
    lpng = os.path.join(TMP, "sheet-lunote.png")
    sh("-background", "none", lsvg, lpng)
    comp(png, lpng, 0, 0)
    return png, (hp20, wp20, hp5, wp5)


def silhouettes():
    out = []
    for name, yw, pt in (("front", 0, 0), ("34", 35, 0), ("cam", CAM_NET[0], CAM[1])):
        m = model()
        x0, y0, x1, y1 = bounds(m, yw, pt)
        sc = 62 / (y1 - y0)
        w = 64
        inner = render(m, yw, pt, sc, w / 2 - (x0 + x1) / 2 * sc, 63 - y1 * sc, 0.5, mono=INK)
        sv = write(f"sil-{name}.svg", w, 64, inner, "#FFFFFF")
        one = os.path.join(TMP, f"sil-{name}-1x.png")
        sh(sv, one)
        x3 = os.path.join(TMP, f"sil-{name}-x3.png")
        sh(one, "-filter", "point", "-resize", "300%", x3)
        out.append((one, x3))
    sh(out[0][0], out[1][0], out[2][0], "+append", os.path.join(OUT, "silhouette-64.png"))
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["bodymap", "sheet"]
    info = {"M_PER_U": M_PER_U, "height_m": H_M, "proj_height_u": HU}
    if "bodymap" in what:
        body_map()
    if "sheet" in what:
        _, px = sheet()
        info["px"] = px
    print(json.dumps(info))
