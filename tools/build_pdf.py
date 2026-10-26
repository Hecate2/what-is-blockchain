#!/usr/bin/env python3
"""README.md -> HTML -> PDF（学术期刊风格）。

用法：python3 tools/build_pdf.py
产物：什么是区块链.pdf（仓库根目录），中间产物在 build/。
"""
import pathlib
import re
import subprocess
import sys

import fitz  # PyMuPDF

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
OUT_PDF = ROOT / "什么是区块链.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def md_to_fragment() -> str:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    proc = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none"],
        input=readme,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def transform(frag: str) -> str:
    frag = frag.replace('<div align="center">', '<div class="figure-block">')
    frag = frag.replace(
        "<p><strong>摘要</strong>", '<p class="abstract"><strong>摘要</strong>'
    )
    frag = frag.replace(
        "<p><strong>关于数据时效</strong>",
        '<p class="data-note"><strong>关于数据时效</strong>',
    )
    frag = re.sub(r"<p><strong>(表 \d+)", r'<p class="tab-caption"><strong>\1', frag)
    # 先把正文里的引用标号变成链接
    frag = re.sub(r"\[(\d{1,2})\]", r'<a class="cite" href="#ref\1">[\1]</a>', frag)
    # 再把参考文献条目锚点化（条目以 "[n]　" 开头）
    frag = re.sub(
        r'<p><a class="cite" href="#ref(\d{1,2})">\[\d{1,2}\]</a>　',
        r'<p class="ref-item" id="ref\1"><span class="refnum">[\1]</span>　',
        frag,
    )
    return frag


def write_html(frag: str) -> pathlib.Path:
    css = (ROOT / "tools" / "style.css").read_text(encoding="utf-8")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>什么是区块链？</title>
<style>
{css}
</style>
</head>
<body>
{frag}
</body>
</html>
"""
    BUILD.mkdir(exist_ok=True)
    out = BUILD / "article.html"
    out.write_text(html, encoding="utf-8")
    return out


def chrome_to_pdf(html_path: pathlib.Path) -> None:
    subprocess.run(
        [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-pdf-header-footer",
            "--virtual-time-budget=8000",
            f"--print-to-pdf={OUT_PDF}",
            html_path.resolve().as_uri(),
        ],
        check=True,
        capture_output=True,
    )


def stamp(pdf_path: pathlib.Path) -> None:
    doc = fitz.open(pdf_path)
    total = doc.page_count
    gray = (0.48, 0.52, 0.57)
    for i, page in enumerate(doc):
        r = page.rect
        if i > 0:
            page.insert_text(
                (56, 42),
                "什么是区块链？",
                fontname="china-s",
                fontsize=8.5,
                color=(0.58, 0.62, 0.66),
            )
            page.draw_line(
                (56, 48), (r.width - 56, 48), color=(0.84, 0.87, 0.9), width=0.5
            )
        footer = f"第 {i + 1} 页 / 共 {total} 页"
        w = fitz.get_text_length(footer, fontname="china-s", fontsize=9)
        page.insert_text(
            ((r.width - w) / 2, r.height - 34),
            footer,
            fontname="china-s",
            fontsize=9,
            color=gray,
        )
    tmp = pdf_path.with_suffix(".stamped.pdf")
    doc.save(tmp)
    doc.close()
    tmp.replace(pdf_path)


def build_outline(pdf_path: pathlib.Path) -> None:
    doc = fitz.open(pdf_path)
    toc = []
    headings = [
        "1. 从一本谁都能改的账本说起",
        "2. 哈希：数字世界的指纹",
        "3. 数字签名：证明",
        "4. 共识：全网怎么对账",
        "5. 会算账的账本",
        "6. 跟着一笔钱走完全程",
        "7. 零知识证明",
        "8. 这件事对软件世界意味着什么",
        "9. 冷静一下",
        "10. 结语",
        "参考文献",
    ]
    for title in headings:
        for pno in range(doc.page_count):
            hits = doc[pno].search_for(title)
            if hits:
                toc.append([1, title, pno + 1])
                break
    if toc:
        doc.set_toc(toc)
    tmp = pdf_path.with_suffix(".outline.pdf")
    doc.save(tmp)
    doc.close()
    tmp.replace(pdf_path)


def main() -> int:
    frag = transform(md_to_fragment())
    html_path = write_html(frag)
    chrome_to_pdf(html_path)
    stamp(OUT_PDF)
    build_outline(OUT_PDF)
    print(f"OK -> {OUT_PDF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
