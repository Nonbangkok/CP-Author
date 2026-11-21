# Python reference for lp_dp03_lakeside_stalls (must pass under the judge's x4 time).
import sys


def line(values) -> int:
    take = skip = 0
    for v in values:
        take, skip = skip + v, (take if take > skip else skip)
    return take if take > skip else skip


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    print(max(line(a[:-1]), line(a[1:])))


main()
