#!/usr/bin/env python3
"""Testcase generator for lp_mat02_patrol_routes.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 5, L <= 10, Q <= 10; cases 3-5 L <= 500, Q <= 10 (the
step-by-step count still passes); cases 6-10 L up to 10^18 and Q = 100, the
first of them with every L >= 10^17 so stepping must time out, and 100
separate O(N^3 log L) matrix powers are too slow as well. Covers parallel
corridors and self-loops, M = 0, a directed cycle (periodic answers), a DAG
(no long walks), two disconnected parts, L = 0 and s = t, s != t.
"""

import random
import sys
from pathlib import Path

NMAX, MMAX, QMAX, LMAX = 50, 5000, 100, 10**18


def random_edges(rng, n, m):
    return [(rng.randint(1, n), rng.randint(1, n)) for _ in range(m)]


def random_queries(rng, n, q, lo, hi, extra=()):
    queries = list(extra)
    while len(queries) < q:
        queries.append((rng.randint(1, n), rng.randint(1, n), rng.randint(lo, hi)))
    return queries[:q]


def case(index, rng):
    if index == 1:  # one room, two parallel self-loops, plus L = 0
        edges = [(1, 1), (1, 1)]
        return 1, edges, [(1, 1, l) for l in (0, 1, 2, 5, 10)]
    if index == 2:
        n = 5
        return n, random_edges(rng, n, 12) + [(2, 3), (2, 3)], random_queries(rng, n, 10, 0, 10, [(4, 4, 0), (1, 5, 0)])
    if index == 3:
        n = 50
        return n, random_edges(rng, n, MMAX), random_queries(rng, n, 10, 450, 500, [(1, 50, 500)])
    if index == 4:  # directed cycle 1 -> 2 -> ... -> 50 -> 1
        n = 50
        edges = [(i, i % n + 1) for i in range(1, n + 1)]
        return n, edges, random_queries(rng, n, 10, 0, 500, [(1, 1, 500), (7, 7, 450), (3, 10, 457)])
    if index == 5:  # two separate parts 1..20 and 21..30, both dense with loops
        n = 30
        edges = [(rng.randint(1, 20), rng.randint(1, 20)) for _ in range(600)]
        edges += [(rng.randint(21, 30), rng.randint(21, 30)) for _ in range(300)]
        return n, edges, random_queries(rng, n, 10, 490, 500, [(1, 25, 500), (22, 3, 499), (21, 21, 500)])
    if index == 6:  # first case of the last subtask: every L is huge
        n = 50
        return n, random_edges(rng, n, MMAX), random_queries(rng, n, QMAX, 10**17, LMAX, [(1, 1, LMAX), (50, 1, LMAX)])
    if index == 7:  # complete digraph with self-loops, every pair twice: A = all 2
        n = 50
        edges = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1)] * 2
        rng.shuffle(edges)
        extra = [(1, 2, 2**59 - 1), (3, 3, LMAX - 1), (5, 9, 1), (8, 8, 0)]
        return n, edges, random_queries(rng, n, QMAX, 0, LMAX, extra)
    if index == 8:  # DAG: only u < v, so walks longer than 49 steps do not exist
        n = 50
        edges = []
        while len(edges) < 3000:
            u, v = sorted(rng.sample(range(1, n + 1), 2))
            edges.append((u, v))
        extra = [(1, 50, l) for l in range(1, 50)] + [(1, 50, LMAX), (2, 2, 0)]
        return n, edges, random_queries(rng, n, QMAX, 0, 60, extra)
    if index == 9:  # cycle with a few chords and one loop
        n = 50
        edges = [(i, i % n + 1) for i in range(1, n + 1)]
        edges += [(rng.randint(1, n), rng.randint(1, n)) for _ in range(8)] + [(17, 17)]
        return n, edges, random_queries(rng, n, QMAX, 0, LMAX)
    # index 10: n = 37, no corridors at all except queries with L = 0 make sense
    n = 37
    extra = [(i, i, 0) for i in range(1, 11)] + [(1, 2, 0), (5, 5, LMAX)]
    return n, [], random_queries(rng, n, QMAX, 0, LMAX, extra)


def main() -> None:
    out = Path(sys.argv[1])
    for index in range(1, 11):
        rng = random.Random(20261121 + index)
        n, edges, queries = case(index, rng)
        assert 1 <= n <= NMAX and 0 <= len(edges) <= MMAX and 1 <= len(queries) <= QMAX
        for u, v in edges:
            assert 1 <= u <= n and 1 <= v <= n
        for s, t, l in queries:
            assert 1 <= s <= n and 1 <= t <= n and 0 <= l <= LMAX
        if index <= 2:
            assert n <= 5 and len(queries) <= 10 and max(l for _, _, l in queries) <= 10
        elif index <= 5:
            assert len(queries) <= 10 and max(l for _, _, l in queries) <= 500
        if index == 6:
            assert len(queries) == QMAX and min(l for _, _, l in queries) >= 10**17
        lines = [f"{n} {len(edges)} {len(queries)}"]
        lines += [f"{u} {v}" for u, v in edges]
        lines += [f"{s} {t} {l}" for s, t, l in queries]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
