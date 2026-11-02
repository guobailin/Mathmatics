#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""行程模块第二批示意图（issue #74 P0-3）。

图内只用字母、数字与公式（与几何篇一致，避开中文字体依赖），
中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/travel_batch2.py
产出：
    assets/geometry/travel-*.svg/.png
    assets/geometry/cards/travel-*.svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, poly, seg, dot, text, save,
)

# 浅色只用于粗线条与色块，文字另用同族深色，保证白底可读。
TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"
GREY_D = "#6b7a73"


def arrow(ax, tail, tip, color=INK, lw=3.2, ms=18, z=4):
    ax.annotate("", xy=tip, xytext=tail, zorder=z,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def hbracket(ax, x1, x2, y, label, color=MUTED, size=13, tick=0.16, dy=-0.42):
    """水平括线。"""
    seg(ax, (x1, y), (x2, y), color=color, lw=1.2, z=2)
    for x in (x1, x2):
        seg(ax, (x, y - tick), (x, y + tick), color=color, lw=1.2, z=2)
    text(ax, (x1 + x2) / 2, y + dy, label, size=size, color=color)


def vbracket(ax, y1, y2, x, label, color=MUTED, size=13, tick=0.16, dx=-0.42,
             ha="right"):
    """竖直括线。"""
    seg(ax, (x, y1), (x, y2), color=color, lw=1.2, z=2)
    for y in (y1, y2):
        seg(ax, (x - tick, y), (x + tick, y), color=color, lw=1.2, z=2)
    text(ax, x + dx, (y1 + y2) / 2, label, size=size, color=color, ha=ha)


def axes_ts(ax, tx, sy, lt=6.7, ls=13.6):
    """时间—路程图的坐标轴。"""
    arrow(ax, (0, 0), (lt, 0), color=INK, lw=1.5, ms=14)
    arrow(ax, (0, 0), (0, ls), color=INK, lw=1.5, ms=14)
    text(ax, tx, 0, "$t$", size=16, ha="left")
    text(ax, 0, sy, "$s$", size=16)


def fig_three_meet():
    """三人相遇：两个相遇点各属一对两人问题，第三人只是路标。"""
    fig, ax = new_fig(8.6, 5.4)
    A, B = 0.0, 10.0
    P1, P2 = 4.2, 3.0          # 丙遇甲、丙遇乙

    seg(ax, (A, 0), (B, 0), color=INK, lw=2.2, z=2)
    dot(ax, (A, 0), ms=6.5)
    dot(ax, (B, 0), ms=6.5)
    text(ax, A - 0.55, 0, "$A$", size=15)
    text(ax, B + 0.55, 0, "$B$", size=15)

    # 出发点与箭头的连线：说明三支箭头各从哪端起
    for y in (2.05, 1.30):
        seg(ax, (A, 0.1), (A, y), color=GRID, lw=1.0, ls=":", z=1)
    seg(ax, (B, -0.1), (B, -0.95), color=GRID, lw=1.0, ls=":", z=1)

    # 三人各自的出发点与方向
    arrow(ax, (A, 2.05), (2.45, 2.05), color=TEAL_D)
    text(ax, 2.85, 2.05, "$v_1$", size=15, color=TEAL_D, ha="left")
    arrow(ax, (A, 1.30), (1.60, 1.30), color=WARM_D)
    text(ax, 2.00, 1.30, "$v_2$", size=15, color=WARM_D, ha="left")
    arrow(ax, (B, -0.95), (7.35, -0.95), color=GREY_D)
    text(ax, 6.95, -0.95, "$v_3$", size=15, color=GREY_D, ha="right")

    # 两个相遇点：各挂一条两人速度和式
    for x, up, lab in ((P1, True, "$(v_1+v_3)\\,t_1=S$"),
                       (P2, False, "$(v_2+v_3)\\,t_2=S$")):
        dot(ax, (x, 0), ms=8, z=6)
        if up:
            seg(ax, (x, 0.14), (x, 2.95), color=MUTED, lw=1.0, ls=":", z=1)
            text(ax, x, 3.42, lab, size=14)
        else:
            seg(ax, (x, -0.14), (x, -2.45), color=MUTED, lw=1.0, ls=":", z=1)
            text(ax, x, -2.92, lab, size=14)

    text(ax, 8.05, -2.92, "$t_1<t_2$", size=13, color=MUTED)

    finish(ax, (-1.2, 11.4), (-3.9, 3.95))
    save(fig, "travel-three-meet")


def fig_speed_change():
    """变速：时间—路程折线在 M 处折一下，斜率变化即变速，虚线是平均速度。"""
    fig, ax = new_fig(8.2, 5.2)
    t1, s1 = 2.6, 5.2           # v1 = 2
    t2, s2 = 1.8, 7.2           # v2 = 4
    M = (t1, s1)
    E = (t1 + t2, s1 + s2)

    axes_ts(ax, 6.85, 13.95)

    # 分段：斜率 2 → 斜率 4
    seg(ax, (0, 0), M, color=TEAL, lw=4.2, z=3)
    seg(ax, M, E, color=WARM, lw=4.2, z=3)
    dot(ax, M, ms=6.5, z=6)
    dot(ax, E, ms=6.5, z=6)
    text(ax, M[0] + 0.35, M[1] - 0.85, "$M$", size=15, ha="left")

    # 平均速度线
    seg(ax, (0, 0), E, color=INK, lw=1.5, ls=(0, (5, 2.6)), z=4)

    # 虚线定位
    for p in (M, E):
        seg(ax, (p[0], -0.12), (p[0], p[1]), color=GRID, lw=1.0, ls=":", z=1)
        seg(ax, (0, p[1]), (p[0], p[1]), color=GRID, lw=1.0, ls=":", z=1)

    # 时间括线（轴下）
    hbracket(ax, 0, t1, -1.05, "$t_1$", dy=-0.55)
    hbracket(ax, t1, t1 + t2, -1.05, "$t_2$", dy=-0.55)

    # 路程括线（轴左）
    vbracket(ax, 0, s1, -0.55, "$s_1$")
    vbracket(ax, s1, s1 + s2, -0.55, "$s_2$")

    # 图例：右上角留给 M→E 段，图例放右下空白
    lx, lc = 4.95, 0.60
    for i, (c, lab, ls) in enumerate([(TEAL, "$v_1$", "-"),
                                      (WARM, "$v_2$", "-"),
                                      (INK, "$\\bar v$", (0, (5, 2.6)))]):
        y = 10.4 - i * 1.35
        seg(ax, (lx, y), (lx + lc, y), color=c, lw=4.2 if ls == "-" else 1.5,
            ls=ls, z=3)
        text(ax, lx + lc + 0.28, y, lab, size=15, ha="left")
    text(ax, 6.05, 5.35,
         r"$\bar v=\frac{s_1+s_2}{t_1+t_2}$", size=15)

    ax.set_xlim(-2.7, 7.5)
    ax.set_ylim(-3.0, 14.7)
    ax.set_aspect("auto")
    ax.axis("off")
    save(fig, "travel-speed-change")


def fig_proportion():
    """比例行程：同一起点两条射线，同一时刻的竖直截线给出 s1:s2 = v1:v2。"""
    fig, ax = new_fig(7.4, 5.6)
    t0, v1, v2 = 4.0, 3.0, 2.0
    x_end = 5.2

    axes_ts(ax, 6.75, 14.15)

    seg(ax, (0, 0), (x_end, v1 * x_end), color=TEAL, lw=3.0, z=3)
    seg(ax, (0, 0), (x_end, v2 * x_end), color=WARM, lw=3.0, z=3)
    text(ax, 2.60, 9.10, "$v_1$", size=15, color=TEAL_D)
    text(ax, 3.00, 4.50, "$v_2$", size=15, color=WARM_D)

    # 同一时刻的截线
    seg(ax, (t0, 0), (t0, v1 * t0 + 1.1), color=MUTED, lw=1.2, ls=":", z=1)
    dot(ax, (t0, v1 * t0), ms=7, z=6)
    dot(ax, (t0, v2 * t0), ms=7, z=6)

    # 从轴量到交点的两段
    seg(ax, (t0, v2 * t0), (t0 + 0.55, v2 * t0), color=GRID, lw=1.0, ls=":", z=1)
    seg(ax, (t0, v1 * t0), (t0 + 1.65, v1 * t0), color=GRID, lw=1.0, ls=":", z=1)
    vbracket(ax, 0, v2 * t0, t0 + 0.45, "$s_2$", dx=0.36, ha="left")
    vbracket(ax, 0, v1 * t0, t0 + 1.55, "$s_1$", dx=0.36, ha="left")

    hbracket(ax, 0, t0, -0.95, "$t$", dy=-0.55)

    text(ax, 2.15, 14.35, "$s_1:s_2=v_1:v_2$", size=17)

    ax.set_xlim(-0.9, 7.6)
    ax.set_ylim(-2.6, 16.7)
    ax.set_aspect("auto")
    ax.axis("off")
    save(fig, "travel-proportion")


if __name__ == "__main__":
    fig_three_meet()
    fig_speed_change()
    fig_proportion()
    print("done")
