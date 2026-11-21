# Python reference for lp_lca01_family_tree (must pass under the judge's x4
# time). Binary lifting with list-of-lists tables built by comprehensions; a
# query lifts by the set bits of the depth difference, then from the highest
# useful level down. Depths from a BFS order (no recursion).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    par = [0, 1] + [int(x) for x in data[2:n + 1]]  # par[1] = 1: the root is its own parent
    children = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        children[par[i]].append(i)
    depth = [0] * (n + 1)
    order = [1]
    for u in order:
        d = depth[u] + 1
        for c in children[u]:
            depth[c] = d
        order.extend(children[u])
    up = [par]
    for _ in range(max(1, n.bit_length()) - 1):
        prev = up[-1]
        up.append([prev[x] for x in prev])
    out = []
    pos = n + 1
    for _ in range(q):
        u, v = int(data[pos]), int(data[pos + 1])
        pos += 2
        du, dv = depth[u], depth[v]
        if du < dv:
            u, v, du, dv = v, u, dv, du
        diff, k = du - dv, 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u != v:
            for k in range(dv.bit_length() - 1, -1, -1):
                row = up[k]
                a, b = row[u], row[v]
                if a != b:
                    u, v = a, b
            u = par[u]
        out.append(u)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
