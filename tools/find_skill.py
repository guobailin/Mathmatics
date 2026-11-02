#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按子技能反查覆盖它的例题（读 dist/covered_by.json，只读）

先跑一次 `python3 tools/build.py` 生成索引，然后：

    python3 tools/find_skill.py 试除          # 模糊查：子技能名含「试除」
    python3 tools/find_skill.py --module 08 试除  # 限定模块
    python3 tools/find_skill.py --list 08      # 列出该模块全部子技能

用途：错因归到某个子技能后，直接查到「哪几篇的哪几道题在练它」，
据此选题复练，而不是靠篇名猜。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "dist" / "covered_by.json"


def load() -> dict:
    if not INDEX.exists():
        print("缺少 dist/covered_by.json，请先运行 python3 tools/build.py",
              file=sys.stderr)
        raise SystemExit(2)
    return json.loads(INDEX.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="按子技能反查例题")
    ap.add_argument("keyword", nargs="?", default="", help="子技能名关键词（模糊匹配）")
    ap.add_argument("--module", "-m", help="限定模块前缀，如 08")
    ap.add_argument("--list", action="store_true", help="只列子技能名，不展开例题")
    args = ap.parse_args()

    data = load()

    def in_module(item: dict) -> bool:
        return not args.module or item["moduleDir"].startswith(args.module)

    hits = {}
    for skill, items in data.items():
        sel = [i for i in items if in_module(i)]
        if args.module and not sel:
            continue
        if args.keyword and args.keyword not in skill:
            continue
        hits[skill] = sel

    if not hits:
        print(f"没有匹配「{args.keyword}」的子技能"
              + (f"（模块 {args.module}）" if args.module else ""))
        return 0

    if args.list:
        for skill in sorted(hits):
            print(f"{skill}  ({len(hits[skill])})")
        return 0

    total = 0
    for skill in sorted(hits):
        items = hits[skill]
        total += len(items)
        print(f"\n■ {skill}")
        for i in items:
            print(f"    {i['module']}｜{i['title']}｜{i['exampleTitle']}")
    print(f"\n共 {len(hits)} 个子技能、{total} 道例题")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
