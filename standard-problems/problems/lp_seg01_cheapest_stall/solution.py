# Python reference for lp_seg01_cheapest_stall (must pass under the judge's x4 time).
# Independent of solution.cpp: an iterative bottom-up tree, leaf i at t[size + i]
# (0-indexed), the query climbs from both ends at once.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    size = n
    t = [0] * size + [int(x) for x in data[2:2 + n]]
    for v in range(size - 1, 0, -1):
        left, right = t[2 * v], t[2 * v + 1]
        t[v] = left if left < right else right
    out = []
    pos = 2 + n
    for _ in range(q):
        kind = data[pos]
        x = int(data[pos + 1])
        y = int(data[pos + 2])
        pos += 3
        if kind == b"1":
            v = size + x - 1
            t[v] = y
            v >>= 1
            while v:
                left, right = t[2 * v], t[2 * v + 1]
                t[v] = left if left < right else right
                v >>= 1
        else:
            lo = x - 1 + size
            hi = y + size  # half-open [lo, hi)
            best = 2000000000
            while lo < hi:
                if lo & 1:
                    if t[lo] < best:
                        best = t[lo]
                    lo += 1
                if hi & 1:
                    hi -= 1
                    if t[hi] < best:
                        best = t[hi]
                lo >>= 1
                hi >>= 1
            out.append(best)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
