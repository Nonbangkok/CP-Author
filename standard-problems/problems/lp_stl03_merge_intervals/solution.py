# Python reference for lp_stl03_merge_intervals (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    seg = sorted(zip(map(int, data[1:1 + 2 * n:2]), map(int, data[2:2 + 2 * n:2])))
    strips = 0
    total = 0
    cur_l, cur_r = seg[0]
    for l, r in seg[1:]:
        if l <= cur_r:
            if r > cur_r:
                cur_r = r
        else:
            strips += 1
            total += cur_r - cur_l
            cur_l, cur_r = l, r
    strips += 1
    total += cur_r - cur_l
    sys.stdout.write(f"{strips}\n{total}\n")


main()
