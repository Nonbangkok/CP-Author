# Python reference for lp_bexp01_power_mod (built-in three-argument pow is binary exponentiation).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    out = []
    for j in range(q):
        a, b, m = int(data[1 + 3 * j]), int(data[2 + 3 * j]), int(data[3 + 3 * j])
        out.append(pow(a, b, m))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
