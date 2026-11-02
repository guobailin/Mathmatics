#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数论模块示意图（issue #74 P0-3）。

图内只用字母、数字与公式（matplotlib 默认字体无中文字形），中文解释写在
md 的图注里。每张图同时产出
    assets/geometry/num-*.svg/.png
    assets/geometry/cards/num-*.svg

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/number_figures.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, seg, dot, text, save,
)

from matplotlib.patches import Rectangle, Arc  # noqa: E402

TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"


def arrow(ax, p, q, color=INK, lw=1.6, ls="-", z=5, scale=11):
    """细箭头 p -> q。style.py 没有箭头，用 annotate 补上。"""
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=scale),
                zorder=z)


def box(ax, x, y, w, h, fc, ec=INK, lw=1.1, z=2, alpha=1.0, ls="-"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                           linewidth=lw, zorder=z, alpha=alpha, linestyle=ls))


def bracket(ax, p, q, color=MUTED, lw=1.1, tick=0.10, z=4):
    """两点之间的量取线（两端带短垂线）。"""
    seg(ax, p, q, color=color, lw=lw, z=z)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / L, dx / L
    for t in (p, q):
        seg(ax, (t[0] - tick * nx, t[1] - tick * ny),
            (t[0] + tick * nx, t[1] + tick * ny), color=color, lw=lw, z=z)


# ---------------------------------------------------------------- 1 整除特征
def fig_div_rules():
    """数位条上三种判据各自"看哪里、怎么合"。"""
    fig, ax = new_fig(8.6, 4.75)
    digits = ["5", "4", "7", "3", "9", "2"]
    W, G, H = 0.58, 0.20, 0.66
    x0 = 0.60
    rows = (3.30, 1.85, 0.40)

    def xs(i):
        return x0 + i * (W + G)

    xcut = xs(3) - G / 2
    seg(ax, (xcut, 0.22), (xcut, 4.14), color=MUTED, lw=1.0, ls=(0, (4, 3)))

    for r, y in enumerate(rows):
        for i, d in enumerate(digits):
            if r == 0:
                gone = i < 3
                fc = "white" if gone else TEAL
                col = MUTED if gone else INK
            elif r == 1:
                fc, col = "white", INK
            else:
                fc = TEAL2 if i < 3 else WARM2
                col = INK
            box(ax, xs(i), y, W, H, fc, lw=1.2)
            text(ax, xs(i) + W / 2, y + H / 2, "$%s$" % d, size=16, color=col)
            if r == 0 and i < 3:
                seg(ax, (xs(i) + 0.11, y + 0.11),
                    (xs(i) + W - 0.11, y + H - 0.11), color=GRID, lw=1.5, z=3)
            if r == 1 and i in (0, 1, 3, 4):
                text(ax, xs(i) + W + G / 2, y + H / 2, "$+$", size=11,
                     color=MUTED)

    # 第三行：高位段记 −，末三位段记 +
    text(ax, (xs(0) + xs(2) + W) / 2, rows[2] + H + 0.26, "$-$", size=18)
    text(ax, (xs(3) + xs(5) + W) / 2, rows[2] + H + 0.26, "$+$", size=18)

    text(ax, 2.70, 4.30, "$N=\\overline{a_6a_5\\cdots a_0}$", size=14,
         color=MUTED)

    labels = [("$m\\mid 10^{3}$", "$N\\equiv T$"),
              ("$m\\mid 9\\cdots 9$", "$N\\equiv\\sum a_i$"),
              ("$m\\mid 100\\cdots 01$", "$N\\equiv T-M$")]
    for (a, b), y in zip(labels, rows):
        text(ax, 5.50, y + 0.46, a, size=15, ha="left")
        text(ax, 5.50, y + 0.04, b, size=15, ha="left", color=TEAL_D)

    finish(ax, (0.0, 8.55), (-0.10, 4.62))
    save(fig, "num-div-rules")


# ---------------------------------------------------------------- 2 位值原理
def fig_place_value():
    """位权=数字×10 的幂；对调时十位相加抵消，只剩 99 倍。"""
    fig, ax = new_fig(11.1, 5.8)

    # 上：369 的位值展开
    cols = (0.85, 2.95, 5.05)
    for x, d, pv in zip(cols, ["3", "6", "9"],
                        ["$3\\times100$", "$6\\times10$", "$9\\times1$"]):
        box(ax, x, 4.28, 1.15, 0.72, TEAL2, lw=1.3)
        text(ax, x + 0.575, 4.64, "$%s$" % d, size=22)
        text(ax, x + 0.575, 3.95, pv, size=13.5, color=TEAL_D)
    for x in (2.05, 4.15):
        arrow(ax, (x, 4.64), (x + 0.82, 4.64), color=TEAL_D, lw=1.3, scale=9)
    for x in (2.44, 4.54):
        text(ax, x, 4.98, "$\\times10$", size=12, color=TEAL_D)

    text(ax, 6.85, 4.62, "$\\overline{abc}=100a+10b+c$", size=15.5, ha="left")

    # 下：963 − 369 逐位值相减，十位整列抵消成 0
    band = Rectangle((2.60, 0.98), 0.70, 1.68, facecolor=TEAL2, edgecolor="none",
                     alpha=0.85, zorder=1)
    ax.add_patch(band)
    xd = (2.05, 2.95, 3.85)
    for x, h in zip(xd, ["$10^{2}$", "$10^{1}$", "$10^{0}$"]):
        text(ax, x, 2.90, h, size=11, color=MUTED)
    for x, d in zip(xd, ["$900$", "$60$", "$3$"]):
        text(ax, x, 2.42, d, size=16)
    for x, d in zip(xd, ["$-300$", "$-60$", "$-9$"]):
        text(ax, x, 1.82, d, size=16)
    seg(ax, (1.50, 1.50), (4.24, 1.50), color=INK, lw=1.6)
    for x, d in zip(xd, ["$600$", "$0$", "$-6$"]):
        text(ax, x, 1.16, d, size=16, color=WARM_D)

    text(ax, 4.62, 2.42, "$963-369$", size=15, ha="left")
    text(ax, 4.62, 1.82, "$=600-6=594$", size=15, ha="left")
    text(ax, 4.62, 1.22, "$=99\\times(9-3)$", size=15, ha="left")

    finish(ax, (0.20, 10.55), (-0.05, 5.35))
    save(fig, "num-place-value")


# ---------------------------------------------------------------- 3 进位制
def fig_base_conversion():
    """除 k 取余：余数自下而上读出，才是从高位到低位。"""
    fig, ax = new_fig(9.8, 3.5)
    ys = (4.60, 3.95, 3.30, 2.65, 2.00)
    seg(ax, (1.95, 1.86), (1.95, 4.82), color=INK, lw=2.0)

    text(ax, 1.62, 4.60, "$7$", size=17)
    text(ax, 2.62, 4.60, "$2024$", size=17)

    quot = ["$289$", "$41$", "$5$", "$0$"]
    rems = ["$1$", "$2$", "$6$", "$5$"]
    for y, q, r in zip(ys[1:], quot, rems):
        text(ax, 2.62, y, q, size=17)
        box(ax, 3.72, y - 0.26, 0.58, 0.52, WARM2, ec=WARM_D, lw=1.0)
        text(ax, 4.01, y, r, size=16, color=WARM_D)

    # 余数竖列 → 向上、向右读成高到低
    arrow(ax, (4.56, 1.66), (4.56, 4.30), color=TEAL_D, lw=1.5, scale=11)
    arrow(ax, (4.56, 4.30), (4.78, 4.30), color=TEAL_D, lw=1.5, scale=11)

    digs = ["$5$", "$6$", "$2$", "$1$"]
    for i, d in enumerate(digs):
        x = 5.10 + 0.62 * i
        box(ax, x - 0.28, 4.02, 0.56, 0.56, TEAL2, lw=1.2)
        text(ax, x, 4.30, d, size=18)

    text(ax, 7.45, 4.30, "$(5621)_7$", size=19, ha="left")
    text(ax, 5.10, 3.35, "$5\\cdot7^{3}+6\\cdot7^{2}+2\\cdot7+1$", size=13,
         ha="left", color=MUTED)
    text(ax, 5.10, 2.85, "$=1715+294+14+1=2024$", size=13, ha="left",
         color=MUTED)

    finish(ax, (0.85, 9.80), (1.42, 4.90))
    save(fig, "num-base-conversion")


# ---------------------------------------------------------------- 4 埃氏筛
def fig_sieve():
    """100 以内数表：按"最先划掉它的质数"上色，剩下的就是质数。"""
    fig, ax = new_fig(8.4, 8.8)
    cell, x0, y0 = 0.75, 0.60, 0.85

    colors = {2: GRID, 3: TEAL2, 5: WARM2, 7: WARM}

    def spf(n):
        for p in (2, 3, 5, 7):
            if n != p and n % p == 0:
                return p
        return None

    for n in range(1, 101):
        row, col = (n - 1) // 10, (n - 1) % 10
        x = x0 + col * cell
        y = y0 + (9 - row) * cell
        p = spf(n)
        if n == 1:
            box(ax, x, y, cell, cell, "white", lw=1.0)
            seg(ax, (x + 0.12, y + 0.12), (x + cell - 0.12, y + cell - 0.12),
                color=GRID, lw=1.5)
            text(ax, x + cell / 2, y + cell / 2, "$1$", size=9, color=GRID)
        elif p is None:
            box(ax, x, y, cell, cell, TEAL, lw=1.0)
            text(ax, x + cell / 2, y + cell / 2, "$%d$" % n, size=9.2,
                 color=INK, weight="bold")
        else:
            box(ax, x, y, cell, cell, colors[p], ec=GRID, lw=0.8, alpha=0.62)
            text(ax, x + cell / 2, y + cell / 2, "$%d$" % n, size=9,
                 color=MUTED)

    # 图例
    items = [("$2$", GRID), ("$3$", TEAL2), ("$5$", WARM2), ("$7$", WARM),
             ("$p$", TEAL), ("$1$", "white")]
    for i, (lab, c) in enumerate(items):
        cx = 0.52 + 1.32 * i
        box(ax, cx, 0.16, 0.34, 0.34, c, ec=GRID if c == "white" else INK,
            lw=1.0)
        if lab == "$1$":
            seg(ax, (cx + 0.07, 0.21), (cx + 0.27, 0.45), color=GRID, lw=1.3)
        text(ax, cx + 0.46, 0.33, lab, size=12, ha="left")

    finish(ax, (0.28, 8.45), (0.05, 8.62))
    save(fig, "num-sieve")


# ---------------------------------------------------------------- 5 因数成对
def fig_factor_pairs():
    """36 的因数成对落到 √36 两侧；成对的弧都跨过平方根线。"""
    fig, ax = new_fig(10.4, 5.4)
    k, x0 = 0.215, 0.55

    def X(v):
        return x0 + k * v

    seg(ax, (X(0) - 0.25, 0), (X(36) + 0.25, 0), color=INK, lw=2.0)
    text(ax, X(36) + 0.42, 0, "$N$", size=13, ha="left", color=MUTED)

    for v in (1, 2, 3, 4, 6, 9, 12, 18, 36):
        seg(ax, (X(v), -0.10), (X(v), 0.10), color=INK, lw=1.3)
        text(ax, X(v), -0.34, "$%d$" % v, size=11, color=MUTED)

    pairs = [(1, 36), (2, 18), (3, 12), (4, 9)]
    for a, b in pairs:
        w = X(b) - X(a)
        ax.add_patch(Arc(((X(a) + X(b)) / 2, 0), w, w * 0.55, angle=0,
                         theta1=0, theta2=180, color=TEAL_D, lw=1.7, zorder=3))
    seg(ax, (X(6), 0.10), (X(6), 0.40), color=WARM_D, lw=1.9)
    dot(ax, (X(6), 0.10), ms=5, color=WARM_D)

    seg(ax, (X(6), -0.60), (X(6), 2.45), color=WARM_D, lw=1.2, ls=(0, (4, 3)))
    text(ax, X(6) + 0.18, 2.55, "$\\sqrt{36}=6$", size=13, ha="left",
         color=WARM_D)

    bracket(ax, (X(0), -0.80), (X(6), -0.80), color=MUTED, lw=1.1)
    text(ax, (X(0) + X(6)) / 2, -1.05, "$a\\leq\\sqrt{N}$", size=12,
         color=MUTED)
    bracket(ax, (X(6), -0.80), (X(36), -0.80), color=MUTED, lw=1.1)
    text(ax, (X(6) + X(36)) / 2, -1.05, "$b\\geq\\sqrt{N}$", size=12,
         color=MUTED)

    text(ax, 9.35, 1.55, "$a\\cdot b=36$", size=14, ha="center")

    finish(ax, (-0.35, 10.25), (-1.35, 2.85))
    save(fig, "num-factor-pairs")


# ---------------------------------------------------------------- 6 因数个数
def fig_divisor_grid():
    """1400=2³·5²·7：每行挑一个指数，恰好得到一个因数。"""
    fig, ax = new_fig(8.2, 4.0)
    rows = (2.72, 1.86, 1.00)
    x0, step, W, H = 1.25, 0.80, 0.66, 0.62
    data = [(2, 3), (5, 2), (7, 1)]
    picked = {0: 2, 1: 1, 2: 1}

    for r, (p, a) in enumerate(data):
        y = rows[r]
        for b in range(a + 1):
            x = x0 + b * step
            hot = (picked[r] == b)
            box(ax, x, y, W, H, WARM2 if hot else "white",
                ec=WARM_D if hot else INK, lw=2.2 if hot else 1.1)
            text(ax, x + W / 2, y + H / 2, "$%d^{%d}$" % (p, b), size=13)
        text(ax, 4.42, y + H / 2, "$%d$" % (a + 1), size=15, color=TEAL_D)

    # 连线：一行的选中项接到下一行的选中项
    for r in range(2):
        px = x0 + picked[r] * step + W / 2
        py = rows[r] + H / 2
        qx = x0 + picked[r + 1] * step + W / 2
        qy = rows[r + 1] + H / 2
        seg(ax, (px, py - H / 2), (qx, qy + H / 2), color=WARM_D, lw=1.5,
            ls=(0, (3, 3)), z=6)

    text(ax, 4.42, 2.44, "$\\times$", size=12, color=MUTED)
    text(ax, 4.42, 1.58, "$\\times$", size=12, color=MUTED)
    text(ax, 4.42, 0.60, "$=24$", size=15, color=TEAL_D)

    seg(ax, (2.38, 1.00), (2.38, 0.60), color=WARM_D, lw=1.3, ls=(0, (3, 3)))
    text(ax, 2.10, 0.32, "$2^{2}\\cdot5^{1}\\cdot7^{1}=140$", size=14,
         ha="left", color=WARM_D)

    finish(ax, (0.90, 7.95), (0.05, 3.52))
    save(fig, "num-divisor-grid")


# ---------------------------------------------------------------- 7 短除表
def fig_short_division():
    """短除表：左列连乘给 gcd，左列乘末行给 lcm。"""
    fig, ax = new_fig(9.4, 5.2)
    ys = (4.45, 3.75, 3.05, 2.35)
    cols = (2.55, 3.75, 4.95)

    seg(ax, (1.95, 2.05), (1.95, 4.78), color=INK, lw=2.0)
    divs = ["$2$", "$2$", "$3$"]
    for y, d in zip(ys[:3], divs):
        text(ax, 1.48, y, d, size=16, color=TEAL_D)

    body = [("$24$", "$36$", "$60$"),
            ("$12$", "$18$", "$30$"),
            ("$6$", "$9$", "$15$"),
            ("$2$", "$3$", "$5$")]
    for r, (a, b, c) in enumerate(body):
        for x, s in zip(cols, (a, b, c)):
            col = INK
            if r == 3:
                col = WARM_D
            text(ax, x, ys[r], s, size=16, color=col)

    # 左列（青）与末行（橙）用底色标出
    ax.add_patch(Rectangle((1.16, 2.40), 0.64, 2.38, facecolor=TEAL2,
                           edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((1.95, 2.06), 3.45, 0.54, facecolor=WARM2,
                           edgecolor="none", zorder=1))

    text(ax, 1.05, 1.62, "$(24,36,60)\\ =$", size=16, ha="left")
    text(ax, 4.05, 1.62, "$2\\times2\\times3=12$", size=16, ha="left",
         color=TEAL_D)
    text(ax, 1.05, 0.90, "$[24,36,60]\\ =$", size=16, ha="left")
    text(ax, 4.10, 0.90, "$2\\times2\\times3$", size=16, ha="left",
         color=TEAL_D)
    text(ax, 5.58, 0.90, "$\\times\\,2\\times3\\times5=360$", size=16,
         ha="left", color=WARM_D)

    finish(ax, (0.80, 9.35), (0.58, 5.05))
    save(fig, "num-short-division")


# ---------------------------------------------------------------- 8 辗转相除
def fig_euclid_tiling():
    """(48,18)：大矩形被正方形一路铺满，最后一格的边长就是 gcd。"""
    fig, ax = new_fig(11.3, 4.4)

    for i in range(9):
        seg(ax, (i, 0), (i, 3), color=GRID, lw=0.7, z=1, alpha=0.75)
    for j in range(4):
        seg(ax, (0, j), (8, j), color=GRID, lw=0.7, z=1, alpha=0.75)

    box(ax, 0, 0, 3, 3, TEAL2, lw=1.4, z=2, alpha=0.85)
    box(ax, 3, 0, 3, 3, TEAL2, lw=1.4, z=2, alpha=0.85)
    box(ax, 6, 0, 2, 2, WARM2, lw=1.4, z=2, alpha=0.95)
    box(ax, 6, 2, 1, 1, WARM, lw=1.4, z=2, alpha=0.95)
    box(ax, 7, 2, 1, 1, WARM, lw=1.4, z=2, alpha=0.95)
    box(ax, 0, 0, 8, 3, "none", lw=2.2, z=4, alpha=1.0)

    text(ax, 1.5, 1.5, "$18$", size=18)
    text(ax, 4.5, 1.5, "$18$", size=18)
    text(ax, 7.0, 1.0, "$12$", size=14)
    text(ax, 6.5, 2.5, "$6$", size=10.5)
    text(ax, 7.5, 2.5, "$6$", size=10.5)

    bracket(ax, (0, -0.26), (8, -0.26), color=MUTED, lw=1.1)
    text(ax, 4.0, -0.62, "$48$", size=14, color=MUTED)
    bracket(ax, (-0.26, 0), (-0.26, 3), color=MUTED, lw=1.1)
    text(ax, -0.62, 1.5, "$18$", size=14, color=MUTED)

    text(ax, 8.85, 2.20, "$(48,18)=6$", size=17, ha="left")
    text(ax, 8.85, 1.55, "$48=2\\cdot18+12$", size=13, ha="left", color=MUTED)
    text(ax, 8.85, 1.05, "$18=1\\cdot12+6$", size=13, ha="left", color=MUTED)
    text(ax, 8.85, 0.55, "$12=2\\cdot6$", size=13, ha="left", color=MUTED)

    finish(ax, (-1.05, 12.35), (-1.05, 3.55))
    save(fig, "num-euclid-tiling")


# ---------------------------------------------------------------- 9 带余除法
def fig_remainder_line():
    """数轴上的等距刻度：a 落在 5 个 b 之后，余下 r。"""
    fig, ax = new_fig(10.0, 3.2)
    k, x0 = 0.185, 0.55

    def X(v):
        return x0 + k * v

    seg(ax, (X(0) - 0.2, 0), (X(49), 0), color=INK, lw=2.0)
    arrow(ax, (X(49) - 0.25, 0), (X(49) + 0.15, 0), color=INK, lw=2.0)

    for v in range(0, 43, 7):
        seg(ax, (X(v), -0.10), (X(v), 0.10), color=INK, lw=1.4)
        text(ax, X(v), -0.30, "$%d$" % v, size=11, color=MUTED)
        seg(ax, (X(v), 0.12), (X(v), 0.62), color=GRID, lw=0.9,
            ls=(0, (3, 3)))

    seg(ax, (X(40), 0), (X(40), 0.98), color=WARM_D, lw=1.4, ls=(0, (4, 3)))
    dot(ax, (X(40), 0), ms=6.5, color=WARM_D)
    text(ax, X(40) - 0.16, 1.12, "$a=40$", size=13.5, color=WARM_D,
         ha="right")

    bracket(ax, (X(35), 0.45), (X(40), 0.45), color=WARM_D, lw=1.2, tick=0.08)
    text(ax, (X(35) + X(40)) / 2, 0.74, "$r=5$", size=12, color=WARM_D)

    bracket(ax, (X(0), -0.62), (X(35), -0.62), color=TEAL_D, lw=1.2)
    text(ax, (X(0) + X(35)) / 2, -0.90, "$qb=35$", size=12, color=TEAL_D)
    bracket(ax, (X(0), -1.20), (X(7), -1.20), color=TEAL_D, lw=1.2)
    text(ax, (X(0) + X(7)) / 2, -1.48, "$b=7$", size=12, color=TEAL_D)

    text(ax, 8.55, -0.90, "$a=bq+r$", size=18)
    text(ax, 8.55, -1.42, "$0\\leq r<b$", size=12.5, color=MUTED)

    finish(ax, (0.10, 9.85), (-1.75, 1.45))
    save(fig, "num-remainder-line")


# ---------------------------------------------------------------- 10 同余刻度
def fig_congruence_lattice():
    """两条等差数列各自等距，交点处才同时满足两个余数条件。"""
    fig, ax = new_fig(10.6, 5.6)
    k, x0 = 0.135, 0.55

    def X(v):
        return x0 + k * v

    seg(ax, (X(0), 1.35), (X(60), 1.35), color=GRID, lw=1.2)
    seg(ax, (X(0), -1.35), (X(60), -1.35), color=GRID, lw=1.2)

    for v in range(3, 60, 4):
        dot(ax, (X(v), 1.35), ms=4.6, color=MUTED)
    for v in range(5, 55, 7):
        dot(ax, (X(v), -1.35), ms=4.6, color=MUTED)

    seg(ax, (X(0), 0), (X(60), 0), color=INK, lw=1.6)
    for v in range(0, 61, 10):
        seg(ax, (X(v), -0.09), (X(v), 0.09), color=INK, lw=1.2)
        text(ax, X(v), -0.31, "$%d$" % v, size=10.5, color=MUTED, box=True)

    for v in (19, 47):
        seg(ax, (X(v), -2.05), (X(v), 2.05), color=WARM_D, lw=1.2,
            ls=(0, (4, 3)))
        dot(ax, (X(v), 1.35), ms=8.5, color=WARM_D, z=6)
        dot(ax, (X(v), -1.35), ms=8.5, color=WARM_D, z=6)
        text(ax, X(v), 2.22, "$%d$" % v, size=13, color=WARM_D)

    bracket(ax, (X(19), -2.05), (X(47), -2.05), color=WARM_D, lw=1.2,
            tick=0.10)
    text(ax, (X(19) + X(47)) / 2, -2.42, "$28=[4,7]$", size=13, color=WARM_D)

    text(ax, 0.30, 1.72, "$+4$", size=13, color=MUTED)
    text(ax, 0.30, -1.72, "$+7$", size=13, color=MUTED)

    text(ax, 9.05, 0.40, "$N=19+28t$", size=15)

    finish(ax, (-0.10, 10.50), (-2.75, 2.55))
    save(fig, "num-congruence-lattice")


if __name__ == "__main__":
    fig_div_rules()
    fig_place_value()
    fig_base_conversion()
    fig_sieve()
    fig_factor_pairs()
    fig_divisor_grid()
    fig_short_division()
    fig_euclid_tiling()
    fig_remainder_line()
    fig_congruence_lattice()
    print("done")
