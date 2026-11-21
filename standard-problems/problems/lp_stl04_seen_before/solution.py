# Python reference for lp_stl04_seen_before (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    count: dict[bytes, int] = {}
    out = []
    for w in data[1:1 + n]:
        c = count.get(w, 0) + 1
        count[w] = c
        out.append(c)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
