# Python reference for lp_bsa02_nearest_value (must pass under the judge's x4 time).
import sys
from bisect import bisect_left


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = sorted(map(int, data[2:2 + n]))
    out = []
    for token in data[2 + n:2 + n + q]:
        x = int(token)
        i = bisect_left(a, x)
        if i == n:
            best = a[-1]
        elif i == 0:
            best = a[0]
        else:
            below, above = a[i - 1], a[i]
            best = below if x - below <= above - x else above
        out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
