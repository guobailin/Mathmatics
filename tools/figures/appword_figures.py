#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""应用题模块示意图（issue #74 P0-3 续）。

图内只用字母、数字与公式（避开中文字体依赖），中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/appword_figures.py
产出：
    assets/geometry/app-*.svg/.png
    assets/geometry/cards/app-*.svg
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, poly, outline, seg, dot, text, save,
)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Polygon  # noqa: E402

TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"


def arrow(ax, p, q, color=INK, lw=1.8, ls="-", z=5, scale=13, rad=0.0):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=scale,
                                connectionstyle="arc3,rad=%s" % rad),
                zorder=z)


def bracket(ax, p, q, color=MUTED, lw=1.2, tick=0.12, z=4):
    seg(ax, p, q, color=color, lw=lw, z=z)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for t in (p, q):
        seg(ax, (t[0] - tick * nx, t[1] - tick * ny),
            (t[0] + tick * nx, t[1] + tick * ny), color=color, lw=lw, z=z)


def bar(ax, x0, x1, y, h, color, alpha=0.92, lw=1.3, edge=INK, z=3):
    poly(ax, [(x0, y), (x1, y), (x1, y + h), (x0, y + h)],
         color, alpha=alpha, lw=lw, edge=edge, z=z)


def rect_outline(ax, x0, x1, y, h, color=MUTED, lw=1.2, ls="-", z=4):
    ax.add_patch(plt.Rectangle((x0, y), x1 - x0, h, fill=False,
                               edgecolor=color, linewidth=lw, linestyle=ls,
                               zorder=z))


def cells(ax, x0, total, step, y, h, color, edge=INK, lw=1.0, z=3):
    n = int(round(total / step))
    for i in range(n):
        bar(ax, x0 + i * step, x0 + (i + 1) * step, y, h, color, lw=lw,
            edge=edge, z=z)
    return n


def tree(ax, x, y, s=1.0, color=TEAL):
    poly(ax, [(x, y + 0.40 * s), (x - 0.16 * s, y), (x + 0.16 * s, y)],
         color, alpha=0.95, lw=1.2, z=5)


# ---------------------------------------------------------------- 植树问题
def fig_tree_planting():
    """三种直线栽法与环形：棵数与间隔数差 1、差 0、差 −1。"""
    fig, ax = new_fig(10.2, 5.0)
    rows = [(0.0, [0, 1, 2, 3, 4], "$T=n+1$", "$5$", "$+1$"),
            (-1.75, [0, 1, 2, 3], "$T=n$", "$4$", "$0$"),
            (-3.50, [1, 2, 3], "$T=n-1$", "$3$", "$-1$")]

    for y, pos, form, cnt, dlt in rows:
        seg(ax, (-0.15, y), (4.15, y), color=INK, lw=1.8, z=2)
        for i in range(5):                       # 间隔端点
            seg(ax, (i, y - 0.10), (i, y + 0.10), color=MUTED, lw=1.1, z=3)
        for p in pos:
            tree(ax, p, y)
        text(ax, 2.0, y + 0.72, dlt, size=13.5, color=WARM_D)
        text(ax, -0.55, y, "$n=4$", size=12, color=MUTED, ha="right")
        text(ax, 4.62, y, cnt, size=15, color=TEAL_D, ha="left")
        text(ax, 5.55, y, form, size=13, ha="left")

    # 环形
    cx, cy, R = 8.55, -1.75, 1.35
    ax.add_patch(Circle((cx, cy), R, fill=False, edgecolor=INK, lw=1.8, zorder=2))
    for k in range(4):
        th = math.radians(90 + 90 * k)
        p = (cx + R * math.cos(th), cy + R * math.sin(th))
        tree(ax, p[0], p[1], s=0.9)
    text(ax, cx, cy, "$4$", size=14, color=MUTED)
    text(ax, cx, cy - R - 0.72, "$T=n=4$", size=14, color=TEAL_D)

    finish(ax, (-1.55, 10.9), (-4.05, 2.15))
    save(fig, "app-tree-planting")


# ---------------------------------------------------------------- 方阵问题
def fig_square_formation():
    """最外层 4n−4 的四个角被数两次；空心方阵逐层少 8。"""
    fig, ax = new_fig(9.6, 6.0)

    # 左：5×5 实心方阵
    n = 5
    for r in range(n):
        for c in range(n):
            on_edge = r in (0, n - 1) or c in (0, n - 1)
            ax.add_patch(Circle((c, n - 1 - r), 0.15,
                                facecolor=WARM if on_edge else TEAL2,
                                edgecolor=INK if on_edge else MUTED,
                                linewidth=1.0, zorder=3))
    for (c, r) in [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]:
        ax.add_patch(Circle((c, n - 1 - r), 0.30, facecolor="none",
                            edgecolor=WARM_D, lw=1.5, zorder=4))
    text(ax, 2.0, -0.72, "$S=5^2=25$", size=15, color=TEAL_D)
    text(ax, 2.0, -1.32, "$L=4\\times5-4=16$", size=15, color=WARM_D)

    # 右：7×7 中空两层
    m = 7
    ox = 7.6
    for r in range(m):
        for c in range(m):
            d = min(r, c, m - 1 - r, m - 1 - c)
            if d == 0:
                col, edge = WARM, INK
            elif d == 1:
                col, edge = TEAL, INK
            else:
                continue
            ax.add_patch(Circle((ox + c, m - 1 - r), 0.15,
                                facecolor=col, edgecolor=edge,
                                linewidth=1.0, zorder=3))
    rect_outline(ax, ox + 2 - 0.4, ox + 4 + 0.4, 2 - 0.4, 2 + 0.8,
                 color=MUTED, lw=1.0, ls=(0, (4, 3)), z=2)
    text(ax, ox + 3, -0.72, "$S=7^2-3^2=40$", size=15, color=TEAL_D)
    text(ax, ox + 3, -1.32, "$24-16=8$", size=15, color=WARM_D)
    text(ax, ox + 3, m + 0.40, "$L_1=24,\\ L_2=16$", size=13, color=INK)

    finish(ax, (-1.0, 15.2), (-2.05, 8.05))
    save(fig, "app-square-formation")


# ---------------------------------------------------------------- 浓度问题
def fig_concentration():
    """溶质账本：两份溶质拼成混合后的溶质；下方是十字交叉的线段比。"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.0, 5.6),
                                   gridspec_kw={"height_ratios": [2.1, 1.0]})
    for a in (ax1, ax2):
        a.set_facecolor("none")
        a.axis("off")
    fig.patch.set_alpha(0)

    # ---------- 上：质量条，深色部分是溶质 ----------
    h = 0.52
    rows = [(2.0, 300, 60, "M_1=300", "p_1=20\\%", "S_1=60"),
            (1.0, 200, 10, "M_2=200", "p_2=5\\%", "S_2=10"),
            (0.0, 500, 70, "M=500", "p=14\\%", "S=70")]
    for y, M, S, lm, lp, ls in rows:
        bar(ax1, 0, M, y, h, TEAL2, alpha=0.95)
        if y > 0.5:
            bar(ax1, 0, S, y, h, TEAL, alpha=0.95)
        else:                                    # 混合后：两段溶质拼起来
            bar(ax1, 0, 60, y, h, TEAL, alpha=0.95)
            bar(ax1, 60, 70, y, h, WARM, alpha=0.95)
        text(ax1, M + 16, y + h / 2, "$%s$" % lm, size=13, ha="left")
        text(ax1, M + 128, y + h / 2, "$%s$" % lp, size=13, ha="left",
             color=WARM_D)
        text(ax1, M + 235, y + h / 2, "$%s$" % ls, size=13, ha="left",
             color=TEAL_D)

    # 溶质相加：60 + 10 = 70
    seg(ax1, (60, -0.22), (60, 2.62), color=WARM_D, lw=1.0, ls=(0, (4, 3)), z=1)
    text(ax1, 30, -0.42, "$60$", size=12, color=TEAL_D)
    text(ax1, 65, -0.42, "$+10$", size=12, color=WARM_D, ha="left")
    ax1.text(0, 2.92, "$M_1p_1+M_2p_2=(M_1+M_2)p$", fontsize=16, va="center")
    ax1.set_xlim(-20, 800)
    ax1.set_ylim(-0.75, 3.25)

    # ---------- 下：十字交叉的线段比 ----------
    y0 = 0.0
    seg(ax2, (0, y0), (25, y0), color=INK, lw=1.5, z=2)
    for v, lab in [(0, "0"), (5, "5"), (14, "14"), (20, "20")]:
        seg(ax2, (v, y0 - 4), (v, y0 + 4), color=MUTED, lw=1.1, z=3)
        text(ax2, v, y0 - 13, "$%s$" % lab, size=12, color=MUTED)
    for v, lab, col in [(5, "$p_2$", TEAL_D), (14, "$p$", INK), (20, "$p_1$", WARM_D)]:
        text(ax2, v, y0 + 14, lab, size=13, color=col)
    bracket(ax2, (5, y0 - 26), (14, y0 - 26), color=TEAL_D, tick=2.0)
    text(ax2, 9.5, y0 - 42, "$9$", size=13, color=TEAL_D)
    bracket(ax2, (14, y0 - 26), (20, y0 - 26), color=WARM_D, tick=2.0)
    text(ax2, 17, y0 - 42, "$6$", size=13, color=WARM_D)
    ax2.text(27, y0 + 14, "$M_1:M_2=(p-p_2):(p_1-p)=9:6=3:2$",
             fontsize=13.5, va="center")
    ax2.set_xlim(-0.8, 100)
    ax2.set_ylim(-56, 30)

    fig.tight_layout()
    save(fig, "app-concentration")


# ---------------------------------------------------------------- 牛吃草
def fig_grazing():
    """草量供给线 G+gt 与消耗线 nt 的交点就是吃完的时刻。"""
    fig, ax = new_fig(7.8, 6.8)
    G, g = 6.0, 1.0
    XS = 8.2                      # 供给线画到哪天

    seg(ax, (0, 0), (9.3, 0), color=INK, lw=1.5, z=2)
    seg(ax, (0, 0), (0, G + g * XS + 0.6), color=INK, lw=1.5, z=2)
    for t in range(0, 10, 2):
        seg(ax, (t, -0.20), (t, 0), color=MUTED, lw=1.0, z=2)
        text(ax, t, -0.68, "$%d$" % t, size=11, color=MUTED)
    text(ax, 9.65, -0.68, "$t$", size=13, color=MUTED, ha="left")
    text(ax, -0.5, 15.0, "$Q$", size=13, color=MUTED, ha="right")

    # 供给线
    seg(ax, (0, G), (XS, G + g * XS), color=WARM_D, lw=2.6, z=4)
    dot(ax, (0, G), ms=6, color=WARM_D)
    text(ax, -0.35, G, "$G$", size=13, color=WARM_D, ha="right")
    text(ax, XS + 0.15, G + g * XS + 0.15, "$G+gt$", size=14, color=WARM_D,
         ha="left")

    # 消耗线
    seg(ax, (0, 0), (3.85, 3.0 * 3.85), color=TEAL_D, lw=2.0, z=3)
    seg(ax, (0, 0), (6.25, 2.0 * 6.25), color=TEAL_D, lw=2.0, z=3)
    text(ax, 3.98, 3.0 * 3.98 - 0.3, "$n_1t$", size=13.5, color=TEAL_D,
         ha="left")
    text(ax, 6.40, 11.85, "$n_2t$", size=13.5, color=TEAL_D, ha="left")

    # 临界：n = g，与供给线平行
    seg(ax, (0, 0), (8.9, g * 8.9), color=MUTED, lw=1.8, ls=(0, (6, 4)), z=3)
    text(ax, 9.0, g * 8.9 + 0.35, "$n=g$", size=12.5, color=MUTED, ha="left")

    # 两个交点
    for n, t, lab in [(3.0, 3.0, "1"), (2.0, 6.0, "2")]:
        dot(ax, (t, n * t), ms=7, color=INK)
        seg(ax, (t, 0), (t, n * t), color=GRID, lw=1.1, ls=(0, (3, 3)), z=1)
        text(ax, t, -1.28, "$t_%s$" % lab, size=13)

    finish(ax, (-1.5, 10.6), (-1.9, 15.3))
    save(fig, "app-grazing")


# ---------------------------------------------------------------- 工程问题
def fig_work():
    """设总量 36：甲每天 3、乙每天 2，合起来每天 5，36÷5=7 余 1。"""
    fig, ax = new_fig(10.2, 3.8)
    h = 0.56
    y1, y2, y3 = 2.1, 1.2, 0.0

    cells(ax, 0, 36, 3, y1, h, TEAL)
    text(ax, 1.5, y1 + h / 2, "$3$", size=12)
    text(ax, 36.9, y1 + h / 2, "$12$", size=13, ha="left", color=TEAL_D)

    cells(ax, 0, 36, 2, y2, h, TEAL2)
    text(ax, 1.0, y2 + h / 2, "$2$", size=11)
    text(ax, 36.9, y2 + h / 2, "$18$", size=13, ha="left", color=TEAL_D)

    n = cells(ax, 0, 35, 5, y3, h, WARM)
    bar(ax, 35, 36, y3, h, WARM2, alpha=0.9, lw=1.3, edge=WARM_D)
    text(ax, 2.5, y3 + h / 2, "$5$", size=12)
    text(ax, 35.5, y3 + h / 2, "$1$", size=10.5, color=WARM_D)
    text(ax, 36.9, y3 + h / 2, "$7$", size=13, ha="left", color=WARM_D)

    text(ax, 0, 3.15, "$36\\div12=3$", size=14, color=TEAL_D)
    text(ax, 11.5, 3.15, "$36\\div18=2$", size=14, color=TEAL_D)
    text(ax, 23.0, 3.15, "$3+2=5$", size=14, color=WARM_D)
    text(ax, 23.0, -1.05, "$36\\div5=7\\cdots1\\ \\Rightarrow\\ 7.2$", size=15)

    text(ax, -0.9, y1 + h / 2, "$A$", size=13, ha="right")
    text(ax, -0.9, y2 + h / 2, "$B$", size=13, ha="right")
    text(ax, -0.9, y3 + h / 2, "$A+B$", size=13, ha="right")

    ax.set_xlim(-3.4, 42)
    ax.set_ylim(-1.6, 3.55)
    ax.axis("off")
    save(fig, "app-work")


# ---------------------------------------------------------------- 盈亏问题
def fig_profit_loss():
    """两次分法：一盈一亏，两头相差盈+亏，正好是每人差额的份数倍。"""
    fig, ax = new_fig(10.0, 4.0)
    h = 0.56
    yA, yB = 1.5, 0.5
    k, per_a, per_b = 4, 5, 3

    # 第一种分法：每人 5，总数 20，超出 2（亏 2）
    for i in range(k):
        bar(ax, i * per_a, (i + 1) * per_a, yA, h, TEAL2, lw=1.2)
        text(ax, i * per_a + per_a / 2, yA + h / 2, "$5$", size=11)
    bar(ax, 18, 20, yA, h, WARM, alpha=0.95, lw=1.4)
    text(ax, 19, yA + h / 2, "$2$", size=10.5, color=WARM_D)

    # 第二种分法：每人 3，总数 12，差 6（盈 6）
    for i in range(k):
        bar(ax, i * per_b, (i + 1) * per_b, yB, h, TEAL2, lw=1.2)
        text(ax, i * per_b + per_b / 2, yB + h / 2, "$3$", size=11)
    bar(ax, 12, 18, yB, h, WARM2, alpha=0.75, lw=1.2, edge=WARM_D)
    text(ax, 15, yB + h / 2, "$6$", size=11, color=WARM_D)

    # 物品总量 N = 18
    seg(ax, (18, yB - 0.35), (18, yA + h + 0.55), color=INK, lw=1.4,
        ls=(0, (5, 3)), z=5)
    text(ax, 18, yA + h + 0.85, "$N$", size=14)

    text(ax, 20.6, yA + h / 2, "$4\\times5=20$", size=13, ha="left",
         color=TEAL_D)
    text(ax, 18.6, yB + h / 2 - 0.02, "$4\\times3=12$", size=13, ha="left",
         color=TEAL_D)
    text(ax, 0, -0.55, "$(6+2)\\div(5-3)=4$", size=17)

    ax.set_xlim(-2.2, 34.5)
    ax.set_ylim(-1.05, 2.85)
    ax.axis("off")
    save(fig, "app-profit-loss")


# ---------------------------------------------------------------- 鸡兔同笼
def fig_chicken_rabbit():
    """假设全是鸡：脚数 30，比 40 少 10；每换一只兔多 2 只脚，故 5 只兔。"""
    fig, ax = new_fig(9.8, 3.8)
    h = 0.60
    y1, y2 = 1.75, 0.90

    bar(ax, 0, 30, y1, h, TEAL2, alpha=0.95)
    text(ax, 15, y1 + h / 2, "$2\\times15=30$", size=13)

    bar(ax, 0, 30, y2, h, TEAL2, alpha=0.95)
    for i in range(5):
        bar(ax, 30 + 2 * i, 32 + 2 * i, y2, h, WARM, alpha=0.95, lw=1.2)
    text(ax, 15, y2 + h / 2, "$30$", size=12)
    text(ax, -0.8, y2 + h / 2, "$40$", size=13, ha="right", color=TEAL_D)

    # 多出来的 10 只脚 = 5 只兔 × 2
    bracket(ax, (30, y2 - 0.22), (40, y2 - 0.22), color=WARM_D, tick=0.13)
    text(ax, 35, y2 - 0.66, "$10=5\\times2$", size=13, color=WARM_D)

    text(ax, 0, 3.18, "$(40-2\\times15)\\div(4-2)=5$", size=16)
    text(ax, 0, 2.62, "$15-5=10$", size=14, color=TEAL_D)

    ax.set_xlim(-4.0, 52)
    ax.set_ylim(-1.15, 3.55)
    ax.axis("off")
    save(fig, "app-chicken-rabbit")


# ---------------------------------------------------------------- 和差问题
def fig_sum_difference():
    """把短段补上差，两段一样长：总和加差就是两个大数。"""
    fig, ax = new_fig(10.4, 4.2)
    h = 0.52
    A, B, D = 54, 36, 18

    # 左：两段并列，多出来的 18 就是差
    bar(ax, 0, A, 1.05, h, TEAL)
    bar(ax, 0, B, 0.25, h, WARM2)
    bar(ax, B, A, 1.05, h, WARM, alpha=0.95, lw=1.3, edge=WARM_D)
    text(ax, 27, 1.05 + h / 2, "$A=54$", size=13)
    text(ax, 18, 0.25 + h / 2, "$B=36$", size=13)
    text(ax, 45, 1.05 + h / 2, "$18$", size=11.5, color=WARM_D)
    seg(ax, (B, 0.2), (B, 1.62), color=INK, lw=1.2, ls=(0, (4, 3)), z=4)
    bracket(ax, (36, 1.95), (54, 1.95), color=WARM_D, tick=0.12)
    text(ax, 45, 2.32, "$A-B=18$", size=12.5, color=WARM_D)
    text(ax, 27, -0.55, "$A+B=90$", size=14, color=TEAL_D)

    # 右：接起来，补上差 → 两个 54
    x0 = 64
    bar(ax, x0, x0 + A, 0.65, h, TEAL)
    bar(ax, x0 + A, x0 + A + B, 0.65, h, WARM2)
    bar(ax, x0 + A + B, x0 + 2 * A, 0.65, h, WARM, alpha=0.95, lw=1.3,
        edge=WARM_D)
    text(ax, x0 + 27, 0.65 + h / 2, "$A$", size=13)
    text(ax, x0 + A + 18, 0.65 + h / 2, "$B$", size=13)
    text(ax, x0 + A + 45, 0.65 + h / 2, "$18$", size=11, color=WARM_D)
    seg(ax, (x0 + A, 0.55), (x0 + A, 1.45), color=INK, lw=1.4, z=4)
    bracket(ax, (x0, 1.72), (x0 + A, 1.72), color=TEAL_D, tick=0.12)
    bracket(ax, (x0 + A, 1.72), (x0 + 2 * A, 1.72), color=TEAL_D, tick=0.12)
    text(ax, x0 + 27, 2.12, "$A$", size=13, color=TEAL_D)
    text(ax, x0 + A + 27, 2.12, "$A$", size=13, color=TEAL_D)
    text(ax, x0 + 54, -0.55, "$2A=90+18=108$", size=15)
    arrow(ax, (57, 0.9), (62.5, 0.9), color=MUTED, lw=1.5, scale=15)

    ax.set_xlim(-4.5, 178)
    ax.set_ylim(-1.35, 3.05)
    ax.axis("off")
    save(fig, "app-sum-difference")


# ---------------------------------------------------------------- 平均数
def fig_average():
    """移多补少：高出来的部分正好填平矮的部分，四条一样高就是平均数。"""
    fig, ax = new_fig(7.8, 4.6)
    vals = [6, 3, 5, 2]
    avg = 4.0
    w = 0.62

    # 左：参差不齐
    for i, v in enumerate(vals):
        x = i
        base = bar(ax, x - w / 2, x + w / 2, 0, min(v, avg), TEAL2, alpha=0.95)
        if v > avg:
            bar(ax, x - w / 2, x + w / 2, avg, v - avg, WARM, alpha=0.95, lw=1.2)
        elif v < avg:
            rect_outline(ax, x - w / 2, x + w / 2, v, avg - v,
                         color=WARM_D, lw=1.2, ls=(0, (4, 3)))
        text(ax, x, 0.34, "$%d$" % v, size=13)
        seg(ax, (x - w / 2 - 0.12, 0), (x + w / 2 + 0.12, 0), color=INK, lw=1.5, z=6)
    seg(ax, (-0.55, avg), (3.55, avg), color=INK, lw=1.4, ls=(0, (6, 4)), z=5)
    text(ax, -0.62, avg, "$4$", size=13, ha="right")

    # 右：全部拉平
    off = 4.6
    for i in range(4):
        bar(ax, off + i - w / 2, off + i + w / 2, 0, avg, TEAL2, alpha=0.95)
        seg(ax, (off + i - w / 2 - 0.12, 0), (off + i + w / 2 + 0.12, 0),
            color=INK, lw=1.5, z=6)
    seg(ax, (off - 0.55, avg), (off + 3.55, avg), color=INK, lw=1.4,
        ls=(0, (6, 4)), z=5)

    arrow(ax, (1.75, 6.35), (5.75, 4.85), color=MUTED, lw=1.4, scale=14,
          rad=-0.18)
    text(ax, 3.4, 6.75, "$(6+3+5+2)\\div4=4$", size=15)

    finish(ax, (-1.2, 8.5), (-0.9, 7.4))
    save(fig, "app-average")


if __name__ == "__main__":
    fig_tree_planting()
    fig_square_formation()
    fig_concentration()
    fig_grazing()
    fig_work()
    fig_profit_loss()
    fig_chicken_rabbit()
    fig_sum_difference()
    fig_average()
    print("done")
