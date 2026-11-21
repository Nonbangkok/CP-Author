#!/usr/bin/env python3
"""Testcase generator for lp_gr03_on_time_tasks.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 8; cases 3-5 N <= 3,000; cases 6-10 N <= 10^5 (case 6 is
N = 10^5, where the O(N^2) DP must time out). Covers N = 1 with t > d (answer 0), tasks that never
fit, everything fitting, durations and deadlines near 10^9 (time + t passes
2^31 before a drop), equal deadlines, tight random deadlines.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
LIMIT = 10**9


def tasks(rng, n, max_t, max_d, min_d=1):
    return [(rng.randint(1, max_t), rng.randint(min_d, max_d)) for _ in range(n)]


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append([(10, 9)])                                             # cannot be on time
    rng = random.Random(20261221)
    plans.append(tasks(rng, 8, 6, 15))
    rng = random.Random(20261222)
    plans.append(tasks(rng, 3000, 100, 30_000))
    rng = random.Random(20261223)
    plans.append(tasks(rng, 3000, LIMIT, LIMIT, min_d=LIMIT - 10**6))   # big values, few fit
    rng = random.Random(20261224)
    plans.append(tasks(rng, 3000, 1000, LIMIT, min_d=3 * 10**6))        # everything fits
    rng = random.Random(20261225)
    plans.append(tasks(rng, MAX_N, 1000, 10**7))                        # slow.cpp must TLE here
    rng = random.Random(20261226)
    plans.append(tasks(rng, 30_000, LIMIT, LIMIT))
    rng = random.Random(20261227)
    plans.append([(rng.randint(1, 10**5), LIMIT) for _ in range(50_000)])  # one deadline for all
    rng = random.Random(20261228)
    plans.append(tasks(rng, 50_000, 2 * 10**4, 10**9))
    rng = random.Random(20261229)
    mixed = tasks(rng, 49_000, 5000, 10**8)
    mixed += [(LIMIT, rng.randint(1, LIMIT - 1)) for _ in range(1000)]  # tasks that never fit
    rng.shuffle(mixed)
    plans.append(mixed)
    for index, items in enumerate(plans, start=1):
        assert 1 <= len(items) <= (8 if index <= 2 else 3000 if index <= 5 else MAX_N)
        assert all(1 <= t <= LIMIT and 1 <= d <= LIMIT for t, d in items)
        lines = [str(len(items))] + [f"{t} {d}" for t, d in items]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
