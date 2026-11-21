# Python reference for lp_tp02_closest_sum (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, t = int(data[0]), int(data[1])
    a = sorted(map(int, data[2:2 + n]))
    best = None
    l, r = 0, n - 1
    while l < r:
        s = a[l] + a[r]
        d = abs(s - t)
        if best is None or d < best:
            best = d
        if s < t:
            l += 1
        elif s > t:
            r -= 1
        else:
            break
    print(best)


main()
