#!/usr/bin/env python3
"""Testcase generator for lp_mst03_candidate_roads.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 100, M <= 300; cases 4-6 N <= 2,000, M <= 4,000; cases 7-10
N <= 3 * 10^4, M <= 6 * 10^4. Case 7 has spread-out weights, where one BFS per
road over the cheaper roads must time out. Every graph is connected. Covers
N = 2, parallel roads with equal and unequal weights, few distinct weights
(large groups of ties, where answering inside a group while uniting it gives
wrong NOs), all weights equal (everything YES), and a grid with weights 1..2.
"""

import random
import sys
from pathlib import Path

MAX_N = 30_000
MAX_M = 60_000
MAX_W = 10**9


def relabel(rng, n, edges):
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    mapped = [(perm[u - 1], perm[v - 1], w) if rng.random() < 0.5 else (perm[v - 1], perm[u - 1], w)
              for u, v, w in edges]
    rng.shuffle(mapped)
    return mapped


def random_tree(rng, n, wlo, whi):
    return [(v, rng.randint(1, v - 1), rng.randint(wlo, whi)) for v in range(2, n + 1)]


def random_edges(rng, n, count, wlo, whi):
    edges = []
    while len(edges) < count:
        a, b = rng.randint(1, n), rng.randint(1, n)
        if a != b:
            edges.append((a, b, rng.randint(wlo, whi)))
    return edges


def connected(rng, n, m, wlo, whi):
    return random_tree(rng, n, wlo, whi) + random_edges(rng, n, m - (n - 1), wlo, whi)


def grid(rng, rows, cols, whi):
    def vid(r, c):
        return r * cols + c + 1
    edges = []
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                edges.append((vid(r, c), vid(r, c + 1), rng.randint(1, whi)))
            if r + 1 < rows:
                edges.append((vid(r, c), vid(r + 1, c), rng.randint(1, whi)))
    return edges


def doubled_tree(rng, n, extra):
    """A tree where every road has an equal-cost twin (all YES), plus pricier extras (all NO)."""
    tree = random_tree(rng, n, 1, 10**6)
    edges = tree + [(b, a, w) for a, b, w in tree]
    edges += random_edges(rng, n, extra, 10**6 + 1, MAX_W)
    return edges


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append((2, [(1, 2, MAX_W)]))
    plans.append((7, [(1, 2, 3), (2, 3, 3), (3, 1, 3), (3, 4, 1), (4, 5, 2), (5, 3, 2), (4, 3, 1),
                      (5, 6, 4), (6, 7, 4), (7, 5, 5), (1, 7, 4), (2, 6, 9), (6, 7, 4)]))
    rng = random.Random(20261120 + 5101)
    plans.append((100, connected(rng, 100, 300, 1, 5)))
    rng = random.Random(20261120 + 5102)
    plans.append((2000, connected(rng, 2000, 4000, 1, MAX_W)))
    rng = random.Random(20261120 + 5103)
    plans.append((2000, connected(rng, 2000, 4000, 1, 3)))
    rng = random.Random(20261120 + 5104)
    plans.append((2000, connected(rng, 2000, 4000, 777, 777)))                  # all equal: all YES
    rng = random.Random(20261120 + 5105)
    plans.append((MAX_N, connected(rng, MAX_N, MAX_M, 1, MAX_W)))              # slow.cpp must TLE here
    rng = random.Random(20261120 + 5106)
    plans.append((MAX_N, connected(rng, MAX_N, MAX_M, 1, 20)))
    rng = random.Random(20261120 + 5107)
    plans.append((150 * 200, grid(rng, 150, 200, 2)))
    rng = random.Random(20261120 + 5108)
    plans.append((20_000, doubled_tree(rng, 20_000, 20_000)))
    for index, (n, edges) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 5200 + index)
        edges = relabel(rng, n, edges)
        m = len(edges)
        assert 2 <= n <= MAX_N and n - 1 <= m <= MAX_M
        if index <= 3:
            assert n <= 100 and m <= 300
        elif index <= 6:
            assert n <= 2000 and m <= 4000
        assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W for u, v, w in edges)
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        parts = n
        for u, v, _ in edges:
            a, b = find(u), find(v)
            if a != b:
                parent[a] = b
                parts -= 1
        assert parts == 1, f"case {index} not connected"
        lines = [f"{n} {m}"] + [f"{u} {v} {w}" for u, v, w in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
