#!/usr/bin/env python3
"""Testcase generator for lp_mst02_village_wells.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 10, M <= 20; cases 3-5 N <= 3,000, M <= 6,000; cases 6-10
N <= 5 * 10^4, M <= 10^5. Case 6 has N = 5 * 10^4, where Prim without a heap
(O(N^2)) must time out. Covers N = 1, M = 0 (every village digs), wells cheaper
than every pipe, one cheap well feeding a whole cheap pipe network, pipe graphs
in many pieces, parallel pipes, and totals above 2^31.
"""

import random
import sys
from pathlib import Path

MAX_N = 50_000
MAX_M = 100_000
MAX_W = 10**6


def relabel(rng, n, costs, edges):
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    new_costs = [0] * n
    for old, c in enumerate(costs, start=1):
        new_costs[perm[old - 1] - 1] = c
    mapped = [(perm[u - 1], perm[v - 1], w) if rng.random() < 0.5 else (perm[v - 1], perm[u - 1], w)
              for u, v, w in edges]
    rng.shuffle(mapped)
    return new_costs, mapped


def random_tree(rng, lo, hi, wlo, whi):
    return [(v, rng.randint(lo, v - 1), rng.randint(wlo, whi)) for v in range(lo + 1, hi + 1)]


def random_edges(rng, lo, hi, count, wlo, whi):
    edges = []
    while len(edges) < count:
        u, v = rng.randint(lo, hi), rng.randint(lo, hi)
        if u != v:
            edges.append((u, v, rng.randint(wlo, whi)))
    return edges


def pieces(rng, n, parts, m, wlo, whi):
    """parts groups of villages, pipes only inside a group."""
    cuts = sorted(rng.sample(range(2, n + 1), parts - 1))
    bounds = [1] + cuts + [n + 1]
    ranges = [(lo, hi - 1) for lo, hi in zip(bounds, bounds[1:])]
    edges = []
    for lo, hi in ranges:
        edges += random_tree(rng, lo, hi, wlo, whi)
    big = [r for r in ranges if r[1] > r[0]]
    while len(edges) < m:
        lo, hi = rng.choice(big)
        edges += random_edges(rng, lo, hi, 1, wlo, whi)
    return edges


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append(([7], []))                                                      # one village
    plans.append(([8, 3, 9, 9, 2, 7, 10, 4, 6, 5],
                  [(1, 2, 2), (2, 1, 1), (2, 3, 4), (3, 4, 1), (4, 1, 6), (5, 6, 3), (6, 7, 2),
                   (7, 5, 1), (8, 9, 7), (9, 10, 8), (3, 7, 5), (1, 9, 9), (2, 3, 3)]))
    rng = random.Random(20261120 + 4101)
    n = 3000
    plans.append(([rng.randint(1, MAX_W) for _ in range(n)],
                  random_tree(rng, 1, n, 1, MAX_W) + random_edges(rng, 1, n, 6000 - (n - 1), 1, MAX_W)))
    rng = random.Random(20261120 + 4102)
    plans.append(([rng.randint(10**5, MAX_W) for _ in range(n)], pieces(rng, n, 25, 6000, 1, 10**5)))
    rng = random.Random(20261120 + 4103)
    plans.append(([rng.randint(MAX_W - 100, MAX_W) for _ in range(n)], []))     # M = 0: every village digs, > 2^31
    n = MAX_N
    rng = random.Random(20261120 + 4104)
    plans.append(([rng.randint(1, MAX_W) for _ in range(n)],
                  random_tree(rng, 1, n, 1, MAX_W) + random_edges(rng, 1, n, 10_000, 1, MAX_W)))  # slow.cpp TLEs
    rng = random.Random(20261120 + 4105)
    costs = [rng.randint(MAX_W - 1000, MAX_W) for _ in range(n)]
    costs[rng.randrange(n)] = 1                                                   # one cheap well, cheap pipes
    plans.append((costs, random_tree(rng, 1, n, 1, 1000) + random_edges(rng, 1, n, 15_000, 1, 1000)))
    rng = random.Random(20261120 + 4106)
    plans.append(([rng.randint(1, 100) for _ in range(n)],
                  random_edges(rng, 1, n, 30_000, 101, MAX_W)))                  # every well beats every pipe
    rng = random.Random(20261120 + 4107)
    plans.append(([rng.randint(1, MAX_W) for _ in range(n)], pieces(rng, n, 800, 45_000, 1, MAX_W)))
    rng = random.Random(20261120 + 4108)
    plans.append(([rng.randint(1, MAX_W) for _ in range(30_000)],
                  random_edges(rng, 1, 30_000, 40_000, 1, MAX_W // 2)))
    for index, (costs, edges) in enumerate(plans, start=1):
        n = len(costs)
        rng = random.Random(20261120 + 4200 + index)
        costs, edges = relabel(rng, n, costs, edges)
        m = len(edges)
        assert 1 <= n <= MAX_N and 0 <= m <= MAX_M
        if index <= 2:
            assert n <= 10 and m <= 20
        elif index <= 5:
            assert n <= 3000 and m <= 6000
        assert all(1 <= c <= MAX_W for c in costs)
        assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W for u, v, w in edges)
        lines = [f"{n} {m}", " ".join(map(str, costs))] + [f"{u} {v} {w}" for u, v, w in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
