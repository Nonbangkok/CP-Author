# Python reference for lp_lca02_detour (must pass under the judge's x4 time).
# Independent route to the same number: among lca(a,b), lca(a,c), lca(b,c) the
# deepest is the vertex m of the path a-b closest to c; the detour is walking
# from m to c and back: 2 * dist(c, m), one more LCA. Binary lifting tables
# built with comprehensions, BFS (no recursion).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    pos = 2
    for _ in range(n - 1):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    par = [0] * (n + 1)
    par[1] = 1
    depth = [0] * (n + 1)
    dist = [0] * (n + 1)
    seen = [False] * (n + 1)
    seen[1] = True
    order = [1]
    for u in order:
        du, wu = depth[u] + 1, dist[u]
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                par[v] = u
                depth[v] = du
                dist[v] = wu + w
                order.append(v)
    up = [par]
    for _ in range(max(1, n.bit_length()) - 1):
        prev = up[-1]
        up.append([prev[x] for x in prev])

    def lca(u: int, v: int) -> int:
        du, dv = depth[u], depth[v]
        if du < dv:
            u, v, du, dv = v, u, dv, du
        diff, k = du - dv, 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return u
        for k in range(dv.bit_length() - 1, -1, -1):
            row = up[k]
            a, b = row[u], row[v]
            if a != b:
                u, v = a, b
        return par[u]

    out = []
    for _ in range(q):
        a, b, c = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        x, y, z = lca(a, b), lca(a, c), lca(b, c)
        m = x
        if depth[y] > depth[m]:
            m = y
        if depth[z] > depth[m]:
            m = z
        out.append(2 * (dist[c] + dist[m] - 2 * dist[lca(c, m)]))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
