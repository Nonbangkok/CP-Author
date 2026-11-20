# Python reference for lp_gph02_one_way_flights (must pass under the judge's x4 time).
# Level-by-level BFS from city 1 over a CSR adjacency (no deque, no recursion).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, q = int(data[0]), int(data[1]), int(data[2])
    src = data[3:3 + 2 * m:2]
    dst = data[4:4 + 2 * m:2]
    heads = [[] for _ in range(n + 1)]
    for a, b in zip(map(int, src), map(int, dst)):
        heads[a].append(b)
    dist = [-1] * (n + 1)
    dist[1] = 0
    level = [1]
    d = 0
    while level:
        d += 1
        nxt = []
        for u in level:
            for v in heads[u]:
                if dist[v] < 0:
                    dist[v] = d
                    nxt.append(v)
        level = nxt
    queries = data[3 + 2 * m:3 + 2 * m + q]
    sys.stdout.write("\n".join(str(dist[int(t)]) for t in queries) + "\n")


main()
