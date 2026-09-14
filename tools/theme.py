"""Charte graphique partagée par tous les visuels de la soutenance.

Palette sombre « data science / voyage » : bleu nuit, or, cyan.
Toutes les figures sont générées avec cette charte pour rester cohérentes
avec le PowerPoint final.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager

# --- Couleurs -------------------------------------------------------------
BG = "#0B1220"          # fond principal (identique au PPTX)
PANEL = "#16223A"       # panneaux / terre
PANEL_LIGHT = "#1E2E4D"
GRID = "#25334F"
TEXT = "#F2F6FC"
MUTED = "#9DB0CE"
GOLD = "#E8B45A"
GOLD_SOFT = "#F5D08A"
CYAN = "#4FD1E8"
CYAN_SOFT = "#8FE6F5"
GREEN = "#5BD6A8"
CORAL = "#F2765B"
VIOLET = "#A88BE8"

# --- Polices --------------------------------------------------------------
_available = {f.name for f in font_manager.fontManager.ttflist}
def _pick(*candidates: str) -> str:
    for name in candidates:
        if name in _available:
            return name
    return "DejaVu Sans"


# Segoe UI possède de vraies graisses (contrairement à Bahnschrift, variable)
# et couvre les glyphes typographiques utilisés dans les figures.
HEAD_FONT = _pick("Segoe UI", "Calibri", "Arial")
BODY_FONT = _pick("Segoe UI", "Calibri", "Arial")


# Quand SHOW_TITLES vaut False, les figures sont generees sans leur titre
# interne (les slides du PowerPoint portent deja le leur).
SHOW_TITLES = True


def set_titles(flag: bool) -> None:
    global SHOW_TITLES
    SHOW_TITLES = flag


def titles_on() -> bool:
    return SHOW_TITLES


def apply_theme() -> None:
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "text.color": TEXT,
        "axes.labelcolor": MUTED,
        "axes.edgecolor": GRID,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "grid.color": GRID,
        "font.family": BODY_FONT,
        "font.size": 13,
        "axes.titlesize": 19,
        "axes.titleweight": "bold",
        "figure.dpi": 200,
        "savefig.dpi": 200,
        "legend.frameon": False,
    })


def title(ax, text: str, sub: str | None = None) -> None:
    ax.set_title(text, color=TEXT, fontfamily=HEAD_FONT, fontsize=20,
                 fontweight="bold", pad=18 if sub else 12, loc="left")
    if sub:
        ax.text(0, 1.015, sub, transform=ax.transAxes, color=MUTED,
                fontsize=12, va="bottom", ha="left")


def _autocrop(path, margin: int = 26) -> None:
    """Recadre l'image sur son contenu réel.

    `bbox_inches="tight"` conserve la boîte complète des axes, donc le bandeau
    laissé libre par un titre supprimé reste dans l'image. On recadre sur les
    pixels qui diffèrent du fond.
    """
    from PIL import Image, ImageChops

    with Image.open(path) as im:
        rgb = im.convert("RGB")
        background = Image.new("RGB", rgb.size, BG)
        bbox = ImageChops.difference(rgb, background).getbbox()
        if not bbox:
            return
        x0, y0, x1, y1 = bbox
        x0, y0 = max(x0 - margin, 0), max(y0 - margin, 0)
        x1, y1 = min(x1 + margin, rgb.size[0]), min(y1 + margin, rgb.size[1])
        rgb.crop((x0, y0, x1, y1)).save(path)


def save(fig, path, pad: float = 0.35) -> None:
    fig.savefig(path, bbox_inches="tight", pad_inches=pad, facecolor=BG)
    plt.close(fig)
    if not SHOW_TITLES:
        _autocrop(path)
    print(f"  ✓ {path}")


# --- Contour simplifié de la France métropolitaine ------------------------
# Suite de points (longitude, latitude) suivant le littoral et les frontières.
# Usage purement illustratif : sert de fond de carte, pas de calcul.
FRANCE_OUTLINE = [
    (2.37, 51.03), (1.85, 50.95), (1.60, 50.72), (1.55, 50.20), (1.08, 49.93),
    (0.10, 49.51), (0.25, 49.42), (-0.37, 49.34), (-1.15, 49.40), (-1.26, 49.68),
    (-1.62, 49.68), (-1.94, 49.72), (-1.79, 49.38), (-1.60, 48.84), (-1.51, 48.63),
    (-2.02, 48.65), (-3.05, 48.78), (-3.44, 48.82), (-3.98, 48.73), (-4.77, 48.36),
    (-4.55, 48.09), (-4.74, 48.04), (-4.37, 47.80), (-3.37, 47.72), (-3.12, 47.48),
    (-2.76, 47.52), (-2.20, 47.26), (-2.23, 46.98), (-1.78, 46.49), (-1.15, 46.15),
    (-1.03, 45.62), (-1.06, 45.28), (-1.25, 44.65), (-1.25, 44.15), (-1.43, 43.65),
    (-1.56, 43.48), (-1.78, 43.36), (-1.24, 43.05), (-0.70, 42.95), (0.02, 42.72),
    (0.60, 42.70), (1.53, 42.50), (2.30, 42.52), (3.03, 42.44), (3.05, 42.80),
    (3.15, 43.16), (3.70, 43.38), (4.55, 43.38), (5.35, 43.29), (5.93, 43.09),
    (6.64, 43.26), (7.02, 43.53), (7.53, 43.78), (6.85, 44.90), (6.87, 45.83),
    (6.12, 46.15), (6.05, 46.42), (6.36, 46.90), (7.55, 47.57), (8.22, 48.62),
    (7.97, 49.03), (7.07, 49.11), (6.35, 49.47), (5.77, 49.55), (4.83, 50.15),
    (4.05, 50.30), (3.23, 50.78), (2.37, 51.03),
]

CORSICA_OUTLINE = [
    (8.57, 42.72), (9.35, 42.98), (9.45, 42.72), (9.55, 42.30), (9.40, 41.85),
    (9.25, 41.37), (8.80, 41.55), (8.55, 41.95), (8.70, 42.35), (8.57, 42.72),
]

# Facteur de projection équirectangulaire (latitude moyenne de la France).
import math
LAT0 = 46.5
LON_SCALE = math.cos(math.radians(LAT0))


def draw_france(ax, corsica: bool = True, alpha: float = 1.0) -> None:
    """Dessine le fond de carte France et fige l'aspect géographique."""
    xs = [p[0] * LON_SCALE for p in FRANCE_OUTLINE]
    ys = [p[1] for p in FRANCE_OUTLINE]
    ax.fill(xs, ys, color=PANEL, zorder=0, alpha=alpha)
    ax.plot(xs, ys, color=GRID, linewidth=1.4, zorder=1, alpha=alpha)
    if corsica:
        cxs = [p[0] * LON_SCALE for p in CORSICA_OUTLINE]
        cys = [p[1] for p in CORSICA_OUTLINE]
        ax.fill(cxs, cys, color=PANEL, zorder=0, alpha=alpha)
        ax.plot(cxs, cys, color=GRID, linewidth=1.2, zorder=1, alpha=alpha)
    ax.set_aspect("equal")
    ax.set_xlim(-5.6 * LON_SCALE, 9.9 * LON_SCALE)
    ax.set_ylim(41.0, 53.2)   # bande haute réservée aux titres
    ax.axis("off")


def px(lon: float) -> float:
    """Projette une longitude dans le repère de la carte."""
    return lon * LON_SCALE


def glow_line(ax, xs, ys, color, width=2.6, zorder=3, glow=True):
    """Trace une ligne avec un halo pour un rendu « premium »."""
    if glow:
        ax.plot(xs, ys, color=color, linewidth=width * 4.0, alpha=0.10,
                solid_capstyle="round", zorder=zorder - 1)
        ax.plot(xs, ys, color=color, linewidth=width * 2.2, alpha=0.16,
                solid_capstyle="round", zorder=zorder - 1)
    ax.plot(xs, ys, color=color, linewidth=width, solid_capstyle="round",
            zorder=zorder)
