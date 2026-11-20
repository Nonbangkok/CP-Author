#!/usr/bin/env python3
"""Testcase generator for lp_tr02_longest_trail.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000 (N = 1 and N = 2 included); cases 4-6 N <= 2,000;
cases 7-10 N <= 10^5. Shapes: random, path (deep recursion), star,
caterpillar with light spine and heavy legs (the farthest hut by number of
trails is not the farthest by length), deep random. Case 7 (N = 5*10^4) makes
a search from every hut (O(N^2)) time out. Lengths up to 10^6, so the answer
needs 64 bits on the path case.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
MAX_W = 10**6


def shape_parents(rng: random.Random, n: int, shape: str) -> list[int]:
    parent = [-1] * n
    spine = max(1, n // 10)
    for i in range(1, n):
        if shape == "random":
            parent[i] = rng.randrange(i)
        elif shape == "path":
            parent[i] = i - 1
        elif shape == "star":
            parent[i] = 0
        elif shape == "caterpillar":
            parent[i] = i - 1 if i < spine else rng.randrange(spine)
        elif shape == "deep":
            parent[i] = rng.randrange(max(0, i - 4), i)
        else:
            raise ValueError(shape)
    return parent


def tree_edges(rng: random.Random, n: int, shape: str, low: int, high: int) -> list[tuple[int, int, int]]:
    parent = shape_parents(rng, n, shape)
    spine = max(1, n // 10)
    label = list(range(1, n + 1))
    rng.shuffle(label)
    edges = []
    for i in range(1, n):
        u, v = label[i], label[parent[i]]
        if shape == "caterpillar":
            w = rng.randint(1, 10) if i < spine else rng.randint(high // 2, high)
        else:
            w = rng.randint(low, high)
        edges.append((u, v, w) if rng.random() < 0.5 else (v, u, w))
    rng.shuffle(edges)
    return edges


def check(n: int, edges: list[tuple[int, int, int]]) -> None:
    assert 1 <= n <= MAX_N and len(edges) == n - 1
    root = list(range(n + 1))

    def find(x: int) -> int:
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for u, v, w in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v and 1 <= w <= MAX_W
        a, b = find(u), find(v)
        assert a != b, "cycle"
        root[a] = b


def main() -> None:
    out = Path(sys.argv[1])
    plans = [  # (n, shape, low, high)
        (1, "path", 1, 1), (2, "path", 1, 10**6), (1000, "random", 1, 1000),
        (2000, "path", 1, 10**6), (2000, "star", 1, 10**6), (2000, "caterpillar", 1, 10**6),
        (50_000, "random", 1, 10**6), (100_000, "path", 900_000, 10**6), (60_000, "star", 1, 10**6),
        (60_000, "caterpillar", 1, 10**6),
    ]
    for index, (n, shape, low, high) in enumerate(plans, start=1):
        rng = random.Random(20261211 + index)
        edges = tree_edges(rng, n, shape, low, high)
        check(n, edges)
        lines = [str(n)] + [f"{u} {v} {w}" for u, v, w in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
