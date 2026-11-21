#!/usr/bin/env python3
"""Testcase generator for lp_bexp02_geometric_sum.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 Q <= 10, n <= 1,000; cases 4-5 Q <= 10, n <= 10^6; cases 6-10
Q = 10^4 with n up to 10^18, where adding the terms one by one must time out.
Edge cases: n = 0, a = 0, a = 1, a = 1 (mod m) (so a - 1 has no inverse),
m = 1, composite m (powers of two, 10^9), prime m, n + 1 a power of two.
"""

import random
import sys
from pathlib import Path

BIG = 10**18
PRIMES = [998244353, 999999937, 999999929]


def query(rng: random.Random, max_n: int) -> tuple[int, int, int]:
    roll = rng.random()
    if roll < 0.04:
        m = 1
    elif roll < 0.20:
        m = rng.choice(PRIMES)
    elif roll < 0.35:
        m = rng.choice([10**9, 2**29, 999999000, 735134400])
    elif roll < 0.45:
        m = rng.randint(2, 30)
    else:
        m = rng.randint(2, 10**9)
    roll = rng.random()
    if roll < 0.05:
        a = 0
    elif roll < 0.10:
        a = 1
    elif roll < 0.20:
        a = min(10**9, m * rng.randint(0, 10**9 // m) + 1)  # a = 1 (mod m)
    elif roll < 0.25:
        a = min(10**9, m * rng.randint(1, 10**9 // m))  # a = 0 (mod m)
    else:
        a = rng.randint(0, 10**9)
    roll = rng.random()
    if roll < 0.05:
        n = 0
    elif roll < 0.15:
        n = max_n
    elif roll < 0.22:
        n = min(max_n, 2 ** rng.randint(0, 59) - 1)
    else:
        n = rng.randint(0, max_n)
    return a, n, m


def case(rng: random.Random, q: int, max_n: int, fixed: list[tuple[int, int, int]]) -> str:
    rows = list(fixed)
    while len(rows) < q:
        rows.append(query(rng, max_n))
    rows = rows[:q]
    return "\n".join([str(q)] + [f"{a} {n} {m}" for a, n, m in rows]) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    edge = [(0, 0, 5), (0, 7, 1), (1, 0, 1), (1, 999, 1000), (4, 1000, 3), (10**9, 1000, 10**9)]
    # Case 6 opens with a huge n so the naive loop times out on its first query.
    huge = [(2, BIG, 998244353), (10**9, BIG, 999999999), (1, BIG, 10**9), (999999937, BIG, 2**29)]
    plans = [
        (1, 10, []),
        (10, 100, edge),
        (10, 1000, edge),
        (10, 10**6, [(3, 10**6, 10**9), (1, 10**6, 10**9 - 1), (10**9 - 1, 10**6, 999999937)]),
        (10, 10**6, [(2, 10**6, 2**29), (0, 10**6, 7)] + [(7, 10**6 - i, 998244353) for i in range(8)]),
        (10**4, BIG, huge),
        (10**4, BIG, huge),
        (10**4, BIG, []),
        (10**4, 10**12, huge),
        (10**4, BIG, huge),
    ]
    for index, (q, max_n, fixed) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 100 * index + 13)
        (out / f"input{index:02d}.txt").write_text(case(rng, q, max_n, fixed), encoding="utf-8")


if __name__ == "__main__":
    main()
