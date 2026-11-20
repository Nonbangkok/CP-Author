#!/usr/bin/env python3
"""Testcase generator for lp_sp01_delivery_times.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7, 9, 10 N = 5 * 10^4, case 8 M = 10^5.
Case 7 has N = 5 * 10^4, so the O(N^2) Dijkstra without a heap must time out
there. Long paths with weights near 10^6 push distances past 2^31 (cases 4, 10).
"""

import random
import sys
from pathlib import Path

MAX_N = 50_000
MAX_M = 100_000
MAX_W = 10**6


def relabel(rng: random.Random, n: int, s: int, edges: list[tuple[int, int, int]]):
    """Shuffle vertex numbers and edge order so structure is not visible in labels."""
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    mapped = [(perm[u - 1], perm[v - 1], w) if rng.random() < 0.5 else (perm[v - 1], perm[u - 1], w)
              for u, v, w in edges]
    rng.shuffle(mapped)
    return perm[s - 1], mapped


def random_tree(rng: random.Random, lo: int, hi: int, wmax: int) -> list[tuple[int, int, int]]:
    """A random tree on vertices lo..hi."""
    return [(v, rng.randint(lo, v - 1), rng.randint(1, wmax)) for v in range(lo + 1, hi + 1)]


def random_edges(rng: random.Random, lo: int, hi: int, count: int, wmax: int) -> list[tuple[int, int, int]]:
    edges = []
    while len(edges) < count:
        u, v = rng.randint(lo, hi), rng.randint(lo, hi)
        if u != v:
            edges.append((u, v, rng.randint(1, wmax)))
    return edges


def connected(rng: random.Random, n: int, m: int, wmax: int) -> list[tuple[int, int, int]]:
    return random_tree(rng, 1, n, wmax) + random_edges(rng, 1, n, m - (n - 1), wmax)


def path(n: int, wmax: int) -> list[tuple[int, int, int]]:
    return [(v, v + 1, wmax - (v % 3)) for v in range(1, n)]


def components(rng: random.Random, n: int, parts: int, extra: int, wmax: int) -> list[tuple[int, int, int]]:
    """parts pieces; each piece is a tree plus some extra edges; a few isolated vertices."""
    cuts = sorted(rng.sample(range(2, n), parts - 1))
    bounds = [1] + cuts + [n + 1]
    edges = []
    for lo, hi in zip(bounds, bounds[1:]):
        hi -= 1
        if hi - lo >= 3:  # leave tiny pieces as isolated vertices
            edges += random_tree(rng, lo, hi, wmax)
            edges += random_edges(rng, lo, hi, extra * (hi - lo + 1) // n, wmax)
    return edges


def layered(rng: random.Random, n: int, m: int) -> list[tuple[int, int, int]]:
    """Cheap long detours beside expensive shortcuts: many tentative distances get
    improved later, so the heap holds plenty of stale entries (lazy deletion)."""
    edges = [(v, v + 1, rng.randint(1, 10)) for v in range(1, n)]
    while len(edges) < m:
        u = rng.randint(1, n - 1)
        v = rng.randint(u + 1, min(n, u + 500))
        edges.append((u, v, rng.randint(2000, 9999)))
    return edges


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append((1, 1, []))                                                    # one city, no road
    plans.append((6, 3, [(3, 1, 5), (1, 2, 2), (3, 2, 9), (2, 3, 6), (1, 4, 1), (4, 2, 1)]))  # 5, 6 unreachable; multi-edge
    rng = random.Random(20261120 + 1101)
    plans.append((1000, 17, connected(rng, 1000, 2000, 1000)))
    plans.append((5000, 1, path(5000, MAX_W)))                                  # long path: > 2^31
    rng = random.Random(20261120 + 1102)
    plans.append((5000, 2500, connected(rng, 5000, 10000, MAX_W)))
    rng = random.Random(20261120 + 1103)
    plans.append((5000, 4999, components(rng, 5000, 40, 4000, 50)))
    rng = random.Random(20261120 + 1104)
    plans.append((MAX_N, 777, connected(rng, MAX_N, MAX_N, MAX_W)))             # slow.cpp must TLE here
    rng = random.Random(20261120 + 1106)
    plans.append((5000, 1, layered(rng, 5000, MAX_M)))                          # M = 10^5, many stale heap entries
    rng = random.Random(20261120 + 1105)
    plans.append((MAX_N, 1, components(rng, MAX_N, 300, 0, MAX_W)))
    plans.append((MAX_N, MAX_N, path(MAX_N, MAX_W)))                            # distances near 5 * 10^10
    for index, (n, s, edges) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 1200 + index)
        s, edges = relabel(rng, n, s, edges)
        assert 1 <= n <= MAX_N and 0 <= len(edges) <= MAX_M and 1 <= s <= n
        assert all(1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W for u, v, w in edges)
        lines = [f"{n} {len(edges)} {s}"] + [f"{u} {v} {w}" for u, v, w in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
