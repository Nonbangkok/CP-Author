#!/usr/bin/env python3
"""Testcase generator for lp_fw03_bird_species.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N, Q = 50,000.
Case 7 has thousands of species and long questions, so walking every question
point by point (slow.cpp, O(N Q)) must time out there. Covers N = 1, l = r,
one species everywhere, all species distinct, long runs, repeated and
unsorted questions, and codes up to 10^9 (a count array indexed by the code
itself is impossible).
"""

import random
import sys
from pathlib import Path

MAX_N = 5 * 10**4
LIMIT = 10**9


def write(out: Path, index: int, a: list[int], qs: list[tuple[int, int]]) -> None:
    n, q = len(a), len(qs)
    assert 1 <= n <= MAX_N and 1 <= q <= MAX_N
    if index <= 3:
        assert n <= 1000 and q <= 1000
    elif index <= 6:
        assert n <= 5000 and q <= 5000
    assert all(1 <= v <= LIMIT for v in a)
    assert all(1 <= l <= r <= n for l, r in qs)
    lines = [f"{n} {q}", " ".join(map(str, a))] + [f"{l} {r}" for l, r in qs]
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def pool(rng: random.Random, size: int) -> list[int]:
    return rng.sample(range(1, LIMIT + 1), size)


def random_queries(rng: random.Random, n: int, q: int, min_len: int = 1) -> list[tuple[int, int]]:
    qs = []
    for _ in range(q):
        length = rng.randint(min(min_len, n), n)
        l = rng.randint(1, n - length + 1)
        qs.append((l, l + length - 1))
    return qs


def runs(rng: random.Random, n: int, species: list[int], longest: int) -> list[int]:
    a: list[int] = []
    while len(a) < n:
        a.extend([rng.choice(species)] * rng.randint(1, longest))
    return a[:n]


def main() -> None:
    out = Path(sys.argv[1])
    write(out, 1, [LIMIT], [(1, 1)])
    write(out, 2, [4, 4, 2, 9, 4, 2, 2, 7, 9, 1],
          [(1, 10), (1, 1), (10, 10), (1, 2), (2, 5), (3, 7), (6, 7), (5, 9), (1, 10), (8, 10), (4, 4)])
    rng = random.Random(20261120 + 3301)
    sp = pool(rng, 30)
    write(out, 3, [rng.choice(sp) for _ in range(1000)], random_queries(rng, 1000, 1000))
    rng = random.Random(20261120 + 3302)
    write(out, 4, pool(rng, 5000), random_queries(rng, 5000, 5000))              # all distinct: r - l + 1
    rng = random.Random(20261120 + 3303)
    write(out, 5, [LIMIT] * 5000, random_queries(rng, 5000, 5000))               # one species: always 1
    rng = random.Random(20261120 + 3304)
    write(out, 6, runs(rng, 5000, pool(rng, 200), 40), random_queries(rng, 5000, 5000))
    rng = random.Random(20261120 + 3307)
    # 7: first large case, slow.cpp must TLE: many species, every question long
    sp = pool(rng, 20000)
    a = [rng.choice(sp) for _ in range(MAX_N)]
    qs = [(rng.randint(1, MAX_N // 10), rng.randint(MAX_N * 9 // 10, MAX_N)) for _ in range(MAX_N)]
    write(out, 7, a, qs)
    rng = random.Random(20261120 + 3308)
    sp = pool(rng, 100)
    write(out, 8, [rng.choice(sp) for _ in range(MAX_N)], random_queries(rng, MAX_N, MAX_N))
    rng = random.Random(20261120 + 3309)
    write(out, 9, pool(rng, MAX_N), random_queries(rng, MAX_N, MAX_N, min_len=MAX_N // 3))
    rng = random.Random(20261120 + 3310)
    # 10: runs of a few thousand species; questions of every shape (mostly long), many repeated
    a = runs(rng, MAX_N, pool(rng, 3000), 30)
    qs = []
    for _ in range(MAX_N):
        t = rng.random()
        if t < 0.05:
            p = rng.randint(1, MAX_N)
            qs.append((p, p))
        elif t < 0.3:
            qs.append((1, MAX_N))
        elif t < 0.55:
            qs.append((1, rng.randint(MAX_N // 2, MAX_N)))
        elif t < 0.8:
            qs.append((rng.randint(1, MAX_N // 2), MAX_N))
        else:
            l = rng.randint(1, MAX_N)
            qs.append((l, rng.randint(l, MAX_N)))
    write(out, 10, a, qs)


if __name__ == "__main__":
    main()
