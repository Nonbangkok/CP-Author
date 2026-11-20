# Python reference for lp_dc01_taller_in_front (must pass under the judge's x4 time).
# Independent of solution.cpp: a Fenwick tree over compressed heights, scanned
# from the back -- for each student count the shorter ones already behind.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    rank = {v: i + 1 for i, v in enumerate(sorted(set(a)))}
    size = len(rank)
    tree = [0] * (size + 1)
    count = 0
    for v in reversed(a):
        i = rank[v] - 1  # strictly shorter: ranks 1 .. rank-1
        while i > 0:
            count += tree[i]
            i &= i - 1
        i = rank[v]
        while i <= size:
            tree[i] += 1
            i += i & -i
    print(count)


main()
