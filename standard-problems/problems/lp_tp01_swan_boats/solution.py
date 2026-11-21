# Python reference for lp_tp01_swan_boats (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    boats = 0
    l, r = 0, n - 1
    while l <= r:
        if l < r and a[l] + a[r] <= k:
            l += 1
        r -= 1
        boats += 1
    print(boats)


main()
