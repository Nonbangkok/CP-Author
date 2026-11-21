# Python reference for lp_bsx03_kth_root (must pass under the judge's x4 time).
# n <= 10^18 < 2^60, so the answer is below 2^(60 // k + 1): a small upper bound
# keeps mid ** k short even though Python integers never overflow.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    out = []
    for j in range(q):
        n, k = int(data[1 + 2 * j]), int(data[2 + 2 * j])
        lo, hi = 1, 1 << (60 // k + 1)  # lo ** k <= n, hi ** k > n
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid ** k <= n:
                lo = mid
            else:
                hi = mid
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
