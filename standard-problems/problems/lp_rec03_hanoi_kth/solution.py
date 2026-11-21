# Python reference for lp_rec03_hanoi_kth: descend into the half that holds
# move K, O(N) per query.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    out = []
    for token in data[2:2 + q]:
        k = int(token)
        m, x, y, z = n, 1, 3, 2
        while True:
            half = 1 << (m - 1)
            if k == half:
                out.append(f"{m} {x} {y}")
                break
            if k < half:
                m, y, z = m - 1, z, y
            else:
                k -= half
                m, x, z = m - 1, z, x
    sys.stdout.write("\n".join(out) + "\n")


main()
