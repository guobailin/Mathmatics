#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""行程模块第二批示意图（issue #74 P0-3）：火车追及、环形跑道、流水行船。

图内只用字母、数字与公式（matplotlib 默认字体没有中文字形），
中文解释放在 md 的图注里。

用法：
    cd /Users/kellywang/code/Mathmatics
    /usr/local/bin/python3 tools/figures/travel_batch1.py
产出：
    assets/geometry/travel-*.svg/.png
    assets/geometry/cards/travel-*.svg
"""
import os
import sys
from math import cos, sin, radians

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM, TEAL, WARM2, TEAL2, GRID,
    new_fig, finish, poly, seg, dot, text, save,
)
from matplotlib.patches import Arc, Circle, Polygon, Rectangle  # noqa: E402


def arrow(ax, p, q, color=INK, lw=1.8, scale=14, z=5):
    """从 p 指向 q 的实心箭头。"""
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=scale, shrinkA=0, shrinkB=0),
                zorder=z)


def bracket(ax, x1, x2, y, label, color=INK, size=14, dy=-0.46):
    """横向括线：两端各一小竖，标签写在下方。"""
    seg(ax, (x1, y), (x2, y), color=color, lw=1.3)
    seg(ax, (x1, y - 0.14), (x1, y + 0.14), color=color, lw=1.3)
    seg(ax, (x2, y - 0.14), (x2, y + 0.14), color=color, lw=1.3)
    text(ax, (x1 + x2) / 2, y + dy, label, size=size, color=color)


def fig_train_chase():
    """同向追及：以慢车为静止参照，快车车头要净走 L1+L2 才算超过。

    上下两行是同一段过程的前后两个时刻；乙车两行画在同一位置，就是"参照物"。
    """
    fig, ax = new_fig(9.4, 4.4)
    L1, L2 = 2.8, 1.6
    H = 0.95
    yA, yB = 4.35, 2.70
    a0, a1 = 1.60, 1.60 + L1        # 甲 t=0：车头贴乙车尾
    b0, b1 = a1, a1 + L2            # 乙
    c0, c1 = b1, b1 + L1            # 甲 t：车尾贴乙车头

    def car(x0, x1, y, fill, lab_l, lab_v):
        poly(ax, [(x0, y), (x1, y), (x1, y + H), (x0, y + H)],
             fill, alpha=0.92, lw=1.1)
        seg(ax, (x1, y), (x1, y + H), color=INK, lw=1.9, z=5)   # 车头竖线
        cx = (x0 + x1) / 2
        text(ax, cx, y + H * 0.63, lab_l, size=14)
        text(ax, cx, y + H * 0.24, lab_v, size=11, color=MUTED)

    # 上：甲车头刚贴上乙车尾
    car(a0, a1, yA, TEAL2, "$L_1$", "$v_1$")
    car(b0, b1, yA, WARM, "$L_2$", "$v_2$")
    # 下：甲车尾刚离开乙车头
    car(b0, b1, yB, WARM, "$L_2$", "$v_2$")
    car(c0, c1, yB, TEAL, "$L_1$", "$v_1$")

    text(ax, 1.32, yA + H / 2, "$t=0$", size=12, color=MUTED, ha="right")
    text(ax, b0 - 0.28, yB + H / 2, "$t$", size=12, color=MUTED, ha="right")

    # 甲车头的净位移 = 车长和：点线把上一刻的甲车头接到括线左端
    bracket(ax, a1, c1, yB - 0.62, "$L_1+L_2$", INK, 15, dy=-0.44)
    seg(ax, (a1, yA), (a1, yB - 0.62), color=MUTED, lw=0.9, ls=":", z=6)
    text(ax, (a1 + c1) / 2, yB - 1.72,
         "$L_1+L_2=(v_1-v_2)\\,t$", size=16)

    finish(ax, (0.45, 9.55), (1.35, 5.75))
    save(fig, "travel-train-chase")


def fig_circular():
    """环形跑道同向追及：只有一条圆形跑道，整圈就是 L。

    甲 = 整圈 L + 两人共走的弧 s2，乙 = 弧 s2；两人同一时刻落在 P。
    """
    fig, ax = new_fig(7.0, 6.9)
    R = 3.25
    th_s, th_p = 90.0, -22.0          # S 在正上方，P 在右下

    def pol(r, deg):
        return (r * cos(radians(deg)), r * sin(radians(deg)))

    # 唯一的一条跑道：整圈长 L
    ax.add_patch(Circle((0, 0), R, fill=False, ec=TEAL, lw=5.0, zorder=2))
    # 两人共走的弧 S→P，画在同一条圆上，只做高亮
    ax.add_patch(Arc((0, 0), 2 * R, 2 * R, angle=0,
                     theta1=th_p, theta2=th_s, color=WARM, lw=6.0, zorder=3))

    S = pol(R, th_s)
    P = pol(R, th_p)
    dot(ax, S, ms=7, z=7)
    dot(ax, P, ms=7, z=7)
    text(ax, S[0], S[1] + 0.46, "$S$", size=15)
    text(ax, P[0] + 0.34, P[1] - 0.40, "$P$", size=15)

    # 顺时针方向箭头（整条圆上只放一个，避开 S 与 P）
    def arc_head(r, deg, half, span=9):
        ax.add_patch(Polygon([pol(r, deg - span / 2),
                              pol(r + half, deg + span / 2),
                              pol(r - half, deg + span / 2)],
                             closed=True, facecolor=INK, edgecolor=INK,
                             lw=0.4, zorder=6))

    arc_head(R, 196, 0.13)

    text(ax, 0, -(R + 0.46), "$L$", size=15, color=TEAL)
    text(ax, *pol(R - 0.62, 36), "$s_2$", size=14, color=WARM)

    text(ax, 0, 0.30, "$s_1=s_2+L$", size=15)
    text(ax, 0, -1.05, r"$t=\dfrac{L}{v_1-v_2}$", size=17)

    finish(ax, (-R - 0.75, R + 0.95), (-R - 0.90, R + 0.90))
    save(fig, "travel-circular")


def fig_stream():
    """流水行船：顺流两段同向首尾相接成 v+u；逆流被水顶回 u，净剩 v−u。"""
    fig, ax = new_fig(8.8, 7.3)
    v, u = 5.0, 1.6
    x0 = 1.5

    def river(y0, h=0.36):
        """细水带：颜色浅、箭头小，只交代水流朝下游。"""
        ax.add_patch(Rectangle((1.0, y0), 9.6, h, facecolor=TEAL2,
                               edgecolor="none", alpha=0.75, zorder=0))
        for xc in (1.9, 4.3, 6.7, 9.1):
            ax.annotate("", xy=(xc + 0.46, y0 + h / 2), xytext=(xc, y0 + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0,
                                        mutation_scale=9, shrinkA=0, shrinkB=0),
                        zorder=1)

    def thick(p, q, color, head=True, lw=6.0, z=3):
        """粗速度线；箭头用实心三角形单独画，粗线自己出箭头会糊成一团。"""
        seg(ax, p, q, color=color, lw=lw, z=z)
        if not head:
            return
        s = 1 if q[0] > p[0] else -1
        ax.add_patch(Polygon([(q[0], q[1]),
                              (q[0] - 0.50 * s, q[1] + 0.17),
                              (q[0] - 0.50 * s, q[1] - 0.17)],
                             closed=True, facecolor=color, edgecolor=color,
                             lw=0.4, zorder=z + 1))

    # ---- (1) 顺流：v 与 u 同向首尾相接 ----
    yv1 = 8.70
    river(8.00)
    thick((x0, yv1), (x0 + v, yv1), TEAL, head=False)
    thick((x0 + v, yv1), (x0 + v + u, yv1), WARM)
    text(ax, x0 + v / 2, yv1 + 0.45, "$v$", size=15, color=TEAL)
    text(ax, x0 + v + u / 2, yv1 + 0.45, "$u$", size=15, color=WARM)
    bracket(ax, x0, x0 + v + u, 7.62, "$v+u$", INK, 16)

    # ---- (2) 逆流：v 朝上游，u 在下方把它顶回来 ----
    yv2, yu2 = 5.10, 4.45
    river(3.35)
    xb = x0 + 7.9                     # 船此刻的位置
    thick((xb, yv2), (xb - v, yv2), TEAL)
    thick((xb - v, yu2), (xb - v + u, yu2), WARM)
    seg(ax, (xb - v, yu2), (xb - v, yv2), color=MUTED, lw=0.85, ls=":")
    text(ax, 7.55, yv2 + 0.45, "$v$", size=15, color=TEAL)
    text(ax, xb - v + u / 2, yu2 - 0.43, "$u$", size=15, color=WARM)
    bracket(ax, xb - v + u, xb, 2.98, "$v-u$", INK, 16)

    # ---- 和差还原 ----
    text(ax, 3.35, 1.62, r"$v=\dfrac{(v+u)+(v-u)}{2}$", size=15)
    text(ax, 8.45, 1.62, r"$u=\dfrac{(v+u)-(v-u)}{2}$", size=15)

    finish(ax, (0.6, 11.1), (0.95, 9.55))
    save(fig, "travel-stream")


if __name__ == "__main__":
    fig_train_chase()
    fig_circular()
    fig_stream()
    print("done")
