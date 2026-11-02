#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""行程模块第二批示意图（issue #74 P0-3）：发车、扶梯、时钟。

图内只用字母、数字与公式（避开中文字体依赖），中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/travel_batch3.py
产出：
    assets/geometry/travel-*.svg/.png
    assets/geometry/cards/travel-*.svg
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, poly, seg, dot, text, save, angle_arc,
)

from matplotlib.patches import Circle, Wedge  # noqa: E402


def arrow(ax, p, q, color=INK, lw=1.9, ls="-", z=5, scale=13):
    """细箭头：p -> q。style.py 没有箭头，这里用 annotate 补上。"""
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


def bus(ax, cx, base, color=TEAL, w=1.16, h=0.48):
    """一辆公交车：车身 + 一条车窗带。base 是车身底边的 y。"""
    x0, x1 = cx - w / 2, cx + w / 2
    poly(ax, [(x0, base), (x1, base), (x1, base + h), (x0, base + h)],
         color, alpha=0.9, lw=1.1)
    poly(ax, [(x0 + 0.13, base + 0.16), (x1 - 0.13, base + 0.16),
              (x1 - 0.13, base + h - 0.10), (x0 + 0.13, base + h - 0.10)],
         "white", alpha=0.75, lw=0)


def fig_bus_departure():
    """车距 L 恒定：站着不动的人每 T 分钟过一辆，L = vT。"""
    fig, ax = new_fig(10.4, 3.6)
    xs = [1.3, 4.7, 8.1, 11.5]

    # 线路
    seg(ax, (0.2, 0.0), (12.3, 0.0), color=INK, lw=2.2, z=3)
    seg(ax, (0.2, -0.10), (12.3, -0.10), color=GRID, lw=1.0, z=2)

    for x in xs:
        bus(ax, x, 0.04)

    # 车距 L：取相邻两车
    bracket(ax, (xs[0], 1.02), (xs[1], 1.02), color=INK, lw=1.3)
    text(ax, (xs[0] + xs[1]) / 2, 1.36, "$L$", size=16)

    # 车速方向
    arrow(ax, (9.75, 0.86), (10.55, 0.86), color=MUTED, lw=1.4, scale=11)
    text(ax, 10.80, 0.86, "$v$", size=14, color=MUTED)

    # 静止的观察者
    ax.plot(6.4, 0.06, "o", ms=9, mfc=WARM, mec=INK, mew=1.2, zorder=6)
    text(ax, 6.40, 0.46, "$u=0$", size=13)

    # 时间轴：同一位观察者先后被车经过的时刻
    ts = [1.5, 3.2, 4.9, 6.6]
    arrow(ax, (1.2, -1.48), (8.35, -1.48), color=MUTED, lw=1.2, scale=11)
    text(ax, 8.50, -1.48, "$t$", size=13, color=MUTED, ha="left")
    for x, lab in zip(ts, ["$0$", "$T$", "$2T$", "$3T$"]):
        seg(ax, (x, -1.61), (x, -1.35), color=MUTED, lw=1.1, z=4)
        text(ax, x, -1.86, lab, size=13, color=MUTED)
    bracket(ax, (ts[0], -1.12), (ts[1], -1.12), color=MUTED, lw=1.0)
    text(ax, (ts[0] + ts[1]) / 2, -0.90, "$T$", size=13, color=MUTED)

    text(ax, 10.55, -1.30, "$L=vT$", size=20)

    finish(ax, (-0.65, 12.95), (-2.25, 1.75))
    save(fig, "travel-bus-departure")


def escalator_icon(ax, x0):
    """小型扶梯图标：斜梯身上行，只作语境，不带标注。"""
    B, T = (x0 + 0.12, -0.18), (x0 + 1.02, 1.00)
    L = math.hypot(T[0] - B[0], T[1] - B[1])
    d = ((T[0] - B[0]) / L, (T[1] - B[1]) / L)
    n = (-d[1], d[0])
    w = 0.15

    def P(s, off=0.0):
        return (B[0] + s * d[0] + off * n[0], B[1] + s * d[1] + off * n[1])

    poly(ax, [P(0, w), P(L, w), P(L, -w), P(0, -w)], TEAL2, alpha=0.9, lw=1.0)
    for k in range(1, 7):
        seg(ax, P(L * k / 7, w), P(L * k / 7, -w), color=MUTED, lw=0.9, z=2,
            alpha=0.55)
    arrow(ax, P(0.16), P(L - 0.10), color=INK, lw=1.5, z=6, scale=9)


def escalator_panel(ax, x0, a_u, b_u, mode):
    """一条级数线段：人走的 a（青）与梯送的 b（橙）。

    plus  ：a 与 b 首尾相接，合起来是 N
    minus ：a 的右端被梯子抵消掉 b，剩下的才是 N
    """
    h0, h1 = 0.28, 0.72
    bx = x0 + 1.55
    escalator_icon(ax, x0)

    if mode == "plus":
        total = a_u + b_u
        poly(ax, [(bx, h0), (bx + a_u, h0), (bx + a_u, h1), (bx, h1)],
             TEAL, alpha=0.9, lw=1.1)
        poly(ax, [(bx + a_u, h0), (bx + total, h0),
                  (bx + total, h1), (bx + a_u, h1)],
             WARM2, alpha=0.95, lw=1.1, edge=WARM)
        text(ax, bx + a_u / 2, (h0 + h1) / 2, "$a$", size=16)
        text(ax, bx + a_u + b_u / 2, (h0 + h1) / 2, "$b$", size=16)
        bracket(ax, (bx, 0.10), (bx + total, 0.10), color=MUTED, lw=1.1, tick=0.09)
        text(ax, bx + total / 2, -0.30, "$N=a+b$", size=17)
    else:
        keep = a_u - b_u
        poly(ax, [(bx, h0), (bx + keep, h0), (bx + keep, h1), (bx, h1)],
             TEAL, alpha=0.9, lw=1.1)
        poly(ax, [(bx + keep, h0), (bx + a_u, h0),
                  (bx + a_u, h1), (bx + keep, h1)],
             WARM2, alpha=0.9, lw=1.1, edge=WARM)
        seg(ax, (bx + keep, h0), (bx + a_u, h1), color=WARM, lw=1.4, z=4)
        seg(ax, (bx + keep, h1), (bx + a_u, h0), color=WARM, lw=1.4, z=4)
        text(ax, bx + keep / 2, (h0 + h1) / 2, "$a$", size=16)
        text(ax, bx + keep + b_u / 2, (h0 + h1) / 2, "$b$", size=16)
        bracket(ax, (bx, 0.10), (bx + keep, 0.10), color=MUTED, lw=1.1, tick=0.09)
        text(ax, bx + keep / 2, -0.30, "$N=a-b$", size=17)


def fig_escalator():
    """顺行 a+b、逆行 a−b：两段级数首尾相接或互相抵消。"""
    fig, ax = new_fig(10.6, 3.6)
    escalator_panel(ax, 0.0, 2.40, 0.80, "plus")
    escalator_panel(ax, 5.60, 4.00, 1.20, "minus")

    finish(ax, (-0.15, 11.35), (-0.80, 1.30))
    save(fig, "travel-escalator")


def fig_clock():
    """钟面：两针夹角 θ 与相对角速度 5.5°/分。"""
    fig, ax = new_fig(8.6, 4.6)
    R = 1.25

    ax.add_patch(Circle((0, 0), R, fill=False, edgecolor=INK, lw=1.9, zorder=3))

    # 刻度与数字
    for k in range(12):
        th = math.radians(90 - 30 * k)
        c, s = math.cos(th), math.sin(th)
        seg(ax, ((R - 0.10) * c, (R - 0.10) * s), (R * c, R * s),
            color=MUTED, lw=1.2, z=3)
        num = 12 if k == 0 else k
        text(ax, (R - 0.26) * c, (R - 0.26) * s, f"${num}$", size=10.5,
             color=MUTED)

    # 4:40 —— 分针 240°、时针 140°、夹角 100°
    am, ah = math.radians(90 - 240), math.radians(90 - 140)

    ax.add_patch(Wedge((0, 0), 0.44, -150, -50, facecolor=WARM2,
                       edgecolor="none", alpha=0.85, zorder=1))
    arrow(ax, (0, 0), (0.86 * math.cos(am), 0.86 * math.sin(am)),
          color=TEAL, lw=2.6, z=6, scale=11)
    arrow(ax, (0, 0), (0.52 * math.cos(ah), 0.52 * math.sin(ah)),
          color=INK, lw=3.6, z=7, scale=9)
    dot(ax, (0, 0), ms=6, color=INK, z=8)

    angle_arc(ax, (0, 0), 0.44, -150, -50, color=MUTED, lw=1.5, z=5)
    text(ax, 0.56 * math.cos(math.radians(-100)),
         0.56 * math.sin(math.radians(-100)), "$\\theta$", size=15,
         color=INK)

    # 右侧说明
    seg(ax, (1.62, 0.93), (2.02, 0.93), color=TEAL, lw=3.4)
    text(ax, 2.16, 0.93, "$6^\\circ/\\mathrm{min}$", size=13, ha="left")
    seg(ax, (1.62, 0.50), (2.02, 0.50), color=INK, lw=3.4)
    text(ax, 2.16, 0.50, "$0.5^\\circ/\\mathrm{min}$", size=13, ha="left")
    text(ax, 1.62, 0.02, "$6-0.5=5.5^\\circ/\\mathrm{min}$", size=13,
         ha="left", color=MUTED)

    seg(ax, (1.62, -0.40), (4.35, -0.40), color=GRID, lw=1.0)
    text(ax, 1.62, -0.92, "$\\theta=5.5t-\\Delta$", size=18, ha="left")
    text(ax, 1.62, -1.42, "$\\Delta=30H$", size=12, ha="left", color=MUTED)

    finish(ax, (-1.45, 4.55), (-1.75, 1.45))
    save(fig, "travel-clock")


if __name__ == "__main__":
    fig_bus_departure()
    fig_escalator()
    fig_clock()
    print("done")
