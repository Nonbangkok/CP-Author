# Python reference for lp_mst01_fiber_network (must pass under the judge's x4 time).
# Kruskal with an iterative DSU (path halving + union by size).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    us = data[2:2 + 3 * m:3]
    vs = data[3:3 + 3 * m:3]
    ws = list(map(int, data[4:4 + 3 * m:3]))
    order = sorted(range(m), key=ws.__getitem__)
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    total = 0
    taken = 0
    for i in order:
        a = int(us[i])
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        b = int(vs[i])
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
        taken += 1
        if taken == n - 1:
            break
    print(total if taken == n - 1 else -1)


main()
