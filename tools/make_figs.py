#!/usr/bin/env python3
"""生成 img/ 下十三张中国画风 SVG。

用法：python3 tools/make_figs.py
画法全部在 tools/svgkit.py 与 tools/figs_scenes.py 中，本文件只做命名与落盘。
"""
import pathlib

import figs_scenes as F

OUT = pathlib.Path(__file__).resolve().parent.parent / "img"

FIGS = {
    "fig00_wanjuan": F.fig00,
    "fig01_yinlian": F.fig01,
    "fig02_xuebeng": F.fig02,
    "fig03_jianfeng": F.fig03,
    "fig04_kaishan": F.fig04,
    "fig05_hefu": F.fig05,
    "fig06_sanqi": F.fig06,
    "fig07_zhuanlun": F.fig07,
    "fig08_zhenfa": F.fig08,
    "fig09_merkle": F.fig09,
    "fig10_zhaoyao": F.fig10,
    "fig11_sanyao": F.fig11,
    "fig12_jingui": F.fig12,
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in FIGS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()
