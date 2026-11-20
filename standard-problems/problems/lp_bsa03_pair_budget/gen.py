#!/usr/bin/env python3
"""Testcase generator for lp_bsa03_pair_budget.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N <= 5,000; cases 6-10 N = 100,000, where
trying every pair (O(N^2)) must time out. Budgets are picked so the answer
lands anywhere from 0 to all pairs; the full-range cases need 64-bit sums
(a_i + a_j and K - a_j reach 3 * 10^9) and an answer near 5 * 10^9.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, spread: int, budget: str) -> str:
    values = [rng.randint(-spread, spread) for _ in range(n)]
    if budget == "all":
        k = 2 * LIMIT
    elif budget == "none":
        k = -2 * LIMIT
    elif budget == "pair-sum":
        # Exactly the sum of two existing values, so equality at the boundary matters.
        i, j = rng.sample(range(n), 2) if n > 1 else (0, 0)
        k = values[i] + values[j]
    else:
        k = rng.randint(-2 * spread, 2 * spread)
    k = max(-2 * LIMIT, min(2 * LIMIT, k))
    return f"{n} {k}\n" + " ".join(map(str, values)) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 5, "all"), (60, 20, "pair-sum"), (1000, LIMIT, "random"),
        (5000, 3, "pair-sum"), (5000, LIMIT, "pair-sum"),
        (100000, LIMIT, "all"), (100000, 1000, "pair-sum"), (100000, 10**6, "random"),
        (100000, LIMIT, "pair-sum"), (100000, 10**6, "none"),
    ]
    for index, (n, spread, budget) in enumerate(plans, start=1):
        rng = random.Random(20261122 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, spread, budget), encoding="utf-8")


if __name__ == "__main__":
    main()
