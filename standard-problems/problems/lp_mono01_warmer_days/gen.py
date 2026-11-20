#!/usr/bin/env python3
"""Testcase generator for lp_mono01_warmer_days.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000. Cases 7
(all equal) and 10 (strictly falling, then one hot day at the end) make the
forward walk of slow.cpp ~N^2/2 steps, so it must time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**5


def write(out: Path, index: int, t: list[int]) -> None:
    assert 1 <= len(t) <= 10**5
    assert all(-LIMIT <= x <= LIMIT for x in t)
    if index <= 3:
        assert len(t) <= 1000
    elif index <= 6:
        assert len(t) <= 5000
    text = f"{len(t)}\n{' '.join(map(str, t))}\n"
    (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


def falling_with_plateaus(rng: random.Random, n: int) -> list[int]:
    values, current = [], LIMIT
    while len(values) < n:
        values.extend([current] * rng.randint(1, 5))
        current -= rng.randint(0, 3)
        current = max(current, -LIMIT)
    return values[:n]


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append([-LIMIT])                                               # N = 1
    cases.append([5, 3, 3, 8, -1, 8, 2, 9, 9, 1])
    rng = random.Random(20261120 + 801)
    cases.append([rng.randint(-20, 20) for _ in range(1000)])            # many ties
    cases.append([7] * 5000)                                             # all equal: all zeros
    rng = random.Random(20261120 + 802)
    cases.append(sorted(rng.randint(-LIMIT, LIMIT) for _ in range(5000)))  # rising (with ties)
    rng = random.Random(20261120 + 803)
    cases.append(falling_with_plateaus(rng, 5000))
    cases.append([LIMIT] * 100000)                                       # slow.cpp must TLE here
    rng = random.Random(20261120 + 804)
    cases.append([rng.randint(-LIMIT, LIMIT) for _ in range(100000)])
    rng = random.Random(20261120 + 805)
    saw = []
    while len(saw) < 100000:                                             # falling runs, then a spike
        top = rng.randint(0, LIMIT)
        run = rng.randint(1, 3000)
        saw.extend(max(-LIMIT, top - k) for k in range(run))
    cases.append(saw[:100000])
    cases.append(list(range(LIMIT - 1, LIMIT - 100000, -1)) + [LIMIT])   # every answer reaches the end
    for index, t in enumerate(cases, start=1):
        write(out, index, t)


if __name__ == "__main__":
    main()
