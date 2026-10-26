#!/usr/bin/env python3
"""《天枢账簿》插图共享画法：暖纸、铁线描、工笔重彩、界画。

只用标准库生成 SVG 字符串，不依赖绘图库。
"""
import math

PAPER = "#f2e8d5"
INK = "#241f1c"
CINNABAR = "#a8322a"
AZURITE = "#2f5d7c"
MALACHITE = "#3f6f52"
GAMBOGE = "#d9a441"
OCHRE = "#8c5a3c"
WHITE = "#fbf6ea"
GOLD = "#b8892f"
STEEL = "#3b464b"
DARK = "#1d2529"

FONT = "Songti SC, STSong, serif"
KAI = "STKaiti, Kaiti SC, serif"


def svg(w, h, body, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<pattern id="fiber" width="46" height="46" patternUnits="userSpaceOnUse">
  <path d="M3 9 C14 7 26 12 43 8" stroke="#c9b895" stroke-width="0.45" fill="none" opacity="0.22"/>
  <path d="M0 31 C13 28 27 34 46 30" stroke="#c9b895" stroke-width="0.4" fill="none" opacity="0.18"/>
  <path d="M9 0 C7 14 12 30 8 46" stroke="#c9b895" stroke-width="0.35" fill="none" opacity="0.14"/>
</pattern>
<pattern id="hui" width="26" height="26" patternUnits="userSpaceOnUse">
  <path d="M3 23 L3 3 L23 3 M7 23 L7 7 L23 7" stroke="{GOLD}" stroke-width="1.2" fill="none" opacity="0.55"/>
</pattern>
<pattern id="waves" width="40" height="16" patternUnits="userSpaceOnUse">
  <path d="M0 12 Q10 2 20 12 T40 12" stroke="{AZURITE}" stroke-width="1.1" fill="none" opacity="0.45"/>
</pattern>
<pattern id="tile" width="18" height="12" patternUnits="userSpaceOnUse">
  <path d="M0 11 Q9 6 18 11" stroke="{DARK}" stroke-width="0.8" fill="none" opacity="0.55"/>
</pattern>
{defs}
</defs>
<rect width="{w}" height="{h}" fill="{PAPER}"/>
<rect width="{w}" height="{h}" fill="url(#fiber)"/>
<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="none" stroke="{CINNABAR}" stroke-width="1.1" opacity="0.35"/>
<rect x="17" y="17" width="{w-34}" height="{h-34}" fill="none" stroke="{GOLD}" stroke-width="0.6" opacity="0.4"/>
{body}
</svg>
'''


def cloud(x, y, s=1.0, fill=WHITE, edge=GOLD, op=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" opacity="{op}">
<path d="M0 0 C-2 -17 18 -27 33 -16 C40 -34 70 -34 80 -17 C98 -28 122 -17 119 0 C134 -2 141 12 132 19 L13 19 C-2 19 -10 10 0 0 Z"
 fill="{fill}" stroke="{edge}" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M8 12 C2 6 8 -2 17 0 C24 2 22 11 16 12 Z" fill="none" stroke="{edge}" stroke-width="1.1"/>
<path d="M116 12 C108 4 116 -5 124 1 C130 6 124 13 118 13 Z" fill="none" stroke="{edge}" stroke-width="1.1"/>
</g>'''


def mountain(x, y, w, h, fill=AZURITE, op=0.35):
    return f'''<path d="M{x} {y} C{x+w*0.12} {y-h*0.55} {x+w*0.2} {y-h*0.9} {x+w*0.32} {y-h}
 C{x+w*0.42} {y-h*0.78} {x+w*0.48} {y-h*0.52} {x+w*0.56} {y-h*0.62}
 C{x+w*0.68} {y-h*0.82} {x+w*0.76} {y-h*0.55} {x+w*0.86} {y-h*0.38}
 C{x+w*0.93} {y-h*0.24} {x+w*0.97} {y-h*0.1} {x+w} {y} Z"
 fill="{fill}" opacity="{op}"/>'''


def pine(x, y, s=1.0, trunk=OCHRE, leaf=MALACHITE):
    parts = [f'<g transform="translate({x},{y}) scale({s})">']
    parts.append(f'<path d="M0 0 C-3 -28 3 -55 0 -82" stroke="{trunk}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    for bx, by in [(-2, -78), (-16, -62), (14, -58), (-22, -42), (20, -38), (-6, -24)]:
        parts.append(f'<path d="M0 {by+8} C{bx*0.5} {by+2} {bx*0.8} {by-4} {bx} {by}" stroke="{trunk}" stroke-width="3" fill="none"/>')
        for k in range(3):
            yy = by - 7 + k * 7
            parts.append(f'<path d="M{bx-9+k*2} {yy} Q{bx} {yy-11} {bx+9-k*2} {yy}" stroke="{leaf}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    parts.append('</g>')
    return "".join(parts)


def roof(x, y, w, h, body=DARK, edge=GOLD):
    """庑殿顶正面：曲檐、正脊、瓦垄、鸱吻。"""
    p = []
    p.append(f'<path d="M{x+w*0.5} {y} L{x+w*0.7} {y} '
             f'C{x+w*0.76} {y+h*0.34} {x+w*0.89} {y+h*0.72} {x+w} {y+h*0.86} '
             f'Q{x+w*1.005} {y+h*0.99} {x+w*0.955} {y+h*0.96} '
             f'L{x+w*0.045} {y+h*0.96} Q{x-w*0.005} {y+h*0.99} {x} {y+h*0.86} '
             f'C{x+w*0.11} {y+h*0.72} {x+w*0.24} {y+h*0.34} {x+w*0.3} {y} Z" '
             f'fill="{body}" stroke="{INK}" stroke-width="1.4"/>')
    p.append(f'<path d="M{x+w*0.3} {y} L{x+w*0.7} {y}" stroke="{edge}" stroke-width="3"/>')
    p.append(f'<rect x="{x+w*0.27}" y="{y-4}" width="{w*0.46}" height="6" fill="{body}" stroke="{edge}" stroke-width="0.8"/>')
    for i in range(1, 11):
        t = i / 11
        p.append(f'<path d="M{x+w*(0.3+0.4*t)} {y+4} C{x+w*(0.28+0.44*t)} {y+h*0.4} '
                 f'{x+w*(0.24+0.52*t)} {y+h*0.7} {x+w*(0.2+0.6*t)} {y+h*0.92}" '
                 f'stroke="{INK}" stroke-width="1" fill="none" opacity="0.7"/>')
    p.append(f'<path d="M{x+w*0.045} {y+h*0.96} L{x+w*0.955} {y+h*0.96}" stroke="{edge}" stroke-width="2.2"/>')
    p.append(f'<path d="M{x+w*0.3} {y-2} C{x+w*0.28} {y-14} {x+w*0.33} {y-20} {x+w*0.35} {y-9} '
             f'C{x+w*0.36} {y-3} {x+w*0.33} {y+2} {x+w*0.3} {y-2} Z" fill="{body}" stroke="{edge}" stroke-width="0.9"/>')
    p.append(f'<path d="M{x+w*0.7} {y-2} C{x+w*0.72} {y-14} {x+w*0.67} {y-20} {x+w*0.65} {y-9} '
             f'C{x+w*0.64} {y-3} {x+w*0.67} {y+2} {x+w*0.7} {y-2} Z" fill="{body}" stroke="{edge}" stroke-width="0.9"/>')
    for xx in (x + w * 0.06, x + w * 0.94):
        p.append(f'<circle cx="{xx}" cy="{y+h*0.99}" r="3.2" fill="{GAMBOGE}" stroke="{INK}" stroke-width="0.8"/>')
        p.append(f'<path d="M{xx} {y+h*0.99+3} L{xx-2} {y+h*0.99+11} M{xx} {y+h*0.99+3} L{xx+2} {y+h*0.99+11}" stroke="{INK}" stroke-width="0.8"/>')
    return "".join(p)


def dougong(x, y, w, body=OCHRE, edge=GOLD):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="5" fill="{body}" stroke="{INK}" stroke-width="0.8"/>']
    n = max(3, int(w // 18))
    for i in range(n):
        bx = x + 6 + i * (w - 12) / max(1, n - 1)
        p.append(f'<rect x="{bx-3}" y="{y+5}" width="6" height="6" fill="{body}" stroke="{edge}" stroke-width="0.7"/>')
        p.append(f'<rect x="{bx-7}" y="{y+11}" width="14" height="4" fill="{body}" stroke="{INK}" stroke-width="0.7"/>')
    return "".join(p)


def lattice(x, y, w, h, fill=DARK, bar=GOLD):
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{bar}" stroke-width="1.2"/>']
    for i in range(1, 4):
        p.append(f'<path d="M{x+w*i/4} {y} L{x+w*i/4} {y+h}" stroke="{bar}" stroke-width="0.8" opacity="0.8"/>')
    for j in range(1, 4):
        p.append(f'<path d="M{x} {y+h*j/4} L{x+w} {y+h*j/4}" stroke="{bar}" stroke-width="0.8" opacity="0.8"/>')
    p.append(f'<path d="M{x+w*0.5} {y+h*0.18} L{x+w*0.82} {y+h*0.5} L{x+w*0.5} {y+h*0.82} L{x+w*0.18} {y+h*0.5} Z" '
             f'fill="none" stroke="{bar}" stroke-width="0.9" opacity="0.7"/>')
    return "".join(p)


def railing(x, y, w, color=GOLD):
    p = [f'<path d="M{x} {y} L{x+w} {y}" stroke="{color}" stroke-width="2"/>',
         f'<path d="M{x} {y+7} L{x+w} {y+7}" stroke="{color}" stroke-width="1.2" opacity="0.8"/>']
    n = max(3, int(w // 14))
    for i in range(n + 1):
        xx = x + i * w / n
        p.append(f'<path d="M{xx} {y-2} L{xx} {y+8}" stroke="{color}" stroke-width="1.1"/>')
    return "".join(p)


def armillary(cx, cy, r=30):
    p = [f'<g transform="translate({cx},{cy})">']
    p.append(f'<circle r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.2"/>')
    p.append(f'<ellipse rx="{r}" ry="{r*0.38}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    p.append(f'<ellipse rx="{r*0.38}" ry="{r}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    p.append(f'<path d="M-{r*1.25} 0 L{r*1.25} 0 M0 -{r*1.25} L0 {r*1.25}" stroke="{GOLD}" stroke-width="1.1" opacity="0.7"/>')
    p.append(f'<circle r="4.5" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.8"/>')
    p.append('</g>')
    return "".join(p)


def pagoda(cx, base_y, tiers=9, base_w=300, tier_h=44):
    p = []
    p.append(f'<path d="M{cx-base_w*0.78} {base_y+6} L{cx+base_w*0.78} {base_y+6} L{cx+base_w*0.86} {base_y+26} L{cx-base_w*0.86} {base_y+26} Z" fill="#d9c9a8" stroke="{OCHRE}" stroke-width="1.4"/>')
    p.append(f'<path d="M{cx-base_w*0.72} {base_y+6} L{cx+base_w*0.72} {base_y+6}" stroke="{GOLD}" stroke-width="1"/>')
    for i in range(7):
        p.append(f'<path d="M{cx-base_w*0.7+i*base_w*0.1} {base_y+26} L{cx-base_w*0.7+i*base_w*0.1} {base_y+34}" stroke="{OCHRE}" stroke-width="1"/>')
    p.append(f'<path d="M{cx-base_w*0.2} {base_y+6} L{cx-base_w*0.2} {base_y-46} Q{cx} {base_y-62} {cx+base_w*0.2} {base_y-46} L{cx+base_w*0.2} {base_y+6} Z" fill="#3a2b22" stroke="{GOLD}" stroke-width="1.4"/>')
    p.append(f'<g transform="translate({cx},{base_y-18})">')
    for k in range(8):
        a = math.pi * 2 * k / 8
        p.append(f'<path d="M0 0 L{math.cos(a)*26} {math.sin(a)*13}" stroke="{GOLD}" stroke-width="1.1" opacity="0.8"/>')
    p.append(f'<ellipse rx="26" ry="13" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    p.append(f'<ellipse rx="14" ry="7" fill="none" stroke="{GAMBOGE}" stroke-width="1.2"/>')
    p.append(f'<circle r="3.5" fill="{CINNABAR}"/>')
    p.append('</g>')
    for i in range(tiers):
        w = base_w * (1 - i * 0.062)
        y = base_y - 34 - i * tier_h
        body_h = 22
        roof_h = 20
        p.append(f'<rect x="{cx-w*0.34}" y="{y-body_h}" width="{w*0.68}" height="{body_h}" fill="{WHITE}" stroke="{OCHRE}" stroke-width="1"/>')
        p.append(f'<rect x="{cx-w*0.36}" y="{y-body_h}" width="5" height="{body_h}" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.6"/>')
        p.append(f'<rect x="{cx+w*0.36-5}" y="{y-body_h}" width="5" height="{body_h}" fill="{CINNABAR}" stroke="{INK}" stroke-width="0.6"/>')
        p.append(lattice(cx-w*0.16, y-body_h+4, w*0.32, body_h-8))
        p.append(railing(cx-w*0.42, y, w*0.84))
        p.append(dougong(cx-w*0.44, y-body_h-6, w*0.88))
        p.append(roof(cx-w*0.62, y-body_h-roof_h-7, w*1.24, roof_h))
    top_y = base_y - 34 - (tiers-1)*tier_h - 40
    p.append(f'<path d="M{cx-10} {top_y+10} L{cx} {top_y-28} L{cx+10} {top_y+10} Z" fill="{GOLD}" stroke="{INK}" stroke-width="1"/>')
    p.append(f'<circle cx="{cx}" cy="{top_y-32}" r="4" fill="{CINNABAR}" stroke="{GOLD}" stroke-width="1"/>')
    p.append(armillary(cx, top_y-62, 27))
    p.append(f'<rect x="{cx-38}" y="{base_y-34-8*tier_h-34}" width="76" height="30" fill="{AZURITE}" stroke="{GOLD}" stroke-width="1.4"/>')
    p.append(f'<text x="{cx}" y="{base_y-34-8*tier_h-13}" font-family="{KAI}" font-size="20" fill="{GOLD}" text-anchor="middle" letter-spacing="3">天枢</text>')
    return "".join(p)


def palm_leaf(x, y, w, h, angle=0, fill="#e8d6b0", seal_char=""):
    p = [f'<g transform="translate({x},{y}) rotate({angle})">']
    p.append(f'<path d="M0 0 Q{w*0.5} {-h} {w} 0 Q{w*0.5} {h} 0 0 Z" fill="{fill}" stroke="{OCHRE}" stroke-width="2"/>')
    p.append(f'<path d="M6 0 Q{w*0.5} 0 {w-6} 0" stroke="{OCHRE}" stroke-width="1.2" opacity="0.8"/>')
    for i in range(1, 8):
        t = i / 8
        p.append(f'<path d="M{w*t} 0 Q{w*(t+0.02)} {-h*0.38*(1-t)*2} {w*(t+0.08)} {-h*0.46*(1-t)*2}" stroke="{OCHRE}" stroke-width="0.8" fill="none" opacity="0.6"/>')
        p.append(f'<path d="M{w*t} 0 Q{w*(t+0.02)} {h*0.38*(1-t)*2} {w*(t+0.08)} {h*0.46*(1-t)*2}" stroke="{OCHRE}" stroke-width="0.8" fill="none" opacity="0.6"/>')
    p.append(f'<circle cx="{w*0.12}" cy="0" r="2" fill="{PAPER}" stroke="{OCHRE}" stroke-width="0.6"/>')
    p.append(f'<circle cx="{w*0.88}" cy="0" r="2" fill="{PAPER}" stroke="{OCHRE}" stroke-width="0.6"/>')
    if seal_char:
        p.append(seal(w*0.68, -h*0.22, h*0.42, CINNABAR, seal_char, knob=False, angle=-8))
    p.append('</g>')
    return "".join(p)


def flame(x, y, s=1.0, fill=CINNABAR, inner=GAMBOGE):
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(f'<path d="M0 0 C-16 -18 -8 -38 2 -52 C-4 -34 10 -38 12 -52 C26 -34 24 -12 14 0 Z" fill="{fill}" stroke="{DARK}" stroke-width="1.2"/>')
    p.append(f'<path d="M3 -6 C-4 -18 1 -30 7 -38 C4 -26 13 -26 13 -34 C18 -22 16 -10 10 -4 Z" fill="{inner}" opacity="0.95"/>')
    p.append('</g>')
    return "".join(p)


def seal(x, y, s, fill=CINNABAR, char="", knob=True, angle=0):
    """旧式印章：保留给经文、阵图等小装饰。"""
    p = [f'<g transform="translate({x},{y}) rotate({angle})">']
    if knob:
        p.append(f'<path d="M{-s*0.22} 0 C{-s*0.22} {-s*0.28} {-s*0.12} {-s*0.36} 0 {-s*0.36} '
                 f'C{s*0.12} {-s*0.36} {s*0.22} {-s*0.28} {s*0.22} 0 Z" fill="{fill}" stroke="{GOLD}" stroke-width="1.6"/>')
        p.append(f'<path d="M{-s*0.08} {-s*0.18} C{-s*0.02} {-s*0.26} {s*0.02} {-s*0.26} {s*0.08} {-s*0.18}" stroke="{WHITE}" stroke-width="1.6" fill="none" opacity="0.8"/>')
    p.append(f'<rect x="{-s/2}" y="0" width="{s}" height="{s}" rx="{s*0.04}" fill="{fill}" stroke="{GOLD}" stroke-width="2"/>')
    p.append(f'<rect x="{-s/2+s*0.08}" y="{s*0.08}" width="{s*0.84}" height="{s*0.84}" fill="none" stroke="{WHITE}" stroke-width="1.4" opacity="0.85"/>')
    if char:
        p.append(f'<text x="0" y="{s*0.72}" font-family="{KAI}" font-size="{s*0.56}" fill="{WHITE}" text-anchor="middle" font-weight="600">{char}</text>')
    else:
        for i in range(4):
            yy = s * (0.24 + i * 0.16)
            p.append(f'<path d="M{-s*0.3} {yy} L{s*0.3} {yy} L{s*0.3} {yy+s*0.06} L{-s*0.3} {yy+s*0.06}" stroke="{WHITE}" stroke-width="2.4" fill="none" opacity="0.9"/>')
        p.append(f'<path d="M{-s*0.3} {s*0.24} L{-s*0.3} {s*0.78} M{s*0.3} {s*0.24} L{s*0.3} {s*0.78}" stroke="{WHITE}" stroke-width="2.4" opacity="0.9"/>')
    p.append('</g>')
    return "".join(p)


def ring(x, y, r, color=GOLD, w=3.0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>'


def tassel(x, y, length=26, color=CINNABAR, s=1.0):
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(f'<path d="M0 0 L0 7" stroke="{color}" stroke-width="2"/>')
    p.append(f'<circle cx="0" cy="10" r="4.5" fill="{color}" stroke="{GOLD}" stroke-width="0.8"/>')
    for dx in (-7, -3.5, 0, 3.5, 7):
        p.append(f'<path d="M0 14 C{dx*0.4} {length*0.55} {dx*0.8} {length*0.8} {dx} {length}" stroke="{color}" stroke-width="1.6" fill="none" opacity="0.9"/>')
    p.append('</g>')
    return "".join(p)


def seal_script(cx, cy, s):
    """印面九叠篆：回环折线，远看是一枚真印，近看不是字。"""
    p = []
    cell = s * 0.36
    for qi, (qx, qy) in enumerate([(-0.21, -0.21), (0.21, -0.21), (-0.21, 0.21), (0.21, 0.21)]):
        x0, y0 = cx + qx * s, cy + qy * s
        xl, xr = x0 - cell / 2, x0 + cell / 2
        yt, yb = y0 - cell / 2, y0 + cell / 2
        # 每条横线在不同端回折，形成九叠篆的回环
        for k in range(5):
            yy = yt + k * cell / 4
            if (k + qi) % 2 == 0:
                p.append(f'<path d="M{xl} {yy} L{xr} {yy} L{xr} {yy+cell*0.11} L{xl+cell*0.12} {yy+cell*0.11}" stroke="{WHITE}" stroke-width="{s*0.035}" fill="none" opacity="0.95"/>')
            else:
                p.append(f'<path d="M{xr} {yy} L{xl} {yy} L{xl} {yy+cell*0.11} L{xr-cell*0.12} {yy+cell*0.11}" stroke="{WHITE}" stroke-width="{s*0.035}" fill="none" opacity="0.95"/>')
        # 竖向骨架，位置交错
        vx = xl + cell * (0.16 + 0.2 * (qi % 2))
        p.append(f'<path d="M{vx} {yt-cell*0.02} L{vx} {yb+cell*0.02}" stroke="{WHITE}" stroke-width="{s*0.03}" opacity="0.75"/>')
        vx2 = xr - cell * (0.12 + 0.16 * ((qi + 1) % 2))
        p.append(f'<path d="M{vx2} {yb} L{vx2} {yt+cell*0.18}" stroke="{WHITE}" stroke-width="{s*0.03}" opacity="0.7"/>')
    return "".join(p)


def jade_seal(cx, cy, s, jade="#7fa58c", cracked=False, tassel_on=False, angle=0):
    """螭虎钮玉玺。cy 是印身中心。"""
    top = -s / 2
    p = [f'<g transform="translate({cx},{cy}) rotate({angle})">']
    p.append(ring(0, top - s * 0.64, s * 0.075, GOLD, s * 0.05))
    p.append(f'<path d="M{-s*0.34} {top} C{-s*0.42} {top-s*0.30} {-s*0.26} {top-s*0.50} {-s*0.04} {top-s*0.40} '
             f'C{s*0.16} {top-s*0.50} {s*0.36} {top-s*0.30} {s*0.30} {top} Z" fill="{jade}" stroke="{GOLD}" stroke-width="1.6"/>')
    p.append(f'<path d="M{-s*0.26} {top-s*0.30} C{-s*0.42} {top-s*0.36} {-s*0.44} {top-s*0.16} {-s*0.30} {top-s*0.12} '
             f'C{-s*0.24} {top-s*0.10} {-s*0.20} {top-s*0.20} {-s*0.24} {top-s*0.26} Z" fill="{jade}" stroke="{GOLD}" stroke-width="1.3"/>')
    p.append(f'<path d="M{s*0.24} {top-s*0.26} C{s*0.38} {top-s*0.24} {s*0.40} {top-s*0.06} {s*0.28} {top-s*0.04}" stroke="{GOLD}" stroke-width="1.4" fill="none"/>')
    p.append(f'<path d="M{s*0.28} {top-s*0.05} C{s*0.44} {top-s*0.10} {s*0.46} {top-s*0.26} {s*0.36} {top-s*0.28}" stroke="{GOLD}" stroke-width="1.5" fill="none"/>')
    p.append(f'<ellipse cx="{-s*0.17}" cy="{top-s*0.015}" rx="{s*0.055}" ry="{s*0.028}" fill="{jade}" stroke="{GOLD}" stroke-width="1"/>')
    p.append(f'<ellipse cx="{s*0.15}" cy="{top-s*0.015}" rx="{s*0.055}" ry="{s*0.028}" fill="{jade}" stroke="{GOLD}" stroke-width="1"/>')
    p.append(f'<path d="M{-s*0.12} {top-s*0.38} C{-s*0.02} {top-s*0.44} {s*0.08} {top-s*0.40} {s*0.16} {top-s*0.32}" stroke="{WHITE}" stroke-width="1.1" fill="none" opacity="0.55"/>')
    p.append(f'<circle cx="{-s*0.34}" cy="{top-s*0.19}" r="{s*0.025}" fill="{INK}"/>')
    p.append(f'<rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" rx="{s*0.03}" fill="{jade}" stroke="{GOLD}" stroke-width="2.2"/>')
    p.append(f'<path d="M{-s/2+4} {-s/2+2} L{s/2-4} {-s/2+2} L{s/2-4} {-s/2+5} L{-s/2+4} {-s/2+5} Z" fill="{WHITE}" opacity="0.35"/>')
    p.append(f'<rect x="{-s/2+s*0.07}" y="{-s/2+s*0.07}" width="{s*0.86}" height="{s*0.86}" fill="none" stroke="{WHITE}" stroke-width="1.3" opacity="0.55"/>')
    p.append(seal_script(0, 0, s))
    if cracked:
        p.append(f'<path d="M{-s*0.08} {-s*0.5} L{s*0.02} {-s*0.16} L{-s*0.10} {s*0.10} L{s*0.03} {s*0.5}" stroke="{INK}" stroke-width="2.4" fill="none"/>')
        p.append(f'<path d="M{s*0.5} {s*0.06} L{s*0.42} {s*0.10} L{s*0.46} {s*0.20} L{s*0.38} {s*0.24}" stroke="{INK}" stroke-width="1.8" fill="none"/>')
        p.append(f'<path d="M{s*0.5} {s*0.06} L{s*0.42} {s*0.10} L{s*0.46} {s*0.20} L{s*0.5} {s*0.19} Z" fill="{PAPER}"/>')
    if tassel_on:
        p.append(tassel(0, s / 2 + 2, 38, CINNABAR, 1.25))
    p.append('</g>')
    return "".join(p)


def chain_run(points, step=15, color=GOLD):
    """沿着折线铺金链，链环交替横竖。"""
    p = [f'<path d="M' + " L".join(f"{x} {y}" for x, y in points) + f'" stroke="{color}" stroke-width="2.2" fill="none" opacity="0.9"/>']
    segs = []
    total = 0
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        segs.append((x1, y1, x2, y2, L))
        total += L
    n = max(1, int(total // step))
    for i in range(n):
        t = (i + 0.5) / n * total
        acc = 0
        for x1, y1, x2, y2, L in segs:
            if acc + L >= t:
                u = (t - acc) / L
                x = x1 + (x2 - x1) * u
                y = y1 + (y2 - y1) * u
                ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
                rx, ry = (7, 4) if i % 2 == 0 else (4, 7)
                p.append(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx}" ry="{ry}" fill="none" stroke="{GAMBOGE}" stroke-width="1.8" transform="rotate({ang:.1f} {x:.2f} {y:.2f})"/>')
                break
            acc += L
    return "".join(p)


def gear(cx, cy, r, teeth=16, fill=OCHRE, edge=GOLD):
    p = [f'<g transform="translate({cx},{cy})">']
    for i in range(teeth):
        a = 360 * i / teeth
        p.append(f'<rect x="-4" y="{-r-8}" width="8" height="10" fill="{fill}" stroke="{INK}" stroke-width="0.8" transform="rotate({a})"/>')
    p.append(f'<circle r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.8"/>')
    p.append(f'<circle r="{r*0.78}" fill="none" stroke="{edge}" stroke-width="1.4" opacity="0.9"/>')
    for i in range(6):
        a = math.pi * 2 * i / 6
        p.append(f'<path d="M0 0 L{math.cos(a)*r*0.76} {math.sin(a)*r*0.76}" stroke="{INK}" stroke-width="2" opacity="0.75"/>')
    p.append(f'<circle r="{r*0.18}" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    p.append(f'<circle r="{r*0.07}" fill="{INK}"/>')
    p.append('</g>')
    return "".join(p)


def waterwheel(cx, cy, r):
    p = [f'<g transform="translate({cx},{cy})">']
    p.append(f'<circle r="{r}" fill="none" stroke="{OCHRE}" stroke-width="9"/>')
    p.append(f'<circle r="{r-6}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.8"/>')
    p.append(f'<circle r="{r*0.2}" fill="{OCHRE}" stroke="{INK}" stroke-width="2"/>')
    for i in range(12):
        a = 360 * i / 12
        p.append(f'<path d="M0 0 L{math.cos(math.radians(a))*r} {math.sin(math.radians(a))*r}" stroke="{OCHRE}" stroke-width="4"/>')
    for i in range(16):
        a = 360 * i / 16
        p.append(f'<rect x="-5" y="{-r-9}" width="10" height="18" fill="{OCHRE}" stroke="{INK}" stroke-width="0.9" transform="rotate({a})"/>')
    p.append(f'<circle r="{r*0.1}" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    p.append('</g>')
    return "".join(p)


def robe_figure(x, y, s=1.0, fill=DARK, edge=GOLD, hat=True):
    """背影片影：宽袖、袍摆、幞头。y 为脚底。"""
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(f'<path d="M-14 0 C-13 -20 -11 -32 -9 -42 L9 -42 C11 -32 13 -20 14 0 Z" fill="{fill}" stroke="{edge}" stroke-width="0.9"/>')
    p.append(f'<path d="M-9 -42 C-20 -38 -24 -26 -22 -12 L-14 -14 L-10 -30 Z" fill="{fill}" stroke="{edge}" stroke-width="0.8" opacity="0.95"/>')
    p.append(f'<path d="M9 -42 C20 -38 24 -26 22 -12 L14 -14 L10 -30 Z" fill="{fill}" stroke="{edge}" stroke-width="0.8" opacity="0.95"/>')
    p.append(f'<circle cx="0" cy="-50" r="7" fill="{fill}" stroke="{edge}" stroke-width="0.9"/>')
    if hat:
        p.append(f'<path d="M-9 -54 L9 -54 L7 -62 L-7 -62 Z" fill="{fill}" stroke="{edge}" stroke-width="0.8"/>')
        p.append(f'<path d="M7 -58 L16 -54 L7 -52 Z" fill="{fill}" stroke="{edge}" stroke-width="0.7"/>')
    p.append('</g>')
    return "".join(p)


def fish_half(x, y, s=1.0, side=1, fill=GOLD, edge=OCHRE):
    """半片鱼符。side=1 右半，side=-1 左半。"""
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(f'<path d="M0 -13 C18 -18 32 -10 34 0 C32 10 18 18 0 13 L0 -13 Z" fill="{fill}" stroke="{edge}" stroke-width="1.6"/>')
    p.append(f'<path d="M34 0 C44 -9 54 -8 58 0 C54 8 44 9 34 0 Z" fill="{fill}" stroke="{edge}" stroke-width="1.6"/>')
    p.append(f'<circle cx="12" cy="-4" r="2.6" fill="{edge}"/>')
    for i in range(4):
        p.append(f'<path d="M{6+i*7} {-9+i*1.6} Q{10+i*7} 0 {6+i*7} {9-i*1.6}" stroke="{edge}" stroke-width="1" fill="none" opacity="0.65"/>')
    # 对缝
    p.append(f'<path d="M0 -13 L-4 -4 L2 2 L-3 8 L0 13" stroke="{edge}" stroke-width="1.4" fill="none"/>')
    p.append('</g>')
    return "".join(p)


def turtle(x, y, w, fill="#cdbb9b", edge=OCHRE):
    """赑屃：y 为壳顶，壳高约 52，头向左。"""
    p = [f'<g transform="translate({x},{y})">']
    # 壳
    p.append(f'<path d="M{-w*0.46} 44 C{-w*0.50} 12 {-w*0.28} 0 0 0 C{w*0.28} 0 {w*0.50} 12 {w*0.46} 44 Z" fill="{fill}" stroke="{edge}" stroke-width="2.2"/>')
    p.append(f'<path d="M{-w*0.46} 44 L{w*0.46} 44" stroke="{edge}" stroke-width="2"/>')
    # 龟甲纹
    p.append(f'<path d="M0 4 L{w*0.13} 14 L{w*0.11} 30 L0 39 L{-w*0.11} 30 L{-w*0.13} 14 Z" fill="none" stroke="{edge}" stroke-width="1.4" opacity="0.8"/>')
    for sx in (-0.34, -0.21, 0.21, 0.34):
        p.append(f'<path d="M{w*sx} 10 L{w*(sx*0.72)} 30 L{w*(sx*0.8)} 43" fill="none" stroke="{edge}" stroke-width="1.1" opacity="0.6"/>')
    p.append(f'<path d="M{-w*0.34} 44 L{-w*0.42} 36 M{w*0.34} 44 L{w*0.42} 36" stroke="{edge}" stroke-width="1.1" opacity="0.6"/>')
    # 头与颈
    p.append(f'<path d="M{-w*0.44} 26 C{-w*0.54} 24 {-w*0.58} 30 {-w*0.58} 36 C{-w*0.58} 42 {-w*0.52} 45 {-w*0.44} 43 Z" fill="{fill}" stroke="{edge}" stroke-width="2"/>')
    p.append(f'<ellipse cx="{-w*0.60}" cy="34" rx="{w*0.055}" ry="{w*0.038}" fill="{fill}" stroke="{edge}" stroke-width="1.6"/>')
    p.append(f'<circle cx="{-w*0.615}" cy="32.5" r="1.8" fill="{edge}"/>')
    p.append(f'<path d="M{-w*0.645} 38 L{-w*0.615} 39" stroke="{edge}" stroke-width="1.2"/>')
    # 四足
    for dx, flip in [(-0.34, 1), (0.30, -1)]:
        p.append(f'<path d="M{w*dx} 40 L{w*dx+flip*2} 56 L{w*dx+flip*10} 56 L{w*dx+flip*9} 40 Z" fill="{fill}" stroke="{edge}" stroke-width="1.6"/>')
        p.append(f'<path d="M{w*dx+flip*3} 56 L{w*dx+flip*3} 60 M{w*dx+flip*7} 56 L{w*dx+flip*7} 60" stroke="{edge}" stroke-width="1.2"/>')
    # 尾
    p.append(f'<path d="M{w*0.46} 34 C{w*0.54} 36 {w*0.56} 42 {w*0.50} 44" fill="none" stroke="{edge}" stroke-width="2.4"/>')
    p.append('</g>')
    return "".join(p)
