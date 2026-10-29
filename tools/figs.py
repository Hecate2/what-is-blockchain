#!/usr/bin/env python3
"""《天枢账簿》十三张插图。每张是一处场景，不是一枚贴纸。"""
import math

import figkit as K


def hill(x, y, w, h, color=K.AZU_L, op=0.22):
    """一道远山，无勾线。"""
    return K.pth(f"M{x} {y} C{x + w * 0.10} {y - h * 0.62} {x + w * 0.18} {y - h * 0.92} "
                 f"{x + w * 0.30} {y - h} C{x + w * 0.40} {y - h * 0.72} "
                 f"{x + w * 0.46} {y - h * 0.50} {x + w * 0.54} {y - h * 0.58} "
                 f"C{x + w * 0.64} {y - h * 0.80} {x + w * 0.72} {y - h * 0.52} "
                 f"{x + w * 0.83} {y - h * 0.34} C{x + w * 0.92} {y - h * 0.20} "
                 f"{x + w * 0.97} {y - h * 0.08} {x + w} {y} Z", fill=color, stroke=None, op=op)


def mist(x, y, w, h, op=0.55, color="#fdf8ec"):
    """一条云带：只有面，没有边。"""
    return K.pth(f"M{x} {y} C{x + w * 0.12} {y - h * 0.75} {x + w * 0.26} {y - h} "
                 f"{x + w * 0.40} {y - h * 0.66} C{x + w * 0.52} {y - h * 1.1} "
                 f"{x + w * 0.72} {y - h * 0.98} {x + w * 0.80} {y - h * 0.60} "
                 f"C{x + w * 0.92} {y - h * 0.86} {x + w} {y - h * 0.55} {x + w} {y} Z",
                 fill=color, stroke=None, op=op)


def tongue(x, y, h, w, phase=0.0, fill=K.CINNABAR, inner=K.GAMBOGE, op=1.0):
    """一舌火。phase 让火苗有歪有正，不是同一块贴纸。"""
    tip = x + math.sin(phase) * w * 0.62
    d = (f"M{x - w / 2:.1f} {y:.1f} "
         f"C{x - w * 0.55:.1f} {y - h * 0.34:.1f} {x - w * 0.26:.1f} {y - h * 0.66:.1f} "
         f"{tip - w * 0.09:.1f} {y - h * 0.95:.1f} "
         f"C{tip - w * 0.02:.1f} {y - h * 1.00:.1f} {tip + w * 0.02:.1f} {y - h * 1.00:.1f} "
         f"{tip + w * 0.09:.1f} {y - h * 0.93:.1f} "
         f"C{x + w * 0.28:.1f} {y - h * 0.64:.1f} {x + w * 0.55:.1f} {y - h * 0.32:.1f} "
         f"{x + w / 2:.1f} {y:.1f} Z")
    out = [K.pth(d, fill=fill, stroke=K.DARK, w=1.0, op=op)]
    d2 = (f"M{x - w * 0.20:.1f} {y:.1f} "
          f"C{x - w * 0.24:.1f} {y - h * 0.24:.1f} {x - w * 0.08:.1f} {y - h * 0.44:.1f} "
          f"{tip - w * 0.01:.1f} {y - h * 0.60:.1f} "
          f"C{tip + w * 0.03:.1f} {y - h * 0.44:.1f} {x + w * 0.20:.1f} {y - h * 0.22:.1f} "
          f"{x + w * 0.20:.1f} {y:.1f} Z")
    out.append(K.pth(d2, fill=inner, stroke="none", op=op * 0.92))
    return "".join(out)


def fireband(x0, x1, y, h, n=7, w=None, fill=K.CINNABAR, inner=K.GAMBOGE, op=1.0):
    """一排火：高低错落，互相压着。"""
    out = []
    w = w or (x1 - x0) / n * 1.35
    for i in range(n):
        t = (i + 0.5) / n
        xi = x0 + (x1 - x0) * t
        hh = h * (0.62 + 0.38 * abs(math.sin(i * 1.9 + 0.6)))
        out.append(tongue(xi, y, hh, w, phase=i * 2.3, fill=fill, inner=inner, op=op))
    return "".join(out)


def spin_arc(cx, cy, rx, ry, a0, a1, color=K.GOLD, w=2.2, op=0.85):
    """一段带箭头的虚弧，表示这东西在转。a0/a1 为角度。"""
    t0, t1 = math.radians(a0), math.radians(a1)
    x0, y0 = cx + rx * math.cos(t0), cy + ry * math.sin(t0)
    x1, y1 = cx + rx * math.cos(t1), cy + ry * math.sin(t1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sw = 1 if a1 > a0 else 0
    out = [K.pth(f"M{x0:.1f} {y0:.1f} A{rx} {ry} 0 {large} {sw} {x1:.1f} {y1:.1f}",
                 stroke=color, w=w, op=op, dash="9 6")]
    ux, uy = -math.sin(t1), math.cos(t1)
    if not sw:
        ux, uy = -ux, -uy
    n = math.hypot(ux, uy) or 1.0
    ux, uy = ux / n, uy / n
    px, py = -uy, ux
    L = 11.0
    ax, ay = x1 + ux * L * 0.85, y1 + uy * L * 0.85
    bx, by = ax - ux * L, ay - uy * L
    out.append(K.pth(f"M{ax:.1f} {ay:.1f} "
                     f"L{bx + px * L * 0.52:.1f} {by + py * L * 0.52:.1f} "
                     f"L{bx - px * L * 0.52:.1f} {by - py * L * 0.52:.1f} Z",
                     fill=color, stroke="none", op=op))
    return "".join(out)


def pagoda(cx, base_y, tiers=9, base_w=200, tier_h=42, roof_h=17, body_h=21):
    out = []
    for i in range(tiers):
        w = base_w * (1 - i * 0.034)
        y = base_y - i * tier_h
        out.append(K.rect(cx - w * 0.32, y - body_h, w * 0.64, body_h,
                          fill="#f7efdd", stroke=K.OCHRE, sw=1.0))
        for s in (-1, 1):
            out.append(K.rect(cx + s * w * 0.32 - (5 if s > 0 else 0), y - body_h, 5, body_h,
                              fill=K.CINNABAR, stroke=K.INK, sw=0.6))
        win_w = w * 0.13
        lit = (i == tiers - 1)
        out.append(K.rect(cx - win_w / 2, y - body_h + 4, win_w, body_h - 8,
                          fill="#f6c96b" if lit else "#2f4a58", stroke=K.GOLD, sw=0.9))
        if lit:
            pass
        out.append(K.line(cx - win_w / 2, y - body_h / 2, cx + win_w / 2, y - body_h / 2, K.GOLD, 0.7, 0.8))
        # 平坐与栏杆
        out.append(K.railing(cx - w * 0.34, y, w * 0.68, K.GOLD, 5))
        out.append(K.dougong(cx - w * 0.36, y - body_h - 5, w * 0.72))
        out.append(K.pagoda_roof(cx, y - body_h - 6, w * 1.34, roof_h))
    top = base_y - (tiers - 1) * tier_h - body_h - 6 - roof_h
    out.append(K.pth(f"M{cx - 8} {top + 6} L{cx} {top - 28} L{cx + 8} {top + 6} Z",
                     fill=K.GOLD, stroke=K.INK, w=1.0))
    for i in range(4):
        out.append(K.ell(cx, top - 16 - i * 7, 9 - i * 1.7, 3.0, stroke=K.GOLD, sw=1.4))
    out.append(K.circ(cx, top - 46, 5.5, fill=K.CINNABAR, stroke=K.GOLD, sw=1.2))
    return "".join(out)


def ledger_stack(cx, y, w, n=22, seed=1):
    """一堆账册。"""
    out = []
    for i in range(n):
        bx = cx - w / 2 + ((i * 53 + seed * 17) % 100) / 100 * w * 0.82
        by = y + ((i * 31 + seed * 7) % 100) / 100 * 42
        bw = 34 + (i * 11 + seed) % 26
        bh = 6 + (i * 7) % 4
        out.append(K.pth(f"M{bx} {by} l{bw} 0 l3 {bh} l{-bw - 3} 0 Z",
                         fill=K.WHITE if i % 3 else "#e8d8b6", stroke=K.OCHRE, w=1.0))
        out.append(K.line(bx + 4, by + bh * 0.55, bx + bw * 0.3, by + bh * 0.6, K.CINNABAR, 1.2, 0.65))
    return "".join(out)


# ---------------------------------------------------------------- 00 万卷楼
def book_mound(cx, y, w, rows=3, seed=1):
    """一堆函套：一层层码成塔基。"""
    out = []
    for r in range(rows):
        rw = w * (1 - r * 0.16)
        ry = y - r * 15
        n = max(3, int(rw // 40))
        for i in range(n):
            bx = cx - rw / 2 + i * rw / n + ((i * 37 + r * 11 + seed) % 7) - 3
            bw = rw / n - 4
            out.append(K.pth(f"M{bx} {ry} l{bw} 0 l2 -14 l{-bw - 2} 0 Z",
                             fill=K.WHITE if (i + r) % 3 else "#e6d3ab", stroke=K.OCHRE, w=1.1))
            out.append(K.rect(bx + 3, ry - 10, bw * 0.26, 6, fill=K.CINNABAR, stroke=None, op=0.75))
            out.append(K.line(bx + 2, ry - 2, bx + bw - 2, ry - 2, K.OCHRE, 0.8, 0.6))
    return "".join(out)


def fig00():
    W, H = 720, 520
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#f7efdf"/>')
    o.append(hill(-80, 470, 330, 150, K.AZU_L, 0.14))
    o.append(hill(180, 466, 330, 180, K.AZU_L, 0.11))
    o.append(hill(430, 472, 360, 136, K.AZU_L, 0.16))
    o.append(mist(24, 292, 240, 40, 0.9))
    o.append(mist(430, 206, 260, 34, 0.8))
    o.append(mist(96, 152, 190, 26, 0.55))
    o.append(pagoda(428, 470, tiers=9, base_w=152, tier_h=44, roof_h=18, body_h=20))
    o.append(book_mound(428, 476, 236, rows=3, seed=3))
    o.append(K.pth("M300 512 L566 512 L580 530 L286 530 Z", fill="#dbcaa6", stroke=K.OCHRE, w=1.3))
    o.append(K.rock(-20, 530, 250, 116, fill="#ded0b1", op=1, seed=2))
    o.append(K.rock(556, 530, 200, 92, fill="#d8c9a6", op=1, seed=5))
    o.append(K.pine(640, 512, 1.0, lean=-4))
    o.append(K.pine(66, 520, 0.72, lean=7))
    o.append(K.person(292, 524, 60, robe=K.AZURITE, hat="jin",
                      l_arm=(-0.26, -0.40), r_arm=(0.24, -0.60)))
    o.append(K.lantern(292 + 0.24 * 60, 524 - 0.60 * 60, 0.32))
    o.append(K.person(322, 516, 56, robe=K.OCHRE, hat="douli",
                      l_arm=(-0.22, -0.38), r_arm=(0.26, -0.46)))
    o.append(K.dots(0, 0, W, H, n=80, color="#c0ae87", r=1.0, op=0.16, seed=3))
    return K.canvas(W, H, "".join(o), base="#f8f3e7")


# ---------------------------------------------------------------- 02 雪崩
def slip(x, y, w, h, seed=0, mark=None, angle=0):
    """一条抄经的纸片：几行字，一处朱圈。"""
    o = [f'<g transform="translate({x},{y}) rotate({angle})">']
    o.append(K.rect(0, 0, w, h, fill="#fbf6ea", stroke=K.OCHRE, sw=1.3, rx=2))
    o.append(K.rect(6, 6, w - 12, h - 12, fill="none", stroke=K.CINNABAR, sw=0.7, op=0.4))
    o.append(K.text_lines(16, 24, w - 34, 5, gap=13, op=0.5, seed=seed))
    if mark:
        cx, cy = mark
        o.append(K.rect(cx - 8, cy - 7, 17, 16, fill="none", stroke=K.CINNABAR, sw=2.0, rx=2))
        o.append(K.pth(f"M{cx - 4} {cy - 3} l9 0 l0 3 l-9 0 Z", fill=K.INK, stroke=None, op=0.85))
        o.append(K.pth(f"M{cx - 4} {cy + 2} l6 0 l0 3 l-6 0 Z", fill=K.INK, stroke=None, op=0.85))
    o.append("</g>")
    return "".join(o)


def fig02():
    W, H = 720, 470
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#e7d6b4"/>')
    for i in range(9):
        o.append(K.pth(f"M0 {26 + i * 52} C200 {19 + i * 52} 470 {35 + i * 52} 720 {26 + i * 52}",
                       stroke="#cfb98f", w=1.1, op=0.4))
    o.append(K.glow(360, 90, 300, "#fbeecd", 0.25))

    def page(px, py, ang, gyph, broken, uid):
        g = [f'<g transform="translate({px},{py}) rotate({ang})">']
        g.append(K.rect(0, 0, 264, 340, fill="#fbf6ea", stroke=K.OCHRE, sw=1.4, rx=2))
        g.append(K.rect(9, 9, 246, 322, fill="none", stroke=K.CINNABAR, sw=0.8, op=0.4))
        g.append(K.text_cols(24, 26, 216, 138, cols=5, rows=8, color="#5a4a32", op=0.5, seed=4))
        g.append(K.text_cols(24, 250, 216, 0.1, cols=5, rows=1, color="#5a4a32", op=0.0))
        # 朱笔圈出来的那一个字
        g.append(K.circ(132, 200, 34, fill="none", stroke=K.CINNABAR, sw=2.4))
        g.append(K.txt(132, 220, gyph, 52, "#8c2f22", K.FK))
        # 页脚的印
        if broken:
            g.append('<g transform="translate(132,286)">' + K.seal_burst(0, 0, 96, cells=8,
                     uid=uid, seed=4, spread=1.0) + "</g>")
        else:
            g.append(K.seal_face(84, 238, 96, cells=8, seed=4))
        g.append("</g>")
        return "".join(g)

    o.append(page(48, 40, -1.4, "二", False, "aa"))
    o.append(page(404, 40, 1.4, "三", True, "bb"))
    # 案上：砚与笔
    o.append(K.ell(360, 438, 44, 12, fill="#3a322b", stroke=K.INK, sw=1.4))
    o.append(K.ell(360, 434, 34, 9, fill="#15100e", stroke=None))
    o.append(K.pth("M300 448 C340 430 420 430 462 452", stroke=K.OCHRE, w=6.0))
    o.append(K.pth("M300 448 C340 430 420 430 462 452", stroke=K.INK, w=0.9, op=0.4))
    # 一只按住纸角的手
    o.append(K.hand(672, 372, 1.0, ang=204, cuff=K.DARK))
    o.append(K.arm(726, 312, 682, 366, 30.0, 15.0, K.DARK))
    return K.canvas(W, H, "".join(o), base="#e7d6b4")


# ---------------------------------------------------------------- 01 印链
def fig01():
    W, H = 720, 400
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#efe2c6"/>')
    for i in range(6):
        o.append(K.pth(f"M0 {34 + i * 64} C220 {28 + i * 64} 480 {44 + i * 64} 720 {34 + i * 64}",
                       stroke="#d8c39c", w=1.0, op=0.4))
    pages = [(40, 140, -1.6), (274, 130, 0.4), (508, 140, 1.6)]
    for i, (px, py, ang) in enumerate(pages):
        o.append(f'<g transform="translate({px},{py}) rotate({ang})">')
        o.append(K.rect(0, 0, 186, 224, fill="#fbf6ea", stroke=K.OCHRE, sw=1.3, rx=2))
        o.append(K.rect(8, 8, 170, 208, fill="none", stroke=K.CINNABAR, sw=0.9, op=0.45))
        o.append(K.text_cols(26, 24, 134, 128, cols=4, rows=11, op=0.42, seed=i + 1))
        # 页首：吞进来的前一枚印
        if i > 0:
            o.append(K.seal_impression(122, 16, 26, op=0.62))
            o.append(K.line(96, 29, 118, 29, K.GOLD, 1.2, 0.7))
        broken = 0.0 if i < 2 else 0.55
        o.append(K.seal_face(58, 156, 62, cells=6, seed=i + 2, broken=broken))
        o.append("</g>")
    # 金链：一枚印咬住下一枚印
    o.append(K.chain_link(168, 322, 316, 316, n=9, w=1.9))
    o.append(K.chain_link(396, 316, 558, 322, n=10, w=1.9))
    # 中段那道裂
    o.append(K.pth("M448 132 L430 190 L444 232 L424 282 L438 316", stroke=K.INK, w=2.0, op=0.85))
    o.append(K.pth("M448 132 L442 176 L452 204", stroke=K.INK, w=1.0, op=0.5))
    # 一只手在末页续写
    o.append(K.pth("M676 210 L640 262", stroke=K.OCHRE, w=6.4))
    o.append(K.pth("M676 210 L668 222 L674 228 L682 216 Z", fill=K.DARK, stroke=K.INK, w=1.0))
    o.append(K.pth("M642 260 C636 268 630 274 626 278", stroke=K.INK, w=2.8))
    o.append(K.hand(690, 196, 1.0, ang=224, cuff=K.AZURITE))
    return K.canvas(W, H, "".join(o), base="#efe2c6")


# ---------------------------------------------------------------- 03 剑脊
def fig03():
    """剑峰石碑：一整面碑，只刻一条曲线、一条割线、四块石与一处基点。"""
    W, H = 720, 600
    o = []

    # 碑外的粗石壁
    o.append(f'<rect width="{W}" height="{H}" fill="#d9caab"/>')
    for i in range(7):
        yy = 26 + i * 88
        o.append(K.line(0, yy, W, yy, "#bfae8c", 1.0, 0.32))
    for i in range(6):
        xx = 34 + i * 130
        o.append(K.line(xx, 0, xx + 16, H, "#c4b492", 0.8, 0.26))
    o.append(K.dots(0, 0, W, H, n=90, color="#b9a988", r=1.5, op=0.45, seed=17))

    # 碑身：右上磕去一角
    o.append(K.pth("M30 26 L688 26 L694 40 L694 576 L30 576 Z",
                   fill="#2b231c", stroke=None, op=0.16))
    o.append(K.pth("M22 18 L684 18 L700 34 L700 582 L22 582 Z",
                   fill="#f7eedc", stroke=K.INK, w=2.6))
    o.append(K.pth("M32 28 L682 28 L690 38 L690 574 L32 574 Z",
                   stroke=K.GOLD, w=1.1, op=0.8))
    o.append(K.dots(44, 40, 612, 516, n=110, color="#cbb894", r=1.1, op=0.4, seed=5))

    # 坐标映射：曲线占去碑面绝大部分
    x0, x1, ytop, ybot = 58.0, 662.0, 52.0, 548.0
    wx0, wx1, wy = -1.95, 2.88, 5.45

    def X(x):
        return x0 + (x - wx0) / (wx1 - wx0) * (x1 - x0)

    def Y(y):
        cy = (ytop + ybot) / 2
        sy = (ybot - ytop) / (2 * wy)
        return cy - y * sy

    # 横轴
    o.append(K.line(x0, Y(0), x1, Y(0), "#8d8168", 1.1, 0.42, dash="6 9"))

    # 曲线：按 y 采样，左端收得干净，不会显出折角
    ymax = 5.40
    N = 340

    def curve_x(yy):
        t = yy * yy - 7.0
        return t ** (1 / 3) if t >= 0 else -((-t) ** (1 / 3))

    for sgn in (1, -1):
        pts = []
        for k in range(N + 1):
            yy = ymax * k / N
            pts.append((X(curve_x(yy)), Y(sgn * yy)))
        d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        o.append(K.pth(d, stroke="#7d9fb0", w=15, op=0.16))
        o.append(K.pth(d, stroke=K.WHITE, w=9.4, op=0.95))
        o.append(K.pth(d, stroke=K.AZURITE, w=4.4))
        o.append(K.pth(d, stroke="#a9c8da", w=1.3, op=0.85))

    # P 在右上臂，Q 在左下首端；过两点的割线交曲线于 R
    P = (2.62, (2.62 ** 3 + 7) ** 0.5)
    Q = (-1.90, -((-1.90) ** 3 + 7) ** 0.5)
    m = (P[1] - Q[1]) / (P[0] - Q[0])
    x3 = m * m - P[0] - Q[0]
    y3 = P[1] + m * (x3 - P[0])
    R = (x3, y3)
    S = (x3, -y3)

    # 反射虚线先画，割线压在上面
    o.append(K.line(X(x3), Y(y3), X(x3), Y(-y3), K.GAMBOGE, 2.2, 0.9, dash="9 8"))

    # 割线只取 P、Q 之间，正好穿过 R；白边让它与银痕分得开
    o.append(K.line(X(Q[0]), Y(Q[1]), X(P[0]), Y(P[1]), K.WHITE, 7.4, 0.92))
    o.append(K.line(X(Q[0]), Y(Q[1]), X(P[0]), Y(P[1]), K.CINNABAR, 2.8))

    def dot(x, y, color, r=7.2, hollow=False):
        p = [K.circ(x, y, 11.4, fill=K.WHITE, stroke=None, op=0.96)]
        if hollow:
            p.append(K.circ(x, y, 6.2, fill=K.PAPER, stroke=color, sw=2.6))
        else:
            p.append(K.circ(x, y, r, fill=color, stroke=K.WHITE, sw=2.0))
            p.append(K.circ(x - r * 0.30, y - r * 0.36, 2.0, fill=K.WHITE,
                            stroke=None, op=0.6))
        return "".join(p)

    o.append(dot(X(P[0]), Y(P[1]), K.MALACH))
    o.append(dot(X(Q[0]), Y(Q[1]), K.MALACH))
    o.append(dot(X(R[0]), Y(R[1]), K.CINNABAR, hollow=True))
    o.append(dot(X(S[0]), Y(S[1]), K.GAMBOGE, r=8.0))

    # 基点 G：一块方形起跳石，落在左下臂
    gx, gy = X(-1.2), Y(-((-1.2) ** 3 + 7) ** 0.5)
    o.append(K.rect(gx - 13.6, gy - 13.6, 27.2, 27.2, rx=3.5, fill=K.WHITE, stroke=None, op=0.96))
    o.append(K.rect(gx - 9.2, gy - 9.2, 18.4, 18.4, rx=2.4, fill=K.AZURITE,
                    stroke=K.WHITE, sw=1.8))
    o.append(K.rect(gx - 4.6, gy - 4.6, 9.2, 9.2, rx=1, fill="none",
                    stroke=K.WHITE, sw=0.9, op=0.55))

    def lab(x, y, s, size, color, anchor="start", weight="700"):
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{K.FK}" font-size="{size}" '
                f'font-weight="{weight}" fill="{color}" stroke="{K.WHITE}" stroke-width="4.4" '
                f'paint-order="stroke" text-anchor="{anchor}">{s}</text>')

    o.append(lab(X(P[0]) - 24, Y(P[1]) - 6, "P", 30, K.MALACH, "end"))
    o.append(lab(X(Q[0]) + 20, Y(Q[1]) + 31, "Q", 30, K.MALACH))
    o.append(lab(X(R[0]) - 16, Y(R[1]) - 13, "R", 25, K.CINNABAR, "end"))
    o.append(lab(X(S[0]), Y(S[1]) + 40, "P+Q", 26, K.GOLD, "middle"))
    o.append(lab(gx, gy + 46, "G", 30, K.AZURITE, "middle"))
    o.append(lab(gx, gy + 70, "基点", 16, K.AZURITE, "middle", weight="400"))

    # 方程刻在左上，留白处正好容得下
    def eq(x, y, s, size, color=K.GOLD, anchor="start"):
        return (f'<text x="{x}" y="{y}" font-family="{K.FK}" font-size="{size}" font-weight="700" '
                f'fill="{color}" stroke="{K.WHITE}" stroke-width="3.4" paint-order="stroke" '
                f'text-anchor="{anchor}">{s}</text>')

    o.append(f'<text x="62" y="84" font-family="{K.FK}" font-size="16" letter-spacing="5" '
             f'fill="{K.OCHRE}">椭圆曲线</text>')
    o.append(eq(62, 128, "y", 38))
    o.append(eq(83, 114, "2", 22))
    o.append(eq(101, 128, "=", 38))
    o.append(eq(137, 128, "x", 38))
    o.append(eq(158, 114, "3", 22))
    o.append(eq(182, 128, "+", 38))
    o.append(eq(216, 128, "7", 38))

    # 左下角一方朱印，只是落款
    o.append(K.rect(48, 488, 46, 46, fill=K.CINNABAR, stroke=None, op=0.82))
    o.append(K.rect(51, 491, 40, 40, fill="none", stroke=K.WHITE, sw=1.2, op=0.7))
    o.append(K.seal_script(71, 511, 36))

    return K.canvas(W, H, "".join(o), base="#d9caab", grain=0.4)


# ---------------------------------------------------------------- 04 开山
def waterwheel(cx, cy, r):
    o = [f'<g transform="translate({cx},{cy})">']
    o.append(K.circ(0, 0, r, stroke=K.OCHRE, sw=10))
    o.append(K.circ(0, 0, r - 7, stroke=K.GOLD, sw=1.8, op=0.8))
    o.append(K.circ(0, 0, r * 0.18, fill=K.OCHRE, stroke=K.INK, sw=2))
    for i in range(10):
        a = math.radians(36 * i)
        o.append(K.line(0, 0, math.cos(a) * r, math.sin(a) * r, K.OCHRE, 4.0))
    for i in range(18):
        a = 360 * i / 18
        o.append(f'<rect x="-6" y="{-r - 11}" width="12" height="22" fill="{K.OCHRE}" '
                 f'stroke="{K.INK}" stroke-width="0.9" transform="rotate({a})"/>')
    o.append(K.circ(0, 0, r * 0.07, fill=K.GOLD, stroke=K.INK, sw=1.2))
    o.append("</g>")
    return "".join(o)


def fig04():
    W, H = 720, 460
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#e6dcc6"/>')
    # 石壁
    o.append(K.pth("M436 24 C500 16 560 40 620 26 C676 14 712 34 720 30 L720 440 L436 440 Z",
                   fill="#bcab8a", stroke=K.INK, w=1.6))
    for i in range(9):
        o.append(K.pth(f"M{452 + i * 30} 40 C{446 + i * 30} 140 {458 + i * 30} 250 {450 + i * 30} 430",
                       stroke="#a8977a", w=1.0, op=0.45))
    # 孔阵
    for r in range(7):
        for c in range(5):
            hx = 478 + c * 44 + (r % 2) * 12
            hy = 88 + r * 44
            o.append(K.ell(hx, hy, 9.2, 7.6, fill="#1b1613", stroke="none"))
            o.append(K.pth(f"M{hx - 7.6} {hy + 2.6} A9.2 7.6 0 0 0 {hx + 7.6} {hy + 2.6}",
                           stroke="#c4b695", w=1.8, op=0.8))
            o.append(K.pth(f"M{hx - 9.2} {hy} A9.2 7.6 0 0 1 {hx + 9.2} {hy}",
                           stroke="#8f8168", w=1.0, op=0.55))
            o.append(K.dots(hx - 10, hy + 8, 22, 9, n=6, color="#8d8577", r=1.5, op=0.75, seed=hx))
    # 水渠与水轮
    o.append(K.pth("M-6 296 L196 296 L206 396 L-6 396 Z", fill="#7fa5b4", stroke=K.INK, w=1.4, op=0.95))
    o.append(K.pth("M-6 296 L196 296 L192 306 L-6 306 Z", fill="#cdd8d8", stroke=None, op=0.9))
    for yy in (330, 356, 380):
        o.append(K.waterline(-4, 200, yy, 32, "#e9f1f4", 1.2, 0.55, yy % 7))
    o.append(waterwheel(150, 296, 96))
    # 钻架
    o.append(K.pth("M250 438 L266 438 L262 190 L246 190 Z", fill=K.OCHRE, stroke=K.INK, w=1.4))
    o.append(K.pth("M356 438 L372 438 L368 190 L352 190 Z", fill=K.OCHRE, stroke=K.INK, w=1.4))
    o.append(K.rect(238, 178, 152, 16, fill=K.OCHRE, stroke=K.INK, sw=1.5))
    o.append(K.rect(300, 224, 22, 190, fill=K.OCHRE, stroke=K.INK, sw=1.3))
    # 曲柄连杆
    o.append(K.line(150, 296, 200, 296, K.STEEL, 5.0))
    o.append(K.circ(200, 296, 7, fill=K.GOLD, stroke=K.INK, sw=1.2))
    o.append(K.line(200, 296, 300, 232, K.STEEL, 5.5))
    o.append(K.circ(300, 232, 8, fill=K.GOLD, stroke=K.INK, sw=1.3))
    # 钻杆
    o.append(K.pth("M322 226 L430 214 L430 244 L322 254 Z", fill="#6e7478", stroke=K.INK, w=1.4))
    o.append(K.pth("M430 222 L456 222 L456 240 L430 240 Z", fill=K.STEEL, stroke=K.INK, w=1.2))
    o.append(K.dots(452, 210, 22, 40, n=16, color="#8d8577", r=2.0, op=0.7, seed=4))
    # 猛火油柜
    o.append(K.rect(444, 384, 104, 52, fill="#8a6238", stroke=K.INK, sw=1.6))
    o.append(K.rect(444, 384, 104, 52, fill="url(#brick)", stroke=None, op=0.25))
    o.append(K.rect(448, 374, 96, 12, fill=K.GOLD, stroke=K.INK, sw=1.2))
    o.append(K.rect(470, 350, 52, 26, rx=4, fill=K.STEEL, stroke=K.INK, sw=1.3))
    o.append(K.pth("M522 362 L556 356", stroke=K.STEEL, w=8.0))
    o.append(K.circ(556, 356, 5.4, fill="#20292d", stroke=K.INK, sw=1.2))
    # 一条火龙：从喷嘴横着舔上石壁
    o.append(K.glow(590, 350, 74, "#f2a63c", 0.34))
    # 一条笔直的火线，到石壁上炸开
    o.append(K.pth("M556 349 C578 346 598 344 618 341 L618 371 "
                   "C598 368 578 365 556 363 Z", fill="#f6c96b", stroke=None))
    o.append(K.pth("M556 349 C578 346 598 344 618 341 L618 371 "
                   "C598 368 578 365 556 363 Z", stroke="#a8322a", w=1.2, op=0.85))
    for yy, hh, ww, ph in ((418, 54, 30, 2.9), (392, 84, 36, 1.6), (360, 104, 40, 3.4),
                           (326, 92, 38, 2.1), (298, 66, 32, 0.8)):
        o.append(f'<g transform="translate({616 + (yy % 7)}, {yy})">'
                 + tongue(0, 0, hh, ww, ph) + "</g>")
    o.append(K.glow(616, 356, 96, "#f2a63c", 0.4))
    for i in range(12):
        o.append(K.circ(600 + (i * 23) % 70, 292 + ((i * 37) % 116), 2.2 - i * 0.07,
                        fill="#f2a63c", stroke=None, op=0.6))
    # 两个匠人
    o.append(K.person(410, 442, 96, robe="#6d5a44", hat="jin",
                      l_arm=(-0.24, -0.40), r_arm=(0.42, -0.46)))
    o.append(K.person(560, 442, 92, robe="#5c4a38", hat="douli",
                      l_arm=(-0.40, -0.46), r_arm=(0.24, -0.38)))
    # 碎石
    o.append(K.rock(320, 460, 130, 46, fill="#a8977a", op=1, seed=3))
    return K.canvas(W, H, "".join(o), base="#e6dcc6")


# ---------------------------------------------------------------- 05 合符
FISH_D = ("M44 0 C38 -10 26 -15 12 -16 L-8 -15 C-16 -13 -20 -9 -22 -6 "
          "L-38 -18 L-30 0 L-38 18 L-22 6 C-20 9 -16 13 -8 15 L12 16 "
          "C26 15 38 10 44 0 Z")


def fish_body(cx, cy, s, gap=12, fill=K.GOLD, edge=K.OCHRE, bg="#efe2c6"):
    """一尾鱼符：中间锯开，两半各让开半个 gap。"""
    seam = [(-20, 0), (-10, -2.2), (-3, 1.6), (4, -2.2), (11, 0.8), (20, 0)]
    inner = [
        f'<path d="{FISH_D}" fill="{fill}" stroke="{edge}" stroke-width="2.4" stroke-linejoin="round"/>',
        f'<path d="M12 -16 C18 -25 28 -25 32 -15" fill="{fill}" stroke="{edge}" stroke-width="1.8"/>',
        f'<path d="M8 16 C13 24 21 24 25 15" fill="{fill}" stroke="{edge}" stroke-width="1.4"/>',
        f'<circle cx="30" cy="-3" r="3.4" fill="{edge}"/>',
        f'<path d="M22 -11 C17 0 17 5 22 12" fill="none" stroke="{edge}" stroke-width="1.4" opacity="0.7"/>',
    ]
    for i in range(4):
        bx = 4 - i * 7
        inner.append(f'<path d="M{bx} -12 C{bx - 3} -4 {bx - 3} 4 {bx} 12" fill="none" '
                     f'stroke="{edge}" stroke-width="1.1" opacity="0.45"/>')
    out = [f'<g transform="translate({cx},{cy}) scale({s})">{"".join(inner)}</g>']

    def pt(lx, ly, dx):
        return f"{cx + lx * s + dx:.1f} {cy + ly * s:.1f}"

    left = [pt(lx, ly, -gap / 2) for lx, ly in seam]
    right = [pt(lx, ly, gap / 2) for lx, ly in seam]
    band = "M" + " L".join(left) + " L" + " L".join(reversed(right)) + " Z"
    out.append(f'<path d="{band}" fill="{bg}" stroke="none"/>')
    out.append(f'<path d="M{" L".join(left)}" fill="none" stroke="{edge}" stroke-width="2.4"/>')
    out.append(f'<path d="M{" L".join(right)}" fill="none" stroke="{edge}" stroke-width="2.4"/>')
    return "".join(out)


def fig05():
    W, H = 720, 430
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#241d17"/>')
    for i in range(14):
        o.append(K.line(0, 8 + i * 32, W, 4 + i * 32, "#2e251c", 1.0, 0.5))
    o.append(K.glow(150, 60, 240, "#f2c05c", 0.16))
    # 乌木盘
    o.append(K.rect(60, 44, 600, 348, rx=14, fill="#1b1512", stroke="#0d0908", sw=2.0))
    o.append(K.rect(74, 58, 572, 320, rx=8, fill="#3a2b20", stroke="#120d0a", sw=1.4))
    # 三寸细沙
    o.append(K.rect(88, 72, 544, 292, rx=5, fill="#e8d7b0", stroke="#b99f74", sw=1.2))
    for i in range(11):
        yy = 84 + i * 26
        o.append(K.pth(f"M96 {yy} Q 240 {yy - 5} 360 {yy} T 624 {yy - 2}",
                       stroke="#d3bd90", w=1.2, op=0.55))
    o.append(K.glow(360, 230, 190, "#fbeec8", 0.22))
    # 沙上三个字：开山祖
    for cx_, ch in ((190, "开"), (308, "山"), (426, "祖")):
        o.append(K.txt(cx_ + 2, 306 + 3, ch, 84, "#f6ecd4", K.FK, op=0.9))
        o.append(K.txt(cx_, 306, ch, 84, "#6d5b42", K.FK, op=0.95))
    # 第四个字：才起了两笔，就断了
    for d_, w_ in (("M520 254 l0 74", 7.0), ("M492 258 l52 0", 7.0),
                   ("M492 258 l0 30", 6.0)):
        o.append(K.pth(d_, stroke="#f4e7c6", w=w_, op=0.55))
        o.append(K.pth(d_, stroke="#6d5b42", w=w_ * 0.72, op=0.95))
    o.append(K.pth("M528 300 C548 316 574 320 590 306", stroke="#8a7452", w=4.4, op=0.45))
    # 笔痕：沙被推起来的一道脊
    o.append(K.pth("M470 336 C520 344 566 338 604 318", stroke="#f4e7c6", w=7.0, op=0.6))
    o.append(K.pth("M566 246 C588 254 596 266 592 280", stroke="#c9b389", w=1.4, op=0.5))
    # 丫形桃木笔：下端点在沙上
    o.append(K.pth("M500 286 L500 178", stroke="#8c5a3c", w=9.0))
    o.append(K.pth("M500 286 L500 178", stroke="#4a2c1c", w=1.2, op=0.5))
    o.append(K.pth("M500 190 L420 142", stroke="#8c5a3c", w=8.0))
    o.append(K.pth("M500 190 L580 142", stroke="#8c5a3c", w=8.0))
    o.append(K.circ(500, 186, 8.0, fill="#a06a44", stroke="#4a2c1c", sw=1.3))
    o.append(K.pth("M496 288 l8 0 l-4 10 Z", fill="#3a2417", stroke="#4a2c1c", w=1.0))
    # 两只手，各扶一端
    o.append(K.arm(-40, 236, 410, 140, 34.0, 16.0, K.AZURITE))
    o.append(K.hand(414, 140, 1.05, ang=-22))
    o.append(K.arm(760, 236, 590, 140, 34.0, 16.0, K.CINNABAR))
    o.append(K.hand(586, 140, 1.05, ang=202))
    # 盘沿上落的一点沙
    o.append(K.dots(88, 358, 544, 12, n=22, color="#c9b389", r=1.3, op=0.5, seed=5))
    return K.canvas(W, H, "".join(o), base="#241d17", grain=0.18)


# ---------------------------------------------------------------- 06 三器
def censer(x, y, s=1.0):
    """三足铜炉，炉里一盘香篆。"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    o.append(K.pth("M-38 -30 C-38 -46 38 -46 38 -30 L32 2 L-32 2 Z", fill="#7a6238", stroke=K.INK, w=1.5))
    o.append(K.ell(0, -30, 38, 11, fill="#8c7245", stroke=K.INK, sw=1.4))
    o.append(K.ell(0, -30, 30, 8, fill="#5a4a2c", stroke=None))
    for i in range(4):
        rr = 26 - i * 6
        o.append(K.ell(0, -30, rr, rr * 0.28, stroke=K.GAMBOGE, sw=2.2, op=0.95))
    o.append(K.pth("M-6 -30 A8 8 0 1 1 6 -30", stroke=K.CINNABAR, w=2.6))
    o.append(K.ell(0, -29, 5, 2.4, fill=K.CINNABAR, stroke=None))
    for sx in (-1, 1):
        o.append(K.pth(f"M{sx * 36} -26 C{sx * 52} -30 {sx * 52} -12 {sx * 34} -14",
                       stroke=K.INK, w=2.2))
        o.append(K.pth(f"M{sx * 22} 2 l{sx * 2} 18 l{sx * 8} 0 l{sx * -2} -18 Z",
                       fill="#7a6238", stroke=K.INK, w=1.2))
    o.append("</g>")
    return "".join(o)


def bonsai(x, y, s=1.0):
    """一盆松，三枝共擎一盏灯。"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    o.append(K.pth("M-46 0 L46 0 L34 26 L-34 26 Z", fill="#8c5a3c", stroke=K.INK, w=1.5))
    o.append(K.ell(0, 0, 46, 10, fill="#5a3a26", stroke=K.INK, sw=1.4))
    o.append(K.pth("M-4 0 C-6 -26 4 -44 -2 -66", stroke="#6b4a30", w=7))
    for i, (dx, dy) in enumerate(((-34, -96), (32, -102), (2, -112))):
        o.append(K.pth(f"M-2 -62 C{dx * 0.4} {-72} {dx * 0.8} {-84} {dx} {dy}",
                       stroke="#6b4a30", w=5.0))
        o.append(K.pth(f"M{dx} {dy} C{dx * 0.72} {dy - 16} {dx * 0.3} {dy - 22} "
                       f"{dx * 0.06} {dy - 26}", stroke="#6b4a30", w=3.4))
    o.append(K.lantern(0, -140, 0.66))
    o.append(K.glow(0, -126, 46, "#f6c96b", 0.4))
    for dx, dy in ((-34, -96), (32, -102)):
        for k in range(3):
            o.append(K.pth(f"M{dx - 12 + k * 3} {dy - 4 + k * 6} Q{dx} {dy - 18 + k * 5} "
                           f"{dx + 12 - k * 3} {dy - 4 + k * 6}", stroke=K.MALACH, w=2.4))
    o.append("</g>")
    return "".join(o)


def sluice(x, y, s=1.0):
    """十二渠汇一斗，斗下带水轮。"""
    o = [f'<g transform="translate({x},{y}) scale({s})">']
    # 渠身
    o.append(K.pth("M-104 4 L104 4 L92 40 L-92 40 Z", fill="#8c7245", stroke=K.INK, w=1.5))
    o.append(K.pth("M-92 10 L92 10 L82 32 L-82 32 Z", fill="#5b8fa3", stroke=None, op=0.95))
    # 十二条从两侧进水的支渠
    for i in range(6):
        sx = -1 if i % 2 == 0 else 1
        bx = sx * (26 + (i // 2) * 26)
        o.append(K.pth(f"M{bx + sx * 52} {-28 + (i // 2) * 9} L{bx + sx * 6} 12 "
                       f"L{bx + sx * -2} 12 L{bx + sx * 44} {-32 + (i // 2) * 9} Z",
                       fill="#7d5f34", stroke=K.INK, w=1.2))
        o.append(K.pth(f"M{bx + sx * 48} {-26 + (i // 2) * 9} L{bx + sx * 8} 10 "
                       f"L{bx + sx * 4} 10 L{bx + sx * 44} {-29 + (i // 2) * 9} Z",
                       fill="#5b8fa3", stroke=None, op=0.9))
    # 斗门
    o.append(K.rect(-16, -14, 32, 30, fill="#6b5330", stroke=K.INK, sw=1.4))
    o.append(K.rect(-9, -8, 18, 18, fill="#15100e", stroke=K.GOLD, sw=1.0))
    # 水轮
    o.append(K.circ(0, 40, 22, stroke=K.OCHRE, sw=4.6))
    o.append(K.circ(0, 40, 6, fill=K.GOLD, stroke=K.INK, sw=1.0))
    for i in range(8):
        a = math.radians(45 * i)
        o.append(K.line(0, 40, math.cos(a) * 22, 40 + math.sin(a) * 22, K.OCHRE, 2.4))
    o.append("</g>")
    return "".join(o)


def fig06():
    W, H = 720, 430
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#efe2c6"/>')
    o.append(K.rect(0, 0, W, 250, fill="url(#brick)", stroke=None, op=0.45))
    # 人站在案后
    o.append(K.person(452, 330, 208, robe=K.DARK, hat="futou",
                      l_arm=(-0.34, -0.54), r_arm=(0.28, -0.42), face=True, beard=True))
    # 翘头案
    o.append(K.pth("M40 292 L680 292 L690 344 L30 344 Z", fill="#b98f5e", stroke=K.INK, w=1.5))
    o.append(K.pth("M30 344 L690 344 L690 356 L30 356 Z", fill="#8c5a3c", stroke=K.INK, w=1.3))
    o.append(K.pth("M18 286 C30 286 34 292 44 292 L30 292 Z", fill="#8c5a3c", stroke=K.INK, w=1.2))
    o.append(K.pth("M702 286 C690 286 686 292 676 292 L690 292 Z", fill="#8c5a3c", stroke=K.INK, w=1.2))
    for px in (90, 630):
        o.append(K.pth(f"M{px} 356 l0 70 l-9 0 l-4 -70 Z", fill="#8c5a3c", stroke=K.INK, w=1.2))
    # 三器
    o.append(censer(126, 292, 1.0))
    o.append(K.smoke(126, 254, 100, 14, 1, K.ASH, 0.42))
    o.append(bonsai(284, 292, 0.96))
    o.append(sluice(576, 292, 0.94))
    return K.canvas(W, H, "".join(o), base="#efe2c6")


# ---------------------------------------------------------------- 07 转轮藏
def zhuanlun(cx, base_y, w, h, rows=7):
    """八角转轮藏：中面加两侧斜面，格子里是抽屉。"""
    o = []
    cw = w * 0.56
    sw = w * 0.22
    top = base_y - h
    o.append(K.pth(f"M{cx - cw / 2} {top} L{cx + cw / 2} {top} "
                   f"L{cx + cw / 2 + sw} {top + 26} L{cx - cw / 2 - sw} {top + 26} Z",
                   fill="#7a5f42", stroke=K.INK, w=1.5))
    for s_, x0 in ((-1, cx - cw / 2 - sw), (1, cx + cw / 2)):
        o.append(K.pth(f"M{x0} {top + 26} L{x0 + s_ * sw} {top + 26} "
                       f"L{x0 + s_ * sw} {base_y - 30} L{x0} {base_y - 30} Z",
                       fill="#6b5338", stroke=K.INK, w=1.4))
    o.append(K.rect(cx - cw / 2, top + 26, cw, h - 56, fill="#8c6e48", stroke=K.INK, sw=1.4))
    rh = (h - 56 - 26) / rows
    for r in range(rows):
        yy = top + 36 + r * rh
        for c in range(4):
            bx = cx - cw / 2 + 10 + c * (cw - 20) / 4
            bw = (cw - 20) / 4 - 7
            o.append(K.rect(bx, yy, bw, rh - 9, fill="#c9ab7c", stroke=K.INK, sw=1.1))
            o.append(K.rect(bx + 5, yy + rh * 0.42, bw - 10, rh * 0.20,
                            fill=K.GOLD, stroke=K.INK, sw=0.8))
    for s_, x0 in ((-1, cx - cw / 2 - sw), (1, cx + cw / 2)):
        for r in range(rows):
            yy = top + 36 + r * rh
            o.append(K.rect(x0 + (6 if s_ > 0 else 4), yy, sw - 12, rh - 9,
                            fill="#b89a6c", stroke=K.INK, sw=1.0))
    # 底座齿轮
    o.append(K.rect(cx - cw * 0.62, base_y - 30, cw * 1.24, 18, fill="#6b5338", stroke=K.INK, sw=1.4))
    for i in range(14):
        a = 360 * i / 14
        o.append(f'<rect x="-6" y="-30" width="12" height="14" fill="#5c4a34" stroke="{K.INK}" '
                 f'stroke-width="0.9" transform="translate({cx},{base_y - 12}) rotate({a})"/>')
    o.append(K.circ(cx, base_y - 12, 28, fill="#7a5f42", stroke=K.INK, sw=1.5))
    o.append(K.circ(cx, base_y - 12, 12, fill=K.GOLD, stroke=K.INK, sw=1.2))
    # 推杆
    o.append(K.pth(f"M{cx - cw / 2 - sw - 4} {base_y - 120} L{cx - cw / 2 - sw - 92} "
                   f"{base_y - 40}", stroke="#6b4a30", w=7.0))
    return "".join(o)


def fig07():
    W, H = 720, 512
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#eee0c4"/>')
    o.append(K.rect(0, 0, W, 440, fill="url(#brick)", stroke=None, op=0.4))
    o.append(K.rect(0, 440, W, H - 440, fill="#d6c49f", stroke=None, op=0.9))
    o.append(K.line(0, 440, W, 440, K.INK, 1.5, 0.65))
    o.append(zhuanlun(360, 438, 300, 330))
    # 推柜的僧人
    o.append(K.person(196, 470, 200, robe="#a8623a", hat="none",
                      l_arm=(-0.34, -0.62), r_arm=(0.34, -0.62), face=True))
    # 签筒：签头上系钱，签尾坠砣
    o.append(K.pth("M538 372 L610 372 L604 440 L544 440 Z", fill="#8c5a3c", stroke=K.INK, w=1.5))
    o.append(K.ell(574, 372, 36, 9, fill="#5a3a26", stroke=K.INK, sw=1.2))
    for i, dx in enumerate((-18, -6, 8, 20)):
        hh = 58 + (i % 3) * 16
        o.append(K.line(574 + dx, 378, 574 + dx + 4, 378 - hh, K.OCHRE, 4.0))
        o.append(K.circ(574 + dx + 4, 378 - hh, 3.4, fill=K.CINNABAR, stroke=K.INK, sw=0.8))
    o.append(K.coin_stack(600, 300, 5, 7))
    o.append(K.pth("M600 300 C600 322 592 332 586 340", stroke=K.CINNABAR, w=1.6))
    o.append(K.circ(590, 344, 5, fill=K.STEEL, stroke=K.INK, sw=1.0))
    # 抽出来的一支：沉的那支
    o.append(K.line(504, 386, 470, 300, K.OCHRE, 4.6))
    o.append(K.coin_stack(470, 300, 4, 6))
    o.append(K.circ(506, 386, 5, fill=K.STEEL, stroke=K.INK, sw=1.0))
    # 地上被削功的那一格
    o.append(K.rect(70, 452, 96, 44, fill="#c9ab7c", stroke=K.INK, sw=1.3))
    o.append(K.rect(78, 460, 80, 28, fill="none", stroke=K.GOLD, sw=1.0, op=0.7))
    o.append(K.pth("M118 448 L132 470 L120 496", stroke=K.INK, w=2.0, op=0.8))
    return K.canvas(W, H, "".join(o), base="#eee0c4")


# ---------------------------------------------------------------- 08 式神
def paper_figure(x, y, h=260, robe="#f6efdd", grid=(5, 6), lit=(3, 4)):
    """纸人：背对观者，背上开着契文格。"""
    o = []
    w = 0.20 * h
    o.append(K.pth(f"M{-w} 0 C{-w * 1.04} {-0.30 * h} {-w * 0.62} {-0.52 * h} {-0.10 * h} {-0.58 * h} "
                   f"L{-0.10 * h} {-0.80 * h} L{0.10 * h} {-0.80 * h} L{0.10 * h} {-0.58 * h} "
                   f"C{w * 0.62} {-0.52 * h} {w * 1.04} {-0.30 * h} {w} 0 Z",
                   fill=robe, stroke=K.INK, w=1.6))
    o.append(K.pth("M-0.098*h -0.80*h C-0.24*h -0.74*h -0.30*h -0.52*h -0.28*h -0.34*h "
                   "L-0.14*h -0.36*h L-0.10*h -0.56*h Z".replace("*h", f"*{h}"),
                   fill=robe, stroke=K.INK, w=1.5))
    o.append(K.pth("M0.098*h -0.80*h C0.24*h -0.74*h 0.30*h -0.52*h 0.28*h -0.34*h "
                   "L0.14*h -0.36*h L0.10*h -0.56*h Z".replace("*h", f"*{h}"),
                   fill=robe, stroke=K.INK, w=1.5))
    # 背上那面契文格
    gx, gy, gw = -0.075 * h, -0.52 * h, 0.15 * h
    gh = 0.30 * h
    o.append(K.rect(gx, gy, gw, gh, fill="#fdf8ec", stroke=K.CINNABAR, sw=1.6))
    cols, rows = grid
    cw, ch = gw / cols, gh / rows
    for r in range(rows):
        for c in range(cols):
            is_lit = (c, rows - 1 - r) == lit
            o.append(K.rect(gx + c * cw + 1.4, gy + r * ch + 1.4, cw - 2.8, ch - 2.8,
                            fill=K.CINNABAR if is_lit else "none",
                            stroke=K.CINNABAR, sw=0.8, op=1.0 if is_lit else 0.55))
    # 头与纸褶
    o.append(K.circ(0, -0.855 * h, 0.062 * h * 1.0, fill=robe, stroke=K.INK, sw=1.4))
    for k in (-0.6, 0.1, 0.7):
        o.append(K.pth(f"M{k * w} {-0.02 * h} C{k * w * 0.9} {-0.20 * h} {k * w * 0.5} {-0.34 * h} "
                       f"{k * w * 0.3} {-0.46 * h}", stroke=K.INK, w=1.0, op=0.3))
    # 烧焦的边
    o.append(K.pth(f"M{-w} 0 L{w} 0 L{w * 0.86} {-0.05 * h} L{-w * 0.9} {-0.04 * h} Z",
                   fill="#2b2320", stroke=None, op=0.75))
    o.append(K.dots(-0.12 * h, -0.10 * h, 0.24 * h, 0.10 * h, n=26, color="#2b2320", r=1.6, op=0.35, seed=5))
    return f'<g transform="translate({x},{y})">' + "".join(o) + "</g>"


def shadow_figure(x, y, h=280, robe="#1a1512"):
    """无脸的黑影。"""
    o = []
    w = 0.19 * h
    o.append(K.pth(f"M{-w} 0 C{-w * 1.06} {-0.34 * h} {-w * 0.56} {-0.56 * h} {-0.09 * h} {-0.60 * h} "
                   f"L{-0.09 * h} {-0.80 * h} L{0.09 * h} {-0.80 * h} L{0.09 * h} {-0.60 * h} "
                   f"C{w * 0.56} {-0.56 * h} {w * 1.06} {-0.34 * h} {w} 0 Z",
                   fill=robe, stroke=K.INK, w=1.3))
    o.append(K.pth(f"M{-0.088 * h} {-0.78 * h} C{-0.30 * h} {-0.70 * h} {-0.36 * h} {-0.40 * h} "
                   f"{-0.30 * h} {-0.10 * h} L{-0.16 * h} {-0.16 * h} L{-0.10 * h} {-0.56 * h} Z",
                   fill=robe, stroke=K.INK, w=1.2))
    o.append(K.pth(f"M{0.088 * h} {-0.78 * h} C{0.26 * h} {-0.76 * h} {0.34 * h} {-0.70 * h} "
                   f"{0.42 * h} {-0.62 * h} L{0.36 * h} {-0.52 * h} L{0.10 * h} {-0.58 * h} Z",
                   fill=robe, stroke=K.INK, w=1.2))
    o.append(K.ell(0, -0.86 * h, 0.058 * h, 0.070 * h, fill=robe, stroke=K.INK, sw=1.2))
    o.append(K.pth(f"M{-0.058 * h} {-0.90 * h} C{-0.04 * h} {-0.95 * h} {0.04 * h} {-0.95 * h} "
                   f"{0.058 * h} {-0.90 * h} Z", fill=robe, stroke=K.INK, w=1.0))
    return f'<g transform="translate({x},{y})">' + "".join(o) + "</g>"


def fig08():
    W, H = 720, 512
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#3a322b"/>')
    o.append(K.rect(0, 0, W, 460, fill="url(#brick)", stroke=None, op=0.55))
    o.append(K.rect(0, 0, W, H, fill="#2b2320", stroke=None, op=0.30))
    o.append(K.rect(0, 452, W, H - 452, fill="#2b2320", stroke=None, op=0.55))
    o.append(K.glow(150, 120, 130, "#f2c05c", 0.32))
    o.append(K.lantern(150, 84, 0.8))
    o.append(paper_figure(296, 470, 268))
    o.append(shadow_figure(596, 470, 288))
    # 一条长袖从黑影伸到纸人背上，指头压住传音格
    o.append(K.pth("M470 286 C440 278 414 286 396 300 L392 322 C412 316 442 312 470 316 Z",
                   fill="#1a1512", stroke=K.INK, w=1.2))
    o.append(K.hand(398, 310, 0.95, ang=182, cuff="#1a1512"))
    # 功德从纸里流出来
    for i in range(3):
        o.append(K.pth(f"M330 {368 + i * 14} C390 {352 + i * 16} 450 {382 + i * 12} 508 {368 + i * 14}",
                       stroke=K.GAMBOGE if i % 2 == 0 else "#f2c05c", w=3.4 - i * 0.6, op=0.75))
    # 地上数过三遍的筹
    for k, bx in enumerate((52, 108, 164)):
        for i in range(9):
            o.append(K.line(bx + i * 5, 486, bx + i * 5, 460 - (i % 3) * 3, K.OCHRE, 3.4))
    o.append(K.dots(0, 0, W, H, n=70, color="#f2c05c", r=1.2, op=0.20, seed=7))
    return K.canvas(W, H, "".join(o), base="#3a322b", grain=0.12)


# ---------------------------------------------------------------- 09 贝叶经塔
def leaf_pagoda(cx, base_y, tiers=12, base_w=142, tier_h=25):
    """贝叶经塔：一层石架一摞叶，一根金线从底穿到顶。"""
    o = []
    top_y = base_y - (tiers - 1) * tier_h
    # 中柱，先画，压在叶摞底下
    o.append(K.line(cx, base_y + 6, cx, top_y - 14, K.OCHRE, 3.4))
    for i in range(tiers):
        w = base_w * (1 - i * 0.042)
        y = base_y - i * tier_h
        # 石架：探出的檐，底下压一道影
        o.append(K.pth(f"M{cx - w / 2} {y - 8} L{cx + w / 2} {y - 8} "
                       f"L{cx + w / 2 - 7} {y + 5} L{cx - w / 2 + 7} {y + 5} Z",
                       fill="#98a29a", stroke=K.INK, w=1.3))
        o.append(K.line(cx - w / 2 + 9, y + 2.6, cx + w / 2 - 9, y + 2.6, "#59645c", 1.4, 0.6))
        if i == tiers - 1:
            # 塔顶只有一页：创世卷第一页
            o.append(K.glow(cx, y - 18, 62, "#f6c96b", 0.42))
            o.append(K.palm_leaf(cx, y - 14, w * 0.94, w * 0.285, angle=-15,
                                 fill="#faeecd", edge=K.OCHRE, lines=7))
            o.append(K.line(cx - w * 0.40, y - 10, cx + w * 0.40, y - 19,
                            "#b8892f", 1.3, 0.85))
            continue
        # 一摞贝叶
        bw, bh = w * 0.76, 16
        by = y - 8 - bh
        o.append(K.rect(cx - bw / 2, by, bw, bh, fill="#ecdcb4", stroke=K.OCHRE, sw=1.1))
        o.append(K.line(cx - bw / 2 + 2, by + 1.6, cx + bw / 2 - 2, by + 1.6, "#fbf3dc", 1.6, 0.8))
        for j in range(5):
            yy = by + 4.6 + j * 2.4
            o.append(K.line(cx - bw / 2 + 3, yy, cx + bw / 2 - 3, yy, K.OCHRE, 0.8, 0.4))
        # 两端探出来的叶尖
        for s in (-1, 1):
            o.append(K.pth(f"M{cx + s * (bw / 2 - 6)} {by + bh - 3} "
                           f"q{s * w * 0.11} {-bh * 0.62} {s * w * 0.19} {-bh * 0.34} "
                           f"q{-s * w * 0.09} {bh * 0.46} {-s * w * 0.19} {bh * 0.20} Z",
                           fill="#f2e3bd", stroke=K.OCHRE, w=1.0))
        # 金线穿过这一摞
        o.append(K.line(cx, by, cx, by + bh, "#f2c05c", 2.3, 0.95))
        o.append(K.circ(cx, by + bh / 2, 3.0, fill="#fdf0c8", stroke=K.GAMBOGE, sw=0.9))
    # 塔刹：相轮五重
    sp = top_y - 58
    for k in range(5):
        o.append(K.ell(cx, sp + k * 6.4, 9.5 - k * 1.35, 2.5,
                       fill=K.GOLD, stroke=K.INK, sw=0.7))
    o.append(K.circ(cx, sp - 9, 5.6, fill=K.GAMBOGE, stroke=K.INK, sw=1.1))
    return "".join(o)


def fig09():
    W, H = 720, 528
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#3d372f"/>')
    o.append(K.rect(0, 0, W, H, fill="url(#brick)", stroke=None, op=0.42))
    o.append(K.rect(0, 0, W, H, fill="#332d27", stroke=None, op=0.4))
    # 洞顶的钟乳
    for sx, sy, sw_, sh in ((96, -18, 62, 74), (208, -26, 44, 52), (544, -22, 58, 66),
                            (648, -14, 46, 44)):
        o.append(K.pth(f"M{sx - sw_ / 2} {sy} Q{sx - sw_ * 0.16} {sy + sh * 0.75} "
                       f"{sx + sw_ * 0.06} {sy + sh} Q{sx + sw_ * 0.34} {sy + sh * 0.56} "
                       f"{sx + sw_ / 2} {sy} Z", fill="#2a2520", stroke=None, op=0.85))
    # 地：石铺，向远处收
    o.append(K.rect(0, 344, W, H - 344, fill="#574e43", stroke=None, op=0.97))
    o.append(K.line(0, 344, W, 344, "#14110e", 2.0, 0.7))
    for k in range(-7, 15):
        x0 = 360 + k * 26
        x1 = 360 + k * 96
        o.append(K.line(x0, 344, x1, H, "#3b342c", 1.0, 0.45))
    for yy, op in ((386, 0.35), (436, 0.3), (494, 0.28)):
        o.append(K.line(0, yy, W, yy, "#3b342c", 1.0, op))
    # 青石盘：根印刻在上面，整块会转
    dcx, dcy, DRX, DRY = 440, 428, 196, 64
    o.append(K.ell(dcx, dcy + 7, DRX, DRY, fill="#4a544d", stroke=K.INK, sw=1.2, op=0.85))
    o.append(K.ell(dcx, dcy, DRX, DRY, fill="#6d7a72", stroke=K.INK, sw=2.0))
    o.append(K.ell(dcx, dcy, DRX - 11, (DRX - 11) * DRY / DRX,
                   fill="#76837b", stroke="#8d9a92", sw=1.1, op=0.9))
    # 64 个刻字：两圈
    import math as _m
    for ring_r, n, sz in ((DRX - 26, 32, 4.2), (DRX - 44, 32, 3.4)):
        for k in range(n):
            a = _m.radians(360.0 * k / n + (5 if ring_r < DRX - 30 else 0))
            px = dcx + ring_r * _m.cos(a)
            py = dcy + ring_r * DRY / DRX * _m.sin(a)
            o.append(K.rect(px - sz / 2, py - sz / 2 * DRY / DRX - 1, sz, sz * 0.9,
                            fill="#3f4a44", stroke=None, op=0.75))
    # 在转
    o.append(spin_arc(dcx, dcy, DRX + 12, (DRX + 12) * DRY / DRX, 24, 74, K.GAMBOGE, 2.2, 0.75))
    o.append(spin_arc(dcx, dcy, DRX + 12, (DRX + 12) * DRY / DRX, 196, 248, K.GAMBOGE, 2.2, 0.45))
    # 塔从盘心长出来
    o.append(leaf_pagoda(dcx, dcy, tiers=12, base_w=142, tier_h=25))
    # 槽与鱼符
    o.append(K.rect(242, dcy + 6, 40, 16, fill="#1d2529", stroke=K.INK, sw=1.6))
    o.append(K.rect(242, dcy + 6, 40, 3.0, fill="#0f1416", stroke=None, op=0.85))
    o.append(K.fish_half(258, dcy + 14, 1.15, side=-1, fill=K.GOLD, holes=3))
    # 金线：从槽里起，穿过 14 层，到塔顶那一片
    o.append(K.pth(f"M{dcx} {dcy + 14} L{dcx} {dcy - 11 * 25 - 30}",
                   stroke="#f2c05c", w=2.4, op=0.9))
    o.append(K.pth(f"M278 {dcy + 14} L{dcx} {dcy + 14}",
                   stroke="#f2c05c", w=2.0, op=0.55, dash="5 4"))
    # 14 枚印：一枚一枚亮起来
    for i in range(14):
        f = i / 13.0
        px = dcx - 68 - f * 116
        py = dcy + 14 + f * 2.0
        o.append(K.glow(px, py, 9, "#f6c96b", 0.6))
        o.append(K.rect(px - 2.8, py - 2.8, 5.6, 5.6, fill="#fdf0c8", stroke=K.OCHRE, sw=0.8))
    # 纸：从盘边一道缝里滑出来，摊在地上
    o.append(K.pth(f"M{dcx + 168} {dcy + 24} L{dcx + 262} {dcy + 62} "
                   f"L{dcx + 258} {dcy + 84} L{dcx + 160} {dcy + 44} Z",
                   fill="#fbf6ea", stroke=K.OCHRE, w=1.1))
    for i in range(3):
        x0 = dcx + 180 + i * 22
        y0 = dcy + 38 + i * 8.6
        o.append(K.line(x0, y0, x0 + 16, y0 + 6.4, K.INK, 1.3, 0.45))
    o.append(K.pth(f"M{dcx + 262} {dcy + 62} q14 8 10 22 q-4 12 -16 8",
                   fill="none", stroke=K.OCHRE, w=1.1))
    o.append(K.pth(f"M{dcx + 258} {dcy + 84} q12 2 14 -12",
                   fill="#fbf6ea", stroke=K.OCHRE, w=1.0))
    # 沈拾遗：跪在青石前
    o.append(K.kneel(190, 508, 176, robe=K.AZURITE, hat="jin",
                     facing=1, arms=(-0.14, -0.31)))
    o.append(K.arm(190 + 0.10 * 176, 508 - 0.632 * 176, 232, dcy + 18, 9.5, 11.5, K.AZURITE))
    o.append(K.hand(238, dcy + 15, 0.95, ang=-18))
    # 一盏灯，压在地上
    o.append(K.glow(96, 490, 58, "#f2c05c", 0.38))
    o.append(K.pth("M84 494 l24 0 l-4 11 l-16 0 Z", fill="#8c5a3c", stroke=K.INK, w=1.2))
    o.append(K.flame(96, 490, 1.05, sway=-3))
    o.append(K.ell(96, 505, 19, 4.6, fill="none", stroke=K.INK, sw=1.2, op=0.55))
    return K.canvas(W, H, "".join(o), base="#3d372f", grain=0.16)


# ---------------------------------------------------------------- 10 照妖镜门
def fig10():
    W, H = 720, 500
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#efe2c6"/>')
    o.append(K.rect(0, 0, W, 420, fill="url(#brick)", stroke=None, op=0.4))
    o.append(K.pagoda_roof(360, 62, 700, 46))
    o.append(K.dougong(120, 62, 480))
    o.append(K.rect(96, 82, 528, 26, fill=K.DARK, stroke=K.INK, sw=1.4))
    o.append(K.rect(112, 88, 496, 14, fill="none", stroke=K.GOLD, sw=1.0, op=0.7))
    for px in (120, 582):
        o.append(K.pillar(px, 448, 20, 366))
    o.append(K.rect(0, 440, W, H - 440, fill="#d8c9a6", stroke=None, op=0.9))
    # 镜
    o.append(K.circ(360, 264, 168, fill="#8d7a52", stroke=K.INK, sw=2.2))
    o.append(K.circ(360, 264, 156, fill="#3a3228", stroke=K.GOLD, sw=2.6))
    o.append(K.circ(360, 264, 146, fill="#241f1c", stroke=None))
    for i in range(12):
        a = math.radians(30 * i)
        o.append(K.circ(360 + math.cos(a) * 151, 264 + math.sin(a) * 151, 3.2,
                        fill=K.GOLD, stroke=None, op=0.8))
    o.append(K.glow(360, 264, 120, "#f2c05c", 0.30))
    o.append(K.txt(360, 318, "是", 128, "#f2c05c", K.FK, ls=0))
    # 门后的人影：一层层退下去
    for i, (bx, hh, op) in enumerate(((44, 176, 0.55), (86, 158, 0.45), (128, 140, 0.38),
                                      (176, 124, 0.30), (600, 124, 0.30), (648, 140, 0.38),
                                      (690, 158, 0.45))):
        o.append(K.g(K.person(bx, 452, hh, robe="#6b6155", hat="none", hands=False), op=op))
    # 门前举符的人
    o.append(K.person(206, 468, 200, robe=K.CINNABAR, hat="futou",
                      l_arm=(-0.30, -0.44), r_arm=(0.52, -0.66), face=True))
    o.append(K.fish_half(206 + 0.52 * 200, 468 - 0.66 * 200, 0.62, side=1, fill=K.GAMBOGE, holes=0))
    return K.canvas(W, H, "".join(o), base="#efe2c6")


# ---------------------------------------------------------------- 11 三钥
def fig11():
    W, H = 720, 452
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#efe2c6"/>')
    o.append(K.rect(0, 0, W, 380, fill="url(#brick)", stroke=None, op=0.4))
    o.append(K.rect(0, 384, W, H - 384, fill="#dccfae", stroke=None, op=0.85))
    # 金匮
    o.append(K.chest(196, 342, 344, 190, body="#c9a24a", edge=K.OCHRE, locks=3))
    o.append(K.rect(196 + 40, 342 - 190 + 18, 344 - 80, 22, fill="none", stroke=K.GOLD, sw=1.0, op=0.6))
    # 三个形状不同的锁孔
    holes = [(270, 246, "fish"), (368, 246, "gear"), (466, 246, "gui")]
    for hx, hy, kind in holes:
        o.append(K.rect(hx - 21, hy - 26, 42, 52, rx=5, fill=K.STEEL, stroke=K.INK, sw=1.6))
        if kind == "fish":
            o.append(K.fish_half(hx - 13, hy, 0.42, side=1, fill="#15100e", edge=K.GOLD, holes=0))
        elif kind == "gear":
            o.append(K.circ(hx, hy, 11, fill="#15100e", stroke=K.GOLD, sw=1.2))
            for i in range(6):
                a = math.radians(60 * i)
                o.append(K.circ(hx + math.cos(a) * 13, hy + math.sin(a) * 13, 2.6, fill="#15100e", stroke=None))
        else:
            o.append(K.jade_tablet(hx, hy + 17, 19, 34, fill="#15100e", edge=K.GOLD))
        o.append(K.circ(hx, hy + 34, 2.6, fill=K.GOLD, stroke=None))
    # 漆盘
    o.append(K.pth("M118 356 L602 356 L576 430 L144 430 Z", fill="#2b2320", stroke=K.INK, w=1.8))
    o.append(K.pth("M134 364 L586 364 L564 420 L156 420 Z", fill="#3a322b", stroke=K.GOLD, w=1.0, op=0.6))
    for i in range(5):
        o.append(K.line(164 + i * 96, 368, 172 + i * 92, 418, K.GOLD, 0.8, 0.18))
    # 三钥
    o.append(K.fish_half(238, 392, 1.15, side=1, fill=K.GAMBOGE, edge=K.OCHRE))
    o.append(K.mech_key(388, 390, 1.15, angle=0))
    o.append('<g transform="translate(516,394) rotate(-7) scale(1.0,0.46)">'
             + K.jade_tablet(0, 0, 34, 62) + "</g>")
    # 一只手
    o.append(K.hand(572, 396, 1.05, ang=200, cuff=K.AZURITE))
    o.append(K.arm(700, 352, 584, 392, 30.0, 15.0, K.AZURITE))
    return K.canvas(W, H, "".join(o), base="#efe2c6")


# ---------------------------------------------------------------- 12 金匮火
def wine_pot(x, y, s=1.0, ang=0):
    o = [f'<g transform="translate({x},{y}) rotate({ang}) scale({s})">']
    o.append(K.pth("M-26 -18 C-30 -44 -16 -58 0 -58 C16 -58 30 -44 26 -18 "
                   "C22 6 -22 6 -26 -18 Z", fill=K.GOLD, stroke=K.INK, w=1.6))
    o.append(K.rect(-9, -74, 18, 18, fill=K.GOLD, stroke=K.INK, sw=1.4))
    o.append(K.ell(0, -74, 16, 5, fill=K.GOLD, stroke=K.INK, sw=1.3))
    o.append(K.pth("M-26 -34 C-44 -40 -46 -18 -30 -16", stroke=K.INK, w=2.6))
    o.append(K.ell(0, -2, 22, 7, fill="#a8862e", stroke=K.INK, sw=1.4))
    for i in range(4):
        o.append(K.line(-14 + i * 9, -2, -14 + i * 9, 3, "#f2c05c", 1.2, 0.7))
    o.append("</g>")
    return "".join(o)


def fig12():
    W, H = 720, 470
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#2b2320"/>')
    o.append(K.rect(0, 0, W, 440, fill="url(#brick)", stroke=None, op=0.45))
    o.append(K.glow(360, 386, 310, "#e07a2c", 0.5))
    # 后面的火
    o.append(fireband(160, 560, 456, 148, n=10, w=62, fill="#8f2a22", inner="#c25a22", op=0.92))
    # 柴堆
    for i in range(7):
        o.append(K.line(196 + i * 44, 450, 232 + i * 40, 426, "#5c3a22", 7.0))
    # 金匮
    o.append(K.glow(366, 372, 176, "#f2a63c", 0.6))
    o.append(K.chest(272, 428, 200, 132, body="#c07a36", edge="#f2c05c", locks=2))
    o.append(K.rect(292, 318, 160, 10, fill="#f2c05c", stroke=None, op=0.65))
    # 前面的火舌压在匮上
    o.append(fireband(256, 492, 458, 132, n=9, w=58))
    o.append(fireband(300, 442, 458, 92, n=6, w=44, fill="#d9611f", inner="#fadc8e"))
    # 灰里的酒壶：壶底朝天，64 字正在熔
    o.append(wine_pot(214, 452, 1.05, ang=196))
    for i in range(8):
        o.append(K.circ(214 + ((i * 37) % 60) - 30, 424 + ((i * 23) % 24), 2.6 - i * 0.12,
                        fill="#f2c05c", stroke=None, op=0.7))
    o.append(K.debris(160, 400, 130, 56, n=26, color="#f2c05c", r=2.6, op=0.5, seed=3))
    # 醉山：刚把壶扔进去
    o.append(K.person(112, 452, 216, robe=K.DARK, hat="futou",
                      l_arm=(-0.26, -0.44), r_arm=(0.46, -0.62), face=True, beard=True))
    # 顾振铎：戴镣铐
    o.append(K.person(596, 452, 216, robe="#5b5347", hat="jin",
                      l_arm=(-0.26, -0.44), r_arm=(0.28, -0.42), face=True, beard=True))
    CH = "#b9c4c9"
    o.append(K.pth("M556 392 C582 402 612 402 636 392", stroke=CH, w=4.6))
    o.append(K.pth("M556 392 C582 402 612 402 636 392", stroke="#5d6a70", w=1.2, dash="3 5"))
    for lx in (568, 594, 622):
        o.append(K.circ(lx, 397 + (lx - 594) * 0.02, 8.0, stroke=CH, sw=3.0))
    o.append(K.pth("M596 400 C596 414 594 426 592 436", stroke=CH, w=3.8))
    for ly in (410, 422):
        o.append(K.circ(595, ly, 6.4, stroke=CH, sw=2.6))
    # 烟与火星
    o.append(K.smoke(360, 300, 260, 22, 3, "#8a7c66", 0.28))
    o.append(K.dots(120, 60, 480, 300, n=60, color="#f2a63c", r=1.8, op=0.5, seed=9))
    return K.canvas(W, H, "".join(o), base="#2b2320", grain=0.12)


def fig13():
    """印路：8 笔账的定魂印结成树，验一笔 3 步到根；右边虚一笔演示添账换根。"""
    W, H = 720, 528
    CX = 360
    lx = [CX + (i - 3.5) * 68 for i in range(8)]
    leaf_top, leaf_h, leaf_w = 402, 74, 36
    t1x = [(lx[i] + lx[i + 1]) / 2 for i in (0, 2, 4, 6)]
    t2x = [(t1x[0] + t1x[1]) / 2, (t1x[2] + t1x[3]) / 2]
    t1_y, t1_s = 330, 30
    t2_y, t2_s = 232, 34
    rt_y, rt_s = 120, 64
    pick = 2
    KNOB = 0.28
    GHOST = "#8a7a63"

    def geom(cx, cy, s):
        return dict(cx=cx, cy=cy, s=s, top=cy - s / 2,
                    apex=cy - s / 2 - 0.30 * s, l=cx - KNOB * s, r=cx + KNOB * s)

    root = geom(CX, rt_y, rt_s)
    t2 = [geom(x, t2_y, t2_s) for x in t2x]
    t1 = [geom(x, t1_y, t1_s) for x in t1x]
    leaves = [dict(cx=x, top=leaf_top) for x in lx]

    links = [
        (root, t2[0]), (root, t2[1]),
        (t2[0], t1[0]), (t2[0], t1[1]), (t2[1], t1[2]), (t2[1], t1[3]),
        (t1[0], leaves[0]), (t1[0], leaves[1]),
        (t1[1], leaves[2]), (t1[1], leaves[3]),
        (t1[2], leaves[4]), (t1[2], leaves[5]),
        (t1[3], leaves[6]), (t1[3], leaves[7]),
    ]
    hot = {(id(root), id(t2[0])), (id(t2[0]), id(t1[1])), (id(t1[1]), id(leaves[pick]))}

    def ay_of(node):
        return node["apex"] if "apex" in node else leaf_top - 2.5

    def cord(x1, y1, x2, y2, on=False, ghost=False):
        if ghost:
            return K.line(x1, y1, x2, y2, GHOST, 1.4, 0.8, dash="4 5")
        if on:
            return (K.line(x1, y1, x2, y2, "#eecb84", 8.0, 0.30) +
                    K.line(x1, y1, x2, y2, K.GOLD, 2.8, 0.95))
        return K.line(x1, y1, x2, y2, "#8a6238", 1.65, 0.95)

    o = []
    o.append(cord(CX, -2, CX, root["apex"]))

    for a, b in links:
        if (id(a), id(b)) in hot:
            continue
        o.append(cord(a["l"] if b["cx"] < a["cx"] else a["r"], a["top"], b["cx"], ay_of(b)))
    for a, b in links:
        if (id(a), id(b)) not in hot:
            continue
        o.append(cord(a["l"] if b["cx"] < a["cx"] else a["r"], a["top"], b["cx"], ay_of(b), True))

    def seal_node(g, on, seed):
        x, y, s = g["cx"] - g["s"] / 2, g["cy"] - g["s"] / 2, g["s"]
        out = []
        if on:
            out.append(f'<ellipse cx="{g["cx"]}" cy="{g["cy"]}" rx="{s * 0.92:.1f}" '
                       f'ry="{s * 0.92:.1f}" fill="url(#glow)" opacity="0.6"/>')
            out.append(K.rect(x - 3.6, y - 3.6, s + 7.2, s + 7.2, fill="none",
                              stroke="#c9a05a", sw=1.0, op=0.65))
        out.append(K.seal_face(x, y, s, cells=3 if s < 40 else 5, fill=K.CINNABAR, seed=seed))
        h = 0.30 * s
        bw, tw = KNOB * s, 0.17 * s
        out.append(K.pth(f"M{g['cx'] - bw} {y} C{g['cx'] - bw * 0.86} {y - h * 0.38} "
                         f"{g['cx'] - tw * 1.12} {y - h * 0.64} {g['cx'] - tw} {y - h} "
                         f"L{g['cx'] + tw} {y - h} C{g['cx'] + tw * 1.12} {y - h * 0.64} "
                         f"{g['cx'] + bw * 0.86} {y - h * 0.38} {g['cx'] + bw} {y} Z",
                         fill="#c8a05e" if on else "#b08a63", stroke=K.INK, w=0.9))
        out.append(K.ell(g["cx"], y - h * 0.78, 2.0, 1.1, fill="#f8f3e7",
                         stroke=K.INK, sw=0.45, op=0.75))
        return "".join(out)

    for i, g in enumerate(t1):
        o.append(seal_node(g, i == 1, 21 + i))
    for i, g in enumerate(t2):
        o.append(seal_node(g, i == 0, 31 + i))
    o.append(seal_node(root, True, 41))

    # 叶子：一枚定魂印压在一张账条上
    for i, lf in enumerate(leaves):
        on = i == pick
        x = lf["cx"] - leaf_w / 2
        if on:
            o.append(f'<ellipse cx="{lf["cx"]}" cy="{leaf_top + leaf_h / 2}" rx="36" ry="56" '
                     f'fill="url(#glow)" opacity="0.45"/>')
        o.append(K.rect(x, leaf_top, leaf_w, leaf_h,
                        fill="#fffaf0" if on else "#faf0d8",
                        stroke=K.GOLD if on else "#a07c4e", sw=1.3 if on else 1.15, rx=1.2))
        o.append(K.seal_face(lf["cx"] - 10, leaf_top + 8, 20, cells=3, seed=7 + i))
        for j in range(3):
            ww = 18 - (j % 2) * 3
            o.append(K.line(lf["cx"] - ww / 2, leaf_top + 38 + j * 8,
                            lf["cx"] + ww / 2, leaf_top + 38 + j * 8,
                            "#a89070", 0.95, 0.5 if on else 0.4))
        o.append(K.circ(lf["cx"], leaf_top - 2.2, 2.4, fill=K.GOLD if on else "#bfa075",
                        stroke=None, op=1.0 if on else 0.7))

    # 右边虚一笔：后添的账，还没进树
    nx = 666
    x = nx - leaf_w / 2
    o.append(K.rect(x, leaf_top, leaf_w, leaf_h, fill="none", stroke=GHOST,
                    sw=1.25, op=0.85, rx=1.2))
    o.append(f'<rect x="{x + 4}" y="{leaf_top + 4}" width="{leaf_w - 8}" height="{leaf_h - 8}" '
             f'fill="none" stroke="{GHOST}" stroke-width="0.8" stroke-dasharray="3 4" opacity="0.55"/>')
    o.append(K.seal_face(nx - 10, leaf_top + 8, 20, cells=3, fill="#c2b094", op=0.75, seed=3))
    for j in range(3):
        ww = 16 - (j % 2) * 3
        o.append(K.line(nx - ww / 2, leaf_top + 38 + j * 8, nx + ww / 2,
                        leaf_top + 38 + j * 8, GHOST, 0.9, 0.5, dash="3 4"))
    o.append(K.circ(nx, leaf_top - 2.2, 2.4, fill="none", stroke=GHOST, sw=1.1, op=0.8))

    # 新根：一枚还没盖下的印
    gx, gy, gs = 620, 96, 44
    o.append(K.cord if False else "")
    o.append(cord(nx, leaf_top - 2.2, gx, gy + gs / 2, ghost=True))
    o.append(cord(root["cx"] + rt_s / 2 + 8, rt_y, gx - gs / 2 - 4, gy, ghost=True))
    o.append(f'<g transform="translate({gx - 40},{gy - 4}) rotate(-4)">'
             f'<path d="M0 0 L10 -3.4 L3.4 4 Z" fill="{GHOST}" opacity="0.9"/></g>')
    o.append(K.seal_face(gx - gs / 2, gy - gs / 2, gs, cells=4, fill="#c2b094", op=0.75, seed=9))
    o.append(f'<rect x="{gx - gs / 2 - 1}" y="{gy - gs / 2 - 1}" width="{gs + 2}" height="{gs + 2}" '
             f'fill="none" stroke="{GHOST}" stroke-width="1.1" stroke-dasharray="4 4" opacity="0.9"/>')

    steps = [
        ((leaves[pick]["cx"], leaf_top - 2.5), (t1[1]["l"], t1[1]["top"])),
        ((t1[1]["cx"], t1[1]["apex"]), (t2[0]["r"], t2[0]["top"])),
        ((t2[0]["cx"], t2[0]["apex"]), (root["l"], root["top"])),
    ]
    for i, (a, b) in enumerate(steps):
        px = a[0] + (b[0] - a[0]) * 0.42
        py = a[1] + (b[1] - a[1]) * 0.42
        o.append(K.circ(px, py, 10.2, fill="#f8f3e7", stroke=K.GOLD, sw=1.1))
        o.append(K.txt(px, py + 4.5, str(i + 1), 13.2, K.GOLD, font=K.FS, weight=600))

    ax = t2[0]["cx"] + (root["l"] - t2[0]["cx"]) * 0.5
    ay = t2[0]["apex"] + (root["top"] - t2[0]["apex"]) * 0.5
    import math as _m
    ang = _m.degrees(_m.atan2(root["top"] - t2[0]["apex"], root["l"] - t2[0]["cx"]))
    o.append(f'<g transform="translate({ax:.1f},{ay:.1f}) rotate({ang:.1f})">'
             f'<path d="M-5.8 -3.9 L3.5 0 L-5.8 3.9 Z" fill="{K.GOLD}"/></g>')

    # 标注
    o.append(K.txt(100, 424, "定魂印", 13.0, K.SOFT, font=K.FS, anchor="end", ls=1.2))
    o.append(K.line(102, 420, 110, 420, K.SOFT, 0.7, 0.45))
    o.append(K.txt(CX - 48, 71, "根印", 16.5, K.CINNABAR, font=K.FS, anchor="end", ls=2.2))
    o.append(K.txt(gx, 49, "新根印", 13.5, GHOST, font=K.FS, ls=1.5))
    o.append(K.txt(leaves[pick]["cx"], 504, "此页", 15.5, K.CINNABAR, font=K.FS, ls=2))
    o.append(K.txt(leaves[pick + 1]["cx"], 504, "兄弟页", 15.5, K.OCHRE, font=K.FS, ls=1))
    o.append(K.txt(nx, 504, "新页", 14, GHOST, font=K.FS, ls=1.5))
    return K.canvas(W, H, "".join(o), base="#f8f3e7", grain=0.42)


# ---------------------------------------------------------------- 14 钟面
def fig14():
    """模 23 之后的剑脊：y²=x³+7 的解只落在 23×23 格点上，上下两点成对。"""
    P, cell = 23, 18
    W, H = 720, 552
    gx, gy = 92, 92
    side = P * cell
    o = []

    def cx(x):
        return gx + (x + 0.5) * cell

    def cy(y):
        return gy + (P - 1 - y + 0.5) * cell

    sols = {(x, y) for x in range(P) for y in range(P) if (y * y - (x ** 3 + 7)) % P == 0}

    def lab(x, y, s, size, color, anchor="middle"):
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{K.FK}" font-size="{size}" '
                f'font-weight="600" fill="{color}" stroke="{K.WHITE}" stroke-width="3.2" '
                f'paint-order="stroke" text-anchor="{anchor}">{s}</text>')

    # 碑框与格线
    o.append(K.rect(gx - 14, gy - 14, side + 28, side + 28, fill="#faf4e6", stroke=K.INK, sw=1.7))
    for i in range(P + 1):
        o.append(K.line(gx + i * cell, gy, gx + i * cell, gy + side, "#8d8168", 0.7, 0.30))
        o.append(K.line(gx, gy + i * cell, gx + side, gy + i * cell, "#8d8168", 0.7, 0.30))

    # 不是解的格点：一点灰
    for x in range(P):
        for y in range(P):
            if (x, y) not in sols:
                o.append(K.circ(cx(x), cy(y), 0.9, fill=K.ASH, stroke=None, op=0.45))

    # 挑一对上下点，画一条金虚线
    pair = None
    for x in range(3, P):
        ys = sorted(y for (xx, y) in sols if xx == x)
        if len(ys) == 2 and ys[0] >= 3 and ys[1] <= P - 4:
            pair = (x, ys[0], ys[1])
            break
    if pair:
        x, y1, y2 = pair
        o.append(K.line(cx(x), cy(y1), cx(x), cy(y2), K.GOLD, 1.7, 0.9, dash="6 5"))
        o.append(K.circ(cx(x), cy(y1), 8.4, fill="none", stroke=K.GOLD, sw=1.1, op=0.55))
        o.append(K.circ(cx(x), cy(y2), 8.4, fill="none", stroke=K.GOLD, sw=1.1, op=0.55))

    # 解：朱点（先一圈白光，再点朱）
    for (x, y) in sorted(sols):
        o.append(K.circ(cx(x), cy(y), 7.8, fill=K.WHITE, stroke=None, op=0.92))
    for (x, y) in sorted(sols):
        o.append(K.circ(cx(x), cy(y), 5.0, fill=K.CINNABAR, stroke=K.WHITE, sw=1.2))

    # 刻度只标 0、5、10、15、20、22
    ticks = (0, 5, 10, 15, 20, 22)
    for x in ticks:
        o.append(K.txt(cx(x), gy + side + 26, str(x), 10, K.SOFT, font=K.FS))
    for y in ticks:
        o.append(K.txt(gx - 22, cy(y) + 3.4, str(y), 10, K.SOFT, font=K.FS, anchor="end"))

    # 方程：唯一的说明文字，其余交给图和图注
    o.append(K.txt(W - 16, 52, "y² = x³ + 7  （mod 23）", 16, K.GOLD, font=K.FK, anchor="end", ls=1))

    # 一面二十三刻的钟：走到 23 就回到 0
    dcx, dcy, dr = 610, 250, 58
    o.append(K.circ(dcx, dcy, dr, fill="#faf4e6", stroke=K.INK, sw=1.4))
    for k in range(P):
        a = math.radians(-90 + k * 360.0 / P)
        r0 = dr - (10.5 if k == 0 else 7.0)
        x1, y1 = dcx + r0 * math.cos(a), dcy + r0 * math.sin(a)
        x2, y2 = dcx + (dr - 1.5) * math.cos(a), dcy + (dr - 1.5) * math.sin(a)
        o.append(K.line(x1, y1, x2, y2, K.GOLD if k == 0 else K.OCHRE,
                        2.2 if k == 0 else 0.9, 0.95 if k == 0 else 0.55))
    o.append(K.txt(dcx, dcy - 36, "0", 12, K.SOFT, font=K.FS))
    # 走到 23 就回到 0：一段带箭头的虚弧
    rr = dr + 8
    a0 = math.radians(-90 - 360.0 / P)
    ax, ay = dcx + rr * math.cos(a0), dcy + rr * math.sin(a0)
    o.append(K.pth(f"M{ax:.1f} {ay:.1f} A{rr} {rr} 0 0 1 {dcx} {dcy - rr}",
                   stroke=K.GOLD, w=1.7, op=0.9, dash="6 5"))
    o.append(K.pth(f"M{dcx + 5} {dcy - rr} L{dcx - 4} {dcy - rr - 4.5} "
                   f"L{dcx - 4} {dcy - rr + 4.5} Z", fill=K.GOLD, stroke=None))

    # 落款
    o.append(K.rect(628, 468, 42, 42, fill=K.CINNABAR, stroke=None, op=0.85))
    o.append(K.rect(631, 471, 36, 36, fill="none", stroke=K.WHITE, sw=1.1, op=0.7))
    o.append(K.seal_script(649, 489, 36))
    return K.canvas(W, H, "".join(o), base="#f8f3e7", grain=0.42)


# ---------------------------------------------------------------- 15 单页验法
def fig15():
    """两页账对画：左页页眉空着，右页页眉吞着旧印。绿线是单页自验，红虚线是全账验法，接不上。"""
    cw, ch = 228, 330
    top = 68
    bh = 34                      # 页眉页脚带高
    hb = top + 10                # 页眉带
    fy = top + ch - 50           # 页脚带
    hc, fc = hb + bh / 2, fy + bh / 2
    s = 27                       # 印面边长
    pad = 22                     # 印面距版框内侧
    lx, rx = 44, 376
    gap_c = (lx + cw + rx) / 2   # 两页之间的中缝
    gr = rx + cw + 26            # 右页外侧绿线
    W, H = int(gr + 34), top + ch + 24
    o = []

    def head(px, py, ang_deg, color, L=14.0, Wd=9.0):
        a = math.radians(ang_deg)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        tx, ty = px + ux * L / 2, py + uy * L / 2
        bx, by = px - ux * L / 2, py - uy * L / 2
        return K.pth(f"M{tx:.1f} {ty:.1f} L{bx + nx * Wd / 2:.1f} {by + ny * Wd / 2:.1f} "
                     f"L{bx - nx * Wd / 2:.1f} {by - ny * Wd / 2:.1f} Z", fill=color, stroke=None)

    def badge(px, py, ok, r=13.5):
        col = K.MALACH if ok else K.CINNABAR
        out = [K.circ(px, py, r, fill=K.WHITE, stroke=col, sw=2.4)]
        if ok:
            out.append(K.pth(f"M{px - r * 0.46:.1f} {py + r * 0.02:.1f} "
                             f"L{px - r * 0.12:.1f} {py + r * 0.40:.1f} "
                             f"L{px + r * 0.50:.1f} {py - r * 0.42:.1f}", stroke=col, w=2.8))
        else:
            out.append(K.line(px - r * 0.40, py - r * 0.40, px + r * 0.40, py + r * 0.40, col, 2.8))
            out.append(K.line(px + r * 0.40, py - r * 0.40, px - r * 0.40, py + r * 0.40, col, 2.8))
        return "".join(out)

    def card(x, empty_head=False, changed=False, seed=7):
        bl, br = x + 10, x + cw - 10          # 页眉页脚带的左右边
        out = [K.rect(x, top, cw, ch, fill="#fffaf0", stroke=K.INK, sw=1.9, rx=2)]
        out.append(K.rect(x + 4.5, top + 4.5, cw - 9, ch - 9, fill="none", stroke="#a07c4e",
                          sw=0.9, op=0.45, rx=1))
        # 页眉：前页之印
        out.append(K.rect(bl, hb, br - bl, bh, fill="#f6ecd6", stroke="#a07c4e", sw=1.3))
        if empty_head:
            out.append(K.rect(x + pad, hb + (bh - s) / 2, s, s, fill="#fdf8ec", stroke=K.OCHRE,
                              sw=1.1, op=0.55, rx=0.5))
        else:
            out.append(K.seal_face(x + pad, hb + (bh - s) / 2, s, cells=4, fill="#b06a5a",
                                   op=0.9, broken=0.18, seed=11))
        # 页脚：本页之印
        out.append(K.rect(bl, fy, br - bl, bh, fill="#f6ecd6", stroke="#a07c4e", sw=1.3))
        out.append(K.seal_face(x + cw - pad - s, fy + (bh - s) / 2, s, cells=3,
                               fill=K.CINNABAR, op=1.0, seed=seed))
        # 本页文字
        for j in range(11):
            yy = 122 + j * 20
            ww = cw - 36 - (j % 2) * 14
            if changed and j == 4:
                out.append(K.rect(x + 14, yy - 11, cw - 28, 21, fill=K.CINNABAR, stroke=None, op=0.10))
                out.append(K.pth(f"M{x + 20} {yy} C{x + 24 + ww * 0.28} {yy - 2.2} "
                                 f"{x + 26 + ww * 0.62} {yy + 1.9} {x + 18 + ww} {yy - 1.1}",
                                 stroke=K.CINNABAR, w=2.8, op=0.95))
            else:
                out.append(K.line(x + 20, yy, x + 20 + ww, yy, "#9a7f5c", 1.7, 0.72))
        return "".join(out)

    o.append(card(lx, empty_head=True, changed=True, seed=7))
    o.append(card(rx, seed=13))
    # 页次签：骑在版框上沿的一小方签条
    for x, num in ((lx, "第一"), (rx, "第二")):
        tx, ty = x + cw / 2 - 24, top - 17
        o.append(K.rect(tx, ty, 48, 25, fill="#f8f3e7", stroke=K.INK, sw=1.6))
        o.append(K.txt(tx + 24, ty + 18.5, num, 15, K.INK, font=K.FK, ls=1.5))

    # 红线：拿左页新算的印，去对右页页眉那枚旧数。走到半路就接不上。
    out_x = lx + cw - pad + 4          # 左页页脚印的右缘
    in_x = rx + pad - 8                # 右页页眉印的左缘
    o.append(K.pth(f"M{out_x} {fc} L{gap_c - 7} {fc} Q{gap_c} {fc} {gap_c} {fc - 7} "
                   f"L{gap_c} {hc + 7} Q{gap_c} {hc} {gap_c + 7} {hc} L{in_x - 6} {hc}",
                   stroke=K.CINNABAR, w=2.6, op=0.95, dash="10 7"))
    o.append(head(in_x - 1, hc, 0, K.CINNABAR))
    o.append(badge(gap_c, (hc + fc) / 2, False))

    # 绿线：右页页眉的旧数加本页文字，一路算到页脚，对得上。
    in_f = rx + cw - pad             # 右页页脚印的右缘
    o.append(K.pth(f"M{rx + cw - 10} {hc} L{gr - 7} {hc} Q{gr} {hc} {gr} {hc + 7} "
                   f"L{gr} {fc - 7} Q{gr} {fc} {gr - 7} {fc} L{in_f + 12} {fc}",
                   stroke=K.MALACH, w=2.4, op=0.95))
    o.append(head(in_f + 8, fc, 180, K.MALACH))
    o.append(badge(gr, (hc + fc) / 2, True))
    return K.canvas(W, H, "".join(o), base="#f8f3e7", grain=0.42)


# ---------------------------------------------------------------- 16 墨三的图
def fig16():
    """墨三画在废账纸上的图：左为账簿家族树，右为天枢阁组织图。"""
    W, H = 1120, 680
    o = []

    def panel(x, y, w, h):
        return (K.rect(x + 5, y + 6, w, h, fill="#e8d8b6", stroke=None, op=0.32, rx=3)
                + K.rect(x, y, w, h, fill="#fbf5e7", stroke="#b9a47c", sw=1.1, op=0.95, rx=3)
                + K.rect(x + 6, y + 6, w - 12, h - 12, fill="none", stroke="#dccbaa",
                         sw=0.6, op=0.55, rx=2))

    def head(x, y, s, rule_w):
        out = [K.rect(x, y - 34, 6, 38, fill=K.CINNABAR, stroke=None, op=0.92)]
        out.append(K.txt(x + 20, y, s, 42, K.INK, font=K.FK, anchor="start", ls=4,
                         weight="600"))
        out.append(K.line(x, y + 18, x + rule_w, y + 18, K.GOLD, 1.0, 0.4))
        return "".join(out)

    def arrow(x, y0, y1, col=K.GOLD, w=2.0):
        out = [K.line(x, y0, x, y1 - 9, col, w, 0.9)]
        out.append(K.pth(f"M{x} {y1} L{x - 7} {y1 - 12} L{x + 7} {y1 - 12} Z",
                         fill=col, stroke=None, op=0.92))
        return "".join(out)

    def ledger(x, y, w, h, title, sub, count, accent, ts=30):
        out = [K.rect(x + 5, y + 6, w, h, fill="#e8d8b6", stroke=None, op=0.35, rx=2)]
        out.append(K.rect(x, y, w, h, fill="#fffaf0", stroke=K.INK, sw=1.7, rx=2))
        out.append(K.rect(x + 5, y + 5, w - 10, h - 10, fill="none", stroke="#c9b48d",
                          sw=0.65, op=0.55, rx=1))
        out.append(K.rect(x, y + 4, 6, h - 8, fill=accent, stroke=None, op=0.92))
        out.append(K.txt(x + 28, y + h * 0.47, title, ts, K.INK, font=K.FK,
                         anchor="start", ls=1.2, weight="600"))
        if sub:
            out.append(K.txt(x + 28, y + h * 0.78, sub, 18, K.SOFT, font=K.FS,
                             anchor="start", ls=0.3, op=0.95))
        if count:
            out.append(K.txt(x + w - 24, y + h * 0.47, count, 24, accent, font=K.FS,
                             anchor="end", ls=0.6, weight="600"))
        return "".join(out)

    def tag(x, y, w, h, name, note, accent):
        return (K.rect(x + 4, y + 5, w, h, fill="#e8d8b6", stroke=None, op=0.32, rx=2)
                + K.rect(x, y, w, h, fill="#fdf8ec", stroke="#c9b48d", sw=0.9, op=0.9, rx=2)
                + K.rect(x, y + 4, 5, h - 8, fill=accent, stroke=None, op=0.85)
                + K.txt(x + 20, y + 32, name, 24, K.INK, font=K.FK, anchor="start",
                        ls=1.2, weight="600")
                + K.txt(x + 20, y + 58, note, 17, K.SOFT, font=K.FS, anchor="start",
                        ls=0.3, op=0.92))

    def office(x, y, w, h, name):
        return (K.rect(x + 4, y + 4, w, h, fill="#e8d8b6", stroke=None, op=0.3, rx=2)
                + K.rect(x, y, w, h, fill="#fdf8ec", stroke="#a07c4e", sw=1.05, rx=2)
                + K.txt(x + w / 2, y + h * 0.58, name, 23, K.INK, font=K.FK,
                        ls=0.6, weight="600"))

    # 两栏底板
    o.append(panel(18, 18, 680, 644))
    o.append(panel(716, 18, 386, 644))
    o.append(head(46, 76, "账", 624))
    o.append(head(744, 76, "阁", 330))

    # 左：账簿家族树
    o.append(ledger(208, 112, 300, 76, "祖本", "金匮 · 所有账的源头", "1",
                    K.CINNABAR, ts=30))
    o.append(arrow(358, 188, 214))
    o.append(K.txt(372, 206, "抄", 18, K.OCHRE, font=K.FK, anchor="start", op=0.95))
    o.append(ledger(173, 214, 370, 80, "母本", "藏经阁 · 祖本的第一部抄本", "1",
                    K.OCHRE, ts=30))
    o.append(arrow(358, 294, 322))
    o.append(K.txt(372, 314, "分抄", 18, K.OCHRE, font=K.FK, anchor="start", op=0.95))
    o.append(ledger(123, 322, 470, 84, "108 宗门总账", "一宗一本，共 108 本", "108",
                    K.MALACH, ts=30))
    o.append(arrow(358, 406, 436))
    o.append(K.txt(372, 428, "再抄", 18, K.OCHRE, font=K.FK, anchor="start", op=0.95))
    o.append(ledger(78, 436, 560, 88, "10000 抄本", "万份制度，分藏 108 宗", "10000",
                    K.AZURITE, ts=32))

    # 左：三种本子
    o.append(tag(46, 552, 196, 76, "私册", "个人自留", K.CINNABAR))
    o.append(tag(260, 552, 196, 76, "公册", "账房登记", K.OCHRE))
    o.append(tag(474, 552, 196, 76, "官本", "誊清存档", K.AZURITE))

    # 右：组织图
    o.append(ledger(784, 108, 250, 76, "阁主", "", "", K.CINNABAR, ts=32))
    o.append(arrow(909, 184, 212))
    o.append(ledger(759, 212, 300, 84, "36 家上院", "议事 · 投票 · 定规矩", "",
                    K.OCHRE, ts=28))
    o.append(arrow(909, 296, 324))
    o.append(ledger(759, 324, 300, 88, "108 宗门", "持总账 · 出抄手", "",
                    K.MALACH, ts=28))

    # 四房：从阁主右侧单独引一条线，表示直属
    o.append(K.line(1034, 146, 1088, 146, K.GOLD, 1.6, 0.88))
    o.append(K.line(1088, 146, 1088, 524, K.GOLD, 1.6, 0.88))
    o.append(K.txt(909, 508, "四房", 28, K.CINNABAR, font=K.FK, ls=2.4, weight="600"))
    o.append(K.line(733, 524, 1088, 524, K.GOLD, 1.8, 0.9))
    o.append(K.circ(1088, 524, 4.2, fill=K.GOLD, stroke=None, op=0.9))
    for i, name in enumerate(("执法堂", "印房", "抄算房", "藏经阁")):
        cx = 774 + i * 90
        o.append(K.line(cx, 524, cx, 540, K.GOLD, 1.4, 0.8))
        o.append(office(cx - 42, 540, 84, 88, name))

    # 右上小印
    o.append(K.rect(1050, 38, 36, 36, fill=K.CINNABAR, stroke=None, op=0.82))
    o.append(K.rect(1053, 41, 30, 30, fill="none", stroke=K.WHITE, sw=0.9, op=0.65))
    o.append(K.txt(1068, 64, "枢", 21, K.WHITE, font=K.FK, ls=0.5))

    return K.canvas(W, H, "".join(o), base="#f8f3e7", grain=0.38)

NAMES = {
    "fig00": "fig00_wanjuan", "fig01": "fig01_yinlian", "fig02": "fig02_xuebeng",
    "fig03": "fig03_jianfeng", "fig04": "fig04_kaishan", "fig05": "fig05_fuji",
    "fig06": "fig06_sanqi", "fig07": "fig07_zhuanlun", "fig08": "fig08_zhenfa",
    "fig09": "fig09_merkle", "fig10": "fig10_zhaoyao", "fig11": "fig11_sanyao",
    "fig12": "fig12_jingui", "fig13": "fig13_yinlu", "fig14": "fig14_zhongmian",
    "fig15": "fig15_danye", "fig16": "fig16_nav",
}

if __name__ == "__main__":
    import pathlib
    import sys
    OUT = pathlib.Path(__file__).resolve().parent.parent / "img"
    for name in (sys.argv[1:] or [f"fig{i:02d}" for i in range(13)]):
        (OUT / f"{NAMES.get(name, name)}.svg").write_text(globals()[name](), encoding="utf-8")
        print(NAMES.get(name, name))
