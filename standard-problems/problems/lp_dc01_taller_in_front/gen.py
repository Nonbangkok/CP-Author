#!/usr/bin/env python3
"""Testcase generator for lp_dc01_taller_in_front.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N <= 5,000; cases 6-10 N = 10^5, where
checking every pair must time out. Covers N = 1, all equal (answer 0),
strictly decreasing (answer N(N-1)/2 ~ 5 * 10^9, needs 64 bits), sorted,
few distinct heights, random heights up to 10^9.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
LIMIT = 10**9


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append([170])
    rng = random.Random(20261231)
    plans.append([rng.randint(140, 190) for _ in range(30)])
    rng = random.Random(20261232)
    plans.append([rng.randint(1, LIMIT) for _ in range(1000)])
    plans.append([LIMIT - i for i in range(5000)])                     # decreasing
    rng = random.Random(20261233)
    plans.append([rng.randint(1, 3) for _ in range(5000)])
    rng = random.Random(20261234)
    plans.append([rng.randint(1, LIMIT) for _ in range(MAX_N)])         # slow.cpp must TLE here
    plans.append([LIMIT - 7 * i for i in range(MAX_N)])                 # decreasing: max answer
    plans.append(sorted(rng.randint(1, LIMIT) for _ in range(MAX_N)))   # sorted: answer 0
    rng = random.Random(20261235)
    plans.append([rng.randint(1, 50) for _ in range(MAX_N)])            # many duplicates
    rng = random.Random(20261236)
    nearly = list(range(1, MAX_N + 1))
    for _ in range(2000):
        i, j = rng.randrange(MAX_N), rng.randrange(MAX_N)
        nearly[i], nearly[j] = nearly[j], nearly[i]
    plans.append(nearly)
    for index, a in enumerate(plans, start=1):
        assert 1 <= len(a) <= (1000 if index <= 3 else 5000 if index <= 5 else MAX_N)
        assert all(1 <= v <= LIMIT for v in a)
        (out / f"input{index:02d}.txt").write_text(f"{len(a)}\n{' '.join(map(str, a))}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
