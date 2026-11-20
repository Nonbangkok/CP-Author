#!/usr/bin/env python3
"""Testcase generator for lp_gr01_room_bookings.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-2 N <= 10; cases 3-5 N <= 3,000; cases 6-10 N <= 10^5 (case 6 is
N = 10^5, where the O(N^2) DP must time out). Covers N = 1, identical bookings (answer 1),
touching bookings with C = 0 (all fit), values near 10^9 with C = 10^9 (end + C
needs 64 bits), one huge booking over many small ones.
"""

import random
import sys
from pathlib import Path

MAX_N = 100_000
LIMIT = 10**9


def random_bookings(rng, n, span, max_d):
    return [(rng.randint(0, span), rng.randint(1, max_d)) for _ in range(n)]


def chain(rng, n, step):
    items = [(i * step, step) for i in range(n)]
    rng.shuffle(items)
    return items


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append((5, [(7, 3)]))
    rng = random.Random(20261201)
    plans.append((2, random_bookings(rng, 10, 60, 15)))
    rng = random.Random(20261202)
    plans.append((20, random_bookings(rng, 3000, 100_000, 300)))
    plans.append((LIMIT, [(LIMIT, LIMIT)] * 3000))                      # identical: answer 1
    rng = random.Random(20261203)
    plans.append((0, chain(rng, 3000, 5)))                              # touching, C = 0: all fit
    rng = random.Random(20261204)
    plans.append((1000, random_bookings(rng, MAX_N, 10**7, 3000)))      # slow.cpp must TLE here
    rng = random.Random(20261205)
    plans.append((LIMIT, [(rng.randint(LIMIT - 10**6, LIMIT), rng.randint(LIMIT - 10**6, LIMIT))
                          for _ in range(30_000)]))                     # end + C ~ 3 * 10^9
    rng = random.Random(20261206)
    small = random_bookings(rng, 49_999, LIMIT, 3000)
    small.insert(rng.randrange(50_000), (0, LIMIT))                      # one huge booking
    plans.append((7, small))
    rng = random.Random(20261207)
    plans.append((3, random_bookings(rng, MAX_N, 5000, 10)))            # dense, many duplicates
    rng = random.Random(20261208)
    plans.append((0, chain(rng, MAX_N, 50)))
    for index, (c, items) in enumerate(plans, start=1):
        assert 1 <= len(items) <= MAX_N and 0 <= c <= LIMIT
        assert all(0 <= s <= LIMIT and 1 <= d <= LIMIT for s, d in items)
        assert len(items) <= (10 if index <= 2 else 3000 if index <= 5 else MAX_N)
        lines = [f"{len(items)} {c}"] + [f"{s} {d}" for s, d in items]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
