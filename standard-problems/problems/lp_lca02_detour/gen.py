#!/usr/bin/env python3
"""Testcase generator for lp_lca02_detour.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q <= 5*10^4.
Labels are shuffled. Shapes: path, "Y" (two long arms: climbing one step at a
time costs O(N) per query), star, random, caterpillar, binary. Queries mix
random triples, c on the path a-b (answer 0), c = a or c = b, a = b. Case 7 (a
path, N = 5*10^4, Q = 4*10^4) makes the naive climb time out. Lengths up to 10^6, so
answers need 64 bits.
"""

import random
import sys
from pathlib import Path

MAX_N = 50_000
MAX_Q = 50_000
MAX_W = 10**6


def shape_parents(rng: random.Random, n: int, shape: str) -> list[int]:
    parent = [-1] * n
    for i in range(1, n):
        if shape == "random":
            parent[i] = rng.randrange(i)
        elif shape == "path":
            parent[i] = i - 1
        elif shape == "star":
            parent[i] = 0
        elif shape == "binary":
            parent[i] = (i - 1) // 2
        elif shape == "y":
            parent[i] = max(0, i - 2)
        elif shape == "caterpillar":
            spine = max(1, n // 4)
            parent[i] = i - 1 if i < spine else rng.randrange(spine)
        else:
            raise ValueError(shape)
    return parent


def make_case(rng: random.Random, n: int, q: int, shape: str):
    parent = shape_parents(rng, n, shape)
    label = list(range(1, n + 1))
    rng.shuffle(label)
    par = [0] * (n + 1)  # labelled parent, to pick vertices on a path
    for i in range(1, n):
        par[label[i]] = label[parent[i]]
    edges = []
    for i in range(1, n):
        u, v, w = label[i], label[parent[i]], rng.randint(1, MAX_W)
        edges.append((u, v, w) if rng.random() < 0.5 else (v, u, w))
    rng.shuffle(edges)
    queries = []
    for _ in range(q):
        kind = rng.random()
        a, b = rng.randint(1, n), rng.randint(1, n)
        if kind < 0.25:  # c on the climb from a towards the root: often on the path a-b
            c = a
            for _ in range(rng.randint(0, 40)):
                if par[c] == 0:
                    break
                c = par[c]
        elif kind < 0.3:
            c = rng.choice((a, b))
        elif kind < 0.33:
            b, c = a, rng.randint(1, n)
        else:
            c = rng.randint(1, n)
        queries.append((a, b, c))
    return edges, queries


def check(n: int, q: int, edges, queries) -> None:
    assert 1 <= n <= MAX_N and 1 <= q <= MAX_Q and len(edges) == n - 1 and len(queries) == q
    root = list(range(n + 1))

    def find(x: int) -> int:
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W
        x, y = find(u), find(v)
        assert x != y, "cycle"
        root[x] = y
    assert all(1 <= x <= n for t in queries for x in t)


def main() -> None:
    out = Path(sys.argv[1])
    plans = [  # (n, q, shape)
        (1, 2, "path"), (8, 20, "random"), (1000, 1000, "path"),
        (5000, 5000, "y"), (5000, 5000, "random"), (5000, 5000, "star"),
        (50_000, 40_000, "path"), (40_000, 20_000, "binary"), (30_000, 20_000, "caterpillar"),
        (30_000, 20_000, "y"),
    ]
    for index, (n, q, shape) in enumerate(plans, start=1):
        rng = random.Random(20261241 + index)
        edges, queries = make_case(rng, n, q, shape)
        check(n, q, edges, queries)
        lines = [f"{n} {q}"] + [f"{u} {v} {w}" for u, v, w in edges] + [f"{a} {b} {c}" for a, b, c in queries]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
