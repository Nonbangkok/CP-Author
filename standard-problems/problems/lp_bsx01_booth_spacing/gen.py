#!/usr/bin/env python3
"""Testcase generator for lp_bsx01_booth_spacing.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 10, x <= 100; cases 3-5 N <= 1,000, x <= 10^5; cases 6-10
N <= 10^5, x <= 10^9, where answers reach the hundreds of millions, so trying
every distance d = 1, 2, ... must time out. Covers K = 2 (answer = span),
K = N (answer = smallest gap), dense and clustered points.
"""

import random
import sys
from pathlib import Path


def distinct(rng: random.Random, n: int, top: int, clustered: bool) -> list[int]:
    if clustered:
        # A few tight clusters far apart: the greedy must skip whole clusters.
        centres = rng.sample(range(top // 10, top - top // 10), 8)
        chosen = set()
        while len(chosen) < n:
            c = rng.choice(centres)
            chosen.add(max(0, min(top, c + rng.randint(-top // 200, top // 200))))
        points = list(chosen)
    else:
        points = rng.sample(range(top + 1), n)
    rng.shuffle(points)
    return points


def main() -> None:
    out = Path(sys.argv[1])
    # (n, k, top, clustered)
    plans = [
        (2, 2, 100, False), (10, 4, 100, False),
        (1000, 7, 10**5, False), (1000, 1000, 10**5, False), (1000, 30, 10**5, True),
        (100000, 3, 10**9, False), (100000, 2, 10**9, False), (60000, 9, 10**9, True),
        (100000, 100000, 10**9, False), (50000, 1000, 10**9, False),
    ]
    for index, (n, k, top, clustered) in enumerate(plans, start=1):
        rng = random.Random(20261123 + index)
        points = distinct(rng, n, top, clustered)
        (out / f"input{index:02d}.txt").write_text(f"{n} {k}\n" + " ".join(map(str, points)) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
