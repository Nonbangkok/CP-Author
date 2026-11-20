# Python reference for lp_fw01_shelf_stock (must pass under the judge's x4 time).
# Flat-list Fenwick tree, built in O(N) by pushing each node into its parent.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = [0] + [int(x) for x in data[2:2 + n]]
    bit = a[:]
    for i in range(1, n + 1):
        j = i + (i & -i)
        if j <= n:
            bit[j] += bit[i]
    out = []
    pos = 2 + n
    for _ in range(q):
        t = data[pos]
        u = int(data[pos + 1])
        v = int(data[pos + 2])
        pos += 3
        if t == b"1":
            delta = v - a[u]
            a[u] = v
            if delta:
                i = u
                while i <= n:
                    bit[i] += delta
                    i += i & -i
        else:
            s = 0
            i = v
            while i > 0:
                s += bit[i]
                i -= i & -i
            i = u - 1
            while i > 0:
                s -= bit[i]
                i -= i & -i
            out.append(s)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
