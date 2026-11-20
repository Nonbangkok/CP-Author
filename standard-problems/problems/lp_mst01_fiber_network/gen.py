#!/usr/bin/env python3
"""Testcase generator for lp_mst01_fiber_network.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000, M <= 3,000; cases 4-6 N <= 3,000, M <= 6,000; cases 7-10
N <= 5 * 10^4, M <= 10^5. Case 7 is a big connected random graph where the
naive "DFS the forest before every edge" Kruskal must time out. Covers N = 1,
parallel edges, disconnected graphs (answer -1, incl. one isolated building),
many equal costs, and a path of expensive edges whose total exceeds 2^31.
"""

import random
import sys
from pathlib import Path

MAX_N = 50_000
MAX_M = 100_000
MAX_W = 10**6


def relabel(rng: random.Random, n: int, edges):
    """Shuffle vertex numbers, edge directions and edge order."""
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    mapped = [(perm[u - 1], perm[v - 1], w) if rng.random() < 0.5 else (perm[v - 1], perm[u - 1], w)
              for u, v, w in edges]
    rng.shuffle(mapped)
    return mapped


def random_tree(rng, lo, hi, wlo, whi):
    return [(v, rng.randint(lo, v - 1), rng.randint(wlo, whi)) for v in range(lo + 1, hi + 1)]


def random_edges(rng, lo, hi, count, wlo, whi):
    edges = []
    while len(edges) < count:
        u, v = rng.randint(lo, hi), rng.randint(lo, hi)
        if u != v:
            edges.append((u, v, rng.randint(wlo, whi)))
    return edges


def connected(rng, n, m, wlo, whi):
    return random_tree(rng, 1, n, wlo, whi) + random_edges(rng, 1, n, m - (n - 1), wlo, whi)


def pieces(rng, n, parts, m, whi):
    """parts connected pieces (random trees + extra edges inside pieces)."""
    cuts = sorted(rng.sample(range(2, n + 1), parts - 1))
    bounds = [1] + cuts + [n + 1]
    edges = []
    ranges = []
    for lo, hi in zip(bounds, bounds[1:]):
        edges += random_tree(rng, lo, hi - 1, 1, whi)
        ranges.append((lo, hi - 1))
    while len(edges) < m:
        lo, hi = rng.choice(ranges)
        if hi > lo:
            edges += random_edges(rng, lo, hi, 1, 1, whi)
    return edges


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append((1, []))                                                       # one building
    plans.append((8, [(1, 2, 5), (2, 1, 3), (2, 3, 4), (3, 4, 4), (4, 1, 2), (5, 6, 9), (6, 7, 1),
                      (7, 8, 8), (8, 5, 1), (5, 7, 2), (3, 6, 10), (1, 8, 10), (3, 6, 7)]))  # parallel edges
    rng = random.Random(20261120 + 3101)
    plans.append((1000, connected(rng, 1000, 3000, 1, MAX_W)))
    rng = random.Random(20261120 + 3102)
    plans.append((3000, pieces(rng, 3000, 3, 6000, MAX_W)))                     # -1
    rng = random.Random(20261120 + 3103)
    plans.append((3000, connected(rng, 3000, 6000, 1, 3)))                      # many ties
    plans.append((3000, [(v, v + 1, MAX_W - v % 7) for v in range(1, 3000)]))   # total > 2^31
    rng = random.Random(20261120 + 3104)
    plans.append((MAX_N, connected(rng, MAX_N, 60_000, 1, MAX_W)))              # slow.cpp must TLE here
    rng = random.Random(20261120 + 3105)
    plans.append((MAX_N, connected(rng, MAX_N, MAX_M, 1, MAX_W)))
    rng = random.Random(20261120 + 3106)
    edges = connected(rng, MAX_N - 1, 60_000, 1, 1000)                           # building N isolated: -1
    plans.append((MAX_N, edges))
    rng = random.Random(20261120 + 3107)
    plans.append((MAX_N, random_tree(rng, 1, MAX_N, MAX_W - 1000, MAX_W)))       # a tree: take everything
    for index, (n, edges) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 3200 + index)
        edges = relabel(rng, n, edges)
        m = len(edges)
        assert 1 <= n <= MAX_N and 0 <= m <= MAX_M
        if index <= 3:
            assert n <= 1000 and m <= 3000
        elif index <= 6:
            assert n <= 3000 and m <= 6000
        assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W for u, v, w in edges)
        lines = [f"{n} {m}"] + [f"{u} {v} {w}" for u, v, w in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
