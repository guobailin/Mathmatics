#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计算模块示意图（issue #74 P0-3）。

图内只用字母、数字与公式（避开中文字体依赖），中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/calc_figures.py
产出：
    assets/geometry/calc-*.svg/.png
    assets/geometry/cards/calc-*.svg
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, poly, outline, seg, dot, text, save,
)

from matplotlib.patches import Arc  # noqa: E402

TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"


def arrow(ax, p, q, color=INK, lw=1.9, ls="-", z=5, scale=13):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=scale),
                zorder=z)


def bracket(ax, p, q, color=MUTED, lw=1.2, tick=0.12, z=4):
    """两点之间的量取线（两端带短垂线）。"""
    seg(ax, p, q, color=color, lw=lw, z=z)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for t in (p, q):
        seg(ax, (t[0] - tick * nx, t[1] - tick * ny),
            (t[0] + tick * nx, t[1] + tick * ny), color=color, lw=lw, z=z)


def arch(ax, p, q, apex, color=MUTED, lw=1.2, z=4):
    """同一水平线上两点的上方弧线，顶点高出 p 的 y 值为 apex。"""
    mx = (p[0] + q[0]) / 2
    ax.add_patch(Arc((mx, p[1]), abs(q[0] - p[0]), 2 * apex,
                     angle=0, theta1=0, theta2=180,
                     color=color, lw=lw, zorder=z))


# ---------------------------------------------------------------- 等差数列
def fig_arithmetic():
    """两条阶梯咬合成 n×(a1+an) 的长方形：2S = n(a1+an)。"""
    fig, ax = new_fig(8.8, 6.0)
    vals = [2, 3, 4, 5, 6, 7]
    H = 9                       # a1 + a6
    w = 1.0
    n = len(vals)

    for k, v in enumerate(vals):
        x = k
        poly(ax, [(x - w / 2, 0), (x + w / 2, 0),
                  (x + w / 2, v), (x - w / 2, v)],
             TEAL, alpha=0.85, lw=1.3)
        top = H - vals[n - 1 - k]        # = v，恰好接上
        poly(ax, [(x - w / 2, top), (x + w / 2, top),
                  (x + w / 2, H), (x - w / 2, H)],
             WARM2, alpha=0.95, lw=1.3, edge=WARM)
        text(ax, x, -0.52, f"$a_{k + 1}$", size=13.5)

    outline(ax, [(-w / 2, 0), (n - w / 2, 0),
                 (n - w / 2, H), (-w / 2, H)], color=INK, lw=2.2)

    # 公差 d：相邻两列的高度差
    arrow(ax, (0.5, 2.10), (0.5, 2.92), color=WARM_D, lw=1.6, scale=10)
    text(ax, 0.5, 3.28, "$d$", size=13.5, color=WARM_D, box=True)

    # 上层是倒序的同一串数
    text(ax, 0.0, 7.75, "$a_n$", size=13.5, color=INK)

    bracket(ax, (n - w / 2 + 0.42, 0), (n - w / 2 + 0.42, H), color=MUTED)
    text(ax, n + 1.05, H / 2, "$a_1+a_n$", size=15, ha="left")
    bracket(ax, (-w / 2, -1.02), (n - w / 2, -1.02), color=MUTED)
    text(ax, n / 2, -1.42, "$n$", size=15)

    text(ax, 3.0, 9.78, "$2S_n=n\\,(a_1+a_n)$", size=20)
    text(ax, 3.0, -2.85, "$S_n=\\dfrac{(a_1+a_n)\\,n}{2}$", size=17, color=TEAL_D)

    finish(ax, (-1.25, n + 2.55), (-3.65, 10.55))
    save(fig, "calc-arithmetic-sequence")


# ---------------------------------------------------------------- 平方差
def fig_square_diff():
    """a²−b² 割补成 (a+b)(a−b)：左边挖洞，右边拼成长方形。"""
    fig, ax = new_fig(9.8, 4.2)
    a, b = 5.0, 2.0
    gap = 9.0

    # ---------- 左：a² 挖去 b² ----------
    poly(ax, [(b, 0), (a, 0), (a, a), (b, a)], TEAL, alpha=0.85, lw=1.6)
    poly(ax, [(0, b), (b, b), (b, a), (0, a)], WARM2, alpha=0.95, lw=1.6, edge=WARM)
    poly(ax, [(0, 0), (b, 0), (b, b), (0, b)], GRID, alpha=0.45, lw=1.0,
         edge=MUTED, z=3)
    outline(ax, [(0, 0), (a, 0), (a, a), (0, a)], color=INK, lw=2.2)
    seg(ax, (b, b), (b, a), color=INK, lw=1.4, ls=(0, (5, 3)))

    bracket(ax, (-0.35, 0), (-0.35, a), color=MUTED)
    text(ax, -0.75, a / 2, "$a$", size=15, ha="right")
    bracket(ax, (0, -0.35), (b, -0.35), color=MUTED)
    text(ax, b / 2, -0.78, "$b$", size=15)
    text(ax, 1.0, 1.0, "$b^2$", size=12, color=MUTED)
    text(ax, 3.6, 3.6, "$a^2-b^2$", size=19, color=TEAL_D)

    # ---------- 右：拼成的长方形 ----------
    x0 = gap
    poly(ax, [(x0, 0), (x0 + a, 0), (x0 + a, a - b), (x0, a - b)],
         TEAL, alpha=0.85, lw=1.6)                       # 竖条转 90°
    poly(ax, [(x0 + a, 0), (x0 + a + b, 0),
              (x0 + a + b, a - b), (x0 + a, a - b)],
         WARM2, alpha=0.95, lw=1.6, edge=WARM)           # 上块转 90° 后的另一半
    outline(ax, [(x0, 0), (x0 + a + b, 0),
                 (x0 + a + b, a - b), (x0, a - b)], color=INK, lw=2.0)
    seg(ax, (x0 + a, 0), (x0 + a, a - b), color=INK, lw=1.1, ls=(0, (4, 3)))

    bracket(ax, (x0 - 0.35, 0), (x0 - 0.35, a - b), color=MUTED)
    text(ax, x0 - 0.75, (a - b) / 2, "$a-b$", size=15, ha="right")
    bracket(ax, (x0, -0.35), (x0 + a + b, -0.35), color=MUTED)
    text(ax, x0 + (a + b) / 2, -0.78, "$a+b$", size=15)
    text(ax, x0 + 3.5, 1.5, "$(a+b)(a-b)$", size=16, color=INK)

    arrow(ax, (a + 0.60, 2.95), (gap - 0.80, 2.95), color=MUTED, lw=1.5, scale=16)

    text(ax, gap + (a + b) / 2 - 1.4, 4.35,
         "$a^2-b^2=(a+b)(a-b)$", size=21)

    finish(ax, (-2.0, gap + a + b + 0.8), (-1.65, 5.05))
    save(fig, "calc-square-diff")


# ---------------------------------------------------------------- 分数裂项
def fig_telescoping():
    """1/(k(k+1)) = 1/k − 1/(k+1)：五段首尾相接，铺满 [1/6, 1]。"""
    fig, ax = new_fig(9.6, 5.4)
    n = 5
    h = 0.62

    for k in range(1, n + 1):
        y = n - k                      # k=1 在最上面
        x0, x1 = 1.0 / (k + 1), 1.0 / k
        poly(ax, [(x0, y - h / 2), (x1, y - h / 2),
                  (x1, y + h / 2), (x0, y + h / 2)],
             TEAL if k % 2 else WARM2, alpha=0.9, lw=1.3,
             edge=INK if k % 2 else WARM)


    # 逐层对齐的竖虚线：每段左端恰是下一段的右端
    for k in range(1, n + 1):
        seg(ax, (1.0 / k, -0.42), (1.0 / k, n - 1 + h / 2 + 0.2),
            color=MUTED, lw=1.0, ls=(0, (3, 2)), z=1)

    # 唯一没被盖住的那一段
    poly(ax, [(0.0, -h / 2), (1.0 / (n + 1), -h / 2),
              (1.0 / (n + 1), h / 2), (0.0, h / 2)],
         GRID, alpha=0.5, lw=1.1, edge=MUTED)
    text(ax, -0.03, 0, "$\\dfrac{1}{n+1}$", size=12.5, color=MUTED, ha="right")

    # 坐标轴
    seg(ax, (-0.01, -0.72), (1.03, -0.72), color=MUTED, lw=1.2)
    for j, k in enumerate(range(1, n + 2)):
        v = 1.0 / k
        seg(ax, (v, -0.78), (v, -0.66), color=MUTED, lw=1.1)
        yy = -1.12 if j % 2 == 0 else -1.56
        lab = "$1$" if k == 1 else f"$\\frac{{1}}{{{k}}}$"
        text(ax, v, yy, lab, size=12 if k > 1 else 13, color=MUTED)
    text(ax, -0.01, -1.12, "$0$", size=12.5, color=MUTED, ha="right")

    # 整段长度 = 1 − 1/(n+1)
    bracket(ax, (1.0 / (n + 1), -2.24), (1.0, -2.24), color=INK, tick=0.16)
    text(ax, (1 + 1.0 / (n + 1)) / 2, -2.80,
         "$1-\\dfrac{1}{n+1}$", size=19, color=TEAL_D)

    text(ax, 1.02, 5.42, "$\\dfrac{1}{k(k+1)}=\\dfrac{1}{k}-\\dfrac{1}{k+1}$",
         size=19, ha="right")

    ax.set_xlim(-0.40, 1.22)
    ax.set_ylim(-3.40, 5.90)
    ax.axis("off")
    save(fig, "calc-telescoping")


# ---------------------------------------------------------------- 循环小数
def fig_repeating():
    """小数点右移一个循环节，小数部分整段相同，相减即消。"""
    fig, ax = new_fig(10.0, 4.4)
    dx = 0.36
    d0 = 0.30
    digits = "142857"
    xend = d0 + 12 * dx

    def row(y, s, start, size=14):
        for i, ch in enumerate(s):
            text(ax, start + i * dx, y, f"${ch}$", size=size)

    def overline(y, start, count):
        seg(ax, (start - 0.13, y + 0.33), (start + (count - 1) * dx + 0.13, y + 0.33),
            color=WARM_D, lw=1.6)
        for i in (0, count - 1):
            x = start + i * dx
            seg(ax, (x - 0.13, y + 0.33), (x - 0.13, y + 0.24),
                color=WARM_D, lw=1.6)

    # 两行完全相同的那一段
    poly(ax, [(d0 - 0.17, 0.60), (xend - 0.04, 0.60),
              (xend - 0.04, -1.70), (d0 - 0.17, -1.70)],
         TEAL2, alpha=0.5, lw=0, z=0)

    # 第一行
    text(ax, d0 - 0.32, 0, "$0.$", size=16, color=MUTED, ha="right")
    row(0, digits * 2, d0)
    overline(0, d0, 6)
    overline(0, d0 + 6 * dx, 6)
    text(ax, xend + 0.20, 0, "$\\cdots$", size=15, ha="left")
    text(ax, xend + 0.78, 0, "$=x$", size=15, ha="left")

    # 第二行：小数点右移 6 位
    row(-1.55, digits, d0 - 6 * dx)
    text(ax, d0 - 0.18, -1.55, "$.$", size=16, color=MUTED, ha="center")
    row(-1.55, digits * 2, d0)
    overline(-1.55, d0, 6)
    overline(-1.55, d0 + 6 * dx, 6)
    text(ax, xend + 0.20, -1.55, "$\\cdots$", size=15, ha="left")
    text(ax, xend + 0.78, -1.55, "$=10^6x$", size=15, ha="left")

    arrow(ax, (xend + 2.30, -0.28), (xend + 2.30, -1.24),
          color=WARM_D, lw=1.3, scale=10)
    text(ax, xend + 2.44, -0.76, "$\\times10^6$", size=12,
         color=WARM_D, ha="left")

    # 两行相减
    seg(ax, (-1.90, -2.12), (xend + 0.25, -2.12), color=INK, lw=1.4)
    text(ax, -1.90, -2.55, "$10^6x-x=142857$", size=17, ha="left")
    text(ax, -1.90, -3.22,
         "$x=\\dfrac{142857}{999999}=\\dfrac{1}{7}$", size=19, ha="left",
         color=TEAL_D)
    text(ax, 3.05, 0.98, "$n=6$", size=13, color=WARM_D)

    finish(ax, (-2.30, xend + 3.75), (-3.70, 1.55))
    save(fig, "calc-repeating-decimal")


# ---------------------------------------------------------------- 速算凑整
def fig_quick_pair():
    """打乱顺序后按补数配对：2+8、87+13、124+876 各凑成 10/100/1000。"""
    fig, ax = new_fig(9.6, 5.0)
    vals = [2, 87, 124, 876, 13, 8]
    xs = [i * 1.72 for i in range(6)]
    w, hh = 1.12, 0.86

    for x, v in zip(xs, vals):
        poly(ax, [(x - w / 2, -hh / 2), (x + w / 2, -hh / 2),
                  (x + w / 2, hh / 2), (x - w / 2, hh / 2)],
             TEAL2, alpha=0.95, lw=1.5, edge=TEAL_D)
        text(ax, x, 0, f"${v}$", size=17)

    # 由外到内三条配对弧：外圈 2+8，中圈 87+13，内圈 124+876
    for (i, j), apex, lab in [((0, 5), 2.42, "$2+8=10$"),
                              ((1, 4), 1.72, "$87+13=100$"),
                              ((2, 3), 1.02, "$124+876=1000$")]:
        arch(ax, (xs[i], hh / 2 + 0.04), (xs[j], hh / 2 + 0.04),
             apex, color=WARM_D, lw=1.5)
        text(ax, (xs[i] + xs[j]) / 2, hh / 2 + apex + 0.30, lab,
             size=13.5, color=WARM_D)

    text(ax, xs[5] + 0.32, -0.80, "$10+100+1000=1110$", size=17,
         ha="right", color=TEAL_D)
    text(ax, xs[0] - 0.62, -0.80, "$a+b=10^k$", size=14,
         ha="left", color=MUTED)

    finish(ax, (-0.95, xs[5] + 0.75), (-1.45, 3.95))
    save(fig, "calc-quick-pair")


# ---------------------------------------------------------------- 数表方框
def fig_table_frame():
    """日历 3×3 方框：九格相对中心的偏移 −8…+8 相加为 0，故和为 9x。"""
    fig, ax = new_fig(9.8, 4.2)
    cell = 1.0
    days = [[None, None, 1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17, 18, 19]]

    for r, rowv in enumerate(days):
        for c, v in enumerate(rowv):
            x, y = c * cell, (2 - r) * cell
            if v is not None:
                text(ax, x + cell / 2, y + cell / 2, f"${v}$", size=14)

    for c in range(8):
        seg(ax, (c * cell, 0), (c * cell, 3 * cell), color=GRID, lw=1.0, z=1)
    for r in range(4):
        seg(ax, (0, r * cell), (7 * cell, r * cell), color=GRID, lw=1.0, z=1)

    # 3×3 方框
    poly(ax, [(2 * cell, 0), (5 * cell, 0),
              (5 * cell, 3 * cell), (2 * cell, 3 * cell)],
         TEAL2, alpha=0.5, lw=0, z=0)
    outline(ax, [(2 * cell, 0), (5 * cell, 0),
                 (5 * cell, 3 * cell), (2 * cell, 3 * cell)],
            color=WARM_D, lw=2.4, z=6)
    text(ax, 3.5 * cell, -0.52, "$3\\times3$", size=14, color=WARM_D)

    # 右侧：相对中心的偏移
    ox, oy = 8.7, 0.1
    for r, rowv in enumerate([[-8, -7, -6], [-1, 0, 1], [6, 7, 8]]):
        for c, v in enumerate(rowv):
            x, y = ox + c * cell, oy + (2 - r) * cell
            if v == 0:
                poly(ax, [(x, y), (x + cell, y), (x + cell, y + cell), (x, y + cell)],
                     WARM2, alpha=0.95, lw=0, z=1)
            outline(ax, [(x, y), (x + cell, y), (x + cell, y + cell), (x, y + cell)],
                    color=MUTED, lw=1.0, z=2)
            s = "$x$" if v == 0 else f"${v:+d}$"
            text(ax, x + cell / 2, y + cell / 2, s, size=13,
                 color=WARM_D if v == 0 else INK)

    arrow(ax, (7.55, 1.55), (8.30, 1.55), color=MUTED, lw=1.4, scale=13)
    text(ax, ox + 1.5, 3.60, "$\\sum=0$", size=15, color=MUTED)
    text(ax, ox + 1.5, -0.55, "$\\sum=9x=81$", size=14, color=TEAL_D)

    finish(ax, (-0.55, 12.6), (-1.10, 4.00))
    save(fig, "calc-table-frame")


if __name__ == "__main__":
    fig_arithmetic()
    fig_square_diff()
    fig_telescoping()
    fig_repeating()
    fig_quick_pair()
    fig_table_frame()
    print("done")
