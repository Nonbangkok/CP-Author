#!/usr/bin/env python3
"""Testcase generator for lp_sw01_best_window.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000. Cases 7
and 10 have K near N / 2, so re-adding every window from scratch (O(NK)) must
time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, k: int, low: int, high: int) -> str:
    values = [rng.randint(low, high) for _ in range(n)]
    return f"{n} {k}\n{' '.join(map(str, values))}\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 1, -LIMIT, -LIMIT),               # one day, K = N, the minimum value
        (10, 3, -10, 10),
        (1000, 1000, -LIMIT, LIMIT),          # K = N: the whole array
        (5000, 1, -LIMIT, LIMIT),             # K = 1: the maximum element
        (5000, 2500, -LIMIT, -1),             # every day a loss
        (5000, 37, -LIMIT, LIMIT),
        (100000, 50000, -LIMIT, LIMIT),       # first large case: slow.cpp must TLE here
        (100000, 100000, LIMIT, LIMIT),       # 10^14, far above int
        (100000, 300, -LIMIT, LIMIT),
        (100000, 40000, -LIMIT // 2, LIMIT),
    ]
    for index, (n, k, low, high) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 401 * index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, k, low, high), encoding="utf-8")


if __name__ == "__main__":
    main()
