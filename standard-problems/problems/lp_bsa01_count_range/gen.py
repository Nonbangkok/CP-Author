#!/usr/bin/env python3
"""Testcase generator for lp_bsa01_count_range.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-5 N, Q <= 5,000; cases 6-10 N = Q = 40,000,
where answering each query by scanning the whole array (O(NQ)) must time out.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**6


def case(rng: random.Random, n: int, q: int, spread: int, wide: bool) -> str:
    values = [rng.randint(-spread, spread) for _ in range(n)]
    lines = [f"{n} {q}", " ".join(map(str, values))]
    for _ in range(q):
        if wide and rng.random() < 0.3:
            l, r = sorted((rng.randint(-LIMIT, LIMIT), rng.randint(-LIMIT, LIMIT)))
        else:
            # Narrow queries around existing values, so boundaries (l == a_i, r == a_i) are common.
            centre = rng.choice(values)
            l, r = centre - rng.randint(0, 3), centre + rng.randint(0, 3)
            l, r = max(l, -LIMIT), min(r, LIMIT)
        lines.append(f"{l} {r}")
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 1, 10, False), (60, 80, 20, True), (1000, 1000, 500, True),
        (5000, 5000, 100, True), (5000, 5000, LIMIT, True),
        (40000, 40000, LIMIT, True), (40000, 40000, 50, True), (40000, 40000, LIMIT, False),
        (40000, 40000, 1000, True), (40000, 40000, LIMIT, True),
    ]
    for index, (n, q, spread, wide) in enumerate(plans, start=1):
        rng = random.Random(20261120 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, q, spread, wide), encoding="utf-8")


if __name__ == "__main__":
    main()
