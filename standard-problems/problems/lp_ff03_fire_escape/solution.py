# Python reference for lp_ff03_fire_escape (must pass under the judge's x4 time).
# Different shape from solution.cpp: the grid is padded with a ring of special
# "outside" cells ('O'); fire never enters them, and J escapes when it steps
# onto one. Both searches go level by level over flat indices.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    r, c = int(data[0]), int(data[1])
    w = c + 2
    g = bytearray(b"O" * (w * (r + 2)))
    for i in range(r):
        start = (i + 1) * w + 1
        g[start:start + c] = data[2 + i]
    wall, outside, fire_ch = ord("#"), ord("O"), ord("F")
    n = len(g)
    big = 1 << 30
    fire = [big] * n
    level = [i for i in range(n) if g[i] == fire_ch]
    for i in level:
        fire[i] = 0
    t = 0
    while level:
        t += 1
        nxt = []
        for cur in level:
            for v in (cur - 1, cur + 1, cur - w, cur + w):
                if fire[v] == big and g[v] != wall and g[v] != outside:
                    fire[v] = t
                    nxt.append(v)
        level = nxt
    j = g.find(b"J")
    seen = bytearray(n)
    seen[j] = 1
    level = [j]
    t = 0
    while level:
        t += 1
        nxt = []
        for cur in level:
            for v in (cur - 1, cur + 1, cur - w, cur + w):
                if seen[v]:
                    continue
                cell = g[v]
                if cell == outside:
                    print(t)
                    return
                if cell != wall and t < fire[v]:
                    seen[v] = 1
                    nxt.append(v)
        level = nxt
    print(-1)


main()
