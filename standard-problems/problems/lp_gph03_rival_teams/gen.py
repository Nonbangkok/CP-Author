#!/usr/bin/env python3
"""Testcase generator for lp_gph03_rival_teams.

    python3 gen.py <output-directory>

Writes input01.txt .. input10.txt, deterministic (fixed seeds), smallest first:
cases 1-3 N, M <= 100; cases 4-6 N, M <= 1,000; cases 7-10 N <= 5 * 10^4,
M <= 10^5. Rivalries are undirected, 1-indexed, u != v, no repeated pair.

Each case is built from a hidden two-colouring: rivalries across the colours
never break anything, and the planned "breaking" rivalry joins two vertices of
the same colour that are already connected (an odd cycle). The answer is
recomputed with a union-find with parity and asserted. Covers M = 1, a lone
triangle, a tree, an odd cycle closed by the very last rivalry, an even cycle,
a same-colour rivalry between two different groups (harmless: one group just
flips), and in case 7 an answer of exactly M, so re-checking after every
rivalry does ~M * (N + M) work and must time out.
"""

import random
import sys
from pathlib import Path

MAX_N = 50_000
MAX_M = 100_000

Edge = tuple[int, int]


def first_break(n: int, edges: list[Edge]) -> int:
    parent = list(range(n + 1))
    parity = [0] * (n + 1)
    size = [1] * (n + 1)

    def find(x: int) -> tuple[int, int]:
        p = 0
        while parent[x] != x:
            p ^= parity[x]
            x = parent[x]
        return x, p

    for i, (u, v) in enumerate(edges, start=1):
        ru, pu = find(u)
        rv, pv = find(v)
        if ru == rv:
            if pu == pv:
                return i
        else:
            if size[ru] > size[rv]:
                ru, rv = rv, ru
            parent[ru] = rv                 # union by size keeps find() short
            parity[ru] = pu ^ pv ^ 1
            size[rv] += size[ru]
    return -1


class Builder:
    """Edges consistent with a hidden colouring of vertices 1..n."""

    def __init__(self, rng: random.Random, n: int) -> None:
        self.rng = rng
        self.n = n
        self.color = [0] + [rng.randint(0, 1) for _ in range(n)]
        self.seen: set[Edge] = set()

    def ok(self, u: int, v: int) -> bool:
        return u != v and (min(u, v), max(u, v)) not in self.seen

    def take(self, u: int, v: int) -> Edge:
        assert self.ok(u, v)
        self.seen.add((min(u, v), max(u, v)))
        return (u, v) if self.rng.random() < 0.5 else (v, u)

    def tree(self, members: list[int]) -> list[Edge]:
        """A random spanning tree of `members` using only cross-colour edges
        (members get re-coloured along the tree so that is always possible)."""
        out = []
        for i in range(1, len(members)):
            u, v = members[i], members[self.rng.randrange(i)]
            self.color[u] = 1 - self.color[v]
            out.append(self.take(u, v))
        return out

    def cross(self, members: list[int], count: int) -> list[Edge]:
        out = []
        while len(out) < count:
            u, v = self.rng.choice(members), self.rng.choice(members)
            if self.color[u] != self.color[v] and self.ok(u, v):
                out.append(self.take(u, v))
        return out

    def same(self, members: list[int]) -> Edge:
        while True:
            u, v = self.rng.choice(members), self.rng.choice(members)
            if self.color[u] == self.color[v] and self.ok(u, v):
                return self.take(u, v)

    def anything(self, members: list[int], count: int) -> list[Edge]:
        out = []
        while len(out) < count:
            u, v = self.rng.choice(members), self.rng.choice(members)
            if self.ok(u, v):
                out.append(self.take(u, v))
        return out


def shuffled(rng: random.Random, edges: list[Edge]) -> list[Edge]:
    edges = edges[:]
    rng.shuffle(edges)
    return edges


def relabel(rng: random.Random, n: int, edges: list[Edge]) -> list[Edge]:
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    return [(perm[u - 1], perm[v - 1]) for u, v in edges]


def planned(rng: random.Random, n: int, tree_size: int, extra: int, broken: bool, after: int) -> tuple[list[Edge], int]:
    """A consistent tree on 1..tree_size plus `extra` consistent edges (all
    shuffled), then optionally a breaking edge inside the tree, then `after`
    arbitrary edges. Returns (edges, expected answer)."""
    b = Builder(rng, n)
    every = list(range(1, n + 1))
    members = list(range(1, tree_size + 1))
    prefix = b.tree(members) + b.cross(every, extra)
    prefix = shuffled(rng, prefix)
    if not broken:
        return relabel(rng, n, prefix), -1
    edges = prefix + [b.same(members)] + b.anything(every, after)
    return relabel(rng, n, edges), len(prefix) + 1


def main() -> None:
    out = Path(sys.argv[1])
    cases: list[tuple[int, list[Edge], int, int, int]] = []   # n, edges, expected, cap_n, cap_m

    # --- subtask 1: N, M <= 100
    cases.append((2, [(1, 2)], -1, 100, 100))
    cases.append((3, [(2, 3), (1, 2), (3, 1)], 3, 100, 100))
    rng = random.Random(20261203 + 3)
    e, k = planned(rng, 100, 60, 20, True, 19)
    cases.append((100, e, k, 100, 100))

    # --- subtask 2: N, M <= 1,000
    rng = random.Random(20261203 + 4)
    b = Builder(rng, 1000)
    cases.append((1000, relabel(rng, 1000, shuffled(rng, b.tree(list(range(1, 1001))))), -1, 1000, 1000))   # a tree
    rng = random.Random(20261203 + 5)
    cycle = [(i, i % 999 + 1) for i in range(1, 1000)]            # odd cycle on 1..999, vertex 1000 alone
    rng.shuffle(cycle)
    cases.append((1000, relabel(rng, 1000, cycle), 999, 1000, 1000))
    rng = random.Random(20261203 + 6)
    # two groups A = 1..350, B = 351..700 (300 loners); one same-colour rivalry joins them (harmless),
    # later a same-colour rivalry inside A breaks it
    b = Builder(rng, 1000)
    group_a, group_b = list(range(1, 351)), list(range(351, 701))
    first = shuffled(rng, b.tree(group_a) + b.tree(group_b) + b.cross(group_a, 50) + b.cross(group_b, 50))
    u = rng.choice(group_a)
    v = next(x for x in group_b if b.color[x] == b.color[u])
    bridge = b.take(u, v)
    late = shuffled(rng, b.cross(group_a, 50) + b.cross(group_b, 50))
    edges = first + [bridge] + late + [b.same(group_a)] + b.anything(group_a + group_b, 1000 - len(first) - len(late) - 2)
    cases.append((1000, relabel(rng, 1000, edges), len(first) + len(late) + 2, 1000, 1000))

    # --- subtask 3: N <= 5 * 10^4, M <= 10^5
    rng = random.Random(20261203 + 7)
    e, k = planned(rng, MAX_N, MAX_N, 1, True, 0)                  # answer is exactly M
    cases.append((MAX_N, e, k, MAX_N, MAX_M))                      # slow.cpp must TLE here
    rng = random.Random(20261203 + 8)
    e, k = planned(rng, MAX_N, 30000, MAX_M - 29999, False, 0)     # never breaks, M = 10^5
    cases.append((MAX_N, e, k, MAX_N, MAX_M))
    rng = random.Random(20261203 + 9)
    b = Builder(rng, MAX_N)
    tri = [b.take(1, 2), b.take(2, 3), b.take(3, 1)]               # breaks at rivalry 9
    edges = b.cross(list(range(4, MAX_N + 1)), 6) + tri + b.anything(list(range(1, MAX_N + 1)), 70000)
    cases.append((MAX_N, relabel(rng, MAX_N, edges), 9, MAX_N, MAX_M))
    rng = random.Random(20261203 + 10)
    e, k = planned(rng, MAX_N, 20000, 30000, True, 25000)          # many small groups around one big one
    cases.append((MAX_N, e, k, MAX_N, MAX_M))

    assert len(cases) == 10
    for index, (n, edges, expected, cap_n, cap_m) in enumerate(cases, start=1):
        assert 1 <= n <= cap_n <= MAX_N and 1 <= len(edges) <= cap_m <= MAX_M
        pairs = set()
        for u, v in edges:
            assert 1 <= u <= n and 1 <= v <= n and u != v
            pairs.add((min(u, v), max(u, v)))
        assert len(pairs) == len(edges)
        assert first_break(n, edges) == expected, (index, first_break(n, edges), expected)
        lines = [f"{n} {len(edges)}"] + [f"{u} {v}" for u, v in edges]
        (out / f"input{index:02d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
