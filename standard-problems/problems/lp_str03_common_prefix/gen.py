#!/usr/bin/env python3
"""Testcase generator for lp_str03_common_prefix.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic, smallest first:
cases 1-3 N, Q <= 2,000; cases 4-10 N <= 10^5, Q <= 5 * 10^4. Case 4 is
"aaa...a" with every query near the front, so comparing letter by letter costs
~N per query and must time out. Also: periodic strings, few-letter random
strings, i = j, i or j = N, and a Thue-Morse case where a polynomial hash
taken mod 2^64 (unsigned overflow) collides for every base: the two halves are
A + T + Z and A + ~T + Z, T the Thue-Morse word of length 2048 over {a, b}.
"""

import random
import sys
from pathlib import Path

MAX_N = 10**5
MAX_Q = 5 * 10**4


def thue_morse(k: int) -> str:
    return "".join("ab"[bin(i).count("1") % 2] for i in range(1 << k))


def lcp(s: str, a: int, b: int) -> int:
    k = 0
    while a + k < len(s) and b + k < len(s) and s[a + k] == s[b + k]:
        k += 1
    return k


def random_string(rng: random.Random, n: int, letters: str) -> str:
    return "".join(rng.choice(letters) for _ in range(n))


def periodic(rng: random.Random, n: int, period: int, noise: int) -> str:
    unit = random_string(rng, period, "abc")
    s = list((unit * (n // period + 1))[:n])
    for _ in range(noise):
        s[rng.randrange(n)] = rng.choice("xyz")
    return "".join(s)


def random_queries(rng: random.Random, n: int, q: int) -> list[tuple[int, int]]:
    return [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[str, list[tuple[int, int]]]] = []
    cases.append(("a", [(1, 1)]))
    rng = random.Random(20261120 + 1001)
    s = periodic(rng, 2000, 7, 3)
    cases.append((s, random_queries(rng, 2000, 1997) + [(1, 2000), (2000, 2000), (5, 12)]))
    rng = random.Random(20261120 + 1002)
    s = random_string(rng, 1500, "ab")
    cases.append((s, random_queries(rng, 1500, 1990)))
    # first big case: all 'a', queries near the front -> answers close to N
    rng = random.Random(20261120 + 1003)
    cases.append(("a" * MAX_N, [(rng.randint(1, 1000), rng.randint(1, 1000)) for _ in range(MAX_Q)]))
    rng = random.Random(20261120 + 1004)
    s = periodic(rng, MAX_N, 13, 20)
    queries = [(rng.randint(1, 3000), rng.randint(1, 3000)) for _ in range(20000)]
    queries += [(i, i + 13 * rng.randint(1, 50)) for i in (rng.randint(1, 30000) for _ in range(10000))]
    cases.append((s, queries))
    rng = random.Random(20261120 + 1005)
    s = random_string(rng, MAX_N, "ab")
    cases.append((s, random_queries(rng, MAX_N, 30000) + [(MAX_N, 1), (1, MAX_N), (MAX_N, MAX_N)]))
    rng = random.Random(20261120 + 1006)
    t = thue_morse(11)
    flip = t.translate(str.maketrans("ab", "ba"))
    a_part = random_string(rng, 10, "ab")
    z_part = "ab" * 11000 + random_string(rng, 3000, "ab")
    half = a_part + t + z_part
    s = half + a_part + flip + z_part
    second = len(half) + 1
    queries = [(1 + d, second + d) for d in range(0, 12)] * 50
    queries += [(1 + len(a_part) + 2048 + d, second + len(a_part) + 2048 + d) for d in range(0, 3000, 7)]
    queries += random_queries(rng, len(s), 20000)
    cases.append((s, queries))
    rng = random.Random(20261120 + 1007)
    block = random_string(rng, 30000, "abcdefghijklmnopqrstuvwxyz")
    s = block + block[:29999] + "q" + block + "zz"
    s = s[:MAX_N]
    queries = [(rng.randint(1, 5000), 30000 * rng.randint(1, 2) + rng.randint(1, 5000)) for _ in range(30000)]
    cases.append((s, queries))
    rng = random.Random(20261120 + 1008)
    s = "a" * 60000 + "b" + "a" * 39999
    cases.append((s, random_queries(rng, MAX_N, 30000)))
    rng = random.Random(20261120 + 1009)
    s = periodic(rng, MAX_N, 1000, 0)
    queries = [(rng.randint(1, 50000), 0) for _ in range(30000)]
    queries = [(i, i + 1000 * rng.randint(1, 40)) for i, _ in queries]
    cases.append((s, queries))
    for index, (s, queries) in enumerate(cases, start=1):
        n, q = len(s), len(queries)
        cap_n, cap_q = (2000, 2000) if index <= 3 else (MAX_N, MAX_Q)
        assert 1 <= n <= cap_n and 1 <= q <= cap_q and s.isascii() and s.isalpha() and s.islower(), index
        assert all(1 <= i <= n and 1 <= j <= n for i, j in queries), index
        lines = [f"{n} {q}", s] + [f"{i} {j}" for i, j in queries]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # the Thue-Morse halves really collide mod 2^64 for an odd base, yet differ
    t_hash = lambda w, base: sum(ord(c) * pow(base, len(w) - 1 - k, 1 << 64) for k, c in enumerate(w)) % (1 << 64)
    assert t != flip and t_hash(t, 131) == t_hash(flip, 131)
    assert lcp(cases[6][0], 0, len(half)) == len(a_part)


if __name__ == "__main__":
    main()
