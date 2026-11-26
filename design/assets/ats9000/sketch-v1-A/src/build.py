"""Build explore.png, body-map.png, ats-sheet.png and silhouette-64.png for the ATS-9000.

Run in this folder: python3 build.py [explore] [bodymap] [sheet]
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
TARGET = 1.2 * KIT_PX      # sketch-brief.md "Size"
CAM = (20.0, 42.0)         # sketch-brief.md "Game camera"
CAM_NET = (5.0, 42.0)      # lineup characters turn 15 deg to the camera (ricky/v1/ingame.html L303): 20 - 15
KIT_M = 0.977              # kit/build_report.json (ricky/sketch/ready.md row 3)
KIT_TURN_PX = (53, 1062)   # Kit ink top and sole in kit/turn-front.png (shadow below excluded; measured)

# ---- camera calibration: metres per unit so the metric estimate is 90 px tall in the lineup facing (CAM_NET)
_b = bounds(model(), *CAM_NET)   # calibrate in the lineup facing, as Kit 75 px and Ricky 79 px were measured
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


# ============================================================ EXPLORE
THUMBS = [
    ("1 screen head, top hopper, treads", {}),
    ("2 BMGD: slit, back hopper (hidden)", {"visor": "slit", "hopper": "back", "body": "box", "arm": False}),
    ("3 Viet: screen, treads, stamp, no hopper", {"hopper": "none"}),
    ("4 funnel head (head = hopper)", {"head": "bucket", "hopper": "bucket"}),
    ("5 mailbox: front slot hopper", {"hopper": "slot", "body": "tall", "head_s": 0.8}),
    ("6 big CRT head, top hopper", {"head": "crt"}),
    ("7 side hopper on the shoulder", {"hopper": "side", "antenna": True}),
    ("8 one roller, top hopper", {"base": "roller"}),
    ("9 stub feet, top hopper", {"base": "stubs"}),
    ("10 box body, slit visor, top hopper", {"visor": "slit", "body": "box"}),
]
DIRS = [
    ("A. INBOX BOT (pick)", {}, [
        "Screen face + a funnel on the head top.",
        "At pitch 42 the funnel shows a dark oval:",
        "the 'mouth' that eats CVs, with no human",
        "mouth. Treads + flared body = a stable toy;",
        "the stamp arm breaks the box silhouette."]),
    ("B. MAILBOX BOT", {"hopper": "slot", "body": "tall", "head_s": 0.8}, [
        "Tall body with a front CV slot under a",
        "small screen. The slot sits where a mouth",
        "would be: at 90 px it reads as a grin.",
        "From above the slot is foreshortened",
        "and the head is too small to carry eyes."]),
    ("C. FUNNEL HEAD", {"head": "bucket", "hopper": "bucket"}, [
        "The head IS the hopper: one bold shape.",
        "But a wide open top over a face reads as",
        "a bin: 'your CV goes in the trash' is a",
        "mean joke, and the tone must be kind.",
        "The screen also shrinks inside the taper."]),
]


def explore():
    W, H = 2600, 1900
    i = [text(30, 50, "GHOSTED: ATS-9000, explore (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Illustrator Phase 1-2: local references, 10 rough thumbnails, 3 directions, one pick. "
              "Hand-drawn Bezier profiles extruded to boxes; palette rows only.", 18)]
    ry = 130
    i.append(text(30, ry, "REFERENCES (local only, no web)", 20, "bold", NOTE))
    i.append(text(30, ry + 330, "Mock ATS Tower (02-hub.png): cold blue, boxy", 15))
    i.append(text(400, ry + 330, "ATS Catch (05-ats-catch.png): keywords vs red flags", 15))
    i.append(text(900, ry + 330, "Kit (hero, 0.98 m)", 15))
    i.append(text(1130, ry + 330, "Ricky v1", 15))
    i.append(text(1360, ry + 330, "Ghostie v7", 15))
    i.append(text(1600, ry + 345, "Ricky v1 lineup at the game camera (x2)", 15))
    ty = 520
    i.append(text(30, ty, "THUMBNAILS (10). Top: front, rough. Below: the same at the game camera (x3, 26 m, "
                  "pitch 42, yaw 20, 90 px target).", 20, "bold", NOTE))
    tw = 254
    for n, (lab, o) in enumerate(THUMBS):
        x = 30 + n * tw
        i.append(text(x + 6, ty + 34, lab, 13, "bold"))
        i.append(shadow(x + tw / 2, ty + 272, 70, 7))
        i.append(render(model(o), 0, 0, 0.66, x + tw / 2, ty + 272, 1.8, mark_scale=0.8))
    dy = 1200
    i.append(text(30, dy, "DIRECTIONS (3), developed: front, 3/4, back; then the game camera (x3), ATS left, "
                  "Kit right (real v7 render, same camera)", 20, "bold", NOTE))
    dw = 860
    for n, (lab, o, notes) in enumerate(DIRS):
        x = 30 + n * dw
        i.append(text(x + 10, dy + 40, lab, 20, "bold", NOTE if n == 0 else INK))
        for k, yw in enumerate((0, 35, 180)):
            i.append(shadow(x + 70 + k * 122, dy + 342, 52, 7))
            i.append(render(model(o), yw, 0, 0.5, x + 70 + k * 122, dy + 342, 1.6, mark_scale=0.9))
        for k, ln in enumerate(notes):
            i.append(text(x + 10, dy + 400 + k * 22, ln, 16))
        if n == 0:
            i.append(box(x, dy + 12, x + dw - 20, dy + 530, NOTE, 4))
    i.append(text(30, 1780, "Pick A. Reason: it is the only direction where all three 'reads your CV' parts show at "
                  "the game camera at once: the screen face (front), the hopper mouth (top, seen from pitch 42) and "
                  "the stamp arm (side).", 18, "bold"))
    i.append(text(30, 1808, "It keeps the toy family (soft corners, big head, ink outline, dark base like Kit's "
                  "trousers) and has no human mouth, so it stays literal and kind, not a grinning boss.", 18))
    svg = write("explore.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "explore.png")
    sh(svg, png)
    # references
    r1 = os.path.join(TMP, "ref-hub.png")
    sh(HUB, "-crop", "300x340+820+200", "+repage", "-resize", "x290", r1)
    r2 = os.path.join(TMP, "ref-catch.png")
    sh(CATCH, "-crop", "700x420+290+95", "+repage", "-resize", "x290", r2)
    rk = os.path.join(TMP, "ref-kit.png")
    sh(KIT_FRONT, "-crop", "620x1080+140+20", "+repage", "-resize", "x290", rk)
    rr = os.path.join(TMP, "ref-ricky.png")
    sh(RICKY_FRONT, "-crop", "620x1080+140+20", "+repage", "-resize", "x290", rr)
    rg = os.path.join(TMP, "ref-ghost.png")
    sh(GH_FRONT, "-crop", "620x1080+140+20", "+repage", "-resize", "x290", rg)
    lu = os.path.join(TMP, "ref-lineup.png")
    sh(RK_LINEUP, "-crop", "460x170+660+400", "+repage", "-filter", "point", "-resize", "200%", lu)
    comp(png, r1, 30, ry + 25)
    comp(png, r2, 400, ry + 25)
    comp(png, rk, 880, ry + 25)
    comp(png, rr, 1110, ry + 25)
    comp(png, rg, 1340, ry + 25)
    comp(png, lu, 1600, ry + 15)
    for n, (lab, o) in enumerate(THUMBS):
        _, x3 = cam_png(f"ex-thumb-{n}", o, 76, 112, "#B5D67A")
        comp(png, x3, 30 + n * tw + 13, ty + 290)
    kit3 = os.path.join(TMP, "kit-cam-x3.png")
    sh(GH_LINEUP, "-crop", "76x112+847+398", "+repage", "-filter", "point", "-resize", "300%", kit3)
    for n, (lab, o, notes) in enumerate(DIRS):
        _, x3 = cam_png(f"ex-dir-{n}", o, 76, 112, "#B5D67A")
        comp(png, x3, 30 + n * dw + 380, dy + 60)
        comp(png, kit3, 30 + n * dw + 380 + 236, dy + 60)
    return png


# ============================================================ BODY MAP
def lm_points():
    """3D landmark / attachment points (X, H, Z)."""
    hz = 56
    return {
        "screen": (front_pt(150, 141, hz + 0.5), "screen centre (face zone)"),
        "eye_l": (front_pt(122, LM["eye"], hz + 0.5), "eye"),
        "eye_r": (front_pt(178, LM["eye"], hz + 0.5), "eye"),
        "hopper": (front_pt(150, LM["hop_mouth"], 0), "hopper mouth centre"),
        "hop_base": (front_pt(150, LM["head_top"], 0), "hopper base (on head top)"),
        "ant": (front_pt(ANT_BASE[0], ANT_BASE[1], ANT_BASE[2]), "antenna base"),
        "pivot": (front_pt(HUB_X[0], LM["pivot"], 0), "stamp pivot (shoulder hub)"),
        "neck": (front_pt(150, 191, 30), "neck"),
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
    W, H = 2600, 1720
    i = [text(30, 50, "GHOSTED: ATS-9000 body map v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Decided before the sheet: proportions in head-heights, landmarks for a machine, attachment "
              "points, the joins, and a check at the game camera (26 m, pitch 42, yaw 20).", 18)]
    s = 2.4
    fx, gy0 = 820, 70
    gy = lambda y: gy0 + y * s
    fxx = lambda x: fx + (x - 150) * s
    i.append(text(30, 125, "A. FRONT (upright; units: 1 u = %.2f mm; height %.2f m)" % (M_PER_U * 1000, H_M), 20, "bold", NOTE))
    rows = [("antenna ball top", LM["ant_top"]), ("HOPPER MOUTH (the CV mouth)", LM["hop_mouth"]),
            ("head top = hopper base; antenna base", LM["head_top"]), ("screen top", LM["screen_top"]),
            ("eye line", LM["eye"]), ("scan line rest", LM["scan_rest"]), ("screen bottom", LM["screen_bot"]),
            ("chin = neck top", LM["head_bot"]), ("body top (shoulders)", 198), ("STAMP PIVOT (hub axis)", LM["pivot"]), ("TREAD LINE (body bottom)", LM["body_bot"]), ("axle line (hubs)", LM["axle"]),
            ("ground", LM["ground"])]
    x_end = fxx(300)
    for lab, y in rows:
        i.append(guide(fxx(30), x_end, gy(y)))
        i.append(text(x_end + 8, gy(y) + 5, f"{lab}  y {y}", 15, "bold" if lab.isupper() or "MOUTH" in lab or "PIVOT" in lab or "TREAD" in lab else "normal", NOTE))
    i.append(shadow(fx, gy(342), 170, 14))
    i.append(render(model(), 0, 0, s, fx, gy(GROUND), 4.5))
    # attachment dots on the front view
    P = cam(0, 0)
    for k, (q, lab) in lm_points().items():
        u, v, _ = P(q)
        i.append(dot(fx + u * s, gy(GROUND) + v * s, 6))
    # face zone box
    i.append(box(fxx(84), gy(110), fxx(216), gy(172), "#D93A8C", 2.5))
    i.append(text(fxx(60), gy(372), "pink box = face zone: the screen (eyes + scan line).", 15, "bold", "#D93A8C"))
    i.append(text(fxx(60), gy(372) + 20, "No mouth on the face: the hopper is the mouth.", 15, "bold", "#D93A8C"))
    # width dims
    for (a, b, y, lab) in [(76, 224, 312, "body hem 148 u"), (66, 106, 352, "tread 40 u"),
                           (216, 264, 352, "arm out 48 u")]:
        i.append(f'<path d="M{fxx(a):.1f},{gy(y):.1f} L{fxx(b):.1f},{gy(y):.1f}" stroke="{NOTE}" stroke-width="2"/>')
        i.append(text((fxx(a) + fxx(b)) / 2, gy(y) - 6, lab, 13, "normal", NOTE, "middle"))

    # B. side view with the swing arc
    sx0, sgy0 = 1980, 70
    sgy = lambda y: sgy0 + y * s
    i.append(text(1720, 125, "B. SIDE (robot's left, the stamp side; front = viewer-left)", 20, "bold", NOTE))
    for lab, y in [("hopper mouth", LM["hop_mouth"]), ("head top", 96), ("chin", 184), ("stamp pivot", LM["pivot"]),
                   ("tread line", 304), ("ground", 340)]:
        i.append(guide(sx0 - 230, sx0 + 220, sgy(y)))
        i.append(text(sx0 + 226, sgy(y) + 5, lab, 14, "normal", NOTE))
    i.append(shadow(sx0, sgy(342), 190, 14))
    i.append(render(model(), 90, 0, s, sx0, sgy(GROUND), 4.5))
    pu, pv, _ = cam(90, 0)(front_pt(HUB_X[1], LM["pivot"], 0))
    pcx, pcy = sx0 + pu * s, sgy(GROUND) + pv * s
    i.append(arc(pcx, pcy, 96 * s, 90 + 22, 90 + 150, NOTE))
    i.append(dot(pcx, pcy, 7))
    i.append(text(sx0 - 230, sgy(GROUND) + 64, "stamp swing (dashed): one hinge on the X axis;", 14, "bold", NOTE))
    i.append(text(sx0 - 230, sgy(GROUND) + 84, "rest 22 deg forward, wind-up 150, slam 0", 14, "normal", NOTE))
    tz = cam(90, 0)(front_pt(150, 340, 74))
    i.append(text(sx0 + tz[0] * s - 120, sgy(GROUND) + 40, "tread nose 74 u ahead of the axis (tank nose)", 14, "normal", NOTE))

    # C. table of attachment points
    cy = 1010
    i.append(text(1230, cy, "C. ATTACHMENT POINTS AND JOINS (each one decided; front-view x, y; Z + = front)", 20, "bold", NOTE))
    rows2 = [
        "screen: inset on the head front (Z 56), x 84-216, y 110-172; eyes + scan line live on it (decal / UV)",
        "hopper: turned funnel, base r 36 on the head top centre (y 96), mouth r 58 at y 52, rim 5 u, inside ink",
        "antenna: socket on the head top at the robot's RIGHT corner (x 82, Z -24), stalk tilts out to x 68,",
        "    gold ball r 10 at y 30-50. Clears the hopper rim by 14 u in front view, more in 3D (Z -24)",
        "stamp arm: hub (cylinder, X axis, r 15) on the robot's LEFT side at y 224, x 216-244; bar x 244-258;",
        "    block x 240-264, 54 u long, rubber 8 u (ink). One hinge = the only moving joint in the mesh",
        "neck: short ink block, x 124-176, y 182-200, Z +-30; fixed (the head does not turn)",
        "treads: 2 ink belts, x 66-106 and 194-234, y 304-340, Z -58..74; hubs on the OUTER faces only",
        "body front: plain on purpose (a light name plate under the screen read as a grin at 90 px; dropped)",
        "back: 3 vent lines on the head back, a hatch outline on the body back (so front and back differ)",
    ]
    for k, r in enumerate(rows2):
        i.append(text(1230, cy + 34 + k * 24, r, 15))
    # proportions
    py = cy + 300
    hh = LM["head_bot"] - LM["head_top"]
    i.append(text(1230, py, "D. PROPORTIONS (1 head-height = head box, 88 u = %.0f mm)" % (hh * M_PER_U * 1000), 20, "bold", NOTE))
    props = [("total, ground to antenna ball", GROUND - LM["ant_top"]), ("hopper", LM["head_top"] - LM["hop_mouth"]),
             ("head box", hh), ("neck", 198 - LM["head_bot"]), ("body", LM["body_bot"] - 198),
             ("treads", GROUND - LM["body_bot"]), ("head width", 168), ("body hem width", 148)]
    for k, (lab, u) in enumerate(props):
        i.append(text(1230, py + 32 + k * 24, f"{lab}: {u} u = {u / hh:.2f} heads = {u * M_PER_U:.2f} m", 15))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    # E. game-camera check (x6), both yaws, landmark dots
    ey = 1010
    lab_svg = [text(30, ey, "E. GAME CAMERA CHECK (x5): landmark dots projected with the same camera", 20, "bold", NOTE),
               text(30, ey + 24, "left: yaw 20 (brief); right: yaw 5 (lineup facing, characters turn 15 deg to the camera)", 15, "normal", NOTE)]
    names = []
    for k, yw in enumerate((CAM[0], CAM_NET[0])):
        one, _ = cam_png(f"bm-cam-{int(yw)}", None, 110, 120, "#B5D67A", yw, mark=gamecam_mark)
        x6 = os.path.join(TMP, f"bm-cam-{int(yw)}-x6.png")
        sh(one, "-filter", "point", "-resize", "500%", x6)
        names.append(x6)
    lab = write("bm-labels.svg", W, H, "".join(lab_svg))
    labp = os.path.join(TMP, "bm-labels.png")
    sh("-background", "none", lab, labp)
    comp(png, labp, 0, 0)
    comp(png, names[0], 30, ey + 40)
    comp(png, names[1], 30 + 580, ey + 40)
    # Kit for height (real render scaled to metres)
    kit_px = (KIT_M / M_PER_U) * s
    kk = os.path.join(TMP, "bm-kit.png")
    scale = kit_px / (KIT_TURN_PX[1] - KIT_TURN_PX[0])
    sh(KIT_FRONT, "-resize", f"{scale * 100:.3f}%", kk)
    comp(png, kk, 40, int(gy(GROUND) - KIT_TURN_PX[1] * scale))
    note = write("bm-kitnote.svg", W, H, text(60, gy(GROUND) + 40,
                                              f"Kit (real render) at {KIT_M} m; ATS {H_M:.2f} m", 15, "bold", NOTE))
    notep = os.path.join(TMP, "bm-kitnote.png")
    sh("-background", "none", note, notep)
    comp(png, notep, 0, 0)
    return png


# ============================================================ SHEET
def head_only(parts):
    keep = {"head", "hopper", "socket", "stalk", "ball", "neck"}
    return [p for p in parts if p.name in keep]


def cv_ground():
    """A CV lying on the ground under the stamp (prop for the slam frame)."""
    return prism("cv_ground", ROW[23], "M-30,335 L30,335 L30,338 L-30,338 Z", "zy", 228, 276, bias=-0.5)


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
    W, H = 2800, 2560
    i = [text(30, 50, "GHOSTED: ATS-9000 model sheet v1 (Illustrator, 2026-11-26)", 32, "bold"),
         text(30, 82, "Upright, neutral turnaround. Body map v1 landmarks. Direction A (Inbox Bot). Hand-drawn Bezier "
              "profiles extruded / turned; palette rows only. The stamp arm and antenna sit on opposite sides by design.", 18)]
    s = 1.85
    gy0 = 150
    gy = lambda y: gy0 + y * s
    views = [("FRONT", 0), ("3/4 (front turned to viewer-left)", 35), ("SIDE (facing viewer-left)", 90), ("BACK", 180)]
    cols = [230, 640, 1060, 1480]
    for (lab, yw), cx in zip(views, cols):
        i.append(text(cx - 170, 130, lab, 17, "bold"))
    guides = [("antenna top", LM["ant_top"]), ("hopper mouth", LM["hop_mouth"]), ("head top", LM["head_top"]),
              ("eye line", LM["eye"]), ("chin / neck", LM["head_bot"]), ("stamp pivot", LM["pivot"]),
              ("tread line", LM["body_bot"]), ("ground", LM["ground"])]
    for lab, y in guides:
        i.append(guide(40, 1700, gy(y)))
        i.append(text(1706, gy(y) + 5, lab, 14, "normal", NOTE))
    m = model()
    for (lab, yw), cx in zip(views, cols):
        i.append(shadow(cx, gy(342), 150, 12))
        i.append(render(m, yw, 0, s, cx, gy(GROUND), 3.8))

    # palette
    px, py = 1900, 120
    i.append(text(px, py, "PALETTE (existing rows only, seats/lena-park.md)", 17, "bold"))
    pal = [(18, "body, head, hopper, hub, stamp block"), (22, "ink: outline, screen, treads, neck, rubber, hopper inside"),
           (12, "cream: eyes, scan line (13.3:1 on ink)"), (13, "gold: antenna ball (blink off = x0.62)"),
           (23, "panel: CV prop paper only"), (21, "red-ink: TEXT ONLY, 'NOT A FIT' on the CV (flag)")]
    for k, (r, use) in enumerate(pal):
        y = py + 22 + k * 40
        i.append(f'<path d="M{px},{y} L{px + 30},{y} L{px + 30},{y + 30} L{px},{y + 30} Z" fill="{ROW[r]}" stroke="{INK}" stroke-width="1.5"/>')
        i.append(text(px + 42, y + 21, f"{r} {ROW[r]}  {use}", 15))
    i.append(text(px, py + 270, "Shade: base x 0.85 (neutral grey multiplier). No other colour.", 15))
    i.append(text(px, py + 310, "SHAPE RULES", 17, "bold"))
    rules = ["- Toy machine: soft-cornered boxes, big head,",
             "  3.5 head-heights, %.2f m, ink outline." % H_M,
             "- Face = the screen: 2 cream pill eyes + a cream",
             "  scan line on ink. No mouth anywhere on the face.",
             "- Mouth = the hopper funnel on the head top: from",
             "  the game camera you look into a dark oval.",
             "- Stamp arm on the robot's LEFT (one hinge);",
             "  antenna on the RIGHT top corner (balance).",
             "- Dark ink treads anchor the mid-grey body on",
             "  grass (like Kit's dark trousers).",
             "- Front: screen, plain body. Back: vents + hatch.",
             "- Joins: neck (fixed), hopper base (fixed),",
             "  antenna socket (spring), shoulder hub (hinge),",
             "  treads (fixed; belts and hubs scroll / spin)."]
    for k, r in enumerate(rules):
        i.append(text(px, py + 336 + k * 21, r, 15))
    contrast = [("body 18 vs grass 1", ratio(ROW[18], "#B5D67A")), ("body 18 vs path 3", ratio(ROW[18], "#EBD3A6")),
                ("body 18 vs ink 22", ratio(ROW[18], INK)), ("cream 12 vs ink 22 (eyes)", ratio(ROW[12], INK)),
                ("gold 13 vs body 18", ratio(ROW[13], ROW[18])), ("treads 22 vs grass 1", ratio(INK, "#B5D67A"))]
    for k, (lab, r) in enumerate(contrast):
        i.append(text(px, py + 650 + k * 20, f"{lab}: {r:.2f}:1", 14))

    # motion panels
    my = 930
    i.append(text(30, my, "MOTION PARTS (pose panels; joins in blue)", 20, "bold", NOTE))
    # scan: head close-ups, 3 scan positions
    i.append(text(30, my + 34, "SCAN: the line sweeps the screen top to bottom, eyes go flat (reading)", 15, "bold"))
    for k, sy in enumerate((116, 141, 166)):
        hx = 120 + k * 200
        i.append(render(head_only(model({"expr": "reading", "scan": sy})), 0, 0, 1.0, hx, my + 400, 2.6))
        if k < 2:
            i.append(arrow(hx + 92, my + 220, hx + 112, my + 220))
    i.append(text(30, my + 440, "screen = one decal / UV on the head front; the line scrolls in V", 13, "normal", NOTE))
    # stamp: side view, rest / wind-up / slam
    sx = 690
    i.append(text(sx, my + 34, "STAMP: rest 22 deg, wind-up 150, slam 0 onto the CV ('NOT A FIT')", 15, "bold"))
    for k, (th, lab, cvq) in enumerate([(22, "rest (ready)", False), (150, "wind-up", False), (0, "slam", True)]):
        cxp = sx + 110 + k * 230
        mm = model({"theta": th, "expr": "notfit" if cvq else "idle"})
        if cvq:
            mm.append(cv_ground())
        i.append(shadow(cxp, my + 380, 80, 8))
        i.append(render(mm, 90, 0, 0.95, cxp, my + 380, 2.4))
        pu, pv, _ = cam(90, 0)(front_pt(HUB_X[1], LM["pivot"], 0))
        i.append(dot(cxp + pu * 0.95, my + 380 + pv * 0.95, 4))
        i.append(text(cxp - 40, my + 410, lab, 14))
    i.append(cv_card(sx + 690, my + 150, 1.0))
    i.append(text(sx + 690, my + 330, "the stamped CV (prop)", 13, "normal", NOTE))
    # hopper: 3/4 with a little pitch
    hx0 = 1560
    i.append(text(hx0, my + 34, "HOPPER: a CV drops in; the screen starts reading", 15, "bold"))
    for k, (cv, ex) in enumerate([("above", "idle"), ("half", "idle"), (None, "reading")]):
        cxp = hx0 + 110 + k * 220
        mm = model({"cv": cv, "expr": ex, "scan": 128 if ex == "reading" else LM["scan_rest"]})
        i.append(shadow(cxp, my + 400, 80, 8))
        i.append(render(mm, 25, 24, 0.95, cxp, my + 400, 2.4))
        if k < 2:
            i.append(arrow(cxp + 88, my + 150, cxp + 128, my + 150))
    i.append(text(hx0, my + 440, "pose view: yaw 25, pitch 24 (to see into the mouth)", 13, "normal", NOTE))
    # treads + antenna
    tx0 = 2340
    i.append(text(tx0, my + 34, "TREADS + ANTENNA", 15, "bold"))
    for k, (spin, on) in enumerate([(0, True), (45, False)]):
        cxp = tx0 + 100 + k * 220
        i.append(shadow(cxp, my + 400, 80, 8))
        i.append(render(model({"spin": spin, "ant_on": on}), 35, 0, 0.95, cxp, my + 400, 2.4))
    i.append(text(tx0, my + 430, "hubs spin + belt scrolls; ball blinks", 13, "normal", NOTE))
    i.append(text(tx0, my + 448, "gold (on) / gold x0.62 (off)", 13, "normal", NOTE))

    # screen states
    ey = 1420
    i.append(text(30, ey, "SCREEN STATES (variants; the body never changes)", 20, "bold", NOTE))
    for k, (ex, lab) in enumerate(EXPR.items()):
        hx = 140 + k * 250
        i.append(render(head_only(model({"expr": ex, "scan": 128 if ex == "reading" else (None if ex != "idle" else LM["scan_rest"]),
                                         "antenna": True})), 0, 0, 1.05, hx, ey + 390, 2.6))
        i.append(text(hx - 100, ey + 270, ex, 15, "bold"))
        i.append(text(hx - 100, ey + 290, lab, 13))
    i.append(text(30, ey + 330, "Voice line beat: 'KEYWORD SYNERGY NOT FOUND' = loading -> notfit (soft, sorry eyes), then the stamp. Never angry eyes.", 15))

    # silhouette
    sy0 = 1830
    i.append(text(30, sy0, "64 px SILHOUETTE (front, 3/4, game camera; 1x and x3)", 18, "bold"))
    # lineup
    i.append(text(760, sy0, "LINEUP AT THE GAME CAMERA (x2): ATS estimate on real Ricky v1 grass with Kit, Ricky, 3 Ghosties. "
                  "Colour, then greyscale (Lena's formula).", 18, "bold"))
    # game camera
    i.append(text(2200, sy0, "GAME CAMERA NEXT TO KIT (x3, 1x)", 18, "bold"))
    svg = write("ats-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "ats-sheet.png")
    sh(svg, png)

    # silhouettes
    sil = silhouettes()
    for k, (one, x4) in enumerate(sil):
        comp(png, one, 40 + k * 225, sy0 + 20)
        comp(png, x4, 40 + k * 225, sy0 + 100)
    # lineups
    _, c2 = lineup("lineup-colour")
    _, g2 = lineup("lineup-grey", grey=True)
    comp(png, c2, 760, sy0 + 20)
    comp(png, g2, 760 + 700, sy0 + 20)
    # game camera tiles
    kit3 = os.path.join(TMP, "kit-tile-x3.png")
    kit1 = os.path.join(TMP, "kit-tile-1x.png")
    sh(GH_LINEUP, "-crop", "110x120+831+394", "+repage", kit1)
    sh(kit1, "-filter", "point", "-resize", "300%", kit3)
    a1, a3 = cam_png("sheet-cam-20", None, 110, 120, "#B5D67A", CAM[0])
    b1, b3 = cam_png("sheet-cam-5", None, 110, 120, "#B5D67A", CAM_NET[0])
    comp(png, a3, 2200, sy0 + 20)
    comp(png, kit3, 2200 + 340, sy0 + 20)
    for k, t in enumerate((a1, b1, kit1)):
        comp(png, t, 2210 + k * 130, sy0 + 400)
    hp20, wp20 = measure_px(CAM[0])
    hp5, wp5 = measure_px(CAM_NET[0])
    notes = [f"yaw 5 (lineup facing, as Kit was measured): ATS {hp5} px x {wp5}",
             f"  target 90 = 1.2 x Kit 75. yaw 20 (camera only): {hp20} px x {wp20}",
             f"World height {H_M:.2f} m (Kit 0.98 m). Metric estimate;",
             "Ricky's was 67 px vs 66 px real (ricky/v1/measure.md).",
             "Tiles: x3 ATS yaw 20 | x3 Kit; 1x: yaw 20, yaw 5, Kit."]
    nsvg = write("sheet-camnote.svg", W, H, "".join(text(2200, sy0 + 560 + k * 20, t, 14) for k, t in enumerate(notes)))
    npng = os.path.join(TMP, "sheet-camnote.png")
    sh("-background", "none", nsvg, npng)
    comp(png, npng, 0, 0)
    lsvg = write("sheet-lunote.svg", W, H, "".join(text(760, sy0 + 520 + k * 20, t, 14) for k, t in enumerate([
        f"Kit 75 px, Ricky 79 px (real renders). ATS estimate {hp5} px at yaw 5, on free grass nearer the camera (left of Ricky).",
        f"Grey: body 18 vs grass {ratio(ROW[18], '#B5D67A'):.2f}:1, so the ink outline, the ink treads and the ink screen carry the read.",
        "In grey the ATS reads as a mid-grey box with a dark base and a dark face band: apart from Kit (mid), Ricky (dark), Ghosties (light)."])))
    lpng = os.path.join(TMP, "sheet-lunote.png")
    sh("-background", "none", lsvg, lpng)
    comp(png, lpng, 0, 0)
    return png, (hp20, wp20, hp5, wp5)


def silhouettes():
    out = []
    for name, yw, pt in (("front", 0, 0), ("34", 35, 0), ("cam", CAM[0], CAM[1])):
        m = model()
        x0, y0, x1, y1 = bounds(m, yw, pt)
        sc = 62 / (y1 - y0)
        w = 64
        inner = render(m, yw, pt, sc, w / 2 - (x0 + x1) / 2 * sc, 63 - y1 * sc, 0.5, mono=INK)
        sv = write(f"sil-{name}.svg", w, 64, inner, "#FFFFFF")
        one = os.path.join(TMP, f"sil-{name}-1x.png")
        sh(sv, one)
        x4 = os.path.join(TMP, f"sil-{name}-x3.png")
        sh(one, "-filter", "point", "-resize", "300%", x4)
        out.append((one, x4))
    # the 3-up 1x file
    sh(out[0][0], out[1][0], out[2][0], "+append", os.path.join(OUT, "silhouette-64.png"))
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["explore", "bodymap", "sheet"]
    info = {"M_PER_U": M_PER_U, "height_m": H_M, "proj_height_u": HU}
    if "explore" in what:
        explore()
    if "bodymap" in what:
        body_map()
    if "sheet" in what:
        _, px = sheet()
        info["px"] = px
    print(json.dumps(info))
