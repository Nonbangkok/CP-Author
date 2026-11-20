# Python reference for lp_str02_wallpaper: prefix function once, then O(1)
# per query from pi[L - 1].
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    s = data[2]
    pi = [0] * n
    k = 0
    for i in range(1, n):
        c = s[i]
        while k and c != s[k]:
            k = pi[k - 1]
        if c == s[k]:
            k += 1
        pi[i] = k
    out = []
    for token in data[3:3 + q]:
        length = int(token)
        p = length - pi[length - 1]
        if length % p == 0:
            out.append(f"{p} {length // p}")
        else:
            out.append(f"{p} 1")
    sys.stdout.write("\n".join(out) + "\n")


main()
