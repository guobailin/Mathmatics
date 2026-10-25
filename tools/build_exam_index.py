#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总 8 套真题解答，生成 exam/SUMMARY.md，并把「竞赛真题中的考察」写回知识点正文。"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402

EXAM = ROOT / "exam"
ANSWERS = EXAM / "answers"

PAPERS = [
    ("2024年秋季走美六年级-学生版", "2024 秋·走美", 48),
    ("2025年春季走美六年级-学生版", "2025 春·走美", 49),
    ("2025年秋季走美六年级-学生版", "2025 秋·走美", 50),
    ("2026年春季走美六年级-学生版", "2026 春·走美", 51),
    ("第28届WMO六年级试卷", "第 28 届 WMO", 52),
    ("第30届WMO六年级试卷", "第 30 届 WMO", 53),
    ("第32届WMO六年级试卷", "第 32 届 WMO", 60),
    ("第34届WMO六年级试卷", "第 34 届 WMO", 61),
]
ORDER = {name: i for i, (name, _, _) in enumerate(PAPERS)}
SHORT = {name: short for name, short, _ in PAPERS}
ISSUE = {name: issue for name, _, issue in PAPERS}

ALIAS = {
    "乘法分配律": "乘法运算定律",
    "余数问题物不知数": "余数问题（物不知数）",
    "图形的运动（折叠）": "图形的运动（三）",
    "环形跑道（周期问题）": "环形跑道",
    "百分数应用题": "百分数应用题（折扣与成数）",
    "观察物体（三）——主视图": "观察物体（三）",
    "解方程": "认识方程与解方程",
    "解方程与等式的性质": "等式的性质",
}


def load_answers():
    data = []
    for name, short, issue in PAPERS:
        md = ANSWERS / f"{name}.md"
        js = ANSWERS / f"{name}.json"
        if not js.exists():
            print("!! missing", js)
            continue
        d = json.loads(js.read_text(encoding="utf-8"))
        d["_name"] = name
        d["_short"] = short
        d["_issue"] = issue
        d["_md"] = md
        data.append(d)
    return data


def stars(n):
    try:
        n = int(n)
    except Exception:
        return ""
    return "★" * max(1, min(n, 7))


def clean_method(s, limit=90):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    s = s.replace("|", "\\|")
    if len(s) > limit:
        s = s[:limit].rstrip("，。；; ") + "…"
    return s


def norm_title(t, titles):
    t = str(t or "").strip()
    if t in titles:
        return t
    if t in ALIAS and ALIAS[t] in titles:
        return ALIAS[t]
    return None


def main():
    data = load_answers()
    kps, _, _ = build.load_knowledge_points()
    by_title = {k["title"]: k for k in kps}
    titles = set(by_title)

    entries = defaultdict(list)
    unmatched = Counter()
    total_q = 0
    know_count = Counter()
    diff_count = Counter()
    for d in data:
        total_q += d.get("total", 0)
        for it in d.get("items", []):
            qno = str(it.get("no"))
            diff = it.get("difficulty", 3)
            diff_count[int(diff) if str(diff).isdigit() else 3] += 1
            seen = set()
            for tag in it.get("knowledge", []):
                if tag in seen:
                    continue
                seen.add(tag)
                know_count[tag] += 1
                title = norm_title(tag, titles)
                if not title:
                    unmatched[tag] += 1
                    continue
                entries[title].append({
                    "paper": d["_name"],
                    "short": d["_short"],
                    "issue": d["_issue"],
                    "qno": qno,
                    "method": clean_method(it.get("method")),
                    "diff": stars(diff),
                })

    for title in entries:
        entries[title].sort(key=lambda e: (ORDER.get(e["paper"], 99),
                                           int(e["qno"]) if e["qno"].isdigit() else 999))

    # ---------- exam/SUMMARY.md ----------
    lines = ["# 真题考察总结", ""]
    lines.append(f"本目录 8 套六年级竞赛真题，共 **{total_q} 题**；逐题解答在 `exam/answers/`，"
                 "每个知识点正文末尾的「竞赛真题中的考察」只保留与该知识点相关的题目索引。")
    lines += ["", "## 试卷一览", "",
              "| 试卷 | 题量 | 解答 | Issue |",
              "|---|---:|---|---|"]
    for d in data:
        lines.append(f"| {d['_short']} | {d.get('total', 0)} | "
                     f"[{d['_name']} 解答](answers/{d['_name']}.md) | #{d['_issue']} |")
    lines += ["", "## 高频知识点", "", "| 知识点 | 出现题数 |", "|---|---:|"]
    for tag, n in know_count.most_common(30):
        title = norm_title(tag, titles)
        label = f"[{title}](../{by_title[title]['file']})" if title else tag
        lines.append(f"| {label} | {n} |")
    lines += ["", "## 难度分布", ""]
    for star in range(1, 8):
        if diff_count[star]:
            lines.append(f"- {stars(star)}：{diff_count[star]} 题")
    lines += ["", "## 思路总结", ""]
    lines += [
        "- **最值/极端**：先估上界或下界，再构造达到；常见于数字谜、抽屉、组合最值。",
        "- **分类枚举**：按余数、奇偶、大小、位置分类，做到不重不漏。",
        "- **构造与反例**：证明“最多/至少”时，构造与上界缺一不可。",
        "- **不变量与奇偶**：操作类问题先找总量、奇偶、余数不变量。",
        "- **比例与方程**：经济、浓度、行程、面积比常化为比或方程。",
        "- **图形割补**：圆/扇形、三视图、表面积与展开图，先定几何关系再算。",
        "- **递推与归纳**：数列、周期、操作次数，先算小情形找规律。",
        "- **抽屉原理**：存在性问题先找“抽屉”，再构造反例说明边界。",
    ]
    if unmatched:
        lines += ["", "## 未直接对应到知识点标题的标签", "",
                  "这些标签可归入相近知识点，暂未自动写回正文：", ""]
        for tag, n in unmatched.most_common():
            lines.append(f"- {tag}（{n} 题）")
    lines += ["", "> 生成脚本：`tools/build_exam_index.py`。"]
    (EXAM / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")

    # ---------- 写回知识点 ----------
    changed = 0
    for title, items in entries.items():
        kp = by_title[title]
        path = ROOT / kp["file"]
        text = path.read_text(encoding="utf-8")
        # 去掉旧 section（从 ## 竞赛真题 到下一个 ## 或文件末）
        text = re.sub(r"\n## 竞赛真题.*?(?=\n## |\Z)", "\n", text, flags=re.S).rstrip() + "\n"
        lines = ["", "## 竞赛真题中的考察", ""]
        for e in items:
            method = f"：{e['method']}" if e["method"] else ""
            lines.append(f"- **{e['short']} 第 {e['qno']} 题**{method}（{e['diff']}）")
        lines += ["", "> 完整题目与解答见仓库 `exam/answers/` 对应试卷文件；"
                  "跨卷汇总见 `exam/SUMMARY.md`。", ""]
        section = "\n".join(lines)
        if "\n## 例题" in text:
            text = text.replace("\n## 例题", section + "\n## 例题", 1)
        else:
            text += section
        path.write_text(text, encoding="utf-8")
        changed += 1

    print(f"papers={len(data)} questions={total_q} topics_changed={changed} "
          f"unmatched_tags={len(unmatched)}")
    print("summary:", EXAM / "SUMMARY.md")


if __name__ == "__main__":
    main()
