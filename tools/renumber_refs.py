#!/usr/bin/env python3
"""按正文里第一次引用的先后，重排 README.md 的参考文献编号。

正文的 [n] 与文末 `[n]　条目` 一一对应。[1] 是正文中最先出现的那个引用，
[2] 次之，依次排下去——这是学术期刊的通行编号法，也让读者顺着读时不必
来回翻。编号已经合规时什么也不改（幂等）。

用法：
    python3 tools/renumber_refs.py            # 就地改写
    python3 tools/renumber_refs.py --dry-run   # 只打印置换表
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
REF_HEAD = "## 参考文献"
CITE = re.compile(r"\[(\d{1,2})\]")
ENTRY = re.compile(r"(?m)^\[(\d{1,2})\]　(.*)$")


def first_citation_order(body: str) -> list[int]:
    order: list[int] = []
    for m in CITE.finditer(body):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
    return order


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    md = README.read_text(encoding="utf-8")
    body, sep, refs = md.partition(REF_HEAD)
    if not sep:
        print(f"找不到「{REF_HEAD}」章节", file=sys.stderr)
        return 1

    order = first_citation_order(body)
    slots = list(ENTRY.finditer(refs))
    labels = [int(m.group(1)) for m in slots]
    text = {int(m.group(1)): m.group(2) for m in slots}

    if len(text) != len(slots):
        print("文献编号有重复，先手改掉", file=sys.stderr)
        return 1
    cited, listed = set(order), set(text)
    if cited - listed:
        print(f"正文引用了不存在的文献：{sorted(cited - listed)}", file=sys.stderr)
        return 1
    if listed - cited:
        print(f"这些文献在正文里没有引用：{sorted(listed - cited)}", file=sys.stderr)
        return 1

    mapping = {old: i + 1 for i, old in enumerate(order)}
    if all(mapping[n] == n for n in mapping) and labels == sorted(labels):
        print("编号已经是引用顺序，无需改动")
        return 0

    moved = [(old, new) for old, new in mapping.items() if old != new]
    print(f"{len(mapping)} 条文献，{len(moved)} 条要换号")
    for old, new in moved:
        print(f"  [{old:2d}] -> [{new:2d}]  {text[old][:44]}")

    if dry:
        return 0

    new_body = CITE.sub(lambda m: f"[{mapping[int(m.group(1))]}]", body)

    # 条目槽位不动，只把内容按新号重填，段落间的空行原样留着
    pieces, cursor = [], 0
    for k, slot in enumerate(slots):
        src = order[k]          # 新号 k+1 对应的旧号
        pieces.append(refs[cursor: slot.start()])
        pieces.append(f"[{k + 1}]　{text[src]}")
        cursor = slot.end()
    pieces.append(refs[cursor:])

    README.write_text(new_body + sep + "".join(pieces), encoding="utf-8")
    print("已改写 README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
