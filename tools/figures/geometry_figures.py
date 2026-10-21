#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""几何专题示意图批量生成（七大模型 + 圆扇形 + 勾股）。"""
import os
os.environ["MPLCONFIGDIR"] = "/tmp/mplconfig"
from matplotlib.patches import Arc, Circle, Wedge
from style import (new_fig, save, finish, poly, outline, seg, dot, text,
                   parallel_marks, right_angle, angle_arc, centroid,
                   intersection, INK, MUTED, WARM, TEAL, WARM2, TEAL2)


def area_ratio():
    fig, ax = new_fig(7.4, 5.0)
    A, B, C = (0.0, 3.2), (-2.8, -1.2), (3.2, -1.2)
    D = (0.8, -1.2)          # BD:DC = 3:2
    H = (0.0, -1.2)
    poly(ax, [A, B, D], TEAL, 0.55)
    poly(ax, [A, D, C], WARM, 0.55)
    outline(ax, [A, B, C])
    seg(ax, A, D, lw=1.7)
    seg(ax, A, H, color=MUTED, lw=1.2, ls=(0, (4, 3)))
    right_angle(ax, H, (1, 0), (0, 1), 0.22)
    text(ax, -2.9, 3.35, r"$A$", 16, weight="bold", ha="left")
    text(ax, -3.05, -1.45, r"$B$", 16, weight="bold", ha="right", va="top")
    text(ax, 3.45, -1.45, r"$C$", 16, weight="bold", ha="left", va="top")
    text(ax, 0.95, -1.45, r"$D$", 16, weight="bold", ha="left", va="top")
    text(ax, -0.55, 0.95, r"$S_{ABD}$", 11.5, box=True)
    text(ax, 1.0, 0.95, r"$S_{ADC}$", 11.5, box=True)
    text(ax, 0.2, 0.95, r"$h$", 12, color=MUTED, ha="left")
    text(ax, -1.0, -1.55, r"$3$", 12, color=MUTED, va="top")
    text(ax, 2.0, -1.55, r"$2$", 12, color=MUTED, va="top")
    text(ax, 0.0, -2.15, r"$BD:DC=3:2$", 12.5, color=MUTED)
    text(ax, 0.0, -2.5, r"$S_{\triangle ABD}:S_{\triangle ADC}=BD:DC=3:2$",
         12.5, color=MUTED)
    finish(ax, (-3.7, 4.0), (-2.8, 3.7))
    save(fig, "area-ratio")


def equal_area():
    fig, ax = new_fig(7.6, 5.0)
    B, C = (-2.8, -1.2), (2.8, -1.2)
    A, D = (-2.1, 2.2), (1.7, 2.2)
    seg(ax, (-3.8, 2.2), (3.8, 2.2), color=MUTED, lw=1.1)
    seg(ax, (-3.8, -1.2), (3.8, -1.2), color=MUTED, lw=1.1)
    parallel_marks(ax, (-3.0, 2.2), 0.18, 0.12, MUTED, 1.0)
    parallel_marks(ax, (-3.0, -1.2), 0.18, 0.12, MUTED, 1.0)
    poly(ax, [A, B, C], TEAL, 0.18)
    poly(ax, [D, B, C], WARM, 0.18)
    seg(ax, A, B, color="#3f8a80", lw=1.8)
    seg(ax, A, C, color="#3f8a80", lw=1.8)
    seg(ax, D, B, color="#c08a2e", lw=1.8)
    seg(ax, D, C, color="#c08a2e", lw=1.8)
    seg(ax, B, C, lw=2.4)
    text(ax, -2.3, 2.5, r"$A$", 16, weight="bold")
    text(ax, 1.95, 2.5, r"$D$", 16, weight="bold")
    text(ax, -3.1, -1.55, r"$B$", 16, weight="bold", ha="right", va="top")
    text(ax, 3.1, -1.55, r"$C$", 16, weight="bold", ha="left", va="top")
    text(ax, -3.85, 2.45, r"$l_1$", 13, color=MUTED, ha="right")
    text(ax, -3.85, -0.95, r"$l_2$", 13, color=MUTED, ha="right")
    text(ax, 0.0, -2.05, r"$S_{\triangle ABC}=S_{\triangle DBC}$", 13.5, color=MUTED)
    finish(ax, (-4.1, 4.1), (-2.5, 3.0))
    save(fig, "equal-area")


def bird_head():
    fig, ax = new_fig(7.4, 5.2)
    A, B, C = (0.0, 3.2), (-3.0, -1.2), (3.0, -1.2)
    D = (-2.0, 0.267)
    E = (2.0, 0.267)
    poly(ax, [A, D, E], WARM, 0.58)
    outline(ax, [A, B, C])
    seg(ax, D, E, lw=1.8)
    angle_arc(ax, A, 0.75, 238, 302, MUTED, 1.2)
    text(ax, 0.0, 2.25, r"$\angle A$", 12, color=MUTED)
    text(ax, 0.0, 3.45, r"$A$", 16, weight="bold")
    text(ax, -3.2, -1.45, r"$B$", 16, weight="bold", ha="right", va="top")
    text(ax, 3.2, -1.45, r"$C$", 16, weight="bold", ha="left", va="top")
    text(ax, -2.15, 0.48, r"$D$", 15, weight="bold", ha="right")
    text(ax, 2.15, 0.48, r"$E$", 15, weight="bold", ha="left")
    text(ax, 0.0, 1.1, r"$S_{\triangle ADE}$", 12.5, box=True)
    text(ax, 0.0, -2.0, r"$AD:AB=AE:AC=2:3$", 12.5, color=MUTED)
    text(ax, 0.0, -2.4, r"$S_{\triangle ADE}:S_{\triangle ABC}=4:9$", 12.5, color=MUTED)
    finish(ax, (-3.8, 3.8), (-2.8, 3.7))
    save(fig, "bird-head")


def swallow_tail():
    fig, ax = new_fig(7.4, 5.2)
    A, B, C = (0.0, 3.2), (-3.0, -1.2), (3.0, -1.2)
    P = (0.0, 0.6)
    D = (0.0, -1.2)
    E = intersection(B, P, A, C)
    F = intersection(C, P, A, B)
    poly(ax, [P, B, C], TEAL, 0.50)
    poly(ax, [P, C, A], WARM, 0.50)
    poly(ax, [P, A, B], WARM2, 0.60)
    outline(ax, [A, B, C])
    seg(ax, A, D, lw=1.4)
    seg(ax, B, E, lw=1.4)
    seg(ax, C, F, lw=1.4)
    dot(ax, P)
    text(ax, 0.15, 0.78, r"$P$", 15, weight="bold", ha="left")
    text(ax, 0.0, 3.45, r"$A$", 16, weight="bold")
    text(ax, -3.2, -1.45, r"$B$", 16, weight="bold", ha="right", va="top")
    text(ax, 3.2, -1.45, r"$C$", 16, weight="bold", ha="left", va="top")
    text(ax, 0.12, -1.45, r"$D$", 15, weight="bold", ha="left", va="top")
    text(ax, E[0] + 0.12, E[1] + 0.05, r"$E$", 15, weight="bold", ha="left")
    text(ax, F[0] - 0.12, F[1] + 0.05, r"$F$", 15, weight="bold", ha="right")
    text(ax, -0.9, 1.55, r"$z$", 14, box=True)
    text(ax, 0.9, 1.55, r"$y$", 14, box=True)
    text(ax, 0.0, -0.55, r"$x$", 14, box=True)
    text(ax, 0.0, -2.55, r"$\frac{BD}{DC}=\frac{S_{\triangle ABP}}{S_{\triangle APC}}$",
         12.5, color=MUTED)
    finish(ax, (-3.8, 3.8), (-3.1, 3.7))
    save(fig, "swallow-tail")


def similarity():
    fig, ax = new_fig(7.4, 5.2)
    A, B, C = (0.0, 3.2), (-3.0, -1.2), (3.0, -1.2)
    D = (-1.8, 0.56)
    E = (1.8, 0.56)
    poly(ax, [A, D, E], WARM, 0.58)
    outline(ax, [A, B, C])
    seg(ax, D, E, lw=1.8)
    parallel_marks(ax, (0.0, 0.56), 0.2, 0.12)
    parallel_marks(ax, (0.0, -1.2), 0.2, 0.12)
    text(ax, 0.0, 3.45, r"$A$", 16, weight="bold")
    text(ax, -3.2, -1.45, r"$B$", 16, weight="bold", ha="right", va="top")
    text(ax, 3.2, -1.45, r"$C$", 16, weight="bold", ha="left", va="top")
    text(ax, -2.0, 0.8, r"$D$", 15, weight="bold", ha="right")
    text(ax, 2.0, 0.8, r"$E$", 15, weight="bold", ha="left")
    text(ax, 0.0, 1.25, r"$S_{\triangle ADE}$", 12.5, box=True)
    text(ax, 0.0, -2.0, r"$DE\parallel BC$", 12.5, color=MUTED)
    text(ax, 0.0, -2.4, r"$AD:DB=3:2,\quad S_{\triangle ADE}:S_{\triangle ABC}=9:25$",
         12.2, color=MUTED)
    finish(ax, (-3.8, 3.8), (-2.8, 3.7))
    save(fig, "similarity")


def circle_sector():
    import numpy as np
    fig, ax = new_fig(6.8, 5.4)
    O = (0.0, 0.0)
    r = 2.2
    t1, t2 = 20, 110
    ax.add_patch(Wedge(O, r, t1, t2, facecolor=WARM, edgecolor="none", alpha=0.62, zorder=1))
    ax.add_patch(Circle(O, r, facecolor="none", edgecolor=INK, lw=1.8, zorder=3))
    ax.add_patch(Arc(O, 2*r, 2*r, angle=0, theta1=t1, theta2=t2,
                     color=INK, lw=2.6, zorder=4))
    A = (r * np.cos(np.radians(t1)), r * np.sin(np.radians(t1)))
    B = (r * np.cos(np.radians(t2)), r * np.sin(np.radians(t2)))
    seg(ax, O, A, lw=1.4)
    seg(ax, O, B, lw=1.4)
    angle_arc(ax, O, 0.75, t1, t2, MUTED, 1.2)
    dot(ax, O)
    text(ax, 0.15, -0.2, r"$O$", 15, weight="bold", ha="left")
    text(ax, A[0] + 0.12, A[1] - 0.1, r"$A$", 15, weight="bold", ha="left", va="top")
    text(ax, B[0] - 0.08, B[1] + 0.1, r"$B$", 15, weight="bold", ha="right", va="bottom")
    text(ax, 1.15, 0.15, r"$r$", 12.5, color=MUTED)
    text(ax, 0.95, 0.75, r"$n^\circ$", 12.5, color=MUTED)
    text(ax, 0.0, -2.95, r"$l=\frac{n}{360}\,2\pi r$", 12.5, color=MUTED)
    text(ax, 0.0, -3.5, r"$S=\frac{n}{360}\,\pi r^2$", 12.5, color=MUTED)
    finish(ax, (-2.8, 2.8), (-3.9, 2.8))
    save(fig, "circle-sector")


def pythagoras():
    fig, ax = new_fig(7.8, 7.0)
    C, A, B = (0.0, 0.0), (3.0, 0.0), (0.0, 4.0)
    poly(ax, [(3, 0), (0, 0), (0, -3), (3, -3)], TEAL, 0.45)
    poly(ax, [(0, 4), (0, 0), (-4, 0), (-4, 4)], WARM, 0.45)
    poly(ax, [(3, 0), (0, 4), (4, 7), (7, 3)], WARM2, 0.65)
    outline(ax, [C, A, B])
    right_angle(ax, C, (1, 0), (0, 1), 0.3)
    text(ax, 1.5, -1.5, r"$3^2=9$", 13, color=MUTED)
    text(ax, -2.2, 2.0, r"$4^2=16$", 13, color=MUTED)
    text(ax, 5.3, 5.2, r"$5^2=25$", 13, color=MUTED)
    text(ax, 1.5, 0.28, r"$3$", 13, weight="bold")
    text(ax, -0.32, 2.0, r"$4$", 13, weight="bold")
    text(ax, 1.95, 1.85, r"$5$", 13, weight="bold")
    text(ax, -0.22, -0.22, r"$C$", 15, weight="bold", ha="right", va="top")
    text(ax, 3.2, -0.2, r"$A$", 15, weight="bold", ha="left", va="top")
    text(ax, -0.2, 4.2, r"$B$", 15, weight="bold", ha="right", va="bottom")
    text(ax, 3.0, -3.9, r"$a^2+b^2=c^2$", 14, color=MUTED)
    text(ax, 3.0, -4.4, r"$9+16=25$", 13, color=MUTED)
    finish(ax, (-4.8, 7.8), (-4.7, 7.6))
    save(fig, "pythagoras")


if __name__ == "__main__":
    area_ratio()
    equal_area()
    bird_head()
    swallow_tail()
    similarity()
    circle_sector()
    pythagoras()
