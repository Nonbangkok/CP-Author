# Python reference for lp_fw03_bird_species (must pass under the judge's x4 time).
# Offline: questions sorted by r, a 1 at the last occurrence of every species,
# Fenwick tree over positions. Species only need equality, so the raw tokens
# are dictionary keys (no renumbering needed).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = [None] + data[2:2 + n]
    qs = data[2 + n:2 + n + 2 * q]
    ql = [int(x) for x in qs[0::2]]
    qr = [int(x) for x in qs[1::2]]
    order = sorted(range(q), key=qr.__getitem__)
    bit = [0] * (n + 1)
    last = {}
    answer = [0] * q
    r = 0
    for j in order:
        target = qr[j]
        while r < target:
            r += 1
            v = a[r]
            p = last.get(v, 0)
            while 0 < p <= n:
                bit[p] -= 1
                p += p & -p
            last[v] = r
            p = r
            while p <= n:
                bit[p] += 1
                p += p & -p
        s = 0
        i = target
        while i > 0:
            s += bit[i]
            i -= i & -i
        i = ql[j] - 1
        while i > 0:
            s -= bit[i]
            i -= i & -i
        answer[j] = s
    sys.stdout.write("\n".join(map(str, answer)) + "\n")


main()
