# Python reference for lp_sp02_rebate_roads (must pass under the judge's x4 time).
# Floyd-Warshall with k outermost; each row update is one list comprehension.
# "Unreachable" is float("inf"), so inf + (negative) stays inf.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, q = int(data[0]), int(data[1]), int(data[2])
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    pos = 3
    for _ in range(m):
        u, v, w = int(data[pos]) - 1, int(data[pos + 1]) - 1, int(data[pos + 2])
        pos += 3
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            d[i] = [x if x <= dik + y else dik + y for x, y in zip(di, dk)]
    out = []
    for _ in range(q):
        a, b = int(data[pos]) - 1, int(data[pos + 1]) - 1
        pos += 2
        x = d[a][b]
        out.append("NO" if x == INF else str(x))
    sys.stdout.write("\n".join(out) + "\n")


main()
