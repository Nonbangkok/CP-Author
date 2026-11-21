#!/usr/bin/env python3
"""Testcase generator for lp_ss02_blocked_queens.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic, smallest first:
cases 1-2 N <= 6; cases 3-5 N <= 9; cases 6-10 N = 11..12, where checking
every one of the N! column permutations at the end must time out (case 6 is
N = 12, the first case of the last subtask). Mixes empty floors, random broken
cells, a fully broken row (answer 0) and a broken main diagonal.
"""

import random
import sys
from pathlib import Path


def random_board(rng: random.Random, n: int, broken: float) -> list[str]:
    return ["".join("#" if rng.random() < broken else "." for _ in range(n)) for _ in range(n)]


def main() -> None:
    out = Path(sys.argv[1])
    boards: list[list[str]] = []
    boards.append(["."])                                                  # N = 1
    rng = random.Random(20261120 + 401)
    boards.append(random_board(rng, 6, 0.15))
    boards.append(["." * 8 for _ in range(8)])                            # classic 92
    rng = random.Random(20261120 + 403)
    boards.append(random_board(rng, 9, 0.2))
    rng = random.Random(20261120 + 404)
    boards.append(random_board(rng, 7, 0.1))
    boards.append(["." * 12 for _ in range(12)])                          # first big case: 14200
    rng = random.Random(20261120 + 406)
    boards.append(random_board(rng, 12, 0.1))
    rng = random.Random(20261120 + 407)
    boards.append(random_board(rng, 12, 0.3))
    diagonal = ["".join("#" if r == c else "." for c in range(11)) for r in range(11)]
    boards.append(diagonal)
    rng = random.Random(20261120 + 409)
    last = random_board(rng, 12, 0.05)
    last[7] = "#" * 12                                                    # no queen fits in row 8
    boards.append(last)
    caps = [6, 6, 9, 9, 9, 12, 12, 12, 12, 12]
    for index, (board, cap) in enumerate(zip(boards, caps), start=1):
        n = len(board)
        assert 1 <= n <= cap and all(len(row) == n and set(row) <= {".", "#"} for row in board)
        text = f"{n}\n" + "\n".join(board) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
