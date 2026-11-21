#!/usr/bin/env python3
"""Testcase generator for lp_dpk02_typo_fixer.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 |A|, |B| <= 10; cases 4-10 |A|, |B| <= 2,000. Case 4 (16 x 16)
already needs ~10^11 calls of the memo-less recursion. Covers single letters,
identical words, replace dearer than delete + insert, insert/delete very dear,
B a few typos away from A, unrelated words, and very different lengths.
"""

import random
import sys
from pathlib import Path

MAX_LEN, MAX_COST = 2000, 1000


def write(out: Path, index: int, a: str, b: str, ins: int, dele: int, rep: int) -> None:
    assert 1 <= len(a) <= MAX_LEN and 1 <= len(b) <= MAX_LEN
    assert all("a" <= ch <= "z" for ch in a + b)
    assert all(1 <= x <= MAX_COST for x in (ins, dele, rep))
    if index <= 3:
        assert len(a) <= 10 and len(b) <= 10
    (out / f"input{index:02d}.txt").write_text(f"{a}\n{b}\n{ins} {dele} {rep}\n", encoding="utf-8")


def word(rng: random.Random, n: int, letters: str) -> str:
    return "".join(rng.choice(letters) for _ in range(n))


def typos(rng: random.Random, s: str, count: int) -> str:
    chars = list(s)
    for _ in range(count):
        kind = rng.randrange(3)
        at = rng.randrange(len(chars))
        if kind == 0 and len(chars) > 1:
            del chars[at]
        elif kind == 1:
            chars.insert(at, rng.choice("abcdefghijklmnopqrstuvwxyz"))
        else:
            chars[at] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    return "".join(chars)


def main() -> None:
    out = Path(sys.argv[1])
    rng = random.Random(20261205)
    write(out, 1, "a", "b", 5, 7, 3)
    write(out, 2, "banana", "banana", 1, 1, 1)                               # identical: 0
    write(out, 3, word(rng, 10, "ab"), word(rng, 10, "ab"), 4, 6, 9)       # slow's worst small case
    write(out, 4, word(rng, 16, "abc"), word(rng, 16, "abc"), 3, 2, 4)     # first big case: recursion must TLE
    base = word(rng, MAX_LEN, "abcdefghijklmnopqrstuvwxyz")
    write(out, 5, base, typos(rng, base, 150)[:MAX_LEN], 7, 5, 6)           # a few typos away
    write(out, 6, word(rng, MAX_LEN, "ab"), word(rng, MAX_LEN, "ab"), 2, 3, 1000)  # replace dearer than del + ins
    write(out, 7, word(rng, MAX_LEN, "abcd"), word(rng, MAX_LEN, "abcd"), 1000, 1000, 1)
    write(out, 8, word(rng, MAX_LEN, "xyz"), word(rng, 37, "xyz"), 9, 1, 4)  # very different lengths
    write(out, 9, word(rng, 1, "q"), word(rng, MAX_LEN, "pq"), 1000, 1000, 1000)
    write(out, 10, word(rng, MAX_LEN, "abcdefghijklmnopqrstuvwxyz"), word(rng, MAX_LEN, "abcdefghijklmnopqrstuvwxyz"), 13, 17, 21)


if __name__ == "__main__":
    main()
