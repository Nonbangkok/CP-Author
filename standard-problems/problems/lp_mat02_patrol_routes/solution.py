# Python reference for lp_mat02_patrol_routes (must pass under the judge's x4
# time): precompute the columns of A^(2^i) for i < 60, then per query push the
# row vector e_s through the powers of the set bits of L. Dot products run as
# sum(map(mul, ...)) so the inner loop stays in C.
import sys
from operator import mul

MOD = 10**9 + 7
BITS = 60


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, q = int(data[0]), int(data[1]), int(data[2])
    a = [[0] * n for _ in range(n)]
    pos = 3
    for _ in range(m):
        u, v = int(data[pos]) - 1, int(data[pos + 1]) - 1
        pos += 2
        a[u][v] += 1
    rows = a
    cols_of = []  # cols_of[b][j] = column j of A^(2^b)
    for b in range(BITS):
        cols = [list(c) for c in zip(*rows)]
        cols_of.append(cols)
        if b + 1 < BITS:
            rows = [[sum(map(mul, r, c)) % MOD for c in cols] for r in rows]
    out = []
    for _ in range(q):
        s, t, length = int(data[pos]) - 1, int(data[pos + 1]) - 1, int(data[pos + 2])
        pos += 3
        vec = [0] * n
        vec[s] = 1
        b = 0
        while length:
            if length & 1:
                vec = [sum(map(mul, vec, c)) % MOD for c in cols_of[b]]
            length >>= 1
            b += 1
        out.append(vec[t])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
