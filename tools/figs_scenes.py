#!/usr/bin/env python3
"""《天枢账簿》十三张场景图。"""
import math

from svgkit import (
    PAPER, INK, CINNABAR, AZURITE, MALACHITE, GAMBOGE, OCHRE, WHITE, GOLD,
    STEEL, DARK, FONT, KAI, svg, cloud, mountain, pine, roof, dougong, lattice,
    railing, armillary, pagoda, palm_leaf, flame, seal, ring, tassel, seal_script,
    jade_seal, chain_run, gear, waterwheel, robe_figure, fish_half, turtle,
)


# ---------------- 图 0：万卷楼 ----------------
def fig00():
    b = []
    b.append(mountain(-60, 560, 360, 220, AZURITE, 0.28))
    b.append(mountain(300, 560, 480, 260, AZURITE, 0.2))
    b.append(mountain(20, 590, 760, 170, MALACHITE, 0.18))
    for x, y, s, o in [(30, 180, 0.8, 0.8), (560, 140, 0.7, 0.65), (90, 470, 0.6, 0.6), (600, 440, 0.55, 0.55)]:
        b.append(cloud(x, y, s, WHITE, GOLD, o))
    b.append(pine(80, 610, 1.0))
    b.append(pine(650, 600, 0.9))
    b.append(pagoda(360, 590, tiers=9, base_w=300, tier_h=45))
    for x, y, s in [(120, 230, 1.0), (590, 250, 0.8), (540, 340, 0.6)]:
        b.append(f'''<g transform="translate({x},{y}) scale({s})">
<path d="M0 0 C-8 -7 -20 -14 -30 -12 L-12 2 L-20 10 L0 6 L20 10 L12 2 L30 -12 C20 -14 8 -7 0 0 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.2"/>
<path d="M0 0 L0 12" stroke="{INK}" stroke-width="1"/>
<circle cx="0" cy="0" r="3" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.6"/>
</g>''')
    b.append(f'<path d="M80 610 L640 610 L660 638 L60 638 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<path d="M100 610 L620 610" stroke="{GOLD}" stroke-width="1"/>')
    b.append(f'<rect x="210" y="594" width="230" height="18" fill="{WHITE}" stroke="{OCHRE}" stroke-width="1.2"/>')
    b.append(f'<path d="M230 603 Q320 590 420 603" stroke="{INK}" stroke-width="0.8" fill="none" opacity="0.5"/>')
    b.append(seal(470, 592, 20, CINNABAR, "", knob=False, angle=6))
    b.append(f'<path d="M500 600 L560 600" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    b.append(f'<path d="M560 600 L574 594 L574 606 Z" fill="{INK}"/>')
    return svg(720, 660, "".join(b))


# ---------------- 图 1：印链 ----------------
def fig01():
    b = []
    b.append(f'<rect x="40" y="40" width="640" height="390" fill="#2a2420" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<rect x="56" y="56" width="608" height="358" fill="url(#hui)" opacity="0.26"/>')
    # 屏心的一轮暗月，衬托玉色
    b.append(f'<circle cx="360" cy="230" r="175" fill="none" stroke="{GOLD}" stroke-width="0.8" opacity="0.35"/>')
    b.append(f'<path d="M56 414 L664 414" stroke="{GOLD}" stroke-width="1"/>')
    # 铜盘
    b.append(f'<ellipse cx="360" cy="452" rx="262" ry="26" fill="#cdbb9b" stroke="{OCHRE}" stroke-width="1.8"/>')
    b.append(f'<ellipse cx="360" cy="449" rx="238" ry="18" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.7"/>')
    # 金链
    pts = [(58, 150), (180, 185), (360, 185), (540, 185), (662, 150)]
    b.append(chain_run(pts, step=16))
    # 三枚玉玺
    b.append(jade_seal(180, 300, 100, "#7fa58c", cracked=False, tassel_on=True, angle=-4))
    b.append(jade_seal(360, 300, 112, "#93b39c", cracked=True, tassel_on=True, angle=2))
    b.append(jade_seal(540, 300, 100, "#7fa58c", cracked=False, tassel_on=True, angle=5))
    # 链与钮环的短接
    for cx, yy in [(180, 186), (360, 184), (540, 186)]:
        b.append(f'<path d="M{cx} {yy} L{cx} {yy+10}" stroke="{GOLD}" stroke-width="2.6"/>')
    # 落印的朱砂痕
    b.append(f'<path d="M150 438 C214 446 258 432 316 442" stroke="{CINNABAR}" stroke-width="2.4" fill="none" opacity="0.45"/>')
    return svg(720, 490, "".join(b))


# ---------------- 图 2：雪崩 ----------------
def fig02():
    b = []
    b.append(cloud(40, 58, 0.6, WHITE, GOLD, 0.55))
    b.append(cloud(568, 52, 0.52, WHITE, GOLD, 0.5))
    for ly in (160, 342):
        b.append(palm_leaf(60, ly, 500, 88, angle=0))
    # 贝叶上的经文
    for li, ly in enumerate((160, 342)):
        for row in range(7):
            for col in range(12):
                x = 104 + col * 28
                y = ly - 33 + row * 11
                if li == 0 and row == 3 and col == 6:
                    b.append(f'<rect x="{x-4}" y="{y-6}" width="13" height="13" fill="{CINNABAR}" stroke="{DARK}" stroke-width="0.8"/>')
                    b.append(f'<path d="M{x-1} {y-4} L{x+5} {y-4} L{x+5} {y} L{x} {y} L{x} {y+4} L{x+6} {y+4}" stroke="{WHITE}" stroke-width="1.2" fill="none"/>')
                else:
                    b.append(f'<path d="M{x} {y} L{x+12} {y}" stroke="{INK}" stroke-width="2.1" opacity="0.6"/>')
    # 上印：碎成 64 片
    sx, sy = 438, 160
    b.append(f'<path d="M{sx-31} {sy-31} L{sx+31} {sy-31} L{sx+31} {sy-8} L{sx+23} {sy-2} L{sx+31} {sy+5} L{sx+31} {sy+31} L{sx-31} {sy+31} Z" fill="none" stroke="{CINNABAR}" stroke-width="3"/>')
    for i in range(8):
        for j in range(8):
            gx = sx - 27 + i * 7.4
            gy = sy - 27 + j * 7.4
            ang = math.atan2(gy - sy, gx - sx) + 0.5 * ((i + j) % 2)
            rad = 20 + 74 * ((i * 5 + j * 3) % 9) / 8
            px = gx + math.cos(ang) * rad
            py = gy + math.sin(ang) * rad * 0.92
            rot = (i * 13 + j * 19) % 80 - 40
            sz = 5.5 + ((i + j) % 3) * 1.4
            b.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate({rot})" opacity="{0.55+0.05*((i+j)%5)}"><rect x="{-sz/2:.1f}" y="{-sz/2:.1f}" width="{sz:.1f}" height="{sz:.1f}" fill="{CINNABAR}" stroke="{DARK}" stroke-width="0.5"/><path d="M{-sz*0.25:.1f} {sz*0.2:.1f} L{sz*0.25:.1f} {sz*0.2:.1f}" stroke="{WHITE}" stroke-width="0.8"/></g>')
    for cx, cy, r in [(500, 116, 12), (520, 190, 9), (470, 216, 8)]:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}" opacity="0.12"/>')
    # 下印：完好，六十四格
    b.append(f'<rect x="399" y="306" width="72" height="72" fill="{CINNABAR}" stroke="{GOLD}" stroke-width="2.4"/>')
    b.append(f'<rect x="406" y="313" width="58" height="58" fill="none" stroke="{WHITE}" stroke-width="1.6" opacity="0.9"/>')
    for i in range(8):
        for j in range(8):
            b.append(f'<rect x="{409+i*7:.1f}" y="{316+j*7:.1f}" width="3.8" height="3.8" fill="{WHITE}" opacity="0.92"/>')
    # 一片飞叶
    b.append(palm_leaf(572, 238, 78, 44, angle=-30, fill="#e8d6b0"))
    return svg(720, 470, "".join(b))


# ---------------- 图 3：剑峰石碑 ----------------
def fig03():
    W, H = 720, 560
    b = []
    b.append(mountain(-40, 520, 420, 220, AZURITE, 0.2))
    b.append(mountain(300, 530, 460, 250, AZURITE, 0.14))
    b.append(cloud(48, 86, 0.6, WHITE, GOLD, 0.6))
    b.append(cloud(560, 108, 0.52, WHITE, GOLD, 0.5))
    b.append(pine(624, 526, 0.9))
    # 赑屃
    b.append(turtle(350, 452, 380))
    b.append(f'<path d="M192 445 L508 445 L516 456 L184 456 Z" fill="#d9c9a8" stroke="{OCHRE}" stroke-width="1.6"/>')
    # 碑身
    b.append(f'<rect x="190" y="118" width="320" height="327" fill="#e6ddc6" stroke="{OCHRE}" stroke-width="2.2"/>')
    b.append(f'<rect x="182" y="118" width="336" height="7" fill="{GOLD}" opacity="0.55"/>')
    # 碑首
    b.append(f'<path d="M175 122 L175 96 C175 40 525 40 525 96 L525 122 Z" fill="#e6ddc6" stroke="{OCHRE}" stroke-width="2.4"/>')
    b.append(f'<path d="M188 118 L188 98 C188 54 512 54 512 98 L512 118" fill="none" stroke="{GOLD}" stroke-width="1.3"/>')
    b.append(f'<circle cx="350" cy="84" r="9" fill="{PAPER}" stroke="{GOLD}" stroke-width="1.8"/>')
    # 碑首螭龙
    for sgn in (-1, 1):
        x0 = 350 + sgn * 66
        b.append(f'<path d="M{x0} 108 C{x0-sgn*4} 88 {x0-sgn*26} 82 {x0-sgn*32} 96 C{x0-sgn*38} 112 {x0-sgn*18} 120 {x0-sgn*10} 108 C{x0-sgn*6} 100 {x0-sgn*16} 94 {x0-sgn*22} 100" fill="none" stroke="{GOLD}" stroke-width="1.8" opacity="0.85"/>')
        b.append(f'<path d="M{x0-sgn*30} 94 C{x0-sgn*38} 90 {x0-sgn*38} 104 {x0-sgn*30} 106" fill="none" stroke="{GOLD}" stroke-width="1.4" opacity="0.8"/>')
    b.append(f'<path d="M320 70 C328 62 372 62 380 70 L376 76 L324 76 Z" fill="none" stroke="{GOLD}" stroke-width="1.3"/>')
    # 碑面
    b.append(f'<rect x="200" y="128" width="300" height="304" fill="#efe7d2" stroke="{OCHRE}" stroke-width="1"/>')
    for cx, cy in [(214, 142), (486, 142), (214, 418)]:
        b.append(f'<path d="M{cx} {cy} C{cx+8} {cy-8} {cx+18} {cy-2} {cx+12} {cy+6} C{cx+6} {cy+12} {cx-2} {cy+8} {cx} {cy}" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity="0.65"/>')
    # 椭圆曲线 y^2 = x^3 + 7
    p = (-1.0, math.sqrt(6.0))
    q = (2.0, -math.sqrt(15.0))
    m = (q[1] - p[1]) / (q[0] - p[0])
    x3 = m * m - p[0] - q[0]
    r = (x3, m * x3 + (p[1] - m * p[0]))
    pp = (x3, -r[1])
    cx, cy = 350, 288
    sx, sy = 40.0, 20.5
    def T(pt):
        return (cx + pt[0] * sx, cy - pt[1] * sy)
    left = -7 ** (1 / 3)
    right = 3.6
    for sign in (1, -1):
        pts = []
        for i in range(481):
            x = left + (right - left) * i / 480
            y = sign * math.sqrt(max(0, x ** 3 + 7))
            pts.append(T((x, y)))
        d = "M" + " L".join(f"{a:.2f} {b_:.2f}" for a, b_ in pts)
        b.append(f'<path d="{d}" fill="none" stroke="{AZURITE}" stroke-width="4.2" stroke-linecap="round"/>')
        b.append(f'<path d="{d}" fill="none" stroke="{WHITE}" stroke-width="1.1" opacity="0.45"/>')
    # 割线 P-Q-R
    ps, qs, rs = T(p), T(q), T(r)
    slope = (rs[1] - ps[1]) / (rs[0] - ps[0])
    xa, xb = 275, 494
    ya = ps[1] + (xa - ps[0]) * slope
    yb = ps[1] + (xb - ps[0]) * slope
    b.append(f'<path d="M{xa} {ya:.2f} L{xb} {yb:.2f}" stroke="{CINNABAR}" stroke-width="2.8" stroke-dasharray="10 6"/>')
    # 反射线 R -> P+Q
    pps = T(pp)
    b.append(f'<path d="M{rs[0]:.2f} {rs[1]:.2f} L{pps[0]:.2f} {pps[1]:.2f}" stroke="{GAMBOGE}" stroke-width="2.2" stroke-dasharray="5 5"/>')
    # 四点
    for pt, color, label, lx, ly, anchor in [
        (p, MALACHITE, "P", 296, 226, "end"),
        (q, MALACHITE, "Q", 448, 389, "start"),
        (pp, GAMBOGE, "P+Q", 480, 157, "end"),
        (r, CINNABAR, "R", 480, 444, "end"),
    ]:
        x, y = T(pt)
        b.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="11" fill="{WHITE}"/>')
        b.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7" fill="{color}" stroke="{INK}" stroke-width="1.4"/>')
        b.append(f'<circle cx="{x-2:.2f}" cy="{y-2.6:.2f}" r="1.8" fill="{WHITE}" opacity="0.9"/>')
        fs = 22 if label == "P+Q" else 26
        b.append(f'<text x="{lx}" y="{ly}" font-family="{KAI}" font-size="{fs}" font-weight="700" fill="{color}" stroke="{WHITE}" stroke-width="4" paint-order="stroke" text-anchor="{anchor}">{label}</text>')
    # 石阶
    b.append(f'<path d="M150 512 L550 512 L572 526 L128 526 Z" fill="#d9c9a8" stroke="{OCHRE}" stroke-width="1.4"/>')
    return svg(W, H, "".join(b))


# ---------------- 图 4：机关凿山 ----------------
def fig04():
    W, H = 720, 470
    b = []
    b.append(mountain(0, 440, 720, 120, AZURITE, 0.12))
    # 引水槽与落水
    b.append(f'<path d="M40 72 L182 72 L182 104 L54 104 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<path d="M56 82 L176 82 L176 96 L60 96 Z" fill="{AZURITE}" opacity="0.55"/>')
    for i in range(4):
        b.append(f'<path d="M{168+i*3} 104 C{166+i*3} 128 {172+i*3} 150 {170+i*3} 176" stroke="{AZURITE}" stroke-width="3" opacity="0.55"/>')
    # 水车
    b.append(waterwheel(165, 255, 82))
    b.append(f'<path d="M165 337 L165 392" stroke="{OCHRE}" stroke-width="10"/>')
    b.append(f'<path d="M132 392 L198 392" stroke="{OCHRE}" stroke-width="8"/>')
    # 传动轴与齿轮
    b.append(f'<path d="M165 255 L300 255" stroke="{OCHRE}" stroke-width="9"/>')
    b.append(gear(300, 255, 42, 16))
    b.append(gear(356, 300, 29, 13))
    b.append(f'<path d="M356 300 L420 255" stroke="{OCHRE}" stroke-width="7"/>')
    # 木架
    b.append(f'<path d="M398 360 L398 160 M478 360 L478 160" stroke="{OCHRE}" stroke-width="9"/>')
    b.append(f'<path d="M388 160 L488 160" stroke="{OCHRE}" stroke-width="9"/>')
    b.append(f'<path d="M388 206 L488 206" stroke="{OCHRE}" stroke-width="5" opacity="0.8"/>')
    b.append(dougong(396, 146, 84, OCHRE, GOLD))
    # 钻架与钻杆
    b.append(f'<path d="M414 206 L414 300 M462 206 L462 300" stroke="{OCHRE}" stroke-width="5"/>')
    b.append(f'<rect x="406" y="244" width="64" height="22" fill="{OCHRE}" stroke="{INK}" stroke-width="1.4"/>')
    b.append(f'<path d="M430 255 L514 255" stroke="{STEEL}" stroke-width="9" stroke-linecap="round"/>')
    b.append(f'<path d="M430 251 L514 251" stroke="{WHITE}" stroke-width="2" opacity="0.4"/>')
    # 螺旋钻头
    for i in range(7):
        x = 508 + i * 5
        b.append(f'<path d="M{x} 244 L{x+4} 266" stroke="{GOLD}" stroke-width="2" opacity="0.9"/>')
    b.append(f'<path d="M508 244 L545 255 L508 266 Z" fill="{STEEL}" stroke="{INK}" stroke-width="1.2"/>')
    # 绞盘
    b.append(f'<circle cx="440" cy="180" r="18" fill="none" stroke="{GOLD}" stroke-width="3"/>')
    b.append(f'<path d="M440 162 L440 198 M422 180 L458 180" stroke="{OCHRE}" stroke-width="3"/>')
    # 石壁
    cliff = "M520 54 L700 54 L700 410 L520 410 L504 372 L520 336 L500 298 L522 260 L504 222 L520 184 L502 146 L520 108 Z"
    b.append(f'<path d="{cliff}" fill="#c4b294" stroke="{OCHRE}" stroke-width="2.4"/>')
    for i in range(7):
        y = 80 + i * 46
        b.append(f'<path d="M540 {y} C580 {y-8} 640 {y+10} 690 {y-2}" stroke="{OCHRE}" stroke-width="0.9" fill="none" opacity="0.35"/>')
    # 六十四孔
    for i in range(8):
        for j in range(8):
            x = 536 + i * 18
            y = 108 + j * 18
            glow = (i * 3 + j * 5) % 11 == 0
            b.append(f'<rect x="{x}" y="{y}" width="13" height="13" fill="{"#8a5a22" if glow else "#4a3a2c"}" stroke="{GOLD}" stroke-width="1.1"/>')
            if glow:
                b.append(f'<rect x="{x+3}" y="{y+3}" width="7" height="7" fill="{GAMBOGE}" opacity="0.9"/>')
    # 石屑
    for x, y in [(500, 392), (520, 400), (545, 388), (565, 405), (590, 396)]:
        b.append(f'<path d="M{x} {y} L{x+7} {y-5} L{x+10} {y+2} Z" fill="#a89878" stroke="{OCHRE}" stroke-width="0.7"/>')
    # 城头铜铳
    b.append(f'<path d="M612 54 L668 54 L668 44 L612 44 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1"/>')
    b.append(f'<path d="M620 44 L662 44 L666 30 L616 30 Z" fill="{STEEL}" stroke="{INK}" stroke-width="1.4"/>')
    b.append(f'<rect x="648" y="30" width="6" height="14" fill="{GOLD}" stroke="{INK}" stroke-width="0.8"/>')
    return svg(W, H, "".join(b))


# ---------------- 图 5：铜锁合符 ----------------
def fig05():
    W, H = 720, 470
    b = []
    # 门楼
    b.append(roof(50, 28, 620, 52))
    b.append(f'<rect x="70" y="78" width="580" height="274" fill="#8c2f26" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<rect x="70" y="78" width="580" height="274" fill="url(#tile)" opacity="0.16"/>')
    b.append(f'<rect x="70" y="338" width="580" height="16" fill="#c9b895" stroke="{OCHRE}" stroke-width="1.2"/>')
    # 门框
    b.append(f'<rect x="232" y="104" width="256" height="240" fill="#6f241e" stroke="{GOLD}" stroke-width="3"/>')
    b.append(f'<rect x="240" y="112" width="240" height="232" fill="none" stroke="{GAMBOGE}" stroke-width="1.2"/>')
    b.append(f'<path d="M360 112 L360 344" stroke="{INK}" stroke-width="3"/>')
    # 门钉：8 列 9 行 + 门楣 9 枚
    for j in range(9):
        for i in range(8):
            x = 258 + i * 28
            y = 132 + j * 22
            b.append(f'<circle cx="{x}" cy="{y}" r="5.2" fill="{GAMBOGE}" stroke="{GOLD}" stroke-width="1"/>')
            b.append(f'<circle cx="{x-1.4}" cy="{y-1.6}" r="1.4" fill="{WHITE}" opacity="0.7"/>')
    for i in range(9):
        b.append(f'<circle cx="{250+i*27.5}" cy="{104}" r="5.2" fill="{GAMBOGE}" stroke="{GOLD}" stroke-width="1"/>')
    # 铺首
    for cx in (302, 418):
        b.append(f'<circle cx="{cx}" cy="246" r="24" fill="{GOLD}" stroke="{INK}" stroke-width="1.6"/>')
        b.append(f'<circle cx="{cx}" cy="246" r="15" fill="none" stroke="{INK}" stroke-width="1.2"/>')
        b.append(f'<path d="M{cx-9} 240 C{cx-3} 234 {cx+3} 234 {cx+9} 240 M{cx-9} 252 C{cx-3} 258 {cx+3} 258 {cx+9} 252" stroke="{INK}" stroke-width="1.6" fill="none"/>')
        b.append(f'<circle cx="{cx}" cy="266" r="9" fill="none" stroke="{GAMBOGE}" stroke-width="3.4"/>')
    # 铜锁
    b.append(f'<path d="M330 236 C330 210 390 210 390 236" fill="none" stroke="{GOLD}" stroke-width="7"/>')
    b.append(f'<rect x="324" y="236" width="72" height="48" rx="4" fill="{GAMBOGE}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<rect x="331" y="243" width="58" height="34" fill="none" stroke="{WHITE}" stroke-width="1.2" opacity="0.7"/>')
    b.append(f'<circle cx="360" cy="258" r="5" fill="{INK}"/>')
    b.append(f'<path d="M360 262 L360 272" stroke="{INK}" stroke-width="4"/>')
    b.append(tassel(360, 284, 34, CINNABAR, 1.1))
    # 匾额
    b.append(f'<rect x="300" y="66" width="120" height="30" fill="{AZURITE}" stroke="{GOLD}" stroke-width="2"/>')
    b.append(f'<circle cx="360" cy="81" r="9" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    b.append(f'<path d="M360 76 C367 76 367 86 360 86 C353 86 353 78 360 78" stroke="{GOLD}" stroke-width="1.2" fill="none" opacity="0.8"/>')
    # 灯笼
    for cx in (150, 570):
        b.append(f'<path d="M{cx} 100 L{cx} 124" stroke="{OCHRE}" stroke-width="2"/>')
        b.append(f'<path d="M{cx-18} 124 L{cx+18} 124 L{cx+14} 166 L{cx-14} 166 Z" fill="{CINNABAR}" stroke="{GOLD}" stroke-width="1.6"/>')
        b.append(f'<path d="M{cx-18} 124 L{cx+18} 124 M{cx-14} 166 L{cx+14} 166" stroke="{GOLD}" stroke-width="3"/>')
        b.append(f'<path d="M{cx} 166 L{cx} 186" stroke="{GOLD}" stroke-width="2"/>')
        b.append(tassel(cx, 186, 22, CINNABAR, 0.8))
    # 漆盘
    b.append(f'<rect x="206" y="382" width="308" height="46" rx="10" fill="#2a2420" stroke="{GOLD}" stroke-width="2.4"/>')
    b.append(f'<rect x="216" y="390" width="288" height="30" rx="6" fill="#6f241e" stroke="{GAMBOGE}" stroke-width="1"/>')
    # 鱼符合拢
    cy = 405
    # 合鱼虚影
    b.append(f'<path d="M270 405 C270 382 320 372 360 376 C400 372 450 382 450 405 C450 428 400 438 360 434 C320 438 270 428 270 405 Z" fill="none" stroke="{GOLD}" stroke-width="1" stroke-dasharray="4 4" opacity="0.45"/>')
    seam = "M360 372 L354 384 L366 394 L354 406 L366 418 L360 430"
    # 左半
    left = f'M360 372 C330 370 294 380 276 394 L262 380 L268 405 L262 430 L276 416 C294 430 330 440 360 430 Z'
    b.append(f'<path d="{left}" fill="{GOLD}" stroke="{OCHRE}" stroke-width="1.8"/>')
    # 右半
    right = f'M360 372 C392 370 428 378 448 390 C462 396 468 401 468 405 C468 409 462 414 448 420 C428 432 392 440 360 430 Z'
    b.append(f'<path d="{right}" fill="{GOLD}" stroke="{OCHRE}" stroke-width="1.8"/>')
    b.append(f'<path d="{seam}" fill="none" stroke="{OCHRE}" stroke-width="3"/>')
    # 鱼鳞与眼
    for i in range(4):
        b.append(f'<path d="M{392+i*12} 392 Q{398+i*12} 405 {392+i*12} 418" stroke="{OCHRE}" stroke-width="1.2" fill="none" opacity="0.6"/>')
    b.append(f'<circle cx="440" cy="400" r="2.8" fill="{OCHRE}"/>')
    return svg(W, H, "".join(b))


# ---------------- 图 6：三器 ----------------
def fig06():
    W, H = 720, 460
    b = []
    for x in (40, 260, 480):
        b.append(f'<rect x="{x}" y="88" width="200" height="310" fill="#efe7d2" stroke="{GOLD}" stroke-width="1.6"/>')
        b.append(f'<rect x="{x+7}" y="95" width="186" height="296" fill="none" stroke="{CINNABAR}" stroke-width="0.8" opacity="0.3"/>')
        b.append(f'<rect x="{x+68}" y="76" width="64" height="20" fill="{AZURITE}" stroke="{GOLD}" stroke-width="1.2"/>')
        b.append(f'<circle cx="{x+100}" cy="86" r="4" fill="{GOLD}"/>')
    # 左：博山炉，烟成链
    cx = 140
    b.append(f'<path d="M{cx-44} 350 L{cx+44} 350 L{cx+34} 368 L{cx-34} 368 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<path d="M{cx-14} 368 L{cx-8} 388 M{cx} 368 L{cx} 390 M{cx+14} 368 L{cx+8} 388" stroke="{OCHRE}" stroke-width="4"/>')
    b.append(f'<path d="M{cx-52} 318 C{cx-52} 340 {cx-28} 352 {cx} 352 C{cx+28} 352 {cx+52} 340 {cx+52} 318 Z" fill="{GAMBOGE}" stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<path d="M{cx-46} 314 L{cx+46} 314" stroke="{GOLD}" stroke-width="4"/>')
    b.append(f'<path d="M{cx-40} 314 L{cx-26} 280 L{cx-8} 300 L{cx} 264 L{cx+10} 300 L{cx+28} 280 L{cx+40} 314 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.4"/>')
    b.append(f'<path d="M{cx-14} 314 L{cx-4} 292 L{cx+6} 306" stroke="{GOLD}" stroke-width="1.2" fill="none"/>')
    # 烟链
    b.append(f'<path d="M{cx} 262 C{cx-16} 236 {cx+18} 220 {cx-4} 194 C{cx-22} 170 {cx+16} 150 {cx} 118" stroke="{WHITE}" stroke-width="7" fill="none" opacity="0.55"/>')
    for i in range(6):
        yy = 246 - i * 26
        b.append(f'<ellipse cx="{cx}" cy="{yy}" rx="{14 if i%2==0 else 8}" ry="{6 if i%2==0 else 11}" fill="none" stroke="{WHITE}" stroke-width="3.2" opacity="0.95"/>')
        b.append(f'<ellipse cx="{cx}" cy="{yy}" rx="{14 if i%2==0 else 8}" ry="{6 if i%2==0 else 11}" fill="none" stroke="{AZURITE}" stroke-width="1.2" opacity="0.6"/>')
    # 中：棋树，枝成 DAG
    cx = 360
    b.append(f'<path d="M{cx-42} 342 L{cx+42} 342 L{cx+32} 386 L{cx-32} 386 Z" fill="#3a2b22" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<path d="M{cx-30} 348 L{cx+30} 348" stroke="{GOLD}" stroke-width="1.4" opacity="0.7"/>')
    b.append(f'<path d="M{cx} 342 C{cx-4} 310 {cx+2} 280 {cx} 250" stroke="{OCHRE}" stroke-width="8" fill="none"/>')
    branches = [
        (cx, 250, cx-42, 214), (cx, 250, cx+44, 218),
        (cx-42, 214, cx-64, 178), (cx-42, 214, cx-18, 168),
        (cx+44, 218, cx+22, 176), (cx+44, 218, cx+70, 186),
        (cx-42, 214, cx-52, 258), (cx+44, 218, cx+58, 256),
    ]
    for x1, y1, x2, y2 in branches:
        b.append(f'<path d="M{x1} {y1} C{(x1+x2)/2} {(y1+y2)/2-8} {x2} {y2+6} {x2} {y2}" stroke="{OCHRE}" stroke-width="3.4" fill="none"/>')
    for x1, y1, x2, y2 in branches:
        b.append(f'<circle cx="{x2}" cy="{y2}" r="6" fill="{MALACHITE}" stroke="{GOLD}" stroke-width="1.4"/>')
        b.append(f'<circle cx="{x2}" cy="{y2}" r="2" fill="{WHITE}" opacity="0.7"/>')
    for x, y in [(cx-64,178),(cx-18,168),(cx+22,176),(cx+70,186),(cx-52,258),(cx+58,256)]:
        for dx, dy in [(-10,-8),(0,-12),(10,-8),(0,2)]:
            b.append(f'<ellipse cx="{x+dx}" cy="{y+dy}" rx="9" ry="5" fill="{MALACHITE}" opacity="0.75"/>')
    # 右：分水，四渠并行
    cx = 590
    b.append(f'<rect x="556" y="104" width="68" height="96" fill="#c9b895" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<rect x="564" y="112" width="52" height="80" fill="{AZURITE}" opacity="0.5"/>')
    b.append(f'<path d="M564 112 L564 192 M616 112 L616 192" stroke="{WHITE}" stroke-width="1.4" opacity="0.6"/>')
    p0 = f'M{cx-48} 214 C{cx-30} 198 {cx+30} 198 {cx+48} 214 C{cx+30} 230 {cx-30} 230 {cx-48} 214 Z'
    b.append(f'<path d="{p0}" fill="{OCHRE}" stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<path d="M{cx+40} 214 C{cx+52} 204 {cx+62} 208 {cx+66} 214 C{cx+62} 220 {cx+52} 224 {cx+40} 214 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.4"/>')
    b.append(f'<circle cx="{cx+30}" cy="210" r="1.8" fill="{INK}"/>')
    # 五道石堤，四条水渠
    for i in range(5):
        xt = cx + (i - 2) * 9
        xb = 498 + i * 46
        b.append(f'<path d="M{xt} 232 L{xb} 356" stroke="{OCHRE}" stroke-width="6" opacity="0.75"/>')
        b.append(f'<path d="M{xt} 232 L{xb} 356" stroke="{WHITE}" stroke-width="1.6" opacity="0.35"/>')
    for i in range(4):
        x1 = cx + (i - 1.5) * 9
        x2 = 521 + i * 46
        d = f'M{x1} 232 C{x1+(x2-x1)*0.5} 276 {x2} 312 {x2} 356'
        b.append(f'<path d="{d}" stroke="{AZURITE}" stroke-width="11" fill="none" opacity="0.55"/>')
        b.append(f'<path d="{d}" stroke="{WHITE}" stroke-width="2" fill="none" opacity="0.65"/>')
    b.append(f'<path d="M494 354 L686 354 L672 386 L508 386 Z" fill="{GAMBOGE}" stroke="{INK}" stroke-width="1.8"/>')
    b.append(f'<rect x="506" y="358" width="168" height="11" fill="{AZURITE}" opacity="0.6"/>')
    return svg(W, H, "".join(b))


# ---------------- 图 7：转轮藏 ----------------
def _quad(p0, p1, p3, u, v):
    return (p0[0] + u * (p1[0] - p0[0]) + v * (p3[0] - p0[0]),
            p0[1] + u * (p1[1] - p0[1]) + v * (p3[1] - p0[1]))


def _poly(pts, fill="none", stroke=INK, sw=1.0, op=1.0):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{op}"/>')


def fig07():
    W, H = 720, 560
    b = []
    cx = 360
    # 殿内
    b.append(f'<rect x="42" y="48" width="636" height="484" fill="#efe7d2" stroke="{OCHRE}" stroke-width="1.6"/>')
    b.append(f'<rect x="70" y="80" width="580" height="342" fill="#2a2420" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<rect x="86" y="96" width="548" height="310" fill="url(#hui)" opacity="0.2"/>')
    for x in (92, 628):
        b.append(f'<rect x="{x-9}" y="60" width="18" height="408" fill="{CINNABAR}" stroke="{INK}" stroke-width="1.4"/>')
        b.append(f'<rect x="{x-13}" y="58" width="26" height="9" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>')
        b.append(f'<rect x="{x-13}" y="460" width="26" height="9" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>')
    b.append(f'<path d="M60 52 L660 52" stroke="{OCHRE}" stroke-width="8"/>')
    b.append(dougong(70, 60, 580, OCHRE, GOLD))
    # 地面铺砖
    b.append(f'<rect x="70" y="422" width="580" height="90" fill="#cdbb9b" stroke="{OCHRE}" stroke-width="1.4"/>')
    for i in range(15):
        b.append(f'<path d="M{80+i*40} 422 L{80+i*40} 512" stroke="{OCHRE}" stroke-width="0.7" opacity="0.5"/>')
    for j in range(3):
        b.append(f'<path d="M70 {446+j*24} L650 {446+j*24}" stroke="{OCHRE}" stroke-width="0.7" opacity="0.5"/>')
    # 石槽与齿轨
    b.append(f'<ellipse cx="{cx}" cy="482" rx="250" ry="36" fill="#a8977a" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<ellipse cx="{cx}" cy="482" rx="228" ry="29" fill="#3a2b22" stroke="{GOLD}" stroke-width="1.4" opacity="0.92"/>')
    for k in range(40):
        a = math.radians(k * 9)
        x = cx + math.cos(a) * 228
        y = 482 + math.sin(a) * 29
        b.append(f'<rect x="-5" y="-2.4" width="10" height="4.8" fill="{GOLD}" stroke="{INK}" stroke-width="0.3" '
                 f'transform="translate({x:.1f},{y:.1f}) rotate({k*9})" opacity="0.72"/>')
    # 须弥座
    b.append(_poly([(196, 418), (524, 418), (546, 444), (174, 444)], "#d9c9a8", OCHRE, 1.8))
    b.append(_poly([(236, 444), (484, 444), (500, 464), (220, 464)], "#c9b895", OCHRE, 1.4))
    for i in range(9):
        b.append(f'<path d="M{246+i*28} 446 L{246+i*28} 462" stroke="{OCHRE}" stroke-width="0.9" opacity="0.7"/>')
    # 八角顶面
    top = [(150, 150), (212, 182), (300, 198), (420, 198), (508, 182), (570, 150),
           (508, 118), (212, 118)]
    b.append(_poly(top, "#7a2a22", GOLD, 2.2))
    for s in (0.84, 0.58):
        pts = [(cx + (x - cx) * s, 150 + (y - 150) * s) for x, y in top]
        b.append(_poly(pts, "none", GAMBOGE, 0.9, 0.55))
    # 五面柜身
    faces = [
        ([(150, 150), (212, 182), (212, 418), (150, 418)], "#4a1712"),
        ([(212, 182), (300, 198), (300, 418), (212, 418)], "#5a1d18"),
        ([(300, 198), (420, 198), (420, 418), (300, 418)], "#6f241e"),
        ([(420, 198), (508, 182), (508, 418), (420, 418)], "#5a1d18"),
        ([(508, 182), (570, 150), (570, 418), (508, 418)], "#4a1712"),
    ]
    for pts, fill in faces:
        b.append(_poly(pts, fill, GOLD, 1.6))
    # 经屉
    trays = [
        ((212, 182), (300, 198), (212, 418), 2, 5),
        ((300, 198), (420, 198), (300, 418), 3, 6),
        ((420, 198), (508, 182), (420, 418), 2, 5),
    ]
    for p0, p1, p3, cols, rows in trays:
        b.append(_poly([_quad(p0, p1, p3, u, v) for u, v in
                        [(0.1, 0.05), (0.9, 0.05), (0.9, 0.95), (0.1, 0.95)]],
                       "none", GAMBOGE, 1.0, 0.9))
        for r in range(rows):
            for c in range(cols):
                u0 = 0.16 + c * (0.68 / cols)
                u1 = u0 + 0.68 / cols - 0.03
                v0 = 0.08 + r * (0.84 / rows)
                v1 = v0 + 0.84 / rows - 0.018
                q = [_quad(p0, p1, p3, u, v) for u, v in
                     [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]]
                b.append(_poly(q, "#3a1512", GOLD, 0.5, 0.95))
                mid = _quad(p0, p1, p3, (u0 + u1) / 2, (v0 + v1) / 2)
                b.append(f'<path d="M{mid[0]-2.6:.1f} {mid[1]:.1f} L{mid[0]+2.6:.1f} {mid[1]:.1f}" '
                         f'stroke="{WHITE}" stroke-width="1.5" opacity="0.9"/>')
                b.append(f'<circle cx="{mid[0]:.1f}" cy="{mid[1]:.1f}" r="0.9" fill="{GOLD}"/>')
    # 轴与宝顶
    b.append(f'<path d="M360 118 L360 62" stroke="{OCHRE}" stroke-width="8"/>')
    b.append(f'<path d="M350 118 L370 118" stroke="{GOLD}" stroke-width="3"/>')
    b.append(f'<circle cx="360" cy="56" r="11" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<circle cx="360" cy="56" r="4.6" fill="{CINNABAR}"/>')
    b.append(f'<path d="M360 67 L360 76" stroke="{GOLD}" stroke-width="2"/>')
    # 更漏
    bx = 136
    b.append(f'<rect x="{bx-36}" y="244" width="72" height="8" fill="{OCHRE}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<rect x="{bx-32}" y="452" width="64" height="9" fill="{OCHRE}" stroke="{INK}" stroke-width="1.2"/>')
    for x in (bx - 30, bx + 24):
        b.append(f'<rect x="{x}" y="250" width="6" height="204" fill="{OCHRE}" stroke="{INK}" stroke-width="1"/>')
    for yy, r in [(282, 28), (342, 24), (396, 20)]:
        b.append(f'<path d="M{bx-r} {yy} C{bx-r*1.16:.1f} {yy+18} {bx-r*0.72:.1f} {yy+33} {bx} {yy+35} '
                 f'C{bx+r*0.72:.1f} {yy+33} {bx+r*1.16:.1f} {yy+18} {bx+r} {yy} Z" fill="{GAMBOGE}" stroke="{INK}" stroke-width="1.6"/>')
        b.append(f'<ellipse cx="{bx}" cy="{yy}" rx="{r}" ry="{r*0.3:.1f}" fill="#e8bd5e" stroke="{INK}" stroke-width="1.3"/>')
        b.append(f'<path d="M{bx-r*0.6:.1f} {yy-2} C{bx-r*0.48:.1f} {yy-13} {bx+r*0.48:.1f} {yy-13} {bx+r*0.6:.1f} {yy-2} Z" fill="#b8892f" stroke="{INK}" stroke-width="1"/>')
        b.append(f'<path d="M{bx-r*0.9:.1f} {yy-1} C{bx-r*0.8:.1f} {yy-21} {bx+r*0.8:.1f} {yy-21} {bx+r*0.9:.1f} {yy-1}" fill="none" stroke="{GOLD}" stroke-width="2"/>')
        b.append(f'<path d="M{bx} {yy+35} L{bx} {yy+45}" stroke="{AZURITE}" stroke-width="3"/>')
    # 香炉与烟
    hx, hy = 596, 430
    b.append(f'<path d="M{hx-32} {hy} C{hx-36} {hy+28} {hx+36} {hy+28} {hx+32} {hy} Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<ellipse cx="{hx}" cy="{hy}" rx="32" ry="9" fill="#a9763f" stroke="{INK}" stroke-width="1.4"/>')
    b.append(f'<path d="M{hx-30} {hy} C{hx-46} {hy-8} {hx-42} {hy-24} {hx-30} {hy-16}" fill="none" stroke="{GOLD}" stroke-width="2.6"/>')
    b.append(f'<path d="M{hx+30} {hy} C{hx+46} {hy-8} {hx+42} {hy-24} {hx+30} {hy-16}" fill="none" stroke="{GOLD}" stroke-width="2.6"/>')
    for dx in (-18, 0, 18):
        b.append(f'<path d="M{hx+dx} {hy+20} L{hx+dx*1.12:.1f} {hy+34}" stroke="{INK}" stroke-width="3"/>')
    b.append(cloud(hx - 30, hy - 62, 0.34, WHITE, GOLD, 0.8))
    b.append(cloud(hx - 4, hy - 86, 0.24, WHITE, GOLD, 0.62))
    return svg(W, H, "".join(b))


# ---------------- 图 8：阵图 ----------------
def _lantern(x, y):
    """石灯笼：基座、柱、灯室、攒尖顶。y 为地面。"""
    p = []
    p.append(f'<rect x="{x-20}" y="{y-8}" width="40" height="8" fill="#b9a888" stroke="{OCHRE}" stroke-width="1.1"/>')
    p.append(f'<rect x="{x-7}" y="{y-34}" width="14" height="26" fill="#c9b895" stroke="{OCHRE}" stroke-width="1.1"/>')
    p.append(f'<rect x="{x-17}" y="{y-62}" width="34" height="28" fill="#d9c9a8" stroke="{OCHRE}" stroke-width="1.2"/>')
    p.append(f'<rect x="{x-9}" y="{y-56}" width="18" height="16" fill="{GAMBOGE}" stroke="{INK}" stroke-width="0.8" opacity="0.85"/>')
    p.append(f'<path d="M{x-24} {y-62} L{x+24} {y-62} L{x+14} {y-72} L{x-14} {y-72} Z" fill="{STEEL}" stroke="{GOLD}" stroke-width="1"/>')
    p.append(f'<path d="M{x-24} {y-62} Q{x-28} {y-58} {x-20} {y-59} M{x+24} {y-62} Q{x+28} {y-58} {x+20} {y-59}" stroke="{GOLD}" stroke-width="1" fill="none"/>')
    p.append(f'<circle cx="{x}" cy="{y-78}" r="4" fill="{GOLD}" stroke="{INK}" stroke-width="0.7"/>')
    return "".join(p)


def fig08():
    W, H = 720, 560
    b = []
    cx, cy = 360, 290
    # 八角石台
    pts = []
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        pts.append((cx + math.cos(a) * 280, cy + math.sin(a) * 236))
    b.append(_poly(pts, "#cdbb9b", OCHRE, 2.4))
    pts2 = [(cx + (x - cx) * 0.93, cy + (y - cy) * 0.93) for x, y in pts]
    b.append(_poly(pts2, "#d9c9a8", OCHRE, 1.6))
    # 辐射砖缝
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        b.append(f'<path d="M{cx + math.cos(a)*40:.1f} {cy + math.sin(a)*34:.1f} '
                 f'L{cx + math.cos(a)*258:.1f} {cy + math.sin(a)*218:.1f}" '
                 f'stroke="{OCHRE}" stroke-width="0.8" opacity="0.5"/>')
    for rr in (74, 128, 182):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rr*1.06:.0f}" ry="{rr*0.94:.0f}" fill="none" stroke="{OCHRE}" stroke-width="0.9" opacity="0.55"/>')
    # 外圈六十四砖
    for k in range(64):
        a = math.radians(k * 5.625)
        x = cx + math.cos(a) * 246
        y = cy + math.sin(a) * 207
        b.append(f'<rect x="-5" y="-3.2" width="10" height="6.4" fill="{MALACHITE if k % 2 else GOLD}" '
                 f'stroke="{INK}" stroke-width="0.4" transform="translate({x:.1f},{y:.1f}) rotate({k*5.625})" opacity="0.8"/>')
    # 八门石阶
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        x = cx + math.cos(a) * 246
        y = cy + math.sin(a) * 208
        for j in range(3):
            b.append(f'<path d="M{x-14+j*3:.1f} {y-5+j*5:.1f} L{x+14-j*3:.1f} {y-5+j*5:.1f}" '
                     f'stroke="{OCHRE}" stroke-width="2.2" opacity="0.85" '
                     f'transform="rotate({22.5+45*k} {x:.1f} {y:.1f})"/>')
    # 入阵石道
    b.append(f'<path d="M360 524 L360 404" stroke="#b9a888" stroke-width="30"/>')
    b.append(f'<path d="M347 524 L347 404 M373 524 L373 404" stroke="{GOLD}" stroke-width="1.2" opacity="0.8"/>')
    for yy in (420, 444, 468, 492):
        b.append(f'<path d="M347 {yy} L373 {yy}" stroke="{OCHRE}" stroke-width="0.9" opacity="0.65"/>')
    # 验印台
    b.append(f'<rect x="330" y="376" width="60" height="30" fill="{GAMBOGE}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<rect x="336" y="381" width="48" height="20" fill="{CINNABAR}" stroke="{GOLD}" stroke-width="1"/>')
    for i in range(4):
        for j in range(3):
            b.append(f'<rect x="{340+i*10.5}" y="{384+j*5.6}" width="6" height="3" fill="{WHITE}" opacity="0.9"/>')
    # 扣气秤
    b.append(f'<path d="M360 342 L360 372" stroke="{OCHRE}" stroke-width="4"/>')
    b.append(f'<path d="M318 342 L402 342" stroke="{OCHRE}" stroke-width="4"/>')
    for x in (308, 412):
        b.append(f'<path d="M{x} 342 L{x-8} 361 M{x} 342 L{x+8} 361" stroke="{GOLD}" stroke-width="1"/>')
        b.append(f'<ellipse cx="{x}" cy="364" rx="10" ry="4" fill="{GAMBOGE}" stroke="{INK}" stroke-width="1"/>')
    b.append(f'<circle cx="360" cy="342" r="4" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.7"/>')
    # 成、回两条石道
    for dx, col in ((-1, AZURITE), (1, GAMBOGE)):
        d = (f'M{cx+dx*44} {cy-30} C{cx+dx*110} {cy-92} {cx+dx*150} {cy-140} {cx+dx*186} {cy-172}')
        b.append(f'<path d="{d}" stroke="#b9a888" stroke-width="24" fill="none"/>')
        b.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="1.2" fill="none" opacity="0.85"/>')
        b.append(f'<path d="{d}" stroke="{col}" stroke-width="7" fill="none" opacity="0.4"/>')
    # 成、回牌坊
    for dx, col in ((-1, AZURITE), (1, GAMBOGE)):
        x = cx + dx * 196
        y = cy - 182
        for px in (x - 20, x + 20):
            b.append(f'<rect x="{px-3}" y="{y-38}" width="6" height="46" fill="{OCHRE}" stroke="{INK}" stroke-width="0.9"/>')
        b.append(f'<rect x="{x-28}" y="{y-42}" width="56" height="6" fill="{col}" stroke="{GOLD}" stroke-width="0.8"/>')
        b.append(f'<path d="M{x-32} {y-42} L{x+32} {y-42} L{x+24} {y-48} L{x-24} {y-48} Z" fill="{STEEL}" stroke="{GOLD}" stroke-width="0.8"/>')
    # 中央铜鼎
    b.append(f'<circle cx="{cx}" cy="{cy}" r="64" fill="#a8977a" stroke="{OCHRE}" stroke-width="2.4"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="54" fill="#6f7a52" stroke="{GOLD}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{GAMBOGE}" stroke-width="1.2" opacity="0.7"/>')
    for k in range(3):
        a = math.radians(90 + k * 120)
        x = cx + math.cos(a) * 62
        y = cy + math.sin(a) * 62
        b.append(f'<path d="M{cx + math.cos(a)*50:.1f} {cy + math.sin(a)*50:.1f} L{x:.1f} {y:.1f}" stroke="{OCHRE}" stroke-width="8"/>')
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{GAMBOGE}" stroke="{INK}" stroke-width="1"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="#3a2b22" stroke="{GOLD}" stroke-width="1.4"/>')
    b.append(flame(cx, cy + 12, 1.05))
    b.append(flame(cx - 17, cy + 4, 0.55))
    b.append(flame(cx + 17, cy + 4, 0.55))
    # 重入回路：自成道折返，绕过鼎腹
    loop = (f'M{cx+130} {cy-112} C{cx+202} {cy-38} {cx+186} {cy+72} {cx+106} {cy+86} '
            f'C{cx+54} {cy+96} {cx+24} {cy+50} {cx+44} {cy+26}')
    b.append(f'<path d="{loop}" fill="none" stroke="{CINNABAR}" stroke-width="5" opacity="0.9"/>')
    b.append(f'<path d="{loop}" fill="none" stroke="{WHITE}" stroke-width="1.1" opacity="0.4" stroke-dasharray="4 5"/>')
    b.append(f'<path d="M{cx+40} {cy+20} L{cx+55} {cy+18} L{cx+52} {cy+35}" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.8"/>')
    # 四角石灯笼
    for x, y in [(118, 150), (602, 150), (118, 454), (602, 454)]:
        b.append(_lantern(x, y))
    # 阵眼玉盘
    b.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{MALACHITE}" stroke="{GOLD}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{WHITE}" opacity="0.85"/>')
    # 云纹点角
    b.append(cloud(56, 70, 0.5, WHITE, GOLD, 0.3))
    b.append(cloud(566, 510, 0.44, WHITE, GOLD, 0.3))
    return svg(W, H, "".join(b))


# ---------------- 图 9：贝叶经塔 ----------------
def _walk(pts, n):
    segs, total = [], 0.0
    for i in range(len(pts) - 1):
        d = math.dist(pts[i], pts[i + 1])
        segs.append((total, total + d, pts[i], pts[i + 1]))
        total += d
    out = []
    for k in range(n):
        t = total * k / (n - 1)
        for s0, s1, a, c in segs:
            if t <= s1 + 1e-9:
                u = (t - s0) / (s1 - s0) if s1 > s0 else 0
                out.append((a[0] + u * (c[0] - a[0]), a[1] + u * (c[1] - a[1])))
                break
    return out


def fig09():
    W, H = 720, 580
    b = []
    # 殿内
    b.append(f'<rect x="40" y="40" width="640" height="500" fill="#efe7d2" stroke="{OCHRE}" stroke-width="1.6"/>')
    b.append(f'<rect x="80" y="70" width="560" height="430" fill="#2a2420" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<rect x="94" y="84" width="532" height="402" fill="url(#hui)" opacity="0.2"/>')
    for x in (100, 620):
        b.append(f'<rect x="{x-8}" y="64" width="16" height="440" fill="{CINNABAR}" stroke="{INK}" stroke-width="1.2"/>')
        b.append(f'<rect x="{x-11}" y="62" width="22" height="8" fill="{GOLD}" stroke="{INK}" stroke-width="0.8"/>')
    # 幡
    for x in (132, 566):
        b.append(f'<path d="M{x} 96 L{x} 262 L{x+24} 242 L{x+24} 114 Z" fill="{CINNABAR}" stroke="{GOLD}" stroke-width="1.1" opacity="0.9"/>')
        b.append(f'<path d="M{x+7} 124 C{x+17} 140 {x+9} 154 {x+19} 170 C{x+9} 186 {x+17} 200 {x+7} 216" stroke="{GOLD}" stroke-width="1.2" fill="none" opacity="0.75"/>')
    # 塔基与地宫
    b.append(_poly([(230, 466), (490, 466), (516, 522), (204, 522)], "#d9c9a8", OCHRE, 1.8))
    b.append(_poly([(222, 510), (498, 510), (516, 522), (204, 522)], "#c9b895", OCHRE, 1.2))
    b.append(f'<rect x="314" y="470" width="92" height="46" fill="#2a2420" stroke="{GOLD}" stroke-width="1.6"/>')
    b.append(f'<rect x="328" y="474" width="64" height="38" fill="{CINNABAR}" stroke="{GOLD}" stroke-width="2"/>')
    b.append(f'<rect x="333" y="479" width="54" height="28" fill="none" stroke="{WHITE}" stroke-width="1" opacity="0.8"/>')
    for i in range(8):
        for j in range(5):
            b.append(f'<rect x="{335.5+i*6.4:.1f}" y="{481+j*5.1:.1f}" width="3.4" height="3.1" fill="{WHITE}" opacity="0.92"/>')
    # 五层塔身
    tiers = [(466, 260), (414, 240), (362, 220), (310, 200), (258, 184)]
    for yb, w in tiers:
        x = 360 - w / 2
        b.append(f'<rect x="{x}" y="{yb-38}" width="{w}" height="38" fill="{WHITE}" stroke="{OCHRE}" stroke-width="1.2"/>')
        b.append(f'<rect x="{x+4}" y="{yb-38}" width="6" height="38" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.5"/>')
        b.append(f'<rect x="{x+w-10}" y="{yb-38}" width="6" height="38" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.5"/>')
        b.append(lattice(x + w * 0.32, yb - 31, w * 0.36, 23))
        b.append(railing(x - 12, yb - 2, w + 24, GOLD))
        b.append(roof(x - 18, yb - 38 - 18, w + 36, 18))
    # 攒尖顶
    b.append(roof(360 - 100, 180, 200, 28))
    b.append(f'<path d="M360 180 L360 162" stroke="{OCHRE}" stroke-width="4"/>')
    b.append(f'<circle cx="360" cy="158" r="7" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>')
    # 八片贝叶，挂在第五层檐下
    leaves = []
    for i in range(8):
        x = 244 + i * 28
        b.append(f'<path d="M{x} 219 L{x} 226" stroke="{CINNABAR}" stroke-width="1.4"/>')
        b.append(palm_leaf(x - 12, 226, 24, 13, angle=(-8 if i % 2 == 0 else 7), fill="#e8d6b0"))
        leaves.append((x, 239))
    # 节点
    n5 = [(280, 244), (320, 244), (368, 244), (412, 244)]
    n4 = [(308, 294), (404, 294)]
    n3 = [(360, 342)]
    n2 = [(360, 394)]
    n1 = [(360, 446)]
    root = (360, 474)
    # 暗金连线
    for i, (lx, ly) in enumerate(leaves):
        p = n5[i // 2]
        b.append(f'<path d="M{lx} {ly} L{p[0]} {p[1]}" stroke="{GOLD}" stroke-width="1.4" opacity="0.55"/>')
    for i, p in enumerate(n5):
        q = n4[i // 2]
        b.append(f'<path d="M{p[0]} {p[1]} L{q[0]} {q[1]}" stroke="{GOLD}" stroke-width="1.4" opacity="0.55"/>')
    b.append(f'<path d="M{n4[0][0]} {n4[0][1]} L360 340 M{n4[1][0]} {n4[1][1]} L360 340" stroke="{GOLD}" stroke-width="1.4" opacity="0.55"/>')
    b.append(f'<path d="M360 340 L360 474" stroke="{GOLD}" stroke-width="1.4" opacity="0.55"/>')
    # 高亮路径：十四颗金珠
    route = [leaves[0], n5[0], n4[0], n3[0], n2[0], n1[0], root]
    b.append(f'<path d="' + " L".join(f"{x:.1f} {y:.1f}" for x, y in route) + '" '
             f'fill="none" stroke="{CINNABAR}" stroke-width="4" opacity="0.85"/>')
    for x, y in _walk(route, 14):
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{GAMBOGE}" stroke="{GOLD}" stroke-width="0.8"/>')
    # 节点玉盘
    for n in n5 + n4 + n3 + n2 + n1:
        b.append(f'<circle cx="{n[0]}" cy="{n[1]}" r="9" fill="{MALACHITE}" stroke="{GOLD}" stroke-width="1.8"/>')
        b.append(f'<circle cx="{n[0]}" cy="{n[1]}" r="3.4" fill="{WHITE}" opacity="0.8"/>')
    # 根印金珠
    b.append(f'<circle cx="360" cy="474" r="6" fill="{GAMBOGE}" stroke="{GOLD}" stroke-width="1.2"/>')
    # 塔基石阶
    for i in range(3):
        b.append(f'<path d="M{224+i*6} {526+i*5} L{496-i*6} {526+i*5}" stroke="{OCHRE}" stroke-width="1.2" opacity="0.7"/>')
    return svg(W, H, "".join(b))


from figs_final import fig10, fig11, fig12  # noqa: E402
