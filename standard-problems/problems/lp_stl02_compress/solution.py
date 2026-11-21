# Python reference for lp_stl02_compress (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    distinct = sorted(set(a))
    rank = {value: i + 1 for i, value in enumerate(distinct)}
    sys.stdout.write(f"{len(distinct)}\n" + " ".join(str(rank[x]) for x in a) + "\n")


main()
