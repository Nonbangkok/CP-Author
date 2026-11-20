#!/usr/bin/env python3
"""Testcase generator for lp_dp03_lakeside_stalls.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 20; cases 4-10 N <= 10^5. Case 4 (N = 70, ~10^14 valid
choices) is already too many to try one by one. Covers N = 3 (one spot at
most), all zeros, an odd circle of equal values (the straight-line answer is
one spot too many), heavy ends that a non-circular DP would wrongly take
together, alternating big/small, and 64-bit totals.
"""

import random
import sys
from pathlib import Path

MAX_N, MAX_A = 10**5, 10**9


def write(out: Path, index: int, a: list[int]) -> None:
    n = len(a)
    assert 3 <= n <= MAX_N and all(0 <= x <= MAX_A for x in a)
    if index <= 3:
        assert n <= 20
    (out / f"input{index:02d}.txt").write_text(f"{n}\n{' '.join(map(str, a))}\n", encoding="utf-8")


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261203)
    write(out, 1, [5, 9, 4])                                                  # N = 3: one spot at most
    write(out, 2, [0] * 7)                                                    # all zeros: answer 0
    write(out, 3, [rng.randint(0, 100) for _ in range(20)])
    write(out, 4, [rng.randint(0, 1000) for _ in range(70)])                  # first big case: enumeration must TLE
    write(out, 5, [MAX_A] * (MAX_N - 1))                                      # odd circle of equal values
    ends = [rng.randint(0, 1000) for _ in range(MAX_N)]
    ends[0] = ends[-1] = MAX_A                                                # a line DP would take both ends
    write(out, 6, ends)
    write(out, 7, [MAX_A if i % 2 == 0 else rng.randint(0, 10) for i in range(MAX_N - 1)])
    write(out, 8, [rng.choice([0, 0, 0, rng.randint(0, MAX_A)]) for _ in range(MAX_N)])
    write(out, 9, [rng.randint(0, 5) for _ in range(MAX_N)])                  # many ties
    write(out, 10, [rng.randint(0, MAX_A) for _ in range(MAX_N)])


if __name__ == "__main__":
    main()
