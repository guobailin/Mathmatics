#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""组合模块示意图（issue #74 P0-3）。

图内只用字母、数字与公式（避开中文字体依赖），中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/comb_figures.py
产出：
    assets/geometry/comb-*.svg/.png
    assets/geometry/cards/comb-*.svg
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
from matplotlib.patches import Circle  # noqa: E402

TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"


def arrow(ax, p, q, color=INK, lw=1.9, ls="-", z=5, scale=13):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=scale),
                zorder=z)


def bracket(ax, p, q, color=MUTED, lw=1.2, tick=0.12, z=4):
    seg(ax, p, q, color=color, lw=lw, z=z)
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for t in (p, q):
        seg(ax, (t[0] - tick * nx, t[1] - tick * ny),
            (t[0] + tick * nx, t[1] + tick * ny), color=color, lw=lw, z=z)


def node(ax, p, r=0.26, color=TEAL2, edge=INK, lw=1.3, z=3):
    ax.add_patch(Circle(p, r, facecolor=color, edgecolor=edge,
                        linewidth=lw, zorder=z))


def check(ax, c, s=0.20, color=TEAL_D, lw=2.4):
    x, y = c
    ax.plot([x - s, x - s * 0.25, x + s], [y + 0.02, y - s * 0.75, y + s * 0.72],
            color=color, lw=lw, zorder=6, solid_capstyle="round",
            solid_joinstyle="round")


def cross(ax, c, s=0.18, color=MUTED, lw=1.7):
    x, y = c
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=lw, zorder=6,
            solid_capstyle="round")
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=lw, zorder=6,
            solid_capstyle="round")


# ---------------------------------------------------------------- 幻方
def fig_magic_square():
    """三阶幻方：过中心的四条线各被数一次，中心被多算 3 次 → 4S=45+3c。"""
    fig, ax = new_fig(9.2, 4.4)
    grid = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
    cell = 1.0

    # 四条过中心的线
    poly(ax, [(0, 1), (3, 1), (3, 2), (0, 2)], TEAL2, alpha=0.95, lw=0, z=0)
    poly(ax, [(1, 0), (2, 0), (2, 3), (1, 3)], TEAL2, alpha=0.95, lw=0, z=0)
    for p, q in [((0, 0), (3, 3)), ((0, 3), (3, 0))]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=WARM, lw=7, alpha=0.55,
                zorder=0, solid_capstyle="butt")

    for r in range(4):
        seg(ax, (0, r * cell), (3 * cell, r * cell), color=INK, lw=1.2, z=2)
    for c in range(4):
        seg(ax, (c * cell, 0), (c * cell, 3 * cell), color=INK, lw=1.2, z=2)

    for r, rowv in enumerate(grid):
        for c, v in enumerate(rowv):
            text(ax, c + cell / 2, (2 - r) + cell / 2, f"${v}$", size=17)

    ax.add_patch(Circle((1.5, 1.5), 0.40, facecolor="none", edgecolor=WARM_D,
                        lw=1.8, zorder=5))

    text(ax, 4.15, 2.55, "$S=15$", size=17)
    text(ax, 4.15, 1.80, "$4S=45+3c$", size=16)
    text(ax, 4.15, 1.05, "$c=5$", size=16, color=WARM_D)
    text(ax, 4.15, 0.32, "$S=3c$", size=16, color=TEAL_D)

    finish(ax, (-0.55, 7.15), (-0.85, 3.6))
    save(fig, "comb-magic-square")


# ---------------------------------------------------------------- 数阵图
def fig_number_array():
    """两种骨架的重数：辐射型中心 r=5、封闭型顶点 r=2。"""
    fig, ax = new_fig(10.2, 5.0)

    # ---------- 辐射型 ----------
    cx, cy = 2.45, 2.55
    radii = [0.62, 1.24, 1.86]
    angs = [90, 162, 234, 306, 18]
    for a in angs:
        th = math.radians(a)
        p = (cx + radii[-1] * math.cos(th), cy + radii[-1] * math.sin(th))
        seg(ax, (cx, cy), p, color=MUTED, lw=1.5, z=1)
        for rr in radii:
            node(ax, (cx + rr * math.cos(th), cy + rr * math.sin(th)), r=0.24)
    node(ax, (cx, cy), r=0.30, color=WARM, z=4)
    text(ax, cx, cy, "$c$", size=14.5, color=WARM_D)
    text(ax, cx, cy - 0.98, "$r=5$", size=12.5, color=WARM_D)
    text(ax, cx, cy + 2.22, "$r=1$", size=12.5, color=MUTED)
    text(ax, cx, -0.55, "$5S=T+4c$", size=17, color=TEAL_D)

    # ---------- 封闭型 ----------
    A, B, C = (7.15, 0.55), (12.05, 0.55), (9.60, 3.35)

    def lerp(p, q, t):
        return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))

    for p, q in [(A, B), (B, C), (C, A)]:
        seg(ax, p, q, color=MUTED, lw=1.2, z=1)
        for t in (1 / 3, 2 / 3):
            node(ax, lerp(p, q, t))
    for p in (A, B, C):
        node(ax, p, r=0.30, color=WARM, z=4)

    text(ax, 7.15, -0.05, "$r=2$", size=12.5, color=WARM_D)
    text(ax, 9.60, 1.35, "$r=1$", size=12.5, color=MUTED)
    text(ax, 9.60, -0.55, "$3S=T+O$", size=17, color=TEAL_D)
    text(ax, 9.60, 3.95, "$O$", size=13, color=WARM_D)

    finish(ax, (-0.55, 13.0), (-1.15, 6.05))
    save(fig, "comb-number-array")


# ---------------------------------------------------------------- 游戏策略
def fig_game_strategy():
    """补足法：每 m+1 个一捆，先手取余数；双堆同取的必败局按差值排开。"""
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.6))
    for a in (ax, ax2):
        a.set_facecolor("none")
    fig.patch.set_alpha(0)

    # ---------- 左：11 枚棋子，每 4 枚一捆 ----------
    n, m = 11, 3
    r = 0.24
    xs = []
    for i in range(n):
        group = i // (m + 1)
        xs.append(i * 0.64 + group * 0.18)
    for i, x in enumerate(xs):
        col = WARM if i >= 8 else TEAL2
        ax.add_patch(Circle((x, 0.0), r, facecolor=col, edgecolor=INK,
                            linewidth=1.1, zorder=3))
    for g in range(3):
        i0 = g * (m + 1)
        i1 = min(i0 + m, n - 1)
        bracket(ax, (xs[i0] - 0.28, -0.48), (xs[i1] + 0.28, -0.48),
                color=MUTED, tick=0.10)
        lab = "$m+1=4$" if g < 2 else "$r=3$"
        ax.text((xs[i0] + xs[i1]) / 2, -0.92, lab, fontsize=11.5,
                color=MUTED if g < 2 else WARM_D, ha="center", va="center")
    ax.text(xs[0] - 0.30, 1.28, "$n=q(m+1)+r$", fontsize=16, ha="left")
    ax.text(xs[0] - 0.30, 0.72, "$11=2\\times4+3$", fontsize=14,
            color=TEAL_D, ha="left")
    ax.set_xlim(-0.85, xs[-1] + 0.85)
    ax.set_ylim(-1.45, 1.75)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---------- 右：双堆必败局 ----------
    pts = [(0, 0), (1, 2), (3, 5), (4, 7), (6, 10), (8, 13)]
    ax2.set_xlim(-1.6, 16.2)
    ax2.set_ylim(-2.2, 15.6)
    ax2.set_aspect("equal")
    ax2.axis("off")
    seg(ax2, (0, 0), (14.2, 0), color=INK, lw=1.4, z=1)
    seg(ax2, (0, 0), (0, 14.2), color=INK, lw=1.4, z=1)
    for t in range(0, 16, 4):
        seg(ax2, (t, -0.24), (t, 0.0), color=MUTED, lw=1.0)
        ax2.text(t, -0.85, f"${t}$", fontsize=10, color=MUTED, ha="center")
    ax2.text(-1.25, 13.6, "$b$", fontsize=13, color=MUTED)
    ax2.text(15.0, -0.85, "$a$", fontsize=13, color=MUTED)

    seg(ax2, (0, 0), (13.4, 13.4), color=MUTED, lw=1.0, ls=(0, (4, 3)), z=1)
    ax2.text(11.4, 12.5, "$b=a$", fontsize=12.5, color=MUTED)

    for (a, b) in pts:
        ax2.add_patch(Circle((a, b), 0.30, facecolor=WARM, edgecolor=WARM_D,
                             linewidth=1.2, zorder=4))
        seg(ax2, (a, b), (a, 0), color=GRID, lw=1.0, ls=(0, (3, 2)), z=1)
        seg(ax2, (a, b), (0, b), color=GRID, lw=1.0, ls=(0, (3, 2)), z=1)
    # 第 d 个必败局的差恰为 d
    seg(ax2, (6, 6), (6, 10), color=WARM_D, lw=1.3, z=5)
    arrow(ax2, (6, 6.05), (6, 9.95), color=WARM_D, lw=1.2, scale=8, z=5)
    ax2.text(6.42, 8.0, "$d$", fontsize=14, color=WARM_D)
    ax2.text(6.85, 10.95, "$(a,\\ a+d)$", fontsize=13, color=WARM_D,
             ha="left")
    ax2.text(0.30, 2.95, "$L$", fontsize=15, color=WARM_D)

    fig.tight_layout()
    save(fig, "comb-game-strategy")


# ---------------------------------------------------------------- 统筹优化
def fig_scheduling():
    """双机流水的甘特图：A 机不停，B 机只等一次，工期由 B 的总工时卡住。"""
    fig, ax = new_fig(10.4, 4.0)
    h = 0.46
    yA, yB = 1.28, 0.50
    jobs = [  # (名字, A 开机, A 时长, B 开机, B 时长)
        ("$P_4$", 0, 1, 1, 6, TEAL),
        ("$P_2$", 1, 2, 7, 3, TEAL2),
        ("$P_1$", 3, 3, 10, 5, WARM),
        ("$P_3$", 6, 4, 15, 2, WARM2),
    ]

    # B 的等待段
    poly(ax, [(0, yB - h / 2), (1, yB - h / 2), (1, yB + h / 2), (0, yB + h / 2)],
         GRID, alpha=0.55, lw=1.0, edge=MUTED, z=1)
    text(ax, 0.5, yB, "$1$", size=11, color=MUTED)

    for name, a0, a1, b0, b1, col in jobs:
        poly(ax, [(a0, yA - h / 2), (a0 + a1, yA - h / 2),
                  (a0 + a1, yA + h / 2), (a0, yA + h / 2)],
             col, alpha=0.95, lw=1.3, z=3)
        text(ax, a0 + a1 / 2, yA, name, size=11.5)
        poly(ax, [(b0, yB - h / 2), (b0 + b1, yB - h / 2),
                  (b0 + b1, yB + h / 2), (b0, yB + h / 2)],
             col, alpha=0.95, lw=1.3, z=3)
        text(ax, b0 + b1 / 2, yB, name, size=11.5)

    seg(ax, (-0.3, 0), (17.8, 0), color=INK, lw=1.4, z=2)
    for t in range(18):
        seg(ax, (t, -0.08), (t, 0.0), color=MUTED, lw=1.0, z=2)
        text(ax, t, -0.36, f"${t}$", size=10, color=MUTED)
    text(ax, 18.3, -0.36, "$t$", size=12, color=MUTED, ha="left")

    text(ax, -0.35, yA, "$A$", size=14, ha="right")
    text(ax, -0.35, yB, "$B$", size=14, ha="right")
    text(ax, 17.0, 2.10, "$\\max\\{16+1,\\ 10+2\\}=17$", size=15,
         ha="right", color=TEAL_D)

    ax.set_xlim(-1.35, 19.0)
    ax.set_ylim(-0.75, 2.35)
    ax.axis("off")
    save(fig, "comb-scheduling")


# ---------------------------------------------------------------- 逻辑推理
def fig_logic_grid():
    """对应型列表排除：行推到只剩一格打 ✓，再把该列其余格划掉。"""
    fig, ax = new_fig(7.4, 5.2)
    cell = 1.0
    rows = ["$A$", "$B$", "$C$"]
    cols = ["$1$", "$2$", "$3$"]
    tab = [[False, True, False],       # True = 打勾
           [False, False, True],
           [True, False, False]]

    X0, Y0 = 0.0, 0.0
    W = 4 * cell

    for r in range(4):
        seg(ax, (X0, Y0 + r * cell), (X0 + W, Y0 + r * cell),
            color=GRID, lw=1.0, z=1)
    for c in range(4):
        seg(ax, (X0 + c * cell, Y0), (X0 + c * cell, Y0 + W),
            color=GRID, lw=1.0, z=1)
    # 表头分隔与外围边框
    seg(ax, (X0 + cell, Y0), (X0 + cell, Y0 + W), color=INK, lw=1.3, z=2)
    seg(ax, (X0, Y0 + 3 * cell), (X0 + W, Y0 + 3 * cell), color=INK, lw=1.3, z=2)
    outline(ax, [(X0, Y0), (X0 + W, Y0), (X0 + W, Y0 + W), (X0, Y0 + W)],
            color=INK, lw=1.3, z=2)

    for c, head in enumerate(cols):
        text(ax, X0 + (c + 1) * cell + cell / 2, Y0 + 3 * cell + cell / 2,
             head, size=15, color=MUTED)
    for r, head in enumerate(rows):
        text(ax, X0 + cell / 2, Y0 + (2 - r) * cell + cell / 2,
             head, size=15, color=MUTED)

    for r, rowv in enumerate(tab):
        for c, ok in enumerate(rowv):
            x0, y0 = X0 + (c + 1) * cell, Y0 + (2 - r) * cell
            ctr = (x0 + cell / 2, y0 + cell / 2)
            if ok:
                poly(ax, [(x0, y0), (x0 + cell, y0), (x0 + cell, y0 + cell),
                          (x0, y0 + cell)], TEAL2, alpha=0.9, lw=0, z=1)
                check(ax, ctr)
            else:
                cross(ax, ctr)

    # 一行只剩一格：同行其余格划掉、同列其余格也划掉
    arrow(ax, (2.12, 2.78), (3.62, 2.78), color=TEAL_D, lw=1.1,
          ls=(0, (3, 2)), scale=9)
    arrow(ax, (2.78, 2.12), (2.78, 0.72), color=TEAL_D, lw=1.1,
          ls=(0, (3, 2)), scale=9)

    finish(ax, (-0.15, 4.15), (-0.15, 4.15))
    save(fig, "comb-logic-grid")


# ---------------------------------------------------------------- 最值问题
def fig_extremum():
    """和定积大：周长固定时把顶上一条搬成右边一列，越接近正方积越大。"""
    fig, ax = new_fig(9.4, 6.4)

    # 最悬殊：1×11
    poly(ax, [(0, 0), (1, 0), (1, 11), (0, 11)], TEAL, alpha=0.85, lw=1.6)
    text(ax, 0.5, -0.66, "$1\\times11$", size=13.5)

    # 5×7：顶上一条（橙）要搬走
    x0 = 2.8
    poly(ax, [(x0, 0), (x0 + 5, 0), (x0 + 5, 7), (x0, 7)],
         TEAL, alpha=0.85, lw=1.6)
    poly(ax, [(x0, 6), (x0 + 5, 6), (x0 + 5, 7), (x0, 7)],
         WARM, alpha=0.9, lw=1.4, z=4)
    text(ax, x0 + 2.5, 8.10, "$5\\times7=35$", size=13.5, color=MUTED)
    text(ax, x0 + 2.5, 7.42, "$a+b=12$", size=12.5, color=MUTED)

    # 6×6：右边一列（橙）就是搬过来的那一条
    x1 = 8.6
    poly(ax, [(x1, 0), (x1 + 5, 0), (x1 + 5, 6), (x1, 6)],
         TEAL, alpha=0.85, lw=1.6)
    poly(ax, [(x1 + 5, 0), (x1 + 6, 0), (x1 + 6, 6), (x1 + 5, 6)],
         WARM, alpha=0.9, lw=1.4)
    poly(ax, [(x1 + 5, 5), (x1 + 6, 5), (x1 + 6, 6), (x1 + 5, 6)],
         WARM2, alpha=1.0, lw=1.6, edge=WARM_D, z=5)
    text(ax, x1 + 5.5, 5.5, "$+1$", size=9.5, color=WARM_D, z=6)
    outline(ax, [(x1, 0), (x1 + 6, 0), (x1 + 6, 6), (x1, 6)],
            color=INK, lw=2.2, z=6)
    text(ax, x1 + 3.0, -0.66, "$6\\times6=36$", size=13.5, color=TEAL_D)

    # 搬一条：顶上那一条 → 右边一列
    ax.annotate("", xy=(x1 + 5.55, 4.85), xytext=(x0 + 3.4, 6.6),
                arrowprops=dict(arrowstyle="-|>", color=WARM_D, lw=1.2,
                                linestyle=(0, (4, 3)), mutation_scale=12,
                                connectionstyle="arc3,rad=-0.22"),
                zorder=7)

    text(ax, 7.0, 11.55, "$(a+1)(b-1)-ab=b-a-1$", size=15)

    finish(ax, (-0.9, 15.4), (-1.45, 12.25))
    save(fig, "comb-extremum")


if __name__ == "__main__":
    fig_magic_square()
    fig_number_array()
    fig_game_strategy()
    fig_scheduling()
    fig_logic_grid()
    fig_extremum()
    print("done")
