#!/usr/bin/env python3
"""Testcase generator for lp_tr03_office_party.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 10; cases 3-5 N <= 30; cases 6-10 N <= 10^5. Employee 1 is the
CEO; every other label is shuffled, so a boss may have a larger number than
the employee (looping i = N..2 is not a valid order). Shapes: path (depth
10^5: a recursive DFS overflows the stack), star, random, binary, caterpillar,
deep random.
Case 6 is a caterpillar with a 100-long chain of command, so the DP without
memo (exponential in the depth) must time out there.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
MAX_F = 10**6


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
        elif shape == "caterpillar":
            parent[i] = i - 1 if i < 100 else rng.randrange(100)
        elif shape == "deep":  # random but deep: boss among the last few hires
            parent[i] = rng.randrange(max(0, i - 3), i)
        else:
            raise ValueError(shape)
    return parent


def make_case(rng: random.Random, n: int, shape: str, zero_share: float) -> tuple[list[int], list[int]]:
    """fun values f[1..n] and boss p[2..n] (labels shuffled, 1 stays the CEO)."""
    parent = shape_parents(rng, n, shape)
    label = [1] + rng.sample(range(2, n + 1), n - 1)
    boss = [0] * (n + 1)
    for i in range(1, n):
        boss[label[i]] = label[parent[i]]
    fun = [0 if rng.random() < zero_share else rng.randint(1, MAX_F) for _ in range(n + 1)]
    return fun[1:], boss[2:]


def check(n: int, fun: list[int], boss: list[int]) -> None:
    assert 1 <= n <= MAX_N and len(fun) == n and len(boss) == n - 1
    assert all(0 <= f <= MAX_F for f in fun)
    p = [0, 0] + boss
    assert all(1 <= p[i] <= n and p[i] != i for i in range(2, n + 1))
    children = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        children[p[i]].append(i)
    seen = [1]
    for u in seen:
        seen.extend(children[u])
    assert len(seen) == n, "every chain of bosses must reach employee 1"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [  # (n, shape, share of zero fun)
        (1, "path", 0.0), (10, "random", 0.2),
        (30, "path", 0.0), (30, "random", 0.1), (30, "binary", 0.3),
        (100_000, "caterpillar", 0.1), (100_000, "path", 0.05), (50_000, "star", 0.0),
        (50_000, "random", 0.3), (50_000, "deep", 0.1),
    ]
    for index, (n, shape, zeros) in enumerate(plans, start=1):
        rng = random.Random(20261221 + index)
        fun, boss = make_case(rng, n, shape, zeros)
        check(n, fun, boss)
        text = f"{n}\n{' '.join(map(str, fun))}\n{' '.join(map(str, boss))}\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
