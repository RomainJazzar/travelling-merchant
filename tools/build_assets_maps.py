"""Génère les visuels cartographiques de la soutenance.

Toutes les données proviennent de l'exécution réelle du projet
(src/core.py, src/christofides.py, src/genetic.py) : aucun chiffre saisi à la main.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from tools.theme import (
    BG, PANEL_LIGHT, GRID, TEXT, MUTED, GOLD, GOLD_SOFT, CYAN, CYAN_SOFT,
    GREEN, CORAL, VIOLET, HEAD_FONT, apply_theme, draw_france, px, glow_line,
    save, titles_on,
)
from src.core import load_cities, distance_matrix, build_complete_graph
from src.christofides import christofides, prim_mst

OUT = ROOT / "FINAL_SOUTENANCE" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

apply_theme()

CITIES = load_cities(ROOT / "data" / "villes_france_lat_long.csv")
MATRIX = distance_matrix(CITIES)
GRAPH = build_complete_graph(CITIES, MATRIX)

# Décalages de libellés réglés à la main pour éviter tout chevauchement.
LABELS = {
    "Paris":            (0.00,  0.34, "center", "bottom"),
    "Lille":            (0.00,  0.34, "center", "bottom"),
    "Le Havre":         (-0.22, 0.04, "right",  "center"),
    "Reims":            (0.22,  0.10, "left",   "center"),
    "Strasbourg":       (0.22,  0.02, "left",   "center"),
    "Rennes":           (-0.22, 0.06, "right",  "center"),
    "Nantes":           (-0.22, 0.00, "right",  "center"),
    "Angers":           (0.22,  0.02, "left",   "center"),
    "Bordeaux":         (-0.22, 0.02, "right",  "center"),
    "Toulouse":         (-0.30, -0.06, "right", "center"),
    "Montpellier":      (-0.22, -0.16, "right", "center"),
    "Nîmes":            (0.08,  0.28, "left",   "bottom"),
    "Marseille":        (0.00, -0.38, "center", "top"),
    "Toulon":           (0.22, -0.14, "left",   "center"),
    "Nice":             (0.22,  0.06, "left",   "center"),
    "Grenoble":         (0.22, -0.08, "left",   "center"),
    "Lyon":             (0.22,  0.12, "left",   "center"),
    "Saint-Étienne":    (-0.22, -0.16, "right", "center"),
    "Clermont-Ferrand": (-0.22, 0.06, "right",  "center"),
    "Dijon":            (0.22,  0.08, "left",   "center"),
}



def label_cities(ax, size=11, color=TEXT, only=None, weight="normal"):
    for city in CITIES:
        if only is not None and city.name not in only:
            continue
        dx, dy, ha, va = LABELS[city.name]
        ax.text(px(city.longitude) + dx, city.latitude + dy, city.name,
                fontsize=size, color=color, ha=ha, va=va, zorder=8,
                fontweight=weight,
                path_effects=None)


def dots(ax, color=GOLD, size=62, edge=BG, zorder=7, only=None):
    xs = [px(c.longitude) for c in CITIES if only is None or c.name in only]
    ys = [c.latitude for c in CITIES if only is None or c.name in only]
    ax.scatter(xs, ys, s=size, color=color, zorder=zorder,
               edgecolors=edge, linewidths=1.6)


def legend(ax, handles, loc="lower left"):
    leg = ax.legend(handles=handles, loc=loc, fontsize=11.5, labelcolor=TEXT,
                    handlelength=1.6, borderaxespad=1.2)
    return leg


# ---------------------------------------------------------------------------
# 1. Les 20 villes
# ---------------------------------------------------------------------------
def fig_villes():
    fig, ax = plt.subplots(figsize=(8.2, 8.4))
    draw_france(ax)
    dots(ax, color=GOLD, size=90)
    label_cities(ax, size=12)
    if titles_on():
        ax.text(px(-5.2), 52.9, "20 villes françaises", fontsize=23, color=TEXT,
                fontfamily=HEAD_FONT, fontweight="bold", va="top")
        ax.text(px(-5.2), 52.15, "Sommets du graphe · coordonnées GPS du CSV",
                fontsize=13, color=MUTED, va="top")
    save(fig, OUT / "01_carte_villes.png")


# ---------------------------------------------------------------------------
# 2. Graphe complet : 190 arêtes
# ---------------------------------------------------------------------------
def fig_graphe_complet():
    fig, ax = plt.subplots(figsize=(8.2, 8.4))
    draw_france(ax)
    n = len(CITIES)
    for i in range(n):
        for j in range(i + 1, n):
            ax.plot([px(CITIES[i].longitude), px(CITIES[j].longitude)],
                    [CITIES[i].latitude, CITIES[j].latitude],
                    color=CYAN, linewidth=0.55, alpha=0.20, zorder=2)
    dots(ax, color=GOLD, size=70)
    if titles_on():
        ax.text(px(-5.2), 52.9, "Graphe complet pondéré", fontsize=23, color=TEXT,
                fontfamily=HEAD_FONT, fontweight="bold", va="top")
        ax.text(px(-5.2), 52.15, "20 sommets · 190 arêtes · poids = distance de Haversine",
                fontsize=13, color=MUTED, va="top")
    if titles_on():
        ax.text(px(-4.2), 50.1, "C(20,2) =\n20 × 19 / 2 =\n190 arêtes",
                fontsize=14, color=CYAN_SOFT, ha="center", va="center",
                fontfamily=HEAD_FONT,
                bbox=dict(boxstyle="round,pad=0.6", facecolor=PANEL_LIGHT,
                          edgecolor=CYAN, alpha=0.9, linewidth=1.2))
    save(fig, OUT / "02_graphe_complet.png")


# ---------------------------------------------------------------------------
# 3. MST de Prim
# ---------------------------------------------------------------------------
def fig_mst():
    mst_edges = prim_mst(GRAPH, start=0)
    weight = sum(w for _, _, w in mst_edges)
    fig, ax = plt.subplots(figsize=(8.2, 8.4))
    draw_france(ax)
    for u, v, _ in mst_edges:
        ax.plot([px(CITIES[u].longitude), px(CITIES[v].longitude)],
                [CITIES[u].latitude, CITIES[v].latitude],
                color=CYAN, linewidth=2.4, alpha=0.95, zorder=3,
                solid_capstyle="round")
    dots(ax, color=GOLD, size=75)
    label_cities(ax, size=10.5, color=MUTED)
    if titles_on():
        ax.text(px(-5.2), 52.9, "Arbre couvrant minimal (Prim)", fontsize=23,
                color=TEXT, fontfamily=HEAD_FONT, fontweight="bold", va="top")
        ax.text(px(-5.2), 52.15,
                f"19 arêtes · poids total {weight:,.2f} km".replace(",", " "),
                fontsize=13, color=CYAN_SOFT, va="top")
    if titles_on():
        ax.text(px(-4.2), 50.1, "n sommets\nn - 1 arêtes\naucun cycle",
                fontsize=13.5, color=MUTED, ha="center", va="center",
                fontfamily=HEAD_FONT,
                bbox=dict(boxstyle="round,pad=0.55", facecolor=PANEL_LIGHT,
                          edgecolor=GRID, alpha=0.9))
    save(fig, OUT / "03_mst_prim.png")
    return weight


# ---------------------------------------------------------------------------
# 4. Sommets impairs + couplage
# ---------------------------------------------------------------------------
def fig_matching():
    res = christofides(CITIES)
    mst_edges = prim_mst(GRAPH, start=0)
    odd = set(res.odd_vertices)

    import networkx as nx
    og = nx.Graph()
    og.add_nodes_from(res.odd_vertices)
    for i, u in enumerate(res.odd_vertices):
        for v in res.odd_vertices[i + 1:]:
            og.add_edge(u, v, weight=MATRIX[u][v])
    matching = nx.algorithms.matching.min_weight_matching(og, weight="weight")

    fig, ax = plt.subplots(figsize=(8.2, 8.4))
    draw_france(ax)
    for u, v, _ in mst_edges:
        ax.plot([px(CITIES[u].longitude), px(CITIES[v].longitude)],
                [CITIES[u].latitude, CITIES[v].latitude],
                color=CYAN, linewidth=1.8, alpha=0.45, zorder=3)
    for u, v in matching:
        glow_line(ax, [px(CITIES[u].longitude), px(CITIES[v].longitude)],
                  [CITIES[u].latitude, CITIES[v].latitude],
                  CORAL, width=3.0, zorder=5)

    even_names = {c.name for i, c in enumerate(CITIES) if i not in odd}
    odd_names = {c.name for i, c in enumerate(CITIES) if i in odd}
    dots(ax, color=MUTED, size=55, only=even_names)
    dots(ax, color=GOLD, size=135, only=odd_names)
    label_cities(ax, size=10.5, color=MUTED, only=even_names)
    label_cities(ax, size=11, color=GOLD_SOFT, only=odd_names, weight="bold")

    if titles_on():
        ax.text(px(-5.2), 52.9, "Sommets impairs + couplage minimal", fontsize=22,
                color=TEXT, fontfamily=HEAD_FONT, fontweight="bold", va="top")
        ax.text(px(-5.2), 52.15,
                f"{len(odd)} sommets de degré impair · couplage {res.matching_weight_km:.2f} km",
                fontsize=13, color=MUTED, va="top")
    legend(ax, [
        Line2D([], [], color=CYAN, lw=2.4, label="Arbre couvrant minimal"),
        Line2D([], [], color=CORAL, lw=3.0, label="6 arêtes de couplage"),
        Line2D([], [], color=GOLD, marker="o", lw=0, markersize=10,
               label="Sommet de degré impair"),
        Line2D([], [], color=MUTED, marker="o", lw=0, markersize=6,
               label="Sommet de degré pair"),
    ], loc="lower left")
    save(fig, OUT / "04_impairs_matching.png")
    return res


# ---------------------------------------------------------------------------
# 5 & 6. Les deux itinéraires
# ---------------------------------------------------------------------------
def fig_route(route, color, name, subtitle, filename, headline):
    fig, ax = plt.subplots(figsize=(8.2, 8.4))
    draw_france(ax)
    xs = [px(CITIES[i].longitude) for i in route]
    ys = [CITIES[i].latitude for i in route]
    glow_line(ax, xs, ys, color, width=2.9, zorder=4)

    for step, idx in enumerate(route[:-1], start=1):
        c = CITIES[idx]
        ax.scatter([px(c.longitude)], [c.latitude], s=150, color=BG,
                   edgecolors=color, linewidths=1.9, zorder=7)
        ax.text(px(c.longitude), c.latitude, str(step), fontsize=8.5,
                color=color, ha="center", va="center", zorder=8,
                fontweight="bold", fontfamily=HEAD_FONT)
    start = CITIES[route[0]]
    ax.scatter([px(start.longitude)], [start.latitude], s=330, color=GOLD,
               alpha=0.20, zorder=6)
    label_cities(ax, size=10.5, color=MUTED)

    if titles_on():
        ax.text(px(-5.2), 52.9, name, fontsize=23, color=TEXT,
                fontfamily=HEAD_FONT, fontweight="bold", va="top")
        ax.text(px(-5.2), 52.15, subtitle, fontsize=13, color=MUTED, va="top")
    if titles_on():
        ax.text(px(-4.1), 43.0, headline, fontsize=20, color=color, ha="center",
                va="center", fontfamily=HEAD_FONT, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.7", facecolor=PANEL_LIGHT,
                          edgecolor=color, alpha=0.92, linewidth=1.4))
    save(fig, OUT / filename)


def main():
    print("Cartes :")
    fig_villes()
    fig_graphe_complet()
    mst_w = fig_mst()
    res = fig_matching()

    fig_route(res.route, CYAN, "Itinéraire Christofides",
              "Départ et retour à Paris · 20 villes visitées une seule fois",
              "05_route_christofides.png", f"{res.distance_km:.2f} km")

    # Rejoue exactement la configuration retenue par main.py.
    from dataclasses import asdict
    from src.genetic import GAConfig, genetic_tsp
    base = GAConfig(population_size=160, generations=520, tournament_size=5,
                    mutation_rate=0.22, elite_size=6)
    ga = min((genetic_tsp(CITIES, GAConfig(**{**asdict(base), "seed": s}))
              for s in (11, 22, 33)), key=lambda r: r.distance_km)
    fig_route(ga.route, GOLD, "Itinéraire algorithme génétique",
              "Configuration équilibrée · meilleure tournée observée",
              "06_route_genetique.png", f"{ga.distance_km:.2f} km")

    print(f"\nMST={mst_w:.4f}  Christofides={res.distance_km:.4f}  GA={ga.distance_km:.4f}")


if __name__ == "__main__":
    main()
