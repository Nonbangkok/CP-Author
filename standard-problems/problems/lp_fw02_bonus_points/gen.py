#!/usr/bin/env python3
"""Testcase generator for lp_fw02_bonus_points.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q = 50,000.
Case 7 is almost all long range additions, so adding to every student one by
one (slow.cpp, O(N Q)) must time out there. Questions are interleaved with
the additions everywhere, so one difference array summed at the end is not
enough. Covers N = 1, r = N (no d[r+1]), l = r, negative scores and scores
beyond 2^31 in both directions.
"""

import random
import sys
from pathlib import Path

MAX_N = 5 * 10**4
MAX_V = 10**6


def write(out: Path, index: int, a: list[int], ops: list[tuple]) -> None:
    n, q = len(a), len(ops)
    assert 1 <= n <= MAX_N and 1 <= q <= MAX_N
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    assert all(0 <= v <= MAX_V for v in a)
    assert any(op[0] == 2 for op in ops)
    for op in ops:
        if op[0] == 1:
            _, l, r, x = op
            assert 1 <= l <= r <= n and -MAX_V <= x <= MAX_V
        else:
            assert len(op) == 2 and 1 <= op[1] <= n
    lines = [f"{n} {q}", " ".join(map(str, a))]
    lines += [" ".join(map(str, op)) for op in ops]
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def random_ops(rng: random.Random, n: int, q: int, update_share: float, lo: int, hi: int,
               min_len: int = 1) -> list[tuple]:
    ops = []
    for _ in range(q):
        if rng.random() < update_share:
            length = rng.randint(min(min_len, n), n)
            l = rng.randint(1, n - length + 1)
            ops.append((1, l, l + length - 1, rng.randint(lo, hi)))
        else:
            ops.append((2, rng.randint(1, n)))
    if not any(op[0] == 2 for op in ops):
        ops[-1] = (2, n)
    return ops


def main() -> None:
    out = Path(sys.argv[1])
    # 1: a single student
    write(out, 1, [0], [(2, 1), (1, 1, 1, MAX_V), (1, 1, 1, MAX_V), (2, 1), (1, 1, 1, -MAX_V), (2, 1)])
    # 2: small, hand-made: r = N, l = r, going negative
    write(out, 2, [3, 0, 8, 1, 5, 2, 9],
          [(2, 7), (1, 1, 7, 2), (2, 1), (1, 7, 7, -20), (2, 7), (1, 3, 5, -4), (2, 2), (2, 3),
           (2, 5), (2, 6), (1, 1, 1, 6), (1, 2, 6, 1), (2, 1), (2, 4), (2, 7)])
    rng = random.Random(20261120 + 3201)
    write(out, 3, [rng.randint(0, MAX_V) for _ in range(1000)],
          random_ops(rng, 1000, 1000, 0.5, -MAX_V, MAX_V))
    rng = random.Random(20261120 + 3202)
    write(out, 4, [rng.randint(0, 50) for _ in range(5000)], random_ops(rng, 5000, 5000, 0.5, -30, 30))
    rng = random.Random(20261120 + 3203)
    # 5: always +10^6 over long ranges: scores far above 2^31
    write(out, 5, [MAX_V] * 5000, random_ops(rng, 5000, 5000, 0.8, MAX_V, MAX_V, min_len=4000))
    rng = random.Random(20261120 + 3204)
    # 6: always -10^6: scores far below -2^31
    write(out, 6, [0] * 5000, random_ops(rng, 5000, 5000, 0.8, -MAX_V, -MAX_V, min_len=2500))
    rng = random.Random(20261120 + 3207)
    # 7: first large case, slow.cpp must TLE: 90% additions over most of the class
    write(out, 7, [rng.randint(0, MAX_V) for _ in range(MAX_N)],
          random_ops(rng, MAX_N, MAX_N, 0.9, -MAX_V, MAX_V, min_len=MAX_N * 4 // 5))
    rng = random.Random(20261120 + 3208)
    write(out, 8, [rng.randint(0, MAX_V) for _ in range(MAX_N)],
          random_ops(rng, MAX_N, MAX_N, 0.5, -MAX_V, MAX_V))
    rng = random.Random(20261120 + 3209)
    write(out, 9, [MAX_V] * MAX_N, random_ops(rng, MAX_N, MAX_N, 0.7, MAX_V, MAX_V, min_len=MAX_N // 2))
    rng = random.Random(20261120 + 3210)
    # 10: long additions touching the ends (l = 1 or r = N), single students, questions at the ends
    ops = []
    for _ in range(MAX_N):
        t = rng.random()
        x = rng.randint(-MAX_V, MAX_V)
        if t < 0.4:
            ops.append((1, 1, rng.randint(MAX_N // 2, MAX_N), x))
        elif t < 0.8:
            ops.append((1, rng.randint(1, MAX_N // 2), MAX_N, x))
        elif t < 0.85:
            p = rng.randint(1, MAX_N)
            ops.append((1, p, p, x))
        else:
            ops.append((2, rng.choice([1, MAX_N, rng.randint(1, MAX_N)])))
    write(out, 10, [rng.randint(0, MAX_V) for _ in range(MAX_N)], ops)


if __name__ == "__main__":
    main()
