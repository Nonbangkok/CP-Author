#!/usr/bin/env python3
"""Testcase generator for lp_stl06_top_k_sum.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N = 100,000 with K <= 20; cases 6-10
N = 100,000 with large K, where scanning the K best for the smallest one every
day (O(NK)) must time out (case 6: K = N / 2, random scores).
Covered: N = 1, K = 1, K = N, many equal scores, increasing scores (every new
score enters the top K), decreasing scores (none does), the maximum answer.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**6


def case(rng: random.Random, n: int, k: int, shape: str, spread: int = LIMIT) -> str:
    values = [rng.randint(1, spread) for _ in range(n)]
    if shape == "up":
        values.sort()
    elif shape == "down":
        values.sort(reverse=True)
    elif shape == "max":
        values = [LIMIT] * n
    return f"{n} {k}\n" + " ".join(map(str, values)) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    rngs = [random.Random(20261120 + i) for i in range(1, 11)]
    plans = [
        (1, 1, "random", LIMIT), (40, 3, "random", 10), (1000, 300, "up", LIMIT),
        (100000, 1, "random", LIMIT), (100000, 20, "up", LIMIT),
        (100000, 50000, "random", LIMIT), (100000, 100000, "max", LIMIT),
        (100000, 70000, "up", LIMIT), (100000, 30000, "random", 50),
        (100000, 60000, "random", LIMIT),
    ]
    for index, (n, k, shape, spread) in enumerate(plans, start=1):
        body = case(rngs[index - 1], n, k, shape, spread)
        (out / f"input{index:02d}.txt").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
