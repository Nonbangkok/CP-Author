# Python reference for lp_str01_chant_count: KMP over bytes (indexing bytes
# gives small ints, which compare fast).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t, p = data[0], data[1]
    n, m = len(t), len(p)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        c = p[i]
        while k and c != p[k]:
            k = pi[k - 1]
        if c == p[k]:
            k += 1
        pi[i] = k
    count = 0
    k = 0
    last = pi[m - 1]
    for c in t:
        while k and c != p[k]:
            k = pi[k - 1]
        if c == p[k]:
            k += 1
            if k == m:
                count += 1
                k = last
    print(count)


main()
