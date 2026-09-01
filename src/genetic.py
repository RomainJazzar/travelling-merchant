from __future__ import annotations

import random
from dataclasses import dataclass
from statistics import mean, pstdev

from .core import City, distance_matrix, route_distance


@dataclass(frozen=True)
class GAConfig:
    population_size: int = 300
    generations: int = 1200
    tournament_size: int = 5
    crossover_rate: float = 0.95
    mutation_rate: float = 0.22
    elite_size: int = 8
    seed: int = 42


@dataclass
class GAResult:
    route: list[int]
    distance_km: float
    history: list[float]
    config: GAConfig


def _closed_distance(individual: list[int], matrix: list[list[float]]) -> float:
    # City 0 is omitted from the chromosome and fixed as the cycle anchor.
    route = [0] + individual + [0]
    return route_distance(route, matrix)


def _tournament(population: list[list[int]], distances: list[float], rng: random.Random, k: int) -> list[int]:
    indices = rng.sample(range(len(population)), k=min(k, len(population)))
    best = min(indices, key=lambda idx: distances[idx])
    return population[best]


def _ordered_crossover(a: list[int], b: list[int], rng: random.Random) -> tuple[list[int], list[int]]:
    n = len(a)
    left, right = sorted(rng.sample(range(n), 2))

    def make_child(p1: list[int], p2: list[int]) -> list[int]:
        child = [-1] * n
        child[left:right] = p1[left:right]
        remaining = [gene for gene in p2 if gene not in child]
        it = iter(remaining)
        for i in list(range(0, left)) + list(range(right, n)):
            child[i] = next(it)
        return child

    return make_child(a, b), make_child(b, a)


def _mutate(individual: list[int], rng: random.Random) -> None:
    """Mix swap and inversion mutations to preserve permutation validity."""
    if len(individual) < 2:
        return
    i, j = sorted(rng.sample(range(len(individual)), 2))
    if rng.random() < 0.5:
        individual[i], individual[j] = individual[j], individual[i]
    else:
        individual[i : j + 1] = reversed(individual[i : j + 1])


def genetic_tsp(cities: list[City], config: GAConfig = GAConfig()) -> GAResult:
    if config.population_size < 4:
        raise ValueError("population_size doit être >= 4")
    if config.elite_size >= config.population_size:
        raise ValueError("elite_size doit être inférieur à population_size")

    rng = random.Random(config.seed)
    matrix = distance_matrix(cities)
    genes = list(range(1, len(cities)))  # Fix Paris (index 0) as anchor.

    population: list[list[int]] = []
    for _ in range(config.population_size):
        chromosome = genes.copy()
        rng.shuffle(chromosome)
        population.append(chromosome)

    best_individual: list[int] | None = None
    best_distance = float("inf")
    history: list[float] = []

    for _ in range(config.generations):
        distances = [_closed_distance(ind, matrix) for ind in population]
        ranked = sorted(range(len(population)), key=lambda idx: distances[idx])

        if distances[ranked[0]] < best_distance:
            best_distance = distances[ranked[0]]
            best_individual = population[ranked[0]].copy()
        history.append(best_distance)

        new_population = [population[idx].copy() for idx in ranked[: config.elite_size]]
        while len(new_population) < config.population_size:
            parent1 = _tournament(population, distances, rng, config.tournament_size)
            parent2 = _tournament(population, distances, rng, config.tournament_size)

            if rng.random() < config.crossover_rate:
                child1, child2 = _ordered_crossover(parent1, parent2, rng)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if rng.random() < config.mutation_rate:
                _mutate(child1, rng)
            if rng.random() < config.mutation_rate:
                _mutate(child2, rng)

            new_population.append(child1)
            if len(new_population) < config.population_size:
                new_population.append(child2)
        population = new_population

    assert best_individual is not None
    route = [0] + best_individual + [0]
    return GAResult(route=route, distance_km=best_distance, history=history, config=config)


def benchmark_configs(cities: list[City], configs: dict[str, GAConfig], seeds: list[int]) -> list[dict[str, float | int | str]]:
    """Run each configuration across multiple seeds to assess robustness."""
    rows: list[dict[str, float | int | str]] = []
    for name, base in configs.items():
        values: list[float] = []
        for seed in seeds:
            config = GAConfig(
                population_size=base.population_size,
                generations=base.generations,
                tournament_size=base.tournament_size,
                crossover_rate=base.crossover_rate,
                mutation_rate=base.mutation_rate,
                elite_size=base.elite_size,
                seed=seed,
            )
            result = genetic_tsp(cities, config)
            values.append(result.distance_km)
        rows.append(
            {
                "configuration": name,
                "runs": len(values),
                "best_km": min(values),
                "mean_km": mean(values),
                "std_km": pstdev(values),
                "worst_km": max(values),
            }
        )
    return rows
