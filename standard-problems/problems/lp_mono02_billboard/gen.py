#!/usr/bin/env python3
"""Testcase generator for lp_mono02_billboard.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000, where the
O(N^2) scan over every block of buildings must time out. Covers N = 1, all
equal (answer = everything, up to 10^18), rising, a mountain, few heights.
"""

import random
import sys
from pathlib import Path

MAX_W, MAX_H = 10**4, 10**9


def write(out: Path, index: int, rows: list[tuple[int, int]]) -> None:
    n = len(rows)
    assert 1 <= n <= 10**5
    assert all(1 <= w <= MAX_W and 1 <= h <= MAX_H for w, h in rows)
    if index <= 3:
        assert n <= 1000
    elif index <= 6:
        assert n <= 5000
    text = f"{n}\n" + "".join(f"{w} {h}\n" for w, h in rows)
    (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append([(MAX_W, MAX_H)])                                            # N = 1
    rng = random.Random(20261120 + 811)
    cases.append([(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(10)])
    rng = random.Random(20261120 + 812)
    cases.append([(rng.randint(1, MAX_W), rng.randint(1, MAX_H)) for _ in range(1000)])
    cases.append([(MAX_W, MAX_H)] * 5000)                                     # all equal
    rng = random.Random(20261120 + 813)
    cases.append([(rng.randint(1, 100), h) for h in sorted(rng.randint(1, 10**6) for _ in range(5000))])
    rng = random.Random(20261120 + 814)
    cases.append([(rng.randint(1, MAX_W), rng.randint(1, 20)) for _ in range(5000)])
    rng = random.Random(20261120 + 815)
    cases.append([(rng.randint(1, MAX_W), rng.randint(1, MAX_H)) for _ in range(100000)])  # slow.cpp must TLE here
    cases.append([(MAX_W, MAX_H)] * 100000)                                   # answer 10^18
    rng = random.Random(20261120 + 816)
    up = sorted(rng.randint(1, 10**5) for _ in range(50000))
    down = sorted((rng.randint(1, 10**5) for _ in range(50000)), reverse=True)
    cases.append([(rng.randint(1, 50), h) for h in up + down])                # a mountain
    rng = random.Random(20261120 + 817)
    cases.append([(rng.randint(1, 100), rng.randint(1, 5)) for _ in range(100000)])
    for index, rows in enumerate(cases, start=1):
        write(out, index, rows)


if __name__ == "__main__":
    main()
