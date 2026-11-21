#!/usr/bin/env python3
"""Testcase generator for lp_seg03_tall_enough.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q up to
50,000. In case 7 almost every car is taller than every bay near the start of
a wide range, so walking from l (slow.cpp, O(N Q)) covers ~N bays per car and
must time out there. Covers N = 1, equal heights (>= is inclusive), the answer
exactly at l or at r, answers just outside [l, r] (must give -1), and bays
that get lower as well as higher.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9
MAX_NQ = 5 * 10**4


def write(out: Path, index: int, h: list[int], ops: list[tuple]) -> None:
    n, q = len(h), len(ops)
    assert 1 <= n <= MAX_NQ and 1 <= q <= MAX_NQ
    assert all(1 <= v <= LIMIT for v in h)
    for op in ops:
        if op[0] == 1:
            assert len(op) == 3 and 1 <= op[1] <= n and 1 <= op[2] <= LIMIT
        else:
            assert op[0] == 2 and len(op) == 4 and 1 <= op[1] <= op[2] <= n and 1 <= op[3] <= LIMIT
    assert any(op[0] == 2 for op in ops)
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    lines = [f"{n} {q}", " ".join(map(str, h))]
    lines.extend(" ".join(map(str, op)) for op in ops)
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def random_ops(rng, h, q, max_v, update_share, min_len=1):
    """Random cars; about half are exactly as tall as some current bay."""
    n = len(h)
    cur = list(h)
    ops = []
    for _ in range(q):
        if rng.random() < update_share:
            i, y = rng.randint(1, n), rng.randint(1, max_v)
            cur[i - 1] = y
            ops.append((1, i, y))
        else:
            length = rng.randint(min(min_len, n), n)
            l = rng.randint(1, n - length + 1)
            x = cur[rng.randint(0, n - 1)] if rng.random() < 0.5 else rng.randint(1, max_v)
            ops.append((2, l, l + length - 1, x))
    if all(op[0] == 1 for op in ops):
        ops[-1] = (2, 1, n, 1)
    return ops


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append(([LIMIT], [(2, 1, 1, LIMIT), (1, 1, 1), (2, 1, 1, 2), (2, 1, 1, 1)]))
    # hand-made: answers at l, at r, just past r, equal heights
    cases.append(([3, 9, 4, 9, 2, 7, 7, 1],
                  [(2, 1, 8, 9), (2, 3, 8, 9), (2, 5, 8, 8), (2, 5, 7, 7), (2, 6, 6, 7),
                   (2, 1, 1, 4), (2, 3, 3, 4), (1, 4, 1), (2, 3, 8, 9), (1, 8, 10),
                   (2, 1, 8, 10), (2, 1, 7, 10), (2, 8, 8, 10), (1, 2, 1), (2, 1, 8, 5)]))
    rng = random.Random(20261120 + 3301)
    h = [rng.randint(1, 100) for _ in range(1000)]
    cases.append((h, random_ops(rng, h, 1000, 100, 0.4)))
    rng = random.Random(20261120 + 3302)
    h = [rng.randint(1, LIMIT) for _ in range(5000)]
    cases.append((h, random_ops(rng, h, 5000, LIMIT, 0.4)))
    # all bays equal; cars as tall as the bays or one taller
    rng = random.Random(20261120 + 3303)
    ops = []
    for _ in range(5000):
        if rng.random() < 0.3:
            ops.append((1, rng.randint(1, 5000), rng.choice([500, 501])))
        else:
            l = rng.randint(1, 5000)
            ops.append((2, l, rng.randint(l, 5000), rng.choice([500, 501])))
    cases.append(([500] * 5000, ops))
    # rising bays: the answer is the first index past a threshold
    rng = random.Random(20261120 + 3304)
    h = [2 * i for i in range(1, 5001)]
    cases.append((h, random_ops(rng, h, 5000, 10000, 0.2)))
    # first large case: low bays, a few tall ones at the far end, tall cars
    rng = random.Random(20261120 + 3305)
    h = [rng.randint(1, LIMIT // 2) for _ in range(MAX_NQ)]
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.05:
            i = rng.randint(1, MAX_NQ)
            y = rng.randint(LIMIT // 2, LIMIT) if i > MAX_NQ - 200 else rng.randint(1, LIMIT // 2)
            ops.append((1, i, y))
        else:
            ops.append((2, rng.randint(1, 100), MAX_NQ - rng.randint(0, 50), rng.randint(LIMIT // 2 + 1, LIMIT)))
    cases.append((h, ops))
    rng = random.Random(20261120 + 3306)
    h = [rng.randint(1, LIMIT) for _ in range(40000)]
    cases.append((h, random_ops(rng, h, 40000, LIMIT, 0.5)))
    # heights from a few values, cars from the same values
    rng = random.Random(20261120 + 3308)
    h = [rng.choice([10, 20, 30, 40]) for _ in range(MAX_NQ)]
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.3:
            ops.append((1, rng.randint(1, MAX_NQ), rng.choice([10, 20, 30, 40, 50])))
        else:
            l = rng.randint(1, MAX_NQ)
            ops.append((2, l, rng.randint(l, MAX_NQ), rng.choice([10, 20, 30, 40, 50, 60])))
    cases.append((h, ops))
    # falling bays and wide ranges: tall ones are on the left, so a car taller
    # than bay l walks to r and gets -1 (slow.cpp is far over the limit here too)
    rng = random.Random(20261120 + 3307)
    h = [MAX_NQ - i for i in range(MAX_NQ)]
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.1:
            i = rng.randint(1, MAX_NQ)
            ops.append((1, i, rng.randint(1, h[i - 1])))  # bays only get lower
        else:
            l = rng.randint(1, MAX_NQ // 2)
            # mostly taller than bay l (then every bay to its right is lower too)
            x = rng.randint(MAX_NQ - l + 2, MAX_NQ + 1) if rng.random() < 0.8 else rng.randint(1, MAX_NQ)
            ops.append((2, l, rng.randint(MAX_NQ - 100, MAX_NQ), x))
    cases.append((h, ops))
    for index, (h, ops) in enumerate(cases, start=1):
        write(out, index, h, ops)


if __name__ == "__main__":
    main()
