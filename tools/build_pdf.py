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

def chapters() -> list[str]:
    """章题直接从 README 的一级标题抽取，避免与正文脱节。"""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    out = []
    for line in readme.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title and title != "天枢账簿":
                out.append(title)
    return out


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
    # 1) 封面与题记：以 <!--epigraph--> 标记切分，封面只留书名、副题、卷首图
    open_m, close_m = "<!--epigraph-->", "<!--/epigraph-->"
    if open_m in frag and close_m in frag:
        head, rest = frag.split(open_m, 1)
        body, tail = rest.split(close_m, 1)
        frag = (
            '<div class="cover">\n' + head + "\n</div>\n"
            '<div class="epigraph">\n' + body + "\n</div>\n" + tail
        )
    else:  # 退路：以第一个 hr 为界
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

    # 4) 整段引语：段首是中文引号的段落单独标注，供版式缩进
    frag = re.sub(r'<p>“', r'<p class="say">“', frag)

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
<base href="{ROOT.as_uri()}/">
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


def chapter_starts(doc: fitz.Document, skip: int = 0) -> list[tuple[int, str]]:
    """返回 [(页号0基, 章题)]。skip 用于跳过封面与卷目，避免误命中目录里的标题。"""
    def norm(x: str) -> str:
        return "".join(x.split()).replace("\u00b7", "·")

    titles = chapters()
    texts = [norm(doc[i].get_text()) for i in range(doc.page_count)]
    starts = []
    cursor = skip
    for title in titles:
        key = norm(title)
        for pno in range(cursor, doc.page_count):
            if key in texts[pno]:
                starts.append((pno, title))
                cursor = pno
                break
    return starts


WARM = (0.973, 0.953, 0.906)   # #f8f3e7
INK = (0.17, 0.15, 0.13)
FAINT = (0.78, 0.72, 0.62)
RUBRIC = (0.71, 0.26, 0.18)    # 朱色

TOC_PAGES = 1   # 卷目占几页
FRONT_PAGES = 2  # 封面 + 题记：不排页眉页脚，也不编页码
BODY_START = TOC_PAGES + FRONT_PAGES  # 正文第一页的 0 基下标


def insert_toc_page(doc: fitz.Document, starts: list[tuple[int, str]]) -> None:
    """在封面之后插入一页卷目。starts 为未插页时的章首页码。"""
    page = doc.new_page(pno=1)
    r = page.rect
    page.draw_rect(r, color=None, fill=WARM, overlay=False)

    title = "卷　目"
    w = fitz.get_text_length(title, fontname="china-s", fontsize=17)
    page.insert_text(((r.width - w) / 2, 108), title, fontname="china-s", fontsize=17, color=INK)
    page.draw_line((90, 124), (r.width - 90, 124), color=RUBRIC, width=1.2)

    y = 168
    step = 27
    left, right = 90, r.width - 90
    for pno, name in starts:
        # 封面与题记不编页码，所以卷目里的页码是「章首页的前一页之外」再减一
        shown = str(pno - (FRONT_PAGES - 1))
        pw = fitz.get_text_length(shown, fontname="helv", fontsize=10.5)
        page.insert_text((left, y), name, fontname="china-s", fontsize=10.5, color=INK)
        page.insert_text((right - pw, y), shown, fontname="helv", fontsize=10.5, color=INK)
        tw = fitz.get_text_length(name, fontname="china-s", fontsize=10.5)
        x = left + tw + 8
        dot_end = right - pw - 8
        while x < dot_end:
            page.draw_circle((x, y - 3), 0.45, color=FAINT, fill=FAINT)
            x += 5.5
        y += step


def stamp(pdf_path: pathlib.Path, toc_pages: int) -> None:
    doc = fitz.open(pdf_path)
    starts = chapter_starts(doc, skip=1 + toc_pages)
    for i, page in enumerate(doc):
        r = page.rect
        # 暖纸底色垫在内容之下（封面也铺）
        page.draw_rect(r, color=None, fill=WARM, overlay=False)
        if i < BODY_START:
            continue  # 封面、卷目、题记：不排页眉页脚，也不编页码
        chapter = ""
        for pno, title in starts:
            if pno <= i:
                chapter = title
            else:
                break
        page.insert_text((56, 42), "天枢账簿", fontname="china-s", fontsize=8.5, color=INK)
        if chapter:
            w = fitz.get_text_length(chapter, fontname="china-s", fontsize=8.5)
            page.insert_text(
                (r.width - 56 - w, 42), chapter, fontname="china-s", fontsize=8.5, color=INK
            )
        page.draw_line((56, 48), (r.width - 56, 48), color=FAINT, width=0.5)
        footer = f"— {i - BODY_START + 1} —"
        w = fitz.get_text_length(footer, fontname="helv", fontsize=9)
        page.insert_text(
            ((r.width - w) / 2, r.height - 32), footer, fontname="helv", fontsize=9, color=INK
        )
    tmp = pdf_path.with_suffix(".stamped.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf_path)


def build_outline(pdf_path: pathlib.Path, toc_pages: int) -> None:
    doc = fitz.open(pdf_path)
    starts = chapter_starts(doc, skip=1 + toc_pages)
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

    toc_pages = 1
    doc = fitz.open(OUT_PDF)
    starts = chapter_starts(doc)
    insert_toc_page(doc, starts)
    tmp = OUT_PDF.with_suffix(".toc.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(OUT_PDF)

    stamp(OUT_PDF, toc_pages=toc_pages)
    build_outline(OUT_PDF, toc_pages=toc_pages)
    size_kb = OUT_PDF.stat().st_size // 1024
    print(f"OK -> {OUT_PDF} ({size_kb} KB, {len(starts)} 章)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
