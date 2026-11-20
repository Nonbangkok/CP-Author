# Python reference for lp_gr03_on_time_tasks (must pass under the judge's x4 time).
import heapq
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    durations = list(map(int, data[1:1 + 2 * n:2]))
    deadlines = list(map(int, data[2:2 + 2 * n:2]))
    order = sorted(range(n), key=deadlines.__getitem__)
    heap = []  # negated durations: a max-heap
    total = 0
    for i in order:
        t = durations[i]
        if total + t <= deadlines[i]:
            heapq.heappush(heap, -t)
            total += t
        elif heap and -heap[0] > t:
            # swap the longest chosen task for this shorter one: still on time
            total += t + heapq.heapreplace(heap, -t)
    print(len(heap))


main()
