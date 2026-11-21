# Python reference for lp_lazy01_coin_towers (must pass under the judge's x4 time).
# Independent of solution.cpp: no segment tree. The starting piles are a fixed
# prefix-sum array; the rain of coins goes into two Fenwick trees so that the
# coins added to piles 1..i equal  i * sum(B1, i) - sum(B2, i),
# where "+v on [l, r]" is  B1: +v at l, -v at r+1  and  B2: +v(l-1) at l, -vr at r+1.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    prefix = [0] * (n + 1)
    run = 0
    for i in range(n):
        run += int(data[2 + i])
        prefix[i + 1] = run
    b1 = [0] * (n + 2)
    b2 = [0] * (n + 2)
    limit = n + 1

    def added(i: int) -> int:
        s1 = s2 = 0
        j = i
        while j > 0:
            s1 += b1[j]
            s2 += b2[j]
            j &= j - 1
        return i * s1 - s2

    out = []
    pos = 2 + n
    for _ in range(q):
        l = int(data[pos + 1])
        r = int(data[pos + 2])
        if data[pos] == b"1":
            v = int(data[pos + 3])
            pos += 4
            j, d1, d2 = l, v, v * (l - 1)
            while j <= limit:
                b1[j] += d1
                b2[j] += d2
                j += j & -j
            j, d1, d2 = r + 1, -v, -v * r
            while j <= limit:
                b1[j] += d1
                b2[j] += d2
                j += j & -j
        else:
            pos += 3
            out.append(prefix[r] - prefix[l - 1] + added(r) - added(l - 1))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
