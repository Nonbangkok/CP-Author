#!/usr/bin/env python3
"""Testcase generator for lp_tp02_closest_sum.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000, where
trying every pair (O(N^2)) must time out.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, low: int, high: int, target: int | str) -> str:
    values = [rng.randint(low, high) for _ in range(n)]
    if target == "lattice":
        # Every value a multiple of 1000 and T is not: sums never hit T, the
        # answer is a few hundred instead of the 0 a dense random case gives.
        values = [v - v % 1000 for v in values]
        target = rng.randint(-LIMIT, LIMIT) // 1000 * 1000 + 337
    elif target == "clusters":
        # Half the cards near -10^9, half near +10^9: pair sums form three
        # clusters (near -2*10^9, near 0, near 2*10^9) and T sits in a gap.
        half = n // 2
        values = ([rng.randint(-LIMIT, -9 * 10**8) for _ in range(half)]
                  + [rng.randint(9 * 10**8, LIMIT) for _ in range(n - half)])
        rng.shuffle(values)
        target = 95 * 10**7 + rng.randint(-1000, 1000)
    elif target == "hit":
        # Some pair sums to T exactly (answer 0).
        i, j = rng.sample(range(n), 2)
        target = values[i] + values[j]
    elif target == "near":
        # T between two existing sums, usually not reachable exactly.
        target = rng.choice(values) + rng.choice(values) + rng.choice((-1, 1))
    target = max(-2 * LIMIT, min(int(target), 2 * LIMIT))
    return f"{n} {target}\n{' '.join(map(str, values))}\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (2, -10, 10, 0),
        (10, -20, 20, "near"),
        (1000, -LIMIT, LIMIT, "near"),
        (5000, -LIMIT, LIMIT, "hit"),
        (5000, 0, 1000, 2 * LIMIT),            # far above every sum: answer is T - (two largest)
        (5000, -LIMIT, LIMIT, "near"),
        (100000, -LIMIT, LIMIT, "lattice"),    # first large case: slow.cpp must TLE here
        (100000, -LIMIT, -LIMIT + 5, 2 * LIMIT),  # |a_i + a_j - T| close to 4 * 10^9
        (100000, -1000, 1000, "hit"),
        (100000, -LIMIT, LIMIT, "clusters"),
    ]
    for index, (n, low, high, target) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 211 * index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, low, high, target), encoding="utf-8")


if __name__ == "__main__":
    main()
