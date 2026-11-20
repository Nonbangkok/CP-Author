#!/usr/bin/env python3
"""Testcase generator for lp_gs02_report_card.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, M <= 10; cases 4-10 N <= 20,000 and N * M <= 200,000 (one of
them N = 1, one M = 1, one wide M). No average is ever an exact tie between two printed
values (sum / count with x.xx5 exactly), so rounding is never ambiguous: a
tie is when 200 * sum / count is an odd integer, and the generator nudges a
score until none is.
"""

import random
import sys
from pathlib import Path


def is_tie(total: int, count: int) -> bool:
    return (200 * total) % count == 0 and ((200 * total) // count) % 2 == 1


def case(rng: random.Random, n: int, m: int, style: str) -> str:
    rows = []
    for _ in range(n):
        if style == "high":
            row = [rng.randint(90, 100) for _ in range(m)]
        elif style == "edge":
            row = [rng.choice([0, 100]) for _ in range(m)]
        else:
            row = [rng.randint(0, 100) for _ in range(m)]
        while is_tie(sum(row), m):
            j = rng.randrange(m)
            row[j] = row[j] + 1 if row[j] < 100 else row[j] - 1
        rows.append(row)
    while is_tie(sum(map(sum, rows)), n * m):
        i, j = rng.randrange(n), rng.randrange(m)
        old = rows[i][j]
        rows[i][j] = old + 1 if old < 100 else old - 1
        if is_tie(sum(rows[i]), m):
            rows[i][j] = old
    lines = [f"{n} {m}"] + [" ".join(map(str, row)) for row in rows]
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (1, 1, "flat"), (5, 3, "flat"), (10, 10, "edge"),
        (1, 200000, "flat"), (20000, 1, "flat"), (1000, 7, "flat"),
        (20000, 10, "high"), (13333, 15, "flat"), (400, 500, "edge"), (20000, 8, "flat"),
    ]
    for index, (n, m, style) in enumerate(plans, start=1):
        rng = random.Random(20261120 + index)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, m, style), encoding="utf-8")


if __name__ == "__main__":
    main()
