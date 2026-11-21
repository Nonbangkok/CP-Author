# Python reference for lp_lazy02_greenhouse (must pass under the judge's x4 time).
# Independent of solution.cpp: a non-recursive lazy segment tree (the
# AtCoder-library layout: power-of-two leaves, push down along the two border
# paths, apply bottom-up, pull back up). A tag is one pair (kind, value):
# kind 1 = "set to value", kind 0 = "add value"; a newer tag g composed onto an
# older f gives g if g is a set, else f with g's value added to it.
import sys

NEG = -(1 << 62)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    log = 0
    while (1 << log) < n:
        log += 1
    size = 1 << log
    d = [NEG] * (2 * size)
    for i in range(n):
        d[size + i] = int(data[2 + i])
    for v in range(size - 1, 0, -1):
        a, b = d[2 * v], d[2 * v + 1]
        d[v] = a if a > b else b
    kind = [0] * size  # tags live on internal nodes only
    val = [0] * size

    def push(k: int) -> None:
        kk, vv = kind[k], val[k]
        if kk == 0 and vv == 0:
            return
        for c in (2 * k, 2 * k + 1):
            if kk:
                d[c] = vv
                if c < size:
                    kind[c] = 1
                    val[c] = vv
            else:
                d[c] += vv
                if c < size:
                    val[c] += vv  # add joins a set or an add alike
        kind[k] = 0
        val[k] = 0

    out = []
    pos = 2 + n
    for _ in range(q):
        t = data[pos]
        l = int(data[pos + 1]) - 1 + size
        r = int(data[pos + 2]) + size  # half-open [l, r)
        for i in range(log, 0, -1):
            if ((l >> i) << i) != l:
                push(l >> i)
            if ((r >> i) << i) != r:
                push((r - 1) >> i)
        if t == b"3":
            pos += 3
            best = NEG
            while l < r:
                if l & 1:
                    if d[l] > best:
                        best = d[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if d[r] > best:
                        best = d[r]
                l >>= 1
                r >>= 1
            out.append(best)
            continue
        x = int(data[pos + 3])
        pos += 4
        is_set = t == b"2"
        l0, r0 = l, r
        while l < r:
            if l & 1:
                if is_set:
                    d[l] = x
                    if l < size:
                        kind[l] = 1
                        val[l] = x
                else:
                    d[l] += x
                    if l < size:
                        val[l] += x
                l += 1
            if r & 1:
                r -= 1
                if is_set:
                    d[r] = x
                    if r < size:
                        kind[r] = 1
                        val[r] = x
                else:
                    d[r] += x
                    if r < size:
                        val[r] += x
            l >>= 1
            r >>= 1
        l, r = l0, r0
        for i in range(1, log + 1):
            if ((l >> i) << i) != l:
                k = l >> i
                a, b = d[2 * k], d[2 * k + 1]
                d[k] = a if a > b else b
            if ((r >> i) << i) != r:
                k = (r - 1) >> i
                a, b = d[2 * k], d[2 * k + 1]
                d[k] = a if a > b else b
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
