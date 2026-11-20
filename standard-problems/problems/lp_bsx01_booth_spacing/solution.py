# Python reference for lp_bsx01_booth_spacing (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    x = sorted(map(int, data[2:2 + n]))

    def ok(d: int) -> bool:
        placed, last = 1, x[0]
        for v in x:
            if v - last >= d:
                placed += 1
                if placed >= k:
                    return True
                last = v
        return placed >= k

    lo, hi = 1, x[-1] - x[0] + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
