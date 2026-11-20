#!/usr/bin/env python3
"""Testcase generator for lp_fw01_shelf_stock.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q = 50,000.
Case 7 is almost all long questions, so adding the shelves one by one
(slow.cpp, O(N Q)) must time out there. Covers N = 1, l = r, setting a shelf
to the value it already has (a set, not an add), zeros, and sums beyond 2^31.
"""

import random
import sys
from pathlib import Path

MAX_N = 5 * 10**4
MAX_V = 10**6


def write(out: Path, index: int, a: list[int], ops: list[tuple[int, int, int]]) -> None:
    n, q = len(a), len(ops)
    assert 1 <= n <= MAX_N and 1 <= q <= MAX_N
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    assert all(0 <= v <= MAX_V for v in a)
    assert any(t == 2 for t, _, _ in ops)
    for t, u, v in ops:
        if t == 1:
            assert 1 <= u <= n and 0 <= v <= MAX_V
        else:
            assert t == 2 and 1 <= u <= v <= n
    lines = [f"{n} {q}", " ".join(map(str, a))]
    lines += [f"{t} {u} {v}" for t, u, v in ops]
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def random_ops(rng: random.Random, n: int, q: int, update_share: float, max_v: int,
               min_len: int = 1) -> list[tuple[int, int, int]]:
    ops = []
    for _ in range(q):
        if rng.random() < update_share:
            ops.append((1, rng.randint(1, n), rng.randint(0, max_v)))
        else:
            length = rng.randint(min(min_len, n), n)
            l = rng.randint(1, n - length + 1)
            ops.append((2, l, l + length - 1))
    if not any(t == 2 for t, _, _ in ops):
        ops[-1] = (2, 1, n)
    return ops


def main() -> None:
    out = Path(sys.argv[1])
    # 1: a single shelf
    write(out, 1, [7], [(2, 1, 1), (1, 1, 0), (2, 1, 1), (1, 1, MAX_V), (2, 1, 1)])
    # 2: small, repeated sets of the same value, l = r questions
    write(out, 2, [5, 0, 3, 3, 9, 1, 0, 2],
          [(2, 1, 8), (1, 4, 3), (1, 4, 3), (2, 3, 5), (2, 4, 4), (1, 2, 6), (1, 2, 6),
           (2, 1, 2), (1, 8, 0), (2, 6, 8), (2, 1, 8), (1, 5, 5), (2, 5, 5)])
    rng = random.Random(20261120 + 3101)
    write(out, 3, [rng.randint(0, MAX_V) for _ in range(1000)], random_ops(rng, 1000, 1000, 0.5, MAX_V))
    rng = random.Random(20261120 + 3102)
    write(out, 4, [rng.randint(0, 100) for _ in range(5000)], random_ops(rng, 5000, 5000, 0.5, 100))
    rng = random.Random(20261120 + 3103)
    # 5: all shelves full, mostly whole-range questions: sums near 5 * 10^9 > 2^31
    write(out, 5, [MAX_V] * 5000, random_ops(rng, 5000, 5000, 0.2, MAX_V, min_len=4000))
    rng = random.Random(20261120 + 3104)
    # 6: few distinct shelves updated over and over
    a = [rng.randint(0, MAX_V) for _ in range(5000)]
    ops = []
    for _ in range(5000):
        if rng.random() < 0.6:
            ops.append((1, rng.choice([1, 2, 2500, 4999, 5000]), rng.choice([0, MAX_V, 17])))
        else:
            l = rng.randint(1, 5000)
            ops.append((2, l, rng.randint(l, 5000)))
    write(out, 6, a, ops)
    rng = random.Random(20261120 + 3107)
    # 7: first large case, slow.cpp must TLE: 90% questions, each over most of the shelves
    write(out, 7, [rng.randint(0, MAX_V) for _ in range(MAX_N)],
          random_ops(rng, MAX_N, MAX_N, 0.1, MAX_V, min_len=MAX_N * 4 // 5))
    rng = random.Random(20261120 + 3108)
    write(out, 8, [rng.randint(0, MAX_V) for _ in range(MAX_N)], random_ops(rng, MAX_N, MAX_N, 0.5, MAX_V))
    rng = random.Random(20261120 + 3109)
    write(out, 9, [MAX_V] * MAX_N, random_ops(rng, MAX_N, MAX_N, 0.3, MAX_V, min_len=MAX_N // 2))
    rng = random.Random(20261120 + 3110)
    # 10: tiny shelves, hot updated shelves, l = r and l = 1 / r = N questions, mostly long
    a = [rng.randint(0, 10) for _ in range(MAX_N)]
    ops = []
    for _ in range(MAX_N):
        r = rng.random()
        if r < 0.15:
            ops.append((1, rng.choice([1, MAX_N, rng.randint(1, MAX_N)]), rng.randint(0, MAX_V)))
        elif r < 0.2:
            p = rng.randint(1, MAX_N)
            ops.append((2, p, p))
        elif r < 0.6:
            ops.append((2, 1, rng.randint(MAX_N // 2, MAX_N)))
        else:
            ops.append((2, rng.randint(1, MAX_N // 10), rng.randint(MAX_N * 9 // 10, MAX_N)))
    write(out, 10, a, ops)


if __name__ == "__main__":
    main()
