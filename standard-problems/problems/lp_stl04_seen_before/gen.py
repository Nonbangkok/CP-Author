#!/usr/bin/env python3
"""Testcase generator for lp_stl04_seen_before.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N <= 1,000; cases 4-5 N = 50,000 with at most 20 distinct words;
cases 6-10 N = 50,000 with many distinct words, where searching a list of the
words seen so far (O(N * D)) must time out (case 6: every word distinct).
Words that are prefixes of each other (hi / hii) and one-letter words appear.
"""

import random
import string
import sys
from pathlib import Path


def word(rng: random.Random, low: int = 1, high: int = 10) -> str:
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randint(low, high)))


def vocabulary(rng: random.Random, size: int, low: int = 1) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    while len(out) < size:
        if out and rng.random() < 0.2:  # prefix / extension of an existing word
            base = rng.choice(out)
            w = base + rng.choice("ab") if len(base) < 10 else base[:-1]
        else:
            w = word(rng, low)
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


def case(rng: random.Random, n: int, distinct: int, skew: bool = False) -> str:
    vocab = vocabulary(rng, distinct, low=1 if distinct < 500 else 4)
    if distinct == n:
        words = vocab[:]
        rng.shuffle(words)
    elif skew:
        words = [vocab[min(int(rng.paretovariate(1.0)) - 1, distinct - 1)] for _ in range(n)]
    else:
        words = [rng.choice(vocab) for _ in range(n)]
    return f"{n}\n" + "".join(w + "\n" for w in words)


def main() -> None:
    out = Path(sys.argv[1])
    rngs = [random.Random(20261120 + i) for i in range(1, 11)]
    plans = [(1, 1), (30, 5), (1000, 300), (50000, 20), (50000, 1),
             (50000, 50000), (50000, 30000), (50000, 5000), (50000, 40000), (50000, 50000)]
    for index, (n, distinct) in enumerate(plans, start=1):
        body = case(rngs[index - 1], n, distinct, skew=index == 8)
        (out / f"input{index:02d}.txt").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
