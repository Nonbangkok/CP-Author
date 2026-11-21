# Python reference for lp_mono02_billboard (must pass under the judge's x4 time).
# Independent of solution.cpp: two passes compute, for every building, the
# nearest strictly lower building on the left and on the right, then the
# building's full stretch width comes from prefix sums of the widths.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    w = list(map(int, data[1:1 + 2 * n:2]))
    h = list(map(int, data[2:2 + 2 * n:2]))
    x = [0] * (n + 1)
    for i in range(n):
        x[i + 1] = x[i] + w[i]
    left = [-1] * n
    st = []
    for i in range(n):
        hi = h[i]
        while st and h[st[-1]] >= hi:
            st.pop()
        left[i] = st[-1] if st else -1
        st.append(i)
    right = [n] * n
    st = []
    for i in range(n - 1, -1, -1):
        hi = h[i]
        while st and h[st[-1]] >= hi:
            st.pop()
        right[i] = st[-1] if st else n
        st.append(i)
    best = 0
    for i in range(n):
        area = h[i] * (x[right[i]] - x[left[i] + 1])
        if area > best:
            best = area
    print(best)


main()
