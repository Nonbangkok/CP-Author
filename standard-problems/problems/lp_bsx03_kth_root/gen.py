#!/usr/bin/env python3
"""Testcase generator for lp_bsx03_kth_root.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 n <= 10^6; cases 4-5 Q <= 10, n <= 10^12; cases 6-10 Q = 10^4,
n <= 10^18, where k = 2 answers reach 10^9, so counting x up one at a time must
time out. Many queries sit exactly on a perfect power or one below it -- where
floating-point pow() rounds the wrong way -- and the largest k for each answer.
"""

import random
import sys
from pathlib import Path


def iroot(n: int, k: int) -> int:
    lo, hi = 1, 1 << (60 // k + 1)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** k <= n:
            lo = mid
        else:
            hi = mid
    return lo


def query(rng: random.Random, top: int, small_k_bias: float) -> tuple[int, int]:
    k = 2 if rng.random() < small_k_bias else rng.randint(2, 60)
    roll = rng.random()
    if roll < 0.5:
        # On or next to a perfect power x^k <= top.
        x = rng.randint(1, max(1, iroot(top, k)))
        n = x ** k + rng.choice((-1, 0, 0, 1))
    elif roll < 0.6:
        n = top - rng.randint(0, 2)
    else:
        n = rng.randint(1, top)
    return max(1, min(top, n)), k


def case(rng: random.Random, q: int, top: int, small_k_bias: float, fixed: list[tuple[int, int]]) -> str:
    queries = fixed + [query(rng, top, small_k_bias) for _ in range(q - len(fixed))]
    rng.shuffle(queries)
    return f"{len(queries)}\n" + "".join(f"{n} {k}\n" for n, k in queries)


def main() -> None:
    out = Path(sys.argv[1])
    big = [(10**18, 2), (10**18 - 1, 2), (10**18, 3), (10**18 - 1, 3), (10**18, 60),
           (2**59, 59), (2**59 - 1, 59), (3**37, 37), (3**37 - 1, 37), (1, 2), (1, 60),
           ((10**9 - 1) ** 2, 2), ((10**9 - 1) ** 2 - 1, 2), (999999999999999999, 6)]
    # (q, top, share of k = 2, fixed queries)
    plans = [
        (5, 30, 0.5, [(1, 2)]), (300, 10**6, 0.4, [(10**6, 2), (999999, 2), (10**6, 3), (10**6, 20)]),
        (10000, 10**6, 0.5, []),
        (10, 10**12, 0.6, [(10**12, 2), (10**12 - 1, 2)]), (10, 10**12, 0.3, [(999999999999, 3)]),
        (10000, 10**18, 0.6, big), (10000, 10**18, 0.2, []), (10000, 10**18, 1.0, []),
        (10000, 10**18, 0.0, big), (10000, 10**18, 0.4, []),
    ]
    for index, (q, top, bias, fixed) in enumerate(plans, start=1):
        rng = random.Random(20261125 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, q, top, bias, list(fixed)), encoding="utf-8")


if __name__ == "__main__":
    main()
