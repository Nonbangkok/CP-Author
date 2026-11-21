#!/usr/bin/env python3
"""Testcase generator for lp_dc03_minus_the_max.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N <= 5,000; cases 6-10 N = 10^5, where trying
every block must time out. Covers N = 1 (answer 0), all negative (answer 0),
all positive and huge (whole array, ~10^14 needs 64 bits), increasing values
(the maximum changes at every step), equal values, mixed signs with spikes
that are better left out of the block.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
LIMIT = 10**9


def rand(rng, n, low, high):
    return [rng.randint(low, high) for _ in range(n)]


def spiky(rng, n):
    """Small mostly-positive values with rare huge spikes the block should avoid."""
    values = rand(rng, n, -300, 1000)
    for _ in range(n // 200):
        values[rng.randrange(n)] = rng.randint(LIMIT // 2, LIMIT)
    return values


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append([7])
    rng = random.Random(20261251)
    plans.append(rand(rng, 12, -9, 9))
    rng = random.Random(20261252)
    plans.append(spiky(rng, 1000))
    rng = random.Random(20261253)
    plans.append(rand(rng, 5000, -LIMIT, -1))                          # all negative: 0
    rng = random.Random(20261254)
    plans.append(rand(rng, 5000, -LIMIT, LIMIT))
    rng = random.Random(20261255)
    plans.append(rand(rng, MAX_N, -LIMIT, LIMIT))                       # slow.cpp must TLE here
    rng = random.Random(20261256)
    plans.append(rand(rng, MAX_N, LIMIT - 1000, LIMIT))                 # all positive: whole array
    plans.append([-LIMIT + 20000 * i for i in range(MAX_N)])            # increasing, crosses zero
    rng = random.Random(20261257)
    plans.append(spiky(rng, MAX_N))
    rng = random.Random(20261258)
    plans.append([rng.choice((-5, 5, 5)) for _ in range(MAX_N)])        # many equal maxima
    for index, a in enumerate(plans, start=1):
        assert 1 <= len(a) <= (1000 if index <= 3 else 5000 if index <= 5 else MAX_N)
        assert all(-LIMIT <= v <= LIMIT for v in a)
        (out / f"input{index:02d}.txt").write_text(f"{len(a)}\n{' '.join(map(str, a))}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
