#!/usr/bin/env python3
"""Testcase generator for lp_lazy01_coin_towers.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q up to
50,000. Cases 7 and 10 use only near-whole-row events, so adding pile by pile
(slow.cpp, O(N Q)) must time out there; case 10 is also the largest total
(about 2.5 * 10^18, so 32-bit sums, or a tag multiplied in 32 bits, overflow).
Covers N = 1, one-pile ranges, empty starting piles, overlapping rains and
questions right after a rain on exactly the same range.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9
MAX_NQ = 5 * 10**4


def write(out: Path, index: int, a: list[int], ops: list[tuple]) -> None:
    n, q = len(a), len(ops)
    assert 1 <= n <= MAX_NQ and 1 <= q <= MAX_NQ
    assert all(0 <= v <= LIMIT for v in a)
    for op in ops:
        if op[0] == 1:
            assert len(op) == 4 and 1 <= op[1] <= op[2] <= n and 1 <= op[3] <= LIMIT
        else:
            assert op[0] == 2 and len(op) == 3 and 1 <= op[1] <= op[2] <= n
    assert any(op[0] == 2 for op in ops)
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    lines = [f"{n} {q}", " ".join(map(str, a))]
    lines.extend(" ".join(map(str, op)) for op in ops)
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rand_range(rng, n, min_len=1):
    length = rng.randint(min(min_len, n), n)
    l = rng.randint(1, n - length + 1)
    return l, l + length - 1


def random_ops(rng, n, q, max_v, add_share, min_len=1):
    ops = []
    for _ in range(q):
        l, r = rand_range(rng, n, min_len)
        if rng.random() < add_share:
            ops.append((1, l, r, rng.randint(1, max_v)))
        else:
            ops.append((2, l, r))
    if all(op[0] == 1 for op in ops):
        ops[-1] = (2, 1, n)
    return ops


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append(([0], [(2, 1, 1), (1, 1, 1, LIMIT), (2, 1, 1), (1, 1, 1, 1), (2, 1, 1)]))
    cases.append(([5, 0, 3, 0, 0, 7, 1, 2],
                  [(1, 1, 8, 1), (2, 1, 8), (1, 3, 6, 4), (2, 3, 6), (2, 2, 3), (2, 6, 7),
                   (1, 5, 5, 10), (2, 4, 5), (2, 5, 5), (1, 2, 7, 3), (2, 1, 1), (2, 8, 8),
                   (2, 1, 8), (1, 1, 4, 2), (2, 4, 6)]))
    rng = random.Random(20261120 + 3401)
    cases.append(([rng.randint(0, 100) for _ in range(1000)], random_ops(rng, 1000, 1000, 100, 0.5)))
    rng = random.Random(20261120 + 3402)
    cases.append(([rng.randint(0, LIMIT) for _ in range(5000)], random_ops(rng, 5000, 5000, LIMIT, 0.5)))
    # empty piles; rains then the same range is asked right away
    rng = random.Random(20261120 + 3403)
    ops = []
    while len(ops) < 5000:
        l, r = rand_range(rng, 5000)
        ops.append((1, l, r, rng.randint(1, LIMIT)))
        ops.append((2, l, r) if rng.random() < 0.5 else (2, *rand_range(rng, 5000)))
    cases.append(([0] * 5000, ops[:5000]))
    # short ranges and single piles
    rng = random.Random(20261120 + 3404)
    ops = []
    for _ in range(5000):
        l = rng.randint(1, 5000)
        r = min(5000, l + rng.randint(0, 3))
        ops.append((1, l, r, rng.randint(1, LIMIT)) if rng.random() < 0.5 else (2, l, r))
    cases.append(([rng.randint(0, LIMIT) for _ in range(5000)], ops))
    # first large case: near-whole-row events only
    rng = random.Random(20261120 + 3405)
    ops = []
    for _ in range(MAX_NQ):
        l, r = rng.randint(1, 100), MAX_NQ - rng.randint(0, 99)
        ops.append((1, l, r, rng.randint(1, 10**6)) if rng.random() < 0.6 else (2, l, r))
    cases.append(([rng.randint(0, 10**6) for _ in range(MAX_NQ)], ops))
    rng = random.Random(20261120 + 3406)
    cases.append(([rng.randint(0, LIMIT) for _ in range(40000)], random_ops(rng, 40000, 40000, LIMIT, 0.5)))
    rng = random.Random(20261120 + 3407)
    ops = []
    for _ in range(MAX_NQ):
        l = rng.randint(1, MAX_NQ)
        r = min(MAX_NQ, l + rng.randint(0, 200))
        ops.append((1, l, r, rng.randint(1, 1000)) if rng.random() < 0.5 else (2, *rand_range(rng, MAX_NQ)))
    cases.append(([rng.randint(0, 1000) for _ in range(MAX_NQ)], ops))
    # the biggest totals: full piles, 90% maximal rains on the whole row
    rng = random.Random(20261120 + 3408)
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.9:
            ops.append((1, 1, MAX_NQ, LIMIT) if rng.random() < 0.8 else (1, 1, rng.randint(MAX_NQ - 100, MAX_NQ), LIMIT))
        else:
            ops.append((2, rng.randint(1, 100), MAX_NQ - rng.randint(0, 99)))
    ops[-1] = (2, 1, MAX_NQ)
    cases.append(([LIMIT] * MAX_NQ, ops))
    for index, (a, ops) in enumerate(cases, start=1):
        write(out, index, a, ops)


if __name__ == "__main__":
    main()
