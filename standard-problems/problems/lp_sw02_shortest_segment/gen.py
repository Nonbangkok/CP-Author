#!/usr/bin/env python3
"""Testcase generator for lp_sw02_shortest_segment.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000. Cases 7
and 10 need a window of half the array or have no answer at all, so extending
every start until it reaches S (O(N^2)) must time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, high: int, need: str | int) -> str:
    values = [rng.randint(1, high) for _ in range(n)]
    total = sum(values)
    if need == "half":
        s = total // 2
    elif need == "none":
        s = total + 1                 # nobody can reach S: answer -1
    elif need == "total":
        s = total                     # only the whole array works
    elif need == "short":
        s = (total // n) * rng.randint(3, 40)
    else:
        s = int(need)
    s = max(1, min(s, 10**15))
    return f"{n} {s}\n{' '.join(map(str, values))}\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 10, 1),                   # one cell is enough
        (12, 9, 20),
        (1000, 1000, "total"),
        (5000, LIMIT, LIMIT),         # some single cell may already be enough
        (5000, 100, "none"),
        (5000, LIMIT, "short"),
        (100000, 1000, "half"),       # first large case: slow.cpp must TLE here
        (100000, LIMIT, "short"),     # sums far above int
        (100000, LIMIT, 10**15),      # S above the total of any array: -1
        (100000, 50, "none"),
    ]
    for index, (n, high, need) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 503 * index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, high, need), encoding="utf-8")


if __name__ == "__main__":
    main()
