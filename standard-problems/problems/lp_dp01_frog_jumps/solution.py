# Python reference for lp_dp01_frog_jumps (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    h = list(map(int, data[2:2 + n]))
    dp = [0] * n
    for i in range(1, n):
        hi = h[i]
        best = -1
        for j in range(max(0, i - k), i):
            d = hi - h[j]
            c = dp[j] + (d if d >= 0 else -d)
            if best < 0 or c < best:
                best = c
        dp[i] = best
    print(dp[n - 1])


main()
