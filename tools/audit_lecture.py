#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""讲解层只读审计（不参与 build，不改任何文件）

用法：
    python3 tools/audit_lecture.py            # 全量报告
    python3 tools/audit_lecture.py --module 10 # 只看某一模块（按目录前缀）

检查四件事，对应 issue #74 的 P1-8 / P1-9 / P1-10 / P1-6：
    1. 易错点是否为 ### 标题（粗体不成锚点、不进目录、脚本抓不到）
    2. 速查卡是否带 ⚠️ 易错行
    3. 例题解析开头是否给出策略引导（思路句）
    4. related 是否为空

关于「思路句」的口径（重要）：
    旧口径「**解析**：后 120 字内是否含『为什么』」会系统性高估缺口——本库
    大量解析用「看到……就想到」「只给速度比，说明要用……」「取法不连续，
    补足法失效，只能……」这类隐含写法，语义等价但不含「为什么」三字。
    故本脚本分两级报告：
        显式：解析开头出现「**为什么……？**」问句
        隐含：开头出现策略词（看到/说明/只能/关键/转化为……）但无问句
    只有两级都不命中的才计入「疑似缺思路句」，且仍需人工确认——
    脚本不做语义判断，命中不等于写得好，未命中也不等于写得差。
    已知漏判（人工逐条读过，确有思路句，只是没用「为什么」也没用词表里的
    策略词，故列入 KNOWN_FN 单列，不计入缺口）：
        08-奥数-数论/余数问题物不知数.md 例2 —— 「从除以 7 余 3 起步（除数最大，列得最少）」
        08-奥数-数论/奇数与偶数.md 例2 —— 「这类题的关键，是把每枚硬币和每次操作用同一个数连起来」
        08-奥数-数论/数的整除特征.md 例4 —— 「第一步，选工具」（7 与 13 同现 → 1001）
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OLY_MODULES = ["06", "07", "08", "09", "10", "11"]

# 显式设问：解析开头出现「为什么」（本库写法多样：有的带 ？、有的带 ：、
# 有的加粗、有的不加粗，故只判关键词，不强制标点与加粗）
RE_EXPLICIT = re.compile(r"为什么")
# 隐含策略词：出现在解析开头 100 字内即视为给出了策略判断
STRATEGY_WORDS = (
    "看到", "想", "说明", "只能", "必须", "关键是", "关键在", "难点", "突破口",
    "因为", "所以", "先", "注意", "题意", "题目", "条件", "转化", "翻译",
    "失效", "不妨", "只需", "只要", "反例", "极端", "显然", "不难", "本质上",
)

# 人工确认过、确有思路句但检测器词表覆盖不到的组合（相对路径, 例号）
KNOWN_FN = {
    ("08-奥数-数论/余数问题物不知数.md", "2"),
    ("08-奥数-数论/奇数与偶数.md", "2"),
    ("08-奥数-数论/数的整除特征.md", "4"),
}


def oly_files() -> list[Path]:
    out: list[Path] = []
    for m in OLY_MODULES:
        out.extend(sorted(CONTENT.glob(f"{m}-*/*.md")))
    return out


def split_examples(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"^### 例(\d+)[^\n]*$", text, flags=re.M)[1:]
    return [(parts[i], parts[i + 1]) for i in range(0, len(parts) - 1, 2)]


def analyze(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    res: dict = {"path": path, "issues": []}

    # 1. 易错点标题：要求「讲解」节内恰有一个含「易错」的 ### 标题
    heads = [m for m in re.finditer(r"^### ([^\n]*易错[^\n]*)$", text, re.M)]
    lec_start = text.find("## 讲解")
    exam_start = text.find("## 竞赛真题中的考察")
    in_lec = [m for m in heads if lec_start < m.start() < exam_start]
    if len(in_lec) != 1:
        res["issues"].append(
            f"易错点标题：讲解节内有 {len(in_lec)} 个（应为 1 个 ### 标题）"
        )

    # 2. 速查卡必带 ⚠️ 行
    card = re.search(r"<!-- card:auto -->(.*?)<!-- /card:auto -->", text, re.S)
    if not card:
        res["issues"].append("速查卡：缺少 card:auto 块")
    elif "⚠️" not in card.group(1):
        res["issues"].append("速查卡：缺少 ⚠️ 易错行")

    # 3. 例题解析的思路句分级
    explicit, implicit, missing, known = 0, 0, [], []
    rel = str(path.relative_to(CONTENT))
    examples = split_examples(text)
    for no, body in examples:
        m = re.search(r"\*\*解析\*\*[：:]?(.{0,100})", body, re.S)
        if not m:
            missing.append(no)
            continue
        seg = m.group(1)
        if RE_EXPLICIT.search(seg):
            explicit += 1
        elif any(w in seg for w in STRATEGY_WORDS):
            implicit += 1
        elif (rel, no) in KNOWN_FN:
            known.append(no)
        else:
            missing.append(no)
    res.update(
        examples=len(examples),
        explicit=explicit,
        implicit=implicit,
        missing=missing,
        known=known,
    )
    for no in missing:
        res["issues"].append(f"例{no}：解析开头未见策略引导（需人工确认）")

    # 4. related 非空
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm or not re.search(r"^related:\s*\S", fm.group(1), re.M):
        res["issues"].append("related：为空")

    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="讲解层只读审计")
    ap.add_argument("--module", help="只看某个模块前缀，如 10")
    ap.add_argument("--verbose", "-v", action="store_true", help="逐篇打印明细")
    args = ap.parse_args()

    files = oly_files()
    if args.module:
        files = [f for f in files if f.parent.name.startswith(args.module)]
    if not files:
        print("没有匹配的文件", file=sys.stderr)
        return 2

    results = [analyze(f) for f in files]
    total_ex = sum(r["examples"] for r in results)
    tot_exp = sum(r["explicit"] for r in results)
    tot_imp = sum(r["implicit"] for r in results)
    tot_known = sum(len(r["known"]) for r in results)
    tot_miss = sum(len(r["missing"]) for r in results)
    clean = [r for r in results if not r["issues"]]

    print(f"篇数 {len(results)}｜例题 {total_ex} 道")
    print(f"  易错点 ### 标题合规：{sum(1 for r in results if not any('易错点标题' in i for i in r['issues']))}/{len(results)}")
    print(f"  速查卡 ⚠️ 行：    {sum(1 for r in results if not any('速查卡' in i for i in r['issues']))}/{len(results)}")
    print(f"  related 非空：    {sum(1 for r in results if not any('related' in i for i in r['issues']))}/{len(results)}")
    print(f"  思路句（显式问句）：{tot_exp}/{total_ex}")
    print(f"  思路句（隐含策略）：{tot_imp}/{total_ex}")
    print(f"  思路句（人工确认漏判）：{tot_known}/{total_ex}")
    print(f"  疑似缺思路句：     {tot_miss}/{total_ex}")

    if tot_miss:
        print("\n疑似缺思路句（需人工确认）：")
        for r in results:
            for no in r["missing"]:
                print(f"  {r['path'].relative_to(ROOT)} 例{no}")

    if args.verbose:
        print("\n有问题的篇目：")
        for r in results:
            if r["issues"]:
                print(f"  {r['path'].relative_to(ROOT)}")
                for i in r["issues"]:
                    print(f"      - {i}")
    else:
        print(f"\n全部合规 {len(clean)}/{len(results)} 篇（明细加 -v）")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
