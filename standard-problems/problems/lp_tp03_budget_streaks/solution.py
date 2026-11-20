# Python reference for lp_tp03_budget_streaks (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, s = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    count = 0
    total = 0
    l = 0
    for r in range(n):
        total += a[r]
        while total > s:
            total -= a[l]
            l += 1
        count += r - l + 1
    print(count)


main()
