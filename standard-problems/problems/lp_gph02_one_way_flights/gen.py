#!/usr/bin/env python3
"""Testcase generator for lp_gph02_one_way_flights.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, M, Q <= 1,000; cases 4-6 Q <= 10; cases 7-10 no extra limit.
Flights are directed, 1-indexed, a != b, no repeated ordered pair (a -> b and
b -> a may both exist). Covers N = 1, city 1 with no outgoing flight, flights
that only point back towards city 1, a long chain, and (case 7) a big
reachable part plus cities that can only fly INTO it: every query there is
unreachable, so a fresh BFS per query explores ~10^5 edges each time and must
time out.
"""

import random
import sys
from pathlib import Path

MAX_N = 50_000
MAX_M = 100_000
MAX_Q = 50_000

Edge = tuple[int, int]


def relabel(rng: random.Random, n: int, edges: list[Edge], queries: list[int]) -> tuple[list[Edge], list[int]]:
    """Rename cities 2..n randomly (city 1 stays the start) and shuffle edges."""
    rest = list(range(2, n + 1))
    rng.shuffle(rest)
    perm = [0, 1] + rest
    out = [(perm[a], perm[b]) for a, b in edges]
    rng.shuffle(out)
    return out, [perm[t] for t in queries]


def add_random(rng: random.Random, edges: list[Edge], seen: set[Edge], count: int,
               sources: list[int], targets: list[int]) -> None:
    added = 0
    while added < count:
        a, b = rng.choice(sources), rng.choice(targets)
        if a == b or (a, b) in seen:
            continue
        seen.add((a, b))
        edges.append((a, b))
        added += 1


def random_graph(rng: random.Random, n: int, m: int) -> list[Edge]:
    edges: list[Edge] = []
    every = list(range(1, n + 1))
    add_random(rng, edges, set(), m, every, every)
    return edges


def chain(n: int) -> list[Edge]:
    return [(i, i + 1) for i in range(1, n)]


def trap(rng: random.Random, n: int, reach: int, inner: int, inward: int) -> list[Edge]:
    """Cities 1..reach are reachable from 1 (a random out-tree plus extra edges
    among them); cities reach+1..n only have flights INTO 1..reach."""
    edges: list[Edge] = []
    seen: set[Edge] = set()
    for v in range(2, reach + 1):
        a = rng.randint(1, v - 1)
        edges.append((a, v))
        seen.add((a, v))
    inside = list(range(1, reach + 1))
    add_random(rng, edges, seen, inner, inside, inside)
    add_random(rng, edges, seen, inward, list(range(reach + 1, n + 1)), inside)
    return edges


def layers(rng: random.Random, n: int, width: int, back: int) -> list[Edge]:
    """Layer k -> layer k+1 forward flights, plus flights that only go back."""
    edges: list[Edge] = []
    seen: set[Edge] = set()
    layer = [list(range(s, min(s + width, n + 1))) for s in range(2, n + 1, width)]
    for v in layer[0]:
        edges.append((1, v))
        seen.add((1, v))
    for prev, cur in zip(layer, layer[1:]):
        for v in cur:
            a = rng.choice(prev)
            edges.append((a, v))
            seen.add((a, v))
    every = list(range(2, n + 1))
    added = 0
    while added < back:                                  # backwards (and to city 1): never shortens
        a = rng.choice(every)
        la = (a - 2) // width
        b = 1 if la == 0 else rng.choice(layer[rng.randrange(la)])
        if (a, b) in seen:
            continue
        seen.add((a, b))
        edges.append((a, b))
        added += 1
    return edges


def validate(n: int, edges: list[Edge], queries: list[int], caps: tuple[int, int, int]) -> None:
    cap_n, cap_m, cap_q = caps
    assert 1 <= n <= cap_n <= MAX_N
    assert 0 <= len(edges) <= cap_m <= MAX_M
    assert 1 <= len(queries) <= cap_q <= MAX_Q
    assert len(set(edges)) == len(edges)
    for a, b in edges:
        assert 1 <= a <= n and 1 <= b <= n and a != b
    for t in queries:
        assert 1 <= t <= n


def main() -> None:
    out = Path(sys.argv[1])
    small = (1000, 1000, 1000)
    tiny_q = (MAX_N, MAX_M, 10)
    full = (MAX_N, MAX_M, MAX_Q)
    cases = []

    # --- subtask 1: N, M, Q <= 1,000
    cases.append((1, [], [1], small))                                       # only city 1: answer 0
    rng = random.Random(20261202 + 2)
    n = 1000
    cases.append((n, *relabel(rng, n, random_graph(rng, n, 1000), [rng.randint(1, n) for _ in range(1000)]), small))
    rng = random.Random(20261202 + 3)
    n = 600
    cases.append((n, *relabel(rng, n, layers(rng, n, 37, 400), list(range(1, n + 1))), small))

    # --- subtask 2: Q <= 10
    rng = random.Random(20261202 + 4)
    n = MAX_N
    cases.append((n, *relabel(rng, n, chain(n), [n, n - 1, 1, 2, n // 2, 7, 3, n - 2, 40000, 12345]), tiny_q))
    rng = random.Random(20261202 + 5)
    n = 20000
    edges = [(b, a) for a, b in chain(n)]                                   # every flight points towards 1
    cases.append((n, *relabel(rng, n, edges, [1, 2, n, 100, 5000, 9, 19999, 3, 4, 11]), tiny_q))
    rng = random.Random(20261202 + 6)
    n = 30000
    cases.append((n, *relabel(rng, n, random_graph(rng, n, 33000), [rng.randint(1, n) for _ in range(10)]), tiny_q))

    # --- subtask 3: N <= 5 * 10^4, M <= 10^5, Q <= 5 * 10^4
    rng = random.Random(20261202 + 7)
    n, reach = MAX_N, 40000
    queries = [rng.randint(reach + 1, n) for _ in range(30000)]            # all unreachable
    cases.append((n, *relabel(rng, n, trap(rng, n, reach, 30000, 15000), queries), full))  # slow.cpp must TLE here
    rng = random.Random(20261202 + 8)
    n = MAX_N
    cases.append((n, *relabel(rng, n, chain(n), [rng.randint(1, n) for _ in range(30000)] + [n] * 20000), full))
    rng = random.Random(20261202 + 9)
    n = MAX_N
    cases.append((n, *relabel(rng, n, random_graph(rng, n, 80000), [rng.randint(1, n) for _ in range(20000)]), full))
    rng = random.Random(20261202 + 10)
    n = MAX_N
    cases.append((n, *relabel(rng, n, layers(rng, n, 50, 30000), [rng.randint(1, n) for _ in range(20000)]), full))

    assert len(cases) == 10
    for index, (n, edges, queries, caps) in enumerate(cases, start=1):
        validate(n, edges, queries, caps)
        lines = [f"{n} {len(edges)} {len(queries)}"] + [f"{a} {b}" for a, b in edges] + [" ".join(map(str, queries))]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
