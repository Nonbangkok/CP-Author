#!/usr/bin/env python3
"""Testcase generator for lp_seg02_best_streak.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q up to 50,000.
Case 7 asks only near-whole-row questions, so a fresh Kadane scan over [l, r]
for every question (slow.cpp, O(N Q)) must time out there. Covers N = 1,
all-negative ranges (the answer is the single largest day), all-positive
ranges (the answer is the whole sum, beyond 32 bits), best streaks that cross
the middle of a node, and extreme values.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9
MAX_NQ = 5 * 10**4


def write(out: Path, index: int, a: list[int], ops: list[tuple[int, int, int]]) -> None:
    n, q = len(a), len(ops)
    assert 1 <= n <= MAX_NQ and 1 <= q <= MAX_NQ
    assert all(-LIMIT <= v <= LIMIT for v in a)
    for kind, x, y in ops:
        if kind == 1:
            assert 1 <= x <= n and -LIMIT <= y <= LIMIT
        else:
            assert kind == 2 and 1 <= x <= y <= n
    assert any(kind == 2 for kind, _x, _y in ops)
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    lines = [f"{n} {q}", " ".join(map(str, a))]
    lines.extend(f"{kind} {x} {y}" for kind, x, y in ops)
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def random_ops(rng, n, q, value, update_share, min_len=1):
    ops = []
    for _ in range(q):
        if rng.random() < update_share:
            ops.append((1, rng.randint(1, n), value()))
        else:
            length = rng.randint(min(min_len, n), n)
            l = rng.randint(1, n - length + 1)
            ops.append((2, l, l + length - 1))
    if all(kind == 1 for kind, _x, _y in ops):
        ops[-1] = (2, 1, n)
    return ops


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append(([-LIMIT], [(2, 1, 1), (1, 1, LIMIT), (2, 1, 1), (1, 1, 0), (2, 1, 1)]))
    cases.append(([2, -1, 2, -10, 6, -1, -1, 6, -20, 1],
                  [(2, 1, 10), (2, 1, 4), (2, 4, 9), (2, 9, 9), (1, 4, 10), (2, 1, 10),
                   (2, 2, 3), (1, 9, 25), (2, 1, 10), (2, 6, 7), (1, 1, -3), (2, 1, 3)]))
    rng = random.Random(20261120 + 3201)
    small = lambda: rng.randint(-100, 100)
    cases.append(([small() for _ in range(1000)], random_ops(rng, 1000, 1000, small, 0.5)))
    rng = random.Random(20261120 + 3202)
    big = lambda: rng.randint(-LIMIT, LIMIT)
    cases.append(([big() for _ in range(5000)], random_ops(rng, 5000, 5000, big, 0.4)))
    # all negative: every answer is the largest single day of the range
    rng = random.Random(20261120 + 3203)
    neg = lambda: rng.randint(-LIMIT, -1)
    cases.append(([neg() for _ in range(5000)], random_ops(rng, 5000, 5000, neg, 0.4)))
    # all positive and huge: the answer is the whole range, far beyond int
    rng = random.Random(20261120 + 3204)
    pos = lambda: rng.randint(LIMIT - 1000, LIMIT)
    cases.append(([pos() for _ in range(5000)], random_ops(rng, 5000, 5000, pos, 0.3)))
    # first large case: only wide questions, so slow.cpp scans ~N per question
    rng = random.Random(20261120 + 3205)
    a = [rng.randint(-LIMIT, LIMIT) for _ in range(MAX_NQ)]
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.3:
            ops.append((1, rng.randint(1, MAX_NQ), rng.randint(-LIMIT, LIMIT)))
        else:
            ops.append((2, rng.randint(1, 100), MAX_NQ - rng.randint(0, 99)))
    cases.append((a, ops))
    # slightly negative drift (values up to 10^6): best streaks are long but not the whole range
    rng = random.Random(20261120 + 3206)
    drift = lambda: rng.randint(-10**6, 10**6 - 2 * 10**4)
    cases.append(([drift() for _ in range(MAX_NQ)], random_ops(rng, MAX_NQ, MAX_NQ, drift, 0.5)))
    # blocks of positives (up to 10^6) separated by deep negatives; updates break or join blocks
    rng = random.Random(20261120 + 3207)
    a = []
    while len(a) < 40000:
        a.extend(rng.randint(1, 10**6) for _ in range(rng.randint(1, 300)))
        a.append(-LIMIT)
    a = a[:40000]
    flip = lambda: rng.choice([-LIMIT, 10**6, rng.randint(-10**6, 10**6)])
    cases.append((a, random_ops(rng, 40000, 40000, flip, 0.3)))
    rng = random.Random(20261120 + 3208)
    cases.append(([rng.randint(-LIMIT, LIMIT) for _ in range(MAX_NQ)],
                  random_ops(rng, MAX_NQ, MAX_NQ, lambda: rng.randint(-LIMIT, LIMIT), 0.35, min_len=MAX_NQ // 2)))
    for index, (a, ops) in enumerate(cases, start=1):
        write(out, index, a, ops)


if __name__ == "__main__":
    main()
