# Python reference for lp_swp01_busiest_moment (must pass under the judge's x4 time).
# Independent of solution.cpp: sorts arrivals and departures separately and
# merges them; a departure at the same time as an arrival is processed first.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    arrive = sorted(map(int, data[1:1 + 2 * n:2]))
    leave = sorted(map(int, data[2:2 + 2 * n:2]))
    j = 0
    best, when = 0, 0
    for i in range(n):
        t = arrive[i]
        while leave[j] <= t:  # never runs past the end: some guest is still inside at t
            j += 1
        here = i + 1 - j
        if here > best:
            best, when = here, t
    print(best, when)


main()
