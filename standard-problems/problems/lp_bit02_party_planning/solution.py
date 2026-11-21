# Python reference for lp_bit02_party_planning: build the per-mask tables by
# doubling (masks that use item i are the old masks with bit i added), so the
# 2^N work happens inside list comprehensions.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m, budget = int(data[0]), int(data[1]), int(data[2])
    c = [int(data[3 + 2 * i]) for i in range(n)]
    v = [int(data[4 + 2 * i]) for i in range(n)]
    pos = 3 + 2 * n
    conflict = [0] * n
    for _ in range(m):
        x, y = int(data[pos]) - 1, int(data[pos + 1]) - 1
        pos += 2
        conflict[x] |= 1 << y
        conflict[y] |= 1 << x
    cost, fun, ok = [0], [0], [True]
    for i in range(n):
        ci, vi, lower = c[i], v[i], conflict[i] & ((1 << i) - 1)
        cost += [x + ci for x in cost]
        fun += [x + vi for x in fun]
        ok += [o and not (mask & lower) for mask, o in enumerate(ok)]
    best = max(f for f, w, o in zip(fun, cost, ok) if o and w <= budget)
    sys.stdout.write(f"{best}\n")


main()
