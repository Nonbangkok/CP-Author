# Python reference for lp_bit03_light_switches: XOR of every set of switches,
# built by doubling inside list comprehensions.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])

    def mask(word: bytes) -> int:
        return int(word[::-1], 2)  # character p is bit p

    target = mask(data[2]) ^ ((1 << n) - 1)
    xr, presses = [0], [0]
    for j in range(m):
        tj = mask(data[3 + j])
        xr += [x ^ tj for x in xr]
        presses += [p + 1 for p in presses]
    best = min((p for x, p in zip(xr, presses) if x == target), default=-1)
    sys.stdout.write(f"{best}\n")


main()
