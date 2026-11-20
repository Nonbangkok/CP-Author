#!/usr/bin/env python3
"""Testcase generator for lp_gs03_mod_product.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 3, a_i <= 1,000 (plain int is enough); cases 4-6 a_i <= 10^9
(< P, but the product step needs long long); cases 7-10 a_i <= 10^18, where
a_i must be reduced modulo P before multiplying and the plain sum overflows
long long. Zeros and multiples of P (product 0) appear on purpose.
"""

import random
import sys
from pathlib import Path

MOD = 10**9 + 7
TOP = 10**18


def mixed_big(rng: random.Random) -> int:
    digits = rng.choice([1, 5, 10, 12, 15, 18, 18, 19])
    if digits == 19:
        return rng.randint(TOP - 10**15, TOP)
    return rng.randint(10 ** (digits - 1), 10**digits - 1)


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261120)
    cases: list[list[int]] = [
        [0],
        [1000, 1000, 1000],
        [rng.randint(0, 1000) for _ in range(3)],
        [10**9, 10**9, 10**9, 10**9, 10**9],
        [rng.randint(10**9 - 10**6, 10**9) for _ in range(100000)],
        [rng.randint(1, 10**9) for _ in range(30000)] + [0] + [rng.randint(1, 10**9) for _ in range(5)],
        [TOP] * 1000,
        [mixed_big(rng) for _ in range(40000)],
        [rng.randint(TOP - 10**12, TOP) for _ in range(30000)],
        [mixed_big(rng) for _ in range(30000)] + [MOD * 999999993] + [mixed_big(rng) for _ in range(30000)],
    ]
    for index, values in enumerate(cases, start=1):
        assert 1 <= len(values) <= 100000 and all(0 <= v <= TOP for v in values)
        text = f"{len(values)}\n" + " ".join(map(str, values)) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
