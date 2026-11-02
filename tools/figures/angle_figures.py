#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""角度计算篇示意图（09-奥数-几何/角度计算.md）。

左图：两平行线之间的拐点，过拐点作平行线把一个角拆成两个（25°+40°）。
右图：等腰三角形沿 DE 折叠，A 落到 A'，∠1、∠2 与 ∠A 的关系。

关键几何约束（改图前先看这里，别凭手感挪点）：
- 左图 A、C 取在同一竖线上，E 由两个已知角反解得到，才能保证图上标的度数是真的。
  取 ∠A=25°（顶线）、∠C=40°（底线），解得 E=(x0+1.8381, 1.5429)。
  A、E、C 若共线就不是拐点图形了——这条曾经画错过一次。
- 右图等腰 ∠A=50°，折痕 DE 在 y=1.85，A' 是 A 关于 DE 的对称点，落在 (ox, 0.8)，
  必须在 BC(y=0) 之上，否则看起来像退化图形。

图内只用字母、数字与公式，中文写进 md 图注。

用法：cd /Users/kellywang/code/Mathmatics && /usr/local/bin/python3 tools/figures/angle_figures.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (  # noqa: E402
    INK, MUTED, WARM2, TEAL2,
    new_fig, finish, poly, seg, dot, text, angle_arc, parallel_marks,
    right_angle, save,
)

TEAL_D = "#2f8b7e"
WARM_D = "#c08a2e"


def fig_angle_calculation():
    fig, ax = new_fig(10.6, 5.5)

    # ---------- 左图：平行线拐点 ----------
    x0, x1 = -0.1, 4.5
    y_top, y_bot = 2.4, 0.0
    seg(ax, (x0, y_top), (x1, y_top), color=INK, lw=1.6)
    seg(ax, (x0, y_bot), (x1, y_bot), color=INK, lw=1.6)
    parallel_marks(ax, (x1 - 0.35, y_top))
    parallel_marks(ax, (x1 - 0.35, y_bot))

    A = (0.75, y_top)
    C = (0.75, y_bot)
    E = (0.75 + 1.8381, 1.5429)      # ∠A=25°、∠C=40° 反解

    # 辅助平行线：过 E 作 EF∥AB，一个角拆成 25° 与 40°
    seg(ax, (E[0] - 1.95, E[1]), (E[0] + 1.55, E[1]), color=MUTED, lw=1.0, ls=(0, (5, 3)))

    seg(ax, A, E, color=TEAL_D, lw=1.8)
    seg(ax, E, C, color=TEAL_D, lw=1.8)

    dot(ax, A); dot(ax, C); dot(ax, E, color=TEAL_D)
    text(ax, A[0] - 0.30, y_top + 0.26, "$A$", size=14)
    text(ax, C[0] - 0.30, y_bot - 0.28, "$C$", size=14)
    text(ax, E[0] + 0.30, E[1] + 0.08, "$E$", size=14, color=TEAL_D)
    text(ax, E[0] + 2.10, E[1] + 0.26, "$EF\\parallel AB$", size=11, color=MUTED)

    # ∠A = 25°（顶线与 AE 之间）
    angle_arc(ax, A, 0.55, 335, 360, color=WARM_D)
    text(ax, A[0] + 0.86, y_top - 0.24, r"$25^\circ$", size=12, color=WARM_D)
    # ∠C = 40°（底线与 CE 之间）
    angle_arc(ax, C, 0.55, 0, 40, color=WARM_D)
    text(ax, C[0] + 0.92, y_bot + 0.30, r"$40^\circ$", size=12, color=WARM_D)

    # E 处被 EF 拆出的两个内错角
    angle_arc(ax, E, 0.40, 155, 180, color=TEAL_D)
    angle_arc(ax, E, 0.40, 180, 220, color=TEAL_D)
    text(ax, E[0] - 0.84, E[1] + 0.20, r"$25^\circ$", size=11, color=TEAL_D)
    text(ax, E[0] - 0.80, E[1] - 0.26, r"$40^\circ$", size=11, color=TEAL_D)

    text(ax, 1.95, -0.95, r"$\angle AEC=25^\circ+40^\circ$", size=13, color=TEAL_D)

    # ---------- 右图：折叠 ----------
    ox = 7.35
    A2 = (ox, 2.9)
    B2 = (ox - 1.352, 0.0)       # ∠A = 50°
    C2 = (ox + 1.352, 0.0)
    D2 = (ox - 0.4897, 1.85)     # 折痕 DE，y=1.85
    E2 = (ox + 0.4897, 1.85)
    A3 = (ox, 0.8)               # A 关于 DE 的对称点，落在三角形内

    poly(ax, [A2, B2, C2], TEAL2, alpha=0.85)
    poly(ax, [A3, D2, E2], WARM2, alpha=0.95)
    seg(ax, A2, B2, color=INK, lw=1.4)
    seg(ax, B2, C2, color=INK, lw=1.4)
    seg(ax, C2, A2, color=INK, lw=1.4)
    seg(ax, D2, E2, color=INK, lw=1.4, ls=(0, (4, 3)))
    seg(ax, A3, D2, color=WARM_D, lw=1.3, ls="--")
    seg(ax, A3, E2, color=WARM_D, lw=1.3, ls="--")
    seg(ax, A2, A3, color=MUTED, lw=0.9, ls=":")
    right_angle(ax, (ox, 1.85), (1, 0), (0, 1), size=0.17, color=MUTED)

    for p, lab, dx, dy, col in [
        (A2, "$A$", 0, 0.30, INK), (B2, "$B$", -0.26, -0.20, INK),
        (C2, "$C$", 0.26, -0.20, INK), (D2, "$D$", -0.30, 0.14, INK),
        (E2, "$E$", 0.30, 0.14, INK), (A3, "$A'$", 0.30, -0.14, WARM_D),
    ]:
        dot(ax, p, color=col)
        text(ax, p[0] + dx, p[1] + dy, lab, size=14, color=col)

    # ∠1=∠BDA'、∠2=∠CEA'，两个楔角都在三角形内侧
    angle_arc(ax, D2, 0.30, 245, 295, color=WARM_D, lw=1.3)
    angle_arc(ax, E2, 0.30, 245, 295, color=WARM_D, lw=1.3)
    text(ax, D2[0], D2[1] - 0.62, "$1$", size=13, color=WARM_D)
    text(ax, E2[0], E2[1] - 0.62, "$2$", size=13, color=WARM_D)

    text(ax, ox, -0.78, r"$AA'\perp DE$", size=11, color=MUTED)
    text(ax, ox, -1.20, r"$\angle1+\angle2=2\angle A$", size=13, color=WARM_D)

    finish(ax, (-0.45, 9.05), (-1.70, 3.40))
    save(fig, "angle-calculation")


if __name__ == "__main__":
    fig_angle_calculation()
    print("done")
