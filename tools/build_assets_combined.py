"""Deux figures composées, dessinées spécialement pour occuper une slide entière.

Elles regroupent des notions que l'on veut présenter d'un seul tenant à l'oral :
- Euler / Hamilton / raccourci (la conversion au cœur de Christofides) ;
- les quatre opérateurs de l'algorithme génétique.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from matplotlib.patches import FancyBboxPatch

from tools.theme import (
    BG, PANEL, PANEL_LIGHT, GRID, TEXT, MUTED, GOLD, GOLD_SOFT, CYAN,
    GREEN, CORAL, VIOLET, HEAD_FONT, save,
)
from tools.build_assets_charts import OUT, blank, head, circ, box, arrow


# ---------------------------------------------------------------------------
# 21 — Euler → Hamilton → raccourci
# ---------------------------------------------------------------------------
def fig_euler_hamilton_raccourci():
    fig, ax = blank((13, 6.4))
    head(ax, "Euler, Hamilton, et le raccourci",
         "Les trois idées qui transforment un multigraphe en tournée.",
         y=99, fs=24)

    pos = {"A": (9, 52), "B": (25, 52), "C": (25, 30), "D": (9, 30), "E": (17, 68)}
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "E"), ("B", "E")]

    def graph(dx, hl_edges, hl_nodes, color, caption, rule):
        for u, v in edges:
            on = (u, v) in hl_edges or (v, u) in hl_edges
            ax.plot([pos[u][0] + dx, pos[v][0] + dx], [pos[u][1], pos[v][1]],
                    color=color if on else GRID, lw=3.2 if on else 1.5,
                    zorder=2, solid_capstyle="round")
        for name, (x, y) in pos.items():
            on = name in hl_nodes
            circ(ax, x + dx, y, 2.7, facecolor=color if on else PANEL,
                 edgecolor=color if on else GRID, lw=1.8, zorder=3)
            ax.text(x + dx, y, name, fontsize=11, color=BG if on else MUTED,
                    ha="center", va="center", fontweight="bold", zorder=4)
        ax.text(dx + 17, 23, caption, fontsize=14, color=color, ha="center",
                va="top", fontweight="bold", fontfamily=HEAD_FONT)
        ax.text(dx + 17, 16.5, rule, fontsize=11.5, color=MUTED, ha="center",
                va="top", linespacing=1.6)

    graph(0, set(edges), set(), CYAN, "1 · Circuit EULÉRIEN",
          "chaque ARÊTE une seule fois\nc'est Hierholzer qui le construit")
    graph(33, {("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")},
          {"A", "B", "C", "D"}, GOLD, "2 · Cycle HAMILTONIEN",
          "chaque SOMMET une seule fois\nc'est ce que cherche le TSP")

    ax.plot([32, 32], [18, 78], color=GRID, lw=1.1, ls=(0, (4, 4)))
    ax.plot([65, 65], [18, 78], color=GRID, lw=1.1, ls=(0, (4, 4)))

    A, B, C = (73, 38), (84, 62), (95, 38)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=CORAL, lw=2.8, zorder=2)
    ax.plot([B[0], C[0]], [B[1], C[1]], color=CORAL, lw=2.8, zorder=2)
    ax.plot([A[0], C[0]], [A[1], C[1]], color=GREEN, lw=3.2, zorder=3)
    for p, n, off in ((A, "A", -3.2), (C, "C", 3.2)):
        circ(ax, p[0], p[1], 2.0, facecolor=GOLD, edgecolor=BG, lw=1.4, zorder=4)
        ax.text(p[0] + off, p[1], n, fontsize=12, color=TEXT,
                ha="right" if off < 0 else "left", va="center",
                fontweight="bold", fontfamily=HEAD_FONT)
    circ(ax, B[0], B[1], 2.0, facecolor=MUTED, edgecolor=BG, lw=1.4, zorder=4)
    ax.text(B[0], B[1] + 4.0, "B", fontsize=12, color=TEXT, ha="center",
            va="bottom", fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(84, 31, "d(A,C)  ≤  d(A,B) + d(B,C)", fontsize=12, color=GREEN,
            ha="center", fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(84, 23, "3 · Le RACCOURCI", fontsize=14, color=GREEN, ha="center",
            va="top", fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(84, 16.5, "B est déjà visitée : on la saute,\n"
                      "sans jamais rallonger le trajet.",
            fontsize=11.5, color=MUTED, ha="center", va="top", linespacing=1.6)

    ax.add_patch(FancyBboxPatch((0, -9.0), 100, 8.5,
                                boxstyle="round,pad=0,rounding_size=1.6",
                                facecolor=PANEL_LIGHT, edgecolor=GOLD, lw=1.6))
    ax.text(50, -4.7, "Aucune de ces étapes n'allonge la tournée   →   "
                      "Christofides ≤ 1,5 × OPT  pour un TSP métrique",
            fontsize=14, color=GOLD_SOFT, ha="center", va="center",
            fontweight="bold", fontfamily=HEAD_FONT)
    save(fig, OUT / "21_euler_hamilton_raccourci.png")


# ---------------------------------------------------------------------------
# 22 — Les quatre opérateurs
# ---------------------------------------------------------------------------
def fig_operateurs():
    fig, ax = blank((13, 6.9))
    head(ax, "Les quatre opérateurs de notre algorithme génétique",
         "Un chromosome est une permutation : chaque opérateur doit la préserver.",
         y=99, fs=24)

    p1 = ["B", "C", "D", "E", "F", "G", "H"]
    p2 = ["D", "G", "B", "H", "C", "F", "E"]
    left, right = 2, 5
    child = [None] * 7
    child[left:right] = p1[left:right]
    rest = [g for g in p2 if g not in child]
    it = iter(rest)
    for i in list(range(left)) + list(range(right, 7)):
        child[i] = next(it)

    cw, ch, gap, x0 = 5.4, 7.6, 0.9, 11.0
    seg = {g: GOLD for g in p1[left:right]}

    def strip(y, seq, label, colors, highlight_segment=True, faded=()):
        ax.text(x0 - 1.4, y + ch / 2, label, fontsize=11.5, color=TEXT,
                ha="right", va="center", fontweight="bold")
        for i, g in enumerate(seq):
            x = x0 + i * (cw + gap)
            inside = highlight_segment and left <= i < right
            col = colors.get(g, GRID)
            dim = g in faded
            ax.add_patch(FancyBboxPatch(
                (x, y), cw, ch, boxstyle="round,pad=0,rounding_size=1.0",
                facecolor=PANEL_LIGHT if inside else PANEL,
                edgecolor=col, lw=1.9 if inside else 1.1,
                alpha=0.35 if dim else 1.0))
            ax.text(x + cw / 2, y + ch / 2, g, fontsize=12, color=col,
                    ha="center", va="center", fontweight="bold",
                    fontfamily=HEAD_FONT, alpha=0.35 if dim else 1.0)

    ax.text(0, 82, "1 · CROISEMENT — Ordered Crossover (OX)", fontsize=13,
            color=GOLD, fontweight="bold", fontfamily=HEAD_FONT)
    strip(72, p1, "Parent 1", {**{g: MUTED for g in p1}, **seg})
    strip(60, p2, "Parent 2", {g: (GRID if g in seg else CYAN) for g in p2},
          highlight_segment=False, faded=set(seg))
    strip(45, child, "Enfant", {**{g: CYAN for g in child}, **seg})
    arrow(ax, x0 + 3.5 * (cw + gap), 58.5, x0 + 3.5 * (cw + gap), 54.5,
          color=GOLD, lw=1.8, ms=13)
    ax.text(0, 40, "Le segment du parent 1 est conservé ; les villes manquantes sont "
                   "reprises\ndans l'ordre du parent 2. Le résultat reste une "
                   "permutation valide.",
            fontsize=10.5, color=MUTED, va="top", linespacing=1.6)

    ax.text(0, 25, "2 · MUTATION — échange (swap) ou inversion de segment",
            fontsize=13, color=CORAL, fontweight="bold", fontfamily=HEAD_FONT)
    mw, mh, mg = 4.2, 6.6, 0.7

    def mrow(xs, y, seq, hl, color):
        for i, g in enumerate(seq):
            x = xs + i * (mw + mg)
            on = i in hl
            ax.add_patch(FancyBboxPatch(
                (x, y), mw, mh, boxstyle="round,pad=0,rounding_size=0.9",
                facecolor=PANEL_LIGHT if on else PANEL,
                edgecolor=color if on else GRID, lw=1.7 if on else 1.0))
            ax.text(x + mw / 2, y + mh / 2, g, fontsize=11,
                    color=color if on else MUTED, ha="center", va="center",
                    fontweight="bold", fontfamily=HEAD_FONT)

    base = ["A", "B", "C", "D", "E", "F"]
    for xs, after, hl, color, name in (
            (2, ["A", "E", "C", "D", "B", "F"], {1, 4}, CORAL, "swap"),
            (36, ["A", "E", "D", "C", "B", "F"], {1, 2, 3, 4}, VIOLET, "inversion")):
        ax.text(xs + 3 * (mw + mg) - mg / 2, 19.5, name, fontsize=11,
                color=color, ha="center", va="bottom")
        mrow(xs, 12, base, hl, color)
        mrow(xs, 1, after, hl, color)
        arrow(ax, xs + 3 * (mw + mg) - mg / 2, 11,
              xs + 3 * (mw + mg) - mg / 2, 8.6, color=color, lw=1.6, ms=12)

    ax.plot([67, 67], [0, 90], color=GRID, lw=1.1, ls=(0, (4, 4)))
    ax.text(71, 82, "3 · SÉLECTION — tournoi (k = 5)", fontsize=13, color=CYAN,
            fontweight="bold", fontfamily=HEAD_FONT)
    vals = [3412, 3289, 3877, 3157, 3602]
    for i, v in enumerate(vals):
        y = 72 - i * 8.4
        best = v == min(vals)
        ax.add_patch(FancyBboxPatch(
            (71, y), 21, 6.6, boxstyle="round,pad=0,rounding_size=1.0",
            facecolor=PANEL_LIGHT if best else PANEL,
            edgecolor=CYAN if best else GRID, lw=1.8 if best else 1.0))
        ax.text(72.8, y + 3.3, f"Tournée {i+1}", fontsize=10.5,
                color=TEXT if best else MUTED, va="center")
        ax.text(90.5, y + 3.3, f"{v} km", fontsize=11,
                color=CYAN if best else MUTED, va="center", ha="right",
                fontweight="bold")
        if best:
            ax.text(93.2, y + 3.3, "parent", fontsize=10.5, color=CYAN,
                    va="center", fontweight="bold")
    ax.text(71, 30, "5 individus tirés au hasard, le meilleur devient parent.\n"
                    "k règle la pression de sélection.",
            fontsize=10.5, color=MUTED, va="top", linespacing=1.6)

    ax.text(71, 17, "4 · ÉLITISME — 6 individus conservés", fontsize=13,
            color=GREEN, fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(71, 12, "Les 6 meilleures tournées passent telles quelles à la\n"
                    "génération suivante : la meilleure solution connue ne\n"
                    "peut jamais être perdue en cours de route.",
            fontsize=10.5, color=MUTED, va="top", linespacing=1.6)
    save(fig, OUT / "22_operateurs.png")


def main():
    print("Figures composées :")
    fig_euler_hamilton_raccourci()
    fig_operateurs()


if __name__ == "__main__":
    main()
