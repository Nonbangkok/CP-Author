# Python reference for lp_sp01_delivery_times (must pass under the judge's x4 time).
import sys
from heapq import heappush, heappop


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, s = int(data[0]), int(data[1]), int(data[2])
    adj = [[] for _ in range(n + 1)]
    pos = 3
    for _ in range(m):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heappush(heap, (nd, v))
    print(" ".join("-1" if x == INF else str(x) for x in dist[1:]))


main()
