# Python reference for lp_str03_common_prefix: polynomial hashing mod 2^61 - 1
# with a random base, and a binary search on the common prefix length per query.
import random
import sys

MOD = (1 << 61) - 1


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    s = data[2]
    base = random.randrange(10**5, MOD - 1)
    h = [0] * (n + 1)
    pw = [1] * (n + 1)
    for i in range(n):
        h[i + 1] = (h[i] * base + s[i]) % MOD
        pw[i + 1] = pw[i] * base % MOD
    out = []
    pos = 3
    for _ in range(q):
        a = int(data[pos]) - 1
        b = int(data[pos + 1]) - 1
        pos += 2
        if a == b:
            out.append(n - a)
            continue
        lo, hi = 0, n - max(a, b)  # prefix of length lo matches; answer <= hi
        ha, hb = h[a], h[b]
        while lo < hi:
            m = (lo + hi + 1) >> 1
            p = pw[m]
            if (h[a + m] - ha * p) % MOD == (h[b + m] - hb * p) % MOD:
                lo = m
            else:
                hi = m - 1
        out.append(lo)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
