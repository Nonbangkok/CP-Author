#!/usr/bin/env python3
"""Testcase generator for lp_swp03_low_awning.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q up to
50,000, where checking every awning for every truck (slow.cpp, O(N Q)) must
time out (cases 7 and 10 are full size). Covers points on both ends
(inclusive), one-point awnings, equal heights (erase one copy only), nested
awnings, uncovered points, duplicate and unsorted queries.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def write(out: Path, index: int, awnings: list[tuple[int, int, int]], points: list[int]) -> None:
    n, q = len(awnings), len(points)
    assert 1 <= n <= 5 * 10**4 and 1 <= q <= 5 * 10**4
    assert all(0 <= l <= r <= LIMIT and 1 <= h <= LIMIT for l, r, h in awnings)
    assert all(0 <= p <= LIMIT for p in points)
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    text = f"{n} {q}\n" + "".join(f"{l} {r} {h}\n" for l, r, h in awnings) + " ".join(map(str, points)) + "\n"
    (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


def random_awnings(rng, n, horizon, longest, max_h):
    result = []
    for _ in range(n):
        l = rng.randint(0, horizon)
        r = min(horizon, l + rng.randint(0, longest))
        result.append((l, r, rng.randint(1, max_h)))
    return result


def endpoint_points(rng, awnings, q, horizon):
    """Mix of exact ends, one past the ends, and random points."""
    points = []
    for _ in range(q):
        l, r, _h = rng.choice(awnings)
        pick = rng.randint(0, 4)
        p = [l, r, max(0, l - 1), min(horizon, r + 1), rng.randint(0, horizon)][pick]
        points.append(p)
    return points


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append(([(0, LIMIT, LIMIT)], [LIMIT]))                                 # N = Q = 1, far end
    cases.append(([(1, 4, 6), (4, 4, 6), (4, 9, 2), (6, 8, 6), (10, 10, 1)],
                  [0, 1, 4, 5, 9, 10, 11, 4, 8]))
    rng = random.Random(20261120 + 921)
    aw = random_awnings(rng, 1000, 2000, 100, 50)
    cases.append((aw, endpoint_points(rng, aw, 1000, 2000)))
    rng = random.Random(20261120 + 922)
    aw = [(i, 10000 - i, 5000 - i) for i in range(5000)]                        # nested, lower inside
    cases.append((aw, [rng.randint(0, 10000) for _ in range(5000)]))
    rng = random.Random(20261120 + 923)
    aw = [(rng.randint(0, 100), rng.randint(100, 200), rng.randint(1, 3)) for _ in range(5000)]  # many equal heights
    cases.append((aw, endpoint_points(rng, aw, 5000, 200)))
    rng = random.Random(20261120 + 924)
    aw = random_awnings(rng, 5000, LIMIT, 10**5, LIMIT)                          # sparse: many -1
    cases.append((aw, endpoint_points(rng, aw, 5000, LIMIT)))
    rng = random.Random(20261120 + 925)
    aw = random_awnings(rng, 50000, 10**6, 10**5, 10**6)                         # slow.cpp must TLE here
    cases.append((aw, endpoint_points(rng, aw, 50000, 10**6)))
    rng = random.Random(20261120 + 926)
    aw = [(rng.randint(0, 1000), rng.randint(0, 1000), 7) for _ in range(20000)]
    aw = [(min(l, r), max(l, r), h) for l, r, h in aw]                           # all the same height
    cases.append((aw, [rng.randint(0, 1000) for _ in range(20000)]))
    rng = random.Random(20261120 + 927)
    aw = random_awnings(rng, 30000, LIMIT, 10**4, LIMIT)
    cases.append((aw, endpoint_points(rng, aw, 30000, LIMIT)))
    rng = random.Random(20261120 + 928)
    aw = [(rng.randint(0, 5 * 10**4), rng.randint(5 * 10**4, 10**5), rng.randint(1, 10**6)) for _ in range(50000)]
    cases.append((aw, [rng.randint(0, 10**5) for _ in range(50000)]))
    for index, (aw, pts) in enumerate(cases, start=1):
        write(out, index, aw, pts)


if __name__ == "__main__":
    main()
