# Python reference for lp_mst02_village_wells (must pass under the judge's x4 time).
# Virtual vertex 0 with an edge 0 - i of cost c_i, then Kruskal with an
# iterative DSU.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    us = [0] * n + list(map(int, data[2 + n:2 + n + 3 * m:3]))
    vs = list(range(1, n + 1)) + list(map(int, data[3 + n:3 + n + 3 * m:3]))
    ws = list(map(int, data[2:2 + n])) + list(map(int, data[4 + n:4 + n + 3 * m:3]))
    order = sorted(range(n + m), key=ws.__getitem__)
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    total = 0
    joined = 0
    for i in order:
        a = us[i]
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        b = vs[i]
        while parent[b] != b:
            parent[b] = parent[parent[b]]
            b = parent[b]
        if a == b:
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        total += ws[i]
        joined += 1
        if joined == n:
            break
    print(total)


main()
