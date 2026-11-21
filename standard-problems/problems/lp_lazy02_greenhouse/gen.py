#!/usr/bin/env python3
"""Testcase generator for lp_lazy02_greenhouse.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q up to
50,000. Cases 7 and 10 use only near-whole-row events, so changing bed by bed
(slow.cpp, O(N Q)) must time out there. The events are mixed so that a set
lands on top of a pending add and an add on top of a pending set at every
depth of the tree (the order of the two tags matters); also covers N = 1,
all-negative temperatures, sets to the value already there, and values far
beyond 32 bits.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9
MAX_NQ = 5 * 10**4


def write(out: Path, index: int, a: list[int], ops: list[tuple]) -> None:
    n, q = len(a), len(ops)
    assert 1 <= n <= MAX_NQ and 1 <= q <= MAX_NQ
    assert all(-LIMIT <= v <= LIMIT for v in a)
    for op in ops:
        if op[0] in (1, 2):
            assert len(op) == 4 and 1 <= op[1] <= op[2] <= n and -LIMIT <= op[3] <= LIMIT
        else:
            assert op[0] == 3 and len(op) == 3 and 1 <= op[1] <= op[2] <= n
    assert any(op[0] == 3 for op in ops)
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    lines = [f"{n} {q}", " ".join(map(str, a))]
    lines.extend(" ".join(map(str, op)) for op in ops)
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rand_range(rng, n, min_len=1, max_len=None):
    max_len = n if max_len is None else min(n, max_len)
    length = rng.randint(min(min_len, max_len), max_len)
    l = rng.randint(1, n - length + 1)
    return l, l + length - 1


def random_ops(rng, n, q, add_v, set_v, shares, min_len=1, max_len=None):
    """shares = (add, set); the rest are questions."""
    ops = []
    for _ in range(q):
        l, r = rand_range(rng, n, min_len, max_len)
        u = rng.random()
        if u < shares[0]:
            ops.append((1, l, r, add_v()))
        elif u < shares[0] + shares[1]:
            ops.append((2, l, r, set_v()))
        else:
            ops.append((3, l, r))
    if all(op[0] != 3 for op in ops):
        ops[-1] = (3, 1, n)
    return ops


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append(([-LIMIT], [(3, 1, 1), (1, 1, 1, LIMIT), (3, 1, 1), (2, 1, 1, 7), (1, 1, 1, -3),
                             (3, 1, 1), (2, 1, 1, LIMIT), (1, 1, 1, LIMIT), (3, 1, 1)]))
    # hand-made order traps: add then set, set then add, then look at a part
    cases.append(([5, 1, 4, 1, 5, 9, 2, 6],
                  [(1, 1, 8, 10), (2, 1, 4, 0), (3, 1, 8), (3, 2, 3), (1, 1, 8, 5), (3, 1, 2),
                   (2, 5, 8, -1), (1, 3, 6, 2), (3, 4, 5), (3, 6, 8), (2, 1, 8, 3), (3, 7, 7),
                   (1, 2, 2, 4), (2, 3, 8, 3), (1, 1, 8, -20), (3, 1, 8), (3, 3, 8)]))
    rng = random.Random(20261120 + 3501)
    sm = lambda: rng.randint(-100, 100)
    cases.append(([sm() for _ in range(1000)], random_ops(rng, 1000, 1000, sm, sm, (0.35, 0.3))))
    rng = random.Random(20261120 + 3502)
    big = lambda: rng.randint(-LIMIT, LIMIT)
    cases.append(([big() for _ in range(5000)], random_ops(rng, 5000, 5000, big, big, (0.35, 0.3))))
    # nested ranges around the middle, so tags stack on the same nodes
    rng = random.Random(20261120 + 3503)
    ops = []
    for _ in range(5000):
        w = rng.randint(0, 2499)
        l, r = 2500 - w, 2501 + w
        u = rng.random()
        if u < 0.4:
            ops.append((1, l, r, rng.randint(-50, 50)))
        elif u < 0.7:
            ops.append((2, l, r, rng.randint(-50, 50)))
        else:
            ops.append((3, *rand_range(rng, 5000)))
    cases.append(([0] * 5000, ops))
    # everything cold: negative sets, cooling only, so every maximum is negative
    rng = random.Random(20261120 + 3504)
    cases.append(([rng.randint(-LIMIT, -1) for _ in range(5000)],
                  random_ops(rng, 5000, 5000, lambda: rng.randint(-10**5, -1),
                             lambda: rng.randint(-LIMIT, -1), (0.4, 0.2))))
    # first large case: near-whole-row events only
    rng = random.Random(20261120 + 3505)
    ops = []
    for _ in range(MAX_NQ):
        l, r = rng.randint(1, 100), MAX_NQ - rng.randint(0, 99)
        u = rng.random()
        if u < 0.4:
            ops.append((1, l, r, rng.randint(-10**4, 10**4)))
        elif u < 0.6:
            ops.append((2, l, r, rng.randint(-10**4, 10**4)))
        else:
            ops.append((3, l, r))
    cases.append(([rng.randint(-10**4, 10**4) for _ in range(MAX_NQ)], ops))
    rng = random.Random(20261120 + 3506)
    cases.append(([big() for _ in range(40000)], random_ops(rng, 40000, 40000, big, big, (0.35, 0.25))))
    # short ranges and many small sets: lots of partly covered nodes
    rng = random.Random(20261120 + 3507)
    small = lambda: rng.randint(-1000, 1000)
    cases.append(([small() for _ in range(MAX_NQ)],
                  random_ops(rng, MAX_NQ, MAX_NQ, small, small, (0.35, 0.3), max_len=300)))
    # wide events, large heating: temperatures drift far beyond 32 bits
    rng = random.Random(20261120 + 3508)
    ops = []
    for _ in range(MAX_NQ):
        l, r = rng.randint(1, 50), MAX_NQ - rng.randint(0, 49)
        u = rng.random()
        if u < 0.7:
            ops.append((1, l, r, rng.randint(LIMIT // 2, LIMIT)))
        elif u < 0.75:
            ops.append((2, l, r, rng.randint(-LIMIT, LIMIT)))
        else:
            ops.append((3, *rand_range(rng, MAX_NQ, min_len=MAX_NQ // 2)))
    cases.append(([LIMIT] * MAX_NQ, ops))
    for index, (a, ops) in enumerate(cases, start=1):
        write(out, index, a, ops)


if __name__ == "__main__":
    main()
