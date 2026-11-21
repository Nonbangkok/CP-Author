# Python reference for lp_dpk01_gold_path (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    rows, cols = int(data[0]), int(data[1])
    grid = data[2:2 + rows]
    rock = 35  # ord("#")
    prev = [-1] * cols  # the row above; -1 = unreachable
    for r in range(rows):
        line = grid[r]
        cur = [-1] * cols
        left = 0 if r == 0 else -1  # (0, 0) is reached "from nowhere" with 0 gold
        for c in range(cols):
            ch = line[c]
            if ch == rock:
                left = -1
                continue
            up = prev[c]
            best = up if up > left else left
            if best >= 0:
                left = best + ch - 48
                cur[c] = left
            else:
                left = -1
        prev = cur
    print(prev[cols - 1])


main()
