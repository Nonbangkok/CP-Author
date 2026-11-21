# Python reference for lp_tr03_office_party (must pass under the judge's x4
# time). Independent formulation of the DP: best[v] = max(f[v] + sum of best
# over grandchildren, sum of best over children), computed bottom-up along a
# BFS order walked backwards (no recursion). Each vertex pushes its value to
# its boss (child sum) and to its boss's boss (grandchild sum).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    f = [0] + [int(x) for x in data[1:1 + n]]
    boss = [0, 0] + [int(x) for x in data[1 + n:n + n]]
    reports = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        reports[boss[i]].append(i)
    order = [1]
    for u in order:
        order.extend(reports[u])
    child_sum = [0] * (n + 1)
    grand_sum = [0] * (n + 1)
    best = [0] * (n + 1)
    for v in reversed(order):
        b = f[v] + grand_sum[v]
        if child_sum[v] > b:
            b = child_sum[v]
        best[v] = b
        p = boss[v]
        if p:
            child_sum[p] += b
            grand_sum[boss[p]] += b  # boss[1] = 0: a harmless dump slot
    print(best[1])


main()
