#!/usr/bin/env python3
"""Testcase generator for lp_gph01_friend_groups.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, M <= 1,000; cases 4-6 N, M <= 5,000; cases 7-10 N, M <= 10^5.
Edges are undirected, 1-indexed, no self-loops, no repeated pairs. Covers
N = 1, M = 0 (everyone alone), one big group, many small groups, a star, and
a shuffled path (case 7): there every friendship merges two groups, so the
relabel-everyone approach does ~N^2 work and must time out.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
MAX_M = 100_000


def shuffled(rng: random.Random, n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Rename vertices randomly, flip edge ends and shuffle the order."""
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    out = []
    for u, v in edges:
        a, b = perm[u - 1], perm[v - 1]
        if rng.random() < 0.5:
            a, b = b, a
        out.append((a, b))
    rng.shuffle(out)
    return out


def path(n: int) -> list[tuple[int, int]]:
    return [(i, i + 1) for i in range(1, n)]


def random_edges(rng: random.Random, n: int, m: int) -> list[tuple[int, int]]:
    seen: set[tuple[int, int]] = set()
    edges = []
    while len(edges) < m:
        u, v = rng.randint(1, n), rng.randint(1, n)
        if u == v:
            continue
        key = (min(u, v), max(u, v))
        if key in seen:
            continue
        seen.add(key)
        edges.append((u, v))
    return edges


def groups_of(rng: random.Random, sizes: list[int], extra_per_group: int) -> tuple[int, list[tuple[int, int]]]:
    """Disjoint groups: a random tree inside each plus a few extra edges."""
    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    start = 1
    for size in sizes:
        members = list(range(start, start + size))
        for i in range(1, size):
            u, v = members[i], members[rng.randrange(i)]
            seen.add((min(u, v), max(u, v)))
            edges.append((u, v))
        for _ in range(extra_per_group if size >= 3 else 0):
            u, v = rng.sample(members, 2)
            key = (min(u, v), max(u, v))
            if key not in seen:
                seen.add(key)
                edges.append((u, v))
        start += size
    return start - 1, edges


def validate(n: int, edges: list[tuple[int, int]], cap_n: int, cap_m: int) -> None:
    assert 1 <= n <= cap_n <= MAX_N
    assert 0 <= len(edges) <= cap_m <= MAX_M
    seen = set()
    for u, v in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        key = (min(u, v), max(u, v))
        assert key not in seen
        seen.add(key)


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[int, list[tuple[int, int]], int, int]] = []

    # --- subtask 1: N, M <= 1,000
    cases.append((1, [], 1000, 1000))                                  # one person, no friends
    rng = random.Random(20261201 + 1)
    cases.append((1000, shuffled(rng, 1000, random_edges(rng, 1000, 400)), 1000, 1000))
    rng = random.Random(20261201 + 2)
    n, e = groups_of(rng, [rng.randint(1, 25) for _ in range(40)], 3)
    cases.append((n, shuffled(rng, n, e), 1000, 1000))

    # --- subtask 2: N, M <= 5,000
    cases.append((5000, [], 5000, 5000))                               # M = 0: 5000 groups of 1
    rng = random.Random(20261201 + 4)
    cases.append((5000, shuffled(rng, 5000, path(5000)), 5000, 5000))  # one long chain
    rng = random.Random(20261201 + 5)
    cases.append((5000, shuffled(rng, 5000, random_edges(rng, 5000, 5000)), 5000, 5000))

    # --- subtask 3: N, M <= 10^5
    rng = random.Random(20261201 + 7)
    cases.append((MAX_N, shuffled(rng, MAX_N, path(MAX_N)), MAX_N, MAX_M))   # slow.cpp must TLE here
    rng = random.Random(20261201 + 8)
    star = [(1, v) for v in range(2, 80001)]                           # a star of 80,000 plus loners
    cases.append((MAX_N, shuffled(rng, MAX_N, star), MAX_N, MAX_M))
    rng = random.Random(20261201 + 9)
    sizes = [rng.randint(1, 200) for _ in range(850)]
    n, e = groups_of(rng, sizes, 8)
    assert n <= MAX_N
    cases.append((n, shuffled(rng, n, e), MAX_N, MAX_M))
    rng = random.Random(20261201 + 10)
    cases.append((MAX_N, shuffled(rng, MAX_N, random_edges(rng, MAX_N, 60000)), MAX_N, MAX_M))

    assert len(cases) == 10
    for index, (n, edges, cap_n, cap_m) in enumerate(cases, start=1):
        validate(n, edges, cap_n, cap_m)
        lines = [f"{n} {len(edges)}"] + [f"{u} {v}" for u, v in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
