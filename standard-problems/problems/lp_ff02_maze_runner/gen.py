#!/usr/bin/env python3
"""Testcase generator for lp_ff02_maze_runner.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 R, C <= 30; cases 4-6 R, C <= 100; cases 7-10 R, C <= 1,000. Cells
are '#', '.', and exactly one 'S' and one 'E'. Covers a 1 x 2 maze, an exit
that cannot be reached (small, and a big open field around a sealed exit),
an empty field, random walls, perfect mazes, and serpentine corridors: there
the sweep-until-nothing-changes approach needs about one sweep per upward
step and must time out (case 7, 1000 x 1000).
"""

import random
import sys
from collections import deque
from pathlib import Path

MAX_SIDE = 1000


def snake(r: int, c: int) -> list[list[str]]:
    g = [["."] * c for _ in range(r)]
    for x in range(1, c, 2):
        gap = r - 1 if x % 4 == 1 else 0
        for y in range(r):
            if y != gap:
                g[y][x] = "#"
    return g


def perfect_maze(rng: random.Random, r: int, c: int) -> list[list[str]]:
    """Iterative backtracker; rooms at even coordinates, r and c odd."""
    g = [["#"] * c for _ in range(r)]
    g[0][0] = "."
    stack = [(0, 0)]
    while stack:
        y, x = stack[-1]
        options = [(y + dy, x + dx, dy, dx) for dy, dx in ((-2, 0), (2, 0), (0, -2), (0, 2))
                   if 0 <= y + dy < r and 0 <= x + dx < c and g[y + dy][x + dx] == "#"]
        if not options:
            stack.pop()
            continue
        ny, nx, dy, dx = rng.choice(options)
        g[y + dy // 2][x + dx // 2] = "."
        g[ny][nx] = "."
        stack.append((ny, nx))
    return g


def random_walls(rng: random.Random, r: int, c: int, density: float) -> list[list[str]]:
    return [["#" if rng.random() < density else "." for _ in range(c)] for _ in range(r)]


def place(g: list[list[str]], s: tuple[int, int], e: tuple[int, int]) -> list[str]:
    g[s[0]][s[1]] = "S"
    g[e[0]][e[1]] = "E"
    return ["".join(row) for row in g]


def shortest(g: list[str]) -> int:
    r, c = len(g), len(g[0])
    flat = "".join(g)
    s, e = flat.index("S"), flat.index("E")
    dist = {s: 0}
    q = deque([s])
    while q:
        cur = q.popleft()
        y, x = divmod(cur, c)
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < r and 0 <= nx < c and g[ny][nx] != "#" and ny * c + nx not in dist:
                dist[ny * c + nx] = dist[cur] + 1
                q.append(ny * c + nx)
    return dist.get(e, -1)


def random_open(rng: random.Random, g: list[list[str]]) -> tuple[int, int]:
    while True:
        y, x = rng.randrange(len(g)), rng.randrange(len(g[0]))
        if g[y][x] == ".":
            return y, x


def snake_end(r: int, c: int) -> tuple[int, int]:
    """The far end of the serpentine that starts at (0, 0)."""
    last = c - 1 if (c - 1) % 2 == 0 else c - 2
    return (r - 1 if (last // 2) % 2 == 0 else 0), last


def validate(g: list[str], cap: int) -> None:
    r, c = len(g), len(g[0])
    assert 1 <= r <= cap <= MAX_SIDE and 1 <= c <= cap and r * c >= 2
    flat = "".join(g)
    assert all(len(row) == c for row in g) and set(flat) <= set("#.SE")
    assert flat.count("S") == 1 and flat.count("E") == 1


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[list[str], int, int | None]] = []   # grid, cap, expected (None: positive, any)

    # --- subtask 1: R, C <= 30
    cases.append((["SE"], 30, 1))
    sealed = [list(".....") for _ in range(5)]
    for y, x in ((1, 2), (2, 1), (2, 3), (3, 2)):
        sealed[y][x] = "#"
    cases.append((place(sealed, (0, 0), (2, 2)), 30, -1))
    rng = random.Random(20261205 + 3)
    cases.append((place(perfect_maze(rng, 29, 29), (0, 0), (28, 28)), 30, None))

    # --- subtask 2: R, C <= 100
    cases.append((place([["."] * 100 for _ in range(100)], (0, 0), (99, 99)), 100, 198))
    rng = random.Random(20261205 + 5)
    g = random_walls(rng, 100, 100, 0.3)
    g[0][0] = g[99][99] = "."
    cases.append((place(g, (0, 0), (99, 99)), 100, None))
    cases.append((place(snake(40, 100), (0, 0), snake_end(40, 100)), 100, None))

    # --- subtask 3: R, C <= 1,000
    cases.append((place(snake(1000, 1000), (0, 0), snake_end(1000, 1000)), 1000, None))   # slow.cpp must TLE here
    rng = random.Random(20261205 + 8)
    cases.append((place(perfect_maze(rng, 999, 999), (0, 0), (998, 998)), 1000, None))
    field = [["."] * 1000 for _ in range(1000)]
    for y, x in ((499, 500), (501, 500), (500, 499), (500, 501)):
        field[y][x] = "#"
    cases.append((place(field, (0, 0), (500, 500)), 1000, -1))                            # sealed exit, BFS sees everything
    rng = random.Random(20261205 + 10)
    g = random_walls(rng, 1000, 600, 0.3)
    s = random_open(rng, g)
    e = random_open(rng, g)
    cases.append((place(g, s, e), 1000, None))

    assert len(cases) == 10
    for index, (g, cap, expected) in enumerate(cases, start=1):
        validate(g, cap)
        answer = shortest(g)
        assert answer == expected if expected is not None else answer > 0, (index, answer)
        text = f"{len(g)} {len(g[0])}\n" + "\n".join(g) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
