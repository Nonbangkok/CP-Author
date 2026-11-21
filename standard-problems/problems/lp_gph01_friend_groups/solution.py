# Python reference for lp_gph01_friend_groups (must pass under the judge's x4 time).
# Independent of solution.cpp: union-find with path halving instead of DFS.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    for i in range(m):
        a = find(int(data[2 + 2 * i]))
        b = find(int(data[3 + 2 * i]))
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            groups -= 1
    largest = max(size[find(x)] for x in range(1, n + 1))
    print(groups, largest)


main()
