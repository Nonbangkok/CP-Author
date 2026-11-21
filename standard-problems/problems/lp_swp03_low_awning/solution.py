# Python reference for lp_swp03_low_awning (must pass under the judge's x4 time).
# Independent of solution.cpp: queries sorted by position, awnings sorted by
# left end; a min-heap of (height, right end) holds the opened awnings, and
# awnings that already ended are thrown away lazily when they reach the top.
import sys
import heapq


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    vals = list(map(int, data[2:2 + 3 * n]))
    awnings = sorted(zip(vals[0::3], vals[1::3], vals[2::3]))
    pts = list(map(int, data[2 + 3 * n:2 + 3 * n + q]))
    order = sorted(range(q), key=pts.__getitem__)
    answer = [-1] * q
    heap = []
    i = 0
    for j in order:
        p = pts[j]
        while i < n and awnings[i][0] <= p:
            l, r, h = awnings[i]
            heapq.heappush(heap, (h, r))
            i += 1
        while heap and heap[0][1] < p:
            heapq.heappop(heap)
        if heap:
            answer[j] = heap[0][0]
    sys.stdout.write("\n".join(map(str, answer)) + "\n")


main()
