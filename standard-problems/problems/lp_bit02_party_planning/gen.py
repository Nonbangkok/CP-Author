#!/usr/bin/env python3
"""Testcase generator for lp_bit02_party_planning.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 10; cases 4-5 N = 20 with M = 0; cases 6-10 N = 20 with
conflicts. Budgets are set around half of the total cost so the limit binds,
plus edge cases: nothing affordable (answer 0), everything affordable, a
budget far above 2^31, the maximum M, and a value sum above 2^31.
"""

import random
import sys
from pathlib import Path


def case(rng: random.Random, n: int, m: int, budget_kind: str, big: bool) -> str:
    top = 10**9 if big else 1000
    c = [rng.randint(1, top) for _ in range(n)]
    v = [rng.randint(1, top) for _ in range(n)]
    total = sum(c)
    if budget_kind == "none":
        budget = min(c) - 1
    elif budget_kind == "all":
        budget = 10**10
    elif budget_kind == "tight":
        budget = rng.randint(total // 4, total // 2)
    else:
        budget = rng.randint(total // 2, total * 3 // 4)
    pairs = [(x, y) for x in range(1, n + 1) for y in range(x + 1, n + 1)]
    rng.shuffle(pairs)
    chosen = []
    for x, y in pairs[:m]:
        chosen.append((x, y) if rng.random() < 0.5 else (y, x))
    lines = [f"{n} {len(chosen)} {budget}"] + [f"{ci} {vi}" for ci, vi in zip(c, v)]
    lines += [f"{x} {y}" for x, y in chosen]
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 0, "all", False),
        (6, 4, "tight", False),
        (10, 12, "half", True),
        (20, 0, "tight", True),
        (20, 0, "all", True),
        (20, 50, "half", True),
        (20, 20, "tight", True),
        (20, 50, "all", True),
        (20, 35, "none", True),
        (20, 10, "half", True),
    ]
    for index, (n, m, budget_kind, big) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 100 * index + 33)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, m, budget_kind, big), encoding="utf-8")


if __name__ == "__main__":
    main()
