#!/usr/bin/env python3
"""Testcase generator for lp_rec03_hanoi_kth.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 10, cases 4-6 N <= 20, cases 7-10 N <= 60, where replaying the
moves one by one (2^N - 1 of them) cannot finish.
"""

import random
import sys
from pathlib import Path


def queries(rng: random.Random, n: int, q: int) -> list[int]:
    top = (1 << n) - 1
    fixed = [1, top, 1 << (n - 1), (1 << (n - 1)) - 1, (1 << (n - 1)) + 1, 2, top - 1]
    fixed = [k for k in fixed if 1 <= k <= top]
    picked = fixed[:q]
    while len(picked) < q:
        if rng.random() < 0.2:
            # Multiples of a high power of two: the small disk's moves are rare there.
            shift = rng.randint(0, n - 1)
            k = rng.randint(1, max(1, top >> shift)) << shift
            k = min(max(k, 1), top)
        else:
            k = rng.randint(1, top)
        picked.append(k)
    rng.shuffle(picked)
    return picked


def main() -> None:
    out = Path(sys.argv[1])
    plans = [(1, 1), (4, 15), (10, 1000), (15, 1000), (20, 1000), (20, 1000),
             (60, 1000), (37, 1000), (59, 1000), (60, 1000)]
    for index, (n, q) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 500 + index)
        ks = list(range(1, 16)) if (n, q) == (4, 15) else queries(rng, n, q)
        text = f"{n} {len(ks)}\n" + "\n".join(map(str, ks)) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
