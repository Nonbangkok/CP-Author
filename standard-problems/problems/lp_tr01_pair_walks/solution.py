# Python reference for lp_tr01_pair_walks (must pass under the judge's x4 time).
# BFS order from house 1, then subtree sizes from the back of the order.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    for i in range(n - 1):
        u, v = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (n + 1)
    parent[1] = -1
    order = [1]
    for u in order:  # the list grows while we walk it: a BFS
        pu = parent[u]
        for v in adj[u]:
            if v != pu:
                parent[v] = u
                order.append(v)
    size = [1] * (n + 1)
    answer = 0
    for i in range(n - 1, 0, -1):
        v = order[i]
        s = size[v]
        size[parent[v]] += s
        answer += s * (n - s)
    print(answer)


main()
