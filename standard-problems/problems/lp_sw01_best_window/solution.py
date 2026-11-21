# Python reference for lp_sw01_best_window (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    s = sum(a[:k])
    best = s
    for i in range(k, n):
        s += a[i] - a[i - k]
        if s > best:
            best = s
    print(best)


main()
