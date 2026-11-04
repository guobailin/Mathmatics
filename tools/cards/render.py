#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小学奥数知识点速查卡 · 排版生成器
输入: content/*.json  (卡片内容)
输出: build/cards.html  (A4 横向打印，2x2 卡片，支持双面正反对齐)

用法:
    python3 render.py            # 生成 html
    python3 render.py --pdf      # 同时用 Chrome headless 打印 pdf
    python3 render.py --check    # 溢出检查
"""
import glob
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HERE, "content")
BUILD_DIR = os.path.join(HERE, "build")
# 速查卡专用小画布示意图（由 tools/figures/style.py 的 save() 一并产出）
ASSETS_CARD = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                           "assets", "geometry", "cards")


def load_svg(name, prefix):
    """内联读取卡片版 SVG；剥离 xml 头与 metadata，并重命名内部 id 避免同页多图冲突。"""
    p = os.path.join(ASSETS_CARD, name + ".svg")
    if not os.path.exists(p):
        return ""
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"<\?xml.*?\?>", "", s, flags=re.S)
    s = re.sub(r"<!DOCTYPE.*?>", "", s, flags=re.S)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', s)):
        s = s.replace('id="%s"' % i, 'id="%s_%s"' % (prefix, i))
        s = s.replace("url(#%s)" % i, "url(#%s_%s)" % (prefix, i))
    return s.strip()

# ---------------- A4 landscape 参数 (mm) ----------------
PAGE_W, PAGE_H = 297.0, 210.0
CARD_W, CARD_H = 130.0, 90.0
# 外边距 12/10，卡片之间留裁剪余量
MX = (PAGE_W - 2 * CARD_W) / 3.0      # 水平三等分 -> 12.33
MY = (PAGE_H - 2 * CARD_H) / 3.0      # 垂直三等分 -> 10.0
SLOTS = [(MX, MY), (MX * 2 + CARD_W, MY), (MX, MY * 2 + CARD_H), (MX * 2 + CARD_W, MY * 2 + CARD_H)]

# 每页 4 张卡；相邻两页互为一张纸的正反面（页面为奇数 index=正面）
MODULES = [
    ("12-奥数-应用题", "应用题", "#7A5C3E"),
    ("06-奥数-计算", "计算", "#B4531F"),
    ("07-奥数-计数", "计数", "#8A4B8F"),
    ("08-奥数-数论", "数论", "#1F5C99"),
    ("09-奥数-几何", "几何", "#1E7A5A"),
    ("10-奥数-行程", "行程", "#A0323C"),
    ("11-奥数-组合", "组合", "#55603A"),
]
MOD_COLOR = {m[0]: (m[1], m[2]) for m in MODULES}


# ------------------------------------------------------------------
# 极简 LaTeX -> HTML（离线、无外部依赖）
# ------------------------------------------------------------------
SYMBOLS = {
    r"\times": "&#215;", r"\div": "&#247;", r"\cdot": "&#183;", r"\pm": "&#177;",
    r"\le": "&#8804;", r"\le ": "&#8804;", r"\leq": "&#8804;", r"\ge": "&#8805;", r"\geq": "&#8805;",
    r"\ne": "&#8800;", r"\neq": "&#8800;", r"\approx": "&#8776;", r"\equiv": "&#8801;",
    r"\dots": "&#8230;", r"\ldots": "&#8230;", r"\cdots": "&#8943;",
    r"\to": "&#8594;", r"\rightarrow": "&#8594;", r"\Rightarrow": "&#8658;",
    r"\Rightarrow": "&#8658;", r"\in": "&#8712;", r"\infty": "&#8734;",
    r"\angle": "&#8736;", r"\triangle": "&#9651;", r"\square": "&#9633;",
    r"\parallel": "&#8741;", r"\perp": "&#8869;", r"\sim": "&#8764;", r"\cong": "&#8773;",
    r"\alpha": "&#945;", r"\beta": "&#946;", r"\gamma": "&#947;", r"\theta": "&#952;",
    r"\pi": "&#960;", r"\lambda": "&#955;", r"\mu": "&#956;", r"\varphi": "&#966;",
    r"\Delta": "&#916;", r"\Sigma": "&#931;", r"\Omega": "&#937;",
    r"\cap": "&#8745;", r"\cup": "&#8746;", r"\varnothing": "&#8709;",
    r"\degree": "&#176;", r"\circ": "&#176;",
    r"\ge0": "&#8805;0",
    r"\qquad": "  ", r"\quad": " ", r"\;": " ", r"\,": " ", r"\!": "", r"\ ": " ",
    r"\{": "{", r"\}": "}", r"\%": "%", r"\$": "$",
    r"\left": "", r"\right": "", r"\displaystyle": "", r"\limits": "",
}
LONG_MACROS = [r"\dfrac", r"\frac", r"\sqrt", r"\text", r"\overline", r"\binom", r"\bmod", r"\pmod"]


def _take_group(s, i):
    """s[i] == '{'，返回 (内容, 结束索引后一位)"""
    assert s[i] == "{"
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def latex2html(s):
    """把行内 LaTeX 转成 HTML。返回 str。"""
    if s is None:
        return ""
    if "$" in s:
        # 处理行内公式与文本混排：$...$ 走公式，其余转义
        parts = re.split(r"(\$[^$]*\$)", s)
        out = []
        for p in parts:
            if p.startswith("$") and p.endswith("$") and len(p) > 1:
                out.append(_conv(p[1:-1]))
            else:
                out.append(_html.escape(p))
        return "".join(out)
    return _conv(s)


def _conv(s):
    """纯 LaTeX 片段 -> HTML"""
    out, i = [], 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+|.)", s[i:])
            if not m:
                out.append("\\")
                i += 1
                continue
            tok = "\\" + m.group(1)
            rest = i + len(tok)
            if tok in LONG_MACROS and rest < n and s[rest] == "{":
                # 双参数宏
                a, j = _take_group(s, rest)
                if tok in (r"\frac", r"\dfrac", r"\binom"):
                    if j < n and s[j] == "{":
                        b, k = _take_group(s, j)
                    else:
                        b, k = s[j:j + 1], j + 1
                    if tok == r"\binom":
                        out.append(
                            '<span class="paren">(</span><span class="binom">'
                            '<span class="bn">%s</span><span class="bd">%s</span></span>'
                            '<span class="paren">)</span>' % (_conv(a), _conv(b)))
                    else:
                        out.append('<span class="frac"><span class="num">%s</span>'
                                   '<span class="den">%s</span></span>'
                                   % (_conv(a), _conv(b)))
                    i = k
                    continue
                if tok == r"\sqrt":
                    out.append('<span class="sqrt"><span class="rad">&#8730;</span>'
                               '<span class="radi">%s</span></span>' % _conv(a))
                    i = j
                    continue
                if tok == r"\text":
                    out.append(_html.escape(a))
                    i = j
                    continue
                if tok == r"\overline":
                    out.append('<span class="ol">%s</span>' % _conv(a))
                    i = j
                    continue
                if tok in (r"\bmod", r"\pmod"):
                    out.append('<span class="op">(mod %s)</span>' % _conv(a))
                    i = j
                    continue
            # 单字符 / 单参数
            if tok == r"\frac" and rest < n:  # \frac12 形式
                a, j = s[rest], rest + 1
                b, k = s[j], j + 1
                out.append('<span class="frac"><span class="num">%s</span>'
                           '<span class="den">%s</span></span>' % (a, b))
                i = k
                continue
            if tok in SYMBOLS:
                out.append(SYMBOLS[tok])
                i = rest
                continue
            # \underbrace{}_{}? 忽略
            i = rest
            continue
        if c in "{":
            grp, j = _take_group(s, i)
            out.append(_conv(grp))
            i = j
            continue
        if c == "}":
            i += 1
            continue
        if c in "^_":
            if i + 1 < n and s[i + 1] == "{":
                grp, j = _take_group(s, i + 1)
                body = _conv(grp)
            else:
                mm = re.match(r"\\[a-zA-Z]+|.", s[i + 1:])
                body = _conv(mm.group(0)) if mm else ""
                j = i + 1 + (len(mm.group(0)) if mm else 0)
            out.append('<sup>%s</sup>' % body if c == "^" else '<sub>%s</sub>' % body)
            i = j
            continue
        if c.isalpha():
            out.append('<i>%s</i>' % c)
            i += 1
            continue
        if c == " ":
            out.append(" ")
            i += 1
            continue
        out.append(_html.escape(c))
        i += 1
    return "".join(out)


# ------------------------------------------------------------------
# CSS
# ------------------------------------------------------------------
CSS = """
@page { size: 297mm 210mm; margin: 0; }
html, body { margin: 0; padding: 0; background: #fff; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }
body { font-family: "PingFang SC", "Hiragino Sans GB", "Heiti SC", STHeiti,
       "Microsoft YaHei", sans-serif; color: #1b1b1b; }

.page { position: relative; width: 297mm; height: 210mm; overflow: hidden;
        page-break-after: always; background: #fff; }
.page:last-child { page-break-after: auto; }
.guide { position: absolute; border-top: 0.15mm dashed #c9ccd1; left: 0; right: 0; height: 0; }
.guide-v { position: absolute; border-left: 0.15mm dashed #c9ccd1; top: 0; bottom: 0; width: 0; }
.pmark { position: absolute; font-size: 6pt; color: #9aa0a6; letter-spacing: .05em; }

.card { position: absolute; width: 130mm; height: 90mm; border: 0.35mm solid #2b2b2b;
        background: #fff; padding: 3.8mm 4.6mm 3.2mm 4.6mm; border-radius: 1.2mm;
        overflow: hidden; }
.c-head { display: flex; align-items: baseline; justify-content: space-between;
          border-bottom: 0.4mm solid currentColor; padding-bottom: 0.8mm; margin-bottom: 1.6mm; }
.c-badge { font-size: 6.8pt; letter-spacing: .06em; opacity: .85; white-space: nowrap; }
.c-title { font-size: 11.5pt; font-weight: 700; text-align: right; line-height: 1.15; }
.c-body { font-size: 8.1pt; line-height: 1.45; }

.sec { font-weight: 700; font-size: 7.9pt; margin: 2.0mm 0 0.8mm; letter-spacing: .02em;
       border-left: 0.9mm solid currentColor; padding-left: 1.4mm; line-height: 1.3; }
.card > .c-body > .sec:first-child { margin-top: 0; }

.li { display: flex; margin: 0.4mm 0; align-items: baseline; }
.li .dot { flex: 0 0 2.6mm; }
.li .txt { flex: 1 1 auto; }

.fx { text-align: center; margin: 1.0mm 0; font-size: 9.2pt; }
.fig { float: right; width: 34mm; margin: 0.3mm 0 0.6mm 2.6mm; }
.fig svg { display: block; width: 100%; height: auto; }
.c-body::after { content: ""; display: block; clear: both; }
.warn { margin: 0.6mm 0; font-size: 7.4pt; color: #b3261e; }
.warn::before { content: "\\26A0\\FE0E\\2009"; }
.tip { margin: 0.6mm 0; font-size: 7.4pt; color: #0b6b3a; }
.tip::before { content: "\\2714\\FE0E\\2009"; }
.key { background: rgba(0,0,0,.055); padding: 0 .4mm; border-radius: .6mm; }

i { font-family: "Times New Roman", "Songti SC", Georgia, serif; font-style: italic;
    padding: 0 .12mm; }
sup, sub { font-size: .72em; font-family: Georgia, serif; }
sup { vertical-align: super; } sub { vertical-align: sub; }
.frac { display: inline-flex; flex-direction: column; vertical-align: middle;
        text-align: center; margin: 0 .35mm; }
.frac .num { border-bottom: 0.3mm solid currentColor; padding: 0 .5mm; }
.frac .den { padding: 0 .5mm; }
.sqrt { display: inline-flex; align-items: stretch; vertical-align: middle; }
.rad { font-family: Georgia, serif; }
.radi { border-top: 0.3mm solid currentColor; padding: 0 .4mm; margin-top: .2mm; }
.ol { border-top: 0.3mm solid currentColor; }
.binom { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; }
.paren { font-family: Georgia, serif; }

/* 屏幕专用打印提示条：@media print 下整条移除，不影响出纸与 PDF */
.hint { margin: 0; padding: 2.4mm 6mm 2.2mm; background: #FFF6E0;
        border-bottom: 0.5mm solid #E3A93F; color: #463306;
        font-size: 9pt; line-height: 1.6; }
.hint b { font-size: 9.6pt; letter-spacing: .02em; }
.hint .k { background: #fff; border: 0.25mm solid #E3A93F; border-radius: .9mm;
           padding: 0 1.4mm; margin: 0 .5mm; white-space: nowrap; }
.hint .hn { display: block; margin-top: .8mm; color: #6B5A33; font-size: 8pt; }
.hint a { color: #8A5A00; }
@media print { .hint { display: none !important; } }
"""

HTML_TPL = """<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title><style>{css}</style></head>
<body>{pages}</body></html>"""

HINT_TPL = (
    '<div class="hint">'
    '<b>打印设置</b>（Ctrl / &#8984; + P）：'
    '<span class="k">纸张 A4</span>'
    '<span class="k">方向 横向</span>'
    '<span class="k">边距 无</span>'
    '<span class="k">缩放 100%</span>'
    '<span class="k">取消「页眉和页脚」</span>'
    '<span class="k">双面 沿长边翻转</span>'
    '<span class="hn">共 {n_items} 个知识点 / {n_cards} 张卡 / {n_sheets} 张 A4（正反）。'
    '尺寸已固定，优先打印 <a href="cards.pdf">cards.pdf</a>；'
    '用本页打印务必按上面设置——缩放一改（如“适合页面”）卡片就缩到约 126mm、裁切线错位，'
    '边距一改就会每张纸后多出一页空白。本提示条不会被打印出来。</span>'
    '</div>')


def hint_html(n_items, n_cards, n_sheets):
    return HINT_TPL.format(n_items=n_items, n_cards=n_cards, n_sheets=n_sheets)


def render_card(item, module_dir, side_label, idx_label):
    """渲染单张卡片的一个面"""
    meta = MOD_COLOR.get(module_dir, (module_dir, "#333"))
    code, color = meta
    b = ['<div class="card" style="color:%s">' % color]
    b.append('<div class="c-head" style="color:%s">'
             '<span class="c-badge">%s</span>'
             '<span class="c-title">%s</span></div>'
             % (color, idx_label, _html.escape(item["title"])))
    body = []
    for blk in item.get("blocks", []):
        t = blk.get("t", "li")
        v = blk.get("v", "")
        if t == "sec":
            body.append('<div class="sec" style="color:%s">%s</div>' % (color, _html.escape(v)))
        elif t == "fx":
            body.append('<div class="fx">%s</div>' % latex2html(v))
        elif t == "warn":
            body.append('<div class="warn">%s</div>' % latex2html(v))
        elif t == "tip":
            body.append('<div class="tip">%s</div>' % latex2html(v))
        elif t == "fig":
            svg = load_svg(v, "g_" + re.sub(r"\W", "_", v))
            if svg:
                body.append('<div class="fig">%s</div>' % svg)
        else:
            body.append('<div class="li"><span class="dot">&#183;</span>'
                        '<span class="txt">%s</span></div>' % latex2html(v))
    b.append('<div class="c-body">%s</div>' % "".join(body))
    b.append("</div>")
    return "".join(b)


def build_pages(cards):
    """
    cards: list of dict {module, front: item, back: item|None}
    一张 A4 纸 = 正面页(4 张卡的正面) + 背面页(同 4 张卡的背面)，
    slot 坐标完全一致 -> 双面长边翻转打印后正反面严格背对背。
    """
    pages = []
    total = len(cards)
    n_sheets = (total + 3) // 4
    for s in range(n_sheets):
        chunk = cards[s * 4:(s + 1) * 4]
        for side in ("front", "back"):
            b = ['<div class="page">']
            # 裁剪辅助虚线（居中十字）
            b.append('<div class="guide" style="top:%smm"></div>' % round(PAGE_H / 2, 2))
            b.append('<div class="guide-v" style="left:%smm"></div>' % round(PAGE_W / 2, 2))
            sheet_no = s + 1
            label = "第 %d 张纸 · %s（正面 %s，背面 %s）" % (
                sheet_no, "正面" if side == "front" else "背面",
                "、".join(c["front"]["title"] for c in chunk),
                "、".join((c["back"]["title"] if c.get("back") else "空白") for c in chunk))
            pos = "bottom"
            b.append('<div class="pmark" style="%s:3mm;left:12mm">%s</div>' % (pos, label))
            for k, c in enumerate(chunk):
                x, y = SLOTS[k]
                it = c.get(side) or ({"title": "—", "blocks": []} if side == "back" else None)
                if it is None:
                    continue
                idx = "%s %02d%s" % (MOD_COLOR.get(c["module"], ("", ""))[0],
                                     s * 4 + k + 1, "正" if side == "front" else "背")
                b.append('<div style="position:absolute;left:%smm;top:%smm">%s</div>'
                         % (round(x, 2), round(y, 2),
                            render_card(it, c["module"], side, idx)))
            # 补齐空 slot 的占位框（背面页可能有空卡），便于裁剪
            b.append("</div>")
            pages.append("".join(b))
    return pages


def load_items():
    items = []
    for f in sorted(glob.glob(os.path.join(CONTENT_DIR, "*.json"))):
        data = json.load(open(f, encoding="utf-8"))
        mdir = data.get("module_dir")
        for it in data.get("items", []):
            it["_module_dir"] = mdir
            it["_file"] = os.path.basename(f)
            items.append(it)
    return items


def pair_cards(items):
    """
    配对：把 items 按 pair_with 字段（同一模块内相邻）两两配成一张卡的正面/背面。
    span=2 的知识点独占一张卡（front_blocks / back_blocks 拆成正反面）。
    """
    order = []
    seen = set()
    for it in items:
        if it["id"] in seen:
            continue
        if it.get("span") == 2:
            seen.add(it["id"])
            front = dict(it, blocks=it.get("front_blocks", it.get("blocks", [])))
            back = dict(it, blocks=it.get("back_blocks", []),
                        title=it["title"] + "（续）")
            order.append({"module": it["_module_dir"], "front": front,
                          "back": back, "_full": True})
            continue
        partner = None
        pid = it.get("pair_with")
        if pid:
            for cand in items:
                if cand["id"] == pid and cand["id"] not in seen:
                    partner = cand
                    break
        if partner is not None:
            seen.add(it["id"])
            seen.add(partner["id"])
            order.append({"module": it["_module_dir"], "front": it, "back": partner})
        else:
            seen.add(it["id"])
            order.append({"module": it["_module_dir"], "front": it, "back": None})
    return order


def main():
    items = load_items()
    cards = pair_cards(items)
    print("知识点 %d 个 -> 卡片 %d 张 -> A4 %d 张（正反打印）"
          % (len(items), len(cards), (len(cards) + 3) // 4))
    # 校验：是否有遗漏/孤儿
    ids = [i["id"] for i in items]
    dup = [i for i in set(ids) if ids.count(i) > 1]
    if dup:
        print("!! 重复 id:", dup)
    pages = build_pages(cards)
    os.makedirs(BUILD_DIR, exist_ok=True)
    hint = hint_html(len(items), len(cards), (len(cards) + 3) // 4)
    body = hint + "".join(pages)
    out = os.path.join(BUILD_DIR, "cards.html")
    open(out, "w", encoding="utf-8").write(
        HTML_TPL.format(title="小学奥数知识点速查卡", css=CSS, pages=body))
    print("HTML ->", out)

    if "--check" in sys.argv:
        js = """
<script>
window.addEventListener('load', function(){
  var bad = [];
  document.querySelectorAll('.card').forEach(function(c){
    var title = c.querySelector('.c-title');
    title = title ? title.textContent.trim() : '?';
    if (c.scrollHeight > c.clientHeight + 1 || c.scrollWidth > c.clientWidth + 1) {
      c.style.outline = '1.5mm solid red';
      bad.push(title + ' h' + (c.scrollHeight - c.clientHeight));
    }
  });
  document.body.setAttribute('data-overflow', bad.join(' | '));
  document.title = 'OV:' + bad.length;
});
</script>"""
        chk = os.path.join(BUILD_DIR, "check.html")
        open(chk, "w", encoding="utf-8").write(
            HTML_TPL.format(title="check", css=CSS, pages=body).replace(
                "</body>", js + "</body>"))
        chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser") or "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                            "--virtual-time-budget=12000", "--dump-dom",
                            "file://" + chk],
                           capture_output=True, text=True, timeout=180)
        m = re.search(r'data-overflow="([^"]*)"', r.stdout)
        msg = m.group(1) if m else "?(未取到)"
        print("溢出卡片:", msg if msg else "无")

    if "--pdf" in sys.argv:
        pdf = os.path.join(BUILD_DIR, "cards.pdf")
        chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
               "--run-all-compositor-stages-before-draw",
               "--virtual-time-budget=8000",
               "--print-to-pdf=%s" % pdf, "--no-pdf-header-footer",
               "file://" + out]
        if os.path.exists(pdf):
            os.remove(pdf)
        subprocess.run(cmd, capture_output=True, timeout=180)
        print("PDF  ->", pdf, os.path.getsize(pdf) if os.path.exists(pdf) else "失败")


if __name__ == "__main__":
    main()
