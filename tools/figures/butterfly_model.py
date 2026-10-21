#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""蝴蝶模型示意图：梯形 AB∥CD，对角线 AC、BD 交于 O。

输出：
  assets/geometry/butterfly-model.svg  （网站 / 打印，透明背景）
  assets/geometry/butterfly-model.png  （审阅 / 小程序备用，白底）
"""
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

# 顶点：A、B 为上底，C、D 为下底；AB ∥ CD
A = (-2.4, 2.0)
B = (1.8, 2.0)
C = (3.2, -2.0)
D = (-3.0, -2.0)

def intersection(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

# 对角线交点 O（由 AC 与 BD 联立）
O = intersection(A, C, B, D)

INK = "#1f2a26"
MUTED = "#5f6a64"
WARM = "#f0c987"
TEAL = "#9fd0c8"

fig, ax = plt.subplots(figsize=(7.6, 5.2))
fig.patch.set_alpha(0)
ax.set_facecolor("none")

# 四块三角形：上/下用暖色，左右翅用青色
tris = [
    ([A, B, O], WARM, 0.55),   # S1 上块 AOB
    ([B, C, O], TEAL, 0.62),   # S2 右翅 BOC
    ([C, D, O], WARM, 0.55),   # S3 下块 COD
    ([D, A, O], TEAL, 0.62),   # S4 左翅 AOD
]
for pts, color, alpha in tris:
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor="none",
                         alpha=alpha, zorder=1))

# 梯形外框与对角线
outline = [A, B, C, D, A]
ax.add_line(Line2D([p[0] for p in outline], [p[1] for p in outline],
                   color=INK, lw=2.2, solid_capstyle="round", zorder=3))
for p, q in [(A, C), (B, D)]:
    ax.add_line(Line2D([p[0], q[0]], [p[1], q[1]], color=INK, lw=1.45,
                       alpha=0.9, zorder=2))

# 交点
ax.plot(*O, "o", ms=5.5, color=INK, zorder=4)
ax.text(O[0] + 0.13, O[1] + 0.10, r"$O$", fontsize=15, color=INK,
        ha="left", va="bottom", zorder=5,
        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))

# 顶点标签
labels = {
    "A": (A[0] - 0.12, A[1] + 0.12, "right", "bottom"),
    "B": (B[0] + 0.12, B[1] + 0.12, "left", "bottom"),
    "C": (C[0] + 0.12, C[1] - 0.12, "left", "top"),
    "D": (D[0] - 0.12, D[1] - 0.12, "right", "top"),
}
for name, (x, y, ha, va) in labels.items():
    ax.text(x, y, rf"${name}$", fontsize=16, fontweight="bold",
            color=INK, ha=ha, va=va, zorder=5)

# 四块面积标签
def centroid(p, q, r):
    return ((p[0] + q[0] + r[0]) / 3, (p[1] + q[1] + r[1]) / 3)

c1 = centroid(A, B, O)
c2 = centroid(B, C, O)
c3 = centroid(C, D, O)
c4 = centroid(D, A, O)
areas = {
    r"$S_1$": (c1[0], c1[1] + 0.13),
    r"$S_2$": (c2[0] + 0.34, c2[1] + 0.02),
    r"$S_3$": (c3[0], c3[1] - 0.13),
    r"$S_4$": (c4[0] - 0.34, c4[1] + 0.02),
}
for text, (x, y) in areas.items():
    ax.text(x, y, text, fontsize=13.5, color=INK, ha="center", va="center",
            zorder=5, bbox=dict(boxstyle="round,pad=0.18", fc="white",
                                ec="none", alpha=0.82))

# 上、下底的平行标记（双斜杠）
def parallel_marks(mid, half=0.24, dy=0.14):
    x, y = mid
    for dx in (-half, half):
        ax.add_line(Line2D([x + dx - 0.07, x + dx + 0.07],
                           [y - dy, y + dy], color=INK, lw=1.4, zorder=4))

parallel_marks(((-2.4 + 1.8) / 2, 2.0))
parallel_marks(((3.2 - 3.0) / 2, -2.0))

# 底部说明
ax.text(0.0, -2.62, r"$AB\parallel CD$", fontsize=12.5, color=MUTED,
        ha="center", va="center")
ax.text(0.0, -2.92, r"$S_1\cdot S_3=S_2\cdot S_4,\qquad S_2=S_4$",
        fontsize=12.5, color=MUTED, ha="center", va="center")

ax.set_xlim(-3.9, 4.0)
ax.set_ylim(-3.2, 2.55)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

out_svg = "assets/geometry/butterfly-model.svg"
out_png = "assets/geometry/butterfly-model.png"
fig.savefig(out_svg, transparent=True, bbox_inches="tight", pad_inches=0.05)
fig.savefig(out_png, dpi=220, facecolor="white", bbox_inches="tight", pad_inches=0.05)
print("saved", out_svg, out_png)
