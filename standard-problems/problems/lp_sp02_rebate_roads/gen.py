#!/usr/bin/env python3
"""Testcase generator for lp_sp02_rebate_roads.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 50; cases 4-6 N <= 100; cases 7-10 N = 200, M and Q up to 2 * 10^4.

No negative cycle by construction: every weight is c + p[u] - p[v] with c >= 0
(around any cycle the p terms cancel), or the graph is acyclic. gen.py also
checks it with Floyd-Warshall (no d[i][i] < 0). Case 7 is built against
Bellman-Ford per query: the cheapest routes follow a 200-vertex chain whose
edges are listed backwards, so each round advances one step.
"""

import random
import sys
from pathlib import Path

MAX_N = 200
MAX_M = 20_000
MAX_Q = 20_000
MAX_W = 10**6
HALF = MAX_W // 2


def potential_edges(rng: random.Random, n: int, m: int, p: list[int]) -> list[tuple[int, int, int]]:
    edges = []
    while len(edges) < m:
        u, v = rng.randint(1, n), rng.randint(1, n)
        if u != v:
            edges.append((u, v, rng.randint(0, HALF) + p[u] - p[v]))
    return edges


def potentials(rng: random.Random, n: int) -> list[int]:
    return [0] + [rng.randint(0, HALF) for _ in range(n)]


def dag_edges(rng: random.Random, n: int, m: int, lo: int, hi: int) -> list[tuple[int, int, int]]:
    """Edges only from a smaller to a larger number: no cycle at all (relabelled later)."""
    edges = []
    while len(edges) < m:
        u, v = sorted(rng.sample(range(1, n + 1), 2))
        edges.append((u, v, rng.randint(lo, hi)))
    return edges


def queries(rng: random.Random, n: int, q: int) -> list[tuple[int, int]]:
    return [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]


def chain_case(rng: random.Random) -> tuple[int, list, list]:
    """Chain 1 -> 2 -> ... -> N with reduced cost 0 (negative weights), listed last
    and backwards; other edges have reduced cost >= 1000, so routes follow the chain."""
    n = MAX_N
    p = [0] + sorted(rng.randint(0, HALF) for _ in range(n))     # increasing: chain weights <= 0
    chain = [(v, v + 1, p[v] - p[v + 1]) for v in range(1, n)]
    extra = []
    while len(extra) < MAX_M - len(chain):
        u, v = rng.randint(1, n), rng.randint(1, n)
        if u != v:
            extra.append((u, v, rng.randint(1000, HALF) + p[u] - p[v]))
    qs = [(rng.randint(1, 20), rng.randint(n - 20, n)) for _ in range(MAX_Q)]
    return n, extra + chain[::-1], qs


def relabel(rng: random.Random, n: int, edges, qs, shuffle_edges: bool = True):
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    edges = [(perm[u - 1], perm[v - 1], w) for u, v, w in edges]
    if shuffle_edges:
        rng.shuffle(edges)
    return edges, [(perm[a - 1], perm[b - 1]) for a, b in qs]


def no_negative_cycle(n: int, edges) -> bool:
    inf = float("inf")
    d = [[inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u - 1][v - 1] = min(d[u - 1][v - 1], w)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik != inf:
                d[i] = [x if x <= dik + y else dik + y for x, y in zip(d[i], dk)]
    return all(d[i][i] >= 0 for i in range(n))


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append((1, [], [(1, 1)], True))
    small = [(1, 2, 3), (2, 1, -1), (2, 3, -4), (1, 3, 7), (3, 4, 2), (3, 4, -2), (4, 2, 6)]  # 5 isolated
    plans.append((5, small, [(a, b) for a in range(1, 6) for b in range(1, 6)], True))
    rng = random.Random(20261120 + 2101)
    plans.append((50, potential_edges(rng, 50, 500, potentials(rng, 50)), queries(rng, 50, 100), True))
    rng = random.Random(20261120 + 2102)
    plans.append((100, dag_edges(rng, 100, 1500, -MAX_W, MAX_W), queries(rng, 100, 500), True))
    rng = random.Random(20261120 + 2103)
    plans.append((100, potential_edges(rng, 100, 2000, potentials(rng, 100)), queries(rng, 100, 500), True))
    rng = random.Random(20261120 + 2104)
    p = potentials(rng, 100)
    left = [(u, v, w) for u, v, w in potential_edges(rng, 50, 900, p)]
    right = [(u + 50, v + 50, rng.randint(0, HALF) + p[u + 50] - p[v + 50]) for u, v, _ in potential_edges(rng, 50, 900, p)]
    links = [(rng.randint(1, 50), rng.randint(51, 100), rng.randint(-MAX_W, MAX_W)) for _ in range(200)]  # one way only
    plans.append((100, left + right + links, queries(rng, 100, 500), True))
    rng = random.Random(20261120 + 2105)
    n, edges, qs = chain_case(rng)
    plans.append((n, edges, qs, False))                                        # slow.cpp must TLE here
    rng = random.Random(20261120 + 2106)
    qs = queries(rng, MAX_N, MAX_Q - MAX_N) + [(v, v) for v in range(1, MAX_N + 1)]
    plans.append((MAX_N, potential_edges(rng, MAX_N, MAX_M, potentials(rng, MAX_N)), qs, True))
    rng = random.Random(20261120 + 2107)
    p = potentials(rng, MAX_N)
    sparse = [(u + 40 * g, v + 40 * g, w) for g in range(5)
              for u, v, w in potential_edges(rng, 40, 60, [0] + p[1 + 40 * g:41 + 40 * g])]
    plans.append((MAX_N, sparse, queries(rng, MAX_N, MAX_Q), True))
    rng = random.Random(20261120 + 2108)
    plans.append((MAX_N, dag_edges(rng, MAX_N, MAX_M, -MAX_W, -1), queries(rng, MAX_N, MAX_Q), True))
    for index, (n, edges, qs, shuffle_edges) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 2200 + index)
        edges, qs = relabel(rng, n, edges, qs, shuffle_edges)
        assert 1 <= n <= MAX_N and 0 <= len(edges) <= MAX_M and 1 <= len(qs) <= MAX_Q
        assert all(1 <= u <= n and 1 <= v <= n and u != v and -MAX_W <= w <= MAX_W for u, v, w in edges)
        assert all(1 <= a <= n and 1 <= b <= n for a, b in qs)
        assert no_negative_cycle(n, edges)
        lines = [f"{n} {len(edges)} {len(qs)}"] + [f"{u} {v} {w}" for u, v, w in edges] + [f"{a} {b}" for a, b in qs]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
