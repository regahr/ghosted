"""2D estimate of the game camera (26 m, pitch 42 deg, yaw 20 deg) from the front view.

Model (an estimate; Viet's real render proves it):
- The body is round in plan (v5 front and side widths are about equal). Its radius r(h) comes from the
  right half of the hand-drawn FRONT_BODY outline.
- A mark drawn on the front view at (x, y) lies on the body surface: h = hem - y, X = x - 150,
  z = sqrt(r^2 - X^2) (toward the camera).
- The outline and the arms lie in the z = 0 plane (the widest slice), so they map with z = 0.
- The dome top seen from above is the convex hull of the projected surface.
Screen: yaw turns about the vertical axis, then v_up = h cos(p) - z' sin(p).
"""
import math
import re

from ghost import FRONT_BODY, LM

PITCH = 42.0
YAW = 20.0
HEM = LM["hem"]


def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3
        b = 3 * t * (1 - t) ** 2
        c = 3 * t * t * (1 - t)
        d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def _profile():
    """Half-width r against y, from the dome and side segments of FRONT_BODY (arms skipped)."""
    segs = [((150, 36), (204, 36), (242, 72), (244, 134)),
            ((244, 134), (245, 160), (246, 178), (252, 190)),
            ((254, 260), (253, 270), (256, 280), (262, 292))]
    pts = []
    for s in segs:
        pts += bez(*s, n=40)
    pts.append((252.5, 218))  # arm root band: the body side runs straight under the arm
    pts = sorted(pts, key=lambda p: p[1])
    return [(y, x - 150) for x, y in pts]


PROFILE = _profile()


def r_at(y):
    if y <= PROFILE[0][0]:
        return 0.0
    for (y0, r0), (y1, r1) in zip(PROFILE, PROFILE[1:]):
        if y0 <= y <= y1:
            return r0 + (r1 - r0) * (y - y0) / max(y1 - y0, 1e-6)
    return PROFILE[-1][1]


def project(X, h, z, yaw=YAW, pitch=PITCH):
    ps, py = math.radians(yaw), math.radians(pitch)
    x1 = X * math.cos(ps) - z * math.sin(ps)
    z1 = X * math.sin(ps) + z * math.cos(ps)
    v_up = h * math.cos(py) - z1 * math.sin(py)
    return x1, -v_up        # screen u right, v down


def on_surface(x, y, yaw=YAW, inset=0.0):
    X = x - 150
    r = max(r_at(y) - inset, 1e-3)
    X = max(-r, min(r, X))
    z = math.sqrt(max(r * r - X * X, 0.0))
    return project(X, HEM - y, z, yaw)


def on_slice(x, y, yaw=YAW):
    return project(x - 150, HEM - y, 0.0, yaw)


def map_path(d, fn):
    toks = re.findall(r"[MCLZ]|-?\d+(?:\.\d+)?", d)
    out, i, nums = [], 0, []
    while i < len(toks):
        t = toks[i]
        if t in "MCLZ":
            out.append(t)
            i += 1
            continue
        x, y = float(t), float(toks[i + 1])
        u, v = fn(x, y)
        out.append(f"{u:.2f},{v:.2f}")
        i += 2
    return " ".join(out)


def hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def dome_hull(yaw=YAW):
    """Projected body of revolution (top cap + hem ring), as a polygon path."""
    pts = []
    for y in range(36, int(HEM) + 1, 3):
        r = r_at(y)
        for a in range(0, 360, 6):
            t = math.radians(a)
            pts.append(project(r * math.sin(t), HEM - y, r * math.cos(t), yaw))
    hp = hull(pts)
    return "M" + " L".join(f"{u:.2f},{v:.2f}" for u, v in hp) + " Z"


def landmarks(yaw=YAW, eye=None):
    """Screen positions (u, v) of the main landmarks, front-centre marks on the surface."""
    eye = LM["eye"] if eye is None else eye
    top = min(v for _, v in [project(r_at(y) * math.sin(math.radians(a)), HEM - y,
                                     r_at(y) * math.cos(math.radians(a)), yaw)
                             for y in range(36, int(HEM), 3) for a in range(0, 360, 10)])
    bottom = max(on_surface(150, HEM, yaw)[1], on_slice(56, HEM, yaw)[1])
    return {"top": top, "bottom": bottom,
            "eye_l": on_surface(124, eye, yaw), "eye_r": on_surface(176, eye, yaw)}
