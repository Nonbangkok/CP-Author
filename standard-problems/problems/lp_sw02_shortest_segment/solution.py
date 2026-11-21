# Python reference for lp_sw02_shortest_segment (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, s = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    best = n + 1
    total = 0
    l = 0
    for r in range(n):
        total += a[r]
        while total >= s:
            if r - l + 1 < best:
                best = r - l + 1
            total -= a[l]
            l += 1
    print(best if best <= n else -1)


main()
