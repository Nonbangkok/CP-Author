#!/usr/bin/env python3
"""Testcase generator for lp_rec01_subset_sum.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 10, cases 4-10 N <= 20 (all 2^N subsets must be tried).
"""

import random
import sys
from pathlib import Path


def pick_target(rng: random.Random, values: list[int]) -> int:
    # The sum of a random subset, so the answer is usually not 0.
    chosen = [x for x in values if rng.random() < 0.5] or [values[0]]
    return sum(chosen)


def case(n: int, s: int | None, values: list[int], rng: random.Random) -> str:
    if s is None:
        s = pick_target(rng, values)
    return f"{n} {s}\n" + " ".join(map(str, values)) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    for index in range(1, 11):
        rng = random.Random(20261120 + 300 + index)
        if index == 1:
            values, s = [7], 7                                   # N = 1, take it
        elif index == 2:
            values = [rng.randint(1, 10) for _ in range(8)]
            s = None
        elif index == 3:
            values, s = [rng.randint(1, 1000) for _ in range(10)], 1  # likely 0 ways
        elif index == 4:
            values, s = [1] * 20, 10                             # C(20, 10) = 184756
        elif index == 5:
            values, s = [10**6] * 20, 20 * 10**6                 # all coins, S at its maximum
        elif index == 6:
            values = [rng.randint(1, 5) for _ in range(20)]
            s = sum(values) // 2                                 # many ways
        elif index == 7:
            values = [rng.randint(1, 10**6) for _ in range(20)]
            s = None
        elif index == 8:
            values = [rng.randint(1, 10**6) for _ in range(20)]
            s = sum(values) + 1 if sum(values) + 1 <= 2 * 10**7 else 2 * 10**7  # impossible
        elif index == 9:
            values = [2 ** k for k in range(19)] + [1]           # powers of two and a twin 1
            s = 1000
        else:
            values = [rng.randint(1, 30) for _ in range(20)]
            s = None
        cases.append(case(len(values), s, values, rng))
    for index, text in enumerate(cases, start=1):
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
