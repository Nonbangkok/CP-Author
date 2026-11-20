#!/usr/bin/env python3
"""Testcase generator for lp_gr02_deadline_jobs.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 10; cases 3-5 N <= 5,000; cases 6-10 N <= 10^5. Case 6 has
N = 10^5 and every deadline >= N, so scanning down for a free day (slow.cpp) is O(N^2)
there. Covers N = 1, all deadlines 1 (answer = max profit), deadlines >= N
(answer = sum, past 2^31), equal profits, tight random deadlines.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
LIMIT = 10**9


def jobs(rng, n, max_d, low_p, high_p, min_d=1):
    return [(rng.randint(min_d, max_d), rng.randint(low_p, high_p)) for _ in range(n)]


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append([(1, 42)])
    rng = random.Random(20261211)
    plans.append(jobs(rng, 10, 4, 1, 50))
    rng = random.Random(20261212)
    plans.append(jobs(rng, 5000, 1, 1, LIMIT))                          # all deadline 1
    rng = random.Random(20261213)
    plans.append(jobs(rng, 5000, 2500, 1, 1000))
    rng = random.Random(20261214)
    plans.append(jobs(rng, 5000, LIMIT, 1, LIMIT, min_d=5000))          # everything fits
    rng = random.Random(20261215)
    plans.append(jobs(rng, MAX_N, 2 * MAX_N, 1, 10**6, min_d=MAX_N))    # slow.cpp must TLE here
    rng = random.Random(20261216)
    plans.append(jobs(rng, 50_000, 15_000, 1, LIMIT))
    rng = random.Random(20261217)
    plans.append(jobs(rng, MAX_N, MAX_N, 7, 7))                         # equal profits
    rng = random.Random(20261218)
    plans.append(jobs(rng, 50_000, 1000, LIMIT - 1000, LIMIT))
    rng = random.Random(20261219)
    plans.append(jobs(rng, 50_000, MAX_N, 1, LIMIT, min_d=MAX_N // 4))
    for index, items in enumerate(plans, start=1):
        assert 1 <= len(items) <= (10 if index <= 2 else 5000 if index <= 5 else MAX_N)
        assert all(1 <= d <= LIMIT and 1 <= p <= LIMIT for d, p in items)
        lines = [str(len(items))] + [f"{d} {p}" for d, p in items]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
