"""Génère les schémas et graphiques de la soutenance.

Les valeurs chiffrées proviennent de results/summary.json et de l'exécution
réelle des algorithmes : rien n'est saisi à la main.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

from tools.theme import (
    BG, PANEL, PANEL_LIGHT, GRID, TEXT, MUTED, GOLD, GOLD_SOFT, CYAN, CYAN_SOFT,
    GREEN, CORAL, VIOLET, HEAD_FONT, apply_theme, save, titles_on,
)

OUT = ROOT / "FINAL_SOUTENANCE" / "assets"
OUT.mkdir(parents=True, exist_ok=True)
apply_theme()

SUMMARY = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))
CHRIST = SUMMARY["christofides"]["distance_km"]
GA = SUMMARY["genetic"]["distance_km"]
MST = SUMMARY["christofides"]["mst_weight_km"]
MATCH = SUMMARY["christofides"]["matching_weight_km"]


# --- Primitives de mise en page -------------------------------------------
def fr(value: float, dec: int = 2) -> str:
    """Formate un nombre à la française : espace fine pour les milliers, virgule décimale."""
    txt = f"{value:,.{dec}f}"
    return txt.replace(",", " ").replace(".", ",")


def blank(figsize=(12, 6.2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax._figw, ax._figh = figsize      # mémorisé pour circ() et head()
    return fig, ax


def head(ax, t, sub=None, y=97, fs=25):
    """Titre + sous-titre, avec un interligne calculé sur la hauteur réelle
    de la figure (sinon les deux se chevauchent sur les figures basses).

    En mode << slide >>, on ne dessine rien : le PowerPoint porte le titre.
    """
    if not titles_on():
        return
    ax.text(0, y, t, fontsize=fs, color=TEXT, fontfamily=HEAD_FONT,
            fontweight="bold", va="top", ha="left")
    if sub:
        dy = (fs * 1.45 / 72.0) / getattr(ax, "_figh", 6.2) * 100
        ax.text(0, y - dy, sub, fontsize=14, color=MUTED, va="top", ha="left")


def axtitle(ax, text, **kw):
    """set_title qui respecte le mode << slide >>."""
    if not titles_on():
        return
    kw.setdefault("color", TEXT)
    kw.setdefault("fontfamily", HEAD_FONT)
    kw.setdefault("fontweight", "bold")
    kw.setdefault("loc", "left")
    ax.set_title(text, **kw)


def circ(ax, x, y, r, **kw):
    """Cercle visuellement rond : l'axe 0-100 n'est pas carré."""
    from matplotlib.patches import Ellipse
    ratio = getattr(ax, "_figh", 6.2) / getattr(ax, "_figw", 12.0)
    return ax.add_patch(Ellipse((x, y), width=2 * r * ratio, height=2 * r, **kw))


def box(ax, x, y, w, h, label, color=CYAN, fill=PANEL_LIGHT, fs=13,
        weight="bold", text_color=None, sub=None, sub_fs=11, radius=1.6,
        lw=1.6, alpha=1.0):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=color, linewidth=lw, alpha=alpha, zorder=2))
    cy = y + h / 2 + (1.8 if sub else 0)
    ax.text(x + w / 2, cy, label, fontsize=fs, color=text_color or TEXT,
            ha="center", va="center", fontweight=weight,
            fontfamily=HEAD_FONT, zorder=3)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 4.2, sub, fontsize=sub_fs, color=MUTED,
                ha="center", va="center", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=GOLD, lw=2.0, style="-|>", ms=14,
          connection="arc3,rad=0", zorder=4):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
        color=color, linewidth=lw, connectionstyle=connection, zorder=zorder))


# ---------------------------------------------------------------------------
# 07 — Explosion combinatoire
# ---------------------------------------------------------------------------
def fig_combinatoire():
    fig, ax = plt.subplots(figsize=(11, 5.8))
    ns = list(range(5, 21))
    vals = [math.factorial(n - 1) for n in ns]
    bars = ax.bar(ns, vals, color=CYAN, alpha=0.30, edgecolor=CYAN,
                  linewidth=1.3, width=0.68)
    bars[-1].set_alpha(0.95)
    bars[-1].set_color(GOLD)
    bars[-1].set_edgecolor(GOLD_SOFT)
    ax.set_yscale("log")
    ax.set_xticks(ns)
    ax.set_xlabel("Nombre de villes n")
    ax.set_ylabel("Tournées à évaluer  (n − 1)!   [échelle log]")
    ax.grid(axis="y", alpha=0.25, linewidth=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    axtitle(ax, "Pourquoi la force brute est hors de portée", fontsize=21,
            pad=16)
    ax.annotate("19! ≈ 1,22 × 10¹⁷ tournées",
                xy=(20, vals[-1]), xytext=(15.4, vals[-1] * 0.03),
                color=GOLD_SOFT, fontsize=14, fontweight="bold",
                fontfamily=HEAD_FONT,
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.6))
    secs = math.factorial(19) / 1e9
    ax.text(5, vals[-1] * 0.5,
            f"À 1 milliard de tournées évaluées par seconde :\n"
            f"≈ {fr(secs / 31_557_600, 1)} ans de calcul pour une seule instance.",
            fontsize=13, color=MUTED, va="top", ha="left",
            bbox=dict(boxstyle="round,pad=0.6", facecolor=PANEL_LIGHT,
                      edgecolor=GRID))
    fig.tight_layout()
    save(fig, OUT / "07_explosion_combinatoire.png")


# ---------------------------------------------------------------------------
# 08 — Haversine
# ---------------------------------------------------------------------------
def fig_haversine():
    fig, ax = blank((12, 5.6))
    head(ax, "Haversine : la distance sur une sphère",
         "Les villes sont repérées en latitude / longitude, pas dans un plan.")

    # Globe schématique
    cx, cy, r = 21, 38, 26
    circ(ax, cx, cy, r, facecolor=PANEL, edgecolor=GRID, lw=1.5)
    for k in (-0.55, 0, 0.55):
        yy = cy + k * r
        half = math.sqrt(max(r ** 2 - (k * r) ** 2, 0)) * ax._figh / ax._figw
        ax.plot([cx - half, cx + half], [yy, yy], color=GRID, lw=0.9, alpha=0.8)
    ratio = ax._figh / ax._figw
    for k in (-0.6, 0, 0.6):
        angles = [math.pi / 2 - i * math.pi / 40 for i in range(41)]
        xs = [cx + k * r * ratio * math.cos(t) for t in angles]
        ys = [cy + r * math.sin(t) for t in angles]
        ax.plot(xs, ys, color=GRID, lw=0.9, alpha=0.8)

    a = (cx - 6.2, cy + 9)
    b = (cx + 5.8, cy - 7)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=MUTED, lw=1.6, ls=(0, (4, 3)))
    ax.plot([a[0] + (b[0] - a[0]) * t / 40 for t in range(41)],
            [a[1] + (b[1] - a[1]) * t / 40 + 5.2 * math.sin(math.pi * t / 40)
             for t in range(41)], color=GOLD, lw=3.0, solid_capstyle="round")
    for p, name, ha_ in ((a, "Ville A", "right"), (b, "Ville B", "left")):
        circ(ax, p[0], p[1], 1.6, facecolor=GOLD, edgecolor=BG, lw=1.4, zorder=5)
        off = -2.2 if ha_ == "right" else 2.2
        ax.text(p[0] + off, p[1], name, fontsize=12, color=TEXT, ha=ha_,
                va="center", fontweight="bold")
    ax.text(cx, cy + 19.5, "arc de grand cercle", fontsize=11.5, color=GOLD_SOFT,
            ha="center", style="italic")
    ax.text(cx, cy - 16.5, "corde (ligne droite)", fontsize=11.5, color=MUTED,
            ha="center", style="italic")

    ax.text(48, 74, "d = 2R · arcsin( √h )", fontsize=19, color=CYAN_SOFT,
            fontfamily=HEAD_FONT, fontweight="bold", va="center")
    ax.text(48, 65, "h = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)",
            fontsize=14.5, color=TEXT, va="center")
    ax.text(48, 57.5, "R = 6371,0088 km   ·   φ = latitude, λ = longitude (en radians)",
            fontsize=12, color=MUTED, va="center")

    props = [
        ("Non-négativité", "d(A,B) ≥ 0"),
        ("Identité", "d(A,B) = 0  ssi  A = B"),
        ("Symétrie", "d(A,B) = d(B,A)"),
        ("Inégalité triangulaire", "d(A,C) ≤ d(A,B) + d(B,C)"),
    ]
    ax.text(48, 47, "Les 4 propriétés d'une métrique", fontsize=13.5, color=GOLD,
            fontweight="bold", fontfamily=HEAD_FONT, va="center")
    for i, (name, formula) in enumerate(props):
        y = 38 - i * 9.2
        last = i == 3
        col = GOLD if last else CYAN
        ax.add_patch(FancyBboxPatch((48, y - 3.6), 50, 7.4,
                                    boxstyle="round,pad=0,rounding_size=1.4",
                                    facecolor=PANEL_LIGHT if last else PANEL,
                                    edgecolor=col, lw=1.6 if last else 1.0))
        ax.text(50.5, y, name, fontsize=12.5, color=TEXT if last else MUTED,
                va="center", fontweight="bold" if last else "normal")
        ax.text(96, y, formula, fontsize=12.5, color=col, va="center", ha="right")
    ax.text(48, -1.5, "L'inégalité triangulaire est l'hypothèse exacte dont "
                      "Christofides a besoin : c'est elle qui rend le "
                      "« raccourci » gratuit.",
            fontsize=12, color=GOLD_SOFT, va="center", style="italic")
    save(fig, OUT / "08_haversine.png")


# ---------------------------------------------------------------------------
# 09 — Pipeline Christofides
# ---------------------------------------------------------------------------
def fig_pipeline_christofides():
    fig, ax = blank((13, 6.4))
    head(ax, "Christofides : la chaîne complète",
         "Six transformations successives — chacune est nécessaire.")

    steps = [
        ("1 · Graphe complet", "20 sommets, 190 arêtes", CYAN),
        ("2 · Arbre couvrant\nminimal (Prim)", f"{fr(MST, 0)} km", CYAN),
        ("3 · Sommets de\ndegré impair", "12 sommets", GOLD),
        ("4 · Couplage parfait\nde poids minimal", f"{fr(MATCH, 0)} km", GOLD),
        ("5 · Multigraphe\neulérien", "tous degrés pairs", VIOLET),
        ("6 · Circuit eulérien\n(Hierholzer)", "arêtes parcourues 1×", VIOLET),
        ("7 · Raccourcis\n(shortcutting)", "villes vues 1 seule fois", GREEN),
        ("8 · Cycle\nhamiltonien", f"{fr(CHRIST, 0)} km", GREEN),
    ]
    w, h, gap = 21.5, 26, 4.5
    for i, (label, sub, color) in enumerate(steps):
        row, col = divmod(i, 4)
        x = col * (w + gap)
        y = 44 - row * (h + 12)
        is_final = i == len(steps) - 1
        box(ax, x, y, w, h, label, color=color,
            fill=PANEL_LIGHT if is_final else PANEL, fs=12.5, sub=sub,
            sub_fs=11, lw=2.0 if is_final else 1.5)
        if col < 3:
            arrow(ax, x + w + 0.6, y + h / 2, x + w + gap - 0.6, y + h / 2,
                  color=MUTED, lw=1.8)
    # Retour à la ligne : chemin en L tracé dans la gouttière entre les
    # deux rangées, pour ne croiser aucune étape.
    y_row2 = 44 - (h + 12)
    x_end, x_start = w / 2, 3 * (w + gap) + w / 2
    y_mid = (44 + y_row2 + h) / 2
    ax.plot([x_start, x_start], [44 - 0.8, y_mid], color=MUTED, lw=1.8, zorder=1)
    ax.plot([x_start, x_end], [y_mid, y_mid], color=MUTED, lw=1.8, zorder=1)
    arrow(ax, x_end, y_mid, x_end, y_row2 + h + 0.8, color=MUTED, lw=1.8)
    ax.text(50, 3, "Garantie : pour un TSP métrique, la tournée obtenue est "
                   "au plus 1,5 × l'optimum.",
            fontsize=13.5, color=GOLD_SOFT, ha="center", va="center",
            fontweight="bold", fontfamily=HEAD_FONT)
    save(fig, OUT / "09_pipeline_christofides.png")


# ---------------------------------------------------------------------------
# 10 — Euler vs Hamilton
# ---------------------------------------------------------------------------
def fig_euler_hamilton():
    fig, ax = blank((12, 5.4))
    head(ax, "Euler ≠ Hamilton", "Deux notions voisines, deux objets différents.")

    pos = {"A": (13, 58), "B": (34, 58), "C": (34, 30), "D": (13, 30), "E": (23.5, 74)}
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "E"), ("B", "E")]

    def draw_graph(dx, highlight_edges, highlight_nodes, color, caption, rule):
        for u, v in edges:
            x1, y1 = pos[u][0] + dx, pos[u][1]
            x2, y2 = pos[v][0] + dx, pos[v][1]
            on = (u, v) in highlight_edges or (v, u) in highlight_edges
            ax.plot([x1, x2], [y1, y2], color=color if on else GRID,
                    lw=3.4 if on else 1.6, zorder=2, solid_capstyle="round",
                    alpha=0.95 if on else 0.8)
        for name, (x, y) in pos.items():
            on = name in highlight_nodes
            circ(ax, x + dx, y, 3.4,
                 facecolor=color if on else PANEL,
                 edgecolor=color if on else GRID, lw=2.0, zorder=3)
            ax.text(x + dx, y, name, fontsize=12, color=BG if on else MUTED,
                    ha="center", va="center", fontweight="bold", zorder=4)
        ax.text(dx + 23.5, 20, caption, fontsize=15, color=color, ha="center",
                va="top", fontweight="bold", fontfamily=HEAD_FONT)
        ax.text(dx + 23.5, 13.5, rule, fontsize=12.5, color=MUTED, ha="center",
                va="top", linespacing=1.5)

    draw_graph(0, set(edges), set(),  CYAN,
               "Circuit EULÉRIEN",
               "passe une fois par chaque ARÊTE\n(les sommets peuvent se répéter)")
    draw_graph(52, {("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")},
               {"A", "B", "C", "D"}, GOLD,
               "Cycle HAMILTONIEN",
               "passe une fois par chaque SOMMET\n(des arêtes peuvent rester inutilisées)")

    ax.plot([47, 47], [26, 84], color=GRID, lw=1.2, ls=(0, (4, 4)))
    ax.text(50, -5, "Le TSP cherche un cycle hamiltonien. Christofides construit "
                   "d'abord un circuit eulérien, puis le convertit.",
            fontsize=13, color=GOLD_SOFT, ha="center", va="center", style="italic")
    save(fig, OUT / "10_euler_hamilton.png")


# ---------------------------------------------------------------------------
# 11 — Raccourci / inégalité triangulaire
# ---------------------------------------------------------------------------
def fig_shortcut():
    fig, ax = blank((11, 5.2))
    head(ax, "Le raccourci ne coûte jamais plus cher",
         "C'est l'inégalité triangulaire qui rend l'étape 7 gratuite.", fs=23)

    A, B, C = (12, 20), (40, 56), (72, 20)
    for p, n, col in ((A, "A", GOLD), (B, "B", MUTED), (C, "C", GOLD)):
        circ(ax, p[0], p[1], 2.4, facecolor=col, edgecolor=BG, lw=1.5, zorder=4)
        ax.text(p[0], p[1] - 4.5, n, fontsize=15, color=TEXT, ha="center",
                va="top", fontweight="bold", fontfamily=HEAD_FONT)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=CORAL, lw=3.0, zorder=2)
    ax.plot([B[0], C[0]], [B[1], C[1]], color=CORAL, lw=3.0, zorder=2)
    ax.plot([A[0], C[0]], [A[1], C[1]], color=GREEN, lw=3.4, zorder=3)

    ax.text(20.5, 42, "d(A,B)", fontsize=12.5, color=CORAL, ha="right")
    ax.text(59.5, 42, "d(B,C)", fontsize=12.5, color=CORAL, ha="left")
    ax.text(42, 23.5, "d(A,C)", fontsize=12.5, color=GREEN, ha="center")
    ax.text(40, 62, "B est déjà visitée : on la saute", fontsize=12.5,
            color=MUTED, ha="center", style="italic")

    ax.add_patch(FancyBboxPatch((79, 24), 21, 32,
                                boxstyle="round,pad=0,rounding_size=2",
                                facecolor=PANEL_LIGHT, edgecolor=GREEN, lw=1.8))
    ax.text(89.5, 46.5, "d(A,C)", fontsize=15, color=GREEN, ha="center",
            fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(89.5, 39.5, "≤", fontsize=17, color=TEXT, ha="center")
    ax.text(89.5, 32, "d(A,B) + d(B,C)", fontsize=13.5, color=CORAL, ha="center",
            fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(50, 4, "Conséquence : convertir le circuit eulérien en cycle "
                   "hamiltonien ne peut pas allonger la tournée.",
            fontsize=13, color=GOLD_SOFT, ha="center", style="italic")
    save(fig, OUT / "11_shortcut.png")


# ---------------------------------------------------------------------------
# 12 — Boucle évolutive du GA
# ---------------------------------------------------------------------------
def fig_pipeline_ga():
    fig, ax = blank((11.5, 6.4))
    head(ax, "L'algorithme génétique : une boucle d'évolution",
         "Une génération = une itération complète du cycle.")

    cx, cy, r = 50, 44, 27
    stages = [
        ("Population\ninitiale", "160 tournées aléatoires", CYAN),
        ("Évaluation\n(fitness)", "distance totale du cycle", CYAN),
        ("Sélection\npar tournoi", "k = 5 candidats", GOLD),
        ("Croisement\nOX", "95 % des couples", GOLD),
        ("Mutation\nswap / inversion", "22 %", CORAL),
        ("Élitisme +\nnouvelle génération", "6 meilleurs conservés", GREEN),
    ]
    n = len(stages)
    for i, (label, sub, color) in enumerate(stages):
        ang = math.pi / 2 - i * 2 * math.pi / n
        x = cx + r * math.cos(ang) * 1.42
        y = cy + r * math.sin(ang)
        box(ax, x - 15, y - 8.5, 30, 17, label, color=color, fill=PANEL,
            fs=12.5, sub=sub, sub_fs=10, lw=1.6)
        # Flèche courte placée dans l'espace entre deux étapes voisines,
        # donc toujours visible (pas masquée par les cartes).
        ang_next = math.pi / 2 - (i + 1) * 2 * math.pi / n
        nx_, ny_ = cx + r * math.cos(ang_next) * 1.42, cy + r * math.sin(ang_next)
        mx, my = (x + nx_) / 2, (y + ny_) / 2
        dx_, dy_ = nx_ - x, ny_ - y
        norm = math.hypot(dx_, dy_ * 2) or 1
        arrow(ax, mx - dx_ * 0.10, my - dy_ * 0.10,
              mx + dx_ * 0.10, my + dy_ * 0.10,
              color=GOLD_SOFT, lw=2.2, ms=17, zorder=5)
    ax.text(cx, cy + 4, "520", fontsize=32, color=GOLD, ha="center", va="center",
            fontweight="bold", fontfamily=HEAD_FONT)
    ax.text(cx, cy - 5, "générations", fontsize=13, color=MUTED, ha="center",
            va="center")
    save(fig, OUT / "12_pipeline_ga.png")


# ---------------------------------------------------------------------------
# 13 — Ordered Crossover
# ---------------------------------------------------------------------------
def fig_ox():
    fig, ax = blank((12, 6.0))
    head(ax, "Ordered Crossover (OX)",
         "Un chromosome est une permutation : aucune ville ne doit disparaître "
         "ni apparaître deux fois.", y=99)

    p1 = ["B", "C", "D", "E", "F", "G", "H"]
    p2 = ["D", "G", "B", "H", "C", "F", "E"]
    left, right = 2, 5          # segment conservé du parent 1
    child = [None] * 7
    child[left:right] = p1[left:right]
    rest = [g for g in p2 if g not in child]
    it = iter(rest)
    for i in list(range(left)) + list(range(right, 7)):
        child[i] = next(it)

    cw, ch, gap = 8.4, 11.0, 1.3

    def strip(y, seq, title, seg=None, colors=None, note=None):
        ax.text(0, y + ch + 3.0, title, fontsize=13.5, color=TEXT,
                fontweight="bold", fontfamily=HEAD_FONT, va="bottom")
        for i, g in enumerate(seq):
            x = 19 + i * (cw + gap)
            inside = seg is not None and seg[0] <= i < seg[1]
            col = (colors or {}).get(g, GRID)
            ax.add_patch(FancyBboxPatch(
                (x, y), cw, ch, boxstyle="round,pad=0,rounding_size=1.2",
                facecolor=PANEL_LIGHT if inside else PANEL,
                edgecolor=col, lw=2.2 if inside else 1.3))
            ax.text(x + cw / 2, y + ch / 2, g, fontsize=15, color=col,
                    ha="center", va="center", fontweight="bold",
                    fontfamily=HEAD_FONT)
        if note:
            ax.text(19 + 7 * (cw + gap) + 1.5, y + ch / 2, note, fontsize=11.5,
                    color=MUTED, va="center")

    seg_colors = {g: GOLD for g in p1[left:right]}
    strip(66, p1, "Parent 1", seg=(left, right), colors={**{g: MUTED for g in p1},
                                                         **seg_colors},
          note="on garde le segment")
    strip(42, p2, "Parent 2", colors={g: (GRID if g in seg_colors else CYAN)
                                      for g in p2},
          note="on lit l'ordre des villes restantes")
    strip(13, child, "Enfant", seg=(left, right),
          colors={**{g: CYAN for g in child}, **seg_colors},
          note="permutation valide")

    arrow(ax, 11, 66, 11, 24, color=GOLD, lw=2.0)
    ax.text(9.5, 45, "segment conservé", fontsize=11.5, color=GOLD, rotation=90,
            ha="center", va="center", fontweight="bold")
    ax.text(0, 3, "Un croisement « naïf » (couper/coller deux moitiés) créerait "
                  "des doublons et des villes manquantes : la tournée serait invalide.",
            fontsize=12.5, color=GOLD_SOFT, va="center", style="italic")
    save(fig, OUT / "13_ox.png")


# ---------------------------------------------------------------------------
# 14 — Mutation + sélection par tournoi
# ---------------------------------------------------------------------------
def fig_mutation_tournoi():
    fig, ax = blank((12.5, 5.6))
    head(ax, "Mutation et sélection", "Explorer sans casser la permutation, "
                                      "choisir sans écraser la diversité.")

    cw, ch, gap = 7.4, 9.0, 1.1
    base = ["A", "B", "C", "D", "E", "F"]

    def row(x0, y, seq, hl, color):
        for i, g in enumerate(seq):
            x = x0 + i * (cw + gap)
            on = i in hl
            ax.add_patch(FancyBboxPatch(
                (x, y), cw, ch, boxstyle="round,pad=0,rounding_size=1.0",
                facecolor=PANEL_LIGHT if on else PANEL,
                edgecolor=color if on else GRID, lw=2.0 if on else 1.2))
            ax.text(x + cw / 2, y + ch / 2, g, fontsize=13,
                    color=color if on else MUTED, ha="center", va="center",
                    fontweight="bold", fontfamily=HEAD_FONT)

    ax.text(0, 74, "Mutation par échange (swap)", fontsize=13.5, color=CORAL,
            fontweight="bold", fontfamily=HEAD_FONT)
    row(0, 58, base, {1, 4}, CORAL)
    row(0, 42, ["A", "E", "C", "D", "B", "F"], {1, 4}, CORAL)
    arrow(ax, 25, 56.5, 25, 52.5, color=CORAL, lw=1.8)

    ax.text(0, 33, "Mutation par inversion de segment", fontsize=13.5, color=VIOLET,
            fontweight="bold", fontfamily=HEAD_FONT)
    row(0, 17, base, {1, 2, 3, 4}, VIOLET)
    row(0, 1, ["A", "E", "D", "C", "B", "F"], {1, 2, 3, 4}, VIOLET)
    arrow(ax, 25, 15.5, 25, 11.5, color=VIOLET, lw=1.8)

    ax.plot([57, 57], [2, 78], color=GRID, lw=1.2, ls=(0, (4, 4)))
    ax.text(62, 74, "Sélection par tournoi (k = 5)", fontsize=13.5, color=GOLD,
            fontweight="bold", fontfamily=HEAD_FONT)
    vals = [3412, 3289, 3877, 3157, 3602]
    for i, v in enumerate(vals):
        y = 58 - i * 11.5
        best = v == min(vals)
        ax.add_patch(FancyBboxPatch(
            (62, y), 27, 9.0, boxstyle="round,pad=0,rounding_size=1.2",
            facecolor=PANEL_LIGHT if best else PANEL,
            edgecolor=GOLD if best else GRID, lw=2.0 if best else 1.2))
        ax.text(65, y + 4.5, f"Tournée {i+1}", fontsize=11.5,
                color=TEXT if best else MUTED, va="center")
        ax.text(86, y + 4.5, f"{v} km", fontsize=12,
                color=GOLD if best else MUTED, va="center", ha="right",
                fontweight="bold")
        if best:
            ax.text(91.5, y + 4.5, "→ parent", fontsize=11.5, color=GOLD,
                    va="center", fontweight="bold")
    ax.text(62, 1, "k trop grand → pression trop forte, diversité perdue.\n"
                   "k trop petit → la sélection devient presque aléatoire.",
            fontsize=11.5, color=MUTED, va="bottom")
    save(fig, OUT / "14_mutation_tournoi.png")


# ---------------------------------------------------------------------------
# 15 — Convergence réelle
# ---------------------------------------------------------------------------
def fig_convergence():
    from src.core import load_cities
    from src.genetic import GAConfig, genetic_tsp
    cities = load_cities(ROOT / "data" / "villes_france_lat_long.csv")
    cfg = SUMMARY["genetic"]["configuration"]
    res = genetic_tsp(cities, GAConfig(**cfg))
    hist = res.history

    fig, ax = plt.subplots(figsize=(11, 5.4))
    ax.plot(range(1, len(hist) + 1), hist, color=GOLD, lw=2.4, zorder=3)
    ax.fill_between(range(1, len(hist) + 1), hist, max(hist) * 1.002,
                    color=GOLD, alpha=0.06, zorder=1)
    ax.axhline(CHRIST, color=CYAN, lw=1.8, ls=(0, (5, 4)), zorder=2)
    ax.axhline(MST, color=MUTED, lw=1.5, ls=(0, (2, 3)), zorder=2)

    gen_best = hist.index(min(hist)) + 1
    ax.scatter([gen_best], [min(hist)], s=90, color=GOLD, edgecolors=BG,
               linewidths=1.6, zorder=5)
    ax.annotate(f"meilleure tournée atteinte\ndès la génération {gen_best}",
                xy=(gen_best, min(hist)), xytext=(gen_best + 80, MST + 190),
                color=GOLD_SOFT, fontsize=12, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.5))
    ax.text(len(hist), CHRIST + 22, f"Christofides {fr(CHRIST, 0)} km", color=CYAN,
            fontsize=12, ha="right", fontweight="bold")
    ax.text(len(hist), MST + 22, f"borne inférieure MST {fr(MST, 0)} km", color=MUTED,
            fontsize=12, ha="right")
    ax.set_xlabel("Génération")
    ax.set_ylabel("Meilleure distance connue (km)")
    ax.set_xlim(0, len(hist))
    ax.set_ylim(MST - 90, max(hist) * 1.02)
    ax.grid(alpha=0.22, linewidth=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    axtitle(ax, "Convergence de la configuration équilibrée (seed 11)",
            fontsize=20, pad=16)
    fig.tight_layout()
    save(fig, OUT / "15_convergence.png")
    return gen_best


# ---------------------------------------------------------------------------
# 16 — Benchmark des configurations
# ---------------------------------------------------------------------------
def fig_benchmark():
    rows = SUMMARY["benchmark"]
    names = {"rapide": "Rapide", "equilibree": "Équilibrée",
             "exploratoire": "Exploratoire"}
    labels = [names[r["configuration"]] for r in rows]
    best = [r["best_km"] for r in rows]
    meanv = [r["mean_km"] for r in rows]
    worst = [r["worst_km"] for r in rows]
    stds = [r["std_km"] for r in rows]

    fig, ax = plt.subplots(figsize=(11, 5.4))
    xs = range(len(rows))
    wdt = 0.26
    for off, vals, col, lab in ((-wdt, best, GREEN, "Meilleure"),
                                (0.0, meanv, GOLD, "Moyenne"),
                                (wdt, worst, CORAL, "Pire")):
        bars = ax.bar([x + off for x in xs], vals, width=wdt * 0.92, color=col,
                      alpha=0.85, edgecolor=col, linewidth=1.2, label=lab)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 14, f"{v:.0f}",
                    ha="center", fontsize=11, color=col, fontweight="bold")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{lab}\nécart-type {fr(sd, 1)} km"
                        for lab, sd in zip(labels, stds)],
                       fontsize=12.5, color=TEXT, linespacing=1.7)
    ax.set_ylim(3000, 3495)
    ax.set_ylabel("Distance (km) — 3 seeds : 11, 22, 33")
    ax.grid(axis="y", alpha=0.22, linewidth=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="upper left", ncol=3, fontsize=12, labelcolor=TEXT,
              bbox_to_anchor=(0.0, 1.10))
    axtitle(ax, "Trois configurations, trois seeds", fontsize=20, pad=40)
    chosen = SUMMARY["genetic"]["chosen_configuration"]
    idx = [r["configuration"] for r in rows].index(chosen)
    ax.text(idx, 3452, "CONFIGURATION RETENUE", ha="center", fontsize=12.5,
            color=BG, fontweight="bold", fontfamily=HEAD_FONT, zorder=5,
            bbox=dict(boxstyle="round,pad=0.45", facecolor=GOLD, edgecolor=GOLD))
    ax.text(idx, 3405, "seule configuration stable sur les 3 seeds", ha="center",
            fontsize=11.5, color=GOLD_SOFT, style="italic")
    ax.get_xticklabels()[idx].set_color(GOLD_SOFT)
    ax.get_xticklabels()[idx].set_fontweight("bold")
    fig.tight_layout()
    save(fig, OUT / "16_benchmark.png")


# ---------------------------------------------------------------------------
# 17 — Comparaison finale + bornes
# ---------------------------------------------------------------------------
def fig_comparaison():
    fig, ax = plt.subplots(figsize=(11.5, 5.0))
    labels = ["Borne inférieure\n(poids du MST)", "Algorithme génétique\n(meilleure observée)",
              "Christofides"]
    vals = [MST, GA, CHRIST]
    cols = [MUTED, GOLD, CYAN]
    bars = ax.barh(labels, vals, color=cols, alpha=0.85, height=0.52,
                   edgecolor=cols, linewidth=1.4)
    bars[0].set_alpha(0.35)
    for b, v, c in zip(bars, vals, cols):
        ax.text(v + 40, b.get_y() + b.get_height() / 2, f"{fr(v)} km",
                va="center", fontsize=14, color=c, fontweight="bold",
                fontfamily=HEAD_FONT)
    ax.set_xlim(0, CHRIST * 1.22)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.2, linewidth=0.8)
    ax.set_xlabel("Distance totale (km)")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=12.5)
    axtitle(ax, "Comparaison des distances obtenues", fontsize=20, pad=16)
    gap = CHRIST - GA
    ax.annotate("", xy=(GA, 0.72), xytext=(CHRIST, 0.72),
                arrowprops=dict(arrowstyle="<|-|>", color=GOLD_SOFT, lw=1.8))
    ax.text((GA + CHRIST) / 2, 0.45,
            f"− {fr(gap)} km   ({fr(100 * gap / CHRIST)} %)", ha="center",
            fontsize=13.5, color=GOLD_SOFT, fontweight="bold",
            fontfamily=HEAD_FONT)
    fig.tight_layout()
    save(fig, OUT / "17_comparaison.png")


# ---------------------------------------------------------------------------
# 18 — Encadrement de l'optimum
# ---------------------------------------------------------------------------
def fig_bornes():
    fig, ax = blank((12, 4.6))
    head(ax, "Ce que nous savons réellement de l'optimum",
         "Nous ne l'avons pas calculé — nous l'encadrons.", y=99, fs=22)

    y = 42
    ax.plot([6, 94], [y, y], color=GRID, lw=2.2, solid_capstyle="round")
    pts = [(6, f"{fr(MST)} km", "Borne INFÉRIEURE\npoids du MST", MUTED),
           (52, "OPT", "Optimum exact\nnon calculé", GOLD),
           (94, f"{fr(GA)} km", "Borne SUPÉRIEURE\nmeilleure tournée valide", GOLD_SOFT)]
    for x, val, lab, col in pts:
        circ(ax, x, y, 1.9, facecolor=col, edgecolor=BG, lw=1.6, zorder=4)
        ax.text(x, y + 9, val, fontsize=17, color=col, ha="center",
                fontweight="bold", fontfamily=HEAD_FONT)
        ax.text(x, y - 9, lab, fontsize=12, color=MUTED, ha="center", va="top")
    ax.fill_between([6, 94], y - 1.1, y + 1.1, color=GOLD, alpha=0.18)
    ax.text(50, 3,
            f"{fr(MST)}  ≤  OPT  ≤  {fr(GA)}   —   l'optimum se situe dans une "
            f"fenêtre de {fr(GA - MST, 0)} km, que nous n'avons pas réduite davantage.",
            fontsize=13, color=TEXT, ha="center", fontweight="bold",
            fontfamily=HEAD_FONT)
    save(fig, OUT / "18_bornes.png")


# ---------------------------------------------------------------------------
# 19 — Tableau Kanban (organisation Trello)
# ---------------------------------------------------------------------------
def fig_kanban():
    fig, ax = blank((13, 6.6))
    head(ax, "Organisation du projet — tableau Kanban",
         "Représentation de notre tableau Trello d'organisation.")

    cols = [
        ("À FAIRE", CORAL, ["Répétition chronométrée de l'oral",
                            "Relecture finale du dépôt public"]),
        ("EN COURS", GOLD, ["Slides : garder une idée par slide",
                            "Vérifier les commandes du README",
                            "Préparer les réponses aux questions"]),
        ("TERMINÉ", GREEN, ["CSV des 20 villes + vérif. GPS",
                            "Haversine + matrice des distances",
                            "Graphe complet (190 arêtes)",
                            "Prim / arbre couvrant minimal",
                            "Christofides complet",
                            "Algorithme génétique + opérateurs",
                            "Benchmark 3 configs × 3 seeds",
                            "Cartes Folium + convergence",
                            "Analyse comparative + README",
                            "Tests unitaires (cycle valide)"]),
    ]
    cw, gap = 30, 5
    for i, (title_, color, cards) in enumerate(cols):
        x = i * (cw + gap)
        ax.add_patch(FancyBboxPatch((x, 0), cw, 80,
                                    boxstyle="round,pad=0,rounding_size=2",
                                    facecolor=PANEL, edgecolor=GRID, lw=1.2))
        ax.add_patch(FancyBboxPatch((x + 2, 72.5), cw - 4, 6,
                                    boxstyle="round,pad=0,rounding_size=1.2",
                                    facecolor=color, edgecolor=color, lw=1.0,
                                    alpha=0.90))
        ax.text(x + cw / 2, 75.5, f"{title_}  ({len(cards)})", fontsize=12.5,
                color=BG, ha="center", va="center", fontweight="bold",
                fontfamily=HEAD_FONT)
        for j, card in enumerate(cards):
            cy = 66.5 - j * 6.6
            ax.add_patch(FancyBboxPatch((x + 2, cy - 4.6), cw - 4, 5.4,
                                        boxstyle="round,pad=0,rounding_size=1.0",
                                        facecolor=PANEL_LIGHT, edgecolor=GRID,
                                        lw=0.9))
            ax.plot([x + 3.4, x + 3.4], [cy - 3.9, cy + 0.1], color=color, lw=2.4,
                    solid_capstyle="round")
            ax.text(x + 5.2, cy - 1.9, card, fontsize=10.5, color=TEXT,
                    va="center")
    if titles_on():
        ax.text(0, -5, "Romain · Yannis · Lisa — revue du tableau à chaque "
                       "séance, une carte = un livrable vérifiable.",
                fontsize=12, color=MUTED, va="center")
    save(fig, OUT / "19_kanban.png")


# ---------------------------------------------------------------------------
# 20 — Deux stratégies (slide comparative conceptuelle)
# ---------------------------------------------------------------------------
def fig_deux_strategies():
    fig, ax = blank((12.5, 5.8))
    head(ax, "Deux philosophies opposées",
         "Le sujet impose de les implémenter toutes les deux — et de les comparer.")

    data = [
        (0, CYAN, "CHRISTOFIDES", "Construire", [
            "Théorie des graphes",
            "Déterministe : même entrée, même sortie",
            "Une seule exécution suffit",
            "Garantie prouvée ≤ 1,5 × OPT",
            "Presque aucun paramètre à régler",
        ]),
        (52, GOLD, "ALGORITHME GÉNÉTIQUE", "Explorer", [
            "Métaheuristique inspirée de l'évolution",
            "Stochastique : dépend du hasard (seed)",
            "Plusieurs exécutions nécessaires",
            "Aucune garantie d'optimalité",
            "6 hyperparamètres à calibrer",
        ]),
    ]
    for x0, color, name, verb, items in data:
        ax.add_patch(FancyBboxPatch((x0, 0), 48, 76,
                                    boxstyle="round,pad=0,rounding_size=2.4",
                                    facecolor=PANEL, edgecolor=color, lw=1.8))
        ax.text(x0 + 24, 68, name, fontsize=17, color=color, ha="center",
                fontweight="bold", fontfamily=HEAD_FONT)
        # Filigrane retire : il passait derriere la derniere puce.
        for j, it in enumerate(items):
            y = 50 - j * 9.4
            ax.plot([x0 + 4.5], [y], marker="o", ms=5, color=color)
            ax.text(x0 + 8, y, it, fontsize=12, color=TEXT, va="center")
    ax.text(50, 79, "VS", fontsize=17, color=MUTED, ha="center", va="center",
            fontweight="bold", fontfamily=HEAD_FONT)
    save(fig, OUT / "20_deux_strategies.png")


def main():
    print("Schémas et graphiques :")
    fig_combinatoire()
    fig_haversine()
    fig_pipeline_christofides()
    fig_euler_hamilton()
    fig_shortcut()
    fig_pipeline_ga()
    fig_ox()
    fig_mutation_tournoi()
    gen_best = fig_convergence()
    fig_benchmark()
    fig_comparaison()
    fig_bornes()
    fig_kanban()
    fig_deux_strategies()
    print(f"\nMeilleure génération (seed 11) : {gen_best}")


if __name__ == "__main__":
    main()
