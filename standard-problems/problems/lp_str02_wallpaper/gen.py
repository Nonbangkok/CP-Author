#!/usr/bin/env python3
"""Testcase generator for lp_str02_wallpaper.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic, smallest first:
cases 1-3 N <= 1,000, Q <= 100; cases 4-10 N <= 2 * 10^5, Q <= 2 * 10^4.
Case 4 is "aaa...ab" with long prefixes asked, where trying every period and
checking the whole prefix costs ~L^2 / 2 per query and must time out. Also:
exact repetitions (p | L), periods that do not divide L, a single letter,
nested periodic blocks ("aab aab aac ..." style), random text.
"""

import random
import sys
from pathlib import Path

MAX_N = 2 * 10**5
MAX_Q = 2 * 10**4


def rand(rng: random.Random, n: int, letters: str) -> str:
    return "".join(rng.choice(letters) for _ in range(n))


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[str, list[int]]] = []
    cases.append(("z", [1]))
    rng = random.Random(20261120 + 901)
    unit = rand(rng, 6, "ab")
    s = (unit * 200)[:1000]
    cases.append((s, [rng.randint(1, 1000) for _ in range(90)] + [1000, 999, 6, 12, 7]))
    rng = random.Random(20261120 + 902)
    s = "a" * 999 + "b"
    cases.append((s, [1000, 999, 998, 500] + [rng.randint(1, 1000) for _ in range(96)]))
    # first big case: "aaa...ab", long prefixes that end with the b
    rng = random.Random(20261120 + 903)
    s = "a" * (MAX_N - 1) + "b"
    cases.append((s, [MAX_N - rng.randint(0, 0) for _ in range(30)] + [rng.randint(1, MAX_N) for _ in range(MAX_Q - 30)]))
    rng = random.Random(20261120 + 904)
    unit = rand(rng, 1234, "abc")
    s = (unit * (MAX_N // 1234 + 1))[:MAX_N]
    qs = [1234 * rng.randint(1, MAX_N // 1234) for _ in range(MAX_Q // 2)]
    qs += [rng.randint(1, MAX_N) for _ in range(MAX_Q - len(qs))]
    cases.append((s, qs))
    rng = random.Random(20261120 + 905)
    block = "aab" * 3 + "aac"                       # nested: period 12 built of near-period 3
    s = (block * (MAX_N // len(block) + 1))[:MAX_N]
    cases.append((s, [rng.randint(1, MAX_N) for _ in range(MAX_Q)]))
    rng = random.Random(20261120 + 906)
    cases.append(("q" * MAX_N, [rng.randint(1, MAX_N) for _ in range(MAX_Q)]))
    rng = random.Random(20261120 + 907)
    s = rand(rng, MAX_N, "ab")
    cases.append((s, list(range(1, MAX_Q + 1))))
    rng = random.Random(20261120 + 908)
    w = rand(rng, 50, "abcdefghijklmnopqrstuvwxyz")
    s = (w * 3999)[: MAX_N - 3] + "xyz"
    s = s[:MAX_N]
    cases.append((s, [50 * rng.randint(1, 3999) for _ in range(MAX_Q // 2)] + [rng.randint(1, len(s)) for _ in range(MAX_Q // 2)]))
    rng = random.Random(20261120 + 909)
    s = rand(rng, MAX_N, "abcdefghijklmnopqrstuvwxyz")
    cases.append((s, [rng.randint(1, MAX_N) for _ in range(MAX_Q)]))
    for index, (s, qs) in enumerate(cases, start=1):
        cap_n, cap_q = (1000, 100) if index <= 3 else (MAX_N, MAX_Q)
        n = len(s)
        assert 1 <= n <= cap_n and 1 <= len(qs) <= cap_q and s.isalpha() and s.islower(), index
        assert all(1 <= x <= n for x in qs), index
        text = f"{n} {len(qs)}\n{s}\n" + " ".join(map(str, qs)) + "\n"
        (out / f"input{index:02d}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
