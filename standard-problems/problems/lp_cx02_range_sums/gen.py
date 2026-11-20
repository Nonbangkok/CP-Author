#!/usr/bin/env python3
"""Testcase generator for lp_cx02_range_sums.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, Q <= 1,000; cases 4-6 N, Q <= 5,000; cases 7-10 N = Q = 40,000.
Case 7 asks only long ranges, so re-adding every range (O(NQ), about 1.5e9
additions) must time out there. Sums reach 4e10, beyond int.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**6


def case(rng: random.Random, n: int, q: int, values: str, ranges: str) -> str:
    if values == "max":
        a = [LIMIT] * n
    elif values == "min":
        a = [-LIMIT] * n
    else:
        a = [rng.randint(-LIMIT, LIMIT) for _ in range(n)]
    lines = [f"{n} {q}", " ".join(map(str, a))]
    for _ in range(q):
        kind = ranges if ranges != "mixed" else rng.choice(["wide", "short", "any", "point"])
        if kind == "wide":
            l = rng.randint(1, max(1, n // 20))
            r = rng.randint(n - n // 20, n)
        elif kind == "short":
            l = rng.randint(1, n)
            r = min(n, l + rng.randint(0, 10))
        elif kind == "point":
            l = r = rng.randint(1, n)
        else:
            l, r = sorted((rng.randint(1, n), rng.randint(1, n)))
        lines.append(f"{l} {r}")
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 1, "rand", "any"), (100, 100, "max", "mixed"), (1000, 1000, "rand", "mixed"),
        (5000, 5000, "rand", "wide"), (5000, 5000, "min", "mixed"), (5000, 5000, "rand", "any"),
        (40000, 40000, "rand", "wide"), (40000, 40000, "max", "mixed"),
        (40000, 40000, "rand", "any"), (40000, 40000, "min", "wide"),
    ]
    for index, (n, q, values, ranges) in enumerate(plans, start=1):
        rng = random.Random(20261120 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, q, values, ranges), encoding="utf-8")


if __name__ == "__main__":
    main()
