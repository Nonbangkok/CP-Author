# Python reference for lp_mst03_candidate_roads (must pass under the judge's x4 time).
# Kruskal in groups of equal weight: answer the whole group against the DSU of
# strictly lighter roads, then unite the group. Iterative find (path halving).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    us = list(map(int, data[2:2 + 3 * m:3]))
    vs = list(map(int, data[3:3 + 3 * m:3]))
    ws = list(map(int, data[4:4 + 3 * m:3]))
    order = sorted(range(m), key=ws.__getitem__)
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    yes = [False] * m
    i = 0
    while i < m:
        j = i
        wi = ws[order[i]]
        while j < m and ws[order[j]] == wi:
            j += 1
        for k in range(i, j):
            e = order[k]
            yes[e] = find(us[e]) != find(vs[e])
        for k in range(i, j):
            e = order[k]
            a, b = find(us[e]), find(vs[e])
            if a != b:
                if size[a] < size[b]:
                    a, b = b, a
                parent[b] = a
                size[a] += size[b]
        i = j
    sys.stdout.write("\n".join("YES" if y else "NO" for y in yes) + "\n")


main()
