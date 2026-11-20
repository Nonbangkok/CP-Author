#!/usr/bin/env python3
"""Testcase generator for lp_bsx02_split_work.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 10, a <= 100; cases 3-5 N <= 1,000, a <= 100; cases 6-10
N <= 10^5, a <= 10^9, where the answer sits ~10^9 .. 10^14 above max(a), so
trying every cap from max(a) upwards must time out, and sums need 64 bits.
Covers K = 1 (answer = total), K = N (answer = max), one huge element.
"""

import random
import sys
from pathlib import Path


def main() -> None:
    out = Path(sys.argv[1])
    # (n, k, low, high)
    plans = [
        (1, 1, 1, 100), (10, 3, 1, 100),
        (1000, 40, 1, 100), (1000, 1000, 1, 100), (1000, 333, 90, 100),
        (100000, 70, 1, 10**9), (100000, 1, 10**9 - 1000, 10**9), (100000, 4000, 1, 10**6),
        (100000, 100000, 1, 10**9), (50000, 17, 1, 10**9),
    ]
    for index, (n, k, low, high) in enumerate(plans, start=1):
        rng = random.Random(20261124 + index)
        values = [rng.randint(low, high) for _ in range(n)]
        if index == 8:
            values[rng.randrange(n)] = 10**9  # one giant task dominates its part
        (out / f"input{index:02d}.txt").write_text(f"{n} {k}\n" + " ".join(map(str, values)) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
