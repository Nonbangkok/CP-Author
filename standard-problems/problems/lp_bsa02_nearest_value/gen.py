#!/usr/bin/env python3
"""Testcase generator for lp_bsa02_nearest_value.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-5 N, Q <= 5,000; cases 6-10 N = Q = 40,000,
where scanning the whole array for every query (O(NQ)) must time out.
Queries hit exact values, exact midpoints (ties), and both ends beyond the data.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, q: int, spread: int) -> str:
    values = [rng.randint(-spread, spread) for _ in range(n)]
    ordered = sorted(set(values))
    queries = []
    for _ in range(q):
        roll = rng.random()
        if roll < 0.25 and len(ordered) > 1:
            # A midpoint between two neighbours: an exact tie when the gap is even.
            k = rng.randrange(len(ordered) - 1)
            lo, hi = ordered[k], ordered[k + 1]
            x = (lo + hi) // 2 if rng.random() < 0.7 else (lo + hi + 1) // 2
        elif roll < 0.45:
            x = rng.choice(values) + rng.randint(-1, 1)
        elif roll < 0.55:
            x = rng.choice((-LIMIT, LIMIT, rng.randint(-LIMIT, LIMIT)))
        else:
            x = rng.randint(-spread - spread // 10 - 5, spread + spread // 10 + 5)
        queries.append(max(-LIMIT, min(LIMIT, x)))
    return "\n".join([f"{n} {q}", " ".join(map(str, values))] + list(map(str, queries))) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 5, 10), (50, 80, 30), (1000, 1000, LIMIT),
        (5000, 5000, 2000), (5000, 5000, LIMIT),
        (40000, 40000, LIMIT), (40000, 40000, 100), (40000, 40000, 100000),
        (40000, 40000, LIMIT), (40000, 40000, 30000),
    ]
    for index, (n, q, spread) in enumerate(plans, start=1):
        rng = random.Random(20261121 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, q, spread), encoding="utf-8")


if __name__ == "__main__":
    main()
