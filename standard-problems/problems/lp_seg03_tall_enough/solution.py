# Python reference for lp_seg03_tall_enough (must pass under the judge's x4 time).
# Independent of solution.cpp: an iterative bottom-up max tree over a
# power-of-two number of leaves (padding leaves are 0, below every x). The
# query lists the O(log N) nodes that tile [l, r] from left to right, takes the
# first whose maximum reaches x, and walks down from it, preferring the left child.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    size = 1
    while size < n:
        size *= 2
    t = [0] * (2 * size)
    for i in range(n):
        t[size + i] = int(data[2 + i])
    for v in range(size - 1, 0, -1):
        a, b = t[2 * v], t[2 * v + 1]
        t[v] = a if a > b else b
    out = []
    pos = 2 + n
    for _ in range(q):
        if data[pos] == b"1":
            v = size + int(data[pos + 1]) - 1
            t[v] = int(data[pos + 2])
            pos += 3
            v >>= 1
            while v:
                a, b = t[2 * v], t[2 * v + 1]
                t[v] = a if a > b else b
                v >>= 1
            continue
        lo = int(data[pos + 1]) - 1 + size
        hi = int(data[pos + 2]) + size  # half-open [lo, hi)
        x = int(data[pos + 3])
        pos += 4
        left_nodes = []
        right_nodes = []
        while lo < hi:
            if lo & 1:
                left_nodes.append(lo)
                lo += 1
            if hi & 1:
                hi -= 1
                right_nodes.append(hi)
            lo >>= 1
            hi >>= 1
        right_nodes.reverse()
        answer = -1
        for v in left_nodes + right_nodes:
            if t[v] >= x:
                while v < size:
                    v = 2 * v if t[2 * v] >= x else 2 * v + 1
                answer = v - size + 1
                break
        out.append(answer)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
