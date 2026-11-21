#!/usr/bin/env python3
"""Testcase generator for lp_stl01_leaderboard.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-4 N <= 1,000; cases 5-10 N <= 30,000, where an O(N^2) sort must time out.
Names are distinct; many names are prefixes of each other and scores repeat a lot,
so the name tie-break really decides the order.
"""

import random
import string
import sys
from pathlib import Path


def names(rng: random.Random, n: int, prefixy: bool) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    while len(out) < n:
        if prefixy and out and rng.random() < 0.4:
            base = rng.choice(out)
            name = (base + rng.choice("ab"))[:10] if len(base) < 10 else base[: rng.randint(1, 9)]
        else:
            name = "".join(rng.choice(string.ascii_lowercase[: rng.choice((3, 26))])
                           for _ in range(rng.randint(1, 10)))
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def case(rng: random.Random, n: int, low: int, high: int, prefixy: bool, order: str) -> str:
    rows = [(name, rng.randint(low, high)) for name in names(rng, n, prefixy)]
    if order == "reverse":  # worst case for bubble sort: exactly backwards
        rows.sort(key=lambda r: (-r[1], r[0]))
        rows.reverse()
    elif order == "sorted":
        rows.sort(key=lambda r: (-r[1], r[0]))
    return f"{n}\n" + "".join(f"{name} {score}\n" for name, score in rows)


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 0, 100, False, "random"), (8, 7, 7, True, "random"),
        (300, 0, 5, True, "random"), (1000, 0, 100, True, "reverse"),
        (30000, 0, 100, True, "reverse"), (30000, 0, 100, False, "random"),
        (30000, 42, 42, True, "random"), (30000, 0, 3, True, "random"),
        (30000, 0, 100, True, "sorted"), (30000, 0, 100, True, "random"),
    ]
    for index, (n, low, high, prefixy, order) in enumerate(plans, start=1):
        rng = random.Random(20261120 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, low, high, prefixy, order), encoding="utf-8")


if __name__ == "__main__":
    main()
