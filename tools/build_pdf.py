#!/usr/bin/env python3
"""README.md -> HTML -> PDF（《天枢账簿》暖纸书式）。

用法：python3 tools/build_pdf.py
产物：天枢账簿.pdf（仓库根目录），中间产物在 build/。
"""
import io
import pathlib
import re
import subprocess
import sys

import fitz  # PyMuPDF
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
OUT_PDF = ROOT / "天枢账簿.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAPER = "#f8f3e7"      # 与 stamp() 里铺的暖纸底色一致
FIG_W_PX = 860        # 图在版面上宽约 415pt，按 150dpi 出像素
FIG_QUALITY = 86      # JPEG 质量：线稿偏高一点，避免边缘发糊


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


def citation_order_problem(readme: str | None = None) -> str:
    """参考文献编号必须是正文里第一次引用的先后。不合规就返回一句说明。

    排版会把编号原样印在纸上，编号乱了读者就得来回翻，所以宁可让构建
    失败，也不默默出一份乱序的 PDF。
    """
    if readme is None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
    body = readme.partition("## 参考文献")[0]
    order: list[int] = []
    for m in re.finditer(r"\[(\d{1,2})\]", body):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
    for i, n in enumerate(order):
        if n != i + 1:
            return f"正文第 {i + 1} 个出现的引用是 [{n}]，应为 [{i + 1}]"
    return ""


def rasterize_images() -> dict[str, str]:
    """把 SVG 预渲染成单张 JPEG。

    Chrome 打印时会把带 pattern/渐变填充的 SVG 切成十几条横向碎图（各带一张
    SMask），既糊又占空间。这里按版面显示宽度先栅格化一次，交给浏览器一张
    定宽的 JPEG，它就会原样以 DCTDecode 嵌进去：一张图、一个流、150dpi。
    """
    cache = BUILD / "raster"
    cache.mkdir(parents=True, exist_ok=True)
    out: dict[str, str] = {}
    for svg in sorted((ROOT / "img").glob("*.svg")):
        jpg = cache / (svg.stem + ".jpg")
        if not jpg.exists() or jpg.stat().st_mtime < svg.stat().st_mtime:
            png = subprocess.run(
                ["rsvg-convert", "-w", str(FIG_W_PX), "-b", PAPER, str(svg)],
                capture_output=True,
                check=True,
            ).stdout
            with Image.open(io.BytesIO(png)) as im:
                im.convert("RGB").save(
                    jpg, "JPEG", quality=FIG_QUALITY, optimize=True, progressive=False
                )
        out[f"img/{svg.name}"] = jpg.as_uri()
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


def transform(frag: str, raster: dict[str, str]) -> str:
    # 0) SVG 换成预渲染的 JPEG（只在 PDF 里换，README 仍指向矢量原图）
    for src, uri in raster.items():
        frag = frag.replace(f'src="{src}"', f'src="{uri}"')

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

    # 1b) 封面署名：只进 PDF，不动 README 正文
    frag = re.sub(
        r"(</h2>)",
        r'\1\n<p class="byline">Hecate2<span class="by-role">著</span></p>',
        frag,
        count=1,
    )

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

CJK = "china-s"   # 内置未嵌入中文字体（Heiti）
LAT = "tiro"      # Times-Roman，配数字与拉丁字母


def runs(text: str) -> list[tuple[str, bool]]:
    """把字符串切成「连续 ASCII」与「连续非 ASCII」两种片段。"""
    out: list[tuple[str, bool]] = []
    for ch in text:
        ascii_ = ord(ch) < 128
        if out and out[-1][1] == ascii_:
            out[-1] = (out[-1][0] + ch, ascii_)
        else:
            out.append((ch, ascii_))
    return out


def width_of(text: str, size: float) -> float:
    return sum(
        fitz.get_text_length(seg, fontname=LAT if a else CJK, fontsize=size)
        for seg, a in runs(text)
    )


def draw_text(page: fitz.Page, x: float, y: float, text: str, size: float, color) -> float:
    """中英混排：中文用内置字体，ASCII 用 Times。

    内置中文字体把 ASCII 也排成方块全角，数字会被拆成「3 0 0 1」，
    所以数字与拉丁字母必须换字体单独画。
    """
    for seg, a in runs(text):
        page.insert_text((x, y), seg, fontname=LAT if a else CJK, fontsize=size, color=color)
        x += fitz.get_text_length(seg, fontname=LAT if a else CJK, fontsize=size)
    return x

TOC_PAGES = 1   # 卷目占几页
FRONT_PAGES = 2  # 封面 + 题记：不排页眉页脚，也不编页码
BODY_START = TOC_PAGES + FRONT_PAGES  # 正文第一页的 0 基下标

CITE_MAX_SIZE = 8.5   # 正文上标 [n] 的字号（.cite 是 7.6pt）
REF_MIN_SIZE = 9.0    # 参考文献条目序号 [n] 的字号（.refnum 是 9.4pt）


def citation_marks(page: fitz.Page) -> list[tuple[int, float, fitz.Rect]]:
    """页面上每个 [n] 标号的（编号, 字号, 矩形）。字号用来分辨正文上标与文献序号。"""
    found: list[tuple[int, float, fitz.Rect]] = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                chars = span["chars"]
                text = "".join(c["c"] for c in chars)
                for m in re.finditer(r"\[(\d{1,2})\]", text):
                    box = fitz.Rect(chars[m.start()]["bbox"])
                    for c in chars[m.start() + 1: m.end()]:
                        box |= fitz.Rect(c["bbox"])
                    found.append((int(m.group(1)), span["size"], box))
    return found


def link_citations(doc: fitz.Document) -> int:
    """把正文上标 [n] 与文末参考文献 [n] 连成双向跳转。

    Chrome 自己会给 href="#refN" 生成跳转，但它按内容区坐标算落点，漏掉了
    页面上边距，实际偏高约 59pt（一行多）。这里整片重做：正文标号跳到文献
    条目，文献标号跳回第一次引用它的地方。
    """
    body: dict[int, list[tuple[int, fitz.Rect]]] = {}
    refs: dict[int, tuple[int, fitz.Rect]] = {}

    for pno, page in enumerate(doc):
        for link in page.get_links():
            if link["kind"] in (fitz.LINK_GOTO, fitz.LINK_NAMED):
                page.delete_link(link)
        for num, size, box in citation_marks(page):
            if size <= CITE_MAX_SIZE:
                body.setdefault(num, []).append((pno, box))
            elif size >= REF_MIN_SIZE:
                refs[num] = (pno, box)

    def jump(page: fitz.Page, box: fitz.Rect, target: fitz.Page, at: fitz.Point) -> None:
        page.insert_link(
            {
                "kind": fitz.LINK_GOTO,
                "from": fitz.Rect(box.x0 - 2, box.y0 - 2, box.x1 + 2, box.y1 + 2),
                "page": target.number,
                "to": fitz.Point(at.x, max(at.y, 0)),
                "zoom": 0,
            }
        )

    linked = 0
    for num, (rpno, rbox) in refs.items():
        hits = sorted(body.get(num, []), key=lambda h: (h[0], h[1].y0))
        if not hits:
            continue
        # 文献序号 → 第一次引用它的地方；往上留一点，好让读者看见上下文
        bpno, bbox = hits[0]
        jump(doc[rpno], rbox, doc[bpno], fitz.Point(bbox.x0, bbox.y0 - 42))
        for bpno, bbox in hits:
            jump(doc[bpno], bbox, doc[rpno], fitz.Point(rbox.x0, rbox.y0 - 12))
        linked += 1
    return linked


def insert_toc_page(doc: fitz.Document, starts: list[tuple[int, str]]) -> None:
    """在封面之后插入一页卷目。starts 为未插页时的章首页码。"""
    page = doc.new_page(pno=1)
    r = page.rect
    page.draw_rect(r, color=None, fill=WARM, overlay=False)

    title = "卷　目"
    w = width_of(title, 17)
    draw_text(page, (r.width - w) / 2, 108, title, 17, INK)
    page.draw_line((90, 124), (r.width - 90, 124), color=RUBRIC, width=1.2)

    y = 176
    step = 33
    left, right = 90, r.width - 90
    for pno, name in starts:
        # 封面与题记不编页码，所以卷目里的页码是「章首页的前一页之外」再减一
        shown = str(pno - (FRONT_PAGES - 1))
        pw = width_of(shown, 11.5)
        draw_text(page, left, y, name, 11.5, INK)
        draw_text(page, right - pw, y, shown, 11.5, INK)
        tw = width_of(name, 11.5)
        dot_end = right - pw - 9
        if left + tw + 9 < dot_end:
            # 一条细虚线当引线：比逐点画圆小两个数量级，观感一样
            page.draw_line(
                (left + tw + 9, y - 3),
                (dot_end, y - 3),
                color=FAINT,
                width=0.9,
                dashes="[0.7 3.6] 0",
                lineCap=1,
            )
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
        draw_text(page, 56, 42, "天枢账簿", 8.5, INK)
        if chapter:
            w = width_of(chapter, 8.5)
            draw_text(page, r.width - 56 - w, 42, chapter, 8.5, INK)
        page.draw_line((56, 48), (r.width - 56, 48), color=FAINT, width=0.5)
        footer = f"— {i - BODY_START + 1} —"
        w = width_of(footer, 9)
        draw_text(page, (r.width - w) / 2, r.height - 32, footer, 9, INK)
    tmp = pdf_path.with_suffix(".stamped.pdf")
    doc.save(tmp, garbage=4, deflate=True, clean=True)
    doc.close()
    tmp.replace(pdf_path)


def build_outline(pdf_path: pathlib.Path, toc_pages: int) -> int:
    """补书签、连引用跳转，并把整份 PDF 压到最小。

    use_objstms 会把字体描述、CID 宽度表、ToUnicode 这些「非流对象」也塞进
    压缩的对象流里——PDF 里这一堆元数据比正文本身还占地方。
    """
    doc = fitz.open(pdf_path)
    meta = doc.metadata
    meta["author"] = "Hecate2"
    doc.set_metadata(meta)
    starts = chapter_starts(doc, skip=1 + toc_pages)
    toc = [[1, title, pno + 1] for pno, title in starts]
    if toc:
        doc.set_toc(toc)
    linked = link_citations(doc)
    tmp = pdf_path.with_suffix(".outline.pdf")
    doc.save(
        tmp,
        garbage=4,
        clean=True,
        deflate=True,
        deflate_fonts=True,
        use_objstms=1,
    )
    doc.close()
    tmp.replace(pdf_path)
    return linked


def main() -> int:
    problem = citation_order_problem()
    if problem:
        print(f"参考文献编号不合规：{problem}", file=sys.stderr)
        print("先跑 python3 tools/renumber_refs.py", file=sys.stderr)
        return 1

    raster = rasterize_images()
    frag = transform(md_to_fragment(), raster)
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
    linked = build_outline(OUT_PDF, toc_pages=toc_pages)
    size_kb = OUT_PDF.stat().st_size // 1024
    print(f"OK -> {OUT_PDF} ({size_kb} KB, {len(starts)} 章, {linked} 条文献双向跳转)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
