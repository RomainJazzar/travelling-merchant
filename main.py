from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict
from pathlib import Path

from src.christofides import christofides
from src.core import load_cities, route_names
from src.genetic import GAConfig, benchmark_configs, genetic_tsp
from src.visualization import save_ga_history, save_route_map, save_route_png

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "villes_france_lat_long.csv"
RESULTS = ROOT / "results"


def run_all() -> dict:
    RESULTS.mkdir(exist_ok=True)
    cities = load_cities(DATA)

    start = time.perf_counter()
    christ = christofides(cities)
    christ_time = time.perf_counter() - start

    configs = {
        "rapide": GAConfig(population_size=80, generations=220, tournament_size=4, mutation_rate=0.18, elite_size=4),
        "equilibree": GAConfig(population_size=160, generations=520, tournament_size=5, mutation_rate=0.22, elite_size=6),
        "exploratoire": GAConfig(population_size=240, generations=800, tournament_size=6, mutation_rate=0.30, elite_size=8),
    }

    benchmark_start = time.perf_counter()
    benchmark = benchmark_configs(cities, configs, seeds=[11, 22, 33])
    benchmark_time = time.perf_counter() - benchmark_start
    best_config_name = min(benchmark, key=lambda row: (float(row["mean_km"]), float(row["std_km"]), float(row["best_km"])))['configuration']
    chosen = configs[str(best_config_name)]

    ga_runs = []
    ga_total_start = time.perf_counter()
    for seed in [11, 22, 33]:
        config = GAConfig(**{**asdict(chosen), "seed": seed})
        t0 = time.perf_counter()
        result = genetic_tsp(cities, config)
        elapsed = time.perf_counter() - t0
        ga_runs.append((result, elapsed))
    ga_total_time = time.perf_counter() - ga_total_start
    ga, ga_best_time = min(ga_runs, key=lambda item: item[0].distance_km)

    save_route_map(cities, christ.route, RESULTS / "route_christofides.html", "Itinéraire Christofides")
    save_route_map(cities, ga.route, RESULTS / "route_genetique.html", "Itinéraire algorithme génétique")
    save_route_png(cities, christ.route, RESULTS / "route_christofides.png", f"Christofides — {christ.distance_km:.1f} km")
    save_route_png(cities, ga.route, RESULTS / "route_genetique.png", f"Algorithme génétique — {ga.distance_km:.1f} km")
    save_ga_history(ga.history, RESULTS / "convergence_genetique.png")

    with (RESULTS / "benchmark_ga.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(benchmark[0].keys()))
        writer.writeheader()
        writer.writerows(benchmark)

    summary = {
        "cities": len(cities),
        "christofides": {
            "distance_km": christ.distance_km,
            "execution_seconds": christ_time,
            "mst_weight_km": christ.mst_weight_km,
            "matching_weight_km": christ.matching_weight_km,
            "odd_vertices_count": len(christ.odd_vertices),
            "route": route_names(christ.route, cities),
        },
        "genetic": {
            "distance_km": ga.distance_km,
            "best_single_run_seconds": ga_best_time,
            "total_three_runs_seconds": ga_total_time,
            "chosen_configuration": best_config_name,
            "configuration": asdict(ga.config),
            "route": route_names(ga.route, cities),
        },
        "benchmark_seconds": benchmark_time,
        "benchmark": benchmark,
        "difference_ga_minus_christofides_km": ga.distance_km - christ.distance_km,
        "difference_percent": 100 * (ga.distance_km - christ.distance_km) / christ.distance_km,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Projet TSP — Le marchand ambulant")
    parser.add_argument("--json", action="store_true", help="Afficher le résumé JSON")
    args = parser.parse_args()
    summary = run_all()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Christofides : {summary['christofides']['distance_km']:.2f} km")
        print(f"Génétique    : {summary['genetic']['distance_km']:.2f} km")
        print("Résultats générés dans ./results")


if __name__ == "__main__":
    main()
