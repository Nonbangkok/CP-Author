#!/usr/bin/env python3
"""Testcase generator for lp_dp02_secret_code.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 20; cases 4-10 N <= 2 * 10^5. Case 4 (N = 200, all ones,
M = 111) already has ~10^52 cuttings, so counting them one by one must time
out. Most big cases are concatenations of valid sticker numbers, so the answer
is not 0 and zeros sit inside pieces (100, 205, 10); one is random digits with
a "000" that kills every cutting, and one has M = 1 (exactly one way).
"""

import random
import sys
from pathlib import Path

MAX_N, MAX_M = 2 * 10**5, 999


def write(out: Path, index: int, m: int, s: str) -> None:
    n = len(s)
    assert 1 <= n <= MAX_N and 1 <= m <= MAX_M and s.isdigit() and s.isascii()
    if index <= 3:
        assert n <= 20
    (out / f"input{index:02d}.txt").write_text(f"{n} {m}\n{s}\n", encoding="utf-8")


def stickers(rng: random.Random, n: int, m: int, pool: list[int] | None = None) -> str:
    """Concatenate random numbers in [1, m] (or from pool) until length n, then cut to n."""
    parts: list[str] = []
    length = 0
    while length < n:
        v = rng.choice(pool) if pool else rng.randint(1, m)
        parts.append(str(v))
        length += len(parts[-1])
    s = "".join(parts)[:n]
    return s


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261202)
    write(out, 1, 5, "0")                                                    # a lone zero: 0 ways
    write(out, 2, 26, stickers(rng, 20, 26))
    write(out, 3, 999, "1" * 20)                                             # slow's worst small case
    write(out, 4, 111, "1" * 200)                                            # first big case: enumeration must TLE
    write(out, 5, 10, stickers(rng, MAX_N, 10))                              # lots of "10"
    write(out, 6, 26, stickers(rng, MAX_N, 26))
    write(out, 7, 999, stickers(rng, MAX_N, 999, [100, 205, 990, 101, 7, 30, 999, 1, 12]))
    s8 = "".join(rng.choice("0123456789") for _ in range(MAX_N))
    s8 = s8[:MAX_N // 2] + "000" + s8[MAX_N // 2 + 3:]
    write(out, 8, 500, s8)                                                   # "000": 0 ways
    write(out, 9, 1, "1" * MAX_N)                                            # M = 1: exactly one way
    write(out, 10, 999, "1" * MAX_N)                                         # every piece of 1..3 ones is valid


if __name__ == "__main__":
    main()
