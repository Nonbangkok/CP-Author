# Python reference for lp_stl06_top_k_sum (must pass under the judge's x4 time).
import sys
from heapq import heappush, heappushpop


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    best: list[int] = []
    total = 0
    running = 0
    for x in map(int, data[2:2 + n]):
        if len(best) < k:
            heappush(best, x)
            running += x
        elif x > best[0]:
            running += x - heappushpop(best, x)
        total += running
    sys.stdout.write(f"{total}\n")


main()
