# Python reference for lp_mono01_warmer_days (must pass under the judge's x4 time).
# Independent of solution.cpp: scans right to left and keeps a stack of the
# "candidate" warmer days to the right (strictly increasing temperatures from
# top to bottom); the top after popping every day that is not warmer is the answer.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = list(map(int, data[1:1 + n]))
    d = [0] * n
    st = []
    for i in range(n - 1, -1, -1):
        ti = t[i]
        while st and t[st[-1]] <= ti:
            st.pop()
        if st:
            d[i] = st[-1] - i
        st.append(i)
    sys.stdout.write(" ".join(map(str, d)) + "\n")


main()
