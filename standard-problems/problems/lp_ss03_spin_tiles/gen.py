#!/usr/bin/env python3
"""Testcase generator for lp_ss03_spin_tiles.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic, smallest first:
cases 1-3 Q = 1 (the solved board, a random board, a farthest board);
cases 4-10 Q up to 20,000, where a fresh BFS per query must time out (case 4
already has 400 random boards). Includes boards one turn away in either
direction (a backwards-BFS that turns the wrong way gets these wrong), all the
farthest boards, and every board's 8 neighbours.
"""

import random
import sys
from operator import itemgetter
from pathlib import Path

BLOCKS = [(0, 1, 4, 3), (1, 2, 5, 4), (3, 4, 7, 6), (4, 5, 8, 7)]
GOAL = "123456789"
MAX_Q = 20000


def getter(block, clockwise: bool):
    a, b, c, d = block
    src = list(range(9))
    if clockwise:  # the tile at a moves to b, b to c, c to d, d to a
        src[b], src[c], src[d], src[a] = a, b, c, d
    else:
        src[a], src[b], src[c], src[d] = b, c, d, a
    return itemgetter(*src)


CW = [getter(b, True) for b in BLOCKS]
CCW = [getter(b, False) for b in BLOCKS]


def distances() -> dict[str, int]:
    dist = {GOAL: 0}
    queue = [GOAL]
    head = 0
    while head < len(queue):
        s = queue[head]
        head += 1
        for get in CCW:
            t = "".join(get(s))
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    return dist


def random_board(rng: random.Random) -> str:
    tiles = list(GOAL)
    rng.shuffle(tiles)
    return "".join(tiles)


def main() -> None:
    out = Path(sys.argv[1])
    dist = distances()
    assert len(dist) == 362880
    far = max(dist.values())
    farthest = sorted(s for s, d in dist.items() if d == far)
    states = sorted(dist)
    near = sorted({"".join(g(GOAL)) for g in CW + CCW})
    plans: list[list[str]] = []
    plans.append([GOAL])
    plans.append([random_board(random.Random(20261120 + 502))])
    plans.append([farthest[len(farthest) // 2]])
    rng = random.Random(20261120 + 504)
    plans.append([random_board(rng) for _ in range(400)])              # first big case
    rng = random.Random(20261120 + 505)
    plans.append(near + [random_board(rng) for _ in range(5000)])
    rng = random.Random(20261120 + 506)
    plans.append([random_board(rng) for _ in range(MAX_Q)])
    rng = random.Random(20261120 + 507)
    plans.append([rng.choice(farthest) for _ in range(MAX_Q)])
    rng = random.Random(20261120 + 508)
    walk = [GOAL]
    while len(walk) < MAX_Q:                                            # boards a few turns from the goal
        s = GOAL
        for _ in range(rng.randint(1, 6)):
            s = "".join(rng.choice(CW + CCW)(s))
        walk.append(s)
    plans.append(walk)
    rng = random.Random(20261120 + 509)
    plans.append(rng.sample(states, MAX_Q))
    rng = random.Random(20261120 + 510)
    plans.append([GOAL] * 100 + [random_board(rng) for _ in range(MAX_Q - 100)])
    for index, boards in enumerate(plans, start=1):
        assert 1 <= len(boards) <= (1 if index <= 3 else MAX_Q)
        assert all(sorted(b) == list(GOAL) for b in boards)
        lines = [str(len(boards))]
        for b in boards:
            lines += [" ".join(b[0:3]), " ".join(b[3:6]), " ".join(b[6:9])]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
