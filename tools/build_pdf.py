#!/usr/bin/env python3
"""README.md -> HTML -> PDF（《天枢账簿》暖纸书式）。

用法：python3 tools/build_pdf.py
产物：天枢账簿.pdf（仓库根目录），中间产物在 build/。
"""
import pathlib
import re
import subprocess
import sys

import fitz  # PyMuPDF

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
OUT_PDF = ROOT / "天枢账簿.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 章题（用于页眉右侧与书签），顺序即文中出现顺序
CHAPTERS = [
    "楔子　消失的账页",
    "第 1 章　定魂印",
    "第 2 章　剑意账印",
    "第 3 章　开山夺脉",
    "第 4 章　论功行签",
    "第 5 章　万叉一会",
    "第 6 章　心魔法阵",
    "第 7 章　证链",
    "第 8 章　问心魔劫",
    "第 9 章　万界共阵",
    "第 10 章　代价",
    "尾声　一年后",
    "参考文献",
]


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
    # 1) 封面：第一个 <hr /> 之前的内容包进 .cover，并删除该 hr
    first_hr = frag.find("<hr")
    if first_hr != -1:
        head, tail = frag[:first_hr], frag[first_hr:]
        tail = re.sub(r"^<hr[^>]*>\s*", "", tail)
        frag = '<div class="cover">\n' + head + "\n</div>\n" + tail

    # 2) 独立图片段落 -> figure-block + 图题
    frag = re.sub(
        r'<p><img src="([^"]+)" alt="([^"]*)"\s*/></p>',
        r'<div class="figure-block"><img src="\1" alt="\2">'
        r'<p class="figcap">\2</p></div>',
        frag,
    )

    # 3) 案卷框
    frag = re.sub(
        r"<blockquote>\s*(<p><strong>【天枢阁·案卷】)",
        r'<blockquote class="casebox">\n\1',
        frag,
    )

    # 4) 对话着色（中文弯引号只出现在正文文本中，安全）
    frag = re.sub(r"“([^“”]{1,120})”", r'<em class="say">“\1”</em>', frag)

    # 5) 正文引用标号 -> 链接；参考文献条目 -> 锚点
    frag = re.sub(r"\[(\d{1,2})\]", r'<a class="cite" href="#ref\1">[\1]</a>', frag)
    frag = re.sub(
        r'<p><a class="cite" href="#ref(\d{1,2})">\[\d{1,2}\]</a>　',
        r'<p class="ref-item" id="ref\1"><span class="refnum">[\1]</span>　',
        frag,
    )

    # 6) 数据时效说明
    frag = frag.replace(
        "<p><strong>关于数据时效</strong>",
        '<p class="data-note"><strong>关于数据时效</strong>',
    )
    return frag


def write_html(frag: str) -> pathlib.Path:
    css = (ROOT / "tools" / "style.css").read_text(encoding="utf-8")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>天枢账簿：什么是区块链？</title>
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


def chapter_starts(doc: fitz.Document) -> list[tuple[int, str]]:
    """返回 [(页号0基, 章题)]，按页号升序。"""
    starts = []
    cursor = 0
    for title in CHAPTERS:
        for pno in range(cursor, doc.page_count):
            if doc[pno].search_for(title):
                starts.append((pno, title))
                cursor = pno
                break
    return starts


def stamp(pdf_path: pathlib.Path) -> None:
    doc = fitz.open(pdf_path)
    total = doc.page_count
    starts = chapter_starts(doc)
    warm = (0.973, 0.953, 0.906)  # #f8f3e7
    ink = (0.17, 0.15, 0.13)
    faint = (0.78, 0.72, 0.62)
    for i, page in enumerate(doc):
        r = page.rect
        # 暖纸底色垫在内容之下（封面也铺）
        page.draw_rect(r, color=None, fill=warm, overlay=False)
        if i == 0:
            continue  # 封面不加页眉页脚
        chapter = ""
        for pno, title in starts:
            if pno <= i:
                chapter = title
            else:
                break
        page.insert_text((56, 42), "天枢账簿", fontname="china-s", fontsize=8.5, color=ink)
        if chapter:
            w = fitz.get_text_length(chapter, fontname="china-s", fontsize=8.5)
            page.insert_text(
                (r.width - 56 - w, 42), chapter, fontname="china-s", fontsize=8.5, color=ink
            )
        page.draw_line((56, 48), (r.width - 56, 48), color=faint, width=0.5)
        footer = f"— {i + 1} —"
        w = fitz.get_text_length(footer, fontname="china-s", fontsize=9)
        page.insert_text(
            ((r.width - w) / 2, r.height - 32), footer, fontname="china-s", fontsize=9, color=ink
        )
    tmp = pdf_path.with_suffix(".stamped.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf_path)


def build_outline(pdf_path: pathlib.Path) -> None:
    doc = fitz.open(pdf_path)
    starts = chapter_starts(doc)
    toc = [[1, title, pno + 1] for pno, title in starts]
    if toc:
        doc.set_toc(toc)
    tmp = pdf_path.with_suffix(".outline.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf_path)


def main() -> int:
    frag = transform(md_to_fragment())
    html_path = write_html(frag)
    chrome_to_pdf(html_path)
    stamp(OUT_PDF)
    build_outline(OUT_PDF)
    size_kb = OUT_PDF.stat().st_size // 1024
    print(f"OK -> {OUT_PDF} ({size_kb} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
