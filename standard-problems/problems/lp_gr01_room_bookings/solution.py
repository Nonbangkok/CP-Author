# Python reference for lp_gr01_room_bookings (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, c = int(data[0]), int(data[1])
    starts = list(map(int, data[2:2 + 2 * n:2]))
    durations = list(map(int, data[3:3 + 2 * n:2]))
    ends = [s + d for s, d in zip(starts, durations)]
    order = sorted(range(n), key=ends.__getitem__)
    taken = 0
    free_at = -1  # every start is >= 0
    for i in order:
        if starts[i] >= free_at:
            taken += 1
            free_at = ends[i] + c
    print(taken)


main()
