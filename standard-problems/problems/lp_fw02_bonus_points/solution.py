# Python reference for lp_fw02_bonus_points (must pass under the judge's x4 time).
# Fenwick tree over the difference array, flat list, all input read at once.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = [0] + [int(x) for x in data[2:2 + n]]
    bit = [0] * (n + 1)
    out = []
    pos = 2 + n
    for _ in range(q):
        if data[pos] == b"1":
            l = int(data[pos + 1])
            r = int(data[pos + 2]) + 1
            x = int(data[pos + 3])
            pos += 4
            while l <= n:
                bit[l] += x
                l += l & -l
            while r <= n:
                bit[r] -= x
                r += r & -r
        else:
            i = int(data[pos + 1])
            pos += 2
            s = a[i]
            while i > 0:
                s += bit[i]
                i -= i & -i
            out.append(s)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
