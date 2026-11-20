#!/usr/bin/env python3
"""Testcase generator for lp_str01_chant_count.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic, smallest first:
cases 1-3 |T| <= 5,000; cases 4-10 |T| up to 10^6. Case 4 is T = "aaa...a",
P = "aaa...a" of half the length: every start matches for a long time, so
comparing from every start (O(|T| |P|)) must time out. Also: P = T, P longer
runs with one different letter at the end, periodic text, random text over
two letters, a single-letter pattern, and no occurrence at all. The last
case is "abab..." with a long "abab..." pattern, again quadratic for the naive scan.
Total size stays under ~5 MiB.
"""

import random
import sys
from pathlib import Path

MAX_T = 10**6


def rand(rng: random.Random, n: int, letters: str) -> str:
    return "".join(rng.choice(letters) for _ in range(n))


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[str, str]] = []
    cases.append(("a", "a"))
    rng = random.Random(20261120 + 801)
    cases.append((rand(rng, 3000, "ab"), "abab"))
    cases.append(("a" * 4999 + "b", "a" * 2000 + "b"))
    cases.append(("a" * 600000, "a" * 300000))                         # first big case
    rng = random.Random(20261120 + 805)
    cases.append((rand(rng, 300000, "xyz"), "y"))                      # single-letter pattern
    t = ("a" * 999 + "b") * 600
    cases.append((t, "a" * 1500 + "b"))                                # never matches, long partial matches
    rng = random.Random(20261120 + 806)
    cases.append((rand(rng, MAX_T, "ab"), "abbab"))
    rng = random.Random(20261120 + 807)
    unit = rand(rng, 37, "abc")
    t = (unit * (800000 // 37 + 1))[:800000]
    cases.append((t, unit * 100 + unit[:5]))
    rng = random.Random(20261120 + 808)
    t = rand(rng, 300000, "abcdefghijklmnopqrstuvwxyz")
    cases.append((t, t))                                               # P = T
    cases.append(("ab" * 250000, "ab" * 50000))                        # half the starts match 10^5 letters
    for index, (t, p) in enumerate(cases, start=1):
        cap = 5000 if index <= 3 else MAX_T
        assert 1 <= len(p) <= len(t) <= cap and t.isalpha() and t.islower() and p.isalpha() and p.islower()
        (out / f"input{index:02d}.txt").write_text(f"{t}\n{p}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
