from __future__ import annotations

from pathlib import Path

import folium
import matplotlib.pyplot as plt

from .core import City


def save_route_map(cities: list[City], route: list[int], output_path: str | Path, title: str) -> None:
    center = [sum(c.latitude for c in cities) / len(cities), sum(c.longitude for c in cities) / len(cities)]
    m = folium.Map(location=center, zoom_start=6, tiles="CartoDB positron")

    for order, idx in enumerate(route[:-1], start=1):
        city = cities[idx]
        folium.CircleMarker(
            [city.latitude, city.longitude],
            radius=6,
            tooltip=f"{order}. {city.name}",
            popup=f"{order}. {city.name}",
            fill=True,
        ).add_to(m)

    points = [[cities[idx].latitude, cities[idx].longitude] for idx in route]
    folium.PolyLine(points, weight=4, opacity=0.8, tooltip=title).add_to(m)
    m.get_root().html.add_child(folium.Element(f"<h3 style='position:fixed;top:10px;left:50px;z-index:9999;background:white;padding:8px'>{title}</h3>"))
    m.save(str(output_path))


def save_route_png(cities: list[City], route: list[int], output_path: str | Path, title: str) -> None:
    xs = [cities[i].longitude for i in route]
    ys = [cities[i].latitude for i in route]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(xs, ys, marker="o", linewidth=1.8)
    for step, idx in enumerate(route[:-1], start=1):
        city = cities[idx]
        ax.annotate(f"{step}. {city.name}", (city.longitude, city.latitude), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def save_ga_history(history: list[float], output_path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(range(1, len(history) + 1), history)
    ax.set_title("Convergence de l'algorithme génétique")
    ax.set_xlabel("Génération")
    ax.set_ylabel("Meilleure distance (km)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
