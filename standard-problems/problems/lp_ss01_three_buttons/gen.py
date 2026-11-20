#!/usr/bin/env python3
"""Testcase generator for lp_ss01_three_buttons.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic, smallest first:
cases 1-3 L <= 100 with answer <= 10; cases 4-5 answer <= 12 (L up to 10^6);
cases 6-10 L up to 10^6 with answers above 20, where trying every sequence of
presses (3^answer) must time out. Every target is checked reachable by BFS.
"""

import random
import sys
from pathlib import Path


def bfs(limit: int, start: int) -> list[int]:
    dist = [-1] * (limit + 1)
    dist[start] = 0
    queue = [start]
    head = 0
    while head < len(queue):
        x = queue[head]
        head += 1
        for y in (2 * x, x - 1, int(str(x)[::-1])):
            if 1 <= y <= limit and dist[y] < 0:
                dist[y] = dist[x] + 1
                queue.append(y)
    return dist


def pick(rng: random.Random, limit: int, start: int, want: int) -> int:
    """A target at distance exactly `want` from start (the largest one if want < 0)."""
    dist = bfs(limit, start)
    if want < 0:
        want = max(dist)
    choices = [t for t in range(1, limit + 1) if dist[t] == want]
    assert choices, (limit, start, want)
    return rng.choice(choices)


def main() -> None:
    out = Path(sys.argv[1])
    # (L, S, wanted answer or a fixed target as ("t", T)), and the cap the subtask promises
    plans = [
        (1, 1, ("t", 1), 10),           # L = 1: nothing to press, answer 0
        (100, 63, 6, 10),
        (100, 97, 10, 10),
        (1000000, 777777, 12, 12),
        (500000, 1, 12, 12),
        (1000000, 1, -1, None),          # first big case: the farthest target from 1
        (1000000, 999999, -1, None),
        (999999, 123456, 22, None),
        (1000000, 1000000, -1, None),
        (654321, 2, 21, None),
    ]
    for index, (limit, start, want, cap) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 300 + index)
        if isinstance(want, tuple):
            target = want[1]
        else:
            target = pick(rng, limit, start, want)
        answer = bfs(limit, start)[target]
        assert 1 <= start <= limit <= 10**6 and 1 <= target <= limit and answer >= 0
        if cap is not None:
            assert answer <= cap, (index, answer)
            if index <= 3:
                assert limit <= 100
        else:
            assert answer > 20, (index, answer)
        (out / f"input{index:02d}.txt").write_text(f"{limit} {start} {target}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
