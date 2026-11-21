# Python reference for lp_bit01_bit_ops.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = [0] + [int(x) for x in data[2:2 + n]]
    pos = 2 + n
    out = []
    for _ in range(q):
        t, i = int(data[pos]), int(data[pos + 1])
        if t == 5:
            out.append(bin(a[i]).count("1"))
            pos += 2
            continue
        k = int(data[pos + 2])
        pos += 3
        if t == 1:
            a[i] |= 1 << k
        elif t == 2:
            a[i] &= ~(1 << k)
        elif t == 3:
            a[i] ^= 1 << k
        else:
            out.append((a[i] >> k) & 1)
    out.append(" ".join(map(str, a[1:])))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
