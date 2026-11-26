"""Build body-map.png, ghostie-sheet.png, tie-options.png and silhouette-64.png (sketch v2).

Run in this folder: python3 build.py [bodymap] [sheet] [tie]
Reads only v5/lineup-grass-crop-x3.png and kit/hero.png. Writes only into ../ and ./ (and ./_tmp).
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ghost import *  # noqa
import camera as cam  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
V5 = os.path.join(OUT, "..", "v5")
KIT = os.path.join(OUT, "..", "..", "kit", "hero.png")
LINEUP = os.path.join(V5, "lineup-grass-crop-x3.png")
TMP = os.path.join(HERE, "_tmp")
os.makedirs(TMP, exist_ok=True)

K = 0.142          # px per unit at 1x: v5 ghost is 125 px tall in the x3 crop (41.7 px at 1x), model H 293
OUTLINE_PX = 1.6   # v5/ingame.html line 196


def sh(*a):
    subprocess.run(["magick", *a], check=True)


def write(name, w, h, inner, bg=None):
    p = os.path.join(HERE, name)
    open(p, "w").write(svg_doc(w, h, inner, bg))
    return p


def comp(base, over, x, y):
    sh(base, over, "-geometry", f"+{int(x)}+{int(y)}", "-composite", base)


def guide(x0, x1, y, dash=False, op=0.6):
    da = ' stroke-dasharray="6,5"' if dash else ""
    return (f'<path d="M{x0},{y:.1f} L{x1},{y:.1f}" fill="none" stroke="{NOTE}" stroke-width="1.5" '
            f'stroke-opacity="{op}"{da}/>')


# ============================================================ game-camera estimate
def cam_svg(variant="tie", yaw=cam.YAW, eye=None, neck=None, mark=False, scale=K):
    """The ghost at the game camera, in 1x pixels, centred on (0, 0) = mid of the silhouette."""
    eye = LM["eye"] if eye is None else eye
    neck = LM["neck"] if neck is None else neck
    L = cam.landmarks(yaw, eye)
    mid = (L["top"] + L["bottom"]) / 2

    def S(fn):
        return lambda x, y: tuple(c * scale for c in (fn(x, y)[0], fn(x, y)[1] - mid))

    surf = S(lambda x, y: cam.on_surface(x, y, yaw))
    slc = S(lambda x, y: cam.on_slice(x, y, yaw))
    dome = cam.map_path(cam.dome_hull(yaw), lambda u, v: (u * scale, (v - mid) * scale))
    body = cam.map_path(FRONT_BODY, slc)
    ow = OUTLINE_PX * 2
    o = [path(dome, INK, INK, ow), path(body, INK, INK, ow), path(dome, BODY), path(body, BODY)]
    for (x, y) in [(124, eye), (176, eye)]:
        o.append(path(cam.map_path(oval_path(x, y, 8.5, 13), surf), INK))
    tw = 3.75 * scale       # tie ink is geometry: it scales with the tie
    if variant == "tie":
        for c in collar_paths(150, neck):
            o.append(path(cam.map_path(c, surf), BODY, INK, 2.75 * scale))
        k, b = tie_paths(150, neck + 4)
        o.append(path(cam.map_path(b, surf), TIE, INK, tw))
        o.append(path(cam.map_path(k, surf), TIE, INK, tw))
    elif variant == "glasses":
        for (x, y) in [(124, eye), (176, eye)]:
            o.append(path(cam.map_path(oval_path(x, y, 17, 18), surf), "none", ACC, 5.5 * scale))
    elif variant == "headset":
        o.append(path(cam.map_path(HEADSET_BAND, slc), "none", ACC, 9 * scale))
        for x in LM["ear_x"]:
            o.append(path(cam.map_path(oval_path(x, eye + 2, 12, 19), slc), ACC, INK, 3 * scale))
    if mark:
        x0, y0, x1, y1 = 132, eye + 18, 168, neck - 6
        zone = f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z"
        o.append(path(cam.map_path(zone, surf), "none", NOTE, 0.6))
    return "".join(o)


def cam_tile(name, variant="tie", w=60, h=60, bg=GRASS, **kw):
    """1x tile, plus x3 nearest (same as v5 make_sheets.py line 46)."""
    inner = (f'<ellipse cx="{w / 2}" cy="{h / 2 + 18}" rx="12" ry="3" fill="#2B1E16" '
             f'fill-opacity="0.18" stroke="none"/>'
             f'<g transform="translate({w / 2},{h / 2 - 2})">{cam_svg(variant, **kw)}</g>')
    sv = write(f"{name}.svg", w, h, inner, bg)
    one = os.path.join(TMP, f"{name}-1x.png")
    sh(sv, one)
    x3 = os.path.join(TMP, f"{name}-x3.png")
    sh(one, "-scale", "300%", x3)
    return one, x3


def kit_crops():
    kg = os.path.join(TMP, "kit-game-x3.png")
    sh(LINEUP, "-crop", "180x270+590+60", "+repage", kg)
    kg1 = os.path.join(TMP, "kit-game-1x.png")
    sh(kg, "-sample", "33.3333%", kg1)
    v5g = os.path.join(TMP, "v5-ghost-x3.png")
    sh(LINEUP, "-crop", "150x160+90+15", "+repage", v5g)
    return kg, kg1, v5g


# ============================================================ BODY MAP
def body_map():
    W, H = 2500, 1900
    i = [text(30, 50, "GHOSTED: Ghostie body map v2 (Illustrator, 2026-11-25)", 32, "bold"),
         text(30, 82, "Decided before the sketch: proportions, landmarks, attachment points, the empty mouth "
              "zone, and a 2D estimate at the game camera (26 m, pitch 42, yaw 20).", 18)]

    # ---- A. explore: 8 thumbnails (eye line x neck line) at the game camera
    ax, ay = 30, 130
    i.append(text(ax, ay, "A. EXPLORE: 8 thumbnails at the game camera (x3). Eye line from v5 (150) up to 104; "
                  "neck 48 or 64 units under the eye line.", 20, "bold", NOTE))
    combos = [(150, 48), (134, 48), (118, 48), (104, 48), (150, 64), (134, 64), (118, 64), (104, 64)]
    for n, (e, g) in enumerate(combos):
        tx = ax + n * 200
        L = cam.landmarks(cam.YAW, e)
        frac = (L["eye_l"][1] - L["top"]) / (L["bottom"] - L["top"])
        knot = cam.on_surface(150, e + g + 4, cam.YAW)[1]
        gap = (knot - L["eye_l"][1]) * K
        lab = f"eye {e}, neck +{g}"
        i.append(text(tx + 5, ay + 30, lab, 15, "bold"))
        i.append(text(tx + 5, ay + 250, f"eyes at {frac * 100:.0f}% down", 15))
        i.append(text(tx + 5, ay + 270, f"knot {gap:.1f} px under eyes", 15))
    i.append(text(ax + 1610, ay + 70, "Pick: eye 118, neck +48", 18, "bold", NOTE))
    i.append(text(ax + 1610, ay + 94, "- face sits high (eyes 47% down", 15))
    i.append(text(ax + 1610, ay + 114, "  at the camera; v5 was 56%)", 15))
    i.append(text(ax + 1610, ay + 134, "- a clear gap for the empty", 15))
    i.append(text(ax + 1610, ay + 154, "  mouth zone above the collar", 15))
    i.append(text(ax + 1610, ay + 174, "- 104 crowds the crown and the", 15))
    i.append(text(ax + 1610, ay + 194, "  headset band; +64 pushes the", 15))
    i.append(text(ax + 1610, ay + 214, "  tie into the arm and hem zone", 15))
    pick = 2
    i.append(path(f"M{ax + pick * 200 - 2},{ay + 8} L{ax + pick * 200 + 190},{ay + 8} "
                  f"L{ax + pick * 200 + 190},{ay + 280} L{ax + pick * 200 - 2},{ay + 280} Z",
                  "none", NOTE, 4))

    # ---- B. front body map (large)
    bx, by, bs = 60, 520, 2.6
    i.append(text(30, by - 20, "B. FRONT LANDMARKS (upright, symmetric). Units: front-view units, "
                  "body 265 crown-to-hem.", 20, "bold", NOTE))
    gy = lambda y: by - 60 + y * bs
    x_end = bx + 300 * bs + 40
    rows = [("crown", LM["crown"]), ("eye line + ear points", LM["eye"]),
            ("neck line (collar top)", LM["neck"]), ("arm root top (soft shoulder)", LM["arm_top"]),
            ("chest", LM["chest"]), ("arm root bottom", LM["arm_bottom"]), ("tie V point", LM["tie_v"]),
            ("hem (lobe cusps)", LM["hem"])]
    for lab, y in rows:
        i.append(guide(bx - 20, x_end, gy(y)))
        dy = {"tie V point": -9, "arm root bottom": 19}.get(lab, 5)
        i.append(text(x_end + 10, gy(y) + dy, f"{lab}  y {y}", 16, "bold" if "eye" in lab or "neck" in lab else "normal", NOTE))
    i.append(place(front("tie"), bx, by - 60, bs))
    # ear points
    for x in LM["ear_x"]:
        i.append(ellipse(bx + x * bs, gy(LM["eye"]), 9, 9, NOTE))
    # mouth zone
    x0, y0, x1, y1 = LM["mouth"]
    i.append(f'<path d="M{bx + x0 * bs},{gy(y0)} L{bx + x1 * bs},{gy(y0)} L{bx + x1 * bs},{gy(y1)} '
             f'L{bx + x0 * bs},{gy(y1)} Z" fill="none" stroke="{NOTE}" stroke-width="3" stroke-dasharray="8,6"/>')
    # head-height ruler on the left
    rx = 30
    hh = LM["neck"] - LM["crown"]
    for k_, (y0_, y1_) in enumerate([(LM["crown"], LM["neck"]), (LM["neck"], LM["neck"] + hh)]):
        yA, yB = gy(y0_), gy(min(y1_, 316))
        i.append(path(f"M{rx},{yA} L{rx},{yB}", "none", NOTE, 3))
        i.append(path(f"M{rx - 8},{yA} L{rx + 8},{yA}", "none", NOTE, 3))
    i.append(path(f"M{rx - 8},{gy(316)} L{rx + 8},{gy(316)}", "none", NOTE, 3))
    i.append(text(rx + 6, gy((LM["crown"] + LM["neck"]) / 2) - 30, "1 head", 14, "bold", NOTE))
    i.append(text(rx + 6, gy(LM["neck"] + 28) - 4, "2nd", 14, "bold", NOTE))
    i.append(text(rx + 6, gy(LM["neck"] + 28) + 12, "head", 14, "bold", NOTE))

    # ---- B notes (right of the big ghost)
    nx = x_end + 300
    notes = ["PROPORTIONS", "Head = crown to neck line = 130 units.",
             "Whole body = crown to lowest hem lobe",
             "  = 280 units = 2.15 head-heights.",
             "Width at the arm roots 208 (1.6 hh);",
             "  arms reach 2.15 hh tip to tip. v5 size kept.",
             "", "LANDMARKS",
             "Eye line y 118 (v5 150): 30% down the body.",
             "Ear points: on the eye line, at the side",
             "  edges (x 56 and 244). No ear shapes.",
             "Mouth zone (dashed): x 132-168, y 136-160.",
             "  ALWAYS EMPTY. No mouth, ever.",
             "Neck line y 166: a small centred collar.",
             "  The collar and the knot sit BELOW the",
             "  mouth zone.",
             "Chest: y 186-258, centre. The tie lies here.",
             "Arm roots: y 190-260, soft shoulder on top",
             "  and below; arm tips below the eye bottom",
             "  (y 131) at rest and in the wave.",
             "Hem: 5 soft lobes round the body; 3 seen",
             "  from the front, a notch centred at the back."]
    for k_, ln in enumerate(notes):
        bold = ln in ("PROPORTIONS", "LANDMARKS")
        i.append(text(nx, by + 20 + k_ * 24, ln, 17, "bold" if bold else "normal", NOTE if bold else INK))

    # ---- C. attachment points
    cx_, cy_, cs = 30, 1330, 1.05
    i.append(text(cx_, cy_ - 20, "C. ATTACHMENT POINTS (blue dots)", 20, "bold", NOTE))
    att = [("headset: band centred over", "the crown, a cup on each ear point", front("headset"),
            [(56, LM["eye"]), (244, LM["eye"]), (150, 46)]),
           ("tie: centred, hangs from", "the collar at the neck line", front("tie"),
            [(150, LM["neck"])]),
           ("glasses: on the eye line,", "a rim round each eye", front("glasses"),
            [(124, LM["eye"]), (176, LM["eye"])])]
    for n, (l1, l2, v, dots) in enumerate(att):
        x = cx_ + n * 340
        i.append(text(x + 10, cy_ + 12, l1, 16, "bold"))
        i.append(text(x + 10, cy_ + 32, l2, 16))
        i.append(place(v, x, cy_ + 40, cs))
        for (px_, py_) in dots:
            i.append(ellipse(x + px_ * cs, cy_ + 40 + py_ * cs, 6, 6, NOTE))
    # side landmarks
    sx_ = cx_ + 3 * 340 + 20
    i.append(text(sx_ + 10, cy_ + 12, "side: the same lines;", 16, "bold"))
    i.append(text(sx_ + 10, cy_ + 32, "tie and collar inside the outline", 16))
    for y in (LM["eye"], LM["neck"], LM["hem"]):
        i.append(guide(sx_, sx_ + 300 * cs, cy_ + 40 + y * cs))
    i.append(place(side("tie"), sx_, cy_ + 40, cs))

    # ---- D. game camera estimate
    dx_, dy_ = 1440, 1330
    i.append(text(dx_, dy_ - 20, "D. GAME-CAMERA ESTIMATE (x3; tile 3 also at 1x, right)", 20, "bold", NOTE))
    i.append(text(dx_, dy_ + 260, "1 v5 crop  2 model on the v5 eye line  3 body map v2 (tie; blue box = mouth zone)", 15))
    i.append(text(dx_, dy_ + 282, "4 headset  5 glasses. Model check: v5 eyes measured 56% down the ghost", 15))
    i.append(text(dx_, dy_ + 304, "(lineup crop, ink bbox y 33-158, eyes y 99-107); model gives 55%.", 15))
    knot_gap = (cam.on_surface(150, LM["knot"])[1] - cam.landmarks()["eye_l"][1]) * K
    vpt = (cam.on_surface(150, LM["tie_v"])[1] - cam.landmarks()["eye_l"][1]) * K
    i.append(text(dx_, dy_ + 338, f"Knot top lands {knot_gap:.1f} px (1x) under the eye dots; the V point "
                  f"{vpt:.1f} px under them.", 16, "bold"))
    i.append(text(dx_, dy_ + 360, "Opinion: the centred tie is a vertical lilac stripe under the face. It is", 16))
    i.append(text(dx_, dy_ + 382, "the one risk to the no-mouth read; Viet's real render must prove it.", 16))
    svg = write("body-map.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "body-map.png")
    sh(svg, png)

    # paste the 8 exploration tiles
    for n, (e, g) in enumerate(combos):
        _, x3 = cam_tile(f"bm-explore-{n}", "tie", eye=e, neck=e + g, mark=True)
        comp(png, x3, ax + n * 200 + 5, ay + 45)
    # D tiles
    kg, kg1, v5g = kit_crops()
    tiles = [("bm-v5model", dict(eye=150, neck=150 + 48)), ("bm-tie", dict(mark=True)),
             ("bm-headset", dict()), ("bm-glasses", dict())]
    v5s = os.path.join(TMP, "v5-ghost-sq.png")
    sh(v5g, "-gravity", "center", "-background", GRASS, "-extent", "180x180", v5s)
    comp(png, v5s, dx_, dy_ + 20)
    xs = [dx_ + 190, dx_ + 380, dx_ + 570, dx_ + 760]
    for n, (name, kw) in enumerate(tiles):
        var = {"bm-headset": "headset", "bm-glasses": "glasses"}.get(name, "tie")
        one, x3 = cam_tile(name, var, **kw)
        comp(png, x3, xs[n], dy_ + 20)
        if name == "bm-tie":
            comp(png, one, dx_ + 965, dy_ + 80)
    sh(png, "-font", "Helvetica", "-pointsize", "14", "-fill", NOTE, "-annotate",
       f"+{dx_ + 958}+{dy_ + 72}", "3 at 1x", png)
    for n, x in enumerate([dx_] + xs):
        sh(png, "-font", "Helvetica-Bold", "-pointsize", "18", "-fill", NOTE, "-annotate",
           f"+{x + 6}+{dy_ + 222}", str(n + 1), png)
    return png


# ============================================================ MODEL SHEET
def sheet():
    W, H = 2600, 1960
    i = [text(30, 50, "GHOSTED: Ghostie model sheet v2 (Illustrator, 2026-11-25)", 32, "bold"),
         text(30, 82, "Upright, neutral, symmetric turnaround. Body map v2 landmarks. Tie centred under a "
              "collar. Hand-drawn Bezier curves; palette rows 16, 27, 10, 22 only.", 18)]
    y1, s1 = 140, 1.38
    views = [("FRONT", front("tie")), ("3/4 (front turned to viewer-left)", three_quarter("tie")),
             ("SIDE (arm_L toward viewer)", side("tie")), ("BACK (notch centred on the hem)", back())]
    for yy, lab in [(36, "crown"), (118, "eye line"), (166, "neck line"), (238, "arm tips"), (301, "hem")]:
        gyy = y1 + 20 + yy * s1
        i.append(guide(30, 1860, gyy, op=0.45))
        i.append(text(1870, gyy + 5, lab, 15, "normal", NOTE))
    for k_, (lab, v) in enumerate(views):
        x = 30 + k_ * 460
        i.append(text(x + 10, y1, lab, 19, "bold"))
        i.append(shadow(x, y1 + 20, s1))
        i.append(place(v, x, y1 + 20, s1))

    # palette + rules column
    px = 2010
    i.append(text(px, y1, "PALETTE (only these)", 20, "bold"))
    for k_, (hexv, lab) in enumerate([(BODY, "16 body #F8F4EA"), (ACC, "27 glasses, headset #C8C0D8"),
                                      (TIE, "10 tie #C9A6D6"), (INK, "22 ink #2B1E16")]):
        yy = y1 + 20 + k_ * 46
        i.append(path(f"M{px},{yy} L{px + 40},{yy} L{px + 40},{yy + 34} L{px},{yy + 34} Z", hexv, INK, 2))
        i.append(text(px + 52, yy + 23, lab, 17))
    rules = ["SHAPE RULES", "- Shade: neutral band, body x0.94.", "- Dome: one smooth arc, symmetric.",
             "- Shoulders: the side bends out into", "  each arm; soft curve on top and below.",
             "- Arm tips below the eye bottom, at", "  rest and in the wave.",
             "- Hem: 5 soft lobes round the body.", "- Eyes: two tall ink ovals, y 118.",
             "- NO MOUTH. The mouth zone stays", "  empty in every view and variant.",
             "- Accessories sit where the real", "  object sits: cups on the ears,", "  tie under a collar, glasses on eyes."]
    for k_, ln in enumerate(rules):
        i.append(text(px, y1 + 230 + k_ * 23, ln, 16, "bold" if k_ == 0 else "normal"))

    # row 2: variants, wave, rest pose
    y2, s2 = 800, 1.1
    i.append(text(30, y2 - 20, "VARIANTS (swap parts; same body)", 21, "bold", NOTE))
    var = [("tie: centred, under a collar", front("tie")), ("glasses: round rims on the eyes", front("glasses")),
           ("headset: band centred, 2 cups", front("headset"))]
    for k_, (lab, v) in enumerate(var):
        x = 30 + k_ * 380
        i.append(text(x + 10, y2 + 12, lab, 17, "bold"))
        i.append(shadow(x, y2 + 30, s2))
        i.append(place(v, x, y2 + 30, s2))
    xw = 1200
    i.append(text(xw + 10, y2 - 20, "WAVE (upright): arm_L 0 to +40 deg", 21, "bold", NOTE))
    i.append(shadow(xw + 90, y2 + 30, s2))
    i.append(place(front("tie"), xw + 90, y2 + 30, s2).replace(
        f'fill="{BODY}" stroke="{INK}" stroke-width="5"', f'fill="none" stroke="{NOTE}" stroke-opacity="0.3" stroke-width="5"', 1))
    i.append(place(front("tie", body=FRONT_WAVE), xw + 90, y2 + 30, s2))
    bx = xw + 40
    i.append(path(f"M{bx},{y2 + 140} L{bx},{y2 + 260}", "none", NOTE, 3))
    i.append(path(f"M{bx},{y2 + 128} L{bx - 7},{y2 + 143} L{bx + 7},{y2 + 143} Z", NOTE, NOTE, 1))
    i.append(path(f"M{bx},{y2 + 272} L{bx - 7},{y2 + 257} L{bx + 7},{y2 + 257} Z", NOTE, NOTE, 1))
    i.append(text(xw + 10, y2 + 300, "float", 15, "bold", NOTE))
    i.append(text(xw + 10, y2 + 318, "bob", 15, "bold", NOTE))
    ax_ = xw + 90 + 300 * s2 + 40
    i.append(text(ax_, y2 + 200, "+40 deg", 16, "bold", NOTE))
    i.append(text(ax_, y2 + 220, "faint blue", 14, "normal", NOTE))
    i.append(text(ax_, y2 + 238, "= rest", 14, "normal", NOTE))
    xr = 1840
    i.append(text(xr + 10, y2 - 20, "REST POSE (in game only)", 21, "bold", NOTE))
    i.append(text(xr + 10, y2 + 12, "4 deg tilt; arm_R droops lower", 16))
    i.append(shadow(xr, y2 + 30, s2))
    i.append(place(rest_pose("tie"), xr, y2 + 30, s2, -4))

    # row 3
    y3 = 1430
    i.append(text(30, y3 - 14, "64 px SILHOUETTE (1x, x4)", 20, "bold", NOTE))
    i.append(text(620, y3 - 14, "GAME CAMERA ESTIMATE x3 (26 m, pitch 42, yaw 20), next to Kit", 20, "bold", NOTE))
    i.append(text(1640, y3 - 14, "TIE BUILD SPEC (front-view units)", 20, "bold", NOTE))
    tsx, tsy, ts = 1640, y3 + 10, 2.0
    i.append(path(f"M{tsx},{tsy} L{tsx + 380},{tsy} L{tsx + 380},{tsy + 420} L{tsx},{tsy + 420} Z", BODY, INK, 2))
    i.append(f'<g transform="translate({tsx + 190 - 150 * ts},{tsy + 30 - 150 * ts})"><g transform="scale({ts})">'
             f'{tie_svg(150, 5)}</g></g>')
    spec = ["Centred on the body axis (x 150).",
            "Collar: 2 flat wings, span 46, top on",
            "  the neck line y 166; body colour,",
            "  thin ink; inside the outline.",
            "Knot: trapezoid 18 > 12 wide, 14 tall,",
            "  top y 170.",
            "Blade: 10 at the knot, 28 at the V",
            "  shoulders, 74 long, symmetric V,",
            "  point at y 258.",
            "Ink: a closed line round knot, blade,",
            "  V and collar.",
            "Budget: cap 68 tris (Viet). The v5",
            "  tie was 39; wings add about 12-16.",
            "Drop the collar wings first if over."]
    for k_, ln in enumerate(spec):
        i.append(text(2040, y3 + 30 + k_ * 23, ln, 15))
    svg = write("ghostie-sheet.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "ghostie-sheet.png")
    sh(svg, png)

    sil = f'<g transform="translate(3,0) scale(0.193)">{front("tie", silhouette=True)}</g>'
    sv = write("silhouette-64.svg", 64, 64, sil, "#FFFFFF")
    s1x = os.path.join(OUT, "silhouette-64.png")
    sh(sv, s1x)
    s4 = os.path.join(TMP, "sil-x4.png")
    sh(s1x, "-scale", "400%", "-bordercolor", INK, "-border", "1", s4)
    comp(png, s1x, 40, y3 + 10)
    comp(png, s4, 130, y3 + 10)

    kg, kg1, v5g = kit_crops()
    for k_, var_ in enumerate(["tie", "glasses", "headset"]):
        one, x3 = cam_tile(f"sheet-cam-{var_}", var_)
        comp(png, x3, 620 + k_ * 190, y3 + 10)
        comp(png, one, 620 + k_ * 190 + 60, y3 + 215)
    comp(png, kg, 620 + 3 * 190, y3 + 10)
    sh(png, "-font", "Helvetica", "-pointsize", "16", "-fill", INK,
       "-annotate", f"+620+{y3 + 312}", "tie, glasses, headset (2D estimate), then Kit from v5/lineup-grass-crop-x3.png.",
       "-annotate", f"+620+{y3 + 334}", "1x below each. Viet's real render replaces these estimates.", png)
    return png


# ============================================================ TIE SHEET
def tie_sheet():
    W, H = 1500, 1080
    i = [text(30, 46, "GHOSTED: Ghostie tie, centred under a collar (sketch v2), next to Kit", 28, "bold"),
         text(30, 76, "Upright front view at card scale; close-up; 2D game-camera estimate (x3, with the "
              "mouth zone as a blue box; 1x).", 17)]
    i.append(text(40, 120, "Ghostie: tie centred", 21, "bold"))
    i.append(shadow(30, 140, 1.3))
    i.append(place(front("tie"), 30, 140, 1.3))
    i.append(text(780, 120, "Kit (reference, locked)", 21, "bold"))
    i.append(text(30, 640, "Close-up (x2.4 of card)", 18, "bold", NOTE))
    i.append(text(30, 960, "Ghostie: card read - knot under a collar, blade widens, V point, ink all round,", 16))
    i.append(text(30, 982, "hangs straight down the centre like Kit's. Game camera (estimate): the knot is 7 px (1x)", 16))
    i.append(text(30, 1004, "under the eye dots, only 1-2 px clear. Opinion: in this estimate the centred tie reads", 16))
    i.append(text(30, 1026, "like a tongue under the eyes. Viet's real render decides (bodymap-brief, next steps).", 16))
    i.append(text(780, 960, "Kit: assets/kit/hero.png (card, close-up);", 16))
    i.append(text(780, 982, "v5/lineup-grass-crop-x3.png (game camera).", 16))
    svg = write("tie-options.svg", W, H, "".join(i), CREAM)
    png = os.path.join(OUT, "tie-options.png")
    sh(svg, png)
    s = 2.4
    cx, cy = 150, 214
    body = (f'<g transform="translate({210 - cx * s},{140 - cy * s}) scale({s})">{front("tie")}</g>')
    sv = write("tie-close.svg", 420, 280, body, CREAM)
    pn = os.path.join(TMP, "tie-close.png")
    sh(sv, pn)
    sh(pn, "-bordercolor", INK, "-border", "2", pn)
    comp(png, pn, 30, 655)
    kc = os.path.join(TMP, "kit-close.png")
    sh(KIT, "-crop", "296x197+387+564", "+repage", "-resize", "420x280!", "-bordercolor", INK, "-border", "2", kc)
    comp(png, kc, 780, 655)
    kcard = os.path.join(TMP, "kit-card.png")
    sh(KIT, "-crop", "820x880+190+230", "+repage", "-resize", "420x450", kcard)
    comp(png, kcard, 780, 140)
    one, x3 = cam_tile("tie-cam", "tie")
    _, x3m = cam_tile("tie-cam-mark", "tie", mark=True)
    # x3 clean and x3 marked side by side, 1x under them
    sh(png, x3, "-geometry", "+470+140", "-composite", png)
    sh(png, x3m, "-geometry", "+470+330", "-composite", png)
    sh(png, one, "-geometry", "+540+530", "-composite", png)
    kg, kg1, _ = kit_crops()
    sh(png, kg, "-geometry", "+1230+655", "-composite", png)
    sh(png, kg1, "-geometry", "+1250+140", "-composite", png)
    sh(png, "-font", "Helvetica", "-pointsize", "15", "-fill", NOTE,
       "-annotate", "+470+132", "game cam x3", "-annotate", "+470+322", "x3, mouth zone",
       "-annotate", "+520+522", "1x", "-annotate", "+1230+647", "Kit, game cam x3",
       "-annotate", "+1250+132", "Kit 1x", png)
    return png


if __name__ == "__main__":
    which = sys.argv[1:] or ["bodymap", "sheet", "tie"]
    if "bodymap" in which:
        print(body_map())
    if "sheet" in which:
        print(sheet())
    if "tie" in which:
        print(tie_sheet())
