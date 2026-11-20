#!/usr/bin/env python3
"""Testcase generator for lp_dc02_twice_as_big.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N <= 5,000; cases 6-10 N = 10^5, where
checking every pair must time out. Covers N = 1, all equal and negative (every
pair counts, ~5 * 10^9), all equal and positive (none), zeros, values near
+-10^9 (2 * a_j overflows int), decreasing positives, mixed signs.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
LIMIT = 10**9


def rand(rng, n, low, high):
    return [rng.randint(low, high) for _ in range(n)]


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append([-3])
    rng = random.Random(20261241)
    plans.append(rand(rng, 20, -10, 10))
    rng = random.Random(20261242)
    plans.append(rand(rng, 1000, -LIMIT, LIMIT))
    plans.append([0] * 2500 + [5] * 2500)                               # zeros, then equal positives: 0
    rng = random.Random(20261243)
    plans.append(sorted(rand(rng, 5000, -LIMIT, LIMIT), reverse=True))  # decreasing, mixed signs
    rng = random.Random(20261244)
    plans.append(rand(rng, MAX_N, -LIMIT, LIMIT))                       # slow.cpp must TLE here
    plans.append([-LIMIT] * MAX_N)                                      # every pair counts
    plans.append([LIMIT - 20000 * i for i in range(MAX_N)])              # decreasing, crosses zero
    rng = random.Random(20261245)
    plans.append(rand(rng, MAX_N, 1, 1000))
    rng = random.Random(20261246)
    mixed = rand(rng, MAX_N // 2, LIMIT // 2, LIMIT) + rand(rng, MAX_N // 2, -LIMIT, -LIMIT // 2)
    rng.shuffle(mixed)
    plans.append(mixed)
    for index, a in enumerate(plans, start=1):
        assert 1 <= len(a) <= (1000 if index <= 3 else 5000 if index <= 5 else MAX_N)
        assert all(-LIMIT <= v <= LIMIT for v in a)
        (out / f"input{index:02d}.txt").write_text(f"{len(a)}\n{' '.join(map(str, a))}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
