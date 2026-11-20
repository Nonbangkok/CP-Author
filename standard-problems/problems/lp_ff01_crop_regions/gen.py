#!/usr/bin/env python3
"""Testcase generator for lp_ff01_crop_regions.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 R, C <= 30; cases 4-6 R, C <= 100; cases 7-10 R, C <= 1,000. Every
cell is a lowercase letter. Covers a 1 x 1 field, one crop everywhere, a
checkerboard (every cell its own region), single rows/columns, random noise,
big blocks with noise, and winding "snake" regions: there the
sweep-until-nothing-changes approach needs about one sweep per step of every
upward stretch and must time out (case 7, 1000 x 1000).
"""

import random
import sys
from pathlib import Path

MAX_SIDE = 1000
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def snake(r: int, c: int, path: str = "a", wall: str = "b") -> list[str]:
    """Wall columns at odd x, with a gap alternately at the bottom and the top,
    so the `path` letter forms one long serpentine region."""
    g = [[path] * c for _ in range(r)]
    for x in range(1, c, 2):
        gap = r - 1 if x % 4 == 1 else 0
        for y in range(r):
            if y != gap:
                g[y][x] = wall
    return ["".join(row) for row in g]


def noise(rng: random.Random, r: int, c: int, letters: str, weights: list[float] | None = None) -> list[str]:
    return ["".join(rng.choices(letters, weights=weights, k=c)) for _ in range(r)]


def blocks(rng: random.Random, r: int, c: int, size: int, letters: str, flip: float) -> list[str]:
    tile = [[rng.choice(letters) for _ in range((c + size - 1) // size)] for _ in range((r + size - 1) // size)]
    rows = []
    for y in range(r):
        row = []
        for x in range(c):
            row.append(rng.choice(letters) if rng.random() < flip else tile[y // size][x // size])
        rows.append("".join(row))
    return rows


def checkerboard(r: int, c: int) -> list[str]:
    return ["".join("xy"[(y + x) % 2] for x in range(c)) for y in range(r)]


def validate(g: list[str], cap: int) -> None:
    r, c = len(g), len(g[0])
    assert 1 <= r <= cap <= MAX_SIDE and 1 <= c <= cap
    for row in g:
        assert len(row) == c and all(ch in LETTERS for ch in row)


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[list[str], int]] = []

    # --- subtask 1: R, C <= 30
    cases.append((["q"], 30))
    cases.append((noise(random.Random(20261204 + 2), 3, 30, "ab"), 30))
    cases.append((snake(30, 29), 30))

    # --- subtask 2: R, C <= 100
    cases.append((["z" * 100] * 100, 100))                                  # one region of 10^4
    cases.append((checkerboard(100, 100), 100))                             # 10^4 regions of 1
    cases.append((snake(40, 100, "m", "k"), 100))                        # shorter snake: the sweeps still finish

    # --- subtask 3: R, C <= 1,000
    cases.append((snake(1000, 1000), 1000))                                 # slow.cpp must TLE here
    cases.append((noise(random.Random(20261204 + 8), 1000, 1000, LETTERS), 1000))
    cases.append((blocks(random.Random(20261204 + 9), 1000, 1000, 25, "abc", 0.05), 1000))
    cases.append((noise(random.Random(20261204 + 10), 1000, 500, "ab", [0.62, 0.38]), 1000))

    assert len(cases) == 10
    for index, (g, cap) in enumerate(cases, start=1):
        validate(g, cap)
        text = f"{len(g)} {len(g[0])}\n" + "\n".join(g) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
