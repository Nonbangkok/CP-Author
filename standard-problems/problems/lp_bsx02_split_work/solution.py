# Python reference for lp_bsx02_split_work (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))

    def ok(cap: int) -> bool:
        parts, current = 1, 0
        for v in a:
            if current + v > cap:
                parts += 1
                if parts > k:
                    return False
                current = 0
            current += v
        return True

    lo, hi = max(a) - 1, sum(a)  # ok(lo) is false, ok(hi) is true
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    print(hi)


main()
