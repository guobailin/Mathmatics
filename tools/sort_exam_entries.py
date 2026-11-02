#!/usr/bin/env python3
"""把每个知识点「竞赛真题中的考察」节内的条目按星级升序稳定排序。

只重排列表行的顺序，不改任何一行文字；排序前后做全文字数校验，
确保除了行序之外没有任何内容变化。

用法：
    python3 tools/sort_exam_entries.py --dry-run   # 只报告会改哪些篇
    python3 tools/sort_exam_entries.py             # 实际写入
"""
from __future__ import annotations

import argparse
import glob
import os
import re

SECTION = "## 竞赛真题中的考察"
ENTRY = re.compile(r"^- \*\*")


def star_count(line: str) -> int:
    return line.count("★")


def sort_file(path: str, dry_run: bool) -> bool:
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    try:
        start = lines.index(SECTION)
    except ValueError:
        return False

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break

    # 找到节内连续的条目块（通常只有一块，但容错处理多块）
    changed = False
    i = start + 1
    while i < end:
        if ENTRY.match(lines[i]):
            j = i
            while j < end and ENTRY.match(lines[j]):
                j += 1
            block = lines[i:j]
            ordered = sorted(block, key=star_count)
            if ordered != block:
                lines[i:j] = ordered
                changed = True
            i = j
        else:
            i += 1

    if not changed:
        return False

    # 校验：排序前后该节的行数与字符总数必须一致
    original = open(path, encoding="utf-8").read()
    new_text = "\n".join(lines)
    if len(original.split("\n")) != len(lines):
        raise SystemExit(f"行数不一致，已中止：{path}")
    if sum(len(x) for x in original.split("\n")) != sum(len(x) for x in lines):
        raise SystemExit(f"字符总数不一致，已中止：{path}")
    if sorted(original.split("\n")) != sorted(lines):
        raise SystemExit(f"行内容集合发生变化，已中止：{path}")

    if not dry_run:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_text)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pattern = os.path.join(root, "content", "*", "*.md")
    total = 0
    for path in sorted(glob.glob(pattern)):
        if os.path.basename(path) == "curriculum.yaml":
            continue
        if sort_file(path, args.dry_run):
            total += 1
            print(("将改动 " if args.dry_run else "已排序 ") + os.path.relpath(path, root))
    print(f"\n共 {total} 篇" + ("需要排序（dry-run，未写入）" if args.dry_run else "完成排序"))


if __name__ == "__main__":
    main()
