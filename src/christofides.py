from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import networkx as nx

from .core import City, build_complete_graph, distance_matrix, route_distance


@dataclass
class ChristofidesResult:
    route: list[int]
    distance_km: float
    mst_weight_km: float
    matching_weight_km: float
    odd_vertices: list[int]


def prim_mst(graph: nx.Graph, start: int = 0) -> list[tuple[int, int, float]]:
    """Compute a minimum spanning tree with Prim's algorithm."""
    if start not in graph:
        raise ValueError("Sommet de départ absent du graphe.")

    import heapq

    visited = {start}
    heap: list[tuple[float, int, int]] = []
    for neighbor, attrs in graph[start].items():
        heapq.heappush(heap, (float(attrs["weight"]), start, neighbor))

    edges: list[tuple[int, int, float]] = []
    while heap and len(visited) < graph.number_of_nodes():
        weight, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        edges.append((u, v, weight))
        for nxt, attrs in graph[v].items():
            if nxt not in visited:
                heapq.heappush(heap, (float(attrs["weight"]), v, nxt))

    if len(visited) != graph.number_of_nodes():
        raise ValueError("Le graphe n'est pas connexe.")
    return edges


def _hierholzer_multigraph(adjacency: dict[int, list[tuple[int, int]]], start: int) -> list[int]:
    """Return an Eulerian circuit using Hierholzer's algorithm.

    adjacency contains (neighbor, edge_id) pairs so parallel edges are supported.
    """
    local = {node: list(edges) for node, edges in adjacency.items()}
    used_edges: set[int] = set()
    stack = [start]
    circuit: list[int] = []

    while stack:
        v = stack[-1]
        while local[v] and local[v][-1][1] in used_edges:
            local[v].pop()
        if not local[v]:
            circuit.append(stack.pop())
            continue
        u, edge_id = local[v].pop()
        if edge_id in used_edges:
            continue
        used_edges.add(edge_id)
        stack.append(u)

    circuit.reverse()
    return circuit


def christofides(cities: list[City], start: int = 0) -> ChristofidesResult:
    """Christofides 3/2-approximation for the metric TSP."""
    matrix = distance_matrix(cities)
    graph = build_complete_graph(cities, matrix)

    # 1) Minimum spanning tree (implemented with Prim)
    mst_edges = prim_mst(graph, start=start)
    mst_weight = sum(weight for _, _, weight in mst_edges)

    degree = [0] * len(cities)
    for u, v, _ in mst_edges:
        degree[u] += 1
        degree[v] += 1
    odd_vertices = [v for v, deg in enumerate(degree) if deg % 2 == 1]

    # 2) Minimum-weight perfect matching on odd-degree vertices
    odd_graph = nx.Graph()
    odd_graph.add_nodes_from(odd_vertices)
    for idx, u in enumerate(odd_vertices):
        for v in odd_vertices[idx + 1 :]:
            odd_graph.add_edge(u, v, weight=matrix[u][v])

    matching = nx.algorithms.matching.min_weight_matching(odd_graph, weight="weight")
    matching_edges = [(int(u), int(v), matrix[int(u)][int(v)]) for u, v in matching]
    matching_weight = sum(weight for _, _, weight in matching_edges)

    # 3) Union MST + matching -> connected Eulerian multigraph
    adjacency: dict[int, list[tuple[int, int]]] = defaultdict(list)
    all_edges = mst_edges + matching_edges
    for edge_id, (u, v, _) in enumerate(all_edges):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))

    # 4) Eulerian tour, then shortcut repeated vertices (metric property)
    euler = _hierholzer_multigraph(adjacency, start)
    seen: set[int] = set()
    hamiltonian: list[int] = []
    for vertex in euler:
        if vertex not in seen:
            hamiltonian.append(vertex)
            seen.add(vertex)
    hamiltonian.append(hamiltonian[0])

    return ChristofidesResult(
        route=hamiltonian,
        distance_km=route_distance(hamiltonian, matrix),
        mst_weight_km=mst_weight,
        matching_weight_km=matching_weight,
        odd_vertices=odd_vertices,
    )
