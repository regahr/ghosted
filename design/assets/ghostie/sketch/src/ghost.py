"""Ghostie sketch v2 parts. Every shape is a hand-written cubic Bezier path.

Python only places the hand-drawn paths on the sheet and writes SVG files.
Local frame of one view: 300 x 340 units, body axis x 150, crown y 36,
hem cusps y 301 (front). Landmarks (body map v2) are in LM below.
"""
import re

BODY = "#F8F4EA"   # row 16
ACC = "#C8C0D8"    # row 27
TIE = "#C9A6D6"    # row 10
INK = "#2B1E16"    # row 22
SHADE = "#E9E5DC"  # body x 0.94, neutral (bodymap-brief "Decided needs")
CREAM = "#FDE6C8"  # card background, sampled from v5/hero.png
GRASS = "#BDD662"  # ground, acceptance/ghostie/v3/lena-park.md line 24
NOTE = "#1D63C8"   # notes and guides (not a character colour)

# ---------------------------------------------------------------- body map landmarks (front view, y down)
LM = {
    "crown": 36,
    "eye": 118,          # eye line (v5: 150). Ear points sit on it at the side edges.
    "eye_bottom": 131,
    "mouth": (132, 136, 168, 160),   # empty mouth zone x0, y0, x1, y1
    "neck": 166,         # neck line = collar top
    "knot": 170,         # knot top
    "arm_top": 190,      # arm root, top (shoulder)
    "arm_bottom": 260,   # arm root, bottom
    "chest": 214,
    "tie_v": 258,
    "hem": 301,
    "ear_x": (56, 244),  # side edges on the eye line
}
EYES = [(124, 118), (176, 118)]

# ---------------------------------------------------------------- front, upright, symmetric
# Right half (viewer-right = arm_L, +x), then the mirror of it for the left half.
FRONT_BODY = (
    "M150,36 "
    "C204,36 242,72 244,134 "
    "C245,160 246,178 252,190 "      # soft shoulder: the side bends out into the arm
    "C258,202 270,212 278,220 "      # arm top (the v5 mesh droop, about 22 deg, both arms)
    "C288,228 290,246 276,247 "      # round tip
    "C264,247 256,250 254,260 "      # underside turns down into the side (soft)
    "C253,270 256,280 262,292 "
    "C266,310 216,318 188,301 "      # hem lobe (5 lobes round; 3 seen)
    "C172,316 128,316 112,301 "      # centre lobe
    "C84,318 34,310 38,292 "
    "C44,280 47,270 46,260 "         # mirror of the right half from here
    "C44,250 36,247 24,247 "
    "C10,246 12,228 22,220 "
    "C30,212 42,202 48,190 "
    "C54,178 55,160 56,134 "
    "C58,72 96,36 150,36 Z"
)
# Back: same outline, hem phase turned so a notch sits on the centre (5 lobes; Viet, sketch-viet.md §2).
BACK_BODY = FRONT_BODY.replace(
    "C266,310 216,318 188,301 C172,316 128,316 112,301 C84,318 34,310 38,292 ",
    "C266,310 236,314 206,300 C194,314 164,316 150,302 C136,316 106,314 94,300 C64,314 34,310 38,292 ")

# Wave (upright): arm_L lifted +40 deg from its rest, from the same soft shoulder.
FRONT_WAVE = FRONT_BODY.replace(
    "C245,160 246,178 252,190 "
    "C258,202 270,212 278,220 "
    "C288,228 290,246 276,247 "
    "C264,247 256,250 254,260 "
    "C253,270 256,280 262,292 ",
    "C245,152 247,166 252,176 "
    "C257,186 270,178 282,174 "
    "C296,170 302,190 290,196 "
    "C278,202 262,212 256,226 "
    "C252,236 256,272 262,292 ")

# Rest pose (its own panel): arm_R (viewer-left) droops more; the whole body tilts 4 deg.
FRONT_REST = FRONT_BODY.replace(
    "C44,250 36,247 24,247 "
    "C10,246 12,228 22,220 "
    "C30,212 42,202 48,190 ",
    "C44,250 38,256 30,262 "
    "C18,270 6,256 14,244 "
    "C22,232 40,206 48,190 ")

FRONT_SHADE = (  # neutral band inside the viewer-left side
    "M72,104 C63,140 61,190 62,232 C64,260 68,278 74,290 "
    "C64,290 52,288 44,282 C47,262 52,232 55,190 C57,160 60,128 72,104 Z"
)

# ---------------------------------------------------------------- 3/4 (front turned to the viewer-left, upright)
Q_BODY = (
    "M140,36 "
    "C196,36 236,74 240,138 "
    "C241,160 243,176 249,188 "      # near soft shoulder
    "C256,202 268,212 276,220 "
    "C286,228 288,246 274,247 "
    "C262,247 254,250 252,260 "
    "C252,270 254,282 258,292 "
    "C262,310 206,320 184,298 "
    "C166,320 122,318 106,296 "
    "C92,314 56,310 52,292 "
    "C49,270 47,244 49,222 "         # far arm hidden behind the body; side stays convex
    "C51,196 54,166 56,136 "
    "C60,72 92,36 140,36 Z"
)
Q_SHADE = (
    "M68,104 C60,150 58,206 62,250 C64,272 68,290 76,302 "
    "C64,300 56,298 54,290 C54,250 55,200 57,160 C58,136 61,118 68,104 Z"
)
Q_EYES = [(98, 118), (148, 118)]
Q_AXIS = 123   # the body's front centre line in the 3/4 view

# ---------------------------------------------------------------- side (upright, facing viewer-left)
S_BODY = (
    "M150,36 "
    "C204,36 232,78 232,140 "
    "C232,196 236,252 240,294 "
    "C234,312 208,314 194,300 "
    "C180,316 120,316 106,300 "
    "C92,314 66,312 60,294 "
    "C64,252 68,196 68,140 "
    "C68,78 96,36 150,36 Z"
)
S_SHADE = (
    "M206,84 C220,124 224,196 228,250 C230,274 232,288 236,298 "
    "C228,304 220,304 212,300 C212,240 212,170 206,84 Z"
)
S_ARM = (  # arm_L seen end-on: a closed soft bulge (the 3D hull draws a loop here)
    "M152,206 C170,206 180,214 180,224 C180,234 168,240 152,240 "
    "C136,240 124,234 124,224 C124,214 134,206 152,206 Z"
)
S_ARM_SHADE = "M128,228 C138,236 166,236 177,228 C174,236 164,239 152,239 C140,239 132,235 128,228 Z"

# ---------------------------------------------------------------- helpers
def ellipse(cx, cy, rx, ry, fill, stroke=None, sw=0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ' stroke="none"'
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{st}{extra}/>'


def path(d, fill, stroke=None, sw=0, extra=""):
    st = (f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
          f' stroke-linecap="round"') if stroke else ' stroke="none"'
    return f'<path d="{d}" fill="{fill}"{st}{extra}/>'


def oval_path(cx, cy, rx, ry):
    """An ellipse as 4 Bezier arcs (so it can be projected point by point)."""
    k = 0.5523
    return (f"M{cx},{cy - ry} C{cx + k * rx},{cy - ry} {cx + rx},{cy - k * ry} {cx + rx},{cy} "
            f"C{cx + rx},{cy + k * ry} {cx + k * rx},{cy + ry} {cx},{cy + ry} "
            f"C{cx - k * rx},{cy + ry} {cx - rx},{cy + k * ry} {cx - rx},{cy} "
            f"C{cx - rx},{cy - k * ry} {cx - k * rx},{cy - ry} {cx},{cy - ry} Z")


# ---------------------------------------------------------------- tie + collar (centred, hangs from the neck line)
def collar_paths(cx, y, sx=1.0):
    """Two small collar wings lying flat on the body, points down, inside the outline."""
    def w(s):
        return (f"M{cx + s * 2 * sx},{y + 2} C{cx + s * 9 * sx},{y} {cx + s * 16 * sx},{y - 1} {cx + s * 23 * sx},{y} "
                f"C{cx + s * 22 * sx},{y + 6} {cx + s * 20 * sx},{y + 12} {cx + s * 17 * sx},{y + 17} "
                f"C{cx + s * 12 * sx},{y + 13} {cx + s * 7 * sx},{y + 10} {cx + s * 4 * sx},{y + 8} "
                f"C{cx + s * 3 * sx},{y + 6} {cx + s * 2 * sx},{y + 4} {cx + s * 2 * sx},{y + 2} Z")
    return [w(-1), w(1)]


def tie_paths(cx, y, sx=1.0):
    """Knot (trapezoid) + blade that widens + symmetric V. Kit-like; length 88."""
    knot = (f"M{cx - 9 * sx},{y} L{cx + 9 * sx},{y} L{cx + 6 * sx},{y + 14} L{cx - 6 * sx},{y + 14} Z")
    blade = (f"M{cx - 5 * sx},{y + 15} "
             f"C{cx - 7 * sx},{y + 34} {cx - 11 * sx},{y + 54} {cx - 14 * sx},{y + 70} "
             f"L{cx},{y + 88} L{cx + 14 * sx},{y + 70} "
             f"C{cx + 11 * sx},{y + 54} {cx + 7 * sx},{y + 34} {cx + 5 * sx},{y + 15} Z")
    return knot, blade


def tie_svg(cx=150, sw=5, sx=1.0, neck=None):
    neck = LM["neck"] if neck is None else neck
    y = neck + 4
    out = [path(c, BODY, INK, sw * 0.55) for c in collar_paths(cx, neck, sx)]
    k, b = tie_paths(cx, y, sx)
    out += [path(b, TIE, INK, sw * 0.75), path(k, TIE, INK, sw * 0.75)]
    return "".join(out)


def glasses_svg(eyes, sw=5, r=(17, 17)):
    (x1, y1), (x2, y2) = eyes
    out = [ellipse(x1, y1, r[0], r[0] + 1, "none", ACC, 5.5),
           ellipse(x2, y2, r[1], r[1] + 1, "none", ACC, 5.5)]
    a, b = x1 + r[0], x2 - r[1]
    out.append(path(f"M{a},{y1 - 3} C{a + 5},{y1 - 8} {b - 5},{y2 - 8} {b},{y2 - 3}", "none", ACC, 4.5))
    return "".join(out)


HEADSET_BAND = "M58,118 C58,66 98,46 150,46 C202,46 242,66 242,118"   # over the crown, centred


def headset_svg(sw=5):
    out = [path(HEADSET_BAND, "none", ACC, 9)]
    for x in LM["ear_x"]:
        out.append(ellipse(x, LM["eye"] + 2, 12, 19, ACC, INK, sw * 0.6))
    return "".join(out)


# ---------------------------------------------------------------- views
def eyes_svg(eyes, rx=(8.5, 8.5)):
    return "".join(ellipse(x, y, rx[i], 13, INK) for i, (x, y) in enumerate(eyes))


def front(variant="tie", sw=5, body=None, silhouette=False):
    body = body or FRONT_BODY
    if silhouette:
        s = path(body, INK)
        if variant == "headset":
            s += "".join(ellipse(x, LM["eye"] + 2, 12, 19, INK) for x in LM["ear_x"])
        return s
    out = [path(body, BODY, INK, sw), path(FRONT_SHADE, SHADE), eyes_svg(EYES)]
    if variant == "tie":
        out.append(tie_svg(150, sw))
    elif variant == "glasses":
        out.append(glasses_svg(EYES, sw))
    elif variant == "headset":
        out.append(headset_svg(sw))
    return "".join(out)


def three_quarter(variant="tie", sw=5):
    out = [path(Q_BODY, BODY, INK, sw), path(Q_SHADE, SHADE),
           eyes_svg(Q_EYES, (7.0, 8.5))]
    if variant == "tie":
        out.append(tie_svg(Q_AXIS, sw, sx=0.92))
    return "".join(out)


def side(variant="tie", sw=5):
    out = [path(S_BODY, BODY, INK, sw), path(S_SHADE, SHADE),
           ellipse(77, LM["eye"], 4.5, 12.5, INK)]
    if variant == "tie":
        tw = sw * 0.75
        # seen edge-on on the front surface, inside the outline
        out.append(path("M79,168 C84,168 90,169 94,171 C92,174 90,177 88,180 C85,176 82,172 79,168 Z", BODY, INK, sw * 0.55))
        out.append(path("M80,185 C80,206 80,228 81,244 L86,258 L92,244 C91,228 90,206 88,185 Z", TIE, INK, tw))
        out.append(path("M78,171 L90,171 L89,185 L80,185 Z", TIE, INK, tw))
    out.append(path(S_ARM, BODY, INK, sw * 0.9))
    out.append(path(S_ARM_SHADE, SHADE))
    return "".join(out)


def back(sw=5):
    return (f'<g transform="translate(300,0) scale(-1,1)">'
            f'{path(BACK_BODY, BODY, INK, sw)}{path(FRONT_SHADE, SHADE)}</g>')


def rest_pose(variant="tie", sw=5):
    return front(variant, sw, body=FRONT_REST)


def place(svg_inner, x, y, s=1.0, rot=0.0):
    """Put a 300x340 view at (x, y), scale s. rot is used ONLY for the rest-pose panel."""
    inner = f'<g transform="rotate({rot},150,300)">{svg_inner}</g>' if rot else svg_inner
    return f'<g transform="translate({x},{y}) scale({s})">{inner}</g>'


def shadow(x, y, s=1.0, o=0.16):
    return (f'<ellipse cx="{x + 150 * s}" cy="{y + 352 * s}" rx="{92 * s}" '
            f'ry="{12 * s}" fill="#2B1E16" fill-opacity="{o}" stroke="none"/>')


def text(x, y, t, size=16, weight="normal", fill=INK, anchor="start"):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{t}</text>')


def svg_doc(w, h, inner, bg=None):
    # ImageMagick's MSVG loses group transforms after <text>, <rect> or dashed paths: draw those last.
    texts = re.findall(r"<text[^>]*>[^<]*</text>", inner)
    inner = re.sub(r"<text[^>]*>[^<]*</text>", "", inner)
    late = re.findall(r"<rect[^>]*/>|<path[^>]*stroke-dasharray[^>]*/>", inner)
    inner = re.sub(r"<rect[^>]*/>|<path[^>]*stroke-dasharray[^>]*/>", "", inner)
    inner = inner + "".join(late) + "".join(texts)
    b = f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}" stroke="none"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{b}{inner}</svg>')
