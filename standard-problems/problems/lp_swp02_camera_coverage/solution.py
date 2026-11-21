# Python reference for lp_swp02_camera_coverage (must pass under the judge's x4 time).
# Independent of solution.cpp: merges the sorted starts and sorted ends with two
# pointers instead of sorting tagged events; cur only changes at those points.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    starts = sorted(map(int, data[1:1 + 2 * n:2]))
    ends = sorted(map(int, data[2:2 + 2 * n:2]))
    exact = [0] * (n + 2)
    i = j = 0
    cur = 0
    prev = starts[0]
    while j < n:
        if i < n and starts[i] <= ends[j]:
            x = starts[i]
            exact[cur] += x - prev
            cur += 1
            i += 1
        else:
            x = ends[j]
            exact[cur] += x - prev
            cur -= 1
            j += 1
        prev = x
    out = [0] * n
    run = 0
    for k in range(n, 0, -1):
        run += exact[k]
        out[k - 1] = run
    sys.stdout.write(" ".join(map(str, out)) + "\n")


main()
