#!/usr/bin/env python3
"""Testcase generator for lp_dp01_frog_jumps.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 20 (N = 1, K = 1, K >= N); cases 4-10 N <= 2 * 10^4. Case 4 is
already far too many routes for plain recursion (N = 60, K = 3: ~10^15 routes),
the later ones are full size with K up to 100, giant heights (64-bit answers),
a zigzag where short hops are expensive, and a staircase.
"""

import random
import sys
from pathlib import Path

MAX_N, MAX_K, MAX_H = 2 * 10**4, 100, 10**9


def write(out: Path, index: int, k: int, h: list[int]) -> None:
    n = len(h)
    assert 1 <= n <= MAX_N and 1 <= k <= MAX_K and all(1 <= x <= MAX_H for x in h)
    if index <= 3:
        assert n <= 20
    (out / f"input{index:02d}.txt").write_text(f"{n} {k}\n{' '.join(map(str, h))}\n", encoding="utf-8")


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261201)
    write(out, 1, 1, [7])                                                     # N = 1: answer 0
    write(out, 2, 1, [rng.randint(1, 100) for _ in range(12)])                # K = 1: walk every stone
    write(out, 3, 20, [rng.randint(1, 100) for _ in range(20)])               # K >= N, slow's worst small case
    write(out, 4, 3, [rng.randint(1, 1000) for _ in range(60)])               # first big case: recursion must TLE
    write(out, 5, 100, [rng.randint(1, MAX_H) for _ in range(MAX_N)])
    write(out, 6, 1, [rng.randint(1, MAX_H) for _ in range(MAX_N)])           # K = 1, answer ~ 6.7 * 10^12
    zig = [MAX_H if i % 2 else 1 for i in range(MAX_N)]                       # odd hops cost 10^9, even hops 0
    write(out, 7, 2, zig)
    write(out, 8, 57, [i * 50000 + 1 for i in range(MAX_N)])                  # staircase: every route costs the same
    write(out, 9, 100, [rng.randint(1, 50) for _ in range(MAX_N)])            # many ties
    write(out, 10, 100, [rng.choice([1, MAX_H, rng.randint(1, MAX_H)]) for _ in range(MAX_N)])


if __name__ == "__main__":
    main()
