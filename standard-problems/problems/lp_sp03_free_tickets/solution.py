# Python reference for lp_sp03_free_tickets (must pass under the judge's x4 time).
# Dijkstra on the state graph (city, tickets used); state id = city * (K + 1) + used.
import sys
from heapq import heappush, heappop


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    adj = [[] for _ in range(n)]
    pos = 3
    for _ in range(m):
        u, v, w = int(data[pos]) - 1, int(data[pos + 1]) - 1, int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    layers = k + 1
    INF = float("inf")
    dist = [INF] * (n * layers)
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, state = heappop(heap)
        if d > dist[state]:
            continue
        u, used = divmod(state, layers)
        for v, w in adj[u]:
            base = v * layers + used
            nd = d + w
            if nd < dist[base]:          # pay for this ride
                dist[base] = nd
                heappush(heap, (nd, base))
            if used < k and d < dist[base + 1]:   # use a free ticket
                dist[base + 1] = d
                heappush(heap, (d, base + 1))
    best = min(dist[(n - 1) * layers:])
    print(-1 if best == INF else best)


main()
