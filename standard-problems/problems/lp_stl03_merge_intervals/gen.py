#!/usr/bin/env python3
"""Testcase generator for lp_stl03_merge_intervals.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-6 N <= 5,000; cases 7-10 N = 50,000, where
comparing each interval with every strip found so far (O(N^2)) must time out
(case 7: all intervals disjoint, so the strip list keeps growing).
Edge cases: touching ends ([1, 3] + [3, 5]), a gap of exactly 1, nested
intervals, one interval covering everything, and (case 10) islands that a
last wave of bridges joins into a single strip.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def disjoint(rng: random.Random, n: int, touch: float) -> list[tuple[int, int]]:
    """n intervals left to right; with probability `touch` the next one starts
    exactly where the previous ended (merging), otherwise after a gap >= 1."""
    step = LIMIT // n
    out, pos = [], 0
    for _ in range(n):
        start = pos if (out and rng.random() < touch) else pos + rng.randint(1, max(1, step // 4))
        end = min(LIMIT, start + rng.randint(1, max(1, step // 2)))
        if start >= end:
            start = end - 1
        out.append((start, end))
        pos = end
    return out


def random_segments(rng: random.Random, n: int, max_len: int) -> list[tuple[int, int]]:
    out = []
    for _ in range(n):
        l = rng.randint(0, LIMIT - 1)
        out.append((l, min(LIMIT, l + rng.randint(1, max_len))))
    return out


def nested(rng: random.Random, n: int) -> list[tuple[int, int]]:
    out = [(0, LIMIT)]
    for _ in range(n - 1):
        l = rng.randint(0, LIMIT - 1)
        out.append((l, rng.randint(l + 1, LIMIT)))
    return out


def bridged(rng: random.Random, n: int) -> list[tuple[int, int]]:
    """n // 2 separate islands in random order, then the n // 2 - 1 bridges
    that join neighbours (each touching both ends), also shuffled. Every strip
    stays apart until the bridges arrive, and the answer is a single strip."""
    islands = disjoint(rng, n // 2, 0.0)
    bridges = [(islands[i][1], islands[i + 1][0]) for i in range(len(islands) - 1)]
    rng.shuffle(islands)
    rng.shuffle(bridges)
    return islands + bridges


def text(rng: random.Random, segs: list[tuple[int, int]], shuffle: bool = True) -> str:
    if shuffle:
        rng.shuffle(segs)
    return f"{len(segs)}\n" + "".join(f"{l} {r}\n" for l, r in segs)


def main() -> None:
    out = Path(sys.argv[1])
    rngs = [random.Random(20261120 + i) for i in range(1, 11)]
    texts = [
        "1\n0 1000000000\n",
        text(rngs[1], [(1, 3), (3, 5), (6, 7), (8, 9), (9, 9 + 1), (20, 30), (21, 22), (0, 1), (11, 12)]),
        text(rngs[2], random_segments(rngs[2], 1000, 3_000_000)),
        text(rngs[3], disjoint(rngs[3], 5000, 0.3)),
        text(rngs[4], nested(rngs[4], 5000)),
        text(rngs[5], random_segments(rngs[5], 5000, 400_000)),
        text(rngs[6], disjoint(rngs[6], 50000, 0.0)),
        text(rngs[7], disjoint(rngs[7], 50000, 0.5)),
        text(rngs[8], random_segments(rngs[8], 50000, 40_000)),
        text(rngs[9], bridged(rngs[9], 50000), shuffle=False),
    ]
    for index, body in enumerate(texts, start=1):
        (out / f"input{index:02d}.txt").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
