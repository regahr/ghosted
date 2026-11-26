"""Paint-over on the v5 renders (hero, variants, lineup x3).

Step 1 (magick): erase the v5 tie (colour mask, dilated, limited to a box) and
refill with the lit body tone sampled from the same render.
Step 2 (SVG overlay, hand-drawn): new tie B, redrawn outline where the old tie
crossed it, paint fixes and numbered marks for Viet.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ghost import *  # noqa
from build import sh, write, TMP, OUT, V5, comp  # noqa

LIT = "#F3E3C6"        # sampled: v5/hero.png (640,640), v5/variants.png (960,360)
LIT_GAME = "#F2E0C0"   # sampled: v5/lineup-grass-crop-x3.png (190,95)
CARD_BG = "#FDE6C8"    # sampled: v5/hero.png (850,520)


def erase(src, out, box, fill, colour, fuzz="14%", dil=6):
    x0, y0, x1, y1 = box
    w, h = [int(v) for v in os.popen(f'magick identify -format "%w %h" "{src}"').read().split()]
    m = os.path.join(TMP, "m.png")
    sh(src, "-alpha", "off", "-fuzz", fuzz, "-fill", "white", "-opaque", colour,
       "-fill", "black", "+opaque", "white", "-morphology", "Dilate", f"Disk:{dil}", m)
    sh(m, "(", "-size", f"{w}x{h}", "xc:black", "-fill", "white", "-draw",
       f"rectangle {x0},{y0} {x1},{y1}", ")", "-compose", "multiply", "-composite", m)
    sh(src, "(", "-size", f"{w}x{h}", f"xc:{fill}", ")", m, "-composite", out)


def overlay(base, svg_name, w, h, inner, out):
    sv = write(svg_name, w, h, inner)
    ov = os.path.join(TMP, svg_name.replace(".svg", ".png"))
    sh("-background", "none", sv, ov)
    sh(base, ov, "-compose", "over", "-composite", out)


def mark(n, cx, cy, r, lx, ly, lines, size=16):
    import math
    dx, dy = lx - cx, (ly - 6) - cy
    dd = math.hypot(dx, dy) or 1
    sx_, sy_ = cx + dx / dd * r, cy + dy / dd * r
    o = [ellipse(cx, cy, r, r, "none", NOTE, 3),
         path(f"M{sx_:.0f},{sy_:.0f} L{lx - 2},{ly - 6}", "none", NOTE, 2),
         ellipse(lx + 10, ly - 6, 12, 12, NOTE),
         text(lx + 10, ly - 1, str(n), 15, "bold", "#FFFFFF", "middle")]
    for k, ln in enumerate(lines):
        o.append(text(lx + 28, ly + k * (size + 4), ln, size, "bold" if k == 0 else "normal", NOTE))
    return "".join(o)


def tie_at(x, y, s, sx=0.9, rot=-6, sw=3.06):
    """Tie B, knot top centre (219,180) placed at (x, y)."""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s * sx},{s}) '
            f'translate(-219,-173)">{tie_parts("B", sw)}</g>')


def hero():
    src = os.path.join(V5, "hero.png")
    a = os.path.join(TMP, "hero-a.png")
    erase(src, a, (590, 490, 797, 632), LIT, "#D2A1BF", dil=7)
    o = []
    # old tip was outside the outline: give back the background, redraw the outline
    o.append(path("M796,470 L870,470 L870,572 L811,572 Z", CARD_BG))
    o.append(path("M786,512 L802,512 L806,552 L786,552 Z", LIT))
    o.append(path("M788,440 C794,480 804,540 814,594", "none", INK, 6.5))
    # paint fixes: crease out, wedge filled flat
    o.append(path("M706,610 L782,684", "none", LIT, 7))
    o.append(path("M748,736 L792,748 L790,776 L770,776 Z", LIT))
    o.append(tie_at(652, 574, 2.18))
    o.append(mark(1, 744, 648, 52, 900, 560, ["Remove the ink crease", "(hull shows through", "the concave join)"]))
    o.append(mark(2, 772, 758, 30, 900, 700, ["Fill the pale root wedge:", "one flat body tone"]))
    o.append(mark(3, 812, 772, 22, 900, 820, ["Underside ink starts inside", "the body (hook): close it", "on the outline"]))
    o.append(mark(4, 655, 650, 92, 120, 900, ["New tie: B, slipped", "knot below the eye line,", "hangs down off-centre,", "V clear of the arm"]))
    o.append(mark(5, 560, 300, 40, 120, 160, ["Opinion: dome shows flat", "facets at card size; smooth", "within budget (Viet)"]))
    o.append(text(30, 1170, "Paint-over on v5/hero.png. Blue = notes for Viet. "
                  "Old tie erased; new tie B painted at card scale.", 20, "bold", NOTE))
    out = os.path.join(TMP, "po-hero.png")
    overlay(a, "po-hero.svg", 1200, 1200, "".join(o), out)
    return out


def variants():
    src = os.path.join(V5, "variants.png")
    a = os.path.join(TMP, "var-a.png")
    erase(src, a, (288, 308, 424, 396), LIT, "#D2A1C0", dil=5)
    # glasses: erase the octagon rims to redraw them round
    erase(a, a, (745, 276, 872, 358), LIT, "#D8C8CC", fuzz="9%", dil=3)
    o = []
    o.append(path("M425,300 L480,300 L480,392 L441,392 Z", CARD_BG))
    o.append(path("M414,312 L429,312 L433,352 L414,352 Z", LIT))
    o.append(path("M418,268 C422,284 425,298 428,318 C432,348 437,374 443,400", "none", INK, 4.5))
    for (c0, c1, w0) in (((368, 385), (418, 440), (395, 478)), ((968, 385), (1018, 440), (995, 478)),
                         ((1528, 388), (1590, 444), (1570, 476))):
        o.append(path(f"M{c0[0]},{c0[1]} L{c1[0]},{c1[1]}", "none", LIT, 5))
        wx, wy = w0
        o.append(path(f"M{wx},{wy} L{wx + 25},{wy + 6} L{wx + 23},{wy + 22} L{wx + 10},{wy + 22} Z", LIT))
    o.append(tie_at(327, 352, 1.40, sw=3.06))
    # glasses round rims (row 27), same centres as v5
    o.append(ellipse(772, 320, 21, 30, "none", ACC, 6))
    o.append(ellipse(837, 316, 28, 33, "none", ACC, 6))
    o.append(path("M793,318 C798,312 804,311 809,314", "none", ACC, 5))
    # headset: oval cup with ink rim over the octagon
    o.append(ellipse(1583, 291, 26, 34, ACC, INK, 3))
    for c1, c2, c3 in (((393, 412), (408, 490), (444, 508)), ((993, 412), (1008, 490), (1044, 508)),
                       ((1558, 414), (1585, 488), (1640, 512))):
        o.append(ellipse(c1[0], c1[1], 36, 36, "none", NOTE, 3))
        o.append(text(c1[0], c1[1] + 54, "1", 16, "bold", NOTE, "middle"))
        o.append(ellipse(c2[0], c2[1], 18, 18, "none", NOTE, 3))
        o.append(text(c2[0] - 28, c2[1] + 10, "2", 16, "bold", NOTE, "middle"))
        o.append(ellipse(c3[0], c3[1], 13, 13, "none", NOTE, 3))
        o.append(text(c3[0] + 22, c3[1] + 22, "3", 16, "bold", NOTE, "middle"))
    o.append(ellipse(330, 410, 62, 70, "none", NOTE, 3))
    o.append(text(250, 470, "4 tie B", 16, "bold", NOTE))
    o.append(text(800, 380, "5 round rims", 16, "bold", NOTE, "middle"))
    o.append(text(1583, 350, "5 oval cup", 16, "bold", NOTE, "middle"))
    o.append(text(20, 640, "1 crease out   2 flat root, no wedge   3 hem hook under the near arm: "
                  "close the outline   4 tie B   5 clean-up only", 20, "bold", NOTE))
    out = os.path.join(TMP, "po-var.png")
    overlay(a, "po-var.svg", 1800, 800, "".join(o), out)
    return out


def lineup():
    src = os.path.join(V5, "lineup-grass-crop-x3.png")
    a = os.path.join(TMP, "lin-a.png")
    erase(src, a, (176, 82, 214, 118), LIT_GAME, "#C99BC0", fuzz="18%", dil=3)
    o = []
    # tie B at the game camera (x3): knot below the eye line on the +x side
    o.append(f'<g transform="translate(185,108) rotate(-6) scale(0.42,0.36) translate(-219,-173)">'
             f'{tie_parts("B", 3)}</g>')
    o.append(f'<rect x="139" y="111" width="24" height="22" fill="none" stroke="{NOTE}" '
             f'stroke-width="2" stroke-dasharray="4,3"/>')
    o.append(text(20, 395, "Lineup x3 (26 m): old tie erased, tie B painted at its real size. "
                  "Dashed box = mouth zone, must stay empty.", 16, "bold", NOTE))
    out = os.path.join(TMP, "po-lin.png")
    overlay(a, "po-lin.svg", 900, 420, "".join(o), out)
    return out


def paintover():
    h, v, l = hero(), variants(), lineup()
    final = os.path.join(OUT, "paintover-v5.png")
    top = os.path.join(TMP, "po-top.png")
    sh(h, "-resize", "900x900", top)
    right = os.path.join(TMP, "po-right.png")
    sh(l, "-background", CREAM, "-gravity", "north", "-extent", "900x900", right)
    row1 = os.path.join(TMP, "po-row1.png")
    sh(top, right, "+append", row1)
    sh(row1, v, "-background", CREAM, "-gravity", "center", "-append", final)
    return final


if __name__ == "__main__":
    print(paintover())
