#!/usr/bin/env python3
"""把 PDF 里同一字重的宋体子集合并成一个内嵌字体。

Chrome 打印长文时，会把同一个 Songti SC 拆成十几个 Type0/Identity-H 子集。
这些子集的字形编号来自同一套系统字体，编号和字形一一对应，只是各自只带
一部分字形。因此不需要改文字流，只要做三件事：

1. 从每个子集里收集用到的 glyph id，按常规/粗体求并集；
2. 用系统 Songti.ttc 按同样的 glyph id 子集化，保留原编号（retain_gids）；
3. 把每个旧 Type0 字体字典的 DescendantFonts 与 ToUnicode 指向合并字体。

文字流里的 2 字节编号原样不动，所以版面、字距、复制出的文字都不会变。
旧的子集字体失去引用后，由 PyMuPDF 的 garbage collection 清掉。

用法：
    python3 tools/merge_fonts.py [输入.pdf] [输出.pdf]

不写输出路径时原地替换。构建脚本会直接调用 merge_songti_fonts()。
"""
from __future__ import annotations

import io
import logging
import os
import pathlib
import re
import sys

import pymupdf
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SYSTEM_SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"
FACES = {"reg": 6, "bold": 1}   # Songti SC Regular / Bold

# fontTools 会对 feat/meta/morx 这些与 PDF 无关的表发警告，构建时不必看
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)


def _tounicode_codes(stream: str) -> set[int]:
    """取出 ToUnicode CMap 里出现过的源编号，用来补齐没有轮廓的空格等字形。"""
    codes: set[int] = set()
    for block in re.findall(r"beginbfchar(.*?)endbfchar", stream, re.S):
        for src, _dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
            codes.add(int(src, 16))
    for block in re.findall(r"beginbfrange(.*?)endbfrange", stream, re.S):
        for lo, hi, _dst in re.findall(
            r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block
        ):
            codes.update(range(int(lo, 16), int(hi, 16) + 1))
        for lo, hi, _arr in re.findall(
            r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[([^\]]*)\]", block
        ):
            codes.update(range(int(lo, 16), int(hi, 16) + 1))
    return codes


def collect_songti_subsets(doc: pymupdf.Document) -> dict[int, tuple[str, set[int]]]:
    """返回 {字体 xref: (字重, 用到的 glyph id 集合)}。"""
    subsets: dict[int, tuple[str, set[int]]] = {}
    for page in doc:
        for row in page.get_fonts(full=True):
            xref, ext, _ftype, base, _name, _enc = row[:6]
            if xref in subsets or ext == "n/a" or "STSongti" not in base:
                continue
            fam = "bold" if "Bold" in base else "reg"
            font = TTFont(io.BytesIO(doc.extract_font(xref)[3]))
            used: set[int] = set()
            glyf = font["glyf"]
            for gid, glyph_name in enumerate(font.getGlyphOrder()):
                try:
                    if glyf[glyph_name].numberOfContours:
                        used.add(gid)
                except Exception:
                    pass
            obj = doc.xref_object(xref, compressed=False)
            m = re.search(r"/ToUnicode\s+(\d+)\s+0\s+R", obj)
            if m:
                stream = doc.xref_stream(int(m.group(1))).decode("latin1")
                used |= _tounicode_codes(stream)
            subsets[xref] = (fam, used)
    return subsets


def build_merged_font(face: int, gids: set[int], out_path: str) -> None:
    """按原 glyph id 子集化系统宋体，保留编号。"""
    font = TTFont(SYSTEM_SONG, fontNumber=face)
    opts = Options()
    opts.retain_gids = True       # 关键：编号不变，文字流才能原样复用
    opts.glyph_names = True
    opts.notdef_outline = True
    subsetter = Subsetter(options=opts)
    subsetter.populate(gids=sorted(gids | {0}))
    subsetter.subset(font)
    font.save(out_path)


def _descendant_and_tounicode(doc: pymupdf.Document, t0_xref: int) -> tuple[int, int]:
    obj = doc.xref_object(t0_xref, compressed=False)
    descendant = re.search(r"/DescendantFonts\s*\[\s*(\d+)\s+0\s+R", obj)
    tounicode = re.search(r"/ToUnicode\s+(\d+)\s+0\s+R", obj)
    if not descendant or not tounicode:
        raise RuntimeError(f"字体 {t0_xref} 不是带 ToUnicode 的 Type0 字体")
    return int(descendant.group(1)), int(tounicode.group(1))


def _patch_ellipsis(doc: pymupdf.Document, tounicode_xref: int) -> None:
    """系统字体把省略号映射成 U+22EF，中文排版习惯是 U+2026。

    只改 ToUnicode，不改字形。复制出来仍是“……”而不是“⋯⋯”。
    """
    stream = doc.xref_stream(tounicode_xref).decode("latin1")
    patched = stream.replace("<22ef>", "<2026>").replace("<22EF>", "<2026>")
    if patched != stream:
        doc.update_stream(tounicode_xref, patched.encode("latin1"))


def merge_songti_fonts(
    pdf_path: str | pathlib.Path,
    verbose: bool = True,
) -> dict[str, int]:
    """原地合并 PDF 里的宋体子集，返回统计信息。

    如果文件里已经没有 STSongti 子集，直接返回，便于重复调用。
    """
    pdf_path = pathlib.Path(pdf_path)
    size_before = pdf_path.stat().st_size
    doc = pymupdf.open(pdf_path)
    subsets = collect_songti_subsets(doc)
    if not subsets:
        doc.close()
        return {
            "old_fonts": 0,
            "new_fonts": 0,
            "size_before": size_before,
            "size_after": size_before,
        }

    tmp_dir = pdf_path.parent / "build"
    tmp_dir.mkdir(exist_ok=True)
    merged_paths: dict[str, str] = {}
    for fam, face in FACES.items():
        gids: set[int] = set()
        for subset_fam, subset_gids in subsets.values():
            if subset_fam == fam:
                gids |= subset_gids
        out_path = str(tmp_dir / f"merged_{fam}.ttf")
        build_merged_font(face, gids, out_path)
        merged_paths[fam] = out_path

    page = doc[0]
    new_t0 = {
        "reg": page.insert_font(fontfile=merged_paths["reg"], fontname="SongtiSC-Regular"),
        "bold": page.insert_font(fontfile=merged_paths["bold"], fontname="SongtiSC-Bold"),
    }
    descendant: dict[str, int] = {}
    tounicode: dict[str, int] = {}
    for fam, xref in new_t0.items():
        descendant[fam], tounicode[fam] = _descendant_and_tounicode(doc, xref)
        _patch_ellipsis(doc, tounicode[fam])

    for xref, (fam, _gids) in subsets.items():
        base = "SongtiSC-Regular" if fam == "reg" else "SongtiSC-Bold"
        doc.update_object(
            xref,
            (
                "<< /Type /Font /Subtype /Type0 "
                f"/BaseFont /{base} /Encoding /Identity-H "
                f"/DescendantFonts [ {descendant[fam]} 0 R ] "
                f"/ToUnicode {tounicode[fam]} 0 R >>"
            ),
        )

    tmp_pdf = pdf_path.with_suffix(".merged.pdf")
    doc.save(
        tmp_pdf,
        garbage=4,
        deflate=True,
        clean=True,
        deflate_fonts=True,
        use_objstms=1,
    )
    doc.close()
    tmp_pdf.replace(pdf_path)

    stats = {
        "old_fonts": len(subsets),
        "new_fonts": len({fam for fam, _ in subsets.values()}),
        "size_before": size_before,
        "size_after": pdf_path.stat().st_size,
    }
    if verbose:
        print(
            f"字体合并：{stats['old_fonts']} 个子集 -> {stats['new_fonts']} 个，"
            f"{stats['size_before'] // 1024} KB -> {stats['size_after'] // 1024} KB"
        )
    return stats


def main() -> int:
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "天枢账簿.pdf"
    dst = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else src
    if src.resolve() != dst.resolve():
        doc = pymupdf.open(src)
        doc.save(dst, garbage=4, deflate=True, clean=True, use_objstms=1)
        doc.close()
    merge_songti_fonts(dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
