# Python reference for lp_gr02_deadline_jobs (must pass under the judge's x4 time).
# Independent of solution.cpp: most profitable first, each job takes the latest
# free day <= its deadline, found with a union-find over days (day 0 = none left).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deadlines = list(map(int, data[1:1 + 2 * n:2]))
    profits = list(map(int, data[2:2 + 2 * n:2]))
    order = sorted(range(n), key=profits.__getitem__, reverse=True)
    parent = list(range(n + 1))  # parent chain leads to the latest free day <= x
    total = 0
    for i in order:
        x = min(deadlines[i], n)
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:  # path compression
            parent[x], x = root, parent[x]
        if root:
            total += profits[i]
            parent[root] = root - 1
    print(total)


main()
