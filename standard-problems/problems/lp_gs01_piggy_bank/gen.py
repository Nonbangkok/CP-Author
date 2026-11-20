#!/usr/bin/env python3
"""Testcase generator for lp_gs01_piggy_bank.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 at most 1,000 values with |a_i| <= 1,000 (an int sum is enough);
cases 4-10 up to 100,000 values with |a_i| <= 10^9, where the sum leaves the
int range (the judge's -fsanitize=signed-integer-overflow turns that into a
Runtime Error). Values are spread over lines of random width, ragged on purpose.
"""

import random
import sys
from pathlib import Path

BIG = 10**9


def layout(rng: random.Random, values: list[int]) -> str:
    lines, i = [], 0
    while i < len(values):
        width = rng.choice([1, 1, 2, 3, 5, 10, 20])
        lines.append(" ".join(map(str, values[i:i + width])))
        i += width
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[list[int]] = []
    rng = random.Random(20261120)
    cases.append([-7])                                                   # one value, negative answer
    cases.append([rng.randint(-1000, 1000) for _ in range(50)])
    cases.append([rng.choice([1000, 999, -1000]) for _ in range(1000)])  # int is still fine here
    cases.append([BIG, BIG, BIG])                                       # 3e9: smallest overflow
    cases.append([-BIG] * 2000 + [BIG] * 1999)                          # partial sums dip to -2e12, total -1e9
    cases.append([rng.randint(-BIG, BIG) for _ in range(20000)])
    cases.append([rng.randint(BIG - 1000, BIG) for _ in range(100000)])  # about 1e14
    cases.append([-rng.randint(BIG - 1000, BIG) for _ in range(100000)])  # about -1e14
    cases.append([rng.randint(-BIG, BIG) for _ in range(100000)])
    mixed = [BIG] * 50000 + [-BIG] * 49999 + [12345]
    rng.shuffle(mixed)
    cases.append(mixed)
    for index, values in enumerate(cases, start=1):
        case_rng = random.Random(20261120 + index)
        (out / f"input{index:02d}.txt").write_text(layout(case_rng, values), encoding="utf-8")


if __name__ == "__main__":
    main()
