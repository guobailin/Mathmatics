#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""几何示意图补充：三视图、立体、染色、格点、面积综合、
斜三角形、巧求周长、周长问题、几何思想方法。

约定：
  - 只写字母/数字/LaTeX 公式，不写中文（matplotlib 无中文字体会出方框）
  - 标注少而精（3~6 个），因为图会缩到 34mm 宽印在速查卡上
  - 在仓库根目录运行：
      PYTHONPATH=tools/figures python3 tools/figures/more_figures.py
"""
import os
os.environ["MPLCONFIGDIR"] = "/tmp/mplconfig"

from style import (new_fig, save, finish, poly, outline, seg, dot, text,
                   parallel_marks, right_angle, INK, MUTED, WARM, TEAL,
                   WARM2, TEAL2, GRID)


# ---------------------------------------------------------------- 三视图
def three_views():
    """一个小正方体堆 + 主视图/俯视图/左视图三个轮廓"""
    fig, ax = new_fig(7.8, 5.0)
    # --- 左：等距投影的小立方体堆（底层 3x2、上层 2x1）
    ux, uy = 0.62, 0.36          # 等距基向量
    oz = 0.0

    def cube(cx, cy, cz, fc, al=0.75):
        # 顶面、左面、右面
        p = [(cx, cy), (cx + ux, cy + uy), (cx + ux, cy + uy + 1.0), (cx, cy + 1.0)]
        top = [(x, y + cz) for (x, y) in
               [(cx, cy + 1.0), (cx + ux, cy + uy + 1.0),
                (cx + ux - ux, cy + uy + 1.0 + uy), (cx - ux, cy + 1.0 + uy)]]
        # 简化：只画正面矩形 + 顶面 + 侧面，用平行四边形近似
        front = [(cx, cy + cz), (cx + ux, cy + uy + cz),
                 (cx + ux, cy + uy + cz + 1.0), (cx, cy + cz + 1.0)]
        side = [(cx + ux, cy + uy + cz), (cx + 2 * ux, cy + cz),
                (cx + 2 * ux, cy + cz + 1.0), (cx + ux, cy + uy + cz + 1.0)]
        rooff = [(cx, cy + cz + 1.0), (cx + ux, cy + uy + cz + 1.0),
                 (cx + 2 * ux, cy + cz + 1.0), (cx + ux, cy - uy + cz + 1.0)]
        poly(ax, front, fc, al, lw=1.0)
        poly(ax, side, fc, 0.55, lw=1.0)
        poly(ax, rooff, fc, 0.85, lw=1.0)

    # 底层 3x2
    for i in range(3):
        for j in range(2):
            cube(i * ux - j * ux, -i * uy - j * uy + j * 1.0, 0.0, TEAL)
    # 上层 1 块（示意层数）
    cube(0.0, 1.0, 0.0, WARM, 0.9)
    text(ax, -0.35, 3.35, r"3D view", 12, color=MUTED, ha="left")

    # --- 右：三个视图轮廓（方格）
    def grid(x0, y0, cols, rows, cell=0.42, fc=TEAL2, al=0.75):
        for i in range(cols):
            for j in range(rows):
                poly(ax, [(x0 + i * cell, y0 + j * cell),
                          (x0 + (i + 1) * cell, y0 + j * cell),
                          (x0 + (i + 1) * cell, y0 + (j + 1) * cell),
                          (x0 + i * cell, y0 + (j + 1) * cell)],
                     fc, al, lw=0.9)
        outline(ax, [(x0, y0), (x0 + cols * cell, y0),
                     (x0 + cols * cell, y0 + rows * cell),
                     (x0, y0 + rows * cell)], lw=1.6)

    grid(2.35, 1.95, 3, 2)          # 主视图
    grid(2.35, 0.35, 3, 2)          # 俯视图
    grid(2.35, -1.25, 2, 2)         # 左视图
    text(ax, 2.98, 3.05, r"front", 12.5, color=MUTED)
    text(ax, 2.98, 1.45, r"top", 12.5, color=MUTED)
    text(ax, 2.98, -0.15, r"left", 12.5, color=MUTED)
    text(ax, 4.6, 3.05, r"$V=\#\ \mathrm{cubes}$", 13, color=MUTED, ha="left")
    finish(ax, (-1.5, 6.6), (-1.9, 3.9))
    save(fig, "three-views")


# ------------------------------------------------------------ 立体几何综合
def solid_geometry():
    """圆柱（r,h）与圆锥（r,h,l）并排"""
    fig, ax = new_fig(7.8, 4.8)
    # --- 圆柱
    cx, r, h = -2.1, 1.15, 2.5
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((cx, 0), 2 * r, 0.62, facecolor=TEAL, alpha=0.55,
                         edgecolor=INK, lw=1.5, zorder=2))
    ax.add_patch(Ellipse((cx, h), 2 * r, 0.62, facecolor=TEAL2, alpha=0.9,
                         edgecolor=INK, lw=1.5, zorder=3))
    seg(ax, (cx - r, 0), (cx - r, h), lw=1.7)
    seg(ax, (cx + r, 0), (cx + r, h), lw=1.7)
    seg(ax, (cx, 0), (cx, h), color=MUTED, lw=1.1, ls=(0, (4, 3)))
    seg(ax, (cx, -0.42), (cx + r, -0.42), color=MUTED, lw=1.1)
    text(ax, cx + r / 2 + 0.05, -0.62, r"$r$", 13, color=MUTED)
    text(ax, cx - 0.28, h / 2, r"$h$", 13, color=MUTED, ha="right")
    text(ax, cx, -1.25, r"$V=\pi r^{2}h$", 14, color=MUTED)

    # --- 圆锥
    cx2 = 2.0
    ax.add_patch(Ellipse((cx2, 0), 2 * r, 0.62, facecolor=WARM, alpha=0.5,
                         edgecolor=INK, lw=1.5, zorder=2))
    seg(ax, (cx2 - r, 0), (cx2, h + 0.35), lw=1.7)
    seg(ax, (cx2 + r, 0), (cx2, h + 0.35), lw=1.7)
    seg(ax, (cx2, 0), (cx2, h + 0.35), color=MUTED, lw=1.1, ls=(0, (4, 3)))
    text(ax, cx2 + 0.22, h / 2 - 0.15, r"$l$", 13, color=MUTED, ha="left")
    text(ax, cx2 + r / 2 + 0.05, -0.62, r"$r$", 13, color=MUTED)
    text(ax, cx2, -1.25, r"$V=\frac{1}{3}\pi r^{2}h$", 14, color=MUTED)
    text(ax, 0.0, 3.35, r"$l=\sqrt{r^{2}+h^{2}}$", 13.5, color=MUTED)
    finish(ax, (-4.0, 4.6), (-1.7, 3.9))
    save(fig, "solid-geometry")


# ---------------------------------------------------------------- 表面染色
def surface_coloring():
    """4x4x4 正方体的一面展开视图：四类块用不同颜色"""
    fig, ax = new_fig(6.6, 5.4)
    n = 4
    cell = 0.85
    for i in range(n):
        for j in range(n):
            edge_i = i in (0, n - 1)
            edge_j = j in (0, n - 1)
            if edge_i and edge_j:
                fc, al = INK, 0.82        # 三面（角）
            elif edge_i or edge_j:
                fc, al = WARM, 0.85       # 两面（棱）
            else:
                fc, al = TEAL, 0.75       # 一面（面内）
            poly(ax, [(i * cell, j * cell), ((i + 1) * cell, j * cell),
                      ((i + 1) * cell, (j + 1) * cell), (i * cell, (j + 1) * cell)],
                 fc, al, lw=1.1)
    outline(ax, [(0, 0), (n * cell, 0), (n * cell, n * cell), (0, n * cell)], lw=2.0)
    text(ax, 0.42, 0.42, r"$3$", 15, ha="center", va="center", color="#ffffff", weight="bold")
    text(ax, 1.7, 0.42, r"$2$", 15, color=INK, weight="bold")
    text(ax, 1.7, 1.7, r"$1$", 15, color=INK, weight="bold")
    text(ax, 0.42, 1.7, r"$2$", 15, color=INK, weight="bold")
    # 图例
    ly = -0.62
    for k, (c, lab) in enumerate([(INK, r"$3$ faces: $8$"),
                                  (WARM, r"$2$: $12(n-2)$"),
                                  (TEAL, r"$1$: $6(n-2)^{2}$")]):
        x = 0.15 + k * 1.72
        poly(ax, [(x, ly), (x + 0.42, ly), (x + 0.42, ly + 0.42), (x, ly + 0.42)],
             c, 0.85 if c == INK else 0.8, lw=1.0)
        text(ax, x + 0.58, ly + 0.21, lab, 12.5, color=MUTED, ha="left")
    text(ax, n * cell / 2, -1.5, r"$0$ face: $(n-2)^{3}$", 13, color=MUTED)
    finish(ax, (-0.5, 4.4), (-1.9, 4.4))
    save(fig, "surface-coloring")


# ---------------------------------------------------------------- 格点面积
def lattice_area():
    """格点多边形：内部格点 N、边界格点 B"""
    fig, ax = new_fig(7.0, 5.2)
    # 网格
    for i in range(-1, 8):
        seg(ax, (i, -1), (i, 6), color=GRID, lw=0.7, alpha=0.8)
    for j in range(-1, 7):
        seg(ax, (-1, j), (8, j), color=GRID, lw=0.7, alpha=0.8)
    # 多边形顶点（都在格点上）
    P = [(0, 0), (4, 0), (5, 2), (4, 4), (2, 5), (0, 3)]
    poly(ax, P, TEAL, 0.5, lw=0)
    outline(ax, P, lw=2.1)
    # 边界格点（含顶点）
    bound = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 2), (4, 4),
             (3, 3), (2, 5), (1, 4), (0, 3), (0, 2), (0, 1), (4, 1), (4, 2), (4, 3)]
    for (x, y) in bound:
        ax.plot(x, y, "o", ms=5.4, mfc="white", mec=INK, mew=1.35, zorder=4)
    # 内部格点
    inner = [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 4), (2, 4)]
    for (x, y) in inner:
        ax.plot(x, y, "o", ms=5.0, color="#b3261e", zorder=4)
    text(ax, 2.4, 2.05, r"$N=10$", 12.5, color="#b3261e", box=True)
    text(ax, 3.4, 0.42, r"$B$", 12.5, color=INK, box=True)
    text(ax, 2.4, -1.5, r"$S=N+\frac{B}{2}-1$", 14.5, color=MUTED)
    finish(ax, (-1.8, 7.2), (-2.0, 6.2))
    save(fig, "lattice-area")


# ---------------------------------------------------------------- 面积综合
def area_synthesis():
    """凹多边形：一条辅助虚线切成两块（割），另一处补成大长方形（补）"""
    fig, ax = new_fig(7.4, 5.0)
    # L 形（凹）
    L = [(0, 0), (5, 0), (5, 2), (2, 2), (2, 5), (0, 5)]
    poly(ax, L, TEAL, 0.55, lw=0)
    outline(ax, L, lw=2.1)
    # 割：竖虚线
    seg(ax, (2, 0), (2, 2), color=MUTED, lw=1.4, ls=(0, (5, 3)))
    # 补：横竖虚线补成大长方形
    seg(ax, (2, 2), (5, 2), color="#b3261e", lw=1.4, ls=(0, (5, 3)))
    seg(ax, (2, 2), (2, 5), color="#b3261e", lw=1.4, ls=(0, (5, 3)))
    seg(ax, (5, 2), (5, 5), color="#b3261e", lw=1.4, ls=(0, (5, 3)))
    seg(ax, (2, 5), (5, 5), color="#b3261e", lw=1.4, ls=(0, (5, 3)))
    text(ax, 1.0, 2.6, r"$S_{1}$", 13)
    text(ax, 3.4, 1.0, r"$S_{2}$", 13)
    text(ax, 3.5, 3.6, r"$+$", 15, color="#b3261e")
    text(ax, 2.5, -1.0, r"cut: $S=S_{1}+S_{2}$", 13, color=MUTED)
    text(ax, 2.5, -1.75, r"fill: $S=S_{big}-S_{gap}$", 13, color=MUTED)
    finish(ax, (-1.0, 6.6), (-2.4, 6.0))
    save(fig, "area-synthesis")


# ------------------------------------------------------------ 斜三角形面积
def oblique_triangle():
    """钝角三角形：高落在形外"""
    fig, ax = new_fig(7.4, 5.0)
    A, B, C = (0.4, 3.0), (-3.2, -1.0), (3.4, -1.0)
    poly(ax, [A, B, C], TEAL, 0.5, lw=0)
    outline(ax, [A, B, C], lw=2.1)
    H = (0.4, -1.0)
    seg(ax, A, H, color=MUTED, lw=1.5, ls=(0, (5, 3)))
    seg(ax, B, (4.6, -1.0), color=INK, lw=1.2, ls=(0, (5, 3)))   # 底边延长线
    right_angle(ax, H, (1, 0), (0, 1), 0.26)
    text(ax, 0.62, 1.1, r"$h$", 13.5, color=MUTED, ha="left")
    text(ax, 1.9, -1.42, r"$a$", 13.5, color=MUTED, va="top")
    text(ax, -0.15, 3.35, r"$A$", 15, weight="bold", ha="right")
    text(ax, -3.5, -1.35, r"$B$", 15, weight="bold", ha="right", va="top")
    text(ax, 3.7, -1.35, r"$C$", 15, weight="bold", ha="left", va="top")
    text(ax, 0.62, -1.42, r"$H$", 13.5, color=MUTED, va="top", ha="left")
    text(ax, 0.4, -2.4, r"$S=\frac{1}{2}ah$", 14.5, color=MUTED)
    text(ax, 0.4, -3.05, r"$h^{2}=c^{2}-x^{2}$", 13, color=MUTED)
    finish(ax, (-4.3, 5.4), (-3.6, 4.2))
    save(fig, "oblique-triangle")


# ---------------------------------------------------------------- 巧求周长
def perimeter_tricks():
    """阶梯图形：凹边平移到外沿，周长 = 大长方形周长"""
    fig, ax = new_fig(7.4, 5.0)
    P = [(0, 0), (1.1, 0), (1.1, 1.2), (2.6, 1.2), (2.6, 2.4),
         (5.2, 2.4), (5.2, 3.6), (0, 3.6)]
    poly(ax, P, WARM, 0.6, lw=0)
    outline(ax, P, lw=2.1)
    # 平移箭头：竖边向上平移到顶边
    for x in (1.1, 2.6, 5.2):
        ax.annotate("", xy=(x, 4.15), xytext=(x, 0.0),
                    arrowprops=dict(arrowstyle="->", color="#b3261e", lw=1.5,
                                    linestyle=(0, (5, 3))))
    # 平移箭头：横边向左平移到左边
    for y in (1.2, 2.4, 3.6):
        ax.annotate("", xy=(-0.95, y), xytext=(5.2, y),
                    arrowprops=dict(arrowstyle="->", color="#b3261e", lw=1.5,
                                    linestyle=(0, (5, 3))))
    outline(ax, [(-0.95, 0), (5.2, 0), (5.2, 4.15), (-0.95, 4.15)],
            color="#b3261e", lw=1.6, z=1)
    text(ax, 2.1, -0.85, r"$C=2(a+b)$", 14.5, color=MUTED)
    text(ax, 2.1, -1.55, r"shift $\rightarrow$ rectangle", 12.5, color=MUTED)
    finish(ax, (-1.9, 6.4), (-2.1, 5.0))
    save(fig, "perimeter-tricks")


# ---------------------------------------------------------------- 周长问题
def perimeter_problem():
    """组合图形：标边长；剪一刀周长 +2 条边"""
    fig, ax = new_fig(7.4, 5.0)
    # 两个正方形并排（2a x a 长方形）拼一个正方形在上面
    poly(ax, [(0, 0), (3.2, 0), (3.2, 1.6), (0, 1.6)], TEAL, 0.5, lw=0)
    poly(ax, [(0.8, 1.6), (2.4, 1.6), (2.4, 3.2), (0.8, 3.2)], TEAL, 0.5, lw=0)
    outline(ax, [(0, 0), (3.2, 0), (3.2, 1.6), (2.4, 1.6), (2.4, 3.2),
                 (0.8, 3.2), (0.8, 1.6), (0, 1.6)], lw=2.1)
    text(ax, 1.6, 0.8, r"$a$", 13.5)
    text(ax, 1.6, -0.6, r"$2a$", 13.5, color=MUTED, va="top")
    text(ax, -0.25, 0.8, r"$a$", 13.5, ha="right")
    text(ax, 1.6, 2.4, r"$a$", 13.5)
    # 剪一刀示意
    seg(ax, (1.6, 0), (1.6, 1.6), color="#b3261e", lw=1.6, ls=(0, (5, 3)))
    text(ax, 1.78, 0.75, r"cut", 12, color="#b3261e", ha="left")
    text(ax, 1.6, -1.35, r"cut once: $C+2\times$edge", 13, color=MUTED)
    finish(ax, (-1.2, 4.6), (-1.9, 4.0))
    save(fig, "perimeter-problem")


# ------------------------------------------------------------ 几何思想方法
def geometry_method():
    """割补：三角形补成平行四边形（等积变形）"""
    fig, ax = new_fig(7.6, 5.0)
    # 三角形 ABC
    A, B, C = (0.0, 2.6), (-2.6, -1.2), (2.6, -1.2)
    poly(ax, [A, B, C], TEAL, 0.5, lw=0)
    outline(ax, [A, B, C], lw=2.1)
    # 割补：过 A 作 BC 平行线，过 C 作 AB 平行线 -> 平行四边形
    D = (5.2, 2.6)
    seg(ax, A, D, color=MUTED, lw=1.4, ls=(0, (5, 3)))
    seg(ax, C, D, color=MUTED, lw=1.4, ls=(0, (5, 3)))
    poly(ax, [A, B, C, D], WARM, 0.28, lw=0)
    outline(ax, [A, B, C, D], color=MUTED, lw=1.5, z=1)
    # 高
    H = (0.0, -1.2)
    seg(ax, A, H, color=INK, lw=1.2, ls=(0, (4, 3)))
    right_angle(ax, H, (1, 0), (0, 1), 0.24)
    text(ax, 0.22, 0.6, r"$h$", 13, color=MUTED, ha="left")
    text(ax, 1.4, -1.55, r"$a$", 13, color=MUTED, va="top")
    text(ax, -0.2, 2.95, r"$A$", 15, weight="bold", ha="right")
    text(ax, -2.85, -1.5, r"$B$", 15, weight="bold", ha="right", va="top")
    text(ax, 2.9, -1.5, r"$C$", 15, weight="bold", ha="left", va="top")
    text(ax, 5.4, 2.95, r"$D$", 15, weight="bold", ha="left")
    text(ax, 1.3, -2.5, r"$S_{\triangle}=\frac{1}{2}S_{\text{para}}$"
         .replace(r"\text{para}", r"para"), 13.5, color=MUTED)
    finish(ax, (-3.6, 6.4), (-3.2, 3.9))
    save(fig, "geometry-method")


if __name__ == "__main__":
    three_views()
    solid_geometry()
    surface_coloring()
    lattice_area()
    area_synthesis()
    oblique_triangle()
    perimeter_tricks()
    perimeter_problem()
    geometry_method()
