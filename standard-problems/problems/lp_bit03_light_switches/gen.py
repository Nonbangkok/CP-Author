#!/usr/bin/env python3
"""Testcase generator for lp_bit03_light_switches.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 M <= 10; cases 4-5 N <= 20, M = 20; cases 6-10 N up to 60, M = 20.
Most targets are planted (the XOR of a hidden set of switches, with extra
switches that are XORs of others, so a cheaper set may exist than the planted
one); some cases are impossible (-1) or already solved (0). Lamps 32..60
exist from case 6 on, so building the mask with 1 << p in int breaks.
"""

import random
import sys
from pathlib import Path


def to_string(mask: int, n: int) -> str:
    return "".join("1" if (mask >> p) & 1 else "0" for p in range(n))


def case(rng: random.Random, n: int, m: int, kind: str) -> str:
    full = (1 << n) - 1
    base = max(1, m * 2 // 3)
    switches = [rng.randint(1, full) for _ in range(base)]
    while len(switches) < m:
        # A dependent switch: the XOR of a few existing ones (a shortcut).
        picks = rng.sample(range(len(switches)), min(len(switches), rng.randint(2, 4)))
        value = 0
        for p in picks:
            value ^= switches[p]
        switches.append(value if value else rng.randint(1, full))
    rng.shuffle(switches)
    if kind == "done":
        off = 0
    elif kind == "impossible":
        basis = [0] * n  # basis[b] has highest bit b (Gaussian elimination over GF(2))
        for s in switches:
            for b in range(n - 1, -1, -1):
                if (s >> b) & 1:
                    if basis[b]:
                        s ^= basis[b]
                    else:
                        basis[b] = s
                        break
        while True:
            off = rng.randint(1, full)
            x = off
            for b in range(n - 1, -1, -1):
                if (x >> b) & 1 and basis[b]:
                    x ^= basis[b]
            if x:  # not a XOR of any set of switches
                break
    else:
        chosen = [s for s in switches if rng.random() < 0.6]
        off = 0
        for s in chosen:
            off ^= s
    lamps = full ^ off
    lines = [f"{n} {m}", to_string(lamps, n)] + [to_string(s, n) for s in switches]
    return "\n".join(lines) + "\n"


def main() -> None:
    out = Path(sys.argv[1])
    plans = [
        (3, 3, "planted"), (8, 6, "impossible"), (30, 10, "planted"),
        (20, 20, "planted"), (20, 20, "impossible"),
        (60, 20, "planted"), (60, 20, "done"), (45, 20, "planted"), (60, 20, "impossible"), (60, 20, "planted"),
    ]
    for index, (n, m, kind) in enumerate(plans, start=1):
        rng = random.Random(20261120 + 100 * index + 47)
        (out / f"input{index:02d}.txt").write_text(case(rng, n, m, kind), encoding="utf-8")


if __name__ == "__main__":
    main()
