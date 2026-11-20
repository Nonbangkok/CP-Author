# Python reference for lp_bsa01_count_range (must pass under the judge's x4 time).
import sys
from bisect import bisect_left, bisect_right


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = sorted(map(int, data[2:2 + n]))
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        out.append(bisect_right(a, r) - bisect_left(a, l))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
