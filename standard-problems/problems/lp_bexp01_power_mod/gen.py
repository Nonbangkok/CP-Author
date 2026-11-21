#!/usr/bin/env python3
"""Testcase generator for lp_bexp01_power_mod.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 Q <= 100, b <= 1,000; cases 4-5 Q <= 1,000, b <= 10^4; cases 6-10
Q = 10^4 with b up to 10^18, where multiplying b times must time out.
Edge cases: b = 0, a = 0 (including 0^0), m = 1, a >= m, a a multiple of m,
m = 10^9 (largest products), and primes near 10^9.
"""

import random
import sys
from pathlib import Path

BIG = 10**18
PRIMES = [998244353, 999999937, 999999929, 999999893]


def query(rng: random.Random, max_b: int, max_a: int) -> tuple[int, int, int]:
    roll = rng.random()
    if roll < 0.05:
        m = 1
    elif roll < 0.25:
        m = rng.choice(PRIMES) if rng.random() < 0.7 else 10**9
    elif roll < 0.35:
        m = rng.randint(2, 20)
    else:
        m = rng.randint(2, 10**9)
    m = min(m, 10**9)
    roll = rng.random()
    if roll < 0.05:
        a = 0
    elif roll < 0.10:
        a = m * rng.randint(1, max(1, max_a // m))
    elif roll < 0.15:
        a = 1
    else:
        a = rng.randint(0, max_a)
    a = min(a, max_a)
    roll = rng.random()
    if roll < 0.05:
        b = 0
    elif roll < 0.10:
        b = 1
    elif roll < 0.25:
        b = max_b
    else:
        b = rng.randint(0, max_b)
    return a, b, m


def case(rng: random.Random, q: int, max_b: int, max_a: int, fixed: list[tuple[int, int, int]]) -> str:
    rows = list(fixed)
    while len(rows) < q:
        rows.append(query(rng, max_b, max_a))
    rows = rows[:q]
    return "\n".join([str(q)] + [f"{a} {b} {m}" for a, b, m in rows]) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    edge = [(0, 0, 7), (0, 0, 1), (0, 3, 5), (5, 0, 1), (10**9, 1, 10**9), (10**9 - 1, 2, 10**9)]
    # Case 6 opens with a huge exponent so the naive loop times out on its first query.
    huge = [(2, BIG, 998244353), (BIG, BIG, 10**9), (BIG - 1, BIG - 1, 999999937)]
    plans = [
        (1, 10, 10, []),
        (8, 20, 100, edge),
        (100, 1000, BIG, edge),
        (1000, 10**4, BIG, edge),
        (1000, 10**4, BIG, [(BIG, 10**4, 10**9)] * 3),
        (10**4, BIG, BIG, huge + edge),
        (10**4, BIG, 10**9, huge),
        (10**4, BIG, BIG, huge),
        (10**4, 10**9, BIG, edge),
        (10**4, BIG, BIG, huge + edge),
    ]
    for index, (q, max_b, max_a, fixed) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 100 * index + 7)
        (out / f"input{index:02d}.txt").write_text(case(rng, q, max_b, max_a, fixed), encoding="utf-8")


if __name__ == "__main__":
    main()
