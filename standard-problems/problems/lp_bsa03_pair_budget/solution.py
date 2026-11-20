# Python reference for lp_bsa03_pair_budget (must pass under the judge's x4 time).
import sys
from bisect import bisect_right


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = sorted(map(int, data[2:2 + n]))
    pairs = 0
    for j in range(n):
        pairs += bisect_right(a, k - a[j], 0, j)
    print(pairs)


main()
