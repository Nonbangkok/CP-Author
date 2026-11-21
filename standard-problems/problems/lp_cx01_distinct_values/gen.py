#!/usr/bin/env python3
"""Testcase generator for lp_cx01_distinct_values.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 10,000; cases 7-10 N = 100,000. Case 7
is all distinct -- the worst case for the O(N^2) scan, which then never stops
early -- so the naive solution must time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def distinct(rng: random.Random, n: int) -> list[int]:
    return rng.sample(range(-LIMIT, LIMIT + 1), n)


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261120)
    cases: list[list[int]] = [
        [LIMIT],
        [rng.randint(-3, 3) for _ in range(100)],
        distinct(rng, 1000),
        [rng.randint(-50, 50) for _ in range(10000)],
        [rng.randint(-LIMIT, LIMIT) for _ in range(10000)],
        distinct(rng, 10000),
        distinct(rng, 100000),
        [rng.randint(0, 1000) for _ in range(100000)],
        [x for x in distinct(rng, 50000) for _ in range(2)],
        [-LIMIT, LIMIT] * 10 + distinct(rng, 99980),
    ]
    for index, values in enumerate(cases, start=1):
        if index in (9, 10):
            random.Random(20261120 + index).shuffle(values)
        assert 1 <= len(values) <= 100000 and all(-LIMIT <= v <= LIMIT for v in values)
        text = f"{len(values)}\n" + " ".join(map(str, values)) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
