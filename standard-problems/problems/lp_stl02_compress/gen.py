#!/usr/bin/env python3
"""Testcase generator for lp_stl02_compress.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N = 50,000 with at most 100 distinct values;
cases 6-10 N = 50,000 with up to N distinct values, where the O(N * D) linear
search must time out (case 6 is all distinct).
"""

import random
import sys
from pathlib import Path

LIMIT = 10**9


def case(rng: random.Random, n: int, distinct: int | None, spread: int) -> str:
    if distinct is None:
        values = [rng.randint(-spread, spread) for _ in range(n)]
    else:
        pool = rng.sample(range(-spread, spread + 1), distinct)
        values = [rng.choice(pool) for _ in range(n)]
        values[:distinct] = pool  # every pool value appears at least once
        rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


def all_distinct(rng: random.Random, n: int) -> str:
    values = rng.sample(range(-LIMIT, LIMIT + 1), n)
    values[0], values[1] = -LIMIT, LIMIT
    rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    texts: list[str] = []
    rngs = [random.Random(20261120 + i) for i in range(1, 11)]
    texts.append("1\n-1000000000\n")
    texts.append(case(rngs[1], 50, None, 10))
    texts.append(case(rngs[2], 1000, None, LIMIT))
    texts.append(case(rngs[3], 50000, 100, LIMIT))
    texts.append(case(rngs[4], 50000, 1, 5))
    texts.append(all_distinct(rngs[5], 50000))
    texts.append(case(rngs[6], 50000, None, LIMIT))
    texts.append(case(rngs[7], 50000, None, 20000))
    texts.append(case(rngs[8], 50000, 30000, LIMIT))
    texts.append(all_distinct(rngs[9], 50000))
    for index, text in enumerate(texts, start=1):
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
