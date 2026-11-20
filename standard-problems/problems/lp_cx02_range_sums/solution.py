# Python reference for lp_cx02_range_sums (must pass under the judge's x4 time).
import sys
from itertools import accumulate


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    pre = [0, *accumulate(map(int, data[2:2 + n]))]
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        out.append(pre[r] - pre[l - 1])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
