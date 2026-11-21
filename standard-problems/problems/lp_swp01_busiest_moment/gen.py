#!/usr/bin/env python3
"""Testcase generator for lp_swp01_busiest_moment.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N up to 100,000, where
counting the guests at every arrival (slow.cpp, O(N^2)) must time out. Many
cases put leaves and arrivals on the same second, so the tie rule decides the
answer (a hand-off chain where the wrong rule doubles the count, etc.).
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def write(out: Path, index: int, guests: list[tuple[int, int]]) -> None:
    n = len(guests)
    assert 1 <= n <= 10**5
    assert all(0 <= a < b <= LIMIT for a, b in guests)
    if index <= 3:
        assert n <= 1000
    elif index <= 6:
        assert n <= 5000
    text = f"{n}\n" + "".join(f"{a} {b}\n" for a, b in guests)
    (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


def random_guests(rng: random.Random, n: int, horizon: int, longest: int) -> list[tuple[int, int]]:
    guests = []
    for _ in range(n):
        a = rng.randint(0, horizon - 1)
        b = min(horizon, a + rng.randint(1, longest))
        guests.append((a, b))
    return guests


def chain(rng: random.Random, n: int, step: int) -> list[tuple[int, int]]:
    """Guest i leaves exactly when guest i+1 arrives (plus a few overlapping ones)."""
    guests = [(i * step, (i + 1) * step) for i in range(n)]
    rng.shuffle(guests)
    return guests


def main() -> None:
    out = Path(sys.argv[1])
    cases = []
    cases.append([(0, LIMIT)])                                                  # N = 1
    cases.append([(5, 9), (1, 5), (9, 12), (2, 3), (3, 5), (5, 6), (0, 1), (12, 13)])
    rng = random.Random(20261120 + 901)
    cases.append(random_guests(rng, 1000, 100, 10))                             # dense ties
    rng = random.Random(20261120 + 902)
    cases.append(chain(rng, 5000, 7))                                           # answer 1, not 2
    rng = random.Random(20261120 + 903)
    cases.append([(rng.randint(0, 10), LIMIT - rng.randint(0, 10)) for _ in range(5000)])
    rng = random.Random(20261120 + 904)
    cases.append(random_guests(rng, 5000, LIMIT, 10**7))
    rng = random.Random(20261120 + 905)
    cases.append(random_guests(rng, 100000, LIMIT, 10**8))                      # slow.cpp must TLE here
    rng = random.Random(20261120 + 906)
    cases.append(random_guests(rng, 50000, 1000, 50))                           # many equal times
    rng = random.Random(20261120 + 907)
    peak = [(500000 - i, 500000 + i + 1) for i in range(30000)]                 # nested around 500000
    cases.append(peak + chain(rng, 20000, 50) + random_guests(rng, 10000, LIMIT, 1000))
    rng = random.Random(20261120 + 908)
    cases.append(random_guests(rng, 100000, 86400, 3600))
    for index, guests in enumerate(cases, start=1):
        rng = random.Random(index)
        rng.shuffle(guests)
        write(out, index, guests)


if __name__ == "__main__":
    main()
