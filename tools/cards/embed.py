#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把速查卡内容回写到各知识点 md 的「## 例题」之前。

数据源：tools/cards/content/*.json（卡片唯一真源）
落点  ：content/**/*.md 里 frontmatter id 对应的文件，插在 `## 例题` 之前
幂等  ：以 `<!-- card:auto -->` 起始标记，重跑时整段替换，不会重复堆叠

用法：
  python3 tools/cards/embed.py --dry     # 只报告，不写
  python3 tools/cards/embed.py           # 写入
"""
import sys, os, re, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CONTENT = os.path.join(ROOT, "content")
CARD_DIR = os.path.join(HERE, "content")

MARK = "<!-- card:auto -->"
END_HINT = "<!-- /card:auto -->"

sys.path.insert(0, HERE)
import render  # noqa: E402  复用模块顺序、配色、badge 规则


# ----------------------------------------------------------------------
# 1. id -> badge（与 PDF 卡面左上角编号完全一致）
# ----------------------------------------------------------------------
def id_badge_map():
    items = render.load_items()
    cards = render.pair_cards(items)
    m = {}
    for s in range(0, (len(cards) + 3) // 4):
        chunk = cards[s * 4:(s + 1) * 4]
        for side in ("front", "back"):
            for k, c in enumerate(chunk):
                it = c.get(side)
                if not it:
                    continue
                code = render.MOD_COLOR.get(c["module"], ("", ""))[0]
                m[it["id"]] = "%s %02d%s" % (code, s * 4 + k + 1, "正" if side == "front" else "背")
    return m


# ----------------------------------------------------------------------
# 2. blocks -> markdown
# ----------------------------------------------------------------------
def blocks_to_md(blocks, badge, md_text, title):
    out = [MARK, "## 速查卡", ""]
    out.append("> 裁剪即用：本页对应速查卡「%s」。下面是本节最紧的一版摘要，"
               "公式与结论与正文完全一致，用于做题前扫一遍。全套卡片见 "
               "`tools/cards/build/cards.html`。" % badge)
    out.append("")

    # tip / warn 统一挪到段末，避免夹在条目中间打断阅读
    tips, warns = [], []
    has_err_sec = any(b["t"] == "sec" and "易错" in b["v"] for b in blocks)

    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        t = b["t"]
        v = b["v"]
        if t == "sec":
            out += ["**%s**" % v, ""]
        elif t == "fx":
            out += ["$$%s$$" % v, ""]
        elif t == "li":
            out.append("- %s" % v)
            if i + 1 >= n or blocks[i + 1]["t"] != "li":
                out.append("")
        elif t == "tip":
            tips.append(v)
        elif t == "warn":
            warns.append(v)
        elif t == "fig":
            rel = "/assets/geometry/%s.svg" % v
            if rel not in md_text:          # md 正文已引用过就不重复插图
                out += ["![%s](%s)" % (title, rel), ""]
        i += 1

    quote = []
    for v in tips:
        quote.append("> \u2705 %s" % v)
    for v in warns:
        # 卡片里若已有「易错」小节，这一行只作补充，去掉重复的“易错：”
        if has_err_sec and v.startswith("易错："):
            v = v[len("易错："):]
        quote.append("> \u26a0\ufe0f %s" % v)
    if quote:
        out += quote + [""]

    while out and out[-1] == "":
        out.pop()
    out.append(END_HINT)
    return "\n".join(out) + "\n\n"


# ----------------------------------------------------------------------
# 3. 定位 md
# ----------------------------------------------------------------------
def md_index():
    idx = {}
    for root, _, fs in os.walk(CONTENT):
        for f in fs:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            s = open(p, encoding="utf-8").read()
            m = re.match(r"---\n(.*?)\n---", s, re.S)
            if not m:
                continue
            fm = m.group(1)
            mm = re.search(r"^id:\s*(\S+)", fm, re.M)
            if mm:
                idx[mm.group(1)] = p
    return idx


def insert(md_text, block):
    """把 block 插到 `## 例题` 之前；已有标记则替换旧块。"""
    # 先删旧块（幂等）
    md_text = re.sub(re.escape(MARK) + r".*?" + re.escape(END_HINT) + r"\n*", "", md_text, flags=re.S)

    m = re.search(r"^##\s*例题\s*$", md_text, re.M)
    if m:
        start = m.start()
    else:
        # 没有「例题」：退化为插到第一个 ## 之后？不猜，交回调用方报告
        return None
    return md_text[:start] + block + md_text[start:]


def main():
    dry = "--dry" in sys.argv
    badges = id_badge_map()
    idx = md_index()

    items = []
    for f in sorted(glob.glob(os.path.join(CARD_DIR, "*.json"))):
        items += json.load(open(f, encoding="utf-8"))["items"]

    done, no_md, no_ex = [], [], []
    for it in items:
        p = idx.get(it["id"])
        if not p:
            no_md.append((it["id"], it["title"]))
            continue
        s = open(p, encoding="utf-8").read()
        block = blocks_to_md(it["blocks"], badges.get(it["id"], "?"), s, it["title"])
        new = insert(s, block)
        if new is None:
            no_ex.append((it["id"], it["title"], p))
            continue
        if not dry:
            open(p, "w", encoding="utf-8").write(new)
        done.append((it["id"], it["title"], p))

    print("知识点 %d 个：写入 %d，无 md %d，无「## 例题」%d%s"
          % (len(items), len(done), len(no_md), len(no_ex), "（干跑）" if dry else ""))
    for x in no_md:
        print("  无 md :", x[0], x[1])
    for x in no_ex:
        print("  无例题:", x[0], x[1], x[2])


if __name__ == "__main__":
    main()
