#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""行程模块示意图（issue #74 P0-3）。

图内只用字母、数字与公式（与几何篇一致，避开中文字体依赖），
中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/travel_figures.py
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


def fig_average():
    """两段速度不同：平均速度按时间加权，不是速度的算术平均。"""
    fig, ax = new_fig(8.0, 4.0)
    y = 0.0
    A, M, B = (0.0, y), (4.2, y), (10.0, y)

    seg(ax, A, M, color=TEAL, lw=5, z=2)
    seg(ax, M, B, color=WARM, lw=5, z=2)
    dot(ax, A); dot(ax, M); dot(ax, B)
    text(ax, A[0] - 0.35, y, "$A$", size=15)
    text(ax, M[0], y + 0.62, "$M$", size=15)
    text(ax, B[0] + 0.35, y, "$B$", size=15)

    text(ax, (A[0] + M[0]) / 2, y - 0.55, "$s_1=v_1t_1$", size=15, color=TEAL)
    text(ax, (M[0] + B[0]) / 2, y - 0.55, "$s_2=v_2t_2$", size=15, color=WARM)
    text(ax, (A[0] + M[0]) / 2, y + 0.52, "$v_1,\\ t_1$", size=14, color=MUTED)
    text(ax, (M[0] + B[0]) / 2, y + 0.52, "$v_2,\\ t_2$", size=14, color=MUTED)

    # 全程括线
    seg(ax, (0, 1.35), (10, 1.35), color=MUTED, lw=1.0)
    seg(ax, (0, 1.2), (0, 1.5), color=MUTED, lw=1.0)
    seg(ax, (10, 1.2), (10, 1.5), color=MUTED, lw=1.0)
    text(ax, 5.0, 1.62, "$s=s_1+s_2$", size=15)

    text(ax, 5.0, -1.45,
         r"$\bar v=\dfrac{s_1+s_2}{t_1+t_2}=\dfrac{v_1t_1+v_2t_2}{t_1+t_2}$",
         size=17)
    text(ax, 2.6, -3.05,
         r"$t_1=t_2$ → $\bar v=\frac{v_1+v_2}{2}$", size=13, color=MUTED)
    text(ax, 7.6, -3.05,
         r"$s_1=s_2$ → $\bar v=\frac{2v_1v_2}{v_1+v_2}$", size=13, color=MUTED)

    finish(ax, (-1.0, 11.0), (-3.5, 2.0))
    save(fig, "travel-average")


def fig_encounters():
    """时间—路程图：两条折线，交点即相遇，横轴上的和路程是 1S、3S、5S。"""
    fig, ax = new_fig(7.4, 5.4)
    S = 6.0
    va, vb = 2.0, 1.0

    def zig(v, start, t_max):
        """从 start 端点出发，速度 v，折返。返回 (times, positions)。"""
        ts, xs = [0.0], [start]
        t, x, d = 0.0, start, (1 if start == 0 else -1)
        while t < t_max:
            remain = (S - x) if d > 0 else x
            dt = remain / v
            if t + dt > t_max:
                x = x + d * v * (t_max - t)
                ts.append(t_max); xs.append(x)
                break
            t += dt; x = x + d * remain
            ts.append(t); xs.append(x)
            d = -d
        return ts, xs

    t_max = 11.5
    ta, xa = zig(va, 0.0, t_max)
    tb, xb = zig(vb, S, t_max)

    # 两条折线
    ax.plot(ta, xa, color=TEAL, lw=2.6, zorder=3, solid_capstyle="round")
    ax.plot(tb, xb, color=WARM, lw=2.6, zorder=3, solid_capstyle="round")
    seg(ax, (0, 0), (t_max, 0), color=GRID, lw=1.2, z=1)
    seg(ax, (0, S), (t_max, S), color=GRID, lw=1.2, z=1)

    text(ax, -0.8, 0, "$A$", size=15)
    text(ax, -0.8, S, "$B$", size=15)
    text(ax, 0.5, S + 0.55, "$v_1$", size=13, color=TEAL)
    text(ax, 0.5, -0.85, "$v_2$", size=13, color=WARM)

    # 第 k 次相遇 t=(2k-1)S/(v1+v2)，位置由甲走过 (2k-1)*... 折返折算
    def fold(dist):
        m = dist % (2 * S)
        return m if m <= S else 2 * S - m

    for k, lab in [(1, "$1S$"), (2, "$3S$"), (3, "$5S$")]:
        t = (2 * k - 1) * S / (va + vb)
        if t >= t_max:
            continue
        x = fold(va * t)
        dot(ax, (t, x), ms=7, color=INK, z=6)
        dy = -0.55 if x < 1.2 else 0.42
        text(ax, t, x + dy, f"{k}·{lab}", size=12, color=INK)

    finish(ax, (-1.4, t_max + 0.6), (-1.8, S + 1.6))
    save(fig, "travel-encounters")


def fig_train_bridge():
    """火车过桥三情形：浅色为起点车、深色为终点车，括线量的是车头净走的距离。

    (1) 过一个点 s=L；(2) 完全通过 s=B+L；(3) 完全在桥上 s=B−L。
    """
    fig, ax = new_fig(8.6, 6.6)
    L, B = 2.2, 6.0
    H = 0.62

    def car(x_head, y, solid=True):
        """以车头（右端）位置 x_head 画一节车厢。"""
        x0 = x_head - L
        poly(ax, [(x0, y), (x_head, y), (x_head, y + H), (x0, y + H)],
             TEAL if solid else TEAL2, alpha=0.85 if solid else 0.95, lw=1.0)
        seg(ax, (x_head, y), (x_head, y + H), color=INK, lw=1.6, z=5)

    def bridge(x0, y):
        poly(ax, [(x0, y - 0.16), (x0 + B, y - 0.16), (x0 + B, y + 0.16), (x0, y + 0.16)],
             WARM2, alpha=0.95, lw=0.8)

    def mark(x, y, tag):
        seg(ax, (x, y - 0.30), (x, y + H + 0.26), color=MUTED, lw=0.9, ls=":")
        text(ax, x, y + H + 0.50, tag, size=11, color=MUTED)

    def bracket(x1, x2, y, label, color):
        seg(ax, (x1, y), (x2, y), color=color, lw=1.3)
        seg(ax, (x1, y - 0.14), (x1, y + 0.14), color=color, lw=1.3)
        seg(ax, (x2, y - 0.14), (x2, y + 0.14), color=color, lw=1.3)
        text(ax, (x1 + x2) / 2, y - 0.42, label, size=14, color=color)

    # (1) 通过一个点 P：车头从 P 走到车尾离 P
    y1 = 9.4
    P = 4.0
    car(P, y1, solid=False)
    car(P + L, y1, solid=True)
    mark(P, y1, "$S$")
    mark(P + L, y1, "$E$")
    dot(ax, (P, y1 - 0.55), ms=7)
    text(ax, P, y1 - 0.95, "$P$", size=13)
    bracket(P, P + L, y1 - 1.32, "$s=L$", INK)
    text(ax, 9.6, y1 + 0.28, "(1)", size=13, color=MUTED)

    # (2) 完全通过：车头自桥头走到"桥尾 + 车长"
    y2 = 5.9
    car(2.0, y2, solid=False)
    car(2.0 + B + L, y2, solid=True)
    bridge(2.0, y2 - 0.62)
    text(ax, 2.0 + B / 2, y2 - 1.12, "$B$", size=12, color=MUTED)
    mark(2.0, y2, "$S$")
    mark(2.0 + B + L, y2, "$E$")
    bracket(2.0, 2.0 + B + L, y2 - 1.62, "$s=B+L$", TEAL)
    text(ax, 11.15, y2 + 0.28, "(2)", size=13, color=MUTED)

    # (3) 完全在桥上：车尾压桥头 → 车头到桥尾
    y3 = 2.4
    car(2.0 + L, y3, solid=False)
    car(2.0 + B, y3, solid=True)
    bridge(2.0, y3 - 0.62)
    text(ax, 2.0 + B / 2, y3 - 1.12, "$B$", size=12, color=MUTED)
    mark(2.0 + L, y3, "$S$")
    mark(2.0 + B, y3, "$E$")
    bracket(2.0 + L, 2.0 + B, y3 - 1.62, "$s=B-L$", WARM)
    text(ax, 11.15, y3 + 0.28, "(3)", size=13, color=MUTED)

    finish(ax, (-0.4, 11.9), (-0.6, 10.6))
    save(fig, "travel-train-bridge")


if __name__ == "__main__":
    fig_average()
    fig_encounters()
    fig_train_bridge()
    print("done")
