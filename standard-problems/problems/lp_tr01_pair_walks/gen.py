#!/usr/bin/env python3
"""Testcase generator for lp_tr01_pair_walks.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 4,000; cases 7-10 N <= 2*10^5. Shapes:
random, path (deep recursion: a recursive DFS overflows the stack), star,
caterpillar, binary. Labels are shuffled so vertex 1 is not special. Case 7
(N = 10^5) makes a BFS from every vertex (O(N^2)) time out.
"""

import random
import sys
from pathlib import Path

MAX_N = 200_000


def shape_parents(rng: random.Random, n: int, shape: str) -> list[int]:
    """parent[i] for i = 1..n-1 on internal labels 0..n-1 (0 is the top)."""
    parent = [-1] * n
    spine = max(1, n // 20)
    for i in range(1, n):
        if shape == "random":
            parent[i] = rng.randrange(i)
        elif shape == "path":
            parent[i] = i - 1
        elif shape == "star":
            parent[i] = 0
        elif shape == "binary":
            parent[i] = (i - 1) // 2
        elif shape == "caterpillar":  # a long spine with leaves hanging off it
            parent[i] = i - 1 if i < spine else rng.randrange(spine)
        elif shape == "deep":  # random but deep: parent among the last few
            parent[i] = rng.randrange(max(0, i - 5), i)
        else:
            raise ValueError(shape)
    return parent


def tree_edges(rng: random.Random, n: int, shape: str) -> list[tuple[int, int]]:
    parent = shape_parents(rng, n, shape)
    label = list(range(1, n + 1))
    rng.shuffle(label)
    edges = []
    for i in range(1, n):
        u, v = label[i], label[parent[i]]
        edges.append((u, v) if rng.random() < 0.5 else (v, u))
    rng.shuffle(edges)
    return edges


def check(n: int, edges: list[tuple[int, int]]) -> None:
    assert 1 <= n <= MAX_N and len(edges) == n - 1
    root = list(range(n + 1))

    def find(x: int) -> int:
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for u, v in edges:
        assert 1 <= u <= n and 1 <= v <= n and u != v
        a, b = find(u), find(v)
        assert a != b, "cycle"
        root[a] = b


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, "path"), (600, "random"), (1000, "path"),
        (4000, "random"), (4000, "star"), (4000, "caterpillar"),
        (100_000, "random"), (200_000, "path"), (60_000, "star"), (80_000, "deep"),
    ]
    for index, (n, shape) in enumerate(plans, start=1):
        rng = random.Random(20261201 + index)
        edges = tree_edges(rng, n, shape)
        check(n, edges)
        lines = [str(n)] + [f"{u} {v}" for u, v in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
