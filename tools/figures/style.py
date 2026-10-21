#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""几何示意图统一样式。"""
import os
os.environ["MPLCONFIGDIR"] = "/tmp/mplconfig"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, Circle, Wedge

INK = "#1f2a26"
MUTED = "#5f6a64"
WARM = "#f0c987"
TEAL = "#9fd0c8"
WARM2 = "#f6e3c4"
TEAL2 = "#d7ebe7"
GRID = "#d8d2c5"

plt.rcParams.update({
    "font.size": 13,
    "mathtext.fontset": "dejavusans",
})


def new_fig(w=7.6, h=5.2):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    return fig, ax


def save(fig, name):
    svg = f"assets/geometry/{name}.svg"
    png = f"assets/geometry/{name}.png"
    fig.savefig(svg, transparent=True, bbox_inches="tight", pad_inches=0.06)
    fig.savefig(png, dpi=220, facecolor="white", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("saved", svg, png)


def finish(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def poly(ax, pts, color, alpha=0.55, lw=0, edge=INK, z=1):
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=edge,
                         linewidth=lw, alpha=alpha, zorder=z))


def outline(ax, pts, color=INK, lw=2.1, z=3):
    ax.add_patch(Polygon(pts, closed=True, facecolor="none", edgecolor=color,
                         linewidth=lw, zorder=z, joinstyle="round"))


def seg(ax, p, q, color=INK, lw=1.35, ls="-", z=2, alpha=1.0):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, linestyle=ls,
            zorder=z, alpha=alpha, solid_capstyle="round")


def dot(ax, p, ms=5.2, color=INK, z=4):
    ax.plot(p[0], p[1], "o", ms=ms, color=color, zorder=z)


def text(ax, x, y, s, size=14, color=INK, ha="center", va="center",
         box=False, weight=None, z=5):
    kw = dict(fontsize=size, color=color, ha=ha, va=va, zorder=z)
    if weight:
        kw["fontweight"] = weight
    if box:
        kw["bbox"] = dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.85)
    ax.text(x, y, s, **kw)


def parallel_marks(ax, mid, half=0.24, dy=0.14, color=INK, lw=1.4):
    x, y = mid
    for dx in (-half, half):
        ax.plot([x + dx - 0.07, x + dx + 0.07], [y - dy, y + dy],
                color=color, lw=lw, zorder=4, solid_capstyle="round")


def right_angle(ax, p, d1, d2, size=0.24, color=INK, lw=1.1):
    px, py = p
    a = (px + size * d1[0], py + size * d1[1])
    b = (px + size * (d1[0] + d2[0]), py + size * (d1[1] + d2[1]))
    c = (px + size * d2[0], py + size * d2[1])
    ax.plot([a[0], b[0], c[0]], [a[1], b[1], c[1]], color=color, lw=lw, zorder=4)


def angle_arc(ax, center, radius, t1, t2, color=MUTED, lw=1.1, z=4):
    ax.add_patch(Arc(center, 2 * radius, 2 * radius, angle=0,
                     theta1=t1, theta2=t2, color=color, lw=lw, zorder=z))


def centroid(p, q, r):
    return ((p[0] + q[0] + r[0]) / 3, (p[1] + q[1] + r[1]) / 3)


def intersection(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
