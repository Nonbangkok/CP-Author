# Python reference for lp_gs02_report_card (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    out = []
    total = 0
    pos = 2
    for _ in range(n):
        s = sum(map(int, data[pos:pos + m]))
        pos += m
        total += s
        out.append(f"{s / m:.2f}")
    out.append(f"{total / (n * m):.2f}")
    sys.stdout.write("\n".join(out) + "\n")


main()
