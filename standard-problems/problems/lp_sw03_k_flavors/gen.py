#!/usr/bin/env python3
"""Testcase generator for lp_sw03_k_flavors.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 100,000. Cases 7
and 10 allow tens of thousands of flavours in a window, so extending every
start until a (K+1)-th flavour appears (O(N^2)) must time out there.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def pool(rng: random.Random, size: int) -> list[int]:
    """size distinct flavour numbers spread over [1, 10^9]."""
    return rng.sample(range(1, LIMIT + 1), size)


def random_case(rng: random.Random, n: int, kinds: int) -> list[int]:
    flavours = pool(rng, kinds)
    return [rng.choice(flavours) for _ in range(n)]


def runs_case(rng: random.Random, n: int, kinds: int, longest: int) -> list[int]:
    """Runs of one flavour each, so long windows with few flavours exist."""
    flavours = pool(rng, kinds)
    values: list[int] = []
    while len(values) < n:
        values.extend([rng.choice(flavours)] * rng.randint(1, longest))
    return values[:n]


def main() -> None:
    out = Path(sys.argv[1])
    plans = []
    plans.append(([7], 1))                                            # N = K = 1
    plans.append(([5, 5, 9, 5, 1, 9, 9, 2, 2, 2, 9, 1], 12))           # K = N: the whole array
    rng = random.Random(20261120 + 601)
    plans.append((random_case(rng, 1000, 20), 5))
    plans.append(([LIMIT] * 5000, 1))                                  # one flavour, K = 1
    rng = random.Random(20261120 + 602)
    plans.append((pool(rng, 5000), 7))                                 # all distinct: answer K
    rng = random.Random(20261120 + 603)
    plans.append((runs_case(rng, 5000, 300, 30), 100))
    rng = random.Random(20261120 + 604)
    plans.append((pool(rng, 100000), 50000))                           # first large case: slow.cpp must TLE here
    rng = random.Random(20261120 + 605)
    plans.append((runs_case(rng, 100000, 3, 50), 2))                   # few flavours, long runs
    rng = random.Random(20261120 + 606)
    plans.append((runs_case(rng, 100000, 1000, 200), 300))
    rng = random.Random(20261120 + 607)
    plans.append((random_case(rng, 100000, 60000), 40000))
    for index, (values, k) in enumerate(plans, start=1):
        text = f"{len(values)} {k}\n{' '.join(map(str, values))}\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
