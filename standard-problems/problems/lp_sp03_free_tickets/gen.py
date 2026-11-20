#!/usr/bin/env python3
"""Testcase generator for lp_sp03_free_tickets.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 K = 0; cases 3-5 N <= 500; cases 6-10 N = 5,000, M = 1.5 * 10^4.
Case 6 has N (K + 1) = 5.5 * 10^4 states, so the O((N K)^2) heap-less Dijkstra
must time out there. Vertex 1 and vertex N keep their numbers when the other
vertices are shuffled. Most graphs are "banded" (roads only join cities whose
hidden positions are close), so every route needs hundreds of rides and K free
tickets cannot make the trip free; a random graph would have a 0 answer.
"""

import random
import sys
from pathlib import Path

MAX_N = 5_000
MAX_M = 15_000
MAX_K = 10
MAX_W = 10**6


def random_tree(rng: random.Random, lo: int, hi: int, wmax: int):
    return [(v, rng.randint(lo, v - 1), rng.randint(1, wmax)) for v in range(lo + 1, hi + 1)]


def random_edges(rng: random.Random, lo: int, hi: int, count: int, weight):
    edges = []
    while len(edges) < count:
        u, v = rng.randint(lo, hi), rng.randint(lo, hi)
        if u != v:
            edges.append((u, v, weight()))
    return edges


def connected(rng: random.Random, n: int, m: int, wmax: int):
    return random_tree(rng, 1, n, wmax) + random_edges(rng, 1, n, m - (n - 1), lambda: rng.randint(1, wmax))


def banded(rng: random.Random, n: int, m: int, band: int, weight):
    """A connected graph whose roads only join positions at most band apart."""
    edges = [(v, rng.randint(max(1, v - band), v - 1), weight()) for v in range(2, n + 1)]
    while len(edges) < m:
        u = rng.randint(1, n - 1)
        edges.append((u, rng.randint(u + 1, min(n, u + band)), weight()))
    return edges


def spiky_weight(rng: random.Random):
    return lambda: rng.randint(1, 20) if rng.random() < 0.7 else rng.randint(MAX_W - 1000, MAX_W)


def path(n: int):
    return [(v, v + 1, MAX_W - (v % 7)) for v in range(1, n)]


def trap(rng: random.Random, n: int, m: int, k: int):
    """A route of exactly k + 1 huge rides from 1 to n beside a long cheap path
    and random medium roads: with k tickets the huge route costs one ride."""
    hubs = rng.sample(range(2, n), k)
    route = [1] + hubs + [n]
    edges = [(a, b, MAX_W) for a, b in zip(route, route[1:])]
    order = [1] + [v for v in rng.sample(range(2, n), n - 2) if v not in hubs] + [n]
    edges += [(a, b, rng.randint(1, 300)) for a, b in zip(order, order[1:])]
    while len(edges) < m:                                   # medium roads between close positions
        i = rng.randint(0, len(order) - 2)
        j = rng.randint(i + 1, min(len(order) - 1, i + 15))
        edges.append((order[i], order[j], rng.randint(10_000, MAX_W)))
    return edges


def relabel(rng: random.Random, n: int, edges):
    middle = list(range(2, n))
    rng.shuffle(middle)
    perm = [1] + middle + [n] if n > 1 else [1]
    mapped = [(perm[u - 1], perm[v - 1], w) if rng.random() < 0.5 else (perm[v - 1], perm[u - 1], w)
              for u, v, w in edges]
    rng.shuffle(mapped)
    return mapped


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append((1, 0, []))                                                      # N = 1: already there
    rng = random.Random(20261120 + 3101)
    plans.append((1000, 0, connected(rng, 1000, 3000, MAX_W)))
    plans.append((7, 2, [(1, 2, 4), (2, 3, 4), (3, 1, 1), (4, 5, 9), (5, 6, 2), (6, 7, 3), (4, 7, 1)]))  # N unreachable
    rng = random.Random(20261120 + 3102)
    plans.append((500, 3, banded(rng, 500, 2000, 10, lambda: rng.randint(1, MAX_W))))
    rng = random.Random(20261120 + 3103)
    plans.append((500, 10, banded(rng, 500, 2000, 8, spiky_weight(rng))))
    rng = random.Random(20261120 + 3104)
    plans.append((MAX_N, MAX_K, banded(rng, MAX_N, MAX_M, 20, lambda: rng.randint(1, MAX_W))))  # slow.cpp must TLE here
    rng = random.Random(20261120 + 3108)
    plans.append((MAX_N, 1, banded(rng, MAX_N, MAX_M, 25, spiky_weight(rng))))
    rng = random.Random(20261120 + 3106)
    plans.append((MAX_N, 5, trap(rng, MAX_N, MAX_M, 5)))
    rng = random.Random(20261120 + 3107)
    half = MAX_N // 2                                                             # 1 in one half, N in the other
    weight = lambda: rng.randint(1, MAX_W)
    plans.append((MAX_N, MAX_K, banded(rng, half, MAX_M - (MAX_N - half - 1), 12, weight)
                  + [(u + half, v + half, w) for u, v, w in banded(rng, MAX_N - half, MAX_N - half - 1, 12, weight)]))
    plans.append((MAX_N, MAX_K, path(MAX_N) + [(v, v + 2, MAX_W) for v in range(1, MAX_N - 1)]))  # answer > 2^31
    for index, (n, k, edges) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 3200 + index)
        edges = relabel(rng, n, edges)
        assert 1 <= n <= MAX_N and 0 <= len(edges) <= MAX_M and 0 <= k <= MAX_K
        assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W for u, v, w in edges)
        lines = [f"{n} {len(edges)} {k}"] + [f"{u} {v} {w}" for u, v, w in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
