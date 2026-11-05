#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把单张卡渲染到一张 A4 横向纸上（130×90mm，居中，带四角裁切标记），直接出可打印 PDF。

与主卡库的关系：卡源放在 tools/cards/extra/，不进 tools/cards/content/，
因此不会改变主册的页序与卡编号（主册 55 张卡的分页保持不变）。

用法：
  python3 tools/cards/render_one.py extra/equation-types.json
  python3 tools/cards/render_one.py extra/equation-types.json --png
"""
import sys, os, re, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render  # noqa: E402

PAGE_W, PAGE_H = 297.0, 210.0
CARD_W, CARD_H = 130.0, 90.0
LEFT = (PAGE_W - CARD_W) / 2.0      # 83.5
TOP = (PAGE_H - CARD_H) / 2.0       # 60
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 让 render_card 能取到模块配色：code 用于角标，color 用于标题与分隔线
render.MOD_COLOR.setdefault("02-代数初步", ("代数", "#3A5A8C"))

NOTE_CSS = """
.cutnote { position: absolute; left: 0; right: 0; text-align: center;
           font-size: 7pt; color: #8a8f96; letter-spacing: .02em; }
"""


def mark_lines():
    """四角裁切标记：每个角两条短线，位于卡片外侧。"""
    seg = []
    L, G = 7.0, 2.0
    x0, y0, x1, y1 = LEFT, TOP, LEFT + CARD_W, TOP + CARD_H

    def h(xa, xb, y):
        seg.append('<div style="position:absolute;left:%.2fmm;top:%.2fmm;width:%.2fmm;'
                   'border-top:0.2mm solid #b8bcc2"></div>' % (xa, y, xb - xa))

    def v(ya, yb, x):
        seg.append('<div style="position:absolute;left:%.2fmm;top:%.2fmm;height:%.2fmm;'
                   'border-left:0.2mm solid #b8bcc2"></div>' % (x, ya, yb - ya))

    for x in (x0, x1):
        for y in (y0, y1):
            sx = -1 if x == x0 else 1
            sy = -1 if y == y0 else 1

            def f(v_, base, s):
                a, b = base + s * G, base + s * (G + L)
                return (min(a, b), max(a, b))

            xa, xb = f(None, x, sx)
            h(xa, xb, y)
            ya, yb = f(None, y, sy)
            v(ya, yb, x)
    return "".join(seg)


def build_page(item):
    card = render.render_card(item, "02-代数初步", "正", item.get("badge", "代数 · 方程"))
    note = ('<div class="cutnote" style="top:{top:.2f}mm">'
            '13 × 9 cm 速查卡　·　沿四角标记裁切　·　'
            '打印：A4 横向 / 边距「无」/ 缩放 100%</div>').format(top=TOP + CARD_H + 8)
    return ('<div class="page">%s'
            '<div style="position:absolute;left:%.2fmm;top:%.2fmm">%s</div>%s</div>'
            % (mark_lines(), LEFT, TOP, card, note))


def main():
    if len(sys.argv) < 2:
        sys.exit("用法: python3 render_one.py <extra/xxx.json> [--png]")
    src = sys.argv[1]
    if not os.path.isabs(src):
        src = os.path.join(HERE, src)
    data = json.load(open(src, encoding="utf-8"))
    item = data["items"][0]

    outdir = os.path.join(HERE, "build")
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0]

    page = build_page(item)
    html = render.HTML_TPL.format(
        title=item["title"], css=render.CSS + NOTE_CSS, pages=page)
    html_path = os.path.join(outdir, stem + ".html")
    open(html_path, "w", encoding="utf-8").write(html)

    # 溢出实测：同一套判定，scrollHeight 超出即报警
    js = """<script>
window.addEventListener('load', function(){
  var c = document.querySelector('.card'); var t = c.querySelector('.c-title');
  document.body.setAttribute('data-ov',
    (c.scrollHeight - c.clientHeight) + '|' + (c.clientWidth - c.scrollWidth) + '|' + t.textContent.trim());
});</script>"""
    chk = os.path.join(outdir, stem + "_check.html")
    open(chk, "w", encoding="utf-8").write(html.replace("</body>", js + "</body>"))
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--virtual-time-budget=8000", "--dump-dom", "file://" + chk],
                       capture_output=True, text=True, timeout=180)
    m = re.search(r'data-ov="([^"]*)"', r.stdout)
    if m:
        dh, dw, title = m.group(1).split("|")
        print("卡片：%s  纵向溢出 %spx  横向溢出 %spx" % (title, dh, dw))
    else:
        print("卡片：未能取到溢出数据")

    pdf = os.path.join(outdir, stem + ".pdf")
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=8000", "--no-pdf-header-footer",
                    "--print-to-pdf=%s" % pdf, "--no-pdf-header-footer",
                    "file://" + html_path], capture_output=True, timeout=180)
    print("PDF  ->", pdf, os.path.getsize(pdf) if os.path.exists(pdf) else "失败")

    if "--png" in sys.argv:
        png = os.path.join(outdir, stem + ".png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--window-size=1420,1004",
                        "--screenshot=" + png, "--virtual-time-budget=8000",
                        "file://" + html_path], capture_output=True, timeout=180)
        print("PNG  ->", png)


if __name__ == "__main__":
    main()
