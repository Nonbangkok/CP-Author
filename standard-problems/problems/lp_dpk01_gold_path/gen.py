#!/usr/bin/env python3
"""Testcase generator for lp_dpk01_gold_path.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 R, C <= 10; cases 4-10 R, C <= 1,000. Case 4 (18 x 18 without
rocks) already has C(34, 17) ~ 2.3 * 10^9 paths, too many to walk one by one.
Covers 1 x 1, a rock on the start, a single column, a rock wall (answer -1),
and rocky grids that keep one random right/down corridor open so a path exists.
"""

import random
import sys
from pathlib import Path

MAX_SIDE = 1000


def write(out: Path, index: int, grid: list[str]) -> None:
    rows, cols = len(grid), len(grid[0])
    assert 1 <= rows <= MAX_SIDE and 1 <= cols <= MAX_SIDE
    assert all(len(line) == cols and set(line) <= set("0123456789#") for line in grid)
    if index <= 3:
        assert rows <= 10 and cols <= 10
    (out / f"input{index:02d}.txt").write_text(f"{rows} {cols}\n" + "\n".join(grid) + "\n", encoding="utf-8")


def random_grid(rng: random.Random, rows: int, cols: int, rock: float, corridor: bool) -> list[str]:
    cells = [["#" if rng.random() < rock else str(rng.randint(0, 9)) for _ in range(cols)] for _ in range(rows)]
    if corridor:  # carve one random monotone path from (0, 0) to the end
        r = c = 0
        while True:
            if cells[r][c] == "#":
                cells[r][c] = str(rng.randint(0, 9))
            if r == rows - 1 and c == cols - 1:
                break
            if r == rows - 1 or (c < cols - 1 and rng.random() < cols / (rows + cols)):
                c += 1
            else:
                r += 1
    return ["".join(row) for row in cells]


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261204)
    write(out, 1, ["7"])                                                       # 1 x 1
    write(out, 2, ["#12", "345"])                                              # rock on the start: -1
    write(out, 3, random_grid(rng, 10, 10, 0.0, False))                        # slow's worst small case
    write(out, 4, random_grid(rng, 18, 18, 0.0, False))                        # first big case: recursion must TLE
    write(out, 5, random_grid(rng, MAX_SIDE, 1, 0.0, False))                   # a single column
    wall = random_grid(rng, 600, 1000, 0.1, False)
    wall = [line[:299] + "#" + line[300:] for line in wall]                    # a full column of rock: -1
    write(out, 6, wall)
    write(out, 7, random_grid(rng, 600, 1000, 0.35, True))
    write(out, 8, random_grid(rng, 1000, 500, 0.2, True))
    write(out, 9, random_grid(rng, 3, 1000, 0.3, True))
    write(out, 10, random_grid(rng, MAX_SIDE, MAX_SIDE, 0.05, True))


if __name__ == "__main__":
    main()
