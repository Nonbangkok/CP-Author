# Python reference for lp_rec02_permutations: backtracking over letter counts,
# letters tried in alphabetical order, so the output is sorted and duplicate-free.
import sys


def main() -> None:
    w = sys.stdin.readline().strip()
    n = len(w)
    letters = sorted(set(w))
    cnt = {c: w.count(c) for c in letters}
    cur = []
    out = []

    def gen() -> None:
        if len(cur) == n:
            out.append("".join(cur))
            return
        for c in letters:
            if cnt[c]:
                cnt[c] -= 1
                cur.append(c)
                gen()
                cur.pop()
                cnt[c] += 1

    gen()
    sys.stdout.write("\n".join(out) + "\n")


main()
