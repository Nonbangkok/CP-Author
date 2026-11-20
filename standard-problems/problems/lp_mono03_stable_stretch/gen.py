#!/usr/bin/env python3
"""Testcase generator for lp_mono03_stable_stretch.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000. Cases 7
and 10 have stable stretches tens of thousands long, so extending from every
start (slow.cpp) needs ~10^9 steps and must time out there. Covers N = 1,
D = 0, D = 10^9 (whole array), ties between longest stretches.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def write(out: Path, index: int, d: int, a: list[int]) -> None:
    n = len(a)
    assert 1 <= n <= 10**5 and 0 <= d <= LIMIT
    assert all(0 <= v <= LIMIT for v in a)
    if index <= 3:
        assert n <= 1000
    elif index <= 6:
        assert n <= 5000
    text = f"{n} {d}\n{' '.join(map(str, a))}\n"
    (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


def walk(rng: random.Random, n: int, step: int, base: int) -> list[int]:
    values, current = [], base
    for _ in range(n):
        current = min(LIMIT, max(0, current + rng.randint(-step, step)))
        values.append(current)
    return values


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append((0, [LIMIT]))                                                  # N = 1
    cases.append((2, [3, 1, 2, 5, 4, 4, 9, 8, 7, 1]))                           # two longest of length 3
    rng = random.Random(20261120 + 821)
    cases.append((15, walk(rng, 1000, 5, 500)))
    rng = random.Random(20261120 + 822)
    cases.append((0, [rng.choice([4, 4, 4, 9]) for _ in range(5000)]))         # D = 0: equal runs
    rng = random.Random(20261120 + 823)
    cases.append((LIMIT, [rng.randint(0, LIMIT) for _ in range(5000)]))        # whole array
    rng = random.Random(20261120 + 824)
    cases.append((1000, walk(rng, 5000, 100, 10**6)))
    rng = random.Random(20261120 + 825)
    cases.append((LIMIT, [rng.randint(0, LIMIT) for _ in range(100000)]))      # slow.cpp must TLE here
    rng = random.Random(20261120 + 826)
    cases.append((10**6, [rng.randint(0, LIMIT) for _ in range(100000)]))      # short stretches only
    rng = random.Random(20261120 + 827)
    cases.append((5000, walk(rng, 100000, 50, 5 * 10**5)))
    cases.append((50000, list(range(100000))))                                 # every stretch is 50,001 long
    for index, (d, a) in enumerate(cases, start=1):
        write(out, index, d, a)


if __name__ == "__main__":
    main()
