#!/usr/bin/env python3
"""Testcase generator for lp_bit01_bit_ops.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 100 with 30-bit values; cases 4-5 full N, Q with 30-bit
values; cases 6-10 full 60-bit values and k up to 59 (1 << k in int breaks).
Edge cases: a_i = 0, a_i = 2^60 - 1, set an already-set bit, clear an
already-clear bit, bits 31 and 59.
"""

import random
import sys
from pathlib import Path


def case(rng: random.Random, n: int, q: int, bits: int) -> str:
    full = (1 << bits) - 1
    a = []
    for _ in range(n):
        roll = rng.random()
        if roll < 0.1:
            a.append(0)
        elif roll < 0.2:
            a.append(full)
        elif roll < 0.4:
            a.append(rng.randint(0, full) & rng.randint(0, full) & rng.randint(0, full))  # sparse
        else:
            a.append(rng.randint(0, full))
    lines = [f"{n} {q}", " ".join(map(str, a))]
    high = [bits - 1, bits - 2, 31, 32, 30] if bits > 32 else [bits - 1, 0, 1]
    for _ in range(q):
        t = rng.choice([1, 2, 3, 4, 4, 5, 5])
        i = rng.randint(1, n)
        if t == 5:
            lines.append(f"5 {i}")
            continue
        k = rng.choice(high) if rng.random() < 0.3 else rng.randint(0, bits - 1)
        lines.append(f"{t} {i} {k}")
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 5, 30), (10, 60, 30), (100, 100, 30),
        (1000, 50000, 30), (3, 50000, 30),
        (1000, 50000, 60), (1, 50000, 60), (50, 50000, 60), (1000, 50000, 60), (1000, 50000, 60),
    ]
    for index, (n, q, bits) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 100 * index + 21)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, q, bits), encoding="utf-8")


if __name__ == "__main__":
    main()
