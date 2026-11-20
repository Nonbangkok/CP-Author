# Python reference for lp_stl01_leaderboard (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    rows = [(data[1 + 2 * i].decode(), int(data[2 + 2 * i])) for i in range(n)]
    rows.sort(key=lambda row: (-row[1], row[0]))
    sys.stdout.write("".join(f"{name} {score}\n" for name, score in rows))


main()
