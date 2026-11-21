# Python reference for lp_seg02_best_streak (must pass under the judge's x4 time).
# Independent of solution.cpp: an iterative bottom-up tree over a power-of-two
# number of leaves, four parallel lists (sum, prefix, suffix, best). The merge
# is not commutative, so the query keeps a left result and a right result and
# glues them in order at the end.
import sys

NEG = -(1 << 62)  # "nothing chosen yet"; Python ints cannot overflow


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    size = 1
    while size < n:
        size *= 2
    S = [0] * (2 * size)
    P = [0] * (2 * size)
    X = [0] * (2 * size)
    B = [0] * (2 * size)
    for i in range(n):
        v = int(data[2 + i])
        S[size + i] = P[size + i] = X[size + i] = B[size + i] = v

    def pull(v: int) -> None:
        l, r = 2 * v, 2 * v + 1
        sl, sr = S[l], S[r]
        S[v] = sl + sr
        a = sl + P[r]
        P[v] = P[l] if P[l] > a else a
        a = sr + X[l]
        X[v] = X[r] if X[r] > a else a
        best = B[l] if B[l] > B[r] else B[r]
        a = X[l] + P[r]
        B[v] = best if best > a else a

    for v in range(size - 1, 0, -1):
        pull(v)
    out = []
    pos = 2 + n
    for _ in range(q):
        kind = data[pos]
        x = int(data[pos + 1])
        y = int(data[pos + 2])
        pos += 3
        if kind == b"1":
            v = size + x - 1
            S[v] = P[v] = X[v] = B[v] = y
            v >>= 1
            while v:
                pull(v)
                v >>= 1
            continue
        lo, hi = x - 1 + size, y + size  # half-open [lo, hi)
        # left result (s1, p1, x1, b1) and right result (s2, p2, x2, b2)
        s1, p1, x1, b1 = 0, NEG, NEG, NEG
        s2, p2, x2, b2 = 0, NEG, NEG, NEG
        while lo < hi:
            if lo & 1:
                s, p, xx, b = S[lo], P[lo], X[lo], B[lo]
                # left := left + node
                nb = max(b1, b, x1 + p)
                p1 = max(p1, s1 + p)
                x1 = max(xx, s + x1)
                s1 += s
                b1 = nb
                lo += 1
            if hi & 1:
                hi -= 1
                s, p, xx, b = S[hi], P[hi], X[hi], B[hi]
                # right := node + right
                nb = max(b, b2, xx + p2)
                p2 = max(p, s + p2)
                x2 = max(x2, s2 + xx)
                s2 += s
                b2 = nb
            lo >>= 1
            hi >>= 1
        out.append(max(b1, b2, x1 + p2))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
