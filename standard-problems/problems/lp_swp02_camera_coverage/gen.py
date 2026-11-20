#!/usr/bin/env python3
"""Testcase generator for lp_swp02_camera_coverage.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 3,000; cases 7-10 N up to 100,000, where
re-counting the cameras over every elementary piece (slow.cpp, O(N^2)) must
time out. Covers N = 1, identical cameras (S_k = full length for every k),
touching endpoints, disjoint cameras, nested cameras.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def write(out: Path, index: int, cams: list[tuple[int, int]]) -> None:
    n = len(cams)
    assert 1 <= n <= 10**5
    assert all(0 <= l < r <= LIMIT for l, r in cams)
    if index <= 3:
        assert n <= 1000
    elif index <= 6:
        assert n <= 3000
    text = f"{n}\n" + "".join(f"{l} {r}\n" for l, r in cams)
    (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


def random_cams(rng: random.Random, n: int, horizon: int, longest: int) -> list[tuple[int, int]]:
    cams = []
    for _ in range(n):
        l = rng.randint(0, horizon - 1)
        r = min(horizon, l + rng.randint(1, longest))
        cams.append((l, r))
    return cams


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append([(0, LIMIT)])                                                  # N = 1
    cases.append([(3, 7), (7, 9), (0, 3), (3, 7), (5, 6), (1, 2), (8, 12), (2, 4)])
    rng = random.Random(20261120 + 911)
    cases.append(random_cams(rng, 1000, 200, 30))                               # lots of shared endpoints
    cases.append([(10, 10 + 7 * 3000)] * 3000)                                  # identical
    cases.append([(i * 5, i * 5 + 5) for i in range(3000)])                     # touching chain: S_2 = 0
    rng = random.Random(20261120 + 912)
    cases.append(random_cams(rng, 3000, LIMIT, 10**8))
    rng = random.Random(20261120 + 913)
    cases.append(random_cams(rng, 100000, LIMIT, 10**7))                        # slow.cpp must TLE here
    cases.append([(i, LIMIT - i) for i in range(30000)])                        # nested
    rng = random.Random(20261120 + 914)
    cases.append(random_cams(rng, 80000, 10**5, 500))
    rng = random.Random(20261120 + 915)
    cases.append(random_cams(rng, 50000, LIMIT, 10**6))
    for index, cams in enumerate(cases, start=1):
        rng = random.Random(index)
        rng.shuffle(cams)
        write(out, index, cams)


if __name__ == "__main__":
    main()
