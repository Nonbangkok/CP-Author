#!/usr/bin/env python3
"""Testcase generator for lp_stl05_nearest_van.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 Q <= 1,000; cases 4-6 Q <= 5,000; cases 7-10 Q = 100,000, where a
linear scan per command must time out (case 7: half inserts, then half queries
against a full road). Every erase targets a spot that is on the road.
Covered: empty road (-1), exact hits, ties (even spots, odd queries), many
copies of one spot with single-copy erases, both ends 0 and 10^9.
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def commands(rng: random.Random, q: int, spread: int, p_ins: float, p_del: float,
             warmup: int = 0, even: bool = False) -> str:
    road: list[int] = []
    lines = []

    def spot() -> int:
        v = rng.randint(0, spread)
        if rng.random() < 0.02:
            v = rng.choice((0, LIMIT))
        return v - v % 2 if even else v

    for step in range(q):
        roll = rng.random()
        if step < warmup or (roll < p_ins):
            v = spot()
            road.append(v)
            lines.append(f"1 {v}")
        elif roll < p_ins + p_del and road:
            k = rng.randrange(len(road))
            road[k], road[-1] = road[-1], road[k]
            lines.append(f"2 {road.pop()}")
        else:
            x = rng.choice(road) + rng.randint(-1, 1) if road and rng.random() < 0.3 else rng.randint(0, spread)
            x = min(max(x, 0), LIMIT)
            if even and rng.random() < 0.5:
                x |= 1
                x = min(x, LIMIT)
            lines.append(f"3 {x}")
    return f"{q}\n" + "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    rngs = [random.Random(20261120 + i) for i in range(1, 11)]
    texts = [
        "3\n3 0\n1 1000000000\n3 0\n",
        commands(rngs[1], 60, 20, 0.4, 0.3, even=True),
        commands(rngs[2], 1000, LIMIT, 0.4, 0.2),
        commands(rngs[3], 5000, 5, 0.45, 0.4),                  # few spots, many copies
        commands(rngs[4], 5000, LIMIT, 0.5, 0.1, even=True),
        commands(rngs[5], 5000, 10000, 0.35, 0.3),
        commands(rngs[6], 100000, LIMIT, 0.0, 0.0, warmup=50000),  # full road, then queries
        commands(rngs[7], 100000, LIMIT, 0.4, 0.2, warmup=20000, even=True),
        commands(rngs[8], 100000, 1000, 0.45, 0.35),
        commands(rngs[9], 100000, LIMIT, 0.3, 0.05, warmup=40000),
    ]
    for index, body in enumerate(texts, start=1):
        (out / f"input{index:02d}.txt").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
