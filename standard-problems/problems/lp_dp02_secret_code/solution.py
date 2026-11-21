# Python reference for lp_dp02_secret_code (must pass under the judge's x4 time).
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    d = [c - 48 for c in data[2][:n]]
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        total = 0
        a = d[i - 1]
        if a != 0 and a <= m:
            total = dp[i - 1]
        if i >= 2:
            b = d[i - 2]
            if b != 0 and b * 10 + a <= m:
                total += dp[i - 2]
            if i >= 3:
                c = d[i - 3]
                if c != 0 and c * 100 + b * 10 + a <= m:
                    total += dp[i - 3]
        dp[i] = total % MOD
    print(dp[n])


main()
