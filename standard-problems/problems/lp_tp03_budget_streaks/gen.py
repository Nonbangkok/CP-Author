#!/usr/bin/env python3
"""Testcase generator for lp_tp03_budget_streaks.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000. Cases 7
and 10 have a budget so large that most subarrays fit, so extending every
start until the budget breaks (O(N^2)) must time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, high: int, zero_share: float, budget: str | int) -> str:
    values = [0 if rng.random() < zero_share else rng.randint(1, high) for _ in range(n)]
    total = sum(values)
    if budget == "all":
        s = total                       # every subarray fits
    elif budget == "most":
        s = total * 9 // 10             # almost every subarray fits
    elif budget == "window":
        # A typical window of a few dozen days fits.
        s = (total // n) * rng.randint(5, 60)
    else:
        s = int(budget)
    s = max(0, min(s, 10**14))
    return f"{n} {s}\n{' '.join(map(str, values))}\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 10, 0.0, 3),                      # a single day over budget: answer 0
        (15, 5, 0.3, "window"),
        (1000, 1000, 0.1, "window"),
        (5000, 100, 0.5, 0),                  # S = 0: only runs of zero days count
        (5000, LIMIT, 0.0, "all"),            # every subarray fits: N(N+1)/2
        (5000, LIMIT, 0.05, "window"),
        (100000, 1000, 0.1, "most"),          # first large case: slow.cpp must TLE here
        (100000, LIMIT, 0.0, "window"),
        (100000, LIMIT, 0.2, LIMIT // 2),     # many single days already over budget
        (100000, 10, 0.3, "all"),             # answer N(N+1)/2, far above int
    ]
    for index, (n, high, zero_share, budget) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 307 * index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, high, zero_share, budget), encoding="utf-8")


if __name__ == "__main__":
    main()
