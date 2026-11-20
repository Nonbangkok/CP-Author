# Python reference for lp_dpk03_heavy_treasures (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, cap = int(data[0]), int(data[1])
    items = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n)]
    total = sum(v for _, v in items)
    inf = 1 << 62
    minw = [inf] * (total + 1)  # minw[s] = least weight worth exactly s
    minw[0] = 0
    reach = 0
    for w, v in items:
        reach += v
        # 0/1 item: read the old row for s - v before overwriting s, i.e. s downward
        for s in range(reach, v - 1, -1):
            x = minw[s - v] + w
            if x < minw[s]:
                minw[s] = x
    best = 0
    for s in range(total + 1):
        if minw[s] <= cap:
            best = s
    print(best)


main()
