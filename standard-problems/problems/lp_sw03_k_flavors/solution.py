# Python reference for lp_sw03_k_flavors (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = data[2:2 + n]  # flavours only need equality, so the raw tokens will do
    cnt = {}
    distinct = 0
    best = 0
    l = 0
    for r in range(n):
        v = a[r]
        c = cnt.get(v, 0)
        if c == 0:
            distinct += 1
        cnt[v] = c + 1
        while distinct > k:
            u = a[l]
            cnt[u] -= 1
            if cnt[u] == 0:
                distinct -= 1
            l += 1
        if r - l + 1 > best:
            best = r - l + 1
    print(best)


main()
