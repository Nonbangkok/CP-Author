#!/usr/bin/env python3
"""Testcase generator for lp_dpk03_heavy_treasures.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 20; cases 4-10 N <= 100. Case 4 (N = 45, everything fits)
already has 2^45 subsets to try. Covers an item heavier than W, everything
fitting at once (answer = sum of values), nothing fitting (answer 0), equal
weights, values all 1000 (sum v = 10^5), and W far below the total weight.
"""

import random
import sys
from pathlib import Path

MAX_N, MAX_W, MAX_V = 100, 10**9, 1000


def write(out: Path, index: int, cap: int, items: list[tuple[int, int]]) -> None:
    n = len(items)
    assert 1 <= n <= MAX_N and 1 <= cap <= MAX_W
    assert all(1 <= w <= MAX_W and 1 <= v <= MAX_V for w, v in items)
    if index <= 3:
        assert n <= 20
    lines = [f"{n} {cap}"] + [f"{w} {v}" for w, v in items]
    (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rand_items(rng: random.Random, n: int, wlo: int, whi: int, vlo: int, vhi: int) -> list[tuple[int, int]]:
    return [(rng.randint(wlo, whi), rng.randint(vlo, vhi)) for _ in range(n)]


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261206)
    write(out, 1, 5, [(7, 100)])                                               # the only item is too heavy: 0
    write(out, 2, MAX_W, rand_items(rng, 20, 1, 10**7, 1, MAX_V))              # everything fits
    write(out, 3, 3 * 10**9 // 4, rand_items(rng, 20, 10**7, 10**8, 1, MAX_V))  # slow's worst small case
    write(out, 4, MAX_W, rand_items(rng, 45, 1, 2 * 10**7, 1, MAX_V))          # first big case: 2^45 subsets
    write(out, 5, MAX_W, [(MAX_W, MAX_V)] * MAX_N)                            # one item at most
    write(out, 6, 10**8, rand_items(rng, MAX_N, 10**8 + 1, MAX_W, 1, MAX_V))   # nothing fits: 0
    write(out, 7, 37 * 10**7, [(10**7 * rng.randint(1, 9), MAX_V) for _ in range(MAX_N)])  # sum v = 10^5
    write(out, 8, MAX_W, rand_items(rng, MAX_N, 1, MAX_W // 10, 1, MAX_V))
    write(out, 9, 123456789, rand_items(rng, MAX_N, 1, 10**8, 990, MAX_V))     # near-equal values
    write(out, 10, MAX_W // 2, rand_items(rng, MAX_N, 1, 4 * 10**7, 1, MAX_V))


if __name__ == "__main__":
    main()
