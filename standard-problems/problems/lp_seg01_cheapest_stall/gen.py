#!/usr/bin/env python3
"""Testcase generator for lp_seg01_cheapest_stall.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N = Q = 50,000.
Case 7 asks only near-whole-row questions, so scanning [l, r] for every
question (slow.cpp, O(N Q)) must time out there. Covers N = 1, one-stall
ranges, the minimum at either end of a range, equal prices, extreme prices,
a price set to the value it already has, and rising/falling rows.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9
MAX_NQ = 5 * 10**4


def write(out: Path, index: int, a: list[int], ops: list[tuple[int, int, int]]) -> None:
    n, q = len(a), len(ops)
    assert 1 <= n <= MAX_NQ and 1 <= q <= MAX_NQ
    assert all(1 <= v <= LIMIT for v in a)
    for kind, x, y in ops:
        if kind == 1:
            assert 1 <= x <= n and 1 <= y <= LIMIT
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


def random_ops(rng, n, q, max_v, update_share, min_len=1):
    ops = []
    for _ in range(q):
        if rng.random() < update_share:
            ops.append((1, rng.randint(1, n), rng.randint(1, max_v)))
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
    cases.append(([LIMIT], [(2, 1, 1), (1, 1, 1), (2, 1, 1), (1, 1, 1), (2, 1, 1)]))
    cases.append(([4, 4, 9, 1, 7, 7, 3, 10],
                  [(2, 1, 8), (2, 5, 8), (2, 4, 4), (1, 4, 20), (2, 1, 8), (2, 1, 3),
                   (1, 1, 2), (2, 1, 2), (2, 2, 8), (1, 8, 1), (2, 6, 8), (2, 8, 8)]))
    rng = random.Random(20261120 + 3101)
    cases.append(([rng.randint(1, 100) for _ in range(1000)], random_ops(rng, 1000, 1000, 100, 0.5)))
    rng = random.Random(20261120 + 3102)
    cases.append(([rng.randint(1, LIMIT) for _ in range(5000)], random_ops(rng, 5000, 5000, LIMIT, 0.4)))
    # all prices equal; updates set prices to the same value or to the maximum
    rng = random.Random(20261120 + 3103)
    ops = []
    for _ in range(5000):
        if rng.random() < 0.5:
            ops.append((1, rng.randint(1, 5000), rng.choice([7, LIMIT])))
        else:
            l = rng.randint(1, 5000)
            ops.append((2, l, rng.randint(l, 5000)))
    cases.append(([7] * 5000, ops))
    # rising row: the minimum is at the left end of every range until updates move it
    rng = random.Random(20261120 + 3104)
    cases.append((list(range(1, 5001)), random_ops(rng, 5000, 5000, 5000, 0.3)))
    # first large case: only wide questions, so slow.cpp scans ~N per question
    rng = random.Random(20261120 + 3105)
    a = [rng.randint(1, LIMIT) for _ in range(MAX_NQ)]
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.05:
            ops.append((1, rng.randint(1, MAX_NQ), rng.randint(1, LIMIT)))
        else:
            ops.append((2, rng.randint(1, 100), MAX_NQ - rng.randint(0, 99)))
    cases.append((a, ops))
    rng = random.Random(20261120 + 3106)
    cases.append(([rng.randint(1, LIMIT) for _ in range(MAX_NQ)], random_ops(rng, MAX_NQ, MAX_NQ, LIMIT, 0.5)))
    # falling row with small prices: minimum at the right end, many short ranges
    rng = random.Random(20261120 + 3107)
    a = [MAX_NQ - i for i in range(MAX_NQ)]
    ops = []
    for _ in range(MAX_NQ):
        if rng.random() < 0.3:
            ops.append((1, rng.randint(1, MAX_NQ), rng.randint(1, 1000)))
        else:
            l = rng.randint(1, MAX_NQ)
            ops.append((2, l, min(MAX_NQ, l + rng.randint(0, 50))))
    cases.append((a, ops))
    rng = random.Random(20261120 + 3108)
    cases.append(([rng.randint(1, LIMIT) for _ in range(MAX_NQ)],
                  random_ops(rng, MAX_NQ, MAX_NQ, LIMIT, 0.2, min_len=MAX_NQ // 2)))
    for index, (a, ops) in enumerate(cases, start=1):
        write(out, index, a, ops)


if __name__ == "__main__":
    main()
