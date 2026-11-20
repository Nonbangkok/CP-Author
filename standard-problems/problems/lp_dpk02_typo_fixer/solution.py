# Python reference for lp_dpk02_typo_fixer (must pass under the judge's x4 time).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    a, b = data[0], data[1]
    ins, dele, rep = int(data[2]), int(data[3]), int(data[4])
    m = len(b)
    prev = [j * ins for j in range(m + 1)]
    for i in range(1, len(a) + 1):
        ai = a[i - 1]
        left = i * dele
        cur = [left]
        append = cur.append
        diag = prev[0]
        for j in range(1, m + 1):
            up = prev[j]
            best = diag if ai == b[j - 1] else diag + rep
            x = up + dele
            if x < best:
                best = x
            x = left + ins
            if x < best:
                best = x
            append(best)
            left = best
            diag = up
        prev = cur
    print(prev[m])


main()
