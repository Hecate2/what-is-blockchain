#!/usr/bin/env python3
"""《天枢账簿》插图基本画法：铁线描、工笔重彩、界画。

本文件只出图元，构图全在 figs.py。所有函数返回 SVG 片段字符串。
"""
import math

PAPER = "#f4ebd9"
PAPER_D = "#e7d9bd"
INK = "#241f1c"
SOFT = "#4a4038"
CINNABAR = "#a8322a"
ROUGE = "#c0503c"
AZURITE = "#2f5d7c"
AZU_L = "#7d9fb0"
MALACH = "#3f6f52"
MAL_L = "#8aab93"
GAMBOGE = "#d9a441"
OCHRE = "#8c5a3c"
WHITE = "#fbf6ea"
GOLD = "#b8892f"
STEEL = "#3b464b"
DARK = "#1d2529"
JADE = "#7fa58c"
ASH = "#9a9284"

FS = "Songti SC, STSong, serif"
FK = "STKaiti, Kaiti SC, serif"

DEFS = f"""
<pattern id="fiber" width="46" height="46" patternUnits="userSpaceOnUse">
  <path d="M3 9 C14 7 26 12 43 8" stroke="#c9b895" stroke-width="0.5" fill="none" opacity="0.30"/>
  <path d="M0 31 C13 28 27 34 46 30" stroke="#c9b895" stroke-width="0.42" fill="none" opacity="0.24"/>
  <path d="M9 0 C7 14 12 30 8 46" stroke="#c9b895" stroke-width="0.36" fill="none" opacity="0.20"/>
</pattern>
<pattern id="wave" width="34" height="13" patternUnits="userSpaceOnUse">
  <path d="M0 9 Q8.5 2 17 9 T34 9" stroke="{AZU_L}" stroke-width="1.0" fill="none" opacity="0.75"/>
</pattern>
<pattern id="tile" width="17" height="10" patternUnits="userSpaceOnUse">
  <path d="M0 9.5 Q8.5 5 17 9.5" stroke="{INK}" stroke-width="0.7" fill="none" opacity="0.5"/>
</pattern>
<pattern id="brick" width="34" height="18" patternUnits="userSpaceOnUse">
  <path d="M0 17.5 L34 17.5 M0 8.5 L34 8.5 M8 8.5 L8 17.5 M26 0.5 L26 8.5" stroke="{INK}" stroke-width="0.55" fill="none" opacity="0.30"/>
</pattern>
<radialGradient id="glow" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="#f6c96b" stop-opacity="0.62"/>
  <stop offset="55%" stop-color="#e0a044" stop-opacity="0.22"/>
  <stop offset="100%" stop-color="#e0a044" stop-opacity="0"/>
</radialGradient>
<linearGradient id="blade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#8a2f22"/><stop offset="38%" stop-color="#c0562c"/>
  <stop offset="68%" stop-color="#e8a63f"/><stop offset="100%" stop-color="#f4d489"/>
</linearGradient>
<linearGradient id="inkwash" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#1d2529" stop-opacity="0.34"/>
  <stop offset="100%" stop-color="#1d2529" stop-opacity="0"/>
</linearGradient>
"""


def pth(d, fill="none", stroke=INK, w=1.2, op=1.0, join="round", cap="round", dash=None):
    s = ""
    if stroke:
        s = f' stroke="{stroke}" stroke-width="{w}" stroke-linejoin="{join}" stroke-linecap="{cap}"'
        if dash:
            s += f' stroke-dasharray="{dash}"'
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<path d="{d}" fill="{fill}"{s}{o}/>'


def line(x1, y1, x2, y2, color=INK, w=1.2, op=1.0, dash=None):
    s = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op != 1 else ""
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round"{s}{o}/>')


def rect(x, y, w, h, fill="none", stroke=INK, sw=1.2, op=1.0, rx=0):
    o = f' opacity="{op}"' if op != 1 else ""
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}{o}/>'


def circ(x, y, r, fill="none", stroke=INK, sw=1.2, op=1.0):
    o = f' opacity="{op}"' if op != 1 else ""
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{s}{o}/>'


def ell(x, y, rx, ry, fill="none", stroke=INK, sw=1.2, op=1.0, rot=0):
    o = f' opacity="{op}"' if op != 1 else ""
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    t = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}"{s}{o}{t}/>'


def txt(x, y, s, size=14, fill=INK, font=FK, anchor="middle", ls=0, op=1.0, weight=None):
    o = f' opacity="{op}"' if op != 1 else ""
    wgt = f' font-weight="{weight}"' if weight else ""
    lsp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{lsp}{wgt}{o}>{s}</text>')


def g(body, tx=0, ty=0, s=1.0, rot=0, op=1.0):
    t = f"translate({tx},{ty})"
    if s != 1:
        t += f" scale({s})"
    if rot:
        t += f" rotate({rot})"
    o = f' opacity="{op}"' if op != 1 else ""
    return f'<g transform="{t}"{o}>{body}</g>'


def canvas(w, h, body, base=PAPER, grain=0.55):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">\n<defs>{DEFS}</defs>\n'
            f'<rect width="{w}" height="{h}" fill="{base}"/>\n'
            f'<rect width="{w}" height="{h}" fill="url(#fiber)" opacity="{grain}"/>\n'
            f'{body}\n</svg>\n')


def band(x0, y0, x1, y1, w0, w1):
    """从 (x0,y0) 到 (x1,y1) 的一条带子（袖、杆、梁）。"""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    return (f"M{x0 + nx * w0 / 2:.2f} {y0 + ny * w0 / 2:.2f} "
            f"L{x1 + nx * w1 / 2:.2f} {y1 + ny * w1 / 2:.2f} "
            f"L{x1 - nx * w1 / 2:.2f} {y1 - ny * w1 / 2:.2f} "
            f"L{x0 - nx * w0 / 2:.2f} {y0 - ny * w0 / 2:.2f} Z")


# ============================================================ 人
def _sleeve(x0, y0, x1, y1, w0, w1, fill, hand=False):
    """一只宽袖：顺手臂的喇叭筒，口沿落一汪。"""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    a = (x0 + nx * w0 / 2, y0 + ny * w0 / 2)
    b = (x1 + nx * w1 / 2, y1 + ny * w1 / 2)
    c = (x1 - nx * w1 / 2, y1 - ny * w1 / 2)
    d_ = (x0 - nx * w0 / 2, y0 - ny * w0 / 2)
    sag = min(w1 * 0.92, 1.6 * min(0.22 * (w1 / 0.092), w1 * 4.2 * abs(ux)))  # 手臂越平，下缘坠得越低
    lx, ly = (c[0] + d_[0]) / 2 + ux * 4, (c[1] + d_[1]) / 2 + sag
    d = (f"M{a[0]:.1f} {a[1]:.1f} "
         f"C{a[0] + ux * L * 0.34 + nx * w0 * 0.26:.1f} {a[1] + uy * L * 0.34 + ny * w0 * 0.26:.1f} "
         f"{b[0] - ux * w1 * 0.55 + nx * w1 * 0.10:.1f} {b[1] - uy * w1 * 0.55 + ny * w1 * 0.10:.1f} "
         f"{b[0]:.1f} {b[1]:.1f} "
         f"C{b[0] + ux * w1 * 0.42:.1f} {b[1] + uy * w1 * 0.42:.1f} "
         f"{c[0] + ux * w1 * 0.42:.1f} {c[1] + uy * w1 * 0.42:.1f} "
         f"{c[0]:.1f} {c[1]:.1f} "
         f"Q{lx:.1f} {ly:.1f} {d_[0]:.1f} {d_[1]:.1f} Z")
    out = [pth(d, fill=fill, stroke=INK, w=1.5)]
    ang = math.degrees(math.atan2(ny, nx))
    out.append(ell((b[0] + c[0]) / 2 + ux * w1 * 0.16, (b[1] + c[1]) / 2 + uy * w1 * 0.16,
                   w1 * 0.38, w1 * 0.13, fill="none", stroke=INK, sw=1.1, op=0.85, rot=ang))
    if hand:
        out.append(ell((b[0] + c[0]) / 2 + ux * w1 * 0.34, (b[1] + c[1]) / 2 + uy * w1 * 0.34,
                       w1 * 0.24, w1 * 0.15, fill="#f6e3c8", stroke=INK, sw=1.0, rot=ang))
    return "".join(out)


def person(x, y, h=170, robe=DARK, trim=GOLD, sash=CINNABAR,
           hat="futou", l_arm=(-0.21, -0.40), r_arm=(0.21, -0.40),
           sleeve=None, facing=1, face=False, beard=False, hands=True):
    """立像。(x,y) 为脚底中点，h 为总高。

    l_arm / r_arm 是左右袖口相对脚底中点的坐标（以 h 为单位），
    (-0.21,-0.40) 是自然下垂，(0.30,-0.66) 是抬起手。
    """
    sl = sleeve or robe
    sx = 0.102 * h
    sy = -0.792 * h
    hemw, waistw = 0.166 * h, 0.076 * h
    out = []

    # 袖：先画，大半压在袍身下面
    for cf in (l_arm, r_arm):
        cx_, cy_ = cf[0] * h, cf[1] * h
        sh = sx if cx_ > 0 else -sx
        out.append(_sleeve(sh * 0.5, sy - 0.006 * h, cx_, cy_, 0.074 * h, 0.092 * h, sl))

    # 袍身
    d = (f"M{-hemw} 0 "
         f"C{-hemw * 0.99} {-0.16 * h} {-waistw * 1.30} {-0.40 * h} {-waistw} {-0.55 * h} "
         f"C{-waistw * 1.12} {-0.66 * h} {-sx} {-0.735 * h} {-sx * 0.86} {-0.805 * h} "
         f"L{sx * 0.86} {-0.805 * h} "
         f"C{sx} {-0.735 * h} {waistw * 1.12} {-0.66 * h} {waistw} {-0.55 * h} "
         f"C{waistw * 1.30} {-0.40 * h} {hemw * 0.99} {-0.16 * h} {hemw} 0 Z")
    out.append(pth(d, fill=robe, stroke=INK, w=1.6))

    # 下摆褶
    for t in (-0.62, -0.18, 0.34):
        out.append(pth(f"M{hemw * t:.1f} {-0.02 * h:.1f} "
                       f"C{waistw * t * 0.9:.1f} {-0.22 * h:.1f} {waistw * t * 0.5:.1f} "
                       f"{-0.34 * h:.1f} {waistw * t * 0.28:.1f} {-0.46 * h:.1f}",
                       stroke=INK, w=1.0, op=0.28))

    # 交领
    out.append(pth(f"M{-0.044 * h:.1f} {-0.806 * h:.1f} L0 {-0.700 * h:.1f} "
                   f"L{0.044 * h:.1f} {-0.806 * h:.1f}", stroke=trim, w=1.7, op=0.8))
    out.append(pth(f"M{-0.050 * h:.1f} {-0.812 * h:.1f} L{-0.014 * h:.1f} {-0.700 * h:.1f}",
                   stroke=INK, w=1.0, op=0.45))

    # 革带
    out.append(pth(f"M{-waistw * 1.14:.1f} {-0.552 * h:.1f} "
                   f"C{-waistw * 0.3:.1f} {-0.572 * h:.1f} {waistw * 0.3:.1f} "
                   f"{-0.572 * h:.1f} {waistw * 1.14:.1f} {-0.552 * h:.1f}",
                   stroke=sash, w=0.028 * h, op=0.95))
    out.append(line(0.012 * h, -0.556 * h, 0.012 * h, -0.44 * h, sash, 0.016 * h, 0.95))
    out.append(circ(0.012 * h, -0.552 * h, 0.014 * h, fill=GOLD, stroke=INK, sw=0.9))

    # 颈与头
    out.append(pth(f"M{-0.024 * h:.1f} {-0.812 * h:.1f} l0 {-0.032 * h:.1f} "
                   f"l{0.048 * h:.1f} 0 l0 {0.032 * h:.1f} Z", fill=WHITE, stroke=INK, w=1.0))
    hx, hy = 0.004 * h * facing, -0.878 * h
    out.append(ell(hx, hy, 0.055 * h, 0.064 * h, fill=WHITE, stroke=INK, sw=1.3))

    # 冠帽
    if hat == "futou":
        out.append(pth(f"M{-0.060 * h:.1f} {-0.906 * h:.1f} "
                       f"C{-0.070 * h:.1f} {-0.968 * h:.1f} {0.066 * h:.1f} {-0.968 * h:.1f} "
                       f"{0.060 * h:.1f} {-0.906 * h:.1f} Z", fill=INK, stroke=INK, w=1.1))
        out.append(pth(f"M{-0.058 * h:.1f} {-0.916 * h:.1f} "
                       f"C{-0.020 * h:.1f} {-0.956 * h:.1f} {0.030 * h:.1f} {-0.950 * h:.1f} "
                       f"{0.058 * h:.1f} {-0.912 * h:.1f}", stroke=GOLD, w=1.2, op=0.6))
        for s_ in (-1, 1):
            out.append(pth(f"M{s_ * 0.058 * h:.1f} {-0.918 * h:.1f} "
                           f"C{s_ * 0.085 * h:.1f} {-0.930 * h:.1f} {s_ * 0.108 * h:.1f} "
                           f"{-0.944 * h:.1f} {s_ * 0.116 * h:.1f} {-0.952 * h:.1f} "
                           f"L{s_ * 0.108 * h:.1f} {-0.922 * h:.1f} "
                           f"L{s_ * 0.058 * h:.1f} {-0.906 * h:.1f} Z",
                           fill=INK, stroke=INK, w=0.7))
    elif hat == "jin":
        out.append(pth(f"M{-0.058 * h:.1f} {-0.902 * h:.1f} "
                       f"C{-0.068 * h:.1f} {-0.962 * h:.1f} {0.068 * h:.1f} {-0.962 * h:.1f} "
                       f"{0.058 * h:.1f} {-0.902 * h:.1f} Z", fill=SOFT, stroke=INK, w=1.1))
        out.append(pth(f"M{0.056 * h:.1f} {-0.922 * h:.1f} "
                       f"C{0.082 * h:.1f} {-0.910 * h:.1f} {0.078 * h:.1f} {-0.868 * h:.1f} "
                       f"{0.058 * h:.1f} {-0.874 * h:.1f}", fill=SOFT, stroke=INK, w=1.0))
    elif hat == "douli":
        out.append(pth(f"M0 {-1.002 * h:.1f} L{-0.112 * h:.1f} {-0.902 * h:.1f} "
                       f"Q0 {-0.930 * h:.1f} {0.112 * h:.1f} {-0.902 * h:.1f} Z",
                       fill=OCHRE, stroke=INK, w=1.3))
        for t in (0.3, 0.55, 0.8):
            out.append(line(0, -0.998 * h, -0.112 * h + 0.224 * h * t, -0.910 * h, INK, 0.7, 0.45))
    elif hat == "none":
        out.append(pth(f"M{-0.056 * h:.1f} {-0.918 * h:.1f} "
                       f"C{-0.050 * h:.1f} {-0.966 * h:.1f} {0.050 * h:.1f} {-0.966 * h:.1f} "
                       f"{0.056 * h:.1f} {-0.918 * h:.1f} Z", fill=INK, stroke=INK, w=1.0))

    if face:
        out.append(pth(f"M{hx + 0.014 * h * facing:.1f} {hy - 0.020 * h:.1f} "
                       f"l{0.026 * h * facing:.1f} {-0.004 * h:.1f}", stroke=INK, w=1.2, op=0.75))
        out.append(circ(hx + 0.026 * h * facing, hy - 0.004 * h, 0.0062 * h, fill=INK, stroke=None))
    if beard:
        out.append(pth(f"M{hx - 0.024 * h:.1f} {hy + 0.046 * h:.1f} "
                       f"C{hx:.1f} {hy + 0.104 * h:.1f} {hx + 0.028 * h:.1f} {hy + 0.070 * h:.1f} "
                       f"{hx + 0.020 * h:.1f} {hy + 0.044 * h:.1f} Z",
                       fill=WHITE, stroke=INK, w=1.0, op=0.85))


    return f'<g transform="translate({x},{y})">' + "".join(out) + "</g>"


def kneel(x, y, h=120, robe=DARK, trim=GOLD, sash=CINNABAR, hat="jin",
          facing=1, arms=(-0.24, -0.30)):
    """正坐像。y 为膝前地面，h 为坐高（约为立像的 0.83，显得矮一截）。"""
    out = []
    # 袖：先画，压在裙下
    for s_ in (-1, 1):
        out.append(_sleeve(s_ * 0.100 * h, -0.632 * h, -s_ * abs(arms[0]) * h, arms[1] * h,
                           0.075 * h, 0.096 * h, robe))
    # 下裳：膝在前，铺开一大片
    out.append(pth(f"M{-0.300 * h:.1f} {-0.012 * h:.1f} "
                   f"C{-0.316 * h:.1f} {-0.126 * h:.1f} {-0.252 * h:.1f} {-0.226 * h:.1f} "
                   f"{-0.132 * h:.1f} {-0.250 * h:.1f} L{0.132 * h:.1f} {-0.250 * h:.1f} "
                   f"C{0.252 * h:.1f} {-0.226 * h:.1f} {0.316 * h:.1f} {-0.126 * h:.1f} "
                   f"{0.300 * h:.1f} {-0.012 * h:.1f} "
                   f"C{0.180 * h:.1f} {0.024 * h:.1f} {-0.180 * h:.1f} {0.024 * h:.1f} "
                   f"{-0.300 * h:.1f} {-0.012 * h:.1f} Z", fill=robe, stroke=INK, w=1.6))
    # 膝头一道横褶，说明腿是折着的
    out.append(pth(f"M{-0.262 * h:.1f} {-0.062 * h:.1f} "
                   f"C{-0.140 * h:.1f} {-0.098 * h:.1f} {0.140 * h:.1f} "
                   f"{-0.098 * h:.1f} {0.262 * h:.1f} {-0.062 * h:.1f}",
                   stroke=INK, w=1.3, op=0.34))
    # 膝头的褶
    for t in (-0.66, -0.22, 0.24, 0.66):
        out.append(pth(f"M{t * 0.300 * h:.1f} {-0.026 * h:.1f} "
                       f"C{t * 0.306 * h:.1f} {-0.100 * h:.1f} {t * 0.262 * h:.1f} "
                       f"{-0.172 * h:.1f} {t * 0.196 * h:.1f} {-0.222 * h:.1f}",
                       stroke=INK, w=1.0, op=0.4))
    # 上身
    out.append(pth(f"M{-0.101 * h:.1f} {-0.238 * h:.1f} "
                   f"C{-0.099 * h:.1f} {-0.382 * h:.1f} {-0.105 * h:.1f} {-0.524 * h:.1f} "
                   f"{-0.101 * h:.1f} {-0.656 * h:.1f} L{0.101 * h:.1f} {-0.656 * h:.1f} "
                   f"C{0.105 * h:.1f} {-0.524 * h:.1f} {0.099 * h:.1f} {-0.382 * h:.1f} "
                   f"{0.101 * h:.1f} {-0.238 * h:.1f} Z", fill=robe, stroke=INK, w=1.5))
    # 交领
    out.append(pth(f"M{-0.046 * h:.1f} {-0.652 * h:.1f} L0 {-0.546 * h:.1f} "
                   f"L{0.046 * h:.1f} {-0.652 * h:.1f}", stroke=trim, w=1.7, op=0.85))
    out.append(pth(f"M{-0.052 * h:.1f} {-0.658 * h:.1f} L{-0.014 * h:.1f} {-0.548 * h:.1f}",
                   stroke=INK, w=1.0, op=0.45))
    # 革带
    out.append(pth(f"M{-0.104 * h:.1f} {-0.376 * h:.1f} "
                   f"C{-0.030 * h:.1f} {-0.394 * h:.1f} {0.030 * h:.1f} "
                   f"{-0.394 * h:.1f} {0.104 * h:.1f} {-0.376 * h:.1f}",
                   stroke=sash, w=0.026 * h, op=0.95))
    # 颈与头
    out.append(pth(f"M{-0.021 * h:.1f} {-0.652 * h:.1f} l0 {-0.026 * h:.1f} "
                   f"l{0.042 * h:.1f} 0 l0 {0.026 * h:.1f} Z", fill=WHITE, stroke=INK, w=1.0))
    out.append(ell(0.004 * h, -0.752 * h, 0.052 * h, 0.060 * h, fill=WHITE, stroke=INK, sw=1.3))
    if hat == "jin":
        out.append(pth(f"M{-0.055 * h:.1f} {-0.780 * h:.1f} "
                       f"C{-0.064 * h:.1f} {-0.836 * h:.1f} {0.064 * h:.1f} {-0.836 * h:.1f} "
                       f"{0.055 * h:.1f} {-0.780 * h:.1f} Z", fill=SOFT, stroke=INK, w=1.1))
    elif hat == "futou":
        out.append(pth(f"M{-0.057 * h:.1f} {-0.784 * h:.1f} "
                       f"C{-0.066 * h:.1f} {-0.842 * h:.1f} {0.062 * h:.1f} {-0.842 * h:.1f} "
                       f"{0.057 * h:.1f} {-0.784 * h:.1f} Z", fill=INK, stroke=INK, w=1.1))
    return (f'<g transform="translate({x},{y}) scale({facing},1)">'
            + "".join(out) + "</g>")


def hand(x, y, s=1.0, ang=0, skin="#f3ddbe", cuff=None):
    """一只侧掌，指向前方（ang=0 时朝右）。"""
    p = [f'<g transform="translate({x},{y}) rotate({ang}) scale({s})">']
    if cuff:
        p.append(pth("M-30 -6 C-18 -12 -6 -10 0 -6 L0 8 C-8 12 -20 12 -30 8 Z",
                     fill=cuff, stroke=INK, w=1.2))
        p.append(ell(-3, 1, 4.5, 8.5, fill=skin, stroke=INK, sw=1.0))
    p.append(pth("M0 -9 C7 -11 14 -9 18 -5 L21 -1 C22 4 19 8 13 10 C6 12 -2 10 -2 4 Z",
                 fill=skin, stroke=INK, w=1.2))
    for k, (dy, ln) in enumerate(((-7.5, 13), (-3.5, 16), (0.5, 16.5), (4.5, 14))):
        p.append(pth(f"M6 {dy} L{ln} {dy + 0.6}", stroke=INK, w=3.0, op=1))
        p.append(pth(f"M6 {dy} L{ln} {dy + 0.6}", stroke=skin, w=1.8))
    p.append(pth("M2 8 C6 14 12 15 16 12", stroke=INK, w=3.4))
    p.append(pth("M2 8 C6 14 12 15 16 12", stroke=skin, w=2.2))
    p.append("</g>")
    return "".join(p)


# ============================================================ 山水
def rock(x, y, w, h, fill=PAPER_D, edge=INK, cun=True, op=1.0, seed=0):
    """一块带披麻皴的山石，y 为底边。"""
    d = (f"M{x} {y} C{x + w * 0.04} {y - h * 0.42} {x + w * 0.16} {y - h * 0.72} {x + w * 0.30} {y - h * 0.86} "
         f"C{x + w * 0.42} {y - h * 0.99} {x + w * 0.56} {y - h * 0.94} {x + w * 0.66} {y - h * 0.78} "
         f"C{x + w * 0.78} {y - h * 0.58} {x + w * 0.86} {y - h * 0.40} {x + w * 0.94} {y - h * 0.16} "
         f"L{x + w} {y} Z")
    out = [pth(d, fill=fill, stroke=edge, w=1.5, op=op)]
    if cun:
        for i in range(7):
            t = (i + 0.5) / 8
            bx = x + w * (0.10 + 0.78 * t) + seed * 3
            by = y - h * (0.10 + 0.10 * math.sin(i * 2.1 + seed))
            out.append(pth(f"M{bx} {by} C{bx + w * 0.05} {by - h * 0.16} "
                           f"{bx + w * 0.02} {by - h * 0.30} {bx + w * 0.09} {by - h * 0.46}",
                           stroke=edge, w=0.9, op=0.34 * op))
    return "".join(out)


def waterline(x0, x1, y, step=34, color=AZU_L, w=1.1, op=0.8, seed=0):
    out = []
    n = int((x1 - x0) / step)
    for i in range(n):
        bx = x0 + i * step
        yy = y + (i % 3 - 1) * 2.2 + seed
        out.append(pth(f"M{bx} {yy} Q{bx + step * 0.25} {yy - 4.5} {bx + step * 0.5} {yy} "
                       f"T{bx + step} {yy}", stroke=color, w=w, op=op))
    return "".join(out)


def cloud_wisp(x, y, w, color=WHITE, edge=GOLD, op=1.0):
    """一缕平云。"""
    h = w * 0.16
    d = (f"M{x} {y} C{x + w * 0.10} {y - h * 0.9} {x + w * 0.26} {y - h * 1.05} {x + w * 0.36} {y - h * 0.5} "
         f"C{x + w * 0.46} {y - h * 1.15} {x + w * 0.64} {y - h * 1.0} {x + w * 0.66} {y - h * 0.42} "
         f"C{x + w * 0.82} {y - h * 0.85} {x + w * 0.96} {y - h * 0.5} {x + w} {y} Z")
    return pth(d, fill=color, stroke=edge, w=1.3, op=op)


def flame(x, y, s=1.0, fill=CINNABAR, inner=GAMBOGE, sway=0):
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(pth(f"M0 0 C-18 -14 -12 -34 -2 -48 C-8 -30 8 -36 8 -50 "
                 f"C24 -34 26 -14 14 0 Z", fill=fill, stroke=DARK, w=1.1, op=0.95))
    p.append(pth(f"M2 -3 C-5 -15 0 -28 6 -36 C3 -24 12 -26 12 -34 "
                 f"C18 -22 16 -10 10 -3 Z", fill=inner, stroke=None, op=0.95))
    p.append("</g>")
    return "".join(p)


def smoke(x, y, h, w=16, n=1, color=ASH, op=0.35):
    out = []
    for k in range(n):
        bx = x + k * 9
        out.append(pth(f"M{bx} {y} C{bx - w} {y - h * 0.32} {bx + w} {y - h * 0.5} "
                       f"{bx - w * 0.3} {y - h * 0.74} C{bx - w * 0.9} {y - h * 0.9} "
                       f"{bx + w * 0.4} {y - h * 0.95} {bx + w * 0.2} {y - h}",
                       stroke=color, w=1.6, op=op))
    return "".join(out)


# ============================================================ 建筑
def roof_eave(x, y, w, body=DARK, edge=GOLD, up=26, hang=16):
    """只见一段檐口：瓦垄在上，滴水在下。y 为檐口线。"""
    out = []
    out.append(pth(f"M{x} {y} L{x + w} {y} L{x + w - 8} {y + hang} L{x + 8} {y + hang} Z",
                   fill=body, stroke=INK, w=1.2))
    n = max(4, int(w // 15))
    for i in range(n + 1):
        bx = x + i * w / n
        out.append(pth(f"M{bx} {y - up} C{bx + 2} {y - up * 0.5} {bx + 2} {y - 4} {bx + 3} {y}",
                       stroke=edge, w=1.1, op=0.7))
    out.append(line(x, y, x + w, y, edge, 2.4))
    out.append(pth(f"M{x - 14} {y - 4} C{x - 4} {y - up * 1.1} {x + w * 0.16} {y - up * 1.35} "
                   f"{x + w * 0.30} {y - up * 1.30} L{x + w * 0.70} {y - up * 1.30} "
                   f"C{x + w * 0.84} {y - up * 1.35} {x + w + 4} {y - up * 1.1} {x + w + 14} {y - 4} "
                   f"L{x + w} {y - 2} L{x} {y - 2} Z",
                   fill=body, stroke=INK, w=1.5))
    for i in range(n + 1):
        bx = x + i * w / n
        out.append(pth(f"M{bx} {y - 2} L{bx + (bx - x - w / 2) * 0.02} {y - up * 1.28}",
                       stroke=edge, w=0.9, op=0.5))
    return "".join(out)


def dougong(x, y, w, body=OCHRE, edge=GOLD):
    out = [rect(x, y, w, 5, fill=body, stroke=INK, sw=0.9)]
    n = max(3, int(w // 17))
    for i in range(n):
        bx = x + 7 + i * (w - 14) / max(1, n - 1)
        out.append(rect(bx - 3, y + 5, 6, 6, fill=body, stroke=edge, sw=0.8))
        out.append(rect(bx - 8, y + 11, 16, 4, fill=body, stroke=INK, sw=0.8))
    return "".join(out)


def pillar(x, y, w, h, body=CINNABAR, base=PAPER_D):
    """檐柱，y 为柱脚。"""
    out = [rect(x - w * 0.22, y - 8, w * 1.44, 9, fill=base, stroke=INK, sw=1.2)]
    out.append(rect(x, y - 9, w, -h + 9, fill=body, stroke=INK, sw=1.3))
    out.append(pth(f"M{x + w * 0.24} {y - 12} l0 {-h + 16}", stroke=INK, w=0.9, op=0.35))
    out.append(pth(f"M{x + w * 0.70} {y - 12} l0 {-h + 16}", stroke=INK, w=0.9, op=0.35))
    return "".join(out)


def railing(x, y, w, color=GOLD, h=13):
    out = [line(x, y - h, x + w, y - h, color, 2.0), line(x, y - h + 8, x + w, y - h + 8, color, 1.1, 0.8)]
    n = max(3, int(w // 13))
    for i in range(n + 1):
        bx = x + i * w / n
        out.append(line(bx, y - h - 2, bx, y + 1, color, 1.0))
    return "".join(out)


def steps(x, y, w, n=5, dy=11, color=PAPER_D):
    out = []
    for i in range(n):
        yy = y - i * dy
        out.append(pth(f"M{x - i * 3} {yy} L{x + w + i * 3} {yy}", stroke=INK, w=1.1, op=0.75))
        out.append(pth(f"M{x - i * 3} {yy} L{x - (i + 1) * 3} {yy - dy}", stroke=INK, w=1.0, op=0.5))
        out.append(pth(f"M{x + w + i * 3} {yy} L{x + w + (i + 1) * 3} {yy - dy}", stroke=INK, w=1.0, op=0.5))
    return "".join(out)


def wall(x, y, w, h):
    return rect(x, y, w, h, fill="url(#brick)", stroke=INK, sw=1.2)


def screen(x, y, w, h, frame=OCHRE, panel=PAPER_D):
    """屏风：三扇。"""
    out = [rect(x, y, w, h, fill=panel, stroke=frame, sw=3.0)]
    out.append(rect(x + 7, y + 7, w - 14, h - 14, fill="none", stroke=frame, sw=0.9, op=0.7))
    for i in (1, 2):
        out.append(line(x + w * i / 3, y, x + w * i / 3, y + h, frame, 2.4))
    return "".join(out)


def lantern(x, y, s=1.0):
    """一盏挂灯，y 为悬挂点。"""
    out = [line(x, y - 26, x, y, GOLD, 1.2)]
    out.append(circ(x, y + 15 * s, 15 * s, fill="#f2c05c", stroke=INK, sw=1.3, op=0.92))
    out.append(circ(x, y + 15 * s, 15 * s, fill="url(#glow)", stroke=None))
    out.append(line(x - 15 * s, y + 15 * s, x + 15 * s, y + 15 * s, INK, 1.0, 0.5))
    out.append(line(x, y - 1, x, y + 31 * s, INK, 1.0, 0.35))
    out.append(rect(x - 6 * s, y - 2, 12 * s, 4, fill=GOLD, stroke=INK, sw=0.9))
    out.append(rect(x - 6 * s, y + 29 * s, 12 * s, 4, fill=GOLD, stroke=INK, sw=0.9))
    return "".join(out)


# ============================================================ 器物
def table(x, y, w, h=9, color=OCHRE):
    """翘头案，y 为案面。"""
    out = []
    out.append(pth(f"M{x} {y} L{x + w} {y} L{x + w} {y + h} L{x} {y + h} Z",
                   fill=color, stroke=INK, w=1.3))
    out.append(pth(f"M{x - 10} {y - 6} C{x - 2} {y - 6} {x + 2} {y} {x + 8} {y} "
                   f"M{x + w + 10} {y - 6} C{x + w + 2} {y - 6} {x + w - 2} {y} {x + w - 8} {y}",
                   stroke=color, w=4.0))
    for px in (x + w * 0.10, x + w * 0.90):
        out.append(pth(f"M{px} {y + h} l0 {52} l{-7} 0 l-3 -52 Z", fill=color, stroke=INK, w=1.2))
        out.append(pth(f"M{px - 14} {y + h + 52} l28 0", stroke=INK, w=1.6))
    return "".join(out)


def arm(x0, y0, x1, y1, w0=8.0, w1=10.0, fill=None, hand=False):
    """一段袖子，从肩到腕。给跪像补一只伸出去的手。"""
    return _sleeve(x0, y0, x1, y1, w0, w1, fill if fill is not None else DARK, hand=hand)


def seal_face(x, y, s, cells=8, fill=CINNABAR, op=1.0, broken=0.0, seed=7, jitter=1.0):
    """一方印面：cells×cells 的格。broken>0 时格线崩散下滑。"""
    out = [rect(x, y, s, s, fill=fill, stroke=None, op=op)]
    inner = s * 0.09
    cw = (s - inner * 2) / cells
    for i in range(cells):
        for j in range(cells):
            if broken and ((i * 7 + j * 13 + seed) % 11) < broken * 3.6:
                continue
            dx = dy = 0
            if broken:
                t = (j / cells) ** 2
                dx = ((i * 5 + j * 3) % 5 - 2) * broken * 3.4 * t * jitter
                dy = ((i * 3 + j * 7) % 6) * broken * 5.2 * t * jitter
            ww = cw * (0.62 + 0.22 * (((i * 5 + j * 11 + seed) % 4) / 3))
            hh = cw * 0.44
            if broken and ((i * 3 + j * 5 + seed) % 7) < broken * 2.4:
                hh *= 0.42
            out.append(rect(x + inner + i * cw + (cw - ww) / 2 + dx,
                            y + inner + j * cw + (cw - hh) / 2 + dy,
                            ww, hh, fill=WHITE, stroke=None, op=0.92 * op))
    out.append(rect(x + inner * 0.5, y + inner * 0.5, s - inner, s - inner,
                    fill="none", stroke=WHITE, sw=0.9, op=0.7 * op))
    return "".join(out)


def seal_impression(x, y, s, fill=CINNABAR, op=0.9, cells=4):
    """小印影：一枚带框的朱方块，内里四点纹。"""
    out = [rect(x, y, s, s, fill=fill, stroke=None, op=op)]
    out.append(rect(x + s * 0.10, y + s * 0.10, s * 0.80, s * 0.80,
                    fill="none", stroke=WHITE, sw=s * 0.05, op=0.75 * op))
    for (px, py) in ((0.28, 0.28), (0.60, 0.28), (0.28, 0.60), (0.60, 0.60)):
        out.append(rect(x + s * px, y + s * py, s * 0.16, s * 0.16, fill=WHITE, stroke=None, op=0.85 * op))
    return "".join(out)


def chain_link(x1, y1, x2, y2, n=None, color=GOLD, w=1.7, ring=(7, 4)):
    """两点之间一串链环。"""
    L = math.hypot(x2 - x1, y2 - y1)
    if not n:
        n = max(2, int(L / (ring[0] * 1.5)))
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    out = [line(x1, y1, x2, y2, color, w * 0.9, 0.55)]
    for i in range(n):
        t = (i + 0.5) / n
        cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        rx, ry = (ring[0], ring[1]) if i % 2 == 0 else (ring[1], ring[0])
        out.append(ell(cx, cy, rx, ry, stroke=GAMBOGE, sw=w, rot=ang))
    return "".join(out)


def palm_leaf(x, y, w, h, angle=0, fill="#e9d6ae", edge=OCHRE, lines=9, pad=False):
    """贝叶：一片多罗树叶。x,y 为叶心。"""
    out = [f'<g transform="translate({x},{y}) rotate({angle})">']
    out.append(pth(f"M{-w / 2} 0 C{-w * 0.30} {-h} {w * 0.30} {-h} {w / 2} 0 "
                   f"C{w * 0.30} {h} {-w * 0.30} {h} {-w / 2} 0 Z",
                   fill=fill, stroke=edge, w=1.9))
    out.append(line(-w / 2 + 4, 0, w / 2 - 4, 0, edge, 1.3, 0.75))
    for i in range(1, lines):
        t = i / lines
        bx = -w / 2 + w * t
        k = 1 - abs(t - 0.5) * 1.9
        out.append(pth(f"M{bx - 2} {-h * 0.02} Q{bx + w * 0.02} {-h * 0.42 * k} {bx + w * 0.06} {-h * 0.72 * k}",
                       stroke=edge, w=0.8, op=0.42))
        out.append(pth(f"M{bx - 2} {h * 0.02} Q{bx + w * 0.02} {h * 0.42 * k} {bx + w * 0.06} {h * 0.72 * k}",
                       stroke=edge, w=0.8, op=0.42))
    for sx_ in (-0.40, 0.40):
        out.append(circ(w * sx_, 0, 2.4, fill=PAPER, stroke=edge, sw=0.9))
    if pad:
        out.append(pth(f"M{-w * 0.06} 0 l{-w * 0.08} {-h * 0.18} l{w * 0.02} {h * 0.18} Z",
                       fill=fill, stroke=edge, w=1.2))
    out.append("</g>")
    return "".join(out)


def scroll_page(x, y, w, h, angle=0, fill=WHITE, edge=OCHRE, bars=True):
    """一张摊开的纸页，x,y 为左上角。"""
    out = [f'<g transform="translate({x},{y}) rotate({angle})">']
    out.append(pth(f"M0 0 L{w} 0 L{w} {h} L0 {h} Z", fill=fill, stroke=edge, w=1.4))
    if bars:
        out.append(rect(-7, -9, w + 14, 9, fill=OCHRE, stroke=INK, sw=1.1))
        out.append(rect(-7, h, w + 14, 9, fill=OCHRE, stroke=INK, sw=1.1))
    out.append("</g>")
    return "".join(out)


def text_lines(x, y, w, n, gap=7, color=INK, op=0.45, seed=3, vary=0.28):
    """一段假字：一排排短横。表示"字很多"。"""
    out = []
    for i in range(n):
        t = (i * 37 + seed * 11) % 100 / 100.0
        ww = w * (1 - vary + vary * t)
        out.append(line(x, y + i * gap, x + ww, y + i * gap, color, 1.5, op))
    return "".join(out)


def fish_half(x, y, s=1.0, side=1, fill=GOLD, edge=OCHRE, holes=3):
    """半片鱼符：鱼身自合缝起向右，尾在后。x,y 为鱼身中心。"""
    out = [f'<g transform="translate({x},{y}) scale({s * side},1)">']
    # 身
    out.append(pth("M0 -13 C14 -15 30 -13 44 -8 C46 -3 46 3 44 8 C30 13 14 15 0 13 Z",
                   fill=fill, stroke=edge, w=1.6))
    # 尾
    out.append(pth("M44 -8 C54 -14 64 -13 70 -6 L62 -1 L70 5 C64 12 54 13 44 8 Z",
                   fill=fill, stroke=edge, w=1.6))
    # 背鳍
    out.append(pth("M16 -13 C22 -20 30 -20 36 -13", fill=fill, stroke=edge, w=1.3))
    # 腹鳍
    out.append(pth("M20 13 C24 18 30 18 34 13", fill=fill, stroke=edge, w=1.2))
    # 眼与鳃
    out.append(circ(9, -4, 2.8, fill=edge, stroke=None))
    out.append(pth("M14 -9 C10 0 10 3 14 10", stroke=edge, w=1.1, op=0.75))
    # 鳞：三排弧
    for i in range(3):
        bx = 20 + i * 8
        out.append(pth(f"M{bx} -10 C{bx + 4} -4 {bx + 4} 4 {bx} 10", stroke=edge, w=0.9, op=0.5))
    # 合缝上的孔
    for i in range(holes):
        out.append(circ(1.0, -7 + i * 7, 2.6, fill=PAPER, stroke=edge, sw=1.0))
    # 合缝：锯齿
    out.append(pth("M0 -13 L-3 -7 L1 -1 L-3 5 L0 13", stroke=edge, w=1.4))
    out.append("</g>")
    return "".join(out)


def chain_link(x1, y1, x2, y2, n=None, color=GOLD, w=1.7, ring=(7, 4)):
    """两点之间一串链环。"""
    L = math.hypot(x2 - x1, y2 - y1)
    if not n:
        n = max(2, int(L / (ring[0] * 1.5)))
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    out = [line(x1, y1, x2, y2, color, w * 0.9, 0.55)]
    for i in range(n):
        t = (i + 0.5) / n
        cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        rx, ry = (ring[0], ring[1]) if i % 2 == 0 else (ring[1], ring[0])
        out.append(ell(cx, cy, rx, ry, stroke=GAMBOGE, sw=w, rot=ang))
    return "".join(out)


def palm_leaf(x, y, w, h, angle=0, fill="#e9d6ae", edge=OCHRE, lines=9, pad=False):
    """贝叶：一片多罗树叶。x,y 为叶心。"""
    out = [f'<g transform="translate({x},{y}) rotate({angle})">']
    out.append(pth(f"M{-w / 2} 0 C{-w * 0.30} {-h} {w * 0.30} {-h} {w / 2} 0 "
                   f"C{w * 0.30} {h} {-w * 0.30} {h} {-w / 2} 0 Z",
                   fill=fill, stroke=edge, w=1.9))
    out.append(line(-w / 2 + 4, 0, w / 2 - 4, 0, edge, 1.3, 0.75))
    for i in range(1, lines):
        t = i / lines
        bx = -w / 2 + w * t
        k = 1 - abs(t - 0.5) * 1.9
        out.append(pth(f"M{bx - 2} {-h * 0.02} Q{bx + w * 0.02} {-h * 0.42 * k} {bx + w * 0.06} {-h * 0.72 * k}",
                       stroke=edge, w=0.8, op=0.42))
        out.append(pth(f"M{bx - 2} {h * 0.02} Q{bx + w * 0.02} {h * 0.42 * k} {bx + w * 0.06} {h * 0.72 * k}",
                       stroke=edge, w=0.8, op=0.42))
    for sx_ in (-0.40, 0.40):
        out.append(circ(w * sx_, 0, 2.4, fill=PAPER, stroke=edge, sw=0.9))
    if pad:
        out.append(pth(f"M{-w * 0.06} 0 l{-w * 0.08} {-h * 0.18} l{w * 0.02} {h * 0.18} Z",
                       fill=fill, stroke=edge, w=1.2))
    out.append("</g>")
    return "".join(out)


def scroll_page(x, y, w, h, angle=0, fill=WHITE, edge=OCHRE, bars=True):
    """一张摊开的纸页，x,y 为左上角。"""
    out = [f'<g transform="translate({x},{y}) rotate({angle})">']
    out.append(pth(f"M0 0 L{w} 0 L{w} {h} L0 {h} Z", fill=fill, stroke=edge, w=1.4))
    if bars:
        out.append(rect(-7, -9, w + 14, 9, fill=OCHRE, stroke=INK, sw=1.1))
        out.append(rect(-7, h, w + 14, 9, fill=OCHRE, stroke=INK, sw=1.1))
    out.append("</g>")
    return "".join(out)


def text_lines(x, y, w, n, gap=7, color=INK, op=0.45, seed=3, vary=0.28):
    """一段假字：一排排短横。表示"字很多"。"""
    out = []
    for i in range(n):
        t = (i * 37 + seed * 11) % 100 / 100.0
        ww = w * (1 - vary + vary * t)
        out.append(line(x, y + i * gap, x + ww, y + i * gap, color, 1.5, op))
    return "".join(out)


def fish_half(x, y, s=1.0, side=1, fill=GOLD, edge=OCHRE, holes=3):
    """半片鱼符。x,y 为鱼身中心。"""
    out = [f'<g transform="translate({x},{y}) scale({s * side},1)">']
    out.append(pth("M0 -13 C18 -17 34 -10 36 0 C34 10 18 17 0 13 L0 -13 Z",
                   fill=fill, stroke=edge, w=1.6))
    out.append(pth("M36 0 C46 -10 57 -8 62 0 C57 8 46 10 36 0 Z", fill=fill, stroke=edge, w=1.6))
    out.append(pth("M-2 -13 L-6 -4 L0 2 L-5 8 L-2 13", stroke=edge, w=1.5))
    out.append(circ(12, -4, 2.6, fill=edge, stroke=None))
    for i in range(holes):
        out.append(circ(1.0, -8 + i * 8, 2.6, fill=PAPER, stroke=edge, sw=1.0))
    out.append("</g>")
    return "".join(out)


def bronze_lock(x, y, s=1.0, body=STEEL, open_=False):
    """广锁：横着的一条铜栓，抱柱从上面扣下。x,y 为锁身中心。"""
    out = [f'<g transform="translate({x},{y}) scale({s})">']
    out.append(pth("M-34 -8 C-34 -26 0 -30 0 -22 C0 -30 34 -26 34 -8", stroke=GOLD, w=6.0))
    out.append(pth("M-34 -8 C-34 -26 0 -30 0 -22 C0 -30 34 -26 34 -8", stroke=body, w=3.2))
    out.append(rect(-36, -9, 72, 20, rx=3, fill=body, stroke=INK, sw=1.6))
    out.append(rect(-36, -9, 72, 6, rx=2, fill=GOLD, stroke=None, op=0.55))
    for dx in (-24, 24):
        out.append(rect(dx - 3, -9, 6, 20, fill="none", stroke=INK, sw=1.0, op=0.55))
    out.append(rect(-4, -6, 8, 15, fill="#15100e", stroke=INK, sw=1.0))
    out.append(pth("M-1 -2 l2 0 l0 7 l-2 0 Z", fill=GOLD, stroke=None))
    out.append("</g>")
    return "".join(out)


def mech_key(x, y, s=1.0, body=STEEL, edge=GOLD, angle=0):
    """机关钥：铜柄、露齿、柄端一枚小齿轮。"""
    out = [f'<g transform="translate({x},{y}) rotate({angle}) scale({s})">']
    out.append(circ(-26, 0, 11, fill=body, stroke=edge, sw=1.6))
    out.append(circ(-26, 0, 4.2, fill=PAPER, stroke=edge, sw=1.2))
    for i in range(8):
        a = 45 * i
        out.append(rect(-28.5, -13.6, 5, 3.6, fill=body, stroke=edge, sw=0.8,
                        ))
    out.append(rect(-17, -4, 44, 8, rx=2, fill=body, stroke=INK, sw=1.3))
    for i, hh in enumerate((10, 6, 12)):
        out.append(rect(6 + i * 9, 3, 5, hh, fill=body, stroke=INK, sw=1.1))
    out.append(rect(24, -4, 4, 8, fill=edge, stroke=None, op=0.9))
    out.append("</g>")
    return "".join(out)


def jade_tablet(x, y, w, h, fill=JADE, edge=GOLD):
    """玉圭：上尖下方的长板。x,y 为底边中点。"""
    out = [pth(f"M{x - w / 2} {y} L{x - w / 2} {y - h * 0.82} L{x} {y - h} "
               f"L{x + w / 2} {y - h * 0.82} L{x + w / 2} {y} Z",
               fill=fill, stroke=edge, w=1.8)]
    out.append(rect(x - w / 2 + 5, y - h * 0.76, w - 10, h * 0.68,
                    fill="none", stroke=WHITE, sw=1.0, op=0.5))
    for i in range(3):
        out.append(line(x - w * 0.28, y - h * (0.18 + i * 0.18),
                        x + w * 0.28, y - h * (0.18 + i * 0.18), WHITE, 1.2, 0.45))
    return "".join(out)


def chest(x, y, w, h, body=GOLD, edge=OCHRE, locks=3):
    """金匮：一具铜箱，y 为底边。"""
    out = []
    out.append(rect(x, y - h, w, h, fill=body, stroke=INK, sw=1.8))
    out.append(pth(f"M{x} {y - h} L{x + w * 0.5} {y - h - 16} L{x + w} {y - h} Z",
                   fill=body, stroke=INK, w=1.8))
    out.append(line(x + w * 0.5, y - h, x + w * 0.5, y, edge, 1.6))
    out.append(rect(x + 6, y - h + 6, w - 12, h - 12, fill="none", stroke=edge, sw=1.1, op=0.65))
    for i in range(locks):
        lx = x + w * (i + 1) / (locks + 1)
        out.append(rect(lx - 9, y - h * 0.62, 18, 26, rx=3, fill=STEEL, stroke=INK, sw=1.2))
        out.append(circ(lx, y - h * 0.62 + 13, 3.0, fill=GOLD, stroke=INK, sw=0.8))
    return "".join(out)


def coin_stack(x, y, n=6, r=7, fill=GAMBOGE):
    """一摞铜钱。"""
    out = []
    for i in range(n):
        out.append(ell(x, y - i * 2.6, r, r * 0.34, fill=fill, stroke=OCHRE, sw=1.0))
        if i == n - 1:
            out.append(rect(x - 2.2, y - i * 2.6 - 2.2, 4.4, 4.4, fill=PAPER, stroke=OCHRE, sw=0.7))
    return "".join(out)


def tally_sticks(x, y, n=10, w=3.2, h=30, ang=0, color=OCHRE):
    """一把算筹。"""
    out = []
    for i in range(n):
        bx = x + i * (w + 1.6)
        out.append(pth(f"M{bx} {y} l{0} {-h + (i % 3) * 3}", stroke=color, w=w, op=0.9))
    return "".join(out)


def pagoda_roof(cx, y, w, h, body="#33424a", edge=GOLD, ridge=0.28):
    """一层塔檐（正面）。y 为檐口线，h 为屋面高。"""
    out = []
    d = (f"M{cx - w / 2} {y} "
         f"C{cx - w * 0.28} {y - h * 0.86} {cx - w * 0.19} {y - h} {cx - w * ridge} {y - h} "
         f"L{cx + w * ridge} {y - h} "
         f"C{cx + w * 0.19} {y - h} {cx + w * 0.28} {y - h * 0.86} {cx + w / 2} {y} "
         f"Q{cx + w * 0.508} {y + 6} {cx + w * 0.462} {y + 5} "
         f"L{cx - w * 0.462} {y + 5} Q{cx - w * 0.508} {y + 6} {cx - w / 2} {y} Z")
    out.append(pth(d, fill=body, stroke=INK, w=1.4))
    n = 15
    for i in range(n + 1):
        t = i / n
        bx = cx - w * 0.48 + w * 0.96 * t
        ex = cx + (t - 0.5) * w * 0.56
        out.append(pth(f"M{ex} {y - h + 2} C{ex + (t - 0.5) * w * 0.16} {y - h * 0.55} "
                       f"{bx + (t - 0.5) * w * 0.04} {y - h * 0.18} {bx} {y}", stroke="#5d707a", w=1.1, op=0.85))
        out.append(pth(f"M{ex + 3} {y - h + 2} C{ex + 3 + (t - 0.5) * w * 0.16} {y - h * 0.55} "
                       f"{bx + 3 + (t - 0.5) * w * 0.04} {y - h * 0.18} {bx + 3} {y}",
                       stroke="#22303a", w=0.9, op=0.55))
    out.append(line(cx - w * 0.462, y + 4, cx + w * 0.462, y + 4, edge, 1.6, 0.9))
    out.append(pth(f"M{cx - w * 0.462} {y + 5} L{cx + w * 0.462} {y + 5} L{cx + w * 0.44} {y + 9} "
                   f"L{cx - w * 0.44} {y + 9} Z", fill="#22303a", stroke=INK, w=0.8))
    out.append(rect(cx - w * ridge - 4, y - h - 5, w * ridge * 2 + 8, 6, fill="#22303a", stroke=edge, sw=0.9))
    for s_ in (-1, 1):
        out.append(pth(f"M{cx + s_ * w * ridge} {y - h - 2} "
                       f"C{cx + s_ * (w * ridge + 6)} {y - h - 15} {cx + s_ * (w * ridge + 1)} {y - h - 22} "
                       f"{cx + s_ * (w * ridge - 6)} {y - h - 11} "
                       f"C{cx + s_ * (w * ridge - 3)} {y - h - 4} {cx + s_ * (w * ridge - 7)} {y - h - 1} "
                       f"{cx + s_ * w * ridge} {y - h - 2} Z", fill="#22303a", stroke=edge, w=0.9))
    return "".join(out)


def glow(x, y, r, color="#f6c96b", op=0.55):
    """一团不带硬边的光。"""
    gid = f"g{abs(hash((x, y, r, color))) % 99999}"
    return (f'<radialGradient id="{gid}"><stop offset="0%" stop-color="{color}" stop-opacity="1"/>'
            f'<stop offset="55%" stop-color="{color}" stop-opacity="0.42"/>'
            f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/></radialGradient>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})" opacity="{op}"/>')


def dots(x, y, w, h, n=40, color=INK, r=0.9, op=0.3, seed=1):
    out = []
    for i in range(n):
        px = x + ((i * 73 + seed * 37) % 997) / 997 * w
        py = y + ((i * 149 + seed * 53) % 991) / 991 * h
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{color}" opacity="{op}"/>')
    return "".join(out)


def pine(x, y, s=1.0, trunk=OCHRE, leaf=MALACH, lean=0):
    """一棵松：干、枝、针叶团。"""
    p = [f'<g transform="translate({x},{y}) scale({s}) rotate({lean})">']
    p.append(pth(f"M0 0 C{-3} {-26} {4} {-52} {-2} {-84}", stroke=trunk, w=6.5))
    p.append(pth(f"M0 0 C{-3} {-26} {4} {-52} {-2} {-84}", stroke=INK, w=1.0, op=0.4))
    for bx, by, ln in ((-2, -80, 26), (-19, -62, 22), (17, -58, 24),
                       (-26, -42, 20), (24, -38, 18), (-8, -22, 16)):
        p.append(pth(f"M0 {by + 9} C{bx * 0.4} {by + 3} {bx * 0.8} {by - 3} {bx * 1.1} {by - 2}",
                     stroke=trunk, w=3.0))
        for k in range(3):
            yy = by - 6 + k * 7
            p.append(pth(f"M{bx - ln * 0.42 + k * 2} {yy} Q{bx} {yy - 11} {bx + ln * 0.42 - k * 2} {yy}",
                         stroke=leaf, w=2.4))
        p.append(pth(f"M{bx - ln * 0.30} {by - 12} Q{bx} {by - 24} {bx + ln * 0.30} {by - 12}",
                     stroke=leaf, w=2.0, op=0.85))
    p.append("</g>")
    return "".join(p)


def text_cols(x, y, w, h, cols=6, rows=10, color=INK, op=0.5, seed=0, sx=None):
    """竖排的假字：一列列短横。"""
    out = []
    gapx = w / cols
    gapy = h / rows
    for c in range(cols):
        cx = x + gapx * (c + 0.5)
        for r in range(rows):
            if (c * 13 + r * 7 + seed) % 17 == 0:
                continue
            ww = gapx * (0.52 + 0.22 * (((c * 5 + r * 3 + seed) % 4) / 3))
            out.append(line(cx - ww / 2, y + r * gapy, cx + ww / 2, y + r * gapy, color, 1.6, op))
    return "".join(out)


def debris(x, y, w, h, n=26, color=CINNABAR, seed=1, r=2.0, op=0.6):
    out = []
    for i in range(n):
        px = x + ((i * 61 + seed * 29) % 991) / 991 * w
        py = y + ((i * 97 + seed * 43) % 983) / 983 * h
        ww = r * (0.7 + ((i * 7) % 5) / 4)
        out.append(rect(px, py, ww, ww * 0.55, fill=color, stroke=None, op=op))
    return "".join(out)


def seal_burst(x, y, s, cells=9, uid="b0", fill=CINNABAR, seed=3, spread=1.0):
    """一方炸开的印：主体残存，碎片向右上飞散。"""
    shards = [
        ("M0 0 L0.60 0 L0.55 0.26 L0.70 0.50 L0.57 0.76 L0.64 1 L0 1 Z", 0, 0, 0),
        ("M0.60 0 L1 0 L1 0.32 L0.72 0.20 Z", 34, -40, -16),
        ("M0.70 0.30 L1 0.34 L1 0.62 L0.74 0.54 Z", 66, 4, 22),
        ("M0.60 0.64 L1 0.66 L1 1 L0.64 1 Z", 48, 44, -9),
        ("M0.62 0.06 L0.80 0.08 L0.77 0.26 L0.60 0.22 Z", 108, -66, 38),
    ]
    face = seal_face(x, y, s, cells=cells, seed=seed)
    out = []
    for i, (poly, dx, dy, rot) in enumerate(shards):
        cid = f"{uid}s{i}"
        pts = []
        for tok in poly.replace("M", "").replace("Z", "").split("L"):
            a, b = tok.strip().split()
            pts.append((x + float(a) * s, y + float(b) * s))
        d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + " Z"
        out.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        if i == 0:
            out.append(f'<g clip-path="url(#{cid})">{face}</g>')
        else:
            out.append(f'<g clip-path="url(#{cid})" transform="translate({dx * spread:.1f},'
                       f'{dy * spread:.1f}) rotate({rot} {x + s / 2} {y + s / 2})">{face}</g>')
    # 飞屑
    for i in range(150):
        t = ((i * 71) % 997) / 997
        ang = -0.75 + t * 1.9
        rad = s * (0.55 + (((i * 131) % 991) / 991) ** 0.55 * 2.3)
        bx = x + s * 0.86 + math.cos(ang) * rad * spread
        by = y + s * 0.40 + math.sin(ang) * rad * 0.85 * spread
        sz = max(1.4, 6.4 - rad / 46)
        out.append(rect(bx, by, sz, sz * 0.5, fill=fill, stroke=None,
                        op=min(0.72, 0.70 - rad / 520)))
    return "".join(out)


def seal_script(cx, cy, s, bold=1.0):
    """印面九叠篆：四个回环，远看是字，近看不是。"""
    p = []
    q = s * 0.20
    cell = s * 0.30
    for qi, (sx, sy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        ox, oy = cx + sx * q, cy + sy * q
        x0, x1 = ox - cell / 2, ox + cell / 2
        y0, y1 = oy - cell / 2, oy + cell / 2
        flip = (qi % 2) == 0
        w = s * 0.040 * bold
        if flip:
            d = (f"M{x0} {y0} L{x1} {y0} L{x1} {y1} L{x0 + cell * 0.22} {y1} "
                 f"L{x0 + cell * 0.22} {y0 + cell * 0.34} L{x1 - cell * 0.18} {y0 + cell * 0.34}")
        else:
            d = (f"M{x1} {y0} L{x0} {y0} L{x0} {y1} L{x1 - cell * 0.22} {y1} "
                 f"L{x1 - cell * 0.22} {y0 + cell * 0.34} L{x0 + cell * 0.18} {y0 + cell * 0.34}")
        p.append(pth(d, stroke=WHITE, w=w, op=0.92))
        p.append(pth(f"M{ox + sx * cell * 0.06:.1f} {oy + cell * 0.42:.1f} "
                     f"L{ox + sx * cell * 0.06:.1f} {oy + cell * 0.16:.1f}",
                     stroke=WHITE, w=w * 0.8, op=0.7))
    return "".join(p)


def jade_seal(cx, cy, s, jade=JADE, angle=0):
    """一方玉印。cy 为印身中心。"""
    top = -s / 2
    p = [f'<g transform="translate({cx},{cy}) rotate({angle})">']
    p.append(pth(f"M{-s * 0.30} {top} C{-s * 0.40} {top - s * 0.34} {-s * 0.18} {top - s * 0.52} "
                 f"{s * 0.02} {top - s * 0.42} C{s * 0.20} {top - s * 0.52} {s * 0.38} {top - s * 0.30} "
                 f"{s * 0.30} {top} Z", fill=jade, stroke=GOLD, w=1.5))
    p.append(pth(f"M{s * 0.30} {top - s * 0.22} C{s * 0.44} {top - s * 0.30} {s * 0.42} {top - s * 0.06} "
                 f"{s * 0.28} {top - s * 0.04}", stroke=GOLD, w=1.3))
    p.append(rect(-s / 2, -s / 2, s, s, fill=jade, stroke=GOLD, sw=2.0, rx=s * 0.03))
    p.append(rect(-s / 2 + s * 0.07, -s / 2 + s * 0.07, s * 0.86, s * 0.86,
                  fill="none", stroke=WHITE, sw=1.1, op=0.5))
    p.append(seal_script(0, 0, s))
    p.append("</g>")
    return "".join(p)


def sword(x, y, L, ang=0, blade="#a9b1b5", hot=False, open_pommel=False, grain=7):
    """一柄剑，横置。(x,y) 为剑格中心，ang 为剑尖方向。"""
    p = [f'<g transform="translate({x},{y}) rotate({ang})">']
    bf = "url(#blade)" if hot else blade
    p.append(pth(f"M6 -4.4 L{L * 0.80} -3.4 L{L * 0.86} 0 L{L * 0.80} 3.4 L6 4.4 Z",
                 fill=bf, stroke=INK, w=1.4))
    if hot:
        p.append(pth(f"M8 -1.4 L{L * 0.79} -1.1", stroke="#fdf0c8", w=2.0, op=0.85))
    for i in range(grain):
        t = (i + 0.5) / grain
        bx = 12 + t * (L * 0.74)
        p.append(line(bx, -3.2 + t * 0.6, bx, 3.2 - t * 0.7,
                      "#fdf0c8" if hot else "#eef3f4", 1.1, 0.75))
    p.append(rect(-1, -12, 8, 24, rx=2, fill=GOLD, stroke=INK, sw=1.3))
    p.append(rect(-26, -4.6, 26, 9.2, rx=3, fill="#5c4a36", stroke=INK, sw=1.2))
    for i in range(4):
        p.append(line(-23 + i * 6, -4.2, -21 + i * 6, 4.2, GOLD, 0.9, 0.55))
    if open_pommel:
        p.append(circ(-30, 0, 7.0, fill="#2b2320", stroke=INK, sw=1.4))
        p.append(circ(-30, 0, 4.0, fill="#15100e", stroke=None))
    else:
        p.append(circ(-30, 0, 7.0, fill=GOLD, stroke=INK, sw=1.3))
        p.append(circ(-30, 0, 2.4, fill=CINNABAR, stroke=None))
    p.append("</g>")
    return "".join(p)


def socket(x, y, r=9, ang=0):
    """柄首的空槽。"""
    return (f'<g transform="translate({x},{y}) rotate({ang})">'
            + circ(0, 0, r, fill="#2b2320", stroke=INK, sw=1.4)
            + circ(0, 0, r * 0.58, fill="#15100e", stroke=None)
            + pth(f"M{-r * 0.5} {-r * 0.55} A{r} {r} 0 0 1 {r * 0.5} {-r * 0.55}",
                  stroke=WHITE, w=1.0, op=0.35)
            + "</g>")
