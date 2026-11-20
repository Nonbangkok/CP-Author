#!/usr/bin/env python3
"""Testcase generator for lp_rec02_permutations.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 have distinct letters, cases 4-10 may repeat letters (N <= 8 keeps
every output under 8! = 40,320 lines).
"""

import random
import sys
from pathlib import Path


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261120 + 400)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    words = [
        "q",                                          # N = 1
        "".join(rng.sample(alphabet, 5)),             # distinct, unsorted
        "".join(rng.sample(alphabet, 8)),             # distinct, full size: 40,320 lines
        "zz",                                         # one word only
        "aaaaaaaa",                                   # all the same: one line
        "bbbbaaaa",                                   # 70 words
        "".join(rng.choice("ab") for _ in range(7)) + "c",
        "hgfedcba"[:6] + "aa",                        # mostly distinct, one pair
        "".join(rng.choice("xyz") for _ in range(8)),
        "".join(rng.choices(alphabet[:7], k=8)),
    ]
    for index, word in enumerate(words, start=1):
        (out / f"input{index:02d}.txt").write_text(word + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
