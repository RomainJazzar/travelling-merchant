from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import networkx as nx

EARTH_RADIUS_KM = 6371.0088


@dataclass(frozen=True)
class City:
    name: str
    latitude: float
    longitude: float


def load_cities(csv_path: str | Path) -> list[City]:
    """Load cities from the project's CSV file."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV introuvable: {path}")

    cities: list[City] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"Ville", "Latitude", "Longitude"}
        if set(reader.fieldnames or []) != expected:
            raise ValueError(
                f"Colonnes attendues {sorted(expected)}, reçues {reader.fieldnames}"
            )
        for row in reader:
            cities.append(
                City(
                    name=row["Ville"].strip(),
                    latitude=float(row["Latitude"]),
                    longitude=float(row["Longitude"]),
                )
            )
    if len(cities) < 3:
        raise ValueError("Le TSP nécessite au moins 3 villes.")
    return cities


def haversine_km(a: City, b: City) -> float:
    """Great-circle distance between two cities, in kilometres."""
    lat1, lon1 = math.radians(a.latitude), math.radians(a.longitude)
    lat2, lon2 = math.radians(b.latitude), math.radians(b.longitude)
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(h))


def distance_matrix(cities: list[City]) -> list[list[float]]:
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine_km(cities[i], cities[j])
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix


def build_complete_graph(cities: list[City], matrix: list[list[float]] | None = None) -> nx.Graph:
    """Build the complete weighted graph used by the metric TSP."""
    matrix = matrix or distance_matrix(cities)
    graph = nx.Graph()
    for i, city in enumerate(cities):
        graph.add_node(i, name=city.name, latitude=city.latitude, longitude=city.longitude)
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            graph.add_edge(i, j, weight=matrix[i][j])
    return graph


def route_distance(route: Iterable[int], matrix: list[list[float]]) -> float:
    route_list = list(route)
    if len(route_list) < 2:
        return 0.0
    return sum(matrix[route_list[i]][route_list[i + 1]] for i in range(len(route_list) - 1))


def route_names(route: Iterable[int], cities: list[City]) -> list[str]:
    return [cities[i].name for i in route]
