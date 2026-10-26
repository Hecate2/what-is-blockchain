#!/usr/bin/env python3
"""后三图：照妖镜门、三钥、金匮火。

这三图都靠建筑与器物撑住画面，人形只作远景剪影，避免火柴人。
"""
import math

from svgkit import (
    PAPER, INK, CINNABAR, AZURITE, MALACHITE, GAMBOGE, OCHRE, WHITE, GOLD,
    STEEL, DARK, KAI, svg, cloud, mountain, pine, roof, dougong, lattice,
    railing, armillary, flame, seal, tassel, jade_seal, gear, robe_figure,
)


def _poly(pts, fill="none", stroke=INK, sw=1.0, op=1.0):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{op}"/>')


def _lantern(x, y, s=1.0, body=CINNABAR):
    """宫灯：y 为挂绳起点。"""
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(f'<path d="M0 0 L0 12" stroke="{OCHRE}" stroke-width="2"/>')
    p.append(f'<rect x="-13" y="12" width="26" height="6" fill="{GOLD}" stroke="{OCHRE}" stroke-width="0.9"/>')
    p.append(f'<path d="M-13 18 C-22 28 -22 44 -13 52 L13 52 C22 44 22 28 13 18 Z" fill="{body}" stroke="{OCHRE}" stroke-width="1.4"/>')
    for i in range(4):
        p.append(f'<path d="M{-14+i*9.4} 22 C{-17+i*9.4} 33 {-17+i*9.4} 42 {-14+i*9.4} 50" stroke="#7d201a" stroke-width="1" fill="none" opacity="0.7"/>')
    p.append(f'<rect x="-13" y="52" width="26" height="5" fill="{GOLD}" stroke="{OCHRE}" stroke-width="0.9"/>')
    p.append(f'<path d="M-4 57 L-4 64 M4 57 L4 64" stroke="{OCHRE}" stroke-width="1.4"/>')
    p.append(f'<path d="M-2 64 C-8 70 -8 78 -2 82 M2 64 C8 70 8 78 2 82" stroke="{CINNABAR}" stroke-width="2.4" fill="none"/>')
    p.append('</g>')
    return "".join(p)


def _censer(x, y, s=1.0):
    """三足小香炉，y 为足底。"""
    p = [f'<g transform="translate({x},{y}) scale({s})">']
    p.append(f'<path d="M-18 -22 C-18 -32 -10 -38 0 -38 C10 -38 18 -32 18 -22 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.2"/>')
    p.append(f'<path d="M-20 -22 L20 -22" stroke="{GOLD}" stroke-width="2.2"/>')
    p.append(f'<path d="M-14 -16 C-14 -6 -8 0 0 0 C8 0 14 -6 14 -16 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.2"/>')
    p.append(f'<path d="M-8 -8 C-4 -12 4 -12 8 -8" stroke="{GOLD}" stroke-width="1" fill="none"/>')
    for dx in (-11, 0, 11):
        p.append(f'<path d="M{dx} 0 L{dx*1.25} 5" stroke="{INK}" stroke-width="2"/>')
    p.append(f'<path d="M-18 -28 C-26 -26 -26 -18 -20 -18" stroke="{GOLD}" stroke-width="1.8" fill="none"/>')
    p.append(f'<path d="M18 -28 C26 -26 26 -18 20 -18" stroke="{GOLD}" stroke-width="1.8" fill="none"/>')
    p.append('</g>')
    return "".join(p)


def _padlock(cx, cy, s=1.0, body=GAMBOGE):
    """铜锁：锁梁、锁体、匙孔。"""
    p = [f'<g transform="translate({cx},{cy}) scale({s})">']
    p.append(f'<path d="M-6 -4 C-6 -14 6 -14 6 -4" fill="none" stroke="{GOLD}" stroke-width="2.4"/>')
    p.append(f'<rect x="-9" y="-4" width="18" height="15" rx="2" fill="{body}" stroke="{OCHRE}" stroke-width="1.1"/>')
    p.append(f'<circle cx="0" cy="1.5" r="1.7" fill="{DARK}"/>')
    p.append(f'<path d="M0 3 L0 7" stroke="{DARK}" stroke-width="1.4"/>')
    p.append('</g>')
    return "".join(p)


# ---------------- 图 10：照妖镜门 ----------------
def fig10():
    W, H = 720, 560
    defs = '''<linearGradient id="f10sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#34433f"/><stop offset="0.5" stop-color="#1f2b28"/><stop offset="1" stop-color="#121917"/></linearGradient>
<linearGradient id="f10wall" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#3c2a21"/><stop offset="1" stop-color="#241813"/></linearGradient>
<linearGradient id="f10door" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#34241c"/><stop offset="1" stop-color="#1a1210"/></linearGradient>
<linearGradient id="f10mir" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#8aa892"/><stop offset="0.45" stop-color="#547260"/><stop offset="1" stop-color="#2b4034"/></linearGradient>
<radialGradient id="f10glow" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#d9a441" stop-opacity="0.42"/><stop offset="1" stop-color="#d9a441" stop-opacity="0"/></radialGradient>
<radialGradient id="f10vig" cx="0.5" cy="0.42" r="0.72">
<stop offset="0.52" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="0.38"/></radialGradient>
<clipPath id="f10mirclip"><circle cx="360" cy="352" r="76"/></clipPath>'''

    b = []
    # 夜空与月
    b.append(f'<rect x="40" y="40" width="640" height="462" fill="url(#f10sky)"/>')
    b.append(f'<circle cx="560" cy="108" r="58" fill="url(#f10glow)"/>')
    b.append(f'<circle cx="560" cy="108" r="32" fill="#efe7d0" opacity="0.92"/>')
    b.append(f'<path d="M498 116 C516 110 530 112 542 118 M548 126 C564 120 582 122 596 128" stroke="#2a3733" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.9"/>')
    b.append(cloud(66, 92, 0.62, "#2b3834", "#54645a", 0.9))
    b.append(cloud(430, 66, 0.5, "#2b3834", "#4c5a51", 0.7))
    # 远山
    b.append(mountain(-70, 462, 260, 96, "#1e2a26", 0.7))
    b.append(mountain(420, 464, 330, 110, "#182320", 0.65))
    # 地面
    b.append(f'<rect x="40" y="470" width="640" height="32" fill="#161d1b"/>')
    for yy in (482, 494):
        b.append(f'<path d="M40 {yy} L680 {yy}" stroke="#28352d" stroke-width="1" opacity="0.9"/>')
    for x0 in range(90, 680, 96):
        b.append(f'<path d="M{x0} 470 L{x0-14} 502" stroke="#232f28" stroke-width="1" opacity="0.7"/>')
    # 台基与三级石阶
    b.append(f'<path d="M140 430 L580 430 L580 454 L140 454 Z" fill="#545b4c" stroke="{OCHRE}" stroke-width="1.4"/>')
    b.append(f'<path d="M140 430 L580 430" stroke="{GOLD}" stroke-width="1.2" opacity="0.6"/>')
    for i, (x0, w0, y0) in enumerate([(124, 472, 454), (104, 512, 468), (84, 552, 482)]):
        b.append(f'<rect x="{x0}" y="{y0}" width="{w0}" height="14" fill="#5c6354" stroke="#2a3029" stroke-width="1"/>')
        b.append(f'<path d="M{x0+6} {y0} L{x0+w0-6} {y0}" stroke="#7c8371" stroke-width="1.4" opacity="0.8"/>')
        b.append(f'<path d="M{x0} {y0+14} L{x0+w0} {y0+14}" stroke="#1a2018" stroke-width="2" opacity="0.8"/>')
    # 墙体
    b.append(f'<rect x="120" y="252" width="480" height="180" fill="url(#f10wall)" stroke="{OCHRE}" stroke-width="1.2"/>')
    for x0 in (128, 538):
        b.append(f'<rect x="{x0}" y="278" width="54" height="122" fill="{DARK}" stroke="{OCHRE}" stroke-width="1.4"/>')
        for i in range(1, 4):
            b.append(f'<path d="M{x0} {278+122*i/4} L{x0+54} {278+122*i/4}" stroke="{GOLD}" stroke-width="0.9" opacity="0.65"/>')
        for i in range(1, 3):
            b.append(f'<path d="M{x0+54*i/3} 278 L{x0+54*i/3} 400" stroke="{GOLD}" stroke-width="0.9" opacity="0.65"/>')
    # 门楼
    b.append(roof(120, 150, 480, 62))
    b.append(dougong(150, 212, 420, OCHRE, GOLD))
    b.append(f'<rect x="300" y="224" width="120" height="26" fill="{DARK}" stroke="{GOLD}" stroke-width="1.8"/>')
    b.append(f'<text x="360" y="244" font-family="{KAI}" font-size="18" fill="{GOLD}" text-anchor="middle" letter-spacing="6">天枢</text>')
    # 立柱
    for x0 in (190, 510):
        b.append(f'<rect x="{x0}" y="252" width="20" height="178" fill="{CINNABAR}" stroke="{OCHRE}" stroke-width="1.2"/>')
        b.append(f'<rect x="{x0-3}" y="248" width="26" height="7" fill="{GOLD}" stroke="{OCHRE}" stroke-width="0.8"/>')
        b.append(f'<rect x="{x0-3}" y="426" width="26" height="8" fill="{GOLD}" stroke="{OCHRE}" stroke-width="0.8"/>')
        b.append(f'<path d="M{x0+7} 258 L{x0+7} 424" stroke="#c25a48" stroke-width="2" opacity="0.55"/>')
    # 门框与门扇
    b.append(f'<rect x="232" y="258" width="256" height="176" fill="#4a2f22" stroke="{GOLD}" stroke-width="2"/>')
    for x0 in (240, 368):
        b.append(f'<rect x="{x0}" y="266" width="120" height="160" fill="url(#f10door)" stroke="{OCHRE}" stroke-width="1.2"/>')
        for i in range(4):
            for j in range(5):
                b.append(f'<circle cx="{x0+18+i*28}" cy="{280+j*30}" r="2.6" fill="{GOLD}" opacity="0.8"/>')
    b.append(f'<rect x="360" y="266" width="8" height="160" fill="{GOLD}" opacity="0.9"/>')
    b.append(f'<rect x="356" y="266" width="16" height="160" fill="url(#f10glow)" opacity="0.5"/>')
    # 宫灯
    b.append(_lantern(222, 258, 0.92))
    b.append(_lantern(498, 258, 0.92))
    # 石灯笼与松
    b.append(pine(92, 492, 1.05))
    b.append(pine(640, 490, 0.92))
    b.append(f'<rect x="596" y="500" width="34" height="8" fill="#4a5045" stroke="{OCHRE}" stroke-width="1"/>')
    b.append(f'<rect x="606" y="470" width="14" height="30" fill="#4a5045" stroke="{OCHRE}" stroke-width="1"/>')
    b.append(f'<rect x="598" y="456" width="30" height="18" fill="#4a5045" stroke="{OCHRE}" stroke-width="1"/>')
    b.append(f'<rect x="604" y="460" width="18" height="10" fill="{GAMBOGE}" opacity="0.75"/>')
    b.append(f'<path d="M594 456 L613 442 L632 456 Z" fill="#3a4038" stroke="{OCHRE}" stroke-width="1"/>')
    # 镜架
    b.append(f'<path d="M320 492 L400 492 L392 478 L328 478 Z" fill="#43301f" stroke="{GOLD}" stroke-width="1.4"/>')
    b.append(f'<rect x="352" y="436" width="16" height="44" fill="#43301f" stroke="{GOLD}" stroke-width="1.2"/>')
    b.append(f'<path d="M324 470 C310 440 302 412 306 392" stroke="#43301f" stroke-width="9" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M396 470 C410 440 418 412 414 392" stroke="#43301f" stroke-width="9" fill="none" stroke-linecap="round"/>')
    b.append(f'<circle cx="360" cy="352" r="128" fill="url(#f10glow)" opacity="0.7"/>')
    # 镜背与镜面
    b.append(f'<circle cx="360" cy="352" r="88" fill="#6a5126" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<circle cx="360" cy="352" r="82" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    b.append(f'<circle cx="360" cy="352" r="76" fill="url(#f10mir)" stroke="#3a2c14" stroke-width="1.2"/>')
    # 镜中：门内一影
    b.append(f'<g clip-path="url(#f10mirclip)">')
    b.append(f'<rect x="284" y="276" width="152" height="152" fill="#1b2721"/>')
    b.append(f'<rect x="326" y="288" width="56" height="142" fill="#6b4a24" opacity="0.9"/>')
    b.append(f'<rect x="332" y="296" width="44" height="132" fill="#a57a3c" opacity="0.55"/>')
    for i in range(3):
        b.append(f'<path d="M332 {300+i*10} L376 {300+i*10}" stroke="#4a3018" stroke-width="1.6" opacity="0.8"/>')
    b.append(f'<path d="M326 288 L326 428 M382 288 L382 428" stroke="#2a1d0f" stroke-width="2.4"/>')
    b.append(f'<path d="M284 410 C320 398 400 398 436 410 L436 428 L284 428 Z" fill="#243128"/>')
    b.append(f'<ellipse cx="350" cy="414" rx="54" ry="9" fill="#c99a4e" opacity="0.22"/>')
    # 案、账簿、笔、灯
    b.append(f'<rect x="290" y="390" width="70" height="7" fill="#4a3322" stroke="{OCHRE}" stroke-width="0.8"/>')
    b.append(f'<path d="M294 397 L294 412 M356 397 L356 412" stroke="#33220f" stroke-width="3"/>')
    b.append(f'<path d="M302 386 L338 384 L340 391 L304 393 Z" fill="#e6d9b8" stroke="{OCHRE}" stroke-width="0.8"/>')
    b.append(f'<path d="M306 388 L334 387 M306 390 L334 389" stroke="#7c705a" stroke-width="0.7"/>')
    b.append(f'<path d="M344 384 L362 376" stroke="#2a211a" stroke-width="2"/>')
    b.append(f'<circle cx="316" cy="378" r="9" fill="url(#f10glow)" opacity="0.8"/>')
    b.append(f'<path d="M310 386 L310 380 Q316 372 322 380 L322 386 Z" fill="{GAMBOGE}" opacity="0.8"/>')
    b.append(robe_figure(396, 412, 1.2, "#15110f", "#c9a24a", True))
    b.append(f'<path d="M318 296 C346 288 370 290 394 298" stroke="#d9c79b" stroke-width="1.2" fill="none" opacity="0.28"/>')
    b.append(f'<path d="M292 330 C306 318 312 316 322 318" stroke="#f6efdd" stroke-width="3" fill="none" opacity="0.2"/>')
    b.append(f'<circle cx="410" cy="300" r="2.2" fill="#f6efdd" opacity="0.4"/>')
    b.append('</g>')
    # 镜钮与流苏
    b.append(f'<circle cx="360" cy="266" r="7.5" fill="{GOLD}" stroke="{OCHRE}" stroke-width="1.2"/>')
    b.append(f'<path d="M352 262 C356 258 364 258 368 262" stroke="#f0cf8e" stroke-width="1.4" fill="none"/>')
    # 镜面反光
    b.append(f'<path d="M314 316 C330 294 356 282 382 284" stroke="{WHITE}" stroke-width="2.4" fill="none" opacity="0.22"/>')
    # 阶前落叶
    for x, y, a in [(168, 508, -24), (552, 512, 18), (486, 500, 40)]:
        b.append(f'<path d="M{x} {y} C{x+7} {y-5} {x+13} {y-2} {x+15} {y+3} C{x+8} {y+6} {x+2} {y+5} {x} {y} Z" fill="{OCHRE}" opacity="0.65" transform="rotate({a} {x} {y})"/>')
    # 暗角
    b.append(f'<rect x="40" y="40" width="640" height="462" fill="url(#f10vig)"/>')
    return svg(W, H, "".join(b), defs)


# ---------------- 图 11：三钥 ----------------
def fig11():
    W, H = 720, 520
    defs = '''<linearGradient id="f11wall" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#efe5cf"/><stop offset="1" stop-color="#ded0b4"/></linearGradient>
<linearGradient id="f11night" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#31443f"/><stop offset="0.55" stop-color="#1d2c28"/><stop offset="1" stop-color="#101917"/></linearGradient>
<linearGradient id="f11lac" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#4a2c1e"/><stop offset="1" stop-color="#2a1711"/></linearGradient>
<linearGradient id="f11jade" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#a9c6ae"/><stop offset="0.5" stop-color="#7fa58c"/><stop offset="1" stop-color="#5d8569"/></linearGradient>
<radialGradient id="f11moon" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#efe6cf" stop-opacity="0.5"/><stop offset="1" stop-color="#efe6cf" stop-opacity="0"/></radialGradient>
<clipPath id="f11win"><circle cx="360" cy="186" r="112"/></clipPath>'''
    b = []
    b.append(f'<rect x="40" y="40" width="640" height="420" fill="url(#f11wall)"/>')
    b.append(f'<rect x="40" y="460" width="640" height="18" fill="#c9b795"/>')
    b.append(f'<path d="M40 460 L680 460" stroke="{OCHRE}" stroke-width="1.6" opacity="0.6"/>')
    # 月洞窗
    b.append(f'<circle cx="360" cy="186" r="134" fill="none" stroke="{OCHRE}" stroke-width="9"/>')
    b.append(f'<circle cx="360" cy="186" r="124" fill="none" stroke="{GOLD}" stroke-width="1.8"/>')
    b.append(f'<g clip-path="url(#f11win)">')
    b.append(f'<rect x="248" y="74" width="224" height="224" fill="url(#f11night)"/>')
    b.append(f'<circle cx="416" cy="140" r="46" fill="url(#f11moon)"/>')
    b.append(f'<circle cx="416" cy="140" r="21" fill="#efe7d0" opacity="0.9"/>')
    b.append(f'<path d="M380 150 C392 140 412 142 422 148 C434 138 452 142 460 150 C446 156 414 158 400 152 Z" fill="#22302c" opacity="0.85"/>')
    b.append(f'<path d="M248 260 C286 246 320 250 348 258 C380 266 416 264 472 248 L472 300 L248 300 Z" fill="#0e1614" opacity="0.9"/>')
    b.append(armillary(360, 202, 52))
    b.append(f'<path d="M282 268 L438 268" stroke="{GOLD}" stroke-width="2" opacity="0.5"/>')
    b.append(f'<path d="M292 268 L292 258 M316 268 L316 258 M340 268 L340 258 M364 268 L364 258 M388 268 L388 258 M412 268 L412 258 M430 268 L430 258" stroke="{GOLD}" stroke-width="1.2" opacity="0.5"/>')
    b.append('</g>')
    # 地
    b.append(f'<rect x="40" y="460" width="640" height="20" fill="#c9b795"/>')
    b.append(f'<path d="M40 460 L680 460" stroke="{OCHRE}" stroke-width="1.4" opacity="0.6"/>')
    # 长案
    b.append(_poly([(92, 348), (628, 348), (648, 370), (72, 370)], "url(#f11lac)", GOLD, 1.6))
    b.append(f'<rect x="72" y="370" width="576" height="9" fill="#241310" stroke="{OCHRE}" stroke-width="1"/>')
    b.append(_poly([(96, 379), (624, 379), (624, 396), (96, 396)], "#33201a", GOLD, 1.1))
    for cx in (200, 360, 520):
        b.append(f'<path d="M{cx-14} 388 C{cx-8} 382 {cx-2} 384 {cx} 388 C{cx+2} 384 {cx+8} 382 {cx+14} 388" stroke="{GOLD}" stroke-width="1.3" fill="none" opacity="0.7"/>')
    for x0 in (112, 592):
        b.append(f'<rect x="{x0}" y="396" width="16" height="60" fill="#33201a" stroke="{OCHRE}" stroke-width="1"/>')
        b.append(f'<path d="M{x0-6} 456 L{x0+22} 456 L{x0+18} 462 L{x0-2} 462 Z" fill="#241310" stroke="{OCHRE}" stroke-width="1"/>')
    # 漆盘
    b.append(_poly([(132, 332), (588, 332), (610, 356), (110, 356)], "#6e241d", GOLD, 1.6))
    b.append(_poly([(146, 337), (574, 337), (592, 351), (128, 351)], "#8a2f26", "#c98a5c", 1.0))
    b.append(f'<path d="M150 341 L570 341" stroke="#a8483a" stroke-width="1" opacity="0.7"/>')
    # 鱼符：一整条鱼，中缝锯开
    b.append('<path d="M148 340 C154 314 178 302 206 308 C222 311 234 318 240 326 L236 331 L241 337 L236 343 L241 349 L236 355 L240 358 C234 366 222 371 206 372 C178 378 154 366 148 340 Z" fill="#c9a24a" stroke="#8c5a3c" stroke-width="1.8"/>')
    b.append('<path d="M246 326 C252 317 264 311 280 309 C290 308 298 312 302 318 L302 362 C298 368 290 372 280 371 C264 369 252 363 246 354 L250 349 L245 343 L250 337 L245 331 Z" fill="#d9b45e" stroke="#8c5a3c" stroke-width="1.8"/>')
    b.append('<path d="M302 320 L326 304 L318 338 L326 372 L302 360 Z" fill="#d9b45e" stroke="#8c5a3c" stroke-width="1.8"/>')
    b.append('<circle cx="168" cy="340" r="4" fill="#8a2f26" stroke="#f0cf8e" stroke-width="1.4"/>')
    b.append('<circle cx="310" cy="336" r="3.4" fill="#8a2f26" stroke="#f0cf8e" stroke-width="1.2"/>')
    for i in range(4):
        b.append(f'<path d="M{188+i*11} 328 Q{192+i*11} 340 {188+i*11} 352" stroke="#a8813a" stroke-width="1" fill="none" opacity="0.8"/>')
    b.append('<path d="M270 320 Q278 340 270 352" stroke="#a8813a" stroke-width="1" fill="none" opacity="0.8"/>')
    # 机关钥
    b.append(f'<ellipse cx="346" cy="334" rx="17" ry="19" fill="#c9a24a" stroke="{OCHRE}" stroke-width="1.8"/>')
    b.append(f'<ellipse cx="346" cy="334" rx="7" ry="8" fill="#8a2f26" stroke="#f0cf8e" stroke-width="1.3"/>')
    b.append(f'<path d="M338 317 C334 310 340 305 345 310 C350 304 356 310 352 317" stroke="{OCHRE}" stroke-width="3" fill="none"/>')
    b.append(f'<rect x="360" y="330" width="90" height="9" fill="#c9a24a" stroke="{OCHRE}" stroke-width="1.2"/>')
    b.append(f'<path d="M364 333 L446 333" stroke="#f0cf8e" stroke-width="1.2" opacity="0.8"/>')
    b.append(f'<rect x="456" y="326" width="38" height="30" rx="2" fill="#c9a24a" stroke="{OCHRE}" stroke-width="1.4"/>')
    b.append(f'<rect x="462" y="332" width="24" height="16" fill="#3a2c14" stroke="{GOLD}" stroke-width="1"/>')
    b.append(gear(474, 340, 7, 8, GOLD, OCHRE))
    b.append(f'<path d="M458 356 L458 366 L468 366 L468 356" fill="none" stroke="{OCHRE}" stroke-width="3"/>')
    b.append(f'<path d="M478 356 L478 366 L488 366" fill="none" stroke="{OCHRE}" stroke-width="3"/>')
    # 玉圭
    b.append(f'<rect x="516" y="350" width="66" height="5" fill="{OCHRE}" stroke="{INK}" stroke-width="1"/>')
    b.append(f'<rect x="522" y="336" width="7" height="16" fill="#c9a24a" stroke="{OCHRE}" stroke-width="1"/>')
    b.append(f'<rect x="570" y="336" width="7" height="16" fill="#c9a24a" stroke="{OCHRE}" stroke-width="1"/>')
    b.append(f'<path d="M527 340 L527 264 L537 250 L561 250 L571 264 L571 340 Z" fill="url(#f11jade)" stroke="#3f6f52" stroke-width="2"/>')
    b.append(f'<path d="M532 336 L532 267 L540 256 L558 256 L566 267 L566 336" fill="none" stroke="#e2f0e4" stroke-width="1.1" opacity="0.55"/>')
    for cy in (280, 306, 328):
        b.append(f'<path d="M538 {cy} C541 {cy-9} 552 {cy-9} 556 {cy} C552 {cy+6} 545 {cy+4} 545 {cy-1} C545 {cy-5} 550 {cy-5} 551 {cy-1}" stroke="#3f6f52" stroke-width="1.2" fill="none" opacity="0.9"/>')
    b.append(f'<path d="M549 260 L549 332" stroke="#3f6f52" stroke-width="1" opacity="0.45"/>')
    b.append(f'<circle cx="549" cy="264" r="3" fill="#efe6cf" stroke="#3f6f52" stroke-width="1"/>')
    b.append(tassel(549, 268, 18, CINNABAR, 0.7))
    # 香炉
    b.append(_censer(602, 344, 0.9))
    for i in range(3):
        b.append(f'<path d="M{602+i*4-4} 300 C{598+i*6} 292 {606+i*5} 286 {602+i*5} 278" stroke="{WHITE}" stroke-width="1.6" fill="none" opacity="0.6"/>')
    return svg(W, H, "".join(b), defs)


# ---------------- 图 12：金匮火 ----------------
def fig12():
    W, H = 720, 540
    defs = '''<linearGradient id="f12wall" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#3f463c"/><stop offset="0.6" stop-color="#2b312a"/><stop offset="1" stop-color="#20251f"/></linearGradient>
<linearGradient id="f12bronze" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#8c9668"/><stop offset="0.45" stop-color="#6f7a52"/><stop offset="1" stop-color="#4b5338"/></linearGradient>
<linearGradient id="f12pot" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#d9b45e"/><stop offset="0.5" stop-color="#bd9440"/><stop offset="1" stop-color="#8c6a28"/></linearGradient>
<radialGradient id="f12fire" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#e8a33c" stop-opacity="0.55"/><stop offset="1" stop-color="#e8a33c" stop-opacity="0"/></radialGradient>
<radialGradient id="f12vig" cx="0.5" cy="0.42" r="0.72">
<stop offset="0.5" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="0.42"/></radialGradient>'''
    b = []
    b.append(f'<rect x="40" y="40" width="640" height="448" fill="url(#f12wall)"/>')
    # 石砌墙缝
    for j, y0 in enumerate(range(70, 470, 42)):
        b.append(f'<path d="M40 {y0} L680 {y0}" stroke="#1b201a" stroke-width="1.4" opacity="0.55"/>')
        off = 0 if j % 2 == 0 else 44
        for x0 in range(40 + off, 680, 88):
            b.append(f'<path d="M{x0} {y0} L{x0} {y0+42}" stroke="#1b201a" stroke-width="1.2" opacity="0.45"/>')
    # 石拱
    b.append(f'<path d="M150 470 L150 300 A210 210 0 0 1 570 300 L570 470 L520 470 L520 306 A160 160 0 0 0 200 306 L200 470 Z" fill="#333a30" stroke="#1c211a" stroke-width="1.4"/>')
    b.append(f'<path d="M150 300 A210 210 0 0 1 570 300" fill="none" stroke="#8a7a52" stroke-width="1.2" opacity="0.35"/>')
    for a in (200, 228, 256, 284, 312, 340):
        cx = 360 + 210 * math.cos(math.radians(a))
        cy = 300 + 210 * math.sin(math.radians(a))
        b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.6" fill="#7a7458" opacity="0.6"/>')
    # 地面
    b.append(f'<rect x="40" y="470" width="640" height="18" fill="#1b201a"/>')
    for x0 in range(60, 680, 70):
        b.append(f'<path d="M{x0} 470 L{x0} 488" stroke="#2d342b" stroke-width="1.2" opacity="0.8"/>')
    # 壁炬
    for x0 in (106, 614):
        b.append(f'<path d="M{x0} 262 L{x0} 288 M{x0-12} 288 L{x0+12} 288 L{x0+7} 300 L{x0-7} 300 Z" fill="{OCHRE}" stroke="{INK}" stroke-width="1.2"/>')
        b.append(f'<circle cx="{x0}" cy="290" r="42" fill="url(#f12fire)" opacity="0.6"/>')
        b.append(flame(x0, 288, 1.0))
    # 石座
    b.append(f'<rect x="130" y="432" width="400" height="24" fill="#394035" stroke="#1e241d" stroke-width="1.2"/>')
    b.append(f'<path d="M130 432 L530 432" stroke="{GOLD}" stroke-width="1.2" opacity="0.6"/>')
    b.append(f'<path d="M130 456 C200 462 460 462 530 456" stroke="#20261f" stroke-width="2" fill="none"/>')
    # 铜匮：顶盖
    b.append(f'<rect x="160" y="204" width="360" height="16" fill="url(#f12bronze)" stroke="{OCHRE}" stroke-width="1.6"/>')
    b.append(f'<path d="M160 204 L520 204" stroke="{GOLD}" stroke-width="2"/>')
    b.append(f'<rect x="168" y="220" width="344" height="14" fill="#4b5338" stroke="{GOLD}" stroke-width="1.2"/>')
    b.append(f'<rect x="170" y="234" width="340" height="196" fill="url(#f12bronze)" stroke="{OCHRE}" stroke-width="2"/>')
    b.append(f'<rect x="182" y="248" width="316" height="170" fill="#2f3527" stroke="{GOLD}" stroke-width="1.2"/>')
    # 柜角云纹包角
    for cx, cy, fl in [(184, 250, 1), (496, 250, -1), (184, 416, 1), (496, 416, -1)]:
        b.append(f'<path d="M{cx} {cy+14*fl} L{cx} {cy} L{cx+14*fl} {cy}" stroke="{GOLD}" stroke-width="3" opacity="0.8"/>')
    # 匮内火光
    b.append(f'<rect x="222" y="248" width="90" height="170" fill="#42180f"/>')
    b.append(f'<circle cx="266" cy="384" r="92" fill="url(#f12fire)" opacity="0.9"/>')
    b.append(f'<rect x="222" y="248" width="90" height="170" fill="#5a1e10" opacity="0.45"/>')
    # 左门半开（几乎侧立）
    b.append(f'<path d="M182 248 L222 258 L222 406 L182 416 Z" fill="#3f452e" stroke="{GOLD}" stroke-width="1.4"/>')
    b.append(f'<path d="M186 258 L186 408" stroke="#22281c" stroke-width="3" opacity="0.7"/>')
    for j in range(4):
        b.append(f'<circle cx="208" cy="{276+j*40}" r="2.0" fill="{GOLD}" opacity="0.75"/>')
    # 火舌从门内探出
    b.append(flame(238, 414, 1.6))
    b.append(flame(268, 408, 2.05))
    b.append(flame(298, 414, 1.4))
    b.append(f'<ellipse cx="266" cy="420" rx="64" ry="10" fill="#e8a33c" opacity="0.26"/>')
    # 右门，九道铜锁
    b.append(f'<rect x="312" y="248" width="186" height="170" fill="#3f452e" stroke="{GOLD}" stroke-width="1.6"/>')
    b.append(f'<path d="M316 252 C340 244 470 244 494 252" stroke="#22281c" stroke-width="1" fill="none" opacity="0.6"/>')
    for sx in (340, 396, 452):
        b.append(f'<rect x="{sx}" y="256" width="8" height="154" fill="{GOLD}" stroke="{OCHRE}" stroke-width="0.8"/>')
        for cy in (278, 324, 370):
            b.append(_padlock(sx + 4, cy, 1.3))
    b.append(f'<path d="M312 418 L498 418" stroke="{GOLD}" stroke-width="2"/>')
    # 已落的锁
    for cx, cy, a in [(154, 478, 18), (196, 486, -22), (232, 478, 40)]:
        b.append(f'<g transform="rotate({a} {cx} {cy})">{_padlock(cx, cy, 1.1)}</g>')
    # 火从盖缝里冒出
    b.append(flame(296, 204, 1.2))
    b.append(flame(348, 200, 1.55))
    b.append(flame(396, 204, 1.0))
    b.append(f'<path d="M282 198 C274 172 292 158 288 138 C304 154 308 172 302 192" stroke="#5a5245" stroke-width="3" fill="none" opacity="0.45"/>')
    b.append(f'<path d="M402 198 C412 174 398 158 406 140 C418 158 422 176 414 196" stroke="#5a5245" stroke-width="3" fill="none" opacity="0.4"/>')
    # 倒置酒壶
    b.append(f'<ellipse cx="602" cy="470" rx="78" ry="7" fill="#0f1410" opacity="0.5"/>')
    b.append(f'<g transform="rotate(-10 600 430)">')
    b.append(f'<ellipse cx="560" cy="424" rx="38" ry="30" fill="url(#f12pot)" stroke="{OCHRE}" stroke-width="1.8"/>')
    b.append(f'<ellipse cx="560" cy="424" rx="32" ry="24" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.8"/>')
    # 壶底六十四字：八行八列
    for i in range(8):
        for j in range(8):
            gx = 560 + (i - 3.5) * 8.0
            gy = 424 + (j - 3.5) * 5.4
            b.append(f'<rect x="{gx-1.7:.1f}" y="{gy-1.4:.1f}" width="3.4" height="2.8" fill="#f2d38a" opacity="0.9"/>')
    b.append(f'<ellipse cx="606" cy="430" rx="40" ry="38" fill="url(#f12pot)" stroke="{OCHRE}" stroke-width="1.6"/>')
    b.append(f'<path d="M582 402 C592 396 610 398 620 406" stroke="#f2d38a" stroke-width="2" fill="none" opacity="0.55"/>')
    b.append(f'<path d="M638 414 L658 418 L658 446 L638 450 Z" fill="url(#f12pot)" stroke="{OCHRE}" stroke-width="1.4"/>')
    b.append(f'<ellipse cx="659" cy="432" rx="5" ry="14" fill="#4a3413" stroke="{OCHRE}" stroke-width="1.2"/>')
    b.append(f'<path d="M636 402 C650 386 664 378 678 374 L682 382 C668 386 654 394 642 410 Z" fill="url(#f12pot)" stroke="{OCHRE}" stroke-width="1.2"/>')
    b.append(f'<path d="M590 398 C578 372 602 358 616 370 C626 379 620 392 608 394" fill="none" stroke="{OCHRE}" stroke-width="7" stroke-linecap="round"/>')
    b.append(f'<path d="M608 452 C618 456 628 454 634 448" stroke="#f7e2b0" stroke-width="2" fill="none" opacity="0.4"/>')
    b.append('</g>')
    # 飘起的经文
    for ch, x, y, sz, op in [("天", 526, 238, 26, 0.95), ("地", 534, 274, 25, 0.85),
                             ("玄", 542, 310, 23, 0.74), ("黄", 550, 346, 21, 0.62),
                             ("宇", 562, 382, 19, 0.48)]:
        b.append(f'<text x="{x}" y="{y}" font-family="{KAI}" font-size="{sz}" fill="#f2d38a" opacity="{op}" text-anchor="middle">{ch}</text>')
    b.append(f'<path d="M574 402 C562 370 548 320 528 236" stroke="#e8b45a" stroke-width="1.4" fill="none" opacity="0.35"/>')
    # 飞灰
    for k in range(10):
        a = 0.6 + k * 0.7
        b.append(f'<circle cx="{360 + 120 * math.cos(a):.1f}" cy="{380 - 120 * math.sin(a):.1f}" r="{1.2 + (k % 3) * 0.5}" fill="#e8b45a" opacity="0.5"/>')
    # 暗角
    b.append(f'<rect x="40" y="40" width="640" height="448" fill="url(#f12vig)"/>')
    return svg(W, H, "".join(b), defs)
