# Python reference for lp_dc03_minus_the_max (must pass under the judge's x4 time).
# Independent of solution.cpp: let a_i be the maximum. With monotonic stacks
# find the widest range (L, R) where nothing is bigger than a_i; the best block
# there is max P[r + 1] over r in [i, R) minus min P[l] over l in (L, i],
# minus a_i, where P are prefix sums. Range max/min come from sparse tables.
import sys


def sparse(arr, pick):
    table = [arr]
    width = 1
    while 2 * width <= len(arr):
        prev = table[-1]
        table.append(list(map(pick, prev[:len(prev) - width], prev[width:])))
        width *= 2
    return table


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    prefix = [0] * (n + 1)
    for i, v in enumerate(a):
        prefix[i + 1] = prefix[i] + v

    left = [-1] * n   # previous index with a bigger value
    stack = []
    for i, v in enumerate(a):
        while stack and a[stack[-1]] <= v:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    right = [n] * n   # next index with a bigger value
    stack = []
    for i in range(n - 1, -1, -1):
        v = a[i]
        while stack and a[stack[-1]] <= v:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    hi_table = sparse(prefix, max)
    lo_table = sparse(prefix, min)
    best = 0
    for i in range(n):
        lo, hi = i + 1, right[i]             # P[r + 1] for r in [i, R)
        k = (hi - lo + 1).bit_length() - 1
        row = hi_table[k]
        top = max(row[lo], row[hi - (1 << k) + 1])
        lo, hi = left[i] + 1, i              # P[l] for l in (L, i]
        k = (hi - lo + 1).bit_length() - 1
        row = lo_table[k]
        bottom = min(row[lo], row[hi - (1 << k) + 1])
        value = top - bottom - a[i]
        if value > best:
            best = value
    print(best)


main()
