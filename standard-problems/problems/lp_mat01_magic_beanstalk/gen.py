#!/usr/bin/env python3
"""Testcase generator for lp_mat01_magic_beanstalk.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000 (N = 0 and N = 1 edge cases); cases 4-5 N <= 10^7 (the
day-by-day loop still passes); cases 6-10 N up to 10^18, the first of them
N = 10^18 so the O(N) loop must time out. Also covers all-maximal values,
a = b = 0 (constant from day 2), a = 1, b = 0, c = 1 (linear growth), c = 0,
and an exponent whose binary form is all ones.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9
NMAX = 10**18


def main() -> None:
    out = Path(sys.argv[1])
    # (a, b, c, f0, f1, n); None = random in [0, 10^9]
    plans = [
        (None, None, None, None, None, 0),
        (None, None, None, None, None, 1),
        (None, None, None, None, None, 1000),
        (None, None, None, None, None, 10**7),
        (0, LIMIT, LIMIT, LIMIT, 7, 10**7 - 1),
        (None, None, None, None, None, NMAX),
        (LIMIT, LIMIT, LIMIT, LIMIT, LIMIT, NMAX - 1),
        (None, None, 0, None, None, 2**59 - 1),
        (0, 0, 123456789, 5, 6, 999999999999999989),
        (1, 0, 1, 0, 987654321, 876543210987654321),
    ]
    for index, plan in enumerate(plans, start=1):
        rng = random.Random(20261120 + index)
        a, b, c, f0, f1, n = (rng.randint(0, LIMIT) if v is None else v for v in plan)
        for v in (a, b, c, f0, f1):
            assert 0 <= v <= LIMIT
        assert 0 <= n <= NMAX
        if index <= 3:
            assert n <= 1000
        elif index <= 5:
            assert n <= 10**7
        (out / f"input{index:02d}.txt").write_text(f"{a} {b} {c}\n{f0} {f1} {n}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
