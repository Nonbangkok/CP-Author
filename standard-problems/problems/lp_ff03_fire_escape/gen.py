#!/usr/bin/env python3
"""Testcase generator for lp_ff03_fire_escape.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 R, C <= 30; cases 4-6 R, C <= 100; cases 7-10 R, C <= 1,000. Cells
are '#', '.', 'F' (any number, possibly none) and exactly one 'J'. Covers a
1 x 1 warehouse, J on the edge next to a fire, no fire at all, fire on every
edge cell (no way out, case 9), random walls and fires, and a walled
serpentine corridor with the fire one step behind J (cases 6 and 7): J
escapes after ~RC/2 minutes, so a minute-by-minute simulation of the whole
grid must time out (case 7, 1000 x 999). Every answer is recomputed here with
an independent BFS and asserted where it is known in advance.
"""

import random
import sys
from collections import deque
from pathlib import Path

MAX_SIDE = 1000
INF = 1 << 30


def fire_times(g: list[str]) -> list[int]:
    """Minute each cell catches fire (flat index y * c + x), INF if never."""
    r, c = len(g), len(g[0])
    flat = "".join(g)
    fire = [INF] * (r * c)
    q = deque(i for i, ch in enumerate(flat) if ch == "F")
    for i in q:
        fire[i] = 0
    while q:
        cur = q.popleft()
        y, x = divmod(cur, c)
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            v = ny * c + nx
            if 0 <= ny < r and 0 <= nx < c and flat[v] != "#" and fire[v] == INF:
                fire[v] = fire[cur] + 1
                q.append(v)
    return fire


def escape(g: list[str], fire: list[int], start: int) -> int:
    r, c = len(g), len(g[0])
    me = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        y, x = divmod(cur, c)
        t = me[cur]
        if y in (0, r - 1) or x in (0, c - 1):
            return t + 1
        for v in (cur - c, cur + c, cur - 1, cur + 1):
            if g[v // c][v % c] != "#" and v not in me and t + 1 < fire[v]:
                me[v] = t + 1
                q.append(v)
    return -1


def answer(g: list[str]) -> int:
    flat = "".join(g)
    return escape(g, fire_times(g), flat.index("J"))


def walled_snake(r: int, c: int) -> tuple[list[str], int]:
    """A border of walls around a serpentine corridor (inner width c - 2 must be
    odd). F at the corridor's start, J right after it, one exit in the border
    at the far end. Returns (grid, corridor length)."""
    ir, ic = r - 2, c - 2
    assert ic % 2 == 1 and ir >= 2
    g = [["#"] * c for _ in range(r)]
    for y in range(ir):
        for x in range(ic):
            wall_col = x % 2 == 1
            gap = ir - 1 if x % 4 == 1 else 0
            if not wall_col or y == gap:
                g[y + 1][x + 1] = "."
    g[1][1] = "F"
    g[2][1] = "J"
    last = ic - 1
    end_row = ir - 1 if (last // 2) % 2 == 0 else 0
    exit_row = r - 1 if end_row == ir - 1 else 0
    g[exit_row][last + 1] = "."
    cells = sum(row.count(".") for row in g) + 1           # + J
    return ["".join(row) for row in g], cells


def random_grid(rng: random.Random, r: int, c: int, walls: float, fires: int, fire_cols: int = 0) -> list[list[str]]:
    """Random walls; fires anywhere, or only in the first `fire_cols` columns."""
    g = [["#" if rng.random() < walls else "." for _ in range(c)] for _ in range(r)]
    for _ in range(fires):
        g[rng.randrange(r)][rng.randrange(fire_cols or c)] = "F"
    return g


def with_j(rng: random.Random, g: list[list[str]], minimum: int) -> list[str]:
    """Put J on a random open cell whose answer is at least `minimum`; tries
    cells until one fits (deterministic)."""
    r, c = len(g), len(g[0])
    rows = ["".join(row) for row in g]
    fire = fire_times(rows)
    for _ in range(10_000):
        y, x = rng.randrange(r), rng.randrange(c)
        if g[y][x] != "." or fire[y * c + x] <= minimum:
            continue
        if escape(rows, fire, y * c + x) >= minimum:
            g[y][x] = "J"
            return ["".join(row) for row in g]
    raise AssertionError("no suitable J found")


def validate(g: list[str], cap: int) -> None:
    r, c = len(g), len(g[0])
    assert 1 <= r <= cap <= MAX_SIDE and 1 <= c <= cap
    flat = "".join(g)
    assert all(len(row) == c for row in g) and set(flat) <= set("#.FJ")
    assert flat.count("J") == 1


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[list[str], int, int | None]] = []        # grid, cap, expected (None: anything)

    # --- subtask 1: R, C <= 30
    cases.append((["J"], 30, 1))
    cases.append((["F#F", "FJF"], 30, 1))                       # J stands on the edge: out in 1 minute
    rng = random.Random(20261206 + 3)
    cases.append((with_j(rng, random_grid(rng, 30, 30, 0.25, 4), 6), 30, None))

    # --- subtask 2: R, C <= 100
    open_field = [["."] * 100 for _ in range(100)]
    open_field[50][50] = "J"
    cases.append((["".join(row) for row in open_field], 100, 50))      # no fire at all
    rng = random.Random(20261206 + 5)
    cases.append((with_j(rng, random_grid(rng, 100, 100, 0.2, 8), 15), 100, None))
    g, length = walled_snake(30, 99)
    cases.append((g, 100, length))                               # J takes `length` corridor steps, last one out

    # --- subtask 3: R, C <= 1,000
    g, length = walled_snake(1000, 999)
    cases.append((g, 1000, length))                              # slow.cpp must TLE here
    rng = random.Random(20261206 + 8)
    cases.append((with_j(rng, random_grid(rng, 1000, 1000, 0.3, 60), 40), 1000, None))
    ring = [["."] * 1000 for _ in range(1000)]
    for i in range(1000):
        ring[0][i] = ring[999][i] = ring[i][0] = ring[i][999] = "F"
    ring[500][500] = "J"
    cases.append((["".join(row) for row in ring], 1000, -1))     # every edge cell burns from minute 0
    rng = random.Random(20261206 + 10)
    cases.append((with_j(rng, random_grid(rng, 1000, 1000, 0.1, 1500, 300), 10), 1000, None))

    assert len(cases) == 10
    for index, (g, cap, expected) in enumerate(cases, start=1):
        validate(g, cap)
        if expected is not None:
            assert answer(g) == expected, (index, answer(g), expected)
        text = f"{len(g)} {len(g[0])}\n" + "\n".join(g) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
