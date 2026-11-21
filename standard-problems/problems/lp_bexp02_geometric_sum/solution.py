# Python reference for lp_bexp02_geometric_sum: the same bit walk as solution.cpp.
import sys


def geometric(a: int, n: int, m: int) -> int:
    a %= m
    s, p = 0, 1 % m
    for bit in bin(n + 1)[2:]:
        s = s * (1 + p) % m
        p = p * p % m
        if bit == "1":
            s = (s + p) % m
            p = p * a % m
    return s


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    out = []
    for j in range(q):
        out.append(geometric(int(data[1 + 3 * j]), int(data[2 + 3 * j]), int(data[3 + 3 * j])))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
