#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""卡片内容静态校验：覆盖度 / 配对一致性 / 容量估算 / LaTeX 子集"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HERE, "content")
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "content"))
MODULES = ["06-奥数-计算", "07-奥数-计数", "08-奥数-数论",
           "09-奥数-几何", "10-奥数-行程", "11-奥数-组合",
           "12-奥数-应用题"]
# 可选模块：卡片只覆盖其中一部分知识点，缺失不算错误
MODULES_OPTIONAL = ["05-应用题"]

ALLOWED_MACROS = {
    "frac", "dfrac", "sqrt", "binom", "pmod", "bmod", "overline", "text",
    "times", "div", "cdot", "pm", "le", "leq", "ge", "geq", "ne", "neq",
    "approx", "equiv", "to", "rightarrow", "Rightarrow", "angle", "triangle",
    "square", "parallel", "perp", "sim", "cong", "alpha", "beta", "gamma",
    "theta", "pi", "lambda", "mu", "varphi", "cdots", "ldots", "dots", "in",
    "infty", "degree", "circ", "quad", "qquad", "left", "right", "displaystyle",
    "limits", "Delta", "Sigma", "Omega", "cap", "cup", "varnothing",
}
ALLOWED_CHARS = {"\\{", "\\}", "\\%", "\\$", "\\,", "\\;", "\\!", "\\ "}


def est_width(text):
    """粗略估算一段文本渲染后的字符宽度（中文字符=1，公式内按符号折算）"""
    w = 0.0
    in_math = False
    for ch in text:
        if ch == "$":
            in_math = not in_math
            continue
        if ord(ch) > 0x2E80:
            w += 1.0
        elif in_math:
            w += 0.55
        elif ch.isalpha():
            w += 0.55
        elif ch.isdigit():
            w += 0.55
        else:
            w += 0.45
    return w


def est_lines(blocks):
    """估算显示行数（每行约 40 字符宽）"""
    total = 0.0
    for b in blocks:
        t = b.get("t", "li")
        v = b.get("v", "")
        if t == "sec":
            total += 1.25
        elif t == "fx":
            total += 1.45
        elif t in ("warn", "tip"):
            total += max(1.0, round(est_width(v) / 38.0 + 0.45))
        elif t == "fig":
            # 图浮在右侧约占 5 行高度，且正文被挤到 68% 宽 -> 等效约 4 行
            total += 4.0
        else:
            total += max(1.0, round(est_width(v) / 38.0 + 0.45))
    return total


def main():
    # 1) 源知识点清单（id 从 frontmatter 取）
    expected = {}
    opt_ids = set()
    for m in MODULES:
        for f in glob.glob(os.path.join(SRC, m, "*.md")):
            head = open(f, encoding="utf-8").read(2000)
            mid = re.search(r"^id:\s*(\S+)", head, re.M)
            tit = re.search(r"^title:\s*(.+)$", head, re.M)
            expected[mid.group(1)] = (m, tit.group(1).strip())
    for m in MODULES_OPTIONAL:
        for f in glob.glob(os.path.join(SRC, m, "*.md")):
            head = open(f, encoding="utf-8").read(2000)
            mid = re.search(r"^id:\s*(\S+)", head, re.M)
            opt_ids.add(mid.group(1))

    items = []
    for f in sorted(glob.glob(os.path.join(CONTENT_DIR, "[0-9]*.json"))):
        data = json.load(open(f, encoding="utf-8"))
        for it in data["items"]:
            it["_f"] = os.path.basename(f)
            it["_mdir"] = data["module_dir"]
            items.append(it)
    ids = {i["id"] for i in items}
    print("== 覆盖度 ==")
    missing = sorted(set(expected) - ids)
    extra = sorted(ids - set(expected) - opt_ids)
    print("必覆盖知识点 %d，已有卡片 %d" % (len(expected), len(ids) - len(ids & opt_ids)))
    if missing:
        print("!! 缺失:", missing)
    if extra:
        print("!! 多余(不在源清单):", extra)
    opt_used = sorted(ids & opt_ids)
    if opt_used:
        print("可选模块(05-应用题)已收录 %d 个：%s" % (len(opt_used), "、".join(opt_used)))

    print("\n== 配对一致性 ==")
    by_id = {i["id"]: i for i in items}
    bad = 0
    for it in items:
        p = it.get("pair_with")
        if not p:
            continue
        if p not in by_id:
            print("!! %s pair_with=%s 不存在" % (it["id"], p)); bad += 1
        elif by_id[p].get("pair_with") != it["id"]:
            print("!! %s ↔ %s 非双向" % (it["id"], p)); bad += 1
        elif by_id[it["id"]]["_mdir"] != by_id[p]["_mdir"]:
            print("!! %s ↔ %s 跨模块" % (it["id"], p)); bad += 1
    if not bad:
        print("OK")

    print("\n== 容量估算（>16 行需复核）==")
    over = []
    for it in items:
        blocks = it.get("blocks") or it.get("front_blocks", [])
        n = est_lines(blocks)
        if it.get("span") == 2:
            n2 = est_lines(it.get("back_blocks", []))
            flag = "F%.1f/B%.1f" % (n, n2)
            if n > 16.5 or n2 > 16.5:
                over.append((it, flag))
        else:
            flag = "%.1f" % n
            if n > 16.5:
                over.append((it, flag))
        it["_est"] = n
    for it, flag in sorted(over, key=lambda x: -x[0]["_est"]):
        print("!! %-40s %s 行 (%s)" % (it["title"], flag, it["_f"]))
    if not over:
        print("OK（全部 ≤16.5 行）")

    print("\n== LaTeX 子集检查 ==")
    bad_ltx = 0
    for it in items:
        for key in ("blocks", "front_blocks", "back_blocks"):
            for b in it.get(key, []) or []:
                v = b.get("v", "")
                for mch in re.finditer(r"\\([a-zA-Z]+|.)", v):
                    tok = mch.group(1)
                    if tok not in ALLOWED_MACROS and ("\\" + tok) not in ALLOWED_CHARS:
                        print("!! %s: 不支持宏 \\%s  in  %s" % (it["id"], tok, v[:60]))
                        bad_ltx += 1
                if "$$" in v:
                    print("!! %s: 含 $$" % it["id"]); bad_ltx += 1
                if b.get("t") == "fx" and "$" in v:
                    print("!! %s: fx 不应带 $" % it["id"]); bad_ltx += 1
    if not bad_ltx:
        print("OK")

    print("\n== span 统计 ==")
    full = [i["title"] for i in items if i.get("span") == 2]
    print("span=2:", full if full else "无")


if __name__ == "__main__":
    main()
