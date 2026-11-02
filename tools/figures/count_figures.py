#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计数模块示意图（issue #74 P0-3）。

图内只用字母、数字与公式（与几何、行程篇一致，避开中文字体依赖），
中文解释一律写在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/count_figures.py
产出：
    assets/geometry/cnt-*.svg/.png
    assets/geometry/cards/cnt-*.svg
"""
import os
import sys
from math import comb, cos, radians, sin

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, poly, seg, dot, text, save, intersection,
)
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch  # noqa: E402

# 浅色只用于色块与粗线条，文字另用同族深色，保证白底可读。
TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"
GREY_D = "#6b7a73"


def box(ax, cx, cy, w, h, fc="none", ec=INK, lw=1.5, ls="-", z=2, alpha=1.0):
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, facecolor=fc,
                           edgecolor=ec, linewidth=lw, linestyle=ls, zorder=z,
                           alpha=alpha, joinstyle="round"))


def arrow(ax, tail, tip, color=INK, lw=2.2, ms=14, z=4, ls="-",
          rad=0.0, shrink=0.0):
    ax.add_patch(FancyArrowPatch(
        tail, tip, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
        linestyle=ls, zorder=z, shrinkA=shrink, shrinkB=shrink,
        connectionstyle=f"arc3,rad={rad}"))


def hbracket(ax, x1, x2, y, label, color=MUTED, size=13, tick=0.12, dy=-0.34):
    seg(ax, (x1, y), (x2, y), color=color, lw=1.1, z=2)
    for x in (x1, x2):
        seg(ax, (x, y - tick), (x, y + tick), color=color, lw=1.1, z=2)
    text(ax, (x1 + x2) / 2, y + dy, label, size=size, color=color)


def vbracket(ax, y1, y2, x, label, color=MUTED, size=13, tick=0.12, dx=-0.34):
    seg(ax, (x, y1), (x, y2), color=color, lw=1.1, z=2)
    for y in (y1, y2):
        seg(ax, (x - tick, y), (x + tick, y), color=color, lw=1.1, z=2)
    text(ax, x + dx, (y1 + y2) / 2, label, size=size, color=color, ha="right")


# ---------------------------------------------------------------- 容斥：两量
def fig_venn_two():
    """两量容斥：交集被 |A|、|B| 各数一遍，所以并集要减掉它一次。"""
    fig, ax = new_fig(7.6, 4.8)
    r = 1.55
    cA, cB = (-0.80, 0.0), (0.80, 0.0)

    for c, fc, ec in ((cA, TEAL, TEAL_D), (cB, WARM, WARM_D)):
        ax.add_patch(Circle(c, r, facecolor=fc, edgecolor="none",
                            alpha=0.45, zorder=1))
        ax.add_patch(Circle(c, r, facecolor="none", edgecolor=ec,
                            lw=1.8, zorder=3))

    text(ax, -0.98, 1.16, "$|A|=33$", size=15, color=TEAL_D)
    text(ax, 0.98, 1.16, "$|B|=20$", size=15, color=WARM_D)

    text(ax, -1.44, -0.05, "27", size=17)
    text(ax, 0.0, 0.02, "6", size=18, weight="bold")
    text(ax, 1.44, -0.05, "14", size=17)

    text(ax, 0.0, -0.78, "$\\times 2$", size=13, color=WARM_D)
    text(ax, 0.0, -2.28, "$|A\\cup B|=33+20-6=47$", size=16)

    finish(ax, (-2.6, 2.6), (-2.95, 2.05))
    save(fig, "cnt-venn-two")


# ---------------------------------------------------------------- 容斥：三量
def fig_venn_three():
    """三量容斥：七个区域各是一个数，交集里的数被重复计数。"""
    fig, ax = new_fig(6.6, 6.2)
    r = 1.42
    cA = (0.0, 0.90)
    cB = (-0.78, -0.46)
    cC = (0.78, -0.46)
    for c, fc, ec in ((cA, TEAL, TEAL_D), (cB, WARM, WARM_D),
                      (cC, TEAL2, GREY_D)):
        ax.add_patch(Circle(c, r, facecolor=fc, edgecolor="none",
                            alpha=0.45, zorder=1))
        ax.add_patch(Circle(c, r, facecolor="none", edgecolor=ec,
                            lw=1.7, zorder=3))

    text(ax, 0.0, 2.56, "$A=30$", size=13, color=TEAL_D)
    text(ax, -2.62, -1.80, "$B=26$", size=13, color=WARM_D)
    text(ax, 2.62, -1.80, "$C=24$", size=13, color=GREY_D)

    # 只参加一项
    text(ax, 0.0, 1.34, "11", size=13)
    text(ax, -1.40, -0.86, "3", size=13)
    text(ax, 1.40, -0.86, "5", size=13)
    # 恰好两项
    text(ax, -0.60, 0.62, "9", size=13)
    text(ax, 0.60, 0.62, "5", size=13)
    text(ax, 0.0, -1.06, "9", size=13)
    # 三项都参加
    text(ax, 0.0, 0.02, "5", size=14, weight="bold")
    # 三项都不参加
    text(ax, -2.70, 1.70, "$n=3$", size=13, color=MUTED)

    text(ax, 0.0, -2.62, "$30+26+24-14-10-14+5=47$", size=12)

    finish(ax, (-2.95, 2.95), (-2.95, 2.95))
    save(fig, "cnt-venn-three")


# ------------------------------------------------------------ 容斥最值：下界
def fig_ie_overlap():
    """两量并集被 40 人装满：26 与 22 两段怎么摆都要重叠至少 8。"""
    fig, ax = new_fig(8.0, 4.4)
    L = 40.0
    a, b = 26.0, 22.0
    yA, yB, bh = 2.05, 0.95, 0.62

    box(ax, L / 2, 1.55, L, 3.0, fc="none", ec=MUTED, lw=1.5, ls=(0, (6, 3)))
    text(ax, 1.2, -0.95, "$|U|=40$", size=14, color=MUTED, ha="left")

    # 重叠带：两段都被数到的 8 人
    ax.add_patch(Rectangle((L - b, 0.35), a - (L - b), 2.72, facecolor=TEAL2,
                           edgecolor="none", alpha=0.85, zorder=1))

    ax.add_patch(Rectangle((0, yA - bh / 2), a, bh, facecolor=TEAL,
                           edgecolor=TEAL_D, lw=1.4, alpha=0.9, zorder=2))
    ax.add_patch(Rectangle((L - b, yB - bh / 2), b, bh, facecolor=WARM,
                           edgecolor=WARM_D, lw=1.4, alpha=0.9, zorder=2))
    text(ax, a / 2 - 1.4, yA, "$|A|=26$", size=13, color=INK, z=6)
    text(ax, L - b / 2 + 1.4, yB, "$|B|=22$", size=13, color=INK, z=6)

    x1, x2 = L - b, a
    for x in (x1, x2):
        seg(ax, (x, 0.18), (x, 3.32), color=INK, lw=1.1, ls=":", z=5)
    seg(ax, (x1, 3.32), (x2, 3.32), color=INK, lw=1.2, z=5)
    for x in (x1, x2):
        seg(ax, (x, 3.14), (x, 3.50), color=INK, lw=1.2, z=5)
    text(ax, (x1 + x2) / 2, 3.80, "$8$", size=15)

    text(ax, L / 2, -2.25, "$|A\\cap B|\\geq 26+22-40=8$", size=15)

    ax.set_xlim(-2.5, 42.5)
    ax.set_ylim(-2.95, 4.35)
    ax.set_aspect("auto")
    ax.axis("off")
    save(fig, "cnt-ie-overlap")


# ---------------------------------------------------------------- 抽屉原理
def fig_pigeonhole():
    """最坏情形：每只抽屉 3 个共 12 个还不出现 4 个，再加 1 个必然破局。"""
    fig, ax = new_fig(8.2, 5.6)
    n = 4
    bw, bh, gap = 1.10, 3.40, 0.62
    xs = [gap + bw / 2 + i * (bw + gap) for i in range(n)]
    ys = [0.55, 1.40, 2.25]

    for i, cx in enumerate(xs):
        full = (i == 1)
        box(ax, cx, 1.85, bw, bh, fc=WARM2 if full else "none", ec=GREY_D, lw=1.6)
        for y in ys:
            dot(ax, (cx, y), ms=13, color=TEAL)
            dot(ax, (cx, y), ms=7.5, color=TEAL_D)
        if full:
            dot(ax, (cx, 3.10), ms=13, color=WARM)
            dot(ax, (cx, 3.10), ms=7.5, color=WARM_D)
            arrow(ax, (cx - 0.58, 3.10), (cx - 0.14, 3.10), color=WARM_D,
                  lw=1.6, ms=12, z=6)
            text(ax, cx - 0.70, 3.10, "$+1$", size=14, color=WARM_D, ha="right")
        text(ax, cx, -0.42, "$4$" if full else "$3$", size=15,
             color=WARM_D if full else MUTED,
             weight="bold" if full else None)

    cx_all = (xs[0] + xs[-1]) / 2
    text(ax, cx_all, -1.20, "$4\\times(4-1)+1=13$", size=16)
    text(ax, cx_all, 4.30, "$n=4,\\ k=4,\\ m=13$", size=15)
    text(ax, xs[-1] + 0.95, 1.85, "$\\left\\lceil\\dfrac{13}{4}\\right\\rceil=4$",
         size=16, ha="left")

    finish(ax, (-0.55, xs[-1] + 2.45), (-1.85, 4.90))
    save(fig, "cnt-pigeonhole")


# ------------------------------------------------------------------ 标数法
def fig_grid_path():
    """标数表：每点写"从 A 到这里有几条路"，右 4 上 3 的终点是 35。"""
    fig, ax = new_fig(7.0, 5.6)
    s = 1.62
    nx, ny = 4, 3

    for i in range(nx + 1):
        seg(ax, (i * s, 0), (i * s, ny * s), color=GRID, lw=1.2, z=1)
    for j in range(ny + 1):
        seg(ax, (0, j * s), (nx * s, j * s), color=GRID, lw=1.2, z=1)

    for i in range(nx + 1):
        for j in range(ny + 1):
            v = comb(i + j, i)
            if (i, j) == (nx, ny):
                text(ax, i * s, j * s, "$%d$" % v, size=14, color=WARM_D,
                     weight="bold", box=True)
            elif (i, j) == (0, 0):
                text(ax, i * s, j * s, "$1$", size=12, color=TEAL_D, box=True)
            else:
                text(ax, i * s, j * s, "$%d$" % v, size=11, color=INK, box=True)

    text(ax, -0.95, -0.05, "$A$", size=15)
    text(ax, nx * s + 0.95, ny * s + 0.15, "$B$", size=15)
    text(ax, 1.15 * s, ny * s + 1.15, "$35=\\binom{7}{3}$", size=14)
    text(ax, 2 * s, -1.55, "$f(i,j)=f(i-1,j)+f(i,j-1)$", size=13)

    finish(ax, (-1.25, nx * s + 1.30), (-2.05, ny * s + 1.75))
    save(fig, "cnt-grid-path")


# ------------------------------------------------------------------ 递推
def fig_stairs():
    """到第 n 级只有两种最后一步：从第 n-1 级跨 1 级，或从第 n-2 级跨 2 级。"""
    fig, ax = new_fig(7.8, 4.6)
    vals = [1, 2, 3, 5, 8]
    w, h = 1.10, 0.74
    xs = [0.70 + k * 1.40 for k in range(5)]
    yy = 0.0
    ty = h / 2

    for k, cx in enumerate(xs):
        fc = TEAL if k == 4 else (TEAL2 if k >= 2 else "white")
        box(ax, cx, yy, w, h, fc=fc, ec=TEAL_D, lw=1.5)
        text(ax, cx, yy, "$%d$" % vals[k], size=15, color=TEAL_D, weight="bold")
        text(ax, cx, yy - ty - 0.30, "$a_{%d}$" % (k + 1), size=12, color=MUTED)

    # 最后一步跨 1 级：a_{n-1} -> a_n
    arrow(ax, (xs[3], ty + 0.28), (xs[4], ty + 0.28), color=WARM_D, lw=2.0,
          ms=13)
    text(ax, (xs[3] + xs[4]) / 2, ty + 0.60, "$1$", size=13, color=WARM_D)

    # 最后一步跨 2 级：a_{n-2} -> a_n，从上方绕过去
    top = 1.34
    seg(ax, (xs[2], ty + 0.02), (xs[2], top), color=GREY_D, lw=1.4,
        ls=(0, (4, 2.6)))
    seg(ax, (xs[2], top), (xs[4], top), color=GREY_D, lw=1.4, ls=(0, (4, 2.6)))
    arrow(ax, (xs[4], top - 0.02), (xs[4], ty + 0.14), color=GREY_D, lw=1.4,
          ms=12, ls=(0, (4, 2.6)))
    text(ax, (xs[2] + xs[4]) / 2, top + 0.26, "$2$", size=13, color=GREY_D)

    text(ax, 3.55, 2.20, "$a_n=a_{n-1}+a_{n-2}$", size=16)
    finish(ax, (-0.30, 7.30), (-1.20, 2.45))
    save(fig, "cnt-stairs")


# --------------------------------------------------------------- 线分圆环
def fig_circle_lines():
    """第 3 条弦被前两条切成 3 段，所以恰好多出 3 块。"""
    fig, ax = new_fig(6.4, 6.2)
    R = 2.0
    ax.add_patch(Circle((0, 0), R, facecolor="none", edgecolor=INK, lw=1.8,
                        zorder=3))

    def pt(deg):
        return (R * cos(radians(deg)), R * sin(radians(deg)))

    # 六个端点按星形配对，保证三条弦两两交于圆内、且无三线共点
    angs = (19, 67, 135, 174, 261, 313)
    ch = ((angs[0], angs[3]), (angs[1], angs[4]), (angs[2], angs[5]))
    for idx, (a1, a2) in enumerate(ch):
        if idx == 2:
            continue
        seg(ax, pt(a1), pt(a2), color=GREY_D, lw=1.6, z=2)

    a, b = pt(ch[2][0]), pt(ch[2][1])
    seg(ax, a, b, color=WARM, lw=4.2, z=4)
    seg(ax, a, b, color=WARM_D, lw=1.1, z=5)

    q1 = intersection(a, b, pt(ch[0][0]), pt(ch[0][1]))
    q2 = intersection(a, b, pt(ch[1][0]), pt(ch[1][1]))
    seq = sorted([a, q1, q2, b], key=lambda p: (p[0] - a[0]) ** 2 + (p[1] - a[1]) ** 2)

    dx, dy = b[0] - a[0], b[1] - a[1]
    L = (dx ** 2 + dy ** 2) ** 0.5
    nx, ny = -dy / L, dx / L
    for i in range(3):
        mx = (seq[i][0] + seq[i + 1][0]) / 2
        my = (seq[i][1] + seq[i + 1][1]) / 2
        if nx * (0 - mx) + ny * (0 - my) < 0:
            ox, oy = -nx, -ny
        else:
            ox, oy = nx, ny
        text(ax, mx + 0.30 * ox, my + 0.30 * oy, "$%d$" % (i + 1), size=13,
             color=WARM_D)
    for p in (q1, q2):
        dot(ax, p, ms=7, color=INK, z=6)

    text(ax, 0.0, -2.62, "$1+3+\\binom{3}{2}=7$", size=15)
    finish(ax, (-2.5, 2.5), (-3.05, 2.35))
    save(fig, "cnt-circle-lines")


# --------------------------------------------------------------- 几何计数
def fig_rect_count():
    """长方形 = 选两条横线 × 选两条竖线；先全算，再挑一组出来。"""
    fig, ax = new_fig(7.4, 5.2)
    nx, ny = 3, 2
    s = 1.22
    pick_v = (0, 2)
    pick_h = (0, 2)

    ax.add_patch(Rectangle((pick_v[0] * s, pick_h[0] * s),
                           (pick_v[1] - pick_v[0]) * s,
                           (pick_h[1] - pick_h[0]) * s,
                           facecolor=TEAL2, edgecolor="none", alpha=0.85,
                           zorder=1))

    for i in range(nx + 1):
        c = INK if i in pick_v else GRID
        seg(ax, (i * s, 0), (i * s, ny * s), color=c,
            lw=2.4 if i in pick_v else 1.3, z=3 if i in pick_v else 2)
    for j in range(ny + 1):
        c = INK if j in pick_h else GRID
        seg(ax, (0, j * s), (nx * s, j * s), color=c,
            lw=2.4 if j in pick_h else 1.3, z=3 if j in pick_h else 2)

    hbracket(ax, -0.06, nx * s + 0.06, -0.52, "$C_4^2=6$")
    vbracket(ax, -0.06, ny * s + 0.06, -0.52, "$C_3^2=3$")
    text(ax, nx * s / 2, ny * s + 0.62, "$C_4^2\\times C_3^2=6\\times3=18$",
         size=16)

    finish(ax, (-1.55, nx * s + 0.45), (-1.25, ny * s + 1.05))
    save(fig, "cnt-rect-count")


# ------------------------------------------------------------------ 插空法
def fig_gaps():
    """4 个隔板隔出 5 个空，每空至多放一个，才保证互不相邻。"""
    fig, ax = new_fig(8.2, 4.2)
    bw, gapx = 0.82, 1.86
    xs = [1.30 + i * gapx for i in range(4)]
    gx = [0.37 + i * gapx for i in range(5)]

    for x in gx:
        ax.add_patch(Circle((x, 0), 0.30, facecolor="none", edgecolor=GRID,
                            lw=1.2, ls=(0, (3, 2.5)), zorder=2))
        text(ax, x, 0.64, "$\\leq 1$", size=9, color=MUTED)
    for i, x in enumerate(xs):
        box(ax, x, 0, bw, bw, fc=TEAL, ec=TEAL_D, lw=1.5)
        text(ax, x, 0, "$B$", size=12, color=TEAL_D, weight="bold")

    for x, ch in zip((gx[0], gx[2], gx[3]), ("$a$", "$b$", "$c$")):
        ax.add_patch(Circle((x, 0), 0.20, facecolor=WARM, edgecolor=WARM_D,
                            lw=1.2, zorder=4))
        text(ax, x, 0, ch, size=8, color=WARM_D)

    for i, x in enumerate(gx):
        text(ax, x, -0.72, "$%d$" % (i + 1), size=11, color=MUTED)

    text(ax, 3.66, -1.55, "$4!\\times A_5^3=1440$", size=16)
    finish(ax, (-0.30, 8.20), (-2.05, 1.15))
    save(fig, "cnt-gaps")


# --------------------------------------------------------------- 捆绑 + 除序
def fig_bundle():
    """a、b、c 先捆成一个整体 X，整体与 d、e 排队，再乘回内部 3!。"""
    fig, ax = new_fig(7.8, 5.6)
    s = 0.80
    top_y = 2.45
    xs_top = [1.05, 2.15, 3.25, 4.75, 5.95]

    for x, ch in zip(xs_top, "abcde"):
        box(ax, x, top_y, s, s, fc="white", ec=GREY_D, lw=1.4)
        text(ax, x, top_y, "$%s$" % ch, size=13)
    bx = xs_top[1]
    box(ax, bx, top_y, 3 * 1.10 + 0.14, s + 0.44, fc="none", ec=WARM_D,
        lw=1.8, ls=(0, (5, 3)), z=3)
    text(ax, bx, top_y + 0.92, "$X$", size=14, color=WARM_D)

    bot_y = 0.0
    ux = [bx, 4.75, 5.95]
    box(ax, ux[0], bot_y + 0.02, 1.55, 1.45, fc=WARM2, ec=WARM_D, lw=1.6)
    text(ax, ux[0], bot_y + 0.34, "$X$", size=11, color=WARM_D, weight="bold")
    text(ax, ux[0], bot_y - 0.34, "$3!$", size=10, color=WARM_D)
    for x, ch in zip(ux[1:], "de"):
        box(ax, x, bot_y, s, s, fc="white", ec=GREY_D, lw=1.4)
        text(ax, x, bot_y, "$%s$" % ch, size=13)

    arrow(ax, (bx, top_y - 0.68), (bx, bot_y + 0.80), color=GREY_D,
          lw=1.6, ms=14, ls=(0, (4, 2)))

    hbracket(ax, ux[0] - 0.80, ux[2] + 0.46, bot_y - 0.90, "$3!$", dy=-0.52)
    text(ax, (ux[0] + ux[2]) / 2, -2.60, "$3!\\times 3! = 36$", size=15)

    finish(ax, (-0.25, 6.65), (-3.10, 3.60))
    save(fig, "cnt-bundle")


# ------------------------------------------------------------- 轴对称计数
def fig_symmetry():
    """3×3 棋盘关于中线对称：中间一列是不动点，两侧成对必须同色。"""
    fig, ax = new_fig(6.2, 6.0)
    s = 1.12
    pair_fill = {0: WARM2, 1: TEAL2, 2: TEAL}
    pair_name = {0: "c", 1: "b", 2: "a"}

    for i in range(3):
        for j in range(3):
            cx, cy = (i + 0.5) * s, (j + 0.5) * s
            if i == 1:
                fc, lab, col = WARM, "$t$", WARM_D
            else:
                fc, lab, col = pair_fill[j], "$%s$" % pair_name[j], TEAL_D
            box(ax, cx, cy, s * 0.94, s * 0.94, fc=fc, ec=GREY_D, lw=1.3)
            text(ax, cx, cy, lab, size=15, color=col, weight="bold",
                 box=(i == 1))

    seg(ax, (1.5 * s, -0.38), (1.5 * s, 3 * s + 0.38), color=GREY_D,
        lw=1.4, ls=(0, (6, 3)), z=5)
    text(ax, 1.5 * s + 0.16, 3 * s + 0.52, "$l$", size=14, color=GREY_D,
         ha="left")

    text(ax, 1.5 * s, 3 * s + 1.00, "$k^{m+t}=2^{3+3}=64$", size=15)
    finish(ax, (-0.35, 3 * s + 0.35), (-0.55, 3 * s + 1.30))
    save(fig, "cnt-symmetry")


# ------------------------------------------------------------------ 概率
def fig_dice_grid():
    """两枚骰子的 36 个等可能结果；和为 7 的 6 格在同一条对角线上。"""
    fig, ax = new_fig(6.6, 6.2)
    s = 0.80
    for i in range(1, 7):
        for j in range(1, 7):
            cx, cy = (i - 0.5) * s, (j - 0.5) * s
            hit = (i + j == 7)
            box(ax, cx, cy, s * 0.96, s * 0.96,
                fc=WARM if hit else WARM2, ec=GREY_D, lw=1.0,
                alpha=0.95 if hit else 0.55, z=2)
            text(ax, cx, cy, "$%d$" % (i + j), size=9,
                 color=WARM_D if hit else MUTED,
                 weight="bold" if hit else None)

    for i in range(1, 7):
        text(ax, (i - 0.5) * s, -0.50, "$%d$" % i, size=11, color=MUTED)
        text(ax, -0.48, (i - 0.5) * s, "$%d$" % i, size=11, color=MUTED)
    text(ax, 6.35 * s, -1.02, "$i$", size=13, color=MUTED)
    text(ax, -0.95, 6.3 * s, "$j$", size=13, color=MUTED)

    text(ax, 3.0 * s, 6.9 * s, "$i+j=7$", size=13, color=WARM_D)
    text(ax, 3.0 * s, -3.15, "$\\dfrac{6}{36}=\\dfrac{1}{6}$", size=16)

    finish(ax, (-1.25, 6.9 * s), (-3.85, 7.6 * s))
    save(fig, "cnt-dice-grid")


# --------------------------------------------------------------- 加乘原理
def fig_tree():
    """左：分类相加（两棵互不相干的小树）；右：分步相乘（每条枝再分叉）。"""
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.8))
    ax1, ax2 = axes
    XL, YL = (-0.50, 2.60), (-2.30, 2.80)

    # (a) 加法：根分出两类，各自长出一组叶子，总数是两组之和
    root = (0.0, 0.0)
    na, nb = (0.95, 1.05), (0.95, -1.05)
    for nd in (na, nb):
        seg(ax1, root, nd, color=INK, lw=1.4)
        dot(ax1, nd, ms=5.5)
    dot(ax1, root, ms=6)
    for y, col in [(1.62, TEAL_D), (1.05, TEAL_D), (0.48, TEAL_D),
                   (-0.62, WARM_D), (-1.48, WARM_D)]:
        src = na if y > 0 else nb
        seg(ax1, src, (1.88, y), color=col, lw=1.3)
        dot(ax1, (1.88, y), ms=7, color=col)
        dot(ax1, (1.88, y), ms=3.2, color="white")
    text(ax1, 2.12, 1.05, "$3$", size=14, color=TEAL_D)
    text(ax1, 2.12, -1.05, "$2$", size=14, color=WARM_D)
    text(ax1, 1.05, 2.45, "$3+2=5$", size=16)
    text(ax1, 1.05, -2.05, "(a)", size=14, color=MUTED)
    finish(ax1, XL, YL)

    # (b) 乘法：第一步 2 种，每种下面再挂 3 种，叶子数 = 2 x 3
    r2 = (0.0, 0.0)
    m1, m2 = (0.95, 0.60), (0.95, -0.60)
    for nd in (m1, m2):
        seg(ax2, r2, nd, color=INK, lw=1.4)
        dot(ax2, nd, ms=5.5)
    dot(ax2, r2, ms=6)
    for nd in (m1, m2):
        for off in (0.50, 0.0, -0.50):
            y = nd[1] + off
            seg(ax2, nd, (1.90, y), color=TEAL_D, lw=1.3)
            dot(ax2, (1.90, y), ms=7, color=TEAL_D)
            dot(ax2, (1.90, y), ms=3.2, color="white")
    text(ax2, 0.46, 0.82, "$2$", size=14, color=INK)
    text(ax2, 2.14, 0.60, "$3$", size=14, color=TEAL_D)
    text(ax2, 2.14, -0.60, "$3$", size=14, color=TEAL_D)
    text(ax2, 1.05, 2.45, "$2\\times 3=6$", size=16)
    text(ax2, 1.05, -2.05, "(b)", size=14, color=MUTED)
    finish(ax2, XL, YL)

    fig.tight_layout()
    save(fig, "cnt-tree")


if __name__ == "__main__":
    fig_venn_two()
    fig_venn_three()
    fig_ie_overlap()
    fig_pigeonhole()
    fig_grid_path()
    fig_stairs()
    fig_circle_lines()
    fig_rect_count()
    fig_gaps()
    fig_bundle()
    fig_symmetry()
    fig_dice_grid()
    fig_tree()
    print("done")
