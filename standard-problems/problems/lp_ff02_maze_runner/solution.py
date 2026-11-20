# Python reference for lp_ff02_maze_runner (must pass under the judge's x4 time).
# Level-by-level BFS on a flattened grid padded with walls (no bounds checks).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    r, c = int(data[0]), int(data[1])
    w = c + 2
    g = bytearray(b"#" * (w * (r + 2)))
    for i in range(r):
        start = (i + 1) * w + 1
        g[start:start + c] = data[2 + i]
    s = g.find(b"S")
    e = g.find(b"E")
    wall = ord("#")
    seen = bytearray(len(g))
    seen[s] = 1
    level = [s]
    steps = 0
    while level:
        if seen[e]:
            print(steps)
            return
        steps += 1
        nxt = []
        for cur in level:
            for v in (cur - 1, cur + 1, cur - w, cur + w):
                if not seen[v] and g[v] != wall:
                    seen[v] = 1
                    nxt.append(v)
        level = nxt
    print(-1)


main()
