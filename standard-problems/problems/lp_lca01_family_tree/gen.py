#!/usr/bin/env python3
"""Testcase generator for lp_lca01_family_tree.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q <= 10^5.
Person 1 is the root; all other labels are shuffled, so a parent may have a
larger number than the child. Shapes: path (depth N), "Y" (two long arms, so
climbing one step at a time costs O(N) per query from both sides), star,
random, caterpillar, binary. Queries mix random pairs, u = v, and
ancestor/descendant pairs. Case 7 (a path, N = Q = 10^5) makes the naive climb
(O(depth) per query) time out.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
MAX_Q = 100_000


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
        elif shape == "y":  # two arms hanging from the root: 0-1-3-5-... and 0-2-4-6-...
            parent[i] = max(0, i - 2)
        elif shape == "caterpillar":
            spine = max(1, n // 4)
            parent[i] = i - 1 if i < spine else rng.randrange(spine)
        else:
            raise ValueError(shape)
    return parent


def make_case(rng: random.Random, n: int, q: int, shape: str) -> tuple[list[int], list[tuple[int, int]]]:
    parent = shape_parents(rng, n, shape)
    label = [1] + rng.sample(range(2, n + 1), n - 1)
    par = [0] * (n + 1)
    for i in range(1, n):
        par[label[i]] = label[parent[i]]
    queries = []
    for _ in range(q):
        kind = rng.random()
        u = rng.randint(1, n)
        if kind < 0.05:
            v = u
        elif kind < 0.2:  # an ancestor of u, some steps up
            v = u
            for _ in range(rng.randint(0, 50)):
                if v == 1:
                    break
                v = par[v]
            if rng.random() < 0.5:
                u, v = v, u
        else:
            v = rng.randint(1, n)
        queries.append((u, v))
    return par[2:], queries


def check(n: int, q: int, par: list[int], queries: list[tuple[int, int]]) -> None:
    assert 1 <= n <= MAX_N and 1 <= q <= MAX_Q and len(par) == n - 1 and len(queries) == q
    p = [0, 0] + par
    assert all(1 <= p[i] <= n and p[i] != i for i in range(2, n + 1))
    children = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        children[p[i]].append(i)
    seen = [1]
    for u in seen:
        seen.extend(children[u])
    assert len(seen) == n, "every chain of parents must reach person 1"
    assert all(1 <= u <= n and 1 <= v <= n for u, v in queries)


def main() -> None:
    out = Path(sys.argv[1])
    plans = [  # (n, q, shape)
        (1, 3, "path"), (10, 20, "random"), (1000, 1000, "path"),
        (5000, 5000, "y"), (5000, 5000, "random"), (5000, 5000, "star"),
        (100_000, 100_000, "path"), (100_000, 40_000, "binary"), (60_000, 40_000, "caterpillar"),
        (60_000, 40_000, "y"),
    ]
    for index, (n, q, shape) in enumerate(plans, start=1):
        rng = random.Random(20261231 + index)
        par, queries = make_case(rng, n, q, shape)
        check(n, q, par, queries)
        lines = [f"{n} {q}", " ".join(map(str, par))] + [f"{u} {v}" for u, v in queries]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
