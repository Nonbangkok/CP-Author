#!/usr/bin/env python3
"""Testcase generator for lp_tp01_swan_boats.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N up to 200,000.
Cases 7 and 10 pair up almost everyone, so searching for the lightest free
person from the left every time (O(N^2)) must time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, k: int, low: int, high: int) -> str:
    values = sorted(rng.randint(low, high) for _ in range(n))
    return f"{n} {k}\n{' '.join(map(str, values))}\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 10, 10, 10),                      # one person, exactly K
        (9, 20, 1, 20),
        (1000, 1000, 1, 1000),
        (5000, LIMIT, LIMIT // 2 + 1, LIMIT), # nobody can share: N boats
        (5000, 10000, 1, 5000),               # everybody can share: ceil(N / 2)
        (5000, LIMIT, 1, LIMIT),
        (200000, 20000, 1, 10000),            # first large case: slow.cpp must TLE here
        (100000, LIMIT, 1, LIMIT),
        (200000, 10**6, 1, 10**6),
        (199999, 9999, 1, 4999),              # odd N, everybody shares but one
    ]
    for index, (n, k, low, high) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 113 * index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, k, low, high), encoding="utf-8")


if __name__ == "__main__":
    main()
