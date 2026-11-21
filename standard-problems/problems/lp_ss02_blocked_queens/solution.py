# Python reference for lp_ss02_blocked_queens: row-by-row backtracking with
# bitmasks for used columns and both diagonal directions (depth N <= 12).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    full = (1 << n) - 1
    free = []
    for r in range(n):
        row = data[1 + r]
        mask = 0
        for c in range(n):
            if row[c] == 46:  # '.'
                mask |= 1 << c
        free.append(mask)

    def place(r: int, cols: int, left: int, right: int) -> int:
        if r == n:
            return 1
        total = 0
        avail = free[r] & ~(cols | left | right) & full
        while avail:
            bit = avail & -avail
            avail ^= bit
            total += place(r + 1, cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1)
        return total

    print(place(0, 0, 0, 0))


main()
