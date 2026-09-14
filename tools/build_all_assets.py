"""Génère les deux jeux d'illustrations du dossier de soutenance.

    python tools/build_all_assets.py

- FINAL_SOUTENANCE/assets/        : figures avec leur titre interne
                                    (guide PDF, consultation isolée) ;
- FINAL_SOUTENANCE/assets/slide/  : les mêmes sans titre, pour le PowerPoint
                                    (les slides portent déjà leur titre).

Toutes les valeurs proviennent de l'exécution réelle du projet.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import theme


def _run(out_dir: Path, with_titles: bool) -> None:
    theme.set_titles(with_titles)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Les modules lisent OUT au moment de l'appel : on le réécrit avant.
    from tools import build_assets_charts as charts
    from tools import build_assets_combined as combined
    from tools import build_assets_maps as maps

    maps.OUT = out_dir
    charts.OUT = out_dir
    combined.OUT = out_dir

    maps.main()
    charts.main()
    combined.main()


def main() -> None:
    base = ROOT / "FINAL_SOUTENANCE" / "assets"
    print("=== Jeu 1/2 : figures avec titre (guide) ===")
    _run(base, with_titles=True)
    print("\n=== Jeu 2/2 : figures sans titre (PowerPoint) ===")
    _run(base / "slide", with_titles=False)
    print("\nTerminé.")


if __name__ == "__main__":
    main()
