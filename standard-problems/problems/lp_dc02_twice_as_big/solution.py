# Python reference for lp_dc02_twice_as_big (must pass under the judge's x4 time).
# Independent of solution.cpp: scan left to right with a Fenwick tree over the
# compressed values seen so far; earlier cards > 2 * a_j = seen - (seen <= 2 * a_j).
import sys
from bisect import bisect_right


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    values = sorted(set(a))
    rank = {v: i + 1 for i, v in enumerate(values)}
    size = len(values)
    tree = [0] * (size + 1)
    count = 0
    for seen, v in enumerate(a):
        i = bisect_right(values, 2 * v)  # distinct values <= 2v are ranks 1..i
        at_most = 0
        while i > 0:
            at_most += tree[i]
            i &= i - 1
        count += seen - at_most
        i = rank[v]
        while i <= size:
            tree[i] += 1
            i += i & -i
    print(count)


main()
